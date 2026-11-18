#!/usr/bin/env python3
"""Second-root reconstruction (0707/05.25). NONPRODUCTION. Rebuild proto-l with the frozen pass01 builder in a NEW
root; rerun R0/F1b through freshness pass03 and N5-1 / PR-7 / CTX-1 (n5-same-cut + preservation groups) through pass04;
require the first run's verdicts and an 'executed' proof. Also: earlier labs/inputs and frozen app rows byte-identical
to pack05.25; no app/ file changed after the pack05.25 manifest. Rooms explicit and retained.
usage: reconstruct25.py --root NEW-DIR --first-fbt FBT.json --first-h4 H4.json --out FILE"""

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path

LIVE = Path(r"D:\Git\lib-build")
PACK25 = LIVE / "00.kernel/00.00.10.work/0707.app-use-check/evidence/pack05.25/source-manifest.json"
IDENT = LIVE / "labs/loop-convergence-harness-pass02/inputs/inputs-proto-l.json"


def sha_file(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def run(argv):
    p = subprocess.run([sys.executable, "-B", *map(str, argv)], capture_output=True, text=True)
    return {"exit": p.returncode, "stdout_tail": p.stdout[-600:], "stderr_tail": p.stderr[-300:]}


def v(p):
    return {r["id"]: r["verdict"] for r in json.loads(Path(p).read_text(encoding="utf-8"))["records"]}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--first-fbt", required=True)
    ap.add_argument("--first-h4", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    root = Path(a.root)
    root.mkdir(parents=True, exist_ok=False)
    rows = {r["path"]: r for r in json.loads(PACK25.read_bytes())["files"]}
    st = {"build": run([LIVE / "labs/loop-convergence-harness-pass01/make_candidate.py", "--kind", "proto-l", "--root", root / "cand"])}
    st["fbt"] = run([LIVE / "labs/freshness-boundary-tests-pass03/run.py", "--candidate", root / "cand", "--identity", IDENT, "--rooms", root / "fbt",
                     "--out", root / "fbt.json", "--cases", "R0,F1b"])
    st["h4"] = run([LIVE / "labs/loop-convergence-harness-pass04/harness.py", "--candidate", root / "cand", "--inputs", IDENT, "--rooms", root / "h4",
                    "--out", root / "h4.json", "--suite", "n5-same-cut,preservation"])
    f1, h1 = v(a.first_fbt), v(a.first_h4)
    f2, h2 = v(root / "fbt.json"), v(root / "h4.json")
    st["verdicts"] = {"fbt": {k: (f1.get(k), x) for k, x in f2.items()}, "h4": {k: (h1.get(k), x) for k, x in h2.items()}}
    st["verdicts_equal"] = all(f1.get(k) == x for k, x in f2.items()) and all(h1.get(k) == x for k, x in h2.items())
    proofs = {}
    for name in ("fbt.json", "h4.json"):
        d = json.loads((root / name).read_text(encoding="utf-8"))
        proofs[name] = {k: x["class"] for k, x in (d.get("execution_proof") or {}).items()}
    st["proof_classes"] = proofs
    old = [p for p in rows if p.startswith(("labs/loop-convergence-harness-pass0", "labs/freshness-boundary-tests-pass01/",
                                            "labs/freshness-boundary-tests-pass02/", "app/"))]
    t0 = PACK25.stat().st_mtime
    st["preserved"] = {"rows": len(old), "drift": [p for p in old if sha_file(LIVE / p) != rows[p]["sha256"]],
                       "app_modified_after_pack05.25": sorted(str(p.relative_to(LIVE)).replace("\\", "/") for p in (LIVE / "app").rglob("*")
                                                              if p.is_file() and "__pycache__" not in p.parts and p.stat().st_mtime > t0)}
    ok = (st["build"]["exit"] == 0 and st["verdicts_equal"] and all(set(x.values()) == {"executed"} for x in proofs.values())
          and not st["preserved"]["drift"] and not st["preserved"]["app_modified_after_pack05.25"])
    st["ok"] = ok
    Path(a.out).write_text(json.dumps(st, indent=1) + "\n", encoding="utf-8")
    print(json.dumps({k: (x["exit"] if isinstance(x, dict) and "exit" in x else x) for k, x in st.items()}, indent=1))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
