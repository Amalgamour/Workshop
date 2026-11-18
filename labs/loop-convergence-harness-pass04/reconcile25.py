#!/usr/bin/env python3
"""Per-case reconciliation of successor verdicts against an OLD result (0707/05.25). NONPRODUCTION.
Each differing case must be in the INTENDED set (declared here before the runs, from 06.24.review / 06.40); any other
difference is UNEXPECTED. usage: reconcile25.py --old OLD.json --new NEW.json --label L --out FILE  (exit 0 iff none unexpected)"""

import argparse
import json
import sys
from pathlib import Path

INTENDED = {   # cases whose fixture/target contract changed in pass04; a changed verdict there is explained, not silent
    "N5-1": "v7 closure installed; successful baseline required", "N5-2": "same", "N5-3": "same",
    "PR-7": "declared workbook after a successful control", "CTX-1": "explicit build_intake hook / successful observations",
    "RC-1": "declared builder --root with side-effect detection",
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--old", required=True)
    ap.add_argument("--new", required=True)
    ap.add_argument("--label", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    o = {r["id"]: r["verdict"] for r in json.loads(Path(a.old).read_text(encoding="utf-8"))["records"]}
    n = {r["id"]: r["verdict"] for r in json.loads(Path(a.new).read_text(encoding="utf-8"))["records"]}
    rows = []
    for cid, v in n.items():
        if cid not in o:
            cls = "new (not in old run)"
        elif o[cid] == v:
            cls = "same"
        else:
            cls = f"changed: intended ({INTENDED[cid]})" if cid in INTENDED else "UNEXPECTED"
        rows.append({"id": cid, "old": o.get(cid), "new": v, "class": cls})
    bad = [r for r in rows if r["class"] == "UNEXPECTED"]
    Path(a.out).write_text(json.dumps({"schema": "reconcile25/1", "label": a.label, "old": a.old, "new": a.new, "rows": rows, "unexpected": bad}, indent=1) + "\n", encoding="utf-8")
    for r in rows:
        if r["class"] != "same":
            print(f"{r['class'][:60]:60} {r['id']:7} old={r['old']!s:28} new={r['new']}")
    print(f"{a.label}: {len(rows)} rows; same {sum(r['class'] == 'same' for r in rows)}; unexpected {len(bad)}")
    return 0 if not bad else 1


if __name__ == "__main__":
    sys.exit(main())
