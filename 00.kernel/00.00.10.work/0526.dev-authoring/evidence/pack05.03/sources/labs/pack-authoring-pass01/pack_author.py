#!/usr/bin/env python3
"""Source-linked incremental pack author.

Compute reserves the pass, numbers items, renders the draft, and calls the
pinned dependency reader and pack checker. The model supplies meaning and
the semantic review. A rendered draft is not approval or release.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import stat
import subprocess
import sys
import time
from pathlib import Path

sys.dont_write_bytecode = True
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"

SCHEMA = "authoring-record/1"
RESULT = "authoring-result/1"
HELP = "labs/pack-authoring-pass01/PRIME-USE.md"
REPARSE = 0x400
CHECKOUT = Path(r"D:\Git\lib-build")
LIVE_BOOK = CHECKOUT / "00.kernel" / "00.00.10.work"
OP_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,63}$")
HEX_RE = re.compile(r"^[0-9a-f]{64}$")
ITEM_RE = re.compile(r"^\d{2}$")
WORK_RE = re.compile(r"^05(\d{2})\.(.+)$")
PASS_PAGE_RE = re.compile(r"^05\.(\d+)\.md$")
PASS_PARTIAL_RE = re.compile(r"^05\.(\d+)\.md\.partial$")
SLOT_RE = re.compile(r"^authoring05\.(\d+)$")
COMMANDS = ("start", "add-note", "add-item", "revise", "inspect", "review", "freeze")
BANNED = ("--template", "--executable", "--module", "--set", "--dest", "--output", "--tool", "--python", "--pins")
MARKS = ("discussion", "proposal", "recorded-decision")
DISPOSITIONS = ("integrated", "deferred", "rejected", "unresolved")
CONDITIONS = ("applicable", "inapplicable", "unknown")
INTENT_KEYS = ("goal", "finish", "executor", "reviewer")
SCOPE_KEYS = ("included", "excluded", "allowed_writes")
ITEM_KEYS = {
    "title",
    "purpose",
    "requirements",
    "interfaces",
    "acceptance",
    "note_refs",
    "open_choices",
    "dependency_refs",
    "relationship",
    "condition",
}
PINS = {
    "labs/module-dependencies-pass02/depdecl.py": (
        "a517b0ec3906589e16e2df9bcfb6b3e21a5dd0bd3ef1099d59bf95c0f15ff4e7",
        53693,
    ),
    "labs/app-dependencies-pass02/set.json": (
        "444dba1589c0d6a0204e7a3d6be334b3135d524e4b376e7e92eb8fb434e6f706",
        7054,
    ),
    "labs/pack-custody-pass01/pack_check.py": (
        "9bbd9d57f3b7da43234ac2e6ae4ce40a0ab6af2f53c8135ecfb2ee0c8a6e322d",
        21563,
    ),
    "labs/pack-authoring-pass01/profiles/0423-to-0526.json": (
        "5845d229daeff045e1422dd6b7273f5d876b287be316f1aa87d0bcaaa7a44013",
        1091,
    ),
    "labs/pack-authoring-pass01/profiles/fixture-authoring.json": (
        "026d3561814ecdfa046224ea4b828e9cb23f4036dfd6f07203a782105c0c5823",
        1094,
    ),
    "labs/pack-authoring-pass01/template/build-pack-v1.json": (
        "9e92ee322c5c4e20bb0006e2f92ab9f1fd1308f2812ab70b34c248ddebb5bdcc",
        1008,
    ),
}
PROFILE_FILES = {
    "0423-to-0526": "labs/pack-authoring-pass01/profiles/0423-to-0526.json",
    "fixture-authoring": "labs/pack-authoring-pass01/profiles/fixture-authoring.json",
}


class Refuse(Exception):
    pass


class Partial(Exception):
    pass


def refuse(message: str) -> None:
    raise Refuse(message)


def digest(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def canonical_json(value: object) -> bytes:
    return json.dumps(value, indent=2, ensure_ascii=False).encode("utf-8") + b"\n"


def pairs_hook(items: list[tuple[str, object]]) -> dict:
    obj: dict = {}
    for key, value in items:
        if key in obj:
            refuse(f"duplicate key: {key}")
        obj[key] = value
    return obj


def is_link(path: Path) -> bool:
    try:
        info = os.lstat(path)
    except FileNotFoundError:
        return False
    return stat.S_ISLNK(info.st_mode) or bool(getattr(info, "st_file_attributes", 0) & REPARSE)


def inside(child: Path, parent: Path) -> bool:
    child_s = os.path.normcase(os.path.abspath(child))
    parent_s = os.path.normcase(os.path.abspath(parent))
    if child_s == parent_s:
        return True
    prefix = parent_s if parent_s.endswith(os.sep) else parent_s + os.sep
    return child_s.startswith(prefix)


def ancestor_is_linked(path: Path) -> bool:
    current = path
    while True:
        parent = current.parent
        if parent == current:
            return False
        try:
            os.lstat(parent)
        except FileNotFoundError:
            return False
        if is_link(parent):
            return True
        current = parent


def realpath_text(path: Path) -> str:
    text = os.path.realpath(path)
    if text.startswith("\\\\?\\UNC\\"):
        text = "\\\\" + text[8:]
    elif text.startswith("\\\\?\\"):
        text = text[4:]
    return text


def absolute_directory(text: str, label: str) -> Path:
    if not isinstance(text, str) or text.strip() == "":
        refuse(f"{label} is empty")
    if text.startswith("\\\\") or text.startswith("//"):
        refuse(f"UNC path {label}")
    path = Path(text)
    if not path.is_absolute():
        refuse(f"{label} must be absolute")
    if ".." in path.parts:
        refuse(f"unsafe path {label}")
    if is_link(path) or not path.exists() or not path.is_dir():
        refuse(f"{label} is not a directory")
    return path


def assert_book_policy(path: Path, policy: str) -> None:
    checkout = Path(realpath_text(CHECKOUT))
    live = Path(realpath_text(LIVE_BOOK))
    same_checkout = (inside(path, CHECKOUT) and inside(CHECKOUT, path)) or (
        inside(path, checkout) and inside(checkout, path)
    )
    if policy == "live-or-outside" and same_checkout:
        return
    for target in (CHECKOUT, checkout, LIVE_BOOK, live):
        if inside(path, target) or inside(target, path):
            refuse("book root must stay outside D:\\Git\\lib-build")


def book_root(text: str, policy: str) -> Path:
    path = absolute_directory(text, "book root")
    if ancestor_is_linked(path):
        refuse("book root ancestor is linked and was not followed")
    assert_book_policy(path, policy)
    canonical = Path(realpath_text(path))
    if ".." in canonical.parts or not canonical.is_absolute():
        refuse("unsafe path book root")
    if is_link(canonical) or not canonical.is_dir():
        refuse("book root is not a directory")
    if ancestor_is_linked(canonical):
        refuse("book root ancestor is linked and was not followed")
    assert_book_policy(canonical, policy)
    return canonical


def on_live_tree(path: Path) -> bool:
    checkout = Path(realpath_text(CHECKOUT))
    return inside(path, CHECKOUT) or inside(path, checkout)


def relative_parts(rel: str) -> list[str]:
    if not isinstance(rel, str) or rel == "" or "\\" in rel or rel.startswith("/") or rel.startswith("//"):
        refuse("unsafe profile path")
    parts = rel.split("/")
    if any(part in ("", ".", "..") for part in parts):
        refuse("unsafe profile path")
    return parts


def resolve_pin(code_root: Path, rel: str) -> Path:
    digest_expected, size = PINS[rel]
    current = code_root
    if is_link(current):
        refuse("code root is linked and was not followed")
    for part in rel.split("/"):
        current = current / part
        if is_link(current):
            refuse("tool path is linked and was not followed")
    if not current.is_file():
        refuse(f"pinned tool is missing: {rel}")
    raw = current.read_bytes()
    if digest(raw) != digest_expected or len(raw) != size:
        refuse(f"pinned tool hash does not match: {rel}")
    return current


def load_pins(code_root: Path) -> dict[str, Path]:
    return {rel: resolve_pin(code_root, rel) for rel in PINS}


def load_profile(pins: dict[str, Path], profile_id: str) -> dict:
    if profile_id not in PROFILE_FILES:
        refuse("unknown profile")
    raw = pins[PROFILE_FILES[profile_id]].read_bytes()
    try:
        document = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        refuse("profile is not strict json")
    if not isinstance(document, dict) or document.get("profile_id") != profile_id:
        refuse("profile id does not match the file")
    if document.get("book_policy") not in ("live-or-outside", "outside-only"):
        refuse("profile book policy is undeclared")
    return document


def walk_book(book: Path, rel: str, kind: str) -> Path:
    current = book
    parts = relative_parts(rel)
    for index, part in enumerate(parts):
        current = current / part
        if is_link(current):
            refuse("source path is linked and was not followed")
        last = index == len(parts) - 1
        if not current.exists():
            refuse(f"missing source {rel}")
        if last:
            if kind == "dir" and not current.is_dir():
                refuse(f"missing work page {rel}")
            if kind == "file" and not current.is_file():
                refuse(f"missing source {rel}")
        elif not current.is_dir():
            refuse(f"missing source {rel}")
    return current


def measure(path: Path, rel: str, role: str) -> dict:
    raw = path.read_bytes()
    utf8 = True
    try:
        raw.decode("utf-8")
    except UnicodeDecodeError:
        utf8 = False
    return {"role": role, "path": rel, "sha256": digest(raw), "bytes": len(raw), "utf8": utf8}


def require_text(measured: dict) -> None:
    if not measured["utf8"]:
        refuse(f"source is not utf-8: {measured['path']}")


def empty_intent() -> dict:
    return {
        "goal": "",
        "scope": {"included": "", "excluded": "", "allowed_writes": ""},
        "finish": "",
        "executor": "",
        "reviewer": "",
    }


def field_stop(field: str, expected: str, retained: str) -> None:
    refuse(f"typed-field: {field} expected {expected}; retained input {retained}. Help: {HELP}")


def load_input(path_text: str | None) -> tuple[dict | None, bytes]:
    if path_text is None:
        return None, b""
    if not isinstance(path_text, str) or path_text.strip() == "":
        refuse("input is empty")
    if path_text.startswith("\\\\") or path_text.startswith("//"):
        refuse("UNC path input")
    path = Path(path_text)
    if not path.is_absolute() or ".." in path.parts:
        refuse("unsafe path input")
    if ancestor_is_linked(path) or is_link(path) or not path.is_file():
        refuse("input is not a file")
    raw = path.read_bytes()
    if len(raw) > 262144:
        refuse("input is over the 262144-byte bound")
    if raw.startswith(b"\xef\xbb\xbf"):
        refuse("input is not utf-8")
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        refuse("input is not utf-8")
    try:
        value, end = json.JSONDecoder(object_pairs_hook=pairs_hook).raw_decode(text)
    except Refuse:
        raise
    except json.JSONDecodeError:
        refuse("input is not strict json")
    if text[end:].strip():
        refuse("input has trailing data")
    if not isinstance(value, dict):
        refuse("input is not an object")
    return value, raw


def need_object_keys(value: dict, allowed: set[str], required: set[str], retained: str) -> None:
    extra = sorted(set(value) - allowed)
    if extra:
        field_stop(extra[0], "an absent field", retained)
    missing = sorted(required - set(value))
    if missing:
        field_stop(missing[0], "a required field", retained)


def need_string(value: dict, key: str, retained: str) -> str:
    got = value.get(key)
    if not isinstance(got, str) or got.strip() == "":
        field_stop(key, "non-empty string", retained)
    if len(got) > 4000:
        field_stop(key, "a string up to 4000 characters", retained)
    return got


def need_string_list(value: dict, key: str, retained: str, minimum: int) -> list[str]:
    got = value.get(key)
    if not isinstance(got, list):
        field_stop(key, "a list of strings", retained)
    if len(got) < minimum or len(got) > 32:
        field_stop(key, f"a list of {minimum} to 32 strings", retained)
    out = []
    for item in got:
        if not isinstance(item, str) or item.strip() == "" or len(item) > 4000:
            field_stop(key, "a list of non-empty strings", retained)
        out.append(item)
    return out


def parse_intent(value: dict, retained: str) -> dict:
    need_object_keys(value, set(INTENT_KEYS) | {"scope"}, set(INTENT_KEYS) | {"scope"}, retained)
    scope = value["scope"]
    if not isinstance(scope, dict):
        field_stop("scope", "an object", retained)
    need_object_keys(scope, set(SCOPE_KEYS), set(SCOPE_KEYS), retained)
    return {
        "goal": need_string(value, "goal", retained),
        "scope": {key: need_string(scope, key, retained) for key in SCOPE_KEYS},
        "finish": need_string(value, "finish", retained),
        "executor": need_string(value, "executor", retained),
        "reviewer": need_string(value, "reviewer", retained),
    }


def parse_dependency_ref(value: object, retained: str) -> dict:
    if not isinstance(value, dict):
        field_stop("dependency_refs", "objects with repository and path", retained)
    allowed = {"repository", "path", "claimed_sha256"}
    need_object_keys(value, allowed, {"repository", "path"}, retained)
    ref = {"repository": need_string(value, "repository", retained), "path": need_string(value, "path", retained)}
    if "claimed_sha256" in value:
        claimed = value["claimed_sha256"]
        if not isinstance(claimed, str) or not HEX_RE.fullmatch(claimed):
            field_stop("claimed_sha256", "64 lowercase hex", retained)
        ref["claimed_sha256"] = claimed
    else:
        ref["claimed_sha256"] = None
    relative_parts(ref["path"])
    return ref


def parse_relationship(value: object, retained: str) -> dict | None:
    if value is None:
        return None
    if not isinstance(value, dict):
        field_stop("relationship", "an object", retained)
    need_object_keys(value, {"target_repository", "target_path", "meaning"}, {"target_repository", "target_path", "meaning"}, retained)
    rel = {
        "target_repository": need_string(value, "target_repository", retained),
        "target_path": need_string(value, "target_path", retained),
        "meaning": need_string(value, "meaning", retained),
        "state": "unresolved-not-in-set",
    }
    relative_parts(rel["target_path"])
    return rel


def parse_condition(value: object, retained: str) -> dict | None:
    if value is None:
        return None
    if not isinstance(value, dict):
        field_stop("condition", "an object", retained)
    need_object_keys(value, {"module", "id", "state"}, {"module", "id", "state"}, retained)
    module = need_string(value, "module", retained)
    if module.count(":") != 1:
        field_stop("condition.module", "REPOSITORY:PATH", retained)
    state = value["state"]
    if state not in CONDITIONS:
        field_stop("condition.state", "applicable, inapplicable, or unknown", retained)
    return {"module": module, "id": need_string(value, "id", retained), "state": state}


def parse_item(value: dict, retained: str) -> dict:
    need_object_keys(value, ITEM_KEYS, ITEM_KEYS - {"relationship", "condition"}, retained)
    if "delete" in value:
        refuse(f"deletion is not a command in this slice; retained input {retained}. Help: {HELP}")
    return {
        "title": need_string(value, "title", retained),
        "purpose": need_string(value, "purpose", retained),
        "requirements": need_string_list(value, "requirements", retained, 1),
        "interfaces": need_string_list(value, "interfaces", retained, 0),
        "acceptance": need_string_list(value, "acceptance", retained, 1),
        "note_refs": need_string_list(value, "note_refs", retained, 0),
        "open_choices": need_string_list(value, "open_choices", retained, 0),
        "dependency_refs": [parse_dependency_ref(item, retained) for item in value["dependency_refs"]]
        if isinstance(value["dependency_refs"], list)
        else field_stop("dependency_refs", "a list", retained),
        "relationship": parse_relationship(value.get("relationship"), retained),
        "condition": parse_condition(value.get("condition"), retained),
    }


def parse_note(value: dict, retained: str) -> dict:
    allowed = {"text", "attribution", "source", "mark"}
    need_object_keys(value, allowed, {"text", "attribution", "source"}, retained)
    note = {
        "text": need_string(value, "text", retained),
        "attribution": need_string(value, "attribution", retained),
        "source": need_string(value, "source", retained),
        "mark": None,
    }
    if "mark" in value:
        mark = value["mark"]
        if mark not in MARKS:
            field_stop("mark", "discussion, proposal, or recorded-decision", retained)
        note["mark"] = mark
    return note


def parse_review(value: dict, retained: str) -> dict:
    keys = {"assessment", "unresolved_issues", "stop_conditions"}
    need_object_keys(value, keys, keys, retained)
    return {
        "assessment": need_string(value, "assessment", retained),
        "unresolved_issues": need_string(value, "unresolved_issues", retained),
        "stop_conditions": need_string(value, "stop_conditions", retained),
    }


def known_note_ids(record: dict) -> set[str]:
    return {note["id"] for note in record["declared_notes"]} | {note["id"] for note in record["draft_notes"]}


def check_note_refs(record: dict, item: dict, retained: str) -> None:
    known = known_note_ids(record)
    for ref in item["note_refs"]:
        if ref not in known:
            field_stop("note_refs", "a declared or draft note id", retained)


class WorkLock:
    def __init__(self, work_dir: Path) -> None:
        self.work_dir = work_dir
        self.lock: Path | None = None

    def __enter__(self) -> Path:
        evidence = self.work_dir / "evidence"
        if is_link(self.work_dir):
            refuse("work page is not a directory")
        if evidence.exists() and (is_link(evidence) or not evidence.is_dir()):
            refuse("evidence path is linked and was not followed")
        evidence.mkdir(exist_ok=True)
        lock = evidence / "authoring.lockdir"
        for _ in range(400):
            try:
                lock.mkdir()
            except FileExistsError:
                time.sleep(0.05)
                continue
            self.lock = lock
            return lock
        refuse("authoring lock is busy")
        return lock

    def __exit__(self, exc_type, exc, tb) -> None:
        if self.lock is not None:
            try:
                self.lock.rmdir()
            except OSError:
                pass
            self.lock = None


def occupied_numbers(work_dir: Path) -> set[int]:
    found: set[int] = set()

    def take(name: str, pattern: re.Pattern[str]) -> None:
        match = pattern.fullmatch(name)
        if match:
            found.add(int(match.group(1)))

    for entry in os.scandir(work_dir):
        path = Path(entry.path)
        if is_link(path):
            refuse("work page entry is linked and was not followed")
        take(entry.name, PASS_PAGE_RE)
        take(entry.name, PASS_PARTIAL_RE)
    evidence = work_dir / "evidence"
    if evidence.is_dir():
        for entry in os.scandir(evidence):
            path = Path(entry.path)
            if is_link(path):
                refuse("authoring slot is linked and was not followed")
            take(entry.name, SLOT_RE)
    return found


def reserve_pass(work_dir: Path) -> tuple[str, Path]:
    if is_link(work_dir) or not work_dir.is_dir():
        refuse("work page is not a directory")
    evidence = work_dir / "evidence"
    if evidence.exists() and (is_link(evidence) or not evidence.is_dir()):
        refuse("evidence path is linked and was not followed")
    evidence.mkdir(exist_ok=True)
    occupied = occupied_numbers(work_dir)
    number = 1
    while number < 1000:
        if number in occupied:
            number += 1
            continue
        slot = evidence / f"authoring05.{number:02d}"
        try:
            slot.mkdir()
        except FileExistsError:
            occupied.add(number)
            number += 1
            continue
        return f"05.{number:02d}", slot
    refuse("no free pass")
    return "", evidence


def commit_record(record_path: Path, document: dict, operation: str, replace=os.replace) -> None:
    partial = record_path.with_name(f"record.json.partial-{operation}")
    if partial.exists():
        refuse(f"partial already exists: {partial.name}")
    payload = canonical_json(document)
    flags = os.O_CREAT | os.O_EXCL | os.O_WRONLY
    if hasattr(os, "O_BINARY"):
        flags |= os.O_BINARY
    fd = os.open(partial, flags)
    try:
        os.write(fd, payload)
        os.fsync(fd)
    finally:
        os.close(fd)
    try:
        replace(str(partial), str(record_path))
    except OSError as exc:
        raise Partial(
            f"record replace failed; previous record retained; partial {partial.name}; {exc.strerror or exc}"
        ) from exc


def write_face(slot: Path, record: dict, operation: str) -> None:
    text = render(record).encode("utf-8")
    face = slot / "draft.md"
    if face.exists() and not is_link(face):
        current = face.read_bytes()
        if current != text:
            conflict = slot / f"draft.md.conflict-{operation}"
            if not conflict.exists():
                conflict.write_bytes(current)
    partial = slot / f"draft.md.partial-{operation}"
    partial.write_bytes(text)
    os.replace(partial, face)


def load_record(path: Path) -> dict:
    if is_link(path) or not path.is_file():
        refuse("authoring record is missing")
    raw = path.read_bytes()
    try:
        document = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        refuse("authoring record is damaged")
    if not isinstance(document, dict) or document.get("schema") != SCHEMA:
        refuse("authoring record is damaged")
    return document


def iter_records(work_dir: Path) -> list[tuple[Path, dict]]:
    evidence = work_dir / "evidence"
    found = []
    if not evidence.is_dir() or is_link(evidence):
        return found
    for entry in sorted(evidence.iterdir(), key=lambda item: item.name):
        if not SLOT_RE.fullmatch(entry.name):
            continue
        if is_link(entry):
            refuse("authoring slot is linked and was not followed")
        record_path = entry / "record.json"
        if not record_path.exists():
            continue
        found.append((entry, load_record(record_path)))
    return found


def request_sha(command: str, flags: dict[str, str], raw: bytes) -> str:
    parts = [
        command,
        flags.get("target", ""),
        flags.get("item", ""),
        flags.get("note", ""),
        flags.get("draft", ""),
    ]
    payload = "\0".join(parts).encode("utf-8") + b"\0" + raw
    return digest(payload)


def find_operation(work_dir: Path, profile_id: str, op_id: str) -> tuple[Path, dict, dict] | None:
    for slot, record in iter_records(work_dir):
        if record.get("profile_id") != profile_id:
            continue
        operation = record.get("operations", {}).get(op_id)
        if operation:
            return slot, record, operation
    return None


def open_sessions(work_dir: Path, profile_id: str) -> list[tuple[Path, dict]]:
    return [
        (slot, record)
        for slot, record in iter_records(work_dir)
        if record.get("profile_id") == profile_id and record.get("state") != "frozen"
    ]


def source_digest(sources: list[dict]) -> str:
    text = "\n".join(f"{item['path']} {item['sha256']}" for item in sources)
    return digest(text.encode("utf-8"))


def render(record: dict) -> str:
    lines = [
        f"# {record['pass']} - authored draft",
        f"profile: {record['profile_id']}",
        f"pass: {record['pass']}",
        "approval: false",
        "release: false",
        "authority: authoring record; this face is derived",
        "label: the meaning below is supplied by the caller",
        "",
        "## Intent",
    ]
    intent = record["intent"]
    for key in INTENT_KEYS:
        lines.append(f"{key}: {intent.get(key) or ''}")
    scope = intent.get("scope") or {}
    for key in SCOPE_KEYS:
        lines.append(f"scope.{key}: {scope.get(key) or ''}")
    lines.extend(["", "## Declared notes"])
    for note in record["declared_notes"]:
        lines.append(
            f"- {note['id']} disposition {note['disposition']} item {note.get('integrated_item') or '-'} why {note.get('why') or '-'}"
        )
        lines.append(f"  sha256 {note['sha256']} bytes {note['bytes']}")
    lines.extend(["", "## Draft notes"])
    if not record["draft_notes"]:
        lines.append("- none")
    for note in record["draft_notes"]:
        mark = note.get("mark") or "-"
        lines.append(
            f"- {note['id']} mark {mark} disposition {note['disposition']} attribution {note['attribution']} source {note['source']}"
        )
        lines.append(f"  {note['text']}")
    lines.extend(["", "## Items"])
    if not record["items"]:
        lines.append("none")
    for item in record["items"]:
        lines.append(f"## #{item['id']} - {item['title']}")
        lines.append(item["purpose"])
        lines.append("requirements:")
        lines.extend(f"- {part}" for part in item["requirements"])
        lines.append("interfaces:")
        lines.extend(f"- {part}" for part in item["interfaces"])
        if not item["interfaces"]:
            lines.append("- none")
        lines.append("acceptance:")
        lines.extend(f"- {part}" for part in item["acceptance"])
        lines.append("note-refs:")
        lines.extend(f"- {part}" for part in item["note_refs"])
        if not item["note_refs"]:
            lines.append("- none")
        lines.append("open-choices:")
        lines.extend(f"- {part}" for part in item["open_choices"])
        if not item["open_choices"]:
            lines.append("- none")
        lines.append("dependency-refs:")
        if item["dependency_refs"]:
            for ref in item["dependency_refs"]:
                claimed = ref.get("claimed_sha256") or "-"
                lines.append(f"- {ref['repository']}:{ref['path']} claimed {claimed}")
        else:
            lines.append("- none")
        if item.get("relationship"):
            rel = item["relationship"]
            lines.append(
                f"relationship: {rel['target_repository']}:{rel['target_path']} {rel['state']} {rel['meaning']}"
            )
        lines.append("")
    dep = record["dependency"]
    lines.extend(
        [
            "## Dependencies",
            f"set-path: {dep['set']['path']}",
            f"set-sha256: {dep['set']['sha256']}",
            f"set-label: {dep['set']['label']}",
            f"set-form: {dep['set']['form']}",
            "complete_claim: false",
        ]
    )
    for query in dep["queries"]:
        module = query.get("module") or "-"
        labels = ",".join(query["labels"]) or "-"
        lines.append(
            f"query {query['command']} module {module} exit {query['exit']} status {query.get('status') or '-'} labels {labels}"
        )
    for ref in dep["item_refs"]:
        labels = ",".join(ref["labels"]) or "-"
        lines.append(f"ref {ref['repository']}:{ref['path']} exit {ref['exit']} labels {labels}")
    ret = record["return_intent"]
    occupants = ",".join(ret["occupants"]) or "-"
    lines.extend(
        [
            "",
            "## Return",
            f"intended: {ret['intended']}",
            f"status: {ret['status']}",
            f"occupants: {occupants}",
            f"readiness: {ret['readiness']}",
            "n7nn: page-local",
            "",
            "## Review",
        ]
    )
    if record["review"] is None:
        lines.append("review: absent")
    else:
        lines.append("review: present")
        lines.append(record["review"]["assessment"])
        lines.append(f"unresolved: {record['review']['unresolved_issues']}")
        lines.append(f"stop-conditions: {record['review']['stop_conditions']}")
    lines.extend(
        [
            "",
            "## Sources",
        ]
    )
    for source in record["sources"]:
        lines.append(f"- {source['role']} {source['path']} sha256 {source['sha256']} bytes {source['bytes']} utf8 {str(source['utf8']).lower()}")
    lines.extend(
        [
            "",
            "Freeze emits these bytes unchanged. Approval and release stay separate.",
            "",
        ]
    )
    return "\n".join(lines)


def gaps(record: dict) -> list[str]:
    missing = []
    intent = record["intent"]
    for key in INTENT_KEYS:
        if not intent.get(key):
            missing.append(key)
    scope = intent.get("scope") or {}
    for key in SCOPE_KEYS:
        if not scope.get(key):
            missing.append(f"scope.{key}")
    item_ids = {item["id"] for item in record["items"]}
    for note in list(record["declared_notes"]) + list(record["draft_notes"]):
        disposition = note["disposition"]
        if disposition == "unresolved":
            missing.append(f"disposition {note['id']}")
        elif disposition in ("deferred", "rejected") and not note.get("why"):
            missing.append(f"why {note['id']}")
        elif disposition == "integrated" and note.get("integrated_item") not in item_ids:
            missing.append(f"integrated item {note['id']}")
    if not record["items"]:
        missing.append("item")
    if record["review"] is None:
        missing.append("review")
    if record["return_intent"]["readiness"] != "ready":
        missing.append("return readiness")
    return missing


def next_step(record: dict, live: bool) -> str:
    if live:
        return "Prime can inspect this draft. Freeze on the live checkout is refused. This is not the Prime pilot."
    missing = gaps(record)
    if any(item in missing for item in ("goal", "finish", "executor", "reviewer")) or any(item.startswith("scope.") for item in missing):
        return "supply intent through revise --target intent"
    if any(item.startswith("disposition ") for item in missing):
        return "supply a disposition for each declared note"
    if "item" in missing:
        return "add an item"
    if "review" in missing:
        return "review the exact draft"
    if record["state"] != "frozen":
        return "freeze with the draft sha256 shown by inspect; return readiness stays blocked"
    return "The prepared page is written. Return readiness stays blocked."


def return_intent(work_dir: Path) -> dict:
    match = WORK_RE.fullmatch(work_dir.name)
    if not match:
        refuse("undeclared work page kind")
    nn, subject = match.group(1), match.group(2)
    intended = f"01{nn}.{subject}"
    occupants = []
    linked = []
    named = False
    for entry in os.scandir(work_dir.parent):
        if not entry.name.startswith(f"01{nn}."):
            continue
        path = Path(entry.path)
        if is_link(path):
            linked.append(entry.name)
            continue
        if entry.is_dir(follow_symlinks=False):
            if entry.name == intended:
                named = True
            else:
                occupants.append(entry.name)
    if linked:
        status = "linked-occupant"
    elif named:
        status = "named-slot-present"
    elif occupants:
        status = "occupied"
    else:
        status = "unfiled"
    return {
        "intended": intended,
        "status": status,
        "occupants": sorted(occupants),
        "linked": sorted(linked),
        "named_slot_present": named,
        "readiness": "blocked",
        "n7nn": "page-local",
        "rule": "N5NN matches N1NN same NN and subject; N7NN stays page-local",
    }


def run_reader(code_root: Path, depdecl: Path, set_path: Path, spec: dict) -> dict:
    command = [sys.executable, "-B", str(depdecl), spec["command"], "--set", str(set_path)]
    if spec["command"] == "requires":
        command.extend(["--module", spec["module"], "--depth", str(spec["depth"])])
        for condition in spec.get("condition") or []:
            command.extend(["--condition", condition])
    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    try:
        result = subprocess.run(
            command,
            cwd=code_root,
            shell=False,
            capture_output=True,
            env=env,
            timeout=60,
        )
    except subprocess.TimeoutExpired:
        return {"exit": None, "parsed": None}
    parsed = None
    try:
        text = result.stdout.decode("utf-8")
        if text.strip().startswith("{"):
            parsed = json.loads(text)
    except (UnicodeDecodeError, json.JSONDecodeError):
        parsed = None
    return {"exit": result.returncode, "parsed": parsed}


def labels_from_parsed(parsed: dict, claimed: str | None) -> list[str]:
    labels = []
    root = parsed.get("root") or {}
    state = root.get("state") if isinstance(root, dict) else None
    if state == "undeclared":
        labels.append("missing")
    if state == "ambiguous-version":
        labels.append("ambiguous")
    counts = parsed.get("finding_counts") or {}
    if isinstance(counts, dict):
        for name in counts:
            if name == "record-missing":
                labels.append("missing")
            elif name == "pin-differs":
                labels.append("stale")
            elif name in ("ambiguous-version", "identity-conflict", "identity-pair-mismatch"):
                labels.append("ambiguous")
            elif name in ("condition-inapplicable", "condition-unknown"):
                labels.append("conditional")
            elif name in ("environment-unverified", "environment-unavailable"):
                labels.append("environment")
    declaration = root.get("declaration") if isinstance(root, dict) else None
    implementation = declaration.get("implementation_sha256") if isinstance(declaration, dict) else None
    if claimed and implementation and claimed != implementation:
        labels.append("stale")
    requirements = parsed.get("requirements") or []
    if isinstance(requirements, list):
        for edge in requirements:
            if not isinstance(edge, dict):
                continue
            condition = edge.get("condition") or {}
            if isinstance(condition, dict) and condition.get("applies") == "conditional":
                labels.append("conditional")
            resolution = edge.get("resolution")
            if resolution == "pin-differs":
                labels.append("stale")
            elif resolution == "record-missing":
                labels.append("missing")
            elif resolution in ("ambiguous-version", "identity-conflict"):
                labels.append("ambiguous")
    return labels


def summarize_reader(spec: dict, run: dict, claimed: str | None = None) -> dict:
    parsed = run["parsed"]
    labels = []
    status = None
    counts: dict = {}
    if run["exit"] in (None, 2):
        labels.append("reader-refused")
    if isinstance(parsed, dict):
        status = parsed.get("status")
        raw_counts = parsed.get("finding_counts") or {}
        if isinstance(raw_counts, dict):
            counts = raw_counts
        labels.extend(labels_from_parsed(parsed, claimed))
    else:
        labels.append("reader-unparsed")
    return {
        "command": spec["command"],
        "module": spec.get("module"),
        "condition": list(spec.get("condition") or []),
        "exit": run["exit"],
        "status": status,
        "finding_counts": counts,
        "labels": sorted(set(labels)),
    }


def measure_set(profile: dict, book: Path, pins: dict[str, Path]) -> tuple[Path, dict]:
    spec = profile["dependency_set"]
    if spec["root"] == "code":
        path = pins["labs/app-dependencies-pass02/set.json"]
        rel = spec["path"]
    elif spec["root"] == "book":
        path = walk_book(book, spec["path"], "file")
        rel = spec["path"]
    else:
        refuse("dependency set root is undeclared")
        return book, {}
    raw = path.read_bytes()
    return path, {
        "path": rel,
        "root": spec["root"],
        "sha256": digest(raw),
        "bytes": len(raw),
        "label": "measured-file",
        "form": "working-tree",
    }


def collect_dependencies(code_root: Path, pins: dict[str, Path], set_path: Path, profile: dict, items: list[dict]) -> dict:
    depdecl = pins["labs/module-dependencies-pass02/depdecl.py"]
    queries = []
    for spec in profile["queries"]:
        queries.append(summarize_reader(spec, run_reader(code_root, depdecl, set_path, spec)))
    item_refs = []
    for item in items:
        for ref in item["dependency_refs"]:
            module = f"{ref['repository']}:{ref['path']}"
            spec = {"command": "requires", "module": module, "depth": 1, "condition": []}
            condition = item.get("condition")
            if condition and condition["module"] == module:
                spec["condition"] = [f"{condition['id']}={condition['state']}"]
            item_refs.append(
                {
                    "repository": ref["repository"],
                    "path": ref["path"],
                    "claimed_sha256": ref.get("claimed_sha256"),
                    **{
                        key: value
                        for key, value in summarize_reader(
                            spec, run_reader(code_root, depdecl, set_path, spec), ref.get("claimed_sha256")
                        ).items()
                        if key in ("exit", "status", "finding_counts", "labels")
                    },
                }
            )
    return {"queries": queries, "item_refs": item_refs}


def measure_sources(book: Path, profile: dict) -> list[dict]:
    rows = [
        ("source", profile["source_page"]),
        ("work-note", profile["work_page_note"]),
        ("template", profile["template"]),
    ]
    rows.extend(("declared-note", rel) for rel in profile["declared_notes"])
    rows.extend(("raw", rel) for rel in profile["raw_sources"])
    measured = []
    for role, rel in rows:
        info = measure(walk_book(book, rel, "file"), rel, role)
        if role != "raw":
            require_text(info)
        measured.append(info)
    return measured


def declared_note_rows(sources: list[dict]) -> list[dict]:
    rows = []
    for source in sources:
        if source["role"] != "declared-note":
            continue
        rows.append(
            {
                "id": source["path"],
                "kind": "declared-source",
                "path": source["path"],
                "sha256": source["sha256"],
                "bytes": source["bytes"],
                "disposition": "unresolved",
                "integrated_item": None,
                "why": None,
            }
        )
    return rows


def invalidate_review(record: dict, reason: str) -> None:
    if record["review"] is not None:
        record["review_history"].append(dict(record["review"], invalidated_because=reason))
        record["review"] = None


def blocking_dependency(record: dict, set_sha: str) -> str | None:
    if record["dependency"]["set"]["sha256"] != set_sha:
        return "stale dependency set"
    for query in record["dependency"]["queries"]:
        if "reader-refused" in query["labels"] or "reader-unparsed" in query["labels"]:
            return f"dependency query {query['command']} was refused"
    for ref in record["dependency"]["item_refs"]:
        for label in ("missing", "stale", "ambiguous", "reader-refused", "reader-unparsed"):
            if label in ref["labels"]:
                return f"dependency {ref['repository']}:{ref['path']} is {label}"
    for item in record["items"]:
        relationship = item.get("relationship")
        if relationship and not relationship.get("meaning"):
            return "relationship meaning is missing"
    return None


def coverage_blocks(record: dict) -> str | None:
    item_ids = {item["id"] for item in record["items"]}
    for note in list(record["declared_notes"]) + list(record["draft_notes"]):
        if note["disposition"] == "unresolved":
            return f"note {note['id']} is unresolved"
        if note["disposition"] in ("deferred", "rejected") and not note.get("why"):
            return f"note {note['id']} needs why"
        if note["disposition"] == "integrated" and note.get("integrated_item") not in item_ids:
            return f"note {note['id']} names a missing item"
    return None


def intent_missing(record: dict) -> bool:
    intent = record["intent"]
    if any(not intent.get(key) for key in INTENT_KEYS):
        return True
    return any(not intent["scope"].get(key) for key in SCOPE_KEYS)


def refresh_current(code_root: Path, pins: dict[str, Path], book: Path, profile: dict, record: dict) -> tuple[list[dict], dict, dict]:
    sources = measure_sources(book, profile)
    set_path, set_info = measure_set(profile, book, pins)
    dependency = collect_dependencies(code_root, pins, set_path, profile, record["items"])
    dependency["set"] = set_info
    return sources, set_info, dependency


def live_view(record: dict, sources: list[dict], set_info: dict) -> dict:
    return {
        "source_digest": source_digest(sources),
        "recorded_source_digest": source_digest(record["sources"]),
        "source_drift": source_digest(sources) != source_digest(record["sources"]),
        "set_sha256": set_info["sha256"],
        "recorded_set_sha256": record["dependency"]["set"]["sha256"],
        "set_drift": set_info["sha256"] != record["dependency"]["set"]["sha256"],
    }


def result_for(record: dict, slot: Path, command: str, live: bool) -> dict:
    text = render(record)
    face = slot / "draft.md"
    conflict = False
    if face.is_file() and not is_link(face):
        conflict = face.read_bytes() != text.encode("utf-8")
    page = slot.parent.parent / f"{record['pass']}.md"
    page_bytes = page.read_bytes() if page.is_file() and not is_link(page) else None
    return {
        "schema": RESULT,
        "command": command,
        "state": record["state"],
        "pass": record["pass"],
        "record": str(slot / "record.json"),
        "draft": str(face),
        "draft_sha256": digest(text.encode("utf-8")),
        "draft_text": text,
        "next": next_step(record, live),
        "missing": gaps(record),
        "return_intent": record["return_intent"],
        "derived_conflict": conflict,
        "page": str(page) if page_bytes is not None else None,
        "page_matches_draft": page_bytes == text.encode("utf-8") if page_bytes is not None else False,
        "coverage": [
            {"id": note["id"], "disposition": note["disposition"]}
            for note in list(record["declared_notes"]) + list(record["draft_notes"])
        ],
    }


def human(result: dict) -> str:
    occupants = ",".join(result["return_intent"]["occupants"]) or "-"
    lines = [
        "authoring-result/1",
        f"command: {result['command']}",
        f"state: {result['state']}",
        f"pass: {result['pass']}",
        f"record: {result['record']}",
        f"draft: {result['draft']}",
        f"draft-sha256: {result['draft_sha256']}",
        f"next: {result['next']}",
        f"return: {result['return_intent']['intended']} {result['return_intent']['status']} occupants {occupants} readiness {result['return_intent']['readiness']}",
        "",
    ]
    return "\n".join(lines)


def emit(result: dict, code: int, as_json: bool) -> int:
    if code != 0:
        print(f"stop: {result.get('stop', 'refused')}", file=sys.stderr)
        return code
    if as_json:
        sys.stdout.write(canonical_json(result).decode("utf-8"))
    else:
        sys.stdout.write(human(result))
    return 0


def store_operation(record: dict, op_id: str, command: str, request: str, code: int, result: dict) -> None:
    record["operations"][op_id] = {
        "command": command,
        "request_sha256": request,
        "exit": code,
        "result": result,
    }


def replay_or_conflict(found: tuple[Path, dict, dict] | None, request: str, command: str, as_json: bool) -> int | None:
    if found is None:
        return None
    _slot, _record, operation = found
    if operation["request_sha256"] == request and operation["command"] == command:
        return emit(operation["result"], operation["exit"], as_json)
    refuse("conflicting operation; the record was preserved")
    return None


def finish(slot: Path, record: dict, op_id: str, command: str, request: str, as_json: bool, live: bool, code: int = 0, stop: str | None = None) -> int:
    result = result_for(record, slot, command, live)
    if stop:
        result["stop"] = stop
    store_operation(record, op_id, command, request, code, result)
    commit_record(slot / "record.json", record, op_id)
    if code == 0:
        write_face(slot, record, op_id)
    return emit(result, code, as_json)


def command_start(ctx: dict) -> int:
    work_dir = ctx["work_dir"]
    sources = measure_sources(ctx["book"], ctx["profile"])
    set_path, set_info = measure_set(ctx["profile"], ctx["book"], ctx["pins"])
    intent = parse_intent(ctx["input"], ctx["retained"]) if ctx["input"] is not None else empty_intent()
    with WorkLock(work_dir):
        found = find_operation(work_dir, ctx["profile_id"], ctx["op_id"])
        replay = replay_or_conflict(found, ctx["request"], "start", ctx["json"])
        if replay is not None:
            return replay
        if open_sessions(work_dir, ctx["profile_id"]):
            refuse("an open session already exists")
        dependency = collect_dependencies(ctx["code_root"], ctx["pins"], set_path, ctx["profile"], [])
        dependency["set"] = set_info
        pass_name, slot = reserve_pass(work_dir)
        record = {
            "schema": SCHEMA,
            "profile_id": ctx["profile_id"],
            "book": str(ctx["book"]),
            "pass": pass_name,
            "work_home": ctx["profile"]["work_home"],
            "state": "drafting",
            "stamp": "draft",
            "intent": intent,
            "declared_notes": declared_note_rows(sources),
            "draft_notes": [],
            "items": [],
            "revisions": [],
            "review": None,
            "review_history": [],
            "sources": sources,
            "template_schema": {
                "path": "labs/pack-authoring-pass01/template/build-pack-v1.json",
                "sha256": PINS["labs/pack-authoring-pass01/template/build-pack-v1.json"][0],
                "bytes": PINS["labs/pack-authoring-pass01/template/build-pack-v1.json"][1],
            },
            "dependency": dependency,
            "return_intent": return_intent(work_dir),
            "operations": {},
        }
        return finish(slot, record, ctx["op_id"], "start", ctx["request"], ctx["json"], ctx["live"])


def require_open(ctx: dict) -> tuple[Path, dict]:
    sessions = open_sessions(ctx["work_dir"], ctx["profile_id"])
    if not sessions:
        refuse("no open session")
    if len(sessions) != 1:
        refuse("ambiguous session")
    return sessions[0]


def apply_source_drift(record: dict, sources: list[dict], set_info: dict, dependency: dict) -> str | None:
    reason = None
    if source_digest(sources) != source_digest(record["sources"]):
        reason = "source-drift"
        record["sources"] = sources
        for note in record["declared_notes"]:
            match = next(item for item in sources if item["path"] == note["path"])
            note["sha256"] = match["sha256"]
            note["bytes"] = match["bytes"]
    if set_info["sha256"] != record["dependency"]["set"]["sha256"]:
        reason = reason or "stale dependency set"
    record["dependency"] = dependency
    if reason:
        invalidate_review(record, reason)
    return reason


def command_add_note(ctx: dict) -> int:
    with WorkLock(ctx["work_dir"]):
        found = find_operation(ctx["work_dir"], ctx["profile_id"], ctx["op_id"])
        replay = replay_or_conflict(found, ctx["request"], "add-note", ctx["json"])
        if replay is not None:
            return replay
        slot, record = require_open(ctx)
        note = parse_note(ctx["input"], ctx["retained"])
        sources, set_info, dependency = refresh_current(ctx["code_root"], ctx["pins"], ctx["book"], ctx["profile"], record)
        apply_source_drift(record, sources, set_info, dependency)
        number = len(record["draft_notes"]) + 1
        record["draft_notes"].append(
            {
                "id": f"d{number:02d}",
                "text": note["text"],
                "attribution": note["attribution"],
                "source": note["source"],
                "mark": note["mark"],
                "disposition": "unresolved",
                "integrated_item": None,
                "why": None,
            }
        )
        return finish(slot, record, ctx["op_id"], "add-note", ctx["request"], ctx["json"], ctx["live"])


def command_add_item(ctx: dict) -> int:
    with WorkLock(ctx["work_dir"]):
        found = find_operation(ctx["work_dir"], ctx["profile_id"], ctx["op_id"])
        replay = replay_or_conflict(found, ctx["request"], "add-item", ctx["json"])
        if replay is not None:
            return replay
        slot, record = require_open(ctx)
        item = parse_item(ctx["input"], ctx["retained"])
        if not isinstance(ctx["input"].get("dependency_refs"), list):
            field_stop("dependency_refs", "a list", ctx["retained"])
        if len(record["items"]) >= 32:
            refuse("item list is full")
        sources, set_info, _old = refresh_current(ctx["code_root"], ctx["pins"], ctx["book"], ctx["profile"], record)
        draft = dict(item, id=f"{len(record['items']) + 1:02d}", revision=1)
        check_note_refs(record, draft, ctx["retained"])
        record["items"].append(draft)
        _sources, set_info, dependency = refresh_current(ctx["code_root"], ctx["pins"], ctx["book"], ctx["profile"], record)
        apply_source_drift(record, sources, set_info, dependency)
        return finish(slot, record, ctx["op_id"], "add-item", ctx["request"], ctx["json"], ctx["live"])


def command_revise(ctx: dict) -> int:
    with WorkLock(ctx["work_dir"]):
        found = find_operation(ctx["work_dir"], ctx["profile_id"], ctx["op_id"])
        replay = replay_or_conflict(found, ctx["request"], "revise", ctx["json"])
        if replay is not None:
            return replay
        slot, record = require_open(ctx)
        target = ctx["flags"]["target"]
        sources, set_info, dependency = refresh_current(ctx["code_root"], ctx["pins"], ctx["book"], ctx["profile"], record)
        if target == "intent":
            record["intent"] = parse_intent(ctx["input"], ctx["retained"])
            invalidate_review(record, "intent")
        elif target == "item":
            item_id = ctx["flags"]["item"]
            if not ITEM_RE.fullmatch(item_id):
                refuse("item id must be NN")
            current = next((item for item in record["items"] if item["id"] == item_id), None)
            if current is None:
                refuse("item is not in the draft")
            revised = parse_item(ctx["input"], ctx["retained"])
            check_note_refs(record, revised, ctx["retained"])
            record["revisions"].append({"id": item_id, "revision": current["revision"], "item": current})
            revised["id"] = item_id
            revised["revision"] = current["revision"] + 1
            record["items"] = [revised if item["id"] == item_id else item for item in record["items"]]
            invalidate_review(record, "item")
            _sources, set_info, dependency = refresh_current(
                ctx["code_root"], ctx["pins"], ctx["book"], ctx["profile"], record
            )
        elif target == "disposition":
            note_id = ctx["flags"]["note"]
            note = next((item for item in record["declared_notes"] + record["draft_notes"] if item["id"] == note_id), None)
            if note is None:
                refuse("note is not in the draft")
            value = ctx["input"]
            need_object_keys(value, {"disposition", "item", "why"}, {"disposition"}, ctx["retained"])
            disposition = value["disposition"]
            if disposition not in DISPOSITIONS:
                field_stop("disposition", "integrated, deferred, rejected, or unresolved", ctx["retained"])
            why = value.get("why")
            item_name = value.get("item")
            if disposition in ("deferred", "rejected"):
                if not isinstance(why, str) or why.strip() == "":
                    field_stop("why", "non-empty string", ctx["retained"])
            elif why is not None:
                field_stop("why", "an absent field", ctx["retained"])
            if disposition == "integrated":
                if not isinstance(item_name, str) or not ITEM_RE.fullmatch(item_name):
                    field_stop("item", "NN", ctx["retained"])
                if item_name not in {item["id"] for item in record["items"]}:
                    field_stop("item", "an existing item", ctx["retained"])
            elif item_name is not None:
                field_stop("item", "an absent field", ctx["retained"])
            note["disposition"] = disposition
            note["why"] = why if isinstance(why, str) else None
            note["integrated_item"] = item_name if disposition == "integrated" else None
            invalidate_review(record, "disposition")
        else:
            refuse("unknown revise target")
        apply_source_drift(record, sources, set_info, dependency)
        return finish(slot, record, ctx["op_id"], "revise", ctx["request"], ctx["json"], ctx["live"])


def command_review(ctx: dict) -> int:
    with WorkLock(ctx["work_dir"]):
        found = find_operation(ctx["work_dir"], ctx["profile_id"], ctx["op_id"])
        replay = replay_or_conflict(found, ctx["request"], "review", ctx["json"])
        if replay is not None:
            return replay
        slot, record = require_open(ctx)
        supplied = parse_review(ctx["input"], ctx["retained"])
        sources, set_info, dependency = refresh_current(ctx["code_root"], ctx["pins"], ctx["book"], ctx["profile"], record)
        drift = apply_source_drift(record, sources, set_info, dependency)
        if drift:
            return finish(
                slot,
                record,
                ctx["op_id"],
                "review",
                ctx["request"],
                ctx["json"],
                ctx["live"],
                2,
                drift,
            )
        record["review"] = {
            "assessment": supplied["assessment"],
            "unresolved_issues": supplied["unresolved_issues"],
            "stop_conditions": supplied["stop_conditions"],
            "draft_sha256": "",
            "template_sha256": next(item["sha256"] for item in sources if item["role"] == "template"),
            "source_digest": source_digest(sources),
            "set_sha256": set_info["sha256"],
            "reviewer_supplied": True,
        }
        text = render(record)
        draft_sha = digest(text.encode("utf-8"))
        record["review"]["draft_sha256"] = draft_sha
        expect = ctx["flags"].get("draft")
        if expect and expect != draft_sha:
            record["review"] = None
            refuse(
                f"draft sha256 does not match the rendered draft; retained input {ctx['retained']}. Help: {HELP}"
            )
        return finish(slot, record, ctx["op_id"], "review", ctx["request"], ctx["json"], ctx["live"])


def exclusive_bytes(path: Path, payload: bytes) -> None:
    flags = os.O_CREAT | os.O_EXCL | os.O_WRONLY
    if hasattr(os, "O_BINARY"):
        flags |= os.O_BINARY
    fd = os.open(path, flags)
    try:
        os.write(fd, payload)
        os.fsync(fd)
    finally:
        os.close(fd)


def write_snapshot(slot: Path, record: dict, book: Path) -> tuple[Path, dict]:
    frozen = slot / "frozen"
    if frozen.exists():
        refuse("frozen snapshot directory already exists")
    frozen.mkdir()
    snapshots = frozen / "snapshots"
    snapshots.mkdir()
    rows = []
    for source in record["sources"]:
        raw = walk_book(book, source["path"], "file").read_bytes()
        if digest(raw) != source["sha256"] or len(raw) != source["bytes"]:
            refuse("source changed while freezing")
        snapshot = "snapshots/" + source["path"]
        target = frozen / snapshot
        target.parent.mkdir(parents=True, exist_ok=True)
        if is_link(target.parent):
            refuse("snapshot path is linked and was not followed")
        exclusive_bytes(target, raw)
        rows.append(
            {"path": source["path"], "sha256": source["sha256"], "bytes": source["bytes"], "snapshot": snapshot}
        )
    manifest = {
        "schema": "prime-pack-sources/1",
        "repository": "measured-file",
        "sources": rows,
    }
    manifest_path = frozen / "source-manifest.json"
    exclusive_bytes(manifest_path, canonical_json(manifest))
    return manifest_path, manifest


def run_checker(code_root: Path, pins: dict[str, Path], manifest: Path) -> tuple[int, dict | None]:
    checker = pins["labs/pack-custody-pass01/pack_check.py"]
    command = [
        sys.executable,
        "-B",
        str(checker),
        "--format",
        "prime-pack-sources/1",
        "--manifest",
        str(manifest),
        "--json",
    ]
    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    try:
        result = subprocess.run(command, cwd=code_root, shell=False, capture_output=True, env=env, timeout=60)
    except subprocess.TimeoutExpired:
        refuse("pack check timed out")
    except OSError as exc:
        refuse(f"pack check could not start: {exc.strerror or exc}")
    parsed = None
    try:
        parsed = json.loads(result.stdout.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        parsed = None
    return result.returncode, parsed


def command_freeze(ctx: dict) -> int:
    if ctx["live"] or on_live_tree(ctx["book"]):
        refuse("freeze on the live checkout is outside this slice")
    with WorkLock(ctx["work_dir"]):
        found = find_operation(ctx["work_dir"], ctx["profile_id"], ctx["op_id"])
        replay = replay_or_conflict(found, ctx["request"], "freeze", ctx["json"])
        if replay is not None:
            return replay
        slot, record = require_open(ctx)
        page = ctx["work_dir"] / f"{record['pass']}.md"
        partial_page = ctx["work_dir"] / f"{record['pass']}.md.partial"
        if page.exists() or partial_page.exists():
            refuse("pass page is occupied")
        sources, set_info, dependency = refresh_current(ctx["code_root"], ctx["pins"], ctx["book"], ctx["profile"], record)
        drift = apply_source_drift(record, sources, set_info, dependency)
        if drift:
            return finish(slot, record, ctx["op_id"], "freeze", ctx["request"], ctx["json"], False, 2, drift)
        if intent_missing(record):
            refuse("intent is incomplete")
        if not record["items"]:
            refuse("draft has no item")
        coverage = coverage_blocks(record)
        if coverage:
            refuse(coverage)
        blocked = blocking_dependency(record, set_info["sha256"])
        if blocked:
            refuse(blocked)
        if record["review"] is None:
            refuse("review is absent")
        text = render(record)
        draft_sha = digest(text.encode("utf-8"))
        review = record["review"]
        if ctx["flags"]["draft"] != draft_sha or review["draft_sha256"] != draft_sha:
            refuse("changed review target")
        if review["source_digest"] != source_digest(sources) or review["set_sha256"] != set_info["sha256"]:
            invalidate_review(record, "review-target")
            return finish(
                slot,
                record,
                ctx["op_id"],
                "freeze",
                ctx["request"],
                ctx["json"],
                False,
                2,
                "changed review target",
            )
        manifest_path, _manifest = write_snapshot(slot, record, ctx["book"])
        code, report = run_checker(ctx["code_root"], ctx["pins"], manifest_path)
        matched = (
            code == 0
            and isinstance(report, dict)
            and report.get("entries")
            and all(item.get("result") == "match" for item in report["entries"])
        )
        if not matched:
            record["checker"] = {"exit": code, "report": report if isinstance(report, dict) else None}
            return finish(
                slot,
                record,
                ctx["op_id"],
                "freeze",
                ctx["request"],
                ctx["json"],
                False,
                2,
                "pack check did not match the measured snapshot",
            )
        payload = text.encode("utf-8")
        exclusive_bytes(page, payload)
        record["state"] = "frozen"
        record["stamp"] = "prepared"
        record["checker"] = {"exit": code, "manifest": str(manifest_path), "label": "measured-file", "form": "working-tree"}
        return finish(slot, record, ctx["op_id"], "freeze", ctx["request"], ctx["json"], False)


def command_inspect(ctx: dict) -> int:
    sessions = open_sessions(ctx["work_dir"], ctx["profile_id"])
    frozen = [
        (slot, record)
        for slot, record in iter_records(ctx["work_dir"])
        if record.get("profile_id") == ctx["profile_id"] and record.get("state") == "frozen"
    ]
    if len(sessions) == 1:
        slot, record = sessions[0]
    elif not sessions and len(frozen) == 1:
        slot, record = frozen[0]
    elif not sessions and not frozen:
        refuse("no open session")
    else:
        refuse("ambiguous session")
    sources, set_info, dependency = refresh_current(ctx["code_root"], ctx["pins"], ctx["book"], ctx["profile"], record)
    result = result_for(record, slot, "inspect", ctx["live"])
    result["live"] = live_view(record, sources, set_info)
    result["live_dependency"] = {"queries": dependency["queries"], "item_refs": dependency["item_refs"]}
    result["review_valid"] = (
        record["review"] is not None
        and not result["live"]["source_drift"]
        and not result["live"]["set_drift"]
        and record["review"]["draft_sha256"] == result["draft_sha256"]
    )
    return emit(result, 0, ctx["json"])


def parse_call(args: list[str]) -> tuple[str, dict[str, str], bool]:
    if not args:
        refuse("missing authoring command")
    command = args[0]
    if command not in COMMANDS:
        refuse("unknown authoring command")
    allowed = {
        "start": {"--book", "--profile", "--operation", "--input", "--json"},
        "add-note": {"--book", "--profile", "--operation", "--input", "--json"},
        "add-item": {"--book", "--profile", "--operation", "--input", "--json"},
        "revise": {"--book", "--profile", "--operation", "--target", "--input", "--item", "--note", "--json"},
        "inspect": {"--book", "--profile", "--json"},
        "review": {"--book", "--profile", "--operation", "--input", "--draft-sha256", "--json"},
        "freeze": {"--book", "--profile", "--operation", "--draft-sha256", "--json"},
    }[command]
    values: dict[str, str] = {}
    as_json = False
    index = 1
    while index < len(args):
        token = args[index]
        if token in BANNED or any(token.startswith(prefix + "=") for prefix in BANNED):
            refuse("caller tool override is refused")
        if token == "--json":
            if as_json:
                refuse("repeated --json")
            as_json = True
            index += 1
            continue
        if not token.startswith("--"):
            refuse("unknown argument")
        if token not in allowed:
            refuse("unknown argument")
        key = token[2:]
        if key in values:
            refuse(f"repeated {token}")
        if index + 1 >= len(args) or args[index + 1].startswith("--"):
            refuse(f"missing value for {token}")
        values[key] = args[index + 1]
        index += 2
    for name in ("book", "profile"):
        if name not in values:
            refuse(f"missing --{name}")
    if command != "inspect" and "operation" not in values:
        refuse("missing --operation")
    if command in ("add-note", "add-item", "revise", "review") and "input" not in values:
        refuse("missing --input")
    if command == "revise" and "target" not in values:
        refuse("missing --target")
    if command == "revise" and values["target"] == "item" and "item" not in values:
        refuse("missing --item")
    if command == "revise" and values["target"] == "disposition" and "note" not in values:
        refuse("missing --note")
    if command == "freeze" and "draft-sha256" not in values:
        refuse("missing --draft-sha256")
    if "draft-sha256" in values and not HEX_RE.fullmatch(values["draft-sha256"]):
        refuse("draft sha256 must be 64 lowercase hex")
    if "operation" in values and not OP_RE.fullmatch(values["operation"]):
        refuse("operation id is not a label")
    renamed = dict(values)
    if "draft-sha256" in renamed:
        renamed["draft"] = renamed.pop("draft-sha256")
    return command, renamed, as_json


def perform(args: list[str], code_root: Path, replace=os.replace) -> int:
    command, flags, as_json = parse_call(args)
    pins = load_pins(code_root)
    profile = load_profile(pins, flags["profile"])
    book = book_root(flags["book"], profile["book_policy"])
    if command == "freeze" and (on_live_tree(book) or inside(book, CHECKOUT)):
        refuse("freeze on the live checkout is outside this slice")
    work_dir = walk_book(book, profile["work_home"], "dir")
    retained = flags.get("input", "")
    document, raw = load_input(flags.get("input"))
    if command in ("add-note", "add-item", "revise", "review") and document is None:
        refuse("missing --input")
    op_id = flags.get("operation", "")
    request = request_sha(command, flags, raw) if command != "inspect" else ""
    ctx = {
        "code_root": code_root,
        "pins": pins,
        "profile": profile,
        "profile_id": flags["profile"],
        "book": book,
        "work_dir": work_dir,
        "live": on_live_tree(book),
        "json": as_json,
        "op_id": op_id,
        "request": request,
        "input": document,
        "retained": retained,
        "flags": flags,
        "replace": replace,
    }
    if command == "inspect":
        return command_inspect(ctx)
    if command == "start":
        return command_start(ctx)
    if command == "add-note":
        return command_add_note(ctx)
    if command == "add-item":
        return command_add_item(ctx)
    if command == "revise":
        return command_revise(ctx)
    if command == "review":
        return command_review(ctx)
    if command == "freeze":
        return command_freeze(ctx)
    refuse("unknown authoring command")
    return 2


def main(argv: list[str] | None = None) -> int:
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="backslashreplace", newline="\n")
    args = list(sys.argv[1:] if argv is None else argv)
    try:
        return perform(args, Path(__file__).resolve().parents[2])
    except Refuse as exc:
        print(f"stop: {exc}", file=sys.stderr)
        return 2
    except Partial as exc:
        print(f"partial: {exc}", file=sys.stderr)
        return 4


if __name__ == "__main__":
    sys.exit(main())
