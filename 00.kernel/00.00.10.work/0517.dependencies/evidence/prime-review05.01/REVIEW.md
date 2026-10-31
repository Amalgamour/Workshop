# Prime review — dependency prototype 05.01
Date: 2026-10-31. Reviewer: Codex Prime.
Disposition: useful exploratory prototype retained; correction required before
workflow-completion or completeness-sensitive dependency use. Not a seated module.

## Verified facts
Prime independently ran all 15 tests: 15 passed, no skips/failures, 38.603 seconds.
All 14 artifact rows and six captured payloads match. Member 0178 freshly verifies.
The submitted nine-mutation and thirteen-step demo results are Builder evidence;
Prime did not rerun those scripts. Prime ran separate disposable graph probes.
Their exact inputs/outcomes are recorded in independent-probes.json.

## What works
Explicit declarations distinguish missing roots from stated no-requirements.
Declared requirements have conditions, code identities and full workflow links;
forward/reverse lookup and provenance are useful. Unknown and missing records in
the real prime-cycle chain remain visible. No claimed complete runtime discovery,
environment probe, command execution, model invocation or second readiness gate.
The prototype answers questions that otherwise require Prime to reread source.

## Findings before integration
D-01 — Reverse impact silently stops at --depth. For C <- B <- A, querying C at
depth 1 returns B and exit 0 with no finding, while A is omitted. Add a depth-limit
or explicit truncation record when more consumers exist. A naturally exhausted
bounded walk may be complete; don't mark every depth-1 query incomplete blindly.
Preserve shared paths/cycle handling and show affected identities and provenance.

D-02 — Module target resolution compares pin.sha256 but ignores pin.bytes. The
independent fixture names the correct target digest with length 999 while the
target declaration says length 1; result is resolved, complete, exit 0. Declared
identity inconsistency must be a finding. Check the pair consistently wherever
length is represented, without claiming the module's real bytes were measured.

D-03 — The proposed change record accepts old=null for a new module, but delta
requires --old and always opens an existing predecessor. It cannot account for
newly introduced modules, despite the completion proposal saying 'adds or changes'.
Provide an explicit creation mode with no invented predecessor: null old, no
supersedes, all initial requirements introduced with reasons/task reference.
Keep revision checks and evidence preservation. Don't rewrite the original record.

## Technical dispositions for Builder questions
Module-local declarations with a derived index align with 0316; keep this as a
prototype until reviewed integration. No production migration or seating now.
An import not enforced by the subject's own hash check may be honestly recorded
as unpinned; that is distinct from a delivery selecting and verifying exact bytes.
Do not invent a subject-enforced pin. Reproducible deliveries still need explicit
verified identities or an unknown result. Defer adapter integration to its own pass.
README says nothing unknown can be complete, while the contract permits benign
environment-unverified findings for 'complete-for-declared-coverage'. Align the
guide to the bounded meaning: declared graph answered is not environment readiness.

## Next action and retained learning
One bounded repair of D-01 through D-03 plus documentation; no new registry layer
or extra declarations merely to make the example green. Then use/verify the revised
prototype before finalizing 0518 Colab integration pins. The EGM assessment and
integration draft remain preserved; no cold model review is launched here.
The pattern is similar to the readiness repair: passing tests did not cover a few
important distinctions. Preserve the first submitted evidence and add regressions.
AR-01 remains held. No Director preference or design fork blocks these corrections.
