#!/usr/bin/env python3
"""HELPER EVIDENCE ONLY (0707/05.23). Not an end-to-end test and not a demonstrated publication exploit.

Extracts the frozen L prototype's region helper (regions() and its two heading constants) from
labs/n7-local-lifecycle-pass01/workbook.py by AST, hash-checked against pack05.23, WITHOUT importing or running the
module. Applies it to every pack-region fixture before and after its edit, and reports whether bound_sha256 (the
value the prototype's freshness exemption compares) changes. 'exempt' = the edit leaves bound_sha256 unchanged.
usage: helper_regions.py --out FILE
"""

import argparse
import ast
import hashlib
import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import run as R  # noqa: E402  (fixture text only; no candidate is executed)

LIVE = Path(r"D:\Git\lib-build")
SRC = "labs/n7-local-lifecycle-pass01/workbook.py"


def extract():
    row = R.frozen_rows()[SRC]
    data = (LIVE / SRC).read_bytes()
    if hashlib.sha256(data).hexdigest() != row["sha256"]:
        raise SystemExit("refused: the L workbook differs from its pack05.23 freeze")
    tree = ast.parse(data.decode("utf-8"))
    keep = [n for n in tree.body if (isinstance(n, ast.FunctionDef) and n.name == "regions")
            or (isinstance(n, ast.Assign) and any(getattr(t, "id", "") in ("REVIEW_HEADING", "POINTER_HEADING") for t in n.targets))]
    ns = {"sha": lambda b: hashlib.sha256(b).hexdigest()}
    exec(compile(ast.Module(body=keep, type_ignores=[]), SRC, "exec"), ns)     # only the 3 extracted nodes
    return ns["regions"], hashlib.sha256(data).hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    regions, src_sha = extract()
    lines = ("Returned: 05.01.return.md (lab, 2026-11-04), sha256 " + "1" * 64 + ", 10 bytes.\n"
             "Artifact manifest: evidence/e0501/artifact-manifest.json, sha256 " + "2" * 64 + ", 20 bytes.").encode()
    out = {}
    for cid, (variant, anchor, repl, expect) in R.REGION.items():
        if anchor in ("return", "artifact"):
            out[cid] = {"applies": False, "why": "return/artifact changes are row changes, not pack-region changes"}
            continue
        before = R.pack_text(variant).encode("utf-8").replace(b"POINTER-SLOT", lines)
        after = before + repl if anchor is None else before.replace(anchor, repl, 1)
        rb, ra = regions(before), regions(after)
        exempt = rb["bound_sha256"] == ra["bound_sha256"]
        out[cid] = {"applies": True, "required_end_to_end": expect, "helper_exempts_edit": exempt,
                    "helper_agrees_with_requirement": (exempt and expect == "current") or (not exempt and expect == "not-current")}
    doc = {"schema": "helper-regions/1", "label": "HELPER EVIDENCE ONLY; not end-to-end; not an exploit", "source": SRC, "source_sha256": src_sha,
           "cases": out}
    Path(a.out).write_text(json.dumps(doc, indent=1) + "\n", encoding="utf-8")
    for k, v in out.items():
        print(k, v if not v.get("applies") else ("exempt" if v["helper_exempts_edit"] else "bound-changes", "agrees" if v["helper_agrees_with_requirement"] else "DISAGREES"))


if __name__ == "__main__":
    main()
