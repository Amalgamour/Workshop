"""N7NN exchange workflow, pass04.

The fact store is investigation.json at schema colab-exchange-investigation/2.
A commit retains the previous investigation.json and seal.json pair, then
publishes the new pair by replacing staged bytes. It does not truncate those
two files in place. Markdown files are projections. Page-local returns keep
the supplied bytes. A later pass opens only from one recorded request-next
review. Attach calls the pinned v2 producer verify. This tool does not call
the standalone checker, prepare a package, reserve a capture, migrate a
pass02 book, recover a partial page, or write the live book.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
import re
import stat
import subprocess
import sys
from pathlib import Path


SCHEMA_NAME = "colab-exchange-result/1"
INVESTIGATION_SCHEMA = "colab-exchange-investigation/2"
LOCAL_RETURN_SCHEMA = "colab-exchange-local-return/1"
OPEN_SCHEMA = "colab-exchange-open/1"
REVIEW_SCHEMA = "colab-exchange-review/1"
SEAL_SCHEMA = "colab-exchange-seal/1"
PARTIAL_SCHEMA = "colab-exchange-partial/1"
CHECKPOINT_SCHEMA = "colab-exchange-checkpoint/1"
PUBLICATION_SCHEMA = "colab-exchange-publication/1"
PUBLISHED_SCHEMA = "colab-exchange-published/1"
ATTEMPT_SCHEMA = "colab-exchange-attempt/1"
PROVENANCE_SCHEMA = "colab-exchange-provenance/1"
DIGEST_ALG = "colab-package-digest/2"
VERIFICATION_SCHEMA = "colab-package-verification/2"
CONFIG_SCHEMA = "colab-config/2"
BINDING_SCHEMA = "colab-binding/1"
MANIFEST_SCHEMA = "prime-pack-sources/1"

PRODUCER_SHA = "2b720434ac4c4331835c1484b0eca362e01e8afbecde0ab800ca392530abf68b"
PRODUCER_LEN = 53892
PRODUCER_V1_SHA = "33bbe41c52485fc7b2b611d830bae8a15129721ad807a931e8193f17944c467c"
PRODUCER_V1_LEN = 67781
ASSEMBLER_SHA = "75d49679cbf3e624a82573229ca8c7cd9b758799bc26b6f080111feb6eaa275c"
ASSEMBLER_LEN = 43928
CHECKER_SHA = "9bbd9d57f3b7da43234ac2e6ae4ce40a0ab6af2f53c8135ecfb2ee0c8a6e322d"
CHECKER_LEN = 21563
CAPTURE_SHA = "8f3da5c651f6924fca6dedb0b95da7d181eb58884dc030dd9cbc3d8b6a5b15ac"
CAPTURE_LEN = 45767
INSPECT_SHA = "947915febaa5918f56b6be03c81840c030d081fcab9a3bead2cd660973a9999b"
INSPECT_LEN = 11402

FILE_ATTRIBUTE_REPARSE_POINT = 0x400
TEXT_LIMIT = 4096
TITLE_LIMIT = 200
PAGE_LIMIT = 80
LIST_LIMIT = 32
TARGET_LIMIT = 32
RETURN_LIMIT = 1048576
TRANSITION_LIMIT = 64
LIVE_BOOK = os.path.normcase(os.path.abspath(r"D:\Git\lib-build\00.kernel\00.00.10.work"))
LIVE_KERNEL = os.path.normcase(os.path.abspath(r"D:\Git\lib-build\00.kernel"))
PAGE_RE = re.compile(r"^[0-9]{4}\.[a-z][a-z0-9-]*$")
HEADING_RE = re.compile(r"^(#{1,6})[ \t]+\S")
PASS_RE = re.compile(r"^05\.[0-9]{2}$")
MEMBER_RE = re.compile(r"^(\d{4})\.([A-Za-z0-9][A-Za-z0-9._-]{0,63})$")
TARGET_RE = re.compile(r"^T[0-9]{2}$")
FINDING_RE = re.compile(r"^F[0-9]{2}$")
ROUTES = ("hold", "finish", "request-next", "route-n5nn")
DISPOSITIONS = ("held", "rejected", "adopted", "answered", "deferred", "escalated")
UNRESOLVED = ("held", "deferred", "escalated")
CONFIG_KEYS = ("schema", "repositories", "python", "assembler", "checker", "helper", "inspector", "producer_v1")
TOOL_PINS = {
    "assembler": (ASSEMBLER_SHA, ASSEMBLER_LEN),
    "checker": (CHECKER_SHA, CHECKER_LEN),
    "helper": (CAPTURE_SHA, CAPTURE_LEN),
    "inspector": (INSPECT_SHA, INSPECT_LEN),
    "producer_v1": (PRODUCER_V1_SHA, PRODUCER_V1_LEN),
}
CUSTODY_LINES = ("result complete", "not approved", "not accepted", "not published")
REVIEW_KEYS = ("schema", "by", "on", "assessment", "findings", "pending_questions", "route", "next_pass")
FINDING_KEYS = (
    "id",
    "consequential",
    "observation",
    "source_binding",
    "disposition",
    "reason",
    "director_reply",
    "pending",
)

TRANSITION_ACTIONS = (
    "open",
    "attach",
    "append-note",
    "place-return",
    "seal-return",
    "review",
    "open-pass",
)
TRANSITION_KEYS = ("action", "facts", "pass", "prev", "seq", "sha256")
FACT_KEYS = {
    "open": {"page", "title", "targets_sha256"},
    "attach": {"package_digest", "pack_sha256", "notes_sha256", "verification_sha256", "zip_sha256"},
    "append-note": {"notes_count", "note_sha256"},
    "place-return": {
        "kind",
        "manifest_sha256",
        "member",
        "origin_batch",
        "origin_book",
        "origin_page",
        "receipt_sha256",
        "return_sha256",
        "return_bytes",
    },
    "seal-return": {"kind", "return_sha256", "return_bytes", "declared_transport", "package_digest"},
    "review": {"route", "next_pass", "review_sha256"},
    "open-pass": {"opened_pass", "requested_by", "review_sha256"},
}
LOCAL_RETURN_KEYS = {
    "schema",
    "kind",
    "return_sha256",
    "return_bytes",
    "declared_transport",
    "package_digest",
    "pass",
}
N1_RETURN_KEYS = {
    "kind",
    "manifest_sha256",
    "member",
    "origin_batch",
    "origin_book",
    "origin_page",
    "receipt_sha256",
    "return_bytes",
    "return_sha256",
}

RUN_PROCESS = None
WRITE_HOOK = None
REPLACE_HOOK = None


class Refuse(Exception):
    def __init__(self, reason: str, wrote: bool = False) -> None:
        super().__init__(reason)
        self.reason = reason
        self.wrote = wrote


class Usage(Exception):
    pass


def refuse(reason: str, wrote: bool = False) -> None:
    raise Refuse(reason, wrote)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical(value) -> bytes:
    try:
        text = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)
    except (TypeError, ValueError):
        refuse("malformed json")
    return (text + "\n").encode("utf-8")


def parse_json(data: bytes):
    if data.startswith(b"\xef\xbb\xbf"):
        refuse("malformed json")

    def pairs(items):
        out = {}
        for key, value in items:
            if key in out:
                refuse("duplicate key")
            out[key] = value
        return out

    def constant(_name):
        refuse("malformed json")

    try:
        return json.loads(data.decode("utf-8"), object_pairs_hook=pairs, parse_constant=constant)
    except Refuse:
        raise
    except (UnicodeError, json.JSONDecodeError):
        refuse("malformed json")


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def producer_path() -> Path:
    return repo_root() / "labs/colab-support-pass02/colab_support.py"


def is_reparse(path: Path) -> bool:
    info = os.lstat(path)
    attrs = getattr(info, "st_file_attributes", 0) or 0
    return bool(attrs & FILE_ATTRIBUTE_REPARSE_POINT or stat.S_ISLNK(info.st_mode))


def plain_problem(path: Path, kind: str) -> str | None:
    if not os.path.lexists(path):
        return "missing"
    try:
        info = os.lstat(path)
    except OSError as exc:
        return f"filesystem: {type(exc).__name__}: {exc.strerror or exc}"
    if is_reparse(path):
        return "link"
    if kind == "dir" and not stat.S_ISDIR(info.st_mode):
        return "not-directory"
    if kind == "file" and not stat.S_ISREG(info.st_mode):
        return "not-file"
    if kind == "file" and info.st_nlink != 1:
        return "link"
    return None


def refuse_chain(path: Path) -> None:
    if not path.is_absolute():
        refuse("unsafe path")
    current = Path(path.anchor)
    for part in path.parts[1:]:
        if part in ("", ".", ".."):
            refuse("unsafe path")
        current = current / part
        if not os.path.lexists(current):
            return
        if is_reparse(current):
            refuse("unsafe path")


def norm(path: Path) -> str:
    return os.path.normcase(os.path.abspath(path))


def within(child: Path, parent: Path) -> bool:
    try:
        return os.path.commonpath([norm(child), norm(parent)]) == norm(parent)
    except ValueError:
        return False


def refuse_live(path: Path) -> None:
    here = norm(path)
    if here == LIVE_BOOK or here == LIVE_KERNEL or here.startswith(LIVE_KERNEL + os.sep):
        refuse("live work book is not a fixture")


def require_book(text: str) -> Path:
    if not isinstance(text, str) or text == "":
        refuse("book path is not absolute")
    path = Path(text)
    if not path.is_absolute():
        refuse("book path is not absolute")
    refuse_live(path)
    refuse_chain(path)
    problem = plain_problem(path, "dir")
    if problem:
        refuse("unsafe path" if problem == "link" else "book is missing")
    return path


def require_input_dir(text: str, label: str) -> Path:
    if not isinstance(text, str) or text == "":
        refuse(f"{label} path is not absolute")
    path = Path(text)
    if not path.is_absolute():
        refuse(f"{label} path is not absolute")
    refuse_chain(path)
    problem = plain_problem(path, "dir")
    if problem:
        refuse("unsafe path" if problem == "link" else f"{label} is missing")
    return path


def require_input_file(text: str, label: str) -> Path:
    if not isinstance(text, str) or text == "":
        refuse(f"{label} path is not absolute")
    path = Path(text)
    if not path.is_absolute():
        refuse(f"{label} path is not absolute")
    refuse_chain(path)
    problem = plain_problem(path, "file")
    if problem:
        refuse("unsafe path" if problem == "link" else f"{label} is missing")
    return path


def source_parts(text: str) -> list[str]:
    if not isinstance(text, str) or text == "" or "\\" in text or text.startswith("/"):
        refuse("unsafe path")
    parts = text.split("/")
    if any(part in ("", ".", "..") for part in parts):
        refuse("unsafe path")
    return parts


def emitted_parts(text: str) -> list[str]:
    parts = source_parts(text)
    for part in parts:
        if part.endswith(".colab"):
            refuse("colab tail")
        if part == "07.md":
            refuse("face 07")
    return parts


def write_bytes(path: Path, data: bytes) -> None:
    if WRITE_HOOK is not None:
        WRITE_HOOK(path, data)
    path.parent.mkdir(parents=True, exist_ok=True)
    if os.path.lexists(path) and is_reparse(path):
        refuse("unsafe path")
    flags = os.O_WRONLY | os.O_CREAT | os.O_TRUNC
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


def write_marker(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    flags = os.O_WRONLY | os.O_CREAT | os.O_TRUNC
    if hasattr(os, "O_BINARY"):
        flags |= os.O_BINARY
    fd = os.open(str(path), flags)
    try:
        os.write(fd, data)
    finally:
        os.close(fd)


def run_process(argv: list[str]) -> tuple[int, bytes, bytes]:
    if RUN_PROCESS is not None:
        return RUN_PROCESS(argv)
    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    proc = subprocess.run([sys.executable, "-B", *argv], capture_output=True, env=env, shell=False)
    return proc.returncode, proc.stdout, proc.stderr


def result(command: str, name: str, wrote: bool, **extra) -> dict:
    body = {"command": command, "reason": None, "result": name, "schema": SCHEMA_NAME, "wrote": wrote}
    body.update(extra)
    return body


def one_line(value, label: str) -> str:
    if not isinstance(value, str) or value == "" or len(value) > TEXT_LIMIT:
        refuse(f"malformed {label}")
    if any(ord(ch) < 32 for ch in value):
        refuse(f"malformed {label}")
    return value


def require_pass(value: str) -> str:
    if not isinstance(value, str) or PASS_RE.fullmatch(value) is None:
        refuse("malformed pass")
    return value


def require_page(value: str) -> str:
    if not isinstance(value, str) or len(value) > PAGE_LIMIT or PAGE_RE.fullmatch(value) is None:
        refuse("malformed page")
    number = int(value[:4])
    if number < 701 or number > 799:
        refuse("outside declared band")
    return value


def page_dir(book: Path, page: str) -> Path:
    require_page(page)
    dest = book / page
    if not within(dest, book):
        refuse("unsafe path")
    return dest


def pass_nn(pass_id: str) -> str:
    return pass_id.split(".")[1]


def pack_name(pass_id: str) -> str:
    return f"05.{pass_nn(pass_id)}.pack.md"


def notes_name(pass_id: str) -> str:
    return f"06.{pass_nn(pass_id)}.notes.md"


def return_name(pass_id: str) -> str:
    return f"05.{pass_nn(pass_id)}.return.md"


def review_name(pass_id: str) -> str:
    return f"06.{pass_nn(pass_id)}.review.md"


def pin_file(path: Path, digest: str, length: int) -> None:
    problem = plain_problem(path, "file")
    if problem:
        refuse("pin mismatch")
    data = path.read_bytes()
    if sha256(data) != digest or len(data) != length:
        refuse("pin mismatch")


def load_config(path: Path) -> dict:
    body = parse_json(path.read_bytes())
    if not isinstance(body, dict) or body.get("schema") != CONFIG_SCHEMA or set(body) != set(CONFIG_KEYS):
        refuse("unknown schema")
    for key in ("assembler", "checker", "helper", "inspector", "producer_v1"):
        pin_file(require_input_file(body[key], key), *TOOL_PINS[key])
    return body


def heading_matches(data: bytes, wanted: str) -> list[str]:
    try:
        text = data.decode("utf-8")
    except UnicodeError:
        refuse("unresolved section")
    fenced = False
    matches = []
    for line in text.split("\n"):
        if line.endswith("\r"):
            line = line[:-1]
        probe = line.lstrip(" ")
        if probe.startswith("```") or probe.startswith("~~~"):
            fenced = not fenced
            continue
        if fenced:
            continue
        if line == wanted and HEADING_RE.match(line):
            matches.append(line)
    return matches


def resolve_section(data: bytes, section) -> None:
    if section is None:
        return
    if isinstance(section, dict) and section.get("kind") == "id":
        refuse("unsupported section id")
    if not isinstance(section, dict) or set(section) != {"kind", "occurrence", "value"}:
        refuse("malformed section")
    if section["kind"] != "heading" or not isinstance(section["value"], str):
        refuse("malformed section")
    matches = heading_matches(data, section["value"])
    occurrence = section["occurrence"]
    if occurrence is None:
        if len(matches) != 1:
            refuse("ambiguous section" if matches else "unresolved section")
        return
    if isinstance(occurrence, bool) or not isinstance(occurrence, int) or occurrence < 1:
        refuse("malformed section")
    if occurrence > len(matches):
        refuse("unresolved section")


def require_target(target: dict, ids: set[str]) -> None:
    if not isinstance(target, dict):
        refuse("malformed target")
    if set(target) != {"book", "file", "id", "page", "section", "source"}:
        refuse("malformed target")
    if not isinstance(target["id"], str) or TARGET_RE.fullmatch(target["id"]) is None or target["id"] in ids:
        refuse("malformed target")
    ids.add(target["id"])
    one_line(target["book"], "target book")
    one_line(target["page"], "target page")
    one_line(target["file"], "target file")
    source = target["source"]
    if not isinstance(source, dict) or set(source) != {"commit", "path", "repository", "sha256"}:
        refuse("malformed target")
    one_line(source["path"], "source path")
    source_parts(source["path"])
    if not isinstance(source["sha256"], str) or len(source["sha256"]) != 64:
        refuse("malformed target")
    one_line(source["repository"], "repository")
    one_line(source["commit"], "commit")
    if isinstance(target.get("section"), dict) and target["section"].get("kind") == "id":
        refuse("unsupported section id")


def require_open_request(body: dict) -> dict:
    if not isinstance(body, dict) or body.get("schema") != OPEN_SCHEMA:
        refuse("unknown schema")
    if set(body) != {"book", "page", "pass", "schema", "targets", "title"}:
        refuse("malformed request")
    one_line(body["book"], "book")
    if "/" in body["book"] or "\\" in body["book"]:
        refuse("malformed book")
    require_page(body["page"])
    require_pass(body["pass"])
    title = one_line(body["title"], "title")
    if len(title) > TITLE_LIMIT:
        refuse("malformed title")
    targets = body["targets"]
    if not isinstance(targets, list) or not targets or len(targets) > TARGET_LIMIT:
        refuse("malformed target")
    ids: set[str] = set()
    for target in targets:
        require_target(target, ids)
        if isinstance(target.get("section"), dict) and target["section"].get("kind") == "id":
            refuse("unsupported section id")
    return body


def read_source_bytes(root: Path, relative: str) -> bytes:
    dest = root
    for part in source_parts(relative):
        dest = dest / part
    if not within(dest, root):
        refuse("unsafe path")
    problem = plain_problem(dest, "file")
    if problem:
        refuse("unsafe path" if problem == "link" else "missing file")
    return dest.read_bytes()


def walk_refuse_links(root: Path) -> None:
    for dirpath, dirnames, filenames in os.walk(root):
        current = Path(dirpath)
        if current != root and is_reparse(current):
            refuse("unsafe path")
        for name in dirnames + filenames:
            path = current / name
            if os.path.lexists(path) and is_reparse(path):
                refuse("unsafe path")


def binding_matches(request: dict, binding: dict) -> None:
    if not isinstance(binding, dict) or binding.get("schema") != BINDING_SCHEMA:
        refuse("unknown schema")
    investigation = binding.get("investigation")
    if investigation != {"book": request["book"], "page": request["page"], "pass": request["pass"]}:
        refuse("wrong origin")
    if canonical(binding.get("targets")) != canonical(request["targets"]):
        refuse("wrong origin")


def load_closure(request: dict, output: Path) -> None:
    package = output / "package"
    binding = parse_json(read_source_bytes(package, "binding.json"))
    binding_matches(request, binding)
    manifest = parse_json(read_source_bytes(package, "source-manifest.json"))
    if not isinstance(manifest, dict) or manifest.get("schema") != MANIFEST_SCHEMA:
        refuse("unknown schema")
    rows = manifest.get("sources")
    if not isinstance(rows, list):
        refuse("malformed package")
    by_path = {}
    for row in rows:
        if not isinstance(row, dict):
            refuse("malformed package")
        by_path[row.get("path")] = row
    for target in request["targets"]:
        row = by_path.get(target["source"]["path"])
        if not isinstance(row, dict):
            refuse("hash conflict")
        snapshot = row.get("snapshot")
        if not isinstance(snapshot, str):
            refuse("malformed package")
        data = read_source_bytes(package, snapshot)
        digest = sha256(data)
        if digest != row.get("sha256") or len(data) != row.get("bytes") or digest != target["source"]["sha256"]:
            refuse("hash conflict")
        resolve_section(data, target["section"])


def load_sources(request: dict, sources: Path) -> None:
    for target in request["targets"]:
        data = read_source_bytes(sources, target["source"]["path"])
        if sha256(data) != target["source"]["sha256"]:
            refuse("hash conflict")
        resolve_section(data, target["section"])


def empty_slot() -> dict:
    return {"notes": [], "package": None, "return": None, "review": None}


def pass_number(pass_id: str) -> int:
    return int(pass_id.split(".")[1])


def transition_core(item: dict) -> dict:
    return {key: item[key] for key in ("action", "facts", "pass", "prev", "seq")}


def transition_digest(core: dict) -> str:
    return sha256(canonical(core))


def make_transition(previous: list, action: str, pass_id: str, facts: dict) -> dict:
    core = {
        "action": action,
        "facts": facts,
        "pass": pass_id,
        "prev": None if not previous else previous[-1]["sha256"],
        "seq": len(previous) + 1,
    }
    core["sha256"] = transition_digest(core)
    return core


def append_transition(record: dict, action: str, pass_id: str, facts: dict) -> dict:
    updated = copy.deepcopy(record)
    new = make_transition(updated["transitions"], action, pass_id, facts)
    updated["transitions"] = [*updated["transitions"], new]
    if updated["transitions"][:-1] != record["transitions"]:
        refuse("hash conflict")
    check_chain(updated)
    return updated


def fresh_record(request: dict) -> dict:
    record = {
        "book": request["book"],
        "page": request["page"],
        "passes": {request["pass"]: empty_slot()},
        "schema": INVESTIGATION_SCHEMA,
        "targets": request["targets"],
        "title": request["title"],
        "transitions": [],
    }
    facts = {
        "page": request["page"],
        "targets_sha256": sha256(canonical(request["targets"])),
        "title": request["title"],
    }
    record["transitions"] = [make_transition([], "open", request["pass"], facts)]
    return record


def read_plain(path: Path) -> bytes:
    problem = plain_problem(path, "file")
    if problem == "link":
        refuse("unsafe path")
    if problem:
        refuse("hash conflict")
    return path.read_bytes()


def expect_bytes(path: Path, data: bytes) -> None:
    if read_plain(path) != data:
        refuse("hash conflict")


def absent(path: Path) -> None:
    if os.path.lexists(path):
        refuse("hash conflict")


def check_chain(record: dict) -> None:
    rows = record.get("transitions")
    passes = record.get("passes")
    if not isinstance(rows, list) or not isinstance(passes, dict):
        refuse("hash conflict")
    if len(rows) > TRANSITION_LIMIT:
        refuse("declared limit")
    for index, item in enumerate(rows):
        if not isinstance(item, dict) or set(item) != set(TRANSITION_KEYS):
            refuse("hash conflict")
        if item["action"] not in TRANSITION_ACTIONS or not isinstance(item["facts"], dict):
            refuse("hash conflict")
        if set(item["facts"]) != FACT_KEYS[item["action"]]:
            refuse("hash conflict")
        if item["seq"] != index + 1 or not isinstance(item["pass"], str) or PASS_RE.fullmatch(item["pass"]) is None:
            refuse("hash conflict")
        expected_prev = None if index == 0 else rows[index - 1]["sha256"]
        if item["prev"] != expected_prev or item["sha256"] != transition_digest(transition_core(item)):
            refuse("hash conflict")
    if not rows or rows[0]["action"] != "open":
        refuse("hash conflict")
    opened = rows[0]
    if opened["facts"]["page"] != record.get("page") or opened["facts"]["title"] != record.get("title"):
        refuse("hash conflict")
    if opened["facts"]["targets_sha256"] != sha256(canonical(record.get("targets"))):
        refuse("hash conflict")
    introduced: dict[str, str] = {}
    for item in rows:
        if item["action"] == "open":
            if item["seq"] != 1 or item["pass"] in introduced:
                refuse("hash conflict")
            introduced[item["pass"]] = "open"
        elif item["action"] == "open-pass":
            named = item["facts"]["opened_pass"]
            if named != item["pass"] or named in introduced:
                refuse("hash conflict")
            introduced[named] = "open-pass"
    if set(introduced) != set(passes):
        refuse("hash conflict")
    for pass_id, slot in passes.items():
        if not isinstance(slot, dict) or set(slot) != {"notes", "package", "return", "review"}:
            refuse("hash conflict")
        if not isinstance(slot["notes"], list):
            refuse("hash conflict")
        mine = [item for item in rows if item["pass"] == pass_id]
        creators = [item for item in mine if item["action"] in ("open", "open-pass")]
        attaches = [item for item in mine if item["action"] == "attach"]
        notes = [item for item in mine if item["action"] == "append-note"]
        returns = [item for item in mine if item["action"] in ("seal-return", "place-return")]
        reviews = [item for item in mine if item["action"] == "review"]
        if len(creators) != 1:
            refuse("hash conflict")
        package = slot["package"]
        if package is None:
            if attaches or notes or slot["notes"]:
                refuse("hash conflict")
        else:
            if not isinstance(package, dict) or not attaches:
                refuse("hash conflict")
            last = attaches[-1]["facts"]
            if last["package_digest"] != package.get("digest") or last["pack_sha256"] != package.get("pack_sha256"):
                refuse("hash conflict")
            if last["notes_sha256"] != package.get("notes_sha256") or last["verification_sha256"] != package.get("verification_sha256"):
                refuse("hash conflict")
            if last["zip_sha256"] != package.get("zip_sha256"):
                refuse("hash conflict")
        if len(notes) != len(slot["notes"]):
            refuse("hash conflict")
        for index, (item, line) in enumerate(zip(notes, slot["notes"]), start=1):
            if not isinstance(line, str) or item["facts"]["notes_count"] != index:
                refuse("hash conflict")
            if item["facts"]["note_sha256"] != sha256(line.encode("utf-8")):
                refuse("hash conflict")
        placed = slot["return"]
        if placed is None:
            if returns:
                refuse("hash conflict")
        else:
            if package is None or len(returns) != 1 or not isinstance(placed, dict):
                refuse("hash conflict")
            facts = returns[0]["facts"]
            if returns[0]["action"] == "seal-return":
                if set(placed) != LOCAL_RETURN_KEYS or placed["kind"] != "page-local" or placed["schema"] != LOCAL_RETURN_SCHEMA:
                    refuse("hash conflict")
                if placed["pass"] != pass_id or facts["kind"] != "page-local":
                    refuse("hash conflict")
                for key in ("return_sha256", "return_bytes", "declared_transport", "package_digest"):
                    if facts[key] != placed[key]:
                        refuse("hash conflict")
            else:
                if set(placed) != N1_RETURN_KEYS or placed["kind"] != "n1nn" or facts["kind"] != "n1nn":
                    refuse("hash conflict")
                for key in (
                    "manifest_sha256",
                    "member",
                    "origin_batch",
                    "origin_book",
                    "origin_page",
                    "receipt_sha256",
                    "return_sha256",
                    "return_bytes",
                ):
                    if facts[key] != placed[key]:
                        refuse("hash conflict")
        review = slot["review"]
        if review is None:
            if reviews:
                refuse("hash conflict")
        else:
            if placed is None or len(reviews) != 1 or not isinstance(review, dict):
                refuse("hash conflict")
            facts = reviews[0]["facts"]
            if facts["route"] != review.get("route") or facts["next_pass"] != review.get("next_pass"):
                refuse("hash conflict")
            if facts["review_sha256"] != sha256(canonical(review)):
                refuse("hash conflict")
    for item in rows:
        if item["action"] != "open-pass":
            continue
        facts = item["facts"]
        requester = facts["requested_by"]
        if requester not in passes or pass_number(facts["opened_pass"]) <= pass_number(requester):
            refuse("hash conflict")
        req = passes[requester]
        review = req["review"]
        ret = req["return"]
        if req["package"] is None or not isinstance(review, dict) or not isinstance(ret, dict):
            refuse("hash conflict")
        if review.get("route") != "request-next" or review.get("next_pass") != facts["opened_pass"]:
            refuse("hash conflict")
        if facts["review_sha256"] != sha256(canonical(review)) or ret.get("kind") != "page-local":
            refuse("hash conflict")


def check_files(page: Path, record: dict) -> None:
    expect_bytes(page / "01.md", render_face(record))
    expect_bytes(page / "08.md", render_pointer(record))
    for pass_id, slot in record["passes"].items():
        package = slot["package"]
        artifact = page / "artifacts" / pass_id
        if package is None:
            absent(page / pack_name(pass_id))
            absent(page / notes_name(pass_id))
        else:
            pack = read_plain(artifact / "package" / pack_name(pass_id))
            notes = read_plain(artifact / "package" / notes_name(pass_id))
            if sha256(pack) != package["pack_sha256"] or sha256(notes) != package["notes_sha256"]:
                refuse("hash conflict")
            expect_bytes(page / pack_name(pass_id), pack)
            expect_bytes(page / notes_name(pass_id), project_notes(pass_id, notes, slot["notes"]))
            if sha256(read_plain(artifact / "prepared-colab.zip")) != package["zip_sha256"]:
                refuse("hash conflict")
            if sha256(read_plain(artifact / "verification.json")) != package["verification_sha256"]:
                refuse("hash conflict")
        placed = slot["return"]
        if placed is None:
            absent(page / return_name(pass_id))
            absent(artifact / "return.md")
        else:
            data = read_plain(artifact / "return.md")
            if sha256(data) != placed["return_sha256"] or len(data) != placed["return_bytes"]:
                refuse("hash conflict")
            expect_bytes(page / return_name(pass_id), data)
        if slot["review"] is None:
            absent(page / review_name(pass_id))
        else:
            expect_bytes(page / review_name(pass_id), render_review(pass_id, slot["review"]))


def require_loaded(page: Path) -> dict:
    if (page / "partial.json").exists() or (page / ".write.lock").exists() or (page / "attempt.json").exists():
        refuse("resume refused")
    inv = page / "investigation.json"
    seal = page / "seal.json"
    if plain_problem(inv, "file") or plain_problem(seal, "file"):
        refuse("resume refused")
    data = inv.read_bytes()
    body = parse_json(seal.read_bytes())
    if not isinstance(body, dict) or body.get("schema") != SEAL_SCHEMA or body.get("sha256") != sha256(data):
        refuse("resume refused")
    record = parse_json(data)
    if not isinstance(record, dict) or record.get("schema") != INVESTIGATION_SCHEMA:
        refuse("unknown schema")
    check_chain(record)
    check_files(page, record)
    return record


def open_pass_decision(record: dict, pass_id: str) -> tuple[str, dict | None]:
    requests = []
    for pid in sorted(record["passes"]):
        review = record["passes"][pid]["review"]
        if review and review["route"] == "request-next" and review["next_pass"] == pass_id:
            requests.append(pid)
    if len(requests) == 0:
        return "next pass not requested", None
    if len(requests) > 1:
        return "conflicting requests", None
    requester = requests[0]
    if pass_number(pass_id) <= pass_number(requester):
        return "earlier pass", None
    req = record["passes"][requester]
    if req["package"] is None:
        return "missing investigation", None
    placed = req["return"]
    if placed is None:
        return "sealed return missing", None
    if placed.get("kind") != "page-local" or placed.get("schema") != LOCAL_RETURN_SCHEMA:
        return "local return required", None
    review_sha = sha256(canonical(req["review"]))
    info = {"requested_by": requester, "review_sha256": review_sha}
    slot = record["passes"].get(pass_id)
    if slot is None:
        return "create", info
    creators = [
        item
        for item in record["transitions"]
        if item["action"] == "open-pass" and item["facts"].get("opened_pass") == pass_id
    ]
    opens = [item for item in record["transitions"] if item["action"] == "open" and item["pass"] == pass_id]
    if (
        len(creators) == 1
        and creators[0]["facts"].get("requested_by") == requester
        and creators[0]["facts"].get("review_sha256") == review_sha
    ):
        return "repeat", info
    if opens and not creators:
        return "occupied pass", None
    return "occupied different state", None


def projections(page: Path, record: dict) -> list[tuple[str, bytes]]:
    files = []
    files.append(("01.md", render_face(record)))
    files.append(("08.md", render_pointer(record)))
    for pass_id, slot in sorted(record["passes"].items()):
        emitted_parts(pack_name(pass_id))
        emitted_parts(notes_name(pass_id))
        emitted_parts(return_name(pass_id))
        emitted_parts(review_name(pass_id))
        package = slot["package"]
        if package is not None:
            snapshot = (page / "artifacts" / pass_id / "package" / notes_name(pass_id)).read_bytes()
            pack = (page / "artifacts" / pass_id / "package" / pack_name(pass_id)).read_bytes()
            if sha256(snapshot) != package["notes_sha256"] or sha256(pack) != package["pack_sha256"]:
                refuse("hash conflict")
            files.append((pack_name(pass_id), pack))
            files.append((notes_name(pass_id), project_notes(pass_id, snapshot, slot["notes"])))
        if slot["return"] is not None:
            stored = (page / "artifacts" / pass_id / "return.md").read_bytes()
            if sha256(stored) != slot["return"]["return_sha256"] or len(stored) != slot["return"]["return_bytes"]:
                refuse("hash conflict")
            files.append((return_name(pass_id), stored))
        if slot["review"] is not None:
            files.append((review_name(pass_id), render_review(pass_id, slot["review"])))
    for rel, _data in files:
        emitted_parts(rel)
    return files


def write_new(path: Path, data: bytes, occupied: str) -> None:
    if WRITE_HOOK is not None:
        WRITE_HOOK(path, data)
    path.parent.mkdir(parents=True, exist_ok=True)
    if os.path.lexists(path):
        if is_reparse(path):
            refuse("unsafe path")
        refuse(occupied)
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
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


def publish_replace(src: Path, dest: Path) -> None:
    if os.path.lexists(dest) and is_reparse(dest):
        refuse("unsafe path")
    refuse_chain(dest)
    if REPLACE_HOOK is not None:
        REPLACE_HOOK(src, dest)
    os.replace(str(src), str(dest))


def prior_pair(page: Path) -> tuple[str, str | None, bytes | None, bytes | None]:
    inv_path = page / "investigation.json"
    seal_path = page / "seal.json"
    inv_exists = os.path.lexists(inv_path)
    seal_exists = os.path.lexists(seal_path)
    if not inv_exists and not seal_exists:
        return "none", None, None, None
    if not inv_exists or not seal_exists:
        refuse("resume refused")
    if is_reparse(inv_path) or is_reparse(seal_path):
        refuse("unsafe path")
    inv_bytes = inv_path.read_bytes()
    seal_bytes = seal_path.read_bytes()
    body = parse_json(seal_bytes)
    if not isinstance(body, dict) or body.get("schema") != SEAL_SCHEMA or body.get("sha256") != sha256(inv_bytes):
        refuse("resume refused")
    return "retained-prior", sha256(inv_bytes), inv_bytes, seal_bytes


def retain_prior(page: Path, checkpoint_id: str, inv_bytes: bytes, seal_bytes: bytes, publication_id: str) -> None:
    dest = page / "checkpoints" / checkpoint_id
    if os.path.lexists(dest):
        refuse("checkpoint collision")
    refuse_chain(dest / "investigation.json")
    identity = canonical(
        {
            "checkpoint_id": checkpoint_id,
            "investigation_bytes": len(inv_bytes),
            "investigation_sha256": checkpoint_id,
            "publication_id": publication_id,
            "role": "retained-prior",
            "schema": CHECKPOINT_SCHEMA,
            "seal_sha256": checkpoint_id,
        }
    )
    write_new(dest / "investigation.json", inv_bytes, "checkpoint collision")
    write_new(dest / "seal.json", seal_bytes, "checkpoint collision")
    write_new(dest / "identity.json", identity, "checkpoint collision")
    if (dest / "investigation.json").read_bytes() != inv_bytes or (dest / "seal.json").read_bytes() != seal_bytes:
        raise OSError("checkpoint mismatch")


def commit(page: Path, record: dict, extra: list[tuple[str, bytes]] | None = None) -> None:
    inv = canonical(record)
    publication_id = sha256(inv)
    seal_file = canonical({"schema": SEAL_SCHEMA, "sha256": publication_id})
    predecessor, checkpoint_id, prior_inv, prior_seal = prior_pair(page)
    if (page / "partial.json").exists() or (page / "attempt.json").exists() or (page / ".write.lock").exists():
        refuse("resume refused")
    publication_path = page / "publications" / f"{publication_id}.json"
    published_path = page / "publications" / f"{publication_id}.published"
    if os.path.lexists(publication_path) or os.path.lexists(published_path):
        if (os.path.lexists(publication_path) and is_reparse(publication_path)) or (
            os.path.lexists(published_path) and is_reparse(published_path)
        ):
            refuse("unsafe path")
        refuse("publication collision")
    publication = canonical(
        {
            "candidate_investigation_bytes": len(inv),
            "candidate_investigation_sha256": publication_id,
            "candidate_seal_sha256": sha256(seal_file),
            "predecessor": predecessor,
            "publication_id": publication_id,
            "retained_checkpoint": checkpoint_id,
            "schema": PUBLICATION_SCHEMA,
        }
    )
    attempt = canonical(
        {
            "predecessor": predecessor,
            "publication_id": publication_id,
            "retained_checkpoint": checkpoint_id,
            "schema": ATTEMPT_SCHEMA,
        }
    )
    published = canonical(
        {
            "predecessor": predecessor,
            "publication_id": publication_id,
            "retained_checkpoint": checkpoint_id,
            "schema": PUBLISHED_SCHEMA,
        }
    )
    partial_body = canonical(
        {
            "predecessor": predecessor,
            "publication_id": publication_id,
            "reason": "interrupted write",
            "retained_checkpoint": checkpoint_id,
            "schema": PARTIAL_SCHEMA,
        }
    )
    lock = page / ".write.lock"
    stage = page / "staging" / publication_id
    try:
        write_marker(lock, b"1\n")
        if predecessor == "retained-prior":
            retain_prior(page, checkpoint_id, prior_inv, prior_seal, publication_id)
        write_new(page / "publications" / f"{publication_id}.json", publication, "publication collision")
        write_new(page / "attempt.json", attempt, "resume refused")
        for rel, data in extra or []:
            emitted_parts(rel.split("/")[-1]) if not rel.startswith("artifacts/") else None
            write_bytes(page.joinpath(*rel.split("/")), data)
        for rel, data in projections(page, record):
            src = stage / "projections" / rel
            write_new(src, data, "occupied staging")
            if src.read_bytes() != data:
                raise OSError("staged projection mismatch")
            publish_replace(src, page.joinpath(*rel.split("/")))
        staged_inv = stage / "investigation.json"
        staged_seal = stage / "seal.json"
        write_new(staged_inv, inv, "occupied staging")
        write_new(staged_seal, seal_file, "occupied staging")
        if staged_inv.read_bytes() != inv or staged_seal.read_bytes() != seal_file:
            raise OSError("staged record mismatch")
        publish_replace(staged_inv, page / "investigation.json")
        publish_replace(staged_seal, page / "seal.json")
        if (page / "investigation.json").read_bytes() != inv or (page / "seal.json").read_bytes() != seal_file:
            raise OSError("published record mismatch")
        write_new(page / "publications" / f"{publication_id}.published", published, "publication collision")
        attempt_path = page / "attempt.json"
        if attempt_path.exists() and not is_reparse(attempt_path):
            os.remove(attempt_path)
        partial = page / "partial.json"
        if partial.exists() and not is_reparse(partial):
            os.remove(partial)
    except Refuse:
        raise
    except Exception as exc:
        write_marker(page / "partial.json", partial_body)
        raise Refuse("interrupted write", True) from exc
    finally:
        if lock.exists() and not is_reparse(lock):
            os.remove(lock)


def render_face(record: dict) -> bytes:
    lines = [
        f"# {record['page']}",
        "",
        f"schema: {OPEN_SCHEMA}",
        f"passes: {' '.join(sorted(record['passes']))}",
        f"title: {record['title']}",
        "Return and review are not created by open.",
        "",
    ]
    return "\n".join(lines).encode("utf-8")


def render_pointer(record: dict) -> bytes:
    lines = ["# 08 — Return pointer", ""]
    for pass_id, slot in sorted(record["passes"].items()):
        placed = slot["return"]
        if placed is None:
            lines.append(f"{pass_id}: no return is placed.")
        elif placed.get("kind") == "page-local":
            lines.append(
                f"{pass_id}: page-local return {placed['return_sha256']}. bytes {placed['return_bytes']}. "
                f"transport {placed['declared_transport']}. package {placed['package_digest']}. "
                f"file {return_name(pass_id)}."
            )
        else:
            lines.append(
                f"{pass_id}: member {placed['member']}. receipt {placed['receipt_sha256']}. "
                f"return {placed['return_sha256']}. bytes {placed['return_bytes']}. file {return_name(pass_id)}."
            )
    lines.append("")
    return "\n".join(lines).encode("utf-8")


def project_notes(pass_id: str, snapshot: bytes, notes: list[str]) -> bytes:
    header = (
        f"# {notes_name(pass_id)}\n\n"
        "role: working projection\n"
        f"pass: {pass_id}\n"
        f"launch-sha256: {sha256(snapshot)}\n"
        f"launch-bytes: {len(snapshot)}\n\n"
    ).encode("utf-8")
    rows = ["## Working appends", f"count: {len(notes)}"]
    rows.extend(f"{index}. {line}" for index, line in enumerate(notes, start=1))
    return header + snapshot + ("\n" + "\n".join(rows) + "\n").encode("utf-8")


def launch_slice(data: bytes) -> bytes:
    length = None
    start = 0
    scanned = 0
    while scanned < 8192:
        end = data.find(b"\n", start)
        if end < 0:
            refuse("malformed notes")
        line = data[start:end]
        scanned = end
        if line.startswith(b"launch-bytes: "):
            raw = line.split(b": ", 1)[1]
            if not raw.isdigit():
                refuse("malformed notes")
            length = int(raw.decode("ascii"))
        if line == b"" and length is not None:
            body = end + 1
            return data[body : body + length]
        start = end + 1
    refuse("malformed notes")


def render_review(pass_id: str, review: dict) -> bytes:
    lines = [
        f"# {review_name(pass_id)}",
        "",
        f"schema: {REVIEW_SCHEMA}",
        f"by: {review['by']}",
        f"on: {review['on']}",
        f"route: {review['route']}",
        f"next_pass: {review['next_pass'] if review['next_pass'] else 'none'}",
        "This file is derived from the supplied review record. It is not the return. A route is not approval.",
        "",
        "## Prime assessment",
        review["assessment"],
        "",
        "## Findings",
    ]
    unresolved = []
    for finding in review["findings"]:
        lines.extend(
            [
                f"### {finding['id']}",
                f"consequential: {str(finding['consequential']).lower()}",
                f"source_binding: {finding['source_binding']}",
                f"disposition: {finding['disposition']}",
                f"pending: {str(finding['pending']).lower()}",
                f"observation: {finding['observation']}",
                f"reason: {finding['reason']}",
                f"director_reply: {finding['director_reply']}",
                "",
            ]
        )
        if finding["pending"] or finding["disposition"] in UNRESOLVED:
            unresolved.append(f"{finding['id']} {finding['disposition']}")
    lines.append("## Unresolved")
    lines.extend(unresolved or ["none"])
    lines.extend(["", "## Pending questions"])
    lines.extend(review["pending_questions"] or ["none"])
    lines.extend(
        [
            "",
            "## Route",
            review["route"],
            "A next pack is not created by this file.",
            "",
        ]
    )
    return "\n".join(lines).encode("utf-8")


def command_seal_return(book: Path, page_name: str, pass_id: str, return_file: Path, transport: str) -> dict:
    require_pass(pass_id)
    label = one_line(transport, "declared transport")
    page = page_dir(book, page_name)
    record = require_loaded(page)
    slot = record["passes"].get(pass_id)
    if slot is None or slot["package"] is None:
        refuse("missing investigation")
    info = os.lstat(return_file)
    if info.st_size > RETURN_LIMIT:
        refuse("declared limit")
    data = return_file.read_bytes()
    if len(data) > RETURN_LIMIT:
        refuse("declared limit")
    digest = sha256(data)
    local = {
        "declared_transport": label,
        "kind": "page-local",
        "package_digest": slot["package"]["digest"],
        "pass": pass_id,
        "return_bytes": len(data),
        "return_sha256": digest,
        "schema": LOCAL_RETURN_SCHEMA,
    }
    current = slot["return"]
    if current is not None:
        if current == local:
            stored = page / "artifacts" / pass_id / "return.md"
            projected = page / return_name(pass_id)
            if read_plain(stored) == data and read_plain(projected) == data:
                return result("seal-return-local", "repeat", False, return_sha256=digest)
            refuse("hash conflict")
        same_bytes = (
            current.get("kind") == "page-local"
            and current.get("return_sha256") == digest
            and current.get("return_bytes") == len(data)
            and current.get("package_digest") == local["package_digest"]
        )
        if same_bytes and current.get("declared_transport") != label:
            refuse("declared transport differs")
        refuse("occupied different content")
    updated = copy.deepcopy(record)
    updated["passes"][pass_id]["return"] = local
    updated = append_transition(
        updated,
        "seal-return",
        pass_id,
        {
            "declared_transport": label,
            "kind": "page-local",
            "package_digest": local["package_digest"],
            "return_bytes": len(data),
            "return_sha256": digest,
        },
    )
    commit(page, updated, [(f"artifacts/{pass_id}/return.md", data)])
    if read_plain(page / return_name(pass_id)) != data or read_plain(page / "artifacts" / pass_id / "return.md") != data:
        refuse("hash conflict", True)
    return result("seal-return-local", "complete", True, return_sha256=digest)


def earlier_pass_bytes(page: Path, record: dict) -> dict[str, bytes]:
    found = {}
    for pass_id, slot in record["passes"].items():
        if slot["package"] is not None:
            for name in (pack_name(pass_id), notes_name(pass_id)):
                path = page / name
                found[name] = read_plain(path)
            snapshot = page / "artifacts" / pass_id / "package" / notes_name(pass_id)
            found[f"artifacts/{pass_id}/package/{notes_name(pass_id)}"] = read_plain(snapshot)
        if slot["return"] is not None:
            found[return_name(pass_id)] = read_plain(page / return_name(pass_id))
            found[f"artifacts/{pass_id}/return.md"] = read_plain(page / "artifacts" / pass_id / "return.md")
        if slot["review"] is not None:
            found[review_name(pass_id)] = read_plain(page / review_name(pass_id))
    return found


def command_open_pass(book: Path, page_name: str, pass_id: str) -> dict:
    require_pass(pass_id)
    page = page_dir(book, page_name)
    record = require_loaded(page)
    if page_name != record["page"]:
        refuse("missing investigation")
    decision, info = open_pass_decision(record, pass_id)
    if decision == "repeat":
        return result("open-pass", "repeat", False, opened_pass=pass_id)
    if decision != "create" or info is None:
        refuse(decision)
    updated = copy.deepcopy(record)
    updated["passes"][pass_id] = empty_slot()
    updated = append_transition(
        updated,
        "open-pass",
        pass_id,
        {
            "opened_pass": pass_id,
            "requested_by": info["requested_by"],
            "review_sha256": info["review_sha256"],
        },
    )
    before = earlier_pass_bytes(page, record)
    before_count = len(record["transitions"])
    commit(page, updated)
    for rel, data in before.items():
        if read_plain(page.joinpath(*rel.split("/"))) != data:
            refuse("hash conflict", True)
    for name in (pack_name(pass_id), notes_name(pass_id), return_name(pass_id), review_name(pass_id)):
        if os.path.lexists(page / name):
            refuse("hash conflict", True)
    try:
        loaded = require_loaded(page)
    except Refuse as exc:
        refuse(exc.reason, True)
    if len(loaded["transitions"]) != before_count + 1 or pass_id not in loaded["passes"]:
        refuse("hash conflict", True)
    if loaded["passes"][pass_id] != empty_slot():
        refuse("hash conflict", True)
    return result("open-pass", "complete", True, opened_pass=pass_id)


def command_propose(book: Path) -> dict:
    used = set()
    for child in book.iterdir():
        if child.is_dir() and PAGE_RE.fullmatch(child.name):
            number = int(child.name[:4])
            if 701 <= number <= 799:
                used.add(number)
    for number in range(701, 800):
        if number not in used:
            return result("propose", "complete", False, page=f"{number:04d}.free")
    refuse("outside declared band")


def command_open(book: Path, request_path: Path, closure: Path | None, sources: Path | None) -> dict:
    if (closure is None) == (sources is None):
        refuse("malformed request")
    request = require_open_request(parse_json(request_path.read_bytes()))
    if closure is not None:
        load_closure(request, closure)
    else:
        load_sources(request, sources)
    page = page_dir(book, request["page"])
    if page.exists():
        refuse("occupied page")
    page.mkdir()
    record = fresh_record(request)
    check_chain(record)
    commit(page, record)
    return result("open", "complete", True, page=request["page"])


def listed_files(recorded: dict) -> dict[str, dict]:
    rows = recorded.get("out_files")
    if not isinstance(rows, list):
        refuse("malformed package")
    out = {}
    for row in rows:
        if not isinstance(row, dict) or not isinstance(row.get("path"), str):
            refuse("malformed package")
        out[row["path"]] = row
    return out


def classify_verify(code: int, payload: bytes, expect: str) -> dict:
    try:
        body = parse_json(payload)
    except Refuse:
        refuse("malformed package")
    if not isinstance(body, dict):
        refuse("malformed package")
    findings = body.get("findings") if isinstance(body.get("findings"), list) else []
    codes = [item.get("code") for item in findings if isinstance(item, dict)]
    if code == 0 and body.get("result") == "intact":
        digest = body.get("digest")
        if digest == expect:
            return body
        if isinstance(digest, str) and len(digest) == 64:
            refuse("stale expected hash")
        refuse("malformed package")
    if "version" in codes:
        refuse("unknown schema")
    if "pin" in codes:
        refuse("pin mismatch")
    if body.get("result") == "partial" or "not-completed" in codes:
        refuse("malformed package")
    if code == 1 or body.get("result") == "mismatch":
        refuse("conflicting bytes")
    refuse("malformed package")


def command_attach(book: Path, page_name: str, pass_id: str, output: Path, config: str, expect: str, producer: Path) -> dict:
    require_pass(pass_id)
    if not isinstance(expect, str) or len(expect) != 64 or any(ch not in "0123456789abcdef" for ch in expect):
        refuse("malformed digest")
    page = page_dir(book, page_name)
    record = require_loaded(page)
    if page_name != record["page"] or pass_id not in record["passes"]:
        refuse("missing investigation")
    walk_refuse_links(output)
    if not producer.is_absolute():
        refuse("producer path is not absolute")
    refuse_chain(producer)
    pin_file(producer, PRODUCER_SHA, PRODUCER_LEN)
    config = require_input_file(config, "config")
    load_config(config)
    code, payload, _err = run_process(
        [str(producer), "verify", "--output", str(output), "--config", str(config), "--json"]
    )
    body = classify_verify(code, payload, expect)
    if body.get("investigation") != {"book": record["book"], "page": record["page"], "pass": pass_id}:
        refuse("wrong origin")
    exchange = body.get("exchange")
    if not isinstance(exchange, dict):
        refuse("malformed package")
    if exchange.get("pass") != pass_id or exchange.get("pack") != pack_name(pass_id):
        refuse("conflicting bytes")
    if exchange.get("notes") != notes_name(pass_id) or exchange.get("return_name") != return_name(pass_id):
        refuse("conflicting bytes")
    if exchange.get("review_name") != review_name(pass_id):
        refuse("conflicting bytes")
    verification_path = output / "verification.json"
    if plain_problem(verification_path, "file") or plain_problem(output / "prepared-colab.zip", "file"):
        refuse("malformed package")
    recorded = parse_json(verification_path.read_bytes())
    if not isinstance(recorded, dict) or recorded.get("schema") != VERIFICATION_SCHEMA:
        refuse("unknown schema")
    if recorded.get("digest") != expect:
        refuse("stale expected hash" if isinstance(recorded.get("digest"), str) else "malformed package")
    if recorded.get("investigation") != {"book": record["book"], "page": record["page"], "pass": pass_id}:
        refuse("wrong origin")
    rows = listed_files(recorded)
    package_root = output / "package"
    found = []
    for dirpath, _dirs, filenames in os.walk(package_root):
        for name in filenames:
            path = Path(dirpath) / name
            if is_reparse(path):
                refuse("unsafe path")
            rel = "package/" + path.relative_to(package_root).as_posix()
            if rel.endswith(".return.md") or rel.endswith(".review.md"):
                refuse("conflicting bytes")
            data = path.read_bytes()
            row = rows.get(rel)
            if row is None or row.get("sha256") != sha256(data) or row.get("bytes") != len(data):
                refuse("conflicting bytes")
            found.append((rel, data))
    for rel in rows:
        if rel.startswith("package/") and rel not in {item[0] for item in found}:
            refuse("conflicting bytes")
    zip_path = output / "prepared-colab.zip"
    zip_bytes = zip_path.read_bytes()
    zip_row = rows.get("prepared-colab.zip")
    if zip_row is None or zip_row.get("sha256") != sha256(zip_bytes) or zip_row.get("bytes") != len(zip_bytes):
        refuse("conflicting bytes")
    verification_bytes = verification_path.read_bytes()
    pack_bytes = None
    notes_bytes = None
    for rel, data in found:
        if rel == "package/" + pack_name(pass_id):
            pack_bytes = data
        if rel == "package/" + notes_name(pass_id):
            notes_bytes = data
    if pack_bytes is None or notes_bytes is None:
        refuse("malformed package")
    package_info = {
        "digest": expect,
        "digest_alg": DIGEST_ALG,
        "notes_sha256": sha256(notes_bytes),
        "pack_sha256": sha256(pack_bytes),
        "verification_sha256": sha256(verification_bytes),
        "zip_sha256": sha256(zip_bytes),
    }
    current = record["passes"][pass_id]["package"]
    if current == package_info:
        stored = page / "artifacts" / pass_id / "package" / pack_name(pass_id)
        if stored.is_file() and stored.read_bytes() == pack_bytes:
            return result("attach", "repeat", False, digest=expect)
        refuse("conflicting bytes")
    if current is not None:
        refuse("conflicting bytes")
    provenance = canonical(
        {
            "digest": expect,
            "digest_alg": DIGEST_ALG,
            "layout": "colab-exchange-layout/2",
            "notes_sha256": package_info["notes_sha256"],
            "pack_sha256": package_info["pack_sha256"],
            "pins": {
                "assembler": ASSEMBLER_SHA,
                "checker": CHECKER_SHA,
                "helper": CAPTURE_SHA,
                "inspector": INSPECT_SHA,
            },
            "producer_sha256": PRODUCER_SHA,
            "producer_v1_sha256": PRODUCER_V1_SHA,
            "schema": PROVENANCE_SCHEMA,
            "statements": [
                "The verifier result is mechanical evidence, not approval.",
                "Handoff metadata is not the authority for this attach.",
            ],
            "verifier_result": "intact",
            "zip_sha256": package_info["zip_sha256"],
        }
    )
    if b"colab-config" in provenance or b":\\" in provenance or b":/" in provenance:
        refuse("malformed package")
    if str(config).encode("utf-8") in provenance or str(output).encode("utf-8") in provenance:
        refuse("malformed package")
    updated = copy.deepcopy(record)
    updated["passes"][pass_id]["package"] = package_info
    updated = append_transition(
        updated,
        "attach",
        pass_id,
        {
            "notes_sha256": package_info["notes_sha256"],
            "package_digest": package_info["digest"],
            "pack_sha256": package_info["pack_sha256"],
            "verification_sha256": package_info["verification_sha256"],
            "zip_sha256": package_info["zip_sha256"],
        },
    )
    extra = [(f"artifacts/{pass_id}/" + rel, data) for rel, data in found]
    extra.append((f"artifacts/{pass_id}/prepared-colab.zip", zip_bytes))
    extra.append((f"artifacts/{pass_id}/verification.json", verification_bytes))
    extra.append((f"artifacts/{pass_id}/provenance.json", provenance))
    commit(page, updated, extra)
    return result("attach", "complete", True, digest=expect)


def command_note(book: Path, page_name: str, pass_id: str, text: str) -> dict:
    require_pass(pass_id)
    line = one_line(text, "note")
    page = page_dir(book, page_name)
    record = require_loaded(page)
    slot = record["passes"].get(pass_id)
    if slot is None or slot["package"] is None:
        refuse("missing investigation")
    if line in slot["notes"]:
        return result("append-note", "repeat", False)
    updated = copy.deepcopy(record)
    updated["passes"][pass_id]["notes"] = [*slot["notes"], line]
    updated = append_transition(
        updated,
        "append-note",
        pass_id,
        {"note_sha256": sha256(line.encode("utf-8")), "notes_count": len(slot["notes"]) + 1},
    )
    before = (page / "artifacts" / pass_id / "package" / notes_name(pass_id)).read_bytes()
    commit(page, updated)
    after = (page / "artifacts" / pass_id / "package" / notes_name(pass_id)).read_bytes()
    if after != before or sha256(after) != updated["passes"][pass_id]["package"]["notes_sha256"]:
        refuse("hash conflict", True)
    return result("append-note", "complete", True)


def custody_from_verify(payload: bytes) -> str:
    text = payload.decode("utf-8", "replace")
    lines = text.splitlines()
    if any(line not in lines for line in CUSTODY_LINES):
        refuse("partial custody")
    receipts = [line.split(" ", 1)[1] for line in lines if line.startswith("receipt ")]
    if len(receipts) != 1 or len(receipts[0]) != 64:
        refuse("partial custody")
    return receipts[0]


def command_place(book: Path, page_name: str, pass_id: str, member: str, config_path: Path) -> dict:
    require_pass(pass_id)
    if not isinstance(member, str) or MEMBER_RE.fullmatch(member) is None:
        refuse("malformed member")
    page = page_dir(book, page_name)
    record = require_loaded(page)
    slot = record["passes"].get(pass_id)
    if slot is None or slot["package"] is None:
        refuse("missing investigation")
    config = load_config(config_path)
    helper = Path(config["helper"])
    inspector = Path(config["inspector"])
    code, payload, _err = run_process([str(inspector), "inspect", "--book", str(book), "--member", member, "--json"])
    if code != 0:
        refuse("partial custody")
    observed = parse_json(payload)
    if not isinstance(observed, dict) or observed.get("status") != "complete":
        refuse("partial custody")
    capture = observed.get("capture")
    if not isinstance(capture, dict):
        refuse("partial custody")
    origin = capture.get("origin")
    if origin != {"batch": pass_id, "book": record["book"], "page": record["page"]}:
        refuse("wrong origin")
    returned = capture.get("return")
    if not isinstance(returned, dict):
        refuse("partial custody")
    verify_code, verify_out, _err = run_process([str(helper), "verify", "--book", str(book), "--member", member])
    if verify_code != 0:
        refuse("partial custody")
    receipt = custody_from_verify(verify_out)
    if receipt != capture.get("receipt_sha256"):
        refuse("hash conflict")
    member_dir = book / member
    if not within(member_dir, book):
        refuse("unsafe path")
    return_path = member_dir / "return.md"
    problem = plain_problem(return_path, "file")
    if problem:
        refuse("partial custody")
    data = return_path.read_bytes()
    digest = sha256(data)
    if digest != returned.get("sha256") or len(data) != returned.get("bytes"):
        refuse("hash conflict")
    placed = {
        "kind": "n1nn",
        "manifest_sha256": capture.get("manifest_sha256"),
        "member": member,
        "origin_batch": pass_id,
        "origin_book": record["book"],
        "origin_page": record["page"],
        "receipt_sha256": receipt,
        "return_bytes": len(data),
        "return_sha256": digest,
    }
    current = slot["return"]
    existing = page / return_name(pass_id)
    if current is not None:
        if current == placed and existing.is_file() and existing.read_bytes() == data:
            return result("place-return", "repeat", False, member=member)
        refuse("occupied different content")
    updated = copy.deepcopy(record)
    updated["passes"][pass_id]["return"] = placed
    updated = append_transition(
        updated,
        "place-return",
        pass_id,
        {
            "kind": "n1nn",
            "manifest_sha256": placed["manifest_sha256"],
            "member": member,
            "origin_batch": placed["origin_batch"],
            "origin_book": placed["origin_book"],
            "origin_page": placed["origin_page"],
            "receipt_sha256": receipt,
            "return_bytes": len(data),
            "return_sha256": digest,
        },
    )
    commit(page, updated, [(f"artifacts/{pass_id}/return.md", data)])
    written = (page / return_name(pass_id)).read_bytes()
    if written != data:
        refuse("hash conflict", True)
    return result("place-return", "complete", True, member=member)


def require_review(body: dict, record: dict, pass_id: str) -> dict:
    if not isinstance(body, dict) or body.get("schema") != REVIEW_SCHEMA:
        refuse("unknown schema")
    if set(body) != set(REVIEW_KEYS):
        refuse("malformed review")
    one_line(body["by"], "reviewer")
    one_line(body["on"], "review date")
    one_line(body["assessment"], "assessment")
    if body["route"] not in ROUTES:
        refuse("malformed review")
    next_pass = body["next_pass"]
    if body["route"] == "request-next":
        require_pass(next_pass)
        if next_pass == pass_id:
            refuse("malformed review")
    elif next_pass is not None:
        refuse("malformed review")
    findings = body["findings"]
    questions = body["pending_questions"]
    if not isinstance(findings, list) or len(findings) > LIST_LIMIT:
        refuse("malformed review")
    if not isinstance(questions, list) or len(questions) > LIST_LIMIT:
        refuse("malformed review")
    ids = {target["id"] for target in record["targets"]}
    seen = set()
    unresolved = False
    for finding in findings:
        if not isinstance(finding, dict) or set(finding) != set(FINDING_KEYS):
            if isinstance(finding, dict) and "director_reply" not in finding:
                refuse("director reply required")
            refuse("malformed review")
        if finding["director_reply"] is None or finding["director_reply"] == "":
            refuse("director reply required")
        one_line(finding["director_reply"], "director reply")
        if not isinstance(finding["id"], str) or FINDING_RE.fullmatch(finding["id"]) is None or finding["id"] in seen:
            refuse("malformed review")
        seen.add(finding["id"])
        if not isinstance(finding["consequential"], bool) or not isinstance(finding["pending"], bool):
            refuse("malformed review")
        if finding["disposition"] not in DISPOSITIONS:
            refuse("malformed review")
        if finding["source_binding"] not in ids:
            refuse("malformed review")
        one_line(finding["observation"], "observation")
        one_line(finding["reason"], "reason")
        if finding["pending"] or finding["disposition"] in UNRESOLVED:
            unresolved = True
    for question in questions:
        one_line(question, "question")
    if body["route"] == "finish" and unresolved:
        refuse("unresolved findings")
    return body


def command_review(book: Path, page_name: str, pass_id: str, review_path: Path) -> dict:
    require_pass(pass_id)
    page = page_dir(book, page_name)
    record = require_loaded(page)
    slot = record["passes"].get(pass_id)
    if slot is None or slot["package"] is None:
        refuse("missing investigation")
    if slot["return"] is None:
        refuse("review before return")
    review = require_review(parse_json(review_path.read_bytes()), record, pass_id)
    current = slot["review"]
    if current == review:
        return result("record-review", "repeat", False, route=review["route"])
    if current is not None:
        refuse("occupied different content")
    updated = copy.deepcopy(record)
    updated["passes"][pass_id]["review"] = review
    updated = append_transition(
        updated,
        "review",
        pass_id,
        {
            "next_pass": review["next_pass"],
            "review_sha256": sha256(canonical(review)),
            "route": review["route"],
        },
    )
    before = (page / return_name(pass_id)).read_bytes()
    commit(page, updated)
    if (page / return_name(pass_id)).read_bytes() != before:
        refuse("hash conflict", True)
    if review["route"] == "request-next" and (page / pack_name(review["next_pass"])).exists():
        refuse("malformed review", True)
    return result("record-review", "complete", True, route=review["route"])


def pass_flags(slot: dict) -> dict:
    review = slot["review"]
    unresolved = False
    held = False
    if review is not None:
        for finding in review["findings"]:
            if finding["disposition"] == "held":
                held = True
            if finding["pending"] or finding["disposition"] in UNRESOLVED:
                unresolved = True
    return {
        "attached": slot["package"] is not None,
        "explicit_finish": bool(review and review["route"] == "finish"),
        "held": held,
        "request_next": review["next_pass"] if review and review["route"] == "request-next" else None,
        "return_kind": None if slot["return"] is None else slot["return"].get("kind"),
        "return_placed": slot["return"] is not None,
        "review_pending": bool(review and (unresolved or review["route"] != "finish")),
        "review_recorded": review is not None,
        "route": None if review is None else review["route"],
        "route_n5nn": bool(review and review["route"] == "route-n5nn"),
    }


def command_show(book: Path) -> dict:
    pages = []
    for child in sorted(book.iterdir(), key=lambda item: item.name):
        if not child.is_dir() or PAGE_RE.fullmatch(child.name) is None:
            continue
        blocked = (child / "partial.json").exists() or (child / "attempt.json").exists() or (child / ".write.lock").exists()
        if blocked:
            pages.append({"page": child.name, "partial": True, "passes": [], "transitions": None})
            continue
        if not (child / "investigation.json").is_file():
            continue
        record = require_loaded(child)
        passes = []
        for pass_id, slot in sorted(record["passes"].items()):
            flags = pass_flags(slot)
            flags["pass"] = pass_id
            passes.append(flags)
        pages.append(
            {"page": child.name, "partial": False, "passes": passes, "transitions": record["transitions"]}
        )
    return result("show", "complete", False, pages=pages)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="colab_workflow.py")

    def error(_message):
        raise Usage()

    parser.error = error
    sub = parser.add_subparsers(dest="command", required=True)

    def add(name: str) -> argparse.ArgumentParser:
        item = sub.add_parser(name)
        item.error = error
        return item

    propose = add("propose")
    propose.add_argument("--book", required=True)
    opened = add("open")
    opened.add_argument("--book", required=True)
    opened.add_argument("--request", required=True)
    opened.add_argument("--closure")
    opened.add_argument("--sources")
    attach = add("attach")
    attach.add_argument("--book", required=True)
    attach.add_argument("--page", required=True)
    attach.add_argument("--pass", dest="pass_id", required=True)
    attach.add_argument("--output", required=True)
    attach.add_argument("--config", required=True)
    attach.add_argument("--expect-digest", required=True)
    attach.add_argument("--producer")
    note = add("append-note")
    note.add_argument("--book", required=True)
    note.add_argument("--page", required=True)
    note.add_argument("--pass", dest="pass_id", required=True)
    note.add_argument("--text", required=True)
    place = add("place-return")
    place.add_argument("--book", required=True)
    place.add_argument("--page", required=True)
    place.add_argument("--pass", dest="pass_id", required=True)
    place.add_argument("--member", required=True)
    place.add_argument("--config", required=True)
    review = add("record-review")
    review.add_argument("--book", required=True)
    review.add_argument("--page", required=True)
    review.add_argument("--pass", dest="pass_id", required=True)
    review.add_argument("--review", required=True)
    seal = add("seal-return-local")
    seal.add_argument("--book", required=True)
    seal.add_argument("--page", required=True)
    seal.add_argument("--pass", dest="pass_id", required=True)
    seal.add_argument("--return-file", required=True)
    seal.add_argument("--declared-transport", required=True)
    later = add("open-pass")
    later.add_argument("--book", required=True)
    later.add_argument("--page", required=True)
    later.add_argument("--pass", dest="pass_id", required=True)
    show = add("show")
    show.add_argument("--book", required=True)
    return parser


def dispatch(args) -> dict:
    book = require_book(args.book)
    if args.command == "propose":
        return command_propose(book)
    if args.command == "open":
        closure = require_input_dir(args.closure, "closure") if args.closure else None
        sources = require_input_dir(args.sources, "sources") if args.sources else None
        return command_open(book, require_input_file(args.request, "request"), closure, sources)
    if args.command == "attach":
        producer = Path(args.producer) if args.producer else producer_path()
        return command_attach(
            book,
            args.page,
            args.pass_id,
            require_input_dir(args.output, "output"),
            args.config,
            args.expect_digest,
            producer,
        )
    if args.command == "append-note":
        return command_note(book, args.page, args.pass_id, args.text)
    if args.command == "place-return":
        return command_place(
            book,
            args.page,
            args.pass_id,
            args.member,
            require_input_file(args.config, "config"),
        )
    if args.command == "record-review":
        return command_review(
            book,
            args.page,
            args.pass_id,
            require_input_file(args.review, "review"),
        )
    if args.command == "seal-return-local":
        return command_seal_return(
            book,
            args.page,
            args.pass_id,
            require_input_file(args.return_file, "return file"),
            args.declared_transport,
        )
    if args.command == "open-pass":
        return command_open_pass(book, args.page, args.pass_id)
    return command_show(book)


def execute(argv: list[str]) -> tuple[int, bytes, bytes]:
    try:
        args = build_parser().parse_args(argv)
        body = dispatch(args)
    except Usage:
        return 2, b"", b"usage\n"
    except Refuse as exc:
        body = result(argv[0] if argv else "workflow", "refused", exc.wrote, reason=exc.reason)
        return 2, canonical(body), b""
    return 0, canonical(body), b""


def main(argv: list[str] | None = None) -> int:
    code, out, err = execute(sys.argv[1:] if argv is None else argv)
    sys.stdout.buffer.write(out)
    sys.stderr.buffer.write(err)
    return code


if __name__ == "__main__":
    sys.exit(main())
