#!/usr/bin/env python3
"""Reconcile adapter-run verdicts with the OLD verdicts of the same baseline (0707/05.24). NONPRODUCTION.
The adapters change identity only, so every case run here must keep its old verdict exactly:
  freshness: evidence/design05.23/run-<kind>-01.json   convergence: evidence/design05.22/harness-<kind>-run01.json
usage: reconcile24.py --kind proto-l|staged-g --fbt NEW.json --h3 NEW.json --out FILE   (exit 0 only if all equal)"""

import argparse
import json
import sys
from pathlib import Path

LIVE = Path(r"D:\Git\lib-build")
EV = LIVE / "00.kernel/00.00.10.work/0707.app-use-check/evidence"


def verdicts(p):
    return {r["id"]: r["verdict"] for r in json.loads(Path(p).read_text(encoding="utf-8"))["records"]}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--kind", required=True)
    ap.add_argument("--fbt", required=True)
    ap.add_argument("--h3", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    rows = []
    for name, new, old in (("freshness", a.fbt, EV / f"design05.23/run-{a.kind}-01.json"), ("convergence", a.h3, EV / f"design05.22/harness-{a.kind}-run01.json")):
        n, o = verdicts(new), verdicts(old)
        for cid, v in n.items():
            rows.append({"suite": name, "id": cid, "old": o.get(cid), "new": v, "equal": o.get(cid) == v})
    bad = [r for r in rows if not r["equal"]]
    Path(a.out).write_text(json.dumps({"schema": "reconcile24/1", "kind": a.kind, "rows": rows, "differs": bad}, indent=1) + "\n", encoding="utf-8")
    for r in rows:
        print(f"{'same' if r['equal'] else 'DIFF'} {r['suite']:11} {r['id']:7} old={r['old']!s:26} new={r['new']}")
    print(f"{len(rows)} rows; differs {len(bad)}")
    return 0 if not bad else 1


if __name__ == "__main__":
    sys.exit(main())
