#!/usr/bin/env python3
"""0707/05.13 NONPRODUCTION example builder and cut measurer.

Writes small SYNTHETIC source pages under ./examples/fixture, then MEASURES every cited cut
(resolves exactly once? sha256) for examples a, b, c1-c3 and for the design application to the
real 0412/06.08 record. The holds/states in each example are the SPECIFIED behavior from
task-agreement.declaration.json, labelled NOT RUN: no target, core or API is called.
usage: make_examples.py   (refuses to overwrite ./examples/views)
"""

from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
FX = HERE / "examples" / "fixture" / "book" / "00.00.10.work"
VIEWS = HERE / "examples" / "views"
WORK = HERE.parents[2]          # 00.kernel/00.00.10.work
M = "SYNTHETIC FIXTURE — 0707/05.13 design example. Not live work, not a Director record, not authority."


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def cut(path: Path, kind: str, heading: str | None = None) -> dict:
    """Measure a cut. heading: bytes from '## <heading>' to before the next '## ' line."""
    if not path.is_file():
        return {"path": str(path), "resolved": False, "reason": "file missing"}
    b = path.read_bytes()
    if kind == "whole":
        return {"resolved": True, "count": 1, "sha256": sha(b), "bytes": len(b)}
    if kind == "pack":
        i = b.find(b"\n## Return pointer")
        body = b if i < 0 else b[: i + 1]
        return {"resolved": True, "count": 1, "sha256": sha(body), "bytes": len(body)}
    pat = re.compile(rb"^## " + re.escape(heading.encode()) + rb"\r?$", re.M)
    hits = list(pat.finditer(b))
    if len(hits) != 1:
        return {"resolved": False, "count": len(hits), "reason": "heading must occur exactly once"}
    start = hits[0].start()
    nxt = re.compile(rb"^## ", re.M).search(b, hits[0].end())
    body = b[start: nxt.start() if nxt else len(b)]
    return {"resolved": True, "count": 1, "sha256": sha(body), "bytes": len(body)}


def put(rel: str, text: str) -> Path:
    p = FX / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(text.encode("utf-8"))
    return p


def block(d: dict) -> str:
    return "```task-agreement\n" + json.dumps(d, indent=1) + "\n```\n"


def main() -> int:
    if VIEWS.exists():
        sys.exit("refused: views exist")
    VIEWS.mkdir(parents=True)
    # standing records (synthetic stand-ins for 0412/01 and the director agreement)
    put("0412x.standing/01.md", f"# 01\n{M}\n\n## Local work agreement\nA work page records goal, scope, independent Prime choices, Director-required choices, finish conditions and decisions.\n\n## Other\nx\n")
    put("0412x.standing/evidence/director-agreement.md", f"# Director agreement (SYNTHETIC)\n{M}\n\"Anything that requires my judgement or starts conflicting with our design or forking. That is a hard stop.\"\n")
    standing = [{"path": "0412x.standing/01.md", "kind": "heading", "heading": "Local work agreement", "applicability": "standing"},
                {"path": "0412x.standing/evidence/director-agreement.md", "kind": "whole", "applicability": "standing"}]
    dstand = [standing[1]]

    def pack(rel, title, goal, scope, finish, agreement):
        return put(rel, f"# {title}\n{M}\n\n## Goal\n{goal}\n\n## Scope\n{scope}\n\n## Finish\n{finish}\n\n" + (block(agreement) if agreement else "") + "\n## Return pointer\nPENDING.\n\n## Review - Codex Prime\nPENDING.\n")

    A = {"schema": "task-agreement/1",
         "goal": [{"path": "self", "kind": "heading", "heading": "Goal"}],
         "scope": [{"path": "self", "kind": "heading", "heading": "Scope"}],
         "finish_criteria": [{"path": "self", "kind": "heading", "heading": "Finish"}],
         "prime_discretion": standing, "director_required": dstand,
         "recorded_decisions": [{"record": "0599.fixture-task/06.02.decisions.md", "verbatim_cut": "Director - verbatim",
                                 "interpretation_cut": "Prime - exact proposal this reply approves", "answers_cut": "Prime - exact proposal this reply approves",
                                 "answers_scope": "only the cited proposal"}]}
    pa = pack("0599.fixture-task/05.02.md", "05.02 - Fixture bounded task", "Add a parser module with three tests.",
              "Included: new module labs/x. Excluded: app edits. Allowed writes: labs/x, evidence/build05.02.", "Return with tests run and first failures.", A)
    dec_a = put("0599.fixture-task/06.02.decisions.md", f"# 06.02 decisions\n{M}\n\n## Director - verbatim\nSYNTHETIC: Ok pack it\n\n## Prime - exact proposal this reply approves\nBuilder adds the parser module in labs/x only; no app change.\n")

    # b: N7NN hold / reply / successor
    B = dict(A, recorded_decisions=[{"record": "0799.fixture-colab/06.02.decisions.md", "verbatim_cut": "Director - verbatim",
                                      "interpretation_cut": "Prime - interpretation", "answers_cut_record": "0799.fixture-colab/06.01.review.md",
                                      "answers_cut": "Question Q1", "answers_scope": "only the cited question"}])
    pb = pack("0799.fixture-colab/05.01.pack.md", "05.01.pack - Fixture design", "Design two cache options.", "Design only. No code.", "Return both options with a recommendation.", B)
    put("0799.fixture-colab/06.01.review.md", f"# 06.01.review (SYNTHETIC tool-recorded stand-in)\n{M}\n\n## Question Q1\nMay the cache write outside the page evidence folder?\n\n## Holds\nD1 (build the cache) waits for Q1. I1 (docs) continues.\n")
    put("0799.fixture-colab/06.02.decisions.md", f"# 06.02 decisions\n{M}\n\n## Director - verbatim\n#Q1 SYNTHETIC: Yes, but only under the page evidence folder.\n\n## Prime - interpretation\nQ1 is answered for location only; D1 still needs a released pack.\n")

    # c1: absent block; c2: decision changed after binding; c3: scope conflict
    pc1 = pack("0598.fixture-old/05.01.md", "05.01 - Fixture old pack", "Repair the parser.", "Labs only.", "Return tests.", None)
    pc3 = pack("0597.fixture-conflict/05.01.md", "05.01 - Fixture conflict", "Improve review output.", "Included: labs only. Excluded: app edits.", "Return with tests.",
               dict(A, recorded_decisions=[{"record": "0597.fixture-conflict/06.01.decisions.md", "verbatim_cut": "Director - verbatim",
                                            "interpretation_cut": "Prime - exact proposal this reply approves", "answers_cut": "Prime - exact proposal this reply approves",
                                            "answers_scope": "only the cited proposal"}]))
    put("0597.fixture-conflict/06.01.decisions.md", f"# 06.01 decisions\n{M}\n\n## Director - verbatim\nSYNTHETIC: Ok, and change the app entry too.\n\n## Prime - exact proposal this reply approves\nImprove review output in labs.\n")

    def measure(pack_path: Path, ag: dict | None, page_dir: str) -> dict:
        out = {"pack_cut": cut(pack_path, "pack")}
        if not ag:
            out["block"] = "absent"
            return out
        for f in ("goal", "scope", "finish_criteria", "prime_discretion", "director_required"):
            out[f] = [dict(c, measured=cut(pack_path if c["path"] == "self" else FX / c["path"], c["kind"], c.get("heading"))) for c in ag[f]]
        ds = []
        for d in ag["recorded_decisions"]:
            rec = FX / d["record"]
            ans = FX / d.get("answers_cut_record", d["record"])
            ds.append(dict(d, verbatim=cut(rec, "heading", d["verbatim_cut"]), interpretation=cut(rec, "heading", d["interpretation_cut"]),
                           answers=cut(ans, "heading", d["answers_cut"]), distinct_cuts=d["verbatim_cut"] != d["interpretation_cut"]))
        out["recorded_decisions"] = ds
        return out

    views = {}
    views["a"] = {"example": "a bounded authorized task", "measured": measure(pa, A, "0599"),
                  "specified_NOT_RUN": {"states": {"goal": "cited", "scope": "cited", "finish_criteria": "cited", "prime_discretion": "cited", "director_required": "cited", "recorded_decisions": "cited"},
                                        "may_continue": ["record, inspect and publish a review", "Prime operations within the cited scope"],
                                        "must_wait": ["builder execution: still needs the named Director invocation of the pack; 'Ok pack it' approved packaging of the cited proposal only"],
                                        "unknown": []}}
    views["b"] = {"example": "b N7NN hold, reply and successor", "measured": measure(pb, B, "0799"),
                  "specified_NOT_RUN": {"states": {"recorded_decisions": "cited"},
                                        "resolves": ["hold Q1 (location question) only"],
                                        "must_wait": ["D1: execution needs a released pack; the reply does not release it"],
                                        "may_continue": ["I1", "a successor review on the same pass recording Q1 as answered"],
                                        "separation": "the Director verbatim cut and the Prime interpretation cut are distinct and both bound"}}
    views["c1"] = {"example": "c1 old pack without a task-agreement block (like the real 0522/05.13)", "measured": measure(pc1, None, "0598"),
                   "specified_NOT_RUN": {"states": {f: "unknown" for f in ("goal", "scope", "finish_criteria", "prime_discretion", "director_required", "recorded_decisions")},
                                         "report": "agreement block absent (pack predates task-agreement/1); not migrated; not inferred from the headings Goal/Scope/Finish",
                                         "may_continue": ["preliminary review: record, publish, recover"], "must_wait": ["see holds table: complete, finished, release"]}}
    before = measure(pa, A, "0599")
    dec_a.write_bytes(dec_a.read_bytes().replace(b"SYNTHETIC: Ok pack it", b"SYNTHETIC: Ok pack it, but also the app."))
    after = measure(pa, A, "0599")
    dec_a.write_bytes(dec_a.read_bytes().replace(b"SYNTHETIC: Ok pack it, but also the app.", b"SYNTHETIC: Ok pack it"))
    views["c2"] = {"example": "c2 decision record changed after binding", "measured_before": before["recorded_decisions"][0]["verbatim"],
                   "measured_after": after["recorded_decisions"][0]["verbatim"], "restored_for_other_examples": True,
                   "specified_NOT_RUN": {"states": {"recorded_decisions": "stale"}, "keep": "the original binding and its sha", "never": "rebind silently",
                                         "reconciliation_request": {"stale_binding": "0599.fixture-task/06.02.decisions.md#Director - verbatim", "bound_sha256": before["recorded_decisions"][0]["verbatim"].get("sha256"),
                                                                    "observed_sha256": after["recorded_decisions"][0]["verbatim"].get("sha256"), "routed_to": "Director (a changed verbatim Director record is itself a conflict)"},
                                         "must_wait": ["acts depending on that decision"]}}
    views["c3"] = {"example": "c3 scope conflicts with the decision", "measured": measure(pc3, json.loads(re.search(r"```task-agreement\n(.*?)\n```", pc3.read_text(encoding='utf-8'), re.S).group(1)), "0597"),
                   "specified_NOT_RUN": {"states": {"scope": "conflict", "recorded_decisions": "conflict"},
                                         "both_cuts_kept": ["0597.fixture-conflict/05.01.md#Scope ('Excluded: app edits')", "0597.fixture-conflict/06.01.decisions.md#Director - verbatim ('change the app entry too')"],
                                         "routed_to": "Director judgment", "must_wait": ["any app edit"], "may_continue": ["labs-only work inside both cuts"]}}
    # design application to the real batch record (read-only measurement)
    me = WORK / "0707.app-use-check" / "05.13.pack.md"
    r608 = WORK / "0412.prime-review" / "06.08.md"
    app = {"note": "DESIGN APPLICATION, not an active grant mutation. Measured read-only at design time.",
           "binding": {"page": "0707.app-use-check", "pass": "05.13", "pack_cut": cut(me, "pack")},
           "goal": {"cite": "05.13.pack.md#Question / selected evidence", "measured": cut(me, "heading", "Question / selected evidence")},
           "scope": {"cite": "05.13.pack.md#Deliverables / boundaries", "measured": cut(me, "heading", "Deliverables / boundaries")},
           "finish_criteria": {"cite": "05.13.pack.md#Deliverables / boundaries (Return line)", "measured": cut(me, "heading", "Deliverables / boundaries"),
                               "note": "the same cut as scope; a dedicated '## Finish' heading in future packs would separate them"},
           "prime_discretion": {"cite": "0412.prime-review/01.md#Local work agreement (standing)", "measured": cut(WORK / "0412.prime-review" / "01.md", "heading", "Local work agreement")},
           "director_required": {"cite": "0412.prime-review/evidence/director-agreement.md (whole, standing)", "measured": cut(WORK / "0412.prime-review/evidence/director-agreement.md", "whole")},
           "recorded_decisions": [{"record": "0412.prime-review/06.08.md", "verbatim": cut(r608, "heading", "Director - verbatim"),
                                   "interpretation_and_answers": cut(r608, "heading", "Prime - exact proposal this reply approves"),
                                   "answers_scope": "only the cited proposal ('Claude designs explicit source-bound task-agreement references ... without production code or invented authority')"}],
           "specified_NOT_RUN": {"states": "all cited", "may_continue": ["this design return"], "must_wait": ["any production build: not covered by 'Ok pack it' for this item"]}}
    views["application-0412-06.08"] = app
    problems = []
    for k, v in views.items():
        (VIEWS / f"{k}.json").write_text(json.dumps(v, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
        flat = json.dumps(v)
        if k in ("a", "b", "c3", "application-0412-06.08") and '"resolved": false' in flat:
            problems.append(f"{k}: an expected-resolvable cut did not resolve")
    if views["c2"]["measured_before"].get("sha256") == views["c2"]["measured_after"].get("sha256"):
        problems.append("c2: the change was not observed")
    for p in sorted((HERE / "examples" / "fixture").rglob("*")):
        if p.is_file() and "SYNTHETIC" not in p.read_text(encoding="utf-8"):
            problems.append(f"{p.name}: no SYNTHETIC marker")
    (VIEWS / "check.json").write_text(json.dumps({"proves": "fixture validity and measured cuts only; no target behavior", "problems": problems}, indent=1) + "\n", encoding="utf-8")
    print("views", len(views), "problems", problems)
    return 0 if not problems else 1


if __name__ == "__main__":
    sys.exit(main())
