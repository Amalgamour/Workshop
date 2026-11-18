#!/usr/bin/env python3
"""Line/pass return route, schema return-line-capture/1.

Reserve, capture, verify, and look up one pass on a matching line.
Stage and adopt a migration from a backup outside the book.
A receipt is a byte check. It is not approval, acceptance, seating,
publication, or finish. This tool does not call the sequential allocator.
"""

from __future__ import annotations

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


SCHEMA = "return-line-capture/1"
DESCRIPTOR_SCHEMA = "return-line-descriptor/1"
RESULT_SCHEMA = "return-line-result/1"
LAYOUT_SCHEMA = "return-line-layout/1"
PLAN_SCHEMA = "return-line-plan/1"
TOOL_PATH = "labs/return-lines-pass01/return_lines.py"
LAYOUT_NAME = "return-line-layout.json"
INDEX_NAME = "return-line-index.json"
MIGRATION_NAME = "return-line-migration.json"
STAGE_JOURNAL = "stage-journal.json"
STAGE_MARKER = "stage-complete.json"
ADOPT_JOURNAL = "adopt-journal.json"
ADOPT_MARKER = "adopt-complete.json"
DOOR = "0100.band.returns"
ESCALATION = (
    "Escalation: Codex Prime on 0521.return-placement/05.03. "
    "This tool does not decide meaning, acceptance, or live authority."
)
PLACEMENT_SHA = "db96f7023c73dcececba0e7d42b821da8193af7534a4bdf8cd2e5d6cd53d0754"
PLACEMENT_BYTES = 66097
READER_SHA = "8f3da5c651f6924fca6dedb0b95da7d181eb58884dc030dd9cbc3d8b6a5b15ac"
READER_BYTES = 45767
REPARSE = 0x400

LAYOUT_KEYS = {"schema", "book", "allocation", "sequential_allocation", "bands"}
ORIGIN_KEYS = {"book", "page", "batch"}
LINE_KEYS = {
    "workflow_space", "target_page", "target_number", "subject", "route",
    "pass", "return_path", "custody_dir",
}
RESERVATION_KEYS = {
    "schema", "kind", "submission_id", "origin", "expected_outputs",
    "submitter", "reviewer", "release", "supersedes", "reserved_at",
    "line", "sequential_allocation",
}
MANIFEST_KEYS = {
    "schema", "kind", "submission_id", "reservation_sha256", "return",
    "source_commit", "captured_at", "sources", "omitted", "required",
}
RETURN_KEYS = {"sha256", "bytes"}
SOURCE_KEYS = {"logical", "payload", "sha256", "bytes"}
RECEIPT_KEYS = {
    "schema", "kind", "submission_id", "reservation_sha256", "manifest_sha256",
    "return_sha256", "captured_at", "acceptance", "approved", "accepted", "published",
}
DESCRIPTOR_KEYS = {
    "schema", "origin", "route", "target_page", "return_path", "custody_path",
    "receipt_path", "manifest_path", "submission_id", "custody_format",
    "receipt_sha256", "return_sha256", "return_bytes", "state", "verification",
}
VERIFICATION_KEYS = {"tool_path", "tool_sha256", "result", "evidence_path"}
RESULT_KEYS = {
    "schema", "command", "check", "state", "exit", "correction", "evidence",
    "descriptor", "detail",
}
RELOCATION_KEYS = {
    "schema", "custody_format", "old_member", "original_destination",
    "reservation_destination_rewritten", "source_backup", "return_sha256",
    "return_bytes",
}
_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,63}$")
_PLACEMENT = None
_READER = None
_TOOL_SHA = None


class LineError(Exception):
    def __init__(self, check, reason, correction, evidence=None, exit_code=2,
                 state="refused", descriptor=None, detail=None):
        super().__init__(reason)
        self.check = check
        self.reason = reason
        self.correction = correction
        self.evidence = evidence
        self.exit_code = exit_code
        self.state = state
        self.descriptor = descriptor
        self.detail = detail or {}


def repo_root() -> str:
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.abspath(os.path.join(here, "..", ".."))


def live_book_path() -> str:
    return os.path.abspath(os.path.join(repo_root(), "00.kernel", "00.00.10.work"))


def norm(path: str) -> str:
    return os.path.normcase(os.path.normpath(path))


def within(parent: str, child: str) -> bool:
    try:
        parent_n = norm(os.path.abspath(parent))
        child_n = norm(os.path.abspath(child))
        return os.path.commonpath([parent_n, child_n]) == parent_n
    except ValueError:
        return False


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def is_reparse(path: str) -> bool:
    st = os.lstat(path)
    attrs = getattr(st, "st_file_attributes", 0) or 0
    if attrs & REPARSE:
        return True
    return stat.S_ISLNK(st.st_mode)


def dump(obj: object) -> bytes:
    text = json.dumps(obj, ensure_ascii=False, sort_keys=True, indent=2, allow_nan=False)
    return (text + "\n").encode("utf-8")


def loads(data: bytes, check: str):
    def reject(name: str):
        raise LineError(check, f"nonfinite JSON {name}", "Replace the record with finite JSON.")

    def pairs(seq):
        obj = {}
        for key, value in seq:
            if not isinstance(key, str) or key in obj:
                raise LineError(check, "JSON keys are not unique strings", "Rewrite the record.")
            obj[key] = value
        return obj

    try:
        return json.loads(data.decode("utf-8"), object_pairs_hook=pairs, parse_constant=reject)
    except LineError:
        raise
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise LineError(check, f"invalid JSON: {exc}", "Restore the JSON record.") from exc


def expect_keys(body: object, keys: set[str], check: str, label: str) -> dict:
    if not isinstance(body, dict) or set(body) != keys:
        raise LineError(check, f"{label} keys do not match the contract", "Restore the record or write it again with this tool.")
    return body


def now_stamp() -> str:
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")


def tool_sha() -> str:
    global _TOOL_SHA
    if _TOOL_SHA is None:
        _TOOL_SHA = sha(read_exact(os.path.abspath(__file__)))
    return _TOOL_SHA


def read_exact(path: str) -> bytes:
    if not os.path.lexists(path):
        raise LineError("filesystem", f"missing {path}", "Restore the file before retrying.")
    if is_reparse(path):
        raise LineError("filesystem", f"link refused: {path}", "Use a regular file.")
    st = os.lstat(path)
    if not stat.S_ISREG(st.st_mode):
        raise LineError("filesystem", f"not a regular file: {path}", "Use a regular file.")
    if st.st_nlink != 1:
        raise LineError("filesystem", f"link count refused: {path}", "Use a file with link count 1.")
    with open(path, "rb") as handle:
        return handle.read()


def write_new(path: str, data: bytes) -> None:
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    flags = os.O_CREAT | os.O_EXCL | os.O_WRONLY
    if hasattr(os, "O_BINARY"):
        flags |= os.O_BINARY
    fd = os.open(path, flags)
    try:
        view = data
        while view:
            wrote = os.write(fd, view)
            view = view[wrote:]
    finally:
        os.close(fd)


def save_json(path: str, body: object) -> bytes:
    raw = dump(body)
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    tmp = path + ".tmp"
    if os.path.lexists(tmp):
        os.remove(tmp)
    write_new(tmp, raw)
    os.replace(tmp, path)
    return raw


def require_dir(path: str, label: str) -> str:
    absolute = os.path.abspath(path)
    if not os.path.lexists(absolute) or is_reparse(absolute) or not os.path.isdir(absolute):
        raise LineError("filesystem", f"{label} is not a directory", f"Pass an existing directory for {label}.")
    return absolute


def assert_contained(root: str, path: str) -> str:
    absolute = os.path.abspath(path)
    if not within(root, absolute):
        raise LineError("filesystem", "path escapes its root", "Keep the operation inside the declared root.")
    return absolute


def assert_mutable(book_abs: str) -> None:
    if norm(book_abs) == norm(live_book_path()):
        raise LineError(
            "live book",
            "mutating command refused on the live work book",
            "Use a disposable copy. Prime reviews the read-only plan before any live operation.",
        )
    door = os.path.join(book_abs, DOOR)
    if os.path.lexists(door):
        raise LineError(
            "live book",
            "book contains 0100.band.returns",
            "Do not mutate a book that still has the return door. Rehearse on a copy that omits it.",
        )


def load_module(rel: str, digest: str, size: int, name: str, check: str):
    here = os.path.dirname(os.path.abspath(__file__))
    path = os.path.abspath(os.path.join(here, rel))
    if not os.path.lexists(path) or is_reparse(path) or not os.path.isfile(path):
        raise LineError(check, "pinned file is missing", "Restore the pinned file. Do not substitute another reader.")
    data = read_exact(path)
    if sha(data) != digest or len(data) != size:
        raise LineError(check, "pinned file hash or length mismatch", "Restore the pinned bytes. Do not edit them in this pass.")
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise LineError(check, "pinned file did not load", "Restore the pinned file.")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def placement():
    global _PLACEMENT
    if _PLACEMENT is None:
        _PLACEMENT = load_module(
            os.path.join("..", "return-placement-pass01", "return_placement.py"),
            PLACEMENT_SHA, PLACEMENT_BYTES, "return_placement_pinned", "pinned placement mismatch",
        )
    return _PLACEMENT


def reader():
    global _READER
    if _READER is None:
        _READER = load_module(
            os.path.join("..", "return-capture-pass01", "return_capture.py"),
            READER_SHA, READER_BYTES, "return_capture_pinned", "pinned reader mismatch",
        )
    return _READER


def route_for(book_name: str, page: str, batch: str) -> dict:
    origin = {"book": book_name, "page": page, "batch": batch}
    try:
        return placement().compute_route(origin)
    except placement().PlacementError as exc:
        raise LineError(
            "return-placement-route/1",
            exc.reason,
            "Stop. Read 0417.return-placement/06.01.md. Do not invent a route for an undeclared band.",
        ) from exc


def valid_id(value: object) -> bool:
    return isinstance(value, str) and bool(_ID.fullmatch(value))


def valid_text(value: object) -> bool:
    if not isinstance(value, str) or value == "" or len(value) > 4096:
        return False
    return not any(ord(ch) < 32 or ord(ch) == 127 for ch in value)


def valid_logical(value: object) -> bool:
    if not isinstance(value, str) or value == "" or len(value) > 4096:
        return False
    if "\\" in value or value.startswith("/") or re.match(r"^[A-Za-z]:", value):
        return False
    if any(ord(ch) < 32 or ord(ch) == 127 for ch in value):
        return False
    for part in value.split("/"):
        if part in ("", ".", "..") or part.endswith(".") or part.endswith(" "):
            return False
    return True


def book_name_ok(name: object) -> bool:
    return isinstance(name, str) and bool(name) and len(name) <= 4096 and all(
        ch not in name for ch in "/\\\n\r"
    )


def layout_body(name: str) -> dict:
    return {
        "allocation": "line-pass",
        "bands": {"5": "matched-workflow-return-line", "7": "page-local-colab"},
        "book": name,
        "schema": LAYOUT_SCHEMA,
        "sequential_allocation": False,
    }


def read_layout(book_abs: str) -> dict:
    path = os.path.join(book_abs, LAYOUT_NAME)
    if not os.path.lexists(path):
        raise LineError(
            LAYOUT_SCHEMA,
            "layout is absent",
            "Run init on this book before reserve, capture, lookup, stage, or adopt.",
            evidence=LAYOUT_NAME,
        )
    body = expect_keys(loads(read_exact(path), LAYOUT_SCHEMA), LAYOUT_KEYS, LAYOUT_SCHEMA, "layout")
    if body["schema"] != LAYOUT_SCHEMA or body["allocation"] != "line-pass" or body["sequential_allocation"] is not False:
        raise LineError(LAYOUT_SCHEMA, "layout declaration is not line-pass", "Replace the layout with init on an empty declaration.")
    if body["bands"] != {"5": "matched-workflow-return-line", "7": "page-local-colab"}:
        raise LineError(LAYOUT_SCHEMA, "layout bands are not the declared pair", "Do not add a band in this tool.")
    if not book_name_ok(body["book"]):
        raise LineError(LAYOUT_SCHEMA, "layout book name is not usable", "Reinitialize with a plain book name.")
    return body


def occupants(book_abs: str, target_number: str, target_page: str) -> list[str]:
    found = []
    prefix = target_number + "."
    with os.scandir(book_abs) as entries:
        for entry in entries:
            if entry.name == target_page or not entry.name.startswith(prefix):
                continue
            path = entry.path
            if is_reparse(path):
                raise LineError("occupied-line", f"reparse occupant {entry.name}", "Remove the link from the book copy before retrying.")
            if entry.is_dir(follow_symlinks=False):
                found.append(entry.name)
    found.sort()
    return found


def join_book(book_abs: str, rel: str) -> str:
    parts = rel.split("/")
    if any(part in ("", ".", "..") for part in parts):
        raise LineError("filesystem", f"unsafe relative path {rel}", "Use a normalized book-relative path.")
    return assert_contained(book_abs, os.path.join(book_abs, *parts))


def descriptor(origin: dict, route_name: str, target_page: str, return_path: str,
               custody_path: str, receipt_path: str, manifest_path: str, submission_id: str | None,
               custody_format: str, receipt_sha256: str | None, return_sha256: str | None,
               return_bytes: int | None, state: str, evidence_path: str) -> dict:
    body = {
        "custody_format": custody_format,
        "custody_path": custody_path,
        "manifest_path": manifest_path,
        "origin": {"batch": origin["batch"], "book": origin["book"], "page": origin["page"]},
        "receipt_path": receipt_path,
        "receipt_sha256": receipt_sha256,
        "return_bytes": return_bytes,
        "return_path": return_path,
        "return_sha256": return_sha256,
        "route": route_name,
        "schema": DESCRIPTOR_SCHEMA,
        "state": state,
        "submission_id": submission_id,
        "target_page": target_page,
        "verification": {
            "evidence_path": evidence_path,
            "result": state,
            "tool_path": TOOL_PATH,
            "tool_sha256": tool_sha(),
        },
    }
    expect_keys(body, DESCRIPTOR_KEYS, DESCRIPTOR_SCHEMA, "descriptor")
    expect_keys(body["origin"], ORIGIN_KEYS, DESCRIPTOR_SCHEMA, "origin")
    expect_keys(body["verification"], VERIFICATION_KEYS, DESCRIPTOR_SCHEMA, "verification")
    if state not in {"complete", "reserved", "incomplete", "conflict"}:
        raise LineError(DESCRIPTOR_SCHEMA, "descriptor state is not declared", "Report the check instead of inventing a state.")
    return body


def envelope(command: str, check: str, state: str, exit_code: int, correction: str,
             evidence: str | None, described: dict | None, detail: dict | None) -> dict:
    if exit_code != 0 and "Escalation:" not in correction:
        correction = correction.rstrip() + " " + ESCALATION
    body_detail = dict(detail or {})
    body_detail.setdefault("acceptance", None)
    body_detail.setdefault("accepted", False)
    body_detail.setdefault("approved", False)
    body_detail.setdefault("published", False)
    body = {
        "check": check,
        "command": command,
        "correction": correction,
        "descriptor": described,
        "detail": body_detail,
        "evidence": evidence,
        "exit": exit_code,
        "schema": RESULT_SCHEMA,
        "state": state,
    }
    expect_keys(body, RESULT_KEYS, RESULT_SCHEMA, "result")
    return body


def guard(command: str, fn):
    try:
        return fn()
    except LineError as exc:
        return envelope(
            command, exc.check, exc.state, exc.exit_code, exc.correction,
            exc.evidence, exc.descriptor, exc.detail,
        )
    except OSError as exc:
        return envelope(
            command, "filesystem", "refused", 2,
            f"{type(exc).__name__}: {exc.strerror or exc}",
            None, None, {},
        )


def init_run(book: str, name: str) -> dict:
    def work():
        book_abs = require_dir(book, "book")
        assert_mutable(book_abs)
        if not book_name_ok(name):
            raise LineError(LAYOUT_SCHEMA, "book name is not usable", "Pass the book name, not a filesystem path.")
        path = os.path.join(book_abs, LAYOUT_NAME)
        raw = dump(layout_body(name))
        if os.path.lexists(path):
            current = read_exact(path)
            if current != raw:
                raise LineError(LAYOUT_SCHEMA, "layout bytes differ", "Do not overwrite a different declaration.", evidence=LAYOUT_NAME, state="conflict")
            return envelope("init", LAYOUT_SCHEMA, "complete", 0, "Layout already matches.", LAYOUT_NAME, None, {"rewritten": False})
        write_new(path, raw)
        return envelope("init", LAYOUT_SCHEMA, "complete", 0, "Layout written. This declaration is not custody.", LAYOUT_NAME, None, {"rewritten": False})
    return guard("init", work)


def reservation_identity(body: dict) -> tuple:
    origin = body["origin"]
    line = body["line"]
    return (
        body["submission_id"], origin["book"], origin["page"], origin["batch"],
        tuple(body["expected_outputs"]), body["submitter"], body["reviewer"],
        body["release"], body["supersedes"], line["target_page"], line["pass"], line["route"],
    )


def parse_reservation(data: bytes) -> dict:
    body = expect_keys(loads(data, SCHEMA), RESERVATION_KEYS, SCHEMA, "reservation")
    if body["schema"] != SCHEMA or body["kind"] != "reservation" or body["sequential_allocation"] is not False:
        raise LineError(SCHEMA + " reservation", "reservation schema is not return-line-capture/1", "Do not relabel a sealed /1 reservation.")
    if not valid_id(body["submission_id"]):
        raise LineError(SCHEMA + " reservation", "submission id is not usable", "Use one windows-safe submission id for this pass.")
    origin = expect_keys(body["origin"], ORIGIN_KEYS, SCHEMA, "origin")
    line = expect_keys(body["line"], LINE_KEYS, SCHEMA, "line")
    outputs = body["expected_outputs"]
    if not isinstance(outputs, list) or any(not valid_logical(item) for item in outputs):
        raise LineError(SCHEMA + " expected outputs", "expected outputs are not usable", "Pass logical names in order.")
    folded = [item.casefold() for item in outputs]
    if len(folded) != len(set(folded)):
        raise LineError(SCHEMA + " expected outputs", "expected outputs collide", "Use one name per output.")
    for label in ("submitter", "reviewer", "release"):
        if not valid_text(body[label]):
            raise LineError(SCHEMA + " reservation", f"{label} is not usable", "Pass a plain text value.")
    if body["supersedes"] is not None and not valid_id(body["supersedes"]):
        raise LineError(SCHEMA + " reservation", "supersedes is not usable", "Use null or a windows-safe id. This does not allocate a member.")
    if not isinstance(body["reserved_at"], str) or body["reserved_at"] == "":
        raise LineError(SCHEMA + " reservation", "reserved_at is empty", "Restore the reservation file.")
    for key in ORIGIN_KEYS:
        if not isinstance(origin[key], str) or origin[key] == "":
            raise LineError(SCHEMA + " reservation", "origin is not usable", "Restore the reservation.")
    for key in LINE_KEYS:
        if not isinstance(line[key], str) or line[key] == "":
            raise LineError(SCHEMA + " reservation", "line is not usable", "Restore the reservation.")
    return body


def file_sha(path: str) -> tuple[str | None, int | None]:
    if not os.path.lexists(path):
        return None, None
    data = read_exact(path)
    return sha(data), len(data)


def assess_new(book_abs: str, layout: dict, page: str, batch: str) -> dict:
    route = route_for(layout["book"], page, batch)
    custody_rel = route["custody_dir"]
    custody_abs = join_book(book_abs, custody_rel)
    res_abs = os.path.join(custody_abs, "reservation.json")
    man_abs = os.path.join(custody_abs, "manifest.json")
    rec_abs = os.path.join(custody_abs, "receipt.json")
    ret_abs = os.path.join(custody_abs, "return.md")
    tail_abs = join_book(book_abs, route["return_path"])
    evidence = f"{custody_rel}/reservation.json"
    origin = {"book": layout["book"], "page": page, "batch": batch}
    if not os.path.lexists(res_abs):
        described = descriptor(
            origin, route["route"], route["target_page"], route["return_path"], custody_rel,
            f"{custody_rel}/receipt.json", f"{custody_rel}/manifest.json", None, SCHEMA,
            None, None, None, "incomplete", evidence,
        )
        return {"route": route, "exit": 1, "state": "incomplete", "descriptor": described, "check": SCHEMA + " reservation"}
    reservation_bytes = read_exact(res_abs)
    reservation = parse_reservation(reservation_bytes)
    if reservation["origin"] != origin or reservation["line"]["return_path"] != route["return_path"]:
        raise LineError(SCHEMA + " reservation", "reservation origin does not match the route", "Do not reuse this pass for a different origin.", evidence=evidence, state="conflict")
    if reservation["line"]["target_page"] != route["target_page"] or reservation["line"]["pass"] != batch:
        raise LineError(SCHEMA + " reservation", "reservation line does not match the pass", "Keep one submission on this page and batch.", evidence=evidence, state="conflict")
    receipt_sha256, _ = file_sha(rec_abs) if os.path.lexists(rec_abs) else (None, None)
    return_sha256, return_bytes = file_sha(tail_abs) if os.path.lexists(tail_abs) else (None, None)
    problems = []
    if not os.path.lexists(rec_abs):
        partial = os.path.lexists(man_abs) or os.path.lexists(ret_abs) or os.path.lexists(os.path.join(custody_abs, "payload"))
        state = "incomplete" if partial else "reserved"
        described = descriptor(
            origin, route["route"], route["target_page"], route["return_path"], custody_rel,
            f"{custody_rel}/receipt.json", f"{custody_rel}/manifest.json", reservation["submission_id"],
            SCHEMA, None, return_sha256, return_bytes, state, evidence,
        )
        return {"route": route, "exit": 1, "state": state, "descriptor": described, "check": SCHEMA + " receipt", "reservation": reservation}
    try:
        manifest = expect_keys(loads(read_exact(man_abs), SCHEMA), MANIFEST_KEYS, SCHEMA, "manifest")
        receipt = expect_keys(loads(read_exact(rec_abs), SCHEMA), RECEIPT_KEYS, SCHEMA, "receipt")
        ret_meta = expect_keys(manifest["return"], RETURN_KEYS, SCHEMA, "return")
        if manifest["schema"] != SCHEMA or manifest["kind"] != "manifest":
            problems.append("manifest schema")
        if manifest["submission_id"] != reservation["submission_id"] or receipt["submission_id"] != reservation["submission_id"]:
            problems.append("submission")
        if manifest["reservation_sha256"] != sha(reservation_bytes) or receipt["reservation_sha256"] != sha(reservation_bytes):
            problems.append("reservation hash")
        if manifest["source_commit"] is not None or manifest["omitted"] != []:
            problems.append("manifest provenance")
        if manifest["required"] != reservation["expected_outputs"]:
            problems.append("expected outputs")
        sources = manifest["sources"]
        if not isinstance(sources, list) or [item.get("logical") if isinstance(item, dict) else None for item in sources] != manifest["required"]:
            problems.append("payload list")
        else:
            described_payloads = []
            for index, source in enumerate(sources, start=1):
                expect_keys(source, SOURCE_KEYS, SCHEMA, "source")
                payload_name = f"{index:04d}.blob"
                if source["payload"] != payload_name:
                    problems.append("payload name")
                payload_abs = os.path.join(custody_abs, "payload", payload_name)
                payload = read_exact(payload_abs)
                if sha(payload) != source["sha256"] or len(payload) != source["bytes"]:
                    problems.append(f"hash {payload_name}")
                described_payloads.append(payload_name)
            payload_dir = os.path.join(custody_abs, "payload")
            if sources and not os.path.isdir(payload_dir):
                problems.append("payload directory")
            if not sources and os.path.lexists(payload_dir):
                problems.append("unexpected payload")
            if os.path.isdir(payload_dir):
                present = sorted(name for name in os.listdir(payload_dir) if os.path.isfile(os.path.join(payload_dir, name)))
                if present != described_payloads:
                    problems.append("payload set")
        if not isinstance(ret_meta["bytes"], int) or not isinstance(ret_meta["sha256"], str):
            problems.append("return meta")
        custody_return = read_exact(ret_abs)
        tail = read_exact(tail_abs)
        if sha(custody_return) != ret_meta["sha256"] or len(custody_return) != ret_meta["bytes"]:
            problems.append("custody return")
        if tail != custody_return:
            problems.append("tail bytes")
        if receipt["schema"] != SCHEMA or receipt["kind"] != "receipt":
            problems.append("receipt schema")
        if receipt["manifest_sha256"] != sha(read_exact(man_abs)) or receipt["return_sha256"] != sha(tail):
            problems.append("receipt hash")
        if receipt["acceptance"] is not None or receipt["approved"] is not False or receipt["accepted"] is not False or receipt["published"] is not False:
            problems.append("acceptance flags")
        if not isinstance(receipt["captured_at"], str) or receipt["captured_at"] == "":
            problems.append("captured_at")
    except LineError as exc:
        problems.append(exc.reason)
    state = "complete" if not problems else "conflict"
    described = descriptor(
        origin, route["route"], route["target_page"], route["return_path"], custody_rel,
        f"{custody_rel}/receipt.json", f"{custody_rel}/manifest.json", reservation["submission_id"],
        SCHEMA, receipt_sha256, return_sha256, return_bytes, state, f"{custody_rel}/receipt.json",
    )
    return {
        "route": route, "exit": 0 if state == "complete" else 2, "state": state,
        "descriptor": described, "check": SCHEMA + " receipt", "reservation": reservation,
        "problems": problems,
    }


def refuse_occupied(book_abs: str, route: dict) -> None:
    found = occupants(book_abs, route["target_number"], route["target_page"])
    if found:
        raise LineError(
            "occupied-line",
            "target number has another directory: " + ", ".join(found),
            "Stage that occupant and adopt it before writing this line. Do not overwrite the subject.",
            evidence=found[0],
            state="conflict",
        )


def reserve_run(book: str, page: str, batch: str, submission: str, outputs: list[str],
                submitter: str, reviewer: str, release: str, supersedes: str | None) -> dict:
    def work():
        book_abs = require_dir(book, "book")
        assert_mutable(book_abs)
        layout = read_layout(book_abs)
        if not valid_id(submission):
            raise LineError(SCHEMA + " reservation", "submission id is not usable", "Use one windows-safe submission id.")
        if any(not valid_logical(item) for item in outputs):
            raise LineError(SCHEMA + " expected outputs", "expected outputs are not usable", "Pass logical names in order.")
        folded = [item.casefold() for item in outputs]
        if len(folded) != len(set(folded)):
            raise LineError(SCHEMA + " expected outputs", "expected outputs collide", "Use one name per output.")
        for label, value in (("submitter", submitter), ("reviewer", reviewer), ("release", release)):
            if not valid_text(value):
                raise LineError(SCHEMA + " reservation", f"{label} is not usable", "Pass a plain text value.")
        if supersedes is not None and not valid_id(supersedes):
            raise LineError(SCHEMA + " reservation", "supersedes is not usable", "Use null or a windows-safe id.")
        route = route_for(layout["book"], page, batch)
        refuse_occupied(book_abs, route)
        body = {
            "expected_outputs": list(outputs),
            "kind": "reservation",
            "line": {
                "custody_dir": route["custody_dir"],
                "pass": route["pass"],
                "return_path": route["return_path"],
                "route": route["route"],
                "subject": route["subject"],
                "target_number": route["target_number"],
                "target_page": route["target_page"],
                "workflow_space": route["workflow_space"],
            },
            "origin": {"batch": batch, "book": layout["book"], "page": page},
            "release": release,
            "reserved_at": now_stamp(),
            "reviewer": reviewer,
            "schema": SCHEMA,
            "sequential_allocation": False,
            "submission_id": submission,
            "submitter": submitter,
            "supersedes": supersedes,
        }
        raw = dump(body)
        path = join_book(book_abs, route["custody_dir"] + "/reservation.json")
        evidence = route["custody_dir"] + "/reservation.json"
        if os.path.lexists(path):
            existing = parse_reservation(read_exact(path))
            if reservation_identity(existing) != reservation_identity(body):
                raise LineError(
                    SCHEMA + " reservation",
                    "this pass already has a different reservation",
                    "Keep the sealed reservation. A conflicting pass is not written over it.",
                    evidence=evidence, state="conflict",
                )
            assessed = assess_new(book_abs, layout, page, batch)
            return envelope("reserve", SCHEMA + " reservation", assessed["state"], assessed["exit"],
                            "Reservation already matches. It was not rewritten.", evidence, assessed["descriptor"], {"rewritten": False})
        write_new(path, raw)
        assessed = assess_new(book_abs, layout, page, batch)
        return envelope("reserve", SCHEMA + " reservation", "reserved", 1,
                        "Reservation stored. Capture is still required. Reserved is not done.",
                        evidence, assessed["descriptor"], {"rewritten": False})
    return guard("reserve", work)


def next_attempt(book_abs: str, route: dict) -> str:
    root_rel = f"{route['target_page']}/{route['pass']}.refused"
    number = 1
    while os.path.lexists(join_book(book_abs, f"{root_rel}/attempt-{number:03d}")):
        number += 1
    return f"{root_rel}/attempt-{number:03d}"


def write_attempt(book_abs: str, route: dict, return_data: bytes, artifacts: list[tuple[str, bytes]], reason: str, sealed: str | None) -> str:
    rel = next_attempt(book_abs, route)
    write_new(join_book(book_abs, rel + "/return.md"), return_data)
    listed = []
    for index, (logical, data) in enumerate(artifacts, start=1):
        payload = f"{index:04d}.blob"
        write_new(join_book(book_abs, f"{rel}/payload/{payload}"), data)
        listed.append({"bytes": len(data), "logical": logical, "sha256": sha(data)})
    refusal = {
        "attempt_return_sha256": sha(return_data),
        "check": SCHEMA + " bytes",
        "outputs": listed,
        "reason": reason,
        "schema": "return-line-refusal/1",
        "sealed_return_sha256": sealed,
    }
    write_new(join_book(book_abs, rel + "/refusal.json"), dump(refusal))
    return rel


def capture_run(book: str, page: str, batch: str, submission: str, return_file: str,
                artifacts: list[tuple[str, str]]) -> dict:
    def work():
        book_abs = require_dir(book, "book")
        assert_mutable(book_abs)
        layout = read_layout(book_abs)
        route = route_for(layout["book"], page, batch)
        refuse_occupied(book_abs, route)
        res_abs = join_book(book_abs, route["custody_dir"] + "/reservation.json")
        if not os.path.lexists(res_abs):
            raise LineError(SCHEMA + " reservation", "reservation is absent", "Reserve this pass before capture.", evidence=route["custody_dir"] + "/reservation.json")
        reservation = parse_reservation(read_exact(res_abs))
        logicals = [item[0] for item in artifacts]
        if reservation["submission_id"] != submission or logicals != reservation["expected_outputs"]:
            raise LineError(
                SCHEMA + " expected outputs",
                "capture inputs do not match the reservation",
                "Pass the reserved submission and the expected outputs in the same order.",
                evidence=route["custody_dir"] + "/reservation.json", state="conflict",
            )
        return_data = read_exact(os.path.abspath(return_file))
        payload_bytes = [(logical, read_exact(os.path.abspath(path))) for logical, path in artifacts]
        assessed = assess_new(book_abs, layout, page, batch)
        if assessed["state"] == "complete":
            tail = read_exact(join_book(book_abs, route["return_path"]))
            same = tail == return_data
            if same:
                for index, (_logical, data) in enumerate(payload_bytes, start=1):
                    existing = read_exact(join_book(book_abs, f"{route['custody_dir']}/payload/{index:04d}.blob"))
                    if existing != data:
                        same = False
            if same:
                return envelope("capture", SCHEMA + " bytes", "complete", 0,
                                "Capture already matches. It was not rewritten.",
                                route["custody_dir"] + "/receipt.json", assessed["descriptor"], {"rewritten": False})
        if assessed["state"] in {"complete", "conflict"} or os.path.lexists(join_book(book_abs, route["return_path"])):
            sealed_sha, _ = file_sha(join_book(book_abs, route["return_path"])) if os.path.lexists(join_book(book_abs, route["return_path"])) else (None, None)
            if os.path.lexists(join_book(book_abs, route["return_path"])):
                existing_tail = read_exact(join_book(book_abs, route["return_path"]))
                if existing_tail != return_data or assessed["state"] == "complete":
                    rel = write_attempt(book_abs, route, return_data, payload_bytes, "conflicting bytes retained beside the sealed pass", sealed_sha)
                    fresh = assess_new(book_abs, layout, page, batch)
                    return envelope("capture", SCHEMA + " bytes", "conflict", 2,
                                    "Conflicting bytes were kept under the refused attempt. The sealed pass was not overwritten.",
                                    rel, fresh.get("descriptor"), {"rewritten": False})
        custody = route["custody_dir"]
        sources = []
        for index, (logical, data) in enumerate(payload_bytes, start=1):
            payload = f"{index:04d}.blob"
            dest = join_book(book_abs, f"{custody}/payload/{payload}")
            if os.path.lexists(dest) and read_exact(dest) != data:
                rel = write_attempt(book_abs, route, return_data, payload_bytes, "partial custody bytes differ", None)
                return envelope("capture", SCHEMA + " bytes", "conflict", 2,
                                "Partial custody bytes were kept. The new bytes are under the refused attempt.",
                                rel, assessed.get("descriptor"), {"rewritten": False})
            if not os.path.lexists(dest):
                write_new(dest, data)
            sources.append({"bytes": len(data), "logical": logical, "payload": payload, "sha256": sha(data)})
        ret_abs = join_book(book_abs, custody + "/return.md")
        if os.path.lexists(ret_abs) and read_exact(ret_abs) != return_data:
            rel = write_attempt(book_abs, route, return_data, payload_bytes, "custody return bytes differ", sha(read_exact(ret_abs)))
            return envelope("capture", SCHEMA + " bytes", "conflict", 2,
                            "The custody return was kept. The new bytes are under the refused attempt.",
                            rel, None, {"rewritten": False})
        if not os.path.lexists(ret_abs):
            write_new(ret_abs, return_data)
        tail_abs = join_book(book_abs, route["return_path"])
        if not os.path.lexists(tail_abs):
            write_new(tail_abs, return_data)
        manifest = {
            "captured_at": now_stamp(),
            "kind": "manifest",
            "omitted": [],
            "required": list(reservation["expected_outputs"]),
            "reservation_sha256": sha(read_exact(res_abs)),
            "return": {"bytes": len(return_data), "sha256": sha(return_data)},
            "schema": SCHEMA,
            "source_commit": None,
            "sources": sources,
            "submission_id": submission,
        }
        man_abs = join_book(book_abs, custody + "/manifest.json")
        if not os.path.lexists(man_abs):
            write_new(man_abs, dump(manifest))
        receipt = {
            "acceptance": None,
            "accepted": False,
            "approved": False,
            "captured_at": now_stamp(),
            "kind": "receipt",
            "manifest_sha256": sha(read_exact(man_abs)),
            "published": False,
            "reservation_sha256": sha(read_exact(res_abs)),
            "return_sha256": sha(return_data),
            "schema": SCHEMA,
            "submission_id": submission,
        }
        rec_abs = join_book(book_abs, custody + "/receipt.json")
        if not os.path.lexists(rec_abs):
            write_new(rec_abs, dump(receipt))
        fresh = assess_new(book_abs, layout, page, batch)
        if fresh["state"] != "complete":
            return envelope("capture", fresh["check"], fresh["state"], fresh["exit"],
                            "Capture wrote the files it could. The pass is not complete: " + ", ".join(fresh.get("problems") or []),
                            custody + "/receipt.json", fresh["descriptor"], {"problems": fresh.get("problems")})
        remember_index(book_abs, None, submission, fresh["descriptor"])
        return envelope("capture", SCHEMA + " receipt", "complete", 0,
                        "Receipt hashes match the written bytes. This is not acceptance.",
                        custody + "/receipt.json", fresh["descriptor"], {"rewritten": False})
    return guard("capture", work)


def verify_run(book: str, page: str, batch: str) -> dict:
    def work():
        book_abs = require_dir(book, "book")
        layout = read_layout(book_abs)
        legacy = assess_legacy_at(book_abs, layout, page, batch)
        if legacy is not None:
            return finish_assess("verify", legacy)
        assessed = assess_new(book_abs, layout, page, batch)
        return finish_assess("verify", assessed)
    return guard("verify", work)


def finish_assess(command: str, assessed: dict) -> dict:
    state = assessed["state"]
    if state == "complete":
        correction = "Observed checks passed. This is not acceptance, seating, or publication."
    elif state == "reserved":
        correction = "The pass is reserved. Capture it before treating it as done."
    elif state == "incomplete":
        correction = "Evidence is incomplete. Keep the record visible and do not invent the missing return."
    else:
        correction = "The recorded bytes do not verify. Keep them and correct the mismatch."
    return envelope(command, assessed["check"], state, assessed["exit"], correction,
                    assessed["descriptor"]["verification"]["evidence_path"], assessed["descriptor"],
                    {"problems": assessed.get("problems", [])})


def member_key(name: str) -> tuple:
    head, _, tail = name.partition(".")
    try:
        number = int(head)
    except ValueError:
        number = 10**9
    return (number, tail)


def load_audit(path: str) -> tuple[dict, str, int]:
    data = read_exact(os.path.abspath(path))
    body = loads(data, "audit identity")
    if not isinstance(body, dict) or body.get("schema") != "return-placement-audit/2":
        raise LineError("audit identity", "audit schema is not return-placement-audit/2", "Point stage at audit-corrected.json or a fixture of that schema.")
    if not isinstance(body.get("records"), list) or not isinstance(body.get("files"), list):
        raise LineError("audit identity", "audit records or files are missing", "Restore the audit.")
    return body, sha(data), len(data)


def split_member(path: str, names: set[str]) -> tuple[str | None, str | None]:
    normed = path.replace("\\", "/")
    for name in names:
        token = name + "/"
        index = normed.find(token)
        if index == 0 or (index > 0 and normed[index - 1] == "/"):
            return name, normed[index + len(token):]
    return None, None


def walk_files(root_abs: str) -> list[str]:
    found = []
    for dirpath, dirnames, filenames in os.walk(root_abs, followlinks=False):
        dirnames[:] = [name for name in dirnames if not is_reparse(os.path.join(dirpath, name))]
        for name in dirnames:
            path = os.path.join(dirpath, name)
            if is_reparse(path):
                raise LineError("filesystem", f"link refused: {path}", "Do not walk a reparse point.")
        for name in filenames:
            path = os.path.join(dirpath, name)
            assert_contained(root_abs, path)
            read_exact(path)
            rel = os.path.relpath(path, root_abs).replace("\\", "/")
            found.append(rel)
    found.sort()
    return found


def require_backup(book_abs: str, backup: str) -> str:
    backup_abs = os.path.abspath(backup)
    parent = os.path.dirname(backup_abs)
    if not os.path.isdir(backup_abs):
        if os.path.lexists(backup_abs):
            raise LineError("filesystem", "backup is not a directory", "Pass a backup directory outside the book.")
        if not parent or not os.path.isdir(parent):
            raise LineError("filesystem", "backup parent is missing", "Create the parent, not the live book.")
        os.makedirs(backup_abs)
    if is_reparse(backup_abs):
        raise LineError("filesystem", "backup is a link", "Use a real directory.")
    if within(book_abs, backup_abs) or within(backup_abs, book_abs):
        raise LineError("filesystem", "book and backup contain each other", "Place the backup outside the book.")
    live = live_book_path()
    if within(live, backup_abs) or norm(backup_abs) == norm(live):
        raise LineError("live book", "backup is inside the live work book", "Place the backup outside the live book.")
    if os.path.lexists(os.path.join(backup_abs, DOOR)):
        raise LineError("live book", "backup contains 0100.band.returns", "Do not use the live door as a backup.")
    return backup_abs


def reader_reason(member_abs: str) -> str | None:
    module = reader()
    try:
        module.verify_member(Path(member_abs))
    except module.Refusal as exc:
        text = str(exc).strip().splitlines()
        return text[0] if text else "reader refused"
    return None


def new_stage_journal(audit_sha: str, audit_bytes: int, book_name: str) -> dict:
    return {
        "audit_bytes": audit_bytes,
        "audit_sha256": audit_sha,
        "blocked": [],
        "book": book_name,
        "checks": [],
        "complete": False,
        "copied_count": 0,
        "files": [],
        "interrupted": False,
        "schema": "return-line-stage-journal/1",
    }


def stage_paths(backup_abs: str) -> tuple[str, str]:
    return os.path.join(backup_abs, STAGE_JOURNAL), os.path.join(backup_abs, STAGE_MARKER)


def load_json_file(path: str, check: str) -> dict | None:
    if not os.path.lexists(path):
        return None
    body = loads(read_exact(path), check)
    if not isinstance(body, dict):
        raise LineError(check, "journal is not an object", "Restore the journal.")
    return body


def prepare_records(layout: dict, audit: dict) -> list[tuple[dict, dict]]:
    prepared = []
    blocked = []
    for record in audit["records"]:
        if not isinstance(record, dict) or not isinstance(record.get("old_member"), str):
            blocked.append({"check": "audit identity", "evidence": None, "reason": "record has no old_member"})
            continue
        origin = record.get("origin")
        try:
            route = route_for(layout["book"], origin.get("page") if isinstance(origin, dict) else "", origin.get("batch") if isinstance(origin, dict) else "")
        except LineError as exc:
            blocked.append({"check": exc.check, "evidence": record["old_member"], "reason": exc.reason})
            continue
        if not isinstance(origin, dict) or origin.get("book") != layout["book"]:
            blocked.append({"check": "audit identity", "evidence": record["old_member"], "reason": "origin book does not match the layout"})
        elif route["route"] != record.get("route") or route["return_path"] != record.get("target_return"):
            blocked.append({
                "check": "audit identity",
                "evidence": record["old_member"],
                "reason": "audit route disagrees with compute_route",
            })
        else:
            prepared.append((record, route))
    prepared.sort(key=lambda item: member_key(item[0]["old_member"]))
    return prepared, blocked


def journal_file(journal: dict, backup_rel: str) -> dict | None:
    for item in journal["files"]:
        if item.get("backup_rel") == backup_rel:
            return item
    return None


def copy_evidence(src: str, dest: str, journal: dict, backup_rel: str, kind: str, source: str,
                  audit_sha256: str | None, audit_bytes: int | None, match: bool) -> bool:
    """Copy one file. Return True when this call wrote bytes."""
    data = read_exact(src)
    digest, size = sha(data), len(data)
    wrote = False
    if os.path.lexists(dest):
        current = read_exact(dest)
        if sha(current) != digest:
            if match:
                raise LineError("return-line-stage-journal/1", "backup bytes differ from the source", "Keep the backup evidence. Do not overwrite it.", evidence=backup_rel, state="conflict")
        # Mismatch evidence is kept. A matching source may replace nothing if the backup already matches.
        if current != data and match:
            raise LineError("return-line-stage-journal/1", "backup bytes differ from the source", "Keep the backup evidence.", evidence=backup_rel, state="conflict")
    else:
        write_new(dest, data)
        wrote = True
    row = journal_file(journal, backup_rel)
    body = {
        "audit_bytes": audit_bytes,
        "audit_sha256": audit_sha256,
        "backup_rel": backup_rel,
        "bytes": size,
        "kind": kind,
        "match": match and digest == audit_sha256 and size == audit_bytes if audit_sha256 else match,
        "sha256": digest,
        "source": source,
    }
    if row is None:
        journal["files"].append(body)
    else:
        row.update(body)
    if wrote:
        journal["copied_count"] = journal.get("copied_count", 0) + 1
    return wrote


def stage_run(book: str, backup: str, audit_path: str, interrupt_after: int | None = None, resume: bool = False) -> dict:
    command = "stage-resume" if resume else "stage"

    def work():
        book_abs = require_dir(book, "book")
        assert_mutable(book_abs)
        backup_abs = require_backup(book_abs, backup)
        layout = read_layout(book_abs)
        audit, audit_sha256, audit_bytes = load_audit(audit_path)
        journal_path, marker_path = stage_paths(backup_abs)
        existing = load_json_file(journal_path, "return-line-stage-journal/1")
        if existing is None:
            journal = new_stage_journal(audit_sha256, audit_bytes, layout["book"])
        else:
            journal = existing
            if journal.get("audit_sha256") != audit_sha256 or journal.get("audit_bytes") != audit_bytes:
                raise LineError("audit identity", "audit hash differs from the stage journal", "Keep this journal with the audit it names.", evidence=STAGE_JOURNAL, state="conflict")
        if os.path.lexists(marker_path):
            marker = load_json_file(marker_path, "return-line-stage-complete/1")
            if marker and marker.get("audit_sha256") == audit_sha256 and marker.get("journal_sha256") == sha(read_exact(journal_path)):
                return envelope(command, "return-line-stage-complete/1", "complete", 0,
                                "Stage marker already matches. This is not adoption and not acceptance.",
                                STAGE_MARKER, None, {"file_count": marker.get("file_count"), "source_count": marker.get("source_count")})
        prepared, blocked = prepare_records(layout, audit)
        if blocked:
            journal["blocked"] = blocked
            journal["complete"] = False
            save_json(journal_path, journal)
            return envelope(command, blocked[0]["check"], "conflict", 2,
                            "Audit identity disagrees with the route. No retirement was performed.",
                            blocked[0]["evidence"], None, {"blocked": blocked})
        names = {record["old_member"] for record, _route in prepared}
        grouped: dict[str, dict[str, dict]] = {name: {} for name in names}
        unassigned = []
        for entry in audit["files"]:
            if not isinstance(entry, dict) or not isinstance(entry.get("path"), str):
                unassigned.append(str(entry)[:120])
                continue
            member, rel = split_member(entry["path"], names)
            if member is None or rel is None:
                unassigned.append(entry["path"])
                continue
            grouped[member][rel] = entry
        if unassigned:
            journal["blocked"] = [{"check": "audit identity", "evidence": unassigned[0], "reason": "audit file is not under a staged member"}]
            journal["complete"] = False
            save_json(journal_path, journal)
            return envelope(command, "audit identity", "conflict", 2,
                            "An audit file is outside the staged members. No copy continued.",
                            unassigned[0], None, {"unassigned": unassigned[:20]})
        copied_this = 0

        def interrupt(evidence: str) -> dict:
            journal["interrupted"] = True
            journal["complete"] = False
            save_json(journal_path, journal)
            return envelope(command, "return-line-stage-journal/1", "interrupted", 3,
                            "Stage stopped before the marker. Resume the same backup and audit.",
                            evidence, None, {"copied_this_call": copied_this})

        for record, route in prepared:
            member = record["old_member"]
            member_abs = os.path.join(book_abs, member)
            if not os.path.isdir(member_abs) or is_reparse(member_abs):
                journal["blocked"] = [{"check": "audit identity", "evidence": member, "reason": "source member is missing"}]
                journal["complete"] = False
                save_json(journal_path, journal)
                return envelope(command, "audit identity", "conflict", 2, "Source member is missing. Nothing was retired.", member, None, {})
            present = walk_files(member_abs)
            expected = grouped.get(member, {})
            extras = [rel for rel in present if rel not in expected]
            missing = [rel for rel in expected if rel not in present]
            if extras or missing:
                journal["blocked"] = [{
                    "check": "audit identity",
                    "evidence": member,
                    "reason": "source files do not match the audit",
                    "extra": extras,
                    "missing": missing,
                }]
                journal["complete"] = False
                save_json(journal_path, journal)
                return envelope(command, "audit identity", "conflict", 2,
                                "Source files do not match the audit. The book source was not deleted.",
                                member, None, {"extra": extras, "missing": missing})
            for rel in present:
                entry = expected[rel]
                src = os.path.join(member_abs, *rel.split("/"))
                data = read_exact(src)
                digest, size = sha(data), len(data)
                audit_file_sha = entry.get("sha256")
                audit_file_bytes = entry.get("bytes")
                match = digest == audit_file_sha and size == audit_file_bytes
                backup_rel = f"sources/{member}/{rel}"
                dest = assert_contained(backup_abs, os.path.join(backup_abs, *backup_rel.split("/")))
                if os.path.lexists(dest) and read_exact(dest) != data and match:
                    held = assert_contained(backup_abs, os.path.join(backup_abs, "mismatches", *backup_rel.split("/")))
                    current = read_exact(dest)
                    if os.path.lexists(held) and read_exact(held) != current:
                        raise LineError(
                            "return-line-stage-journal/1",
                            "an earlier mismatch evidence file differs",
                            "Keep both evidence copies. Do not overwrite either.",
                            evidence="mismatches/" + backup_rel, state="conflict",
                        )
                    if not os.path.lexists(held):
                        os.makedirs(os.path.dirname(held), exist_ok=True)
                        os.rename(dest, held)
                    else:
                        os.remove(dest)
                already = os.path.lexists(dest) and read_exact(dest) == data
                if not already and interrupt_after is not None and copied_this >= interrupt_after:
                    return interrupt(backup_rel)
                wrote = copy_evidence(src, dest, journal, backup_rel, "source", member, audit_file_sha, audit_file_bytes, match)
                if wrote:
                    copied_this += 1
                save_json(journal_path, journal)
                if not match:
                    journal["blocked"] = [{
                        "check": "audit identity",
                        "evidence": backup_rel,
                        "reason": "source bytes differ from the audit",
                        "live_sha256": digest,
                        "audit_sha256": audit_file_sha,
                    }]
                    journal["complete"] = False
                    save_json(journal_path, journal)
                    return envelope(command, "audit identity", "conflict", 2,
                                    "Stale source bytes were copied as evidence and the marker was not written.",
                                    backup_rel, None, {"live_sha256": digest, "audit_sha256": audit_file_sha})
            reason = reader_reason(member_abs)
            has_return = "return.md" in present
            verify_exit = record.get("verify_exit")
            if verify_exit == 0 and reason is not None:
                journal["checks"] = [item for item in journal["checks"] if item.get("old_member") != member]
                journal["checks"].append({"old_member": member, "reader": "fail", "reason": reason})
                journal["blocked"] = [{"check": "sealed reader", "evidence": member, "reason": reason}]
                journal["complete"] = False
                save_json(journal_path, journal)
                return envelope(command, "sealed reader", "conflict", 2,
                                "A source the audit marks verified did not pass the pinned reader.",
                                member, None, {"reason": reason})
            if verify_exit != 0 and has_return and reason is not None:
                journal["blocked"] = [{"check": "sealed reader", "evidence": member, "reason": reason}]
                journal["complete"] = False
                save_json(journal_path, journal)
                return envelope(command, "sealed reader", "conflict", 2,
                                "A return is present but the pinned reader refused it.",
                                member, None, {"reason": reason})
            reader_state = "pass" if reason is None else "incomplete"
            journal["checks"] = [item for item in journal["checks"] if item.get("old_member") != member]
            journal["checks"].append({"old_member": member, "reader": reader_state, "reason": reason})
            if route["route"] == "page-local-colab" and has_return:
                tail_rel = route["return_path"]
                tail_abs = os.path.join(book_abs, *tail_rel.split("/"))
                backup_rel = f"tails/{tail_rel}"
                if not os.path.lexists(tail_abs):
                    journal["blocked"] = [{"check": "N7 tail", "evidence": tail_rel, "reason": "page-local tail is missing"}]
                    journal["complete"] = False
                    save_json(journal_path, journal)
                    return envelope(command, "N7 tail", "conflict", 2, "The page-local tail is missing. It was not invented.", tail_rel, None, {})
                tail_data = read_exact(tail_abs)
                member_return = read_exact(os.path.join(member_abs, "return.md"))
                if tail_data != member_return:
                    dest = assert_contained(backup_abs, os.path.join(backup_abs, *backup_rel.split("/")))
                    if not os.path.lexists(dest):
                        if interrupt_after is not None and copied_this >= interrupt_after:
                            return interrupt(backup_rel)
                        write_new(dest, tail_data)
                        copied_this += 1
                    journal["blocked"] = [{"check": "N7 tail", "evidence": tail_rel, "reason": "page-local tail differs from the member return"}]
                    journal["complete"] = False
                    save_json(journal_path, journal)
                    return envelope(command, "N7 tail", "conflict", 2,
                                    "The page-local tail differs. It was not overwritten.",
                                    tail_rel, None, {})
                dest = assert_contained(backup_abs, os.path.join(backup_abs, *backup_rel.split("/")))
                already = os.path.lexists(dest) and read_exact(dest) == tail_data
                if not already and interrupt_after is not None and copied_this >= interrupt_after:
                    return interrupt(backup_rel)
                wrote = copy_evidence(tail_abs, dest, journal, backup_rel, "tail", member, sha(tail_data), len(tail_data), True)
                if wrote:
                    copied_this += 1
                save_json(journal_path, journal)
        journal["blocked"] = []
        journal["interrupted"] = False
        journal["complete"] = True
        raw = save_json(journal_path, journal)
        marker = {
            "audit_bytes": audit_bytes,
            "audit_sha256": audit_sha256,
            "file_count": len(journal["files"]),
            "journal_sha256": sha(raw),
            "schema": "return-line-stage-complete/1",
            "source_count": len(prepared),
        }
        if os.path.lexists(marker_path):
            os.remove(marker_path)
        write_new(marker_path, dump(marker))
        return envelope(command, "return-line-stage-complete/1", "complete", 0,
                        "Stage marker written. Adoption has not started. This is not acceptance.",
                        STAGE_MARKER, None, {"file_count": marker["file_count"], "source_count": marker["source_count"]})
    return guard(command, work)


def new_adopt_journal(audit_sha: str, stage_marker_sha: str) -> dict:
    return {
        "audit_sha256": audit_sha,
        "blocked": [],
        "complete": False,
        "created": [],
        "interrupted": False,
        "retired": [],
        "schema": "return-line-adopt-journal/1",
        "stage_marker_sha256": stage_marker_sha,
    }


def created_row(journal: dict, rel: str) -> dict | None:
    for item in journal["created"]:
        if item.get("rel") == rel:
            return item
    return None


def place_bytes(book_abs: str, backup_abs: str, journal: dict, journal_path: str, rel: str, data: bytes,
                copied_this: list[int], interrupt_after: int | None, command: str) -> dict | None:
    dest = join_book(book_abs, rel)
    digest, size = sha(data), len(data)
    if os.path.lexists(dest):
        current = read_exact(dest)
        if current != data:
            journal["blocked"] = [{"check": SCHEMA + " bytes", "evidence": rel, "reason": "existing bytes differ"}]
            journal["complete"] = False
            save_json(journal_path, journal)
            return envelope(command, SCHEMA + " bytes", "conflict", 2,
                            "Existing bytes differ. They were not overwritten.",
                            rel, None, {})
        return None
    if interrupt_after is not None and copied_this[0] >= interrupt_after:
        journal["interrupted"] = True
        journal["complete"] = False
        save_json(journal_path, journal)
        return envelope(command, "return-line-adopt-journal/1", "interrupted", 3,
                        "Adopt stopped before the marker. Resume the same backup and audit.",
                        rel, None, {"copied_this_call": copied_this[0]})
    write_new(dest, data)
    copied_this[0] += 1
    row = {"bytes": size, "rel": rel, "sha256": digest}
    if created_row(journal, rel) is None:
        journal["created"].append(row)
    save_json(journal_path, journal)
    return None


def remember_index(book_abs: str, old_member: str | None, submission: str | None, described: dict) -> None:
    path = os.path.join(book_abs, INDEX_NAME)
    if os.path.lexists(path):
        body = loads(read_exact(path), "return-line-index/1")
    else:
        body = {"items": [], "schema": "return-line-index/1"}
    if not isinstance(body, dict) or not isinstance(body.get("items"), list):
        return
    item = {
        "custody_format": described["custody_format"],
        "custody_path": described["custody_path"],
        "old_member": old_member,
        "origin": described["origin"],
        "return_path": described["return_path"],
        "state": described["state"],
        "submission_id": submission if submission is not None else described["submission_id"],
    }
    items = []
    replaced = False
    for current in body["items"]:
        if isinstance(current, dict) and current.get("origin") == item["origin"] and current.get("old_member") == item["old_member"]:
            items.append(item)
            replaced = True
        else:
            items.append(current)
    if not replaced:
        items.append(item)
    body["items"] = items
    body["schema"] = "return-line-index/1"
    save_json(path, body)


def adopt_run(book: str, backup: str, audit_path: str, interrupt_after: int | None = None, resume: bool = False) -> dict:
    command = "adopt-resume" if resume else "adopt"

    def work():
        book_abs = require_dir(book, "book")
        assert_mutable(book_abs)
        backup_abs = require_backup(book_abs, backup)
        layout = read_layout(book_abs)
        audit, audit_sha256, audit_bytes = load_audit(audit_path)
        _stage_journal_path, marker_path = stage_paths(backup_abs)
        if not os.path.lexists(marker_path):
            raise LineError("return-line-stage-complete/1", "stage marker is absent", "Finish staging every source before adoption.", evidence=STAGE_MARKER)
        marker_bytes = read_exact(marker_path)
        marker = loads(marker_bytes, "return-line-stage-complete/1")
        if not isinstance(marker, dict) or marker.get("audit_sha256") != audit_sha256:
            raise LineError("audit identity", "stage marker does not match this audit", "Do not adopt against a different audit.", evidence=STAGE_MARKER, state="conflict")
        stage_journal = load_json_file(os.path.join(backup_abs, STAGE_JOURNAL), "return-line-stage-journal/1")
        if stage_journal is None or sha(read_exact(os.path.join(backup_abs, STAGE_JOURNAL))) != marker.get("journal_sha256"):
            raise LineError("return-line-stage-journal/1", "stage journal does not match its marker", "Keep the journal and do not adopt.", state="conflict")
        for item in stage_journal.get("files", []):
            path = os.path.join(backup_abs, *item["backup_rel"].split("/"))
            data = read_exact(path)
            if sha(data) != item["sha256"] or len(data) != item["bytes"] or not item.get("match"):
                raise LineError("rollback copy", "backup bytes no longer match the stage journal", "Stop. Keep the backup evidence.", evidence=item["backup_rel"], state="conflict")
        journal_path = os.path.join(backup_abs, ADOPT_JOURNAL)
        adopt_marker = os.path.join(backup_abs, ADOPT_MARKER)
        existing = load_json_file(journal_path, "return-line-adopt-journal/1")
        if existing is None:
            journal = new_adopt_journal(audit_sha256, sha(marker_bytes))
        else:
            journal = existing
            if journal.get("audit_sha256") != audit_sha256:
                raise LineError("audit identity", "adopt journal names a different audit", "Keep this journal.", state="conflict")
        if os.path.lexists(adopt_marker):
            current = loads(read_exact(adopt_marker), "return-line-adopt-complete/1")
            if isinstance(current, dict) and current.get("audit_sha256") == audit_sha256 and current.get("journal_sha256") == sha(read_exact(journal_path)):
                return envelope(command, "return-line-adopt-complete/1", "complete", 0,
                                "Adopt marker already matches. This is not live authority and not acceptance.",
                                ADOPT_MARKER, None, {"created_count": current.get("created_count"), "retired_count": current.get("retired_count")})
        prepared, blocked = prepare_records(layout, audit)
        if blocked:
            return envelope(command, blocked[0]["check"], "conflict", 2, "Audit identity disagrees. Adoption did not continue.", blocked[0]["evidence"], None, {"blocked": blocked})
        staged_names = {record["old_member"] for record, _route in prepared}
        copied_this = [0]
        for record, route in prepared:
            member = record["old_member"]
            source_root = os.path.join(backup_abs, "sources", member)
            if not os.path.isdir(source_root):
                raise LineError("rollback copy", "staged source is missing", "Restore the stage backup before adoption.", evidence=f"sources/{member}")
            reason = reader_reason(source_root)
            source_files = walk_files(source_root)
            has_return = "return.md" in source_files
            if record.get("verify_exit") == 0 and reason is not None:
                raise LineError("sealed reader", reason or "reader refused", "Do not adopt a source the pinned reader refuses.", evidence=f"sources/{member}", state="conflict")
            return_data = read_exact(os.path.join(source_root, "return.md")) if has_return else None
            tail_abs = join_book(book_abs, route["return_path"])
            if return_data is not None and os.path.lexists(tail_abs) and read_exact(tail_abs) != return_data:
                journal["blocked"] = [{"check": "N7 tail", "evidence": route["return_path"], "reason": "existing tail differs"}]
                journal["complete"] = False
                save_json(journal_path, journal)
                return envelope(command, "N7 tail", "conflict", 2,
                                "The existing tail differs. It was not overwritten and the page was not retired.",
                                route["return_path"], None, {})
            for name in occupants(book_abs, route["target_number"], route["target_page"]):
                if name not in staged_names:
                    journal["blocked"] = [{"check": "occupied-line", "evidence": name, "reason": "occupant is not a staged source"}]
                    journal["complete"] = False
                    save_json(journal_path, journal)
                    return envelope(command, "occupied-line", "conflict", 2,
                                    "An occupant is not one of the staged sources. It was not overwritten.",
                                    name, None, {})
                retired = any(item.get("name") == name for item in journal["retired"])
                src = os.path.join(book_abs, name)
                dest = assert_contained(backup_abs, os.path.join(backup_abs, "retired", name))
                if retired and os.path.isdir(dest) and not os.path.exists(src):
                    continue
                if not os.path.isdir(src):
                    raise LineError("occupied-line", f"occupant {name} is not in the book or the retired backup", "Stop and keep the evidence.", evidence=name, state="conflict")
                os.makedirs(os.path.dirname(dest), exist_ok=True)
                os.rename(src, dest)
                journal["retired"].append({"backup_rel": f"retired/{name}", "name": name})
                save_json(journal_path, journal)
            for rel in source_files:
                data = read_exact(os.path.join(source_root, *rel.split("/")))
                stopped = place_bytes(book_abs, backup_abs, journal, journal_path, f"{route['custody_dir']}/{rel}", data, copied_this, interrupt_after, command)
                if stopped is not None:
                    return stopped
            reservation = None
            res_backup = os.path.join(source_root, "reservation.json")
            if os.path.lexists(res_backup):
                try:
                    reservation = loads(read_exact(res_backup), "sealed reader")
                except LineError:
                    reservation = None
            destination = reservation.get("destination") if isinstance(reservation, dict) else None
            relocation = {
                "custody_format": "legacy-relocated/1",
                "old_member": member,
                "original_destination": destination,
                "reservation_destination_rewritten": False,
                "return_bytes": None if return_data is None else len(return_data),
                "return_sha256": None if return_data is None else sha(return_data),
                "schema": "return-line-relocation/1",
                "source_backup": f"sources/{member}",
            }
            stopped = place_bytes(book_abs, backup_abs, journal, journal_path, f"{route['custody_dir']}/relocation.json", dump(relocation), copied_this, interrupt_after, command)
            if stopped is not None:
                return stopped
            if return_data is not None and not os.path.lexists(tail_abs):
                stopped = place_bytes(book_abs, backup_abs, journal, journal_path, route["return_path"], return_data, copied_this, interrupt_after, command)
                if stopped is not None:
                    return stopped
        migration = {
            "audit_sha256": audit_sha256,
            "backup_path": backup_abs,
            "schema": "return-line-migration/1",
            "stage_marker": STAGE_MARKER,
        }
        stopped = place_bytes(book_abs, backup_abs, journal, journal_path, MIGRATION_NAME, dump(migration), copied_this, interrupt_after, command)
        if stopped is not None:
            return stopped
        items = []
        for record, route in prepared:
            origin = record["origin"]
            member = record["old_member"]
            source_root = os.path.join(backup_abs, "sources", member)
            has_return = os.path.lexists(os.path.join(source_root, "return.md"))
            submission = record.get("submission")
            state = "incomplete" if not has_return else "complete"
            items.append({
                "custody_format": "legacy-relocated/1",
                "custody_path": route["custody_dir"],
                "old_member": member,
                "origin": {"batch": origin["batch"], "book": origin["book"], "page": origin["page"]},
                "return_path": route["return_path"],
                "state": state,
                "submission_id": submission,
            })
        index = {"items": items, "schema": "return-line-index/1"}
        index_path = os.path.join(book_abs, INDEX_NAME)
        index_raw = dump(index)
        if os.path.lexists(index_path) and read_exact(index_path) != index_raw:
            # A later new-work capture may have extended the index. Rebuild from files.
            index = rebuild_index(book_abs, items)
            index_raw = dump(index)
        if not os.path.lexists(index_path):
            stopped = place_bytes(book_abs, backup_abs, journal, journal_path, INDEX_NAME, index_raw, copied_this, interrupt_after, command)
            if stopped is not None:
                return stopped
        elif read_exact(index_path) != index_raw:
            save_json(index_path, index)
        journal["blocked"] = []
        journal["interrupted"] = False
        journal["complete"] = True
        raw = save_json(journal_path, journal)
        marker_body = {
            "audit_sha256": audit_sha256,
            "created_count": len(journal["created"]),
            "index_sha256": sha(read_exact(index_path)),
            "journal_sha256": sha(raw),
            "retired_count": len(journal["retired"]),
            "schema": "return-line-adopt-complete/1",
            "stage_marker_sha256": sha(marker_bytes),
        }
        if os.path.lexists(adopt_marker):
            os.remove(adopt_marker)
        write_new(adopt_marker, dump(marker_body))
        return envelope(command, "return-line-adopt-complete/1", "complete", 0,
                        "Adopt marker written. This copy is still not live authority and not acceptance.",
                        ADOPT_MARKER, None, {"created_count": marker_body["created_count"], "retired_count": marker_body["retired_count"], "audit_bytes": audit_bytes})
    return guard(command, work)


def rebuild_index(book_abs: str, migrated: list[dict]) -> dict:
    items = list(migrated)
    seen = {(item.get("old_member"), item["origin"]["page"], item["origin"]["batch"]) for item in items}
    for page_name, batch, custody_abs in iter_custodies(book_abs):
        res_abs = os.path.join(custody_abs, "reservation.json")
        if not os.path.lexists(res_abs):
            continue
        try:
            reservation = parse_reservation(read_exact(res_abs))
        except LineError:
            continue
        origin = reservation["origin"]
        key = (None, origin["page"], origin["batch"])
        if (None, origin["page"], origin["batch"]) in seen or (origin["page"], origin["batch"]) in {(item["origin"]["page"], item["origin"]["batch"]) for item in items}:
            continue
        if key in seen:
            continue
        items.append({
            "custody_format": SCHEMA,
            "custody_path": reservation["line"]["custody_dir"],
            "old_member": None,
            "origin": origin,
            "return_path": reservation["line"]["return_path"],
            "state": "reserved",
            "submission_id": reservation["submission_id"],
        })
        seen.add(key)
    return {"items": items, "schema": "return-line-index/1"}


def iter_custodies(book_abs: str):
    with os.scandir(book_abs) as pages:
        for page in pages:
            if is_reparse(page.path) or not page.is_dir(follow_symlinks=False):
                continue
            with os.scandir(page.path) as children:
                for child in children:
                    if not child.name.endswith(".custody"):
                        continue
                    if is_reparse(child.path) or not child.is_dir(follow_symlinks=False):
                        continue
                    yield page.name, child.name[: -len(".custody")], child.path


def migration_backup(book_abs: str) -> str | None:
    path = os.path.join(book_abs, MIGRATION_NAME)
    if not os.path.lexists(path):
        return None
    body = loads(read_exact(path), "return-line-migration/1")
    if isinstance(body, dict) and isinstance(body.get("backup_path"), str):
        return body["backup_path"]
    return None


def assess_legacy_at(book_abs: str, layout: dict, page: str, batch: str) -> dict | None:
    route = route_for(layout["book"], page, batch)
    reloc_abs = join_book(book_abs, route["custody_dir"] + "/relocation.json")
    if not os.path.lexists(reloc_abs):
        return None
    relocation = expect_keys(loads(read_exact(reloc_abs), "return-line-relocation/1"), RELOCATION_KEYS, "return-line-relocation/1", "relocation")
    if relocation["reservation_destination_rewritten"] is not False or relocation["custody_format"] != "legacy-relocated/1":
        raise LineError("return-line-relocation/1", "relocation rewrote the destination or the format", "Keep the original reservation bytes.", evidence=route["custody_dir"] + "/relocation.json", state="conflict")
    origin = {"book": layout["book"], "page": page, "batch": batch}
    backup = migration_backup(book_abs)
    source_rel = relocation["source_backup"]
    problems = []
    receipt_sha256 = None
    return_sha256 = None
    return_bytes = None
    submission = None
    if isinstance(relocation.get("old_member"), str):
        pass
    if backup is None or not os.path.isdir(os.path.join(backup, *source_rel.split("/"))):
        problems.append("rollback copy missing")
    else:
        source_abs = os.path.join(backup, *source_rel.split("/"))
        reason = reader_reason(source_abs)
        custody_abs = join_book(book_abs, route["custody_dir"])
        for rel in walk_files(source_abs):
            copied = os.path.join(custody_abs, *rel.split("/"))
            if not os.path.lexists(copied) or read_exact(copied) != read_exact(os.path.join(source_abs, *rel.split("/"))):
                problems.append(f"custody bytes {rel}")
        res_abs = os.path.join(source_abs, "reservation.json")
        if os.path.lexists(res_abs):
            reservation = loads(read_exact(res_abs), "sealed reader")
            if isinstance(reservation, dict):
                submission = reservation.get("submission_id")
                recorded = reservation.get("destination")
                if recorded != relocation["original_destination"]:
                    problems.append("original destination")
        has_return = os.path.lexists(os.path.join(source_abs, "return.md"))
        if not has_return:
            state = "incomplete"
            if reason is None:
                problems.append("reader passed without a return")
        else:
            member_return = read_exact(os.path.join(source_abs, "return.md"))
            return_sha256, return_bytes = sha(member_return), len(member_return)
            tail_abs = join_book(book_abs, route["return_path"])
            if not os.path.lexists(tail_abs) or read_exact(tail_abs) != member_return:
                problems.append("tail bytes")
            if reason is not None:
                problems.append(reason)
            state = "complete" if not problems else "conflict"
        rec_abs = os.path.join(custody_abs, "receipt.json")
        if os.path.lexists(rec_abs):
            receipt_sha256 = sha(read_exact(rec_abs))
        if not has_return:
            state = "incomplete" if not problems else "conflict"
            return_sha256, return_bytes = None, None
    if backup is None or not os.path.isdir(os.path.join(backup, *str(source_rel).split("/"))):
        state = "conflict"
    described = descriptor(
        origin, route["route"], route["target_page"], route["return_path"], route["custody_dir"],
        route["custody_dir"] + "/receipt.json", route["custody_dir"] + "/manifest.json",
        submission if isinstance(submission, str) else None, "legacy-relocated/1",
        receipt_sha256, return_sha256, return_bytes, state, route["custody_dir"] + "/relocation.json",
    )
    exit_code = {"complete": 0, "incomplete": 1, "reserved": 1}.get(state, 2)
    return {"exit": exit_code, "state": state, "descriptor": described, "check": "return-line-relocation/1", "problems": problems}


def lookup_source_member(book_abs: str, layout: dict, member: str) -> dict | None:
    res_abs = os.path.join(book_abs, member, "reservation.json")
    if not os.path.lexists(res_abs):
        return None
    raw = loads(read_exact(res_abs), "audit identity")
    if not isinstance(raw, dict):
        return None
    origin = raw.get("origin") if isinstance(raw.get("origin"), dict) else None
    if origin is None:
        return None
    try:
        route = route_for(layout["book"], origin.get("page", ""), origin.get("batch", ""))
    except LineError:
        return None
    described = descriptor(
        {"book": origin.get("book", layout["book"]), "page": origin["page"], "batch": origin["batch"]},
        route["route"], route["target_page"], route["return_path"], route["custody_dir"],
        route["custody_dir"] + "/receipt.json", route["custody_dir"] + "/manifest.json",
        raw.get("submission_id") if isinstance(raw.get("submission_id"), str) else None,
        "legacy-relocated/1", None, None, None, "incomplete", f"{member}/reservation.json",
    )
    return {"exit": 1, "state": "incomplete", "descriptor": described, "check": "return-line-stage-complete/1", "problems": ["adoption not complete"]}


def origin_from_custody(custody_abs: str, backup: str | None, source_rel: str | None) -> dict | None:
    for path in (
        os.path.join(custody_abs, "reservation.json"),
        os.path.join(backup, *source_rel.split("/"), "reservation.json") if backup and source_rel else "",
    ):
        if path and os.path.lexists(path):
            body = loads(read_exact(path), "sealed reader")
            origin = body.get("origin") if isinstance(body, dict) else None
            if isinstance(origin, dict) and {"book", "page", "batch"} <= set(origin):
                return origin
    return None


def find_by_member(book_abs: str, layout: dict, member: str) -> dict:
    for page_name, batch, custody_abs in iter_custodies(book_abs):
        reloc = os.path.join(custody_abs, "relocation.json")
        if not os.path.lexists(reloc):
            continue
        body = loads(read_exact(reloc), "return-line-relocation/1")
        if not isinstance(body, dict) or body.get("old_member") != member:
            continue
        origin = origin_from_custody(custody_abs, migration_backup(book_abs), body.get("source_backup") if isinstance(body.get("source_backup"), str) else None)
        if origin is None:
            raise LineError("return-line-relocation/1", "relocated reservation has no origin", "Keep the reservation bytes with the backup copy.", evidence=f"{page_name}/{batch}.custody/reservation.json", state="conflict")
        route = route_for(layout["book"], origin["page"], origin["batch"])
        if route["target_page"] != page_name or route["pass"] != batch:
            raise LineError("return-placement-route/1", "custody directory does not match the origin route", "Do not treat a target directory name as the origin page.", evidence=f"{page_name}/{batch}.custody", state="conflict")
        return assess_legacy_at(book_abs, layout, origin["page"], origin["batch"])
    pending = lookup_source_member(book_abs, layout, member)
    if pending is not None:
        return pending
    raise LineError("return-line-index/1", f"member {member} is not on a line", "Stage and adopt the source, or pass the origin page and batch.")


def find_by_submission(book_abs: str, layout: dict, submission: str) -> dict:
    for page_name, batch, custody_abs in iter_custodies(book_abs):
        reloc = os.path.join(custody_abs, "relocation.json")
        res = os.path.join(custody_abs, "reservation.json")
        if os.path.lexists(reloc):
            body = loads(read_exact(reloc), "return-line-relocation/1")
            if isinstance(body, dict):
                backup = migration_backup(book_abs)
                source = body.get("source_backup")
                if backup and isinstance(source, str):
                    pointer = os.path.join(backup, *source.split("/"), "reservation.json")
                    if os.path.lexists(pointer):
                        reservation = loads(read_exact(pointer), "sealed reader")
                        if isinstance(reservation, dict) and reservation.get("submission_id") == submission:
                            origin = reservation.get("origin") if isinstance(reservation.get("origin"), dict) else None
                            if origin is None:
                                continue
                            route = route_for(layout["book"], origin.get("page", ""), origin.get("batch", ""))
                            if route["target_page"] != page_name or route["pass"] != batch:
                                raise LineError("return-placement-route/1", "custody directory does not match the origin route", "Look up the origin page and batch.", evidence=f"{page_name}/{batch}.custody", state="conflict")
                            found = assess_legacy_at(book_abs, layout, origin["page"], origin["batch"])
                            if found is not None:
                                return found
        if os.path.lexists(res):
            try:
                reservation = parse_reservation(read_exact(res))
            except LineError:
                continue
            if reservation["submission_id"] == submission:
                return assess_new(book_abs, layout, reservation["origin"]["page"], reservation["origin"]["batch"])
    raise LineError("return-line-index/1", "submission is not on a line", "Reserve the pass or adopt the historical member first.")


def lookup_run(book: str, member: str | None = None, page: str | None = None,
               batch: str | None = None, submission: str | None = None) -> dict:
    def work():
        book_abs = require_dir(book, "book")
        layout = read_layout(book_abs)
        if page and batch:
            legacy = assess_legacy_at(book_abs, layout, page, batch)
            assessed = legacy if legacy is not None else assess_new(book_abs, layout, page, batch)
        elif member:
            assessed = find_by_member(book_abs, layout, member)
        elif submission:
            assessed = find_by_submission(book_abs, layout, submission)
        else:
            raise LineError("return-line-index/1", "lookup needs a member, a submission, or a page and batch", "Pass one of those selectors.")
        return finish_assess("lookup", assessed)
    return guard("lookup", work)


def descriptor_run(book: str, member: str | None = None, page: str | None = None,
                   batch: str | None = None, submission: str | None = None) -> dict:
    result = lookup_run(book, member, page, batch, submission)
    result["command"] = "descriptor"
    return result


def hashes_match(path: str, digest: str, size: int) -> bool:
    if not os.path.lexists(path):
        return False
    data = read_exact(path)
    return sha(data) == digest and len(data) == size


def prune_empty(start: str, stop: str) -> None:
    current = start
    stop_n = norm(stop)
    while norm(current) != stop_n:
        try:
            os.rmdir(current)
        except OSError:
            return
        parent = os.path.dirname(current)
        if parent == current:
            return
        current = parent


def rollback_stage_run(book: str, backup: str) -> dict:
    def work():
        book_abs = require_dir(book, "book")
        assert_mutable(book_abs)
        backup_abs = require_backup(book_abs, backup)
        adopt = load_json_file(os.path.join(backup_abs, ADOPT_JOURNAL), "return-line-adopt-journal/1")
        if adopt and (adopt.get("created") or adopt.get("retired")):
            raise LineError("return-line-adopt-journal/1", "adoption has already created or retired files", "Roll back adoption before rolling back the stage backup.")
        journal_path, marker_path = stage_paths(backup_abs)
        journal = load_json_file(journal_path, "return-line-stage-journal/1")
        if journal is None:
            raise LineError("return-line-stage-journal/1", "stage journal is absent", "There is no stage backup to roll back.")
        marker_sha = sha(read_exact(marker_path)) if os.path.lexists(marker_path) else None
        if os.path.lexists(marker_path):
            os.remove(marker_path)
        files = list(journal.get("files") or [])
        for item in files:
            path = os.path.join(backup_abs, *item["backup_rel"].split("/"))
            if not os.path.lexists(path):
                continue
            if not hashes_match(path, item["sha256"], item["bytes"]):
                raise LineError("rollback copy", "backup file changed since the journal", "Stop. The remaining backup evidence stays.", evidence=item["backup_rel"], state="conflict")
        for item in sorted(files, key=lambda row: row["backup_rel"].count("/"), reverse=True):
            path = os.path.join(backup_abs, *item["backup_rel"].split("/"))
            if os.path.lexists(path):
                os.remove(path)
                prune_empty(os.path.dirname(path), backup_abs)
        journal["files"] = []
        journal["complete"] = False
        journal["interrupted"] = False
        journal["blocked"] = []
        save_json(journal_path, journal)
        return envelope("rollback-stage", "return-line-stage-journal/1", "complete", 0,
                        "Journaled backup files whose hashes matched were removed. The book was not modified.",
                        STAGE_JOURNAL, None, {"marker_sha256": marker_sha})
    return guard("rollback-stage", work)


def rollback_adopt_run(book: str, backup: str) -> dict:
    def work():
        book_abs = require_dir(book, "book")
        assert_mutable(book_abs)
        backup_abs = require_backup(book_abs, backup)
        journal_path = os.path.join(backup_abs, ADOPT_JOURNAL)
        marker_path = os.path.join(backup_abs, ADOPT_MARKER)
        journal = load_json_file(journal_path, "return-line-adopt-journal/1")
        if journal is None:
            raise LineError("return-line-adopt-journal/1", "adopt journal is absent", "There is no adoption to roll back.")
        marker_sha = sha(read_exact(marker_path)) if os.path.lexists(marker_path) else None
        for item in journal.get("created") or []:
            path = join_book(book_abs, item["rel"])
            if os.path.lexists(path) and not hashes_match(path, item["sha256"], item["bytes"]):
                raise LineError(SCHEMA + " bytes", "a created file changed since the journal", "Stop before deleting. The evidence stays.", evidence=item["rel"], state="conflict")
        if os.path.lexists(marker_path):
            os.remove(marker_path)
        for item in sorted(journal.get("created") or [], key=lambda row: row["rel"].count("/"), reverse=True):
            path = join_book(book_abs, item["rel"])
            if os.path.lexists(path):
                os.remove(path)
                prune_empty(os.path.dirname(path), book_abs)
        for item in list(journal.get("retired") or []):
            src = os.path.join(backup_abs, *item["backup_rel"].split("/"))
            dest = os.path.join(book_abs, item["name"])
            if os.path.exists(dest):
                raise LineError("occupied-line", f"{item['name']} is already in the book", "Stop. Do not overwrite it with the retired copy.", evidence=item["name"], state="conflict")
            if not os.path.isdir(src):
                raise LineError("rollback copy", f"retired copy {item['name']} is missing", "Stop. Do not invent the directory.", evidence=item["backup_rel"], state="conflict")
            os.rename(src, dest)
        journal["created"] = []
        journal["retired"] = []
        journal["complete"] = False
        journal["interrupted"] = False
        save_json(journal_path, journal)
        return envelope("rollback-adopt", "return-line-adopt-journal/1", "complete", 0,
                        "Journaled adoption was reversed. A hash mismatch would have stopped the reversal.",
                        ADOPT_JOURNAL, None, {"marker_sha256": marker_sha})
    return guard("rollback-adopt", work)


def guard_out(book_abs: str, out_path: str) -> str:
    out_abs = os.path.abspath(out_path)
    if within(book_abs, out_abs):
        rel = os.path.relpath(out_abs, book_abs).replace("\\", "/")
        if rel == DOOR or rel.startswith(DOOR + "/"):
            raise LineError("live book", "refusing to write inside the return door", "Write the plan under the batch evidence directory.")
        for part in rel.split("/"):
            if re.fullmatch(r"^01(?:0[1-9]|[1-9][0-9])\..+", part):
                raise LineError("live book", "refusing to write inside a capture member", "Write the plan outside every 01NN member.")
    parent = os.path.dirname(out_abs)
    if parent and not os.path.isdir(parent):
        os.makedirs(parent, exist_ok=True)
    return out_abs


def plan_run(book: str, audit_path: str, out_path: str) -> dict:
    def work():
        book_abs = require_dir(book, "book")
        out_abs = guard_out(book_abs, out_path)
        try:
            plan = placement().build_plan(book_abs, os.path.abspath(audit_path))
        except placement().PlacementError as exc:
            raise LineError("return-line-plan/1", exc.reason, "Fix the plan inputs. This command does not move the book.") from exc
        body = {
            "enforcement": "pending",
            "live_apply": False,
            "live_moves": False,
            "new_work_route": {
                "allocation": "line-pass",
                "bands": {"5": "matched-workflow-return-line", "7": "page-local-colab"},
                "schema": SCHEMA,
                "tool": TOOL_PATH,
            },
            "placement_plan": plan,
            "post_audit_changes": plan.get("changes_since_audit"),
            "preconditions": [
                "Prime reviews this plan before any live operation.",
                "live_moves and live_apply are false. This file is not permission to move.",
                "Do not call the sequential allocator.",
                "Do not allocate 0184.",
                "0121.return-placement stays unfiled until 0121.archive-resolution-0508 is migrated and Prime accepts that retirement.",
                "Stage every source and keep a backup outside the page namespace before retiring an occupant.",
                "0154 stays incomplete.",
                "Shared caller pins are unchanged. Live enforcement is pending.",
                "The placement candidate live-book guard stays in place.",
            ],
            "schema": PLAN_SCHEMA,
            "sequential_allocation": False,
        }
        raw = dump(body)
        with open(out_abs, "wb") as handle:
            handle.write(raw)
        changes = plan.get("changes_since_audit") or []
        return envelope(
            "plan", PLAN_SCHEMA, "incomplete", 0,
            "Read-only plan written. Live migration is not authorized.",
            os.path.basename(out_abs), None,
            {
                "bytes": len(raw),
                "change_count": len(changes),
                "enforcement": "pending",
                "item_count": plan.get("item_count"),
                "live_apply": False,
                "live_moves": False,
                "occupancy_conflict_count": plan.get("occupancy_conflict_count"),
                "sha256": sha(raw),
            },
        )
    return guard("plan", work)


def emit(result: dict, descriptor_only: bool) -> int:
    if descriptor_only and isinstance(result.get("descriptor"), dict):
        sys.stdout.buffer.write(dump(result["descriptor"]))
    else:
        sys.stdout.buffer.write(dump(result))
    return int(result["exit"])


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Line/pass return route and staged migration")
    sub = parser.add_subparsers(dest="command", required=True)

    init = sub.add_parser("init")
    init.add_argument("--book", required=True)
    init.add_argument("--name", required=True)

    reserve = sub.add_parser("reserve")
    reserve.add_argument("--book", required=True)
    reserve.add_argument("--page", required=True)
    reserve.add_argument("--batch", required=True)
    reserve.add_argument("--submission", required=True)
    reserve.add_argument("--output", action="append", default=[])
    reserve.add_argument("--submitter", required=True)
    reserve.add_argument("--reviewer", required=True)
    reserve.add_argument("--release", required=True)
    reserve.add_argument("--supersedes", default=None)

    capture = sub.add_parser("capture")
    capture.add_argument("--book", required=True)
    capture.add_argument("--page", required=True)
    capture.add_argument("--batch", required=True)
    capture.add_argument("--submission", required=True)
    capture.add_argument("--return-file", required=True)
    capture.add_argument("--artifact", nargs=2, action="append", default=[], metavar=("LOGICAL", "FILE"))

    for name in ("verify",):
        verify = sub.add_parser(name)
        verify.add_argument("--book", required=True)
        verify.add_argument("--page", required=True)
        verify.add_argument("--batch", required=True)

    for name in ("lookup", "descriptor"):
        lookup = sub.add_parser(name)
        lookup.add_argument("--book", required=True)
        lookup.add_argument("--member")
        lookup.add_argument("--page")
        lookup.add_argument("--batch")
        lookup.add_argument("--submission")

    for name in ("stage", "stage-resume", "adopt", "adopt-resume"):
        phase = sub.add_parser(name)
        phase.add_argument("--book", required=True)
        phase.add_argument("--backup", required=True)
        phase.add_argument("--audit", required=True)
        phase.add_argument("--interrupt-after", type=int, default=None)

    for name in ("rollback-stage", "rollback-adopt"):
        rollback = sub.add_parser(name)
        rollback.add_argument("--book", required=True)
        rollback.add_argument("--backup", required=True)

    plan = sub.add_parser("plan")
    plan.add_argument("--book", required=True)
    plan.add_argument("--audit", required=True)
    plan.add_argument("--out", required=True)

    args = parser.parse_args(argv)
    if args.command == "init":
        result = init_run(args.book, args.name)
    elif args.command == "reserve":
        result = reserve_run(args.book, args.page, args.batch, args.submission, args.output, args.submitter, args.reviewer, args.release, args.supersedes)
    elif args.command == "capture":
        result = capture_run(args.book, args.page, args.batch, args.submission, args.return_file, [(a, b) for a, b in args.artifact])
    elif args.command == "verify":
        result = verify_run(args.book, args.page, args.batch)
    elif args.command in {"lookup", "descriptor"}:
        result = lookup_run(args.book, args.member, args.page, args.batch, args.submission)
        if args.command == "descriptor":
            result["command"] = "descriptor"
    elif args.command in {"stage", "stage-resume"}:
        result = stage_run(args.book, args.backup, args.audit, args.interrupt_after, args.command == "stage-resume")
    elif args.command in {"adopt", "adopt-resume"}:
        result = adopt_run(args.book, args.backup, args.audit, args.interrupt_after, args.command == "adopt-resume")
    elif args.command == "rollback-stage":
        result = rollback_stage_run(args.book, args.backup)
    elif args.command == "rollback-adopt":
        result = rollback_adopt_run(args.book, args.backup)
    else:
        result = plan_run(args.book, args.audit, args.out)
    return emit(result, args.command == "descriptor")


if __name__ == "__main__":
    sys.exit(main())
