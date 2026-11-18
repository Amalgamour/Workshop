#!/usr/bin/env python3
"""Plan-bound authorization over frozen return-lines pass02.

This file loads pass02 by pin and does not edit it. Pass02 loads pass01
by pin. A matching record is not acceptance, seating, or a live release.
The canonical work book stays refused for this pack.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import os
import sys

sys.dont_write_bytecode = True

TOOL_PATH = "labs/return-lines-pass03/return_lines.py"
PASS02_PATH = "labs/return-lines-pass02/return_lines.py"
PASS02_SHA = "6691d0587ab97ba24a1709c9950b506961152939e2d112ee608f9dbd23e92908"
PASS02_BYTES = 82908
FIXTURE_SCHEMA = "return-line-authorization/1"
RECORDED_SCHEMA = "return-line-recorded-release/1"
RELEASE_SCHEMA = "return-line-director-release/1"
CANDIDATE_SCHEMA = "return-line-release-candidate/1"
BOOK_NAME = "00.00.10.work"
ESCALATION = (
    "Escalation: Codex Prime on 0521.return-placement/05.05. "
    "This tool does not decide meaning, acceptance, or live authority. "
    "Live migration is not released."
)
BIND_FIELDS = (
    "book", "book_path", "executor", "layout_sha256", "plan_sha256", "plan_bytes",
    "audit_sha256", "audit_bytes", "backup_root", "staging_root", "retired_root", "operations",
)
RELEASE_KEYS = {"schema", "release_text", *BIND_FIELDS}
RECORDED_KEYS = {"schema", "synthetic", "release_path", "release_sha256", "release_bytes", *BIND_FIELDS}
CANDIDATE_KEYS = {"schema", "active", "release_text", "unresolved", *BIND_FIELDS}
PATH_FIELDS = {"book_path", "backup_root", "staging_root", "retired_root"}
BOOK_SOURCE_COMMANDS = {
    "init", "stage", "stage-resume", "reconstruct", "reconstruct-resume",
    "publish", "publish-resume",
}
_P2 = None
_ORIG_REQUIRE = None
_ORIG_NEEDS = None
_DESIGNATED = {"path": None}


def repo_root() -> str:
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.abspath(os.path.join(here, "..", ".."))


def load_pass02():
    global _P2, _ORIG_REQUIRE, _ORIG_NEEDS
    if _P2 is not None:
        return _P2
    path = os.path.join(repo_root(), *PASS02_PATH.split("/"))
    with open(path, "rb") as handle:
        data = handle.read()
    if hashlib.sha256(data).hexdigest() != PASS02_SHA or len(data) != PASS02_BYTES:
        raise SystemExit("refused: pass02 pin mismatch; nothing was written")
    spec = importlib.util.spec_from_file_location("return_lines_pass02_pinned", path)
    if spec is None or spec.loader is None:
        raise SystemExit("refused: pass02 did not load; nothing was written")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    _ORIG_REQUIRE = module.require_authorization
    _ORIG_NEEDS = module.needs_auth
    module.patched_assert = patched_assert
    module.require_authorization = require_authorization
    module.needs_auth = needs_auth
    module.live_refusal = live_refusal
    _P2 = module
    module.load_lines()
    return module


def lines():
    return load_pass02().load_lines()


def designate_live(path: str) -> None:
    """Test seam. Not a CLI flag. Marks one disposable copy as a live identity."""
    if not isinstance(path, str) or not os.path.isabs(path):
        raise ValueError("designate_live expects an absolute disposable path")
    _DESIGNATED["path"] = os.path.abspath(path)


def clear_designation() -> None:
    _DESIGNATED["path"] = None


def arm_fault(phase: str, skip: int, mode: str) -> None:
    load_pass02().arm_fault(phase, skip, mode)


def clear_fault() -> None:
    load_pass02().clear_fault()


def is_designated(path: str) -> bool:
    chosen = _DESIGNATED["path"]
    if chosen is None:
        return False
    return lines().norm(chosen) == lines().norm(os.path.abspath(path))


def is_real_live(path: str) -> bool:
    module = lines()
    return module.norm(os.path.abspath(path)) == module.norm(module.live_book_path())


def refuse(check: str, reason: str, correction: str, evidence: str | None = None,
           exit_code: int = 2, state: str = "refused", detail: dict | None = None) -> None:
    text = correction.rstrip()
    if reason and reason not in text:
        text = f"{reason}. {text}"
    if "Escalation:" not in text:
        text = text + " " + ESCALATION
    raise lines().LineError(
        check, reason, text, evidence=evidence, exit_code=exit_code, state=state, detail=detail or {},
    )


def is_sha(value: object) -> bool:
    return isinstance(value, str) and len(value) == 64 and all(char in "0123456789abcdef" for char in value)


def is_length(value: object) -> bool:
    return isinstance(value, int) and not isinstance(value, bool) and value >= 0


def plain_text(value: object, allow_lf: bool) -> bool:
    if not isinstance(value, str) or not value or len(value) > 4096:
        return False
    for char in value:
        code = ord(char)
        if code < 32 or code == 127:
            if allow_lf and char in "\n\t":
                continue
            return False
    return True


def operations_ok(value: object) -> bool:
    if not isinstance(value, list) or not value:
        return False
    if any(not isinstance(item, str) or not item for item in value):
        return False
    return len(value) == len(set(value))


def outside_book(book_abs: str, path: str, label: str) -> str:
    module = lines()
    absolute = os.path.abspath(path)
    live = module.live_book_path()
    if module.within(book_abs, absolute) or module.norm(absolute) == module.norm(book_abs):
        refuse(RECORDED_SCHEMA, f"{label} is inside the target book", "Keep the release outside the book being checked.", evidence=label)
    if module.within(live, absolute) or module.norm(absolute) == module.norm(live):
        refuse(RECORDED_SCHEMA, f"{label} is inside the live work book", "Keep the release outside the live work book.", evidence=label)
    return absolute


def same_volume(book_abs: str, roots: list[str]) -> None:
    module = lines()
    drives = {os.path.splitdrive(module.norm(path))[0] for path in [book_abs, *roots]}
    if len(drives) != 1 or drives == {""}:
        refuse(
            "filesystem",
            "roots are not on the book volume",
            "Use roots on the same volume as the book. A cross-device rename stops, and this tool does not copy-then-delete.",
        )


def parents_ready(roots: dict[str, str]) -> None:
    module = lines()
    for label, absolute in roots.items():
        if os.path.lexists(absolute) and not os.path.isdir(absolute):
            refuse("filesystem", f"{label} is not a directory", f"Pass a directory for {label}.")
        if module.is_reparse(absolute) if os.path.lexists(absolute) else False:
            refuse("filesystem", f"{label} is a link", "Use a real directory.")
        parent = os.path.dirname(absolute)
        if not parent or not os.path.isdir(parent):
            refuse("filesystem", f"{label} parent is missing", "Create the parent outside the book before execution.", evidence=label)


def call_roots(book_abs: str, backup: str, staging: str, retired: str):
    try:
        return load_pass02().roots_ok(book_abs, backup, staging, retired)
    except lines().LineError as exc:
        refuse(exc.check, exc.reason, exc.correction, evidence=exc.evidence, state=exc.state, detail=exc.detail)


def read_body(path: str, check: str) -> tuple[bytes, dict]:
    module = lines()
    try:
        raw = module.read_exact(os.path.abspath(path))
        body = module.loads(raw, check)
    except module.LineError as exc:
        refuse(exc.check, exc.reason, exc.correction, evidence=exc.evidence, state=exc.state, detail=exc.detail)
    if not isinstance(body, dict):
        refuse(check, "record is not an object", "Rewrite the JSON object.")
    return raw, body


def source_report(book_abs: str, audit_path: str) -> dict:
    module = lines()
    audit, audit_sha, audit_len = module.load_audit(audit_path)
    names = {record.get("old_member") for record in audit["records"] if isinstance(record, dict)}
    names = {name for name in names if isinstance(name, str)}
    checked = 0
    unassigned = 0
    mismatches = []
    for entry in audit["files"]:
        if not isinstance(entry, dict) or not isinstance(entry.get("path"), str):
            mismatches.append({"path": None, "reason": "audit file row is unusable"})
            continue
        member, rel = module.split_member(entry["path"], names)
        if member is None or rel is None:
            unassigned += 1
            continue
        if not is_sha(entry.get("sha256")) or not is_length(entry.get("bytes")):
            mismatches.append({"path": entry["path"], "reason": "audit file row has no hash"})
            continue
        target = module.join_book(book_abs, member + "/" + rel)
        if not os.path.lexists(target):
            mismatches.append({"path": entry["path"], "reason": "missing"})
            continue
        try:
            blob = module.read_exact(target)
        except module.LineError as exc:
            mismatches.append({"path": entry["path"], "reason": exc.reason})
            continue
        checked += 1
        if module.sha(blob) != entry["sha256"] or len(blob) != entry["bytes"]:
            mismatches.append({"path": entry["path"], "reason": "bytes differ"})
    return {
        "audit_bytes": audit_len,
        "audit_sha256": audit_sha,
        "source_files_checked": checked,
        "source_mismatch_count": len(mismatches),
        "source_example": None if not mismatches else mismatches[0],
        "unassigned_count": unassigned,
    }


def layout_bytes(book_name: str) -> bytes:
    module = lines()
    return module.dump(module.layout_body(book_name))


def checks_book_sources(operation: str | None) -> bool:
    return operation is None or operation in BOOK_SOURCE_COMMANDS


def binding_difference(release: dict, auth: dict) -> str | None:
    module = lines()
    for key in BIND_FIELDS:
        if key in PATH_FIELDS:
            if not isinstance(release[key], str) or not isinstance(auth[key], str):
                return key
            if module.norm(release[key]) != module.norm(auth[key]):
                return key
        elif release[key] != auth[key]:
            return key
    return None


def require_release_shape(body: dict) -> None:
    module = lines()
    try:
        module.expect_keys(body, RELEASE_KEYS, RELEASE_SCHEMA, "director release")
    except module.LineError as exc:
        refuse(RELEASE_SCHEMA, exc.reason, exc.correction)
    if body["schema"] != RELEASE_SCHEMA:
        refuse(RELEASE_SCHEMA, "release schema is not return-line-director-release/1", "Write the external release file with this schema.")
    if body["book"] != BOOK_NAME:
        refuse(RELEASE_SCHEMA, "release book name is not 00.00.10.work", "Name the book, not a filesystem path.")
    if not plain_text(body["executor"], False):
        refuse(RELEASE_SCHEMA, "recorded executor is empty or not plain text", "Record the executing identity in the release file. A label alone is not authority.")
    if not plain_text(body["release_text"], True):
        refuse(RELEASE_SCHEMA, "release text is empty or not plain text", "Write the Director sentence in the release file. This tool does not accept a hard-coded invocation.")
    if not operations_ok(body["operations"]):
        refuse(RELEASE_SCHEMA, "operations are not a list of unique command names", "Name each command. There is no blanket force.")
    for key in ("layout_sha256", "plan_sha256", "audit_sha256"):
        if not is_sha(body[key]):
            refuse(RELEASE_SCHEMA, f"{key} is not a sha256", "Bind the reviewed hash.")
    for key in ("plan_bytes", "audit_bytes"):
        if not is_length(body[key]):
            refuse(RELEASE_SCHEMA, f"{key} is not a length", "Bind the reviewed length.")
    for key in PATH_FIELDS:
        if not isinstance(body[key], str) or not os.path.isabs(body[key]):
            refuse(RELEASE_SCHEMA, f"{key} is not an absolute path", "Use an absolute path.")


def require_recorded_shape(body: dict) -> None:
    module = lines()
    try:
        module.expect_keys(body, RECORDED_KEYS, RECORDED_SCHEMA, "recorded release")
    except module.LineError as exc:
        refuse(RECORDED_SCHEMA, exc.reason, exc.correction)
    if body["schema"] != RECORDED_SCHEMA:
        refuse(RECORDED_SCHEMA, "authorization schema is not return-line-recorded-release/1", "Point --authorization at the recorded release.")
    if body["synthetic"] is not False:
        refuse(RECORDED_SCHEMA, "synthetic fixture is not a recorded release", "A synthetic fixture cannot authorize a designated-live identity.")
    if not plain_text(body["executor"], False):
        refuse(RECORDED_SCHEMA, "recorded executor is empty or not plain text", "Record the executing identity. A label alone is not authority.")
    if not operations_ok(body["operations"]):
        refuse(RECORDED_SCHEMA, "operations are not a list of unique command names", "Name each command. There is no blanket force.")
    if not is_sha(body["release_sha256"]):
        refuse(RECORDED_SCHEMA, "release_sha256 is not a sha256", "Pin the external release file.")
    if not is_length(body["release_bytes"]):
        refuse(RECORDED_SCHEMA, "release_bytes is not a length", "Pin the external release file.")
    for key in ("layout_sha256", "plan_sha256", "audit_sha256"):
        if not is_sha(body[key]):
            refuse(RECORDED_SCHEMA, f"{key} is not a sha256", "Bind the reviewed hash.")
    for key in ("plan_bytes", "audit_bytes"):
        if not is_length(body[key]):
            refuse(RECORDED_SCHEMA, f"{key} is not a length", "Bind the reviewed length.")
    for key in ("release_path", *PATH_FIELDS):
        if not isinstance(body[key], str) or not os.path.isabs(body[key]):
            refuse(RECORDED_SCHEMA, f"{key} is not an absolute path", "Use an absolute path.")
    if body["book"] != BOOK_NAME:
        refuse(RECORDED_SCHEMA, "authorization book name is not 00.00.10.work", "Name the book, not a filesystem path.")


def candidate_detail(body: dict, book_abs: str, audit: str) -> dict:
    detail = {
        "accepted": False,
        "active": body.get("active") if isinstance(body, dict) else None,
        "approved": False,
        "candidate": True,
        "executed": False,
        "live_book": is_real_live(book_abs),
        "live_execution": False,
        "mutated": False,
        "published": False,
        "unresolved": body.get("unresolved") if isinstance(body, dict) else None,
    }
    try:
        report = source_report(book_abs, audit)
        detail.update(report)
    except lines().LineError as exc:
        detail["source_error"] = exc.reason
    return detail


def refuse_candidate(body: dict, detail: dict) -> None:
    module = lines()
    try:
        module.expect_keys(body, CANDIDATE_KEYS, CANDIDATE_SCHEMA, "release candidate")
    except module.LineError as exc:
        refuse(CANDIDATE_SCHEMA, "candidate keys do not match the contract", exc.correction, detail=detail)
    if body.get("active") is True:
        refuse(
            CANDIDATE_SCHEMA,
            "candidate claims active authority",
            "Do not execute a candidate. Record a new director release after review.",
            detail=detail,
        )
    refuse(
        CANDIDATE_SCHEMA,
        "candidate is not authority",
        "Prime records a director release before execution. A candidate is not that record.",
        detail=detail,
    )


def check_materials(book_abs: str, auth: dict, release: dict, operation: str | None, name: str | None,
                    audit: str, plan: str, backup: str, staging: str, retired: str) -> dict:
    module = lines()
    if name is not None and name != auth["book"]:
        refuse(RECORDED_SCHEMA, "init name does not match the authorization book", "Pass the book name, not a path.")
    if operation is not None and operation not in auth["operations"]:
        refuse(RECORDED_SCHEMA, f"operation {operation} is not authorized", "Add this command to the recorded operations list.", evidence=operation)
    if module.norm(auth["book_path"]) != module.norm(book_abs):
        refuse(RECORDED_SCHEMA, "authorization book path does not match", "Name the disposable book this command is using.", evidence=book_abs)
    laid = layout_bytes(auth["book"])
    if module.sha(laid) != auth["layout_sha256"]:
        refuse(RECORDED_SCHEMA, "layout hash does not match the line-pass declaration", "Bind the hash of the pass01 layout body.")
    layout_path = os.path.join(book_abs, module.LAYOUT_NAME)
    if os.path.lexists(layout_path) and module.read_exact(layout_path) != laid:
        refuse("return-line-layout/1", "layout bytes differ", "Do not overwrite a different declaration.", evidence=module.LAYOUT_NAME, state="conflict")
    audit_bytes = module.read_exact(os.path.abspath(audit))
    if module.sha(audit_bytes) != auth["audit_sha256"] or len(audit_bytes) != auth["audit_bytes"]:
        refuse("audit identity", "audit hash or length does not match the recorded release", "Point the command at the authorized audit.", state="conflict")
    plan_bytes = module.read_exact(os.path.abspath(plan))
    if module.sha(plan_bytes) != auth["plan_sha256"] or len(plan_bytes) != auth["plan_bytes"]:
        refuse("return-line-plan/1", "plan hash or length does not match the recorded release", "Point the command at the authorized plan. Editing the plan drops the old pin.", state="conflict")
    plan_body = module.loads(plan_bytes, "return-line-plan/1")
    if not isinstance(plan_body, dict) or plan_body.get("live_moves") is not False or plan_body.get("live_apply") is not False:
        refuse("return-line-plan/1", "plan is not a read-only plan", "Keep live_moves and live_apply false. This file is not permission to move.")
    for label, arg, bound in (
        ("backup", backup, auth["backup_root"]),
        ("staging", staging, auth["staging_root"]),
        ("retired", retired, auth["retired_root"]),
    ):
        if module.norm(os.path.abspath(arg)) != module.norm(bound):
            refuse(RECORDED_SCHEMA, f"{label} does not match the authorization", "Use the root named by the recorded release.", evidence=label)
    backup_abs, staging_abs, retired_abs = call_roots(book_abs, backup, staging, retired)
    same_volume(book_abs, [backup_abs, staging_abs, retired_abs])
    parents_ready({"backup": backup_abs, "staging": staging_abs, "retired": retired_abs})
    if checks_book_sources(operation):
        report = source_report(book_abs, audit)
    else:
        report = {
            "audit_bytes": len(audit_bytes),
            "audit_sha256": module.sha(audit_bytes),
            "source_files_checked": 0,
            "source_mismatch_count": 0,
            "source_example": None,
            "unassigned_count": 0,
        }
    if checks_book_sources(operation) and report["source_mismatch_count"]:
        refuse(
            "stale source",
            "source bytes no longer match the audit",
            "Stop before mutation. Refreshing the plan requires a new recorded release.",
            evidence=None if report["source_example"] is None else report["source_example"].get("path"),
            state="conflict",
            detail=report,
        )
    differed = binding_difference(release, auth)
    if differed is not None:
        refuse(RECORDED_SCHEMA, "authorization binding disagrees with the release file", "Do not prefer either side. Write a new release file and pin it.", evidence=differed, state="conflict")
    return {
        "audit": os.path.abspath(audit),
        "auth": auth,
        "backup": backup_abs,
        "book": book_abs,
        "layout": laid,
        "layout_sha256": auth["layout_sha256"],
        "mode": "recorded",
        "plan_sha256": auth["plan_sha256"],
        "release": release,
        "report": report,
        "retired": retired_abs,
        "staging": staging_abs,
    }


def load_recorded(book_abs: str, auth_path: str, body: dict) -> tuple[dict, dict]:
    require_recorded_shape(body)
    auth_abs = outside_book(book_abs, auth_path, "authorization file")
    release_abs = outside_book(book_abs, body["release_path"], "release file")
    if lines().norm(auth_abs) == lines().norm(release_abs):
        refuse(RECORDED_SCHEMA, "release file is the authorization file", "Pin a separate external release file.")
    raw, release = read_body(release_abs, RELEASE_SCHEMA)
    module = lines()
    if module.sha(raw) != body["release_sha256"] or len(raw) != body["release_bytes"]:
        refuse(RELEASE_SCHEMA, "release bytes no longer match the authorization pin", "The release file changed. Record a new pin. The old approval does not follow it.", state="conflict")
    require_release_shape(release)
    differed = binding_difference(release, body)
    if differed is not None:
        refuse(RECORDED_SCHEMA, "authorization binding disagrees with the release file", "Do not prefer either side. Write a new release file and pin it.", evidence=differed, state="conflict")
    return body, release


def fixture_from_path(auth_path: str, book_abs: str, operation: str | None, name: str | None,
                      audit: str, plan: str, backup: str, staging: str, retired: str) -> dict:
    try:
        auth = load_pass02().load_auth(os.path.abspath(auth_path))
    except lines().LineError as exc:
        refuse(exc.check, exc.reason, exc.correction, evidence=exc.evidence, state=exc.state, detail=exc.detail)
    module = lines()
    if name is not None and name != auth["book"]:
        refuse(FIXTURE_SCHEMA, "init name does not match the authorization book", "Pass the book name, not a path.")
    if operation is not None and operation not in auth["operations"]:
        refuse(FIXTURE_SCHEMA, f"operation {operation} is not authorized", "Add this command to the fixture operations list.", evidence=operation)
    if module.norm(auth["book_path"]) != module.norm(book_abs):
        refuse(FIXTURE_SCHEMA, "authorization book path does not match", "Name the disposable book this command is using.")
    laid = layout_bytes(auth["book"])
    if module.sha(laid) != auth["layout_sha256"]:
        refuse(FIXTURE_SCHEMA, "layout hash does not match the line-pass declaration", "Bind the hash of the pass01 layout body.")
    audit_bytes = module.read_exact(os.path.abspath(audit))
    if module.sha(audit_bytes) != auth["audit_sha256"] or len(audit_bytes) != auth["audit_bytes"]:
        refuse("audit identity", "audit hash or length does not match the authorization", "Point the command at the authorized audit.", state="conflict")
    plan_bytes = module.read_exact(os.path.abspath(plan))
    if module.sha(plan_bytes) != auth["plan_sha256"]:
        refuse("return-line-plan/1", "plan hash does not match the authorization", "Point the command at the authorized plan.", state="conflict")
    for label, arg, bound in (
        ("backup", backup, auth["backup_root"]),
        ("staging", staging, auth["staging_root"]),
        ("retired", retired, auth["retired_root"]),
    ):
        if module.norm(os.path.abspath(arg)) != module.norm(bound):
            refuse(FIXTURE_SCHEMA, f"{label} does not match the authorization", "Use the approved root.", evidence=label)
    backup_abs, staging_abs, retired_abs = call_roots(book_abs, backup, staging, retired)
    same_volume(book_abs, [backup_abs, staging_abs, retired_abs])
    report = source_report(book_abs, audit) if checks_book_sources(operation) else {
        "source_files_checked": 0,
        "source_mismatch_count": 0,
        "source_example": None,
        "unassigned_count": 0,
    }
    if checks_book_sources(operation) and report["source_mismatch_count"]:
        refuse("stale source", "source bytes no longer match the audit", "Preflight refuses before any write.", state="conflict", detail=report,
               evidence=None if report["source_example"] is None else report["source_example"].get("path"))
    return {
        "auth": auth,
        "book": book_abs,
        "layout": laid,
        "layout_sha256": auth["layout_sha256"],
        "mode": "fixture",
        "report": report,
    }


def names_live(body: dict) -> bool:
    book_path = body.get("book_path") if isinstance(body, dict) else None
    return isinstance(book_path, str) and os.path.isabs(book_path) and is_real_live(book_path)


def inspect(authorization: str, operation: str | None, book: str, name: str | None,
            audit: str, plan: str, backup: str, staging: str, retired: str, execute: bool) -> dict:
    if not authorization:
        refuse("authorization", "authorization is absent", "Pass a recorded release or the synthetic fixture.")
    book_abs = os.path.abspath(book)
    if not os.path.lexists(authorization):
        if is_real_live(book_abs):
            refuse("live execution", "this pack does not execute the canonical live book", "This tooling build does not migrate the live book.")
        refuse("authorization", "authorization is absent", "Pass a recorded release or the synthetic fixture.")
    _raw, body, error = peek_record(authorization)
    schema = body.get("schema") if isinstance(body, dict) else None
    if schema == CANDIDATE_SCHEMA:
        refuse_candidate(body, candidate_detail(body, book_abs, audit))
    if is_real_live(book_abs) or names_live(body if isinstance(body, dict) else {}):
        refuse(
            "live execution",
            "this pack does not execute the canonical live book",
            "This tooling build does not migrate the live book. The test seam cannot lift this check.",
        )
    if error is not None:
        refuse(error.check, error.reason, error.correction, evidence=error.evidence, state=error.state, detail=error.detail)
    if not isinstance(body, dict):
        refuse("authorization", "authorization schema is not a known record", "Use a fixture, a recorded release, or a candidate.")
    if schema == FIXTURE_SCHEMA:
        if is_designated(book_abs):
            refuse(FIXTURE_SCHEMA, "fixture authorization cannot authorize a designated-live book", "Use a recorded release for a designated copy. A synthetic fixture is not that release.")
        if execute:
            return {"mode": "fixture"}
        return fixture_from_path(authorization, book_abs, operation, name, audit, plan, backup, staging, retired)
    if schema == RECORDED_SCHEMA:
        if not is_designated(book_abs):
            refuse(RECORDED_SCHEMA, "recorded release requires a designated-live identity", "The production CLI has no live override. Tests designate a disposable copy in-process.")
        auth, release = load_recorded(book_abs, authorization, body)
        return check_materials(book_abs, auth, release, operation, name, audit, plan, backup, staging, retired)
    refuse("authorization", "authorization schema is not a known record", "Use a fixture, a recorded release, or a candidate.")
    return {}


def peek_record(path: str):
    module = lines()
    try:
        raw = module.read_exact(os.path.abspath(path))
        body = module.loads(raw, "authorization")
    except module.LineError as exc:
        return None, None, exc
    return raw, body, None


def materialize(found: dict) -> dict:
    module = load_pass02()
    return {
        "audit": found["audit"],
        "auth": found["auth"],
        "backup": module.ensure_dir(found["backup"], "backup"),
        "book": found["book"],
        "layout": found["layout"],
        "layout_sha256": found["layout_sha256"],
        "plan_sha256": found["plan_sha256"],
        "retired": module.ensure_dir(found["retired"], "retired"),
        "staging": module.ensure_dir(found["staging"], "staging"),
    }


def require_authorization(authorization: str, operation: str, book: str, name: str | None,
                          audit: str, plan: str, backup: str, staging: str, retired: str) -> dict:
    found = inspect(authorization, operation, book, name, audit, plan, backup, staging, retired, True)
    if found["mode"] == "fixture":
        return _ORIG_REQUIRE(authorization, operation, book, name, audit, plan, backup, staging, retired)
    return materialize(found)


def needs_auth(command: str, book: str) -> bool:
    if is_real_live(book) or is_designated(book):
        return True
    return _ORIG_NEEDS(command, book)


def live_refusal(book: str) -> None:
    if is_real_live(book):
        refuse(
            "live execution",
            "this pack does not execute the canonical live book",
            "This tooling build does not migrate the live book.",
        )


def patched_assert(book_abs: str) -> None:
    module = lines()
    pass02 = load_pass02()
    if is_real_live(book_abs):
        raise module.LineError(
            "live execution",
            "this pack does not execute the canonical live book",
            "This tooling build does not migrate the live book. The test seam cannot lift this check. " + ESCALATION,
        )
    designated = is_designated(book_abs)
    has_door = os.path.lexists(os.path.join(book_abs, module.DOOR))
    if has_door or designated:
        bound = pass02._BOUND.get()
        if bound is None or module.norm(bound["book"]) != module.norm(book_abs):
            reason = "designated-live book has no bound recorded release" if designated else "book contains 0100.band.returns"
            raise module.LineError(
                "live execution" if designated else "live book",
                reason,
                "Pass a release bound to this book. " + ESCALATION,
            )
        auth = bound["auth"]
        if designated:
            if auth.get("schema") != RECORDED_SCHEMA or auth.get("synthetic") is not False:
                raise module.LineError(
                    RECORDED_SCHEMA,
                    "designated-live book requires a recorded release",
                    "A synthetic fixture cannot authorize this identity. " + ESCALATION,
                    state="refused",
                )
            return
        if auth.get("schema") != FIXTURE_SCHEMA or auth.get("synthetic") is not True:
            raise module.LineError(
                FIXTURE_SCHEMA,
                "door-marked copy requires the synthetic fixture schema",
                "Use return-line-authorization/1 with synthetic true on a copy that is not designated live. " + ESCALATION,
                state="refused",
            )
        return
    pass02._ORIGINAL_ASSERT(book_abs)


def success_detail(found: dict, operation: str | None) -> dict:
    report = found.get("report") or {}
    auth = found["auth"]
    detail = {
        "acceptance": None,
        "accepted": False,
        "approved": False,
        "audit_bytes": report.get("audit_bytes"),
        "audit_sha256": report.get("audit_sha256"),
        "authority_schema": auth.get("schema"),
        "designated_live": is_designated(found.get("book", "")) if found.get("book") else False,
        "executed": False,
        "live_execution": False,
        "mutated": False,
        "operation": operation,
        "plan_sha256": auth.get("plan_sha256"),
        "published": False,
        "release_sha256": auth.get("release_sha256"),
        "source_files_checked": report.get("source_files_checked"),
        "source_mismatch_count": report.get("source_mismatch_count", 0),
        "unassigned_count": report.get("unassigned_count"),
    }
    return detail


def preflight_main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(prog="return_lines.py preflight")
    parser.add_argument("--book", required=True)
    parser.add_argument("--authorization", required=True)
    parser.add_argument("--audit", required=True)
    parser.add_argument("--plan", required=True)
    parser.add_argument("--backup", required=True)
    parser.add_argument("--staging", required=True)
    parser.add_argument("--retired", required=True)
    parser.add_argument("--operation", default=None)
    args = parser.parse_args(argv)
    module = lines()
    try:
        found = inspect(
            args.authorization, args.operation, args.book, None, args.audit, args.plan,
            args.backup, args.staging, args.retired, False,
        )
    except module.LineError as exc:
        correction = exc.correction if "Escalation:" in exc.correction else exc.correction.rstrip() + " " + ESCALATION
        result = module.envelope("preflight", exc.check, exc.state, exc.exit_code, correction, exc.evidence, None, exc.detail)
        return module.emit(result, False)
    if found.get("mode") == "fixture":
        found = fixture_from_path(
            args.authorization, os.path.abspath(args.book), args.operation, None, args.audit, args.plan,
            args.backup, args.staging, args.retired,
        )
    detail = success_detail(found, args.operation)
    result = module.envelope(
        "preflight", "readiness", "complete", 0,
        "Read-only preflight matched this record. Nothing was written. This is not execution and not live authority.",
        os.path.basename(args.authorization), None, detail,
    )
    return module.emit(result, False)


def main(argv: list[str] | None = None) -> int:
    load_pass02()
    args = list(sys.argv[1:] if argv is None else argv)
    if args and args[0] == "preflight":
        return preflight_main(args[1:])
    return load_pass02().main(args)


if __name__ == "__main__":
    sys.exit(main())
