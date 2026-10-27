"""Local return capture, schema return-capture/1.

Reserve, capture, and verify one return member. A receipt means the copy
finished and the hashes match. It does not approve, accept, seat, publish,
or finish the work. This tool does not split a return on a Review heading.
The book may be an ordinary directory in a Git checkout. This tool does not
invoke Git.
"""

from __future__ import annotations

import argparse
import functools
import hashlib
import json
import os
import re
import stat
import sys
import time
import unicodedata
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path


SCHEMA = "return-capture/1"
DOOR_NAME = "0100.band.returns"
LOCK_NAME = ".allocation.lock"
MEMBER_MIN = 101
MEMBER_MAX = 199
LOCK_WAIT_SECONDS = 5.0
TEXT_LIMIT = 4096
FILE_ATTRIBUTE_REPARSE_POINT = 0x400

RESERVED_WINDOWS = {
    "CON",
    "PRN",
    "AUX",
    "NUL",
    *(f"COM{n}" for n in range(1, 10)),
    *(f"LPT{n}" for n in range(1, 10)),
}

_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,63}$")
_BATCH = re.compile(r"^05\.\d{2}$")
_SLOT = re.compile(r"^(\d{4})(?:$|\.|[^0-9])")
_MEMBER = re.compile(r"^(\d{4})\.([A-Za-z0-9][A-Za-z0-9._-]{0,63})$")
_HEX40 = re.compile(r"^[0-9a-f]{40}$")
_HEX64 = re.compile(r"^[0-9a-f]{64}$")

RESERVATION_KEYS = {
    "schema",
    "kind",
    "submission_id",
    "origin",
    "destination",
    "expected_outputs",
    "submitter",
    "reviewer",
    "release",
    "supersedes",
    "reserved_at",
}
ORIGIN_KEYS = {"book", "page", "batch"}
DESTINATION_KEYS = {"member", "name", "path"}
MANIFEST_KEYS = {
    "schema",
    "kind",
    "submission_id",
    "reservation_sha256",
    "return",
    "retrospective",
    "source_commit",
    "captured_at",
    "sources",
    "omitted",
    "required",
}
RETURN_KEYS = {"sha256", "bytes", "includes_prime_review"}
SOURCE_KEYS = {"logical", "payload", "sha256", "bytes"}
OMITTED_KEYS = {"logical", "reason"}
RECEIPT_KEYS = {
    "schema",
    "kind",
    "submission_id",
    "reservation_sha256",
    "manifest_sha256",
    "captured_at",
}
CAPTURE_NAMES = {"return.md", "manifest.json", "receipt.json"}
ROOT_FILES = {
    "01.md",
    "reservation.json",
    "return.md",
    "manifest.json",
    "receipt.json",
    "payload",
}


class Refusal(Exception):
    pass


class Result:
    def __init__(self, code: int, text: str) -> None:
        if not text.endswith("\n"):
            text += "\n"
        self.code = code
        self.text = text


def refuse(message: str) -> None:
    if not message.endswith("\n"):
        message += "\n"
    if "result refused" not in message:
        message += "result refused\n"
    raise Refusal(message)


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
        return f"{label} is not a string"
    if value != unicodedata.normalize("NFKC", value):
        return f"{label} is ambiguous"
    if not _ID.fullmatch(value) or value.endswith(".") or value.endswith(" "):
        return f"{label} is not a windows-safe id"
    if value.split(".", 1)[0].upper() in RESERVED_WINDOWS:
        return f"{label} is a reserved windows name"
    return None


def require_id(value, label: str) -> str:
    problem = id_problem(value, label)
    if problem:
        refuse(problem)
    return value


def require_text(value, label: str) -> str:
    if not isinstance(value, str):
        refuse(f"{label} is not a string")
    if value == "" or len(value) > TEXT_LIMIT:
        refuse(f"{label} is empty or too long")
    if any(ord(ch) < 32 or ord(ch) == 127 for ch in value):
        refuse(f"{label} has control characters")
    return value


def logical_problem(value: str) -> str | None:
    if not isinstance(value, str) or value == "" or len(value) > TEXT_LIMIT:
        return "logical name is empty or too long"
    if any(ord(ch) < 32 or ord(ch) == 127 for ch in value):
        return "logical name has control characters"
    if "\\" in value or value.startswith("/") or re.match(r"^[A-Za-z]:", value):
        return "logical name is absolute"
    parts = value.split("/")
    for part in parts:
        if part in ("", ".", "..") or part.endswith(".") or part.endswith(" "):
            return "logical name has an unsafe segment"
        if part.split(".", 1)[0].upper() in RESERVED_WINDOWS:
            return "logical name is a reserved windows name"
    return None


def require_logical(value: str) -> str:
    problem = logical_problem(value)
    if problem:
        refuse(problem)
    return value


def relative_problem(value: str) -> str | None:
    if not isinstance(value, str) or value == "" or len(value) > TEXT_LIMIT:
        return "artifact path is empty or too long"
    if any(ord(ch) < 32 or ord(ch) == 127 for ch in value):
        return "artifact path has control characters"
    if "\\" in value or value.startswith("/") or re.match(r"^[A-Za-z]:", value):
        return "artifact path is absolute"
    parts = value.split("/")
    for part in parts:
        if part in ("", ".", "..") or part.endswith(".") or part.endswith(" "):
            return "artifact path has an unsafe segment"
        if part.split(".", 1)[0].upper() in RESERVED_WINDOWS:
            return "artifact path is a reserved windows name"
    return None


def require_relative(value: str) -> str:
    problem = relative_problem(value)
    if problem:
        refuse(problem)
    return value


def require_absolute(text: str, label: str) -> Path:
    if not isinstance(text, str) or not os.path.isabs(text):
        refuse(f"{label} must be absolute")
    return Path(os.path.abspath(text))


def writer_destination_problem(path: Path) -> str | None:
    """A checkout may contain the book. Roots and Git control paths may not.

    The check looks at this path only. It does not walk parents for a
    `.git` marker, so a worktree whose `.git` entry is a file stays usable.
    A filesystem root is refused before any door or member is created.
    """
    absolute = Path(os.path.abspath(path))
    if absolute.parent == absolute:
        return "a filesystem root"
    for part in absolute.parts:
        if part.casefold() == ".git":
            return "a Git control path"
    return None


def require_writer_book(text: str) -> Path:
    book = require_absolute(text, "book")
    problem = writer_destination_problem(book)
    if problem:
        refuse(f"book is {problem}")
    problem = plain_dir_problem(book)
    if problem:
        refuse(f"book is {problem}")
    return book


def require_reader_book(text: str) -> Path:
    book = require_absolute(text, "book")
    problem = plain_dir_problem(book)
    if problem:
        refuse(f"book is {problem}")
    return book


def reject_reparse_parents(path: Path) -> None:
    if not path.is_absolute():
        refuse("path is not absolute")
    current = Path(path.anchor)
    for part in path.parts[1:]:
        if part in ("", ".", ".."):
            refuse(f"path escape: {path}")
        current = current / part
        if not os.path.lexists(current):
            return
        try:
            if is_reparse(current):
                refuse(f"link: {current}")
        except OSError as exc:
            refuse(f"filesystem: {type(exc).__name__}: {exc.strerror or exc}")


def within(child: Path, parent: Path) -> bool:
    try:
        child_abs = os.path.normcase(os.path.abspath(child))
        parent_abs = os.path.normcase(os.path.abspath(parent))
        return os.path.commonpath([child_abs, parent_abs]) == parent_abs
    except ValueError:
        return False


def exclusive_write(path: Path, data: bytes) -> None:
    flags = os.O_CREAT | os.O_EXCL | os.O_WRONLY
    if hasattr(os, "O_BINARY"):
        flags |= os.O_BINARY
    fd = os.open(str(path), flags)
    try:
        view = memoryview(data)
        while view:
            written = os.write(fd, view)
            if written <= 0:
                raise OSError("short write")
            view = view[written:]
    finally:
        os.close(fd)


def ensure_door(door: Path) -> None:
    if os.path.lexists(door):
        problem = plain_dir_problem(door)
        if problem:
            refuse(f"return door is {problem}")
        return
    try:
        os.mkdir(door)
    except FileExistsError:
        problem = plain_dir_problem(door)
        if problem:
            refuse(f"return door is {problem}")


@contextmanager
def allocation_lock(door: Path):
    """Hold the door lock for this reserve only. A crash can leave the lock."""
    ensure_door(door)
    lock = door / LOCK_NAME
    fd = None
    deadline = time.monotonic() + LOCK_WAIT_SECONDS
    while True:
        try:
            fd = os.open(str(lock), os.O_CREAT | os.O_EXCL | os.O_RDWR)
            break
        except FileExistsError:
            if time.monotonic() >= deadline:
                refuse(f"allocation lock held: {lock}")
            time.sleep(0.05)
    try:
        yield
    finally:
        if fd is not None:
            os.close(fd)
            os.remove(lock)


def slot_number(name: str) -> int | None:
    match = _SLOT.match(name)
    if not match:
        return None
    number = int(match.group(1))
    if MEMBER_MIN <= number <= MEMBER_MAX:
        return number
    return None


def member_name(number: int, slug: str) -> str:
    return f"{number:04d}.{slug}"


def occupied_numbers(book: Path) -> set[int]:
    taken: set[int] = set()
    if not os.path.lexists(book):
        return taken
    for entry in os.listdir(book):
        number = slot_number(entry)
        if number is not None:
            taken.add(number)
    return taken


def read_exact(path: Path) -> bytes:
    problem = plain_file_problem(path)
    if problem:
        refuse(f"{problem}: {path.name}")
    return path.read_bytes()


def read_stable(path: Path) -> bytes:
    first = read_exact(path)
    second = read_exact(path)
    if first != second:
        refuse("bytes changed before capture")
    return first


def load_json_file(path: Path):
    data = read_exact(path)
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        refuse(f"invalid JSON bytes: {path.name}")
    value = loads_strict(text)
    return data, value


def require_object(value, label: str) -> dict:
    if not isinstance(value, dict):
        refuse(f"{label} is not an object")
    return value


def require_exact_keys(value: dict, keys: set[str], label: str) -> None:
    if set(value) != keys:
        refuse(f"{label} keys are {sorted(value)}")


def parse_reservation(data: bytes, value) -> dict:
    body = require_object(value, "reservation")
    require_exact_keys(body, RESERVATION_KEYS, "reservation")
    if body["schema"] != SCHEMA or body["kind"] != "reservation":
        refuse("reservation schema mismatch")
    if id_problem(body["submission_id"], "submission"):
        refuse("reservation submission is not usable")
    origin = require_object(body["origin"], "origin")
    require_exact_keys(origin, ORIGIN_KEYS, "origin")
    destination = require_object(body["destination"], "destination")
    require_exact_keys(destination, DESTINATION_KEYS, "destination")
    outputs = body["expected_outputs"]
    if not isinstance(outputs, list) or any(logical_problem(item) for item in outputs):
        refuse("reservation expected outputs are not usable")
    folded = [item.casefold() for item in outputs]
    if len(folded) != len(set(folded)):
        refuse("reservation expected outputs collide")
    for label in ("submitter", "reviewer", "release"):
        if not isinstance(body[label], str):
            refuse(f"reservation {label} is not usable")
    supersedes = body["supersedes"]
    if supersedes is not None and not isinstance(supersedes, str):
        refuse("reservation supersedes is not usable")
    if not isinstance(body["reserved_at"], str) or body["reserved_at"] == "":
        refuse("reservation time is not usable")
    for key in ("book", "page", "batch"):
        if not isinstance(origin[key], str) or origin[key] == "":
            refuse("reservation origin is not usable")
    for key in ("member", "name", "path"):
        if not isinstance(destination[key], str) or destination[key] == "":
            refuse("reservation destination is not usable")
    return body


def reservation_identity(body: dict) -> tuple:
    origin = body["origin"]
    return (
        body["submission_id"],
        origin["book"],
        origin["page"],
        origin["batch"],
        tuple(body["expected_outputs"]),
        body["submitter"],
        body["reviewer"],
        body["release"],
        body["supersedes"],
        body["destination"]["name"],
    )


def request_identity(fields: dict) -> tuple:
    return (
        fields["submission_id"],
        fields["origin_book"],
        fields["origin_page"],
        fields["origin_batch"],
        tuple(fields["expected_outputs"]),
        fields["submitter"],
        fields["reviewer"],
        fields["release"],
        fields["supersedes"],
        fields["name"],
    )


def iter_member_dirs(book: Path) -> list[tuple[int, str, Path]]:
    found = []
    for entry in os.listdir(book):
        number = slot_number(entry)
        if number is None:
            continue
        path = book / entry
        if plain_dir_problem(path) is not None:
            continue
        found.append((number, entry, path))
    found.sort(key=lambda item: (item[0], item[1].casefold()))
    return found


def reservations_for(book: Path, submission_id: str) -> list[tuple[str, dict, bytes]]:
    matches = []
    if plain_dir_problem(book) is not None:
        return matches
    for _number, entry, path in iter_member_dirs(book):
        pointer = path / "reservation.json"
        if not os.path.lexists(pointer):
            continue
        if plain_file_problem(pointer) is not None:
            continue
        try:
            data, value = load_json_file(pointer)
            body = parse_reservation(data, value)
        except Refusal:
            continue
        if body["submission_id"] == submission_id:
            matches.append((entry, body, data))
    return matches


def index_page(fields: dict, folder: str) -> bytes:
    lines = [
        "# 01",
        "",
        f"schema: {SCHEMA}",
        f"submission: {fields['submission_id']}",
        f"origin-book: {fields['origin_book']}",
        f"origin-page: {fields['origin_page']}",
        f"origin-batch: {fields['origin_batch']}",
        f"member: {folder}",
    ]
    if fields["supersedes"]:
        lines.append(f"supersedes: {fields['supersedes']}")
    lines.extend(
        [
            "",
            "This page is an index. It is not a completion status.",
            "Verify receipt.json.",
            "A verified receipt is not approval, acceptance, seating, publication, or finish.",
            "",
        ]
    )
    return "\n".join(lines).encode("utf-8")


def check_supersedes(book: Path, supersedes: str, submission_id: str) -> None:
    match = _MEMBER.fullmatch(supersedes)
    if not match or id_problem(match.group(2), "supersedes"):
        refuse("supersedes is not a member path")
    number = int(match.group(1))
    if not (MEMBER_MIN <= number <= MEMBER_MAX):
        refuse("supersedes is outside the return band")
    target = book / supersedes
    if plain_dir_problem(target) is not None:
        refuse(f"supersedes is missing: {supersedes}")
    pointer = target / "reservation.json"
    if plain_file_problem(pointer) is not None:
        refuse(f"supersedes has no reservation: {supersedes}")
    data, value = load_json_file(pointer)
    body = parse_reservation(data, value)
    if body["submission_id"] == submission_id:
        refuse("supersedes is the same submission")
    if body["destination"]["path"] != supersedes:
        refuse("supersedes destination does not match its folder")


def guarded(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except Refusal as exc:
            return Result(2, str(exc))

    return wrapper


@guarded
def reserve(
    book: str,
    submission: str,
    name: str,
    origin_book: str,
    origin_page: str,
    origin_batch: str,
    expected_outputs: list[str] | None,
    submitter: str,
    reviewer: str,
    release: str,
    supersedes: str | None = None,
) -> Result:
    fields = {
        "submission_id": require_id(submission, "submission"),
        "name": require_id(name, "name"),
        "origin_book": require_id(origin_book, "origin book"),
        "origin_page": require_id(origin_page, "origin page"),
        "origin_batch": origin_batch,
        "expected_outputs": list(expected_outputs or []),
        "submitter": require_text(submitter, "submitter"),
        "reviewer": require_text(reviewer, "reviewer"),
        "release": require_text(release, "release"),
        "supersedes": supersedes,
    }
    if not isinstance(origin_batch, str) or not _BATCH.fullmatch(origin_batch):
        refuse("origin batch must match 05.NN")
    folded = []
    for item in fields["expected_outputs"]:
        logical = require_logical(item)
        if logical.casefold() in folded:
            refuse(f"duplicate logical name: {logical}")
        folded.append(logical.casefold())
    if supersedes is not None:
        require_text(supersedes, "supersedes")
    book_path = require_writer_book(book)
    if supersedes is not None and plain_dir_problem(book_path / DOOR_NAME) == "missing":
        if not os.path.lexists(book_path / supersedes):
            refuse(f"supersedes is missing: {supersedes}")
    with allocation_lock(book_path / DOOR_NAME):
        matches = reservations_for(book_path, fields["submission_id"])
        if len(matches) > 1:
            lines = [f"conflict submission {fields['submission_id']}"]
            lines.extend(f"existing {entry}" for entry, _body, _data in matches)
            refuse("\n".join(lines))
        if len(matches) == 1:
            entry, body, _data = matches[0]
            if reservation_identity(body) != request_identity(fields):
                refuse(
                    f"conflict submission {fields['submission_id']}\nexisting {entry}"
                )
            return Result(
                0,
                f"member {entry}\nsubmission {fields['submission_id']}\n"
                "result already-reserved",
            )
        if supersedes is not None:
            check_supersedes(book_path, supersedes, fields["submission_id"])
        taken = occupied_numbers(book_path)
        number = None
        for candidate in range(MEMBER_MIN, MEMBER_MAX + 1):
            if candidate not in taken:
                number = candidate
                break
        if number is None:
            refuse("return band is full")
        folder = member_name(number, fields["name"])
        target = book_path / folder
        if os.path.lexists(target):
            refuse(f"member path raced: {folder}")
        os.mkdir(target)
        # A crash after mkdir and before reservation.json leaves the number
        # occupied with no submission id. A later retry can take a new number.
        body = {
            "schema": SCHEMA,
            "kind": "reservation",
            "submission_id": fields["submission_id"],
            "origin": {
                "book": fields["origin_book"],
                "page": fields["origin_page"],
                "batch": fields["origin_batch"],
            },
            "destination": {
                "member": f"{number:04d}",
                "name": fields["name"],
                "path": folder,
            },
            "expected_outputs": list(fields["expected_outputs"]),
            "submitter": fields["submitter"],
            "reviewer": fields["reviewer"],
            "release": fields["release"],
            "supersedes": supersedes,
            "reserved_at": now_stamp(),
        }
        exclusive_write(target / "reservation.json", canonical(body))
        exclusive_write(target / "01.md", index_page(fields, folder))
    return Result(
        0,
        f"member {folder}\nsubmission {fields['submission_id']}\nresult reserved",
    )


def resolve_source(root: Path, relative: str) -> Path:
    require_relative(relative)
    reject_reparse_parents(root)
    current = root
    for part in relative.split("/"):
        current = current / part
        if not os.path.lexists(current):
            refuse(f"missing {relative}")
        if is_reparse(current):
            refuse(f"link: {current}")
    if not within(current, root):
        refuse(f"path escape: {relative}")
    return current


def capture_entries(member: Path) -> list[str]:
    retained = []
    if not os.path.isdir(member):
        return retained
    for name in CAPTURE_NAMES:
        if os.path.lexists(member / name):
            retained.append(name)
    payload = member / "payload"
    if os.path.lexists(payload):
        retained.append("payload")
        if plain_dir_problem(payload) is None:
            for dirpath, dirnames, filenames in os.walk(payload, followlinks=False):
                base = Path(dirpath)
                for dirname in dirnames:
                    rel = (base / dirname).relative_to(member).as_posix()
                    retained.append(rel)
                for filename in filenames:
                    rel = (base / filename).relative_to(member).as_posix()
                    retained.append(rel)
    return sorted(set(retained))


def partial_result(folder: str, member: Path, extra: str | None = None) -> Result:
    lines = [f"partial {folder}"]
    lines.extend(f"retained {rel}" for rel in capture_entries(member))
    if extra:
        lines.append(extra)
    lines.append("result refused")
    return Result(2, "\n".join(lines))


def assess(member: Path) -> tuple[str, dict | None]:
    """Return complete, incomplete, or absent. Absent means no capture files."""
    if capture_entries(member) == []:
        return "absent", None
    try:
        info = verify_member(member)
    except Refusal:
        return "incomplete", None
    return "complete", info


def verify_member(member: Path) -> dict:
    if plain_dir_problem(member) is not None:
        refuse(f"member is {plain_dir_problem(member)}")
    folder = member.name
    match = _MEMBER.fullmatch(folder)
    if not match or id_problem(match.group(2), "member"):
        refuse("member path is not a return member")
    number = int(match.group(1))
    if not (MEMBER_MIN <= number <= MEMBER_MAX):
        refuse("member is outside the return band")
    reject_reparse_parents(member)
    present = set()
    payload_files = []
    for dirpath, dirnames, filenames in os.walk(member, followlinks=False):
        base = Path(dirpath)
        for dirname in list(dirnames):
            path = base / dirname
            rel = path.relative_to(member).as_posix()
            if os.path.lexists(path) and is_reparse(path):
                refuse(f"unexpected {rel}")
            if rel != "payload":
                refuse(f"unexpected {rel}")
        for filename in filenames:
            path = base / filename
            rel = path.relative_to(member).as_posix()
            if is_reparse(path) or plain_file_problem(path) is not None:
                refuse(f"unexpected {rel}")
            present.add(rel)
            if rel.startswith("payload/"):
                payload_files.append(rel)
    file_allowed = ROOT_FILES - {"payload"}
    extra_files = [
        rel
        for rel in present
        if rel not in file_allowed and not rel.startswith("payload/")
    ]
    if extra_files:
        refuse(f"unexpected {sorted(extra_files)[0]}")
    for required_name in ("reservation.json", "return.md", "manifest.json", "receipt.json"):
        if required_name not in present:
            refuse(f"missing {required_name}")
    reservation_bytes, reservation_value = load_json_file(member / "reservation.json")
    reservation = parse_reservation(reservation_bytes, reservation_value)
    destination = reservation["destination"]
    if destination["path"] != folder:
        refuse("destination path does not match the member folder")
    if destination["member"] != f"{number:04d}" or destination["name"] != match.group(2):
        refuse("destination identity does not match the member folder")
    manifest_bytes, manifest_value = load_json_file(member / "manifest.json")
    manifest = require_object(manifest_value, "manifest")
    require_exact_keys(manifest, MANIFEST_KEYS, "manifest")
    if manifest["schema"] != SCHEMA or manifest["kind"] != "manifest":
        refuse("manifest schema mismatch")
    if manifest["submission_id"] != reservation["submission_id"]:
        refuse("manifest submission mismatch")
    if manifest["reservation_sha256"] != sha256_bytes(reservation_bytes):
        refuse("hash mismatch reservation")
    if not _HEX64.fullmatch(manifest["reservation_sha256"]):
        refuse("hash mismatch reservation")
    return_meta = require_object(manifest["return"], "return")
    require_exact_keys(return_meta, RETURN_KEYS, "return")
    if type(return_meta["includes_prime_review"]) is not bool:
        refuse("return review flag is not a boolean")
    if type(return_meta["bytes"]) is not int or return_meta["bytes"] < 0:
        refuse("return length is not an integer")
    if not isinstance(return_meta["sha256"], str) or not _HEX64.fullmatch(return_meta["sha256"]):
        refuse("return hash is not usable")
    if type(manifest["retrospective"]) is not bool:
        refuse("retrospective flag is not a boolean")
    source_commit = manifest["source_commit"]
    if manifest["retrospective"]:
        if not isinstance(source_commit, str) or not _HEX40.fullmatch(source_commit):
            refuse("source commit is not 40 hex")
    elif source_commit is not None:
        refuse("source commit is set on a current capture")
    if not isinstance(manifest["captured_at"], str) or manifest["captured_at"] == "":
        refuse("captured_at is empty")
    sources = manifest["sources"]
    omitted = manifest["omitted"]
    required = manifest["required"]
    if not isinstance(sources, list) or not isinstance(omitted, list) or not isinstance(required, list):
        refuse("manifest lists are not usable")
    if omitted != []:
        refuse("omitted evidence is present")
    for item in required:
        if logical_problem(item):
            refuse("required logical name is not usable")
    seen = []
    described = []
    for index, source in enumerate(sources, start=1):
        source = require_object(source, "source")
        require_exact_keys(source, SOURCE_KEYS, "source")
        logical = source["logical"]
        if logical_problem(logical):
            refuse("source logical name is not usable")
        if logical.casefold() in seen:
            refuse(f"duplicate logical name: {logical}")
        seen.append(logical.casefold())
        payload_name = f"{index:04d}.blob"
        if source["payload"] != payload_name:
            refuse(f"unexpected payload/{source['payload']}")
        if type(source["bytes"]) is not int or source["bytes"] < 0:
            refuse("source length is not an integer")
        if not isinstance(source["sha256"], str) or not _HEX64.fullmatch(source["sha256"]):
            refuse("source hash is not usable")
        described.append(f"payload/{payload_name}")
    if described != sorted(payload_files):
        extras = [item for item in payload_files if item not in described]
        if extras:
            refuse(f"unexpected {extras[0]}")
        refuse("payload list does not match the manifest")
    if [source["logical"] for source in sources] != required:
        refuse("required outputs do not match the payload")
    has_payload_dir = os.path.lexists(member / "payload")
    if sources and not has_payload_dir:
        refuse("payload list does not match the manifest")
    if not sources and has_payload_dir:
        refuse("unexpected payload")
    return_bytes = read_exact(member / "return.md")
    if sha256_bytes(return_bytes) != return_meta["sha256"] or len(return_bytes) != return_meta["bytes"]:
        refuse("hash mismatch return")
    payload_hashes = []
    for source, rel in zip(sources, described):
        payload_bytes = read_exact(member / rel)
        digest = sha256_bytes(payload_bytes)
        if digest != source["sha256"] or len(payload_bytes) != source["bytes"]:
            refuse(f"hash mismatch {rel}")
        payload_hashes.append((rel, digest))
    receipt_bytes, receipt_value = load_json_file(member / "receipt.json")
    receipt = require_object(receipt_value, "receipt")
    require_exact_keys(receipt, RECEIPT_KEYS, "receipt")
    if receipt["schema"] != SCHEMA or receipt["kind"] != "receipt":
        refuse("receipt schema mismatch")
    if receipt["submission_id"] != reservation["submission_id"]:
        refuse("receipt submission mismatch")
    if receipt["reservation_sha256"] != sha256_bytes(reservation_bytes):
        refuse("hash mismatch reservation")
    if receipt["manifest_sha256"] != sha256_bytes(manifest_bytes):
        refuse("hash mismatch manifest")
    if not isinstance(receipt["captured_at"], str) or receipt["captured_at"] == "":
        refuse("captured_at is empty")
    return {
        "folder": folder,
        "reservation_sha256": sha256_bytes(reservation_bytes),
        "manifest_sha256": sha256_bytes(manifest_bytes),
        "receipt_sha256": sha256_bytes(receipt_bytes),
        "payloads": payload_hashes,
        "manifest": manifest,
        "reservation": reservation,
    }


@guarded
def verify(book: str, member: str) -> Result:
    book_path = require_reader_book(book)
    if not isinstance(member, str) or "/" in member or "\\" in member:
        refuse("member path is not a return member")
    match = _MEMBER.fullmatch(member)
    if not match or id_problem(match.group(2), "member"):
        refuse("member path is not a return member")
    member_path = book_path / member
    if not within(member_path, book_path):
        refuse("member path is outside the book")
    info = verify_member(member_path)
    lines = [
        f"reservation {info['reservation_sha256']}",
        f"manifest {info['manifest_sha256']}",
        f"receipt {info['receipt_sha256']}",
    ]
    for rel, digest in info["payloads"]:
        lines.append(f"payload {Path(rel).name} {digest}")
    lines.extend(
        [
            "result complete",
            "not approved",
            "not accepted",
            "not published",
        ]
    )
    return Result(0, "\n".join(lines))


def same_capture(info: dict, snapshot: dict) -> bool:
    manifest = info["manifest"]
    return_meta = manifest["return"]
    if return_meta["sha256"] != snapshot["return_sha256"]:
        return False
    if return_meta["bytes"] != snapshot["return_bytes"]:
        return False
    if return_meta["includes_prime_review"] is not snapshot["includes_prime_review"]:
        return False
    if manifest["retrospective"] is not snapshot["retrospective"]:
        return False
    if manifest["source_commit"] != snapshot["source_commit"]:
        return False
    if manifest["required"] != snapshot["required"]:
        return False
    sources = manifest["sources"]
    if [item["logical"] for item in sources] != snapshot["logicals"]:
        return False
    if [item["sha256"] for item in sources] != snapshot["hashes"]:
        return False
    if [item["bytes"] for item in sources] != snapshot["lengths"]:
        return False
    return True


@guarded
def capture(
    book: str,
    submission: str,
    return_file: str,
    source_root: str,
    artifacts: list[str] | None = None,
    retrospective: bool = False,
    source_commit: str | None = None,
    return_includes_prime_review: bool = False,
    *,
    interrupt: str | None = None,
) -> Result:
    if interrupt not in (None, "before-write", "after-return", "before-receipt"):
        refuse("interrupt point is not usable")
    submission_id = require_id(submission, "submission")
    book_path = require_writer_book(book)
    root = require_absolute(source_root, "source root")
    if plain_dir_problem(root) is not None:
        refuse(f"source root is {plain_dir_problem(root)}")
    reject_reparse_parents(root)
    return_path = require_absolute(return_file, "return file")
    reject_reparse_parents(return_path)
    if retrospective:
        if not isinstance(source_commit, str) or not _HEX40.fullmatch(source_commit):
            refuse("source commit is not 40 hex")
    elif source_commit is not None:
        refuse("source commit is set on a current capture")
    if type(retrospective) is not bool or type(return_includes_prime_review) is not bool:
        refuse("capture flag is not a boolean")
    matches = reservations_for(book_path, submission_id)
    if len(matches) != 1:
        if not matches:
            refuse(f"reservation is missing: {submission_id}")
        lines = [f"conflict submission {submission_id}"]
        lines.extend(f"existing {entry}" for entry, _body, _data in matches)
        refuse("\n".join(lines))
    folder, reservation, reservation_bytes = matches[0]
    member = book_path / folder
    if reservation["destination"]["path"] != folder:
        refuse("destination path does not match the member folder")
    expected = list(reservation["expected_outputs"])
    parsed: list[tuple[str, str]] = []
    logicals = []
    relatives = []
    for raw in list(artifacts or []):
        if not isinstance(raw, str) or "|" not in raw:
            refuse("artifact must be relative|logical")
        relative, logical = raw.split("|", 1)
        require_relative(relative)
        require_logical(logical)
        if logical.casefold() in [item.casefold() for item in logicals]:
            refuse(f"duplicate logical name: {logical}")
        if relative.casefold() in [item.casefold() for item in relatives]:
            refuse(f"duplicate source: {relative}")
        logicals.append(logical)
        relatives.append(relative)
        parsed.append((relative, logical))
    state, info = assess(member)
    if state == "incomplete":
        return partial_result(folder, member)
    if within(root, member):
        refuse("source root is inside the destination member")
    if within(return_path, member):
        refuse("return file is inside the destination member")
    if state == "complete" and logicals != expected:
        return Result(
            2,
            f"conflict submission {submission_id}\nexisting {folder}\nresult refused",
        )
    if logicals != expected:
        missing = [item for item in expected if item not in logicals]
        if missing:
            lines = [f"missing {item}" for item in missing]
            lines.append("result refused")
            return Result(2, "\n".join(lines))
        refuse("artifact list does not match the reservation")
    for relative, logical in parsed:
        candidate = root.joinpath(*relative.split("/"))
        if not within(candidate, root):
            refuse(f"path escape: {relative}")
        if within(candidate, member):
            refuse(f"artifact is inside the destination member: {relative}")
        if not os.path.lexists(candidate):
            return Result(2, f"missing {logical}\nresult refused")
    wanted = {
        "includes_prime_review": return_includes_prime_review,
        "retrospective": retrospective,
        "source_commit": source_commit if retrospective else None,
        "required": expected,
        "logicals": logicals,
    }
    if state == "complete":
        snapshot = collect_inputs(return_path, root, parsed)
        wanted.update(snapshot)
        if same_capture(info, wanted):
            return Result(
                0,
                f"capture {folder}\nmanifest {info['manifest_sha256']}\n"
                f"receipt {info['receipt_sha256']}\nresult already-captured",
            )
        return Result(
            2,
            f"conflict submission {submission_id}\nexisting {folder}\nresult refused",
        )
    snapshot = collect_inputs(return_path, root, parsed)
    confirm_inputs(return_path, root, parsed, snapshot)
    if interrupt == "before-write":
        refuse("interrupted before-write")
    exclusive_write(member / "return.md", snapshot["return_bytes_data"])
    if interrupt == "after-return":
        return partial_result(folder, member, "interrupted after-return")
    if parsed:
        os.mkdir(member / "payload")
        for index, (relative, logical) in enumerate(parsed, start=1):
            payload_name = f"{index:04d}.blob"
            exclusive_write(member / "payload" / payload_name, snapshot["payload_data"][index - 1])
            del logical
            del relative
    confirm_inputs(return_path, root, parsed, snapshot)
    copied = read_exact(member / "return.md")
    if copied != snapshot["return_bytes_data"]:
        return partial_result(folder, member, "copy mismatch return")
    for index, data in enumerate(snapshot["payload_data"], start=1):
        copied = read_exact(member / "payload" / f"{index:04d}.blob")
        if copied != data:
            return partial_result(folder, member, "copy mismatch payload")
    captured_at = now_stamp()
    sources = []
    for index, logical in enumerate(logicals, start=1):
        data = snapshot["payload_data"][index - 1]
        sources.append(
            {
                "logical": logical,
                "payload": f"{index:04d}.blob",
                "sha256": sha256_bytes(data),
                "bytes": len(data),
            }
        )
    manifest = {
        "schema": SCHEMA,
        "kind": "manifest",
        "submission_id": submission_id,
        "reservation_sha256": sha256_bytes(reservation_bytes),
        "return": {
            "sha256": snapshot["return_sha256"],
            "bytes": snapshot["return_bytes"],
            "includes_prime_review": return_includes_prime_review,
        },
        "retrospective": retrospective,
        "source_commit": source_commit if retrospective else None,
        "captured_at": captured_at,
        "sources": sources,
        "omitted": [],
        "required": expected,
    }
    manifest_bytes = canonical(manifest)
    exclusive_write(member / "manifest.json", manifest_bytes)
    if interrupt == "before-receipt":
        return partial_result(folder, member, "interrupted before-receipt")
    confirm_inputs(return_path, root, parsed, snapshot)
    if read_exact(member / "manifest.json") != manifest_bytes:
        return partial_result(folder, member, "copy mismatch manifest")
    receipt = {
        "schema": SCHEMA,
        "kind": "receipt",
        "submission_id": submission_id,
        "reservation_sha256": sha256_bytes(reservation_bytes),
        "manifest_sha256": sha256_bytes(manifest_bytes),
        "captured_at": captured_at,
    }
    receipt_bytes = canonical(receipt)
    exclusive_write(member / "receipt.json", receipt_bytes)
    if read_exact(member / "receipt.json") != receipt_bytes:
        return partial_result(folder, member, "copy mismatch receipt")
    return Result(
        0,
        f"capture {folder}\nmanifest {sha256_bytes(manifest_bytes)}\n"
        f"receipt {sha256_bytes(receipt_bytes)}\nresult captured",
    )


def collect_inputs(return_path: Path, root: Path, parsed: list[tuple[str, str]]) -> dict:
    if plain_file_problem(return_path) is not None:
        refuse(f"return file is {plain_file_problem(return_path)}")
    return_data = read_stable(return_path)
    payload_data = []
    logicals = []
    hashes = []
    lengths = []
    for relative, logical in parsed:
        path = resolve_source(root, relative)
        problem = plain_file_problem(path)
        if problem:
            refuse(f"{problem}: {relative}")
        data = read_stable(path)
        payload_data.append(data)
        logicals.append(logical)
        hashes.append(sha256_bytes(data))
        lengths.append(len(data))
    return {
        "return_bytes_data": return_data,
        "return_sha256": sha256_bytes(return_data),
        "return_bytes": len(return_data),
        "payload_data": payload_data,
        "logicals": logicals,
        "hashes": hashes,
        "lengths": lengths,
    }


def confirm_inputs(return_path: Path, root: Path, parsed, snapshot: dict) -> None:
    if read_exact(return_path) != snapshot["return_bytes_data"]:
        refuse("bytes changed before capture")
    for index, (relative, _logical) in enumerate(parsed):
        path = resolve_source(root, relative)
        if read_exact(path) != snapshot["payload_data"][index]:
            refuse("bytes changed before capture")


def execute(argv: list[str]) -> Result:
    parser = argparse.ArgumentParser(prog="return_capture.py")
    sub = parser.add_subparsers(dest="command", required=True)

    reserve_parser = sub.add_parser("reserve")
    reserve_parser.add_argument("--book", required=True)
    reserve_parser.add_argument("--submission", required=True)
    reserve_parser.add_argument("--name", required=True)
    reserve_parser.add_argument("--origin-book", required=True)
    reserve_parser.add_argument("--origin-page", required=True)
    reserve_parser.add_argument("--origin-batch", required=True)
    reserve_parser.add_argument("--expected-output", action="append", default=None)
    reserve_parser.add_argument("--submitter", required=True)
    reserve_parser.add_argument("--reviewer", required=True)
    reserve_parser.add_argument("--release", required=True)
    reserve_parser.add_argument("--supersedes", default=None)

    capture_parser = sub.add_parser("capture")
    capture_parser.add_argument("--book", required=True)
    capture_parser.add_argument("--submission", required=True)
    capture_parser.add_argument("--return-file", required=True)
    capture_parser.add_argument("--source-root", required=True)
    capture_parser.add_argument("--artifact", action="append", default=None)
    capture_parser.add_argument("--retrospective", action="store_true")
    capture_parser.add_argument("--source-commit", default=None)
    capture_parser.add_argument("--return-includes-prime-review", action="store_true")

    verify_parser = sub.add_parser("verify")
    verify_parser.add_argument("--book", required=True)
    verify_parser.add_argument("--member", required=True)

    try:
        args = parser.parse_args(argv)
    except SystemExit as exc:
        code = exc.code
        if code is None:
            code = 0
        raise SystemExit(code)
    try:
        if args.command == "reserve":
            return reserve(
                args.book,
                args.submission,
                args.name,
                args.origin_book,
                args.origin_page,
                args.origin_batch,
                list(args.expected_output or []),
                args.submitter,
                args.reviewer,
                args.release,
                args.supersedes,
            )
        if args.command == "capture":
            return capture(
                args.book,
                args.submission,
                args.return_file,
                args.source_root,
                list(args.artifact or []),
                args.retrospective,
                args.source_commit,
                args.return_includes_prime_review,
            )
        return verify(args.book, args.member)
    except Refusal as exc:
        return Result(2, str(exc))
    except OSError as exc:
        return Result(
            2,
            f"filesystem: {type(exc).__name__}: {exc.strerror or exc}\nresult refused",
        )


def main(argv: list[str] | None = None) -> int:
    try:
        result = execute(sys.argv[1:] if argv is None else argv)
    except SystemExit as exc:
        code = exc.code
        return 2 if code is None else int(code)
    sys.stdout.write(result.text)
    return result.code


if __name__ == "__main__":
    sys.exit(main())
