#!/usr/bin/env python3
"""Callback PROBE (0707/05.22). NONPRODUCTION. Runs named harness callbacks against a REAL baseline candidate even
though their dependencies are pending, to show the callbacks execute actual candidate commands and judge the
baseline's real behavior. A probe is NEVER readiness: it bypasses the dependency gate, its records carry
mode 'probe', and it always exits 1. In the suite, the same cases stay 'blocked' until Prime accepts K/R/I.
usage: probe.py --candidate DIR --inputs INPUTS.json --rooms NEW-DIR --out FILE --cases CAP-4,RP-1,RP-2,IN-2
"""

import argparse
import json
import sys
import traceback
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import harness  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--candidate", required=True)
    ap.add_argument("--inputs", required=True)
    ap.add_argument("--rooms", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--cases", required=True)
    a = ap.parse_args()
    inputs = json.loads(Path(a.inputs).read_text(encoding="utf-8"))
    harness.validate(inputs, Path(a.candidate))
    rooms = Path(a.rooms)
    harness.rie.refuse_inside(rooms)
    rooms.mkdir(parents=True, exist_ok=False)
    ctx = harness.Ctx(Path(a.candidate), inputs, rooms)
    by = {c["id"]: c for c in harness.CASES}
    recs = []
    for cid in a.cases.split(","):
        c = by[cid]
        r = {"id": cid, "mode": "probe", "readiness": "not assessed: dependency gate bypassed; never readiness",
             "needs": c["needs"], "candidate_kind": inputs["candidate"]["kind"], "requirement": c["requirement"]}
        try:
            e, o, v = c["fn"](ctx)
            r.update({"expected": e, "observed": o, "verdict": v})
        except Exception as exc:
            r.update({"verdict": "error", "observed": f"{exc.__class__.__name__}: {exc}"[:500], "trace": traceback.format_exc()[-1500:]})
        recs.append(r)
        print(f"PROBE {r['verdict']:6} {cid:6} reasons: {(r.get('observed') or {}).get('judge_reasons') if isinstance(r.get('observed'), dict) else r.get('observed')}")
    Path(a.out).write_text(json.dumps({"schema": "harness-probe/1", "candidate": a.candidate, "records": recs}, indent=1, default=str) + "\n", encoding="utf-8")
    return 1


if __name__ == "__main__":
    sys.exit(main())
