#!/usr/bin/env python3
"""Write the SYNTHETIC examples for the reserved two-pass design (not review jobs).

Every hash in the examples is the real sha256 of a synthetic byte string defined
here, so nothing is a placeholder standing in for evidence. The investigation page
0799.synthetic-reserved does not exist and is not a reservation.
usage: make_examples.py   (writes examples/ next to this file; refuses if present)
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / "examples"
BOOK = "00.00.10.work"
PAGE = "0799.synthetic-reserved"
COMMIT = "1111111111111111111111111111111111111111"

SOURCES = {
    "00.kernel/00.00.10.work/0599.synthetic-build/05.01.md": "SYNTHETIC requirement: the widget refuses an empty name.\n",
    "00.kernel/00.00.10.work/0599.synthetic-build/widget.py": "# SYNTHETIC artifact under test\ndef make(name):\n    return name\n",
    "00.kernel/00.00.10.work/0599.synthetic-build/AUTHORITY.md": "SYNTHETIC authority limits: the reviewer reads and reports only.\n",
    "00.kernel/00.00.10.work/0599.synthetic-build/06.01.md": "SYNTHETIC builder reasoning: empty names are filtered upstream, so make() need not check.\n",
}
FIRST_RETURN = """# SYNTHETIC first return (independent stage) - 0799.synthetic-reserved 05.01
Not a real review. Example of the proposed block.

```reserved-findings
{"schema": "reserved-findings/1", "stage": "independent",
 "reviewer": {"model": "unknown", "family": "unknown", "session": "new", "prior_involvement": "none declared",
              "exposure": ["package digest as launched", "no builder notes"]},
 "findings": [
  {"id": "R01", "claim": "make() returns an empty name instead of refusing it.", "evidence": ["widget.py line 3", "05.01.md requirement"]},
  {"id": "R02", "claim": "No test covers the empty-name case.", "evidence": ["absence in packet"]}
 ]}
```
"""


def sha(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def row(path: str, role: str, targets: list[str], n: int) -> dict:
    data = SOURCES[path] if path in SOURCES else FIRST_RETURN
    return {"source_path": path, "snapshot": f"package/snapshots/{n:04d}.blob", "sha256": sha(data),
            "bytes": len(data.encode("utf-8")), "targets": targets, "role": role}


def main() -> int:
    if OUT.exists():
        print("refused: examples/ exists", file=sys.stderr)
        return 2
    OUT.mkdir()
    b = "00.kernel/00.00.10.work/0599.synthetic-build/"
    req, art, auth, ctx = b + "05.01.md", b + "widget.py", b + "AUTHORITY.md", b + "06.01.md"
    first_return_path = f"00.kernel/{BOOK}/{PAGE}/05.01.return.md"
    cut = {"repository": "workshop", "commit": COMMIT,
           "targets": [{"id": "T01", "path": art, "sha256": sha(SOURCES[art]), "bytes": len(SOURCES[art])}]}
    env = {"os": "unknown", "python": "3.14.0", "relevant": "standard library only"}
    common = {
        "trigger": {"kind": "pre-release-testing", "named_by": "Codex Prime (SYNTHETIC)", "statement": "SYNTHETIC: the widget is about to be tested for release."},
        "question": "SYNTHETIC: does make() meet its stated requirement?",
        "artifact_cut": cut,
        "environment": env,
        "requirements": [{"path": req, "sha256": sha(SOURCES[req]), "why": "the requirement"}],
        "authority_limits": [{"path": auth, "sha256": sha(SOURCES[auth])}],
        "builder_context": [{"path": ctx, "sha256": sha(SOURCES[ctx]), "kind": "reasoning"}],
        "unavailable": [{"item": "builder chat transcript", "reason": "not retained"}],
        "reviewer_assignment": {"model": "unknown", "family": "unknown", "session": "new", "prior_involvement": "none declared"},
        "builder_identity": {"model": "claude-opus-5-5", "family": "Claude"},
    }
    d1 = {"schema": "reserved-review/1", "investigation": {"book": BOOK, "page": PAGE, "pass": "05.01"},
          "stage": "independent", "first_pass": None, "first_return": None, **common}
    d2 = {"schema": "reserved-review/1", "investigation": {"book": BOOK, "page": PAGE, "pass": "05.02"},
          "stage": "informed", "first_pass": "05.01",
          "first_return": {"member": "01NN.synthetic-not-allocated", "return_sha256": sha(FIRST_RETURN), "receipt_sha256": sha("SYNTHETIC receipt\n")},
          **common}
    d1_text = json.dumps(d1, indent=2, sort_keys=True) + "\n"
    d2_text = json.dumps(d2, indent=2, sort_keys=True) + "\n"
    SOURCES[f"00.kernel/{BOOK}/{PAGE}/evidence/reserved05.01.json"] = d1_text
    SOURCES[f"00.kernel/{BOOK}/{PAGE}/evidence/reserved05.02.json"] = d2_text
    trusted1 = {"investigation": {"book": BOOK, "page": PAGE, "pass": "05.01"}, "source_map": [
        row(art, "target", ["T01"], 1), row(req, "required", [], 2), row(auth, "required", [], 3),
        row(f"00.kernel/{BOOK}/{PAGE}/evidence/reserved05.01.json", "required", [], 4)]}
    trusted2 = {"investigation": {"book": BOOK, "page": PAGE, "pass": "05.02"}, "source_map": [
        row(art, "target", ["T01"], 1), row(req, "required", [], 2), row(auth, "required", [], 3),
        row(f"00.kernel/{BOOK}/{PAGE}/evidence/reserved05.02.json", "required", [], 4),
        row(ctx, "required", [], 5), row(first_return_path, "required", [], 6)]}
    request1 = {"withheld": [{"item": ctx, "reason": "builder reasoning, withheld until first findings are sealed"}]}
    binding = {"targets": [{"id": "T01", "source": {"commit": COMMIT}}]}
    capture1 = {"status": "complete", "origin": {"book": BOOK, "page": PAGE, "batch": "05.01"}, "return_sha256": sha(FIRST_RETURN)}
    second = """# SYNTHETIC second return (informed stage) - 0799.synthetic-reserved 05.02
Not a real review.

```reserved-reconciliation
{"schema": "reserved-reconciliation/1", "stage": "informed",
 "reviewer": {"model": "unknown", "family": "unknown", "session": "continuing from 05.01", "prior_involvement": "the 05.01 pass"},
 "exposure_added": ["06.01.md builder reasoning", "05.01.return.md"],
 "dispositions": [
  {"finding": "R01", "status": "different-conditions", "reason": "upstream filtering is claimed in 06.01 but not in the requirement; holds only if callers filter.", "evidence": ["06.01.md", "05.01.md"]},
  {"finding": "R02", "status": "confirmed", "reason": "", "evidence": ["absence in packet"]}
 ],
 "agreements": ["make() itself does not refuse"],
 "disagreements": ["whether the requirement binds make() or its callers"],
 "unique": [{"id": "U01", "origin": "builder", "observation": "upstream filter exists", "evidence": ["06.01.md"]}]}
```
"""
    files = {
        "descriptor-05.01-independent.json": d1_text,
        "descriptor-05.02-informed.json": d2_text,
        "05.01.return.SYNTHETIC.md": FIRST_RETURN,
        "05.02.return.SYNTHETIC.md": second,
        "trusted-05.01.json": json.dumps(trusted1, indent=2, sort_keys=True) + "\n",
        "trusted-05.02.json": json.dumps(trusted2, indent=2, sort_keys=True) + "\n",
        "request-05.01-withheld.json": json.dumps(request1, indent=2, sort_keys=True) + "\n",
        "binding-05.01.json": json.dumps(binding, indent=2, sort_keys=True) + "\n",
        "capture-05.01.json": json.dumps(capture1, indent=2, sort_keys=True) + "\n",
        "README.md": "# SYNTHETIC examples - not review jobs\nGenerated by ../make_examples.py. Page 0799.synthetic-reserved, member 01NN.synthetic-not-allocated and commit 1111... are fictitious. Hashes are real hashes of the synthetic bytes defined in make_examples.py. trusted-*.json imitate handoff_check `trusted` output; they were not produced by it.\n",
    }
    for name, text in files.items():
        (OUT / name).write_bytes(text.encode("utf-8"))
    print("wrote", len(files), "files")
    return 0


if __name__ == "__main__":
    sys.exit(main())
