#!/usr/bin/env python3
"""Source and pass access in front of reviewed return-lines pass03.

This file loads pass03 and the legacy reader by pin. It does not edit them.
It does not import a later authority successor. A descriptor is not acceptance.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import sys

sys.dont_write_bytecode = True
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"

SCHEMA = "return-access-result/1"
PASS03_PATH = "labs/return-lines-pass03/return_lines.py"
PASS03_SHA = "78cc4d8679bb6e54b3f2456ce777643da7a9a650ef5c79c216abd38a4c209c63"
PASS03_BYTES = 33349
PASS02_PATH = "labs/return-lines-pass02/return_lines.py"
PASS02_SHA = "6691d0587ab97ba24a1709c9950b506961152939e2d112ee608f9dbd23e92908"
PASS02_BYTES = 82908
PASS01_PATH = "labs/return-lines-pass01/return_lines.py"
PASS01_SHA = "863968c59974d85910626ba5e80cf49f14a3186c8d33b855efe00bf6ccec378a"
PASS01_BYTES = 100897
PLACEMENT_PATH = "labs/return-placement-pass01/return_placement.py"
PLACEMENT_SHA = "db96f7023c73dcececba0e7d42b821da8193af7534a4bdf8cd2e5d6cd53d0754"
PLACEMENT_BYTES = 66097
READER_PATH = "labs/return-capture-pass01/return_capture.py"
READER_SHA = "8f3da5c651f6924fca6dedb0b95da7d181eb58884dc030dd9cbc3d8b6a5b15ac"
READER_BYTES = 45767
PINS = (
    (PASS03_PATH, PASS03_SHA, PASS03_BYTES, "return_lines_pass03_pinned"),
    (PASS02_PATH, PASS02_SHA, PASS02_BYTES, "return_lines_pass02_checked"),
    (PASS01_PATH, PASS01_SHA, PASS01_BYTES, "return_lines_pass01_checked"),
    (PLACEMENT_PATH, PLACEMENT_SHA, PLACEMENT_BYTES, "return_placement_checked"),
    (READER_PATH, READER_SHA, READER_BYTES, "return_capture_pinned"),
)
NATIVE = "return-line-capture/1"
LEGACY_FORMAT = "legacy-relocated/1"
INCOMPLETE_WITNESS = "0154.colab-support-first-0501"
NATIVE_REASON = "native line-pass return is not a legacy single-envelope page"
AUTHORITY_REQUIREMENT = (
    "A door-marked copy requires the pass03 synthetic fixture "
    "return-line-authorization/1. The reviewed pass03 production CLI has no "
    "recorded-release path without its in-process test seam. No live release exists."
)
LEGACY_WRITERS = (
    {
        "allocates": True,
        "command": "reserve",
        "later_change": "A later helper successor refuses reserve when the book layout is line-pass. verify and inspect stay. No sentinel is added by that sentence.",
        "path": READER_PATH,
        "route": "return_capture reserve",
        "writes_custody": True,
    },
    {
        "allocates": True,
        "command": "reserve",
        "later_change": "These rehearsals call the same reserve command. They are not closed by the new app branch.",
        "path": "labs/capture-handoff-pass01/demo.py",
        "route": "capture-handoff demo",
        "writes_custody": True,
    },
    {
        "allocates": True,
        "command": "reserve",
        "later_change": "The rehearsal calls the same reserve command. It is not closed by the new app branch.",
        "path": "labs/capture-flow-rehearsal-pass01/rehearse.py",
        "route": "capture-flow rehearsal",
        "writes_custody": True,
    },
    {
        "allocates": False,
        "command": "capture",
        "later_change": "After reserve refuses a line-pass book, refuse this door on that book. This pack does not edit the handoff.",
        "path": "labs/capture-handoff-pass01/handoff.py",
        "route": "librarian capture-return",
        "writes_custody": True,
    },
    {
        "allocates": False,
        "command": "inspect",
        "later_change": "Boot hashes the helper and launches return_inspect.py. It does not call reserve. Keep the sibling hash until inspect no longer requires it.",
        "path": "labs/prime-boot-pass01/prime_boot.py",
        "route": "librarian boot",
        "writes_custody": False,
    },
    {
        "allocates": False,
        "command": "inspect",
        "later_change": "Batch observation launches return_inspect.py. It does not call reserve. Keep the pin until the helper and the inspector change together.",
        "path": "labs/batch-observation-pass01/batch_observe.py",
        "route": "librarian batch-observe",
        "writes_custody": False,
    },
)
_PASS03 = None
_READER = None


def die(message: str) -> None:
    sys.stderr.write(message + "\n")
    raise SystemExit(2)


def repo_root() -> str:
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.abspath(os.path.join(here, "..", ".."))


def pin_bytes(rel: str, digest: str, size: int) -> bytes:
    path = os.path.join(repo_root(), *rel.split("/"))
    if not os.path.isfile(path):
        die(f"refused: pin missing {rel}; nothing was written")
    with open(path, "rb") as handle:
        data = handle.read()
    if hashlib.sha256(data).hexdigest() != digest or len(data) != size:
        die(f"refused: pin mismatch {rel}; nothing was written")
    return data


def load_module(rel: str, digest: str, size: int, name: str):
    path = os.path.join(repo_root(), *rel.split("/"))
    pin_bytes(rel, digest, size)
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        die(f"refused: {rel} did not load; nothing was written")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_pass03():
    global _PASS03
    if _PASS03 is None:
        for rel, digest, size, _name in PINS:
            pin_bytes(rel, digest, size)
        _PASS03 = load_module(PASS03_PATH, PASS03_SHA, PASS03_BYTES, "return_lines_pass03_pinned")
        _PASS03.load_pass02()
    return _PASS03


def load_reader():
    global _READER
    if _READER is None:
        _READER = load_module(READER_PATH, READER_SHA, READER_BYTES, "return_capture_pinned")
    return _READER


def lines():
    return load_pass03().lines()


def dump(body: dict) -> bytes:
    return (json.dumps(body, indent=2, ensure_ascii=False) + "\n").encode("utf-8")


def read_json(path: str) -> dict | None:
    try:
        raw = open(path, "rb").read()
    except OSError:
        return None

    def pairs(items: list) -> dict:
        value: dict = {}
        for key, item in items:
            if key in value:
                raise ValueError("duplicate")
            value[key] = item
        return value

    try:
        body = json.loads(raw.decode("utf-8"), object_pairs_hook=pairs)
    except (UnicodeDecodeError, json.JSONDecodeError, ValueError):
        return None
    return body if isinstance(body, dict) else None


def emit(body: dict) -> int:
    sys.stdout.buffer.write(dump(body))
    return int(body["exit"])


def base_result(command: str, check: str, state: str, exit_code: int, correction: str) -> dict:
    return {
        "accepted": False,
        "approved": False,
        "check": check,
        "command": command,
        "correction": correction,
        "custody_is_acceptance": False,
        "descriptor": None,
        "detail": {
            "rewritten": False,
            "sentinel_policy": "not-adopted",
            "successor_consumed": False,
        },
        "exit": exit_code,
        "legacy": None,
        "missing": [],
        "partial": False,
        "published": False,
        "route": None,
        "schema": SCHEMA,
        "state": state,
        "task_association": "not-established",
        "verified": {},
    }


def book_dir(text: str) -> str:
    module = lines()
    if not isinstance(text, str) or text.strip() == "":
        die("refused: book is empty; nothing was written")
    if not os.path.isabs(text):
        die("refused: book must be absolute; nothing was written")
    if module.is_reparse(text) or not os.path.isdir(text):
        die("refused: book is not a directory; nothing was written")
    current = os.path.abspath(text)
    while True:
        parent = os.path.dirname(current)
        if parent == current:
            break
        if module.is_reparse(parent):
            die("refused: book ancestor is linked and was not followed; nothing was written")
        current = parent
    return os.path.abspath(text)


def scan_claims(book_abs: str) -> tuple[dict, dict]:
    module = lines()
    members: dict[str, list[str]] = {}
    origins: dict[tuple[str, str], list[str]] = {}
    try:
        pages = list(os.scandir(book_abs))
    except OSError:
        return members, origins
    for page in pages:
        if module.is_reparse(page.path) or not page.is_dir(follow_symlinks=False):
            continue
        try:
            children = list(os.scandir(page.path))
        except OSError:
            continue
        for child in children:
            if not child.name.endswith(".custody"):
                continue
            if module.is_reparse(child.path) or not child.is_dir(follow_symlinks=False):
                continue
            rel = f"{page.name}/{child.name}"
            reloc = os.path.join(child.path, "relocation.json")
            reservation = os.path.join(child.path, "reservation.json")
            if os.path.isfile(reloc) and not module.is_reparse(reloc):
                body = read_json(reloc)
                old = body.get("old_member") if isinstance(body, dict) else None
                if isinstance(old, str) and old:
                    members.setdefault(old, []).append(rel)
            if os.path.isfile(reservation) and not module.is_reparse(reservation):
                body = read_json(reservation)
                origin = body.get("origin") if isinstance(body, dict) else None
                if isinstance(origin, dict):
                    page_name = origin.get("page")
                    batch = origin.get("batch")
                    if isinstance(page_name, str) and isinstance(batch, str):
                        origins.setdefault((page_name, batch), []).append(rel)
    return members, origins


def route_view(descriptor: dict | None) -> dict | None:
    if not isinstance(descriptor, dict):
        return None
    origin = descriptor.get("origin") if isinstance(descriptor.get("origin"), dict) else {}
    return {
        "custody_path": descriptor.get("custody_path"),
        "pass": origin.get("batch"),
        "return_path": descriptor.get("return_path"),
        "route": descriptor.get("route"),
        "source_page": origin.get("page"),
        "target_page": descriptor.get("target_page"),
    }


def facts(descriptor: dict | None, legacy: dict | None, route_missing: bool) -> tuple[dict, list]:
    verified: dict = {}
    missing: list[str] = []
    if route_missing:
        missing.append("route")
        return verified, missing
    if isinstance(descriptor, dict):
        origin = descriptor.get("origin") if isinstance(descriptor.get("origin"), dict) else {}
        verified["pass"] = origin.get("batch")
        verified["return_path"] = descriptor.get("return_path")
        verified["route"] = descriptor.get("route")
        verified["source_page"] = origin.get("page")
        verified["target_page"] = descriptor.get("target_page")
        if descriptor.get("return_sha256"):
            verified["return_bytes"] = descriptor.get("return_bytes")
            verified["return_sha256"] = descriptor.get("return_sha256")
        elif descriptor.get("state") != "reserved":
            missing.append("return")
        if descriptor.get("receipt_sha256"):
            verified["receipt_sha256"] = descriptor.get("receipt_sha256")
    if isinstance(legacy, dict) and legacy.get("called") is True:
        verified["legacy_member"] = legacy.get("member")
        verified["legacy_parent"] = legacy.get("parent")
        if legacy.get("exit") != 0:
            missing.append("legacy-envelope")
    return verified, missing


def partial_custody(book_abs: str, descriptor: dict | None) -> bool:
    if not isinstance(descriptor, dict) or descriptor.get("state") != "incomplete":
        return False
    custody = descriptor.get("custody_path")
    if not isinstance(custody, str) or not custody:
        return False
    base = os.path.join(book_abs, *custody.split("/"))
    if not os.path.isdir(base):
        return False
    receipt = os.path.join(base, "receipt.json")
    if os.path.lexists(receipt):
        return False
    marks = (
        os.path.join(base, "manifest.json"),
        os.path.join(base, "return.md"),
        os.path.join(base, "payload"),
    )
    return any(os.path.lexists(path) for path in marks)


def retired_root(book_abs: str) -> str | None:
    migration = read_json(os.path.join(book_abs, "return-line-migration.json"))
    backup = migration.get("backup_path") if isinstance(migration, dict) else None
    if not isinstance(backup, str) or not os.path.isabs(backup):
        return None
    pointer = read_json(os.path.join(backup, "retirement-pointer.json"))
    root = pointer.get("retired_root") if isinstance(pointer, dict) else None
    if isinstance(root, str) and os.path.isabs(root) and os.path.isdir(root):
        return root
    return None


def legacy_places(book_abs: str, member: str, retained: dict) -> list[tuple[str, str]]:
    module = lines()
    if not member or "/" in member or "\\" in member:
        return []
    found: list[tuple[str, str]] = []
    roots = []
    recorded = retained.get("retired_root") if isinstance(retained, dict) else None
    if isinstance(recorded, str) and os.path.isabs(recorded):
        roots.append(recorded)
    pointer_root = retired_root(book_abs)
    if pointer_root and pointer_root not in roots:
        roots.append(pointer_root)
    for root in roots:
        for kind in ("originals", "occupants"):
            parent = os.path.join(root, kind)
            member_path = os.path.join(parent, member)
            if os.path.isdir(member_path) and not module.is_reparse(member_path):
                found.append((kind, parent))
    direct = os.path.join(book_abs, member)
    reservation = os.path.join(direct, "reservation.json")
    if os.path.isdir(direct) and os.path.isfile(reservation) and not module.is_reparse(direct):
        found.append(("book", book_abs))
    unique: list[tuple[str, str]] = []
    seen = set()
    for item in found:
        if item not in seen:
            seen.add(item)
            unique.append(item)
    return unique


def call_reader(parent: str, member: str) -> dict:
    result = load_reader().verify(parent, member)
    return {
        "called": True,
        "exit": int(result.code),
        "member": member,
        "parent": parent,
        "reason": None,
        "text": result.text,
    }


def attach_legacy(book_abs: str, descriptor: dict | None, retained: dict, member_arg: str | None) -> dict:
    if not isinstance(descriptor, dict):
        return {"called": False, "exit": None, "member": None, "parent": None, "reason": "no descriptor", "text": None}
    if descriptor.get("custody_format") == NATIVE and not (isinstance(retained, dict) and retained.get("archived_identity")):
        return {"called": False, "exit": None, "member": None, "parent": None, "reason": NATIVE_REASON, "text": None}
    member = None
    if isinstance(retained, dict) and isinstance(retained.get("archived_identity"), str):
        member = retained["archived_identity"]
    elif isinstance(member_arg, str):
        member = member_arg
    places = legacy_places(book_abs, member or "", retained if isinstance(retained, dict) else {})
    archived = [item for item in places if item[0] in {"originals", "occupants"}]
    if len(archived) > 1:
        return {
            "called": False,
            "exit": None,
            "member": member,
            "parent": None,
            "places": [{"kind": kind, "parent": parent} for kind, parent in archived],
            "reason": "ambiguous legacy parent",
            "text": None,
        }
    if len(archived) == 1:
        _kind, parent = archived[0]
        return call_reader(parent, member or "")
    direct = [item for item in places if item[0] == "book"]
    if len(direct) == 1 and isinstance(member, str):
        return call_reader(direct[0][1], member)
    if descriptor.get("custody_format") == LEGACY_FORMAT:
        return {
            "called": False,
            "exit": None,
            "member": member,
            "parent": None,
            "reason": "legacy parent is absent",
            "text": None,
        }
    return {"called": False, "exit": None, "member": None, "parent": None, "reason": NATIVE_REASON, "text": None}


def finish(command: str, backend: dict, book_abs: str, member_arg: str | None, line_check: dict | None) -> dict:
    descriptor = backend.get("descriptor") if isinstance(backend.get("descriptor"), dict) else None
    if line_check is not None and isinstance(line_check.get("descriptor"), dict):
        same_state = line_check.get("state") == backend.get("state")
        same_hash = line_check["descriptor"].get("return_sha256") == (descriptor or {}).get("return_sha256")
        if not same_state or not same_hash:
            body = base_result(command, "return-access-line/1", "conflict", 2, "Line lookup and line verify disagree. No file was rewritten.")
            body["detail"]["lookup"] = backend
            body["detail"]["verify"] = line_check
            return body
        if command == "verify":
            descriptor = line_check["descriptor"]
            backend = dict(backend)
            backend["state"] = line_check.get("state")
            backend["exit"] = line_check.get("exit")
            backend["check"] = line_check.get("check")
            backend["correction"] = line_check.get("correction")
    retained = {}
    detail = backend.get("detail") if isinstance(backend.get("detail"), dict) else {}
    if isinstance(detail.get("retained_original"), dict):
        retained = detail["retained_original"]
    legacy = attach_legacy(book_abs, descriptor, retained, member_arg)
    if legacy.get("reason") == "ambiguous legacy parent":
        body = base_result(command, "return-access-ambiguity/1", "refused", 2, "Ambiguous legacy parent. The reader was not called and no directory was chosen.")
        body["detail"]["places"] = legacy.get("places")
        body["missing"] = ["legacy-parent"]
        return body
    state = backend.get("state") if isinstance(backend.get("state"), str) else "refused"
    exit_code = backend.get("exit") if isinstance(backend.get("exit"), int) else 2
    if state == "complete" and legacy.get("called") is True and legacy.get("exit") not in (0, None):
        state = "conflict"
        exit_code = 2
    route_missing = backend.get("check") == "return-placement-route/1" or (
        descriptor is None and state == "refused" and "undeclared" in str(backend.get("correction") or "")
    )
    verified, missing = facts(descriptor, legacy, route_missing)
    if legacy.get("reason") == "legacy parent is absent":
        missing.append("legacy-parent")
    correction = backend.get("correction") if isinstance(backend.get("correction"), str) else "The return was not resolved."
    body = base_result(
        command,
        backend.get("check") if isinstance(backend.get("check"), str) else "return-access/1",
        state,
        exit_code,
        correction,
    )
    body["descriptor"] = descriptor
    body["legacy"] = legacy
    body["missing"] = missing
    body["partial"] = partial_custody(book_abs, descriptor)
    body["route"] = route_view(descriptor)
    body["verified"] = verified
    body["detail"]["backend"] = backend
    if line_check is not None:
        body["detail"]["line_verify"] = line_check
    return body


def selectors(source: str | None, batch: str | None, member: str | None, submission: str | None) -> tuple[str, str | None, str | None]:
    families = []
    if source or batch:
        families.append("source")
    if member:
        families.append("member")
    if submission:
        families.append("submission")
    if len(families) != 1:
        raise ValueError("selector")
    if families[0] == "source" and (not source or not batch):
        raise ValueError("selector")
    return families[0], source, batch


def lookup_backend(book: str, member: str | None, source: str | None, batch: str | None, submission: str | None, command: str) -> dict:
    module = load_pass03().load_pass02()
    return module.lookup_run(book, member, source, batch, submission, command)


def read_command(command: str, book: str, source: str | None, batch: str | None, member: str | None, submission: str | None) -> dict:
    book_abs = book_dir(book)
    try:
        kind, source, batch = selectors(source, batch, member, submission)
    except ValueError:
        body = base_result(command, "return-access-selector/1", "refused", 2, "Pass a source page and pass, or one member, or one submission. No directory was chosen.")
        return body
    members, origins = scan_claims(book_abs)
    if kind == "member" and member and len(members.get(member, [])) > 1:
        body = base_result(command, "return-access-ambiguity/1", "refused", 2, "Ambiguous return. No directory was chosen.")
        body["detail"]["claimants"] = members[member]
        body["missing"] = ["member"]
        return body
    if kind == "source" and source and batch and len(origins.get((source, batch), [])) > 1:
        body = base_result(command, "return-access-ambiguity/1", "refused", 2, "Ambiguous return. No directory was chosen.")
        body["detail"]["claimants"] = origins[(source, batch)]
        body["missing"] = ["source"]
        return body
    backend = lookup_backend(book_abs, member if kind == "member" else None, source if kind == "source" else None, batch if kind == "source" else None, submission if kind == "submission" else None, "lookup")
    line_check = None
    if command == "verify" and isinstance(backend.get("descriptor"), dict):
        origin = backend["descriptor"].get("origin") if isinstance(backend["descriptor"].get("origin"), dict) else {}
        page = origin.get("page")
        found_batch = origin.get("batch")
        if isinstance(page, str) and isinstance(found_batch, str):
            line_check = lines().verify_run(book_abs, page, found_batch)
    return finish(command, backend, book_abs, member if kind == "member" else None, line_check)


def incomplete_findings(book_abs: str) -> list[dict]:
    findings = []
    index = read_json(os.path.join(book_abs, "return-line-index.json"))
    items = index.get("items") if isinstance(index, dict) else None
    if isinstance(items, list):
        for item in items:
            if not isinstance(item, dict):
                continue
            state = item.get("state")
            if state == "complete":
                continue
            findings.append({
                "completed_by_this_tool": False,
                "member": item.get("old_member"),
                "source_page": (item.get("origin") or {}).get("page") if isinstance(item.get("origin"), dict) else None,
                "state": state,
            })
    return findings


def layout_report(book_abs: str) -> tuple[dict, dict, list]:
    path = os.path.join(book_abs, "return-line-layout.json")
    report = {"allocation": None, "bytes": None, "path": "return-line-layout.json", "present": False, "sequential_allocation": None, "sha256": None}
    verified: dict = {}
    missing: list[str] = []
    if not os.path.isfile(path):
        missing.append("layout")
        return report, verified, missing
    raw = open(path, "rb").read()
    report["present"] = True
    report["bytes"] = len(raw)
    report["sha256"] = hashlib.sha256(raw).hexdigest()
    body = read_json(path)
    if isinstance(body, dict):
        report["allocation"] = body.get("allocation")
        report["sequential_allocation"] = body.get("sequential_allocation")
    verified["layout_sha256"] = report["sha256"]
    verified["layout_bytes"] = report["bytes"]
    return report, verified, missing


def status(book: str) -> dict:
    book_abs = book_dir(book)
    layout, verified, missing = layout_report(book_abs)
    body = base_result(
        "status",
        "return-access-status/1",
        "reported",
        0,
        "Status is read-only. Custody is not acceptance. Legacy writer closure is not established.",
    )
    body["missing"] = missing
    body["verified"] = verified
    body["detail"].update({
        "authority": {
            "established": False,
            "live_release": False,
            "requirement": AUTHORITY_REQUIREMENT,
            "successor_consumed": False,
        },
        "incomplete_closure": "not-established",
        "incomplete_findings": incomplete_findings(book_abs),
        "layout": layout,
        "legacy_writer_closure": "not-established",
        "legacy_writers": [dict(item) for item in LEGACY_WRITERS],
    })
    witness = INCOMPLETE_WITNESS
    if not any(item.get("member") == witness for item in body["detail"]["incomplete_findings"]):
        body["detail"]["incomplete_witness"] = {
            "completed_by_this_tool": False,
            "member": witness,
            "present_in_index": False,
        }
    return body


def take(args: list[str], flag: str) -> str | None:
    if args.count(flag) > 1:
        die(f"refused: repeated {flag}; nothing was written")
    if flag not in args:
        return None
    index = args.index(flag)
    if index + 1 >= len(args) or args[index + 1].startswith("--"):
        die(f"refused: missing value for {flag}; nothing was written")
    return args[index + 1]


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    if not args or args[0] not in {"status", "lookup", "verify"}:
        die("refused: command is not status, lookup, or verify; nothing was written")
    command = args.pop(0)
    known = {"--book", "--source", "--pass", "--member", "--submission"}
    index = 0
    while index < len(args):
        token = args[index]
        if token not in known:
            die("refused: unknown argument; nothing was written")
        index += 2
    book = take(args, "--book")
    if book is None:
        die("refused: missing --book; nothing was written")
    if command == "status":
        if any(flag in args for flag in ("--source", "--pass", "--member", "--submission")):
            die("refused: status takes only --book; nothing was written")
        return emit(status(book))
    body = read_command(command, book, take(args, "--source"), take(args, "--pass"), take(args, "--member"), take(args, "--submission"))
    return emit(body)


if __name__ == "__main__":
    sys.exit(main())
