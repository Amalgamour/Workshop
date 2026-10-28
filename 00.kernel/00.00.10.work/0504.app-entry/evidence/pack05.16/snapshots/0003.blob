"""File-backed Clerk handoff lab. Python standard library only.

Patterns cited from the preserved pass01 lab, not imported
(labs/clerk-handoff-pass01/clerk_lab.py):

- canonical JSON and sha256, lines 21-30
- hash-linked events and a reducer that refuses a broken chain, lines 29-84
- identical delivery is already-recorded; a changed body under that id refuses,
  lines 183-188
- a claim token, and a return that must match the claim, lines 166-169 and 191-193
- an artifact stored as path plus hash and checked again on read, lines 135-141
- path containment, lines 126-133
- explicit resume of an unfinished claim, lines 154-160
- a view is a projection and is never the record, lines 224-232

Not carried forward: hard-coded recipients, closure on an accepted review,
role-selected next(), and SQLite. This module does not import pass01, app/,
the worker bridge, or the kernel.

Schema clerk-handoff-pass02/2. A returned job also has one exclusive-create
completion witness, written before the returned event, recording that event
file's digest. Schema clerk-handoff-pass02/1 is recognized and refused,
not migrated. Every mutation is an exclusive create. An interrupted write
is left in place and is not a successful state. show --json prints one
read-only projection, schema clerk-handoff-inspection/2, and does not write.
Inspection/2 adds returned.event_sha256; its predecessor inspection/1 had no
event digest.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import secrets
import stat
import sys
import unicodedata
from datetime import datetime, timezone
from pathlib import Path


SCHEMA = "clerk-handoff-pass02/2"
EARLIER_SCHEMA = "clerk-handoff-pass02/1"
INSPECTION_SCHEMA = "clerk-handoff-inspection/2"  # predecessor /1: the same document without returned.event_sha256
QUEUED_NAME = "0001.queued.json"
CLAIMED_NAME = "0002.claimed.json"
RETURNED_NAME = "0003.returned.json"
WITNESS_NAME = "0003.witness.json"
KNOWN_NAMES = {QUEUED_NAME, CLAIMED_NAME, RETURNED_NAME, WITNESS_NAME, "outbox"}
JOB_KEYS = {
    "assignee",
    "expected_outputs",
    "instructions",
    "job_id",
    "release",
    "reviewer",
    "routed_by",
}
INSTRUCTION_KEYS = {"path", "sha256"}
QUEUED_KEYS = {"at", "job", "kind", "prev", "schema"}
CLAIMED_KEYS = {"at", "by", "claim", "kind", "prev", "schema"}
RETURNED_KEYS = {
    "artifacts",
    "at",
    "by",
    "claim",
    "delivery",
    "evidence",
    "kind",
    "prev",
    "schema",
}
ARTIFACT_KEYS = {"bytes", "path", "sha256"}
WITNESS_KEYS = {"event", "job_id", "kind", "schema", "sha256"}
FILE_ATTRIBUTE_REPARSE_POINT = 0x400
_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,63}$")
_HEX64 = re.compile(r"^[0-9a-f]{64}$")
_TOKEN = re.compile(r"^[0-9a-f]{32}$")
_RESERVED = {"CON", "PRN", "AUX", "NUL"}
_RESERVED.update(f"COM{i}" for i in range(1, 10))
_RESERVED.update(f"LPT{i}" for i in range(1, 10))


class Refusal(Exception):
    pass


class Incomplete(Refusal):
    pass


class Result:
    def __init__(self, code: int, text: str) -> None:
        self.code = code
        self.text = text


def finish(code: int, lines: list[str]) -> Result:
    label = {0: "result ok", 1: "result findings", 2: "result refused"}[code]
    return Result(code, "\n".join([*lines, label]) + "\n")


def refuse(message: str) -> None:
    if not message.startswith("refused:"):
        message = "refused: " + message
    raise Refusal(message)


def incomplete(message: str) -> None:
    if not message.startswith("incomplete:"):
        message = "incomplete: " + message
    raise Incomplete(message)


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


def now_stamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")


def new_token() -> str:
    return secrets.token_hex(16)


def loads_strict(text: str):
    def reject_constant(name: str):
        refuse(f"nonfinite JSON {name}")

    def pairs(seq):
        obj = {}
        for key, value in seq:
            if not isinstance(key, str):
                refuse("JSON key is not a string")
            if key in obj:
                refuse("duplicate JSON key")
            obj[key] = value
        return obj

    try:
        return json.loads(text, object_pairs_hook=pairs, parse_constant=reject_constant)
    except Refusal:
        raise
    except json.JSONDecodeError:
        refuse("invalid JSON")


def is_reparse(path: Path) -> bool:
    st = os.lstat(path)
    attrs = getattr(st, "st_file_attributes", 0) or 0
    if attrs & FILE_ATTRIBUTE_REPARSE_POINT:
        return True
    return stat.S_ISLNK(st.st_mode)


def plain_file_problem(path: Path) -> str | None:
    if not os.path.lexists(path):
        return "missing"
    if is_reparse(path):
        return "link"
    st = os.lstat(path)
    if not stat.S_ISREG(st.st_mode):
        return "not-regular"
    if st.st_nlink != 1:
        return "link-count"
    return None


def plain_dir_problem(path: Path) -> str | None:
    if not os.path.lexists(path):
        return "missing"
    if is_reparse(path):
        return "link"
    st = os.lstat(path)
    if not stat.S_ISDIR(st.st_mode):
        return "not-directory"
    return None


def id_problem(value, label: str) -> str | None:
    if not isinstance(value, str):
        return f"refused: {label} is not a string"
    if value != unicodedata.normalize("NFKC", value):
        return f"refused: {label} is ambiguous"
    if not _ID.fullmatch(value) or value.endswith(".") or value.endswith(" "):
        return f"refused: {label} is not a windows-safe id"
    if value.split(".", 1)[0].upper() in _RESERVED:
        return f"refused: {label} is a reserved windows name"
    return None


def require_text(value, label: str) -> None:
    if not isinstance(value, str):
        refuse(f"{label} is not a string")
    if value == "" or any(ord(ch) < 32 for ch in value):
        refuse(f"{label} is empty or has control characters")


def absolute_path(text: str, label: str) -> Path:
    if not isinstance(text, str) or not os.path.isabs(text):
        refuse(f"{label} must be absolute")
    return Path(os.path.abspath(text))


def _chains(path: Path):
    seen = set()

    def walk(start: Path):
        current = start
        while True:
            key = str(current).casefold()
            if key in seen:
                return
            seen.add(key)
            yield current
            parent = current.parent
            if parent == current:
                return
            current = parent

    yield from walk(path)
    existing = path
    while not os.path.lexists(existing):
        parent = existing.parent
        if parent == existing:
            return
        existing = parent
    try:
        real = Path(os.path.realpath(existing))
    except OSError:
        refuse("store path cannot be resolved")
    yield from walk(real)


def assert_outside_git(path: Path) -> None:
    for ancestor in _chains(path):
        marker = ancestor / ".git"
        if os.path.lexists(marker):
            refuse("store resolves inside a Git working tree")


def exclusive_write(
    path: Path,
    data: bytes,
    interrupt: bool,
    interrupt_message: str = "event publication interrupted",
) -> None:
    try:
        handle = open(path, "xb")
    except FileExistsError:
        refuse("record already exists")
    try:
        if interrupt:
            handle.write(data[:1] if data else b"{")
            handle.flush()
            os.fsync(handle.fileno())
            incomplete(interrupt_message)
        handle.write(data)
        handle.flush()
        os.fsync(handle.fileno())
    finally:
        handle.close()
    written = path.read_bytes()
    if interrupt:
        return
    if written != data:
        incomplete("event publication did not land intact")


def validate_job(job) -> None:
    if not isinstance(job, dict):
        refuse("job must be a JSON object")
    if set(job) != JOB_KEYS:
        unknown = sorted(set(job) - JOB_KEYS)
        missing = sorted(JOB_KEYS - set(job))
        if unknown:
            refuse("unknown job key " + unknown[0])
        refuse("missing job key " + missing[0])
    for label in ("job_id", "assignee", "reviewer"):
        problem = id_problem(job[label], label)
        if problem:
            raise Refusal(problem)
    if job["assignee"].casefold() == job["reviewer"].casefold():
        refuse("assignee and reviewer must differ")
    require_text(job["release"], "release")
    require_text(job["routed_by"], "routed_by")
    instructions = job["instructions"]
    if not isinstance(instructions, dict) or set(instructions) != INSTRUCTION_KEYS:
        refuse("instructions must be path and sha256")
    path = instructions["path"]
    if not isinstance(path, str):
        refuse("instruction path is not a string")
    if "\\" in path or path.startswith("/") or (len(path) >= 2 and path[1] == ":"):
        refuse("instruction path must be a relative forward-slash path")
    parts = path.split("/")
    if any(part in ("", ".", "..") for part in parts):
        refuse("instruction path traversal")
    for part in parts:
        problem = id_problem(part, "instruction path segment")
        if problem:
            raise Refusal(problem)
    digest = instructions["sha256"]
    if not isinstance(digest, str) or not _HEX64.fullmatch(digest):
        refuse("instruction sha256 must be 64 lowercase hex characters")
    outputs = job["expected_outputs"]
    if not isinstance(outputs, list):
        refuse("expected_outputs must be a list")
    if not outputs:
        refuse("expected_outputs must be a non-empty list")
    seen = set()
    for name in outputs:
        if not isinstance(name, str) or "/" in name or "\\" in name or name in (".", ".."):
            refuse("output path is not a simple filename")
        problem = id_problem(name, "output name")
        if problem:
            refuse("output path is not a simple filename")
        folded = name.casefold()
        if folded in seen:
            refuse("case-colliding output names")
        seen.add(folded)


def resolve_instructions(base_text: str, instructions: dict) -> Path:
    base = absolute_path(base_text, "instructions base")
    problem = plain_dir_problem(base)
    if problem:
        refuse("instructions base is not a plain directory")
    current = base
    file_path = None
    for part in instructions["path"].split("/"):
        current = current / part
        file_path = current
        if not os.path.lexists(current):
            refuse("instruction file is missing")
        if is_reparse(current):
            refuse("instruction path contains a link")
    if file_path is None or plain_file_problem(file_path):
        refuse("instruction file is not a plain file")
    try:
        base_resolved = base.resolve()
        file_resolved = file_path.resolve()
        file_resolved.relative_to(base_resolved)
    except (OSError, ValueError):
        refuse("instruction path escapes the named base")
    data = file_path.read_bytes()
    if sha256_bytes(data) != instructions["sha256"]:
        refuse("instruction hash mismatch")
    return file_path


def instruction_status(base_text: str | None, job: dict | None) -> str:
    if base_text is None:
        return "instructions-not-checked"
    if job is None:
        return "instructions-unusable job record missing"
    try:
        resolve_instructions(base_text, job["instructions"])
    except Refusal as exc:
        detail = str(exc)
        if detail.startswith("refused: "):
            detail = detail[len("refused: "):]
        return "instructions-unusable " + detail
    return "instructions-usable sha256=" + job["instructions"]["sha256"]


def read_job_file(path_text: str) -> dict:
    path = absolute_path(path_text, "job file path")
    if not os.path.lexists(path):
        refuse("job file is missing")
    if plain_file_problem(path):
        refuse("job file is not a plain file")
    try:
        text = path.read_bytes().decode("utf-8")
    except UnicodeDecodeError:
        refuse("job file is not UTF-8")
    job = loads_strict(text)
    validate_job(job)
    return job


def guard_store(path_text: str) -> Path:
    path = absolute_path(path_text, "store path")
    assert_outside_git(path)
    return path


def existing_store(path_text: str) -> Path:
    path = guard_store(path_text)
    if not os.path.lexists(path):
        refuse("no matching store")
    if plain_dir_problem(path):
        refuse("store path is not a plain directory")
    return path


class View:
    def __init__(self, name: str) -> None:
        self.name = name
        self.status = "bad"
        self.structural = True
        self.diagnosis = "unreadable job"
        self.job = None
        self.token = None
        self.events = []
        self.states = []
        self.chain_ok = False
        self.artifacts = []
        self.claim_by = None
        self.delivery = None
        self.evidence = None
        self.return_by = None

    @property
    def assignee(self):
        return None if self.job is None else self.job.get("assignee")

    @property
    def reviewer(self):
        return None if self.job is None else self.job.get("reviewer")


def _event_sha(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def _parse_event(path: Path):
    try:
        text = path.read_bytes().decode("utf-8")
        return loads_strict(text), None
    except (Refusal, UnicodeDecodeError, OSError) as exc:
        return None, str(exc)


def _require_stamp(event: dict, keys: set[str], kind: str) -> str | None:
    if not isinstance(event, dict):
        return "event schema mismatch"
    schema = event.get("schema")
    if schema == EARLIER_SCHEMA:
        return "earlier store format " + EARLIER_SCHEMA
    if set(event) != keys:
        return "event schema mismatch"
    if schema != SCHEMA or event.get("kind") != kind:
        return "event schema mismatch"
    if not isinstance(event.get("at"), str) or event["at"] == "":
        return "event schema mismatch"
    return None


def _read_witness(path: Path, job_id: str):
    try:
        text = path.read_bytes().decode("utf-8")
    except (OSError, UnicodeDecodeError):
        return None, "partial completion witness"
    try:
        event = loads_strict(text)
    except Refusal:
        return None, "partial completion witness"
    if not isinstance(event, dict) or event.get("schema") == EARLIER_SCHEMA:
        if isinstance(event, dict) and event.get("schema") == EARLIER_SCHEMA:
            return None, "earlier store format " + EARLIER_SCHEMA
        return None, "invalid completion witness"
    if (
        set(event) != WITNESS_KEYS
        or event.get("schema") != SCHEMA
        or event.get("kind") != "completion"
        or event.get("job_id") != job_id
        or event.get("event") != RETURNED_NAME
    ):
        return None, "invalid completion witness"
    digest = event.get("sha256")
    if not isinstance(digest, str) or not _HEX64.fullmatch(digest):
        return None, "invalid completion witness"
    return event, None


def _os_lines(exc: OSError, store: Path | None, job_id: str | None) -> list[str]:
    detail = exc.strerror or str(exc)
    lines = [f"incomplete: filesystem error: {type(exc).__name__}: {detail}"]
    if store is None or not job_id:
        lines.append("claim event was not checked")
        return lines
    claimed = store / "jobs" / job_id / CLAIMED_NAME
    try:
        exists = os.path.lexists(claimed)
    except OSError:
        lines.append("claim event was not checked")
        return lines
    if not exists:
        lines.append("claim event does not exist")
        return lines
    lines.append("claim event exists")
    event, error = _parse_event(claimed)
    token = event.get("claim") if isinstance(event, dict) else None
    if error is None and isinstance(token, str) and _TOKEN.fullmatch(token):
        lines.append("existing token " + token)
    lines.append("no new token")
    lines.append("record left in place")
    return lines


def _apply_completion(job_dir: Path, view: View) -> None:
    witness_path = job_dir / WITNESS_NAME
    returned_path = job_dir / RETURNED_NAME
    has_witness = os.path.lexists(witness_path)
    has_return = os.path.lexists(returned_path)
    if not has_witness and not has_return:
        view.status = "claimed"
        view.structural = False
        view.diagnosis = ""
        view.chain_ok = True
        return
    if has_witness and not has_return:
        _parsed, error = _read_witness(witness_path, view.name)
        view.status = "incomplete"
        view.diagnosis = (
            "partial completion witness"
            if error == "partial completion witness"
            else "completion witness without returned event"
        )
        return
    if has_return and not has_witness:
        parsed, _error = _parse_event(returned_path)
        schema = parsed.get("schema") if isinstance(parsed, dict) else None
        if schema == EARLIER_SCHEMA:
            view.diagnosis = "earlier store format " + EARLIER_SCHEMA
            return
        view.status = "incomplete"
        view.diagnosis = "returned event without completion witness"
        return
    witness, error = _read_witness(witness_path, view.name)
    if error:
        if error.startswith("earlier store format"):
            view.diagnosis = error
            return
        view.status = "incomplete"
        view.diagnosis = error
        return
    try:
        returned_bytes = returned_path.read_bytes()
    except OSError:
        view.status = "incomplete"
        view.diagnosis = "returned event is unreadable"
        return
    if sha256_bytes(returned_bytes) != witness["sha256"]:
        view.status = "incomplete"
        view.diagnosis = "completion witness mismatch"
        return
    returned, error = _parse_event(returned_path)
    if error or not isinstance(returned, dict):
        view.status = "incomplete"
        view.diagnosis = "invalid event 0003.returned.json"
        return
    schema_error = _require_stamp(returned, RETURNED_KEYS, "returned")
    if schema_error:
        view.diagnosis = schema_error
        return
    claimed_sha = view.events[-1][1]
    if returned.get("prev") != claimed_sha:
        view.diagnosis = "hash chain mismatch"
        return
    if returned.get("claim") != view.token or returned.get("by") != view.assignee:
        view.diagnosis = "return does not match claim"
        return
    problem = id_problem(returned.get("delivery"), "delivery")
    if problem or not isinstance(returned.get("evidence"), str) or returned["evidence"].strip() == "":
        view.diagnosis = "event schema mismatch"
        return
    artifacts = returned.get("artifacts")
    expected = view.job["expected_outputs"]
    if not isinstance(artifacts, list) or len(artifacts) != len(expected) or not expected:
        view.diagnosis = "artifact list does not match expected outputs"
        return
    for item, name in zip(artifacts, expected):
        if not isinstance(item, dict) or set(item) != ARTIFACT_KEYS:
            view.diagnosis = "event schema mismatch"
            return
        if item["path"] != name or not isinstance(item["sha256"], str):
            view.diagnosis = "artifact list does not match expected outputs"
            return
        if not _HEX64.fullmatch(item["sha256"]) or type(item["bytes"]) is not int:
            view.diagnosis = "event schema mismatch"
            return
        if item["bytes"] < 0:
            view.diagnosis = "event schema mismatch"
            return
    view.artifacts = artifacts
    view.delivery = returned["delivery"]
    view.evidence = returned["evidence"]
    view.return_by = returned["by"]
    view.events.append((RETURNED_NAME, sha256_bytes(returned_bytes), claimed_sha))
    view.states.append("returned")
    view.status = "returned"
    view.structural = False
    view.diagnosis = ""
    view.chain_ok = True


def classify(job_dir: Path) -> View:
    view = View(job_dir.name)
    problem = plain_dir_problem(job_dir)
    if problem:
        view.diagnosis = "job path is not a plain directory"
        return view
    try:
        names = sorted(os.listdir(job_dir))
    except OSError:
        view.diagnosis = "job directory is unreadable"
        return view
    unknown = sorted(set(names) - KNOWN_NAMES)
    planted = [
        name for name in unknown
        if "witness" in name.casefold() or "completion" in name.casefold()
    ]
    if planted:
        view.diagnosis = "planted completion metadata " + planted[0]
        return view
    if unknown:
        view.diagnosis = "extra file " + unknown[0]
        return view
    queued_path = job_dir / QUEUED_NAME
    claimed_path = job_dir / CLAIMED_NAME
    returned_path = job_dir / RETURNED_NAME
    outbox = job_dir / "outbox"
    if not os.path.lexists(queued_path):
        view.status = "incomplete"
        view.diagnosis = (
            "job directory has no queue event"
            if not names
            else "missing event 0001.queued.json"
        )
        return view
    event, error = _parse_event(queued_path)
    if error or not isinstance(event, dict):
        view.status = "incomplete"
        view.diagnosis = "invalid event 0001.queued.json"
        return view
    schema_error = _require_stamp(event, QUEUED_KEYS, "queued")
    if schema_error or event.get("prev") is not None:
        view.diagnosis = schema_error or "hash chain mismatch"
        return view
    try:
        validate_job(event["job"])
    except Refusal:
        view.diagnosis = "event schema mismatch"
        return view
    if event["job"]["job_id"] != job_dir.name:
        view.diagnosis = "job id does not match its folder"
        return view
    queued_sha = _event_sha(queued_path)
    view.events.append((QUEUED_NAME, queued_sha, "null"))
    view.job = event["job"]
    view.states = ["queued"]
    has_claim = os.path.lexists(claimed_path)
    has_return = os.path.lexists(returned_path)
    has_outbox = os.path.lexists(outbox)
    has_witness = os.path.lexists(job_dir / WITNESS_NAME)
    if has_return and not has_claim:
        view.diagnosis = "planted return before claim"
        return view
    if has_outbox and not has_claim:
        view.diagnosis = "outbox exists without a claim"
        return view
    if not has_claim:
        if has_witness:
            view.diagnosis = "planted completion metadata " + WITNESS_NAME
            return view
        view.status = "queued"
        view.structural = False
        view.diagnosis = ""
        view.chain_ok = True
        return view
    claimed, error = _parse_event(claimed_path)
    if error or not isinstance(claimed, dict):
        view.status = "incomplete"
        view.diagnosis = "invalid event 0002.claimed.json"
        return view
    schema_error = _require_stamp(claimed, CLAIMED_KEYS, "claimed")
    if schema_error:
        view.diagnosis = schema_error
        return view
    if claimed.get("prev") != queued_sha:
        view.diagnosis = "hash chain mismatch"
        return view
    if claimed.get("by") != view.assignee or not isinstance(claimed.get("claim"), str):
        view.diagnosis = "event schema mismatch"
        return view
    if not _TOKEN.fullmatch(claimed["claim"]):
        view.diagnosis = "event schema mismatch"
        return view
    view.token = claimed["claim"]
    view.claim_by = claimed["by"]
    view.events.append((CLAIMED_NAME, _event_sha(claimed_path), queued_sha))
    view.states.append("claimed")
    if not has_outbox and not has_return:
        view.status = "incomplete"
        view.diagnosis = "claim recorded but outbox is missing"
        return view
    if plain_dir_problem(outbox):
        view.diagnosis = "outbox is not a plain directory"
        return view
    _apply_completion(job_dir, view)
    return view


def store_entries(store: Path) -> tuple[list[str], list[View]]:
    problems = []
    try:
        children = sorted(os.listdir(store))
    except OSError:
        refuse("store path is not readable")
    jobs_dir = None
    for name in children:
        if name == "jobs":
            jobs_dir = store / name
            continue
        if name.casefold() == "jobs":
            problems.append("bad state: case-colliding jobs directory")
            continue
        problems.append("bad state: unexpected store entry " + name)
    views = []
    if jobs_dir is None:
        return problems, views
    if plain_dir_problem(jobs_dir):
        problems.append("bad state: jobs is not a plain directory")
        return problems, views
    folded = {}
    for name in sorted(os.listdir(jobs_dir)):
        folded.setdefault(name.casefold(), []).append(name)
    for name in sorted(os.listdir(jobs_dir)):
        if len(folded[name.casefold()]) > 1:
            view = View(name)
            view.diagnosis = "case-colliding job folder"
            views.append(view)
            continue
        views.append(classify(jobs_dir / name))
    return problems, views


def structural_line(view: View) -> str:
    if view.status == "incomplete":
        return "bad state: incomplete: " + view.diagnosis
    return "bad state: " + view.diagnosis


def inspect_artifacts(store: Path, view: View) -> list[str]:
    if view.status != "returned":
        return []
    outbox = store / "jobs" / view.name / "outbox"
    expected = [item["path"] for item in view.artifacts]
    try:
        present = sorted(os.listdir(outbox))
    except OSError:
        present = []
    lines = []
    expected_set = set(expected)
    for extra in present:
        if extra not in expected_set:
            lines.append(f"artifact {extra} artifact changed extra outbox file")
    for item in view.artifacts:
        path = outbox / item["path"]
        problem = plain_file_problem(path)
        if problem:
            lines.append(
                f"artifact {item['path']} sha256={item['sha256']} artifact changed"
            )
            continue
        data = path.read_bytes()
        digest = sha256_bytes(data)
        if digest != item["sha256"] or len(data) != item["bytes"]:
            lines.append(
                f"artifact {item['path']} sha256={item['sha256']} artifact changed"
            )
        else:
            lines.append(
                f"artifact {item['path']} sha256={digest} bytes={len(data)} ok"
            )
    return lines


def artifacts_dirty(lines: list[str]) -> bool:
    return any("artifact changed" in line for line in lines)


def _codes(structural: bool, dirty: bool, unusable: bool) -> int:
    if structural:
        return 2
    if dirty or unusable:
        return 1
    return 0


def _ensure_store_dirs(store: Path) -> Path:
    if os.path.lexists(store):
        if plain_dir_problem(store):
            refuse("store path is not a plain directory")
        children = list(os.listdir(store))
        for name in children:
            if name != "jobs":
                refuse("store contains an unexpected entry")
    else:
        parent = store.parent
        if plain_dir_problem(parent):
            refuse("store parent is not a plain directory")
        os.mkdir(store)
    jobs = store / "jobs"
    if not os.path.lexists(jobs):
        os.mkdir(jobs)
    elif plain_dir_problem(jobs):
        refuse("jobs is not a plain directory")
    return jobs


def _job_collision(jobs: Path, job_id: str) -> None:
    if not os.path.lexists(jobs):
        return
    for name in os.listdir(jobs):
        if name.casefold() == job_id.casefold():
            refuse("job id collides with an existing job")


def _require_actor(actor: str) -> None:
    problem = id_problem(actor, "actor")
    if problem:
        raise Refusal(problem)


def _find_view(store: Path, job_id: str) -> View | None:
    problem = id_problem(job_id, "job_id")
    if problem:
        raise Refusal(problem)
    _problems, views = store_entries(store)
    for view in views:
        if view.name == job_id:
            return view
        if view.name.casefold() == job_id.casefold() and view.name != job_id:
            refuse("job id collides with an existing job")
    return None


def queue(store_text: str, job_text: str, base_text: str, *, interrupt=None) -> Result:
    store = None
    job_id = None
    try:
        if interrupt not in (None, "publish"):
            refuse("unknown interrupt seam")
        job = read_job_file(job_text)
        job_id = job["job_id"]
        resolve_instructions(base_text, job["instructions"])
        store = guard_store(store_text)
        jobs = _ensure_store_dirs(store)
        _job_collision(jobs, job["job_id"])
        job_dir = jobs / job["job_id"]
        os.mkdir(job_dir)
        event = {
            "schema": SCHEMA,
            "kind": "queued",
            "job": job,
            "at": now_stamp(),
            "prev": None,
        }
        data = canonical(event)
        path = job_dir / QUEUED_NAME
        exclusive_write(path, data, interrupt == "publish")
        digest = sha256_bytes(path.read_bytes())
        return finish(0, [
            "queued " + job["job_id"],
            f"event {QUEUED_NAME} sha256={digest}",
        ])
    except Incomplete as exc:
        return finish(2, [str(exc)])
    except Refusal as exc:
        return finish(2, [str(exc)])
    except OSError as exc:
        return finish(2, _os_lines(exc, store, job_id))


def claim(store_text: str, job_id: str, actor: str, base_text: str, resume: bool = False, *, interrupt=None) -> Result:
    store = None
    try:
        if interrupt not in (None, "publish", "outbox"):
            refuse("unknown interrupt seam")
        _require_actor(actor)
        store = existing_store(store_text)
        view = _find_view(store, job_id)
        if view is None:
            refuse("no matching job")
        if view.structural:
            refuse(structural_line(view))
        if actor != view.assignee:
            refuse("not assignee")
        if resume:
            if view.status != "claimed":
                refuse("resume requires a complete claim")
            if interrupt is not None:
                refuse("unknown interrupt seam")
            resolve_instructions(base_text, view.job["instructions"])
            status = instruction_status(base_text, view.job)
            return finish(0, [
                "resume " + job_id,
                "token " + view.token,
                status,
            ])
        if view.status == "claimed":
            refuse("already claimed")
        if view.status == "returned":
            refuse("already returned")
        if view.status != "queued":
            refuse(structural_line(view))
        resolve_instructions(base_text, view.job["instructions"])
        prev = view.events[0][1]
        token = new_token()
        event = {
            "schema": SCHEMA,
            "kind": "claimed",
            "claim": token,
            "by": actor,
            "at": now_stamp(),
            "prev": prev,
        }
        data = canonical(event)
        claimed_path = store / "jobs" / job_id / CLAIMED_NAME
        exclusive_write(claimed_path, data, interrupt == "publish")
        if interrupt == "outbox":
            incomplete("interrupted before outbox setup")
        outbox = store / "jobs" / job_id / "outbox"
        os.mkdir(outbox)
        if plain_dir_problem(outbox):
            incomplete("outbox setup did not create a plain directory")
        digest = sha256_bytes(claimed_path.read_bytes())
        status = instruction_status(base_text, view.job)
        return finish(0, [
            "claimed " + job_id,
            "token " + token,
            f"event {CLAIMED_NAME} sha256={digest}",
            status,
        ])
    except Incomplete as exc:
        return finish(2, [str(exc)])
    except Refusal as exc:
        return finish(2, [str(exc)])
    except OSError as exc:
        return finish(2, _os_lines(exc, store, job_id))


def _current_artifacts(store: Path, view: View):
    outbox = store / "jobs" / view.name / "outbox"
    if plain_dir_problem(outbox):
        return None, "outbox is not a plain directory"
    try:
        present = sorted(os.listdir(outbox))
    except OSError:
        return None, "outbox is not readable"
    expected = list(view.job["expected_outputs"])
    if set(present) != set(expected) or len(present) != len(expected):
        missing = [name for name in expected if name not in present]
        extra = [name for name in present if name not in expected]
        if missing:
            return None, "expected output missing"
        if extra:
            return None, "extra outbox file " + extra[0]
        return None, "expected output missing"
    artifacts = []
    for name in expected:
        path = outbox / name
        problem = plain_file_problem(path)
        if problem == "missing":
            return None, "expected output missing"
        if problem == "link":
            return None, "output is a symlink, junction, or reparse point"
        if problem == "link-count":
            return None, "output link count is not one"
        if problem:
            return None, "output is not a regular file"
        data = path.read_bytes()
        artifacts.append({
            "path": name,
            "sha256": sha256_bytes(data),
            "bytes": len(data),
        })
    return artifacts, None


def _recorded_return(store: Path, view: View) -> dict:
    path = store / "jobs" / view.name / RETURNED_NAME
    event, error = _parse_event(path)
    if error or not isinstance(event, dict):
        refuse("bad state: incomplete: invalid event 0003.returned.json")
    return event


def return_job(store_text: str, job_id: str, actor: str, token: str, delivery: str, evidence: str, *, interrupt=None) -> Result:
    store = None
    try:
        if interrupt not in (None, "publish", "witness"):
            refuse("unknown interrupt seam")
        _require_actor(actor)
        problem = id_problem(delivery, "delivery")
        if problem:
            raise Refusal(problem)
        if not isinstance(token, str) or not _TOKEN.fullmatch(token):
            refuse("wrong token")
        if not isinstance(evidence, str):
            refuse("evidence is not a string")
        if evidence.strip() == "":
            refuse("evidence is blank")
        if any(ord(ch) < 32 for ch in evidence):
            refuse("evidence contains a control character; it must be one line of printable text")
        store = existing_store(store_text)
        view = _find_view(store, job_id)
        if view is None:
            refuse("no matching job")
        if view.structural:
            refuse(structural_line(view))
        if view.status == "queued":
            refuse("return before claim")
        if view.status == "returned":
            recorded = _recorded_return(store, view)
            artifacts, error = _current_artifacts(store, view)
            same = (
                error is None
                and recorded.get("delivery") == delivery
                and recorded.get("by") == actor
                and recorded.get("claim") == token
                and recorded.get("evidence") == evidence
                and recorded.get("artifacts") == artifacts
            )
            if recorded.get("delivery") == delivery and not same:
                refuse("delivery conflict")
            if same:
                return finish(0, [
                    "already-recorded " + job_id,
                    "delivery " + delivery,
                ])
            refuse("already returned")
        if view.status != "claimed":
            refuse(structural_line(view))
        if actor != view.assignee:
            refuse("not assignee")
        if token != view.token:
            refuse("wrong token")
        artifacts, error = _current_artifacts(store, view)
        if error:
            refuse(error)
        prev = view.events[-1][1]
        event = {
            "schema": SCHEMA,
            "kind": "returned",
            "claim": token,
            "by": actor,
            "delivery": delivery,
            "artifacts": artifacts,
            "evidence": evidence,
            "at": now_stamp(),
            "prev": prev,
        }
        data = canonical(event)
        digest = sha256_bytes(data)
        job_dir = store / "jobs" / job_id
        witness = {
            "schema": SCHEMA,
            "kind": "completion",
            "job_id": job_id,
            "event": RETURNED_NAME,
            "sha256": digest,
        }
        exclusive_write(
            job_dir / WITNESS_NAME,
            canonical(witness),
            interrupt == "witness",
            "completion witness publication interrupted",
        )
        path = job_dir / RETURNED_NAME
        exclusive_write(path, data, interrupt == "publish")
        landed = sha256_bytes(path.read_bytes())
        if landed != digest:
            incomplete("returned event does not match completion witness")
        lines = [
            "returned " + job_id,
            "delivery " + delivery,
            f"event {RETURNED_NAME} sha256={digest}",
            f"witness {WITNESS_NAME} records event sha256={digest}",
        ]
        for item in artifacts:
            lines.append(
                f"artifact {item['path']} sha256={item['sha256']} bytes={item['bytes']}"
            )
        return finish(0, lines)
    except Incomplete as exc:
        return finish(2, [str(exc)])
    except Refusal as exc:
        return finish(2, [str(exc)])
    except OSError as exc:
        return finish(2, _os_lines(exc, store, job_id))


def _present_job(store: Path, view: View, base_text: str | None) -> tuple[list[str], int]:
    if view.structural:
        return [structural_line(view)], 2
    lines = []
    if view.chain_ok:
        lines.append("state " + view.status)
        lines.append("states " + " ".join(view.states))
        lines.append("chain ok")
    for name, digest, prev in view.events:
        lines.append(f"event {name} sha256={digest} prev={prev}")
    artifact_lines = inspect_artifacts(store, view)
    lines.extend(artifact_lines)
    if view.status == "returned" and artifacts_dirty(artifact_lines):
        lines.append("not-returned-clean")
    status = instruction_status(base_text, view.job)
    lines.append(status)
    unusable = status.startswith("instructions-unusable")
    code = _codes(False, artifacts_dirty(artifact_lines), unusable)
    if view.token and view.status in ("claimed", "returned"):
        lines.insert(1, "claim " + view.token)
    return lines, code


def _inspection_document(
    job_id: str,
    state: str,
    job,
    claim,
    returned,
    events: str,
    completion: str,
    artifacts: str,
    instructions: str,
    problems: list,
) -> dict:
    return {
        "schema": INSPECTION_SCHEMA,
        "job_id": job_id,
        "state": state,
        "job": job,
        "claim": claim,
        "returned": returned,
        "checks": {
            "events": events,
            "completion": completion,
            "artifacts": artifacts,
            "instructions": instructions,
        },
        "problems": problems,
    }


def _json_result(document: dict, code: int) -> Result:
    return Result(code, canonical(document).decode("utf-8"))


def _events_check(view: View | None) -> str:
    if view is None:
        return "not-applicable"
    if view.chain_ok and not view.structural:
        return "ok"
    diagnosis = view.diagnosis
    if (
        diagnosis == "unreadable job"
        or diagnosis == "job directory is unreadable"
        or diagnosis == "returned event is unreadable"
        or diagnosis.startswith("invalid event")
    ):
        return "unreadable"
    return "broken"


def _completion_check(view: View | None, state: str) -> str:
    if view is None or state in ("queued", "claimed"):
        return "not-applicable"
    if state == "returned":
        return "ok"
    diagnosis = view.diagnosis
    if diagnosis == "partial completion witness":
        return "partial"
    if diagnosis == "completion witness without returned event":
        return "missing-event"
    if diagnosis == "returned event without completion witness":
        return "missing-witness"
    if diagnosis in ("completion witness mismatch", "invalid completion witness"):
        return "mismatch"
    if diagnosis.startswith("planted completion metadata"):
        return "mismatch"
    return "not-applicable"


def _artifact_problems(lines: list[str]) -> list[dict]:
    problems = []
    for line in lines:
        if "artifact changed" not in line or not line.startswith("artifact "):
            continue
        rest = line[len("artifact "):]
        path, _marker, _tail = rest.partition(" artifact changed")
        if " sha256=" in path:
            path = path.split(" sha256=", 1)[0]
        problems.append({
            "kind": "artifact-changed",
            "path": path,
            "detail": line,
        })
    return problems


def _instruction_check(base_text: str | None, job):
    if job is None:
        return "not-applicable", None
    status = instruction_status(base_text, job)
    if status == "instructions-not-checked":
        return "not-checked", None
    if status.startswith("instructions-usable"):
        return "usable", None
    prefix = "instructions-unusable "
    detail = status[len(prefix):] if status.startswith(prefix) else status
    return "unusable", detail


def _project_inspection(store: Path, job_id: str, view: View, base_text: str | None):
    if (
        not view.structural
        and view.status in ("queued", "claimed", "returned")
    ):
        state = view.status
    elif view.status == "incomplete":
        state = "incomplete"
    else:
        state = "corrupt"
    job = view.job if state in ("queued", "claimed", "returned") else None
    claim = None
    returned = None
    if state in ("claimed", "returned"):
        by = view.claim_by if isinstance(view.claim_by, str) else view.assignee
        claim = {"by": by, "token": view.token}
    if state == "returned":
        # The digest _apply_completion matched against the witness before it accepted the
        # pair. It is the recorded event's identity: a later artifact change does not alter it.
        name, event_sha256, _prev = view.events[-1]
        if name != RETURNED_NAME:
            raise AssertionError("returned view without its validated returned event")
        returned = {
            "by": view.return_by,
            "delivery": view.delivery,
            "evidence": view.evidence,
            "artifacts": view.artifacts,
            "event_sha256": event_sha256,
        }
    if state in ("incomplete", "corrupt"):
        kind = "incomplete" if state == "incomplete" else "corrupt"
        problems = [{"kind": kind, "detail": view.diagnosis}]
        artifact_check = "not-applicable"
        instruction_check = "not-applicable"
    else:
        problems = []
        artifact_check = "not-applicable"
        if state == "returned":
            lines = inspect_artifacts(store, view)
            problems.extend(_artifact_problems(lines))
            artifact_check = "changed" if problems else "ok"
        instruction_check, instruction_detail = _instruction_check(base_text, job)
        if instruction_detail is not None:
            problems.append({
                "kind": "instructions-unusable",
                "detail": instruction_detail,
            })
    document = _inspection_document(
        job_id,
        state,
        job,
        claim,
        returned,
        _events_check(view),
        _completion_check(view, state),
        artifact_check,
        instruction_check,
        problems,
    )
    if state in ("queued", "claimed", "returned"):
        findings = {"artifact-changed", "instructions-unusable"}
        if not problems:
            code = 0
        elif all(item["kind"] in findings for item in problems):
            code = 1
        else:
            code = 2
    else:
        code = 2
    return document, code


def _refusal_inspection(job_id: str, exc: Refusal) -> Result:
    text = str(exc)
    if isinstance(exc, Incomplete):
        prefix = "incomplete: "
        detail = text[len(prefix):] if text.startswith(prefix) else text
        state, kind = "incomplete", "incomplete"
    else:
        prefix = "refused: "
        detail = text[len(prefix):] if text.startswith(prefix) else text
        state, kind = "unknown", "unknown"
    document = _inspection_document(
        job_id, state, None, None, None,
        "not-applicable", "not-applicable", "not-applicable", "not-applicable",
        [{"kind": kind, "detail": detail}],
    )
    return _json_result(document, 2)


def _filesystem_inspection(job_id: str, exc: OSError) -> Result:
    detail = f"{type(exc).__name__}: {exc.strerror or str(exc)}"
    document = _inspection_document(
        job_id, "unknown", None, None, None,
        "not-applicable", "not-applicable", "not-applicable", "not-applicable",
        [{"kind": "filesystem", "detail": detail}],
    )
    return _json_result(document, 2)


def show(
    store_text: str,
    job_id: str,
    base_text: str | None = None,
    *,
    as_json: bool = False,
) -> Result:
    store = None
    try:
        store = existing_store(store_text)
        view = _find_view(store, job_id)
        if as_json:
            if view is None:
                document = _inspection_document(
                    job_id, "unknown", None, None, None,
                    "not-applicable", "not-applicable", "not-applicable", "not-applicable",
                    [{"kind": "unknown", "detail": "no matching job"}],
                )
                return _json_result(document, 2)
            document, code = _project_inspection(store, job_id, view, base_text)
            return _json_result(document, code)
        if view is None:
            return finish(2, ["show " + job_id, "no matching job"])
        lines, code = _present_job(store, view, base_text)
        return finish(code, ["show " + job_id, *lines])
    except Refusal as exc:
        if as_json:
            return _refusal_inspection(job_id, exc)
        return finish(2, [str(exc)])
    except OSError as exc:
        if as_json:
            return _filesystem_inspection(job_id, exc)
        return finish(2, _os_lines(exc, store, job_id))


def verify(store_text: str, base_text: str | None = None) -> Result:
    store = None
    try:
        store = existing_store(store_text)
        problems, views = store_entries(store)
        lines = ["verify"]
        worst = 2 if problems else 0
        lines.extend(problems)
        if not views and not problems:
            lines.append("jobs 0")
        for view in views:
            lines.append("job " + view.name)
            presented, code = _present_job(store, view, base_text)
            lines.extend(presented)
            worst = max(worst, code)
        return finish(worst, lines)
    except Refusal as exc:
        return finish(2, [str(exc)])
    except OSError as exc:
        return finish(2, _os_lines(exc, store, None))


def inbox(store_text: str, actor: str, base_text: str | None = None) -> Result:
    store = None
    try:
        _require_actor(actor)
        store = existing_store(store_text)
        problems, views = store_entries(store)
        sections = {"queued": [], "claimed": [], "returned": [], "incomplete": []}
        worst = 0
        for problem in problems:
            sections["incomplete"].append(problem)
            worst = 2
        for view in views:
            if view.structural:
                sections["incomplete"].append(view.name + " " + structural_line(view))
                worst = 2
                continue
            status = instruction_status(base_text, view.job)
            unusable = status.startswith("instructions-unusable")
            if unusable:
                worst = max(worst, 1)
            if view.status in ("queued", "claimed") and actor == view.assignee:
                sections[view.status].append(view.name + " " + status)
            elif view.status == "returned" and actor == view.reviewer:
                reports = inspect_artifacts(store, view)
                if not reports:
                    sections["returned"].append(view.name + " " + status)
                for report in reports:
                    sections["returned"].append(view.name + " " + report)
                if artifacts_dirty(reports):
                    worst = max(worst, 1)
                if unusable:
                    sections["returned"].append(view.name + " " + status)
        lines = ["inbox " + actor]
        for name in ("queued", "claimed", "returned", "incomplete"):
            lines.append("section " + name)
            if sections[name]:
                lines.extend(sections[name])
            else:
                lines.append("none")
        return finish(worst, lines)
    except Refusal as exc:
        return finish(2, [str(exc)])
    except OSError as exc:
        return finish(2, _os_lines(exc, store, None))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="clerk.py")
    sub = parser.add_subparsers(dest="command", required=True)

    def add(name: str) -> argparse.ArgumentParser:
        command = sub.add_parser(name)
        command.add_argument("--store", required=True)
        return command

    queue_cmd = add("queue")
    queue_cmd.add_argument("--job", required=True)
    queue_cmd.add_argument("--instructions-base", required=True)

    claim_cmd = add("claim")
    claim_cmd.add_argument("--job", required=True)
    claim_cmd.add_argument("--as", dest="actor", required=True)
    claim_cmd.add_argument("--instructions-base", required=True)
    claim_cmd.add_argument("--resume", action="store_true")

    return_cmd = add("return")
    return_cmd.add_argument("--job", required=True)
    return_cmd.add_argument("--as", dest="actor", required=True)
    return_cmd.add_argument("--claim", dest="token", required=True)
    return_cmd.add_argument("--delivery", required=True)
    return_cmd.add_argument("--evidence", required=True)

    inbox_cmd = add("inbox")
    inbox_cmd.add_argument("--as", dest="actor", required=True)
    inbox_cmd.add_argument("--instructions-base")

    show_cmd = add("show")
    show_cmd.add_argument("--job", required=True)
    show_cmd.add_argument("--instructions-base")
    show_cmd.add_argument("--json", action="store_true")

    verify_cmd = add("verify")
    verify_cmd.add_argument("--instructions-base")
    return parser


def main(argv: list[str] | None = None) -> int:
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="backslashreplace")
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.command == "queue":
        result = queue(args.store, args.job, args.instructions_base)
    elif args.command == "claim":
        result = claim(
            args.store,
            args.job,
            args.actor,
            args.instructions_base,
            resume=args.resume,
        )
    elif args.command == "return":
        result = return_job(
            args.store,
            args.job,
            args.actor,
            args.token,
            args.delivery,
            args.evidence,
        )
    elif args.command == "inbox":
        result = inbox(args.store, args.actor, args.instructions_base)
    elif args.command == "show":
        result = show(
            args.store,
            args.job,
            args.instructions_base,
            as_json=args.json,
        )
    elif args.command == "verify":
        result = verify(args.store, args.instructions_base)
    else:
        result = finish(2, ["refused: unknown command"])
    sys.stdout.write(result.text)
    return result.code


if __name__ == "__main__":
    sys.exit(main())
