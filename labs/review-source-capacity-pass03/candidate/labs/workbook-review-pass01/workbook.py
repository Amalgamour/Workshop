#!/usr/bin/env python3
"""Addressed workbook review. Compute prepares the form and stores Prime's judgment.

A complete return-line descriptor is recorded through the pinned review loop.
Anything else is a preliminary record. This module does not write a receipt.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import stat
import subprocess
import sys
from pathlib import Path

sys.dont_write_bytecode = True
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"

REPO = Path(r"D:\Git\lib-build")
BOOK_NAME = "00.00.10.work"
FORM_REL = "labs/workbook-review-pass01/forms/workbook-review-v1.json"
STORE = "workbook-review"
CYCLE_IDENTITY = "wb"
MAX_INDEX = 12
CUT = 400
REPARSE = 0x400

PINS = {
    "return_access": (
        "labs/return-access-pass01/return_access.py",
        "501d40d7c7b08720d3ae061441284ac26d544e7b80100059b2ddce25f67358f5",
        26561,
    ),
    "review_loop": (
        "labs/review-loop-pass03/review_loop.py",
        "47f47d16426e4d69987398a8244877de58b6089326874f3279003f696814450b",
        55474,
    ),
    "construct": (
        "labs/review-construction-pass04/construct.py",
        "6d541d4225ed0f9ccdb6263b475a79f55e4312be80a7e9a810a3622e5bd8df20",
        42582,
    ),
    "prime_cycle": (
        "labs/prime-cycle-pass03/prime_cycle.py",
        "496b4d721cfb136fa847d998d421209616c60508beb5cda5620af73041eed17c",
        76045,
    ),
    "prime_review": (
        "labs/prime-review-pass02/prime_review.py",
        "80836a13278365de863ed8231cb8118ad14ddbad672dd02ec2ebf69beff3b44e",
        58560,
    ),
    "form": (
        FORM_REL,
        None,
        None,
    ),
}

SECTION_KEYS = (
    "affected",
    "assumptions",
    "consequences",
    "exploration",
    "findings_account",
    "finish_assessments",
    "for_model",
    "issue",
    "learning",
    "limits",
    "next_bounded_action",
    "open_questions",
    "options",
    "outcome_evidence",
    "preservation",
    "prime_finding",
    "proposed_plan",
    "question",
    "recommendation",
    "remaining_choices",
    "return_result",
    "tests_note",
    "tests_passed",
    "within_direction",
)
JUDGMENT_KEYS = (
    "finding",
    "reasons",
    "operation",
    "disposition",
    "pass_terminal",
    "goal_terminal",
    "next_action",
    "semantic_conflict",
    "design_fork",
    "findings",
    "sections",
    "holds",
    "answers",
    "review_passes",
    "gaps",
)
HEADINGS = ("## Review — Codex Prime", "## Review - Codex Prime")
N5 = re.compile(r"^([0-9])5(\d\d)\.([a-z0-9][a-z0-9-]*)$")
N7 = re.compile(r"^([0-9])7(\d\d)\.([a-z0-9][a-z0-9-]*)$")
PASS = re.compile(r"^05\.\d\d$")
HEX = re.compile(r"^[0-9a-f]{64}$")
IDENT = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,63}$")
FINDING = re.compile(r"^[A-Za-z0-9][^#\r\n]{0,180}#[A-Za-z0-9][A-Za-z0-9._-]{0,63}$")
NEXT_HEADING = re.compile(r"^## [^#]")
SUB_LINE = re.compile(r"^Submission: (\S+) sha256 ([0-9a-f]{64}), ([0-9]+) bytes\.$")
MAN_LINE = re.compile(r"^Artifact manifest: (\S+) sha256 ([0-9a-f]{64}), ([0-9]+) bytes\.")
VER_LINE = re.compile(r"^Verification: (\S+) sha256 ([0-9a-f]{64}), ([0-9]+) bytes\.$")

COMMANDS = {
    "prepare": ("--book", "--source", "--pass"),
    "form": ("--book", "--source", "--pass"),
    "record": ("--book", "--source", "--pass", "--intake", "--judgment"),
    "inspect": ("--book", "--source", "--pass"),
    "publish": ("--book", "--source", "--pass", "--review"),
    "read": ("--book", "--source", "--pass"),
    "recover": ("--book", "--source", "--pass"),
}
OPTIONAL = {"record": ("--successor",)}
BANNED = {
    "--dest",
    "--fixture-root",
    "--request",
    "--decision",
    "--tool",
    "--module",
    "--executable",
    "--python",
    "--pins",
    "--member",
    "--registration",
    "--receipt",
    "--descriptor",
}


class Refusal(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message


def refuse(message: str) -> None:
    raise Refusal(message)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical(value) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def pretty(value) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")


def strict_json(data: bytes, label: str):
    if data.startswith(b"\xef\xbb\xbf"):
        refuse(f"{label} is not utf-8")
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        refuse(f"{label} is not utf-8")

    def pairs(items):
        seen = set()
        for key, _value in items:
            if key in seen:
                refuse(f"duplicate key in {label}")
            seen.add(key)
        return dict(items)

    try:
        return json.loads(text, object_pairs_hook=pairs)
    except json.JSONDecodeError:
        refuse(f"{label} is not strict json")


def is_link(path: Path) -> bool:
    try:
        info = os.lstat(path)
    except OSError:
        return False
    return stat.S_ISLNK(info.st_mode) or bool(getattr(info, "st_file_attributes", 0) & REPARSE)


def inside(child: Path, parent: Path) -> bool:
    child_s = os.path.normcase(os.path.abspath(child))
    parent_s = os.path.normcase(os.path.abspath(parent))
    if child_s == parent_s:
        return True
    prefix = parent_s if parent_s.endswith(os.sep) else parent_s + os.sep
    return child_s.startswith(prefix)


def pin_file(key: str) -> Path:
    rel, digest, size = PINS[key]
    path = REPO / rel
    if is_link(path) or not path.is_file():
        refuse(f"pin missing {rel}")
    data = path.read_bytes()
    if digest is not None and (len(data) != size or sha256_bytes(data) != digest):
        refuse(f"pin mismatch {rel}")
    return path


def load_form() -> dict:
    path = pin_file("form")
    document = strict_json(path.read_bytes(), "form declaration")
    if not isinstance(document, dict) or document.get("schema") != "workbook-review-form/1":
        refuse("form declaration schema is not workbook-review-form/1")
    if document.get("form_id") != "workbook-review-v1":
        refuse("form declaration id is not workbook-review-v1")
    fields = document.get("fields")
    if not isinstance(fields, list):
        refuse("form declaration has no fields")
    names = [item.get("name") for item in fields if isinstance(item, dict)]
    if tuple(names) != JUDGMENT_KEYS:
        refuse("form declaration fields do not match the validator")
    return document


def logical(value: str, label: str) -> str:
    if not isinstance(value, str) or value == "" or "\\" in value or value.startswith("/") or re.match(r"^[A-Za-z]:", value):
        refuse(f"unsafe path {label}")
    parts = value.split("/")
    if any(part in ("", ".", "..") for part in parts):
        refuse(f"unsafe path {label}")
    return value


def book_dir(text: str) -> Path:
    if not isinstance(text, str) or text.strip() == "":
        refuse("book is empty")
    if text.startswith("\\\\") or text.startswith("//"):
        refuse("UNC path book")
    path = Path(text)
    if not path.is_absolute() or ".." in path.parts:
        refuse("book must be an absolute path")
    if is_link(path) or not path.is_dir():
        refuse("book is not a directory")
    current = path.resolve()
    while True:
        if is_link(current):
            refuse("book ancestor is linked and was not followed")
        parent = current.parent
        if parent == current:
            break
        current = parent
    return path.resolve()


def writable(path: Path) -> None:
    if inside(path, REPO) or inside(REPO, path):
        refuse("book is inside the checkout; record and publish are refused")


def regular_file(path: Path, label: str) -> bytes:
    if is_link(path) or not path.is_file():
        refuse(f"{label} is not a regular file")
    return path.read_bytes()


def exclusive_write(path: Path, payload: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and not os.access(path, os.W_OK):
        refuse(f"target write failed; temporary kept; record kept: read-only {path.name}")
    temporary = path.with_name(path.name + ".workbook.tmp")
    if os.path.lexists(temporary):
        refuse(f"temporary name is present {temporary.name}")
    flags = os.O_CREAT | os.O_EXCL | os.O_WRONLY
    if hasattr(os, "O_BINARY"):
        flags |= os.O_BINARY
    try:
        handle = os.open(str(temporary), flags)
    except OSError as exc:
        refuse(f"cannot create temporary {path.name}: {exc.errno}")
    try:
        os.write(handle, payload)
        os.fsync(handle)
    except OSError:
        os.close(handle)
        refuse(f"partial file retained: {temporary}")
    os.close(handle)
    try:
        os.replace(temporary, path)
    except OSError as exc:
        refuse(f"target write failed; temporary kept; record kept: {exc.errno}")


def newline_of(data: bytes) -> bytes:
    if b"\r\n" in data:
        return b"\r\n"
    return b"\n"


def split_lines(data: bytes, sep: bytes) -> list[bytes]:
    if data == b"":
        return []
    parts = data.split(sep)
    if data.endswith(sep):
        parts = parts[:-1]
    return parts


def join_lines(lines: list[bytes], sep: bytes, trailing: bool) -> bytes:
    if not lines:
        return b""
    body = sep.join(lines)
    if trailing:
        body += sep
    return body


def locate_review(data: bytes) -> tuple[bytes, bytes, bytes, bytes]:
    sep = newline_of(data)
    lines = split_lines(data, sep)
    ends = data.endswith(sep)
    indexes = []
    for index, line in enumerate(lines):
        text = line.decode("utf-8")
        if text in HEADINGS:
            indexes.append(index)
    if len(indexes) != 1:
        refuse("review heading is missing or duplicated")
    start = indexes[0] + 1
    end = len(lines)
    for index in range(start, len(lines)):
        if NEXT_HEADING.match(lines[index].decode("utf-8")):
            end = index
            break
    prefix_trailing = bool(start) and (start < len(lines) or ends)
    prefix = join_lines(lines[:start], sep, trailing=prefix_trailing)
    current = join_lines(lines[start:end], sep, trailing=end < len(lines) or ends)
    suffix = join_lines(lines[end:], sep, trailing=ends if lines[end:] else False)
    if prefix + current + suffix != data:
        refuse("internal splice mismatch")
    return prefix, current, suffix, sep


def section_between(text: str, heading: str) -> str | None:
    lines = text.split("\n")
    start = None
    for index, line in enumerate(lines):
        if line == heading:
            start = index + 1
            break
    if start is None:
        return None
    end = len(lines)
    for index in range(start, len(lines)):
        if lines[index].startswith("## "):
            end = index
            break
    body = "\n".join(lines[start:end]).strip("\n")
    return body


def first_paragraph(body: str | None) -> str | None:
    if body is None:
        return None
    chunk = body.strip()
    if chunk == "":
        return None
    return chunk.split("\n\n", 1)[0].strip()


def finish_items(body: str | None) -> list[dict] | None:
    if body is None:
        return None
    items = []
    for line in body.split("\n"):
        if not line.startswith("- "):
            continue
        piece = line[2:]
        if ": " not in piece:
            continue
        ident, text = piece.split(": ", 1)
        if IDENT.fullmatch(ident) and text.strip():
            items.append({"id": ident, "text": text.strip()})
    return items


def measured_agreement(text: str) -> tuple[dict, str | None, str | None]:
    goal = first_paragraph(section_between(text, "## Goal"))
    scope = first_paragraph(section_between(text, "## Scope"))
    discretion = first_paragraph(section_between(text, "## Prime discretion"))
    required = first_paragraph(section_between(text, "## Director required"))
    criteria = finish_items(section_between(text, "## Finish"))
    director = section_between(text, "## Director - verbatim")
    if director is None:
        director = section_between(text, "## Director — verbatim")
    decisions = None
    if director is not None:
        raw = director.strip("\n").encode("utf-8")
        decisions = [{
            "id": "director-verbatim",
            "text": director.strip("\n"),
            "source_sha256": sha256_bytes(raw),
        }]
    agreement = {
        "director_required": required,
        "finish_criteria": criteria,
        "goal": goal,
        "prime_discretion": discretion,
        "recorded_decisions": decisions,
        "scope": scope,
    }
    return agreement, goal, director.strip("\n") if isinstance(director, str) else None


def pointer_block(text: str) -> str | None:
    return section_between(text, "## Return pointer")


def parse_pointer(body: str | None) -> dict:
    findings = []
    parsed = {"submission": None, "manifest": None, "state": "absent"}
    if body is None:
        findings.append({"code": "return-pointer-absent", "path": None})
        parsed["findings"] = findings
        return parsed
    stripped = body.strip()
    if stripped == "":
        findings.append({"code": "return-pointer-empty", "path": None})
        parsed["state"] = "empty"
        parsed["findings"] = findings
        return parsed
    if stripped == "PENDING.":
        findings.append({"code": "return-pending", "path": None})
        parsed["state"] = "pending"
        parsed["findings"] = findings
        return parsed
    submission = None
    manifest = None
    for raw_line in body.split("\n"):
        line = raw_line.strip()
        if line == "" or line.startswith("Invocation/claim:"):
            continue
        sub = SUB_LINE.fullmatch(line)
        man = MAN_LINE.fullmatch(line)
        if line.startswith("Submission:"):
            if submission is not None or parsed["state"] == "ambiguous":
                findings.append({"code": "ambiguous-submission", "path": None})
                submission = None
                parsed["state"] = "ambiguous"
                continue
            if sub is None:
                findings.append({"code": "unparsed-return-line", "path": None, "text": line[:180]})
                parsed["state"] = "malformed"
                submission = {"path": None, "sha256": None, "bytes": None}
                continue
        if sub:
            if submission is not None:
                findings.append({"code": "ambiguous-submission", "path": None})
                submission = None
                parsed["state"] = "ambiguous"
                continue
            submission = {"path": sub.group(1), "sha256": sub.group(2), "bytes": int(sub.group(3))}
        elif man:
            if manifest is not None:
                findings.append({"code": "ambiguous-manifest", "path": None})
                manifest = None
                parsed["state"] = "ambiguous"
                continue
            manifest = {"path": man.group(1), "sha256": man.group(2), "bytes": int(man.group(3))}
        else:
            findings.append({"code": "unparsed-return-line", "path": None, "text": line[:180]})
            parsed["state"] = "malformed"
    if parsed["state"] == "absent":
        parsed["state"] = "parsed" if not findings else "malformed"
    if parsed["state"] not in {"ambiguous", "malformed"}:
        parsed["state"] = "parsed"
    parsed["submission"] = None if parsed["state"] in {"ambiguous", "malformed"} else submission
    parsed["manifest"] = None if parsed["state"] in {"ambiguous", "malformed"} else manifest
    if parsed["state"] == "parsed" and submission is None:
        findings.append({"code": "submission-not-declared", "path": None})
    parsed["findings"] = findings
    return parsed


def cut_text(data: bytes) -> dict:
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        return {"encoding": "not-utf-8", "text": None, "truncated": False}
    short = text[:CUT]
    return {"encoding": "utf-8", "text": short, "truncated": len(text) > CUT}


def measure_declared(book: Path, spec: dict | None, role: str, rows: list, findings: list) -> dict | None:
    if not isinstance(spec, dict):
        return None
    rel = spec.get("path")
    if not isinstance(rel, str):
        findings.append({"code": "malformed-declared-path", "path": None})
        return None
    try:
        logical(rel, role)
    except Refusal:
        findings.append({"code": "malformed-declared-path", "path": None})
        return None
    path = book / rel
    if not path.is_file() or is_link(path):
        findings.append({"code": "declared-file-missing", "path": rel})
        return None
    data = path.read_bytes()
    digest = sha256_bytes(data)
    if digest != spec.get("sha256") or len(data) != spec.get("bytes"):
        findings.append({
            "code": "declared-hash-mismatch",
            "path": rel,
            "measured_sha256": digest,
            "measured_bytes": len(data),
        })
    rows.append({
        "bytes": len(data),
        "path": rel,
        "role": role,
        "sha256": digest,
    })
    return {"bytes": len(data), "cut": cut_text(data), "path": rel, "sha256": digest}


def manifest_entries(data: bytes) -> list[dict]:
    try:
        payload = json.loads(data.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        return []
    items = payload.get("files") if isinstance(payload, dict) else None
    if not isinstance(items, list):
        return []
    found = []
    for item in items:
        if isinstance(item, dict) and isinstance(item.get("path"), str):
            found.append(item)
    return found


def address_of(source: str, pass_id: str) -> dict:
    if not isinstance(source, str) or "/" in source or "\\" in source or source.strip() == "":
        refuse("source is a page id, not a path")
    if not isinstance(pass_id, str) or PASS.fullmatch(pass_id) is None:
        refuse("pass is not 05.NN")
    n5 = N5.fullmatch(source)
    n7 = N7.fullmatch(source)
    if n5 is None and n7 is None:
        return {
            "kind": None,
            "member": None,
            "missing": ["route"],
            "page": source,
            "pass": pass_id,
        }
    if n5 is not None:
        space, nn, subject = n5.groups()
        member = f"{space}1{nn}.{subject}"
        return {
            "assignment_candidates": [f"{source}/{pass_id}.md"],
            "destination": f"{source}/{pass_id}.md",
            "kind": "N5NN",
            "member": member,
            "missing": [],
            "page": source,
            "pass": pass_id,
            "return_path": f"{member}/{pass_id}.return.md",
            "target_kind": "section",
        }
    tail = pass_id.split(".", 1)[1]
    return {
        "assignment_candidates": [f"{source}/{pass_id}.pack.md", f"{source}/{pass_id}.md"],
        "destination": f"{source}/06.{tail}.review.md",
        "kind": "N7NN",
        "member": None,
        "missing": [],
        "page": source,
        "pass": pass_id,
        "return_path": f"{source}/{pass_id}.return.md",
        "target_kind": "file",
    }


def choose_assignment(book: Path, address: dict, findings: list) -> str | None:
    if address["kind"] is None:
        return None
    found = []
    for rel in address["assignment_candidates"]:
        path = book / rel
        if path.is_file() and not is_link(path):
            found.append(rel)
    if len(found) > 1:
        findings.append({"code": "ambiguous-assignment", "path": None})
        return None
    if len(found) == 0:
        findings.append({"code": "assignment-missing", "path": address["assignment_candidates"][0]})
        return None
    return found[0]


def call_json(script: Path, args: list[str]) -> tuple[int, dict | None, str]:
    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    proc = subprocess.run(
        [sys.executable, "-B", str(script), *args],
        cwd=str(REPO),
        env=env,
        capture_output=True,
        shell=False,
    )
    err = proc.stderr.decode("utf-8", "replace")
    try:
        payload = json.loads(proc.stdout.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        payload = None
    if not isinstance(payload, dict):
        payload = None
    return proc.returncode, payload, err


def lookup_custody(book: Path, source: str, pass_id: str) -> dict:
    script = pin_file("return_access")
    code, payload, err = call_json(script, ["lookup", "--book", str(book), "--source", source, "--pass", pass_id])
    return {"exit": code, "payload": payload, "stderr": err.strip()[:600]}


def descriptor_facts(lookup: dict) -> dict:
    payload = lookup.get("payload") if isinstance(lookup, dict) else None
    descriptor = payload.get("descriptor") if isinstance(payload, dict) else None
    facts = {
        "accepted": False,
        "approved": False,
        "descriptor": descriptor if isinstance(descriptor, dict) else None,
        "missing": payload.get("missing") if isinstance(payload, dict) and isinstance(payload.get("missing"), list) else [],
        "published": False,
        "state": payload.get("state") if isinstance(payload, dict) else None,
        "task_association": "not-established",
    }
    return facts


def filed_ready(book: Path, facts: dict) -> bool:
    descriptor = facts.get("descriptor")
    if not isinstance(descriptor, dict):
        return False
    if descriptor.get("schema") not in {"return-line-descriptor/1", "return-line-descriptor/2"}:
        return False
    if descriptor.get("state") != "complete":
        return False
    digest = descriptor.get("receipt_sha256")
    rel = descriptor.get("receipt_path")
    if not isinstance(digest, str) or HEX.fullmatch(digest) is None or not isinstance(rel, str):
        return False
    try:
        logical(rel, "receipt")
    except Refusal:
        return False
    path = book / rel
    if not path.is_file() or is_link(path):
        return False
    data = path.read_bytes()
    return sha256_bytes(data) == digest


def add_row(rows: list, seen: set, path: str, data: bytes, role: str) -> None:
    if path in seen:
        return
    seen.add(path)
    rows.append({"bytes": len(data), "path": path, "role": role, "sha256": sha256_bytes(data)})


def build_intake(book: Path, source: str, pass_id: str) -> dict:
    for key in ("return_access", "prime_review", "form"):
        pin_file(key)
    address = address_of(source, pass_id)
    findings = []
    if address["kind"] is None:
        instance = sha256_bytes(canonical({"book": str(book), "pass": pass_id, "source": source}))
        return {
            "agreement": {},
            "artifact_paths": [],
            "assignment_path": None,
            "book": str(book),
            "custody": "missing",
            "cuts": [],
            "descriptor_schema": None,
            "destination": None,
            "director_text": None,
            "findings": [{"code": "route-undeclared", "path": None}],
            "goal_statement": None,
            "instance_id": instance,
            "intake_id": instance,
            "kind": None,
            "lookup_exit": None,
            "member": None,
            "missing": ["route"],
            "page": source,
            "pass": pass_id,
            "receipt_sha256": None,
            "return_path": None,
            "rows": [],
            "schema": "workbook-review-intake/1",
            "submission_id": None,
            "target_kind": None,
            "unknowns": ["route"],
        }
    assignment = choose_assignment(book, address, findings)
    rows = []
    seen = set()
    page_text = ""
    agreement = {
        "director_required": None,
        "finish_criteria": None,
        "goal": None,
        "prime_discretion": None,
        "recorded_decisions": None,
        "scope": None,
    }
    goal = None
    director = None
    if assignment is not None:
        data = regular_file(book / assignment, "assignment")
        add_row(rows, seen, assignment, data, "assignment")
        page_text = data.decode("utf-8", "replace")
        agreement, goal, director = measured_agreement(page_text)
    if assignment is None and address["kind"] is not None:
        pointer = {"findings": [], "manifest": None, "state": "absent", "submission": None}
        for rel in address["assignment_candidates"]:
            candidate = book / rel
            if not candidate.is_file() or is_link(candidate):
                continue
            text = candidate.read_bytes().decode("utf-8", "replace")
            parsed = parse_pointer(pointer_block(text))
            pointer["findings"].extend(parsed["findings"])
            if parsed["state"] == "ambiguous":
                pointer["state"] = "ambiguous"
    else:
        pointer = parse_pointer(pointer_block(page_text) if assignment else None)
    findings.extend(pointer["findings"])
    cuts = []
    if assignment is not None:
        cuts.append({"path": assignment, "role": "assignment", **cut_text((book / assignment).read_bytes())})
    declared_return = None
    submission = measure_declared(book, pointer.get("submission"), "submission", [], findings)
    if submission is not None:
        add_row(rows, seen, submission["path"], (book / submission["path"]).read_bytes(), "submission")
        cuts.append({"path": submission["path"], "role": "submission", **submission["cut"]})
        sub_text = (book / submission["path"]).read_bytes().decode("utf-8", "replace")
        verification = None
        for line in sub_text.split("\n"):
            match = VER_LINE.fullmatch(line.strip())
            if match:
                verification = {"path": match.group(1), "sha256": match.group(2), "bytes": int(match.group(3))}
        if verification is None and "verification" in sub_text.lower():
            findings.append({"code": "verification-not-measured", "path": submission["path"]})
        measured_verification = measure_declared(book, verification, "verification", [], findings)
        if measured_verification is not None:
            add_row(rows, seen, measured_verification["path"], (book / measured_verification["path"]).read_bytes(), "verification")
            cuts.append({"path": measured_verification["path"], "role": "verification", **measured_verification["cut"]})
        if len(sub_text) < 400 and measured_verification is None:
            findings.append({"code": "thin-submission", "path": submission["path"]})
    manifest = measure_declared(book, pointer.get("manifest"), "artifact-manifest", [], findings)
    extra = []
    if manifest is not None:
        add_row(rows, seen, manifest["path"], (book / manifest["path"]).read_bytes(), "artifact-manifest")
        entries = manifest_entries((book / manifest["path"]).read_bytes())
        if len(entries) > MAX_INDEX:
            findings.append({"code": "index-truncated", "path": manifest["path"], "count": len(entries)})
        for item in entries[:MAX_INDEX]:
            rel = item.get("path")
            if not isinstance(rel, str):
                continue
            try:
                logical(rel, "artifact")
            except Refusal:
                findings.append({"code": "malformed-declared-path", "path": None})
                continue
            candidate = book / rel
            if not candidate.is_file() or is_link(candidate):
                findings.append({"code": "artifact-not-in-book", "path": rel})
                continue
            blob = candidate.read_bytes()
            digest = sha256_bytes(blob)
            declared = item.get("sha256")
            if isinstance(declared, str) and declared != digest:
                findings.append({"code": "artifact-hash-mismatch", "path": rel, "measured_sha256": digest})
            add_row(rows, seen, rel, blob, "artifact")
            extra.append(rel)
    lookup = lookup_custody(book, source, pass_id)
    facts = descriptor_facts(lookup)
    descriptor = facts["descriptor"]
    custody = "missing"
    receipt_sha = None
    descriptor_schema = None
    submission_id = None
    return_path = address["return_path"]
    if isinstance(descriptor, dict):
        descriptor_schema = descriptor.get("schema") if isinstance(descriptor.get("schema"), str) else None
        submission_id = descriptor.get("submission_id") if isinstance(descriptor.get("submission_id"), str) else None
        described = descriptor.get("return_path") if isinstance(descriptor.get("return_path"), str) else None
        if described and described != return_path:
            findings.append({"code": "return-path-disagreement", "path": described})
            return_path = None
        elif described:
            return_path = described
        if filed_ready(book, facts):
            custody = "complete-descriptor"
            receipt_sha = descriptor.get("receipt_sha256")
        else:
            custody = "not-complete"
            findings.append({"code": "custody-not-complete", "path": None})
    else:
        findings.append({"code": "custody-missing", "path": address["member"]})
        for item in facts["missing"]:
            findings.append({"code": "lookup-missing", "path": None, "text": str(item)[:180]})
    if return_path is not None:
        candidate = book / return_path
        if candidate.is_file() and not is_link(candidate):
            add_row(rows, seen, return_path, candidate.read_bytes(), "return")
            cuts.append({"path": return_path, "role": "return", **cut_text(candidate.read_bytes())})
        else:
            findings.append({"code": "return-missing", "path": return_path})
            if custody != "complete-descriptor":
                return_path = None
    unknowns = []
    if agreement["goal"] is None:
        unknowns.append("agreement.goal")
    if agreement["scope"] is None:
        unknowns.append("agreement.scope")
    if agreement["recorded_decisions"] is None:
        unknowns.append("recorded_decisions")
    if custody != "complete-descriptor":
        unknowns.append("receipt")
    instance = sha256_bytes(canonical({"book": str(book), "pass": pass_id, "source": source}))
    intake = {
        "agreement": agreement,
        "assignment_path": assignment,
        "book": str(book),
        "custody": custody,
        "descriptor_schema": descriptor_schema,
        "destination": address["destination"],
        "director_text": director,
        "findings": findings,
        "goal_statement": goal,
        "instance_id": instance,
        "kind": address["kind"],
        "lookup_exit": lookup.get("exit"),
        "member": address["member"],
        "missing": address["missing"],
        "page": source,
        "pass": pass_id,
        "receipt_sha256": receipt_sha,
        "return_path": return_path if return_path in seen else None,
        "rows": rows,
        "schema": "workbook-review-intake/1",
        "submission_id": submission_id,
        "target_kind": address["target_kind"],
        "unknowns": unknowns,
    }
    intake["intake_id"] = sha256_bytes(canonical({key: value for key, value in intake.items() if key != "intake_id"}))
    intake["cuts"] = cuts
    intake["artifact_paths"] = extra
    return intake


def form_view(intake: dict, document: dict) -> dict:
    path = REPO / FORM_REL
    data = path.read_bytes()
    return {
        "bindings": {
            "custody": intake["custody"],
            "destination": intake["destination"],
            "director_text": intake["director_text"],
            "findings": intake["findings"],
            "instance_id": intake["instance_id"],
            "intake_id": intake["intake_id"],
            "kind": intake["kind"],
            "member": intake["member"],
            "return_path": intake["return_path"],
            "rows": intake["rows"],
            "unknowns": intake["unknowns"],
        },
        "correction_help": document.get("correction_help"),
        "declaration": {"bytes": len(data), "path": FORM_REL, "sha256": sha256_bytes(data)},
        "fields": document["fields"],
        "form_id": document["form_id"],
        "not_submitted": document.get("not_submitted"),
        "schema": "workbook-review-form/1",
    }


def flags() -> dict:
    return {
        "accepted": False,
        "approved": False,
        "authority": "none",
        "closes_work": False,
        "eligible_for_custody_completion": False,
        "published_work": False,
        "releases_action": False,
        "task_association": "not-established",
    }


def result(command: str, intake: dict | None, exit_code: int, **extra) -> dict:
    body = {
        "command": command,
        "exit": exit_code,
        "schema": "workbook-review-result/1",
    }
    body.update(flags())
    if intake is not None:
        body["instance_id"] = intake["instance_id"]
        body["intake_id"] = intake["intake_id"]
        body["kind"] = intake["kind"]
        body["page"] = intake["page"]
        body["pass"] = intake["pass"]
    body.update(extra)
    return body


def store_root(book: Path, intake: dict) -> Path:
    return book / STORE / intake["page"] / intake["pass"]


def read_stored_intake(book: Path, intake: dict) -> dict | None:
    path = store_root(book, intake) / "intake.json"
    if not path.is_file() or is_link(path):
        return None
    payload = strict_json(path.read_bytes(), "stored intake")
    return payload if isinstance(payload, dict) else None


def save_failed(book: Path, intake: dict, raw: bytes, correction: str) -> str:
    folder = store_root(book, intake) / "failed"
    folder.mkdir(parents=True, exist_ok=True)
    name = sha256_bytes(raw)[:16] + ".json"
    path = folder / name
    if not path.exists():
        exclusive_write(path, raw)
    note = folder / (sha256_bytes(raw)[:16] + ".correction.txt")
    if not note.exists():
        exclusive_write(note, (correction + "\n").encode("utf-8"))
    return f"{STORE}/{intake['page']}/{intake['pass']}/failed/{name}"


def correction_for(document: dict, name: str, state: str) -> str:
    meaning = ""
    for field in document["fields"]:
        if field["name"] == name:
            meaning = field.get("meaning") or ""
    route = (document.get("correction_help") or {}).get("route")
    return f"{name} is {state}. {meaning} Route: {route}."


def parse_judgment(raw: bytes, document: dict) -> dict:
    payload = strict_json(raw, "judgment")
    if not isinstance(payload, dict):
        refuse(correction_for(document, "finding", "wrong-type"))
    if set(payload) != set(JUDGMENT_KEYS):
        extra = sorted(set(payload) - set(JUDGMENT_KEYS))
        missing = sorted(set(JUDGMENT_KEYS) - set(payload))
        if extra:
            refuse("extra judgment field " + extra[0] + ". " + correction_for(document, "finding", "extra"))
        refuse(correction_for(document, missing[0], "absent"))
    if not isinstance(payload["finding"], str) or payload["finding"].strip() == "":
        refuse(correction_for(document, "finding", "empty"))
    if not isinstance(payload["reasons"], list) or any(not isinstance(item, str) or item.strip() == "" for item in payload["reasons"]):
        refuse(correction_for(document, "reasons", "wrong-type"))
    if payload["operation"] not in {"continue", "director-input", "develop", "complete"}:
        refuse(correction_for(document, "operation", "wrong-type"))
    if payload["disposition"] not in {"accepted", "held", "correction-required"}:
        refuse(correction_for(document, "disposition", "wrong-type"))
    if payload["pass_terminal"] not in {"finished", "open"}:
        refuse(correction_for(document, "pass_terminal", "wrong-type"))
    if payload["goal_terminal"] not in {"completed", "open"}:
        refuse(correction_for(document, "goal_terminal", "wrong-type"))
    if not isinstance(payload["next_action"], str) or payload["next_action"].strip() == "":
        refuse(correction_for(document, "next_action", "empty"))
    if payload["semantic_conflict"] is not None and not isinstance(payload["semantic_conflict"], bool):
        refuse(correction_for(document, "semantic_conflict", "wrong-type"))
    if not isinstance(payload["findings"], list) or not isinstance(payload["holds"], list):
        refuse(correction_for(document, "findings", "wrong-type"))
    if not isinstance(payload["answers"], list) or not isinstance(payload["review_passes"], list) or not isinstance(payload["gaps"], list):
        refuse(correction_for(document, "answers", "wrong-type"))
    if any(not isinstance(item, str) or item.strip() == "" for item in payload["gaps"]):
        refuse(correction_for(document, "gaps", "wrong-type"))
    for item in payload["findings"]:
        if not isinstance(item, dict) or set(item) != {"disposition", "finding_id", "text"}:
            refuse(correction_for(document, "findings", "wrong-type"))
        if item["disposition"] not in {"answered", "fixed", "elevated"}:
            refuse(correction_for(document, "findings", "wrong-type"))
        if not isinstance(item["text"], str) or item["text"].strip() == "" or FINDING.fullmatch(item["finding_id"] or "") is None:
            refuse(correction_for(document, "findings", "wrong-type"))
    sections = payload["sections"]
    if not isinstance(sections, dict) or set(sections) != set(SECTION_KEYS):
        refuse(correction_for(document, "sections", "wrong-type"))
    if sections["tests_passed"] is not None and not isinstance(sections["tests_passed"], bool):
        refuse("tests_passed is wrong-type. Null is unknown, not passed.")
    complete = payload["operation"] == "complete"
    if complete != (payload["goal_terminal"] == "completed"):
        refuse("operation complete must match goal_terminal completed")
    if complete and (payload["disposition"] != "accepted" or payload["pass_terminal"] != "finished"):
        refuse("a completed operation needs disposition accepted and pass finished")
    if payload["operation"] == "director-input" and payload["disposition"] != "held":
        refuse("director-input requires disposition held")
    if payload["disposition"] in {"held", "correction-required"} and (
        payload["pass_terminal"] != "open" or payload["goal_terminal"] != "open"
    ):
        refuse("a held review keeps the pass and the goal open")
    fork = payload["design_fork"]
    if fork is not None:
        if not isinstance(fork, dict) or set(fork) != {"id", "text"}:
            refuse(correction_for(document, "design_fork", "wrong-type"))
        if not isinstance(fork["id"], str) or IDENT.fullmatch(fork["id"]) is None or not isinstance(fork["text"], str) or fork["text"].strip() == "":
            refuse(correction_for(document, "design_fork", "wrong-type"))
    return payload


def review_id_for(intake_id: str, judgment: dict) -> str:
    digest = sha256_bytes(canonical({"intake_id": intake_id, "judgment": judgment}))
    return "w" + digest[:16]


def source_row(path: str, data: bytes, kind: str, identity: dict, bind: bool) -> dict:
    digest = sha256_bytes(data)
    text = None
    try:
        decoded = data.decode("utf-8")
        if len(decoded) <= 12000:
            text = decoded
    except UnicodeDecodeError:
        text = None
    return {
        "bind": bind,
        "content_bytes": len(data),
        "content_sha256": digest,
        "identity": identity,
        "kind": kind,
        "logical_path": path,
        "prior_content_sha256": None,
        "prior_transport_sha256": None,
        "record": text,
        "transport_bytes": len(data),
        "transport_sha256": digest,
    }


def prime_record(intake: dict, judgment: dict, capture: dict | None) -> dict:
    sources = []
    bind = capture is None
    for row in intake["rows"]:
        if capture is not None and row["role"] not in {"assignment", "artifact", "return"}:
            continue
        if row["role"] == "assignment":
            blob = (Path(intake["book"]) / row["path"]).read_bytes()
            sources.append(source_row(row["path"], blob, "page", {"schema": "page-bytes/1"}, bind))
        elif row["role"] == "return" and capture is not None and row["path"] == capture["return_path"]:
            blob = (Path(intake["book"]) / row["path"]).read_bytes()
            sources.append(source_row(row["path"], blob, "capture", capture["identity"], bind))
        elif row["role"] in {"return", "artifact", "submission", "verification"}:
            blob = (Path(intake["book"]) / row["path"]).read_bytes()
            sources.append(source_row(row["path"], blob, "supplied-text", {"schema": "supplied-text/1", "label": "SUPPLIED"}, bind))
    if not sources and intake["assignment_path"]:
        blob = (Path(intake["book"]) / intake["assignment_path"]).read_bytes()
        sources.append(source_row(intake["assignment_path"], blob, "page", {"schema": "page-bytes/1"}, bind))
    return {
        "agreement": intake["agreement"],
        "answers": judgment["answers"],
        "attribution": {
            "actor_label": "Codex Prime (supplied)",
            "evidence": "The actor label is not authentication.",
            "role": "prime",
        },
        "gaps": judgment["gaps"],
        "holds": judgment["holds"],
        "judgment": {
            "design_fork": judgment["design_fork"],
            "finding": judgment["finding"],
            "next_action": judgment["next_action"],
            "outcome": judgment["operation"],
            "reasons": judgment["reasons"],
            "sections": judgment["sections"],
            "semantic_conflict": judgment["semantic_conflict"],
        },
        "review_passes": judgment["review_passes"],
        "schema": "prime-review-record/1",
        "sources": sources,
    }


def call_prime(book: Path, record: dict) -> tuple[int, dict | None, str]:
    script = pin_file("prime_review")
    folder = book / STORE / "tmp"
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / "prime-input.json"
    exclusive_write(path, pretty(record))
    return call_json(script, ["report", "--input", str(path), "--root", str(book), "--json"])


def cycle_paths(book: Path) -> dict:
    base = f"{STORE}/cycle"
    return {
        "decision": f"{base}/decision.json",
        "descriptor": f"{base}/descriptor.json",
        "registration": f"{base}/registration.json",
        "request": f"{base}/request.json",
    }


def write_cycle_inputs(book: Path, intake: dict, review_id: str) -> None:
    descriptor = descriptor_facts(lookup_custody(book, intake["page"], intake["pass"]))["descriptor"]
    if not isinstance(descriptor, dict):
        refuse("descriptor disappeared before the cycle call")
    paths = cycle_paths(book)
    exclusive_write(book / paths["descriptor"], pretty(descriptor))
    evidence = []
    for row in intake["rows"]:
        if row["role"] == "artifact":
            evidence.append({"label": "supplied", "logical_path": row["path"]})
    kind = intake["kind"]
    if kind == "N5NN":
        kernel = f"00.kernel/00.00.10.work/{intake['page']}/{intake['pass']}.md"
        target = intake["assignment_path"]
    else:
        kernel = f"00.kernel/00.00.10.work/{intake['page']}/{intake['pass']}.pack.md"
        target = intake["destination"]
    if not isinstance(intake["goal_statement"], str) or intake["goal_statement"].strip() == "":
        refuse("goal statement was not measured")
    if not isinstance(intake["submission_id"], str) or IDENT.fullmatch(intake["submission_id"]) is None:
        refuse("submission id is not a cycle label")
    registration = {
        "agreement": intake["agreement"],
        "assignment_path": intake["assignment_path"],
        "book": BOOK_NAME,
        "bounds": {"max_output_bytes": 2097152},
        "descriptor_path": paths["descriptor"],
        "evidence": evidence,
        "goal": {
            "evidence": [],
            "goal_id": "g1",
            "statement": intake["goal_statement"],
            "terminal": "open",
        },
        "kernel_page": kernel,
        "page_id": intake["page"],
        "pass": intake["pass"],
        "receipt_label": "supplied",
        "review_identity": CYCLE_IDENTITY,
        "review_location": f"{STORE}/cycle-records",
        "schema": "prime-cycle-registration/2",
        "source_kind": kind,
        "submission_id": intake["submission_id"],
        "target": target,
        "task_id": "task-" + intake["pass"].replace(".", ""),
        "work_id": intake["page"],
    }
    if registration["assignment_path"] is None or registration["target"] is None:
        refuse("assignment path was not measured")
    exclusive_write(book / paths["registration"], pretty(registration))
    exclusive_write(book / paths["request"], pretty({
        "registration_path": paths["registration"],
        "schema": "review-loop-request/1",
    }))


def capture_identity(book: Path, intake: dict) -> dict | None:
    facts = descriptor_facts(lookup_custody(book, intake["page"], intake["pass"]))
    descriptor = facts["descriptor"]
    if not isinstance(descriptor, dict) or intake["kind"] != "N5NN":
        return None
    member = intake["member"]
    if not isinstance(member, str):
        return None
    return {
        "identity": {
            "member": member,
            "origin": {"batch": intake["pass"], "book": BOOK_NAME, "page": intake["page"]},
            "receipt_sha256": descriptor.get("receipt_sha256"),
            "schema": "return-capture/1",
            "submission_id": descriptor.get("submission_id"),
        },
        "return_path": descriptor.get("return_path"),
    }


def attempt_cycle(book: Path, intake: dict, judgment: dict, review_id: str) -> dict:
    pin_file("review_loop")
    pin_file("construct")
    pin_file("prime_cycle")
    try:
        write_cycle_inputs(book, intake, review_id)
    except Refusal as exc:
        return {"called": False, "error": exc.message, "committed": False}
    loop = pin_file("review_loop")
    paths = cycle_paths(book)
    code, view, err = call_json(loop, ["prepare", "--fixture-root", str(book), "--request", paths["request"]])
    template = None
    if isinstance(view, dict):
        inner = view.get("view") if isinstance(view.get("view"), dict) else view
        if isinstance(inner, dict):
            template = inner.get("template")
    if code != 0 or not isinstance(template, dict):
        detail = err.strip() or (view.get("rule") if isinstance(view, dict) else None) or "cycle prepare did not return a template"
        return {"called": True, "error": str(detail)[:600], "committed": False, "prepare_exit": code}
    statement = intake["goal_statement"].encode("utf-8")
    cycle_judgment = {
        "answers": judgment["answers"],
        "design_fork": judgment["design_fork"],
        "disposition": judgment["disposition"],
        "finding": judgment["finding"],
        "goal": {
            "evidence": [intake["assignment_path"]] if judgment["operation"] == "complete" else [],
            "goal_id": "g1",
            "goal_sha256": sha256_bytes(statement),
            "terminal": judgment["goal_terminal"],
        },
        "holds": judgment["holds"],
        "next_action": {"action_id": "next", "authorized_in_grant": None, "text": judgment["next_action"]},
        "outcome": judgment["operation"],
        "pass_terminal": judgment["pass_terminal"],
        "reasons": judgment["reasons"],
        "sections": judgment["sections"],
        "semantic_conflict": judgment["semantic_conflict"],
        "source_refs": [intake["assignment_path"]] if intake["assignment_path"] else [],
        "unresolved": list(judgment["gaps"]),
    }
    capture = capture_identity(book, intake) if intake["kind"] == "N5NN" else None
    supplied = prime_record(intake, judgment, capture)
    decision = dict(template)
    cycle_review_id = f"{intake['pass']}-{CYCLE_IDENTITY}"
    decision["review_id"] = cycle_review_id
    decision["attribution"] = supplied["attribution"]
    decision["judgment"] = cycle_judgment
    decision["supplied_record"] = supplied
    exclusive_write(book / paths["decision"], pretty(decision))
    record_code, record_view, record_err = call_json(
        loop,
        ["record", "--fixture-root", str(book), "--request", paths["request"], "--decision", paths["decision"]],
    )
    committed = isinstance(record_view, dict) and record_code in {0, 1}
    inner_result = None
    if isinstance(record_view, dict):
        nested = record_view.get("record") if isinstance(record_view.get("record"), dict) else record_view
        inner_result = nested.get("result") if isinstance(nested, dict) else None
    if inner_result not in {"recorded", "already-recorded"}:
        committed = False
    return {
        "called": True,
        "committed": committed,
        "error": None if committed else (record_err.strip() or str(inner_result) or "cycle record was not committed")[:600],
        "cycle_record": f"{STORE}/cycle-records/{cycle_review_id}/record.json",
        "cycle_review_id": cycle_review_id,
        "record_exit": record_code,
        "result": inner_result,
        "review_id": review_id,
    }


def render_body(record: dict) -> str:
    judgment = record["judgment"]
    lines = [
        "authority: none",
        "closes_work: false",
        "releases_action: false",
        "authenticates_actor: false",
        f"workbook-review-id: {record['review_id']}",
        f"mode: {record['mode']}",
        f"custody: {record['custody']}",
        "task_association: not-established",
        "This record is not approval, filing, or release.",
        "",
        "### Judgment",
        f"operation: {judgment['operation']}",
        f"disposition: {judgment['disposition']}",
        f"finding: {judgment['finding']}",
        "",
        "### Reasons",
    ]
    if judgment["reasons"]:
        lines.extend(f"- {reason}" for reason in judgment["reasons"])
    else:
        lines.append("none supplied")
    lines.extend(["", "### Findings"])
    if judgment["findings"]:
        for item in judgment["findings"]:
            lines.append(f"- {item['finding_id']} {item['disposition']}: {item['text']}")
    else:
        lines.append("none supplied")
    lines.extend(["", "### Director text"])
    director = record.get("director_text")
    lines.append(director if isinstance(director, str) and director.strip() else "none measured")
    lines.extend(["", "### Answers"])
    if judgment["answers"]:
        for answer in judgment["answers"]:
            reply = answer.get("reply") if isinstance(answer, dict) else None
            lines.append(reply if isinstance(reply, str) else "none supplied")
    else:
        lines.append("none supplied")
    lines.extend(["", "### Next action", judgment["next_action"], "This line is not a release.", ""])
    tests = judgment["sections"].get("tests_passed")
    if tests is True:
        lines.append("tests_passed: true")
    elif tests is False:
        lines.append("tests_passed: false")
    else:
        lines.append("tests_passed: none supplied")
    effective = record.get("prime_review_effective")
    lines.append(f"prime_review_effective: {effective if effective is not None else 'not-run'}")
    if record.get("cycle_error"):
        lines.append(f"cycle_error: {record['cycle_error']}")
    lines.append(f"eligible_for_custody_completion: {str(record['eligible_for_custody_completion']).lower()}")
    text = "\n".join(lines) + "\n"
    if "\r" in text or any(NEXT_HEADING.match(line) for line in text.split("\n")):
        refuse("rendered review contains a page heading")
    return text


def journal_path(book: Path, intake: dict) -> Path:
    return store_root(book, intake) / "journal.json"


def load_journal(book: Path, intake: dict) -> dict:
    path = journal_path(book, intake)
    if not path.is_file():
        return {"current": None, "reviews": [], "schema": "workbook-review-journal/1"}
    payload = strict_json(path.read_bytes(), "journal")
    if not isinstance(payload, dict):
        refuse("journal is not an object")
    return payload


def save_journal(book: Path, intake: dict, journal: dict) -> None:
    exclusive_write(journal_path(book, intake), pretty(journal))


def record_path(book: Path, intake: dict, review_id: str) -> Path:
    return store_root(book, intake) / "reviews" / review_id / "record.json"


def load_record(book: Path, intake: dict, review_id: str) -> dict:
    path = record_path(book, intake, review_id)
    payload = strict_json(regular_file(path, "review record"), "review record")
    if not isinstance(payload, dict):
        refuse("review record is not an object")
    return payload


def vacant(body: bytes) -> bool:
    text = body.decode("utf-8", "replace").replace("\r\n", "\n").strip()
    return text in {"", "PENDING."}


def our_marker(body: bytes, review_id: str) -> bool:
    return f"workbook-review-id: {review_id}".encode("utf-8") in body.replace(b"\r\n", b"\n")


def do_prepare(book: Path, source: str, pass_id: str) -> dict:
    document = load_form()
    intake = build_intake(book, source, pass_id)
    stored = read_stored_intake(book, intake)
    stale = False
    stored_id = None
    if isinstance(stored, dict):
        stored_id = stored.get("intake_id")
        stale = stored_id != intake["intake_id"]
    exit_code = 2 if "route" in intake.get("missing", []) else 0
    return result(
        "prepare",
        intake,
        exit_code,
        custody=intake["custody"],
        cuts=intake["cuts"],
        destination=intake["destination"],
        director_text=intake["director_text"],
        findings=intake["findings"],
        form=form_view(intake, document),
        live_intake_id=intake["intake_id"],
        missing=list(intake.get("missing") or []),
        stale=stale,
        stored_intake_id=stored_id,
        unknowns=intake["unknowns"],
    )


def do_record(book: Path, source: str, pass_id: str, intake_id: str, judgment_path: Path, successor: str | None) -> dict:
    writable(book)
    document = load_form()
    intake = build_intake(book, source, pass_id)
    if intake["kind"] is None:
        return result("record", intake, 2, correction="missing route", missing=["route"], recorded=False)
    raw = regular_file(judgment_path, "judgment")
    try:
        judgment = parse_judgment(raw, document)
    except Refusal as exc:
        failed = save_failed(book, intake, raw, exc.message)
        return result("record", intake, 2, correction=exc.message, failed_input=failed, judgment=None, recorded=False)
    stored = read_stored_intake(book, intake)
    if isinstance(stored, dict) and stored.get("intake_id") != intake["intake_id"]:
        failed = save_failed(book, intake, raw, "stored intake differs from the live measurement")
        return result(
            "record",
            intake,
            2,
            correction="The stored intake was kept. This entry does not repin.",
            failed_input=failed,
            recorded=False,
            stale=True,
            stored_intake_id=stored.get("intake_id"),
        )
    if intake_id != intake["intake_id"]:
        failed = save_failed(book, intake, raw, "intake id does not match the live measurement")
        return result("record", intake, 2, correction="Prepare again and copy the intake id. The live bytes were not stored over an old intake.", failed_input=failed, recorded=False, stale=True)
    if not isinstance(stored, dict):
        exclusive_write(store_root(book, intake) / "intake.json", pretty({key: value for key, value in intake.items() if key not in {"cuts", "artifact_paths"}}))
    review_id = review_id_for(intake["intake_id"], judgment)
    journal = load_journal(book, intake)
    existing = record_path(book, intake, review_id)
    if existing.is_file():
        prior = load_record(book, intake, review_id)
        if canonical(prior.get("judgment")) == canonical(judgment):
            return result("record", intake, 0, already_recorded=True, judgment=prior["judgment"], next_action=judgment["next_action"], recorded=True, review_id=review_id, mode=prior.get("mode"))
        failed = save_failed(book, intake, raw, "a different body is already stored for this review id")
        return result("record", intake, 2, correction="The stored review was kept.", failed_input=failed, recorded=False, review_id=review_id)
    current = journal.get("current")
    if isinstance(current, str) and successor != current:
        failed = save_failed(book, intake, raw, "a current review exists")
        return result("record", intake, 2, correction="Pass --successor with the current review id. The current record was kept.", current=current, failed_input=failed, recorded=False)
    if successor is not None and current is None:
        failed = save_failed(book, intake, raw, "no review to succeed")
        return result("record", intake, 2, correction="Record the first review without --successor.", failed_input=failed, recorded=False)
    cycle = {"called": False, "committed": False, "error": None}
    if intake["custody"] == "complete-descriptor":
        cycle = attempt_cycle(book, intake, judgment, review_id)
    if judgment["operation"] == "complete" and not cycle.get("committed"):
        failed = save_failed(book, intake, raw, "completion is ineligible until the cycle records the review")
        return result(
            "record",
            intake,
            2,
            correction="operation complete was not recorded. Missing custody or a cycle refusal stays ineligible for completion.",
            cycle=cycle,
            failed_input=failed,
            recorded=False,
        )
    mode = "cycle-committed" if cycle.get("committed") else "preliminary"
    custody = "measured" if cycle.get("committed") else "missing"
    if intake["custody"] == "complete-descriptor" and not cycle.get("committed"):
        custody = "present-not-committed"
    attention = []
    effective = None
    prime_exit = None
    if not cycle.get("committed"):
        capture = None
        code, report, err = call_prime(book, prime_record(intake, judgment, capture))
        prime_exit = code
        if code == 2 or not isinstance(report, dict):
            failed = save_failed(book, intake, raw, err.strip() or "prime_review refused the record")
            return result("record", intake, 2, correction=err.strip() or "prime_review refused the record", failed_input=failed, recorded=False)
        effective = report.get("effective")
        attention = report.get("attention") if isinstance(report.get("attention"), list) else []
    account = judgment["sections"].get("findings_account")
    if judgment["findings"] and account is None:
        attention.append("findings_account is unknown")
    if isinstance(account, list):
        accounted = set()
        for item in account:
            if isinstance(item, dict) and isinstance(item.get("finding_id"), str):
                accounted.add(item["finding_id"])
        for item in judgment["findings"]:
            if item["finding_id"] not in accounted:
                failed = save_failed(book, intake, raw, "finding not accounted")
                return result("record", intake, 2, correction="A supplied finding is missing from findings_account. It was not dropped.", failed_input=failed, recorded=False)
    record = {
        "attention": attention,
        "custody": custody,
        "cycle": cycle,
        "cycle_error": cycle.get("error"),
        "director_text": intake["director_text"],
        "eligible_for_custody_completion": bool(cycle.get("committed") and judgment["operation"] == "complete"),
        "holds": judgment["holds"],
        "intake_id": intake["intake_id"],
        "judgment": judgment,
        "mode": mode,
        "next_action": judgment["next_action"],
        "prime_review_effective": effective,
        "prime_review_exit": prime_exit,
        "review_id": review_id,
        "schema": "workbook-review-record/1",
        "successor_of": successor,
    }
    record["rendered"] = render_body(record)
    folder = record_path(book, intake, review_id).parent
    exclusive_write(folder / "judgment.json", pretty(judgment))
    exclusive_write(folder / "record.json", pretty(record))
    exclusive_write(folder / "rendered.md", record["rendered"].encode("utf-8"))
    journal.setdefault("reviews", []).append({
        "judgment_sha256": sha256_bytes(canonical(judgment)),
        "record_sha256": sha256_bytes(pretty(record)),
        "review_id": review_id,
    })
    journal["current"] = review_id
    journal["publication"] = {"review_id": review_id, "status": "recorded"}
    journal["schema"] = "workbook-review-journal/1"
    save_journal(book, intake, journal)
    return result(
        "record",
        intake,
        0,
        attention=attention,
        custody=custody,
        director_text=intake["director_text"],
        eligible_for_custody_completion=record["eligible_for_custody_completion"],
        holds=judgment["holds"],
        judgment=judgment,
        mode=mode,
        next_action=judgment["next_action"],
        recorded=True,
        review_id=review_id,
    )


def do_inspect(book: Path, source: str, pass_id: str) -> dict:
    intake = build_intake(book, source, pass_id)
    document = load_form()
    journal = load_journal(book, intake) if journal_path(book, intake).is_file() else {"current": None, "reviews": []}
    current = journal.get("current") if isinstance(journal.get("current"), str) else None
    record = None
    if current and record_path(book, intake, current).is_file():
        record = load_record(book, intake, current)
    stored = read_stored_intake(book, intake)
    return result(
        "inspect",
        intake,
        0,
        current=current,
        destination=intake["destination"],
        director_text=intake["director_text"],
        findings=intake["findings"],
        form=form_view(intake, document),
        holds=record.get("holds") if isinstance(record, dict) else [],
        judgment=record.get("judgment") if isinstance(record, dict) else None,
        mode=record.get("mode") if isinstance(record, dict) else None,
        publication=journal.get("publication"),
        rendered=record.get("rendered") if isinstance(record, dict) else None,
        stale=isinstance(stored, dict) and stored.get("intake_id") != intake["intake_id"],
        unknowns=intake["unknowns"],
    )


def publish_target(book: Path, intake: dict, rendered: str, review_id: str) -> dict:
    if intake["target_kind"] == "section":
        target = book / intake["destination"]
        before = regular_file(target, "target")
        prefix, current, suffix, sep = locate_review(before)
        current_text = current.replace(b"\r\n", b"\n")
        if not vacant(current) and not our_marker(current, review_id) and b"workbook-review-id:" in current_text:
            return {"before": before, "blocked": "stale-own-review", "changed": False}
        if not vacant(current) and b"workbook-review-id:" not in current_text:
            return {"before": before, "blocked": "manual-review", "changed": False}
        body = rendered.encode("utf-8")
        if sep == b"\r\n":
            body = body.replace(b"\n", b"\r\n")
        if not body.endswith(sep):
            body += sep
        updated = prefix + body + suffix
        if updated == before:
            return {"after": before, "before": before, "blocked": None, "changed": False, "target": intake["destination"]}
        journal = load_journal(book, intake)
        journal["publication"] = {
            "before_sha256": sha256_bytes(before),
            "rendered_sha256": sha256_bytes(rendered.encode("utf-8")),
            "review_id": review_id,
            "status": "pointer-pending",
            "target": intake["destination"],
        }
        save_journal(book, intake, journal)
        exclusive_write(target, updated)
        after = target.read_bytes()
        new_prefix, new_current, new_suffix, _sep = locate_review(after)
        if new_prefix != prefix or new_suffix != suffix:
            return {"after": after, "before": before, "blocked": "unauthorized-diff", "changed": True}
        return {"after": after, "before": before, "blocked": None, "changed": True, "target": intake["destination"]}
    target_rel = intake["destination"]
    target = book / target_rel
    before = target.read_bytes() if target.is_file() and not is_link(target) else None
    if before is not None and not our_marker(before, review_id) and b"workbook-review-id:" not in before and before.strip() not in {b"", b"PENDING."}:
        return {"before": before, "blocked": "manual-review", "changed": False}
    payload = rendered.encode("utf-8")
    if before == payload:
        return {"after": before, "before": before, "blocked": None, "changed": False, "target": target_rel}
    journal = load_journal(book, intake)
    journal["publication"] = {
        "before_sha256": None if before is None else sha256_bytes(before),
        "rendered_sha256": sha256_bytes(payload),
        "review_id": review_id,
        "status": "pointer-pending",
        "target": target_rel,
    }
    save_journal(book, intake, journal)
    return_rel = intake["return_path"]
    return_before = None
    if isinstance(return_rel, str):
        return_path = book / return_rel
        if return_path.is_file():
            return_before = sha256_bytes(return_path.read_bytes())
    exclusive_write(target, payload)
    if isinstance(return_rel, str) and return_before is not None:
        if sha256_bytes((book / return_rel).read_bytes()) != return_before:
            return {"blocked": "return-moved", "changed": True}
    return {"after": target.read_bytes(), "before": before, "blocked": None, "changed": True, "target": target_rel}


def do_publish(book: Path, source: str, pass_id: str, review_id: str) -> dict:
    writable(book)
    intake = build_intake(book, source, pass_id)
    if intake["kind"] is None:
        return result("publish", intake, 2, correction="missing route", missing=["route"], published=False)
    stored = read_stored_intake(book, intake)
    if not isinstance(stored, dict):
        return result("publish", intake, 2, correction="No judgment is recorded.", published=False)
    if stored.get("intake_id") != intake["intake_id"]:
        record = load_record(book, intake, review_id) if record_path(book, intake, review_id).is_file() else None
        return result("publish", intake, 1, correction="Publication is blocked because the assignment changed after intake.", judgment=None if record is None else record.get("judgment"), published=False, review_id=review_id, stale=True)
    if not record_path(book, intake, review_id).is_file():
        return result("publish", intake, 2, correction="That review id is not recorded.", published=False)
    journal = load_journal(book, intake)
    if journal.get("current") != review_id:
        record = load_record(book, intake, review_id)
        return result("publish", intake, 1, correction="Publish names the latest review. An older review was not selected.", judgment=record.get("judgment"), published=False, review_id=review_id)
    record = load_record(book, intake, review_id)
    rendered_path = record_path(book, intake, review_id).parent / "rendered.md"
    rendered = rendered_path.read_text(encoding="utf-8")
    if record.get("mode") == "cycle-committed":
        loop = pin_file("review_loop")
        paths = cycle_paths(book)
        target = book / intake["destination"]
        before = target.read_bytes() if target.is_file() else b""
        try:
            prefix, current, suffix, _sep = locate_review(before)
        except Refusal:
            prefix, current, suffix = b"", before, b""
        if current and not vacant(current) and b"workbook-review-id:" not in current and b"task_binding:" not in current and b"authority: none" not in current:
            return result("publish", intake, 1, correction="Existing manual review text was kept.", judgment=record["judgment"], published=False, review_id=review_id)
        code, view, err = call_json(loop, ["render", "--fixture-root", str(book), "--request", paths["request"]])
        after = target.read_bytes() if target.is_file() else b""
        render = view.get("render") if isinstance(view, dict) and isinstance(view.get("render"), dict) else {}
        render_result = render.get("result")
        blocked = None
        if render_result not in {"rendered", "already-rendered"}:
            blocked = str(render.get("rule") or err.strip() or "cycle render did not publish the review")[:600]
        elif after == before and render_result != "already-rendered":
            blocked = "cycle render did not change the target"
        elif code not in {0, 1}:
            blocked = err.strip() or "cycle render refused"
        else:
            try:
                new_prefix, _new_current, new_suffix, _sep = locate_review(after)
                if new_prefix != prefix or new_suffix != suffix:
                    blocked = "unauthorized-diff"
            except Refusal as exc:
                blocked = exc.message
        if blocked:
            return result("publish", intake, 1, correction=blocked, judgment=record["judgment"], next_action=record["next_action"], published=False, review_id=review_id)
        journal["publication"] = {
            "after_sha256": sha256_bytes(after),
            "before_sha256": sha256_bytes(before),
            "review_id": review_id,
            "status": "published",
            "target": intake["destination"],
        }
        save_journal(book, intake, journal)
        return result("publish", intake, 0, judgment=record["judgment"], next_action=record["next_action"], published=True, review_id=review_id, target=intake["destination"])
    try:
        outcome = publish_target(book, intake, rendered, review_id)
    except Refusal as exc:
        fresh = load_journal(book, intake)
        status = fresh.get("publication", {}).get("status") if isinstance(fresh.get("publication"), dict) else None
        return result(
            "publish",
            intake,
            1,
            correction=exc.message,
            holds=record["holds"],
            judgment=record["judgment"],
            next_action=record["next_action"],
            publication_status=status,
            published=False,
            review_id=review_id,
        )
    if outcome.get("blocked"):
        return result("publish", intake, 1, correction=outcome["blocked"], holds=record["holds"], judgment=record["judgment"], next_action=record["next_action"], published=False, review_id=review_id)
    journal = load_journal(book, intake)
    after = outcome.get("after") or b""
    journal["publication"] = {
        "after_sha256": sha256_bytes(after),
        "before_sha256": None if outcome.get("before") is None else sha256_bytes(outcome["before"]),
        "rendered_sha256": sha256_bytes(rendered.encode("utf-8")),
        "review_id": review_id,
        "status": "published",
        "target": outcome.get("target"),
    }
    save_journal(book, intake, journal)
    return result("publish", intake, 0, judgment=record["judgment"], next_action=record["next_action"], published=True, review_id=review_id, target=outcome.get("target"))


def revalidate(book: Path, intake: dict, review_id: str) -> dict:
    path = record_path(book, intake, review_id)
    data = path.read_bytes()
    record = strict_json(data, "review record")
    journal = load_journal(book, intake)
    rows = journal.get("reviews") if isinstance(journal.get("reviews"), list) else []
    expected = None
    for item in rows:
        if isinstance(item, dict) and item.get("review_id") == review_id:
            expected = item.get("record_sha256")
    record_ok = isinstance(expected, str) and sha256_bytes(data) == expected
    cycle_ok = True
    if isinstance(record, dict) and record.get("mode") == "cycle-committed":
        cycle = record.get("cycle") if isinstance(record.get("cycle"), dict) else {}
        rel = cycle.get("cycle_record")
        cycle_ok = False
        if isinstance(rel, str):
            try:
                logical(rel, "cycle record")
                blob = (book / rel).read_bytes()
                body = json.loads(blob.decode("utf-8"))
                cycle_ok = (
                    isinstance(body, dict)
                    and body.get("schema") == "prime-cycle-review/3"
                    and body.get("review_id") == cycle.get("cycle_review_id")
                )
            except (OSError, UnicodeDecodeError, json.JSONDecodeError, Refusal):
                cycle_ok = False
    rendered_path = path.parent / "rendered.md"
    rendered_ok = False
    if rendered_path.is_file() and isinstance(record, dict):
        rendered_ok = rendered_path.read_text(encoding="utf-8") == record.get("rendered")
    publication = journal.get("publication") if isinstance(journal.get("publication"), dict) else {}
    target_ok = True
    target_state = "not-published"
    if publication.get("status") == "published" and isinstance(publication.get("target"), str):
        target = book / publication["target"]
        if not target.is_file():
            target_ok = False
            target_state = "missing"
        else:
            blob = target.read_bytes()
            target_ok = sha256_bytes(blob) == publication.get("after_sha256")
            if intake["target_kind"] == "section" and target_ok:
                try:
                    prefix, _current, suffix, _sep = locate_review(blob)
                    before_note = publication.get("before_sha256")
                    target_state = "section-verified" if isinstance(before_note, str) else "verified"
                    if record.get("mode") != "cycle-committed":
                        target_ok = f"workbook-review-id: {review_id}" in blob.decode("utf-8", "replace")
                        if not target_ok:
                            target_state = "marker-missing"
                except Refusal:
                    target_ok = False
                    target_state = "heading-unreadable"
            elif not target_ok:
                target_state = "bytes-changed"
            else:
                target_state = "verified"
    elif publication.get("status") == "pointer-pending":
        target_state = "pointer-pending"
        target_ok = False
    stale = not (record_ok and rendered_ok and cycle_ok and (target_ok or publication.get("status") != "published"))
    judgment = record.get("judgment") if record_ok and isinstance(record, dict) else None
    return {
        "custody": None if not isinstance(record, dict) else record.get("custody"),
        "director_text": None if not isinstance(record, dict) else record.get("director_text"),
        "holds": [] if not isinstance(record, dict) or not record_ok else record.get("holds"),
        "judgment": judgment,
        "next_action": None if not isinstance(judgment, dict) else judgment.get("next_action"),
        "record_ok": record_ok,
        "rendered_ok": rendered_ok,
        "review_id": review_id,
        "stale": stale,
        "target_state": target_state,
    }


def do_read(book: Path, source: str, pass_id: str, command: str) -> dict:
    writable(book)
    intake = build_intake(book, source, pass_id)
    if intake["kind"] is None:
        return result(command, intake, 2, correction="missing route", judgment=None, missing=["route"])
    journal = load_journal(book, intake) if journal_path(book, intake).is_file() else {}
    review_id = journal.get("current") if isinstance(journal.get("current"), str) else None
    if not isinstance(review_id, str) or not record_path(book, intake, review_id).is_file():
        return result(command, intake, 2, correction="No recorded judgment.", judgment=None)
    if command == "read":
        record = load_record(book, intake, review_id)
        return result(
            command,
            intake,
            0,
            custody=record.get("custody"),
            director_text=record.get("director_text"),
            holds=record.get("holds"),
            judgment=record.get("judgment"),
            mode=record.get("mode"),
            next_action=record.get("next_action"),
            review_id=review_id,
        )
    checked = revalidate(book, intake, review_id)
    exit_code = 0 if not checked["stale"] else 1
    return result(command, intake, exit_code, **checked)


def parse_call(args: list[str]) -> tuple[str, dict[str, str]]:
    if not args:
        refuse("unknown workbook command")
    command = args[0]
    if command not in COMMANDS:
        refuse("unknown workbook command")
    allowed = set(COMMANDS[command]) | set(OPTIONAL.get(command, ()))
    values: dict[str, str] = {}
    index = 1
    while index < len(args):
        token = args[index]
        if token in BANNED or token.startswith("--tool") or token.startswith("--dest"):
            refuse("caller tool override is refused")
        if token not in allowed:
            refuse("unknown argument")
        if token in values:
            refuse(f"repeated {token}")
        if index + 1 >= len(args) or args[index + 1].startswith("--"):
            refuse(f"missing value for {token}")
        values[token] = args[index + 1]
        index += 2
    for flag in COMMANDS[command]:
        if flag not in values:
            refuse(f"missing {flag}")
    return command, values


def emit(payload: dict) -> None:
    sys.stdout.buffer.write(pretty(payload))


def perform(args: list[str]) -> int:
    command, values = parse_call(args)
    book = book_dir(values["--book"])
    source = values["--source"]
    pass_id = values["--pass"]
    if command == "prepare":
        payload = do_prepare(book, source, pass_id)
    elif command == "form":
        prepared = do_prepare(book, source, pass_id)
        payload = result(
            "form",
            {"instance_id": prepared["instance_id"], "intake_id": prepared["intake_id"], "page": prepared["page"], "pass": prepared["pass"], "kind": prepared["kind"]},
            int(prepared["exit"]),
            form=prepared["form"],
            missing=["route"] if prepared["exit"] == 2 else [],
        )
    elif command == "inspect":
        payload = do_inspect(book, source, pass_id)
    elif command == "record":
        judgment = Path(values["--judgment"])
        if not judgment.is_absolute():
            refuse("judgment path must be absolute")
        payload = do_record(book, source, pass_id, values["--intake"], judgment, values.get("--successor"))
    elif command == "publish":
        payload = do_publish(book, source, pass_id, values["--review"])
    else:
        payload = do_read(book, source, pass_id, command)
    emit(payload)
    return int(payload["exit"])


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    try:
        return perform(args)
    except Refusal as exc:
        print(f"refused: {exc.message}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
