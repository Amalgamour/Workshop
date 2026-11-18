#!/usr/bin/env python3
"""SYNTHETIC examples for pass02, built in memory (and optionally written for reading).

Not review jobs. Page 0799.synthetic-reserved and commit 1111... are fictitious.
Every hash is the real sha256 of synthetic bytes defined here. The trusted maps imitate
handoff_check output shape; they were not produced by it.
usage: examples.py --write DIR   (DIR must not exist)
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
import workflow_model as W  # noqa: E402

BOOK, PAGE, COMMIT = "00.00.10.work", "0799.synthetic-reserved", "1" * 40
B = "00.kernel/00.00.10.work/0599.synthetic-build/"
SOURCES = {
    B + "05.01.md": b"SYNTHETIC requirement: the widget refuses an empty name.\n",
    B + "widget.py": b"# SYNTHETIC artifact under test\ndef make(name):\n    return name\n",
    B + "AUTHORITY.md": b"SYNTHETIC authority limits: the reviewer reads and reports only.\n",
    B + "06.01.md": b"SYNTHETIC builder reasoning: empty names are filtered upstream.\n",
}
FIRST_RETURN_LF = (
    "# SYNTHETIC first return (independent stage)\n\n"
    "```reserved-findings\n"
    '{"schema": "reserved-findings/1", "stage": "independent",\n'
    ' "reviewer": {"model": "unknown", "family": "unknown", "session": "new", "exposure": ["launched packet only"]},\n'
    ' "findings": [{"id": "R01", "claim": "make() returns an empty name.", "evidence": ["widget.py:3"]},\n'
    '              {"id": "R02", "claim": "No test covers the empty name.", "evidence": []},\n'
    '              {"id": "R03", "claim": "The requirement does not say who filters.", "evidence": ["05.01.md"]}]}\n'
    "```\n"
).encode("utf-8")
SECOND_RETURN_LF = (
    "# SYNTHETIC second return (informed stage)\n\n"
    "```reserved-reconciliation\n"
    '{"schema": "reserved-reconciliation/1", "stage": "informed",\n'
    ' "exposure_added": ["06.01.md", "05.01.return.md"],\n'
    ' "dispositions": [\n'
    '  {"finding": "R01", "status": "different-conditions", "reason": "holds only if callers do not filter", "evidence": ["06.01.md"]},\n'
    '  {"finding": "R02", "status": "confirmed", "reason": "", "evidence": []},\n'
    '  {"finding": "R03", "status": "unresolved", "reason": "builder and requirement disagree on who filters", "evidence": []}],\n'
    ' "agreements": ["make() itself does not refuse"],\n'
    ' "disagreements": ["whether the requirement binds make() or its callers"],\n'
    ' "unique": [{"id": "U01", "origin": "builder", "observation": "an upstream filter exists", "evidence": ["06.01.md"]}]}\n'
    "```\n"
).encode("utf-8")


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def dump(v) -> bytes:
    return (json.dumps(v, indent=2, sort_keys=True) + "\n").encode("utf-8")


def row(path, data, role, targets, n):
    return {"source_path": path, "snapshot": f"package/snapshots/{n:04d}.blob", "sha256": sha(data), "bytes": len(data), "targets": targets, "role": role}


def build(first_return: bytes = FIRST_RETURN_LF) -> dict:
    """The whole synthetic scenario, recomputed from the given first-return bytes."""
    req, art, auth, ctx = B + "05.01.md", B + "widget.py", B + "AUTHORITY.md", B + "06.01.md"
    common = {
        "trigger": {"kind": "pre-release-testing", "named_by": "Codex Prime (SYNTHETIC)", "statement": "SYNTHETIC readiness check."},
        "question": "SYNTHETIC: does make() meet its requirement?",
        "artifact_cut": {"repository": "workshop", "commit": COMMIT,
                         "targets": [{"id": "T01", "path": art, "sha256": sha(SOURCES[art]), "bytes": len(SOURCES[art])}]},
        "environment": {"os": "unknown", "python": "3.14.0"},
        "requirements": [{"path": req, "sha256": sha(SOURCES[req]), "why": "the requirement"}],
        "authority_limits": [{"path": auth, "sha256": sha(SOURCES[auth])}],
        "builder_context": [{"path": ctx, "sha256": sha(SOURCES[ctx]), "kind": "reasoning"}],
        "unavailable": [{"item": "builder chat transcript", "reason": "not retained"}],
        "reviewer_assignment": {"model": "unknown", "family": "unknown", "session": "new", "prior_involvement": "none declared"},
        "builder_identity": {"model": "claude-opus-5-5", "family": "Claude"},
    }
    d1 = {"schema": "reserved-review/2", "investigation": {"book": BOOK, "page": PAGE, "pass": "05.01"},
          "stage": "independent", "first_pass": None, "first_return": None, **common}
    d1_raw = dump(d1)
    d1_path = f"00.kernel/{BOOK}/{PAGE}/evidence/reserved05.01.json"
    digest1 = sha(b"SYNTHETIC package 05.01")
    rec = W.open_page(BOOK, PAGE, "05.01")
    rec = W.attach(rec, "05.01", digest1)
    rec = W.seal_return_local(rec, "05.01", first_return, "SYNTHETIC: pasted by Prime from the reviewer's chat")
    rec = W.review(rec, "05.01", "request-next", "05.02", b"SYNTHETIC interim review: request 05.02; findings not dispositioned.\n")
    rec = W.open_pass(rec, "05.02")
    seal = [t for t in rec["transitions"] if t["action"] == "seal-return"][0]
    d2 = {"schema": "reserved-review/2", "investigation": {"book": BOOK, "page": PAGE, "pass": "05.02"},
          "stage": "informed", "first_pass": "05.01",
          "first_return": {"pass": "05.01", "return_sha256": sha(first_return), "return_bytes": len(first_return),
                           "package_digest": digest1, "seal_seq": seal["seq"], "seal_transition_sha256": seal["sha256"]},
          **common}
    d2_raw = dump(d2)
    d2_path = f"00.kernel/{BOOK}/{PAGE}/evidence/reserved05.02.json"
    fr_path = f"00.kernel/{BOOK}/{PAGE}/05.01.return.md"
    digest2 = sha(b"SYNTHETIC package 05.02")
    t1 = {"digest": digest1, "investigation": d1["investigation"], "source_map": [
        row(art, SOURCES[art], "target", ["T01"], 1), row(req, SOURCES[req], "required", [], 2),
        row(auth, SOURCES[auth], "required", [], 3), row(d1_path, d1_raw, "required", [], 4)]}
    t2 = {"digest": digest2, "investigation": d2["investigation"], "source_map": [
        row(art, SOURCES[art], "target", ["T01"], 1), row(req, SOURCES[req], "required", [], 2),
        row(auth, SOURCES[auth], "required", [], 3), row(d2_path, d2_raw, "required", [], 4),
        row(ctx, SOURCES[ctx], "required", [], 5), row(fr_path, first_return, "required", [], 6)]}
    producer1 = {"schema": "colab-support-report/2", "command": "verify", "result": "intact", "digest": digest1,
                 "investigation": d1["investigation"], "findings": []}
    handoff1 = {"result": "valid", "trusted": t1}
    return {
        "d1": d1, "d1_raw": d1_raw, "d2": d2, "d2_raw": d2_raw, "t1": t1, "t2": t2,
        "digest1": digest1, "digest2": digest2, "producer1": producer1, "handoff1": handoff1,
        "request1": {"withheld": [{"item": ctx, "reason": "builder reasoning, withheld until first findings are sealed"}]},
        "binding1": {"targets": [{"id": "T01", "source": {"commit": COMMIT}}]},
        "record": rec, "first_return": first_return, "second_return": SECOND_RETURN_LF,
    }


def main() -> int:
    if len(sys.argv) != 3 or sys.argv[1] != "--write":
        print("usage: examples.py --write DIR", file=sys.stderr)
        return 2
    out = Path(sys.argv[2])
    out.mkdir(parents=True, exist_ok=False)
    s = build()
    files = {
        "descriptor-05.01-independent.json": s["d1_raw"], "descriptor-05.02-informed.json": s["d2_raw"],
        "05.01.return.SYNTHETIC.md": s["first_return"], "05.02.return.SYNTHETIC.md": s["second_return"],
        "05.01.return.SYNTHETIC.crlf.md": s["first_return"].replace(b"\n", b"\r\n"),
        "page-record.SYNTHETIC.json": dump(s["record"]), "trusted-05.01.json": dump(s["t1"]), "trusted-05.02.json": dump(s["t2"]),
        "producer-verify-05.01.json": dump(s["producer1"]),
        "README.md": b"# SYNTHETIC pass02 examples - not review jobs\nGenerated by ../examples.py. Fictitious page, commit and package digests. The page record models the PROPOSED workflow connectors; no real workflow produced it.\n",
    }
    for name, data in files.items():
        (out / name).write_bytes(data)
    print("wrote", len(files))
    return 0


if __name__ == "__main__":
    sys.exit(main())
