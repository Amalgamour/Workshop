#!/usr/bin/env python3
"""Read-only projection of one selected workbook review.

Successor of review-report-pass01. The command calls the pinned librarian
review-loop inspect, read, and recover doors. Record metadata is taken only
from the cut bound at the start of this observation. This process does not
record or publish.
"""

from __future__ import annotations

import importlib.util
import json
import os
import sys
from pathlib import Path

sys.dont_write_bytecode = True
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"

_PASS01 = Path(__file__).resolve().parents[1] / "review-report-pass01" / "report.py"
_SPEC = importlib.util.spec_from_file_location("review_report_pass01", _PASS01)
p1 = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(p1)

SCHEMA = "review-report/2"
PUB_KEYS = (
    "after_sha256",
    "before_sha256",
    "rendered_sha256",
    "review_id",
    "status",
    "target",
)
HEX = set("0123456789abcdef")
PAYLOAD_MISSING = {"artifact-missing", "declared-file-missing"}
DETAIL_FIELDS = [
    "reasons",
    "findings",
    "gaps",
    "answers",
    "sections",
    "intake_findings",
    "artifacts.rows",
    "render_coverage",
    "identity",
    "observation",
    "interface_gap",
]
OBSERVATION_LIMIT = (
    "This observation binds journal current, record digest, and publication identity, "
    "then runs inspect, read, and recover, then rechecks that binding before reading "
    "record metadata and again before the projection is attached. The reporter has no "
    "lock, no concurrency control, and no power-loss guarantee. A change that lands "
    "after the final recheck is outside this observation. A coherent change that is "
    "already stable at the start of a later observation is a new measured cut. A change "
    "during this observation stays out of the emitted judgment, attention, and custody."
)
INTERFACE_GAP = (
    p1.INTERFACE_GAP
    + " Those three results also omit one bound token of journal current, record digest, "
    "and publication identity. This reader measures that token from journal.json before "
    "and after the three calls. A mismatch leaves record metadata unexposed."
)
PROPOSED = (
    "Add attention, prime_review_effective, journal current, record digest, and "
    "publication identity from the same journal-checked record to inspect, read, and recover."
)
JUDGMENT_KEYS = (
    "answers",
    "attention",
    "custody",
    "director_text",
    "disposition",
    "eligible_for_custody_completion",
    "finding",
    "findings",
    "gaps",
    "goal_terminal",
    "holds",
    "judgment_recorded",
    "judgment_recoverable",
    "limits",
    "next_action",
    "operation",
    "pass_terminal",
    "prime_review_effective",
    "reasons",
    "sections",
    "successor_of",
    "tests_note",
    "tests_passed",
    "work_complete",
)
core_call = p1.core_call


def empty_observation() -> dict:
    return {
        "bound": None,
        "changed": [],
        "limit": OBSERVATION_LIMIT,
        "recheck": None,
        "stable": None,
        "status": "not-run",
    }


def block_identity(block) -> dict | None:
    if not isinstance(block, dict):
        return None
    return {key: block.get(key) if isinstance(block.get(key), str) else None for key in PUB_KEYS}


def publication_identity(journal: dict) -> dict:
    return {
        "publication": block_identity(journal.get("publication")),
        "published_target": block_identity(journal.get("published_target")),
    }


def digest_of(journal: dict, current: str | None) -> tuple[str | None, str]:
    rows = journal.get("reviews") if isinstance(journal.get("reviews"), list) else []
    if not isinstance(current, str):
        return None, "missing"
    for item in rows:
        if isinstance(item, dict) and item.get("review_id") == current and "record_sha256" in item:
            value = item.get("record_sha256")
            if isinstance(value, str):
                return value, "str"
            return None, "wrong-type"
    return None, "missing"


def read_cut(book: str, page: str, pass_id: str) -> tuple[dict | None, str]:
    root = Path(book) / "workbook-review" / page / pass_id
    data = p1.read_regular(root / "journal.json")
    if data is None:
        return None, "unreadable"
    journal = p1.load_json(data)
    if journal is None or journal.get("schema") != p1.JOURNAL_SCHEMA:
        return None, "bad"
    current = journal.get("current") if isinstance(journal.get("current"), str) else None
    digest, kind = digest_of(journal, current)
    record_hash = None
    if isinstance(current, str):
        raw = p1.read_regular(root / "reviews" / current / "record.json")
        if raw is not None:
            record_hash = p1.sha256_bytes(raw)
    return {
        "digest_kind": kind,
        "journal_current": current,
        "publication": publication_identity(journal),
        "record_file_sha256": record_hash,
        "record_sha256": digest,
    }, "ok"


def changed_keys(left: dict | None, right: dict | None) -> list[str]:
    if not isinstance(left, dict) or not isinstance(right, dict):
        return ["cut"]
    names = []
    for key in ("digest_kind", "journal_current", "record_file_sha256", "record_sha256"):
        if left.get(key) != right.get(key):
            names.append(key)
    if not p1.same(left.get("publication"), right.get("publication")):
        names.append("publication")
    return names


def counter(scope: str, provenance: str, count, count_state: str, size, bytes_state: str) -> dict:
    return {
        "bytes": size,
        "bytes_state": bytes_state,
        "count": count,
        "count_state": count_state,
        "provenance": provenance,
        "scope": scope,
    }


def unknown_counter(scope: str, provenance: str) -> dict:
    return counter(scope, provenance, None, "unknown", None, "unknown")


def sum_bytes(rows: list[dict], key: str) -> tuple[int | None, str]:
    total = 0
    for row in rows:
        value = row.get(key)
        if type(value) is not int:
            return None, "unknown"
        total += value
    return total, "measured"


def row_item(row: dict) -> dict:
    return {
        "bytes": row.get("bytes") if type(row.get("bytes")) is int else None,
        "declared_bytes": row.get("declared_bytes") if type(row.get("declared_bytes")) is int else None,
        "declared_sha256": row.get("declared_sha256") if isinstance(row.get("declared_sha256"), str) else None,
        "path": row.get("path") if isinstance(row.get("path"), str) else None,
        "role": row.get("role") if isinstance(row.get("role"), str) else None,
        "root": row.get("root") if isinstance(row.get("root"), str) else None,
        "sha256": row.get("sha256") if isinstance(row.get("sha256"), str) else None,
    }


def integrity_of(rows: list[dict]) -> tuple[int, int, int]:
    matched = 0
    mismatched = 0
    unverified = 0
    for row in rows:
        declared = row.get("declared_sha256")
        if not isinstance(declared, str):
            unverified += 1
        elif declared == row.get("sha256") and type(row.get("declared_bytes")) is int and row.get("declared_bytes") == row.get("bytes"):
            matched += 1
        else:
            mismatched += 1
    return matched, mismatched, unverified


def sha_key(value) -> str | None:
    if isinstance(value, str) and len(value) == 64 and all(char in HEX for char in value):
        return value
    return None


def unique_files(rows: list[dict]) -> dict:
    blank = unknown_counter("unique-physical-files", "current-measured")
    if not rows:
        return counter("unique-physical-files", "current-measured", 0, "measured", 0, "measured")
    parent = list(range(len(rows)))

    def find(index: int) -> int:
        while parent[index] != index:
            parent[index] = parent[parent[index]]
            index = parent[index]
        return index

    def union(left: int, right: int) -> None:
        left_root = find(left)
        right_root = find(right)
        if left_root != right_root:
            parent[right_root] = left_root

    path_owner: dict[tuple[str, str], int] = {}
    sha_owner: dict[str, int] = {}
    for index, row in enumerate(rows):
        path_key = None
        if isinstance(row.get("root"), str) and isinstance(row.get("path"), str):
            path_key = (row["root"], row["path"])
        digest = sha_key(row.get("sha256"))
        if path_key is None and digest is None:
            return blank
        if path_key is not None:
            if path_key in path_owner:
                union(index, path_owner[path_key])
            else:
                path_owner[path_key] = index
        if digest is not None:
            if digest in sha_owner:
                union(index, sha_owner[digest])
            else:
                sha_owner[digest] = index
    groups: dict[int, list[dict]] = {}
    for index, row in enumerate(rows):
        groups.setdefault(find(index), []).append(row)
    pieces = []
    for group in groups.values():
        values = [row.get("bytes") for row in group]
        if all(type(value) is int for value in values) and len(set(values)) == 1:
            pieces.append(values[0])
        else:
            return counter("unique-physical-files", "current-measured", len(groups), "measured", None, "unknown")
    return counter("unique-physical-files", "current-measured", len(groups), "measured", sum(pieces), "measured")


def artifacts_of(inspect: dict | None) -> dict:
    unknown = {
        "bytes": None,
        "bytes_state": "unknown",
        "count": None,
        "count_state": "unknown",
        "hash_match": None,
        "hash_mismatch": None,
        "intake_roles": unknown_counter("full-intake-role-rows", "current-measured"),
        "integrity_provenance": "current-measured",
        "integrity_scope": "current-measured-artifact-role-rows",
        "measured_artifact_rows": unknown_counter("current-measured-artifact-role-rows", "current-measured"),
        "measured_by": "accepted-intake",
        "measurement": None,
        "missing": None,
        "not_verified": None,
        "provenance": "declared",
        "rows": None,
        "scope": "manifest-declared-artifact-entries",
        "unique_files": unknown_counter("unique-physical-files", "current-measured"),
    }
    unknown["intake_roles"]["hash_match"] = None
    unknown["intake_roles"]["hash_mismatch"] = None
    unknown["intake_roles"]["label"] = "intake role rows; not a declared artifact total"
    unknown["intake_roles"]["not_verified"] = None
    if not isinstance(inspect, dict):
        return unknown
    measurement = inspect.get("measurement") if isinstance(inspect.get("measurement"), str) else None
    form = inspect.get("form") if isinstance(inspect.get("form"), dict) else {}
    bindings = form.get("bindings") if isinstance(form.get("bindings"), dict) else {}
    raw_rows = bindings.get("rows")
    findings = inspect.get("findings") if isinstance(inspect.get("findings"), list) else []
    missing = []
    for finding in findings:
        if isinstance(finding, dict) and finding.get("code") in PAYLOAD_MISSING:
            missing.append({
                "code": finding.get("code"),
                "path": finding.get("path") if isinstance(finding.get("path"), str) else None,
            })
    body = dict(unknown)
    body["measurement"] = measurement
    body["missing"] = missing
    if not isinstance(raw_rows, list):
        return body
    kept = [row_item(row) for row in raw_rows if isinstance(row, dict)]
    body["rows"] = kept
    if measurement != "complete":
        return body
    artifact_rows = [row for row in kept if row.get("role") == "artifact"]
    intake_count = len(kept)
    intake_bytes, intake_bytes_state = sum_bytes(kept, "bytes")
    intake_match, intake_mismatch, intake_unverified = integrity_of(kept)
    body["intake_roles"] = counter(
        "full-intake-role-rows",
        "current-measured",
        intake_count,
        "measured",
        intake_bytes,
        "measured" if intake_bytes_state == "measured" else "unknown",
    )
    body["intake_roles"]["hash_match"] = intake_match
    body["intake_roles"]["hash_mismatch"] = intake_mismatch
    body["intake_roles"]["label"] = "intake role rows; not a declared artifact total"
    body["intake_roles"]["not_verified"] = intake_unverified
    measured_bytes, measured_state = sum_bytes(artifact_rows, "bytes")
    body["measured_artifact_rows"] = counter(
        "current-measured-artifact-role-rows",
        "current-measured",
        len(artifact_rows),
        "measured",
        measured_bytes,
        "measured" if measured_state == "measured" else "unknown",
    )
    body["unique_files"] = unique_files(kept)
    matched, mismatched, unverified = integrity_of(artifact_rows)
    body["hash_match"] = matched
    body["hash_mismatch"] = mismatched
    body["not_verified"] = unverified
    declared_ready = not missing and all(
        isinstance(row.get("declared_sha256"), str) and type(row.get("declared_bytes")) is int
        for row in artifact_rows
    )
    if declared_ready:
        declared_bytes = sum(row["declared_bytes"] for row in artifact_rows)
        body["count"] = len(artifact_rows)
        body["count_state"] = "declared"
        body["bytes"] = declared_bytes
        body["bytes_state"] = "declared"
    return body


def checked_record(book: str, page: str, pass_id: str, review_id: str, expected: str, inspect: dict, recover: dict) -> tuple[dict | None, str]:
    root = Path(book) / "workbook-review" / page / pass_id
    journal_bytes = p1.read_regular(root / "journal.json")
    if journal_bytes is None:
        return None, "journal-unreadable"
    journal = p1.load_json(journal_bytes)
    if journal is None or journal.get("schema") != p1.JOURNAL_SCHEMA or journal.get("current") != review_id:
        return None, "journal-mismatch"
    rows = journal.get("reviews") if isinstance(journal.get("reviews"), list) else []
    record_sha = None
    found = False
    for item in rows:
        if isinstance(item, dict) and item.get("review_id") == review_id and "record_sha256" in item:
            record_sha = item.get("record_sha256")
            found = True
            break
    if not found or not isinstance(record_sha, str) or record_sha != expected:
        return None, "digest-mismatch"
    data = p1.read_regular(root / "reviews" / review_id / "record.json")
    if data is None or p1.sha256_bytes(data) != expected:
        return None, "record-mismatch"
    record = p1.load_json(data)
    if record is None or not isinstance(record.get("judgment"), dict):
        return None, "record-mismatch"
    if not p1.same(record.get("judgment"), recover.get("judgment")) or not p1.same(record.get("judgment"), inspect.get("judgment")):
        return None, "judgment-mismatch"
    if not p1.same(record.get("custody"), recover.get("custody")):
        return None, "judgment-mismatch"
    return record, "ok"


def base_report(options: dict, state: str, exit_code: int) -> dict:
    report = {
        "accepted": None,
        "action_released": None,
        "answers": {"items": None, "state": "unknown"},
        "approved": None,
        "artifacts": artifacts_of(None),
        "attention": {"lines": None, "lines_state": "unknown", "source": None, "state": "unknown"},
        "authority": None,
        "book": options.get("book"),
        "claims": p1.claims_of(),
        "closes_work": None,
        "code_root": str(options.get("code_root")) if options.get("code_root") is not None else None,
        "core": {"inspect_exit": None, "read_exit": None, "recover_exit": None},
        "custody": None,
        "detail_fields": list(DETAIL_FIELDS),
        "director_text": {"state": "unknown", "text": None},
        "disposition": None,
        "eligible_for_custody_completion": None,
        "evidence_index": {"missing": [], "state": "not-recorded"},
        "exit": exit_code,
        "finding": None,
        "findings": {"items": None, "state": "unknown"},
        "gaps": {"items": None, "state": "unknown"},
        "goal_terminal": None,
        "holds": {"items": None, "state": "unknown"},
        "identity": {
            "inspect_current": None,
            "interface_gap": INTERFACE_GAP,
            "journal_current": None,
            "judgment_matches_core": None,
            "read_review_id": None,
            "record_matches_journal": None,
            "record_sha256": None,
            "recover_review_id": None,
            "selected_by": "none",
        },
        "instance_id": None,
        "intake_findings": None,
        "interface_gap": INTERFACE_GAP,
        "judgment_recorded": False,
        "judgment_recoverable": False,
        "limits": {"state": "unknown", "value": None},
        "next_action": None,
        "observation": empty_observation(),
        "operation": None,
        "pass": options.get("pass"),
        "pass_terminal": None,
        "prime_review_effective": None,
        "proposed_core_exposure": PROPOSED,
        "publication": {
            "class": "unknown",
            "rendered_sha256": None,
            "review_id": None,
            "status": None,
            "target_state": None,
        },
        "reasons": {"items": None, "state": "unknown"},
        "releases_action": None,
        "render_coverage": p1.render_coverage(None, False, None, None, None, None),
        "review_id": None,
        "schema": SCHEMA,
        "sections": None,
        "source": options.get("source"),
        "stale": None,
        "state": state,
        "successor_of": None,
        "task_association": None,
        "tests_note": {"state": "unknown", "text": None},
        "tests_passed": p1.tests_passed_field(None, False),
        "unknowns": None,
        "work_complete": None,
    }
    return report


def clear_judgment(report: dict, stale) -> None:
    fresh = base_report(
        {
            "book": report.get("book"),
            "code_root": report.get("code_root"),
            "pass": report.get("pass"),
            "source": report.get("source"),
        },
        report["state"],
        report["exit"],
    )
    for key in JUDGMENT_KEYS:
        report[key] = fresh[key]
    report["attention"] = {"lines": None, "lines_state": "unknown", "source": None, "state": "not-exposed"}
    report["stale"] = stale
    report["render_coverage"] = p1.render_coverage(
        None,
        False,
        report.get("source") if isinstance(report.get("source"), str) else None,
        report.get("pass") if isinstance(report.get("pass"), str) else None,
        report.get("review_id") if isinstance(report.get("review_id"), str) else None,
        None,
    )


def bind_identity(report: dict, bound: dict | None, selected_by: str) -> None:
    if not isinstance(bound, dict):
        report["identity"]["selected_by"] = selected_by
        return
    report["identity"]["journal_current"] = bound.get("journal_current")
    report["identity"]["record_sha256"] = bound.get("record_sha256")
    report["identity"]["selected_by"] = selected_by
    if isinstance(bound.get("journal_current"), str):
        report["review_id"] = bound["journal_current"]


def set_observation(report: dict, bound, recheck, status: str, stable) -> None:
    report["observation"]["bound"] = bound
    report["observation"]["recheck"] = recheck
    report["observation"]["status"] = status
    report["observation"]["stable"] = stable
    report["observation"]["changed"] = changed_keys(bound, recheck) if stable is False else []


def bound_publication(report: dict, bound: dict | None) -> None:
    block = None
    if isinstance(bound, dict) and isinstance(bound.get("publication"), dict):
        block = bound["publication"].get("publication")
    report["publication"] = {
        "class": "unknown",
        "rendered_sha256": block.get("rendered_sha256") if isinstance(block, dict) else None,
        "review_id": block.get("review_id") if isinstance(block, dict) else None,
        "status": block.get("status") if isinstance(block, dict) else None,
        "target_state": None,
    }


def mark_unstable(report: dict, bound: dict | None, recheck, keys: list[str]) -> None:
    bind_identity(report, bound, "bound-cut")
    clear_judgment(report, True)
    report["state"] = "held"
    report["exit"] = 1
    report["identity"]["record_matches_journal"] = False
    report["identity"]["judgment_matches_core"] = False
    report["observation"]["bound"] = bound
    report["observation"]["recheck"] = recheck
    report["observation"]["changed"] = keys
    report["observation"]["stable"] = False
    report["observation"]["status"] = "unstable"
    bound_publication(report, bound)


def hold_mismatch(report: dict, bound: dict | None, recheck) -> None:
    bind_identity(report, bound, "bound-cut")
    clear_judgment(report, True)
    report["state"] = "held"
    report["exit"] = 1
    report["identity"]["record_matches_journal"] = False
    report["identity"]["judgment_matches_core"] = False
    set_observation(report, bound, recheck, "mismatch", True)
    if isinstance(bound, dict) and isinstance(recheck, dict):
        p1.apply_publication(report, report.get("_inspect", {}), report.get("_recover", {}), True)


def core_exits(procs: dict) -> dict:
    return {
        "inspect_exit": procs["inspect"].returncode if type(procs["inspect"].returncode) is int else None,
        "read_exit": procs["read"].returncode if type(procs["read"].returncode) is int else None,
        "recover_exit": procs["recover"].returncode if type(procs["recover"].returncode) is int else None,
    }


def observe(options: dict) -> dict:
    book = options["book"]
    source = options["source"]
    pass_id = options["pass"]
    bound, bind_why = read_cut(book, source, pass_id)
    procs = {name: core_call(options["code_root"], book, source, pass_id, name) for name in ("inspect", "read", "recover")}
    parsed = {name: p1.parse_core(proc, name) for name, proc in procs.items()}
    if any(parsed[name] is None for name in parsed):
        report = base_report(options, "refused", 2)
        report["core"] = core_exits(procs)
        report["observation"]["bound"] = bound
        report["observation"]["status"] = "unreadable" if bind_why != "ok" else "not-run"
        return report
    inspect, read, recover = parsed["inspect"], parsed["read"], parsed["recover"]
    report = base_report(options, "identity-mismatch", 1)
    report["_inspect"] = inspect
    report["_recover"] = recover
    report["core"] = {
        "inspect_exit": inspect["exit"],
        "read_exit": read["exit"],
        "recover_exit": recover["exit"],
    }
    recheck, recheck_why = read_cut(book, source, pass_id)
    p1.apply_intake(report, inspect)
    report["artifacts"] = artifacts_of(inspect)
    report["evidence_index"] = p1.evidence_of(report["artifacts"])
    moved = ["cut"] if bind_why == "ok" and recheck_why != "ok" else []
    if bind_why == "ok" and recheck_why == "ok":
        moved = changed_keys(bound, recheck)
    if moved:
        mark_unstable(report, bound, recheck if recheck_why == "ok" else None, moved)
        return finish_identity(report)
    if inspect.get("page") != source or inspect.get("pass") != pass_id or not p1.same(inspect.get("instance_id"), read.get("instance_id")) or not p1.same(inspect.get("instance_id"), recover.get("instance_id")):
        report["identity"]["selected_by"] = "mismatch"
        set_observation(report, bound, recheck, "mismatch", True if recheck_why == "ok" else None)
        return finish_identity(report)
    if not p1.apply_envelope(report, inspect, read, recover):
        report["identity"]["selected_by"] = "mismatch"
        set_observation(report, bound, recheck, "mismatch", True if recheck_why == "ok" else None)
        return finish_identity(report)
    inspect_id = p1.text_id(inspect, "current")
    read_id = p1.text_id(read, "review_id")
    recover_id = p1.text_id(recover, "review_id")
    report["identity"]["inspect_current"] = inspect_id
    report["identity"]["read_review_id"] = read_id
    report["identity"]["recover_review_id"] = recover_id
    no_judgment = (
        read.get("exit") == 2
        and recover.get("exit") == 2
        and read.get("correction") == "No recorded judgment."
        and recover.get("correction") == "No recorded judgment."
        and read_id is None
        and recover_id is None
    )
    if inspect_id is None and read_id is None and recover_id is None:
        report["state"] = "not-recorded"
        report["exit"] = 1
        report["stale"] = None
        report["identity"]["selected_by"] = "none"
        set_observation(report, bound, recheck, "coherent" if bind_why == "ok" and recheck_why == "ok" else bind_why, True if bind_why == "ok" and recheck_why == "ok" else None)
        p1.apply_publication(report, inspect, recover, False)
        return finish_identity(report)
    if no_judgment and isinstance(inspect_id, str):
        report["state"] = "held"
        report["exit"] = 1
        report["stale"] = True
        report["review_id"] = inspect_id
        current = bound.get("journal_current") if isinstance(bound, dict) else None
        report["judgment_recorded"] = False
        report["identity"]["journal_current"] = current
        report["identity"]["record_sha256"] = bound.get("record_sha256") if isinstance(bound, dict) else None
        report["identity"]["record_matches_journal"] = False
        report["identity"]["selected_by"] = "journal-current" if current == inspect_id else "none"
        report["attention"] = {"lines": None, "lines_state": "unknown", "source": None, "state": "not-exposed"}
        set_observation(report, bound, recheck, "coherent" if bind_why == "ok" else bind_why, True if bind_why == "ok" and recheck_why == "ok" else None)
        p1.apply_publication(report, inspect, recover, True)
        report["render_coverage"] = p1.render_coverage(None, False, source, pass_id, inspect_id, None)
        return finish_identity(report)
    if not (isinstance(inspect_id, str) and inspect_id == read_id == recover_id):
        report["identity"]["selected_by"] = "mismatch"
        set_observation(report, bound, recheck, "mismatch", True if recheck_why == "ok" and not moved else None)
        p1.apply_publication(report, inspect, recover, False)
        return finish_identity(report)
    if bind_why != "ok" or not isinstance(bound, dict):
        report["identity"]["selected_by"] = "mismatch"
        report["attention"] = {"lines": None, "lines_state": "unknown", "source": None, "state": "not-exposed"}
        set_observation(report, bound, recheck, bind_why, None)
        p1.apply_publication(report, inspect, recover, True)
        return finish_identity(report)
    if bound.get("journal_current") != inspect_id:
        report["identity"]["selected_by"] = "mismatch"
        report["review_id"] = bound.get("journal_current") if isinstance(bound.get("journal_current"), str) else None
        report["identity"]["journal_current"] = bound.get("journal_current")
        report["identity"]["record_sha256"] = bound.get("record_sha256")
        report["attention"] = {"lines": None, "lines_state": "unknown", "source": None, "state": "not-exposed"}
        set_observation(report, bound, recheck, "mismatch", True)
        p1.apply_publication(report, inspect, recover, True)
        return finish_identity(report)
    report["review_id"] = inspect_id
    report["identity"]["journal_current"] = bound.get("journal_current")
    report["identity"]["record_sha256"] = bound.get("record_sha256")
    report["judgment_recorded"] = True
    if bound.get("digest_kind") != "str" or not isinstance(bound.get("record_sha256"), str) or bound.get("record_file_sha256") != bound.get("record_sha256"):
        hold_mismatch(report, bound, recheck)
        report["judgment_recorded"] = False
        return finish_identity(report)
    record, why = checked_record(book, source, pass_id, inspect_id, bound["record_sha256"], inspect, recover)
    after, after_why = read_cut(book, source, pass_id)
    after_moved = [] if after_why != "ok" else changed_keys(bound, after)
    if after_why != "ok" or after_moved:
        mark_unstable(report, bound, after if after_why == "ok" else None, after_moved or ["cut"])
        report["judgment_recorded"] = False
        return finish_identity(report)
    if record is None or why != "ok":
        report["attention"] = {"lines": None, "lines_state": "unknown", "source": None, "state": "not-exposed"}
        report["exit"] = 1
        report["identity"]["judgment_matches_core"] = False
        if why in {"record-mismatch", "digest-mismatch"}:
            report["state"] = "held"
            report["stale"] = True
            report["identity"]["selected_by"] = "bound-cut"
            report["identity"]["record_matches_journal"] = False
            report["judgment_recorded"] = False
            set_observation(report, bound, after, "mismatch", True)
        else:
            report["state"] = "identity-mismatch"
            report["identity"]["selected_by"] = "mismatch"
            report["identity"]["record_matches_journal"] = why == "judgment-mismatch"
            report["judgment_recorded"] = False
            set_observation(report, bound, after, "mismatch", True)
        p1.apply_publication(report, inspect, recover, True)
        report["render_coverage"] = p1.render_coverage(
            None,
            False,
            source,
            pass_id,
            inspect_id,
            recover.get("rendered_ok") if type(recover.get("rendered_ok")) is bool else None,
        )
        return finish_identity(report)
    report["identity"]["record_matches_journal"] = True
    report["identity"]["judgment_matches_core"] = True
    report["identity"]["selected_by"] = "journal-current"
    set_observation(report, bound, after, "coherent", True)
    p1.show_judgment(report, record, recover)
    shown, shown_why = read_cut(book, source, pass_id)
    shown_moved = [] if shown_why != "ok" else changed_keys(bound, shown)
    if shown_why != "ok" or shown_moved:
        mark_unstable(report, bound, shown if shown_why == "ok" else None, shown_moved or ["cut"])
        return finish_identity(report)
    report["stale"] = inspect.get("stale") is True or read.get("stale") is True or recover.get("stale") is True
    report["state"] = "stale" if report["stale"] else "readable"
    report["exit"] = 1 if report["stale"] else 0
    p1.apply_publication(report, inspect, recover, True)
    return finish_identity(report)


def finish_identity(report: dict) -> dict:
    report.pop("_inspect", None)
    report.pop("_recover", None)
    return report


def counter_text(count, count_state: str, size, bytes_state: str, provenance: str) -> str:
    count_shown = "unknown" if count_state == "unknown" or count is None else str(count)
    bytes_shown = "unknown" if bytes_state == "unknown" or size is None else str(size)
    return f"count {count_shown}, bytes {bytes_shown}, provenance {provenance}"


def projection_of(report: dict) -> str:
    observation = report["observation"]
    bound = observation.get("bound") if isinstance(observation.get("bound"), dict) else {}
    artifacts = report["artifacts"]
    lines = [
        f"schema: {report['schema']}",
        f"state: {report['state']}",
        f"review_id: {p1.word(report['review_id'])}",
        f"observation: {observation.get('status')}",
        f"observation_stable: {p1.word(observation.get('stable'))}",
        f"selected_digest: {p1.word(bound.get('record_sha256') if isinstance(bound, dict) else None)}",
        f"judgment_recorded: {p1.word(report['judgment_recorded'])}",
        f"publication_class: {report['publication']['class']}",
        f"publication_status: {p1.word(report['publication']['status'])}",
        f"stale: {p1.word(report['stale'])}",
        f"custody: {p1.word(report['custody'])}",
        f"operation: {p1.word(report['operation'])}",
        f"disposition: {p1.word(report['disposition'])}",
        f"goal_terminal: {p1.word(report['goal_terminal'])}",
        f"pass_terminal: {p1.word(report['pass_terminal'])}",
        f"work_complete: {p1.word(report['work_complete'])}",
        f"action_released: {p1.word(report['action_released'])}",
        f"authority: {p1.word(report['authority'])}",
        f"task_association: {p1.word(report['task_association'])}",
        f"tests_passed: {p1.word(report['tests_passed']['value']) if report['tests_passed']['state'] == 'supplied' else 'unknown'}",
        f"tests_passed_label: {p1.word(report['tests_passed']['label'])}",
        f"tests_note: {report['tests_note']['text'] if report['tests_note']['state'] == 'supplied' else 'unknown'}",
        "limits: " + (
            report["limits"]["value"] if report["limits"]["state"] == "supplied" and isinstance(report["limits"]["value"], str)
            else "unknown" if report["limits"]["state"] != "supplied"
            else json.dumps(report["limits"]["value"], sort_keys=True)
        ),
        f"attention_state: {report['attention']['state']}",
    ]
    if report["attention"]["lines_state"] == "supplied" and isinstance(report["attention"]["lines"], list):
        lines.append("attention:")
        lines.extend(f"- {line}" for line in report["attention"]["lines"])
    elif report["attention"]["lines_state"] == "none-supplied":
        lines.append("attention: none supplied")
    elif report["attention"]["state"] == "not-exposed":
        lines.append("attention: not exposed")
    else:
        lines.append("attention: unknown")
    lines.append(f"next_action: {p1.word(report['next_action'])}")
    lines.append(
        "director_words: " + (
            report["director_text"]["text"] if report["director_text"]["state"] == "supplied"
            else "none measured" if report["director_text"]["state"] == "none-measured"
            else "unknown"
        )
    )
    holds = report["holds"]
    if holds["state"] == "none-supplied":
        lines.append("holds: none supplied")
    elif holds["state"] == "supplied":
        lines.append("holds:")
        for item in holds["items"]:
            if isinstance(item, dict):
                lines.append(f"- {item.get('hold_id')} {item.get('kind')} {item.get('finding_id')}")
            else:
                lines.append("- unknown")
    else:
        lines.append("holds: unknown")
    measured = artifacts.get("measured_artifact_rows") if isinstance(artifacts.get("measured_artifact_rows"), dict) else {}
    unique = artifacts.get("unique_files") if isinstance(artifacts.get("unique_files"), dict) else {}
    intake = artifacts.get("intake_roles") if isinstance(artifacts.get("intake_roles"), dict) else {}
    missing = artifacts.get("missing")
    lines.extend([
        "claims: not-recorded",
        f"evidence_index: {report['evidence_index']['state']}",
        "declared_artifacts: " + counter_text(
            artifacts.get("count"), artifacts.get("count_state", "unknown"),
            artifacts.get("bytes"), artifacts.get("bytes_state", "unknown"), "declared",
        ),
        "measured_artifact_rows: " + counter_text(
            measured.get("count"), measured.get("count_state", "unknown"),
            measured.get("bytes"), measured.get("bytes_state", "unknown"), "current-measured",
        ),
        "unique_files: " + counter_text(
            unique.get("count"), unique.get("count_state", "unknown"),
            unique.get("bytes"), unique.get("bytes_state", "unknown"), "current-measured",
        ),
        "intake_role_rows: " + counter_text(
            intake.get("count"), intake.get("count_state", "unknown"),
            intake.get("bytes"), intake.get("bytes_state", "unknown"), "current-measured",
        ),
        f"artifact_hash_match: {p1.word(artifacts.get('hash_match'))}",
        f"artifact_hash_mismatch: {p1.word(artifacts.get('hash_mismatch'))}",
        f"artifact_not_verified: {p1.word(artifacts.get('not_verified'))}",
        f"artifact_missing: {p1.word(len(missing) if isinstance(missing, list) else None)}",
        f"measurement: {p1.word(artifacts.get('measurement'))}",
        "observation_limit: " + OBSERVATION_LIMIT,
        "detail: " + ", ".join(DETAIL_FIELDS),
        p1.HISTORICAL,
    ])
    return "\n".join(lines) + "\n"


def finish(report: dict) -> dict:
    bound = report["observation"].get("bound")
    book = report.get("book")
    source = report.get("source")
    pass_id = report.get("pass")
    if isinstance(bound, dict) and isinstance(book, str) and isinstance(source, str) and isinstance(pass_id, str):
        cut, why = read_cut(book, source, pass_id)
        keys = ["cut"] if why != "ok" else changed_keys(bound, cut)
        if keys:
            mark_unstable(report, bound, cut if why == "ok" else None, keys)
    if report["observation"].get("stable") is False:
        report["publication"]["class"] = "unknown"
    else:
        report["publication"]["class"] = p1.publication_class(
            report["review_id"] is not None and report["state"] != "not-recorded",
            report["publication"]["status"],
            report["publication"]["target_state"],
            report["state"],
        )
    report["projection"] = projection_of(report)
    return report


def emit(report: dict) -> None:
    raw = (json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")
    sys.stdout.buffer.write(raw)


def main(argv: list[str] | None = None) -> int:
    blank = {"book": None, "code_root": None, "pass": None, "source": None}
    try:
        options = p1.parse_args(argv)
    except p1.Refuse as exc:
        print(f"refused: {exc.message}", file=sys.stderr)
        emit(finish(base_report(blank, "refused", 2)))
        return 2
    try:
        p1.check_pins(options["code_root"])
    except p1.Refuse as exc:
        print(f"refused: {exc.message}", file=sys.stderr)
        emit(finish(base_report(options, "refused", 2)))
        return 2
    report = finish(observe(options))
    if report["exit"] == 2:
        print("refused: core stdout is not one workbook-review-result/1 object", file=sys.stderr)
    emit(report)
    return int(report["exit"])


if __name__ == "__main__":
    sys.exit(main())
