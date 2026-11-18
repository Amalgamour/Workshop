#!/usr/bin/env python3
"""Line/pass reconstruction, publication, and full retirement.

Successor to labs/return-lines-pass01. This file loads that tool by pin
and does not edit it. A receipt is a byte check. It is not approval,
acceptance, seating, or live authority. The publish command installs
bytes on a caller-supplied copy. It does not mark custody published.
"""

from __future__ import annotations

import argparse
import contextvars
import hashlib
import importlib.util
import os
import sys

sys.dont_write_bytecode = True

TOOL_PATH = "labs/return-lines-pass02/return_lines.py"
PASS01_PATH = "labs/return-lines-pass01/return_lines.py"
PASS01_SHA = "863968c59974d85910626ba5e80cf49f14a3186c8d33b855efe00bf6ccec378a"
PASS01_BYTES = 100897
AUTH_SCHEMA = "return-line-authorization/1"
RECON_JOURNAL = "reconstruction-journal.json"
RECON_MANIFEST = "reconstruction-manifest.json"
RECON_MARKER = "reconstruction-complete.json"
PUBLISH_JOURNAL = "publish-journal.json"
PUBLISH_MARKER = "publish-complete.json"
RETIRE_JOURNAL = "retire-journal.json"
RETIRE_MARKER = "retire-complete.json"
RETIRE_POINTER = "retirement-pointer.json"
ESCALATION = (
    "Escalation: Codex Prime on 0521.return-placement/05.04. "
    "This tool does not decide meaning, acceptance, or live authority. "
    "Live migration is not released."
)
RELEASE_TEXT = (
    "Work in D:\\Git\\lib-build.\n"
    "\n"
    "Run:\n"
    "D:\\Git\\lib-build\\00.kernel\\00.00.10.work\\0521.return-placement\\05.04.md\n"
    "\n"
    "This releases the bounded tooling build described there.\n"
    "Reconstruct and verify the correct return pages before retirement.\n"
    "Test full retirement, old-identity lookup, rollback and first new filings\n"
    "on disposable copies, preserving all original bytes.\n"
    "\n"
    "No live moves or app/caller changes. Return with evidence and stop\n"
    "for Codex Prime review.\n"
)
AUTH_KEYS = {
    "schema", "synthetic", "executor", "release", "book", "book_path",
    "layout_sha256", "plan_sha256", "audit_sha256", "audit_bytes",
    "backup_root", "staging_root", "retired_root", "operations",
}
ALWAYS_AUTH = {
    "reconstruct", "reconstruct-resume", "publish", "publish-resume",
    "retire", "retire-resume", "rollback-publish", "rollback-retire",
}
REFUSED_ADOPT = {"adopt", "adopt-resume", "rollback-adopt"}
_BOUND = contextvars.ContextVar("return_lines_pass02_bound", default=None)
_FAULT = {"armed": False, "phase": None, "skip": 0, "mode": None}
_LINES = None
_ORIGINAL_ASSERT = None
_TOOL_SHA = None


def repo_root() -> str:
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.abspath(os.path.join(here, "..", ".."))


def tool_sha() -> str:
    global _TOOL_SHA
    if _TOOL_SHA is None:
        with open(os.path.abspath(__file__), "rb") as handle:
            _TOOL_SHA = hashlib.sha256(handle.read()).hexdigest()
    return _TOOL_SHA


def load_lines():
    global _LINES, _ORIGINAL_ASSERT
    if _LINES is not None:
        return _LINES
    path = os.path.join(repo_root(), *PASS01_PATH.split("/"))
    with open(path, "rb") as handle:
        data = handle.read()
    digest = hashlib.sha256(data).hexdigest()
    if digest != PASS01_SHA or len(data) != PASS01_BYTES:
        raise SystemExit("refused: pass01 pin mismatch; nothing was written")
    spec = importlib.util.spec_from_file_location("return_lines_pass01_pinned", path)
    if spec is None or spec.loader is None:
        raise SystemExit("refused: pass01 did not load; nothing was written")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    _ORIGINAL_ASSERT = module.assert_mutable
    module.assert_mutable = patched_assert
    _LINES = module
    return module


def patched_assert(book_abs: str) -> None:
    lines = load_lines()
    if lines.norm(book_abs) == lines.norm(lines.live_book_path()):
        raise lines.LineError(
            "live book",
            "mutating command refused on the live work book",
            "Use a disposable copy. This build does not release live migration. " + ESCALATION,
        )
    door = os.path.join(book_abs, lines.DOOR)
    if os.path.lexists(door):
        bound = _BOUND.get()
        if bound is None or lines.norm(bound["book"]) != lines.norm(book_abs):
            raise lines.LineError(
                "live book",
                "book contains 0100.band.returns",
                "Pass an explicit synthetic authorization that names this book. " + ESCALATION,
            )
        if bound["auth"].get("synthetic") is not True:
            raise lines.LineError(
                AUTH_SCHEMA,
                "synthetic authorization required; this build does not release live execution",
                "Mark the fixture synthetic. A Prime label is not a live release. " + ESCALATION,
                state="refused",
            )
        return
    _ORIGINAL_ASSERT(book_abs)


def arm_fault(phase: str, skip: int, mode: str) -> None:
    """Test seam. Not a CLI flag. Writes a short file, then stops."""
    if mode != "partial" or not isinstance(skip, int) or skip < 0:
        raise ValueError("arm_fault expects phase, skip>=0, mode 'partial'")
    _FAULT.update(armed=True, phase=phase, skip=skip, mode=mode)


def clear_fault() -> None:
    _FAULT.update(armed=False, phase=None, skip=0, mode=None)


def take_fault(phase: str) -> str | None:
    if not _FAULT["armed"] or _FAULT["phase"] != phase:
        return None
    if _FAULT["skip"] > 0:
        _FAULT["skip"] -= 1
        return None
    _FAULT["armed"] = False
    return _FAULT["mode"]


def refuse(check: str, reason: str, correction: str, evidence: str | None = None,
           exit_code: int = 2, state: str = "refused", detail: dict | None = None) -> None:
    text = correction.rstrip()
    if reason and reason not in text:
        text = f"{reason}. {text}"
    if "Escalation:" not in text:
        text = text + " " + ESCALATION
    correction = text
    raise load_lines().LineError(
        check, reason, correction, evidence=evidence, exit_code=exit_code, state=state, detail=detail or {},
    )


def guard(command: str, fn):
    lines = load_lines()
    try:
        return fn()
    except lines.LineError as exc:
        correction = exc.correction
        if exc.exit_code != 0 and "Escalation:" not in correction:
            correction = correction.rstrip() + " " + ESCALATION
        return lines.envelope(
            command, exc.check, exc.state, exc.exit_code, correction,
            exc.evidence, exc.descriptor, exc.detail,
        )
    except OSError as exc:
        return lines.envelope(
            command, "filesystem", "refused", 2,
            f"{type(exc).__name__}: {exc.strerror or exc}. {ESCALATION}",
            None, None, {},
        )


def ok(command: str, check: str, correction: str, evidence: str, detail: dict) -> dict:
    return load_lines().envelope(command, check, "complete", 0, correction, evidence, None, detail)


def counts_detail(records: list, planned: list, extra: dict | None = None) -> dict:
    detail = {
        "file_count": len(planned),
        "incomplete_count": sum(1 for item in records if item["state"] == "incomplete"),
        "page_local_count": sum(1 for item in records if item["page_local"]),
        "record_count": len(records),
    }
    if extra:
        detail.update(extra)
    return detail


def under(root: str, rel: str) -> str:
    lines = load_lines()
    parts = rel.split("/")
    if any(part in ("", ".", "..") for part in parts):
        refuse("filesystem", f"unsafe relative path {rel}", "Use a normalized relative path.", evidence=rel)
    return lines.assert_contained(root, os.path.join(root, *parts))


def ensure_dir(path: str, label: str) -> str:
    lines = load_lines()
    absolute = os.path.abspath(path)
    parent = os.path.dirname(absolute)
    if not os.path.isdir(absolute):
        if os.path.lexists(absolute):
            refuse("filesystem", f"{label} is not a directory", f"Pass a directory for {label}.")
        if not parent or not os.path.isdir(parent):
            refuse("filesystem", f"{label} parent is missing", "Create the parent outside the book.")
        os.makedirs(absolute)
    if lines.is_reparse(absolute):
        refuse("filesystem", f"{label} is a link", "Use a real directory.")
    return absolute


def live_refusal(book: str) -> None:
    lines = load_lines()
    if lines.norm(os.path.abspath(book)) == lines.norm(lines.live_book_path()):
        refuse(
            "live book",
            "mutating command refused on the live work book",
            "Use a disposable copy. This build does not release live migration.",
        )


def roots_ok(book_abs: str, backup: str, staging: str, retired: str) -> tuple[str, str, str]:
    lines = load_lines()
    live = lines.live_book_path()
    found = {}
    for label, value in (("backup", backup), ("staging", staging), ("retired", retired)):
        absolute = os.path.abspath(value)
        if (
            lines.within(book_abs, absolute) or lines.within(absolute, book_abs)
            or lines.norm(absolute) == lines.norm(book_abs)
        ):
            refuse("filesystem", f"{label} overlaps the book", "Place this root outside the book.", evidence=label)
        if lines.within(live, absolute) or lines.norm(absolute) == lines.norm(live):
            refuse("live book", f"{label} is inside the live work book", "Place this root outside the live book.", evidence=label)
        if os.path.lexists(os.path.join(absolute, lines.DOOR)):
            refuse("live book", f"{label} contains 0100.band.returns", "Do not use the live door as a root.", evidence=label)
        found[label] = absolute
    names = ("backup", "staging", "retired")
    for index, left in enumerate(names):
        for right in names[index + 1:]:
            a, b = found[left], found[right]
            if lines.within(a, b) or lines.within(b, a) or lines.norm(a) == lines.norm(b):
                refuse("filesystem", f"{left} overlaps {right}", "Use three roots that do not contain each other.")
    return found["backup"], found["staging"], found["retired"]


def load_auth(path: str) -> dict:
    lines = load_lines()
    body = lines.loads(lines.read_exact(os.path.abspath(path)), AUTH_SCHEMA)
    lines.expect_keys(body, AUTH_KEYS, AUTH_SCHEMA, "authorization")
    if body["schema"] != AUTH_SCHEMA:
        refuse(AUTH_SCHEMA, "authorization schema is not return-line-authorization/1", "Write the synthetic fixture with this schema.")
    if body["synthetic"] is not True:
        refuse(
            AUTH_SCHEMA,
            "synthetic authorization required; this build does not release live execution",
            "Mark the fixture synthetic. A Prime label is not a live release.",
        )
    if body["executor"] != "Codex Prime":
        refuse(AUTH_SCHEMA, "recorded executor is not Codex Prime", "The builder does not authorize this operation.")
    if body["release"] != RELEASE_TEXT:
        refuse(AUTH_SCHEMA, "release text does not match the recorded Director invocation", "Use the invocation bytes in release.txt.")
    if body["book"] != "00.00.10.work":
        refuse(AUTH_SCHEMA, "authorization book name is not 00.00.10.work", "Name the book, not a filesystem path.")
    if not isinstance(body["operations"], list) or not body["operations"] or any(not isinstance(item, str) for item in body["operations"]):
        refuse(AUTH_SCHEMA, "operations are not a list of command names", "Name each command. There is no blanket force.")
    if len(body["operations"]) != len(set(body["operations"])):
        refuse(AUTH_SCHEMA, "operations are not unique", "Name each command once.")
    for key in ("layout_sha256", "plan_sha256", "audit_sha256"):
        if not isinstance(body[key], str) or len(body[key]) != 64:
            refuse(AUTH_SCHEMA, f"{key} is not a sha256", "Bind the reviewed hash.")
    if not isinstance(body["audit_bytes"], int) or body["audit_bytes"] < 0:
        refuse(AUTH_SCHEMA, "audit_bytes is not a length", "Bind the audit length.")
    for key in ("book_path", "backup_root", "staging_root", "retired_root"):
        if not isinstance(body[key], str) or not os.path.isabs(body[key]):
            refuse(AUTH_SCHEMA, f"{key} is not an absolute path", "Use an absolute disposable path.")
    return body


def require_authorization(authorization: str, operation: str, book: str, name: str | None,
                          audit: str, plan: str, backup: str, staging: str, retired: str) -> dict:
    lines = load_lines()
    live_refusal(book)
    if not authorization:
        book_abs = os.path.abspath(book)
        if os.path.lexists(os.path.join(book_abs, lines.DOOR)) or operation in ALWAYS_AUTH:
            refuse(
                "live book",
                "book contains 0100.band.returns" if os.path.lexists(os.path.join(book_abs, lines.DOOR)) else "authorization is absent",
                "Pass an explicit synthetic authorization for this operation.",
            )
        raise AssertionError("caller should not require authorization")
    auth = load_auth(authorization)
    if lines.norm(auth["book_path"]) == lines.norm(lines.live_book_path()):
        refuse("live book", "mutating command refused on the live work book", "Use a disposable copy. This build does not release live migration.")
    book_abs = lines.require_dir(book, "book")
    if lines.norm(book_abs) == lines.norm(lines.live_book_path()):
        refuse("live book", "mutating command refused on the live work book", "Use a disposable copy. This build does not release live migration.")
    if lines.norm(auth["book_path"]) != lines.norm(book_abs):
        refuse(AUTH_SCHEMA, "authorization book path does not match", "Name the disposable book this command is using.", evidence=book)
    if name is not None and name != auth["book"]:
        refuse(AUTH_SCHEMA, "init name does not match the authorization book", "Pass the book name, not a path.")
    if operation not in auth["operations"]:
        refuse(AUTH_SCHEMA, f"operation {operation} is not authorized", "Add this command to the fixture operations list.", evidence=operation)
    layout = lines.dump(lines.layout_body(auth["book"]))
    if lines.sha(layout) != auth["layout_sha256"]:
        refuse(AUTH_SCHEMA, "layout hash does not match the line-pass declaration", "Bind the hash of the pass01 layout body.")
    layout_path = os.path.join(book_abs, lines.LAYOUT_NAME)
    if os.path.lexists(layout_path) and lines.read_exact(layout_path) != layout:
        refuse("return-line-layout/1", "layout bytes differ", "Do not overwrite a different declaration.", evidence=lines.LAYOUT_NAME, state="conflict")
    audit_bytes = lines.read_exact(os.path.abspath(audit))
    if lines.sha(audit_bytes) != auth["audit_sha256"] or len(audit_bytes) != auth["audit_bytes"]:
        refuse("audit identity", "audit hash or length does not match the authorization", "Point the command at the authorized audit.", state="conflict")
    plan_bytes = lines.read_exact(os.path.abspath(plan))
    if lines.sha(plan_bytes) != auth["plan_sha256"]:
        refuse("return-line-plan/1", "plan hash does not match the authorization", "Point the command at the authorized plan.", state="conflict")
    for label, arg, bound in (
        ("backup", backup, auth["backup_root"]),
        ("staging", staging, auth["staging_root"]),
        ("retired", retired, auth["retired_root"]),
    ):
        if lines.norm(os.path.abspath(arg)) != lines.norm(bound):
            refuse(AUTH_SCHEMA, f"{label} does not match the authorization", "Use the approved root.", evidence=label)
    backup_abs, staging_abs, retired_abs = roots_ok(book_abs, backup, staging, retired)
    return {
        "auth": auth,
        "book": book_abs,
        "backup": ensure_dir(backup_abs, "backup"),
        "staging": ensure_dir(staging_abs, "staging"),
        "retired": ensure_dir(retired_abs, "retired"),
        "audit": os.path.abspath(audit),
        "plan_sha256": auth["plan_sha256"],
        "layout_sha256": auth["layout_sha256"],
        "layout": layout,
    }


def bind_call(bound: dict, fn):
    token = _BOUND.set(bound)
    try:
        return fn()
    finally:
        _BOUND.reset(token)


def needs_auth(command: str, book: str) -> bool:
    lines = load_lines()
    if command in ALWAYS_AUTH or command in REFUSED_ADOPT:
        return True
    book_abs = os.path.abspath(book)
    if lines.norm(book_abs) == lines.norm(lines.live_book_path()):
        return True
    if os.path.lexists(os.path.join(book_abs, lines.DOOR)):
        return True
    return False


def prepared_or_stop(layout: dict, audit: dict) -> list:
    lines = load_lines()
    prepared, blocked = lines.prepare_records(layout, audit)
    if blocked:
        refuse(blocked[0]["check"], blocked[0]["reason"], "Audit identity disagrees with the route. No retirement was performed.", evidence=blocked[0].get("evidence"), state="conflict", detail={"blocked": blocked})
    return prepared


def require_stage(backup_abs: str, audit_sha: str) -> dict:
    lines = load_lines()
    marker_path = os.path.join(backup_abs, lines.STAGE_MARKER)
    if not os.path.lexists(marker_path):
        refuse("return-line-stage-complete/1", "stage marker is absent", "Finish staging every source before reconstruction.", evidence=lines.STAGE_MARKER)
    marker = lines.loads(lines.read_exact(marker_path), "return-line-stage-complete/1")
    if not isinstance(marker, dict) or marker.get("audit_sha256") != audit_sha:
        refuse("audit identity", "stage marker does not match this audit", "Do not reconstruct against a different audit.", evidence=lines.STAGE_MARKER, state="conflict")
    journal_path = os.path.join(backup_abs, lines.STAGE_JOURNAL)
    raw = lines.read_exact(journal_path)
    if lines.sha(raw) != marker.get("journal_sha256"):
        refuse("return-line-stage-journal/1", "stage journal does not match its marker", "Keep the journal.", state="conflict")
    journal = lines.loads(raw, "return-line-stage-journal/1")
    for item in journal.get("files", []):
        path = os.path.join(backup_abs, *item["backup_rel"].split("/"))
        data = lines.read_exact(path)
        if lines.sha(data) != item["sha256"] or len(data) != item["bytes"] or not item.get("match"):
            refuse("rollback copy", "backup bytes no longer match the stage journal", "Stop. Keep the backup evidence.", evidence=item.get("backup_rel"), state="conflict")
    return marker


def snapshot_dir(root: str) -> list[dict]:
    lines = load_lines()
    rows = []
    for rel in lines.walk_files(root):
        data = lines.read_exact(os.path.join(root, *rel.split("/")))
        rows.append({"bytes": len(data), "rel": rel, "sha256": lines.sha(data)})
    return rows


def dirs_match(book_dir: str, backup_dir: str, evidence: str) -> list[dict]:
    lines = load_lines()
    if not os.path.isdir(backup_dir):
        refuse("rollback copy", "staged source is missing", "Restore the stage backup before this phase.", evidence=evidence)
    left = lines.walk_files(book_dir)
    right = lines.walk_files(backup_dir)
    if left != right:
        refuse("audit identity", "book member no longer matches the staged source", "Stop. The book member was not moved.", evidence=evidence, state="conflict")
    rows = []
    for rel in left:
        a = lines.read_exact(os.path.join(book_dir, *rel.split("/")))
        b = lines.read_exact(os.path.join(backup_dir, *rel.split("/")))
        if a != b:
            refuse("audit identity", "book member bytes differ from the staged source", "Stop. The book member was not moved.", evidence=f"{evidence}/{rel}", state="conflict")
        rows.append({"bytes": len(a), "rel": rel, "sha256": lines.sha(a)})
    return rows


def build_plan_rows(book_abs: str, backup_abs: str, prepared: list) -> tuple[list, list]:
    lines = load_lines()
    planned = []
    records = []
    seen: dict[str, dict] = {}
    for record, route in prepared:
        member = record["old_member"]
        source = os.path.join(backup_abs, "sources", member)
        if not os.path.isdir(source):
            refuse("rollback copy", "staged source is missing", "Finish staging before reconstruction.", evidence=f"sources/{member}")
        files = lines.walk_files(source)
        has_return = "return.md" in files
        reason = lines.reader_reason(source)
        if record.get("verify_exit") == 0 and (reason is not None or not has_return):
            refuse("sealed reader", reason or "verified record has no return", "Do not reconstruct a source the pinned reader refuses.", evidence=f"sources/{member}", state="conflict")
        if has_return and reason is not None:
            refuse("sealed reader", reason, "A return is present but the pinned reader refused it.", evidence=f"sources/{member}", state="conflict")
        state = "complete" if has_return else "incomplete"
        return_data = lines.read_exact(os.path.join(source, "return.md")) if has_return else None
        reservation = None
        res_path = os.path.join(source, "reservation.json")
        if os.path.lexists(res_path):
            try:
                reservation = lines.loads(lines.read_exact(res_path), "sealed reader")
            except lines.LineError:
                reservation = None
        destination = reservation.get("destination") if isinstance(reservation, dict) else None
        submission = record.get("submission") if isinstance(record.get("submission"), str) else None
        if not has_return:
            return_path = lines.join_book(book_abs, route["return_path"])
            if os.path.lexists(return_path):
                refuse("broken link", "incomplete record already has a return path", "Do not invent a return, and do not keep a stray one as if it were the record.", evidence=route["return_path"], state="conflict")
        else:
            tail_abs = lines.join_book(book_abs, route["return_path"])
            if route["route"] == "page-local-colab":
                if not os.path.lexists(tail_abs):
                    refuse("N7 tail", "page-local tail is missing", "The page-local tail was not invented.", evidence=route["return_path"])
                if lines.read_exact(tail_abs) != return_data:
                    refuse("N7 tail", "page-local tail differs from the member return", "The page-local tail was not overwritten.", evidence=route["return_path"], state="conflict")
            elif os.path.lexists(tail_abs) and lines.read_exact(tail_abs) != return_data:
                refuse("broken link", "existing return bytes differ", "Existing return bytes were not overwritten.", evidence=route["return_path"], state="conflict")
        logicals = []
        for rel in files:
            data = lines.read_exact(os.path.join(source, *rel.split("/")))
            item = {"bytes": len(data), "logical": f"{route['custody_dir']}/{rel}", "old_member": member, "role": "custody", "sha256": lines.sha(data)}
            planned.append(item)
            logicals.append(item["logical"])
        relocation = {
            "custody_format": "legacy-relocated/1",
            "old_member": member,
            "original_destination": destination,
            "reservation_destination_rewritten": False,
            "return_bytes": None if return_data is None else len(return_data),
            "return_sha256": None if return_data is None else lines.sha(return_data),
            "schema": "return-line-relocation/1",
            "source_backup": f"sources/{member}",
        }
        lines.expect_keys(relocation, lines.RELOCATION_KEYS, "return-line-relocation/1", "relocation")
        rel_bytes = lines.dump(relocation)
        item = {"bytes": len(rel_bytes), "logical": f"{route['custody_dir']}/relocation.json", "old_member": member, "role": "relocation", "sha256": lines.sha(rel_bytes)}
        planned.append(item)
        logicals.append(item["logical"])
        if return_data is not None:
            item = {"bytes": len(return_data), "logical": route["return_path"], "old_member": member, "role": "return", "sha256": lines.sha(return_data)}
            planned.append(item)
            logicals.append(item["logical"])
        origin = record["origin"]
        records.append({
            "archived_identity": member,
            "custody_path": route["custody_dir"],
            "has_return": has_return,
            "logical_return_path": route["return_path"],
            "old_member": member,
            "origin": {"batch": origin["batch"], "book": origin["book"], "page": origin["page"]},
            "page_local": route["route"] == "page-local-colab",
            "source_backup": f"sources/{member}",
            "state": state,
            "submission_id": submission,
            "target_number": route["target_number"],
            "target_page": route["target_page"],
            "route": route["route"],
            "files": logicals,
        })
    for item in planned:
        previous = seen.get(item["logical"])
        if previous is not None and (previous["sha256"] != item["sha256"] or previous["bytes"] != item["bytes"]):
            refuse("broken link", "two records disagree on one logical path", "Stop. Neither body was overwritten.", evidence=item["logical"], state="conflict")
        seen[item["logical"]] = item
    planned.sort(key=lambda item: (lines.member_key(item["old_member"]), item["logical"]))
    return planned, records


def short_bytes(data: bytes) -> bytes:
    if len(data) > 1:
        return data[:-1]
    if data == b"\x00":
        return b"\x01"
    return data + b"\x00"


def read_marker(path: str, schema: str) -> dict | None:
    lines = load_lines()
    if not os.path.lexists(path):
        return None
    body = lines.loads(lines.read_exact(path), schema)
    if not isinstance(body, dict) or body.get("schema") != schema:
        refuse(schema, "completion marker does not match its schema", "Keep the marker. Do not delete it.", evidence=os.path.basename(path), state="conflict")
    return body


def journal_at(path: str, schema: str) -> dict | None:
    lines = load_lines()
    body = lines.load_json_file(path, schema)
    if body is None:
        return None
    if body.get("schema") != schema:
        refuse(schema, "journal schema differs", "Keep this journal.", evidence=os.path.basename(path), state="conflict")
    return body


def recon_paths(staging_abs: str) -> tuple[str, str, str]:
    return (
        os.path.join(staging_abs, RECON_JOURNAL),
        os.path.join(staging_abs, RECON_MANIFEST),
        os.path.join(staging_abs, RECON_MARKER),
    )


def manifest_body(bound: dict, audit_sha: str, audit_bytes: int, records: list) -> dict:
    return {
        "audit_bytes": audit_bytes,
        "audit_sha256": audit_sha,
        "incomplete_count": sum(1 for item in records if item["state"] == "incomplete"),
        "layout_sha256": bound["layout_sha256"],
        "page_local_count": sum(1 for item in records if item["page_local"]),
        "plan_sha256": bound["plan_sha256"],
        "record_count": len(records),
        "records": records,
        "schema": "return-line-reconstruction-manifest/1",
    }


def verify_planned(staging_abs: str, planned: list, phrase: str) -> None:
    lines = load_lines()
    for item in planned:
        path = under(staging_abs, "pages/" + item["logical"])
        if not os.path.lexists(path):
            refuse(phrase, "reconstructed file is missing", "Resume onto this staging root or keep a fresh one. Do not delete partial evidence.", evidence=item["logical"], state="conflict")
        data = lines.read_exact(path)
        if lines.sha(data) != item["sha256"] or len(data) != item["bytes"]:
            refuse(phrase, "reconstruction bytes differ", "Keep the partial file. Use a fresh staging root. Do not delete it.", evidence=item["logical"], state="conflict")


def verify_book_links(book_abs: str, planned: list, records: list) -> None:
    lines = load_lines()
    for item in planned:
        path = lines.join_book(book_abs, item["logical"])
        if not os.path.lexists(path):
            refuse("broken link", "logical page file is missing", "Do not retire while a verified link is missing.", evidence=item["logical"], state="conflict")
        data = lines.read_exact(path)
        if lines.sha(data) != item["sha256"] or len(data) != item["bytes"]:
            refuse("return-line-publish-journal/1", "publication bytes differ", "Keep the book bytes. Do not delete them.", evidence=item["logical"], state="conflict")
    for record in records:
        if record["state"] != "incomplete":
            continue
        path = lines.join_book(book_abs, record["logical_return_path"])
        if os.path.lexists(path):
            refuse("broken link", "incomplete record has a return path", "Do not invent the missing return.", evidence=record["logical_return_path"], state="conflict")


def new_recon_journal(bound: dict, audit_sha: str, audit_bytes: int, planned: list, records: list) -> dict:
    return {
        "audit_bytes": audit_bytes,
        "audit_sha256": audit_sha,
        "backup_root": bound["backup"],
        "blocked": [],
        "book": bound["auth"]["book"],
        "complete": False,
        "copied_count": 0,
        "incomplete_count": sum(1 for item in records if item["state"] == "incomplete"),
        "interrupted": False,
        "layout_sha256": bound["layout_sha256"],
        "page_local_count": sum(1 for item in records if item["page_local"]),
        "plan_sha256": bound["plan_sha256"],
        "planned": planned,
        "record_count": len(records),
        "records": records,
        "schema": "return-line-reconstruction-journal/1",
        "staging_root": bound["staging"],
        "written": [],
    }


def reconstruct_run(book: str, authorization: str, audit: str, plan: str, backup: str,
                    staging: str, retired: str, interrupt_after: int | None, resume: bool) -> dict:
    command = "reconstruct-resume" if resume else "reconstruct"

    def work():
        lines = load_lines()
        bound = require_authorization(authorization, command, book, None, audit, plan, backup, staging, retired)
        return bind_call(bound, lambda: reconstruct_bound(command, bound, interrupt_after))

    return guard(command, work)


def reconstruct_bound(command: str, bound: dict, interrupt_after: int | None) -> dict:
    lines = load_lines()
    if interrupt_after is not None and interrupt_after < 0:
        refuse("return-line-reconstruction-journal/1", "interrupt-after is negative", "Use zero or a positive count.")
    book_abs = bound["book"]
    lines.assert_mutable(book_abs)
    layout = lines.read_layout(book_abs)
    audit, audit_sha, audit_bytes = lines.load_audit(bound["audit"])
    require_stage(bound["backup"], audit_sha)
    prepared = prepared_or_stop(layout, audit)
    planned, records = build_plan_rows(book_abs, bound["backup"], prepared)
    journal_path, manifest_path, marker_path = recon_paths(bound["staging"])
    existing = journal_at(journal_path, "return-line-reconstruction-journal/1")
    if existing is None:
        journal = new_recon_journal(bound, audit_sha, audit_bytes, planned, records)
        lines.save_json(journal_path, journal)
    else:
        journal = existing
        if journal.get("audit_sha256") != audit_sha or journal.get("planned") != planned or journal.get("records") != records:
            refuse("audit identity", "reconstruction journal does not match this audit", "Keep the staging tree. Use a fresh staging root for a different plan.", state="conflict")
    marker = read_marker(marker_path, "return-line-reconstruction-complete/1")
    if marker is not None:
        raw = lines.read_exact(journal_path)
        manifest_ok = os.path.lexists(manifest_path) and lines.sha(lines.read_exact(manifest_path)) == marker.get("manifest_sha256")
        if marker.get("audit_sha256") == audit_sha and marker.get("journal_sha256") == lines.sha(raw) and manifest_ok:
            verify_planned(bound["staging"], planned, "return-line-reconstruction-manifest/1")
            return ok(command, "return-line-reconstruction-complete/1",
                      "Reconstruction marker already matches. Nothing was retired.",
                      RECON_MARKER, counts_detail(records, planned))
        refuse("return-line-reconstruction-complete/1", "reconstruction marker differs", "Keep the marker. Do not delete it.", evidence=RECON_MARKER, state="conflict")
    copied = 0
    written = set(journal.get("written") or [])
    for item in planned:
        dest = under(bound["staging"], "pages/" + item["logical"])
        data = None
        if os.path.lexists(dest):
            current = lines.read_exact(dest)
            if lines.sha(current) != item["sha256"] or len(current) != item["bytes"]:
                refuse("return-line-reconstruction-manifest/1", "reconstruction bytes differ",
                       "Keep the partial file. Use a fresh staging root. Do not delete it.",
                       evidence=item["logical"], state="conflict")
            continue
        if interrupt_after is not None and copied >= interrupt_after:
            journal["interrupted"] = True
            journal["complete"] = False
            lines.save_json(journal_path, journal)
            return lines.envelope(command, "return-line-reconstruction-journal/1", "interrupted", 3,
                                  "Reconstruction stopped before the marker. Resume the same staging root. " + ESCALATION,
                                  item["logical"], None, {"copied_this_call": copied})
        payload = expected_payload(bound, item)
        if lines.sha(payload) != item["sha256"] or len(payload) != item["bytes"]:
            refuse("return-line-reconstruction-manifest/1", "reconstruction bytes differ",
                   "The planned bytes were not written. Keep the staging tree.", evidence=item["logical"], state="conflict")
        if take_fault("reconstruct") == "partial":
            # The short file is closed before the refusal. Resume must keep it.
            lines.write_new(dest, short_bytes(payload))
            journal["interrupted"] = True
            journal["complete"] = False
            journal["blocked"] = [{"check": "return-line-reconstruction-manifest/1", "evidence": item["logical"], "reason": "partial bytes kept"}]
            lines.save_json(journal_path, journal)
            return lines.envelope(command, "return-line-reconstruction-journal/1", "interrupted", 3,
                                  "Partial reconstruction bytes were kept. They were not deleted. " + ESCALATION,
                                  item["logical"], None, {"copied_this_call": copied})
        lines.write_new(dest, payload)
        copied += 1
        written.add(item["logical"])
        journal["written"] = sorted(written)
        journal["copied_count"] = len(written)
        lines.save_json(journal_path, journal)
    verify_planned(bound["staging"], planned, "return-line-reconstruction-manifest/1")
    body = manifest_body(bound, audit_sha, audit_bytes, records)
    raw_manifest = lines.dump(body)
    if os.path.lexists(manifest_path) and lines.read_exact(manifest_path) != raw_manifest:
        refuse("return-line-reconstruction-manifest/1", "reconstruction bytes differ",
               "Keep the manifest. Do not delete it.", evidence=RECON_MANIFEST, state="conflict")
    if not os.path.lexists(manifest_path):
        lines.write_new(manifest_path, raw_manifest)
    journal["blocked"] = []
    journal["interrupted"] = False
    journal["complete"] = True
    raw_journal = lines.save_json(journal_path, journal)
    marker_body = {
        "audit_bytes": audit_bytes,
        "audit_sha256": audit_sha,
        "file_count": len(planned),
        "incomplete_count": body["incomplete_count"],
        "journal_sha256": lines.sha(raw_journal),
        "layout_sha256": bound["layout_sha256"],
        "manifest_sha256": lines.sha(raw_manifest),
        "page_local_count": body["page_local_count"],
        "plan_sha256": bound["plan_sha256"],
        "record_count": len(records),
        "schema": "return-line-reconstruction-complete/1",
    }
    if os.path.lexists(marker_path):
        refuse("return-line-reconstruction-complete/1", "reconstruction marker differs", "Keep the marker. Do not delete it.", state="conflict")
    lines.write_new(marker_path, lines.dump(marker_body))
    return ok(command, "return-line-reconstruction-complete/1",
              "Reconstruction marker written. No original was retired. This is not acceptance.",
              RECON_MARKER, counts_detail(records, planned))


def expected_payload(bound: dict, item: dict) -> bytes:
    """Bytes for a planned row. Relocation is rebuilt. Other roles re-read the source."""
    lines = load_lines()
    if item["role"] == "relocation":
        return relocation_bytes(bound, item["old_member"])
    source_rel = source_rel_for(bound, item)
    return lines.read_exact(os.path.join(bound["backup"], *source_rel.split("/")))


def source_rel_for(bound: dict, item: dict) -> str:
    if item["role"] == "return":
        return f"sources/{item['old_member']}/return.md"
    prefix = None
    for record in load_records(bound):
        if record["old_member"] == item["old_member"]:
            prefix = record["custody_path"] + "/"
            break
    if prefix is None or not item["logical"].startswith(prefix):
        refuse("broken link", "planned custody path has no record", "Keep the journal.", evidence=item["logical"], state="conflict")
    return f"sources/{item['old_member']}/{item['logical'][len(prefix):]}"


def load_records(bound: dict) -> list:
    journal_path, _manifest, _marker = recon_paths(bound["staging"])
    journal = journal_at(journal_path, "return-line-reconstruction-journal/1")
    if journal is None:
        return []
    return list(journal.get("records") or [])


def relocation_bytes(bound: dict, member: str) -> bytes:
    lines = load_lines()
    journal = journal_at(recon_paths(bound["staging"])[0], "return-line-reconstruction-journal/1")
    record = None
    if journal is not None:
        for item in journal.get("records") or []:
            if item.get("old_member") == member:
                record = item
                break
    source = os.path.join(bound["backup"], "sources", member)
    res_path = os.path.join(source, "reservation.json")
    reservation = None
    if os.path.lexists(res_path):
        try:
            reservation = lines.loads(lines.read_exact(res_path), "sealed reader")
        except lines.LineError:
            reservation = None
    destination = reservation.get("destination") if isinstance(reservation, dict) else None
    return_path = os.path.join(source, "return.md")
    return_data = lines.read_exact(return_path) if os.path.lexists(return_path) else None
    if record is not None and record["has_return"] != (return_data is not None):
        refuse("broken link", "staged return presence changed", "Keep the staging tree.", evidence=member, state="conflict")
    relocation = {
        "custody_format": "legacy-relocated/1",
        "old_member": member,
        "original_destination": destination,
        "reservation_destination_rewritten": False,
        "return_bytes": None if return_data is None else len(return_data),
        "return_sha256": None if return_data is None else lines.sha(return_data),
        "schema": "return-line-relocation/1",
        "source_backup": f"sources/{member}",
    }
    lines.expect_keys(relocation, lines.RELOCATION_KEYS, "return-line-relocation/1", "relocation")
    return lines.dump(relocation)


def load_reconstruction(bound: dict, audit_sha: str) -> tuple[dict, dict, list, list]:
    lines = load_lines()
    journal_path, manifest_path, marker_path = recon_paths(bound["staging"])
    marker = read_marker(marker_path, "return-line-reconstruction-complete/1")
    if marker is None:
        refuse("return-line-reconstruction-complete/1", "reconstruction marker is absent", "Verify the logical pages before publication.", evidence=RECON_MARKER)
    if marker.get("audit_sha256") != audit_sha:
        refuse("audit identity", "reconstruction marker does not match this audit", "Do not publish against a different audit.", state="conflict")
    raw = lines.read_exact(journal_path)
    if lines.sha(raw) != marker.get("journal_sha256"):
        refuse("return-line-reconstruction-journal/1", "reconstruction journal does not match its marker", "Keep the journal.", state="conflict")
    if not os.path.lexists(manifest_path) or lines.sha(lines.read_exact(manifest_path)) != marker.get("manifest_sha256"):
        refuse("return-line-reconstruction-manifest/1", "reconstruction manifest does not match its marker", "Keep the manifest.", state="conflict")
    journal = lines.loads(raw, "return-line-reconstruction-journal/1")
    planned = journal["planned"]
    records = journal["records"]
    verify_planned(bound["staging"], planned, "return-line-reconstruction-manifest/1")
    return marker, journal, planned, records


def publish_run(book: str, authorization: str, audit: str, plan: str, backup: str,
                staging: str, retired: str, interrupt_after: int | None, resume: bool) -> dict:
    command = "publish-resume" if resume else "publish"
    return guard(command, lambda: publish_work(command, book, authorization, audit, plan, backup, staging, retired, interrupt_after))


def publish_work(command, book, authorization, audit, plan, backup, staging, retired, interrupt_after) -> dict:
    lines = load_lines()
    bound = require_authorization(authorization, command, book, None, audit, plan, backup, staging, retired)

    def inner():
        if interrupt_after is not None and interrupt_after < 0:
            refuse("return-line-publish-journal/1", "interrupt-after is negative", "Use zero or a positive count.")
        book_abs = bound["book"]
        lines.assert_mutable(book_abs)
        layout = lines.read_layout(book_abs)
        _audit, audit_sha, _audit_bytes = lines.load_audit(bound["audit"])
        require_stage(bound["backup"], audit_sha)
        marker, _journal, planned, records = load_reconstruction(bound, audit_sha)
        prepared = prepared_or_stop(layout, _audit)
        staged_names = {record["old_member"] for record, _route in prepared}
        journal_path = os.path.join(bound["backup"], PUBLISH_JOURNAL)
        marker_path = os.path.join(bound["backup"], PUBLISH_MARKER)
        existing = journal_at(journal_path, "return-line-publish-journal/1")
        if existing is not None and existing.get("rolled_back") is True:
            refuse("return-line-publish-journal/1", "publish journal records a rollback", "Use a fresh backup. Do not reuse rolled-back evidence.")
        if existing is None:
            journal = {
                "audit_sha256": audit_sha,
                "blocked": [],
                "complete": False,
                "created": [],
                "displaced": [],
                "interrupted": False,
                "reconstruction_marker_sha256": lines.sha(lines.read_exact(os.path.join(bound["staging"], RECON_MARKER))),
                "retired_root": bound["retired"],
                "rolled_back": False,
                "schema": "return-line-publish-journal/1",
            }
            lines.save_json(journal_path, journal)
        else:
            journal = existing
            if journal.get("audit_sha256") != audit_sha or lines.norm(journal.get("retired_root", "")) != lines.norm(bound["retired"]):
                refuse("audit identity", "publish journal names a different audit or retired root", "Keep this journal.", state="conflict")
        current = read_marker(marker_path, "return-line-publish-complete/1")
        if current is not None:
            if current.get("audit_sha256") == audit_sha and current.get("journal_sha256") == lines.sha(lines.read_exact(journal_path)):
                verify_book_links(book_abs, planned, records)
                return ok(command, "return-line-publish-complete/1",
                          "Publish marker already matches. This is not acceptance and not live authority.",
                          PUBLISH_MARKER, counts_detail(records, planned, {"created_count": current.get("created_count"), "displaced_count": current.get("displaced_count")}))
            refuse("return-line-publish-complete/1", "publish marker differs", "Keep the marker. Do not delete it.", state="conflict")
        copied = 0
        by_member: dict[str, list] = {}
        for item in planned:
            by_member.setdefault(item["old_member"], []).append(item)
        displaced = {item["name"] for item in journal["displaced"]}
        created = {item["rel"]: item for item in journal["created"]}

        def stop(kind: str, evidence: str, reason: str):
            journal["interrupted"] = True
            journal["complete"] = False
            if kind == "partial":
                journal["blocked"] = [{"check": "return-line-publish-journal/1", "evidence": evidence, "reason": "partial bytes kept"}]
            lines.save_json(journal_path, journal)
            text = "Partial publication bytes were kept. They were not deleted. " if kind == "partial" else "Publication stopped before the marker. Resume the same roots. "
            return lines.envelope(command, "return-line-publish-journal/1", "interrupted", 3, text + ESCALATION, evidence, None, {"copied_this_call": copied})

        for record, route in prepared:
            member = record["old_member"]
            for name in lines.occupants(book_abs, route["target_number"], route["target_page"]):
                if name not in staged_names:
                    journal["blocked"] = [{"check": "occupied-line", "evidence": name, "reason": "occupant is not a staged source"}]
                    journal["complete"] = False
                    lines.save_json(journal_path, journal)
                    return lines.envelope(command, "occupied-line", "conflict", 2,
                                          "An occupant is not one of the staged sources. It was not overwritten. " + ESCALATION,
                                          name, None, {})
                src = os.path.join(book_abs, name)
                dest = under(bound["retired"], f"occupants/{name}")
                if name in displaced and os.path.isdir(dest) and not os.path.exists(src):
                    continue
                if os.path.lexists(dest):
                    refuse("occupied-archive", f"retired occupant {name} already exists", "Do not overwrite the archive.", evidence=f"occupants/{name}", state="conflict")
                if not os.path.isdir(src):
                    refuse("occupied-line", f"occupant {name} is not in the book or the retired root", "Stop and keep the evidence.", evidence=name, state="conflict")
                if interrupt_after is not None and copied >= interrupt_after:
                    return stop("interrupt", name, "interrupt")
                files = dirs_match(src, os.path.join(bound["backup"], "sources", name), name)
                os.makedirs(os.path.dirname(dest), exist_ok=True)
                os.rename(src, dest)
                copied += 1
                journal["displaced"].append({"files": files, "name": name, "retired_rel": f"occupants/{name}"})
                displaced.add(name)
                lines.save_json(journal_path, journal)
            for item in by_member.get(member, []):
                dest = lines.join_book(book_abs, item["logical"])
                payload = lines.read_exact(under(bound["staging"], "pages/" + item["logical"]))
                if lines.sha(payload) != item["sha256"] or len(payload) != item["bytes"]:
                    refuse("return-line-reconstruction-manifest/1", "reconstruction bytes differ", "Stop. The book was not given these bytes.", evidence=item["logical"], state="conflict")
                if os.path.lexists(dest):
                    current = lines.read_exact(dest)
                    if current != payload:
                        refuse("return-line-publish-journal/1", "publication bytes differ", "Keep the book bytes. Do not delete them.", evidence=item["logical"], state="conflict")
                    continue
                if interrupt_after is not None and copied >= interrupt_after:
                    return stop("interrupt", item["logical"], "interrupt")
                if take_fault("publish") == "partial":
                    lines.write_new(dest, short_bytes(payload))
                    return stop("partial", item["logical"], "partial")
                lines.write_new(dest, payload)
                copied += 1
                row = {"bytes": len(payload), "rel": item["logical"], "sha256": item["sha256"]}
                created[item["logical"]] = row
                if not any(existing_row.get("rel") == item["logical"] for existing_row in journal["created"]):
                    journal["created"].append(row)
                lines.save_json(journal_path, journal)
        migration = {
            "audit_sha256": audit_sha,
            "backup_path": bound["backup"],
            "schema": "return-line-migration/1",
            "stage_marker": lines.STAGE_MARKER,
        }
        index = {
            "items": [
                {
                    "custody_format": "legacy-relocated/1",
                    "custody_path": record["custody_path"],
                    "old_member": record["old_member"],
                    "origin": record["origin"],
                    "return_path": record["logical_return_path"],
                    "state": record["state"],
                    "submission_id": record["submission_id"],
                }
                for record in records
            ],
            "schema": "return-line-index/1",
        }
        for rel, payload in (
            (lines.MIGRATION_NAME, lines.dump(migration)),
            (lines.INDEX_NAME, lines.dump(index)),
        ):
            dest = lines.join_book(book_abs, rel)
            if os.path.lexists(dest):
                if lines.read_exact(dest) != payload:
                    refuse("return-line-publish-journal/1", "publication bytes differ", "Keep the existing pointer. Do not delete it.", evidence=rel, state="conflict")
            else:
                if interrupt_after is not None and copied >= interrupt_after:
                    return stop("interrupt", rel, "interrupt")
                lines.write_new(dest, payload)
                copied += 1
                journal["created"].append({"bytes": len(payload), "rel": rel, "sha256": lines.sha(payload)})
                lines.save_json(journal_path, journal)
        verify_book_links(book_abs, planned, records)
        journal["blocked"] = []
        journal["interrupted"] = False
        journal["complete"] = True
        raw = lines.save_json(journal_path, journal)
        marker_body = {
            "audit_sha256": audit_sha,
            "created_count": len(journal["created"]),
            "displaced_count": len(journal["displaced"]),
            "file_count": len(planned),
            "incomplete_count": sum(1 for item in records if item["state"] == "incomplete"),
            "journal_sha256": lines.sha(raw),
            "page_local_count": sum(1 for item in records if item["page_local"]),
            "record_count": len(records),
            "reconstruction_marker_sha256": lines.sha(lines.read_exact(os.path.join(bound["staging"], RECON_MARKER))),
            "schema": "return-line-publish-complete/1",
        }
        if os.path.lexists(marker_path):
            refuse("return-line-publish-complete/1", "publish marker differs", "Keep the marker. Do not delete it.", state="conflict")
        lines.write_new(marker_path, lines.dump(marker_body))
        return ok(command, "return-line-publish-complete/1",
                  "Publish marker written. Bytes were installed on this copy. This is not acceptance and not live authority.",
                  PUBLISH_MARKER, counts_detail(records, planned, {"created_count": marker_body["created_count"], "displaced_count": marker_body["displaced_count"]}))

    return bind_call(bound, inner)


def retire_run(book: str, authorization: str, audit: str, plan: str, backup: str,
               staging: str, retired: str, interrupt_after: int | None, resume: bool) -> dict:
    command = "retire-resume" if resume else "retire"
    return guard(command, lambda: retire_work(command, book, authorization, audit, plan, backup, staging, retired, interrupt_after))


def retire_work(command, book, authorization, audit, plan, backup, staging, retired, interrupt_after) -> dict:
    lines = load_lines()
    bound = require_authorization(authorization, command, book, None, audit, plan, backup, staging, retired)

    def inner():
        if interrupt_after is not None and interrupt_after < 0:
            refuse("return-line-retire-journal/1", "interrupt-after is negative", "Use zero or a positive count.")
        book_abs = bound["book"]
        lines.assert_mutable(book_abs)
        layout = lines.read_layout(book_abs)
        _audit, audit_sha, _audit_bytes = lines.load_audit(bound["audit"])
        _marker, _journal, planned, records = load_reconstruction(bound, audit_sha)
        publish_marker = read_marker(os.path.join(bound["backup"], PUBLISH_MARKER), "return-line-publish-complete/1")
        if publish_marker is None or publish_marker.get("audit_sha256") != audit_sha:
            refuse("return-line-publish-complete/1", "publish marker is absent or names another audit", "Publish the verified pages before retirement.")
        publish_raw = lines.read_exact(os.path.join(bound["backup"], PUBLISH_JOURNAL))
        if lines.sha(publish_raw) != publish_marker.get("journal_sha256"):
            refuse("return-line-publish-journal/1", "publish journal does not match its marker", "Keep the journal.", state="conflict")
        publish_journal = lines.loads(publish_raw, "return-line-publish-journal/1")
        if publish_journal.get("rolled_back") is True:
            refuse("return-line-publish-journal/1", "publication was rolled back", "Do not retire a rolled-back copy.")
        verify_book_links(book_abs, planned, records)
        for record in records:
            if record["old_member"] == record["target_page"]:
                refuse("occupied-line", "old member is the logical target page", "Stop before any retire move.", evidence=record["old_member"], state="conflict")
        journal_path = os.path.join(bound["retired"], RETIRE_JOURNAL)
        marker_path = os.path.join(bound["retired"], RETIRE_MARKER)
        existing = journal_at(journal_path, "return-line-retire-journal/1")
        if existing is not None and existing.get("rolled_back") is True:
            refuse("return-line-retire-journal/1", "retire journal records a rollback", "Use a fresh retired root.")
        if existing is None:
            journal = {
                "already_displaced": [],
                "audit_sha256": audit_sha,
                "blocked": [],
                "complete": False,
                "interrupted": False,
                "moved": [],
                "publish_marker_sha256": lines.sha(lines.read_exact(os.path.join(bound["backup"], PUBLISH_MARKER))),
                "rolled_back": False,
                "schema": "return-line-retire-journal/1",
            }
            lines.save_json(journal_path, journal)
        else:
            journal = existing
            if journal.get("audit_sha256") != audit_sha:
                refuse("audit identity", "retire journal names a different audit", "Keep this journal.", state="conflict")
        current = read_marker(marker_path, "return-line-retire-complete/1")
        if current is not None:
            if current.get("audit_sha256") == audit_sha and current.get("journal_sha256") == lines.sha(lines.read_exact(journal_path)) and current.get("remaining_old_members") == 0:
                return ok(command, "return-line-retire-complete/1",
                          "Retire marker already matches. This is not acceptance and not live authority.",
                          RETIRE_MARKER, {"already_displaced_count": current.get("already_displaced_count"), "moved_count": current.get("moved_count"), "record_count": len(records), "remaining_old_members": 0})
            refuse("return-line-retire-complete/1", "retire marker differs", "Keep the marker. Do not delete it.", state="conflict")
        displaced = {item["name"]: item["retired_rel"] for item in publish_journal.get("displaced") or []}
        moved = {item["name"] for item in journal["moved"]}
        noted = {item["name"] for item in journal["already_displaced"]}
        copied = 0
        for record, _route in prepared_or_stop(layout, _audit):
            name = record["old_member"]
            src = os.path.join(book_abs, name)
            original = under(bound["retired"], f"originals/{name}")
            if name in displaced:
                if os.path.exists(src):
                    refuse("occupied-line", f"{name} is both displaced and still in the book", "Stop and keep both copies.", evidence=name, state="conflict")
                occ = under(bound["retired"], displaced[name])
                if not os.path.isdir(occ):
                    refuse("rollback copy", f"displaced occupant {name} is missing", "Stop. Do not invent the directory.", evidence=displaced[name], state="conflict")
                if name not in noted:
                    journal["already_displaced"].append({"name": name, "retired_rel": displaced[name]})
                    noted.add(name)
                    lines.save_json(journal_path, journal)
                continue
            if name in moved and os.path.isdir(original) and not os.path.exists(src):
                continue
            if not os.path.exists(src):
                if os.path.isdir(original) and name in moved:
                    continue
                refuse("audit identity", f"source member {name} is missing", "Stop. Nothing further was retired.", evidence=name, state="conflict")
            if os.path.lexists(original):
                refuse("occupied-archive", f"retired original {name} already exists", "Do not overwrite the archive.", evidence=f"originals/{name}", state="conflict")
            if interrupt_after is not None and copied >= interrupt_after:
                journal["interrupted"] = True
                journal["complete"] = False
                lines.save_json(journal_path, journal)
                return lines.envelope(command, "return-line-retire-journal/1", "interrupted", 3,
                                      "Retirement stopped before the marker. Resume the same retired root. " + ESCALATION,
                                      name, None, {"copied_this_call": copied})
            files = dirs_match(src, os.path.join(bound["backup"], "sources", name), name)
            os.makedirs(os.path.dirname(original), exist_ok=True)
            os.rename(src, original)
            copied += 1
            journal["moved"].append({"files": files, "name": name, "retired_rel": f"originals/{name}"})
            moved.add(name)
            lines.save_json(journal_path, journal)
        remaining = [record["old_member"] for record, _route in prepared_or_stop(layout, _audit) if os.path.isdir(os.path.join(book_abs, record["old_member"]))]
        if remaining:
            refuse("audit identity", "obsolete member directories remain in the book", "Do not write the retire marker while an old member remains.", evidence=remaining[0], state="conflict", detail={"remaining": remaining})
        pointer = {
            "audit_sha256": audit_sha,
            "retired_root": bound["retired"],
            "schema": "return-line-retirement-pointer/1",
        }
        pointer_bytes = lines.dump(pointer)
        pointer_path = os.path.join(bound["backup"], RETIRE_POINTER)
        if os.path.lexists(pointer_path) and lines.read_exact(pointer_path) != pointer_bytes:
            refuse("return-line-retirement-pointer/1", "retirement pointer differs", "Keep the pointer. Do not delete it.", state="conflict")
        if not os.path.lexists(pointer_path):
            lines.write_new(pointer_path, pointer_bytes)
        journal["pointer_bytes"] = len(pointer_bytes)
        journal["pointer_sha256"] = lines.sha(pointer_bytes)
        journal["blocked"] = []
        journal["interrupted"] = False
        journal["complete"] = True
        raw = lines.save_json(journal_path, journal)
        marker_body = {
            "already_displaced_count": len(journal["already_displaced"]),
            "audit_sha256": audit_sha,
            "journal_sha256": lines.sha(raw),
            "moved_count": len(journal["moved"]),
            "publish_marker_sha256": journal["publish_marker_sha256"],
            "record_count": len(records),
            "remaining_old_members": 0,
            "schema": "return-line-retire-complete/1",
        }
        if os.path.lexists(marker_path):
            refuse("return-line-retire-complete/1", "retire marker differs", "Keep the marker. Do not delete it.", state="conflict")
        lines.write_new(marker_path, lines.dump(marker_body))
        return ok(command, "return-line-retire-complete/1",
                  "Retire marker written. Old member directories are out of the active book. This is not acceptance and not live authority.",
                  RETIRE_MARKER, {"already_displaced_count": marker_body["already_displaced_count"], "moved_count": marker_body["moved_count"], "record_count": len(records), "remaining_old_members": 0})

    return bind_call(bound, inner)


def file_matches(path: str, row: dict) -> bool:
    lines = load_lines()
    if not os.path.lexists(path):
        return False
    data = lines.read_exact(path)
    return lines.sha(data) == row["sha256"] and len(data) == row["bytes"]


def rollback_publish_run(book: str, authorization: str, audit: str, plan: str, backup: str, staging: str, retired: str) -> dict:
    command = "rollback-publish"

    def work():
        lines = load_lines()
        bound = require_authorization(authorization, command, book, None, audit, plan, backup, staging, retired)

        def inner():
            book_abs = bound["book"]
            lines.assert_mutable(book_abs)
            journal_path = os.path.join(bound["backup"], PUBLISH_JOURNAL)
            marker_path = os.path.join(bound["backup"], PUBLISH_MARKER)
            journal = journal_at(journal_path, "return-line-publish-journal/1")
            if journal is None:
                refuse("return-line-publish-journal/1", "publish journal is absent", "There is no publication to roll back.")
            retire_marker = os.path.join(bound["retired"], RETIRE_MARKER)
            retire_journal = journal_at(os.path.join(bound["retired"], RETIRE_JOURNAL), "return-line-retire-journal/1")
            if os.path.lexists(retire_marker) and not (retire_journal or {}).get("rolled_back"):
                refuse("return-line-retire-journal/1", "retirement is still complete", "Roll back retirement before rolling back publication.")
            if journal.get("rolled_back") is True and not os.path.lexists(marker_path):
                return ok(command, "return-line-publish-journal/1", "Publication rollback already finished. Evidence was kept.", PUBLISH_JOURNAL, {})
            for item in journal.get("created") or []:
                path = lines.join_book(book_abs, item["rel"])
                if os.path.lexists(path) and not file_matches(path, item):
                    refuse("return-line-publish-journal/1", "a created file changed since the journal", "Stop before deleting. The evidence stays.", evidence=item["rel"], state="conflict")
            for item in journal.get("displaced") or []:
                root = under(bound["retired"], item["retired_rel"])
                if not os.path.isdir(root):
                    book_slot = os.path.join(book_abs, item["name"])
                    if os.path.isdir(book_slot):
                        continue
                    refuse("rollback copy", f"displaced copy {item['name']} is missing", "Stop. Do not invent the directory.", evidence=item["retired_rel"], state="conflict")
                for row in item.get("files") or []:
                    path = os.path.join(root, *row["rel"].split("/"))
                    if not file_matches(path, row):
                        refuse("rollback copy", "a displaced file changed since the journal", "Stop. The retired copy stays.", evidence=f"{item['retired_rel']}/{row['rel']}", state="conflict")
            if os.path.lexists(marker_path):
                os.remove(marker_path)
            for item in sorted(journal.get("created") or [], key=lambda row: row["rel"].count("/"), reverse=True):
                path = lines.join_book(book_abs, item["rel"])
                if os.path.lexists(path):
                    os.remove(path)
                    lines.prune_empty(os.path.dirname(path), book_abs)
            for item in list(journal.get("displaced") or []):
                src = under(bound["retired"], item["retired_rel"])
                dest = os.path.join(book_abs, item["name"])
                if os.path.isdir(dest) and not os.path.exists(src):
                    continue
                if os.path.exists(dest):
                    refuse("occupied-line", f"{item['name']} is already in the book", "Stop. Do not overwrite it with the retired copy.", evidence=item["name"], state="conflict")
                if not os.path.isdir(src):
                    refuse("rollback copy", f"displaced copy {item['name']} is missing", "Stop. Do not invent the directory.", evidence=item["retired_rel"], state="conflict")
                os.rename(src, dest)
                lines.prune_empty(os.path.dirname(src), bound["retired"])
            journal["rolled_back"] = True
            journal["complete"] = False
            journal["interrupted"] = False
            lines.save_json(journal_path, journal)
            return ok(command, "return-line-publish-journal/1",
                      "Journaled publication was reversed where hashes matched. This is not acceptance.",
                      PUBLISH_JOURNAL, {"created_count": len(journal.get("created") or []), "displaced_count": len(journal.get("displaced") or [])})

        return bind_call(bound, inner)

    return guard(command, work)


def rollback_retire_run(book: str, authorization: str, audit: str, plan: str, backup: str, staging: str, retired: str) -> dict:
    command = "rollback-retire"

    def work():
        lines = load_lines()
        bound = require_authorization(authorization, command, book, None, audit, plan, backup, staging, retired)

        def inner():
            book_abs = bound["book"]
            lines.assert_mutable(book_abs)
            journal_path = os.path.join(bound["retired"], RETIRE_JOURNAL)
            marker_path = os.path.join(bound["retired"], RETIRE_MARKER)
            journal = journal_at(journal_path, "return-line-retire-journal/1")
            if journal is None:
                refuse("return-line-retire-journal/1", "retire journal is absent", "There is no retirement to roll back.")
            if journal.get("rolled_back") is True and not os.path.lexists(marker_path):
                return ok(command, "return-line-retire-journal/1", "Retirement rollback already finished. Evidence was kept.", RETIRE_JOURNAL, {})
            for item in journal.get("moved") or []:
                root = under(bound["retired"], item["retired_rel"])
                if not os.path.isdir(root):
                    if os.path.isdir(os.path.join(book_abs, item["name"])):
                        continue
                    refuse("rollback copy", f"retired original {item['name']} is missing", "Stop. Do not invent the directory.", evidence=item["retired_rel"], state="conflict")
                for row in item.get("files") or []:
                    path = os.path.join(root, *row["rel"].split("/"))
                    if not file_matches(path, row):
                        refuse("rollback copy", "a retired file changed since the journal", "Stop. The retired copy stays.", evidence=f"{item['retired_rel']}/{row['rel']}", state="conflict")
            pointer = os.path.join(bound["backup"], RETIRE_POINTER)
            if os.path.lexists(pointer):
                if "pointer_sha256" not in journal or not file_matches(pointer, {"sha256": journal["pointer_sha256"], "bytes": journal["pointer_bytes"]}):
                    refuse("return-line-retirement-pointer/1", "retirement pointer changed", "Stop. The pointer stays.", state="conflict")
            if os.path.lexists(marker_path):
                os.remove(marker_path)
            if os.path.lexists(pointer):
                os.remove(pointer)
            for item in list(journal.get("moved") or []):
                src = under(bound["retired"], item["retired_rel"])
                dest = os.path.join(book_abs, item["name"])
                if os.path.isdir(dest) and not os.path.exists(src):
                    continue
                if os.path.exists(dest):
                    refuse("occupied-line", f"{item['name']} is already in the book", "Stop. Do not overwrite it with the retired copy.", evidence=item["name"], state="conflict")
                if not os.path.isdir(src):
                    refuse("rollback copy", f"retired original {item['name']} is missing", "Stop. Do not invent the directory.", evidence=item["retired_rel"], state="conflict")
                os.rename(src, dest)
                lines.prune_empty(os.path.dirname(src), bound["retired"])
            journal["rolled_back"] = True
            journal["complete"] = False
            journal["interrupted"] = False
            lines.save_json(journal_path, journal)
            return ok(command, "return-line-retire-journal/1",
                      "Journaled retirement was reversed where hashes matched. Displaced occupants stay until publication rollback.",
                      RETIRE_JOURNAL, {"moved_count": len(journal.get("moved") or [])})

        return bind_call(bound, inner)

    return guard(command, work)


def enrich(book_abs: str, result: dict) -> dict:
    lines = load_lines()
    described = result.get("descriptor")
    if not isinstance(described, dict):
        return result
    detail = result.get("detail")
    if not isinstance(detail, dict):
        detail = {}
        result["detail"] = detail
    detail["new_home"] = {
        "custody_path": described.get("custody_path"),
        "logical_return_path": described.get("return_path"),
        "target_page": described.get("target_page"),
    }
    retained = {
        "archived_identity": None,
        "backup_path": lines.migration_backup(book_abs),
        "book_member_present": None,
        "retired_rel": None,
        "retired_root": None,
        "source_backup": None,
    }
    custody = described.get("custody_path")
    if isinstance(custody, str):
        reloc = lines.join_book(book_abs, custody + "/relocation.json")
        if os.path.lexists(reloc):
            body = lines.loads(lines.read_exact(reloc), "return-line-relocation/1")
            if isinstance(body, dict):
                old = body.get("old_member")
                if isinstance(old, str):
                    retained["archived_identity"] = old
                    retained["book_member_present"] = os.path.isdir(os.path.join(book_abs, old))
                if isinstance(body.get("source_backup"), str):
                    retained["source_backup"] = body["source_backup"]
    backup = retained["backup_path"]
    if isinstance(backup, str):
        pointer = os.path.join(backup, RETIRE_POINTER)
        if os.path.lexists(pointer):
            body = lines.loads(lines.read_exact(pointer), "return-line-retirement-pointer/1")
            if isinstance(body, dict) and isinstance(body.get("retired_root"), str):
                retained["retired_root"] = body["retired_root"]
                old = retained["archived_identity"]
                if isinstance(old, str):
                    for rel in (f"originals/{old}", f"occupants/{old}"):
                        if os.path.isdir(os.path.join(body["retired_root"], *rel.split("/"))):
                            retained["retired_rel"] = rel
                            break
    detail["retained_original"] = retained
    detail["pass02_tool"] = TOOL_PATH
    detail["pass02_tool_sha256"] = tool_sha()
    return result


def lookup_run(book: str, member: str | None, page: str | None, batch: str | None, submission: str | None, command: str) -> dict:
    def work():
        lines = load_lines()
        result = lines.lookup_run(book, member, page, batch, submission)
        result["command"] = command
        if isinstance(result.get("descriptor"), dict):
            enrich(lines.require_dir(book, "book"), result)
        return result
    return guard(command, work)


def refuse_adopt(command: str) -> dict:
    lines = load_lines()
    return lines.envelope(
        command, "successor command", "refused", 2,
        "Use reconstruct, publish, retire, rollback-publish, and rollback-retire. "
        "pass01 adopt retires only colliding occupants into backup/retired and is not this tool's success path. " + ESCALATION,
        None, None, {},
    )


def forwarded_stage_rollback(book: str, backup: str, authorization: str, audit: str, plan: str, staging: str, retired: str) -> dict:
    def work():
        lines = load_lines()
        bound = require_authorization(authorization, "rollback-stage", book, None, audit, plan, backup, staging, retired)

        def inner():
            lines.assert_mutable(bound["book"])
            publish = journal_at(os.path.join(bound["backup"], PUBLISH_JOURNAL), "return-line-publish-journal/1")
            if publish and not publish.get("rolled_back") and (publish.get("created") or publish.get("displaced")):
                refuse("return-line-publish-journal/1", "publication has already created or displaced files", "Roll back publication before rolling back the stage backup.")
            retire = journal_at(os.path.join(bound["retired"], RETIRE_JOURNAL), "return-line-retire-journal/1")
            if retire and not retire.get("rolled_back") and (retire.get("moved") or retire.get("already_displaced")):
                refuse("return-line-retire-journal/1", "retirement has already moved files", "Roll back retirement before rolling back the stage backup.")
            return lines.rollback_stage_run(book, backup)

        return bind_call(bound, inner)
    return guard("rollback-stage", work)


def add_auth(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--authorization", required=True)
    parser.add_argument("--audit", required=True)
    parser.add_argument("--plan", required=True)
    parser.add_argument("--backup", required=True)
    parser.add_argument("--staging", required=True)
    parser.add_argument("--retired", required=True)


def main(argv: list[str] | None = None) -> int:
    lines = load_lines()
    parser = argparse.ArgumentParser(description="Reconstruct, publish, and fully retire return lines on a copy")
    sub = parser.add_subparsers(dest="command", required=True)

    init = sub.add_parser("init")
    init.add_argument("--book", required=True)
    init.add_argument("--name", required=True)
    add_auth(init)

    reserve = sub.add_parser("reserve")
    reserve.add_argument("--book", required=True)
    reserve.add_argument("--page", required=True)
    reserve.add_argument("--batch", required=True)
    reserve.add_argument("--submission", required=True)
    reserve.add_argument("--output", action="append", default=[])
    reserve.add_argument("--submitter", required=True)
    reserve.add_argument("--reviewer", required=True)
    reserve.add_argument("--release", required=True)
    reserve.add_argument("--supersedes", default=None)
    add_auth(reserve)

    capture = sub.add_parser("capture")
    capture.add_argument("--book", required=True)
    capture.add_argument("--page", required=True)
    capture.add_argument("--batch", required=True)
    capture.add_argument("--submission", required=True)
    capture.add_argument("--return-file", required=True)
    capture.add_argument("--artifact", nargs=2, action="append", default=[], metavar=("LOGICAL", "FILE"))
    add_auth(capture)

    verify = sub.add_parser("verify")
    verify.add_argument("--book", required=True)
    verify.add_argument("--page", required=True)
    verify.add_argument("--batch", required=True)

    for name in ("lookup", "descriptor"):
        lookup = sub.add_parser(name)
        lookup.add_argument("--book", required=True)
        lookup.add_argument("--member")
        lookup.add_argument("--page")
        lookup.add_argument("--batch")
        lookup.add_argument("--submission")

    for name in ("stage", "stage-resume"):
        phase = sub.add_parser(name)
        phase.add_argument("--book", required=True)
        phase.add_argument("--interrupt-after", type=int, default=None)
        add_auth(phase)

    for name in ("adopt", "adopt-resume", "rollback-adopt"):
        sub.add_parser(name)

    rollback_stage = sub.add_parser("rollback-stage")
    rollback_stage.add_argument("--book", required=True)
    add_auth(rollback_stage)

    plan = sub.add_parser("plan")
    plan.add_argument("--book", required=True)
    plan.add_argument("--audit", required=True)
    plan.add_argument("--out", required=True)

    for name in ("reconstruct", "reconstruct-resume", "publish", "publish-resume", "retire", "retire-resume"):
        phase = sub.add_parser(name)
        phase.add_argument("--book", required=True)
        phase.add_argument("--interrupt-after", type=int, default=None)
        add_auth(phase)

    for name in ("rollback-publish", "rollback-retire"):
        phase = sub.add_parser(name)
        phase.add_argument("--book", required=True)
        add_auth(phase)

    args = parser.parse_args(argv)
    command = args.command
    if command in REFUSED_ADOPT:
        result = refuse_adopt(command)
        return lines.emit(result, False)

    def auth_tuple():
        return (args.authorization, args.audit, args.plan, args.backup, args.staging, args.retired)

    try:
        result = dispatch(lines, command, args, auth_tuple)
    except lines.LineError as exc:
        correction = exc.correction if "Escalation:" in exc.correction else exc.correction.rstrip() + " " + ESCALATION
        result = lines.envelope(command, exc.check, exc.state, exc.exit_code, correction, exc.evidence, None, exc.detail)
    if not isinstance(result, dict):
        return 2
    return lines.emit(result, command == "descriptor")


def dispatch(lines, command: str, args, auth_tuple) -> dict:
    if command == "plan":
        result = lines.plan_run(args.book, args.audit, args.out)
    elif command == "verify":
        result = lines.verify_run(args.book, args.page, args.batch)
    elif command in {"lookup", "descriptor"}:
        result = lookup_run(args.book, args.member, args.page, args.batch, args.submission, command)
    elif command == "init":
        if needs_auth(command, args.book):
            bound = require_authorization(args.authorization, command, args.book, args.name, *auth_tuple()[1:])
            result = bind_call(bound, lambda: lines.init_run(args.book, args.name))
        else:
            result = lines.init_run(args.book, args.name)
    elif command == "reserve":
        def run_reserve():
            return lines.reserve_run(args.book, args.page, args.batch, args.submission, args.output, args.submitter, args.reviewer, args.release, args.supersedes)
        if needs_auth(command, args.book):
            bound = require_authorization(args.authorization, command, args.book, None, *auth_tuple()[1:])
            result = bind_call(bound, run_reserve)
        else:
            result = run_reserve()
    elif command == "capture":
        def run_capture():
            return lines.capture_run(args.book, args.page, args.batch, args.submission, args.return_file, [(a, b) for a, b in args.artifact])
        if needs_auth(command, args.book):
            bound = require_authorization(args.authorization, command, args.book, None, *auth_tuple()[1:])
            result = bind_call(bound, run_capture)
        else:
            result = run_capture()
    elif command in {"stage", "stage-resume"}:
        def run_stage():
            return lines.stage_run(args.book, args.backup, args.audit, args.interrupt_after, command == "stage-resume")
        if needs_auth(command, args.book):
            bound = require_authorization(args.authorization, command, args.book, None, *auth_tuple()[1:])
            result = bind_call(bound, run_stage)
        else:
            result = run_stage()
    elif command == "rollback-stage":
        if needs_auth(command, args.book):
            result = forwarded_stage_rollback(args.book, args.backup, args.authorization, args.audit, args.plan, args.staging, args.retired)
        else:
            result = lines.rollback_stage_run(args.book, args.backup)
    elif command in {"reconstruct", "reconstruct-resume"}:
        result = reconstruct_run(args.book, args.authorization, args.audit, args.plan, args.backup, args.staging, args.retired, args.interrupt_after, command.endswith("resume"))
    elif command in {"publish", "publish-resume"}:
        result = publish_run(args.book, args.authorization, args.audit, args.plan, args.backup, args.staging, args.retired, args.interrupt_after, command.endswith("resume"))
    elif command in {"retire", "retire-resume"}:
        result = retire_run(args.book, args.authorization, args.audit, args.plan, args.backup, args.staging, args.retired, args.interrupt_after, command.endswith("resume"))
    elif command == "rollback-publish":
        result = rollback_publish_run(args.book, args.authorization, args.audit, args.plan, args.backup, args.staging, args.retired)
    elif command == "rollback-retire":
        result = rollback_retire_run(args.book, args.authorization, args.audit, args.plan, args.backup, args.staging, args.retired)
    else:
        result = lines.envelope(command, "successor command", "refused", 2, "Unknown command. " + ESCALATION, None, None, {})
    return result


if __name__ == "__main__":
    try:
        sys.exit(main())
    except load_lines().LineError as exc:
        correction = exc.correction if "Escalation:" in exc.correction else exc.correction + " " + ESCALATION
        sys.stdout.buffer.write(load_lines().dump(load_lines().envelope(
            "authorization", exc.check, exc.state, exc.exit_code, correction, exc.evidence, None, exc.detail,
        )))
        sys.exit(exc.exit_code)
