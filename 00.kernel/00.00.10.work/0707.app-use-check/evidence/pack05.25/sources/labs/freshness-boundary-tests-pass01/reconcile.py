#!/usr/bin/env python3
"""Reconcile observed verdicts with the expectations PREDECLARED in 06.23.notes.md (before any test code ran).
NONPRODUCTION. Classes: expected-pass | expected-baseline-failure | blocked/deferred as declared |
DIFFERS-FROM-PREDICTION (kept and explained, never edited to match).
F1b was added after smoke-02 (F1 could not reach record on proto-l); its expectation is marked 'declared after smoke'.
usage: reconcile.py --result RES.json --kind proto-l|staged-g --out FILE   (exit 0 only if nothing differs)
"""

import argparse
import json
import sys
from pathlib import Path

PRE = {
    "proto-l": {"M0": "pass", "M1": "fail", "M2": "fail", "M3": "fail", "M4": "pass", "M5": "pass",
                "R0": "pass", "R1": "pass", "R2": "pass", "R3": "pass", "R4": "pass", "F1": "fail", "F2": "fail", "F3": "fail",
                "F4": "observe", "F5": "fail", "F6": "pass", "F7a": "pass", "F7b": "pass", "E1": "fail", "E2": "fail", "E3": "pass",
                "C1": "fail", "C2": "pass", "C3": "pass", "C4": "blocked", "D1": "deferred"},
    "staged-g": {"M0": "pass", "M1": "fail", "M2": "fail", "M3": "fail", "M4": "pass", "M5": "pass",
                 "R0": "fail", "R1": "pass", "R2": "pass", "R3": "pass", "R4": "pass", "F1": "pass", "F2": "pass", "F3": "pass",
                 "F4": "observe", "F5": "pass", "F6": "pass", "F7a": "fail", "F7b": "pass", "E1": "pass", "E2": "pass", "E3": "pass",
                 "C1": "fail", "C2": "fail", "C3": "pass", "C4": "blocked", "D1": "deferred"},
}
LATE = {"proto-l": {"F1b": "fail"}, "staged-g": {"F1b": "observe"}}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--result", required=True)
    ap.add_argument("--kind", required=True, choices=tuple(PRE))
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    res = json.loads(Path(a.result).read_text(encoding="utf-8"))
    rows = []
    for r in res["records"]:
        key = r["id"].split("-")[0] if r["id"].startswith("M") else r["id"]
        late = key in LATE[a.kind]
        want = LATE[a.kind][key] if late else PRE[a.kind].get(key, "?")
        got = r["verdict"]
        if want == "observe":
            cls = "observed (no prediction)"
        elif got == want:
            cls = {"pass": "expected-pass", "fail": "expected-baseline-failure"}.get(got, f"{got} as declared")
        else:
            cls = "DIFFERS-FROM-PREDICTION"
        rows.append({"id": r["id"], "predicted": want, "prediction_time": "after smoke-02" if late else "before code (06.23 notes)",
                     "observed": got, "class": cls, "reasons": r.get("reasons")})
    differs = [x for x in rows if x["class"] == "DIFFERS-FROM-PREDICTION"]
    Path(a.out).write_text(json.dumps({"schema": "fbt-reconcile/1", "kind": a.kind, "rows": rows, "differs": differs}, indent=1) + "\n", encoding="utf-8")
    for x in rows:
        print(f"{x['class']:28} {x['id']:6} predicted={x['predicted']:9} observed={x['observed']}")
    print(f"{len(rows)} rows; differs {len(differs)}")
    return 0 if not differs else 1


if __name__ == "__main__":
    sys.exit(main())
