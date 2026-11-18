# Prime review — 0707.app-use-check / 05.03
Date: 2026-11-01. Reviewer: Codex Prime.
Disposition: accepted as the isolated L1 implementation basis, with the engineering corrections below. Prototype is not production and does not establish app readiness. L2 selection remains later work.

## Goal and independently verified result
The handoff now uses accepted constructor pass04, preserves the cycle's pass02 bind dependency, keeps app/door selection separate, and specifies supplied-state checking and mechanical guidance. It reads the previously missing v2 entry test and identifies rendered-marker-missing as a distinct protected state. This gives a bounded loop build instead of another whole-app redesign.

All 146 frozen input rows match their snapshots and live bytes; all 41 submitted artifact rows match. Read the pack, return, notes, delta contract, acceptance, impact map, builder steps and new pure-rule/probe code; checked relevant existing loop and constructor source. Reproduced the 31-step probe on Python 3.12.14 with both output and scratch redirected to NEW Prime-owned directories. Aggregate pass, exit 0. Original evidence writers were not run over their original destinations. Constructor inspect was exercised read-only; no app/loop/cycle record or render was executed by that reproduction.

## R01 — recompute the envelope binding before apply
The proposed six-point precheck compares the committed decision's task-binding string with the cycle read's string, but does not recompute the binding of the actual envelope about to be rendered. On the real copied A record, changing only envelope.task.task_id to a different synthetic ID still returns verified-against-committed-record. The real pass04 bind command reports original a8761262afb9993a459ce26da4e55b722686f43ba842c880d2e55d3a33cbd74c and changed 8efef6532a60e45e3239fd2e17f52bda2f8576b364ac9ae0e96929853d199264. Both bind calls exit 0; no apply was run. This is a demonstrated precheck omission, not a demonstrated overwrite.

Mandatory implementation correction: before every apply, recompute the current envelope's task binding using the pinned pass04 bind path and compare it with the hash-verified committed decision AND the current cycle view. Keep all constructor source/record alignment and final write-token checks. Refuse before target/support/partial/rendered-marker writes on mismatch. Check other envelope fields against their authoritative registration/record sources, not two copies of the same unchecked declaration. Add task identity, agreement/evidence/receipt mismatch and source-change negatives. The old post-write finish_render comparison remains useful, but is not the first check of task identity.

## R02 — truthful mechanical messages
mechanical(awaiting-review, absent) currently says 'the committed judgment is kept' even though no judgment has been committed. The same stock phrase is used for unknown states. Wording must describe verified state: absent/no record -> not recorded; known committed/render-blocked -> record retained; unknown/mismatched state -> not established. Keep supplied_next_action distinct and never use its prose as execution authority. No new lifecycle state is inferred from wording alone.

## D3.3 — keep the existing L1 precondition, state its limit
For this isolated L1, keep the current target-presence requirement and the existing stale/source/judgment validations. Do not add a refusal based only on target review content. An absent target is reported before judgment work; if it is absent at record, preserve the supplied decision file unchanged and report that the cycle did NOT commit it. This is not a new recording gate or a claim that B8 is fully solved for targetless work. Extending the cycle to commit without an addressable target would be a separate scope. B8 remains: a valid recorded judgment survives a substantive/unsupported target's render block, with no overwrite. No new Director decision is needed to retain these existing preconditions in this slice.

## Additional implementation conditions
Legacy /1 compatibility must have an explicit eligibility basis; do not silently downgrade a newly recorded /2 envelope by deleting supplied state and calling it legacy. The implementation contract must specify that basis and test downgrade refusal plus genuine /1 compatibility. If it requires a shared cycle change, stop and return the exact blocker rather than changing the cycle or weakening verification.

The committed-record checks must also run on read/recover and on any already-rendered shortcut that reports verified state. Missing/malformed files produce bounded refusal or explicit unknown, not a traceback or a false 'verified' claim. The six comparisons are a foundation, not a complete adversarial proof. Full external rewriting of every anchor is outside the stated integrity model; no authenticated identity or approval claim is created.

Keep marker-missing recovery held as proposed: do not infer installed body equality from task binding alone. Preserve the actual raw decision and Director wording, old review and successor identity separation. Keep authority none, accepted false, custody not-established and no release/close/allocation.

## Documentary correction
The method in 06.03.notes says no constructor subprocess would run; the final return, source and raw evidence correctly disclose eight read-only constructor inspect calls. This is a method-record discrepancy, not evidence of a hidden app/loop run. Preserve the original and state the actual calls in the next return rather than repeating 'no tool executed'.

## Next bounded work
Prepared N5NN implementation pack 0522.review-construction/05.08.md for Grok-1: NEW labs/review-loop-pass03 only, R01/R02 and legacy eligibility included, direct loop tests, active app/door/cycle/constructors unchanged. This is distinct from Grok-2's page-local Colab workflow. Stop before L2. No production code by Claude, app selection or fresh-Prime claim is inferred from the design review.
