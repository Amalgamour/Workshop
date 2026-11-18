#!/usr/bin/env python3
"""#06 rollback rehearsal on candidate roots (0707/05.18). NONPRODUCTION.

For an N7 root (0515, no 06.15.review.md) and an N5 root (0512, synthetic PENDING review section):
  v8 selected: prepare -> record -> publish                      (v8-created records)
  ROLLBACK: select v7 (live dispatcher bytes); v8 files stay on disk, inert
  v7: read -> recover -> inspect -> prepare                       (how v8 records appear under v7)
  v7: a NEW record attempt                                        (does v7 overwrite / upgrade v8 ids?)
  RE-SELECT v8: read -> recover                                   (round trip)
Every record file is hashed before and after the rollback steps; the review ids are compared.
usage: rollback.py --rooms NEW-DIR --out FILE
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
import rie  # noqa: E402
import lifecycle  # noqa: E402


def b(res):
    return res.get("body") if isinstance(res.get("body"), dict) else {}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--rooms", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    rooms = Path(a.rooms)
    rie.refuse_inside(rooms)
    rooms.mkdir(parents=True, exist_ok=False)
    out = {"schema": "rie-rollback/1", "rooms": str(rooms), "roots": {}}
    for rid_, key, omit, synth in (("R-N7", "n7-0515", ("06.15.review.md",), None), ("R-N5", "n5-0512", (), "pending-review")):
        root, info = rie.make_root(rooms / rid_, key, omit=omit, dispatcher="v8")
        root = root.path
        fx = rie.FIXTURES[key]
        if synth:
            pf = root / rie.BOOK_REL / fx["page"] / fx["pointer"]
            pf.write_text(pf.read_text(encoding="utf-8").split("## Review - Codex Prime", 1)[0] + "## Review - Codex Prime\nPENDING.\n", encoding="utf-8")
        ev = rooms / f"{rid_}-evidence"
        steps = {}

        def go(name, *args):
            res = rie.app(root, *rie.wb_args(root, key, *args))
            rie.save(res, ev, name)
            bb = b(res)
            steps[name] = {"selected": "v8" if rie.sha_file(root / "app/librarian.py") == rie.sha_file(rie.CAND / "app/librarian.py") else "v7",
                           "exit": res["exit"], **{k: bb.get(k) for k in ("intake_id", "stored_intake_id", "live_intake_id", "review_id", "measurement", "stale",
                                                                            "correction", "recorded", "published", "mode", "state") if k in bb},
                           "finding_codes": sorted({f.get("code") for f in bb.get("findings") or [] if isinstance(f, dict)}), "stderr": res["stderr"][-240:]}
            print(rid_, name, json.dumps(steps[name])[:260])
            return res, bb

        _, p = go("v8-prepare", "prepare")
        jf = ev / "judgment.json"
        jf.write_text(json.dumps(lifecycle.JUDGMENT, indent=1) + "\n", encoding="utf-8")
        _, rec = go("v8-record", "record", "--intake", p.get("intake_id"), "--judgment", str(jf))
        go("v8-publish", "publish", "--review", rec.get("review_id") or "none")
        v8_review = rec.get("review_id")
        records_v8 = rie.tree_hashes(root)
        rie.select(root, "v7")                                  # ROLLBACK: the one selection file
        go("v7-read", "read")
        go("v7-recover", "recover")
        go("v7-inspect", "inspect")
        _, p7 = go("v7-prepare", "prepare")
        _, rec7 = go("v7-record", "record", "--intake", p7.get("intake_id") or "none", "--judgment", str(jf))
        records_after_v7 = rie.tree_hashes(root)
        rie.select(root, "v8")                                  # re-select
        go("v8-read-again", "read")
        go("v8-recover-again", "recover")
        changed = sorted(k for k in records_v8 if records_after_v7.get(k) != records_v8[k])
        added = sorted(set(records_after_v7) - set(records_v8))
        store = sorted(k for k in records_after_v7 if k.startswith("workbook-review/"))
        out["roots"][rid_] = {"fixture": key, "omit": list(omit), "synthetic": synth, "v8_review_id": v8_review, "v7_record_review_id": rec7.get("review_id"),
                              "v8_files_changed_by_v7_steps": changed, "files_added_by_v7_steps": added, "record_store": store, "steps": steps}
    Path(a.out).write_text(json.dumps(out, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
