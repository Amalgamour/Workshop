#!/usr/bin/env python3
"""Recorded-release authorization over frozen return-lines pass03.

This file loads pass03 by pin and does not edit it. Pass03 loads pass02 by
pin, and pass02 loads pass01 by pin. A matching record is readiness for the
named operations. It is not acceptance, seating, or a live migration.
This build does not create a release for the real workbook.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import os
import sys

sys.dont_write_bytecode = True

TOOL_PATH = "labs/return-lines-pass04/return_lines.py"
PASS03_PATH = "labs/return-lines-pass03/return_lines.py"
PASS03_SHA = "78cc4d8679bb6e54b3f2456ce777643da7a9a650ef5c79c216abd38a4c209c63"
PASS03_BYTES = 33349
FIXTURE_SCHEMA = "return-line-authorization/1"
RECORDED_SCHEMA = "return-line-recorded-release/1"
CANDIDATE_SCHEMA = "return-line-release-candidate/1"
ESCALATION = (
    "Escalation: Codex Prime on 0521.return-placement/05.06. "
    "This tool does not decide meaning, acceptance, or live authority. "
    "A matching record is not a release to execute, and this build does not create one."
)
_P3 = None
_ORIG_REQUIRE = None
_CLASSIFIED = {"path": None}


def repo_root() -> str:
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.abspath(os.path.join(here, "..", ".."))


def load_pass03():
    global _P3, _ORIG_REQUIRE
    if _P3 is not None:
        return _P3
    path = os.path.join(repo_root(), *PASS03_PATH.split("/"))
    with open(path, "rb") as handle:
        data = handle.read()
    if hashlib.sha256(data).hexdigest() != PASS03_SHA or len(data) != PASS03_BYTES:
        raise SystemExit("refused: pass03 pin mismatch; nothing was written")
    spec = importlib.util.spec_from_file_location("return_lines_pass03_pinned", path)
    if spec is None or spec.loader is None:
        raise SystemExit("refused: pass03 did not load; nothing was written")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    pass02 = module.load_pass02()
    _ORIG_REQUIRE = module._ORIG_REQUIRE
    pass02.patched_assert = patched_assert
    pass02.require_authorization = require_authorization
    pass02.needs_auth = needs_auth
    pass02.live_refusal = live_refusal
    pass02.load_lines().assert_mutable = patched_assert
    _P3 = module
    return module


def lines():
    return load_pass03().load_pass02().load_lines()


def classify_canonical(path: str) -> None:
    """Test seam. Not a CLI flag. Reports one disposable path as the canonical identity."""
    if not isinstance(path, str) or not os.path.isabs(path):
        raise ValueError("classify_canonical expects an absolute disposable path")
    absolute = os.path.abspath(path)
    module = lines()
    if module.norm(absolute) == module.norm(module.live_book_path()):
        raise ValueError("classify_canonical does not retarget the real workbook")
    _CLASSIFIED["path"] = absolute


def clear_classification() -> None:
    _CLASSIFIED["path"] = None


def arm_fault(phase: str, skip: int, mode: str) -> None:
    load_pass03().arm_fault(phase, skip, mode)


def clear_fault() -> None:
    load_pass03().clear_fault()


def is_canonical(path: str) -> bool:
    module = lines()
    absolute = module.norm(os.path.abspath(path))
    if absolute == module.norm(module.live_book_path()):
        return True
    chosen = _CLASSIFIED["path"]
    if chosen is None:
        return False
    return absolute == module.norm(chosen)


def names_canonical(body: dict) -> bool:
    book_path = body.get("book_path") if isinstance(body, dict) else None
    return isinstance(book_path, str) and os.path.isabs(book_path) and is_canonical(book_path)


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


def raise_translated(exc) -> None:
    predecessor = load_pass03().ESCALATION
    correction = exc.correction.replace(predecessor, ESCALATION)
    if "Escalation:" not in correction:
        correction = correction.rstrip() + " " + ESCALATION
    raise lines().LineError(
        exc.check, exc.reason, correction, evidence=exc.evidence, exit_code=exc.exit_code,
        state=exc.state, detail=exc.detail,
    )


def call_checked(fn):
    try:
        return fn()
    except lines().LineError as exc:
        raise_translated(exc)


def inspect(authorization: str, operation: str | None, book: str, name: str | None,
            audit: str, plan: str, backup: str, staging: str, retired: str, execute: bool) -> dict:
    if not authorization or not os.path.lexists(authorization):
        refuse("authorization", "authorization is absent", "Pass a recorded release or the synthetic fixture.")
    book_abs = os.path.abspath(book)
    predecessor = load_pass03()
    _raw, body, error = predecessor.peek_record(authorization)
    schema = body.get("schema") if isinstance(body, dict) else None
    if schema == CANDIDATE_SCHEMA:
        try:
            predecessor.refuse_candidate(body, predecessor.candidate_detail(body, book_abs, audit))
        except lines().LineError as exc:
            raise_translated(exc)
    if error is not None:
        raise_translated(error)
    if not isinstance(body, dict):
        refuse("authorization", "authorization schema is not a known record", "Use a fixture, a recorded release, or a candidate.")
    if schema == FIXTURE_SCHEMA:
        if is_canonical(book_abs) or names_canonical(body):
            refuse(
                FIXTURE_SCHEMA,
                "fixture authorization cannot authorize the canonical book",
                "A synthetic fixture is not a recorded Director release.",
            )
        if execute:
            return {"mode": "fixture"}
        return call_checked(lambda: predecessor.fixture_from_path(
            authorization, book_abs, operation, name, audit, plan, backup, staging, retired,
        ))
    if schema == RECORDED_SCHEMA:
        if body.get("synthetic") is not False:
            refuse(
                RECORDED_SCHEMA,
                "synthetic fixture is not a recorded release",
                "A synthetic fixture cannot authorize a recorded-release operation.",
            )
        def load():
            auth, release = predecessor.load_recorded(book_abs, authorization, body)
            return predecessor.check_materials(
                book_abs, auth, release, operation, name, audit, plan, backup, staging, retired,
            )
        return call_checked(load)
    refuse("authorization", "authorization schema is not a known record", "Use a fixture, a recorded release, or a candidate.")
    return {}


def require_authorization(authorization: str, operation: str, book: str, name: str | None,
                          audit: str, plan: str, backup: str, staging: str, retired: str) -> dict:
    found = inspect(authorization, operation, book, name, audit, plan, backup, staging, retired, True)
    if found.get("mode") == "fixture":
        return _ORIG_REQUIRE(authorization, operation, book, name, audit, plan, backup, staging, retired)
    return load_pass03().materialize(found)


def needs_auth(command: str, book: str) -> bool:
    if is_canonical(book):
        return True
    return load_pass03()._ORIG_NEEDS(command, book)


def live_refusal(book: str) -> None:
    """Binding is decided by require_authorization and patched_assert."""
    return None


def patched_assert(book_abs: str) -> None:
    module = lines()
    pass02 = load_pass03().load_pass02()
    canonical = is_canonical(book_abs)
    has_door = os.path.lexists(os.path.join(book_abs, module.DOOR))
    if canonical or has_door:
        bound = pass02._BOUND.get()
        if bound is None or module.norm(bound["book"]) != module.norm(book_abs):
            if canonical:
                raise module.LineError(
                    RECORDED_SCHEMA,
                    "canonical book has no bound recorded release",
                    "Pass a recorded release bound to this book in this process. " + ESCALATION,
                )
            raise module.LineError(
                "live book",
                "book contains 0100.band.returns",
                "Pass an authorization bound to this book. " + ESCALATION,
            )
        auth = bound["auth"]
        recorded = auth.get("schema") == RECORDED_SCHEMA and auth.get("synthetic") is False
        if recorded:
            return
        if canonical or auth.get("schema") != FIXTURE_SCHEMA or auth.get("synthetic") is not True:
            check = RECORDED_SCHEMA if canonical else FIXTURE_SCHEMA
            reason = (
                "fixture authorization cannot authorize the canonical book"
                if canonical
                else "door-marked copy requires a fixture or a recorded release"
            )
            raise module.LineError(
                check, reason,
                "A synthetic fixture cannot authorize the canonical book. " + ESCALATION,
                state="refused",
            )
        return
    pass02._ORIGINAL_ASSERT(book_abs)


def success_detail(found: dict, operation: str | None) -> dict:
    report = found.get("report") or {}
    auth = found.get("auth") or {}
    book = found.get("book") or ""
    return {
        "acceptance": None,
        "accepted": False,
        "approved": False,
        "audit_bytes": report.get("audit_bytes"),
        "audit_sha256": report.get("audit_sha256"),
        "authority_schema": auth.get("schema"),
        "canonical": is_canonical(book) if book else False,
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
    detail = success_detail(found, args.operation)
    result = module.envelope(
        "preflight", "readiness", "complete", 0,
        "Read-only preflight matched this record. Nothing was written. This is readiness, not execution and not live authority.",
        os.path.basename(args.authorization), None, detail,
    )
    return module.emit(result, False)


def main(argv: list[str] | None = None) -> int:
    load_pass03()
    args = list(sys.argv[1:] if argv is None else argv)
    if args and args[0] == "preflight":
        return preflight_main(args[1:])
    return load_pass03().main(args)


if __name__ == "__main__":
    sys.exit(main())
