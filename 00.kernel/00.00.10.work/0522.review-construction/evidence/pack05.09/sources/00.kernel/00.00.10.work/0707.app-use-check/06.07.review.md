# 06.07.review - Real candidate matrix
date: 2026-11-01
who: Codex Prime
disposition: evidence reviewed; A22 case defect confirmed; matrix remains FAIL; app integration not released

## Verified facts
Independently verified all 106 frozen source and 462 artifact rows. Verified byte counts/SHA-256 of stdout and stderr for all 127 recorded candidate calls. Summary: 31 PASS, A22 FAIL, A24 MANUAL; zero timeouts, leftovers or incomplete output. Actual config differs from frozen template only in release. No new candidate execution or matrix rerun performed by Prime in this review. The 31 passes are evidence from Claude's run, not a second independent execution or a fresh-model proof.

## A22 classification
Confirmed harness/case defect, not evidence requiring a candidate change. cases.py a22 starts with an absent target, then prepare_and_decide asserts view.template is an object. Actual prepare returns target.state absent, view.template null and truthful no-record wording. Cycle source constructs a template only when a binding and target write token exist. It cannot supply a valid target token for a page that is absent. The failed check stops this case before record-refusal and decision-preservation assertions execute; those assertions remain untested by this external case. Preserve the failure, do not relabel it PASS.

Split the missing coverage into absent-at-prepare (no template, truthful guidance, no judgment) and target-removed-after-valid-prepare (a real decision exists, then record refuses without changing it or committing). Preserve the assertions; correct their prerequisite. No loop repair or targetless recording is authorized by this finding.

## A24 and acceptance limits
The unchanged manual row stays MANUAL. Source and prior independent tests establish the declared pass04 pin and refusal when the declaration is wrong. They do not exactly reproduce replacing the actual construct bytes under a relocated checkout. Record this distinction; do not invent equivalent evidence or edit production dependencies. App integration still requires Prime review of the remaining coverage and an explicit bounded implementation pack.

## Prime authoring defect
The executed 05.07.pack.md retains a stale DRAFT ONLY state line. Prime's preparation script read text using the platform default encoding and rewrote it as UTF-8: the dash became mojibake, so the later exact status-line replacement did not match. Prime failed to assert the final replacement. The actual named Director invocation was recorded by Claude; no authority is inferred from the contradictory stamp. Keep this executed pack and its release evidence intact. Future packs use explicit UTF-8 reads, an ASCII state line and an asserted read-back. This is a Prime preparation error, separate from the candidate failure.

## Learning / next bounded action
Raw probe output outranks the prose summary describing it. A valid JSON shape or green stub suite cannot establish that real fixture prerequisites hold. Prepared 05.08.pack.md for a focused supplemental two-case lab, preserving this full matrix and its 31 passing rows. No wholesale rerun or implementation repair is justified merely to obtain green. App connection 0522/05.09 remains conditional and is updated with the findings.

## Did / Blocked / Need
Did: reviewed full return/source/case output, verified manifests and all recorded call-output hashes, confirmed A22 classification.
Blocked: external absent-at-record coverage incomplete; A24's exact altered-file experiment remains manual; full matrix remains FAIL.
Need: separately invoked supplemental lab and Prime disposition, then finalize the app connection pack if justified. No new Director design choice. No production-code, active app, custody or scheduling changes.
