#!/usr/bin/env python3
"""Investigation I, control C5b (0707/05.19). NONPRODUCTION.
C5 (inv1-run02) showed 0522/05.14 declares the STAGED production v8 declaration and pass04 as artifacts, so a root
holding the lab adapter at those paths measures artifact-hash-mismatch. C5b puts the live production bytes at those
paths (as evidence only) and records through the FAITHFUL pass03 baseline (n7compat2 --repo-root, no patch),
which does not execute pass04; for N5 it parses exactly as v8 (05.17/05.18 parity).
usage: inv1_c5b.py --room NEW-DIR --out FILE
"""

import argparse
import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
import lcd  # noqa: E402
from lcd import rie  # noqa: E402

sys.path.insert(0, str(lcd.LIVE / "labs/review-entry-integration-pass01"))
import lifecycle  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--room", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    root, _ = lcd.make_root(Path(a.room), ["n5-0522-0514"], dispatcher="v7")
    root = root.path
    for rel in ("labs/workbook-review-pass04/workbook.py", "app/review-loop-v8.json", "app/review_loop_tools_v8.py"):
        (root / rel).write_bytes((lcd.LIVE / rel).read_bytes())          # production bytes as EVIDENCE
    jf = Path(a.room) / "lab-judgment.json"
    jf.write_text(json.dumps(lifecycle.JUDGMENT, indent=1) + "\n", encoding="utf-8")
    p = rie.baseline(root, *lcd.args(root, "n5-0522-0514", "prepare"))
    iid = lcd.body(p).get("intake_id")
    rec = rie.baseline(root, *lcd.args(root, "n5-0522-0514", "record", "--intake", iid or "none", "--judgment", str(jf)))
    out = {"measurement": lcd.body(p).get("measurement"), "codes": lcd.codes(p), "book_sources": lcd.book_sources(p),
           "record_exit": rec["exit"], "mode": lcd.body(rec).get("mode"), "review_id": lcd.body(rec).get("review_id"),
           "correction": lcd.body(rec).get("correction")}
    out["as_predicted"] = out["measurement"] == "complete" and out["record_exit"] == 0 and out["mode"] == "preliminary"
    Path(a.out).write_text(json.dumps({"schema": "lcd-inv1-c5b/1", "room": a.room, "result": out}, indent=1) + "\n", encoding="utf-8")
    print(json.dumps(out))
    return 0 if out["as_predicted"] else 1


if __name__ == "__main__":
    sys.exit(main())
