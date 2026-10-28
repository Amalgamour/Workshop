"""Run the disposable rehearsal once and write the retained evidence.

The directories are removed before this process exits. results.json keeps the
raw outputs, hashes, and byte comparisons. This demo is custody only.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path


sys.dont_write_bytecode = True
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"

sys.path.insert(0, str(Path(__file__).resolve().parent))
import rehearse  # noqa: E402


EVIDENCE = (
    rehearse.REPO
    / "00.kernel/00.00.10.work/0504.app-entry/evidence/flow05.19/results.json"
)


def main() -> int:
    report = rehearse.build_evidence()
    rehearse.write_evidence(EVIDENCE, report)
    complete = report["cases"]["complete"]
    identities = complete["identities"]
    text = complete["handoff"]["text"]
    for line in text.splitlines():
        if line in ("result complete", "not approved", "not accepted", "not published"):
            print(line, flush=True)
    repetition = report["cases"]["repetition"]["handoff"]["text"]
    for line in repetition.splitlines():
        if line == "writes none":
            print(line, flush=True)
    print(f"event {identities['returned_event_sha256']}", flush=True)
    print(f"receipt {identities['receipt_sha256']}", flush=True)
    print(f"report {identities['report_sha256']}", flush=True)
    print("demo is custody only", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
