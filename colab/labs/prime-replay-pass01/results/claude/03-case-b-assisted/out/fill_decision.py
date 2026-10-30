"""Fill the case B template's attribution and judgment with my own review (run 03). Mechanical binding is left as read.
usage: python -B fill_decision.py TEMPLATE OUT"""
import json, sys
from pathlib import Path

t = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
t["attribution"] = {"actor_label": "Claude Colab (claude-opus-5-5), replay run 03", "role": "prime",
                    "evidence": "Lab replay judgment; the reviewer used review_packet as a pinned dependency elsewhere; label is not authentication."}
page = t["binding"]["page"]
j = t["judgment"]
j.update(
    outcome="complete", disposition="accepted", pass_terminal="finished",
    finding=("The mechanical review-packet helper does what 0514 05.01 asks: strict explicit request, pinned custody subprocess, "
             "git-blob versus live distinction, artifact-manifest/1 row classes without 'corruption', unsupported schemas reported, "
             "fixed non-acceptance statement, bounded exclusive output with partial status. Claims reproduced: 10 tests, 1 skip (file "
             "symlink, WinError 1314), 0 failures; custody complete; 19/19 own artifact rows historical-match."),
    reasons=["subject tests re-run in the disposable copy: Ran 10, OK (skipped=1)",
             "packet custody via the pinned inspector/helper: complete, receipt bf8cef9f..., 7 payloads",
             "direct assemble with the 0514 artifact-manifest at the disposable commit: 19 historical-match, no conflicts",
             "frozen assistance review_packet equals the subject bytes (f658cbe4...)"],
    source_refs=[page, "00.kernel/00.00.10.work/0167.review-packet-0501/return.md",
                 "00.kernel/00.00.10.work/0514.review-packet/evidence/build05.01/CONTRACT.md",
                 "00.kernel/00.00.10.work/0514.review-packet/evidence/build05.01/REAL-USE.md",
                 "labs/review-packet-pass01/review_packet.py", "labs/review-packet-pass01/tests/test_review_packet.py"],
    next_action=None,
    unresolved=["file-symlink refusal is implemented but untested on this host (privilege)",
                "pack #04 both forbids opening Claude's uncommitted benchmark work and asks to explain differing live bytes; the builder hashed live rows without copying them, disclosed"],
    semantic_conflict=False, design_fork=None, holds=[], answers=[])
j["goal"].update(terminal="completed", evidence=[page, "00.kernel/00.00.10.work/0167.review-packet-0501/receipt.json",
                                                 "00.kernel/00.00.10.work/0514.review-packet/evidence/build05.01/REAL-USE.md"])
j["sections"].update(
    outcome_evidence="Tool, tests, contract and two real specimens exist; claims reproduced in a disposable copy.",
    limits="Lab replay; file-symlink test skipped; no OS sandbox or race guarantee (as the tool states).",
    tests_note="Subject tests re-run here; tests are evidence of mechanics, not of review quality.",
    learning="A mechanical packet shows custody and artifact rows well; review substance still needs the page, contract and code.",
    preservation="Member 0167, specimens and requests unchanged; no repair or overwrite.",
    remaining_choices=["Whether callers (for example prime_cycle packet) should request artifact checks by default is a caller design question."],
    findings_account=[{"finding_id": f"{page}#F-01", "status": "accepted"}],
    finish_assessments=[{"criterion_id": "faithful-review", "assessment": "met"}])
Path(sys.argv[2]).write_text(json.dumps(t, indent=1), encoding="utf-8")
print("written", sys.argv[2])
