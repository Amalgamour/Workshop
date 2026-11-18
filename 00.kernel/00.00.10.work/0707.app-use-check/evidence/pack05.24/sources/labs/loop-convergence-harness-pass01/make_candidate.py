#!/usr/bin/env python3
"""Build a BASELINE candidate root for the 0707/05.21 acceptance harness. NONPRODUCTION. No integration is built.

Candidates (code layer only; fixtures are added per case by the harness):
  proto-l   the exact 0707/05.20 accepted prototype: 05.18 code layer, v8 door, LAB v8 declaration -> n7-local overlay
            (lab bytes) -> 05.18 LAB pass04 at the canonical pass04 path. Dispatcher = 05.18 candidate (selects v8).
  staged-g  the accepted 0522/05.15 staging: v9 door (production bytes) + LAB v9 declaration -> LAB pass05 adapter.
            The v9 door pins PRODUCTION pass04 and v8 files, so those stay at their canonical paths; the LAB pass05
            loads a LAB pass04 from the side path labs/workbook-review-pass04-lab/workbook.py (same depth, so its
            own-root REPO line resolves to the candidate root). Dispatcher = live bytes with the v7 door line -> v9.
Writes <root>/CANDIDATE.json: every file with sha256/bytes/role/source, plus each LAB difference stated.
usage: make_candidate.py --kind proto-l|staged-g --root NEW-DIR
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True
LIVE = Path(r"D:\Git\lib-build")
sys.path.insert(0, str(LIVE / "labs/review-entry-integration-pass01"))
import rie  # noqa: E402

N7L = LIVE / "labs/n7-local-lifecycle-pass01"
P04_LAB = rie.ADAPT / "workbook-pass04.lab.py"
SIDE = "labs/workbook-review-pass04-lab/workbook.py"


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def rep(t: str, a: str, b: str) -> str:
    if t.count(a) != 1:
        raise SystemExit(f"refused: adapter anchor not found exactly once: {a[:60]}")
    return t.replace(a, b)


def pass05_lab() -> bytes:
    t = (LIVE / "labs/workbook-review-pass05/workbook.py").read_text(encoding="utf-8")
    t = rep(t, 'REPO = Path(r"D:\\Git\\lib-build")\n', 'REPO = Path(__file__).resolve().parents[2]  # LAB ADAPTER (production: D:\\Git\\lib-build)\n')
    t = rep(t, 'PASS04_REL = "labs/workbook-review-pass04/workbook.py"\n', f'PASS04_REL = "{SIDE}"  # LAB ADAPTER: side path (production pass04 path stays pinned by the v9 door)\n')
    p4 = P04_LAB.read_bytes()
    t = rep(t, 'PASS04_SHA = "b7b8776c0da775509b21614fadc1b51a39123a946add76d0dfcc9ad3fe3016e2"\nPASS04_BYTES = 6508\n',
            f'PASS04_SHA = "{sha(p4)}"  # LAB ADAPTER: 05.18 lab pass04\nPASS04_BYTES = {len(p4)}  # LAB ADAPTER\n')
    return t.encode("utf-8")


def dispatcher_v9() -> bytes:
    t = (LIVE / "app/librarian.py").read_text(encoding="utf-8")
    t = rep(t, "to the pinned v7 door.", "to the pinned v9 door.")
    t = rep(t, '"review_loop_tools_v7.py", "librarian_review_loop_tools_v7"', '"review_loop_tools_v9.py", "librarian_review_loop_tools_v9"')
    return t.encode("utf-8")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--kind", required=True, choices=("proto-l", "staged-g"))
    ap.add_argument("--root", required=True)
    a = ap.parse_args()
    root = Path(a.root)
    rie.refuse_inside(root)
    root.mkdir(parents=True, exist_ok=False)
    r = rie.Root(root)
    rie.build_code(r)                                  # 05.18 code layer (live app files, v8-pinned labs, v8 door, LAB v8 json, LAB pass04)
    lab = []
    if a.kind == "proto-l":
        r.put_bytes("app/review-loop-v8.json", (N7L / "adapter/review-loop-v8.n7local.lab.json").read_bytes(), "lab-adapter", "05.20")
        r.put_bytes("labs/n7-local-lifecycle-pass01/workbook.py", (N7L / "adapter/workbook.lab.py").read_bytes(), "lab-adapter", "05.20")
        rie.select(root, "v8")
        lab = [{"path": "app/review-loop-v8.json", "differs": "05.20 lab declaration: workbook -> overlay (lab bytes)"},
               {"path": "labs/n7-local-lifecycle-pass01/workbook.py", "differs": "05.20 overlay lab adapter: REPO line, pass04 pin"},
               {"path": "labs/workbook-review-pass04/workbook.py", "differs": "05.18 lab adapter: REPO line"},
               {"path": "app/librarian.py", "differs": "05.18 candidate dispatcher (selects v8); not production"}]
    else:
        for rel in ("app/review-loop-v8.json", "labs/workbook-review-pass04/workbook.py", "app/review_loop_tools_v9.py"):
            r.put_live(rel)                            # production bytes, pinned by the v9 door
        r.put_bytes(SIDE, P04_LAB.read_bytes(), "lab-adapter", "05.18")
        p5 = pass05_lab()
        r.put_bytes("labs/workbook-review-pass05/workbook.py", p5, "lab-adapter", "05.21")
        decl = json.loads((LIVE / "app/review-loop-v9.json").read_bytes())
        decl["_note"] = "LAB ADAPTER (0707/05.21): production v9 declaration with the workbook pin pointed at the lab pass05 adapter bytes."
        decl["tools"]["workbook"] = {"bytes": len(p5), "path": "labs/workbook-review-pass05/workbook.py", "sha256": sha(p5)}
        r.put_bytes("app/review-loop-v9.json", (json.dumps(decl, indent=2, sort_keys=True) + "\n").encode(), "lab-adapter", "05.21")
        d9 = dispatcher_v9()
        (root / "app/librarian.py").write_bytes(d9)
        lab = [{"path": "labs/workbook-review-pass05/workbook.py", "differs": "REPO line; PASS04_REL -> side path; pass04 pin -> 05.18 lab pass04"},
               {"path": SIDE, "differs": "05.18 lab pass04 at a side path (the canonical pass04 path holds production bytes)"},
               {"path": "app/review-loop-v9.json", "differs": "_note and workbook pin -> lab pass05"},
               {"path": "app/librarian.py", "differs": "live dispatcher with the review-loop door line v7 -> v9 (+ docstring); not production"}]
    files = []
    for p in sorted(x for x in root.rglob("*") if x.is_file()):
        rel = str(p.relative_to(root)).replace("\\", "/")
        if rel == "CANDIDATE.json" or rel == "ROOT-INDEX.json":
            continue
        b = p.read_bytes()
        files.append({"path": rel, "sha256": sha(b), "bytes": len(b), "lab": any(x["path"] == rel for x in lab)})
    doc = {"schema": "harness-candidate/1", "kind": a.kind, "lab_differences": lab, "files": files,
           "provides": {"proto-l": ["L(prototype over pass04)"], "staged-g": ["G(pass05)"]}[a.kind]}
    (root / "CANDIDATE.json").write_text(json.dumps(doc, indent=1) + "\n", encoding="utf-8")
    print(json.dumps({"root": str(root), "kind": a.kind, "files": len(files), "candidate_sha256": sha((root / "CANDIDATE.json").read_bytes())}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
