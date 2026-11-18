#!/usr/bin/env python3
"""Readiness aggregation, harness successor (0707/05.22). NONPRODUCTION. Standard library only.

Changes from pass01 (06.21 H2, H4):
  - every collection is type-checked: records, the full required baseline, the selection and the dependency rows.
    None, a dict or a string in place of a list is a reason, never 'zero items';
  - readiness is measured against the IMMUTABLE full required baseline (the registry's required ids), not against
    the selected subset. A subset reports its own result separately and enumerates the missing coverage;
  - dependency rows need id (non-empty str), status (accepted|pending|rejected) and an explicit boolean 'required';
    duplicates and an empty dependency list are reasons.
READY only if: scope is full, every required id has exactly one well-formed record with verdict 'pass', nothing
crashed, and every dependency row is well-formed and accepted. Ready is test evidence, never approval or release.
"""

from __future__ import annotations

VERDICTS = {"pass", "fail", "blocked", "not-run", "error", "known-failure-reproduced", "known-failure-not-reproduced"}
FIELDS = ("id", "group", "requirement", "required", "expected", "observed", "verdict", "evidence", "provenance")
DEP_STATUS = {"accepted", "pending", "rejected"}


def _id_list(value, label, reasons) -> list:
    if not isinstance(value, list):
        reasons.append(f"{label} is not a list (got {type(value).__name__})")
        return []
    bad = [x for x in value if not isinstance(x, str) or not x]
    if bad:
        reasons.append(f"{label} holds non-string or empty ids: {bad[:5]}")
    good = [x for x in value if isinstance(x, str) and x]
    if len(set(good)) != len(good):
        reasons.append(f"{label} repeats ids")
    return good


def check_dependencies(dependencies) -> list:
    reasons = []
    if not isinstance(dependencies, list):
        return [f"dependencies is not a list (got {type(dependencies).__name__})"]
    if not dependencies:
        return ["no dependency rows declared"]
    seen = set()
    for dep in dependencies:
        if not isinstance(dep, dict):
            reasons.append(f"malformed dependency row (not an object): {str(dep)[:60]}")
            continue
        did, st, req = dep.get("id"), dep.get("status"), dep.get("required")
        if not isinstance(did, str) or not did:
            reasons.append(f"malformed dependency row (id): {str(dep)[:60]}")
            continue
        if did in seen:
            reasons.append(f"duplicate dependency id {did}")
        seen.add(did)
        if st not in DEP_STATUS:
            reasons.append(f"dependency {did} has unknown status {st!r}")
        if not isinstance(req, bool):
            reasons.append(f"dependency {did} has no explicit boolean 'required' (got {req!r})")
        elif req and st != "accepted":
            reasons.append(f"dependency {did} is {st}")
    return reasons


def aggregate(records, full_required, dependencies, selected_required=None) -> dict:
    reasons = []
    full = _id_list(full_required, "full required baseline", reasons)
    if isinstance(full_required, list) and not full:
        reasons.append("no required cases declared")
    selected = full if selected_required is None else _id_list(selected_required, "selected required", reasons)
    unknown_sel = sorted(set(selected) - set(full))
    if unknown_sel:
        reasons.append(f"selected ids outside the full required baseline: {unknown_sel}")
    by_id = {}
    if not isinstance(records, list):
        reasons.append(f"records is not a list (got {type(records).__name__})")
        records = []
    for rec in records:
        if not isinstance(rec, dict) or any(f not in rec for f in FIELDS) or not isinstance(rec.get("id"), str):
            reasons.append(f"malformed case record: {str(rec)[:80]}")
            continue
        if rec["id"] in by_id:
            reasons.append(f"duplicate case id {rec['id']}")
        by_id[rec["id"]] = rec
    for cid, rec in by_id.items():
        if not isinstance(rec["required"], bool):
            reasons.append(f"case {cid} has a non-boolean 'required'")
        if rec["verdict"] == "error":
            reasons.append(f"case {cid} crashed")
    missing = [cid for cid in full if cid not in by_id]
    if missing:
        reasons.append(f"coverage incomplete: {len(missing)} required case(s) have no record: {missing}")
    for cid in full:
        rec = by_id.get(cid)
        if rec is None:
            continue
        if rec["required"] is not True:
            reasons.append(f"required case {cid} is not marked required in its record")
        if rec["verdict"] not in VERDICTS:
            reasons.append(f"required case {cid} has unknown verdict {rec['verdict']!r}")
        elif rec["verdict"] != "pass":
            reasons.append(f"required case {cid}: {rec['verdict']}")
    extra = sorted(cid for cid, r in by_id.items() if r.get("required") is True and cid not in full)
    if extra:
        reasons.append(f"required records outside the full required baseline: {extra}")
    reasons += check_dependencies(dependencies)
    counts = {}
    for rec in by_id.values():
        counts[rec["verdict"]] = counts.get(rec["verdict"], 0) + 1
    scope = "full" if selected_required is None or set(selected) == set(full) else "subset"
    sel_recs = [by_id.get(c) for c in selected]
    subset_pass = bool(selected) and all(r is not None and r.get("verdict") == "pass" and r.get("required") is True for r in sel_recs) \
        and not any(r["verdict"] == "error" for r in by_id.values())
    return {"ready": not reasons and scope == "full", "scope": scope, "reasons": reasons, "counts": counts,
            "required_full": len(full), "required_selected": len(selected), "coverage_missing": missing,
            "subset": {"ids": selected, "all_selected_required_pass": subset_pass,
                       "note": "a subset result is diagnostic only; it is never combined readiness"}}
