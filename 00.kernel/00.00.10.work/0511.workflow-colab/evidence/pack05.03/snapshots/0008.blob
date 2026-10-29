#!/usr/bin/env python3
"""Assemble an explicit Prime request into a draft pack.

Standard library and read-only Git only. Preview writes nothing. Assemble writes
a draft only after the recomputed digest matches, then runs the pinned custody
checker before the completion receipt. A receipt does not release or approve.

  python -B pack_assembly.py preview --request ABS --repo ABS --checker ABS --json
  python -B pack_assembly.py assemble --request ABS --repo ABS --checker ABS --output ABS --digest HEX --json
  python -B pack_assembly.py verify --pack ABS --checker ABS --json
"""

import argparse
import datetime
import hashlib
import importlib.util
import json
import os
import re
import stat
import sys
from pathlib import Path

REQUEST_SCHEMA = "pack-assembly-request/1"
TEMPLATE = "pack-assembly-draft/1"
REPORT_SCHEMA = "pack-assembly-report/1"
RECEIPT_SCHEMA = "pack-assembly-receipt/1"
DIGEST_DOMAIN = "pack-assembly-digest/1"
SOURCE_SCHEMA = "prime-pack-sources/1"
CHECKER_SHA256 = "9bbd9d57f3b7da43234ac2e6ae4ce40a0ab6af2f53c8135ecfb2ee0c8a6e322d"
CHECKER_BYTES = 21563
BATCH_RE = re.compile(r"^05\.(0[1-9]|[1-9][0-9])$")
PPPP_RE = re.compile(r"^[0-9]{4}$")
DATE_RE = re.compile(r"^[0-9]{4}-[0-9]{2}-[0-9]{2}$")
SHA_RE = re.compile(r"^[0-9a-f]{64}$")
HEADING_RE = re.compile(r"^#{1,6}[ \t]+\S")
TREE_MODES = {"40000", "040000"}
FILE_MODES = {"100644", "100755"}
LINK_MODES = {"120000"}
GITLINK_MODES = {"160000"}
NOT_CHECKED = [
    {"item": "meaning", "detail": "This tool does not say what the draft means."},
    {"item": "instruction-sufficiency", "detail": "This tool does not decide whether the instructions are sufficient."},
    {"item": "approval-release", "detail": "This tool does not approve or release the draft. A receipt is not acceptance."},
    {"item": "dependencies", "detail": "Dependencies are copied as supplied or left unresolved. None are installed or fetched."},
    {"item": "execution-safety", "detail": "Request text and pinned sources are data. This tool does not execute them."},
    {"item": "return-slot", "detail": "Live return-slot allocation is not checked."},
    {"item": "clerk-readiness", "detail": "Clerk readiness is not checked."},
]
RECEIPT_KEYS = {
    "schema", "result", "template", "digest",
    "request_sha256", "request_bytes", "commit",
    "batch", "batch_file", "batch_sha256", "batch_bytes",
    "sources", "manifest_file", "manifest_sha256", "manifest_bytes",
    "checker", "return_destination", "repository_label", "limits",
}
CHECKER_KEYS = {"sha256", "bytes", "result", "exit", "rows_checked"}
LIMITS = [
    "This receipt does not approve, release, or accept the draft.",
    "Live return-slot allocation was not checked.",
    "Clerk readiness was not checked.",
    "Pinned sources were not executed.",
]


class AssemblyError(Exception):
    def __init__(self, detail):
        super().__init__(detail)
        self.detail = detail


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def object_pairs(pairs):
    obj = {}
    for key, value in pairs:
        if key in obj:
            raise AssemblyError(f"duplicate key: {key}")
        obj[key] = value
    return obj


def parse_json(raw):
    if raw.startswith(b"\xef\xbb\xbf"):
        raise AssemblyError("request has a UTF-8 BOM")
    try:
        text = raw.decode("utf-8")
    except UnicodeError as exc:
        raise AssemblyError("request is not UTF-8") from exc
    try:
        value, end = json.JSONDecoder(object_pairs_hook=object_pairs).raw_decode(text)
    except AssemblyError:
        raise
    except json.JSONDecodeError as exc:
        raise AssemblyError(f"request is not strict json: {exc.msg}") from exc
    if text[end:].strip():
        raise AssemblyError("request has trailing data")
    if not isinstance(value, dict):
        raise AssemblyError("request is not an object")
    return value


def scan_text(value, label):
    """Reject a structural heading outside a fence. Quotes and fences stay data."""
    fenced = False
    for line in value.split("\n"):
        if line.endswith("\r"):
            line = line[:-1]
        probe = line.lstrip(" ")
        if probe.startswith("```"):
            fenced = not fenced
            continue
        if fenced or probe.startswith(">"):
            continue
        if HEADING_RE.match(probe):
            raise AssemblyError(f"{label} contains a structural heading")


def one_line(value, label):
    if not isinstance(value, str) or value == "":
        raise AssemblyError(f"{label} is empty")
    if value != value.strip() or any(ch in value for ch in "\r\n\0\t"):
        raise AssemblyError(f"{label} is not a single line")
    if any(ord(ch) < 32 for ch in value):
        raise AssemblyError(f"{label} contains a control character")
    scan_text(value, label)
    return value


def plain_line(value, label):
    value = one_line(value, label)
    if "#" in value:
        raise AssemblyError(f"{label} contains a heading marker")
    return value


def multi_line(value, label):
    if not isinstance(value, str) or value == "":
        raise AssemblyError(f"{label} is empty")
    if "\0" in value or any(ord(ch) < 32 and ch not in "\n\r\t" for ch in value):
        raise AssemblyError(f"{label} contains a control character")
    scan_text(value, label)
    return value


def require_fields(value, fields, label):
    if not isinstance(value, dict):
        raise AssemblyError(f"{label} is not an object")
    extra = sorted(set(value) - set(fields))
    missing = sorted(set(fields) - set(value))
    if extra or missing:
        raise AssemblyError(f"{label} fields are not {', '.join(fields)}")
    return value


def validate_dependencies(value):
    if not isinstance(value, dict) or "state" not in value:
        raise AssemblyError("dependencies are not explicit")
    state = value.get("state")
    if state == "unresolved":
        if set(value) != {"state"}:
            raise AssemblyError("unresolved dependencies take no invented items")
        return {"state": "unresolved"}
    if state == "supplied":
        require_fields(value, ("state", "items"), "dependencies")
        items = value["items"]
        if not isinstance(items, list) or not items:
            raise AssemblyError("supplied dependencies are empty")
        cleaned = []
        for item in items:
            require_fields(item, ("name", "detail"), "dependency")
            cleaned.append({
                "name": plain_line(item["name"], "dependency name"),
                "detail": plain_line(item["detail"], "dependency detail"),
            })
        return {"state": "supplied", "items": cleaned}
    raise AssemblyError("dependency state is not supplied or unresolved")


def validate_destination(value):
    if not isinstance(value, dict) or "state" not in value:
        raise AssemblyError("return destination is not explicit")
    state = value.get("state")
    if state == "unresolved":
        if set(value) != {"state"}:
            raise AssemblyError("unresolved return destination takes no invented path")
        return {"state": "unresolved"}
    if state == "supplied":
        require_fields(value, ("state", "path"), "return destination")
        return {"state": "supplied", "path": plain_line(value["path"], "return destination")}
    raise AssemblyError("return destination state is not supplied or unresolved")


def validate_request(document, module):
    fields = [
        "schema", "template", "title", "date", "author", "origin", "identity",
        "executor", "reviewer", "goal", "scope", "revision", "paths",
        "instructions", "evidence", "dependencies", "return_destination",
    ]
    extra = sorted(set(document) - set(fields) - {"repository_label"})
    missing = sorted(set(fields) - set(document))
    if extra:
        raise AssemblyError("unsupported request field: " + ", ".join(extra))
    if missing:
        raise AssemblyError("missing request field: " + ", ".join(missing))
    if document["schema"] != REQUEST_SCHEMA:
        raise AssemblyError("unsupported request schema")
    if document["template"] != TEMPLATE:
        raise AssemblyError("unsupported template")
    title = plain_line(document["title"], "title")
    date = plain_line(document["date"], "date")
    if not DATE_RE.fullmatch(date):
        raise AssemblyError("date is not YYYY-MM-DD")
    try:
        datetime.date.fromisoformat(date)
    except ValueError as exc:
        raise AssemblyError("date is not a calendar day") from exc
    author = plain_line(document["author"], "author")
    origin = require_fields(document["origin"], ("book", "page", "batch"), "origin")
    identity = require_fields(document["identity"], ("book", "pppp", "keyword", "batch"), "identity")
    pppp = plain_line(identity["pppp"], "pppp")
    if not PPPP_RE.fullmatch(pppp):
        raise AssemblyError("pppp is not four digits")
    batch = plain_line(identity["batch"], "batch")
    if not BATCH_RE.fullmatch(batch):
        raise AssemblyError("batch is not 05.NN")
    scope = document["scope"]
    if not isinstance(scope, list) or not scope:
        raise AssemblyError("scope is empty or not a list")
    revision = document["revision"]
    if not isinstance(revision, str) or revision == "":
        raise AssemblyError("revision is empty")
    paths = document["paths"]
    if not isinstance(paths, list) or not paths:
        raise AssemblyError("paths is empty or not a list")
    if len(paths) > 9999:
        raise AssemblyError("too many source paths")
    clean_paths = []
    for path in paths:
        if not isinstance(path, str):
            raise AssemblyError("source path is not a string")
        err = module.declared_path(path)
        if err:
            raise AssemblyError(f"source path: {err}")
        clean_paths.append(path)
    try:
        module.reject_aliases(clean_paths, "source path")
    except module.PackError as exc:
        raise AssemblyError(exc.detail) from exc
    instructions = document["instructions"]
    if not isinstance(instructions, list) or not instructions:
        raise AssemblyError("instructions are empty or not a list")
    cleaned = []
    for index, item in enumerate(instructions, start=1):
        require_fields(item, ("nn", "heading", "text"), "instruction")
        nn = item["nn"]
        if not isinstance(nn, str) or nn != f"{index:02d}":
            raise AssemblyError("instruction numbers are not 01..N in order")
        cleaned.append({
            "nn": nn,
            "heading": plain_line(item["heading"], "instruction heading"),
            "text": multi_line(item["text"], "instruction text"),
        })
    label = None
    if "repository_label" in document:
        label = plain_line(document["repository_label"], "repository label")
    return {
        "title": title,
        "date": date,
        "author": author,
        "origin": {
            "book": plain_line(origin["book"], "origin book"),
            "page": plain_line(origin["page"], "origin page"),
            "batch": plain_line(origin["batch"], "origin batch"),
        },
        "book": plain_line(identity["book"], "book"),
        "pppp": pppp,
        "keyword": plain_line(identity["keyword"], "keyword"),
        "batch": batch,
        "executor": plain_line(document["executor"], "executor"),
        "reviewer": plain_line(document["reviewer"], "reviewer"),
        "goal": multi_line(document["goal"], "goal"),
        "evidence": multi_line(document["evidence"], "evidence"),
        "scope": [plain_line(item, "scope") for item in scope],
        "revision": revision,
        "paths": clean_paths,
        "instructions": cleaned,
        "dependencies": validate_dependencies(document["dependencies"]),
        "return_destination": validate_destination(document["return_destination"]),
        "repository_label": label,
    }


def text_lines(value):
    parts = value.split("\n")
    if parts and parts[-1] == "":
        parts.pop()
    return parts


def render_draft(req, sources):
    """Fresh draft stamp. Historical approval stamps are not copied into it."""
    lines = [
        f"# 05 — {req['title']}",
        "version: 001",
        f"Authorization: draft — {req['date']}",
        f"who: {req['author']}",
        "state: draft",
        "Face: 05",
        f"PPPP: {req['pppp']}",
        f"book: {req['book']}",
        f"keyword: {req['keyword']}",
        "",
        "## Assignment",
        f"Executor: {req['executor']}",
        f"Reviewer: {req['reviewer']}",
        "Release: PENDING.",
        "Claim: PENDING.",
        f"Origin book: {req['origin']['book']}",
        f"Origin page: {req['origin']['page']}",
        f"Origin batch: {req['origin']['batch']}",
    ]
    destination = req["return_destination"]
    if destination["state"] == "supplied":
        lines.append(f"Return destination: {destination['path']}")
    else:
        lines.append("Return destination: unresolved")
    dependencies = req["dependencies"]
    if dependencies["state"] == "supplied":
        lines.append("Dependencies: supplied")
        for item in dependencies["items"]:
            lines.append(f"- {item['name']}: {item['detail']}")
    else:
        lines.append("Dependencies: unresolved")
    lines.extend([
        "Live return-slot allocation is not checked.",
        "Clerk readiness is not checked.",
        "This file is a draft. It does not certify release readiness.",
        "",
        "## Goal",
    ])
    lines.extend(text_lines(req["goal"]))
    lines.extend(["", "## Writable scope"])
    for item in req["scope"]:
        lines.append(f"- {item}")
    lines.extend(["", "## Evidence expected"])
    lines.extend(text_lines(req["evidence"]))
    lines.extend(["", "## Sources"])
    for source in sources:
        lines.append(f"- {source['path']} {source['sha256']} {source['bytes']} {source['snapshot']}")
    for item in req["instructions"]:
        lines.extend(["", f"## #{item['nn']} — {item['heading']}"])
        lines.extend(text_lines(item["text"]))
    lines.extend([
        "",
        f"## Return — {req['executor']}",
        "PENDING.",
        "",
        f"## Review — {req['reviewer']}",
        "PENDING.",
    ])
    return ("\n".join(lines) + "\n").encode("utf-8")


def render_manifest(commit, label, sources):
    # The commit and repository fields are labels. They do not fetch a remote.
    body = {"schema": SOURCE_SCHEMA, "commit": commit}
    if label is not None:
        body["repository"] = label
    body["sources"] = [
        {
            "path": source["path"],
            "sha256": source["sha256"],
            "bytes": source["bytes"],
            "snapshot": source["snapshot"],
        }
        for source in sources
    ]
    return (json.dumps(body, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def length_prefix(part):
    if isinstance(part, str):
        part = part.encode("utf-8")
    return len(part).to_bytes(8, "big") + part


def compute_digest(request_raw, commit, sources, planned):
    """Hash the plan. The completion receipt is not an input."""
    parts = [DIGEST_DOMAIN, TEMPLATE, request_raw, commit]
    for source in sources:
        parts.extend([source["path"], source["sha256"], str(source["bytes"])])
    for item in planned:
        parts.extend([item["path"], item["sha256"], str(item["bytes"])])
    digest = hashlib.sha256()
    for part in parts:
        digest.update(length_prefix(part))
    return digest.hexdigest()


def require_absolute(value, label):
    if not value or not os.path.isabs(value):
        raise AssemblyError(f"{label} must be an absolute path")


def extended(path):
    text = os.path.abspath(os.fspath(path))
    if os.name != "nt" or text.startswith("\\\\?\\"):
        return text
    if text.startswith("\\\\"):
        return "\\\\?\\UNC\\" + text[2:]
    return "\\\\?\\" + text


def is_linked(path):
    probe = Path(path)
    try:
        if probe.is_symlink():
            return True
    except OSError:
        return True
    try:
        if hasattr(probe, "is_junction") and probe.is_junction():
            return True
    except OSError:
        return True
    try:
        st = os.lstat(path)
    except OSError:
        return False
    return bool(getattr(st, "st_file_attributes", 0) & 0x400)


def kind_of(path):
    if is_linked(path):
        return "linked"
    try:
        st = os.lstat(path)
    except FileNotFoundError:
        return "missing"
    except OSError:
        return "unreadable"
    if stat.S_ISDIR(st.st_mode):
        return "dir"
    if stat.S_ISREG(st.st_mode):
        return "file"
    return "other"


def walk_chain(path):
    parts = Path(path).absolute().parts
    current = parts[0]
    kind = kind_of(current)
    if kind == "linked":
        raise AssemblyError("path is linked and was not followed")
    for part in parts[1:]:
        current = str(Path(current) / part)
        kind = kind_of(current)
        if kind == "linked":
            raise AssemblyError("path is linked and was not followed")
    return kind


def read_regular_file(path, label):
    require_absolute(path, label)
    if walk_chain(path) != "file":
        raise AssemblyError(f"{label} is not a file")
    try:
        return Path(extended(path)).read_bytes()
    except OSError as exc:
        raise AssemblyError(f"{label} could not be read: {exc.strerror or exc}") from exc


def load_checker(path):
    raw = read_regular_file(path, "checker")
    digest = sha256(raw)
    if digest != CHECKER_SHA256 or len(raw) != CHECKER_BYTES:
        raise AssemblyError("checker sha256 does not match the pin")
    spec = importlib.util.spec_from_file_location("pack_check_pinned", os.path.abspath(path))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module, digest, len(raw)


def read_object(module, repo, sha):
    result = module.git_run(repo, ["cat-file", "--batch"], (sha + "\n").encode("ascii"))
    if result.returncode:
        detail = result.stderr.decode("utf-8", "replace").strip()
        raise AssemblyError("git cat-file failed" + (f": {detail}" if detail else ""))
    data = result.stdout
    newline = data.find(b"\n")
    if newline < 0:
        raise AssemblyError("git cat-file returned a short response")
    head = data[:newline]
    if head.endswith(b" missing"):
        raise AssemblyError("git object is missing")
    try:
        _oid, kind, size_text = head.decode("ascii").split()
        size = int(size_text)
    except ValueError as exc:
        raise AssemblyError("git cat-file returned an unreadable header") from exc
    start = newline + 1
    payload = data[start:start + size]
    if len(payload) != size or data[start + size:start + size + 1] != b"\n":
        raise AssemblyError("git cat-file returned a short object")
    if start + size + 1 != len(data):
        raise AssemblyError("git cat-file returned trailing bytes")
    return kind, payload


def parse_tree(raw):
    entries = {}
    index = 0
    size = len(raw)
    while index < size:
        space = raw.find(b" ", index)
        nul = raw.find(b"\0", space if space >= 0 else index)
        if space < 0 or nul < 0 or nul + 21 > size:
            raise AssemblyError("git tree is truncated")
        mode = raw[index:space].decode("ascii")
        try:
            name = raw[space + 1:nul].decode("utf-8")
        except UnicodeError as exc:
            raise AssemblyError("git tree name is not UTF-8") from exc
        sha = raw[nul + 1:nul + 21].hex()
        if name in entries:
            raise AssemblyError(f"git tree repeats {name}")
        entries[name] = (mode, sha)
        index = nul + 21
    return entries


def blob_at_path(module, repo, commit, path):
    """Read one blob from tree objects. Do not follow a symlink, submodule, or worktree."""
    kind, payload = read_object(module, repo, commit)
    if kind != "commit":
        raise AssemblyError("resolved revision is not a commit object")
    first = payload.split(b"\n", 1)[0]
    if not first.startswith(b"tree ") or len(first) != 45:
        raise AssemblyError("commit has no tree")
    tree_sha = first[5:].decode("ascii")
    cache = {commit: (kind, payload)}
    parts = path.split("/")
    for depth, part in enumerate(parts):
        if tree_sha not in cache:
            cache[tree_sha] = read_object(module, repo, tree_sha)
        found_kind, found = cache[tree_sha]
        if found_kind != "tree":
            raise AssemblyError(f"{path} is not a file")
        entries = parse_tree(found)
        if part not in entries:
            raise AssemblyError(f"source blob is absent: {path}")
        mode, sha = entries[part]
        last = depth == len(parts) - 1
        if not last:
            if mode in LINK_MODES:
                raise AssemblyError(f"source is a symlink and was not followed: {path}")
            if mode in GITLINK_MODES:
                raise AssemblyError(f"source is a submodule and was not resolved: {path}")
            if mode not in TREE_MODES:
                raise AssemblyError(f"source path is not a directory: {path}")
            tree_sha = sha
            continue
        if mode in LINK_MODES:
            raise AssemblyError(f"source is a symlink and was not followed: {path}")
        if mode in GITLINK_MODES:
            raise AssemblyError(f"source is a submodule and was not resolved: {path}")
        if mode not in FILE_MODES:
            raise AssemblyError(f"source is not a file: {path}")
        blob_kind, blob = read_object(module, repo, sha)
        if blob_kind != "blob":
            raise AssemblyError(f"source object is not a blob: {path}")
        return blob
    raise AssemblyError(f"source blob is absent: {path}")


def load_sources(module, repo, revision, paths):
    try:
        commit = module.resolve_commit(repo, revision)
    except module.PackError as exc:
        raise AssemblyError(exc.detail) from exc
    sources = []
    for index, path in enumerate(paths, start=1):
        blob = blob_at_path(module, repo, commit, path)
        sources.append({
            "path": path,
            "sha256": sha256(blob),
            "bytes": len(blob),
            "snapshot": f"snapshots/{index:04d}.blob",
            "data": blob,
        })
    return commit, sources


def plan_outputs(request_raw, req, commit, sources):
    identities = [
        {
            "path": source["path"],
            "sha256": source["sha256"],
            "bytes": source["bytes"],
            "snapshot": source["snapshot"],
        }
        for source in sources
    ]
    files = [
        (f"{req['batch']}.md", render_draft(req, identities)),
        ("request.snapshot", request_raw),
        ("source-manifest.json", render_manifest(commit, req["repository_label"], identities)),
    ]
    for source in sources:
        files.append((source["snapshot"], source["data"]))
    planned = []
    for path, data in files:
        planned.append({"path": path, "sha256": sha256(data), "bytes": len(data), "data": data})
    digest = compute_digest(request_raw, commit, identities, planned)
    return identities, planned, digest


def prepare(request, repo, checker):
    module, checker_sha, checker_bytes = load_checker(checker)
    require_absolute(repo, "repo")
    if walk_chain(repo) != "dir":
        raise AssemblyError("repo is not a directory")
    request_raw = read_regular_file(request, "request")
    document = parse_json(request_raw)
    req = validate_request(document, module)
    commit, sources = load_sources(module, repo, req["revision"], req["paths"])
    identities, planned, digest = plan_outputs(request_raw, req, commit, sources)
    return {
        "module": module,
        "checker_sha256": checker_sha,
        "checker_bytes": checker_bytes,
        "request_raw": request_raw,
        "request": req,
        "commit": commit,
        "sources": identities,
        "planned": planned,
        "digest": digest,
    }


def inside(child, parent):
    child_norm = os.path.normcase(os.path.abspath(child))
    parent_norm = os.path.normcase(os.path.abspath(parent))
    if child_norm == parent_norm:
        return True
    prefix = parent_norm if parent_norm.endswith(os.sep) else parent_norm + os.sep
    return child_norm.startswith(prefix)


def repo_toplevel(module, repo):
    result = module.git_run(repo, ["rev-parse", "--show-toplevel"])
    if result.returncode:
        raise AssemblyError("repository is not a local git work tree")
    text = result.stdout.decode("utf-8", "replace").strip()
    if not text:
        raise AssemblyError("repository is not a local git work tree")
    return text


def inside_book(path):
    current = Path(path).absolute()
    if kind_of(current) == "missing":
        current = current.parent
    while True:
        kernel = current / "00.kernel"
        if kind_of(kernel) in ("dir", "linked"):
            return True
        parent = current.parent
        if parent == current:
            return False
        current = parent


def check_target(module, repo, output):
    require_absolute(output, "output")
    parent = str(Path(output).absolute().parent)
    if walk_chain(parent) != "dir":
        raise AssemblyError("output parent is not a directory")
    kind = walk_chain(output)
    if kind == "missing":
        pass
    elif kind == "dir":
        try:
            if any(Path(extended(output)).iterdir()):
                raise AssemblyError("output is not empty")
        except AssemblyError:
            raise
        except OSError as exc:
            raise AssemblyError(f"output could not be read: {exc.strerror or exc}") from exc
    else:
        raise AssemblyError("output is not an absent or empty directory")
    toplevel = repo_toplevel(module, repo)
    if inside(output, toplevel):
        raise AssemblyError("output is inside the source repository")
    if inside_book(output):
        raise AssemblyError("output is inside a book workspace")


def write_new(path, data):
    flags = os.O_CREAT | os.O_EXCL | os.O_WRONLY | getattr(os, "O_BINARY", 0)
    try:
        fd = os.open(path, flags)
    except FileExistsError as exc:
        raise AssemblyError(f"refusing to overwrite {path}") from exc
    try:
        view = memoryview(data)
        while view:
            written = os.write(fd, view)
            view = view[written:]
    finally:
        os.close(fd)


def write_planned(output, planned):
    target = Path(output)
    if not target.exists():
        os.mkdir(target)
    snapshots = target / "snapshots"
    os.mkdir(snapshots)
    for item in planned:
        dest = target.joinpath(*item["path"].split("/"))
        dest.parent.mkdir(exist_ok=True)
        write_new(dest, item["data"])


def run_checker(module, manifest):
    opts = argparse.Namespace(
        format=module.JSON_SCHEMA,
        manifest=str(manifest),
        root=None,
        git_repo=None,
        rev=None,
        json=False,
    )
    try:
        report, code = module.check(opts)
    except module.PackError as exc:
        raise AssemblyError(exc.detail) from exc
    return report, code


def receipt_bytes(prepared, checker_report, checker_code):
    req = prepared["request"]
    planned = {item["path"]: item for item in prepared["planned"]}
    batch_file = f"{req['batch']}.md"
    manifest = planned["source-manifest.json"]
    batch = planned[batch_file]
    body = {
        "schema": RECEIPT_SCHEMA,
        "result": "completed",
        "template": TEMPLATE,
        "digest": prepared["digest"],
        "request_sha256": sha256(prepared["request_raw"]),
        "request_bytes": len(prepared["request_raw"]),
        "commit": prepared["commit"],
        "batch": req["batch"],
        "batch_file": batch_file,
        "batch_sha256": batch["sha256"],
        "batch_bytes": batch["bytes"],
        "sources": prepared["sources"],
        "manifest_file": "source-manifest.json",
        "manifest_sha256": manifest["sha256"],
        "manifest_bytes": manifest["bytes"],
        "checker": {
            "sha256": prepared["checker_sha256"],
            "bytes": prepared["checker_bytes"],
            "result": checker_report.get("result"),
            "exit": checker_code,
            "rows_checked": checker_report.get("rows_checked"),
        },
        "return_destination": req["return_destination"],
        "repository_label": req["repository_label"],
        "limits": LIMITS,
    }
    return (json.dumps(body, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def public_planned(planned):
    return [{"path": item["path"], "sha256": item["sha256"], "bytes": item["bytes"]} for item in planned]


def report_for(command, result, prepared, findings, checker=None, target=None, receipt=None, supplied=None):
    if prepared is None:
        digest = commit = request_sha = None
        request_bytes = batch = None
        sources = planned = []
    else:
        digest = prepared["digest"]
        commit = prepared["commit"]
        request_sha = sha256(prepared["request_raw"])
        request_bytes = len(prepared["request_raw"])
        batch = prepared["request"]["batch"]
        sources = prepared["sources"]
        planned = public_planned(prepared["planned"])
    return {
        "schema": REPORT_SCHEMA,
        "command": command,
        "result": result,
        "digest": digest,
        "supplied_digest": supplied,
        "template": TEMPLATE,
        "commit": commit,
        "request_sha256": request_sha,
        "request_bytes": request_bytes,
        "batch": batch,
        "sources": sources,
        "planned": planned,
        "target": target,
        "checker": checker,
        "receipt": receipt,
        "findings": findings,
        "not_checked": NOT_CHECKED,
    }


def checker_summary(prepared, checker_report, checker_code):
    return {
        "sha256": prepared["checker_sha256"],
        "bytes": prepared["checker_bytes"],
        "result": checker_report.get("result") if checker_report else None,
        "exit": checker_code,
        "rows_checked": checker_report.get("rows_checked") if checker_report else None,
    }


def preview(request, repo, checker):
    try:
        prepared = prepare(request, repo, checker)
    except AssemblyError as exc:
        return report_for("preview", "invalid", None, [{"code": "invalid", "detail": exc.detail}]), 2
    return report_for("preview", "preview", prepared, []), 0


def assemble(request, repo, checker, output, supplied_digest, before_check=None):
    try:
        prepared = prepare(request, repo, checker)
    except AssemblyError as exc:
        return report_for("assemble", "invalid", None, [{"code": "invalid", "detail": exc.detail}], supplied=supplied_digest), 2
    if supplied_digest != prepared["digest"]:
        return report_for(
            "assemble", "invalid", prepared,
            [{"code": "digest-mismatch", "detail": "digest does not match the recomputed plan"}],
            supplied=supplied_digest,
        ), 2
    try:
        check_target(prepared["module"], repo, output)
    except AssemblyError as exc:
        return report_for(
            "assemble", "invalid", prepared,
            [{"code": "invalid", "detail": exc.detail}],
            supplied=supplied_digest,
        ), 2
    try:
        write_planned(output, prepared["planned"])
        # The CLI does not pass a hook. Tests use it to stop or corrupt before the receipt.
        if before_check is not None:
            before_check(Path(output))
        manifest = Path(output) / "source-manifest.json"
        checker_report, checker_code = run_checker(prepared["module"], manifest)
    except AssemblyError as exc:
        return report_for(
            "assemble", "partial", prepared,
            [{"code": "partial", "detail": exc.detail}],
            target=output, supplied=supplied_digest,
        ), 2
    summary = checker_summary(prepared, checker_report, checker_code)
    if checker_code != 0 or checker_report.get("result") != "pass":
        detail = "custody checker did not pass"
        if checker_report.get("findings"):
            detail = checker_report["findings"][0]["detail"]
        return report_for(
            "assemble", "partial", prepared,
            [{"code": "checker", "detail": detail}],
            checker=summary, target=output, supplied=supplied_digest,
        ), 1
    try:
        write_new(Path(output) / "completion-receipt.json", receipt_bytes(prepared, checker_report, checker_code))
    except AssemblyError as exc:
        return report_for(
            "assemble", "partial", prepared,
            [{"code": "partial", "detail": exc.detail}],
            checker=summary, target=output, supplied=supplied_digest,
        ), 2
    return report_for(
        "assemble", "completed", prepared, [],
        checker=summary, target=output, receipt="completion-receipt.json", supplied=supplied_digest,
    ), 0


def read_receipt(path):
    try:
        raw = Path(extended(path)).read_bytes()
    except OSError as exc:
        raise AssemblyError(f"receipt could not be read: {exc.strerror or exc}") from exc
    if raw.startswith(b"\xef\xbb\xbf"):
        raise AssemblyError("receipt has a UTF-8 BOM")
    try:
        text = raw.decode("utf-8")
    except UnicodeError as exc:
        raise AssemblyError("receipt is not UTF-8") from exc
    try:
        value, end = json.JSONDecoder(object_pairs_hook=object_pairs).raw_decode(text)
    except AssemblyError as exc:
        raise AssemblyError(f"receipt is not strict json: {exc.detail}") from exc
    except json.JSONDecodeError as exc:
        raise AssemblyError(f"receipt is not strict json: {exc.msg}") from exc
    if text[end:].strip():
        raise AssemblyError("receipt has trailing data")
    if not isinstance(value, dict):
        raise AssemblyError("receipt is not an object")
    return raw, value


def verify(pack, checker):
    try:
        module, checker_sha, checker_bytes = load_checker(checker)
        require_absolute(pack, "pack")
        if walk_chain(pack) != "dir":
            raise AssemblyError("pack is not a directory")
    except AssemblyError as exc:
        return report_for("verify", "invalid", None, [{"code": "invalid", "detail": exc.detail}]), 2
    receipt_path = Path(pack) / "completion-receipt.json"
    manifest_path = Path(pack) / "source-manifest.json"
    findings = []
    checker_report = None
    checker_code = None
    if kind_of(manifest_path) == "file":
        try:
            checker_report, checker_code = run_checker(module, manifest_path)
        except AssemblyError as exc:
            findings.append({"code": "checker", "detail": exc.detail})
    if not receipt_path.exists():
        findings.append({"code": "not-completed", "detail": "completion receipt is absent"})
        summary = None
        if checker_report is not None:
            summary = {
                "sha256": checker_sha,
                "bytes": checker_bytes,
                "result": checker_report.get("result"),
                "exit": checker_code,
                "rows_checked": checker_report.get("rows_checked"),
            }
        return report_for("verify", "partial", None, findings, checker=summary, target=pack), 1
    try:
        raw, receipt = read_receipt(receipt_path)
    except AssemblyError as exc:
        return report_for("verify", "mismatch", None, [{"code": "tamper", "detail": exc.detail}], target=pack), 1
    if set(receipt) != RECEIPT_KEYS or receipt.get("schema") != RECEIPT_SCHEMA:
        findings.append({"code": "tamper", "detail": "receipt fields are not the completion record"})
    else:
        compare_receipt(pack, receipt, findings)
        checker_body = receipt.get("checker")
        if not isinstance(checker_body, dict) or set(checker_body) != CHECKER_KEYS:
            findings.append({"code": "tamper", "detail": "receipt checker record is not the pinned result"})
        elif checker_body.get("sha256") != CHECKER_SHA256 or checker_body.get("bytes") != CHECKER_BYTES:
            findings.append({"code": "tamper", "detail": "receipt names a different checker"})
        elif checker_body.get("result") != "pass" or checker_body.get("exit") != 0:
            findings.append({"code": "tamper", "detail": "receipt does not record a passing check"})
    if checker_report is None or checker_code != 0 or checker_report.get("result") != "pass":
        detail = "custody checker did not pass"
        if checker_report and checker_report.get("findings"):
            detail = checker_report["findings"][0]["detail"]
        findings.append({"code": "checker", "detail": detail})
    # Reading the receipt again proves this path did not replace it.
    if Path(extended(receipt_path)).read_bytes() != raw:
        findings.append({"code": "tamper", "detail": "receipt changed while it was being read"})
    summary = {
        "sha256": checker_sha,
        "bytes": checker_bytes,
        "result": None if checker_report is None else checker_report.get("result"),
        "exit": checker_code,
        "rows_checked": None if checker_report is None else checker_report.get("rows_checked"),
    }
    if findings:
        return report_for("verify", "mismatch", None, findings, checker=summary, target=pack, receipt="completion-receipt.json"), 1
    return report_for("verify", "intact", None, [], checker=summary, target=pack, receipt="completion-receipt.json"), 0


def compare_receipt(pack, receipt, findings):
    root = Path(pack)
    expected = {
        receipt.get("batch_file"),
        "request.snapshot",
        "source-manifest.json",
        "completion-receipt.json",
    }
    present = {item.name for item in root.iterdir()}
    snapshots = root / "snapshots"
    if "snapshots" in present:
        present.remove("snapshots")
    if present != expected or kind_of(snapshots) != "dir":
        findings.append({"code": "tamper", "detail": "pack files are not the completed set"})
        return
    identities = [
        ("request.snapshot", receipt.get("request_sha256"), receipt.get("request_bytes")),
        (receipt.get("batch_file"), receipt.get("batch_sha256"), receipt.get("batch_bytes")),
        ("source-manifest.json", receipt.get("manifest_sha256"), receipt.get("manifest_bytes")),
    ]
    for name, digest, nbytes in identities:
        if not isinstance(name, str) or not isinstance(digest, str) or isinstance(nbytes, bool) or not isinstance(nbytes, int):
            findings.append({"code": "tamper", "detail": "receipt identity is not a hash and a length"})
            return
        file_path = root / name
        if kind_of(file_path) != "file":
            findings.append({"code": "tamper", "detail": f"{name} is missing"})
            return
        blob = Path(extended(file_path)).read_bytes()
        if sha256(blob) != digest or len(blob) != nbytes:
            findings.append({"code": "tamper", "detail": f"{name} differs from the receipt"})
    sources = receipt.get("sources")
    if not isinstance(sources, list) or not sources:
        findings.append({"code": "tamper", "detail": "receipt sources are empty"})
        return
    names = []
    for source in sources:
        if not isinstance(source, dict):
            findings.append({"code": "tamper", "detail": "receipt source is not an object"})
            return
        snapshot = source.get("snapshot")
        digest = source.get("sha256")
        nbytes = source.get("bytes")
        if not isinstance(snapshot, str) or not isinstance(digest, str) or isinstance(nbytes, bool) or not isinstance(nbytes, int):
            findings.append({"code": "tamper", "detail": "receipt source identity is incomplete"})
            return
        if not re.fullmatch(r"snapshots/[0-9]{4}\.blob", snapshot) or not SHA_RE.fullmatch(digest):
            findings.append({"code": "tamper", "detail": "receipt snapshot is not a flat numbered blob"})
            return
        blob_path = root.joinpath(*snapshot.split("/"))
        try:
            blob_path.relative_to(snapshots)
        except ValueError:
            findings.append({"code": "tamper", "detail": "receipt snapshot escapes the pack"})
            return
        if kind_of(blob_path) != "file":
            findings.append({"code": "tamper", "detail": f"{snapshot} is missing"})
            return
        blob = Path(extended(blob_path)).read_bytes()
        if sha256(blob) != digest or len(blob) != nbytes:
            findings.append({"code": "tamper", "detail": f"{snapshot} differs from the receipt"})
        names.append(snapshot)
    on_disk = sorted(item.name for item in snapshots.iterdir())
    if on_disk != sorted(Path(name).name for name in names):
        findings.append({"code": "tamper", "detail": "snapshot set differs from the receipt"})


def emit(report, as_json):
    if as_json:
        text = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    else:
        lines = [
            f"schema: {report['schema']}",
            f"command: {report['command']}",
            f"result: {report['result']}",
            f"digest: {report['digest']}",
            f"supplied_digest: {report['supplied_digest']}",
            f"template: {report['template']}",
            f"commit: {report['commit']}",
            f"request_sha256: {report['request_sha256']}",
            f"request_bytes: {report['request_bytes']}",
            f"batch: {report['batch']}",
            f"target: {report['target']}",
            f"receipt: {report['receipt']}",
        ]
        checker = report["checker"]
        if checker:
            lines.append(
                f"checker: {checker['result']} exit {checker['exit']} rows {checker['rows_checked']} sha256 {checker['sha256']}"
            )
        else:
            lines.append("checker: none")
        for item in report["planned"]:
            lines.append(f"planned {item['path']} {item['sha256']} {item['bytes']}")
        for source in report["sources"]:
            lines.append(f"source {source['path']} {source['sha256']} {source['bytes']} {source['snapshot']}")
        for finding in report["findings"]:
            lines.append(f"finding {finding['code']} {finding['detail']}")
        for item in report["not_checked"]:
            lines.append(f"not_checked {item['item']}: {item['detail']}")
        text = "\n".join(lines) + "\n"
    sys.stdout.buffer.write(text.encode("utf-8"))


def build_parser():
    parser = argparse.ArgumentParser(description="Assemble a draft pack from an explicit Prime request. Drafts only.")
    sub = parser.add_subparsers(dest="command", required=True)
    preview_parser = sub.add_parser("preview")
    assemble_parser = sub.add_parser("assemble")
    verify_parser = sub.add_parser("verify")
    for item in (preview_parser, assemble_parser, verify_parser):
        item.add_argument("--checker", required=True)
        item.add_argument("--json", action="store_true")
    for item in (preview_parser, assemble_parser):
        item.add_argument("--request", required=True)
        item.add_argument("--repo", required=True)
    assemble_parser.add_argument("--output", required=True)
    assemble_parser.add_argument("--digest", required=True)
    verify_parser.add_argument("--pack", required=True)
    return parser


def main(argv=None):
    parser = build_parser()
    opts = parser.parse_args(argv)
    try:
        if opts.command == "preview":
            report, code = preview(opts.request, opts.repo, opts.checker)
        elif opts.command == "assemble":
            report, code = assemble(opts.request, opts.repo, opts.checker, opts.output, opts.digest)
        else:
            report, code = verify(opts.pack, opts.checker)
    except AssemblyError as exc:
        report = report_for(opts.command, "invalid", None, [{"code": "invalid", "detail": exc.detail}])
        code = 2
    emit(report, opts.json)
    return code


if __name__ == "__main__":
    sys.exit(main())
