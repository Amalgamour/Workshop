#!/usr/bin/env python3
"""#06 write the minimal replay index (0707/05.18). NONPRODUCTION.

Reads the ROOT-INDEX.json of the matrix02 roots (what was actually copied, with hashes) and the matrix02 results,
and writes bundle/INDEX.json: one combined root (four fixtures) as a list of {path, sha256, bytes, from}, where
`from` names a file in the live checkout (read-only), a pack05.18 snapshot, or a lab candidate/adapter file.
Expected results are root-independent (rows_sha, cuts_sha, row_count, measurement, finding codes); intake_id
includes the book path and is NOT expected to match across roots.
usage: bundle.py --matrix MATRIX.json --out INDEX.json
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
import rie  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--matrix", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    m = json.loads(Path(a.matrix).read_text(encoding="utf-8"))
    frozen = rie.pack18()
    files, expected = {}, {}
    for key, fx in m["fixtures"].items():
        idx = json.loads((Path(fx["root"]) / "ROOT-INDEX.json").read_text(encoding="utf-8"))
        for c in idx["copied"]:
            if c["path"] == "app/librarian.py":
                continue
            if c["source"] == "live":
                src = f"live:{c['path']}"
            elif c["source"] == "pack05.18-snapshot":
                src = f"snapshot:{rie.PACK18.relative_to(rie.LIVE).as_posix()}/{frozen[c['path']]['snapshot']}"
            elif c["path"] == "app/review_loop_tools_v8.py":
                src = "lab:labs/review-entry-integration-pass01/candidate/app/review_loop_tools_v8.py"
            elif c["path"] == "app/review-loop-v8.json":
                src = "lab:labs/review-entry-integration-pass01/adapter/review-loop-v8.lab.json"
            elif c["path"] == "labs/workbook-review-pass04/workbook.py":
                src = "lab:labs/review-entry-integration-pass01/adapter/workbook-pass04.lab.py"
            else:
                raise SystemExit(f"unknown source {c}")
            entry = {"path": c["path"], "sha256": c["sha256"], "bytes": c["bytes"], "from": src}
            if c["path"] in files and files[c["path"]]["sha256"] != c["sha256"]:
                raise SystemExit(f"conflict {c['path']}")
            files[c["path"]] = entry
        s = fx["steps"]["C-prepare"]
        expected[key] = {k: s[k] for k in ("measurement", "row_count", "rows_sha", "cuts_sha", "finding_codes", "kind")} | \
            {"source": fx["fixture"]["page"], "pass": fx["fixture"]["pass"]}
    cand = (rie.CAND / "app/librarian.py").read_bytes()
    files["app/librarian.py"] = {"path": "app/librarian.py", "sha256": rie.sha(cand), "bytes": len(cand),
                                 "from": "lab:labs/review-entry-integration-pass01/candidate/app/librarian.py"}
    out = {"schema": "rie-replay-index/1", "made_from": a.matrix, "live_root": str(rie.LIVE), "book": rie.BOOK_REL,
           "note": "Build ONE root from these files, verify every sha256, run <root>/app/librarian.py review-loop prepare per fixture, "
                   "compare with expected. intake_id is book-path dependent and is not compared.",
           "files": sorted(files.values(), key=lambda e: e["path"]), "expected": expected}
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    Path(a.out).write_text(json.dumps(out, indent=1) + "\n", encoding="utf-8")
    print(len(files), "files;", list(expected))
    return 0


if __name__ == "__main__":
    sys.exit(main())
