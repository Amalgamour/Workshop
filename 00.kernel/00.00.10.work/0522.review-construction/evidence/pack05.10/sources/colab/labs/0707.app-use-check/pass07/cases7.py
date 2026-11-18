#!/usr/bin/env python3
"""0707/05.08 pass07: SUPPLEMENTAL case file (NONPRODUCTION). Two cases only.

Replaces the coverage of original A22 (pass04 cases.py, unchanged; its FAIL stays as
recorded in 0707/05.07) with two cases whose prerequisites match the unchanged cycle:
a template exists only when the target page exists (prime_cycle.py 1177).
Reuses pass04 helpers and patterns unchanged (imported, not copied).
"""

from __future__ import annotations

import json

import cases as C  # pass04 cases.py, unchanged, loaded by the driver after its hash check
import fixtures as F  # pass04 fixtures.py, unchanged; build_book is the pass06 guard wrapper

IDENTITY = "0707-supplemental-a22/1"


def flags_ok(ctx, row, where):
    body = row["json"]
    if isinstance(body, dict):
        bad = {k: body.get(k) for k, v in C.FLAGS.items() if body.get(k) != v}
        ctx.check(f"authority flags false: {where}", not bad, bad)


def committed_reviews(root):
    return sorted(p.parent.name for p in root.glob("cycle/*/COMMITTED.json"))


def facts(ctx, label):
    root = ctx.root
    target = root / F.TARGET
    body = {
        "target_exists": target.exists(),
        "target_sha256": F.sha(target.read_bytes()) if target.exists() else None,
        "decision_sha256": F.sha((root / "decision.json").read_bytes()) if (root / "decision.json").exists() else None,
        "committed_reviews": committed_reviews(root),
        "cycle_tree": F.tree(root / "cycle"),
        "partial": sorted(F.tree(root / "partial")),
    }
    (ctx.dir / f"facts-{label}.json").write_text(json.dumps(body, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return body


def a22a(ctx):
    """Absent before prepare: no template, truthful no-record guidance, no commitment, no permission."""
    C.setup(ctx, "absent")
    d = C.describe(ctx)
    flags_ok(ctx, d, "describe")
    facts(ctx, "before-prepare")
    prep = C.call(ctx, "prepare", "prepare")
    flags_ok(ctx, prep, "prepare")
    ctx.check("prepare exit 0", prep["exit"] == 0, prep["exit"])
    ctx.check("prepare target.state absent", ctx.field(prep["json"], "target.state") == "absent", ctx.field(prep["json"], "target.state"))
    ctx.check("prepare view.template is null (corrected prerequisite)", ctx.field(prep["json"], "view.template") is None,
              ctx.field(prep["json"], "view.template"))
    m = C.mech(ctx, prep)
    ctx.check("prepare text does not claim a commitment", not C.CLAIMS_COMMIT.search(m.get("text", "")), m.get("text"))
    ctx.check("prepare mechanical route grants no record or recover", m.get("route") not in ("record", "recover", None), m.get("route"))
    rd = C.call(ctx, "read", "read")
    flags_ok(ctx, rd, "read")
    text = C.mech(ctx, rd).get("text", "") + " " + json.dumps(ctx.field(rd["json"] or {}, "next"))
    ctx.check("read does not claim a commitment", not C.CLAIMS_COMMIT.search(text), text)
    ctx.check("R02 wording: not recorded (heuristic, unchanged)", bool(C.SAYS_NOT_RECORDED.search(text)), text)
    after = facts(ctx, "after-read")
    ctx.check("no committed review", after["committed_reviews"] == [], after["committed_reviews"])
    ctx.check("target still absent (not created)", after["target_exists"] is False)


def a22b(ctx):
    """Present at prepare, valid decision, target removed, then record must refuse and change nothing."""
    C.setup(ctx, "pending")
    d = C.describe(ctx)
    flags_ok(ctx, d, "describe")
    prep, decision = C.prepare_and_decide(ctx)
    flags_ok(ctx, prep, "prepare")
    ctx.check("prepare target.state pending", ctx.field(prep["json"], "target.state") == "pending", ctx.field(prep["json"], "target.state"))
    if decision is None:
        return
    (ctx.dir / "decision.before-record.json").write_bytes(decision)
    before = facts(ctx, "after-decision")
    target = ctx.root / F.TARGET
    target.unlink()
    removed = facts(ctx, "after-target-removed")
    ctx.check("fixture removed the target", removed["target_exists"] is False and before["target_exists"] is True)
    rec = C.call(ctx, "record", "record", decision=True)
    flags_ok(ctx, rec, "record")
    C.refused(ctx, rec, "record")
    after = facts(ctx, "after-record")
    ctx.check("decision.json bytes identical", (ctx.root / "decision.json").read_bytes() == decision,
              {"before": F.sha(decision), "after": after["decision_sha256"]})
    ctx.check("no committed review", after["committed_reviews"] == [], after["committed_reviews"])
    ctx.check("target not recreated", after["target_exists"] is False)
    ctx.check("no partial", after["partial"] == [], after["partial"])
    rd = C.call(ctx, "read", "read")
    flags_ok(ctx, rd, "read")
    text = C.mech(ctx, rd).get("text", "") + " " + json.dumps(ctx.field(rd["json"] or {}, "next"))
    ctx.check("read does not claim a commitment", not C.CLAIMS_COMMIT.search(text), text)
    ctx.check("R02 wording: not recorded (heuristic, unchanged)", bool(C.SAYS_NOT_RECORDED.search(text)), text)
    final = facts(ctx, "after-read")
    ctx.check("still no committed review after read", final["committed_reviews"] == [])


CASES = [
    {"id": "A22a", "title": "absent before prepare: no template, truthful no-record guidance, no commitment", "fn": a22a},
    {"id": "A22b", "title": "present at prepare, target removed before record: record refuses, decision unchanged", "fn": a22b},
]
