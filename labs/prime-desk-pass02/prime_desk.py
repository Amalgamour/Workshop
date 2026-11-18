#!/usr/bin/env python3
"""Read-only Prime desk view. Current work comes from the assignment record.

The request names every source. This tool does not crawl a repository, call Git,
launch a worker, or write a source record. A legacy selector is a hint.
A hash match proves bytes only.
"""

from __future__ import annotations

import hashlib
import importlib.util
import io
import json
import os
import re
import stat
import sys
from datetime import datetime, timezone

sys.dont_write_bytecode = True
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"

SCHEMA = "prime-desk-request/2"
VIEW_SCHEMA = "prime-desk-view/2"
PACKET_SCHEMA = "prime-desk-packet/2"
SELECTOR_SCHEMA = "prime-desk-selector/1"
CATALOG_SCHEMA = "prime-desk-catalog/2"
EVIDENCE_SCHEMA = "prime-desk-worker-evidence/1"
RULE = "assignment-record/v1"
COVERAGE = "Declared request paths only. Unregistered sources were not searched."
COVERAGE_TOKEN = "declared-paths"
ESCALATION = (
    "Escalation: Codex Prime on 0524.prime-desk/05.02. "
    "This tool does not decide meaning, acceptance, or live authority."
)
QUOTE_MAX = 12000
LABEL_MAX = 200
SUPPLIED_MAX = 500
REPARSE = 0x400
PAGE_RE = re.compile(
    r"^(\d{4})\.([A-Za-z0-9][A-Za-z0-9._-]*)/(05\.\d{2}|06\.\d{2}\.review)\.md$"
)

DESK_ROLES = {"goal", "scope", "authority", "dependency", "talk", "assignment", "other"}
WORK_ROLES = {
    "criteria", "checkpoint", "return", "receipt", "deliverable",
    "verification", "finding", "next",
}
ROLES = DESK_ROLES | WORK_ROLES
ATTENTION_KINDS = {
    "director-question", "return-awaiting-review", "observer-finding", "conflict",
    "missing-evidence", "interrupted", "hold",
}
WORKER_STATES = {"released", "claimed", "returned", "awaiting-review"}
AUTHORS = {"director", "model"}
READERS = {
    "desk-state": (
        "labs/desk-state-pass01/desk_state.py",
        "4d924bf6549fe37b229962d4f3a81924109a879a8206ea95066f4bfde11701b4",
        55144,
    ),
    "prime-brief": (
        "labs/prime-brief-pass01/prime_brief.py",
        "302ed832d2fa955a591420f13d3b22ce91e4a7669c69a778d443fc82627580d7",
        22747,
    ),
    "state-projection": (
        "labs/state-projection-pass01/state_projection.py",
        "b349da5cef5178296a069c354002a600ba4e168c2710aa5d87789724d4951ecb",
        20338,
    ),
    "prime-support": (
        "labs/prime-support-pass01/prime_support.py",
        "700d60d2e49c186d49e56a9a38058e21a722b4a5dd79d461453a305e8d904f70",
        59791,
    ),
    "app-context": (
        "app/context.py",
        "5b1a31d47bb9f9b465a8492541467abbd9bd3a99ae524be7aa0dbffe2380eb9f",
        22063,
    ),
}
TOP_KEYS = {
    "schema", "instance", "workspace", "assignment", "legacy_selector", "coverage",
    "references", "work", "workers", "supplied", "attention", "history", "catalog",
    "operations", "legacy", "foreign", "attribution",
}
RESULT_KEYS = [
    "schema", "command", "state", "exit", "check", "correction", "observed_at",
    "coverage", "instance", "selected", "not_selected", "catalog", "attention",
    "gaps", "workers", "operations", "record", "inspectability", "legacy",
    "foreign", "packet",
]
TASK_ROLES = ("criteria", "checkpoint", "return", "receipt", "deliverable", "verification", "finding", "next")


class Problem(Exception):
    def __init__(self, check: str, message: str) -> None:
        super().__init__(message)
        self.check = check
        self.message = message


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def loads(data: bytes, check: str):
    def reject(name: str):
        raise Problem(check, f"nonfinite JSON {name}")

    def pairs(seq):
        obj = {}
        for key, value in seq:
            if key in obj:
                raise Problem(check, f"duplicate JSON key {key}")
            obj[key] = value
        return obj

    if data.startswith(b"\xef\xbb\xbf"):
        raise Problem(check, "JSON has a BOM")
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise Problem(check, "JSON is not UTF-8") from exc
    try:
        return json.loads(text, object_pairs_hook=pairs, parse_constant=reject)
    except Problem:
        raise
    except json.JSONDecodeError as exc:
        raise Problem(check, f"JSON is not usable ({exc.msg})") from exc


def exact(obj, keys: set[str], check: str) -> None:
    if not isinstance(obj, dict) or set(obj) != keys:
        raise Problem(check, f"exact keys required: {', '.join(sorted(keys))}")


def is_sha(value) -> bool:
    return isinstance(value, str) and len(value) == 64 and all(c in "0123456789abcdef" for c in value)


def is_int(value) -> bool:
    return type(value) is int and value >= 0


def is_label(value, limit: int = 64) -> bool:
    if not isinstance(value, str) or not value or len(value) > limit:
        return False
    return value[0].isalnum() and all(c.isalnum() or c in "._-" for c in value)


def short_text(value, limit: int, check: str) -> str:
    if not isinstance(value, str) or not value.strip() or len(value) > limit:
        raise Problem(check, f"text must be 1..{limit} characters")
    return value


def relative_path(value, check: str) -> str:
    if not isinstance(value, str) or not value or "\\" in value:
        raise Problem(check, "path must be a relative forward-slash path")
    if value.startswith("/") or (len(value) >= 2 and value[1] == ":"):
        raise Problem(check, "path must stay inside the declared root")
    parts = value.split("/")
    if any(part in ("", ".", "..") for part in parts):
        raise Problem(check, "path must stay inside the declared root")
    return value


def absolute_dir(value, check: str) -> str:
    if not isinstance(value, str) or not os.path.isabs(value) or value.startswith("\\\\"):
        raise Problem(check, "directory must be an absolute path")
    if not os.path.lexists(value):
        raise Problem(check, "directory is missing")
    if is_reparse(value) or not os.path.isdir(value):
        raise Problem(check, "directory is not a regular directory")
    return os.path.abspath(value)


def is_reparse(path: str) -> bool:
    try:
        info = os.lstat(path)
    except OSError:
        return True
    attrs = getattr(info, "st_file_attributes", 0) or 0
    return bool(attrs & REPARSE) or stat.S_ISLNK(info.st_mode)


def inside(root: str, path: str) -> bool:
    root_n = os.path.normcase(os.path.abspath(root))
    path_n = os.path.normcase(os.path.abspath(path))
    try:
        return os.path.commonpath([root_n, path_n]) == root_n
    except ValueError:
        return False


def dump(obj: dict) -> bytes:
    text = json.dumps(obj, ensure_ascii=False, sort_keys=True, indent=2, allow_nan=False)
    return (text + "\n").encode("utf-8")


def now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def empty_coverage() -> dict:
    return {
        "statement": COVERAGE,
        "declared": 0,
        "matched": 0,
        "missing": 0,
        "stale": 0,
        "changed": 0,
        "outside": 0,
        "unreadable": 0,
    }


def blank(command: str, observed: str, check: str, correction: str, exit_code: int, state: str) -> dict:
    return {
        "schema": VIEW_SCHEMA if command != "packet" else PACKET_SCHEMA,
        "command": command,
        "state": state,
        "exit": exit_code,
        "check": check,
        "correction": correction,
        "observed_at": observed,
        "coverage": empty_coverage(),
        "instance": None,
        "selected": None,
        "not_selected": [],
        "catalog": None,
        "attention": [],
        "gaps": [],
        "workers": [],
        "operations": [],
        "record": {"references": [], "history": [], "history_inlined": False, "talk_parsed": False, "assignment_reader": [], "attribution": []},
        "inspectability": {
            "request_sha256": None,
            "fingerprint": None,
            "basis_legend": "observed = declared bytes matched; supplied = caller label; unknown = not present; stale = different bytes withheld; changed = bytes moved during the read and were withheld",
            "escalation": ESCALATION,
        },
        "legacy": [],
        "foreign": [],
        "packet": None,
    }


def refuse(command: str, observed: str, check: str, message: str) -> dict:
    text = message if message.endswith(ESCALATION) else message + " " + ESCALATION
    return blank(command, observed, check, text, 2, "refused")


def read_twice(path: str) -> tuple[str, bytes | None, bytes | None]:
    if not os.path.lexists(path):
        return "missing", None, None
    if is_reparse(path):
        return "unreadable", None, None
    info = os.lstat(path)
    if not stat.S_ISREG(info.st_mode):
        return "unreadable", None, None
    try:
        with open(path, "rb") as handle:
            first = handle.read()
        with open(path, "rb") as handle:
            second = handle.read()
    except OSError:
        return "unreadable", None, None
    if first != second:
        return "changed", first, second
    return "bytes", first, second


class Book:
    def __init__(self, root: str, tools_root: str) -> None:
        self.root = root
        self.tools_root = tools_root
        self.coverage = empty_coverage()
        self.accepted: list[tuple[str, str, int]] = []
        self.gaps: list[dict] = []
        self.cache: dict[tuple[str, str, str, int], dict] = {}

    def add_gap(self, kind: str, check: str, message: str, path: str | None, basis: str) -> None:
        self.gaps.append({
            "kind": kind,
            "check": check,
            "message": message,
            "path": path,
            "basis": basis,
        })

    def take(self, base: str, rel: str, expect_sha: str, expect_bytes: int, label: str) -> dict:
        key = (base, rel, expect_sha, expect_bytes)
        if key in self.cache:
            return self.cache[key]
        self.coverage["declared"] += 1
        row = {
            "label": label,
            "path": rel,
            "status": "outside",
            "basis": "unknown",
            "sha256": None,
            "bytes": None,
            "data": None,
        }
        try:
            relative_path(rel, label)
        except Problem as exc:
            self.coverage["outside"] += 1
            self.add_gap("outside-path", label, exc.message, rel, "unknown")
            self.cache[key] = row
            return row
        if not is_sha(expect_sha) or not is_int(expect_bytes):
            raise Problem(label, "sha256 must be 64 lowercase hex and bytes must be a non-negative integer")
        full = os.path.abspath(os.path.join(base, *rel.split("/")))
        if not inside(base, full):
            self.coverage["outside"] += 1
            self.add_gap("outside-path", label, "path leaves the declared root", rel, "unknown")
            self.cache[key] = row
            return row
        status, first, _second = read_twice(full)
        if status == "missing":
            self.coverage["missing"] += 1
            row["status"] = "missing"
            self.add_gap("missing", label, "declared file is absent", rel, "unknown")
        elif status == "unreadable":
            self.coverage["unreadable"] += 1
            row["status"] = "unreadable"
            self.add_gap("unreadable", label, "path is not a regular file", rel, "unknown")
        elif status == "changed":
            self.coverage["changed"] += 1
            row["status"] = "changed"
            row["basis"] = "changed"
            row["sha256"] = sha256_bytes(first or b"")
            row["bytes"] = len(first or b"")
            self.add_gap(
                "changed",
                label,
                "bytes changed during the read; withheld. Rerun after the file is stable. This tool does not refresh onto the new bytes.",
                rel,
                "changed",
            )
        else:
            digest = sha256_bytes(first or b"")
            length = len(first or b"")
            if digest != expect_sha or length != expect_bytes:
                self.coverage["stale"] += 1
                row["status"] = "stale"
                row["basis"] = "stale"
                row["sha256"] = digest
                row["bytes"] = length
                self.add_gap(
                    "stale",
                    label,
                    "bytes differ from the request. Update the request hash in a new request. This run does not use the new bytes.",
                    rel,
                    "stale",
                )
            else:
                self.coverage["matched"] += 1
                self.accepted.append((rel, digest, length))
                row.update(status="matched", basis="observed", sha256=digest, bytes=length, data=first)
        self.cache[key] = row
        return row


def fingerprint(accepted: list[tuple[str, str, int]]) -> str:
    lines = [f"{path}\n{digest}\n{length}\n" for path, digest, length in sorted(set(accepted))]
    return sha256_bytes("".join(lines).encode("utf-8"))


def load_module(tools_root: str, reader: str):
    rel, digest, length = READERS[reader]
    full = os.path.abspath(os.path.join(tools_root, *rel.split("/")))
    if not inside(tools_root, full):
        return None, "reader path leaves tools_root"
    status, first, _second = read_twice(full)
    if status != "bytes" or first is None:
        return None, f"reader module {rel} is not a stable regular file ({status})"
    if sha256_bytes(first) != digest or len(first) != length:
        return None, f"reader pin mismatch for {rel}; nothing was loaded"
    spec = importlib.util.spec_from_file_location(f"prime_desk_pass02_{reader.replace('-', '_')}", full)
    if spec is None or spec.loader is None:
        return None, f"reader module {rel} could not be loaded"
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module, None


def file_fact(row: dict) -> dict:
    return {
        "path": row["path"],
        "status": row["status"],
        "basis": row["basis"],
        "sha256": row["sha256"],
        "bytes": row["bytes"],
    }


def quote_text(row: dict) -> dict:
    fact = file_fact(row)
    if row["status"] != "matched" or row["data"] is None:
        fact["text"] = None
        fact["quoted"] = False
        fact["reason"] = "source bytes were not accepted"
        return fact
    if len(row["data"]) > QUOTE_MAX:
        fact["text"] = None
        fact["quoted"] = False
        fact["reason"] = f"source is {len(row['data'])} bytes; the file is the record and this packet does not cut it"
        return fact
    try:
        text = row["data"].decode("utf-8")
    except UnicodeDecodeError:
        fact["text"] = None
        fact["quoted"] = False
        fact["reason"] = "source is not UTF-8; bytes stay at the path"
        return fact
    fact["text"] = text
    fact["quoted"] = True
    fact["reason"] = None
    return fact


def page_identity(path: str) -> dict | None:
    match = PAGE_RE.fullmatch(path)
    if match is None:
        return None
    number = int(match.group(1))
    subject = match.group(2)
    face = match.group(3)
    address = f"{number:04d}.{subject}/{face}"
    if face.startswith("05."):
        if not (500 <= number <= 599) or face == "05.00":
            return None
        review_number = number - 400
        review_path = f"{review_number:04d}.{subject}/{face}.md"
        return {
            "address": address,
            "kind": "n5",
            "review_path": review_path,
            "review_address": f"{review_number:04d}.{subject}/{face}",
        }
    if not (700 <= number <= 799):
        return None
    return {
        "address": address,
        "kind": "n7",
        "review_path": path,
        "review_address": address,
    }


def parse_binding(binding, check: str, work_ids: set[str]) -> dict:
    if not isinstance(binding, dict) or "scope" not in binding:
        raise Problem(check, "binding must name a scope")
    if binding["scope"] == "desk":
        exact(binding, {"scope"}, check)
        return {"scope": "desk", "work_id": None}
    if binding["scope"] == "work":
        exact(binding, {"scope", "work_id"}, check)
        if binding["work_id"] not in work_ids:
            raise Problem(check, "work_id is not a declared work id")
        return {"scope": "work", "work_id": binding["work_id"]}
    raise Problem(check, "binding scope must be desk or work")


def check_ids(items: list, check: str) -> None:
    seen = set()
    for index, item in enumerate(items):
        if not isinstance(item, dict) or "id" not in item:
            raise Problem(check, f"item {index} needs an id")
        ident = item["id"]
        if not is_label(ident, 80):
            raise Problem(check, f"item {index} id must be a label")
        if ident in seen:
            raise Problem(check, f"duplicate id {ident}")
        seen.add(ident)


def pointer_ok(value, check: str) -> None:
    exact(value, {"path", "sha256", "bytes"}, check)
    relative_path(value["path"], check)
    if not is_sha(value["sha256"]) or not is_int(value["bytes"]):
        raise Problem(check, "sha256 must be 64 lowercase hex and bytes must be a non-negative integer")


def parse_request(raw: bytes) -> dict:
    doc = loads(raw, SCHEMA)
    exact(doc, TOP_KEYS, SCHEMA)
    if doc["schema"] != SCHEMA:
        raise Problem(SCHEMA, "unsupported schema")
    exact(doc["instance"], {"root", "book", "role", "tools_root"}, "instance")
    if not is_label(doc["instance"]["book"]) or not is_label(doc["instance"]["role"]):
        raise Problem("instance", "book and role must be labels")
    if doc["coverage"] != COVERAGE_TOKEN:
        raise Problem("coverage", "coverage is not declared-paths")
    root = absolute_dir(doc["instance"]["root"], "instance.root")
    if doc["instance"]["tools_root"] is None:
        raise Problem("instance.tools_root", "tools_root is required")
    tools = absolute_dir(doc["instance"]["tools_root"], "instance.tools_root")
    pointer_ok(doc["workspace"], "workspace")
    pointer_ok(doc["assignment"], "assignment")
    if doc["assignment"]["path"].split("/")[-1] == "00.live.md":
        raise Problem("assignment", "assignment record is the derived view")
    legacy = doc["legacy_selector"]
    if legacy is not None:
        pointer_ok(legacy, "legacy_selector")
    lists = (
        "references", "work", "workers", "supplied", "attention", "history",
        "operations", "legacy", "foreign", "attribution",
    )
    for name in lists:
        if not isinstance(doc[name], list):
            raise Problem(name, "must be a list")
    pointer_ok(doc["catalog"], "catalog")
    return {"doc": doc, "root": root, "tools": tools}


def prepare(req: dict) -> None:
    names = (
        "references", "work", "workers", "supplied", "attention", "history",
        "operations", "legacy", "foreign", "attribution",
    )
    for name in names:
        check_ids(req[name], name)
    work_ids = [item["id"] for item in req["work"]]
    if len(work_ids) != len(set(work_ids)):
        raise Problem("work", "duplicate work id")
    known = set(work_ids)
    for index, item in enumerate(req["references"]):
        exact(item, {"id", "role", "path", "sha256", "bytes", "label", "binding"}, f"references[{index}]")
        if item["role"] not in ROLES:
            raise Problem(f"references[{index}]", "unknown role")
        short_text(item["label"], LABEL_MAX, f"references[{index}].label")
        parse_binding(item["binding"], f"references[{index}].binding", known)
    for index, item in enumerate(req["work"]):
        exact(item, {"id", "address", "path", "sha256", "bytes"}, f"work[{index}]")
        short_text(item["address"], LABEL_MAX, f"work[{index}].address")
    for index, item in enumerate(req["workers"]):
        exact(item, {"id", "work_id", "evidence"}, f"workers[{index}]")
        if not is_label(item["work_id"], 80):
            raise Problem(f"workers[{index}]", "work_id must be a label")
        if item["evidence"] is not None:
            exact(item["evidence"], {"path", "sha256", "bytes"}, f"workers[{index}].evidence")
    for index, item in enumerate(req["supplied"]):
        exact(item, {"id", "speaker", "about", "text", "limit"}, f"supplied[{index}]")
        short_text(item["speaker"], 80, f"supplied[{index}].speaker")
        if item["about"] != "" and not is_label(item["about"], 80):
            raise Problem(f"supplied[{index}]", "about must be empty or a worker id")
        short_text(item["text"], SUPPLIED_MAX, f"supplied[{index}].text")
        short_text(item["limit"], 300, f"supplied[{index}].limit")
    for index, item in enumerate(req["attention"]):
        exact(item, {"id", "kind", "path", "sha256", "bytes", "open", "label"}, f"attention[{index}]")
        if item["kind"] not in ATTENTION_KINDS:
            raise Problem(f"attention[{index}]", "unknown attention kind")
        if type(item["open"]) is not bool:
            raise Problem(f"attention[{index}]", "open must be a boolean")
        short_text(item["label"], LABEL_MAX, f"attention[{index}].label")
    for index, item in enumerate(req["history"]):
        exact(item, {"id", "path", "sha256", "bytes"}, f"history[{index}]")
    for index, item in enumerate(req["operations"]):
        exact(item, {"id", "name", "path", "sha256", "bytes", "limitation", "past_tests", "activation"}, f"operations[{index}]")
        short_text(item["name"], 80, f"operations[{index}].name")
        short_text(item["limitation"], 500, f"operations[{index}].limitation")
        for key in ("past_tests", "activation"):
            if not isinstance(item[key], str) or len(item[key]) > 80:
                raise Problem(f"operations[{index}]", f"{key} must be a short string")
    for index, item in enumerate(req["legacy"]):
        exact(item, {"id", "reader", "path", "sha256", "bytes"}, f"legacy[{index}]")
        if item["reader"] not in READERS:
            raise Problem(f"legacy[{index}]", "unknown reader")
    for index, item in enumerate(req["foreign"]):
        exact(item, {"id", "root", "address", "note"}, f"foreign[{index}]")
        if not isinstance(item["root"], str) or not os.path.isabs(item["root"]):
            raise Problem(f"foreign[{index}]", "root must be absolute")
        short_text(item["address"], LABEL_MAX, f"foreign[{index}].address")
        short_text(item["note"], LABEL_MAX, f"foreign[{index}].note")
    for index, item in enumerate(req["attribution"]):
        exact(item, {"id", "author", "path", "sha256", "bytes", "start", "end", "binding"}, f"attribution[{index}]")
        if item["author"] not in AUTHORS:
            raise Problem(f"attribution[{index}]", "author must be director or model")
        if not is_int(item["start"]) or not is_int(item["end"]) or item["end"] <= item["start"]:
            raise Problem(f"attribution[{index}]", "start and end must be a non-empty byte span")
        parse_binding(item["binding"], f"attribution[{index}].binding", known)


def strip_prefix(prefix: str, value: str, check: str) -> str:
    if not isinstance(value, str) or not value.startswith(prefix):
        raise Problem(check, "path is outside the declared book instance")
    return relative_path(value[len(prefix):], check)


def workspace_body(row: dict) -> dict:
    if row["status"] != "matched" or row["data"] is None:
        raise Problem("workspace", "workspace bytes were not accepted. This run does not read a replacement workspace.")
    body = loads(row["data"], "workspace")
    if not isinstance(body, dict):
        raise Problem("workspace", "workspace JSON must be an object")
    if body.get("schema") != "librarian-development-workspace" or type(body.get("version")) is not int or body.get("version") != 1:
        raise Problem("workspace", "workspace schema is not librarian-development-workspace version 1")
    for key in ("assignment_record", "desk", "work_book"):
        if not isinstance(body.get(key), str) or not body[key] or "\\" in body[key]:
            raise Problem("workspace", f"workspace {key} is not a usable path")
    return body


def assignment_fields(book: Book, row: dict) -> tuple[dict | None, dict]:
    shown = {
        "source": file_fact(row),
        "reader": "app-context.parse_assignment",
        "fields": None,
        "limit": "assignment_state is a record field, not a live process check. validate_context was not called.",
    }
    if row["status"] != "matched" or row["data"] is None:
        return None, shown
    module, problem = load_module(book.tools_root, "app-context")
    if module is None:
        book.add_gap("reader-pin", "app-context", problem or "reader not loaded", row["path"], "unknown")
        shown["limit"] = problem
        return None, shown
    try:
        fields = module.parse_assignment(row["data"])
    except module.Stop as exc:
        raise Problem("assignment-record", f"canonical assignment is malformed ({exc})") from exc
    except SystemExit as exc:
        raise Problem("assignment-record", f"canonical assignment is malformed ({exc})") from exc
    shown["fields"] = {
        "current_work": fields.get("current_work"),
        "pack": fields.get("pack"),
        "assignment_state": fields.get("assignment_state"),
        "waits_on": fields.get("waits_on"),
        "next": fields.get("next"),
        "updated": fields.get("updated"),
        "basis": "observed",
        "next_limit": "the record next field is not a command and is not the selected next route",
    }
    return fields, shown


def legacy_hint(book: Book, req: dict, canonical_id: str | None) -> dict:
    raw = req["legacy_selector"]
    hint = {
        "present": raw is not None,
        "selected_work_id": None,
        "agrees": None,
        "basis": "unknown",
        "source": None,
        "limit": "hint only. prime-desk-selector/1 does not choose current work. This tool does not write a selector.",
        "unused_fields": [],
    }
    if raw is None:
        hint["basis"] = "unknown"
        hint["limit"] = "no legacy selector was declared. " + hint["limit"]
        return hint
    row = book.take(book.root, raw["path"], raw["sha256"], raw["bytes"], "legacy_selector")
    hint["source"] = file_fact(row)
    if row["status"] != "matched" or row["data"] is None:
        hint["basis"] = row["basis"]
        return hint
    try:
        body = loads(row["data"], SELECTOR_SCHEMA)
        exact(body, {"schema", "selected_work_id", "checkpoint", "verified_result", "next_route"}, SELECTOR_SCHEMA)
    except Problem as exc:
        book.add_gap("legacy-selector", exc.check, exc.message + " The canonical assignment still decides.", row["path"], "observed")
        hint["basis"] = "observed"
        return hint
    if body["schema"] != SELECTOR_SCHEMA or not is_label(body["selected_work_id"], 80):
        book.add_gap("legacy-selector", SELECTOR_SCHEMA, "legacy selector identity is not usable. The canonical assignment still decides.", row["path"], "observed")
        hint["basis"] = "observed"
        return hint
    hint["selected_work_id"] = body["selected_work_id"]
    hint["basis"] = "observed"
    for key in ("checkpoint", "verified_result", "next_route"):
        if body[key] is not None:
            hint["unused_fields"].append(key)
    if hint["unused_fields"]:
        book.add_gap(
            "legacy-selector",
            SELECTOR_SCHEMA,
            "legacy selector checkpoint, verified result, and next route are not applied.",
            row["path"],
            "supplied",
        )
    if canonical_id is None:
        book.add_gap(
            "legacy-selector",
            SELECTOR_SCHEMA,
            f"legacy selector names {body['selected_work_id']}. Canonical selection is absent, so the hint was not used.",
            row["path"],
            "observed",
        )
        hint["agrees"] = False
        return hint
    hint["agrees"] = body["selected_work_id"] == canonical_id
    if not hint["agrees"]:
        book.add_gap(
            "selector-disagreement",
            SELECTOR_SCHEMA,
            f"legacy selector names {body['selected_work_id']}; canonical assignment names {canonical_id}. The canonical assignment is kept.",
            row["path"],
            "observed",
        )
    return hint


def catalog_body(book: Book, row: dict) -> dict | None:
    if row["status"] != "matched" or row["data"] is None:
        return None
    try:
        body = loads(row["data"], CATALOG_SCHEMA)
        exact(body, {"schema", "items"}, CATALOG_SCHEMA)
    except Problem as exc:
        book.add_gap("catalog-shape", exc.check, exc.message, row["path"], "observed")
        return None
    if body["schema"] != CATALOG_SCHEMA or not isinstance(body["items"], list):
        book.add_gap("catalog-shape", CATALOG_SCHEMA, "catalog schema is not usable", row["path"], "observed")
        return None
    items = []
    seen = set()
    for index, item in enumerate(body["items"]):
        try:
            exact(item, {"work_id", "address", "label", "provenance"}, f"catalog.items[{index}]")
            if not is_label(item["work_id"], 80):
                raise Problem(f"catalog.items[{index}]", "work_id must be a label")
            short_text(item["address"], LABEL_MAX, f"catalog.items[{index}].address")
            short_text(item["label"], LABEL_MAX, f"catalog.items[{index}].label")
            short_text(item["provenance"], LABEL_MAX, f"catalog.items[{index}].provenance")
        except Problem as exc:
            book.add_gap("catalog-shape", exc.check, exc.message, row["path"], "observed")
            return None
        if item["work_id"] in seen:
            book.add_gap("catalog-shape", CATALOG_SCHEMA, f"duplicate catalog work_id {item['work_id']}", row["path"], "observed")
            return None
        seen.add(item["work_id"])
        items.append({
            "work_id": item["work_id"],
            "address": item["address"],
            "label": item["label"],
            "provenance": item["provenance"],
            "provenance_basis": "supplied",
            "basis": "observed",
        })
    return {"items": items}


def evidence_state(book: Book, row: dict) -> dict:
    fact = file_fact(row)
    fact["recorded_state"] = None
    fact["note"] = None
    fact["process_activity"] = "unknown"
    if row["status"] != "matched" or row["data"] is None:
        return fact
    try:
        body = loads(row["data"], EVIDENCE_SCHEMA)
        exact(body, {"schema", "state", "note"}, EVIDENCE_SCHEMA)
    except Problem as exc:
        book.add_gap("worker-evidence", exc.check, exc.message, row["path"], "observed")
        return fact
    if body["schema"] != EVIDENCE_SCHEMA or body["state"] not in WORKER_STATES:
        book.add_gap("worker-evidence", EVIDENCE_SCHEMA, "evidence state is not a known recorded state", row["path"], "observed")
        return fact
    if not isinstance(body["note"], str) or len(body["note"]) > 300:
        book.add_gap("worker-evidence", EVIDENCE_SCHEMA, "evidence note is not usable", row["path"], "observed")
        return fact
    fact["recorded_state"] = body["state"]
    fact["note"] = body["note"]
    fact["basis"] = "observed"
    return fact


def legacy_row(book: Book, item: dict, row: dict) -> dict:
    reader = item["reader"]
    out = {
        "id": item["id"],
        "reader": reader,
        "source": file_fact(row),
        "called": None,
        "ok": None,
        "limit": "",
        "executed": False,
    }
    if reader == "prime-support":
        out["limit"] = "not executed; status and collect use Git, which this request forbids"
        return out
    if reader == "desk-state":
        out["limit"] = "build_view was not called because it launches subprocesses and can write a candidate"
        if row["status"] == "matched" and row["data"] is not None:
            try:
                body = loads(row["data"], "desk-state/1")
            except Problem as exc:
                out["called"] = "schema-token"
                out["ok"] = False
                out["limit"] = exc.message + " " + out["limit"]
                return out
            token = body.get("schema") if isinstance(body, dict) else None
            out["called"] = "schema-token"
            out["ok"] = token == "desk-state/1"
        return out
    if row["status"] != "matched" or row["data"] is None:
        out["limit"] = "input bytes were not accepted, so the reader was not called"
        return out
    module, problem = load_module(book.tools_root, reader)
    if module is None:
        book.add_gap("reader-pin", reader, problem or "reader not loaded", row["path"], "unknown")
        out["limit"] = problem or "reader not loaded"
        return out
    try:
        body = loads(row["data"], reader)
    except Problem as exc:
        out["called"] = "loads"
        out["ok"] = False
        out["limit"] = exc.message
        return out
    if reader == "prime-brief":
        out["called"] = "validate"
        try:
            module.validate(body)
            out["ok"] = True
            out["limit"] = module.AUTHORITY + " build was not called, so fixture lifecycle labels were not copied onto this desk."
        except module.Refusal as exc:
            out["ok"] = False
            out["limit"] = f"validate refused the input ({exc}). build was not called."
        return out
    if reader == "state-projection":
        out["called"] = "validate"
        try:
            module.validate(body)
            out["ok"] = True
            out["limit"] = "validate accepted the shape. project and inspect were not called, so no lifecycle label was produced."
        except module.Refusal as exc:
            out["ok"] = False
            out["limit"] = f"validate refused the input ({exc}). project and inspect were not called."
        return out
    if reader == "app-context":
        out["called"] = "schema-token"
        token = body.get("schema") if isinstance(body, dict) else None
        out["ok"] = token == "librarian-development-workspace"
        out["limit"] = "validate_context was not called; it lists a runtime band and checks a runner. A workspace file is not live authority."
        return out
    out["limit"] = "reader was not executed"
    return out


def operation_row(book: Book, item: dict) -> dict:
    row = book.take(book.tools_root, item["path"], item["sha256"], item["bytes"], f"operations:{item['id']}")
    past = item["past_tests"]
    activation = item["activation"]
    recognized = past in ("unknown", "supplied-not-verified") and activation in ("unknown", "supplied-not-verified")
    made = {
        "id": item["id"],
        "name": item["name"],
        "source": file_fact(row),
        "limitation": item["limitation"],
        "limitation_basis": "supplied",
        "past_tests": past,
        "past_tests_basis": "unknown" if past == "unknown" else "supplied",
        "activation": activation,
        "activation_basis": "unknown" if activation == "unknown" else "supplied",
        "executed": False,
        "recognized_token": recognized,
    }
    if not recognized:
        book.add_gap(
            "operation-label",
            f"operations:{item['id']}",
            "past_tests or activation is not unknown or supplied-not-verified. The token is not a passed test and not a live activation.",
            row["path"],
            "supplied",
        )
    return made


def bound_to(item: dict, work_id: str | None) -> bool:
    binding = item["binding"]
    if binding["scope"] == "desk":
        return False
    return work_id is not None and binding["work_id"] == work_id


def attribution_rows(book: Book, req: dict) -> list[dict]:
    rows = []
    for item in req["attribution"]:
        row = book.take(book.root, item["path"], item["sha256"], item["bytes"], f"attribution:{item['id']}")
        made = {
            "id": item["id"],
            "author": item["author"],
            "binding": item["binding"],
            "source": file_fact(row),
            "start": item["start"],
            "end": item["end"],
            "text": None,
            "quoted": False,
            "ambiguous": False,
            "reason": None,
        }
        if row["status"] != "matched" or row["data"] is None:
            made["reason"] = "source bytes were not accepted"
            rows.append(made)
            continue
        if item["end"] > len(row["data"]):
            book.add_gap("attribution-span", item["id"], "span ends past the file. The slice was withheld.", item["path"], "observed")
            made["reason"] = "span is outside the file"
            rows.append(made)
            continue
        slice_bytes = row["data"][item["start"]:item["end"]]
        try:
            made["text"] = slice_bytes.decode("utf-8")
            made["quoted"] = True
        except UnicodeDecodeError:
            book.add_gap("attribution-span", item["id"], "span is not UTF-8. The slice was withheld.", item["path"], "observed")
            made["reason"] = "span is not UTF-8"
        rows.append(made)
    by_path: dict[str, list[dict]] = {}
    for item in rows:
        if item["quoted"]:
            by_path.setdefault(item["source"]["path"], []).append(item)
    for grouped in by_path.values():
        for left in grouped:
            for right in grouped:
                if left is right:
                    continue
                if left["start"] < right["end"] and right["start"] < left["end"]:
                    left["ambiguous"] = True
                    right["ambiguous"] = True
    ambiguous_paths = sorted({item["source"]["path"] for item in rows if item["ambiguous"]})
    for path in ambiguous_paths:
        book.add_gap(
            "attribution-ambiguity",
            path,
            "overlapping attribution spans were found. Both stay visible. Neither is the sole wording.",
            path,
            "observed",
        )
    return rows


def review_home_for(book: Book, ident: dict, declared: dict[str, dict]) -> dict:
    path = ident["review_path"]
    home = {
        "kind": ident["kind"],
        "address": ident["review_address"],
        "path": path,
        "basis": "unknown",
        "source": None,
        "limit": "",
    }
    row = declared.get(path)
    if ident["kind"] == "n7":
        home["basis"] = "observed" if row and row["status"] == "matched" else "unknown"
        home["source"] = None if row is None else file_fact(row)
        home["limit"] = "page-local N7NN review file. Reporting policy is not this destination."
        return home
    if row is not None and row["status"] == "matched":
        home["basis"] = "observed"
        home["source"] = file_fact(row)
        home["limit"] = "derived N1NN page matched a declared source. A hash proves those bytes only."
        return home
    home["limit"] = "Pending custody. The derived review file is not a matched declared source. No receipt is fabricated."
    book.add_gap("custody-pending", ident["review_address"], home["limit"], path, "unknown")
    if row is not None:
        home["source"] = file_fact(row)
        home["basis"] = row["basis"]
    return home


def finish(command: str, work_id: str | None, observed: str, request_sha: str, book: Book, req: dict) -> dict:
    workspace_row = book.take(book.tools_root, req["workspace"]["path"], req["workspace"]["sha256"], req["workspace"]["bytes"], "workspace")
    workspace = workspace_body(workspace_row)
    if workspace["work_book"] != req["instance"]["book"]:
        raise Problem("instance", "instance book does not match the workspace work book")
    prefix = workspace["desk"] + "/" + workspace["work_book"] + "/"
    assignment_rel = strip_prefix(prefix, workspace["assignment_record"], "workspace.assignment_record")
    if assignment_rel != req["assignment"]["path"]:
        raise Problem("assignment", "request assignment path is not the workspace assignment record")
    assignment_row = book.take(book.root, req["assignment"]["path"], req["assignment"]["sha256"], req["assignment"]["bytes"], "assignment")
    fields = None
    reader = {
        "source": file_fact(assignment_row),
        "reader": "app-context.parse_assignment",
        "fields": None,
        "limit": "assignment bytes were not accepted. validate_context was not called.",
    }
    if assignment_row["status"] == "missing":
        raise Problem("assignment", "canonical assignment is absent")
    if assignment_row["status"] == "matched":
        fields, reader = assignment_fields(book, assignment_row)
    selected = None
    selected_row = None
    ident = None
    canonical_id = None
    if fields is not None:
        if fields["desk"] != workspace["desk"] or fields["book"] != workspace["work_book"]:
            raise Problem("instance", "assignment record book does not match this instance")
        current_rel = strip_prefix(prefix, fields["current_work"], "assignment.current_work")
        ident = page_identity(current_rel)
        if ident is None:
            raise Problem("assignment.current_work", "page identity is not N5NN/05.NN or N7NN/06.NN.review")
        matches = [item for item in req["work"] if item["path"] == current_rel]
        if len(matches) != 1:
            book.add_gap(
                "unregistered-selection",
                RULE,
                f"canonical page {current_rel} is not one declared work row. The catalog was not used.",
                current_rel,
                "observed",
            )
        else:
            item = matches[0]
            if item["address"] != ident["address"]:
                book.add_gap(
                    "identity",
                    RULE,
                    f"work address {item['address']} does not equal page {ident['address']}. Normalization did not cross the subject.",
                    item["path"],
                    "observed",
                )
            else:
                selected_row = book.take(book.root, item["path"], item["sha256"], item["bytes"], f"work:{item['id']}")
                if selected_row["status"] == "matched":
                    canonical_id = item["id"]
                    selected = {
                        "id": item["id"],
                        "address": ident["address"],
                        "source": file_fact(selected_row),
                        "basis": "observed",
                        "rule": RULE,
                        "current_work": fields["current_work"],
                        "record_path": req["assignment"]["path"],
                    }
                else:
                    book.add_gap("selector", "work", f"canonical work {item['id']} bytes were not accepted", item["path"], selected_row["basis"])
    hint = legacy_hint(book, req, canonical_id)
    work_rows = []
    declared: dict[str, dict] = {}
    for item in req["work"]:
        row = selected_row if selected is not None and item["id"] == selected["id"] else book.take(
            book.root, item["path"], item["sha256"], item["bytes"], f"work:{item['id']}"
        )
        work_rows.append((item, row))
        declared.setdefault(item["path"], row)
    not_selected = []
    for item, row in work_rows:
        if selected is not None and item["id"] == selected["id"]:
            continue
        not_selected.append({
            "id": item["id"],
            "address": item["address"],
            "source": file_fact(row),
            "reason": "not the canonical assignment record",
            "basis": "observed",
        })
    references = []
    for item in req["references"]:
        row = book.take(book.root, item["path"], item["sha256"], item["bytes"], f"references:{item['id']}")
        declared.setdefault(item["path"], row)
        binding = parse_binding(item["binding"], item["id"], {entry["id"] for entry in req["work"]})
        rec = {
            "id": item["id"],
            "role": item["role"],
            "label": item["label"],
            "label_basis": "supplied",
            "binding": binding,
            "source": file_fact(row),
            "for_selected": bound_to({"binding": binding}, canonical_id) or binding["scope"] == "desk",
        }
        if item["role"] in WORK_ROLES and binding["scope"] != "work":
            book.add_gap(
                "unbound-task",
                item["id"],
                f"{item['role']} is desk-scoped, so it is not this task's {item['role']}.",
                item["path"],
                "supplied",
            )
            rec["for_selected"] = False
        if item["role"] == "talk":
            rec["parsed"] = False
            rec["executable"] = False
            rec["limit"] = "talk is not parsed and is not executable"
        if item["role"] in ("return", "receipt") and binding["scope"] == "work" and canonical_id and binding["work_id"] == canonical_id and row["status"] != "matched":
            book.add_gap(item["role"], f"references:{item['id']}", f"{item['role']} is {row['status']}", item["path"], row["basis"])
        references.append(rec)
    review_home = None
    if selected is not None and ident is not None:
        review_home = review_home_for(book, ident, declared)
        selected["review_home"] = review_home
        selected["legacy_selector"] = hint
    catalog_row = book.take(book.root, req["catalog"]["path"], req["catalog"]["sha256"], req["catalog"]["bytes"], "catalog")
    catalog = catalog_body(book, catalog_row)
    if catalog is not None:
        for item in catalog["items"]:
            if canonical_id is None or item["work_id"] != canonical_id:
                shown = "absent" if canonical_id is None else canonical_id
                book.add_gap(
                    "catalog-not-chosen",
                    CATALOG_SCHEMA,
                    f"catalog names {item['work_id']}; canonical assignment names {shown}. The catalog was not used to choose the work.",
                    catalog_row["path"],
                    "observed",
                )
    attention = []
    for item in req["attention"]:
        row = book.take(book.root, item["path"], item["sha256"], item["bytes"], f"attention:{item['id']}")
        attention.append({
            "id": item["id"],
            "kind": item["kind"],
            "open": item["open"],
            "label": item["label"],
            "label_basis": "supplied",
            "source": file_fact(row),
        })
    history = []
    for item in req["history"]:
        row = book.take(book.root, item["path"], item["sha256"], item["bytes"], f"history:{item['id']}")
        history.append({"id": item["id"], "source": file_fact(row), "inlined": False})
    supplied_by: dict[str, list[dict]] = {}
    for item in req["supplied"]:
        supplied_by.setdefault(item["about"], []).append({
            "id": item["id"],
            "speaker": item["speaker"],
            "text": item["text"],
            "limit": item["limit"],
            "basis": "supplied",
        })
    workers = []
    for item in req["workers"]:
        if item["evidence"] is None:
            evidence = {
                "path": None, "status": "absent", "basis": "unknown", "sha256": None,
                "bytes": None, "recorded_state": None, "note": None, "process_activity": "unknown",
            }
            book.add_gap("worker-unknown", f"workers:{item['id']}", "no recorded evidence file; process activity is unknown", None, "unknown")
        else:
            row = book.take(book.root, item["evidence"]["path"], item["evidence"]["sha256"], item["evidence"]["bytes"], f"workers:{item['id']}")
            evidence = evidence_state(book, row)
        workers.append({
            "id": item["id"],
            "work_id": item["work_id"],
            "association_basis": "supplied",
            "association_limit": "the declared work id is not proof of task association beyond this request",
            "declared_on_selected": canonical_id is not None and item["work_id"] == canonical_id,
            "evidence": evidence,
            "supplied": supplied_by.get(item["id"], []),
            "process_activity": "unknown",
            "process_basis": "unknown",
        })
    operations = [operation_row(book, item) for item in req["operations"]]
    operations.append({
        "id": "review-loop-integration",
        "name": "review-loop",
        "source": None,
        "limitation": "Pending. Successor modules were not imported.",
        "limitation_basis": "tool",
        "past_tests": "unknown",
        "past_tests_basis": "unknown",
        "activation": "unknown",
        "activation_basis": "unknown",
        "executed": False,
        "recognized_token": True,
    })
    legacy = []
    for item in req["legacy"]:
        row = book.take(book.root, item["path"], item["sha256"], item["bytes"], f"legacy:{item['id']}")
        legacy.append(legacy_row(book, item, row))
    foreign = []
    for item in req["foreign"]:
        same = os.path.normcase(os.path.abspath(item["root"])) == os.path.normcase(book.root)
        if same:
            book.add_gap("foreign", f"foreign:{item['id']}", "foreign root is this instance; it was not read as a second copy", None, "unknown")
        foreign.append({
            "id": item["id"],
            "root": item["root"],
            "address": item["address"],
            "note": item["note"],
            "note_basis": "supplied",
            "read": False,
            "same_instance": same,
            "same_address_as_selected": selected is not None and item["address"] == selected["address"],
        })
    spans = attribution_rows(book, req)
    if selected is not None:
        checkpoints = [item for item in references if item["role"] == "checkpoint" and bound_to(item, canonical_id)]
        verified = [item for item in references if item["role"] == "verification" and bound_to(item, canonical_id)]
        routes = [item for item in references if item["role"] == "next" and bound_to(item, canonical_id)]
        if not checkpoints:
            selected["checkpoint"] = {"basis": "unknown", "source": None}
        else:
            selected["checkpoint"] = {"basis": checkpoints[0]["source"]["basis"], "source": checkpoints[0]["source"]}
        if not verified or verified[0]["source"]["status"] != "matched":
            selected["verified_result"] = {"basis": "unknown", "source": None if not verified else verified[0]["source"], "limit": "missing verification is unknown, not a clean bill of health"}
            book.add_gap("verification", "verification", "no matched verification is bound to the canonical work", None, "unknown")
        else:
            selected["verified_result"] = {
                "basis": "observed",
                "source": verified[0]["source"],
                "limit": "a matching hash proves these bytes, not acceptance or process freshness",
            }
        if not routes:
            selected["next_route"] = {"basis": "unknown", "source": None, "limit": "no work-bound next route is declared"}
        else:
            selected["next_route"] = {
                "basis": routes[0]["source"]["basis"],
                "source": routes[0]["source"],
                "limit": "this route is a declared reference, not a command this tool runs",
            }
    packet = None
    packet_refused = False
    if command == "packet":
        if selected is None or work_id != selected["id"]:
            packet_refused = True
            shown = None if selected is None else selected["id"]
            book.add_gap(
                "packet-selection",
                "packet",
                f"--work-id {work_id} is not the canonical selection ({shown}). The packet was not expanded.",
                None,
                "observed",
            )
        else:
            def task_items(role: str) -> list[dict]:
                chosen = []
                for item in references:
                    if item["role"] != role or not bound_to(item, canonical_id):
                        continue
                    row = declared[item["source"]["path"]]
                    quoted = quote_text(row)
                    quoted["id"] = item["id"]
                    quoted["role"] = role
                    quoted["label"] = item["label"]
                    chosen.append(quoted)
                return chosen

            def span_items(author: str) -> list[dict]:
                chosen = []
                for item in spans:
                    binding = item["binding"]
                    if item["author"] != author:
                        continue
                    if binding["scope"] == "work" and binding["work_id"] != canonical_id:
                        continue
                    chosen.append(item)
                return chosen

            packet = {
                "work_id": selected["id"],
                "assignment": quote_text(selected_row),
                "criteria": task_items("criteria"),
                "checkpoint": task_items("checkpoint"),
                "director": span_items("director"),
                "model": span_items("model"),
                "returns": [item for item in references if item["role"] in ("return", "deliverable") and bound_to(item, canonical_id)],
                "receipts": [item for item in references if item["role"] == "receipt" and bound_to(item, canonical_id)],
                "verification": [item for item in references if item["role"] == "verification" and bound_to(item, canonical_id)],
                "findings": [item for item in references if item["role"] == "finding" and bound_to(item, canonical_id)],
                "dependencies": [item for item in references if item["role"] == "dependency" and (item["binding"]["scope"] == "desk" or bound_to(item, canonical_id))],
                "review_home": review_home,
                "next_routes": [item for item in references if item["role"] == "next" and bound_to(item, canonical_id)],
                "desk_policy": [item for item in references if item["binding"]["scope"] == "desk"],
                "assignment_reader": [reader],
                "verification_limit": selected["verified_result"]["limit"],
            }
    open_attention = [item for item in attention if item["open"]]
    exit_code = 1 if book.gaps or open_attention or packet_refused else 0
    if selected is None:
        state = "partial"
    elif exit_code:
        state = "attention"
    else:
        state = "ready"
    correction = "None of the declared open items blocks reading. This view still grants nothing."
    if exit_code:
        correction = "Read the gaps and open attention. Keep the canonical assignment. Do not treat a supplied label or a legacy selector as the current work. " + ESCALATION
    return {
        "schema": PACKET_SCHEMA if command == "packet" else VIEW_SCHEMA,
        "command": command,
        "state": state,
        "exit": exit_code,
        "check": SCHEMA,
        "correction": correction,
        "observed_at": observed,
        "coverage": book.coverage,
        "instance": {
            "root": book.root,
            "book": req["instance"]["book"],
            "role": req["instance"]["role"],
            "tools_root": book.tools_root,
            "basis": "observed",
        },
        "selected": selected,
        "not_selected": not_selected,
        "catalog": None if catalog is None else {
            "source": file_fact(catalog_row),
            "items": catalog["items"],
            "used_for_selection": False,
        },
        "attention": attention,
        "gaps": book.gaps,
        "workers": workers,
        "operations": operations,
        "record": {
            "references": references,
            "history": history,
            "history_inlined": False,
            "talk_parsed": False,
            "assignment_reader": [reader],
            "attribution": spans,
            "supplied_without_worker": supplied_by.get("", []),
        },
        "inspectability": {
            "request_sha256": request_sha,
            "fingerprint": fingerprint(book.accepted),
            "basis_legend": "observed = declared bytes matched; supplied = caller label; unknown = not present; stale = different bytes withheld; changed = bytes moved during the read and were withheld",
            "escalation": ESCALATION,
        },
        "legacy": legacy,
        "foreign": foreign,
        "packet": packet,
    }


def assemble(request_path: str, command: str, work_id: str | None) -> dict:
    observed = now()
    if command not in ("view", "packet"):
        return refuse(command, observed, "command", "command must be view or packet")
    if command == "packet" and (not isinstance(work_id, str) or not is_label(work_id, 80)):
        return refuse("packet", observed, "packet", "--work-id must be a label")
    if not isinstance(request_path, str) or not os.path.isabs(request_path):
        return refuse(command, observed, "request", "--request must be absolute")
    status, first, _second = read_twice(request_path)
    if status != "bytes" or first is None:
        return refuse(command, observed, "request", f"request file is {status}")
    request_sha = sha256_bytes(first)
    try:
        parsed = parse_request(first)
        prepare(parsed["doc"])
        book = Book(parsed["root"], parsed["tools"])
        doc = finish(command, work_id, observed, request_sha, book, parsed["doc"])
    except Problem as exc:
        doc = refuse(command, observed, exc.check, exc.message)
        doc["inspectability"]["request_sha256"] = request_sha
        if "book" in locals():
            doc["coverage"] = book.coverage
            doc["instance"] = {
                "root": book.root,
                "book": parsed["doc"]["instance"]["book"],
                "role": parsed["doc"]["instance"]["role"],
                "tools_root": book.tools_root,
            }
        return doc
    return doc


def fence(text: str) -> str:
    size = 3
    while "`" * size in text:
        size += 1
    return "`" * size


def fenced(text: str) -> str:
    mark = fence(text)
    return f"{mark}\n{text.rstrip(chr(10))}\n{mark}"


def source_line(source: dict | None) -> str:
    if not source:
        return "none"
    path = source.get("path") or "none"
    status = source.get("status") or "none"
    sha = source.get("sha256") or "none"
    short = sha[:12] if isinstance(sha, str) else "none"
    length = source.get("bytes")
    shown = length if type(length) is int else "none"
    basis = source.get("basis") or "unknown"
    return f"`{path}` {status} {short} {shown} basis {basis}"


def render(doc: dict) -> str:
    if doc["state"] == "refused":
        return "\n".join([
            "# Prime desk refusal",
            "",
            f"Check: {doc['check']}",
            f"State: {doc['state']}",
            "",
            doc["correction"],
            "",
        ])
    inst = doc["instance"] or {}
    lines = [
        "# Prime desk",
        "",
        f"Book `{inst.get('book')}` role `{inst.get('role')}`.",
        f"Root: `{inst.get('root')}`.",
        f"Observed: {doc['observed_at']}.",
        f"Coverage: {doc['coverage']['statement']} Matched {doc['coverage']['matched']}, missing {doc['coverage']['missing']}, stale {doc['coverage']['stale']}, changed {doc['coverage']['changed']}.",
        "",
        "## 1. Context and purpose",
        "",
    ]
    record = doc["record"] if isinstance(doc["record"], dict) else {"references": [], "history": []}
    for role in ("goal", "scope", "authority"):
        rows = [item for item in record.get("references", []) if item["role"] == role]
        if not rows:
            lines.append(f"{role}: none declared.")
        for item in rows:
            lines.append(f"{role}: {item['label']} ({source_line(item['source'])}). Label basis supplied.")
    lines.append("This view does not grant authority.")
    lines += ["", "## 2. Current work", ""]
    selected = doc["selected"]
    if selected is None:
        lines.append("Selected work: unknown. The canonical assignment was not accepted. No catalog entry was chosen.")
    else:
        lines.append(f"Selected: {selected['id']} `{selected['address']}`.")
        lines.append(f"Rule: {selected['rule']}.")
        lines.append(f"Source: {source_line(selected['source'])}.")
        lines.append(f"Record current_work: `{selected['current_work']}`.")
        hint = selected.get("legacy_selector") or {}
        lines.append(
            f"Legacy selector: {hint.get('selected_work_id') or 'absent'}. "
            f"Agrees: {hint.get('agrees')}. Hint only."
        )
        home = selected.get("review_home") or {}
        lines.append(f"Review home: `{home.get('address')}` basis {home.get('basis')}. {home.get('limit') or ''}")
        verified = selected.get("verified_result") or {}
        lines.append(f"Verified result: {source_line(verified.get('source'))}. Basis {verified.get('basis')}. {verified.get('limit') or ''}")
        checkpoint = selected.get("checkpoint") or {}
        lines.append(f"Checkpoint: {source_line(checkpoint.get('source'))}. Basis {checkpoint.get('basis')}.")
        nxt = selected.get("next_route") or {}
        lines.append(f"Next route: {source_line(nxt.get('source'))}. Basis {nxt.get('basis')}.")
    if doc["not_selected"]:
        lines.append("Declared and not selected:")
        for item in doc["not_selected"]:
            lines.append(f"- {item['id']} `{item['address']}` {item['reason']}.")
    else:
        lines.append("Declared and not selected: none.")
    catalog = doc["catalog"]
    if catalog is None:
        lines.append("Catalog: not accepted. It was not used to choose the work.")
    else:
        names = ", ".join(item["work_id"] for item in catalog["items"]) or "none"
        lines.append(f"Catalog index names: {names}. Used for selection: false.")
    lines += ["", "## 3. Attention", ""]
    open_rows = [item for item in doc["attention"] if item["open"]]
    lines.append(f"Open declared attention: {len(open_rows)}. Listed in full.")
    for item in doc["attention"]:
        flag = "open" if item["open"] else "closed"
        lines.append(f"- {flag} {item['kind']} {item['id']}: {item['label']} ({source_line(item['source'])}).")
    lines.append(f"Observed gaps: {len(doc['gaps'])}. Listed in full.")
    for gap in doc["gaps"]:
        lines.append(f"- {gap['kind']} {gap['check']}: {gap['message']}")
    lines.append("Unregistered sources were not searched. That is not a report that none exist.")
    lines += ["", "## 4. Workers", ""]
    if not doc["workers"]:
        lines.append("None declared. Activity is unknown.")
    for worker in doc["workers"]:
        evidence = worker["evidence"]
        lines.append(
            f"- {worker['id']} on {worker['work_id']}: recorded {evidence.get('recorded_state') or 'none'} "
            f"({source_line(evidence)}). Association basis supplied. Process activity: unknown."
        )
        for supplied in worker["supplied"]:
            lines.append(f"  supplied {supplied['speaker']}: {supplied['text']} Limit: {supplied['limit']}")
    lines += ["", "## 5. Operations", ""]
    for op in doc["operations"]:
        src = source_line(op["source"]) if op.get("source") else "no file"
        lines.append(
            f"- {op['name']} {src}. Limitation ({op['limitation_basis']}): {op['limitation']} "
            f"Past tests {op['past_tests']} ({op['past_tests_basis']}). Activation {op['activation']} ({op['activation_basis']}). Executed: false."
        )
    lines += ["", "## 6. Record", ""]
    lines.append("Director and model wording are attribution spans, not request roles.")
    for item in record.get("attribution", []):
        lines.append(
            f"- {item['author']} {item['id']} bytes {item['start']}:{item['end']} "
            f"ambiguous {item['ambiguous']} ({source_line(item['source'])})."
        )
    if not record.get("attribution"):
        lines.append("attribution: none declared.")
    talk = [item for item in record.get("references", []) if item["role"] == "talk"]
    if not talk:
        lines.append("talk: none declared.")
    for item in talk:
        lines.append(f"talk: {item['label']} ({source_line(item['source'])}). Not parsed. Not executable.")
    reader = record.get("assignment_reader") or []
    if reader and reader[0].get("fields"):
        fields = reader[0]["fields"]
        lines.append(
            f"assignment_state `{fields.get('assignment_state')}` basis observed. {reader[0].get('limit')}"
        )
    lines.append(f"History records: {len(record.get('history', []))}. Bodies are not copied.")
    for item in record.get("history", []):
        lines.append(f"- {item['id']} {source_line(item['source'])}.")
    lines += ["", "## 7. Inspectability", ""]
    info = doc["inspectability"]
    lines.append(f"Request sha256: {info.get('request_sha256')}.")
    lines.append(f"Fingerprint: {info.get('fingerprint')}.")
    lines.append(info.get("basis_legend", ""))
    lines.append(doc["correction"])
    if doc["command"] == "packet" and doc.get("packet"):
        lines.extend(render_packet(doc["packet"]))
    elif doc["command"] == "packet":
        lines += ["", "## Packet", "", "Not expanded. The work id is not the canonical selection."]
    lines.append("")
    return "\n".join(lines)


def render_packet(packet: dict) -> list[str]:
    lines = ["", "## Packet", ""]
    lines.append("### Assignment")
    lines.append(quote_block(packet["assignment"]))
    lines.append("### Finish criteria")
    if not packet["criteria"]:
        lines.append("None bound to this work.")
    for item in packet["criteria"]:
        lines.append(quote_block(item))
    lines.append("### Director wording")
    lines.append("Declared director spans only. A file role is not an author.")
    if not packet["director"]:
        lines.append("None declared.")
    for item in packet["director"]:
        lines.append(span_block(item))
    lines.append("### Model explanation")
    lines.append("This section is separate from Director wording.")
    if not packet["model"]:
        lines.append("None declared.")
    for item in packet["model"]:
        lines.append(span_block(item))
    lines.append("### Returns and deliverables")
    lines.extend(ref_lines(packet["returns"]))
    lines.append("### Receipts")
    lines.extend(ref_lines(packet["receipts"]))
    lines.append("### Verification")
    lines.append(packet.get("verification_limit") or "")
    lines.extend(ref_lines(packet["verification"]))
    lines.append("### Findings")
    lines.extend(ref_lines(packet["findings"]))
    lines.append("### Dependencies")
    lines.extend(ref_lines(packet["dependencies"]))
    lines.append("### Review home")
    home = packet.get("review_home") or {}
    lines.append(f"`{home.get('address')}` `{home.get('path')}` basis {home.get('basis')}. {home.get('limit') or ''}")
    lines.append("### Next routes")
    lines.extend(ref_lines(packet["next_routes"]))
    lines.append("### Desk policy")
    lines.append("Desk-wide references are policy links. They are not another task's criteria or review destination.")
    lines.extend(ref_lines(packet["desk_policy"]))
    return lines


def quote_block(item: dict) -> str:
    if item.get("quoted") and item.get("text") is not None:
        return fenced(item["text"])
    reason = item.get("reason") or "not quoted"
    return f"Not quoted. {reason} {source_line(item if 'path' in item else item.get('source'))}"


def span_block(item: dict) -> str:
    source = item.get("source") or {}
    head = (
        f"{item['author']} {item['id']} bytes {item['start']}:{item['end']} "
        f"sha256 {source.get('sha256')} ambiguous {item['ambiguous']}"
    )
    if item.get("quoted") and item.get("text") is not None:
        return head + "\n" + fenced(item["text"])
    return head + f"\nNot quoted. {item.get('reason') or 'withheld'}"


def ref_lines(items: list[dict]) -> list[str]:
    if not items:
        return ["None bound to this work."]
    return [f"- {item['id']}: {item.get('label') or item.get('role')} ({source_line(item.get('source') if 'source' in item else item)})." for item in items]


def emit(doc: dict, as_json: bool) -> int:
    if as_json:
        sys.stdout.buffer.write(dump(doc))
    else:
        sys.stdout.buffer.write(render(doc).encode("utf-8"))
    return int(doc["exit"])


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    observed = now()
    if not args or args[0] not in ("view", "packet"):
        return emit(refuse(args[0] if args else "none", observed, "command", "use view or packet"), True)
    command = args.pop(0)
    as_json = False
    request = None
    work_id = None
    index = 0
    while index < len(args):
        flag = args[index]
        if flag == "--json":
            as_json = True
            index += 1
            continue
        if flag in ("--request", "--work-id"):
            if index + 1 >= len(args):
                return emit(refuse(command, observed, flag, "missing value"), as_json)
            if flag == "--request":
                request = args[index + 1]
            else:
                work_id = args[index + 1]
            index += 2
            continue
        return emit(refuse(command, observed, "arguments", f"unknown argument {flag}"), as_json)
    if request is None:
        return emit(refuse(command, observed, "--request", "missing --request"), as_json)
    return emit(assemble(request, command, work_id), as_json)


if __name__ == "__main__":
    sys.exit(main())
