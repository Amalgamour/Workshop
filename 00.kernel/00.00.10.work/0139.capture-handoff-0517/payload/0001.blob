"""Fixture adapter from one returned Clerk job to one pre-reserved capture.

This module is not app wiring and not kernel law. It does not import the
pinned tools. A verified receipt is custody, not review, acceptance,
acknowledgement, closure, or publication. work_ref is a declared label.
The same-user gap between a hash read and a later write stays open.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import stat
import subprocess
import sys
from pathlib import Path


sys.dont_write_bytecode = True
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"

ROOT = Path(__file__).resolve().parents[2]
SCHEMA = "clerk-capture-handoff/1"
RECORD_SCHEMA = "clerk-capture-handoff-record/1"
FAILURE_SCHEMA = "clerk-capture-handoff-failure/1"
INSPECTION_SCHEMA = "clerk-handoff-inspection/2"
MEMBER_SCHEMA = "return-capture-inspection/1"
REPARSE = 0x400
TIMEOUT_S = 60
INTENT_NAME = "intent.json"
COMPLETED_NAME = "completed.json"
RECORD_FILES = {INTENT_NAME, COMPLETED_NAME}
ID_TEXT = __import__("re").compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,63}$")
BATCH_TEXT = __import__("re").compile(r"^05\.\d{2}$")
HEX64 = __import__("re").compile(r"^[0-9a-f]{64}$")
MEMBER_TEXT = __import__("re").compile(r"^(\d{4})\.([A-Za-z0-9][A-Za-z0-9._-]{0,63})$")
RESERVED_WINDOWS = {
    "CON", "PRN", "AUX", "NUL",
    *(f"COM{n}" for n in range(1, 10)),
    *(f"LPT{n}" for n in range(1, 10)),
}
BINDING_KEYS = {
    "artifact_base",
    "artifacts",
    "assignee",
    "book",
    "clerk_store",
    "failure_log",
    "instructions_base",
    "job_id",
    "member",
    "origin",
    "record",
    "report",
    "returned_event_sha256",
    "schema",
    "source_root",
    "submission_id",
    "work_ref",
}
ORIGIN_KEYS = {"batch", "book", "page"}
REPORT_KEYS = {"bytes", "clerk_path", "sha256", "source"}
ARTIFACT_KEYS = {"bytes", "clerk_path", "logical", "sha256", "source"}
TOOL_FILES = {
    "clerk": (
        "labs/clerk-handoff-pass02/clerk.py",
        "f697a7e443117c3d1face62d3021f7634154d76214b77fadec1a5cc3c99d394c",
    ),
    "capture": (
        "labs/return-capture-pass01/return_capture.py",
        "8f3da5c651f6924fca6dedb0b95da7d181eb58884dc030dd9cbc3d8b6a5b15ac",
    ),
    "inspect": (
        "labs/return-capture-pass01/return_inspect.py",
        "947915febaa5918f56b6be03c81840c030d081fcab9a3bead2cd660973a9999b",
    ),
}
INSPECT_EXIT = {
    "complete": 0,
    "reserved": 1,
    "missing": 1,
    "incomplete": 2,
    "refused": 2,
}
HOOK_POINTS = {"before-intent", "after-intent", "after-capture", "before-final-record"}
CUSTODY = ("result complete", "not approved", "not accepted", "not published")


class Refuse(Exception):
    def __init__(self, message: str, *, attention: bool = False) -> None:
        super().__init__(message)
        self.message = message
        self.attention = attention


class Stop(Exception):
    def __init__(self, point: str) -> None:
        super().__init__(point)
        self.point = point


def refuse(message: str, *, attention: bool = False) -> None:
    raise Refuse(message, attention=attention)


def canonical(value) -> bytes:
    text = json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    )
    return (text + "\n").encode("utf-8")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def default_pins() -> dict:
    pins = {}
    for name, (relative, digest) in TOOL_FILES.items():
        pins[name] = (str(ROOT / relative), digest)
    return pins


def is_reparse(path: Path) -> bool:
    try:
        info = os.lstat(path)
    except OSError:
        return False
    attrs = getattr(info, "st_file_attributes", 0) or 0
    return bool(attrs & REPARSE) or stat.S_ISLNK(info.st_mode)


def plain_file_problem(path: Path) -> str | None:
    if not os.path.lexists(path):
        return "missing"
    if is_reparse(path):
        return "link"
    info = os.lstat(path)
    if not stat.S_ISREG(info.st_mode):
        return "not-regular"
    if info.st_nlink != 1:
        return "link-count"
    return None


def plain_dir_problem(path: Path) -> str | None:
    if not os.path.lexists(path):
        return "missing"
    if is_reparse(path):
        return "link"
    info = os.lstat(path)
    if not stat.S_ISDIR(info.st_mode):
        return "not-directory"
    return None


def abspath(text: str) -> str:
    return os.path.abspath(text)


def norm(text: str) -> str:
    return os.path.normcase(os.path.abspath(text))


def inside(child: str, parent: str) -> bool:
    child_s = norm(child)
    parent_s = norm(parent)
    if child_s == parent_s:
        return False
    prefix = parent_s if parent_s.endswith(os.sep) else parent_s + os.sep
    return child_s.startswith(prefix)


def same_path(left: str, right: str) -> bool:
    return norm(left) == norm(right)


def control_segment(text: str) -> bool:
    return any(part.casefold() == ".git" for part in Path(abspath(text)).parts)


def require_id(value, label: str) -> str:
    if type(value) is not str or not ID_TEXT.fullmatch(value) or value.endswith(".") or value.endswith(" "):
        refuse(f"{label} is not a windows-safe id")
    if value.split(".", 1)[0].upper() in RESERVED_WINDOWS:
        refuse(f"{label} is a reserved windows name")
    return value


def require_text(value, label: str) -> str:
    if type(value) is not str or value == "" or len(value) > 4096:
        refuse(f"{label} is empty or too long")
    if any(ord(ch) < 32 or ord(ch) == 127 for ch in value):
        refuse(f"{label} has control characters")
    return value


def require_hash(value, label: str) -> str:
    if type(value) is not str or not HEX64.fullmatch(value):
        refuse(f"{label} is not 64 lowercase hex")
    return value


def require_count(value, label: str) -> int:
    if type(value) is not int or value < 0:
        refuse(f"{label} is not an integer")
    return value


def require_absolute(value, label: str) -> str:
    if type(value) is not str or not os.path.isabs(value):
        refuse(f"{label} must be absolute")
    return abspath(value)


def require_filename(value, label: str) -> str:
    if type(value) is not str or value == "" or "/" in value or "\\" in value:
        refuse(f"{label} is not a simple filename")
    if value in (".", "..") or value.endswith(".") or value.endswith(" "):
        refuse(f"{label} has an unsafe segment")
    if value.split(".", 1)[0].upper() in RESERVED_WINDOWS:
        refuse(f"{label} is a reserved windows name")
    require_id(value, label)
    return value


def parse_object(raw: bytes, label: str) -> dict:
    if raw.startswith(b"\xef\xbb\xbf"):
        refuse(f"{label} is not utf-8")
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        refuse(f"{label} is not utf-8")

    def pairs(seq):
        obj = {}
        for key, item in seq:
            if type(key) is not str:
                refuse(f"{label} key is not a string")
            if key in obj:
                refuse(f"{label} repeats {key}")
            obj[key] = item
        return obj

    try:
        value, end = json.JSONDecoder(object_pairs_hook=pairs).raw_decode(text)
    except Refuse:
        raise
    except json.JSONDecodeError:
        refuse(f"{label} is not strict json")
    if text[end:].strip():
        refuse(f"{label} has trailing data")
    if type(value) is not dict:
        refuse(f"{label} is not an object")
    return value


def require_exact(value: dict, keys: set[str], label: str) -> None:
    unknown = sorted(set(value) - keys)
    missing = sorted(keys - set(value))
    if unknown:
        refuse(f"{label} has unknown field {unknown[0]}")
    if missing:
        refuse(f"{label} misses {missing[0]}")


def walk_no_link(path: Path) -> None:
    current = path
    parts = []
    while True:
        parts.append(current)
        parent = current.parent
        if parent == current:
            break
        current = parent
    for item in reversed(parts):
        if os.path.lexists(item) and is_reparse(item):
            refuse(f"link: {item}")


def read_plain(path: Path, label: str) -> bytes:
    walk_no_link(path)
    problem = plain_file_problem(path)
    if problem:
        refuse(f"{problem}: {label}")
    first = path.read_bytes()
    second = path.read_bytes()
    if first != second:
        refuse(f"bytes changed before read: {label}")
    return first


def require_plain_dir(path: Path, label: str) -> None:
    walk_no_link(path)
    problem = plain_dir_problem(path)
    if problem:
        refuse(f"{label} is {problem}")


def pin_problem(pins: dict) -> str | None:
    if set(pins) != set(TOOL_FILES):
        return "pin table does not match the packed tools"
    for name, (relative, digest) in TOOL_FILES.items():
        supplied, supplied_hash = pins[name]
        expected = str((ROOT / relative).resolve())
        if os.path.normcase(str(Path(supplied).resolve())) != os.path.normcase(expected):
            return f"pin path is not the packed tool: {name}"
        path = Path(supplied)
        problem = plain_file_problem(path)
        if problem:
            return f"pin file is {problem}: {name}"
        data = path.read_bytes()
        actual = sha256_bytes(data)
        if actual != supplied_hash or actual != digest:
            return f"pin hash mismatch: {name}"
    return None


def check_pins(pins: dict) -> None:
    problem = pin_problem(pins)
    if problem:
        refuse(problem)


def file_under(root: str, name: str) -> Path:
    path = Path(root) / name
    if inside(str(path), root) is False and not same_path(str(path.parent), root):
        refuse(f"path escape: {name}")
    if norm(str(path.parent)) != norm(root):
        refuse(f"path escape: {name}")
    return path


def parse_binding(path_text: str) -> tuple[dict, bytes]:
    if type(path_text) is not str or not os.path.isabs(path_text):
        refuse("binding path must be absolute")
    raw = read_plain(Path(path_text), "binding")
    value = parse_object(raw, "binding")
    require_exact(value, BINDING_KEYS, "binding")
    if value["schema"] != SCHEMA:
        refuse("binding schema is not clerk-capture-handoff/1")
    store = require_absolute(value["clerk_store"], "clerk_store")
    base = require_absolute(value["instructions_base"], "instructions_base")
    book = require_absolute(value["book"], "book")
    source_root = require_absolute(value["source_root"], "source_root")
    artifact_base = require_absolute(value["artifact_base"], "artifact_base")
    record = require_absolute(value["record"], "record")
    failure_log = require_absolute(value["failure_log"], "failure_log")
    job_id = require_id(value["job_id"], "job_id")
    assignee = require_id(value["assignee"], "assignee")
    submission = require_id(value["submission_id"], "submission_id")
    work_ref = require_text(value["work_ref"], "work_ref")
    event = require_hash(value["returned_event_sha256"], "returned_event_sha256")
    member = value["member"]
    match = MEMBER_TEXT.fullmatch(member) if type(member) is str else None
    if match is None or not (101 <= int(match.group(1)) <= 199):
        refuse("member is not a return member")
    require_id(match.group(2), "member")
    origin = value["origin"]
    if type(origin) is not dict:
        refuse("origin is not an object")
    require_exact(origin, ORIGIN_KEYS, "origin")
    origin_book = require_id(origin["book"], "origin book")
    origin_page = require_id(origin["page"], "origin page")
    origin_batch = origin["batch"]
    if type(origin_batch) is not str or not BATCH_TEXT.fullmatch(origin_batch):
        refuse("origin batch must match 05.NN")
    report = parse_report(value["report"])
    artifacts = parse_artifacts(value["artifacts"], report)
    for label, text in (
        ("record", record),
        ("failure_log", failure_log),
    ):
        if control_segment(text):
            refuse(f"{label} contains a Git control segment")
    job_dir = str(Path(store) / "jobs" / job_id)
    member_dir = str(Path(book) / member)
    forbid_overlap(record, member_dir, "record", "member")
    forbid_overlap(record, job_dir, "record", "job")
    forbid_overlap(record, source_root, "record", "source root")
    forbid_overlap(failure_log, member_dir, "failure log", "member")
    forbid_overlap(failure_log, job_dir, "failure log", "job")
    forbid_overlap(failure_log, source_root, "failure log", "source root")
    if inside(failure_log, record) or same_path(failure_log, record):
        refuse("failure log is inside the handoff record")
    expected_outbox = str(Path(store) / "jobs" / job_id / "outbox")
    if not same_path(artifact_base, expected_outbox):
        refuse("artifact base is not the Clerk job outbox")
    parsed = {
        "schema": SCHEMA,
        "clerk_store": store,
        "job_id": job_id,
        "instructions_base": base,
        "returned_event_sha256": event,
        "assignee": assignee,
        "work_ref": work_ref,
        "origin": {"book": origin_book, "page": origin_page, "batch": origin_batch},
        "book": book,
        "submission_id": submission,
        "member": member,
        "source_root": source_root,
        "artifact_base": abspath(expected_outbox),
        "report": report,
        "artifacts": artifacts,
        "record": record,
        "failure_log": failure_log,
    }
    return parsed, canonical(parsed)


def forbid_overlap(left: str, right: str, left_label: str, right_label: str) -> None:
    if same_path(left, right) or inside(left, right) or inside(right, left):
        refuse(f"{left_label} overlaps {right_label}")


def parse_report(value) -> dict:
    if type(value) is not dict:
        refuse("report is not an object")
    require_exact(value, REPORT_KEYS, "report")
    clerk_path = require_filename(value["clerk_path"], "report clerk path")
    source = require_filename(value["source"], "report source")
    if source != clerk_path:
        refuse("report source is not the clerk path")
    return {
        "clerk_path": clerk_path,
        "source": source,
        "sha256": require_hash(value["sha256"], "report sha256"),
        "bytes": require_count(value["bytes"], "report bytes"),
    }


def parse_artifacts(value, report: dict) -> list[dict]:
    if type(value) is not list or not value:
        refuse("artifacts must be a non-empty list")
    if len(value) > 32:
        refuse("artifacts list is too long")
    found = []
    seen = set()
    for item in value:
        if type(item) is not dict:
            refuse("artifact is not an object")
        require_exact(item, ARTIFACT_KEYS, "artifact")
        clerk_path = require_filename(item["clerk_path"], "artifact clerk path")
        source = require_filename(item["source"], "artifact source")
        logical = require_filename(item["logical"], "artifact logical")
        if source != clerk_path or logical != clerk_path:
            refuse("artifact mapping is ambiguous")
        if clerk_path in seen:
            refuse(f"duplicate artifact {clerk_path}")
        seen.add(clerk_path)
        parsed = {
            "clerk_path": clerk_path,
            "source": source,
            "logical": logical,
            "sha256": require_hash(item["sha256"], "artifact sha256"),
            "bytes": require_count(item["bytes"], "artifact bytes"),
        }
        if clerk_path == report["clerk_path"] and (
            parsed["sha256"] != report["sha256"] or parsed["bytes"] != report["bytes"]
        ):
            refuse("report does not match its captured artifact")
        found.append(parsed)
    return found


def binding_sha(body: bytes) -> str:
    return sha256_bytes(body)


def launch(script: str, args: list[str], pins: dict) -> tuple[int, str, str]:
    check_pins(pins)
    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env["GIT_OPTIONAL_LOCKS"] = "0"
    env["GIT_TERMINAL_PROMPT"] = "0"
    try:
        proc = subprocess.run(
            [sys.executable, "-B", script, *args],
            cwd=str(ROOT),
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=False,
            timeout=TIMEOUT_S,
        )
    except subprocess.TimeoutExpired:
        refuse("tool timed out")
    stdout = proc.stdout.replace(b"\r\n", b"\n").decode("utf-8", errors="backslashreplace")
    stderr = proc.stderr.replace(b"\r\n", b"\n").decode("utf-8", errors="backslashreplace")
    return proc.returncode, stdout, stderr


def parse_tool_json(text: str, label: str) -> dict:
    try:
        value = json.loads(text)
    except json.JSONDecodeError:
        refuse(f"{label} output is not json")
    if type(value) is not dict:
        refuse(f"{label} output is not an object")
    return value


def call_hook(hook, point: str) -> None:
    if hook is None:
        return
    if point not in HOOK_POINTS:
        refuse(f"hook point is not usable: {point}")
    marker = hook(point)
    if marker == "stop":
        raise Stop(point)
    if marker not in (None, ""):
        refuse("hook returned an unknown marker")


def load_returned(document: dict, parsed: dict) -> tuple[dict, dict]:
    if document.get("schema") != INSPECTION_SCHEMA:
        refuse("inspection schema is not clerk-handoff-inspection/2")
    if document.get("job_id") != parsed["job_id"]:
        refuse("inspection job does not match the binding")
    if document.get("state") != "returned" or type(document.get("returned")) is not dict:
        refuse(f"state is {document.get('state')}")
    returned = document["returned"]
    for key in ("by", "delivery", "evidence", "artifacts", "event_sha256"):
        if key not in returned:
            refuse(f"returned inspection misses {key}")
    if returned["event_sha256"] != parsed["returned_event_sha256"]:
        refuse("returned event does not match the binding")
    if returned["by"] != parsed["assignee"]:
        refuse("assignee does not match the returned job")
    require_text(returned["delivery"], "transport delivery")
    require_text(returned["evidence"], "transport evidence")
    checks = document.get("checks")
    if type(checks) is not dict:
        refuse("inspection checks are missing")
    if checks.get("instructions") != "usable":
        refuse(f"instructions are {checks.get('instructions')}")
    if checks.get("artifacts") == "changed":
        refuse("artifacts are changed")
    if (
        checks.get("events") != "ok"
        or checks.get("completion") != "ok"
        or checks.get("artifacts") != "ok"
        or document.get("problems") != []
    ):
        refuse("returned inspection is not clean")
    artifacts = returned["artifacts"]
    if type(artifacts) is not list:
        refuse("returned artifacts are not a list")
    found = {}
    for item in artifacts:
        if type(item) is not dict or set(item) != {"bytes", "path", "sha256"}:
            refuse("returned artifact shape is not path, sha256, and bytes")
        name = item["path"]
        if type(name) is not str or name in found:
            refuse("returned artifact path is not usable")
        found[name] = {
            "sha256": require_hash(item["sha256"], "returned artifact sha256"),
            "bytes": require_count(item["bytes"], "returned artifact bytes"),
        }
    return found, {
        "delivery": returned["delivery"],
        "evidence": returned["evidence"],
    }


def match_identity(found: dict, item: dict, role: str) -> None:
    recorded = found.get(item["clerk_path"])
    if recorded is None:
        refuse(f"{role} is not a returned artifact")
    if recorded["sha256"] != item["sha256"] or recorded["bytes"] != item["bytes"]:
        refuse(f"{role} does not match the returned artifact record")


def read_identity(parsed: dict, item: dict, role: str) -> bytes:
    outbox = read_plain(file_under(parsed["artifact_base"], item["clerk_path"]), role + " outbox")
    source = read_plain(file_under(parsed["source_root"], item["source"]), role + " source")
    if outbox != source:
        refuse(f"{role} source bytes are not the outbox bytes")
    if sha256_bytes(source) != item["sha256"] or len(source) != item["bytes"]:
        refuse(f"{role} bytes do not match the binding")
    return source


def reservation_problem(view: dict, parsed: dict) -> str | None:
    reservation = view.get("reservation")
    if type(reservation) is not dict:
        return "reservation is missing from the inspection"
    origin = reservation.get("origin")
    destination = reservation.get("destination")
    if reservation.get("submission_id") != parsed["submission_id"]:
        return "submission does not match the reservation"
    if type(origin) is not dict or (
        origin.get("book"),
        origin.get("page"),
        origin.get("batch"),
    ) != (
        parsed["origin"]["book"],
        parsed["origin"]["page"],
        parsed["origin"]["batch"],
    ):
        return "origin does not match the reservation"
    if type(destination) is not dict or destination.get("path") != parsed["member"]:
        return "member does not match the reservation"
    if reservation.get("expected_outputs") != [item["logical"] for item in parsed["artifacts"]]:
        return "logical outputs do not match the reservation"
    return None


def inspect_member(parsed: dict, pins: dict) -> tuple[int, dict, str]:
    script = pins["inspect"][0]
    code, text, err = launch(
        script,
        ["inspect", "--book", parsed["book"], "--member", parsed["member"], "--json"],
        pins,
    )
    if err.strip() and not text.strip():
        refuse("inspect output is not json")
    document = parse_tool_json(text, "inspect")
    if document.get("schema") != MEMBER_SCHEMA:
        refuse("inspect schema is not return-capture-inspection/1")
    status = document.get("status")
    if status not in INSPECT_EXIT or code != INSPECT_EXIT[status]:
        refuse("inspect exit does not match its status")
    return code, document, text


def show_job(parsed: dict, pins: dict) -> tuple[int, dict, str]:
    script = pins["clerk"][0]
    code, text, err = launch(
        script,
        [
            "show",
            "--store", parsed["clerk_store"],
            "--job", parsed["job_id"],
            "--json",
            "--instructions-base", parsed["instructions_base"],
        ],
        pins,
    )
    if err.strip() and not text.strip():
        refuse("show output is not json")
    document = parse_tool_json(text, "show")
    return code, document, text


def write_exclusive(path: Path, data: bytes) -> None:
    flags = os.O_CREAT | os.O_EXCL | os.O_WRONLY
    if hasattr(os, "O_BINARY"):
        flags |= os.O_BINARY
    try:
        fd = os.open(str(path), flags)
    except FileExistsError:
        raise
    try:
        view = memoryview(data)
        while view:
            written = os.write(fd, view)
            if written <= 0:
                raise OSError("short write")
            view = view[written:]
        os.fsync(fd)
    finally:
        os.close(fd)
    if path.read_bytes() != data:
        refuse(f"record write did not land intact: {path.name}", attention=True)


def ensure_record_dir(path: Path) -> None:
    if not os.path.lexists(path):
        parent = path.parent
        require_plain_dir(parent, "record parent")
        os.mkdir(path)
    require_plain_dir(path, "record")


def record_names(path: Path) -> set[str]:
    if not os.path.lexists(path):
        return set()
    require_plain_dir(path, "record")
    return set(os.listdir(path))


def intent_body(parsed: dict, digest: str, transport: dict, identities: list[dict]) -> bytes:
    return canonical({
        "schema": RECORD_SCHEMA,
        "kind": "intent",
        "binding_sha256": digest,
        "returned_event_sha256": parsed["returned_event_sha256"],
        "job_id": parsed["job_id"],
        "submission_id": parsed["submission_id"],
        "member": parsed["member"],
        "work_ref": parsed["work_ref"],
        "work_ref_role": "declared-label",
        "transport": transport,
        "report": parsed["report"],
        "artifacts": identities,
    })


def completed_body(parsed: dict, digest: str, capture: dict) -> bytes:
    return canonical({
        "schema": RECORD_SCHEMA,
        "kind": "completed",
        "binding_sha256": digest,
        "returned_event_sha256": parsed["returned_event_sha256"],
        "reservation_sha256": capture["reservation_sha256"],
        "manifest_sha256": capture["manifest_sha256"],
        "receipt_sha256": capture["receipt_sha256"],
        "job_id": parsed["job_id"],
        "submission_id": parsed["submission_id"],
        "member": parsed["member"],
        "work_ref": parsed["work_ref"],
        "work_ref_role": "declared-label",
    })


def load_record(path: Path, kind: str) -> dict:
    raw = read_plain(path, kind)
    value = parse_object(raw, kind)
    if value.get("schema") != RECORD_SCHEMA or value.get("kind") != kind:
        refuse(f"{kind} record schema does not match", attention=True)
    return value


def capture_command(parsed: dict) -> list[str]:
    report = str(file_under(parsed["source_root"], parsed["report"]["source"]))
    args = [
        "capture",
        "--book", parsed["book"],
        "--submission", parsed["submission_id"],
        "--return-file", report,
        "--source-root", parsed["source_root"],
    ]
    for item in parsed["artifacts"]:
        args.extend(["--artifact", f"{item['source']}|{item['logical']}"])
    return args


def verify_text(parsed: dict, pins: dict) -> str:
    code, text, _err = launch(
        pins["capture"][0],
        ["verify", "--book", parsed["book"], "--member", parsed["member"]],
        pins,
    )
    if code != 0 or any(line not in text for line in CUSTODY):
        refuse("verify did not report custody", attention=True)
    return text


def payload_problem(parsed: dict, view: dict, sources: dict[str, bytes]) -> str | None:
    capture = view.get("capture")
    if type(capture) is not dict:
        return "complete inspection has no capture"
    returned = capture.get("return")
    report = sources[parsed["report"]["clerk_path"]]
    if type(returned) is not dict:
        return "complete inspection has no return"
    if returned.get("sha256") != sha256_bytes(report) or returned.get("bytes") != len(report):
        return "return bytes do not match the report"
    member = Path(parsed["book"]) / parsed["member"]
    on_disk = read_plain(member / "return.md", "return.md")
    if on_disk != report:
        return "return.md does not match the report"
    payloads = capture.get("payloads")
    if type(payloads) is not list or len(payloads) != len(parsed["artifacts"]):
        return "payload list does not match the binding"
    for index, (item, payload) in enumerate(zip(parsed["artifacts"], payloads), start=1):
        if type(payload) is not dict:
            return "payload shape is not usable"
        if payload.get("logical") != item["logical"]:
            return "payload order does not match the binding"
        blob = sources[item["clerk_path"]]
        if payload.get("sha256") != sha256_bytes(blob) or payload.get("bytes") != len(blob):
            return f"payload hash does not match {item['logical']}"
        disk = read_plain(member / "payload" / f"{index:04d}.blob", f"{index:04d}.blob")
        if disk != blob:
            return f"payload bytes do not match {item['logical']}"
    for key in ("reservation_sha256", "manifest_sha256", "receipt_sha256"):
        if type(capture.get(key)) is not str or not HEX64.fullmatch(capture[key]):
            return f"{key} is not usable"
    return None


def reread_sources(parsed: dict, sources: dict[str, bytes]) -> None:
    names = [parsed["report"]["clerk_path"]]
    names.extend(item["clerk_path"] for item in parsed["artifacts"])
    for name in dict.fromkeys(names):
        current = read_plain(file_under(parsed["source_root"], name), name)
        outbox = read_plain(file_under(parsed["artifact_base"], name), name + " outbox")
        if current != sources[name] or outbox != sources[name]:
            refuse("source bytes changed before the handoff record", attention=True)


def finish(kind: str, reason: str, writes: list[str], retained: list[str], extra: list[str]) -> tuple[int, str]:
    lines = []
    if kind == "ok":
        lines.extend(extra)
        if writes:
            lines.extend("writes " + item for item in writes)
        else:
            lines.append("writes none")
        lines.append("result ok")
        return 0, "\n".join(lines) + "\n"
    label = "attention" if kind == "attention" else "refused"
    lines.append(f"{label}: {reason}")
    lines.extend("retained " + item for item in retained)
    if writes:
        lines.extend("writes " + item for item in writes)
    else:
        lines.append("writes none")
    lines.append("result attention" if kind == "attention" else "result refused")
    return 2, "\n".join(lines) + "\n"


def try_failure_log(parsed: dict | None, safe: bool, payload: dict, writes: list[str], retained: list[str]) -> None:
    if not safe or parsed is None:
        return
    path = Path(parsed["failure_log"])
    if os.path.lexists(path):
        retained.append(str(path))
        return
    parent = path.parent
    if plain_dir_problem(parent) or is_reparse(parent):
        return
    try:
        write_exclusive(path, canonical(payload))
    except FileExistsError:
        retained.append(str(path))
        return
    except Refuse:
        retained.append(str(path))
        return
    writes.append("failure-log " + str(path))


def execute(binding_path: str, *, hook=None, pins=None) -> tuple[int, str]:
    parsed = None
    log_safe = False
    writes: list[str] = []
    retained: list[str] = []
    tool_text: list[str] = []
    inspection = None
    member_view = None
    digest = None
    sources: dict[str, bytes] = {}
    try:
        pins = default_pins() if pins is None else pins
        parsed, body = parse_binding(binding_path)
        digest = binding_sha(body)
        log_parent = Path(parsed["failure_log"]).parent
        require_plain_dir(log_parent, "failure log parent")
        log_safe = True
        check_pins(pins)
        require_plain_dir(Path(parsed["clerk_store"]), "clerk store")
        require_plain_dir(Path(parsed["instructions_base"]), "instructions base")
        require_plain_dir(Path(parsed["book"]), "book")
        call_hook(hook, "before-intent")
        show_code, inspection, show_text = show_job(parsed, pins)
        tool_text.append(show_text)
        if show_code not in (0, 1, 2):
            refuse(f"show exit is {show_code}")
        returned_map, transport = load_returned(inspection, parsed)
        if show_code != 0:
            refuse("returned inspection is not clean")
        require_plain_dir(Path(parsed["source_root"]), "source root")
        require_plain_dir(Path(parsed["artifact_base"]), "artifact base")
        match_identity(returned_map, parsed["report"], "report")
        for item in parsed["artifacts"]:
            match_identity(returned_map, item, "artifact")
        sources[parsed["report"]["clerk_path"]] = read_identity(parsed, parsed["report"], "report")
        for item in parsed["artifacts"]:
            sources[item["clerk_path"]] = read_identity(parsed, item, "artifact")
        _inspect_code, member_view, inspect_text = inspect_member(parsed, pins)
        tool_text.append(inspect_text)
        problem = reservation_problem(member_view, parsed)
        if problem and member_view.get("status") in ("reserved", "complete", "incomplete"):
            refuse(problem, attention=member_view.get("status") != "reserved")
        status = member_view.get("status")
        if status == "complete":
            return complete_retry(parsed, pins, digest, sources, member_view, writes, retained)
        if status == "incomplete":
            refuse("partial capture is retained", attention=True)
        if status != "reserved":
            refuse(f"member status is {status}")
        names = record_names(Path(parsed["record"]))
        unexpected = names - RECORD_FILES
        if unexpected:
            refuse("record directory has an unexpected entry", attention=True)
        if COMPLETED_NAME in names:
            refuse("completed record exists for a reserved member", attention=True)
        if INTENT_NAME in names:
            retained.append(str(Path(parsed["record"]) / INTENT_NAME))
            refuse("intent is retained", attention=True)
        ensure_record_dir(Path(parsed["record"]))
        identities = [dict(item) for item in parsed["artifacts"]]
        intent = intent_body(parsed, digest, transport, identities)
        intent_path = Path(parsed["record"]) / INTENT_NAME
        try:
            write_exclusive(intent_path, intent)
        except FileExistsError:
            retained.append(str(intent_path))
            refuse("intent is retained", attention=True)
        writes.append("intent " + str(intent_path))
        call_hook(hook, "after-intent")
        check_pins(pins)
        reread_sources(parsed, sources)
        code, capture_text, _err = launch(pins["capture"][0], capture_command(parsed), pins)
        tool_text.append(capture_text)
        if code != 0 or "result captured" not in capture_text.splitlines():
            retained.append(str(intent_path))
            refuse("capture did not complete", attention=True)
        if f"capture {parsed['member']}" not in capture_text:
            retained.append(str(intent_path))
            refuse("capture member does not match the binding", attention=True)
        call_hook(hook, "after-capture")
        check_pins(pins)
        reread_sources(parsed, sources)
        verified = verify_text(parsed, pins)
        tool_text.append(verified)
        _code, member_view, inspect_text = inspect_member(parsed, pins)
        tool_text.append(inspect_text)
        if member_view.get("status") != "complete":
            retained.append(str(intent_path))
            refuse("inspect is not complete after capture", attention=True)
        mismatch = payload_problem(parsed, member_view, sources)
        if mismatch:
            retained.append(str(intent_path))
            refuse(mismatch, attention=True)
        call_hook(hook, "before-final-record")
        check_pins(pins)
        reread_sources(parsed, sources)
        completed = completed_body(parsed, digest, member_view["capture"])
        completed_path = Path(parsed["record"]) / COMPLETED_NAME
        try:
            write_exclusive(completed_path, completed)
        except FileExistsError:
            retained.extend([str(intent_path), str(completed_path)])
            existing = completed_path.read_bytes()
            if existing == completed:
                return finish("ok", "", [], retained, custody_lines(verified, parsed))
            refuse("completed record exists and does not match", attention=True)
        writes.append("completed " + str(completed_path))
        return finish("ok", "", writes, retained, custody_lines(verified, parsed))
    except Stop as exc:
        return fail(
            parsed, log_safe, True, f"stopped {exc.point}", writes, retained,
            inspection, member_view, tool_text, digest,
        )
    except Refuse as exc:
        return fail(
            parsed, log_safe, exc.attention, exc.message, writes, retained,
            inspection, member_view, tool_text, digest,
        )
    except OSError as exc:
        return fail(
            parsed, log_safe, True, f"filesystem: {type(exc).__name__}: {exc.strerror or exc}",
            writes, retained, inspection, member_view, tool_text, digest,
        )


def custody_lines(verified: str, parsed: dict) -> list[str]:
    lines = [
        "returned-event " + parsed["returned_event_sha256"],
        "work-ref " + parsed["work_ref"],
        "work-ref-role declared-label",
    ]
    for line in verified.splitlines():
        if line in CUSTODY or line.startswith(("reservation ", "manifest ", "receipt ", "payload ")):
            lines.append(line)
    return lines


def complete_retry(parsed, pins, digest, sources, member_view, writes, retained):
    record = Path(parsed["record"])
    intent_path = record / INTENT_NAME
    completed_path = record / COMPLETED_NAME
    if not os.path.lexists(completed_path) or not os.path.lexists(intent_path):
        if os.path.lexists(intent_path):
            retained.append(str(intent_path))
        refuse("complete capture has no completed handoff record", attention=True)
    try:
        intent = load_record(intent_path, "intent")
        completed = load_record(completed_path, "completed")
    except Refuse:
        retained.append(str(completed_path))
        refuse("completed handoff record is not readable", attention=True)
    if intent.get("binding_sha256") != digest or completed.get("binding_sha256") != digest:
        retained.append(str(completed_path))
        refuse("completed handoff record does not match the binding", attention=True)
    if completed.get("returned_event_sha256") != parsed["returned_event_sha256"]:
        retained.append(str(completed_path))
        refuse("completed handoff record does not match the event", attention=True)
    if completed.get("work_ref") != parsed["work_ref"]:
        retained.append(str(completed_path))
        refuse("completed handoff record does not match the binding", attention=True)
    check_pins(pins)
    reread_sources(parsed, sources)
    verified = verify_text(parsed, pins)
    _code, fresh, _text = inspect_member(parsed, pins)
    if fresh.get("status") != "complete":
        refuse("inspect is not complete", attention=True)
    mismatch = payload_problem(parsed, fresh, sources)
    if mismatch:
        refuse(mismatch, attention=True)
    capture = fresh["capture"]
    for key in ("reservation_sha256", "manifest_sha256", "receipt_sha256"):
        if completed.get(key) != capture.get(key):
            retained.append(str(completed_path))
            refuse("completed handoff record does not match the receipt", attention=True)
    del member_view
    return finish("ok", "", writes, retained, custody_lines(verified, parsed))


def fail(parsed, log_safe, attention, reason, writes, retained, inspection, member_view, tool_text, digest):
    kind = "attention" if attention else "refused"
    payload = {
        "schema": FAILURE_SCHEMA,
        "binding_sha256": digest,
        "reason": reason,
        "writes": list(writes),
        "retained": list(retained),
        "inspection": inspection,
        "inspect": member_view,
        "tool_stdout": tool_text,
    }
    before = len(writes)
    try_failure_log(parsed, log_safe, payload, writes, retained)
    if len(writes) == before and log_safe and parsed is not None and os.path.lexists(parsed["failure_log"]):
        if str(parsed["failure_log"]) not in retained:
            retained.append(str(parsed["failure_log"]))
    return finish(kind, reason, writes, retained, [])


def perform(binding_path: str, *, hook=None, pins=None) -> int:
    code, text = execute(binding_path, hook=hook, pins=pins)
    sys.stdout.write(text)
    return code


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="handoff.py")
    sub = parser.add_subparsers(dest="command", required=True)
    perform_cmd = sub.add_parser("perform")
    perform_cmd.add_argument("--binding", required=True)
    try:
        args = parser.parse_args(sys.argv[1:] if argv is None else argv)
    except SystemExit as exc:
        code = exc.code
        return 2 if code is None else int(code)
    if args.command != "perform":
        return 2
    return perform(args.binding)


if __name__ == "__main__":
    sys.exit(main())
