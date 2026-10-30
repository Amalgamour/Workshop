"""Fill the case A template's attribution and judgment with my own review (run 02). Mechanical binding is left as read.
usage: python -B fill_decision.py TEMPLATE OUT"""
import json, sys
from pathlib import Path

t = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
t["attribution"] = {"actor_label": "Claude Colab (claude-opus-5-5), replay run 02", "role": "prime",
                    "evidence": "Lab replay judgment by the model that was also the original Builder of this return; label is not authentication."}
page = t["binding"]["page"]
j = t["judgment"]
j.update(
    outcome="continue", disposition="accepted", pass_terminal="finished",
    finding=("Bounded first instrument returned as specified for 05.01.002; custody intact. Against the accepted method revision "
             "(0414.bench 01.002, 0701 review F01-F04) controls are missing: no pair parity check, wording-based deterministic keys "
             "instead of commitment scoring, no candidate-package re-hash after prepare, no preparation/repair cost record."),
    reasons=["receipt/manifest/payloads and 9 declared outputs re-hashed equal (run 01, manual)",
             "prime_bench.py collect/compare never re-read candidate_files pins (code lines 785-860, 1088-1160)",
             "design-fork-a key uses must_quote of the Director sentence: a wording test the method rejects",
             "historical tests not reproducible in the frozen input: support dependency absent (unknown, not false)"],
    source_refs=[page, "00.kernel/00.00.10.work/0163.prime-bench-harness-0501/return.md",
                 "00.kernel/00.00.10.work/0414.bench/01.002.md", "00.kernel/00.00.10.work/0701.bench-method/06.01.review.md",
                 "labs/prime-bench-pass01/prime_bench.py", "labs/prime-bench-pass01/cases/design-fork-a/evaluator/key.json"],
    next_action={"action_id": "bench-controls-correction", "text": "Pack one implementation correction adding F01-F04 controls with regression cases under a new bench version (lab-only proposal).",
                 "authorized_in_grant": False},
    unresolved=["historical 32-test result not reproduced here", "isolation remains a coordinator declaration"],
    semantic_conflict=False, design_fork=None, holds=[], answers=[])
j["goal"]["terminal"] = "open"
j["sections"].update(return_result="Harness, bench, tests and docs returned; custody verified.",
                     prime_finding="Pass meets its own grant; goal not met until accepted method controls exist.",
                     within_direction="Correction lies within the declared design and the accepted method revision.",
                     next_bounded_action="One correction pack for F01-F04 with regression cases (not released).")
Path(sys.argv[2]).write_text(json.dumps(t, indent=1), encoding="utf-8")
print("written", sys.argv[2])
