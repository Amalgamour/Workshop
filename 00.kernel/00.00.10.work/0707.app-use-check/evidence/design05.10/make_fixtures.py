#!/usr/bin/env python3
"""0707/05.10 NONPRODUCTION fixture generator and fixture checker.

Writes six tiny SYNTHETIC acceptance-case fixtures under ./fixtures, a fixture manifest, and
checks only the fixtures' own validity (files present, hashes recorded, SYNTHETIC markers,
no receipt anywhere, index references resolve). It runs NO target behavior: every target
assertion in CASES.md and index.json stays NOT RUN until Prime binds it to the real API.
usage: make_fixtures.py   (refuses to overwrite ./fixtures)
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
FX = HERE / "fixtures"
MARK = "SYNTHETIC FIXTURE — 0707/05.10 acceptance design. Not live work, not authority, not a receipt."


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def put(rel: str, text: str) -> None:
    p = FX / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(text.encode("utf-8"))


def build() -> None:
    w = "book/00.00.10.work"
    # N5NN work page; the matching N1NN line 0199.fixture-review is deliberately ABSENT (pending custody)
    put(f"{w}/0599.fixture-review/01.md", f"# Fixture review page\n{MARK}\nGoal: exercise core-managed review of a thin N5NN submission.\n")
    put(f"{w}/0599.fixture-review/05.01.md",
        f"# 05.01 - Fixture build pass\n{MARK}\nexecutor: fixture-builder\nreviewer: Codex Prime\n\n"
        "## Goal\nAdd a bounded parser and prove it with three tests.\n\n"
        "## Scope\nNew module only. No other page edits.\n\n"
        "## Return pointer\nSubmission: evidence/build05.01/submission.md\nVerification: evidence/build05.01/VERIFICATION.md\n"
        "Artifact manifest: evidence/build05.01/artifact-manifest.json\nCustody: matching 0199.fixture-review pending; not filed.\n\n"
        "## Review - Codex Prime\nPENDING.\n")
    put(f"{w}/0599.fixture-review/evidence/build05.01/submission.md",
        f"# Submission (thin)\n{MARK}\nSee VERIFICATION.md and artifact-manifest.json. Tests: see verification.\n")
    put(f"{w}/0599.fixture-review/evidence/build05.01/VERIFICATION.md",
        f"# Verification (substantive)\n{MARK}\n| test | state |\n|---|---|\n| T1 parse valid | passed |\n| T2 refuse malformed | failed (first failure kept: run 1) |\n"
        "| T3 large input | not run (unknown) |\n\nKnown limit: Windows path case not covered.\n")
    put(f"{w}/0599.fixture-review/evidence/build05.01/payload/parser.py", f"# {MARK}\ndef parse(text):\n    return text.split()\n")
    payload = (FX / f"{w}/0599.fixture-review/evidence/build05.01/payload/parser.py").read_bytes()
    put(f"{w}/0599.fixture-review/evidence/build05.01/artifact-manifest.json", json.dumps(
        {"note": MARK, "files": [{"path": "payload/parser.py", "bytes": len(payload), "sha256": sha(payload)},
                                 {"path": "VERIFICATION.md", "bytes": None, "sha256": None, "note": "listed, digest deliberately absent: a finding, not a guess"}]}, indent=1) + "\n")
    # N7NN Colab page with prior review, Director hold and reply
    put(f"{w}/0799.fixture-colab/01.md", f"# Fixture Colab page\n{MARK}\n")
    put(f"{w}/0799.fixture-colab/05.01.pack.md", f"# 05.01.pack\n{MARK}\nDesign two options for the cache.\n\n## Return pointer\nReturned: 05.01.return.md\n")
    put(f"{w}/0799.fixture-colab/05.01.return.md", f"# 05.01.return\n{MARK}\nOption 1 keeps a disk cache; option 2 recomputes. Recommendation: option 1.\n")
    put(f"{w}/0799.fixture-colab/06.01.review.md",
        f"# 06.01.review - Codex Prime (SYNTHETIC prior review)\n{MARK}\noperation: director-input\n"
        "question Q1: May the cache write outside the page evidence folder?\nhold: dependent item D1 (build the cache) waits for Q1.\n"
        "independent work: item I1 (docs) continues.\n")
    put(f"{w}/0799.fixture-colab/06.02.decisions.md",
        f"# 06.02.decisions\n{MARK}\n## Director - verbatim (SYNTHETIC)\n#Q1 Yes, but only under the page's evidence folder.\n\n"
        "## Prime - interpretation\n(none recorded yet)\n")
    # supplied judgments: semantic content only, to be transcribed into the REAL returned form by Prime
    j = {"note": MARK + " Semantic content only; field names are contract concepts, not an API.",
         "assessment": "The parser meets T1; T2 failed in run 1 and its fix is not shown; T3 not run.",
         "findings": [{"id": "F1", "text": "T2 first failure has no later passing run", "disposition": "elevated"},
                      {"id": "F2", "text": "artifact manifest lacks a digest for VERIFICATION.md", "disposition": "answered"}],
         "operation": "continue", "reasons": "Routine repair; no Director judgment needed.",
         "next_action": "Ask the builder for a T2 rerun and a VERIFICATION.md digest.",
         "tests": {"T1": "passed", "T2": "failed", "T3": "unknown"}}
    put("judgments/A.preliminary.json", json.dumps(j, indent=1) + "\n")
    put("judgments/F.replay-same.json", json.dumps(j, indent=1) + "\n")
    jc = dict(j, next_action="Close the page.")
    put("judgments/F.replay-conflict.json", json.dumps(jc, indent=1) + "\n")
    jt = json.loads(json.dumps(j))
    jt["tests"]["T3"] = "yes"
    put("judgments/F.wrong-type.json", json.dumps(jt, indent=1) + "\n")
    jo = json.loads(json.dumps(j))
    jo["tests"].pop("T3")
    put("judgments/F.tests-omitted.json", json.dumps(jo, indent=1) + "\n")
    jb = {"note": MARK + " Successor review content for case B.", "assessment": "Director answered Q1: evidence folder only.",
          "findings": [{"id": "Q1", "text": "cache location", "disposition": "answered"}],
          "operation": "continue", "reasons": "Q1 answered by the Director (06.02 #Q1) within the page evidence folder.",
          "next_action": "Prepare D1 constrained to the page evidence folder for a released pack."}
    put("judgments/B.successor.json", json.dumps(jb, indent=1) + "\n")


def check() -> dict:
    files = sorted(p for p in FX.rglob("*") if p.is_file())
    rows = [{"path": p.relative_to(HERE).as_posix(), "bytes": p.stat().st_size, "sha256": sha(p.read_bytes())} for p in files]
    problems = []
    for p in files:
        t = p.read_text(encoding="utf-8")
        if "SYNTHETIC" not in t:
            problems.append(f"{p.name}: no SYNTHETIC marker")
        if p.name.startswith("receipt") or '"receipt"' in t:
            problems.append(f"{p.name}: receipt-like content")
    if (FX / "book/00.00.10.work/0199.fixture-review").exists():
        problems.append("matching N1NN line exists; case A needs it absent")
    idx = json.loads((HERE / "index.json").read_text(encoding="utf-8"))
    for c in idx["cases"]:
        for rel in c["fixtures"]:
            if not (HERE / rel).exists():
                problems.append(f"case {c['id']}: missing fixture {rel}")
        for a in c["assertions"]:
            if a.get("status") != "NOT RUN":
                problems.append(f"case {c['id']} {a['id']}: status must be NOT RUN")
    return {"files": rows, "problems": problems}


def main() -> int:
    if FX.exists():
        sys.exit("refused: fixtures exist")
    build()
    res = check()
    (HERE / "fixture-manifest.json").write_text(json.dumps({"schema": "0707-05.10-fixture-manifest/1", "note": MARK, **res}, indent=1) + "\n", encoding="utf-8")
    print("fixture files", len(res["files"]), "problems", len(res["problems"]))
    for p in res["problems"]:
        print("PROBLEM", p)
    return 0 if not res["problems"] else 1


if __name__ == "__main__":
    sys.exit(main())
