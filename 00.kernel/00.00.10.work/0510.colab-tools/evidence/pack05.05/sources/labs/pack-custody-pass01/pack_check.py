#!/usr/bin/env python3
"""Read-only check of declared pack snapshot bytes.

Standard library and the Git CLI only. This does not execute pinned sources,
fetch, check out, or change Git config. A clean result means only that the
declared snapshots match the declared hashes and lengths.

  python -B pack_check.py --format tsv --manifest PACK/source-manifest.tsv --root PACK/inputs
  python -B pack_check.py --format prime-pack-sources/1 --manifest PACK/source-manifest.json
  python -B pack_check.py --format tsv --git-repo REPO --rev REV --manifest source-manifest.tsv --root inputs
  python -B pack_check.py --format prime-pack-sources/1 --git-repo REPO --rev REV --manifest source-manifest.json
"""
import argparse
import hashlib
import json
import os
import posixpath
import re
import shutil
import stat
import subprocess
import sys
import unicodedata
from pathlib import Path

REPORT_SCHEMA = "pack-custody-report/1"
JSON_SCHEMA = "prime-pack-sources/1"
TSV_HEADER = "path\tsha256\tbytes"
SHA_RE = re.compile(r"^[0-9a-f]{64}$")
BYTES_RE = re.compile(r"^(0|[1-9][0-9]*)$")
COMMIT_RE = re.compile(r"^[0-9a-f]{40}$")
REPARSE = 0x400
NOT_CHECKED = [
    {"item": "meaning", "detail": "This check does not say what the bytes mean."},
    {"item": "instruction-sufficiency", "detail": "This check does not decide whether the pack's instructions are sufficient."},
    {"item": "approval-release", "detail": "This check does not approve or release the pack."},
    {"item": "dependencies", "detail": "This check does not resolve or install dependencies."},
    {"item": "execution-safety", "detail": "This check does not decide whether executing any supplied source is safe or appropriate. It does not run those sources."},
    {"item": "live-source", "detail": "Later worktree drift is not compared. An intact snapshot is not rewritten, and drift alone does not fail a historical blob."},
]


class PackError(Exception):
    def __init__(self, detail):
        super().__init__(detail)
        self.detail = detail


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def declared_path(value):
    """Return an error string when value is not already a canonical relative path."""
    if not isinstance(value, str) or value == "":
        return "path is empty"
    if unicodedata.normalize("NFC", value) != value:
        return "path is not Unicode NFC"
    if any(ch in value for ch in "\\\0\n\r\t"):
        return "path contains a forbidden character"
    if value.startswith("/") or re.match(r"^[A-Za-z]:", value):
        return "path is absolute"
    for part in value.split("/"):
        if part in ("", ".", ".."):
            return "path is not a canonical relative path"
        if part.endswith(" ") or part.endswith("."):
            return "path has a Windows alias"
        if ":" in part or any(ord(ch) < 32 for ch in part):
            return "path contains a control or stream marker"
    return None


def require_path(value, label):
    err = declared_path(value)
    if err:
        raise PackError(f"{label}: {err}")


def reject_aliases(values, label):
    seen = {}
    folded = {}
    for value in values:
        if value in seen:
            raise PackError(f"duplicate {label}: {value}")
        seen[value] = True
        key = value.casefold()
        if key in folded and folded[key] != value:
            raise PackError(f"ambiguous {label} alias: {folded[key]} and {value}")
        folded[key] = value


def parse_tsv(raw):
    if raw.startswith(b"\xef\xbb\xbf"):
        raise PackError("manifest has a UTF-8 BOM")
    try:
        text = raw.decode("utf-8")
    except UnicodeError as exc:
        raise PackError("manifest is not UTF-8") from exc
    lines = text.split("\n")
    if lines and lines[-1] == "":
        lines.pop()
    if not lines:
        raise PackError("manifest is empty")
    header = lines[0][:-1] if lines[0].endswith("\r") else lines[0]
    if header != TSV_HEADER:
        raise PackError("tsv header is not path<TAB>sha256<TAB>bytes")
    if len(lines) == 1:
        raise PackError("tsv has no source rows")
    rows = []
    for line in lines[1:]:
        body = line[:-1] if line.endswith("\r") else line
        parts = body.split("\t")
        if body == "" or len(parts) != 3:
            raise PackError("tsv row is not three fields")
        path, digest, nbytes = parts
        if not SHA_RE.fullmatch(digest):
            raise PackError(f"sha256 is not 64 lowercase hex: {path}")
        if not BYTES_RE.fullmatch(nbytes):
            raise PackError(f"byte length is not a nonnegative integer: {path}")
        rows.append({
            "path": path,
            "sha256": digest,
            "bytes": int(nbytes),
            "snapshot": path,
        })
    return rows, {"repository": None, "commit": None}


def object_pairs(pairs):
    obj = {}
    for key, value in pairs:
        if key in obj:
            raise PackError(f"duplicate key: {key}")
        obj[key] = value
    return obj


def parse_json(raw):
    if raw.startswith(b"\xef\xbb\xbf"):
        raise PackError("manifest has a UTF-8 BOM")
    try:
        text = raw.decode("utf-8")
    except UnicodeError as exc:
        raise PackError("manifest is not UTF-8") from exc
    try:
        value, end = json.JSONDecoder(object_pairs_hook=object_pairs).raw_decode(text)
    except PackError:
        raise
    except json.JSONDecodeError as exc:
        raise PackError(f"manifest is not strict json: {exc.msg}") from exc
    if text[end:].strip():
        raise PackError("manifest has trailing data")
    if not isinstance(value, dict):
        raise PackError("manifest is not an object")
    allowed = {"schema", "sources", "commit", "repository"}
    unknown = sorted(set(value) - allowed)
    if unknown:
        raise PackError("unsupported manifest field: " + ", ".join(unknown))
    if value.get("schema") != JSON_SCHEMA:
        raise PackError("unsupported schema")
    sources = value.get("sources")
    if not isinstance(sources, list) or not sources:
        raise PackError("sources is empty or not a list")
    provenance = {"repository": None, "commit": None}
    for label in ("repository", "commit"):
        if label in value:
            if not isinstance(value[label], str):
                raise PackError(f"{label} label is not a string")
            provenance[label] = value[label]
    rows = []
    source_keys = {"path", "sha256", "bytes", "snapshot"}
    for source in sources:
        if not isinstance(source, dict):
            raise PackError("source is not an object")
        extra = sorted(set(source) - source_keys)
        missing = sorted(source_keys - set(source))
        if extra or missing:
            raise PackError("source fields are not path, sha256, bytes, snapshot")
        path = source["path"]
        digest = source["sha256"]
        nbytes = source["bytes"]
        snapshot = source["snapshot"]
        if not isinstance(path, str) or not isinstance(snapshot, str) or not isinstance(digest, str):
            raise PackError("source path, snapshot, or sha256 is not a string")
        if not SHA_RE.fullmatch(digest):
            raise PackError(f"sha256 is not 64 lowercase hex: {path}")
        # bool is a subclass of int. A JSON true must not pass as a length.
        if isinstance(nbytes, bool) or not isinstance(nbytes, int) or nbytes < 0:
            raise PackError(f"byte length is not a nonnegative integer: {path}")
        rows.append({
            "path": path,
            "sha256": digest,
            "bytes": nbytes,
            "snapshot": snapshot,
        })
    return rows, provenance


def parse_manifest(fmt, raw):
    if fmt == "tsv":
        return parse_tsv(raw)
    if fmt == JSON_SCHEMA:
        return parse_json(raw)
    raise PackError("unsupported format")


def validate_rows(rows):
    for row in rows:
        require_path(row["path"], "path")
        require_path(row["snapshot"], "snapshot")
    reject_aliases([row["path"] for row in rows], "path")
    reject_aliases([row["snapshot"] for row in rows], "snapshot")


def as_extended(path):
    text = os.path.abspath(os.fspath(path))
    if os.name != "nt" or text.startswith("\\\\?\\"):
        return text
    if text.startswith("\\\\"):
        return "\\\\?\\UNC\\" + text[2:]
    return "\\\\?\\" + text


def component_kind(path):
    """Classify one path component without following a symlink or junction."""
    try:
        probe = Path(path)
        try:
            if probe.is_symlink():
                return "linked"
        except OSError:
            pass
        try:
            if hasattr(probe, "is_junction") and probe.is_junction():
                return "linked"
        except OSError:
            pass
        st = os.lstat(path)
    except FileNotFoundError:
        return "missing"
    except OSError:
        return "unreadable"
    if getattr(st, "st_file_attributes", 0) & REPARSE:
        return "linked"
    if stat.S_ISDIR(st.st_mode):
        return "dir"
    if stat.S_ISREG(st.st_mode):
        return "file"
    return "other"


def read_under(root, rel):
    current = as_extended(root)
    parts = rel.split("/")
    for index, part in enumerate(parts):
        current = current + ("\\" if os.name == "nt" else "/") + part
        kind = component_kind(current)
        last = index == len(parts) - 1
        if kind == "missing":
            return "missing", None
        if kind == "linked":
            return "linked", None
        if kind == "unreadable":
            return "unreadable", None
        if last:
            if kind != "file":
                return "not-a-file", None
        elif kind != "dir":
            return "not-a-file", None
    try:
        return "ok", Path(current).read_bytes()
    except PermissionError:
        return "unreadable", None
    except OSError:
        return "unreadable", None


def git_env():
    env = os.environ.copy()
    env["GIT_OPTIONAL_LOCKS"] = "0"
    env["GIT_TERMINAL_PROMPT"] = "0"
    return env


def git_program():
    # CreateProcess on Windows runs git.exe and skips a git.cmd earlier on PATH.
    # Resolve the name ourselves so the process PATH is the one that is used.
    found = shutil.which("git")
    if not found:
        raise PackError("git was not found")
    return found


def git_run(repo, args, input_bytes=None):
    program = git_program()
    tail = ["--no-optional-locks", "-C", str(repo), *args]
    # A git.cmd path is launched through two cmd.exe layers, and each treats
    # ^ as an escape. git.exe does not. Keep the revision peel intact either way.
    if program.lower().endswith((".cmd", ".bat")):
        tail = [item.replace("^", "^^^^") for item in tail]
    try:
        return subprocess.run([program, *tail], input=input_bytes, capture_output=True, env=git_env())
    except OSError as exc:
        raise PackError(f"git could not be started: {exc}") from exc


def resolve_commit(repo, rev):
    if not isinstance(rev, str) or rev == "" or rev.startswith("-") or any(ch in rev for ch in "\r\n\0 \t"):
        raise PackError("revision is not a single local revision")
    result = git_run(repo, ["rev-parse", "--verify", "--quiet", "--end-of-options", rev + "^{commit}"])
    if result.returncode:
        raise PackError("revision does not resolve to one local commit")
    text = result.stdout.decode("ascii", "replace").strip()
    if not COMMIT_RE.fullmatch(text):
        raise PackError("revision does not resolve to one commit")
    return text


def cat_batch(repo, specs):
    """Read blobs by stdin so a long path is not a command-line or worktree path."""
    payload = b"".join(spec.encode("utf-8") + b"\n" for spec in specs)
    result = git_run(repo, ["cat-file", "--batch"], payload)
    if result.returncode:
        detail = result.stderr.decode("utf-8", "replace").strip()
        raise PackError("git cat-file failed" + (f": {detail}" if detail else ""))
    data = result.stdout
    found = []
    cursor = 0
    for spec in specs:
        try:
            newline = data.index(b"\n", cursor)
        except ValueError as exc:
            raise PackError("git cat-file returned a short response") from exc
        head = data[cursor:newline]
        cursor = newline + 1
        if head.endswith(b" missing"):
            found.append(("missing", None))
            continue
        if head.endswith(b" ambiguous"):
            found.append(("ambiguous", None))
            continue
        try:
            _oid, kind, size_text = head.decode("ascii").split()
            size = int(size_text)
        except ValueError as exc:
            raise PackError("git cat-file returned an unreadable header") from exc
        blob = data[cursor:cursor + size]
        if len(blob) != size:
            raise PackError("git cat-file returned a short blob")
        cursor += size + 1
        if kind != "blob":
            found.append(("not-a-blob", kind))
            continue
        found.append(("ok", blob))
    if cursor != len(data):
        raise PackError("git cat-file returned trailing bytes")
    return found


def entry_result(row, location, status, blob):
    if status == "ok":
        actual_hash = sha256(blob)
        actual_len = len(blob)
        if actual_hash == row["sha256"] and actual_len == row["bytes"]:
            return {
                "path": row["path"],
                "snapshot": row["snapshot"],
                "location": location,
                "result": "match",
                "sha256": actual_hash,
                "bytes": actual_len,
                "detail": "snapshot bytes match",
            }
        return {
            "path": row["path"],
            "snapshot": row["snapshot"],
            "location": location,
            "result": "mismatch",
            "sha256": actual_hash,
            "bytes": actual_len,
            "detail": f"declared sha256 {row['sha256']} bytes {row['bytes']}; actual sha256 {actual_hash} bytes {actual_len}",
        }
    detail = {
        "missing": "snapshot is missing",
        "linked": "snapshot path is a symlink or junction and was not followed",
        "unreadable": "snapshot could not be read",
        "not-a-file": "snapshot is not a file",
        "ambiguous": "snapshot path is ambiguous",
        "not-a-blob": f"snapshot object is {blob}, not a blob",
    }[status]
    return {
        "path": row["path"],
        "snapshot": row["snapshot"],
        "location": location,
        "result": status,
        "sha256": None,
        "bytes": None,
        "detail": detail,
    }


def report_for(mode, fmt, manifest, digest, nbytes, commit, root, provenance, entries, invalid_detail):
    if invalid_detail is not None:
        result = "invalid"
        findings = [{"code": "invalid", "path": None, "detail": invalid_detail}]
        checked = 0
        entries = []
    else:
        findings = [
            {"code": item["result"], "path": item["path"], "detail": item["detail"]}
            for item in entries if item["result"] != "match"
        ]
        result = "findings" if findings else "pass"
        checked = len(entries)
    return {
        "schema": REPORT_SCHEMA,
        "result": result,
        "mode": mode,
        "format": fmt,
        "manifest": manifest,
        "manifest_sha256": digest,
        "manifest_bytes": nbytes,
        "commit": commit,
        "root": root,
        "provenance": provenance or {"repository": None, "commit": None},
        "rows_checked": checked,
        "entries": entries,
        "findings": findings,
        "not_checked": NOT_CHECKED,
    }


def emit(report, as_json):
    if as_json:
        text = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    else:
        lines = [
            f"schema: {report['schema']}",
            f"result: {report['result']}",
            f"mode: {report['mode']}",
            f"format: {report['format']}",
            f"manifest: {report['manifest']}",
            f"manifest_sha256: {report['manifest_sha256']}",
            f"manifest_bytes: {report['manifest_bytes']}",
            f"commit: {report['commit']}",
            f"root: {report['root']}",
            f"provenance_repository: {report['provenance']['repository']}",
            f"provenance_commit: {report['provenance']['commit']}",
            f"rows_checked: {report['rows_checked']}",
        ]
        for item in report["entries"]:
            lines.append(
                f"entry {item['result']} {item['path']} snapshot {item['snapshot']} location {item['location']} {item['detail']}"
            )
        for finding in report["findings"]:
            lines.append(f"finding {finding['code']} {finding['detail']}")
        for item in report["not_checked"]:
            lines.append(f"not_checked {item['item']}: {item['detail']}")
        text = "\n".join(lines) + "\n"
    sys.stdout.buffer.write(text.encode("utf-8"))


def mode_of(opts):
    git_bits = (opts.git_repo, opts.rev)
    if any(git_bits) and not all(git_bits):
        raise PackError("git mode needs both --git-repo and --rev")
    if opts.format == "tsv" and not opts.root:
        raise PackError("tsv mode needs --root")
    if opts.format == JSON_SCHEMA and opts.root:
        raise PackError("json snapshots resolve from the manifest directory; do not pass --root")
    if all(git_bits):
        return "git"
    return "filesystem"


def check(opts):
    fmt = opts.format
    as_manifest = opts.manifest
    provenance = {"repository": None, "commit": None}
    try:
        mode = mode_of(opts)
    except PackError as exc:
        return report_for(None, fmt, as_manifest, None, None, None, opts.root, provenance, [], exc.detail), 2
    commit = None
    root_display = opts.root
    digest = None
    nbytes = None
    try:
        if mode == "git":
            require_path(opts.manifest, "manifest")
            if fmt == "tsv":
                require_path(opts.root, "root")
            commit = resolve_commit(opts.git_repo, opts.rev)
            raw_status = cat_batch(opts.git_repo, [f"{commit}:{opts.manifest}"])[0]
            if raw_status[0] != "ok":
                raise PackError(f"manifest blob is {raw_status[0]}")
            raw = raw_status[1]
        else:
            try:
                raw = Path(as_extended(opts.manifest)).read_bytes()
            except OSError as exc:
                raise PackError(f"manifest could not be read: {exc.strerror or exc}") from exc
        digest = sha256(raw)
        nbytes = len(raw)
        if mode == "filesystem" and fmt == "tsv" and component_kind(as_extended(opts.root)) != "dir":
            raise PackError("snapshot root is not a directory")
        rows, provenance = parse_manifest(fmt, raw)
        validate_rows(rows)
    except PackError as exc:
        return report_for(mode, fmt, as_manifest, digest, nbytes, commit, root_display, provenance, [], exc.detail), 2

    entries = []
    if mode == "filesystem":
        base = Path(opts.root) if fmt == "tsv" else Path(opts.manifest).parent
        root_display = str(base)
        for row in rows:
            status, blob = read_under(base, row["snapshot"])
            entries.append(entry_result(row, row["snapshot"], status, blob))
    else:
        if fmt == "tsv":
            locations = [posixpath.join(opts.root, row["snapshot"]) for row in rows]
            root_display = opts.root
        else:
            prefix = posixpath.dirname(opts.manifest)
            locations = [posixpath.join(prefix, row["snapshot"]) if prefix else row["snapshot"] for row in rows]
            root_display = prefix or "."
        for location in locations:
            require_path(location, "snapshot location")
        specs = [f"{commit}:{location}" for location in locations]
        try:
            blobs = cat_batch(opts.git_repo, specs)
        except PackError as exc:
            return report_for(mode, fmt, as_manifest, digest, nbytes, commit, root_display, provenance, [], exc.detail), 2
        if len(blobs) != len(rows):
            return report_for(mode, fmt, as_manifest, digest, nbytes, commit, root_display, provenance, [], "git cat-file returned the wrong number of objects"), 2
        for row, location, (status, blob) in zip(rows, locations, blobs):
            entries.append(entry_result(row, location, status, blob))
    code = 0 if entries and all(item["result"] == "match" for item in entries) else 1
    return report_for(mode, fmt, as_manifest, digest, nbytes, commit, root_display, provenance, entries, None), code


def build_parser():
    parser = argparse.ArgumentParser(description="Check declared pack snapshot bytes. Read-only.")
    parser.add_argument("--format", required=True, choices=("tsv", JSON_SCHEMA))
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--root", help="Snapshot root. Required for tsv. Not used for JSON.")
    parser.add_argument("--git-repo", help="Local repository. With --rev, read blobs at that commit.")
    parser.add_argument("--rev", help="Revision resolved once to a commit. Not fetched.")
    parser.add_argument("--json", action="store_true", help="Write pack-custody-report/1 to stdout.")
    return parser


def main(argv=None):
    parser = build_parser()
    opts = parser.parse_args(argv)
    try:
        report, code = check(opts)
    except PackError as exc:
        report = report_for(None, opts.format, opts.manifest, None, None, None, opts.root, None, [], exc.detail)
        code = 2
    emit(report, opts.json)
    return code


if __name__ == "__main__":
    sys.exit(main())
