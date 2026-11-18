#!/usr/bin/env python3
"""Standalone consumer check for a colab-handoff/2 package.

The expected launch digest is the only trust anchor. Every claim this tool
reports is DERIVED from bytes that digest binds, by the fixed exchange-layout v2
rules; handoff.json is only compared against that derivation and never trusted.
Standard library only. It imports neither Colab producer and no workflow code.

  python -B handoff_check.py check --output ABS --expected-digest HEX --json
  python -B handoff_check.py copy  --output ABS --expected-digest HEX --to ABS --json

Contract: 00.kernel/00.00.10.work/0510.colab-tools/evidence/checker05.04/CONTRACT.md
Exit 0 valid/copied/already-copied; 1 mismatch/partial; 2 refused.
"""

import argparse
import hashlib
import io
import json
import os
import re
import stat
import sys
import unicodedata
import zipfile
from pathlib import Path

CHECK_SCHEMA = "colab-handoff-check/2"
HANDOFF_SCHEMA = "colab-handoff/2"
REQUEST_SCHEMA = "colab-request/2"
BINDING_SCHEMA = "colab-binding/1"
SOURCES_SCHEMA = "prime-pack-sources/1"
LAYOUT = "colab-exchange-layout/2"
DIGEST_DOMAIN = "colab-package-digest/2"
ASM_DOMAIN = "pack-assembly-digest/1"
ASM_TEMPLATE = "pack-assembly-draft/1"
HANDOFF_KEYS = {
    "schema", "layout", "digest", "digest_domain", "digest_preimage", "digest_rule", "investigation", "binding",
    "binding_sha256", "exchange", "not_created", "envelope", "source_map", "support_projection", "zip",
    "evaluator", "verify", "statements",
}
BOUND_KEYS = ("schema", "layout", "digest", "digest_domain", "digest_preimage", "investigation", "binding",
              "binding_sha256", "exchange", "not_created", "envelope", "source_map", "support_projection",
              "zip", "evaluator")
INFORMATIONAL_KEYS = ("verify", "statements", "digest_rule")
PAGE_RE = re.compile(r"^07(0[1-9]|[1-9][0-9])\.[a-z][a-z0-9-]*$")
PASS_RE = re.compile(r"^05\.(0[1-9]|[1-9][0-9])$")
HEX64 = re.compile(r"^[0-9a-f]{64}$")
SNAPSHOT_RE = re.compile(r"^snapshots/[0-9]{4}\.blob$")
MAX_JSON = 4 * 1024 * 1024
MAX_REQUEST = 262144
MAX_FILES = 4096
NOT_VERIFIED = [
    "rendered text of ENTRY, pack, notes, templates, SUPPORT.md and the assembler draft: bound by the digest, not re-rendered",
    "heading-section line ranges of targets",
    "assembler completion receipt content and the custody checker result: bound bytes, not re-run",
    "tool pins and v1 request rules beyond schema and binding shape",
    "use the pinned full producer verify (colab_support.py verify) for these",
]
CAPABILITY = ("Derives investigation, binding, exchange names and roles, source-to-snapshot map, support projection, "
              "ZIP membership, evaluator separation and the full digest preimage from digest-bound bytes by fixed "
              "v2 rules; recomputes the assembler and package digests. Does not re-render prose.")


class Refused(Exception):
    """Malformed, unsafe or unsupported input: exit 2."""

    def __init__(self, code, detail):
        super().__init__(detail)
        self.code = code
        self.detail = detail


class Mismatch(Exception):
    """A bound claim, byte or digest disagrees: exit 1."""

    def __init__(self, code, detail):
        super().__init__(detail)
        self.code = code
        self.detail = detail


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def canonical(value):
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")


# ---------------------------------------------------------------- strict input

def _pairs(pairs):
    obj = {}
    for key, value in pairs:
        if key in obj:
            raise Refused("duplicate-key", f"duplicate key: {key}")
        obj[key] = value
    return obj


def _nonfinite(name):
    raise Refused("nonfinite", f"non-finite number: {name}")


def strict_json(raw, label, limit=MAX_JSON):
    if len(raw) > limit:
        raise Refused("limit", f"{label} is larger than {limit} bytes")
    if raw.startswith(b"\xef\xbb\xbf"):
        raise Refused("bom", f"{label} has a UTF-8 BOM")
    try:
        text = raw.decode("utf-8")
        value = json.loads(text, object_pairs_hook=_pairs, parse_constant=_nonfinite)
    except UnicodeError as exc:
        raise Refused("encoding", f"{label} is not UTF-8") from exc
    except json.JSONDecodeError as exc:
        raise Refused("json", f"{label} is not strict json: {exc.msg}") from exc
    if not isinstance(value, dict):
        raise Refused("json", f"{label} is not an object")
    return value


def need(obj, key, kind, label):
    if not isinstance(obj, dict) or key not in obj:
        raise Refused("missing-key", f"{label} is missing {key}")
    value = obj[key]
    if kind is int:
        ok = isinstance(value, int) and not isinstance(value, bool)
    else:
        ok = isinstance(value, kind)
    if not ok:
        raise Refused("type", f"{label}.{key} has the wrong type")
    return value


def safe_rel(value, label):
    if not isinstance(value, str) or value == "":
        raise Refused("path", f"{label} is empty or not a string")
    if unicodedata.normalize("NFC", value) != value:
        raise Refused("path", f"{label} is not NFC")
    if any(ch in value for ch in "\\\0\r\n\t") or value.startswith("/") or re.match(r"^[A-Za-z]:", value) \
            or value.startswith("//"):
        raise Refused("path", f"{label} is absolute, UNC or has a forbidden character")
    for part in value.split("/"):
        if part in ("", ".", "..") or part.endswith(" ") or part.endswith(".") or ":" in part:
            raise Refused("path", f"{label} is not a canonical relative path")
    return value


# ---------------------------------------------------------------- safe filesystem

def is_linked(path):
    try:
        st = os.lstat(path)
    except FileNotFoundError:
        return False
    except OSError:
        return True
    if stat.S_ISLNK(st.st_mode):
        return True
    if getattr(st, "st_file_attributes", 0) & 0x400:  # reparse point, including junctions
        return True
    probe = Path(path)
    return bool(hasattr(probe, "is_junction") and probe.is_junction())


def check_ancestors(path, label):
    current = Path(os.path.abspath(path))
    for part in [current] + list(current.parents):
        if is_linked(part):
            raise Refused("linked", f"{label} has a linked ancestor: {part}")


def read_tree(root):
    """Every file under root as {posix rel: bytes}; refuse links and hard links."""
    files = {}
    count = 0
    for dirpath, dirnames, filenames in os.walk(root, followlinks=False):
        for name in list(dirnames):
            full = os.path.join(dirpath, name)
            if is_linked(full):
                raise Refused("linked", f"{os.path.relpath(full, root)} is linked")
        for name in filenames:
            full = os.path.join(dirpath, name)
            rel = Path(os.path.relpath(full, root)).as_posix()
            if is_linked(full):
                raise Refused("linked", f"{rel} is linked")
            st = os.lstat(full)
            if not stat.S_ISREG(st.st_mode):
                raise Refused("unexpected", f"{rel} is not a regular file")
            if st.st_nlink > 1:
                raise Refused("hardlink", f"{rel} has {st.st_nlink} hard links")
            count += 1
            if count > MAX_FILES * 2:
                raise Refused("limit", "too many files under the output")
            with open(full, "rb") as handle:
                files[rel] = handle.read()
    return files


# ---------------------------------------------------------------- derivation

def lp(part):
    if isinstance(part, str):
        part = part.encode("utf-8")
    return len(part).to_bytes(8, "big") + part


def names_for(pass_id):
    nn = pass_id[3:]
    return {
        "pass": pass_id, "nn": nn, "pack": f"{pass_id}.pack.md", "notes": f"06.{nn}.notes.md",
        "return_name": f"{pass_id}.return.md", "review_name": f"06.{nn}.review.md",
        "return_template": f"templates/{pass_id}.return.TEMPLATE.md",
        "review_template": f"templates/06.{nn}.review.TEMPLATE.md", "primary_instruction": f"{pass_id}.pack.md",
    }


def derive(tree):
    """Rebuild every consumer-relied claim from package bytes and fixed v2 rules."""
    for rel in tree:
        safe_rel(rel, "output path")
        if rel.endswith(".return.md") or rel.endswith(".review.md"):
            raise Mismatch("fabricated-exchange", f"{rel} exists; preparation never creates a return or review")
    package = {rel[len("package/"):]: data for rel, data in tree.items() if rel.startswith("package/")}
    if len(package) > MAX_FILES:
        raise Refused("limit", "too many package files")
    if "colab-request.json" not in package or "binding.json" not in package:
        raise Mismatch("missing", "package request or binding is missing")
    request = strict_json(package["colab-request.json"], "colab-request.json", MAX_REQUEST)
    if request.get("schema") != REQUEST_SCHEMA:
        raise Refused("version", f"request schema is {request.get('schema')!r}, not {REQUEST_SCHEMA}")
    binding = need(request, "binding", dict, "request")
    if package["binding.json"] != canonical(binding):
        raise Mismatch("binding", "binding.json is not the canonical binding of the bound request")
    if binding.get("schema") != BINDING_SCHEMA:
        raise Refused("version", "binding schema is not colab-binding/1")
    inv = need(binding, "investigation", dict, "binding")
    for key in ("book", "page", "pass"):
        need(inv, key, str, "investigation")
    if set(inv) != {"book", "page", "pass"}:
        raise Refused("binding", "investigation keys are not book, page, pass")
    if not PAGE_RE.fullmatch(inv["page"]) or not PASS_RE.fullmatch(inv["pass"]):
        raise Refused("binding", "investigation is not an N7NN page with a 05.NN pass")
    targets = need(binding, "targets", list, "binding")
    if not targets:
        raise Refused("binding", "binding has no targets")
    target_paths = []
    for t in targets:
        tid = need(t, "id", str, "target")
        src = need(t, "source", dict, f"target {tid}")
        for key in ("repository", "commit", "path", "sha256"):
            need(src, key, str, f"target {tid} source")
        safe_rel(src["path"], f"target {tid} path")
        if src["path"] not in target_paths:
            target_paths.append(src["path"])
    required = need(request, "required_sources", list, "request")
    required_paths = [safe_rel(need(r, "path", str, "required source"), "required source") for r in required]
    names = names_for(inv["pass"])

    manifest = strict_json(package.get("source-manifest.json", b""), "source-manifest.json")
    if manifest.get("schema") != SOURCES_SCHEMA:
        raise Mismatch("manifest", "source manifest schema is not prime-pack-sources/1")
    commit = need(manifest, "commit", str, "source manifest")
    repository = need(manifest, "repository", str, "source manifest")
    rows = need(manifest, "sources", list, "source manifest")
    if [need(r, "path", str, "source row") for r in rows] != target_paths + required_paths:
        raise Mismatch("source-map", "manifest paths are not the target paths followed by the required sources")
    snaps = []
    for index, row in enumerate(rows, start=1):
        snap = need(row, "snapshot", str, "source row")
        if snap != f"snapshots/{index:04d}.blob" or not SNAPSHOT_RE.fullmatch(snap):
            raise Mismatch("source-map", f"snapshot {snap} is out of order")
        data = package.get(snap)
        if data is None:
            raise Mismatch("missing", f"package/{snap} is missing")
        if sha256(data) != need(row, "sha256", str, "source row") or len(data) != need(row, "bytes", int, "source row"):
            raise Mismatch("snapshot", f"package/{snap} differs from its manifest row")
        snaps.append(snap)
    by_path = {r["path"]: r for r in rows}
    for t in targets:
        src = t["source"]
        if src["commit"] != commit or src["repository"] != repository:
            raise Mismatch("binding", f"target {t['id']} commit or repository differs from the manifest")
        if by_path[src["path"]]["sha256"] != src["sha256"]:
            raise Mismatch("snapshot", f"target {t['id']} sha256 differs from its snapshot")

    support = [(f"support/assembler/{inv['pass']}.md", f"{inv['pass']}.md"),
               ("support/assembler/request.snapshot", "request.snapshot"),
               ("support/assembler/completion-receipt.json", "completion-receipt.json")]
    asm_req = strict_json(package.get("support/assembler/request.snapshot", b""), "assembler request")
    want_origin = {"book": inv["book"], "page": inv["page"], "batch": inv["pass"]}
    want_identity = {"book": inv["book"], "pppp": inv["page"][:4], "keyword": inv["page"][5:], "batch": inv["pass"]}
    if (asm_req.get("origin") != want_origin or asm_req.get("identity") != want_identity
            or asm_req.get("revision") != commit or asm_req.get("paths") != target_paths + required_paths):
        raise Mismatch("assembler-request", "assembler request origin, identity, revision or paths differ from the binding")

    colab_order = ["ENTRY.md", names["pack"], names["notes"], names["return_template"], names["review_template"],
                   "binding.json", "colab-request.json", "support/SUPPORT.md"]
    expected_set = set(colab_order) | {"source-manifest.json"} | set(snaps) | {s for s, _ in support}
    missing = sorted(expected_set - set(package))
    extra = sorted(set(package) - expected_set)
    if missing:
        raise Mismatch("missing", "package is missing: " + ", ".join(missing))
    if extra:
        raise Mismatch("extra", "package has unknown files: " + ", ".join(extra))

    asm = hashlib.sha256()
    for part in (ASM_DOMAIN, ASM_TEMPLATE, package["support/assembler/request.snapshot"], commit):
        asm.update(lp(part))
    for row in rows:
        for part in (row["path"], row["sha256"], str(row["bytes"])):
            asm.update(lp(part))
    planned = [(f"{inv['pass']}.md", package[support[0][0]]), ("request.snapshot", package[support[1][0]]),
               ("source-manifest.json", package["source-manifest.json"])] + [(s, package[s]) for s in snaps]
    for name, data in planned:
        for part in (name, sha256(data), str(len(data))):
            asm.update(lp(part))
    asm_digest = asm.hexdigest()

    zip_bytes = tree.get("prepared-colab.zip")
    if zip_bytes is None:
        raise Mismatch("zip", "prepared-colab.zip is missing")
    try:
        with zipfile.ZipFile(io.BytesIO(zip_bytes)) as archive:
            infos = archive.infolist()
            seen = [info.filename for info in infos]
            if len(seen) != len(set(seen)):
                raise Mismatch("zip", "ZIP has duplicate entry names")
            for name in seen:
                safe_rel(name, "ZIP entry")
            members = {info.filename: archive.read(info) for info in infos}
    except zipfile.BadZipFile as exc:
        raise Mismatch("zip", f"ZIP is unreadable: {exc}") from exc
    if members != package:
        raise Mismatch("zip", "ZIP members differ from the package files")

    evaluator = []
    scoring = need(request, "scoring", dict, "request")
    ev_tree = {rel: data for rel, data in tree.items() if rel.startswith("evaluator/")}
    if scoring.get("state") == "scored" and scoring.get("blind") is True:
        ev_manifest_raw = ev_tree.get("evaluator/source-manifest.json")
        if ev_manifest_raw is None:
            raise Mismatch("evaluator", "evaluator/source-manifest.json is missing")
        ev_manifest = strict_json(ev_manifest_raw, "evaluator manifest")
        ev_rows = need(ev_manifest, "sources", list, "evaluator manifest")
        if [need(r, "path", str, "evaluator row") for r in ev_rows] != need(scoring, "evaluator_sources", list, "scoring"):
            raise Mismatch("evaluator", "evaluator manifest paths differ from the request")
        evaluator = [("evaluator/source-manifest.json", ev_manifest_raw)]
        candidate = {sha256(package[s]) for s in snaps}
        for index, row in enumerate(ev_rows, start=1):
            name = f"evaluator/snapshots/{index:04d}.blob"
            data = ev_tree.get(name)
            if data is None or row.get("snapshot") != f"snapshots/{index:04d}.blob":
                raise Mismatch("evaluator", f"{name} is missing or misnamed")
            if sha256(data) != row.get("sha256") or len(data) != row.get("bytes"):
                raise Mismatch("evaluator", f"{name} differs from its manifest row")
            if sha256(data) in candidate:
                raise Mismatch("evaluator", f"{name} has the same bytes as a candidate input")
            evaluator.append((name, data))
        if set(ev_tree) != {n for n, _ in evaluator}:
            raise Mismatch("evaluator", "evaluator/ has unknown files")
    elif ev_tree:
        raise Mismatch("evaluator", "evaluator/ exists but the request declares no blind method")

    preimage = [("text", DIGEST_DOMAIN), ("text", LAYOUT), ("file", "package/colab-request.json"),
                ("file", "package/binding.json"), ("text", asm_digest)]
    for name in colab_order:
        data = package[name]
        preimage += [("text", "package/" + name), ("text", sha256(data)), ("text", str(len(data)))]
    for name, data in evaluator:
        preimage += [("text", name), ("text", sha256(data)), ("text", str(len(data)))]
    for spath, aname in support:
        preimage += [("text", "package/" + spath), ("text", aname)]
    preimage += [("text", sha256(zip_bytes)), ("text", str(len(zip_bytes)))]
    digest = hashlib.sha256()
    file_parts = {"package/colab-request.json": package["colab-request.json"], "package/binding.json": package["binding.json"]}
    for kind, value in preimage:
        digest.update(lp(file_parts[value] if kind == "file" else value))

    role_of = {"ENTRY.md": "entry", names["pack"]: "pack-primary-instruction", names["notes"]: "notes",
               names["return_template"]: "template-return", names["review_template"]: "template-review",
               "binding.json": "binding", "colab-request.json": "request", "source-manifest.json": "source-manifest",
               "support/SUPPORT.md": "support-declaration"}
    support_names = {s for s, _ in support}
    envelope = [{"path": "package/" + n, "role": role_of.get(n) or ("snapshot" if n in snaps else
                 "support-assembler" if n in support_names else "unknown"),
                 "sha256": sha256(d), "bytes": len(d)} for n, d in sorted(package.items())]
    targets_by_path = {}
    for t in targets:
        targets_by_path.setdefault(t["source"]["path"], []).append(t["id"])
    source_map = [{"source_path": r["path"], "snapshot": "package/" + r["snapshot"], "sha256": r["sha256"],
                   "bytes": r["bytes"], "targets": targets_by_path.get(r["path"], []),
                   "role": "target" if r["path"] in targets_by_path else
                   ("required" if r["path"] in required_paths else "other")} for r in rows]
    return {
        "schema": HANDOFF_SCHEMA, "layout": LAYOUT, "digest": digest.hexdigest(), "digest_domain": DIGEST_DOMAIN,
        "digest_preimage": [{"kind": k, "value": v} for k, v in preimage],
        "investigation": inv, "binding": binding, "binding_sha256": sha256(package["binding.json"]),
        "exchange": names, "not_created": [names["return_name"], names["review_name"]], "envelope": envelope,
        "source_map": source_map,
        "support_projection": [{"support_path": "package/" + s, "assembler_name": a, "sha256": sha256(package[s]),
                                "bytes": len(package[s])} for s, a in support],
        "zip": {"path": "prepared-colab.zip", "sha256": sha256(zip_bytes), "bytes": len(zip_bytes),
                "members": sorted(package)},
        "evaluator": [{"path": n, "sha256": sha256(d), "bytes": len(d)} for n, d in evaluator],
    }, package


# ---------------------------------------------------------------- commands

def result(name, code, problems=(), **extra):
    body = {"schema": CHECK_SCHEMA, "result": name, "problems": list(problems), "capability": CAPABILITY,
            "not_verified": NOT_VERIFIED}
    body.update(extra)
    return body, code


def check(output, expected):
    try:
        if not isinstance(expected, str) or not HEX64.fullmatch(expected):
            raise Refused("digest", "expected digest is not 64 lowercase hex")
        if not isinstance(output, str) or not os.path.isabs(output):
            raise Refused("path", "output must be an absolute path")
        check_ancestors(output, "output")
        if not os.path.isdir(output):
            raise Refused("missing", "output is not a directory")
        tree = read_tree(output)
        if "handoff.json" not in tree:
            raise Refused("missing", "handoff.json is missing")
        handoff = strict_json(tree["handoff.json"], "handoff.json")
        if handoff.get("schema") != HANDOFF_SCHEMA:
            raise Refused("version", f"handoff schema is {handoff.get('schema')!r}, not {HANDOFF_SCHEMA}")
        extra_keys = sorted(set(handoff) - HANDOFF_KEYS)
        missing_keys = sorted(HANDOFF_KEYS - set(handoff))
        if extra_keys or missing_keys:
            raise Refused("handoff-keys", f"handoff keys differ: extra {extra_keys}, missing {missing_keys}")
        for part in need(handoff, "digest_preimage", list, "handoff"):
            if not isinstance(part, dict) or set(part) != {"kind", "value"} or not isinstance(part["value"], str):
                raise Refused("preimage", "a preimage part is not {kind, value}")
            if part["kind"] not in ("text", "file"):
                raise Refused("preimage", f"unsupported preimage part kind {part['kind']!r}")
        need(handoff, "verify", dict, "handoff")
        need(handoff, "statements", list, "handoff")
        need(handoff, "digest_rule", str, "handoff")
        derived, _package = derive({k: v for k, v in tree.items() if k != "handoff.json"})
    except Refused as exc:
        return result("refused", 2, [{"code": exc.code, "detail": exc.detail}])
    except Mismatch as exc:
        return result("mismatch", 1, [{"code": exc.code, "detail": exc.detail}])
    problems = []
    if derived["digest"] != expected:
        problems.append({"code": "digest", "detail": "digest derived from bound bytes is not the expected launch digest"})
    for key in BOUND_KEYS:
        if handoff.get(key) != derived[key]:
            problems.append({"code": "handoff-claim", "detail": f"handoff.{key} differs from the value derived from bound bytes"})
    if problems:
        return result("mismatch", 1, problems)
    trusted = {k: derived[k] for k in ("digest", "layout", "investigation", "exchange", "not_created",
                                       "source_map", "support_projection", "zip", "evaluator", "binding_sha256")}
    return result("valid", 0, trusted=trusted,
                  unbound_informational={k: handoff[k] for k in INFORMATIONAL_KEYS})


def copy(output, expected, to):
    body, code = check(output, expected)
    if code:
        return body, code
    trusted = body["trusted"]
    try:
        if not isinstance(to, str) or not os.path.isabs(to):
            raise Refused("path", "destination must be an absolute path")
        dest = Path(os.path.abspath(to))
        src = Path(os.path.abspath(output))
        if dest == src or src in dest.parents or dest in src.parents:
            raise Refused("destination", "destination overlaps the output")
        if not dest.parent.is_dir():
            raise Refused("destination", "destination parent is not a directory")
        check_ancestors(dest.parent, "destination")
        if is_linked(dest):
            raise Refused("linked", "destination is linked")
    except Refused as exc:
        return result("refused", 2, [{"code": exc.code, "detail": exc.detail}])
    package = {e["path"][len("package/"):]: e for e in trusted_envelope(output)}
    if dest.exists():
        try:
            existing = read_tree(str(dest))
        except Refused as exc:
            return result("refused", 2, [{"code": exc.code, "detail": exc.detail}])
        # A copy needs a fresh destination. A replay is read-only: it refuses and says what is there.
        same = set(existing) == set(package) and all(sha256(existing[n]) == package[n]["sha256"] for n in package)
        if same:
            return result("refused", 2, [{"code": "already-copied", "detail": "destination already holds an identical copy; nothing written"}],
                          written=[], retained=sorted(existing))
        return result("refused", 2, [{"code": "occupied", "detail": "destination exists and is not an identical copy; nothing is overwritten"}],
                      written=[], retained=sorted(existing))
    written = []
    try:
        dest.mkdir()
        for name in sorted(package):
            target = dest.joinpath(*name.split("/"))
            target.parent.mkdir(parents=True, exist_ok=True)
            data = (Path(output) / "package").joinpath(*name.split("/")).read_bytes()
            if sha256(data) != package[name]["sha256"]:
                raise Mismatch("source-changed", f"package/{name} changed after the check")
            fd = os.open(target, os.O_CREAT | os.O_EXCL | os.O_WRONLY | getattr(os, "O_BINARY", 0))
            try:
                view = memoryview(data)
                while view:
                    view = view[os.write(fd, view):]
            finally:
                os.close(fd)
            written.append(name)
        copied = read_tree(str(dest))
        if set(copied) != set(package) or any(sha256(copied[n]) != package[n]["sha256"] for n in package):
            raise Mismatch("copy", "the copy differs from the bound package")
    except (Mismatch, Refused, OSError) as exc:
        detail = getattr(exc, "detail", str(exc))
        return result("partial", 1, [{"code": getattr(exc, "code", "io"), "detail": detail}], written=written,
                      retained=written)
    after, code = check(output, expected)
    if code:
        return result("partial", 1, [{"code": "source-changed", "detail": "the source no longer checks after the copy"}],
                      written=written, retained=written)
    return result("copied", 0, trusted=trusted, written=written, retained=[])


def trusted_envelope(output):
    tree = read_tree(output)
    derived, _package = derive({k: v for k, v in tree.items() if k != "handoff.json"})
    return derived["envelope"]


def main(argv=None):
    parser = argparse.ArgumentParser(description="Validate or copy a colab-handoff/2 package from digest-bound bytes.")
    sub = parser.add_subparsers(dest="command", required=True)
    for name in ("check", "copy"):
        item = sub.add_parser(name)
        item.add_argument("--output", required=True)
        item.add_argument("--expected-digest", required=True)
        item.add_argument("--json", action="store_true", required=True)
        if name == "copy":
            item.add_argument("--to", required=True)
    opts = parser.parse_args(argv)
    try:
        if opts.command == "check":
            body, code = check(opts.output, opts.expected_digest)
        else:
            body, code = copy(opts.output, opts.expected_digest, opts.to)
    except (Refused, Mismatch) as exc:  # defensive: no traceback for expected failures
        body, code = result("refused", 2, [{"code": exc.code, "detail": exc.detail}])
    sys.stdout.write(json.dumps(body, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
    return code


if __name__ == "__main__":
    sys.exit(main())
