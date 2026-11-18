# Prime review — 0708.colab-capability / 05.02
Date: 2026-11-01. Reviewer: Codex Prime.
Disposition: accepted as the bounded evidence-preservation probe successor. Original pass01 probe remains held and was not executed.

## Goal and result
The successor addresses F01 by allocating evidence and scratch slots under explicit separate roots, creating slots exclusively, refusing occupied evidence destinations and deleting no prior run directory. It records controlled failure and actual process termination differently and does not convert a killed run into success. This is a usable limited lab wrapper, not an adoption of the reserved method or general-purpose orchestration.

## Independently checked
Read the complete pack/return, method/notes, new probe implementation and focused test coverage. All 53 frozen source rows match snapshots and live bytes. All 75 submitted artifact rows match. The recorded preservation-before and preservation-after objects agree; independently rehashed all 165 listed earlier files across their nine roots, with no mismatch. No earlier return, pass01 source or evidence was modified by this review.

Independent native Python 3.12.14 run of the changed wrapper's focused suite: 17 tests passed, no skips, exit 0. Evidence includes separate successes, prior success/failure preservation, occupied evidence/scratch cases, actual termination retaining a running marker, unique generated IDs, same-ID exclusion in one pair, producer pin mismatch, path/input refusals and preview result validation. Full producer/workflow/app suites and the original destructive probe were not run. The recorded real producer preview remains builder evidence; this review did not repeat that unchanged-tool path unnecessarily.

The submitted slots presently show ok-1/ok-2/race-1/tool-preview complete, fail-1 failed and hold-killed running. A running marker is an incomplete state, not proof that a process is still alive. Its survival after the test's kill is the important preservation result. The occupied seeded marker remains preserved by the matching artifact manifest. One same-ID pair does not establish general race freedom.

## Scope and limitations
No new blocking defect was found within the requested F01 scope. The wrapper's modes are intentionally narrow (ok/fail/hold/preview); it is not a replacement for the original full capability audit. Preview success is not full package verification, semantic acceptance or release. It checks the pinned producer's bytes before launching by path; replacement between read and launch is not covered. Flush/fsync and one killed hold do not prove power-loss durability or kill-during-replace behavior. No authenticated ownership or resumed-run repair is claimed.

Operator handling: keep each completed, failed and incomplete slot. Use a new run ID for later work; never clean an old slot to retry. Inspect status plus raw command/child evidence rather than a process exit alone. Earlier lab runners are not silently repaired by this successor; use its preservation pattern explicitly when new labs are built.

## Review check correction
My first preservation-reader script incorrectly treated a single-file root as a directory and appended its filename twice. That Prime script stopped with FileNotFoundError; it was not a builder defect. I retained the first script and correction note, then corrected only the new reader. The completed integrity result and independent test output are preserved under evidence/prime-review05.02. No failed verification was represented as success.

## Next bounded action
Use this preservation pattern for new integration labs. The separate 0511/05.04 workflow build and 0707/05.03 loop design already have their own owners and outputs; this review creates no shared edits or speculative implementation while those inputs are pending. No new Grok-1 pack is assigned by this return review. No N1NN allocation, receipt, app selection, release or kernel seating follows.
