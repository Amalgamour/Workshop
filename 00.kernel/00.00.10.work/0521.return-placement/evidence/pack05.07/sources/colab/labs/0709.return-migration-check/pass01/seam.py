#!/usr/bin/env python3
"""0709 pass01: seam check of real return_lines descriptors against frozen review-loop pass03 (NONPRODUCTION).

On the disposable rehearsal book only. For each descriptor (a new N5NN capture and a
relocated legacy record), writes an explicit SUPPLIED fixture (registration, request,
assignment, note, PENDING review page) under the book and runs
`labs/review-loop-pass03/review_loop.py prepare` directly (not the app). Records the
observation; infers no task association from custody.
usage: seam.py --book ABS --evidence ABS(new) --lookups ABS(rehearse evidence dir)
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

sys.dont_write_bytecode = True
CHECKOUT = Path(r"D:\Git\lib-build")
LOOP = CHECKOUT / "labs" / "review-loop-pass03" / "review_loop.py"
LOOP_PIN = ("47f47d16426e4d69987398a8244877de58b6089326874f3279003f696814450b", 55474)
EXAMPLE = CHECKOUT / "labs" / "prime-entry-pilot-pass01" / "example-registration.json"
PENDING = (b"# SYNTHETIC PENDING review target - 0709 seam check\nDisposable copy only.\n\n"
           b"## Return pointer\nPENDING.\n\n## Review - Codex Prime\nPENDING.\n")


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def fixture(book: Path, label: str, descriptor: dict) -> str:
    base = book / "seam-fixtures" / label
    base.mkdir(parents=True, exist_ok=False)
    rel = f"seam-fixtures/{label}"
    (base / "descriptor.json").write_bytes((json.dumps(descriptor, indent=2, sort_keys=True) + "\n").encode("utf-8"))
    (base / "assignment.txt").write_bytes(f"SYNTHETIC assignment for the 0709 seam check ({label}).\n".encode())
    (base / "note.md").write_bytes(f"SYNTHETIC note for the 0709 seam check ({label}).\n".encode())
    origin = descriptor["origin"]
    target = f"{origin['page']}/{origin['batch']}.md"
    page = book / Path(*target.split("/"))
    page.parent.mkdir(parents=True, exist_ok=True)
    if not page.exists():
        page.write_bytes(PENDING)
    reg = json.loads(EXAMPLE.read_text(encoding="utf-8"))
    reg.update({
        "assignment_path": f"{rel}/assignment.txt", "descriptor_path": f"{rel}/descriptor.json",
        "evidence": [{"label": "supplied", "logical_path": f"{rel}/note.md"}],
        "kernel_page": f"00.kernel/{origin['book']}/{target}", "page_id": origin["page"], "pass": origin["batch"],
        "submission_id": descriptor["submission_id"], "target": target, "source_kind": "N5NN",
        "task_id": f"seam-0709-{label}-task", "work_id": f"seam-0709-{label}",
    })
    reg["agreement"]["recorded_decisions"] = []
    reg["agreement"]["goal"] = f"SYNTHETIC: check the descriptor seam for {label}."
    reg["goal"]["statement"] = reg["agreement"]["goal"]
    reg["goal"]["goal_id"] = f"g-seam-0709-{label}"
    (base / "registration.json").write_bytes((json.dumps(reg, indent=2, sort_keys=True) + "\n").encode("utf-8"))
    (base / "request.json").write_bytes((json.dumps({"registration_path": f"{rel}/registration.json", "schema": "review-loop-request/1"}) + "\n").encode())
    return f"{rel}/request.json"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--book", required=True)
    ap.add_argument("--evidence", required=True)
    ap.add_argument("--lookups", required=True)
    args = ap.parse_args()
    data = LOOP.read_bytes()
    if (sha(data), len(data)) != LOOP_PIN:
        raise SystemExit("refused: review-loop pass03 differs from its pin")
    book, ev, lk = Path(args.book), Path(args.evidence), Path(args.lookups)
    ev.mkdir(parents=True, exist_ok=False)
    cases = {
        "new-n5nn-0504-0521": json.loads((lk / "synthetic-descriptor.json").read_text(encoding="utf-8")),
        "relocated-0101": json.loads((lk / "lookup-0101.json").read_text(encoding="utf-8"))["descriptor"],
    }
    rows = []
    for label, desc in cases.items():
        request = fixture(book, label, desc)
        argv = [sys.executable, "-B", str(LOOP), "prepare", "--fixture-root", str(book), "--request", request]
        p = subprocess.run(argv, cwd=str(CHECKOUT), capture_output=True, timeout=300, env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1"))
        (ev / f"{label}.prepare.stdout").write_bytes(p.stdout)
        (ev / f"{label}.prepare.stderr").write_bytes(p.stderr)
        body = json.loads(p.stdout) if p.stdout.strip() else {}
        obs = body.get("observation") or (body.get("view") or {}).get("observation") or {}
        rows.append({"label": label, "argv": argv, "exit": p.returncode, "stdout_sha256": sha(p.stdout), "stderr_sha256": sha(p.stderr),
                     "descriptor": {k: desc.get(k) for k in ("schema", "custody_format", "target_page", "custody_path", "return_path", "receipt_path", "route", "origin")},
                     "pass_state": body.get("pass_state"), "rule": body.get("rule"),
                     "observation": {k: obs.get(k) for k in ("state", "reason", "custody_verified", "member", "custody_member", "task_association", "placement_status", "descriptor_state")},
                     "template_offered": isinstance((body.get("view") or {}).get("template"), dict),
                     "stderr_tail": p.stderr.decode("utf-8", "replace")[-400:]})
    (ev / "seam.json").write_text(json.dumps({"schema": "0709-seam-check/1", "loop_pin": LOOP_PIN, "rows": rows}, indent=2) + "\n", encoding="utf-8")
    for r in rows:
        print(r["label"], "exit", r["exit"], r["pass_state"], json.dumps(r["observation"])[:300], r["rule"], r["stderr_tail"][-200:])
    return 0


if __name__ == "__main__":
    sys.exit(main())
