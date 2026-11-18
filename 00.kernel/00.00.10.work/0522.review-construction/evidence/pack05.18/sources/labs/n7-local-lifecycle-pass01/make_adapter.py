#!/usr/bin/env python3
"""Derive the LAB adapter bytes of the n7-local overlay and its lab v8 declaration (0707/05.20). NONPRODUCTION.
Exactly two edits from workbook.py (the proposed production-shaped bytes):
  1. REPO = the file's own root (lab roots are not D:\\Git\\lib-build)
  2. the pass04 pin = the 05.18 lab pass04 adapter bytes (production pins b7b8776c..., 6508)
"""

import hashlib
import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True
L = Path(__file__).resolve().parent
P4_LAB = Path(r"D:\Git\lib-build\labs\review-entry-integration-pass01\adapter\workbook-pass04.lab.py")
DECL_0518 = Path(r"D:\Git\lib-build\labs\review-entry-integration-pass01\adapter\review-loop-v8.lab.json")

src = (L / "workbook.py").read_text(encoding="utf-8")
a = 'REPO = Path(r"D:\\Git\\lib-build")\n'
assert src.count(a) == 1, "REPO line not found exactly once"
out = src.replace(a, 'REPO = Path(__file__).resolve().parents[2]  # LAB ADAPTER: the candidate root (production: D:\\Git\\lib-build)\n')
b = 'PASS04_SHA = "b7b8776c0da775509b21614fadc1b51a39123a946add76d0dfcc9ad3fe3016e2"\nPASS04_BYTES = 6508\n'
assert out.count(b) == 1, "pass04 pin lines not found exactly once"
p4 = P4_LAB.read_bytes()
out = out.replace(b, f'PASS04_SHA = "{hashlib.sha256(p4).hexdigest()}"  # LAB ADAPTER: 05.18 lab pass04 (production b7b8776c...)\n'
                     f'PASS04_BYTES = {len(p4)}  # LAB ADAPTER (production 6508)\n')
(L / "adapter").mkdir(exist_ok=True)
(L / "adapter/workbook.lab.py").write_bytes(out.encode("utf-8"))
decl = json.loads(DECL_0518.read_bytes())
w = (L / "adapter/workbook.lab.py").read_bytes()
decl["_note"] = ("LAB ADAPTER (0707/05.20): the 05.18 lab v8 declaration with the workbook pin pointed at the n7-local overlay "
                 "(lab bytes). Not a production declaration.")
decl["tools"]["workbook"] = {"bytes": len(w), "path": "labs/n7-local-lifecycle-pass01/workbook.py", "sha256": hashlib.sha256(w).hexdigest()}
(L / "adapter/review-loop-v8.n7local.lab.json").write_bytes((json.dumps(decl, indent=2, sort_keys=True) + "\n").encode())
for p in ("workbook.py", "adapter/workbook.lab.py", "adapter/review-loop-v8.n7local.lab.json"):
    data = (L / p).read_bytes()
    print(hashlib.sha256(data).hexdigest(), len(data), p)
