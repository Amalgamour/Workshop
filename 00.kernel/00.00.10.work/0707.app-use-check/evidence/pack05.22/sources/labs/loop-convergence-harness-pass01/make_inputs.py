#!/usr/bin/env python3
"""Write the declared input manifests for the 0707/05.21 harness. NONPRODUCTION.
Each manifest names: the candidate identity (CANDIDATE.json sha256 + every file), the dependency rows with Prime status,
the frozen fixture source (pack05.21 manifest hash) and the retained judgments with expected source counts from
Prime's reviews. PENDING rows carry no path/hash; the harness refuses to run anything that needs them.
usage: make_inputs.py --candidate-root DIR --name NAME --out FILE      (a baseline candidate)
       make_inputs.py --combined --out FILE                              (the future combined candidate; PENDING)
"""

import argparse
import hashlib
import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True
LIVE = Path(r"D:\Git\lib-build")
PAGE = "00.kernel/00.00.10.work/0707.app-use-check"


def sha_file(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def frozen(rel):
    return {"path": rel, "sha256": sha_file(LIVE / rel), "bytes": (LIVE / rel).stat().st_size}


DEPENDENCIES = [
    {"id": "G", "role": "strict N7 parser (pass05, v9 door)", "status": "accepted", "review": "0522.review-construction/06.33.md",
     "files": [frozen("labs/workbook-review-pass05/workbook.py"), frozen("app/review_loop_tools_v9.py"), frozen("app/review-loop-v9.json")]},
    {"id": "L", "role": "N7-local lifecycle (prototype over pass04)", "status": "accepted", "review": "0707.app-use-check/06.20.review.md",
     "files": [frozen("labs/n7-local-lifecycle-pass01/workbook.py")],
     "limits": "accepted as a bounded prototype; production labels and composition over G pending (06.20.review)"},
    {"id": "K", "role": "record source capacity (source-only bound 64)", "status": "pending", "review": "0512.prime-review/06.18.md (05.10 correction required); 0512/05.11 not reviewed",
     "files": "PENDING"},
    {"id": "I", "role": "N5 copied-book instance binding", "status": "pending", "review": "0420.prime-desk/06.48.md; 0522/05.16 not reviewed", "files": "PENDING"},
    {"id": "R", "role": "reporter observing the combined workbook chain", "status": "pending", "review": "06.19.review / 06.20.review obligations; not assigned", "files": "PENDING"},
    {"id": "W", "role": "combined workbook + door + dispatcher", "status": "pending", "review": "not built; waits for K", "files": "PENDING"},
]
JUDGMENTS = [
    {"id": "j-0512-0509", "page": "0512.prime-review", "pass": "05.09", "expected_sources": 29, "review": "0512/06.16",
     **frozen("00.kernel/00.00.10.work/0512.prime-review/evidence/prime-review05.09/core-review/judgment.json")},
    {"id": "j-0522-0514", "page": "0522.review-construction", "pass": "05.14", "expected_sources": 20, "review": "0522/06.31",
     **frozen("00.kernel/00.00.10.work/0522.review-construction/evidence/prime-review05.14/core-review/judgment.json")},
    {"id": "j-0512-0510", "page": "0512.prime-review", "pass": "05.10", "expected_sources": 44, "review": "0512/06.18; 0420/06.49 (use judgment-open.json)",
     **frozen("00.kernel/00.00.10.work/0512.prime-review/evidence/prime-review05.10/core-review/judgment-open.json")},
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--candidate-root")
    ap.add_argument("--name")
    ap.add_argument("--combined", action="store_true")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    if a.combined:
        cand = "PENDING"
        deps = DEPENDENCIES
    else:
        root = Path(a.candidate_root)
        c = json.loads((root / "CANDIDATE.json").read_bytes())
        cand = {"name": a.name, "kind": c["kind"], "candidate_json_sha256": sha_file(root / "CANDIDATE.json"), "files": c["files"],
                "lab_differences": c["lab_differences"],
                "open_entry": "labs/n7-local-lifecycle-pass01/workbook.py" if c["kind"] == "proto-l" else None}
        deps = DEPENDENCIES
    doc = {"schema": "harness-inputs/1", "made_for": "0707/05.21",
           "candidate": cand, "dependencies": deps,
           "fixture_source": frozen(f"{PAGE}/evidence/pack05.21/source-manifest.json"),
           "judgments": JUDGMENTS}
    Path(a.out).write_text(json.dumps(doc, indent=1) + "\n", encoding="utf-8")
    print(a.out, hashlib.sha256(Path(a.out).read_bytes()).hexdigest())


if __name__ == "__main__":
    main()
