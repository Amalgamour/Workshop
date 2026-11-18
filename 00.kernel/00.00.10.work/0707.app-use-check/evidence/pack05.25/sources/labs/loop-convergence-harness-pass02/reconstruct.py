#!/usr/bin/env python3
"""Fresh-root reconstruction from the declared index (0707/05.22 #05). NONPRODUCTION.
From nothing but the frozen builder (pass01 make_candidate.py, hash-checked against pack05.22) and this lab's
make_inputs.py: rebuild both baseline candidates in NEW roots, regenerate their input manifests, require the
regenerated manifests to be byte-identical to the declared copies in inputs/, rerun the three unit suites, and
rerun the strict-n7 subset on the rebuilt staged-g. Then check that production bytes are unchanged: every app/ file
and every frozen labs/ file in pack05.22 still matches, and app/ holds no undeclared file.
usage: reconstruct.py --root NEW-DIR --out FILE      (exit 0 only if every step matches)
"""

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
LIVE = Path(r"D:\Git\lib-build")
PACK22 = LIVE / "00.kernel/00.00.10.work/0707.app-use-check/evidence/pack05.22/source-manifest.json"
BUILDER = "labs/loop-convergence-harness-pass01/make_candidate.py"


def sha_file(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def run(argv):
    p = subprocess.run([sys.executable, "-B", *map(str, argv)], capture_output=True, text=True)
    return {"argv": [str(x) for x in argv], "exit": p.returncode, "stdout_tail": p.stdout[-600:], "stderr_tail": p.stderr[-400:]}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    root = Path(a.root)
    root.mkdir(parents=True, exist_ok=False)
    man = json.loads(PACK22.read_bytes())
    rows = {r["path"]: r for r in man["files"]}
    out = {"schema": "harness-reconstruct/1", "steps": {}}
    st = out["steps"]
    st["builder_frozen"] = sha_file(LIVE / BUILDER) == rows[BUILDER]["sha256"]
    for k in ("proto-l", "staged-g"):
        st[f"build-{k}"] = run([LIVE / BUILDER, "--kind", k, "--root", root / f"cand-{k}"])
        st[f"inputs-{k}"] = run([HERE / "make_inputs.py", "--candidate-root", root / f"cand-{k}", "--name", k, "--out", root / f"inputs-{k}.json"])
        st[f"inputs-{k}-identical"] = (root / f"inputs-{k}.json").read_bytes() == (HERE / f"inputs/inputs-{k}.json").read_bytes()
    st["inputs-combined"] = run([HERE / "make_inputs.py", "--combined", "--out", root / "inputs-combined.json"])
    st["inputs-combined-identical"] = (root / "inputs-combined.json").read_bytes() == (HERE / "inputs/inputs-combined.json").read_bytes()
    for t in ("test_verdict.py", "test_shapes.py", "test_callbacks.py"):
        st[t] = run([HERE / t])
    st["strict-subset-rebuilt-staged-g"] = run([HERE / "harness.py", "--candidate", root / "cand-staged-g", "--inputs", root / "inputs-staged-g.json",
                                                "--rooms", root / "rooms-strict", "--out", root / "strict.json", "--suite", "strict-n7"])
    sres = json.loads((root / "strict.json").read_text(encoding="utf-8"))
    st["strict-verdicts"] = {r["id"]: r["verdict"] for r in sres["records"]}
    prod = {p: r for p, r in rows.items() if p.startswith(("app/", "labs/")) and not p.startswith("labs/loop-convergence-harness-pass02/")}
    drift = [p for p, r in prod.items() if not (LIVE / p).is_file() or sha_file(LIVE / p) != r["sha256"]]
    # run01 compared app/ against the pack rows, but pack05.22 freezes only 20 of the many pre-existing app/ files, so
    # every untouched undeclared file was flagged (my check's defect; kept as reconstruct-run01). Successor rule: no
    # app/ file (frozen or not) was created or modified after the pack05.22 manifest itself was written.
    t0 = PACK22.stat().st_mtime
    extra_app = sorted(str(p.relative_to(LIVE)).replace("\\", "/") for p in (LIVE / "app").rglob("*")
                       if p.is_file() and "__pycache__" not in p.parts and p.stat().st_mtime > t0)
    st["no-production-writes"] = {"frozen_app_and_labs_rows": len(prod), "drift": drift, "app_files_changed_after_pack05.22_manifest": extra_app,
                                  "app_files_scanned": sum(1 for p in (LIVE / "app").rglob("*") if p.is_file())}
    ok = (st["builder_frozen"] and all(st[f"build-{k}"]["exit"] == 0 and st[f"inputs-{k}-identical"] for k in ("proto-l", "staged-g"))
          and st["inputs-combined-identical"] and all(st[t]["exit"] == 0 for t in ("test_verdict.py", "test_shapes.py", "test_callbacks.py"))
          and set(st["strict-verdicts"].values()) == {"pass"} and st["strict-subset-rebuilt-staged-g"]["exit"] == 1
          and not drift and not extra_app)
    out["ok"] = ok
    Path(a.out).write_text(json.dumps(out, indent=1) + "\n", encoding="utf-8")
    print(json.dumps({k: (v if not isinstance(v, dict) or "exit" not in v else v["exit"]) for k, v in st.items()}, indent=1))
    print("RECONSTRUCTION", "OK" if ok else "MISMATCH")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
