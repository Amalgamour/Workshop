#!/usr/bin/env python3
"""Second-root reconstruction (0707/05.23 #05). NONPRODUCTION.
Rebuild ONE representative baseline (proto-l) with the frozen pass01 builder in a NEW root, require its CANDIDATE.json
to equal the declared identity, rerun representative cases there, and require the same verdicts as the first run.
Also checks: pass01/pass02 harness files and input manifests byte-identical to pack05.23; every frozen app/ row
unchanged; no app/ file modified after the pack05.23 manifest was written.
Rooms are retained explicitly under --root (no system temp directories, so no hidden cleanup step can fail).
usage: reconstruct.py --root NEW-DIR --first RESULT.json --out FILE [--cases M1-N7,F1b,R0,C1]
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
PACK23 = LIVE / "00.kernel/00.00.10.work/0707.app-use-check/evidence/pack05.23/source-manifest.json"
BUILDER = "labs/loop-convergence-harness-pass01/make_candidate.py"
IDENT = "labs/loop-convergence-harness-pass02/inputs/inputs-proto-l.json"


def sha_file(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def run(argv):
    p = subprocess.run([sys.executable, "-B", *map(str, argv)], capture_output=True, text=True)
    return {"argv": [str(x) for x in argv], "exit": p.returncode, "stdout_tail": p.stdout[-1500:], "stderr_tail": p.stderr[-600:]}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--first", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--cases", default="M1-N7,F1b,R0,C1")
    a = ap.parse_args()
    root = Path(a.root)
    root.mkdir(parents=True, exist_ok=False)
    rows = {r["path"]: r for r in json.loads(PACK23.read_bytes())["files"]}
    st = {"builder_frozen": sha_file(LIVE / BUILDER) == rows[BUILDER]["sha256"]}
    st["build"] = run([LIVE / BUILDER, "--kind", "proto-l", "--root", root / "cand-proto-l"])
    ident = json.loads((LIVE / IDENT).read_bytes())
    st["candidate_identity_equal"] = sha_file(root / "cand-proto-l/CANDIDATE.json") == ident["candidate"]["candidate_json_sha256"]
    st["run"] = run([HERE / "run.py", "--candidate", root / "cand-proto-l", "--identity", LIVE / IDENT, "--rooms", root / "rooms",
                     "--out", root / "result.json", "--cases", a.cases])
    second = {r["id"]: r["verdict"] for r in json.loads((root / "result.json").read_text(encoding="utf-8"))["records"]}
    first = {r["id"]: r["verdict"] for r in json.loads(Path(a.first).read_text(encoding="utf-8"))["records"]}
    st["verdicts"] = {cid: {"first": first.get(cid), "second": v} for cid, v in second.items()}
    st["verdicts_equal"] = all(first.get(cid) == v for cid, v in second.items())
    frozen_lab = [p for p in rows if p.startswith(("labs/loop-convergence-harness-pass01/", "labs/loop-convergence-harness-pass02/"))]
    st["old_harness_byte_identical"] = {"rows": len(frozen_lab), "drift": [p for p in frozen_lab if sha_file(LIVE / p) != rows[p]["sha256"]]}
    app_rows = [p for p in rows if p.startswith("app/")]
    t0 = PACK23.stat().st_mtime
    st["app"] = {"frozen_rows": len(app_rows), "drift": [p for p in app_rows if sha_file(LIVE / p) != rows[p]["sha256"]],
                 "modified_after_pack05.23": sorted(str(p.relative_to(LIVE)).replace("\\", "/") for p in (LIVE / "app").rglob("*")
                                                   if p.is_file() and "__pycache__" not in p.parts and p.stat().st_mtime > t0)}
    ok = (st["builder_frozen"] and st["build"]["exit"] == 0 and st["candidate_identity_equal"] and st["verdicts_equal"]
          and not st["old_harness_byte_identical"]["drift"] and not st["app"]["drift"] and not st["app"]["modified_after_pack05.23"])
    st["ok"] = ok
    Path(a.out).write_text(json.dumps(st, indent=1) + "\n", encoding="utf-8")
    print(json.dumps({k: (v["exit"] if isinstance(v, dict) and "exit" in v else v) for k, v in st.items()}, indent=1))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
