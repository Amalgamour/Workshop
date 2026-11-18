#!/usr/bin/env python3
"""Harness-hostile demonstrations (0707/05.21). NONPRODUCTION. Each runs harness.py as a NEW process and records its exit.
HX-1 the combined candidate (inputs-combined.json, candidate PENDING; K/I/R/W pending)  -> NOT READY, exit 1, every case blocked
HX-2 a candidate file tampered after its identity was declared                            -> refused before execution, exit 2
HX-3 a PENDING dependency row that carries a guessed pin                                   -> refused, exit 2
HX-4 an 'accepted' dependency row whose declared hash does not match the frozen file        -> refused, exit 2
HX-5 aggregation unit tests (test_verdict.py)                                              -> 16/16, exit 0
HX-6 a suite with only some groups selected never reports more than it ran (proto-l, 'capacity' only) -> NOT READY
usage: demo_hostile.py --candidate DIR --inputs INPUTS.json --rooms NEW-DIR --out FILE
"""

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent


def run(argv, cwd=None):
    p = subprocess.run([sys.executable, "-B", *map(str, argv)], capture_output=True, text=True, cwd=cwd)
    return {"argv": [str(x) for x in argv], "exit": p.returncode, "stdout_tail": p.stdout[-1500:], "stderr_tail": p.stderr[-600:]}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--candidate", required=True)
    ap.add_argument("--inputs", required=True)
    ap.add_argument("--rooms", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    rooms = Path(a.rooms)
    rooms.mkdir(parents=True, exist_ok=False)
    H = HERE / "harness.py"
    base = json.loads(Path(a.inputs).read_text(encoding="utf-8"))
    out = {}

    r = run([H, "--inputs", HERE / "inputs/inputs-combined.json", "--rooms", rooms / "HX-1", "--out", rooms / "HX-1.json"])
    res = json.loads((rooms / "HX-1.json").read_text(encoding="utf-8"))
    out["HX-1"] = {"expected": "exit 1, not ready, all blocked", "exit": r["exit"], "ready": res.get("ready"),
                   "verdicts": sorted({x["verdict"] for x in res.get("records", [])}), "ok": r["exit"] == 1 and res.get("ready") is False
                   and {x["verdict"] for x in res.get("records", [])} == {"blocked"}}

    tam = rooms / "HX-2-candidate"
    shutil.copytree(a.candidate, tam)
    f = tam / "app/review_loop_tools_v8.py"
    f.write_bytes(f.read_bytes() + b"\n# tampered after identity\n")
    r = run([H, "--candidate", tam, "--inputs", a.inputs, "--rooms", rooms / "HX-2", "--out", rooms / "HX-2.json"])
    out["HX-2"] = {"expected": "exit 2, refused, no rooms", "exit": r["exit"], "stdout": r["stdout_tail"][-200:], "rooms_created": (rooms / "HX-2").exists(),
                   "ok": r["exit"] == 2 and not (rooms / "HX-2").exists()}

    bad = json.loads(json.dumps(base))
    next(d for d in bad["dependencies"] if d["id"] == "K")["files"] = [{"path": "labs/review-source-capacity-pass02/prime_review.py", "sha256": "0" * 64, "bytes": 1}]
    p3 = rooms / "HX-3-inputs.json"
    p3.write_text(json.dumps(bad, indent=1), encoding="utf-8")
    r = run([H, "--candidate", a.candidate, "--inputs", p3, "--rooms", rooms / "HX-3", "--out", rooms / "HX-3.json"])
    out["HX-3"] = {"expected": "exit 2 (pending row with a guessed pin)", "exit": r["exit"], "stdout": r["stdout_tail"][-200:], "ok": r["exit"] == 2}

    bad = json.loads(json.dumps(base))
    next(d for d in bad["dependencies"] if d["id"] == "G")["files"][0]["sha256"] = "f" * 64
    p4 = rooms / "HX-4-inputs.json"
    p4.write_text(json.dumps(bad, indent=1), encoding="utf-8")
    r = run([H, "--candidate", a.candidate, "--inputs", p4, "--rooms", rooms / "HX-4", "--out", rooms / "HX-4.json"])
    out["HX-4"] = {"expected": "exit 2 (accepted row does not match frozen bytes)", "exit": r["exit"], "stdout": r["stdout_tail"][-200:], "ok": r["exit"] == 2}

    r = run([HERE / "test_verdict.py"])
    out["HX-5"] = {"expected": "16 unit tests pass, exit 0", "exit": r["exit"], "tail": r["stderr_tail"][-200:], "ok": r["exit"] == 0}

    r = run([H, "--candidate", a.candidate, "--inputs", a.inputs, "--rooms", rooms / "HX-6", "--out", rooms / "HX-6.json", "--suite", "capacity"])
    res = json.loads((rooms / "HX-6.json").read_text(encoding="utf-8"))
    out["HX-6"] = {"expected": "capacity-only suite: exit 1, not ready", "exit": r["exit"], "ready": res.get("ready"), "records": len(res.get("records", [])),
                   "ok": r["exit"] == 1 and res.get("ready") is False}

    agg = {"ok": sum(v["ok"] for v in out.values()), "total": len(out)}
    Path(a.out).write_text(json.dumps({"schema": "harness-hostile/1", "cases": out, "aggregate": agg}, indent=1) + "\n", encoding="utf-8")
    for k, v in out.items():
        print(("OK  " if v["ok"] else "BAD ") + k, v["expected"], "| exit", v["exit"])
    print("aggregate", agg)
    return 0 if agg["ok"] == agg["total"] else 1


if __name__ == "__main__":
    sys.exit(main())
