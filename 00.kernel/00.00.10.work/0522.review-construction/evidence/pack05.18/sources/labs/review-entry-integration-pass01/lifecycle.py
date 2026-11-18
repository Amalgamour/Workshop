#!/usr/bin/env python3
"""#04 review lifecycle on copies through the REAL v8 entry (0707/05.18). NONPRODUCTION.

Per fixture root (v8 dispatcher selected), each a NEW process:
  prepare -> form -> record (synthetic LAB-ONLY judgment) -> inspect (full text saved for reading)
  -> SEPARATE publish -> read -> recover -> read -> recover (idempotence: outputs equal, no writes)
  -> STALE: a material change to the declared submission bytes -> read -> recover -> publish attempt
  -> RE-RECORD on the changed source: prepare -> record; every earlier record file must stay byte-identical.
Variants:
  L1 n5-0512 as is (its page already carries a published v7 workbook review wbf38837cf0fa9c6b)
  L2 n5-0512 SYNTHETIC: the copied page's Review section replaced by 'PENDING.' (labelled; publish path)
  L3 n7-0515 with Prime's manual 06.15.review.md (must be preserved; publication held)
  L4 n7-0515 without 06.15.review.md (absent destination: existing preliminary fallback)
usage: lifecycle.py --rooms NEW-DIR --out FILE [--only L1 ...]
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
import rie  # noqa: E402

JUDGMENT = {
    "finding": "LAB-ONLY SYNTHETIC judgment for the 0707/05.18 integration lab; not a review of the source pass.",
    "reasons": ["LAB-ONLY: exercises record, inspect, publish, read and recover through the real v8 entry on a disposable copy."],
    "operation": "continue", "disposition": "held", "pass_terminal": "open", "goal_terminal": "open",
    "next_action": "LAB-ONLY: no real action; Prime reviews the 0707/05.18 integration handoff.",
    "semantic_conflict": None, "design_fork": None, "findings": [], "holds": [], "answers": [], "review_passes": [],
    "gaps": ["LAB-ONLY: synthetic judgment, not independent review"],
    "sections": {k: None for k in ("affected", "assumptions", "consequences", "exploration", "finish_assessments", "for_model", "issue", "learning",
                                   "limits", "open_questions", "options", "outcome_evidence", "preservation", "proposed_plan", "question",
                                   "recommendation", "remaining_choices", "within_direction")}
    | {"findings_account": [], "next_bounded_action": "LAB-ONLY: none.", "prime_finding": "LAB-ONLY synthetic.", "return_result": "LAB-ONLY synthetic.",
       "tests_note": "LAB-ONLY: no tests judged.", "tests_passed": None},
}
VARIANTS = {"L1": ("n5-0512", (), None), "L2": ("n5-0512", (), "pending-review"), "L3": ("n7-0515", (), None), "L4": ("n7-0515", ("06.15.review.md",), None)}


def body(res):
    return res.get("body") if isinstance(res.get("body"), dict) else {}


def pick(b, *keys):
    return {k: b.get(k) for k in keys if k in b}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--rooms", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--only", action="append")
    a = ap.parse_args()
    rooms = Path(a.rooms)
    rie.refuse_inside(rooms)
    rooms.mkdir(parents=True, exist_ok=False)
    result = {"schema": "rie-lifecycle/1", "rooms": str(rooms), "variants": {}}
    for vid in a.only or list(VARIANTS):
        key, omit, synth = VARIANTS[vid]
        root = rooms / vid
        _, info = rie.make_root(root, key, omit=omit, dispatcher="v8")
        fx = rie.FIXTURES[key]
        page = root / rie.BOOK_REL / fx["page"]
        if synth == "pending-review":
            pf = page / fx["pointer"]
            text = pf.read_text(encoding="utf-8")
            head = text.split("## Review - Codex Prime", 1)[0]
            pf.write_text(head + "## Review - Codex Prime\nPENDING.\n", encoding="utf-8")
        ev = rooms / f"{vid}-evidence"
        steps, log = {}, []
        protected = {p: rie.sha_file(page / p) for p in ("06.15.review.md",) if (page / p).exists()}
        src_before = rie.sha_file(page / fx["pointer"])

        def go(name, args, keep=()):
            res = rie.app(root, *args)
            rie.save(res, ev, name)
            b = body(res)
            steps[name] = {"exit": res["exit"], **pick(b, "intake_id", "live_intake_id", "stored_intake_id", "review_id", "measurement", "stale", "state",
                                                          "custody", "destination", "next_action", "publication_complete", "correction", "mode",
                                                          "judgment_recorded", "accepted", "approved", "closes_work", "releases_action", *keep),
                           "finding_codes": sorted({f.get("code") for f in b.get("findings") or [] if isinstance(f, dict)}),
                           "stderr_tail": res["stderr"][-300:]}
            log.append(f"{vid} {name:16} exit {res['exit']} " + json.dumps({k: v for k, v in steps[name].items() if k in ("intake_id", "review_id", "measurement", "stale", "correction", "state", "publication_complete")})[:220])
            print(log[-1])
            return res, b

        _, p = go("prepare", rie.wb_args(root, key, "prepare"))
        iid = p.get("intake_id")
        go("form", rie.wb_args(root, key, "form"))
        jf = ev / "judgment.json"
        jf.write_text(json.dumps(JUDGMENT, indent=1) + "\n", encoding="utf-8")
        _, rec = go("record", rie.wb_args(root, key, "record", "--intake", iid, "--judgment", str(jf)))
        rid = rec.get("review_id")
        ins_res, ins = go("inspect", rie.wb_args(root, key, "inspect"))
        (ev / "inspect.full-read.txt").write_text(ins_res["stdout"], encoding="utf-8")
        records_after_record = rie.tree_hashes(root)
        go("publish", rie.wb_args(root, key, "publish", "--review", rid or "none"))
        t0 = rie.tree_hashes(root)
        r1, _ = go("read", rie.wb_args(root, key, "read"))
        c1, _ = go("recover", rie.wb_args(root, key, "recover"))
        r2, _ = go("read-again", rie.wb_args(root, key, "read"))
        c2, _ = go("recover-again", rie.wb_args(root, key, "recover"))
        t1 = rie.tree_hashes(root)
        idempotent = {"read_equal": r1["stdout"] == r2["stdout"], "recover_equal": c1["stdout"] == c2["stdout"], "no_writes": t0 == t1}
        # STALE: material change to the declared submission bytes (LAB fault injection)
        sub = root / info["declared"]["Submission"][0]
        sub.write_bytes(sub.read_bytes() + b"\nLAB-ONLY material change after read (0707/05.18 stale test).\n")
        go("stale-read", rie.wb_args(root, key, "read"))
        go("stale-recover", rie.wb_args(root, key, "recover"))
        go("stale-publish", rie.wb_args(root, key, "publish", "--review", rid or "none"))
        t2 = rie.tree_hashes(root)
        _, p2 = go("rerecord-prepare", rie.wb_args(root, key, "prepare"))
        jf2 = ev / "judgment2.json"
        jf2.write_text(json.dumps(JUDGMENT, indent=1) + "\n", encoding="utf-8")
        _, rec2 = go("rerecord", rie.wb_args(root, key, "record", "--intake", p2.get("intake_id") or "none", "--judgment", str(jf2)))
        t3 = rie.tree_hashes(root)
        kept = {k: v for k, v in t2.items() if k in records_after_record and not k.endswith(Path(sub).name)}
        earlier_preserved = all(t3.get(k) == v for k, v in kept.items())
        new_files = sorted(set(t3) - set(t2))
        result["variants"][vid] = {
            "fixture": key, "omit": list(omit), "synthetic": synth, "root": str(root), "steps": steps, "review_id": rid,
            "idempotent": idempotent, "protected_review_preserved": {p: rie.sha_file(page / p) == h for p, h in protected.items()},
            "pointer_page_changed_by_publish": rie.sha_file(page / fx["pointer"]) != src_before,
            "files_written_by_record": sorted(set(records_after_record) - set(rie.tree_hashes(root).keys() and records_after_record) ),
            "files_added_by_publish": sorted(set(t0) - set(records_after_record)),
            "changed_by_publish": sorted(k for k in records_after_record if k in t0 and t0[k] != records_after_record[k]),
            "earlier_records_preserved_after_rerecord": earlier_preserved, "files_added_by_rerecord": new_files,
            "second_review_id": rec2.get("review_id"), "log": log}
        print(vid, json.dumps({k: result["variants"][vid][k] for k in ("idempotent", "protected_review_preserved", "pointer_page_changed_by_publish",
                                                                       "earlier_records_preserved_after_rerecord", "second_review_id")}))
    Path(a.out).write_text(json.dumps(result, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
