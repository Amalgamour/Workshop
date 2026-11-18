#!/usr/bin/env python3
"""Per-case reconciliation: 05.21 harness (pass01) results versus successor (pass02) results, per baseline candidate.
NONPRODUCTION. Each case is classified against the successor expectations DECLARED HERE BEFORE the run (06.22 notes):
  unchanged | revised-H1 (stub -> real callback; blocked either way in the suite) | revised-H3 (strict reason required)
  | revised-#04 (same-.NN destination added) | new | UNEXPECTED (any verdict that differs from the declared expectation)
usage: reconcile.py --old OLD.json --new NEW.json --kind proto-l|staged-g --out FILE
exit 0 only when there is no UNEXPECTED row.
"""

import argparse
import json
import sys
from pathlib import Path

REVISED = {"CAP-4": "revised-H1", "RP-1": "revised-H1", "RP-2": "revised-H1", "IN-2": "revised-H1",
           "ST-1": "revised-H3", "ST-2": "revised-H3", "ST-3": "revised-H3", "LR-6": "revised-#04"}
NEW = {"ST-4", "N7-3"}
# successor expectations declared before the run; unlisted cases are expected to keep their 05.21 verdict
EXPECT = {
    "proto-l": {"ST-1": "fail", "ST-2": "fail", "ST-3": "fail", "ST-4": "pass", "N7-3": "fail", "LR-6": "pass",
                "CAP-4": "blocked", "RP-1": "blocked", "RP-2": "blocked", "IN-2": "blocked"},
    "staged-g": {"ST-1": "pass", "ST-2": "pass", "ST-3": "pass", "ST-4": "pass", "N7-3": "fail", "LR-6": "fail",
                 "CAP-4": "blocked", "RP-1": "blocked", "RP-2": "blocked", "IN-2": "blocked"},
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--old", required=True)
    ap.add_argument("--new", required=True)
    ap.add_argument("--kind", required=True, choices=("proto-l", "staged-g"))
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    old = {r["id"]: r["verdict"] for r in json.loads(Path(a.old).read_text(encoding="utf-8"))["records"]}
    new_doc = json.loads(Path(a.new).read_text(encoding="utf-8"))
    new = {r["id"]: r["verdict"] for r in new_doc["records"]}
    rows = []
    for cid in list(new) + [c for c in old if c not in new]:
        o, n = old.get(cid), new.get(cid)
        want = EXPECT[a.kind].get(cid, o)
        cls = "new" if cid in NEW else REVISED.get(cid, "unchanged")
        if n != want:
            cls = "UNEXPECTED"
        rows.append({"id": cid, "pass01": o, "successor": n, "declared_expectation": want, "class": cls})
    bad = [r for r in rows if r["class"] == "UNEXPECTED"]
    doc = {"schema": "harness-reconcile/1", "kind": a.kind, "old": a.old, "new": a.new, "rows": rows, "unexpected": bad,
           "successor_ready": new_doc.get("ready"), "successor_counts": new_doc.get("aggregate", {}).get("counts")}
    Path(a.out).write_text(json.dumps(doc, indent=1) + "\n", encoding="utf-8")
    for r in rows:
        if r["class"] != "unchanged":
            print(f"{r['class']:12} {r['id']:7} pass01={r['pass01']!s:26} successor={r['successor']!s:26} expected={r['declared_expectation']}")
    print(f"{len(rows)} rows; unchanged {sum(r['class'] == 'unchanged' for r in rows)}; UNEXPECTED {len(bad)}")
    return 0 if not bad else 1


if __name__ == "__main__":
    sys.exit(main())
