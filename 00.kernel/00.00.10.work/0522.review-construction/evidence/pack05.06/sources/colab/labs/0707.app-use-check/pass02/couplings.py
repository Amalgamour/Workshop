#!/usr/bin/env python3
"""0707 pass02 P4: check SYNTHETIC disposition fixtures against the CURRENT cycle rules.

Imports the pinned prime_cycle.py (hash-checked against pack05.02, main not run)
and calls its own check_judgment. Writes only evidence/build05.02/probes/couplings.json.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
from copy import deepcopy
from pathlib import Path

sys.dont_write_bytecode = True
CHECKOUT = Path(r"D:\Git\lib-build")
PAGE = CHECKOUT / "00.kernel" / "00.00.10.work" / "0707.app-use-check"
OUT = PAGE / "evidence" / "build05.02" / "probes" / "couplings.json"
LAB = Path(__file__).resolve().parent
CYCLE = CHECKOUT / "labs" / "prime-cycle-pass03" / "prime_cycle.py"


def main() -> int:
    pins = {r["path"]: r for r in json.loads((PAGE / "evidence/pack05.02/source-manifest.json").read_text(encoding="utf-8"))["files"]}
    data = CYCLE.read_bytes()
    pin = pins["labs/prime-cycle-pass03/prime_cycle.py"]
    if hashlib.sha256(data).hexdigest() != pin["sha256"] or len(data) != pin["bytes"]:
        raise SystemExit("prime_cycle.py does not match pack05.02")
    spec = importlib.util.spec_from_file_location("pinned_prime_cycle", CYCLE)
    cycle = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(cycle)

    fixtures = json.loads((LAB / "fixtures" / "dispositions.json").read_text(encoding="utf-8"))
    reg = fixtures["registration_goal"]
    base = fixtures["base_judgment"]
    base["goal"]["goal_sha256"] = cycle.goal_sha(reg["goal"])
    rows = []
    for case in fixtures["cases"]:
        judgment = deepcopy(base)
        for key, value in case["set"].items():
            if key.startswith("goal."):
                judgment["goal"][key[5:]] = value
            else:
                judgment[key] = value
        try:
            cycle.check_judgment(judgment, reg)
            verdict, rule = "accepted-by-cycle", None
        except cycle.Refusal as exc:
            verdict, rule = "refused-by-cycle", exc.message
        rows.append({"id": case["id"], "expect": case["expect"], "observed": verdict, "rule": rule,
                     "as_expected": verdict == case["expect"], "set": case["set"]})
    body = {"schema": "0707-coupling-probe/1", "cycle_sha256": pin["sha256"], "rows": rows,
            "all_as_expected": all(r["as_expected"] for r in rows)}
    OUT.write_bytes((json.dumps(body, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8"))
    for r in rows:
        print(r["id"], r["observed"], r["rule"] or "", "OK" if r["as_expected"] else "UNEXPECTED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
