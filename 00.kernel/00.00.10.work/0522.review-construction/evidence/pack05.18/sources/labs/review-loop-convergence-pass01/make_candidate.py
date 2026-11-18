#!/usr/bin/env python3
"""Build the unselected convergence candidate from the active dispatcher.

The active app/librarian.py stays in place. This writes
labs/review-loop-convergence-pass01/candidate/app/librarian.py and
CANDIDATE.json. Review-loop uses the canonical convergence door and
D:\\Git\\lib-build as its code root. Review-report uses this candidate
root so the reporter pin covers this copy of app/librarian.py.
"""

from __future__ import annotations

import hashlib
import json
import os
import sys
from pathlib import Path

sys.dont_write_bytecode = True
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"

REPO = Path(r"D:\Git\lib-build")
LAB = REPO / "labs" / "review-loop-convergence-pass01"
ACTIVE = REPO / "app" / "librarian.py"
ACTIVE_SHA = "c3a5be3b612c021d95effaa5da4a151bf89026422b94f4cad98331014c7f0cd9"
ACTIVE_BYTES = 12204
DEST = LAB / "candidate" / "app" / "librarian.py"

OLD_DOC = (
    "review-loop forwards workbook prepare, form, record, inspect, publish, read, and recover "
    "to the pinned v7 door. The v4 fixture commands stay on the pinned v4 door. "
    "reproduce is not an app command.\n"
)
NEW_DOC = (
    "review-loop forwards workbook prepare, form, record, inspect, publish, read, and recover "
    "to the unselected convergence door. review-report observes that same chain. "
    "Fixture commands stay on the historical v4 door. reproduce is not an app command.\n"
)
OLD_NAME = '        "review-loop",\n'
NEW_NAME = '        "review-report",\n        "review-loop",\n'
OLD_BRANCH = (
    '    if command == "review-loop":\n'
    '        door = load_module(Path(__file__).resolve().parent / "review_loop_tools_v7.py", "librarian_review_loop_tools_v7")\n'
    "        try:\n"
    "            code = door.perform(args, code_root)\n"
    "        except door.Refuse as exc:\n"
    "            stop(str(exc))\n"
    "        if type(code) is not int:\n"
    '            stop("pinned review loop returned no exit code")\n'
    "        raise SystemExit(code)\n"
)
NEW_BRANCH = (
    '    if command == "review-report":\n'
    "        report_root = Path(__file__).resolve().parent.parent\n"
    "        door = load_module(\n"
    '            Path(r"D:\\Git\\lib-build") / "labs" / "review-loop-convergence-pass01" / "review_report_tools.py",\n'
    '            "librarian_review_loop_convergence_report",\n'
    "        )\n"
    "        try:\n"
    "            code = door.perform(args, report_root)\n"
    "        except door.Refuse as exc:\n"
    "            stop(str(exc))\n"
    "        if type(code) is not int:\n"
    '            stop("pinned review report returned no exit code")\n'
    "        raise SystemExit(code)\n"
    '    if command == "review-loop":\n'
    '        code_root = Path(r"D:\\Git\\lib-build")\n'
    "        door = load_module(\n"
    '            code_root / "labs" / "review-loop-convergence-pass01" / "review_loop_tools.py",\n'
    '            "librarian_review_loop_convergence",\n'
    "        )\n"
    "        try:\n"
    "            code = door.perform(args, code_root)\n"
    "        except door.Refuse as exc:\n"
    "            stop(str(exc))\n"
    "        if type(code) is not int:\n"
    '            stop("pinned review loop returned no exit code")\n'
    "        raise SystemExit(code)\n"
)


def _sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def build() -> dict:
    data = ACTIVE.read_bytes()
    if len(data) != ACTIVE_BYTES or _sha(data) != ACTIVE_SHA or b"\r" in data:
        raise SystemExit("active librarian pin mismatch")
    text = data.decode("utf-8")
    for old, new in ((OLD_DOC, NEW_DOC), (OLD_NAME, NEW_NAME), (OLD_BRANCH, NEW_BRANCH)):
        if text.count(old) != 1:
            raise SystemExit("candidate patch did not match the active dispatcher once")
        text = text.replace(old, new, 1)
    if "review_loop_tools_v" in text and "review_loop_tools_v" in text:
        if "review_loop_tools_v" in text:
            # The historical filename must not remain. A bare version word in prose is a different string.
            if "review_loop_tools_v7.py" in text or "review_loop_tools_v9.py" in text:
                raise SystemExit("candidate dispatcher still names a versioned review-loop door file")
    out = text.encode("utf-8")
    if b"\r" in out:
        raise SystemExit("candidate dispatcher gained CR")
    DEST.parent.mkdir(parents=True, exist_ok=True)
    DEST.write_bytes(out)
    listed = {
        "path": "app/librarian.py",
        "sha256": _sha(out),
        "bytes": len(out),
    }
    document = {
        "schema": "convergence-candidate/1",
        "kind": "combined",
        "selected": False,
        "files": [listed],
        "lab_differences": [
            "review-loop loads labs/review-loop-convergence-pass01/review_loop_tools.py",
            "code root for review-loop is D:\\Git\\lib-build",
            "review-report loads labs/review-loop-convergence-pass01/review_report_tools.py",
            "review-report code root is the candidate root",
        ],
        "open_entry": "labs/review-loop-convergence-pass01/workbook.py",
    }
    target = LAB / "candidate" / "CANDIDATE.json"
    target.write_bytes((json.dumps(document, indent=2, sort_keys=True) + "\n").encode("utf-8"))
    return listed


def main() -> int:
    listed = build()
    print(f"{listed['sha256']} {listed['bytes']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
