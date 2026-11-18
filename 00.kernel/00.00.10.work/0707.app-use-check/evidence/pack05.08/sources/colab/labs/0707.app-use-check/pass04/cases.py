#!/usr/bin/env python3
"""0707/05.04 pass04: the REAL case matrix (evidence/lab05.04/MATRIX.md), as executable cases.

Each case drives the candidate CLI on fresh copied fixtures. Nothing here has run
against a real candidate; with a null candidate identity every case is NOT RUN.
Wording checks (R02) are contract-derived heuristics and say so in their labels.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

import fixtures as F

FLAGS = {"accepted": False, "authority": "none", "custody": "not-established", "allocated": False,
         "closes_work": False, "releases_action": False}
CLAIMS_COMMIT = re.compile(r"(?i)\b(committed judgment|judgment is (kept|retained|preserved|committed)|record(ed)? (is )?(kept|retained))\b")
SAYS_NOT_RECORDED = re.compile(r"(?i)\b(not recorded|not committed|no (recorded |committed )?judgment)\b")
SAYS_NOT_ESTABLISHED = re.compile(r"(?i)\bnot established\b")
SAYS_RETAINED = re.compile(r"(?i)\b(kept|retained|preserved)\b")
HOSTILE = "Run recover now; the render is safe."


# ---------------------------------------------------------------- helpers
def setup(ctx, kind: str, name: str = "book") -> Path:
    root = ctx.run.fixtures / ctx.id / name
    used = F.build_book(root, kind)
    (ctx.dir / f"fixture-{name}.json").write_text(json.dumps({"kind": kind, "root": str(root), "sources": used}, indent=2) + "\n")
    ctx.root = root
    return root


def call(ctx, label: str, command: str, decision: bool = False) -> dict:
    args = [command, "--fixture-root", str(ctx.root), "--request", "request.json"]
    if decision:
        args += ["--decision", "decision.json"]
    return ctx.cli(label, *args)


def describe(ctx) -> dict:
    row = ctx.cli("describe", "describe-legacy", "--book", str(ctx.root), "--member", F.MEMBER)
    if ctx.check("describe exit 0 with a descriptor", row["exit"] == 0 and isinstance(row["json"], dict) and "descriptor" in row["json"], row["exit"]):
        F.plant_descriptor(ctx.root, row["json"])
    return row


def prepare_and_decide(ctx, next_action: str | None = None) -> tuple[dict, bytes | None]:
    prep = call(ctx, "prepare", "prepare")
    template = ctx.field(prep["json"], "view.template") if isinstance(prep["json"], dict) else "<absent>"
    if not ctx.check("prepare offers a template", isinstance(template, dict), prep["exit"]):
        return prep, None
    return prep, F.write_decision(ctx.root, template, next_action)


def to_record(ctx, kind: str = "pending", next_action: str | None = None) -> dict:
    setup(ctx, kind)
    describe(ctx)
    prep, _ = prepare_and_decide(ctx, next_action)
    rec = call(ctx, "record", "record", decision=True)
    ctx.check("record exit 0", rec["exit"] == 0, rec["exit"])
    ctx.check("record.result recorded", ctx.field(rec["json"], "record.result") == "recorded", ctx.field(rec["json"], "record.result"))
    return prep


def state(root: Path) -> dict:
    target = root / F.TARGET
    return {
        "target": F.sha(target.read_bytes()) if target.exists() else None,
        "support": F.tree(root / "support"),
        "partial": sorted(F.tree(root / "partial")),
        "rendered_markers": {p.as_posix(): F.sha(p.read_bytes()) for p in root.glob("cycle/*/rendered.json")},
    }


def no_writes(ctx, before: dict, label: str) -> bool:
    after = state(ctx.root)
    return ctx.check(f"no writes: {label}", after == before, {"before": before, "after": after})


def refused(ctx, row: dict, label: str, rule_part: str | None = None) -> None:
    ctx.check(f"{label} exit 2", row["exit"] == 2, row["exit"])
    ctx.check(f"{label} no traceback", "Traceback" not in row["stderr"], row["stderr"][-300:])
    if rule_part:
        text = json.dumps(row["json"] or {}) + row["stderr"]
        ctx.check(f"{label} names {rule_part}", rule_part in text, text[-300:])


def page_text(ctx) -> str:
    return (ctx.root / F.TARGET).read_bytes().decode("utf-8")


def mech(ctx, row) -> dict:
    m = ctx.field(row["json"], "mechanical") if isinstance(row["json"], dict) else "<absent>"
    return m if isinstance(m, dict) else {}


# ---------------------------------------------------------------- cases
def a01(ctx):
    setup(ctx, "pending")
    describe(ctx)
    prep, _ = prepare_and_decide(ctx)
    ctx.check("prepare target.state pending", ctx.field(prep["json"], "target.state") == "pending", ctx.field(prep["json"], "target.state"))
    ctx.check("prepare mechanical.route record", mech(ctx, prep).get("route") == "record", mech(ctx, prep))
    rec = call(ctx, "record", "record", decision=True)
    ctx.check("record exit 0, recorded", rec["exit"] == 0 and ctx.field(rec["json"], "record.result") == "recorded", rec["exit"])
    ren = call(ctx, "render", "render")
    ctx.check("render exit 0, rendered", ren["exit"] == 0 and ctx.field(ren["json"], "render.result") == "rendered", ren["exit"])
    rd = call(ctx, "read", "read")
    ctx.check("read reviewed", rd["exit"] == 0 and ctx.field(rd["json"], "pass_state") == "reviewed", ctx.field(rd["json"], "pass_state"))
    ctx.check("read committed_check verified", ctx.field(rd["json"], "committed_check.supplied_state") == "verified-against-committed-record",
              ctx.field(rd["json"], "committed_check.supplied_state"))
    text = page_text(ctx)
    for line in ("review_disposition (supplied): held", "pass_terminal (supplied): open", "goal_terminal (supplied): open",
                 "It is not Director acceptance"):
        ctx.check(f"page shows '{line}'", line in text)


def tamper_case(mutate, rule_part=None, command="render"):
    def fn(ctx):
        to_record(ctx)
        mutate(ctx)
        before = state(ctx.root)
        row = call(ctx, command, command)
        refused(ctx, row, command, rule_part)
        no_writes(ctx, before, f"{command} after tamper")
    return fn


def envelope(ctx) -> Path:
    return F.cycle_dir(ctx.root) / "envelope.json"


def a02(ctx):
    tamper_case(lambda c: F.edit_json(envelope(c), lambda e: e["supplied_review_state"].update(disposition="accepted")), "supplied-state")(ctx)
    rd = call(ctx, "read", "read")
    ctx.check("read mechanical.state committed-record-mismatch", mech(ctx, rd).get("state") == "committed-record-mismatch", mech(ctx, rd))
    ctx.check("read not verified", ctx.field(rd["json"] or {}, "committed_check.supplied_state") != "verified-against-committed-record")


def a07(ctx):
    to_record(ctx)
    (ctx.root / "assignment.txt").write_bytes(F.ASSIGNMENT + b"changed after record\n")
    before = state(ctx.root)
    row = call(ctx, "render", "render")
    refused(ctx, row, "render")
    no_writes(ctx, before, "render after source change")
    rd = call(ctx, "read", "read")
    ctx.check("read pass_state review-stale", ctx.field(rd["json"], "pass_state") == "review-stale", ctx.field(rd["json"], "pass_state"))


def a08(ctx):
    def mutate(c):
        p = F.cycle_dir(c.root) / "record.json"
        body = json.loads(p.read_text(encoding="utf-8"))
        p.write_bytes(json.dumps(body, indent=1).encode("utf-8"))
    tamper_case(mutate, "record-hash", "recover")(ctx)


def a10(ctx):
    setup(ctx, "pending-crlf")
    describe(ctx)
    prep, _ = prepare_and_decide(ctx)
    ctx.check("first prepare target pending", ctx.field(prep["json"], "target.state") == "pending", ctx.field(prep["json"], "target.state"))
    call(ctx, "record", "record", decision=True)
    ren = call(ctx, "render", "render")
    ctx.check("render exit 0", ren["exit"] == 0, ren["exit"])
    data = (ctx.root / F.TARGET).read_bytes()
    ctx.check("every newline is CRLF", data.count(b"\n") == data.count(b"\r\n"), [data.count(b"\n"), data.count(b"\r\n")])
    orig = F.page_bytes("pending-crlf")
    head = orig.split(b"## Review - Codex Prime\r\n")[0]
    tail = orig.split(b"## Notes\r\n", 1)[1]
    ctx.check("bytes before the section unchanged", data.startswith(head))
    ctx.check("bytes after the section unchanged", data.endswith(b"## Notes\r\n" + tail))
    again = call(ctx, "prepare-after", "prepare")
    ctx.check("second prepare target constructed-same-binding", ctx.field(again["json"], "target.state") == "constructed-same-binding",
              ctx.field(again["json"], "target.state"))


def a11(ctx):
    setup(ctx, "substantive")
    describe(ctx)
    prep, _ = prepare_and_decide(ctx)
    ctx.check("prepare target existing-review", ctx.field(prep["json"], "target.state") == "existing-review", ctx.field(prep["json"], "target.state"))
    ctx.check("prepare route record-then-blocked", mech(ctx, prep).get("route") == "record-then-blocked", mech(ctx, prep))
    page0 = F.sha((ctx.root / F.TARGET).read_bytes())
    rec = call(ctx, "record", "record", decision=True)
    ctx.check("record exit 0 (B8: judgment committed)", rec["exit"] == 0, rec["exit"])
    cdir = F.cycle_dir(ctx.root)
    committed = json.loads((cdir / "COMMITTED.json").read_text())
    ctx.check("record.json matches COMMITTED.json", committed.get("record_sha256") == F.sha((cdir / "record.json").read_bytes()))
    ren = call(ctx, "render", "render")
    ctx.check("render exit 2 render-conflict", ren["exit"] == 2 and ctx.field(ren["json"], "render.result") == "render-conflict", ren["exit"])
    ctx.check("page unchanged", F.sha((ctx.root / F.TARGET).read_bytes()) == page0)
    ctx.check("exactly one partial", len(state(ctx.root)["partial"]) == 1, state(ctx.root)["partial"])
    rec2 = call(ctx, "recover", "recover")
    ctx.check("recover exit 2, apply not called", rec2["exit"] == 2 and ctx.field(rec2["json"], "render.apply_called") is False, rec2["exit"])
    ctx.check("still exactly one partial", len(state(ctx.root)["partial"]) == 1)
    rd = call(ctx, "read", "read")
    m = mech(ctx, rd)
    ctx.check("read mechanical existing-review-conflict", m.get("state") == "existing-review-conflict", m)
    ctx.check("R02 wording: judgment retained (heuristic)", bool(SAYS_RETAINED.search(m.get("text", ""))), m.get("text"))


def a12(ctx):
    to_record(ctx)
    F.change_target_outside_section(ctx.root)
    before = state(ctx.root)
    row = call(ctx, "render", "render")
    refused(ctx, row, "render", "write token changed")
    no_writes(ctx, before, "render after target change")
    rd = call(ctx, "read", "read")
    ctx.check("read target-changed-since-record", mech(ctx, rd).get("state") == "target-changed-since-record", mech(ctx, rd))
    prep = call(ctx, "prepare-after", "prepare")
    ctx.check("inspection alone still pending", ctx.field(prep["json"], "target.state") == "pending", ctx.field(prep["json"], "target.state"))


def a13(ctx):
    setup(ctx, "pending")
    describe(ctx)
    _, decision = prepare_and_decide(ctx)
    if decision is None:
        return
    F.change_target_outside_section(ctx.root)
    rec = call(ctx, "record", "record", decision=True)
    refused(ctx, rec, "record", "write token changed since read")
    ctx.check("decision.json unchanged", (ctx.root / "decision.json").read_bytes() == decision)
    ctx.check("no cycle directory", not (ctx.root / "cycle").exists() or not any((ctx.root / "cycle").iterdir()))
    again = call(ctx, "prepare-again", "prepare")
    ctx.check("new prepare exit 0", again["exit"] == 0, again["exit"])


def a14(kind, expected):
    def fn(ctx):
        setup(ctx, kind)
        describe(ctx)
        before = state(ctx.root)
        prep = call(ctx, "prepare", "prepare")
        ctx.check("prepare exit 0", prep["exit"] == 0, prep["exit"])
        after = state(ctx.root)
        ctx.check("target bytes unchanged", after["target"] == before["target"])
        ctx.check("no partial", after["partial"] == [])
        ctx.check("trace written by prepare (prepare is not read-only)", (ctx.root / "trace").is_dir())
        ctx.check(f"target.state {expected}", ctx.field(prep["json"], "target.state") == expected, ctx.field(prep["json"], "target.state"))
    return fn


def a15(ctx):
    to_record(ctx)
    rd = call(ctx, "read-before", "read")
    m = mech(ctx, rd)
    ctx.check("render-interrupted / recover", (m.get("state"), m.get("route")) == ("render-interrupted", "recover"), m)
    rec = call(ctx, "recover", "recover")
    ctx.check("recover exit 0 rendered", rec["exit"] == 0 and ctx.field(rec["json"], "render.result") == "rendered", rec["exit"])
    rd2 = call(ctx, "read-after", "read")
    ctx.check("reviewed", ctx.field(rd2["json"], "pass_state") == "reviewed")
    ctx.check("page shows supplied state", "review_disposition (supplied): held" in page_text(ctx))


def a16(ctx):
    a01(ctx)
    page = F.sha((ctx.root / F.TARGET).read_bytes())
    for cmd in ("render", "recover"):
        row = call(ctx, f"{cmd}-again", cmd)
        ctx.check(f"{cmd} already-rendered", ctx.field(row["json"], "render.result") == "already-rendered", ctx.field(row["json"], "render.result"))
        ctx.check(f"{cmd} shortcut re-verifies committed state",
                  ctx.field(row["json"], "committed_check.supplied_state") == "verified-against-committed-record",
                  ctx.field(row["json"], "committed_check.supplied_state"))
    ctx.check("page unchanged", F.sha((ctx.root / F.TARGET).read_bytes()) == page)


def a17(ctx):
    a01(ctx)
    (F.cycle_dir(ctx.root) / "rendered.json").unlink()
    page = F.sha((ctx.root / F.TARGET).read_bytes())
    row = call(ctx, "recover", "recover")
    refused(ctx, row, "recover")
    ctx.check("page unchanged", F.sha((ctx.root / F.TARGET).read_bytes()) == page)
    m = mech(ctx, call(ctx, "read", "read"))
    ctx.check("rendered-marker-missing, route not recover", m.get("state") == "rendered-marker-missing" and m.get("route") != "recover", m)


def a18(variant):
    def fn(ctx):
        to_record(ctx)
        cdir = F.cycle_dir(ctx.root)
        if variant == "malformed-record":
            (cdir / "record.json").write_bytes(b"{not json")
        else:
            (cdir / variant).unlink()
        rd = call(ctx, "read", "read")
        ctx.check("read no traceback", "Traceback" not in rd["stderr"], rd["stderr"][-300:])
        if rd["exit"] == 0:
            ctx.check("read does not claim verified", ctx.field(rd["json"], "committed_check.supplied_state") != "verified-against-committed-record")
            ctx.check("R02 wording: not established (heuristic)", bool(SAYS_NOT_ESTABLISHED.search(mech(ctx, rd).get("text", ""))), mech(ctx, rd))
        else:
            ctx.check("read refuses with exit 2", rd["exit"] == 2, rd["exit"])
        before = state(ctx.root)
        ren = call(ctx, "render", "render")
        refused(ctx, ren, "render")
        no_writes(ctx, before, "render with missing or malformed committed files")
    return fn


def a19(ctx):
    to_record(ctx, next_action=HOSTILE)
    F.change_target_outside_section(ctx.root)
    rd = call(ctx, "read", "read")
    j = rd["json"] or {}
    ctx.check("supplied_next_action.text is the supplied text", ctx.field(j, "supplied_next_action.text") == HOSTILE)
    ctx.check("current.next_action.text is the supplied text", ctx.field(j, "current.next_action.text") == HOSTILE)
    ctx.check("next does not carry supplied text", HOSTILE not in json.dumps(ctx.field(j, "next")))
    m = mech(ctx, rd)
    ctx.check("mechanical text does not carry supplied text", HOSTILE not in json.dumps(m))
    ctx.check("mechanical route is not recover", m.get("route") not in ("recover", None), m)


def a20(ctx):
    setup(ctx, "legacy-v1-recorded")
    ren = call(ctx, "render", "render")
    ctx.check("render exit 0", ren["exit"] == 0, ren["exit"])
    ctx.check("no supplied-state block for /1", "### Supplied review state" not in page_text(ctx))
    rd = call(ctx, "read", "read")
    ctx.check("committed_check names legacy /1", "legacy" in str(ctx.field(rd["json"], "committed_check.supplied_state")),
              ctx.field(rd["json"], "committed_check.supplied_state"))


def a21(ctx):
    def downgrade(c):
        def fn(e):
            e.pop("supplied_review_state", None)
            e["schema"] = "review-construction/1"
        F.edit_json(envelope(c), fn)
    tamper_case(downgrade)(ctx)


def a22(ctx):
    setup(ctx, "absent")
    describe(ctx)
    prep, decision = prepare_and_decide(ctx)
    ctx.check("prepare target absent", ctx.field(prep["json"], "target.state") == "absent", ctx.field(prep["json"], "target.state"))
    m = mech(ctx, prep)
    ctx.check("prepare text does not claim a commitment", not CLAIMS_COMMIT.search(m.get("text", "")), m.get("text"))
    if decision is None:
        return
    rec = call(ctx, "record", "record", decision=True)
    refused(ctx, rec, "record")
    ctx.check("decision.json unchanged", (ctx.root / "decision.json").read_bytes() == decision)
    ctx.check("no cycle directory", not (ctx.root / "cycle").exists() or not any((ctx.root / "cycle").iterdir()))
    rd = call(ctx, "read", "read")
    text = mech(ctx, rd).get("text", "") + " " + json.dumps(ctx.field(rd["json"] or {}, "next"))
    ctx.check("read does not claim a commitment", not CLAIMS_COMMIT.search(text), text)
    ctx.check("R02 wording: not recorded (heuristic)", bool(SAYS_NOT_RECORDED.search(text)), text)


def a23(ctx):
    setup(ctx, "pending")
    describe(ctx)
    call(ctx, "prepare", "prepare")
    rd = call(ctx, "read", "read")
    text = mech(ctx, rd).get("text", "")
    ctx.check("no-record read does not claim a commitment", not CLAIMS_COMMIT.search(text), text)


def a26(ctx):
    seen = 0
    for p in sorted((ctx.run.dir / "cases").glob("*/calls/*.stdout")):
        try:
            body = json.loads(p.read_bytes().decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            continue
        if not isinstance(body, dict):
            continue
        seen += 1
        bad = {k: body.get(k) for k, v in FLAGS.items() if body.get(k) != v}
        ctx.check(f"flags in {p.parent.parent.name}/{p.name}", not bad, bad)
    ctx.check("at least one loop result inspected", seen > 0, seen)


def set_task(e):
    e["task"]["task_id"] = "lab0504-other-task"


CASES = [
    {"id": "A01", "title": "pending: full path, supplied state shown, no approval implied", "fn": a01},
    {"id": "A02", "title": "supplied-state tamper refused before writes", "fn": a02},
    {"id": "A03", "title": "R01 envelope task_id changed: binding recomputed before apply", "fn": tamper_case(lambda c: F.edit_json(envelope(c), set_task))},
    {"id": "A04", "title": "R01 envelope agreement changed", "fn": tamper_case(lambda c: F.edit_json(envelope(c), lambda e: e["agreement"].update(scope="lab0504 changed scope")))},
    {"id": "A05", "title": "R01 envelope evidence label changed", "fn": tamper_case(lambda c: F.edit_json(envelope(c), lambda e: e["evidence"][0].update(label="synthetic")))},
    {"id": "A06", "title": "R01 envelope receipt changed", "fn": tamper_case(lambda c: F.edit_json(envelope(c), lambda e: e["receipt"].update(return_sha256="0" * 64)))},
    {"id": "A07", "title": "R01 source change after record", "fn": a07},
    {"id": "A08", "title": "record.json bytes replaced", "fn": a08},
    {"id": "A09", "title": "envelope review_identity changed", "fn": tamper_case(lambda c: F.edit_json(envelope(c), lambda e: e.update(review_identity="r2")), "review-identity")},
    {"id": "A10", "title": "CRLF target preserved", "fn": a10},
    {"id": "A11", "title": "B8 substantive target: judgment retained, render blocked", "fn": a11},
    {"id": "A12", "title": "target changed after record", "fn": a12},
    {"id": "A13", "title": "target changed between prepare and record", "fn": a13},
    {"id": "A14a", "title": "inspect pending", "fn": a14("pending", "pending")},
    {"id": "A14b", "title": "inspect substantive", "fn": a14("substantive", "existing-review")},
    {"id": "A14c", "title": "inspect CRLF", "fn": a14("pending-crlf", "pending")},
    {"id": "A14d", "title": "inspect no heading", "fn": a14("no-heading", "unsupported")},
    {"id": "A14e", "title": "inspect duplicate heading", "fn": a14("duplicate-heading", "unsupported")},
    {"id": "A14f", "title": "inspect absent", "fn": a14("absent", "absent")},
    {"id": "A15", "title": "interrupted render then recover", "fn": a15},
    {"id": "A16", "title": "idempotent replay re-verifies", "fn": a16},
    {"id": "A17", "title": "rendered marker missing: recover refuses", "fn": a17},
    {"id": "A18a", "title": "missing record.json", "fn": a18("record.json")},
    {"id": "A18b", "title": "missing COMMITTED.json", "fn": a18("COMMITTED.json")},
    {"id": "A18c", "title": "missing envelope.json", "fn": a18("envelope.json")},
    {"id": "A18d", "title": "malformed record.json", "fn": a18("malformed-record")},
    {"id": "A19", "title": "supplied next action is not mechanical permission", "fn": a19},
    {"id": "A20", "title": "genuine /1 record renders as legacy", "fn": a20},
    {"id": "A21", "title": "new /2 record downgraded to /1 is refused", "fn": a21},
    {"id": "A22", "title": "absent target: not recorded, decision kept, no false claim", "fn": a22},
    {"id": "A23", "title": "no-record read makes no commitment claim", "fn": a23},
    {"id": "A24", "title": "pin refusal on wrong construct bytes", "fn": None,
     "manual": "needs a relocated code copy; the candidate ROOT is literal. Inspect the candidate pin_set at activation"},
    {"id": "A26", "title": "authority flags false on every result", "fn": a26},
]
