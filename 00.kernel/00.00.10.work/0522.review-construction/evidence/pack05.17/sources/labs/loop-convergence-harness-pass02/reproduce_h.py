#!/usr/bin/env python3
"""Reproduce Prime's 06.21 findings H1-H4 against the PRESERVED first harness (labs/loop-convergence-harness-pass01).
NONPRODUCTION. Lab only. The pass01 files are imported read-only and never edited; their hashes are recorded.

H1  pass01 CAP-4 / RP-1 / RP-2 / IN-2 callbacks return 'not-run' unconditionally          (helper probe: direct call)
H2  pass01 aggregate() with dependencies None / {} / 'not-a-list' -> ready True              (helper probe: direct call)
H3  pass01 strict_case passes ST-2 on proto-l without the malformed-n7-declaration reason    (FULL CLI: pass01 harness.py)
H4  pass01 aggregate() with a filtered declared_required and all deps accepted -> ready True (helper probe; the actual
    pass01 CLI is still held by today's pending rows, so no CLI readiness was ever released by it)
usage: reproduce_h.py --proto-l CAND --rooms NEW-DIR --out FILE
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

sys.dont_write_bytecode = True
LIVE = Path(r"D:\Git\lib-build")
P1 = LIVE / "labs/loop-convergence-harness-pass01"


def sha_file(p) -> str:
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def rec(cid, verdict="pass", required=True):
    return {"id": cid, "group": "g", "requirement": "r", "required": required, "expected": "e", "observed": "o",
            "verdict": verdict, "evidence": "x", "provenance": "reproduce_h"}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--proto-l", required=True)
    ap.add_argument("--rooms", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    rooms = Path(a.rooms)
    rooms.mkdir(parents=True, exist_ok=False)
    pins_before = {p.name: sha_file(p) for p in sorted(P1.glob("*.py"))}
    sys.path.insert(0, str(P1))
    v1 = load("pass01_verdict", P1 / "verdict.py")
    h1 = load("pass01_harness", P1 / "harness.py")
    out = {"schema": "reproduce-h/1", "pass01_pins": pins_before}

    # H1 - direct calls of the four callbacks (ctx is never touched by the stubs)
    by = {c["id"]: c for c in h1.CASES}
    h1r = {cid: list(by[cid]["fn"](None)) for cid in ("CAP-4", "RP-1", "RP-2", "IN-2")}
    out["H1"] = {"kind": "helper probe (direct call)", "results": h1r,
                 "reproduced": all(r[2] == "not-run" for r in h1r.values())}

    # H2 - malformed dependency collections
    h2r = {}
    for label, deps in (("None", None), ("dict", {}), ("string", "not-a-list")):
        h2r[label] = v1.aggregate([rec("a")], ["a"], deps)
    out["H2"] = {"kind": "helper probe (direct call)", "results": h2r, "reproduced": all(r["ready"] is True for r in h2r.values())}

    # H4 - filtered required list with all dependencies synthetically accepted
    full_required = [c["id"] for c in h1.CASES if c["required"]]
    subset = [c["id"] for c in h1.CASES if c["required"] and c["group"] == "n5-same-cut"]
    acc = [{"id": d, "status": "accepted"} for d in ("G", "L", "K", "I", "R", "W")]
    r4 = v1.aggregate([rec(x) for x in subset], subset, acc)
    out["H4"] = {"kind": "helper probe (direct call); not a CLI release", "full_required": len(full_required), "subset_required": subset,
                 "result": r4, "reproduced": r4["ready"] is True and len(subset) < len(full_required)}

    # H3 - FULL CLI: pass01 harness on a rebuilt proto-l candidate, strict-n7 group only
    inp = P1 / "inputs/inputs-proto-l.json"
    res_path = rooms / "H3-pass01-strict.json"
    p = subprocess.run([sys.executable, "-B", str(P1 / "harness.py"), "--candidate", a.proto_l, "--inputs", str(inp),
                        "--rooms", str(rooms / "H3-rooms"), "--out", str(res_path), "--suite", "strict-n7"], capture_output=True, text=True)
    (rooms / "H3-pass01-strict.stdout").write_text(p.stdout, encoding="utf-8")
    (rooms / "H3-pass01-strict.stderr").write_text(p.stderr, encoding="utf-8")
    res = json.loads(res_path.read_text(encoding="utf-8"))
    st2 = next(r for r in res["records"] if r["id"] == "ST-2")
    out["H3"] = {"kind": "full CLI (pass01 harness.py --suite strict-n7)", "exit": p.returncode, "ST-2": {"verdict": st2["verdict"], "observed": st2["observed"]},
                 "reproduced": st2["verdict"] == "pass" and "malformed-n7-declaration" not in st2["observed"]["codes"],
                 "note": "pass01 exit is 1 only because K/I/R/W are pending; ST-2 itself is recorded pass for a non-grammar reason"}
    out["pass01_pins_after"] = {p.name: sha_file(p) for p in sorted(P1.glob("*.py"))}
    out["pass01_unchanged"] = out["pass01_pins_after"] == pins_before
    Path(a.out).write_text(json.dumps(out, indent=1, default=str) + "\n", encoding="utf-8")
    for k in ("H1", "H2", "H3", "H4"):
        print(k, "reproduced" if out[k]["reproduced"] else "NOT reproduced", "|", out[k]["kind"])
    print("pass01 unchanged:", out["pass01_unchanged"])
    return 0 if all(out[k]["reproduced"] for k in ("H1", "H2", "H3", "H4")) and out["pass01_unchanged"] else 1


if __name__ == "__main__":
    sys.exit(main())
