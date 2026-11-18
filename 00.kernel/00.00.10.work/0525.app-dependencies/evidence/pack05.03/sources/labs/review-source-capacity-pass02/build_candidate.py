#!/usr/bin/env python3
"""Materialize the uninstalled 64-source candidate. Does not edit the active app or pass01."""

from __future__ import annotations

import hashlib
import json
import os
import shutil
import sys
from pathlib import Path

sys.dont_write_bytecode = True
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"

ROOT = Path(r"D:\Git\lib-build")
LAB = ROOT / "labs" / "review-source-capacity-pass02"
CANDIDATE = LAB / "candidate"
WORK = ROOT / "00.kernel" / "00.00.10.work"
MANIFESTS = (
    WORK / "0512.prime-review" / "evidence" / "build05.09" / "artifact-manifest.json",
    WORK / "0522.review-construction" / "evidence" / "build05.14" / "artifact-manifest.json",
    WORK / "0512.prime-review" / "evidence" / "build05.10" / "artifact-manifest.json",
)
PINS = (
    "app/review_loop_tools_v4.py",
    "app/review-loop-v4.json",
    "app/review_loop_tools_v5.py",
    "app/review-loop-v5.json",
    "app/review_loop_tools_v6.py",
    "app/review-loop-v6.json",
    "app/review_loop_tools_v7.py",
    "app/review-loop-v7.json",
    "labs/review-construction-pass04/construct.py",
    "labs/review-loop-pass03/review_loop.py",
    "labs/return-access-pass01/return_access.py",
    "labs/prime-cycle-pass03/prime_cycle.py",
    "labs/prime-review-pass02/prime_review.py",
    "labs/workbook-review-pass01/workbook.py",
    "labs/workbook-review-pass01/forms/workbook-review-v1.json",
    "labs/workbook-review-pass02/workbook.py",
    "labs/workbook-review-pass02/forms/workbook-review-v1.json",
    "labs/workbook-review-pass03/workbook.py",
    "labs/workbook-review-pass03/forms/workbook-review-v1.json",
    "labs/review-source-capacity-pass01/prime_review.py",
)
TOOLS = {
    "construct_pass04": "labs/review-construction-pass04/construct.py",
    "form": "labs/workbook-review-pass03/forms/workbook-review-v1.json",
    "form_pass01": "labs/workbook-review-pass01/forms/workbook-review-v1.json",
    "form_pass02": "labs/workbook-review-pass02/forms/workbook-review-v1.json",
    "prime_cycle_pass03": "labs/prime-cycle-pass03/prime_cycle.py",
    "prime_review_capacity": "labs/review-source-capacity-pass02/prime_review.py",
    "prime_review_pass02": "labs/prime-review-pass02/prime_review.py",
    "return_access": "labs/return-access-pass01/return_access.py",
    "review_loop": "labs/review-loop-pass03/review_loop.py",
    "review_loop_v4": "app/review_loop_tools_v4.py",
    "review_loop_v4_json": "app/review-loop-v4.json",
    "review_loop_v5": "app/review_loop_tools_v5.py",
    "review_loop_v5_json": "app/review-loop-v5.json",
    "review_loop_v6": "app/review_loop_tools_v6.py",
    "review_loop_v6_json": "app/review-loop-v6.json",
    "review_loop_v7": "app/review_loop_tools_v7.py",
    "review_loop_v7_json": "app/review-loop-v7.json",
    "workbook": "labs/review-source-capacity-pass02/workbook.py",
    "workbook_pass01": "labs/workbook-review-pass01/workbook.py",
    "workbook_pass02": "labs/workbook-review-pass02/workbook.py",
    "workbook_pass03": "labs/workbook-review-pass03/workbook.py",
    "capacity_pass01": "labs/review-source-capacity-pass01/prime_review.py",
}
NOTE = (
    "05.11 source-capacity candidate. Workbook commands use the pass02 lab adapter. "
    "The historical prime_review pass02 pin stays declared and is not the module record executes. "
    "capacity_pass01 is the untouched 32-source successor. This declaration is not installed."
)
PRIOR_SHA = "a12b88958dcf2aea0fdc4c83f30c245b0f7f91d6ddf7c515bf31c7119c01fa87"


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def lf_write(path: Path, data: bytes) -> bytes:
    fixed = data.replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(fixed)
    return fixed


def code_artifacts() -> list[str]:
    found = []
    seen = set()
    for manifest in MANIFESTS:
        document = json.loads(manifest.read_text(encoding="utf-8"))
        for item in document["files"]:
            rel = item["path"]
            if not isinstance(rel, str) or rel.startswith("00.kernel/") or rel in seen:
                continue
            live = ROOT / rel
            data = live.read_bytes()
            if item.get("sha256") != sha(data) or item.get("bytes") != len(data):
                print(f"dependency conflict {rel}", file=sys.stderr)
                print(f"declared {item.get('sha256')} {item.get('bytes')}", file=sys.stderr)
                print(f"live {sha(data)} {len(data)}", file=sys.stderr)
                raise SystemExit(2)
            seen.add(rel)
            found.append(rel)
    return found


def main() -> int:
    extras = code_artifacts()
    if CANDIDATE.exists():
        shutil.rmtree(CANDIDATE)
    CANDIDATE.mkdir(parents=True)
    copied = []
    for rel in list(PINS) + extras:
        src = ROOT / rel
        dest = CANDIDATE / rel
        if dest.exists():
            continue
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src, dest)
        copied.append(rel)
    own = {
        "labs/review-source-capacity-pass02/prime_review.py": LAB / "prime_review.py",
        "labs/review-source-capacity-pass02/workbook.py": LAB / "workbook.py",
        "app/review_loop_tools_source_capacity_v2.py": LAB / "review_loop_tools_source_capacity_v2.py",
    }
    for rel, src in own.items():
        fixed = lf_write(CANDIDATE / rel, src.read_bytes())
        lf_write(src, fixed)
    successor = (CANDIDATE / "labs/review-source-capacity-pass02/prime_review.py").read_bytes()
    adapter = (CANDIDATE / "labs/review-source-capacity-pass02/workbook.py").read_bytes()
    if sha(successor).encode("ascii") not in adapter or str(len(successor)).encode("ascii") not in adapter:
        print("adapter pin does not name the successor bytes", file=sys.stderr)
        raise SystemExit(2)
    prior = (CANDIDATE / "labs/review-source-capacity-pass01/prime_review.py").read_bytes()
    if sha(prior) != PRIOR_SHA:
        print("pass01 successor copy drifted", file=sys.stderr)
        raise SystemExit(2)
    librarian = (ROOT / "app" / "librarian.py").read_bytes()
    first = b"to the pinned v7 door."
    second = b'review_loop_tools_v7.py", "librarian_review_loop_tools_v7"'
    if librarian.count(first) != 1 or librarian.count(second) != 1:
        print("active librarian delta anchors moved", file=sys.stderr)
        raise SystemExit(2)
    if sha(librarian) != "c3a5be3b612c021d95effaa5da4a151bf89026422b94f4cad98331014c7f0cd9":
        print("active librarian hash drifted", file=sys.stderr)
        raise SystemExit(2)
    edited = librarian.replace(first, b"to the pinned source-capacity-64 door.", 1).replace(
        second,
        b'review_loop_tools_source_capacity_v2.py", "librarian_review_loop_source_capacity_v2"',
        1,
    )
    (CANDIDATE / "app" / "librarian.py").write_bytes(edited)
    tools = {}
    for name, rel in sorted(TOOLS.items()):
        data = (CANDIDATE / rel).read_bytes()
        tools[name] = {"bytes": len(data), "path": rel, "sha256": sha(data)}
    tools["candidate_app"] = {"bytes": len(edited), "path": "app/librarian.py", "sha256": sha(edited)}
    document = {
        "_note": NOTE,
        "schema": "review-loop-source-capacity/2",
        "tools": tools,
        "version": 1,
    }
    payload = (json.dumps(document, indent=2, sort_keys=True) + "\n").encode("utf-8")
    (CANDIDATE / "app" / "review-loop-source-capacity-v2.json").write_bytes(payload)
    (LAB / "review-loop-source-capacity-v2.json").write_bytes(payload)
    if (CANDIDATE / "00.kernel").exists():
        print("candidate root contains the work book", file=sys.stderr)
        raise SystemExit(2)
    receipt = {
        "candidate": str(CANDIDATE),
        "code_artifacts": extras,
        "copied_historical": copied,
        "helper": str(ROOT),
        "librarian_bytes": len(edited),
        "librarian_sha256": sha(edited),
        "successor_bytes": len(successor),
        "successor_sha256": sha(successor),
    }
    (LAB / "candidate-build.json").write_bytes((json.dumps(receipt, indent=2, sort_keys=True) + "\n").encode("utf-8"))
    print(f"candidate {CANDIDATE}")
    print(f"successor {sha(successor)} {len(successor)}")
    print(f"librarian {sha(edited)} {len(edited)}")
    print(f"declaration {sha(payload)} {len(payload)}")
    print(f"files {sum(1 for _ in CANDIDATE.rglob('*') if _.is_file())}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
