#!/usr/bin/env python3
"""Second-root reconstruction (0707/05.24). NONPRODUCTION. Rebuild proto-l with the frozen pass01 builder in a NEW
root; require the legacy identity to resolve to the same workbook and the execution proof to pass; rerun R0 and F1b
through the freshness adapter and ST-1..4 through pass03; require the first run's verdicts. Also checks that the old
harness/freshness labs and inputs, and the frozen app rows, are byte-identical to pack05.24, and no app/ file changed
after the pack05.24 manifest. Rooms are explicit and retained.
usage: reconstruct24.py --root NEW-DIR --first-fbt FBT.json --first-h3 H3.json --out FILE"""

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path

LIVE = Path(r"D:\Git\lib-build")
PACK24 = LIVE / "00.kernel/00.00.10.work/0707.app-use-check/evidence/pack05.24/source-manifest.json"
HERE = Path(__file__).resolve().parent
IDENT = LIVE / "labs/loop-convergence-harness-pass02/inputs/inputs-proto-l.json"


def sha_file(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def run(argv):
    p = subprocess.run([sys.executable, "-B", *map(str, argv)], capture_output=True, text=True)
    return {"exit": p.returncode, "stdout_tail": p.stdout[-800:], "stderr_tail": p.stderr[-400:]}


def v(p):
    return {r["id"]: r["verdict"] for r in json.loads(Path(p).read_text(encoding="utf-8"))["records"]}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--first-fbt", required=True)
    ap.add_argument("--first-h3", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    root = Path(a.root)
    root.mkdir(parents=True, exist_ok=False)
    rows = {r["path"]: r for r in json.loads(PACK24.read_bytes())["files"]}
    st = {"build": run([LIVE / "labs/loop-convergence-harness-pass01/make_candidate.py", "--kind", "proto-l", "--root", root / "cand"])}
    st["fbt"] = run([HERE / "run.py", "--candidate", root / "cand", "--identity", IDENT, "--rooms", root / "fbt", "--out", root / "fbt.json", "--cases", "R0,F1b"])
    st["h3"] = run([LIVE / "labs/loop-convergence-harness-pass03/harness.py", "--candidate", root / "cand", "--inputs", IDENT, "--rooms", root / "h3",
                    "--out", root / "h3.json", "--suite", "strict-n7"])
    f2, h2 = v(root / "fbt.json"), v(root / "h3.json")
    f1, h1 = v(a.first_fbt), v(a.first_h3)
    st["verdicts"] = {"fbt": {k: (f1.get(k), x) for k, x in f2.items()}, "h3": {k: (h1.get(k), x) for k, x in h2.items()}}
    st["verdicts_equal"] = all(f1.get(k) == x for k, x in f2.items()) and all(h1.get(k) == x for k, x in h2.items())
    fdoc = json.loads((root / "fbt.json").read_text(encoding="utf-8"))
    st["identity"] = {"mode": fdoc.get("identity_mode"), "workbook": fdoc.get("workbook_entry"),
                      "proof": {k: x["verdict"] for k, x in (fdoc.get("execution_proof") or {}).items()}}
    old = [p for p in rows if p.startswith(("labs/loop-convergence-harness-pass01/", "labs/loop-convergence-harness-pass02/",
                                            "labs/freshness-boundary-tests-pass01/", "app/"))]
    t0 = PACK24.stat().st_mtime
    st["preserved"] = {"rows": len(old), "drift": [p for p in old if sha_file(LIVE / p) != rows[p]["sha256"]],
                       "app_modified_after_pack05.24": sorted(str(p.relative_to(LIVE)).replace("\\", "/") for p in (LIVE / "app").rglob("*")
                                                              if p.is_file() and "__pycache__" not in p.parts and p.stat().st_mtime > t0)}
    ok = (st["build"]["exit"] == 0 and st["verdicts_equal"] and st["identity"]["mode"] == "legacy-discovery"
          and set(st["identity"]["proof"].values()) == {"executed"} and not st["preserved"]["drift"] and not st["preserved"]["app_modified_after_pack05.24"])
    st["ok"] = ok
    Path(a.out).write_text(json.dumps(st, indent=1) + "\n", encoding="utf-8")
    print(json.dumps({k: (x["exit"] if isinstance(x, dict) and "exit" in x else x) for k, x in st.items()}, indent=1))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
