"""Write design05.11/index.json (revised acceptance index). One-off authoring script; kept in scratch, copied into evidence for provenance."""
import hashlib
import json
import sys
from pathlib import Path

PAGE = Path(sys.argv[1])
OUT = PAGE / "evidence/design05.11/index.json"
if OUT.exists():
    sys.exit("refused: exists")
F10 = "evidence/design05.10/fixtures"
fm = json.loads((PAGE / "evidence/design05.10/fixture-manifest.json").read_text(encoding="utf-8"))
pins = {r["path"]: r["sha256"] for r in fm["files"]}


def fx(rel):
    key = f"fixtures/{rel}"
    return {"path": f"{F10}/{rel}", "sha256_frozen": pins[key]}


N = "NOT RUN"
W = "book/00.00.10.work"
STATES = ["judgment_recorded", "publication_complete", "custody_complete", "work_complete", "action_released"]

cases = [
 {"id": "A", "title": "Address intake of a thin N5NN submission; preliminary judgment without custody",
  "source": {"page": "0599.fixture-review", "pass": "05.01"},
  "fixtures": [fx(f"{W}/0599.fixture-review/05.01.md"), fx(f"{W}/0599.fixture-review/evidence/build05.01/submission.md"),
               fx(f"{W}/0599.fixture-review/evidence/build05.01/VERIFICATION.md"), fx(f"{W}/0599.fixture-review/evidence/build05.01/payload/parser.py"),
               fx(f"{W}/0599.fixture-review/evidence/build05.01/artifact-manifest.json"), fx("judgments/A.preliminary.json")],
  "variations": {
    "A-base": "binding builds a VALID artifact manifest in the copy: every listed file measured at setup, path base per the API's declared rule; recorded in the binding log as a binding adaptation, not as originally declared",
    "A-digest": "the 05.10 manifest as frozen (VERIFICATION.md digest deliberately null) — kept separate from A-base",
    "A-missing": "in the copy, delete submission.md before prepare (the Return pointer still names it)",
    "A-ambiguous": "in the copy, change the Return pointer Submission line to name two different files"},
  "expected_states": {"A-base": {"judgment_recorded": True, "publication_complete": True, "custody_complete": False, "work_complete": False, "action_released": False}},
  "assertions": [
   {"id": "A1", "v": "A-base", "status": N, "text": "The intake index shows VERIFICATION.md, the artifact manifest and payload/parser.py as inspectable evidence, not only submission.md (C14)."},
   {"id": "A2", "v": "A-digest", "status": N, "text": "The null digest is reported as a finding or missing evidence; it is not filled in, and A-base is not used to hide it (C14)."},
   {"id": "A3", "v": "A-base", "status": N, "text": "custody_complete is false. No receipt or task association is shown or written; nothing is written under a 01NN path (C16)."},
   {"id": "A4", "v": "A-base", "status": N, "text": "In a new process, read returns the recorded assessment, findings, operation and next action as supplied (C23, C28)."},
   {"id": "A5", "v": "A-base", "status": N, "text": "The supplied prose about T3 being unknown is preserved verbatim. No compute-derived summary shows T3, or the tests, as passed. Compute does not parse the prose into results (C19; 06.10 corr. 4)."},
   {"id": "A6", "v": "A-base", "status": N, "text": "work_complete and action_released are false. The review is ineligible for custody-dependent closure (C16)."},
   {"id": "A7", "v": "all", "status": N, "text": "The files under evidence/build05.01 are byte-identical before and after every operation (C28)."},
   {"id": "A8", "v": "A-base", "status": N, "text": "Compute derives an intake candidate identity, bound before the judgment, and a separate final review identity. The caller may echo a returned identity into a later operation; a fabricated or predicted identity is refused (C23; 06.10 corr. 2)."},
   {"id": "A9", "v": "A-base", "status": N, "text": "Both findings, F1 elevated and F2 answered, appear with their dispositions (C21)."},
   {"id": "A10", "v": "A-missing", "status": N, "text": "The missing return is reported as a finding. No path is guessed; no judgment target is invented; nothing is written (C14)."},
   {"id": "A11", "v": "A-ambiguous", "status": N, "text": "The ambiguous pointer is a finding. Neither file is silently chosen (C14)."}]},
 {"id": "B", "title": "N7NN same-pass successor after a Director hold; a manual predecessor is preserved or blocks",
  "source": {"page": "0799.fixture-colab", "pass": "05.01"},
  "fixtures": [fx(f"{W}/0799.fixture-colab/05.01.pack.md"), fx(f"{W}/0799.fixture-colab/05.01.return.md"),
               fx(f"{W}/0799.fixture-colab/06.01.review.md"), fx(f"{W}/0799.fixture-colab/06.02.decisions.md"), fx("judgments/B.successor.json")],
  "variations": {
    "B-tool": "prerequisite: in a copy WITHOUT 06.01.review.md, record a first review through the real API with operation director-input, question Q1 and hold D1 (content from the 05.10 06.01 text). Then add 06.02.decisions.md (SYNTHETIC Director words), then record the successor (B.successor.json) for the SAME pass 05.01",
    "B-manual": "the 05.10 copy as frozen: 06.01.review.md is a hand-written markdown review, not a tool record"},
  "expected_states": {"B-tool": {"judgment_recorded": True, "publication_complete": True, "custody_complete": "not applicable (N7NN page-local)", "work_complete": False, "action_released": False}},
  "assertions": [
   {"id": "B1", "v": "B-tool", "status": N, "text": "The successor is recorded under the same pass's review home and its bound records. The test does not expect, and the tool does not invent, a new pass number or a new review-numbering scheme. The first tool review stays preserved and distinguishable, and the successor is explicitly selected as current (C26; 06.10 corr. 1)."},
   {"id": "B2", "v": "B-tool", "status": N, "text": "The Director's words (#Q1) appear verbatim and attributed, separate from the successor's model text (C21; 06.06)."},
   {"id": "B3", "v": "B-tool", "status": N, "text": "After the successor 'continue', D1 is NOT released (action_released false). Only the Q1 hold is resolved through the declared record; any other hold remains (C36; Prime interpretation, 06.10 answer B)."},
   {"id": "B4", "v": "B-manual", "status": N, "text": "The hand-written 06.01.review.md is byte-identical afterwards. It is neither adopted as a tool review nor overwritten; publication either preserves it as a predecessor or is blocked or held (C26; 06.10 corr. 1)."},
   {"id": "B5", "v": "B-tool", "status": N, "text": "Independent item I1 is never held (director-agreement)."},
   {"id": "B6", "v": "both", "status": N, "text": "Recording executes no pack, release or worker prompt (C21, C36)."}]},
 {"id": "C", "title": "Drift after intake: selected-input change versus the tool's own pointer write versus an unselected file",
  "source": {"page": "0599.fixture-review", "pass": "05.01"},
  "fixtures": [fx(f"{W}/0599.fixture-review/05.01.md"), fx(f"{W}/0599.fixture-review/evidence/build05.01/VERIFICATION.md"), fx("judgments/A.preliminary.json")],
  "variations": {
    "C-a": "A-base copy; prepare and record; edit one word of the 05.01.md Scope body; publish",
    "C-b": "A-base copy; prepare and record; edit the T3 row of VERIFICATION.md; publish",
    "C-c": "A-base copy; prepare, record and publish normally (the tool writes its own Review-area pointer); then read and recover",
    "C-d": "A-base copy; prepare and record; add a new file 06.99.notes.md (SYNTHETIC, unrelated text) on the page; publish"},
  "expected_states": {"C-a": {"judgment_recorded": True, "publication_complete": False}, "C-b": {"judgment_recorded": True, "publication_complete": False},
                      "C-c": {"judgment_recorded": True, "publication_complete": True, "custody_complete": False, "work_complete": False, "action_released": False},
                      "C-d": {"judgment_recorded": True, "publication_complete": True}},
  "assertions": [
   {"id": "C1", "v": "C-a", "status": N, "text": "Publication is blocked or stale. The recorded judgment is unchanged; nothing is silently repinned or reapproved (C23, C28)."},
   {"id": "C2", "v": "C-b", "status": N, "text": "The same outcome for drift in selected evidence (C23)."},
   {"id": "C3", "v": "C-c", "status": N, "text": "The tool's own pointer write does not make its review stale. Publication is complete, while custody, work and release stay false or not applicable (C28; 06.10 corr. 3)."},
   {"id": "C4", "v": "C-c", "status": N, "text": "The diff of 05.01.md, before versus after, is limited to the Review - Codex Prime area. Both identities are retained (C28)."},
   {"id": "C5", "v": "C-a,C-b", "status": N, "text": "The edited bytes are left in place; the tool does not revert them."},
   {"id": "C6", "v": "C-a,C-b", "status": N, "text": "The stale state survives a new-process read and recover (C36)."},
   {"id": "C7", "v": "C-d", "status": N, "text": "An unselected new notes file is not automatically drift; publication may proceed. (Prime interpretation, 06.10 answer C: freeze the selected inputs; reconcile only if authority or selected inputs change.)"}]},
 {"id": "D", "title": "Judgment recorded; publication blocked by an existing manual Review-area text; new-process recovery",
  "source": {"page": "0599.fixture-review", "pass": "05.01"},
  "fixtures": [fx(f"{W}/0599.fixture-review/05.01.md"), fx("judgments/A.preliminary.json")],
  "variations": {"D": "A-base copy; replace 'PENDING.' in the Review - Codex Prime area with 'Manual review by hand: looks fine.' (SYNTHETIC); prepare, record, publish; end the process; new process: read, then recover"},
  "expected_states": {"D": {"judgment_recorded": True, "publication_complete": False, "custody_complete": False, "work_complete": False, "action_released": False}},
  "assertions": [
   {"id": "D1", "v": "D", "status": N, "text": "The manual text is byte-identical; it is not overwritten and not adopted as a review or an approval (C26)."},
   {"id": "D2", "v": "D", "status": N, "text": "In the new process, the exact judgment, next action and holds are returned from the tool's durable record (C23, C28)."},
   {"id": "D3", "v": "D", "status": N, "text": "publication_complete is false and is reported as incomplete; nothing reports completion (C28)."},
   {"id": "D4", "v": "D", "status": N, "text": "Removing or altering any rendered review file between processes does not change the judgment returned; the rendered file is reported as drifted or missing (C28)."}]},
 {"id": "E", "title": "Interruption between render and pointer; a changed 'completed' output",
  "source": {"page": "0599.fixture-review", "pass": "05.01"},
  "fixtures": [fx(f"{W}/0599.fixture-review/05.01.md"), fx("judgments/A.preliminary.json")],
  "variations": {
    "E-a": "A-base copy; publish, stopping after the render and before the pointer, using a SUPPORTED stop (fault hook or process kill as the API allows); new process: status, then recover. If no supported stop exists: NOT BINDABLE",
    "E-b": "A-base copy; complete a normal publish; append one line to the rendered review file; new process recover",
    "E-c": "A-base copy; complete a normal publish; edit the pointer text in the Review area; new process recover"},
  "expected_states": {"E-a": {"judgment_recorded": True, "publication_complete": "false until verified"}, "E-b": {"publication_complete": "not reported complete"}, "E-c": {"publication_complete": "not reported complete"}},
  "assertions": [
   {"id": "E1", "v": "E-a", "status": N, "text": "Before recovery, status reports publication incomplete (partial), not success (C28)."},
   {"id": "E2", "v": "E-a", "status": N, "text": "Recovery either (i) completes the pointer only after re-verifying the rendered bytes against the record, or (ii) truthfully holds with a supported next retry. Both are acceptable. Reporting complete without the verification is not. The judgment is unchanged (C28; 06.10 corr. 3)."},
   {"id": "E3", "v": "E-b", "status": N, "text": "Recovery does not report completed. It reports the rendered file as changed and does not overwrite it silently; the judgment is kept (C28 'never trusts a done label')."},
   {"id": "E4", "v": "E-c", "status": N, "text": "The same for a changed pointer area."},
   {"id": "E5", "v": "all", "status": N, "text": "The source evidence files are byte-identical in every variant."}]},
 {"id": "F", "title": "Replay, conflict, typed-field errors, required versus nullable",
  "source": {"page": "0599.fixture-review", "pass": "05.01"},
  "fixtures": [fx("judgments/A.preliminary.json"), fx("judgments/F.replay-same.json"), fx("judgments/F.replay-conflict.json")],
  "variations": {
    "F-a": "record A; record F.replay-same with the same operation identity",
    "F-b": "record F.replay-conflict with the same identity",
    "F-c": "fresh copy; pick a field the RETURNED FORM declares with a non-text type (the binding log names it) and supply a value of the wrong type",
    "F-d": "fresh copy; omit a field the returned form declares REQUIRED",
    "F-e": "fresh copy; supply explicit null or unknown for a field the returned form declares NULLABLE (if none exists: NOT BINDABLE)"},
  "note": "The 05.10 files F.wrong-type.json and F.tests-omitted.json assumed a per-test typed T3 field. They are superseded for binding (06.10 corr. 4) and preserved unchanged.",
  "assertions": [
   {"id": "F1", "v": "F-a", "status": N, "text": "No duplicate authoritative result; the same stored result is returned. Diagnostic writes are allowed (C23; 06.10 corr. 4)."},
   {"id": "F2", "v": "F-b", "status": N, "text": "Refused. The authoritative record is unchanged; the conflicting input is preserved with correction help (C23)."},
   {"id": "F3", "v": "F-c", "status": N, "text": "Refused at the named declared field, naming the expected and observed type; the input is kept; nothing is recorded (C19, C23)."},
   {"id": "F4", "v": "F-d", "status": N, "text": "Refused as missing. No default is supplied (C19)."},
   {"id": "F5", "v": "F-e", "status": N, "text": "Recorded as explicit unknown or null. It never becomes passed, empty or consent (C19; Prime interpretation, 06.10 answer F)."},
   {"id": "F6", "v": "all", "status": N, "text": "No variant changes the source files."}]},
]

idx = {"schema": "0707-05.11-acceptance-index/2",
       "note": "Revision of design05.10/index.json (preserved). Interface-neutral; every assertion NOT RUN. Fixtures are referenced by frozen path and sha256; no fixture is regenerated. Prime binds the cases to the returned API.",
       "contract": "evidence/pack05.10/sources/review-integration-contract.md (C<n> = line n)",
       "book_root": f"{F10}/book/00.00.10.work (06.10 corr. 5; 05.10 wrongly said fixtures/book)",
       "states": {s: "reported separately; never inferred from another" for s in STATES},
       "primary_hostile": ["E", "C"],
       "prime_interpretations": {"B": "continue selects the review and next action; it does not release D1 by recording; resolve only the answered hold", "C": "freeze selected source/dependency/decision/template bytes; an unselected notes file is not automatically drift", "F": "unknown never becomes passed; missing required typed fields are refused; declared nullable unknowns stay explicit"},
       "cases": cases,
       "limits": ["same address in another book instance (C14): not specified",
                  "refusal of a finding without a disposition: depends on the returned form; not specified",
                  "the 0412 per-operation report floor: not specified",
                  "filed mode: requires a fixture produced by the accepted line tool at binding; none is fabricated"]}
OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(idx, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
print("written", sum(len(c["assertions"]) for c in cases), "assertions")
