#!/usr/bin/env python3
"""Read-only Prime desk overview and selected-work packet.

The request names every source. This tool does not crawl a repository, call Git,
launch a worker, or write a source record. A hash match proves bytes only.
"""

from __future__ import annotations

import hashlib
import importlib.util
import io
import json
import os
import stat
import sys
from datetime import datetime, timezone

sys.dont_write_bytecode = True
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"

SCHEMA = "prime-desk-request/1"
SELECTOR_SCHEMA = "prime-desk-selector/1"
CATALOG_SCHEMA = "prime-desk-catalog/1"
EVIDENCE_SCHEMA = "prime-desk-worker-evidence/1"
VIEW_SCHEMA = "prime-desk-view/1"
PACKET_SCHEMA = "prime-desk-packet/1"
COVERAGE = "Declared request paths only. Unregistered sources were not searched."
ESCALATION = (
    "Escalation: Codex Prime on 0524.prime-desk/05.01. "
    "This tool does not decide meaning, acceptance, or live authority."
)
QUOTE_MAX = 12000
LABEL_MAX = 200
SUPPLIED_MAX = 500
REPARSE = 0x400

ROLES = {
    "goal", "scope", "authority", "criteria", "assignment", "director", "model",
    "return", "receipt", "deliverable", "verification", "finding", "dependency",
    "review-home", "next", "talk", "other",
}
ATTENTION_KINDS = {
    "director-question", "return-awaiting-review", "observer-finding", "conflict",
    "missing-evidence", "interrupted", "hold",
}
WORKER_STATES = {"released", "claimed", "returned", "awaiting-review"}
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
    "schema", "instance", "selector", "references", "work", "workers", "supplied",
    "attention", "history", "catalog", "operations", "legacy", "foreign",
}
RESULT_KEYS = [
    "schema", "command", "state", "exit", "check", "correction", "observed_at",
    "coverage", "instance", "selected", "not_selected", "catalog", "attention",
    "gaps", "workers", "operations", "record", "inspectability", "legacy",
    "foreign", "packet",
]


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
        value = json.loads(text, object_pairs_hook=pairs, parse_constant=reject)
    except Problem:
        raise
    except json.JSONDecodeError as exc:
        raise Problem(check, f"JSON is not usable ({exc.msg})") from exc
    return value


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
        st = os.lstat(path)
    except OSError:
        return True
    attrs = getattr(st, "st_file_attributes", 0) or 0
    return bool(attrs & REPARSE) or stat.S_ISLNK(st.st_mode)


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
        "schema": VIEW_SCHEMA if command == "view" else PACKET_SCHEMA,
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
        "record": [],
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
    doc = blank(command, observed, check, message + " " + ESCALATION, 2, "refused")
    return doc


def read_twice(path: str) -> tuple[str, bytes | None, bytes | None]:
    if not os.path.lexists(path):
        return "missing", None, None
    if is_reparse(path):
        return "unreadable", None, None
    st = os.lstat(path)
    if not stat.S_ISREG(st.st_mode):
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
    def __init__(self, root: str, tools_root: str | None) -> None:
        self.root = root
        self.tools_root = tools_root
        self.coverage = empty_coverage()
        self.accepted: list[tuple[str, str, int]] = []
        self.gaps: list[dict] = []

    def add_gap(self, kind: str, check: str, message: str, path: str | None, basis: str) -> None:
        self.gaps.append({
            "kind": kind,
            "check": check,
            "message": message,
            "path": path,
            "basis": basis,
        })

    def take(self, base: str, rel: str, expect_sha: str, expect_bytes: int, label: str) -> dict:
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
            return row
        if not is_sha(expect_sha) or not is_int(expect_bytes):
            raise Problem(label, "sha256 must be 64 lowercase hex and bytes must be a non-negative integer")
        full = os.path.abspath(os.path.join(base, *rel.split("/")))
        if not inside(base, full):
            self.coverage["outside"] += 1
            self.add_gap("outside-path", label, "path leaves the declared root", rel, "unknown")
            return row
        status, first, second = read_twice(full)
        if status == "missing":
            self.coverage["missing"] += 1
            row["status"] = "missing"
            self.add_gap("missing", label, "declared file is absent", rel, "unknown")
            return row
        if status == "unreadable":
            self.coverage["unreadable"] += 1
            row["status"] = "unreadable"
            self.add_gap("unreadable", label, "path is not a regular file", rel, "unknown")
            return row
        if status == "changed":
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
            return row
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
            return row
        self.coverage["matched"] += 1
        self.accepted.append((rel, digest, length))
        row.update(status="matched", basis="observed", sha256=digest, bytes=length, data=first)
        return row


def fingerprint(accepted: list[tuple[str, str, int]]) -> str:
    lines = [f"{path}\n{digest}\n{length}\n" for path, digest, length in sorted(accepted)]
    return sha256_bytes("".join(lines).encode("utf-8"))


def load_module(tools_root: str, reader: str):
    rel, digest, length = READERS[reader]
    full = os.path.abspath(os.path.join(tools_root, *rel.split("/")))
    if not inside(tools_root, full):
        return None, "reader path leaves tools_root"
    status, first, _second = read_twice(full)
    if status != "bytes" or first is None:
        return None, f"reader module {rel} is not a stable regular file ({status})"
    got = sha256_bytes(first)
    if got != digest or len(first) != length:
        return None, f"reader pin mismatch for {rel}; nothing was loaded"
    spec = importlib.util.spec_from_file_location(f"prime_desk_pinned_{reader.replace('-', '_')}", full)
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


def parse_request(raw: bytes) -> dict:
    doc = loads(raw, "prime-desk-request/1")
    exact(doc, TOP_KEYS, "prime-desk-request/1")
    if doc["schema"] != SCHEMA:
        raise Problem("prime-desk-request/1", "unsupported schema")
    exact(doc["instance"], {"root", "book", "role", "tools_root"}, "instance")
    if not is_label(doc["instance"]["book"]) or not is_label(doc["instance"]["role"]):
        raise Problem("instance", "book and role must be labels")
    root = absolute_dir(doc["instance"]["root"], "instance.root")
    tools = doc["instance"]["tools_root"]
    if tools is not None:
        tools = absolute_dir(tools, "instance.tools_root")
    exact(doc["selector"], {"path", "sha256", "bytes"}, "selector")
    lists = (
        "references", "work", "workers", "supplied", "attention", "history",
        "operations", "legacy", "foreign",
    )
    for name in lists:
        if not isinstance(doc[name], list):
            raise Problem(name, "must be a list")
    exact(doc["catalog"], {"path", "sha256", "bytes"}, "catalog")
    return {"doc": doc, "root": root, "tools": tools}


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
    except Problem as exc:
        doc = refuse(command, observed, exc.check, exc.message)
        doc["inspectability"]["request_sha256"] = request_sha
        return doc
    book = Book(parsed["root"], parsed["tools"])
    req = parsed["doc"]
    try:
        prepared = prepare(req, book)
        return finish(command, work_id, observed, request_sha, book, req, prepared)
    except Problem as exc:
        doc = refuse(command, observed, exc.check, exc.message)
        doc["inspectability"]["request_sha256"] = request_sha
        doc["coverage"] = book.coverage
        doc["instance"] = {"root": book.root, "book": req["instance"]["book"], "role": req["instance"]["role"], "tools_root": book.tools_root}
        return doc


def prepare(req: dict, book: Book) -> dict:
    check_ids(req["references"], "references")
    check_ids(req["work"], "work")
    check_ids(req["workers"], "workers")
    check_ids(req["supplied"], "supplied")
    check_ids(req["attention"], "attention")
    check_ids(req["history"], "history")
    check_ids(req["operations"], "operations")
    check_ids(req["legacy"], "legacy")
    check_ids(req["foreign"], "foreign")
    work_ids = [item["id"] for item in req["work"]]
    if len(work_ids) != len(set(work_ids)):
        raise Problem("work", "duplicate work id")
    for index, item in enumerate(req["references"]):
        exact(item, {"id", "role", "path", "sha256", "bytes", "label"}, f"references[{index}]")
        if item["role"] not in ROLES:
            raise Problem(f"references[{index}]", "unknown role")
        short_text(item["label"], LABEL_MAX, f"references[{index}].label")
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
            if item[key] not in ("unknown", "supplied-not-verified") and not isinstance(item[key], str):
                raise Problem(f"operations[{index}]", f"{key} must be a string")
            if not isinstance(item[key], str) or len(item[key]) > 80:
                raise Problem(f"operations[{index}]", f"{key} is too long")
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
    return {"ok": True}


def selector_body(book: Book, row: dict) -> dict | None:
    if row["status"] != "matched" or row["data"] is None:
        return None
    try:
        body = loads(row["data"], "prime-desk-selector/1")
        exact(body, {"schema", "selected_work_id", "checkpoint", "verified_result", "next_route"}, "prime-desk-selector/1")
    except Problem as exc:
        book.add_gap("selector-shape", exc.check, exc.message, row["path"], "observed")
        return None
    if body["schema"] != SELECTOR_SCHEMA:
        book.add_gap("selector-shape", "prime-desk-selector/1", "unsupported selector schema", row["path"], "observed")
        return None
    if not is_label(body["selected_work_id"], 80):
        book.add_gap("selector-shape", "prime-desk-selector/1", "selected_work_id must be a label", row["path"], "observed")
        return None
    for key in ("checkpoint", "verified_result"):
        if body[key] is not None:
            exact(body[key], {"path", "sha256", "bytes"}, f"selector.{key}")
    if body["next_route"] is not None:
        exact(body["next_route"], {"path", "sha256", "bytes", "speaker"}, "selector.next_route")
        short_text(body["next_route"]["speaker"], 80, "selector.next_route.speaker")
    return body


def read_pointer(book: Book, pointer: dict | None, label: str) -> dict | None:
    if pointer is None:
        return None
    return book.take(book.root, pointer["path"], pointer["sha256"], pointer["bytes"], label)


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
        fact["basis"] = "observed"
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
            exact(item, {"work_id", "address", "label"}, f"catalog.items[{index}]")
            if not is_label(item["work_id"], 80):
                raise Problem(f"catalog.items[{index}]", "work_id must be a label")
            short_text(item["address"], LABEL_MAX, f"catalog.items[{index}].address")
            short_text(item["label"], LABEL_MAX, f"catalog.items[{index}].label")
        except Problem as exc:
            book.add_gap("catalog-shape", exc.check, exc.message, row["path"], "observed")
            return None
        if item["work_id"] in seen:
            book.add_gap("catalog-shape", CATALOG_SCHEMA, f"duplicate catalog work_id {item['work_id']}", row["path"], "observed")
            return None
        seen.add(item["work_id"])
        items.append({"work_id": item["work_id"], "address": item["address"], "label": item["label"], "basis": "observed"})
    return {"path": row["path"], "sha256": row["sha256"], "bytes": row["bytes"], "basis": "observed", "items": items}


def assignment_fields(book: Book, row: dict) -> dict:
    out = file_fact(row)
    out["reader"] = "app-context.parse_assignment"
    out["fields"] = None
    out["limit"] = "assignment_state is a record field, not a live process check. validate_context was not called."
    if book.tools_root is None:
        out["limit"] = "tools_root is null; parse_assignment was not loaded. " + out["limit"]
        return out
    if row["status"] != "matched" or row["data"] is None:
        out["limit"] = "assignment bytes were not accepted. " + out["limit"]
        return out
    module, problem = load_module(book.tools_root, "app-context")
    if module is None:
        book.add_gap("reader-pin", "app-context", problem or "reader not loaded", row["path"], "unknown")
        out["limit"] = problem
        return out
    buffer = io.StringIO()
    old = sys.stderr
    sys.stderr = buffer
    try:
        fields = module.parse_assignment(row["data"])
    except SystemExit:
        book.add_gap("assignment-record", "app-context.parse_assignment", buffer.getvalue().strip() or "reader refused the record", row["path"], "observed")
        out["limit"] = "parse_assignment refused this file. " + out["limit"]
        return out
    finally:
        sys.stderr = old
    out["fields"] = {
        "current_work": fields.get("current_work"),
        "assignment_state": fields.get("assignment_state"),
        "pack": fields.get("pack"),
        "updated": fields.get("updated"),
        "basis": "observed",
    }
    return out


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
    if book.tools_root is None:
        out["limit"] = "tools_root is null; the reader module was not loaded"
        return out
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
            if token != "desk-state/1":
                out["limit"] = "schema token is not desk-state/1. " + out["limit"]
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
    base = book.tools_root or book.root
    row = book.take(base, item["path"], item["sha256"], item["bytes"], f"operations:{item['id']}")
    past = item["past_tests"]
    activation = item["activation"]
    past_basis = "unknown" if past == "unknown" else "supplied"
    activation_basis = "unknown" if activation == "unknown" else "supplied"
    if past not in ("unknown", "supplied-not-verified"):
        past_basis = "supplied"
    if activation not in ("unknown", "supplied-not-verified"):
        activation_basis = "supplied"
    return {
        "id": item["id"],
        "name": item["name"],
        "source": file_fact(row),
        "limitation": item["limitation"],
        "limitation_basis": "supplied",
        "past_tests": past,
        "past_tests_basis": past_basis,
        "activation": activation,
        "activation_basis": activation_basis,
        "executed": False,
        "recognized_token": past in ("unknown", "supplied-not-verified") and activation in ("unknown", "supplied-not-verified"),
    }


def flag_operation(book: Book, row: dict) -> dict:
    if not row["recognized_token"]:
        book.add_gap(
            "operation-label",
            f"operations:{row['id']}",
            "past_tests or activation is not unknown or supplied-not-verified. The token is not a passed test and not a live activation.",
            (row.get("source") or {}).get("path"),
            "supplied",
        )
    return row


def finish(command: str, work_id: str | None, observed: str, request_sha: str, book: Book, req: dict, _prepared: dict) -> dict:
    selector_row = book.take(book.root, req["selector"]["path"], req["selector"]["sha256"], req["selector"]["bytes"], "selector")
    try:
        body = selector_body(book, selector_row)
    except Problem as exc:
        book.add_gap("selector-shape", exc.check, exc.message, selector_row["path"], "observed")
        body = None
    work_rows = []
    for item in req["work"]:
        row = book.take(book.root, item["path"], item["sha256"], item["bytes"], f"work:{item['id']}")
        work_rows.append((item, row))
    by_id = {item["id"]: (item, row) for item, row in work_rows}
    addresses: dict[str, list[str]] = {}
    for item, _row in work_rows:
        addresses.setdefault(item["address"], []).append(item["id"])
    for address, ids in addresses.items():
        if len(ids) > 1:
            book.add_gap(
                "same-address",
                "work.address",
                f"address {address} is declared for {', '.join(ids)}. Only the selector id can be current.",
                None,
                "observed",
            )
    selected = None
    selected_item = None
    selected_row = None
    if body is not None:
        chosen = body["selected_work_id"]
        if chosen not in by_id:
            book.add_gap("selector", "prime-desk-selector/1", f"selected_work_id {chosen} is not in this request", selector_row["path"], "observed")
        else:
            selected_item, selected_row = by_id[chosen]
            if selected_row["status"] == "matched":
                selected = {
                    "id": chosen,
                    "address": selected_item["address"],
                    "source": file_fact(selected_row),
                    "basis": "observed",
                    "rule": "prime-desk-selector/1",
                }
            else:
                book.add_gap("selector", "work", f"selected work {chosen} bytes were not accepted", selected_item["path"], selected_row["basis"])
    not_selected = []
    current_id = None if selected is None else selected["id"]
    for item, row in work_rows:
        if item["id"] == current_id:
            continue
        not_selected.append({
            "id": item["id"],
            "address": item["address"],
            "source": file_fact(row),
            "reason": "not the canonical selector",
            "basis": "observed",
        })
    checkpoint = verified = next_route = None
    if body is not None:
        checkpoint_row = read_pointer(book, body["checkpoint"], "checkpoint")
        verified_row = read_pointer(book, body["verified_result"], "verified_result")
        next_row = read_pointer(book, body["next_route"], "next_route")
        if body["checkpoint"] is None:
            checkpoint = {"basis": "unknown", "source": None}
            book.add_gap("checkpoint", "selector.checkpoint", "no checkpoint is declared", None, "unknown")
        elif checkpoint_row is not None:
            checkpoint = {"basis": checkpoint_row["basis"], "source": file_fact(checkpoint_row)}
        if body["verified_result"] is None:
            verified = {"basis": "unknown", "source": None, "limit": "missing verification is unknown, not a clean bill of health"}
            book.add_gap("verification", "selector.verified_result", "verified result is null", None, "unknown")
        elif verified_row is not None:
            verified = {
                "basis": verified_row["basis"],
                "source": file_fact(verified_row),
                "limit": "a matching hash proves these bytes, not acceptance or process freshness",
            }
        if body["next_route"] is None:
            next_route = {"basis": "unknown", "speaker": None, "source": None}
        elif next_row is not None:
            next_route = {
                "basis": "supplied" if next_row["status"] == "matched" else next_row["basis"],
                "speaker": body["next_route"]["speaker"],
                "source": file_fact(next_row),
                "limit": "speaker text is supplied route wording, not a command this tool runs",
            }
    catalog_row = book.take(book.root, req["catalog"]["path"], req["catalog"]["sha256"], req["catalog"]["bytes"], "catalog")
    catalog = catalog_body(book, catalog_row)
    if catalog is not None and current_id is not None:
        for item in catalog["items"]:
            if item["work_id"] != current_id:
                book.add_gap(
                    "catalog-not-chosen",
                    CATALOG_SCHEMA,
                    f"catalog names {item['work_id']}; selector names {current_id}. The selector is kept.",
                    catalog_row["path"],
                    "observed",
                )
    elif catalog is None and catalog_row["status"] == "matched":
        pass
    references = []
    assignment_reader = []
    for item in req["references"]:
        row = book.take(book.root, item["path"], item["sha256"], item["bytes"], f"references:{item['id']}")
        rec = {
            "id": item["id"],
            "role": item["role"],
            "label": item["label"],
            "label_basis": "supplied",
            "source": file_fact(row),
        }
        if item["role"] == "talk":
            rec["parsed"] = False
            rec["executable"] = False
            rec["limit"] = "talk is not parsed and is not executable"
        if item["role"] in ("return", "receipt") and row["status"] != "matched":
            book.add_gap(item["role"], f"references:{item['id']}", f"{item['role']} is {row['status']}", item["path"], row["basis"])
        if item["role"] == "assignment":
            assignment_reader.append(assignment_fields(book, row))
        references.append(rec)
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
    workers = []
    supplied_by = {}
    for item in req["supplied"]:
        supplied_by.setdefault(item["about"], []).append({
            "id": item["id"],
            "speaker": item["speaker"],
            "text": item["text"],
            "limit": item["limit"],
            "basis": "supplied",
        })
    for item in req["workers"]:
        if item["evidence"] is None:
            evidence = {"path": None, "status": "absent", "basis": "unknown", "sha256": None, "bytes": None, "recorded_state": None, "note": None, "process_activity": "unknown"}
            book.add_gap("worker-unknown", f"workers:{item['id']}", "no recorded evidence file; process activity is unknown", None, "unknown")
        else:
            row = book.take(
                book.root,
                item["evidence"]["path"],
                item["evidence"]["sha256"],
                item["evidence"]["bytes"],
                f"workers:{item['id']}",
            )
            evidence = evidence_state(book, row)
        workers.append({
            "id": item["id"],
            "work_id": item["work_id"],
            "declared_on_selected": current_id is not None and item["work_id"] == current_id,
            "evidence": evidence,
            "supplied": supplied_by.get(item["id"], []),
            "process_activity": "unknown",
            "process_basis": "unknown",
        })
    operations = [flag_operation(book, operation_row(book, item)) for item in req["operations"]]
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
        same = item["root"] == book.root or os.path.normcase(os.path.abspath(item["root"])) == os.path.normcase(book.root)
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
    open_attention = [item for item in attention if item["open"]]
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
            packet = {
                "work_id": selected["id"],
                "assignment": quote_text(selected_row),
                "criteria": [quote_text_from_ref(book, item) for item in references if item["role"] == "criteria"],
                "director": [quote_text_from_ref(book, item) for item in references if item["role"] == "director"],
                "model": [quote_text_from_ref(book, item) for item in references if item["role"] == "model"],
                "returns": [item for item in references if item["role"] in ("return", "deliverable")],
                "receipts": [item for item in references if item["role"] == "receipt"],
                "verification": [item for item in references if item["role"] == "verification"],
                "findings": [item for item in references if item["role"] == "finding"],
                "dependencies": [item for item in references if item["role"] == "dependency"],
                "review_home": [item for item in references if item["role"] == "review-home"],
                "next_routes": [item for item in references if item["role"] == "next"],
                "assignment_reader": assignment_reader,
            }
            if not packet["verification"] and (verified is None or verified.get("basis") == "unknown"):
                packet["verification_limit"] = "no verification source matched; this is unknown, not a pass"
            else:
                packet["verification_limit"] = "verification bytes are evidence of those bytes only"
    schema = VIEW_SCHEMA if command == "view" else PACKET_SCHEMA
    exit_code = 1 if open_attention or book.gaps or packet_refused else 0
    if body is None and selector_row["status"] != "matched":
        state = "partial"
    elif book.gaps or open_attention or packet_refused:
        state = "partial" if body is None else "attention"
    else:
        state = "ready"
    correction = "None of the declared open items blocks reading. This view still grants nothing."
    if exit_code != 0:
        correction = "Read the gaps and open attention. Restore or explicitly rehash a stale source. Do not treat a supplied label as process activity. " + ESCALATION
    doc = {
        "schema": schema,
        "command": command,
        "state": state,
        "exit": exit_code,
        "check": "prime-desk-request/1",
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
        "selected": None if selected is None else {
            **selected,
            "checkpoint": checkpoint,
            "verified_result": verified,
            "next_route": next_route,
        },
        "not_selected": not_selected,
        "catalog": None if catalog is None else {
            "source": file_fact(catalog_row),
            "items": catalog["items"] if catalog else [],
            "used_for_selection": False,
        },
        "attention": attention,
        "gaps": book.gaps,
        "workers": workers,
        "operations": operations,
        "record": {
            "references": strip_data(references),
            "history": history,
            "history_inlined": False,
            "talk_parsed": False,
            "assignment_reader": assignment_reader,
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
    return doc


def quote_text_from_ref(book: Book, item: dict) -> dict:
    source = dict(item["source"])
    if source["status"] != "matched":
        return {
            "id": item["id"],
            "role": item["role"],
            "source": source,
            "text": None,
            "quoted": False,
            "reason": "source bytes were not accepted",
        }
    full = os.path.abspath(os.path.join(book.root, *source["path"].split("/")))
    status, first, _second = read_twice(full)
    if status != "bytes" or first is None or sha256_bytes(first) != source["sha256"]:
        book.add_gap("changed", item["id"], "bytes changed before quoting; withheld", source["path"], "changed")
        changed = {**source, "status": "changed", "basis": "changed"}
        return {
            "id": item["id"],
            "role": item["role"],
            "source": changed,
            "text": None,
            "quoted": False,
            "reason": "changed before quote",
        }
    fact = quote_text({
        "status": "matched",
        "basis": "observed",
        "path": source["path"],
        "sha256": source["sha256"],
        "bytes": len(first),
        "data": first,
    })
    return {"id": item["id"], "role": item["role"], "source": source, **fact}


def strip_data(references: list[dict]) -> list[dict]:
    out = []
    for item in references:
        copy = dict(item)
        out.append(copy)
    return out


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
        lines = [
            "# Prime desk refusal",
            "",
            f"Check: {doc['check']}",
            f"State: {doc['state']}",
            "",
            doc["correction"],
            "",
        ]
        return "\n".join(lines)
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
        lines.append("Selected work: unknown. The selector was not accepted.")
    else:
        lines.append(f"Selected: {selected['id']} `{selected['address']}`.")
        lines.append(f"Source: {source_line(selected['source'])}.")
        lines.append(f"Checkpoint: {source_line((selected.get('checkpoint') or {}).get('source'))}. Basis {(selected.get('checkpoint') or {}).get('basis')}.")
        verified = selected.get("verified_result") or {}
        lines.append(f"Verified result: {source_line(verified.get('source'))}. Basis {verified.get('basis')}. {verified.get('limit') or ''}")
        nxt = selected.get("next_route") or {}
        lines.append(f"Next route: speaker {nxt.get('speaker')} {source_line(nxt.get('source'))}. Basis {nxt.get('basis')}.")
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
            f"({source_line(evidence)}). Process activity: unknown."
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
    for role in ("director", "model", "talk"):
        rows = [item for item in record.get("references", []) if item["role"] == role]
        if not rows:
            lines.append(f"{role}: none declared.")
        for item in rows:
            extra = ""
            if role == "talk":
                extra = " Not parsed. Not executable."
            if role == "model":
                extra = " Separate from the Director source."
            lines.append(f"{role}: {item['label']} ({source_line(item['source'])}).{extra}")
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
        lines.append("None declared.")
    for item in packet["criteria"]:
        lines.append(quote_block(item))
    lines.append("### Director wording")
    if not packet["director"]:
        lines.append("None declared.")
    for item in packet["director"]:
        lines.append(f"{item['id']} {source_line(item.get('source'))}")
        lines.append(quote_block(item))
    lines.append("### Model explanation")
    lines.append("This section is separate from Director wording.")
    if not packet["model"]:
        lines.append("None declared.")
    for item in packet["model"]:
        lines.append(f"{item['id']} {source_line(item.get('source'))}")
        lines.append(quote_block(item))
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
    lines.extend(ref_lines(packet["review_home"]))
    lines.append("### Next routes")
    lines.extend(ref_lines(packet["next_routes"]))
    reader = packet.get("assignment_reader") or []
    if reader:
        lines.append("### Assignment reader")
        for item in reader:
            fields = item.get("fields") or {}
            lines.append(
                f"current_work `{fields.get('current_work')}` assignment_state `{fields.get('assignment_state')}` "
                f"basis {fields.get('basis')}. {item.get('limit')}"
            )
    return lines


def quote_block(item: dict) -> str:
    if item.get("quoted") and item.get("text") is not None:
        return fenced(item["text"])
    reason = item.get("reason") or "not quoted"
    return f"Not quoted. {reason} {source_line(item if 'path' in item else item.get('source'))}"


def ref_lines(items: list[dict]) -> list[str]:
    if not items:
        return ["None declared."]
    return [f"- {item['id']}: {item['label']} ({source_line(item['source'])})." for item in items]


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
            value = args[index + 1]
            if flag == "--request":
                request = value
            else:
                work_id = value
            index += 2
            continue
        return emit(refuse(command, observed, "arguments", f"unknown argument {flag}"), as_json)
    if request is None:
        return emit(refuse(command, observed, "--request", "missing --request"), as_json)
    doc = assemble(request, command, work_id)
    return emit(doc, as_json)


if __name__ == "__main__":
    sys.exit(main())
