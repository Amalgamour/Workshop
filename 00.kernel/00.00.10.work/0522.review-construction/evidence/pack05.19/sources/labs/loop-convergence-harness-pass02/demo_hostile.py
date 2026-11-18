#!/usr/bin/env python3
"""Harness-hostile demonstrations, successor (0707/05.22). NONPRODUCTION. Each runs the SUCCESSOR harness.py as a NEW
process and records its exit. HX-1..HX-6 are the pass01 cases reconciled to the successor; HX-7..HX-14 are new.
HX-1  combined candidate (inputs-combined.json; K/I/R/W pending)              -> exit 1, NOT READY, every case blocked
HX-2  a candidate file tampered after its identity was declared               -> exit 2, refused, no rooms
HX-3  a PENDING row carrying a guessed pin                                     -> exit 2
HX-4  an accepted row whose declared hash does not match the frozen file       -> exit 2
HX-5  unit suites: test_verdict (40), test_shapes (24), test_callbacks (29)    -> all exit 0
HX-6  capacity-only suite on the given baseline                               -> NOT READY, scope subset, coverage enumerated
HX-7/8/9  dependencies None / {} / "G,L" in the inputs file                    -> exit 2, refused, no rooms (06.21 H2 via CLI)
HX-10 a pending row promoted by editing status to 'accepted' only              -> exit 2
HX-11 an accepted row whose frozen review reference is wrong                   -> exit 2
HX-12 an unknown --suite group                                                 -> exit 2
HX-13 strict-n7 subset on staged-g: every selected case passes                 -> still NOT READY (exit 1: pending deps), subset pass reported separately
HX-14 strict-n7 subset on proto-l                                              -> exit 1; ST-1/2/3 fail for the missing malformed-n7-declaration reason
usage: demo_hostile.py --proto-l DIR --staged-g DIR --rooms NEW-DIR --out FILE
"""

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
H = HERE / "harness.py"


def run(argv):
    p = subprocess.run([sys.executable, "-B", *map(str, argv)], capture_output=True, text=True)
    return {"argv": [str(x) for x in argv], "exit": p.returncode, "stdout_tail": p.stdout[-1500:], "stderr_tail": p.stderr[-600:]}


def harness(rooms, tag, cand, inputs, suite=None):
    argv = [H, "--inputs", inputs, "--rooms", rooms / tag, "--out", rooms / f"{tag}.json"]
    if cand:
        argv[1:1] = ["--candidate", cand]
    if suite:
        argv += ["--suite", suite]
    r = run(argv)
    res = json.loads((rooms / f"{tag}.json").read_text(encoding="utf-8")) if (rooms / f"{tag}.json").exists() else {}
    return r, res


def mutated(rooms, name, base, fn):
    doc = json.loads(json.dumps(base))
    fn(doc)
    p = rooms / f"{name}-inputs.json"
    p.write_text(json.dumps(doc, indent=1), encoding="utf-8")
    return p


def dep(doc, did):
    return next(d for d in doc["dependencies"] if d["id"] == did)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--proto-l", required=True)
    ap.add_argument("--staged-g", required=True)
    ap.add_argument("--rooms", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    rooms = Path(a.rooms)
    rooms.mkdir(parents=True, exist_ok=False)
    inp_p, inp_g = HERE / "inputs/inputs-proto-l.json", HERE / "inputs/inputs-staged-g.json"
    base = json.loads(inp_p.read_text(encoding="utf-8"))
    out = {}

    r, res = harness(rooms, "HX-1", None, HERE / "inputs/inputs-combined.json")
    vs = {x["verdict"] for x in res.get("records", [])}
    out["HX-1"] = {"expected": "exit 1, not ready, all blocked", "exit": r["exit"], "ready": res.get("ready"), "verdicts": sorted(vs),
                   "ok": r["exit"] == 1 and res.get("ready") is False and vs == {"blocked"}}

    tam = rooms / "HX-2-candidate"
    shutil.copytree(a.proto_l, tam)
    f = tam / "app/review_loop_tools_v8.py"
    f.write_bytes(f.read_bytes() + b"\n# tampered after identity\n")
    r, res = harness(rooms, "HX-2", tam, inp_p)
    out["HX-2"] = {"expected": "exit 2, refused, no rooms", "exit": r["exit"], "refused": res.get("refused"),
                   "ok": r["exit"] == 2 and not (rooms / "HX-2").exists()}

    def refusal(tag, expected, fn, cand=a.proto_l):
        p = mutated(rooms, tag, base, fn)
        r, res = harness(rooms, tag, cand, p)
        out[tag] = {"expected": expected, "exit": r["exit"], "refused": res.get("refused"), "ok": r["exit"] == 2 and not (rooms / tag).exists()}

    refusal("HX-3", "exit 2 (pending row with a guessed pin)",
            lambda d: dep(d, "K").update(files=[{"path": "labs/review-source-capacity-pass02/prime_review.py", "sha256": "0" * 64, "bytes": 1}]))
    refusal("HX-4", "exit 2 (accepted row does not match frozen bytes)", lambda d: dep(d, "G")["files"][0].update(sha256="f" * 64))

    units = {}
    for t, n in (("test_verdict.py", 40), ("test_shapes.py", 24), ("test_callbacks.py", 29)):
        rr = run([HERE / t])
        units[t] = {"exit": rr["exit"], "tail": rr["stdout_tail"][-80:]}
    out["HX-5"] = {"expected": "three unit suites exit 0", "units": units, "exit": max(u["exit"] for u in units.values()),
                   "ok": all(u["exit"] == 0 for u in units.values())}

    r, res = harness(rooms, "HX-6", a.proto_l, inp_p, "capacity")
    ag = res.get("aggregate", {})
    out["HX-6"] = {"expected": "capacity-only: NOT READY, scope subset, 32 missing required ids enumerated", "exit": r["exit"], "ready": res.get("ready"),
                   "scope": ag.get("scope"), "missing": len(ag.get("coverage_missing", [])),
                   "ok": r["exit"] in (1, 4) and res.get("ready") is False and ag.get("scope") == "subset" and len(ag.get("coverage_missing", [])) == 32}

    refusal("HX-7", "exit 2 (dependencies None)", lambda d: d.update(dependencies=None))
    refusal("HX-8", "exit 2 (dependencies {})", lambda d: d.update(dependencies={}))
    refusal("HX-9", "exit 2 (dependencies string)", lambda d: d.update(dependencies="G,L"))
    refusal("HX-10", "exit 2 (pending K promoted by a status string only)", lambda d: dep(d, "K").update(status="accepted"))
    refusal("HX-11", "exit 2 (accepted G with a wrong frozen review reference)", lambda d: dep(d, "G")["review_ref"].update(sha256="0" * 64))

    r, res = harness(rooms, "HX-12", a.proto_l, inp_p, "capacity,nonexistent")
    out["HX-12"] = {"expected": "exit 2 (unknown suite group)", "exit": r["exit"], "refused": res.get("refused"), "ok": r["exit"] == 2 and not (rooms / "HX-12").exists()}

    r, res = harness(rooms, "HX-13", a.staged_g, inp_g, "strict-n7")
    ag = res.get("aggregate", {})
    vs = {x["id"]: x["verdict"] for x in res.get("records", [])}
    out["HX-13"] = {"expected": "staged-g strict-n7 subset: every selected case passes; still NOT READY (exit 1, pending deps); subset pass reported",
                    "exit": r["exit"], "ready": res.get("ready"), "verdicts": vs, "subset_pass": ag.get("subset", {}).get("all_selected_required_pass"),
                    "ok": r["exit"] == 1 and res.get("ready") is False and set(vs.values()) == {"pass"} and ag.get("subset", {}).get("all_selected_required_pass") is True}

    r, res = harness(rooms, "HX-14", a.proto_l, inp_p, "strict-n7")
    recs = {x["id"]: x for x in res.get("records", [])}
    why = {k: (recs[k]["observed"].get("judge_reasons") if isinstance(recs.get(k, {}).get("observed"), dict) else None) for k in ("ST-1", "ST-2", "ST-3")}
    out["HX-14"] = {"expected": "proto-l strict-n7: ST-1/2/3 fail naming the absent malformed-n7-declaration reason; ST-4 control passes; exit 1",
                    "exit": r["exit"], "verdicts": {k: v["verdict"] for k, v in recs.items()}, "reasons": why,
                    "ok": r["exit"] == 1 and all(recs[k]["verdict"] == "fail" and any("malformed-n7-declaration reason absent" in x for x in (why[k] or []))
                                                 for k in ("ST-1", "ST-2", "ST-3")) and recs["ST-4"]["verdict"] == "pass"}

    agg = {"ok": sum(v["ok"] for v in out.values()), "total": len(out)}
    Path(a.out).write_text(json.dumps({"schema": "harness-hostile/2", "cases": out, "aggregate": agg}, indent=1, default=str) + "\n", encoding="utf-8")
    for k, v in out.items():
        print(("OK  " if v["ok"] else "BAD ") + k, v["expected"], "| exit", v["exit"])
    print("aggregate", agg)
    return 0 if agg["ok"] == agg["total"] else 1


if __name__ == "__main__":
    sys.exit(main())
