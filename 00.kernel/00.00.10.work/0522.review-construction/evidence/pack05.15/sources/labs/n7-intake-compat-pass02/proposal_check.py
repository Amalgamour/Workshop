#!/usr/bin/env python3
"""Check the UNAPPLIED pass04 proposal against the pass02 lab (0707/05.17). NONPRODUCTION.

Loads the proposal file (read-only, from evidence/design05.17/proposal/) as a module in this process.
1. Parser equivalence: for every test input, in contexts N5NN / N7NN / none, proposal parse == lab parse.
2. Intake on existing disposable copies (child processes): the proposal module with the lab's REPO redirect
   applied (the proposal itself has no redirect) must reproduce the lab's intake_id on the same book.
usage: proposal_check.py --faithful REPO --n5 REPO --expect-n7 ID --expect-n5 ID --out FILE
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import os
import subprocess
import sys
from pathlib import Path

sys.dont_write_bytecode = True
LIVE = Path(r"D:\Git\lib-build")
LAB = LIVE / "labs/n7-intake-compat-pass02"
PROPOSAL = LIVE / "00.kernel/00.00.10.work/0707.app-use-check/evidence/design05.17/proposal/workbook-review-pass04.workbook.py.proposal"
ENV = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")


def load_proposal():
    loader = importlib.machinery.SourceFileLoader("pass04_proposal", str(PROPOSAL))
    spec = importlib.util.spec_from_loader("pass04_proposal", loader)
    mod = importlib.util.module_from_spec(spec)
    loader.exec_module(mod)
    return mod


CHILD = r"""
import sys, json, importlib.machinery, importlib.util
from pathlib import Path
sys.dont_write_bytecode = True
loader = importlib.machinery.SourceFileLoader("pass04_proposal", sys.argv[1])
spec = importlib.util.spec_from_loader("pass04_proposal", loader)
m = importlib.util.module_from_spec(spec); loader.exec_module(m)
root = Path(sys.argv[2]).resolve()
m.p3.wb.REPO = root; m.p3.p2.REPO = root; m.p3.REPO = root      # lab-only redirect, same as n7compat2 --repo-root
sys.exit(m.main(sys.argv[3:]))
"""


def main() -> int:
    ap = argparse.ArgumentParser()
    for k in ("--faithful", "--n5", "--expect-n7", "--expect-n5", "--out"):
        ap.add_argument(k, required=True)
    a = ap.parse_args()
    import importlib.machinery  # noqa: F401
    sys.path.insert(0, str(LAB / "tests"))
    sys.argv = [sys.argv[0]]
    import test_n7v2 as t   # reuses the inputs and the lab parsers (no case is run)
    prop = load_proposal()
    blk = t.P3.wb.pointer_block(t.FROZEN_PACK.read_bytes().decode("utf-8"))
    inputs = dict(t.N5_INPUTS, **{"real-n7": blk})
    eq = {}
    for kind in ("N5NN", "N7NN", None):
        lab = {"N5NN": t.V2_N5, "N7NN": t.V2_N7, None: t.V2_NONE}[kind]
        tok = prop.KIND.set(kind)
        try:
            eq[str(kind)] = {k: prop.parse_pointer(b) == lab(b) for k, b in inputs.items()}
        finally:
            prop.KIND.reset(tok)
    parse_ok = all(all(v.values()) for v in eq.values())
    child = Path(a.out).with_suffix(".child.py")
    child.write_text(CHILD, encoding="utf-8")
    runs = {}
    for name, repo, src, pas, want in (("n7-faithful", a.faithful, "0707.app-use-check", "05.15", a.expect_n7),
                                       ("n5-0522", a.n5, "0522.review-construction", "05.13", a.expect_n5)):
        p = subprocess.run([sys.executable, "-B", str(child), str(PROPOSAL), repo, "prepare", "--book", str(Path(repo) / "00.kernel/00.00.10.work"),
                            "--source", src, "--pass", pas], capture_output=True, env=ENV, timeout=600, cwd=str(LIVE))
        body = json.loads(p.stdout.decode("utf-8")) if p.stdout.strip() else {}
        runs[name] = {"exit": p.returncode, "intake_id": body.get("intake_id"), "expected": want, "equal": body.get("intake_id") == want,
                      "measurement": body.get("measurement"), "stderr_tail": p.stderr.decode("utf-8", "replace")[-200:]}
    ok = parse_ok and all(r["equal"] and r["exit"] == 0 for r in runs.values())
    Path(a.out).write_text(json.dumps({"schema": "pass04-proposal-check/1", "proposal": str(PROPOSAL), "parse_equivalence": eq, "parse_ok": parse_ok,
                                       "intake": runs, "ok": ok}, indent=1) + "\n", encoding="utf-8")
    print("parse_ok", parse_ok, {k: (v["exit"], v["equal"], v["measurement"]) for k, v in runs.items()}, "ok", ok)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
