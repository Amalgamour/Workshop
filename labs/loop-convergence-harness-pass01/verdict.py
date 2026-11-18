#!/usr/bin/env python3
"""Readiness aggregation for the 0707/05.21 acceptance harness. NONPRODUCTION. Standard library only.

READY only if ALL of:
  - at least one required case exists, and the required case list equals the suite's declared required ids;
  - every required case record is well-formed and its verdict is exactly 'pass';
  - no required dependency has status other than 'accepted';
  - no case (required or not) has verdict 'error'.
Everything else is NOT READY. Unknown verdict strings, missing records, missing fields, 'blocked', 'not-run',
'fail', 'known-failure-reproduced' on a required case, or a process exit code are never treated as success.
"""

from __future__ import annotations

VERDICTS = {"pass", "fail", "blocked", "not-run", "error", "known-failure-reproduced", "known-failure-not-reproduced"}
FIELDS = ("id", "group", "requirement", "required", "expected", "observed", "verdict", "evidence", "provenance")


def aggregate(records: list, declared_required: list, dependencies: list) -> dict:
    reasons = []
    by_id = {}
    for rec in records if isinstance(records, list) else []:
        if not isinstance(rec, dict) or any(f not in rec for f in FIELDS):
            reasons.append(f"malformed case record: {str(rec)[:80]}")
            continue
        if rec["id"] in by_id:
            reasons.append(f"duplicate case id {rec['id']}")
        by_id[rec["id"]] = rec
    if not isinstance(records, list):
        reasons.append("records is not a list")
    if not declared_required:
        reasons.append("no required cases declared")
    for cid in declared_required:
        rec = by_id.get(cid)
        if rec is None:
            reasons.append(f"required case {cid} has no record (not-run)")
            continue
        if rec["required"] is not True:
            reasons.append(f"required case {cid} is not marked required in its record")
        if rec["verdict"] not in VERDICTS:
            reasons.append(f"required case {cid} has unknown verdict {rec['verdict']!r}")
        elif rec["verdict"] != "pass":
            reasons.append(f"required case {cid}: {rec['verdict']}")
    extra_required = sorted(cid for cid, r in by_id.items() if r.get("required") is True and cid not in declared_required)
    if extra_required:
        reasons.append(f"required records not declared by the suite: {extra_required}")
    for cid, rec in by_id.items():
        if rec["verdict"] == "error":
            reasons.append(f"case {cid} crashed")
    for dep in dependencies if isinstance(dependencies, list) else []:
        if not isinstance(dep, dict) or "id" not in dep or "status" not in dep:
            reasons.append(f"malformed dependency row: {str(dep)[:80]}")
        elif dep.get("required", True) and dep["status"] != "accepted":
            reasons.append(f"dependency {dep['id']} is {dep['status']}")
    counts = {}
    for rec in by_id.values():
        counts[rec["verdict"]] = counts.get(rec["verdict"], 0) + 1
    return {"ready": not reasons, "reasons": reasons, "counts": counts, "required": len(declared_required)}
