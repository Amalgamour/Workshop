"""Workflow adapter for one declared N7NN Colab investigation.

The canonical fact store is investigation.json. Markdown faces are projections.
Attach keeps an accepted producer package after the pinned verifier runs.
This tool does not prepare Claude's package, call a model, reserve a return,
or write the live work book.
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


SCHEMA_NAME = "colab-workflow-result/1"
INVESTIGATION_SCHEMA = "colab-investigation/1"
OPEN_SCHEMA = "colab-open/1"
SEAL_SCHEMA = "colab-investigation-seal/1"
PARTIAL_SCHEMA = "colab-investigation-partial/1"
DIGEST_ALG = "colab-package-digest/1"
LEGACY_LABEL = "legacy-line-preimage"
PROVENANCE_SCHEMA = "colab-workflow-provenance/1"
PRODUCER_REL = "labs/colab-support-pass01/colab_support.py"
PRODUCER_SHA = "33bbe41c52485fc7b2b611d830bae8a15129721ad807a931e8193f17944c467c"
PRODUCER_LEN = 67781
ASSEMBLER_SHA = "75d49679cbf3e624a82573229ca8c7cd9b758799bc26b6f080111feb6eaa275c"
ASSEMBLER_LEN = 43928
CHECKER_SHA = "9bbd9d57f3b7da43234ac2e6ae4ce40a0ab6af2f53c8135ecfb2ee0c8a6e322d"
CHECKER_LEN = 21563
BINDING_SCHEMA_SHA = "690a0d56e590b7028dbcad8a57ffd6d6eaf20c341c016308506373d82e5c690b"
BINDING_SCHEMA_LEN = 3195
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
PACKAGE_FILE_LIMIT = 64
PACKAGE_BYTE_LIMIT = 262144
FINDING_LIMIT = 64
LIVE_BOOK = os.path.normcase(os.path.abspath(r"D:\Git\lib-build\00.kernel\00.00.10.work"))
LIVE_KERNEL = os.path.normcase(os.path.abspath(r"D:\Git\lib-build\00.kernel"))
PAGE_RE = re.compile(r"^[0-9]{4}\.[a-z][a-z0-9-]*$")
HEADING_RE = re.compile(r"^(#{1,6})[ \t]+\S")
PASS_RE = re.compile(r"^05\.[0-9]{2}$")
MEMBER_RE = re.compile(r"^(\d{4})\.([A-Za-z0-9][A-Za-z0-9._-]{0,63})$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
FINDING_RE = re.compile(r"^F[0-9]{2}$")
TARGET_RE = re.compile(r"^T[0-9]{2}$")
MODES = {"open-design", "hostile", "diagnostic", "experiment"}
STATEMENT_KINDS = {"release", "claim", "review"}
ACTIONS = {"accepted", "rejected", "held", "deferred", "answered"}
BRIEF_HEADINGS = [
    "## Role and mode",
    "## Purpose and question",
    "## Built state and known gaps",
    "## Reasons and assumptions",
    "## Scope and sources",
    "## Dependencies",
    "## Capabilities",
    "## Method",
    "## Permissions and stop",
    "## Return",
]
RETURN_HEADINGS = [
    "## Question",
    "## Evidence",
    "## Hostile",
    "## Factfind",
    "## Overflow",
    "## Unprompted",
    "## Qualitative result",
]
FORBIDDEN_LINE = "Scores first. Opinion second."
IDENTITY_KEYS = (
    "assumptions",
    "book",
    "capabilities",
    "challenge",
    "dependencies",
    "known_gaps",
    "method",
    "mode",
    "page",
    "permissions",
    "purpose",
    "question",
    "reading_order",
    "reasons",
    "return_shape",
    "scope",
    "stop",
    "targets",
    "title",
)
INSPECT_EXIT = {"complete": 0, "reserved": 1, "missing": 1, "incomplete": 2, "refused": 2}
CUSTODY_LINES = (
    "result complete",
    "not approved",
    "not accepted",
    "not published",
)
SKIP_SCHEMA_KEYS = {"$schema", "title"}
WRITE_HOOK = None
RUN_PROCESS = None
CURRENT = "workflow"


class Refuse(Exception):
    def __init__(self, reason: str, wrote: bool = False) -> None:
        super().__init__(reason)
        self.reason = reason
        self.wrote = wrote


def refuse(reason: str, wrote: bool = False) -> None:
    raise Refuse(reason, wrote)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical(value) -> bytes:
    try:
        text = json.dumps(
            value,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        )
    except (TypeError, ValueError):
        refuse("malformed json")
    return (text + "\n").encode("utf-8")


def parse_json(data: bytes):
    if data.startswith(b"\xef\xbb\xbf") or b"\x00" in data:
        refuse("malformed json")
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
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
        return json.loads(text, object_pairs_hook=pairs, parse_constant=constant)
    except Refuse:
        raise
    except json.JSONDecodeError:
        refuse("malformed json")


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def schema_path() -> Path:
    return repo_root() / "00.kernel/00.00.10.work/0411.colab/evidence/n7nn-interface-v1/binding.schema.json"


def default_helpers() -> Path:
    return repo_root() / "labs/return-capture-pass01"


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


def require_abs_path(text: str, label: str, kind: str) -> Path:
    if not isinstance(text, str) or text == "":
        refuse(f"{label} path is not absolute")
    path = Path(text)
    if not path.is_absolute():
        refuse(f"{label} path is not absolute")
    refuse_live(path)
    refuse_chain(path)
    problem = plain_problem(path, kind)
    if problem:
        refuse("unsafe path" if problem == "link" else f"{label} is missing")
    return path


def require_abs_file(text: str, label: str) -> Path:
    return require_abs_path(text, label, "file")


def require_abs_dir(text: str, label: str) -> Path:
    return require_abs_path(text, label, "dir")


def require_input_dir(text: str, label: str) -> Path:
    """Read an input directory. The live-book guard applies to the book, not to a pinned envelope."""
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


def read_file(path: Path) -> bytes:
    problem = plain_problem(path, "file")
    if problem:
        refuse("unsafe path" if problem == "link" else "missing file")
    return path.read_bytes()


def within(child: Path, parent: Path) -> bool:
    try:
        return os.path.commonpath([norm(child), norm(parent)]) == norm(parent)
    except ValueError:
        return False


def source_parts(text: str) -> list[str]:
    if not isinstance(text, str) or text == "" or "\\" in text or text.startswith("/"):
        refuse("unsafe path")
    parts = text.split("/")
    if any(part in ("", ".", "..") for part in parts):
        refuse("unsafe path")
    return parts


def relative_parts(text: str) -> list[str]:
    return source_parts(text)


def emitted_parts(text: str) -> list[str]:
    parts = source_parts(text)
    for part in parts:
        if part.endswith(".colab"):
            refuse("colab tail")
        if part == "07.md":
            refuse("face 07")
    return parts


def join_under(root: Path, relative: str) -> Path:
    dest = root
    for part in source_parts(relative):
        dest = dest / part
    if not within(dest, root):
        refuse("unsafe path")
    return dest


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
    flags = os.O_WRONLY | os.O_CREAT | os.O_TRUNC
    if hasattr(os, "O_BINARY"):
        flags |= os.O_BINARY
    fd = os.open(str(path), flags)
    try:
        os.write(fd, data)
    finally:
        os.close(fd)


def require_text(value, label: str, limit: int = TEXT_LIMIT) -> str:
    if not isinstance(value, str) or value == "" or len(value) > limit:
        refuse(f"malformed {label}")
    if any(ord(ch) < 32 or ord(ch) == 127 for ch in value):
        refuse(f"malformed {label}")
    return value


def require_string_list(value, label: str, minimum: int = 0) -> list[str]:
    if not isinstance(value, list) or len(value) < minimum or len(value) > LIST_LIMIT:
        refuse("limit" if isinstance(value, list) and len(value) > LIST_LIMIT else f"malformed {label}")
    return [require_text(item, label) for item in value]


def require_keys(value, keys: set[str], label: str) -> dict:
    if not isinstance(value, dict):
        refuse(f"malformed {label}")
    if set(value) != keys:
        extra = set(value) - keys
        if extra:
            refuse("unknown field")
        refuse(f"malformed {label}")
    return value


def page_number(page: str) -> int:
    return int(page[:4])


def require_investigation_page(page: str) -> str:
    if not isinstance(page, str) or len(page) > PAGE_LIMIT or PAGE_RE.fullmatch(page) is None:
        refuse("malformed page")
    number = page_number(page)
    if number < 701 or number > 799:
        refuse("outside declared band")
    return page


def require_subject_page(page: str) -> str:
    if not isinstance(page, str) or len(page) > PAGE_LIMIT or PAGE_RE.fullmatch(page) is None:
        refuse("malformed page")
    return page


def require_pass(value: str) -> str:
    if not isinstance(value, str) or PASS_RE.fullmatch(value) is None:
        refuse("malformed pass")
    return value


def notes_name(pass_id: str) -> str:
    return f"06.{pass_id.split('.')[1]}.md"


def pass_name(pass_id: str) -> str:
    return f"{pass_id}.md"


def load_binding_schema() -> dict:
    path = schema_path()
    refuse_chain(path)
    data = read_file(path)
    if len(data) != BINDING_SCHEMA_LEN or sha256(data) != BINDING_SCHEMA_SHA:
        refuse("binding schema pin mismatch")
    parsed = parse_json(data)
    if not isinstance(parsed, dict):
        refuse("binding schema pin mismatch")
    return parsed


def type_names(spec) -> list[str]:
    if isinstance(spec, str):
        return [spec]
    if isinstance(spec, list) and all(isinstance(item, str) for item in spec):
        return spec
    refuse("malformed type")


def matches_type(value, names: list[str]) -> bool:
    for name in names:
        if name == "null" and value is None:
            return True
        if name == "string" and isinstance(value, str):
            return True
        if name == "integer" and isinstance(value, int) and not isinstance(value, bool):
            return True
        if name == "object" and isinstance(value, dict):
            return True
        if name == "array" and isinstance(value, list):
            return True
        if name == "boolean" and isinstance(value, bool):
            return True
    return False


def check_schema(value, schema: dict) -> None:
    if not isinstance(schema, dict):
        refuse("malformed type")
    unknown = set(schema) - SKIP_SCHEMA_KEYS - {
        "type",
        "additionalProperties",
        "required",
        "properties",
        "const",
        "pattern",
        "minLength",
        "minItems",
        "maxItems",
        "items",
        "oneOf",
        "enum",
        "minimum",
    }
    if unknown:
        refuse("unknown field")
    if "oneOf" in schema:
        matched = 0
        for branch in schema["oneOf"]:
            try:
                check_schema(value, branch)
            except Refuse:
                continue
            matched += 1
        if matched != 1:
            refuse("malformed type")
        return
    if "const" in schema and value != schema["const"]:
        refuse("malformed type")
    if "enum" in schema and value not in schema["enum"]:
        refuse("malformed type")
    if "type" in schema:
        names = type_names(schema["type"])
        if not matches_type(value, names):
            refuse("malformed type")
    if isinstance(value, str):
        if "minLength" in schema and len(value) < schema["minLength"]:
            refuse("malformed type")
        if "pattern" in schema and re.fullmatch(schema["pattern"], value) is None:
            refuse("malformed type")
    if isinstance(value, int) and not isinstance(value, bool) and "minimum" in schema:
        if value < schema["minimum"]:
            refuse("malformed type")
    if isinstance(value, list):
        if "minItems" in schema and len(value) < schema["minItems"]:
            refuse("limit")
        if "maxItems" in schema and len(value) > schema["maxItems"]:
            refuse("limit")
        if "items" in schema:
            for item in value:
                check_schema(item, schema["items"])
    if isinstance(value, dict):
        properties = schema.get("properties", {})
        if schema.get("additionalProperties") is False and set(value) - set(properties):
            refuse("unknown field")
        for key in schema.get("required", []):
            if key not in value:
                refuse("malformed type")
        for key, item in value.items():
            if key in properties:
                check_schema(item, properties[key])


def binding_document(book: str, page: str, pass_id: str, targets) -> dict:
    return {
        "schema": "colab-binding/1",
        "investigation": {"book": book, "page": page, "pass": pass_id},
        "targets": targets,
    }


def validate_targets(book: str, page: str, pass_id: str, targets) -> None:
    if not isinstance(targets, list) or not targets:
        refuse("malformed targets")
    if len(targets) > TARGET_LIMIT:
        refuse("limit")
    check_schema(binding_document(book, page, pass_id, targets), load_binding_schema())
    seen_ids = set()
    seen_bodies = set()
    for target in targets:
        source_parts(target["source"]["path"])
        source_parts(target["file"])
        if target["id"] in seen_ids:
            refuse("duplicate target")
        seen_ids.add(target["id"])
        body = canonical(
            {
                "book": target["book"],
                "file": target["file"],
                "page": target["page"],
                "section": target["section"],
                "source": target["source"],
            }
        )
        if body in seen_bodies:
            refuse("duplicate target")
        seen_bodies.add(body)


def heading_matches(data: bytes, wanted: str) -> list[str]:
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
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
    if section.get("kind") == "id":
        refuse("unsupported section id")
    if section.get("kind") != "heading":
        refuse("malformed section")
    matches = heading_matches(data, section["value"])
    occurrence = section["occurrence"]
    if occurrence is None:
        if len(matches) != 1:
            refuse("ambiguous section" if len(matches) else "unresolved section")
        return
    if not isinstance(occurrence, int) or isinstance(occurrence, bool) or occurrence < 1:
        refuse("malformed section")
    if occurrence > len(matches):
        refuse("unresolved section")


def read_tree_file(root: Path, relative: str) -> bytes:
    path = join_under(root, relative)
    if not os.path.lexists(path):
        refuse("unresolved section")
    data = read_file(path)
    if sha256(data) is None:
        refuse("stale source hash")
    return data


def check_snapshot(data: bytes, target: dict) -> None:
    if sha256(data) != target["source"]["sha256"] or len(data) != len(data):
        refuse("stale source hash")
    if sha256(data) != target["source"]["sha256"]:
        refuse("stale source hash")
    resolve_section(data, target["section"])


def require_open_request(value) -> dict:
    keys = set(IDENTITY_KEYS) | {"schema", "pass"}
    require_keys(value, keys, "request")
    if value["schema"] != OPEN_SCHEMA:
        refuse("malformed request")
    require_text(value["book"], "book")
    require_investigation_page(value["page"])
    require_pass(value["pass"])
    require_text(value["title"], "title", TITLE_LIMIT)
    for label in (
        "question",
        "purpose",
        "scope",
        "method",
        "challenge",
        "permissions",
        "stop",
        "return_shape",
    ):
        require_text(value[label], label)
    if value["mode"] not in MODES:
        refuse("malformed mode")
    require_string_list(value["known_gaps"], "known_gaps", 1)
    require_string_list(value["reasons"], "reasons", 1)
    require_string_list(value["assumptions"], "assumptions", 1)
    require_string_list(value["reading_order"], "reading_order", 1)
    dependencies = require_keys(value["dependencies"], {"supplied", "withheld", "unavailable"}, "dependencies")
    for label in ("supplied", "withheld", "unavailable"):
        require_string_list(dependencies[label], label, 0)
    capabilities = require_keys(value["capabilities"], {"read", "write", "execute", "network"}, "capabilities")
    for label in ("read", "write", "execute", "network"):
        require_text(capabilities[label], label)
    validate_targets(value["book"], value["page"], value["pass"], value["targets"])
    return value


def identity_of(value: dict) -> dict:
    return {key: value[key] for key in IDENTITY_KEYS}


def empty_pass() -> dict:
    return {
        "closure": None,
        "dispositions": [],
        "findings": [],
        "package": None,
        "return_pointer": None,
        "statements": [],
    }


def new_record(request: dict) -> dict:
    record = identity_of(request)
    record["schema"] = INVESTIGATION_SCHEMA
    record["passes"] = {request["pass"]: empty_pass()}
    record["proposals"] = []
    record["reconciliation"] = []
    return record


def lines_of(data: bytes) -> list[str]:
    return data.decode("utf-8").splitlines()


def require_headings(data: bytes, headings: list[str], label: str) -> None:
    rows = lines_of(data)
    if FORBIDDEN_LINE in rows:
        refuse(f"scored-exam default in {label}")
    for heading in headings:
        if heading not in rows:
            refuse(f"malformed {label}")


def render_entry(request: dict) -> bytes:
    targets = []
    for target in request["targets"]:
        section = "whole named file" if target["section"] is None else json.dumps(
            target["section"], ensure_ascii=False, sort_keys=True, separators=(",", ":")
        )
        source = target["source"]
        targets.append(
            f"- {target['id']} {target['book']} {target['page']} {target['file']} {section} {source['sha256']}"
        )
    gaps = "\n".join(f"- {item}" for item in request["known_gaps"])
    reasons = "\n".join(f"- {item}" for item in request["reasons"])
    assumptions = "\n".join(f"- {item}" for item in request["assumptions"])
    order = "\n".join(f"- {item}" for item in request["reading_order"])
    dependencies = request["dependencies"]
    capabilities = request["capabilities"]
    text = "\n".join(
        [
            "# Entry",
            "",
            "## Role and mode",
            request["mode"],
            "The recipient is a Colab for this question only. A model label is not a role.",
            "",
            "## Purpose and question",
            f"Purpose: {request['purpose']}",
            f"Question: {request['question']}",
            "",
            "## Built state and known gaps",
            gaps,
            "",
            "## Reasons and assumptions",
            reasons,
            assumptions,
            "",
            "## Scope and sources",
            f"Scope: {request['scope']}",
            "Reading order:",
            order,
            "Targets:",
            *targets,
            "Coverage is the named file or the named section. One file is not the whole page.",
            "",
            "## Dependencies",
            "Supplied: " + ", ".join(dependencies["supplied"]),
            "Withheld: " + ", ".join(dependencies["withheld"]),
            "Unavailable: " + ", ".join(dependencies["unavailable"]),
            "Missing access is not invented.",
            "",
            "## Capabilities",
            f"read: {capabilities['read']}",
            f"write: {capabilities['write']}",
            f"execute: {capabilities['execute']}",
            f"network: {capabilities['network']}",
            "",
            "## Method",
            request["method"],
            f"Challenge: {request['challenge']}",
            "",
            "## Permissions and stop",
            request["permissions"],
            f"Stop: {request['stop']}",
            "",
            "## Return",
            request["return_shape"],
            "Scoring is not declared.",
            "State the qualitative result.",
            "Do not manufacture a number.",
            "",
        ]
    )
    return text.encode("utf-8")


def render_return_template() -> bytes:
    text = "\n".join(
        [
            "# Return template",
            "",
            "Law 0036 remains the historical behaviour baseline. This template does not use its Ask line.",
            "",
            "## Question",
            "",
            "## Evidence",
            "",
            "## Hostile",
            "",
            "## Factfind",
            "",
            "## Overflow",
            "",
            "## Unprompted",
            "",
            "## Qualitative result",
            "Do not manufacture a number.",
            "",
        ]
    )
    return text.encode("utf-8")


def render_face(title: str, body: list[str]) -> bytes:
    rows = [f"# {title}", "", "projection: colab-investigation/1", *body, ""]
    text = "\n".join(rows)
    if FORBIDDEN_LINE in text.splitlines():
        refuse("scored-exam default in projection")
    return text.encode("utf-8")


def section_label(section) -> str:
    if section is None:
        return "whole named file"
    return json.dumps(section, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def projections(record: dict) -> dict[str, bytes]:
    files: dict[str, bytes] = {}
    targets = []
    for target in record["targets"]:
        source = target["source"]
        targets.append(
            f"- {target['id']} {target['book']} {target['page']} {target['file']} "
            f"{section_label(target['section'])} commit {source['commit']} sha256 {source['sha256']}"
        )
    files["01.md"] = render_face(
        record["title"],
        [
            f"page: {record['page']}",
            f"mode: {record['mode']}",
            "",
            "## Role and mode",
            record["mode"],
            "This projection is not a release and not a role.",
            "",
            "## Purpose and question",
            f"Purpose: {record['purpose']}",
            f"Question: {record['question']}",
            "",
            "## Built state and known gaps",
            *[f"- {item}" for item in record["known_gaps"]],
            "",
            "## Reasons and assumptions",
            *[f"- {item}" for item in record["reasons"]],
            *[f"- {item}" for item in record["assumptions"]],
            "",
            "## Scope and sources",
            f"Scope: {record['scope']}",
            "Reading order:",
            *[f"- {item}" for item in record["reading_order"]],
            "Targets:",
            *targets,
            "Coverage is the named file or the named section. One file is not the whole page.",
            "",
            "## Dependencies",
            "Supplied: " + ", ".join(record["dependencies"]["supplied"]),
            "Withheld: " + ", ".join(record["dependencies"]["withheld"]),
            "Unavailable: " + ", ".join(record["dependencies"]["unavailable"]),
            "",
            "## Capabilities",
            f"read: {record['capabilities']['read']}",
            f"write: {record['capabilities']['write']}",
            f"execute: {record['capabilities']['execute']}",
            f"network: {record['capabilities']['network']}",
            "",
            "## Method",
            record["method"],
            f"Challenge: {record['challenge']}",
            "",
            "## Permissions and stop",
            record["permissions"],
            f"Stop: {record['stop']}",
            "",
            "## Return",
            record["return_shape"],
            "Scoring is not declared.",
            "State the qualitative result.",
            "Do not manufacture a number.",
        ],
    )
    files["03.md"] = render_face("03 — Sources", ["These are pointers. A hash binds bytes. It does not authenticate a decision.", *targets])
    reason_rows = ["Supplied reasons. These are not computed findings."]
    reason_rows.extend(f"- {item}" for item in record["reasons"])
    files["06.md"] = render_face("06 — Reasons", reason_rows)
    pointer_rows = ["Package digests and return members. The return body stays in the captured member."]
    for pass_id in sorted(record["passes"]):
        body = record["passes"][pass_id]
        package = body["package"]
        digest = "absent" if package is None else package["digest"]
        pointer = body["return_pointer"]
        member = "absent" if pointer is None else pointer["member"]
        pointer_rows.append(f"- {pass_id} package {digest} return {member}")
        statement_rows = ["Recorded statements are not authority."]
        if body["statements"]:
            for item in body["statements"]:
                statement_rows.append(f"- {item['kind']} {item['on']} {item['by']}: {item['text']}")
        else:
            statement_rows.append("- none")
        return_row = "Return member: absent" if pointer is None else f"Return member: {pointer['member']}"
        package_row = "Package: absent" if package is None else f"Package: {package['digest']}"
        files[pass_name(pass_id)] = render_face(
            pass_id,
            [
                package_row,
                f"Route: artifacts/{pass_id}/",
                *statement_rows,
                return_row,
                "This page points. It is not a copy of the return body.",
            ],
        )
        artifact = "absent"
        if package is not None:
            note = "package/" + notes_name(pass_id)
            match = [item for item in package["files"] if item["path"] in (note, notes_name(pass_id))]
            if match:
                artifact = f"artifacts/{pass_id}/{note} sha256 {match[0]['sha256']}"
        finding_rows = ["Findings and dispositions stay in the canonical record."]
        for finding in body["findings"]:
            finding_rows.append(f"- {finding['id']} target {finding['target']} consequential {str(finding['consequential']).lower()}")
        for item in body["dispositions"]:
            finding_rows.append(f"- disposition {item['finding_id']} {item['action']}")
        files[notes_name(pass_id)] = render_face(
            notes_name(pass_id)[:-3],
            [f"Package artifact: {artifact}", *finding_rows],
        )
    for proposal in record["proposals"]:
        files[f"proposals/{proposal['finding_id']}.md"] = render_face(
            f"Proposal {proposal['finding_id']}",
            [
                f"affected: {proposal['affected_page']} {proposal['affected_file']}",
                f"target: {proposal['target']}",
                "This proposal is not written to the subject page.",
                proposal["text"],
            ],
        )
    files["08.md"] = render_face("08 — Returns and packages", pointer_rows)
    return files


def page_dir(book: Path, page: str) -> Path:
    require_investigation_page(page)
    dest = book / page
    if not within(dest, book):
        refuse("unsafe path")
    return dest


def occupied(page: Path) -> bool:
    if not os.path.lexists(page):
        return False
    if is_reparse(page):
        refuse("unsafe path")
    return any(os.scandir(page))


def create_lock(page: Path) -> None:
    flags = os.O_CREAT | os.O_EXCL | os.O_WRONLY
    if hasattr(os, "O_BINARY"):
        flags |= os.O_BINARY
    try:
        fd = os.open(str(page / ".write.lock"), flags)
    except FileExistsError:
        refuse("resume refused")
    os.close(fd)


def commit(page: Path, record: dict, extra: dict[str, bytes] | None = None) -> None:
    if os.path.lexists(page / "partial.json") or os.path.lexists(page / ".write.lock"):
        refuse("resume refused")
    if os.path.lexists(page / "investigation.json") and not os.path.lexists(page / "seal.json"):
        refuse("resume refused")
    page.mkdir(parents=True, exist_ok=True)
    create_lock(page)
    written: list[str] = []
    try:
        body = canonical(record)
        files = projections(record)
        files["investigation.json"] = body
        if extra:
            for name, data in extra.items():
                emitted_parts(name)
                files[name] = data
        names = ["investigation.json", *sorted(name for name in files if name != "investigation.json" and not name.startswith("artifacts/"))]
        for name in names:
            dest = join_under(page, name)
            write_bytes(dest, files[name])
            written.append(name)
        if extra:
            for name in sorted(extra):
                dest = join_under(page, name)
                write_bytes(dest, extra[name])
                written.append(name)
        seal_files = {}
        for name in names:
            seal_files[name] = sha256(files[name])
        seal = {"files": seal_files, "investigation_sha256": sha256(body), "schema": SEAL_SCHEMA}
        write_bytes(page / "seal.json", canonical(seal))
        written.append("seal.json")
        os.remove(page / ".write.lock")
    except Exception as exc:
        marker = {"retained": written, "resume": False, "schema": PARTIAL_SCHEMA}
        try:
            write_marker(page / "partial.json", canonical(marker))
        except OSError:
            pass
        if isinstance(exc, Refuse):
            raise Refuse(exc.reason, wrote=True)
        refuse("interrupted write", wrote=True)


def read_record_bytes(page: Path) -> dict | None:
    path = page / "investigation.json"
    if not os.path.lexists(path):
        return None
    return parse_json(read_file(path))


def health(page: Path) -> tuple[str, dict | None]:
    if not os.path.lexists(page):
        return "absent", None
    if is_reparse(page):
        refuse("unsafe path")
    info = os.lstat(page)
    if not stat.S_ISDIR(info.st_mode):
        refuse("occupied different content")
    names = {item.name for item in os.scandir(page)}
    if not names:
        return "absent", None
    if "partial.json" in names or ".write.lock" in names or "seal.json" not in names:
        return "partial", read_record_bytes(page) if "investigation.json" in names else None
    record = read_record_bytes(page)
    if not isinstance(record, dict):
        return "diverges", None
    stored = read_file(page / "investigation.json")
    seal = parse_json(read_file(page / "seal.json"))
    if not isinstance(seal, dict) or seal.get("schema") != SEAL_SCHEMA:
        return "diverges", record
    if seal.get("investigation_sha256") != sha256(stored):
        return "diverges", record
    try:
        expected = projections(record)
    except (Refuse, KeyError, TypeError):
        return "diverges", record
    expected["investigation.json"] = stored
    files = seal.get("files")
    if not isinstance(files, dict):
        return "diverges", record
    for name, digest in files.items():
        path = page / name
        if not os.path.lexists(path) or is_reparse(path):
            return "diverges", record
        blob = read_file(path)
        if sha256(blob) != digest or expected.get(name) != blob:
            return "diverges", record
    for body in record.get("passes", {}).values():
        package = body.get("package") if isinstance(body, dict) else None
        if not package:
            continue
        for item in package.get("files", []):
            path = join_under(page, package["route"] + "/" + item["path"])
            if not os.path.lexists(path):
                return "diverges", record
            blob = read_file(path)
            if sha256(blob) != item["sha256"] or len(blob) != item["bytes"]:
                return "diverges", record
    return "ok", record


def require_loaded(page: Path) -> dict:
    state, record = health(page)
    if state == "absent":
        refuse("missing investigation")
    if state == "partial":
        refuse("resume refused")
    if state != "ok" or record is None:
        refuse("projection diverges")
    return record


def titles(book: Path, skip: str) -> list[str]:
    found = []
    if not os.path.lexists(book):
        return found
    for item in os.scandir(book):
        if is_reparse(Path(item.path)):
            refuse("unsafe path")
        if not item.is_dir():
            continue
        if PAGE_RE.fullmatch(item.name) is None:
            continue
        if page_number(item.name) < 701 or page_number(item.name) > 799:
            continue
        if item.name == skip:
            continue
        state, record = health(Path(item.path))
        if state == "ok" and record is not None:
            found.append(record["title"])
        elif state == "partial":
            if record is not None and isinstance(record, dict) and "title" in record:
                found.append(record["title"])
    return found


def result(operation: str, status: str, wrote: bool, **extra) -> dict:
    body = {
        "operation": operation,
        "reason": None,
        "result": status,
        "schema": SCHEMA_NAME,
        "wrote": wrote,
    }
    body.update(extra)
    return body


def flags_of(body: dict) -> dict:
    reviews = [item for item in body["statements"] if item["kind"] == "review"]
    pointer = body["return_pointer"]
    held = any(item["action"] == "held" or item["followup_ref"] or item["park"] for item in body["dispositions"])
    accepted = any(item["action"] == "accepted" for item in body["dispositions"]) and body["closure"] is None
    return {
        "accepted_without_terminal": accepted,
        "custody_complete": pointer is not None and pointer["inspect_status"] == "complete",
        "draft": body["closure"] is None,
        "explicit_completion": body["closure"] is not None,
        "held_followup": held,
        "review_pending": (not reviews) or reviews[-1]["text"] == "PENDING",
    }


def show_page(name: str, state: str, record: dict | None) -> dict:
    if state != "ok" or record is None:
        return {"attention": [state], "page": name, "passes": [], "targets": [], "title": None}
    passes = []
    for pass_id in sorted(record["passes"]):
        body = record["passes"][pass_id]
        passes.append(
            {
                "closure": body["closure"],
                "dispositions": body["dispositions"],
                "findings": body["findings"],
                "flags": flags_of(body),
                "package_digest": None if body["package"] is None else body["package"]["digest"],
                "pass": pass_id,
                "return_pointer": body["return_pointer"],
                "statements": body["statements"],
            }
        )
    attention = []
    for item in record["reconciliation"]:
        if item["state"] == "blocked":
            attention.append(f"reconciliation {item['target']}")
    targets = []
    for target in record["targets"]:
        targets.append(
            {
                "file": target["file"],
                "id": target["id"],
                "page": target["page"],
                "section": target["section"],
                "sha256": target["source"]["sha256"],
            }
        )
    return {
        "attention": attention,
        "page": name,
        "passes": passes,
        "question": record["question"],
        "targets": targets,
        "title": record["title"],
    }


def command_show(book: Path) -> dict:
    rows = []
    for item in sorted(os.scandir(book), key=lambda entry: entry.name):
        path = Path(item.path)
        if is_reparse(path):
            refuse("unsafe path")
        if not item.is_dir() or PAGE_RE.fullmatch(item.name) is None:
            continue
        if page_number(item.name) < 701 or page_number(item.name) > 799:
            continue
        state, record = health(path)
        if state == "absent":
            continue
        rows.append(show_page(item.name, state, record))
    return result(
        "show",
        "complete",
        False,
        index={"investigations": rows, "schema": "colab-index/1", "wrote": False},
    )


def command_propose(book: Path) -> dict:
    used = set()
    for item in os.scandir(book):
        path = Path(item.path)
        if is_reparse(path):
            refuse("unsafe path")
        match = re.match(r"^(07\d{2})(?:\.|$)", item.name)
        if match:
            used.add(int(match.group(1)))
    for number in range(701, 800):
        if number not in used:
            return result("propose", "complete", False, proposal=f"{number:04d}")
    refuse("band full")


def resolve_open_sources(request: dict, sources: Path) -> None:
    if is_reparse(sources) or plain_problem(sources, "dir"):
        refuse("unsafe path")
    for target in request["targets"]:
        data = read_tree_file(sources, target["source"]["path"])
        if sha256(data) != target["source"]["sha256"]:
            refuse("stale source hash")
        resolve_section(data, target["section"])


def resolve_closure(request: dict, closure: Path) -> None:
    if is_reparse(closure) or plain_problem(closure, "dir"):
        refuse("unsafe path")
    package = closure / "package"
    manifest = parse_json(read_file(package / "source-manifest.json"))
    binding = parse_json(read_file(package / "binding.json"))
    if not isinstance(manifest, dict) or manifest.get("schema") != "prime-pack-sources/1":
        refuse("malformed package")
    rows = manifest.get("sources")
    if not isinstance(rows, list) or not rows:
        refuse("malformed package")
    found: dict[str, bytes] = {}
    for row in rows:
        if not isinstance(row, dict) or set(("bytes", "path", "sha256", "snapshot")) - set(row):
            refuse("malformed package")
        source_parts(row["path"])
        source_parts(row["snapshot"])
        data = read_file(join_under(package, row["snapshot"]))
        if sha256(data) != row["sha256"] or len(data) != row["bytes"]:
            refuse("stale source hash")
        if row["path"] in found:
            refuse("duplicate target")
        found[row["path"]] = data
    check_schema(binding, load_binding_schema())
    investigation = binding["investigation"]
    if (
        investigation["book"] != request["book"]
        or investigation["page"] != request["page"]
        or investigation["pass"] != request["pass"]
        or binding["targets"] != request["targets"]
    ):
        refuse("wrong origin")
    for target in request["targets"]:
        path = target["source"]["path"]
        if path not in found:
            refuse("unresolved section")
        data = found[path]
        if sha256(data) != target["source"]["sha256"]:
            refuse("stale source hash")
        resolve_section(data, target["section"])


def command_open(book: Path, request_path: Path, sources: Path | None, closure: Path | None) -> dict:
    request = require_open_request(parse_json(read_file(request_path)))
    if closure is not None:
        resolve_closure(request, closure)
    else:
        resolve_open_sources(request, sources)
    page = page_dir(book, request["page"])
    if request["title"] in titles(book, request["page"]):
        refuse("duplicate title")
    state, record = health(page)
    if state == "partial":
        refuse("resume refused")
    if state == "diverges":
        refuse("projection diverges")
    if state == "absent":
        commit(page, new_record(request))
        return result("open", "complete", True, page=request["page"], **{"pass": request["pass"]})
    if identity_of(record) != identity_of(request):
        refuse("occupied different content")
    if request["pass"] in record["passes"]:
        return result("open", "repeat", False, page=request["page"], **{"pass": request["pass"]})
    updated = copy.deepcopy(record)
    updated["passes"][request["pass"]] = empty_pass()
    commit(page, updated)
    return result("open", "complete", True, page=request["page"], **{"pass": request["pass"]})


def digest_preimage(files: dict[str, bytes]) -> str:
    if "request.json" not in files or "binding.json" not in files:
        refuse("malformed package")
    request = files["request.json"]
    binding = files["binding.json"]
    lines = [
        LEGACY_LABEL,
        f"request {sha256(request)} {len(request)}",
        f"binding {sha256(binding)} {len(binding)}",
    ]
    for path in sorted(files):
        if path in ("request.json", "binding.json", "verification.json"):
            continue
        data = files[path]
        lines.append(f"file {path} {sha256(data)} {len(data)}")
    return sha256(("\n".join(lines) + "\n").encode("utf-8"))


def read_package(root: Path) -> dict[str, bytes]:
    if plain_problem(root, "dir"):
        refuse("unsafe path")
    files: dict[str, bytes] = {}
    for dirpath, dirnames, filenames in os.walk(root, followlinks=False):
        kept = []
        for name in dirnames:
            child = Path(dirpath) / name
            if is_reparse(child):
                refuse("unsafe path")
            kept.append(name)
        dirnames[:] = kept
        for name in filenames:
            path = Path(dirpath) / name
            if is_reparse(path):
                refuse("unsafe path")
            info = os.lstat(path)
            if not stat.S_ISREG(info.st_mode) or info.st_nlink != 1:
                refuse("unsafe path")
            relative = path.relative_to(root).as_posix()
            relative_parts(relative)
            data = path.read_bytes()
            if len(data) > PACKAGE_BYTE_LIMIT:
                refuse("limit")
            files[relative] = data
    if len(files) > PACKAGE_FILE_LIMIT:
        refuse("limit")
    return files


def legacy_tree(files: dict[str, bytes]) -> bool:
    if "package/colab-request.json" in files:
        return False
    return "request.json" in files


def producer_file(override: Path | None) -> Path:
    return repo_root() / PRODUCER_REL if override is None else override


def config_tools(path: Path) -> dict[str, Path]:
    cfg = parse_json(read_file(path))
    if not isinstance(cfg, dict) or cfg.get("schema") != "colab-config/1":
        refuse("malformed package")
    tools = {}
    for key in ("assembler", "checker", "helper", "inspector", "python"):
        value = cfg.get(key)
        if not isinstance(value, str) or value == "" or not Path(value).is_absolute():
            refuse("unsafe path")
        tools[key] = Path(value)
    repos = cfg.get("repositories")
    if not isinstance(repos, dict) or not repos:
        refuse("malformed package")
    return tools


def pin_producer(producer: Path, tools: dict[str, Path]) -> None:
    pin_tool(producer, PRODUCER_SHA, PRODUCER_LEN)
    pin_tool(tools["assembler"], ASSEMBLER_SHA, ASSEMBLER_LEN)
    pin_tool(tools["checker"], CHECKER_SHA, CHECKER_LEN)
    pin_tool(tools["helper"], CAPTURE_SHA, CAPTURE_LEN)
    pin_tool(tools["inspector"], INSPECT_SHA, INSPECT_LEN)


def verify_producer(producer: Path, output: Path, config: Path) -> dict:
    proc = launch(
        [
            sys.executable,
            "-B",
            str(producer),
            "verify",
            "--output",
            str(output),
            "--config",
            str(config),
            "--json",
        ]
    )
    if not proc.stdout:
        refuse("malformed package")
    try:
        body = parse_json(proc.stdout)
    except Refuse:
        refuse("malformed package")
    if not isinstance(body, dict):
        refuse("malformed package")
    body["exit"] = proc.returncode
    return body


def manifest_targets(files: dict[str, bytes], record: dict) -> None:
    manifest = parse_json(files["package/source-manifest.json"])
    if not isinstance(manifest, dict) or manifest.get("schema") != "prime-pack-sources/1":
        refuse("malformed package")
    rows = manifest.get("sources")
    if not isinstance(rows, list):
        refuse("malformed package")
    by_path = {}
    for row in rows:
        if not isinstance(row, dict) or set(("bytes", "path", "sha256", "snapshot")) - set(row):
            refuse("malformed package")
        by_path[row["path"]] = row
    for target in record["targets"]:
        row = by_path.get(target["source"]["path"])
        if row is None:
            refuse("unresolved section")
        name = "package/" + row["snapshot"]
        if name not in files:
            refuse("unresolved section")
        data = files[name]
        if sha256(data) != row["sha256"] or len(data) != row["bytes"] or sha256(data) != target["source"]["sha256"]:
            refuse("stale source hash")
        resolve_section(data, target["section"])


def retained_package(files: dict[str, bytes], recorded: dict, expect: str) -> dict[str, bytes]:
    if recorded.get("schema") != "colab-package-verification/1" or recorded.get("digest") != expect:
        refuse("stale expected hash" if recorded.get("digest") not in (None, expect) else "malformed package")
    rows = recorded.get("package_files")
    if not isinstance(rows, list) or not rows:
        refuse("malformed package")
    listed = {}
    for item in rows:
        if not isinstance(item, dict) or set(("bytes", "path", "sha256")) - set(item):
            refuse("malformed package")
        listed[item["path"]] = item
    on_disk = sorted(name[len("package/") :] for name in files if name.startswith("package/"))
    if on_disk != sorted(listed):
        refuse("conflicting bytes")
    kept: dict[str, bytes] = {}
    for path, item in listed.items():
        emitted_parts(path)
        data = files["package/" + path]
        if sha256(data) != item["sha256"] or len(data) != item["bytes"]:
            refuse("conflicting bytes")
        kept["package/" + path] = data
    zip_row = recorded.get("zip")
    if not isinstance(zip_row, dict) or "prepared-colab.zip" not in files:
        refuse("malformed package")
    zip_bytes = files["prepared-colab.zip"]
    if sha256(zip_bytes) != zip_row.get("sha256") or len(zip_bytes) != zip_row.get("bytes"):
        refuse("conflicting bytes")
    kept["prepared-colab.zip"] = zip_bytes
    envelope = files["verification.json"]
    if recorded.get("request_sha256") != sha256(files["package/colab-request.json"]):
        refuse("conflicting bytes")
    kept["verification.json"] = envelope
    return kept


def provenance_for(expect: str, envelope: bytes, zip_bytes: bytes) -> bytes:
    payload = {
        "digest": expect,
        "digest_alg": DIGEST_ALG,
        "envelope_sha256": sha256(envelope),
        "pins": {
            "assembler": ASSEMBLER_SHA,
            "checker": CHECKER_SHA,
            "helper": CAPTURE_SHA,
            "inspector": INSPECT_SHA,
        },
        "producer_sha256": PRODUCER_SHA,
        "schema": PROVENANCE_SCHEMA,
        "statements": [
            "Verifier result is mechanical evidence, not authority or approval.",
            "Local config paths are not stored.",
        ],
        "verifier_result": "intact",
        "zip_sha256": sha256(zip_bytes),
    }
    data = canonical(payload)
    if b"colab-config" in data or b":\\" in data or b":/" in data:
        refuse("unsafe path")
    return data


def package_view(pass_id: str, files: dict[str, bytes], digest: str) -> dict:
    listed = []
    for path in sorted(files):
        listed.append({"bytes": len(files[path]), "path": path, "sha256": sha256(files[path])})
    return {
        "digest": digest,
        "digest_alg": DIGEST_ALG,
        "files": listed,
        "route": f"artifacts/{pass_id}",
    }


def command_legacy(package: Path) -> dict:
    files = read_package(package)
    if not legacy_tree(files):
        refuse("malformed package")
    return result(
        "legacy-diagnose",
        "legacy",
        False,
        label="legacy-synthetic-05.01",
        note="The former line-oriented preimage is not colab-package-digest/1.",
    )


def command_attach(
    book: Path,
    page_name: str,
    pass_id: str,
    output: Path,
    config: Path,
    expect: str,
    producer: Path | None,
) -> dict:
    require_pass(pass_id)
    if not isinstance(expect, str) or re.fullmatch(r"[0-9a-f]{64}", expect) is None:
        refuse("stale expected hash")
    page = page_dir(book, page_name)
    record = require_loaded(page)
    if pass_id not in record["passes"]:
        refuse("missing investigation")
    files = read_package(output)
    if legacy_tree(files):
        refuse("legacy package")
    tools = config_tools(config)
    producer_path = producer_file(producer)
    pin_producer(producer_path, tools)
    before = {name: sha256(data) for name, data in files.items()}
    report = verify_producer(producer_path, output, config)
    after = {name: sha256(read_file(join_under(output, name))) for name in files}
    if before != after:
        refuse("conflicting bytes")
    if report.get("result") == "intact" and report.get("exit") == 0:
        if report.get("digest") != expect:
            refuse("stale expected hash")
    elif report.get("result") == "partial":
        refuse("malformed package")
    else:
        refuse("conflicting bytes")
    binding = parse_json(files["package/binding.json"])
    investigation = binding["investigation"]
    if (
        investigation["book"] != record["book"]
        or investigation["page"] != record["page"]
        or investigation["pass"] != pass_id
        or binding["targets"] != record["targets"]
        or report.get("investigation") != {"book": record["book"], "page": record["page"], "pass": pass_id}
    ):
        refuse("wrong origin")
    manifest_targets(files, record)
    recorded = parse_json(files["verification.json"])
    kept = retained_package(files, recorded, expect)
    for name in files:
        if name.startswith("evaluator/") or name in ("assembler-request.json", "assembler-run.json"):
            if name in kept:
                refuse("conflicting bytes")
    kept["provenance.json"] = provenance_for(expect, kept["verification.json"], kept["prepared-colab.zip"])
    if str(config).encode("utf-8") in kept["provenance.json"] or str(output).encode("utf-8") in kept["provenance.json"]:
        refuse("unsafe path")
    stored = record["passes"][pass_id]["package"]
    view = package_view(pass_id, kept, expect)
    if stored == view:
        disk = {}
        for item in view["files"]:
            disk[item["path"]] = read_file(join_under(page, view["route"] + "/" + item["path"]))
        if disk == kept:
            return result("attach", "repeat", False, digest=expect, page=page_name, **{"pass": pass_id})
        refuse("retained artifact diverges")
    if stored is not None:
        refuse("conflicting bytes")
    extra = {f"artifacts/{pass_id}/{name}": data for name, data in kept.items()}
    updated = copy.deepcopy(record)
    updated["passes"][pass_id]["package"] = view
    commit(page, updated, extra)
    return result("attach", "complete", True, digest=expect, page=page_name, **{"pass": pass_id})


def require_statement(value) -> dict:
    require_keys(value, {"by", "kind", "on", "text"}, "statement")
    if value["kind"] not in STATEMENT_KINDS:
        refuse("claim/release unknown")
    require_text(value["by"], "by")
    if not isinstance(value["on"], str) or DATE_RE.fullmatch(value["on"]) is None:
        refuse("malformed statement")
    require_text(value["text"], "text")
    stored = dict(value)
    stored["authority"] = "recorded-statement"
    return stored


def command_statement(book: Path, page_name: str, pass_id: str, path: Path) -> dict:
    statement = require_statement(parse_json(read_file(path)))
    page = page_dir(book, page_name)
    record = require_loaded(page)
    require_pass(pass_id)
    if pass_id not in record["passes"]:
        refuse("missing investigation")
    current = [item for item in record["passes"][pass_id]["statements"] if item["kind"] == statement["kind"]]
    if current == [statement]:
        return result("record-statement", "repeat", False)
    if current:
        refuse("occupied different content")
    updated = copy.deepcopy(record)
    updated["passes"][pass_id]["statements"].append(statement)
    commit(page, updated)
    return result("record-statement", "complete", True)


def require_finding(value, targets: set[str]) -> dict:
    require_keys(
        value,
        {"affected_file", "affected_page", "consequential", "evidence_kind", "id", "observation", "target", "topic"},
        "finding",
    )
    if not isinstance(value["id"], str) or FINDING_RE.fullmatch(value["id"]) is None:
        refuse("malformed finding")
    require_text(value["topic"], "topic")
    require_text(value["observation"], "observation")
    require_subject_page(value["affected_page"])
    source_parts(value["affected_file"])
    if value["target"] not in targets:
        refuse("unresolved section")
    if not isinstance(value["consequential"], bool):
        refuse("malformed type")
    require_text(value["evidence_kind"], "evidence_kind")
    return value


def command_findings(book: Path, page_name: str, pass_id: str, path: Path) -> dict:
    parsed = parse_json(read_file(path))
    if not isinstance(parsed, list) or not parsed or len(parsed) > FINDING_LIMIT:
        refuse("limit" if isinstance(parsed, list) and len(parsed) > FINDING_LIMIT else "malformed finding")
    page = page_dir(book, page_name)
    record = require_loaded(page)
    require_pass(pass_id)
    if pass_id not in record["passes"]:
        refuse("missing investigation")
    targets = {item["id"] for item in record["targets"]}
    findings = [require_finding(item, targets) for item in parsed]
    if len({item["id"] for item in findings}) != len(findings):
        refuse("duplicate target")
    current = record["passes"][pass_id]["findings"]
    if current == findings:
        return result("record-findings", "repeat", False)
    if current:
        refuse("occupied different content")
    updated = copy.deepcopy(record)
    updated["passes"][pass_id]["findings"] = findings
    commit(page, updated)
    return result("record-findings", "complete", True)


def blocked_targets(record: dict) -> set[str]:
    return {item["target"] for item in record["reconciliation"] if item["state"] == "blocked"}


def require_disposition(value, finding_ids: set[str], target_ids: set[str], blocked: set[str]) -> dict:
    require_keys(
        value,
        {
            "action",
            "director_reply",
            "director_reply_ref",
            "finding_id",
            "followup_ref",
            "park",
            "reason",
            "reviewer",
            "source_binding",
        },
        "disposition",
    )
    if value["finding_id"] not in finding_ids:
        refuse("findings unaccounted")
    if value["action"] not in ACTIONS:
        refuse("malformed disposition")
    require_text(value["reviewer"], "reviewer")
    require_text(value["reason"], "reason")
    if not isinstance(value["director_reply"], str) or len(value["director_reply"]) > TEXT_LIMIT:
        refuse("malformed disposition")
    if any(ord(ch) < 32 or ord(ch) == 127 for ch in value["director_reply"]):
        refuse("malformed disposition")
    for label in ("director_reply_ref", "followup_ref", "park"):
        item = value[label]
        if item is not None:
            require_text(item, label)
    if value["source_binding"] not in target_ids:
        refuse("malformed disposition")
    if value["source_binding"] in blocked:
        refuse("reconciliation required")
    if value["action"] == "held" and not (value["followup_ref"] or value["park"]):
        refuse("malformed disposition")
    return value


def command_dispositions(book: Path, page_name: str, pass_id: str, path: Path) -> dict:
    parsed = parse_json(read_file(path))
    if not isinstance(parsed, list) or not parsed:
        refuse("malformed disposition")
    page = page_dir(book, page_name)
    record = require_loaded(page)
    require_pass(pass_id)
    body = record["passes"].get(pass_id)
    if body is None:
        refuse("missing investigation")
    finding_ids = {item["id"] for item in body["findings"]}
    target_ids = {item["id"] for item in record["targets"]}
    dispositions = [
        require_disposition(item, finding_ids, target_ids, blocked_targets(record)) for item in parsed
    ]
    if len({item["finding_id"] for item in dispositions}) != len(dispositions):
        refuse("duplicate target")
    known = {item["finding_id"]: item for item in body["dispositions"]}
    if all(known.get(item["finding_id"]) == item for item in dispositions) and len(known) == len(dispositions):
        return result("record-disposition", "repeat", False)
    for item in dispositions:
        if item["finding_id"] in known and known[item["finding_id"]] != item:
            refuse("occupied different content")
    updated = copy.deepcopy(record)
    merged = {item["finding_id"]: item for item in updated["passes"][pass_id]["dispositions"]}
    for item in dispositions:
        merged[item["finding_id"]] = item
    updated["passes"][pass_id]["dispositions"] = [merged[key] for key in sorted(merged)]
    commit(page, updated)
    return result("record-disposition", "complete", True)


def command_proposal(book: Path, page_name: str, pass_id: str, path: Path) -> dict:
    value = require_keys(
        parse_json(read_file(path)),
        {"affected_file", "affected_page", "finding_id", "schema", "target", "text"},
        "proposal",
    )
    if value["schema"] != "colab-subject-proposal/1":
        refuse("malformed proposal")
    page = page_dir(book, page_name)
    record = require_loaded(page)
    require_pass(pass_id)
    body = record["passes"].get(pass_id)
    if body is None:
        refuse("missing investigation")
    findings = {item["id"]: item for item in body["findings"]}
    if value["finding_id"] not in findings:
        refuse("malformed proposal")
    require_subject_page(value["affected_page"])
    source_parts(value["affected_file"])
    if value["target"] not in {item["id"] for item in record["targets"]}:
        refuse("unresolved section")
    require_text(value["text"], "text")
    current = [item for item in record["proposals"] if item["finding_id"] == value["finding_id"]]
    if current == [value]:
        return result("propose-note", "repeat", False)
    if current:
        refuse("occupied different content")
    updated = copy.deepcopy(record)
    updated["proposals"].append(value)
    updated["proposals"].sort(key=lambda item: item["finding_id"])
    commit(page, updated)
    return result("propose-note", "complete", True, wrote_subject=False)


def command_close(book: Path, page_name: str, pass_id: str, path: Path) -> dict:
    value = require_keys(parse_json(read_file(path)), {"by", "explicit", "on", "text"}, "closure")
    if value["explicit"] is not True:
        refuse("explicit close required")
    require_text(value["by"], "by")
    if DATE_RE.fullmatch(value["on"]) is None:
        refuse("malformed closure")
    require_text(value["text"], "text")
    page = page_dir(book, page_name)
    record = require_loaded(page)
    require_pass(pass_id)
    body = record["passes"].get(pass_id)
    if body is None:
        refuse("missing investigation")
    if blocked_targets(record):
        refuse("reconciliation required")
    findings = body["findings"]
    if not findings:
        refuse("findings unaccounted")
    disposed = {item["finding_id"] for item in body["dispositions"]}
    if disposed != {item["id"] for item in findings}:
        refuse("findings unaccounted")
    proposed = {item["finding_id"] for item in record["proposals"]}
    for finding in findings:
        if finding["consequential"] and finding["id"] not in proposed:
            refuse("consequential finding needs a proposal")
    if body["closure"] == value:
        return result("close", "repeat", False)
    if body["closure"] is not None:
        refuse("occupied different content")
    updated = copy.deepcopy(record)
    updated["passes"][pass_id]["closure"] = value
    commit(page, updated)
    return result("close", "complete", True)


def command_check(book: Path, page_name: str, target_id: str, current: Path) -> dict:
    page = page_dir(book, page_name)
    record = require_loaded(page)
    matches = [item for item in record["targets"] if item["id"] == target_id]
    if len(matches) != 1:
        refuse("unresolved section")
    data = read_file(current)
    observed = sha256(data)
    historical = matches[0]["source"]["sha256"]
    return result(
        "check-subject",
        "complete",
        False,
        historical_sha256=historical,
        match=observed == historical,
        observed_sha256=observed,
        target=target_id,
    )


def command_flag(book: Path, page_name: str, target_id: str, current: Path) -> dict:
    observed = command_check(book, page_name, target_id, current)
    if observed["match"]:
        return result("flag-reconciliation", "repeat", False, target=target_id)
    page = page_dir(book, page_name)
    record = require_loaded(page)
    entry = {
        "historical_sha256": observed["historical_sha256"],
        "observed_sha256": observed["observed_sha256"],
        "reason": "",
        "state": "blocked",
        "target": target_id,
    }
    current_rows = [item for item in record["reconciliation"] if item["target"] == target_id]
    if current_rows == [entry]:
        return result("flag-reconciliation", "repeat", False, target=target_id)
    if current_rows:
        refuse("occupied different content")
    updated = copy.deepcopy(record)
    updated["reconciliation"].append(entry)
    commit(page, updated)
    return result("flag-reconciliation", "complete", True, target=target_id)


def command_retain(book: Path, page_name: str, path: Path) -> dict:
    value = require_keys(parse_json(read_file(path)), {"decision", "reason", "target"}, "reconciliation")
    if value["decision"] != "retain-historical":
        refuse("retarget")
    require_text(value["reason"], "reason")
    if TARGET_RE.fullmatch(value["target"]) is None:
        refuse("malformed reconciliation")
    page = page_dir(book, page_name)
    record = require_loaded(page)
    rows = [item for item in record["reconciliation"] if item["target"] == value["target"]]
    if len(rows) != 1 or rows[0]["state"] not in ("blocked", "retained"):
        refuse("malformed reconciliation")
    retained = dict(rows[0])
    retained["state"] = "retained"
    retained["reason"] = value["reason"]
    if rows == [retained]:
        return result("retain-historical", "repeat", False)
    updated = copy.deepcopy(record)
    updated["reconciliation"] = [
        retained if item["target"] == value["target"] else item for item in updated["reconciliation"]
    ]
    historical = rows[0]["historical_sha256"]
    commit(page, updated)
    stored = require_loaded(page)
    target = [item for item in stored["targets"] if item["id"] == value["target"]][0]
    if target["source"]["sha256"] != historical:
        refuse("retarget")
    return result("retain-historical", "complete", True)


def pin_tool(path: Path, digest: str, length: int) -> None:
    if not os.path.lexists(path) or is_reparse(path):
        refuse("pin mismatch")
    info = os.lstat(path)
    if not stat.S_ISREG(info.st_mode) or info.st_nlink != 1:
        refuse("pin mismatch")
    data = path.read_bytes()
    if len(data) != length or sha256(data) != digest:
        refuse("pin mismatch")


def launch(argv: list[str]) -> subprocess.CompletedProcess:
    if RUN_PROCESS is not None:
        return RUN_PROCESS(argv)
    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    return subprocess.run(argv, shell=False, capture_output=True, env=env)


def inspect_member(helpers: Path, book: Path, member: str) -> dict:
    pin_tool(helpers / "return_capture.py", CAPTURE_SHA, CAPTURE_LEN)
    pin_tool(helpers / "return_inspect.py", INSPECT_SHA, INSPECT_LEN)
    proc = launch(
        [
            sys.executable,
            "-B",
            str(helpers / "return_inspect.py"),
            "inspect",
            "--book",
            str(book),
            "--member",
            member,
            "--json",
        ]
    )
    try:
        observed = parse_json(proc.stdout)
    except Refuse:
        refuse("custody disagreement")
    if not isinstance(observed, dict) or observed.get("status") not in INSPECT_EXIT:
        refuse("custody disagreement")
    if proc.returncode != INSPECT_EXIT[observed["status"]]:
        refuse("custody disagreement")
    return observed


def verify_member(helpers: Path, book: Path, member: str) -> tuple[int, list[str]]:
    proc = launch(
        [
            sys.executable,
            "-B",
            str(helpers / "return_capture.py"),
            "verify",
            "--book",
            str(book),
            "--member",
            member,
        ]
    )
    text = proc.stdout.decode("utf-8", errors="replace")
    return proc.returncode, text.splitlines()


def origin_matches(observed: dict, record: dict, pass_id: str) -> bool:
    capture = observed.get("capture")
    if not isinstance(capture, dict):
        return False
    origin = capture.get("origin")
    if not isinstance(origin, dict):
        return False
    return (
        origin.get("book") == record["book"]
        and origin.get("page") == record["page"]
        and origin.get("batch") == pass_id
    )


def candidate_members(book: Path) -> list[str]:
    found = []
    for item in os.scandir(book):
        path = Path(item.path)
        if is_reparse(path):
            refuse("unsafe path")
        match = MEMBER_RE.fullmatch(item.name)
        if match is None or not item.is_dir():
            continue
        number = int(match.group(1))
        if 101 <= number <= 199:
            found.append(item.name)
    return sorted(found)


def pointer_from(observed: dict, lines: list[str], secondary: bool) -> dict:
    capture = observed["capture"]
    receipt = None
    reservation = None
    manifest = None
    for line in lines:
        if line.startswith("receipt "):
            receipt = line.split(" ", 1)[1]
        elif line.startswith("reservation "):
            reservation = line.split(" ", 1)[1]
        elif line.startswith("manifest "):
            manifest = line.split(" ", 1)[1]
    if receipt != capture["receipt_sha256"]:
        refuse("custody disagreement")
    if any(line not in lines for line in CUSTODY_LINES):
        refuse("custody disagreement")
    return {
        "custody": list(CUSTODY_LINES),
        "inspect_status": "complete",
        "includes_prime_review": capture["return"]["includes_prime_review"],
        "manifest_sha256": manifest,
        "member": observed["member"],
        "origin": {
            "batch": capture["origin"]["batch"],
            "book": capture["origin"]["book"],
            "page": capture["origin"]["page"],
        },
        "receipt_sha256": receipt,
        "reservation_sha256": reservation,
        "retrospective": capture["retrospective"],
        "secondary": secondary,
    }


def classify(observed: dict, record: dict, pass_id: str) -> str:
    if observed.get("status") != "complete":
        return "partial"
    if not origin_matches(observed, record, pass_id):
        return "wrong"
    capture = observed["capture"]
    if capture.get("retrospective") is True:
        return "secondary"
    return "primary"


def command_pointer(book: Path, page_name: str, pass_id: str, member: str | None, secondary: bool, helpers: Path) -> dict:
    require_pass(pass_id)
    page = page_dir(book, page_name)
    record = require_loaded(page)
    if pass_id not in record["passes"]:
        refuse("missing investigation")
    pin_tool(helpers / "return_capture.py", CAPTURE_SHA, CAPTURE_LEN)
    pin_tool(helpers / "return_inspect.py", INSPECT_SHA, INSPECT_LEN)
    if member is None:
        names = candidate_members(book)
        observed_rows = [(name, inspect_member(helpers, book, name)) for name in names]
        primary = [row for row in observed_rows if classify(row[1], record, pass_id) == "primary"]
        later = [row for row in observed_rows if classify(row[1], record, pass_id) == "secondary"]
        if len(primary) > 1:
            refuse("ambiguous custody")
        if len(primary) == 1:
            chosen = primary[0]
            secondary = False
        elif later:
            refuse("retrospective capture is secondary")
        else:
            wrong = [row for row in observed_rows if classify(row[1], record, pass_id) == "wrong"]
            if wrong and not primary and not later:
                refuse("wrong origin")
            refuse("partial custody")
    else:
        if MEMBER_RE.fullmatch(member) is None:
            refuse("malformed member")
        observed = inspect_member(helpers, book, member)
        kind = classify(observed, record, pass_id)
        if kind == "partial":
            refuse("partial custody")
        if kind == "wrong":
            refuse("wrong origin")
        if kind == "secondary":
            if not secondary:
                refuse("retrospective capture is secondary")
            names = candidate_members(book)
            for name in names:
                if name == member:
                    continue
                other = inspect_member(helpers, book, name)
                if classify(other, record, pass_id) == "primary":
                    refuse("retrospective capture is secondary")
            chosen = (member, observed)
        else:
            chosen = (member, observed)
            secondary = False
    code, lines = verify_member(helpers, book, chosen[0])
    if code != 0:
        refuse("partial custody")
    pointer = pointer_from(chosen[1], lines, secondary)
    current = record["passes"][pass_id]["return_pointer"]
    if current == pointer:
        return result("return-pointer", "repeat", False, member=pointer["member"])
    if current is not None:
        refuse("occupied different content")
    updated = copy.deepcopy(record)
    updated["passes"][pass_id]["return_pointer"] = pointer
    commit(page, updated)
    return result("return-pointer", "complete", True, member=pointer["member"], secondary=pointer["secondary"])


def build_synthetic_package(dest: Path, request: dict, sources: dict[str, bytes]) -> str:
    """Write one contract-valid synthetic package. This is not the 0510 preparer."""
    refuse_live(dest)
    request = require_open_request(copy.deepcopy(request))
    if os.path.lexists(dest) and is_reparse(dest):
        refuse("unsafe path")
    dest.mkdir(parents=True, exist_ok=True)
    files: dict[str, bytes] = {}
    files["request.json"] = canonical(request)
    binding = binding_document(request["book"], request["page"], request["pass"], request["targets"])
    files["binding.json"] = canonical(binding)
    files["ENTRY.md"] = render_entry(request)
    files["RETURN-TEMPLATE.md"] = render_return_template()
    files[pass_name(request["pass"])] = (
        f"# {request['pass']}\n\nSupplied instructions for this synthetic package.\nPurpose: {request['purpose']}\n"
    ).encode("utf-8")
    files[notes_name(request["pass"])] = (
        f"# {notes_name(request['pass'])[:-3]}\n\nSupplied reason only. This file is not a finding list.\n"
        f"Question: {request['question']}\n"
    ).encode("utf-8")
    manifest_files = []
    for relative, data in sorted(sources.items()):
        path = "snapshots/" + relative
        files[path] = data
        manifest_files.append({"bytes": len(data), "path": path, "sha256": sha256(data)})
    files["source-manifest.json"] = canonical({"files": manifest_files, "schema": "colab-package-sources/1"})
    digest = digest_preimage(files)
    listed = []
    for path in sorted(files):
        listed.append({"bytes": len(files[path]), "path": path, "sha256": sha256(files[path])})
    files["verification.json"] = canonical(
        {
            "binding_sha256": sha256(files["binding.json"]),
            "digest": digest,
            "digest_alg": LEGACY_LABEL,
            "files": listed,
            "request_sha256": sha256(files["request.json"]),
            "schema": "colab-package-verification/1",
        }
    )
    for name, data in files.items():
        path = join_under(dest, name)
        path.parent.mkdir(parents=True, exist_ok=True)
        write_marker(path, data)
    return digest


def add_common(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--book", required=True)


def dispatch(argv: list[str]) -> dict:
    global CURRENT
    parser = argparse.ArgumentParser(prog="colab_workflow.py")
    sub = parser.add_subparsers(dest="command", required=True)
    show = sub.add_parser("show")
    add_common(show)
    propose = sub.add_parser("propose")
    add_common(propose)
    opened = sub.add_parser("open")
    add_common(opened)
    opened.add_argument("--request", required=True)
    source_group = opened.add_mutually_exclusive_group(required=True)
    source_group.add_argument("--sources")
    source_group.add_argument("--closure")
    attach = sub.add_parser("attach")
    add_common(attach)
    attach.add_argument("--page", required=True)
    attach.add_argument("--pass", dest="pass_id", required=True)
    attach.add_argument("--output", required=True)
    attach.add_argument("--config", required=True)
    attach.add_argument("--expect-digest", required=True)
    attach.add_argument("--producer", default=None)
    legacy = sub.add_parser("legacy-diagnose")
    legacy.add_argument("--package", required=True)
    statement = sub.add_parser("record-statement")
    add_common(statement)
    statement.add_argument("--page", required=True)
    statement.add_argument("--pass", dest="pass_id", required=True)
    statement.add_argument("--statement", required=True)
    findings = sub.add_parser("record-findings")
    add_common(findings)
    findings.add_argument("--page", required=True)
    findings.add_argument("--pass", dest="pass_id", required=True)
    findings.add_argument("--findings", required=True)
    dispositions = sub.add_parser("record-disposition")
    add_common(dispositions)
    dispositions.add_argument("--page", required=True)
    dispositions.add_argument("--pass", dest="pass_id", required=True)
    dispositions.add_argument("--dispositions", required=True)
    proposal = sub.add_parser("propose-note")
    add_common(proposal)
    proposal.add_argument("--page", required=True)
    proposal.add_argument("--pass", dest="pass_id", required=True)
    proposal.add_argument("--proposal", required=True)
    close = sub.add_parser("close")
    add_common(close)
    close.add_argument("--page", required=True)
    close.add_argument("--pass", dest="pass_id", required=True)
    close.add_argument("--closure", required=True)
    check = sub.add_parser("check-subject")
    add_common(check)
    check.add_argument("--page", required=True)
    check.add_argument("--target", required=True)
    check.add_argument("--current", required=True)
    flag = sub.add_parser("flag-reconciliation")
    add_common(flag)
    flag.add_argument("--page", required=True)
    flag.add_argument("--target", required=True)
    flag.add_argument("--current", required=True)
    retain = sub.add_parser("retain-historical")
    add_common(retain)
    retain.add_argument("--page", required=True)
    retain.add_argument("--statement", required=True)
    pointer = sub.add_parser("return-pointer")
    add_common(pointer)
    pointer.add_argument("--page", required=True)
    pointer.add_argument("--pass", dest="pass_id", required=True)
    pointer.add_argument("--member", default=None)
    pointer.add_argument("--secondary", action="store_true")
    pointer.add_argument("--helpers", default=None)
    try:
        args = parser.parse_args(argv)
    except SystemExit as exc:
        code = 2 if exc.code is None else int(exc.code)
        raise SystemExit(code)
    CURRENT = args.command
    if args.command == "legacy-diagnose":
        return command_legacy(require_input_dir(args.package, "package"))
    book = require_book(args.book)
    if args.command == "show":
        return command_show(book)
    if args.command == "propose":
        return command_propose(book)
    if args.command == "open":
        return command_open(
            book,
            require_abs_file(args.request, "request"),
            require_abs_dir(args.sources, "sources") if args.sources else None,
            require_input_dir(args.closure, "closure") if args.closure else None,
        )
    if args.command == "attach":
        return command_attach(
            book,
            args.page,
            args.pass_id,
            require_input_dir(args.output, "output"),
            require_input_file(args.config, "config"),
            args.expect_digest,
            require_input_file(args.producer, "producer") if args.producer else None,
        )
    if args.command == "record-statement":
        return command_statement(book, args.page, args.pass_id, require_abs_file(args.statement, "statement"))
    if args.command == "record-findings":
        return command_findings(book, args.page, args.pass_id, require_abs_file(args.findings, "findings"))
    if args.command == "record-disposition":
        return command_dispositions(book, args.page, args.pass_id, require_abs_file(args.dispositions, "dispositions"))
    if args.command == "propose-note":
        return command_proposal(book, args.page, args.pass_id, require_abs_file(args.proposal, "proposal"))
    if args.command == "close":
        return command_close(book, args.page, args.pass_id, require_abs_file(args.closure, "closure"))
    if args.command == "check-subject":
        return command_check(book, args.page, args.target, require_abs_file(args.current, "current"))
    if args.command == "flag-reconciliation":
        return command_flag(book, args.page, args.target, require_abs_file(args.current, "current"))
    if args.command == "retain-historical":
        return command_retain(book, args.page, require_abs_file(args.statement, "statement"))
    helpers = Path(args.helpers) if args.helpers else default_helpers()
    return command_pointer(book, args.page, args.pass_id, args.member, args.secondary, helpers)


def execute(argv: list[str]) -> tuple[int, bytes, bytes]:
    try:
        body = dispatch(argv)
        return 0, canonical(body), b""
    except Refuse as exc:
        body = {
            "operation": CURRENT,
            "reason": exc.reason,
            "result": "refused",
            "schema": SCHEMA_NAME,
            "wrote": exc.wrote,
        }
        return 2, canonical(body), b""
    except SystemExit as exc:
        code = 2 if exc.code is None else int(exc.code)
        return code, b"", b"usage\n"


def main(argv: list[str] | None = None) -> int:
    code, out, err = execute(sys.argv[1:] if argv is None else argv)
    if out:
        sys.stdout.buffer.write(out)
    if err:
        sys.stderr.buffer.write(err)
    return code


if __name__ == "__main__":
    sys.exit(main())
