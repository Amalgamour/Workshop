# Prime review — 0510.colab-tools / 05.06
Date: 2026-11-01. Reviewer: Codex Prime.
Disposition: revised architecture accepted as a basis for the bounded workflow slice, with the conditions below. Prototype is not accepted as a readiness checker. No implementation or next pack is released here.

## Alignment and verified work
The revised proposal corrects the N1NN regression for the reserved pair, separates byte identity/seal identity/recorded order/declared exposure, requires both package verifiers, makes expected mode explicit, and uses a newline-aware parse view while retaining raw hashes. It identifies missing workflow compute instead of treating a design as implemented. These are useful corrections to C01–C05.

Independent checks: all 75 frozen source rows match snapshots and live bytes, and all 48 artifact rows match. The 51-test pure-rule/model suite passes on native Python 3.12.14. Read the pack, submission, contract, change ledger, notes, impact map, acceptance plan and new executable prototypes; inspected the existing workflow entry points supporting the missing-slot/custody findings. No real capture, reserved checker, model, Git write or workflow integration was run.

## D1 — already decided, no new Director question
The Director previously said, in this retained chat: "0702 holds it's packs and returns as a tail.  N5NN matches N1NN not N7NN." The original statement's date/time is not established here. This is preserved Director wording, separate from this Prime interpretation: the N7NN page-local pack/return/review route applies to ordinary as well as reserved Colabs. The new pack also explicitly restated that rule. Existing compute's N1NN-only behavior is an implementation gap, not a competing source of policy authority. Do not ask the Director to choose that route again. Keep legacy captures; do not migrate or rewrite them in this slice.

## Missing compute and build order
Source inspection confirms H3 is false for workflow pass02: fresh_record creates the initial slot, open refuses an occupied page, and attach requires an existing slot. request-next alone cannot create the second slot. K1 page-local return sealing, K2 requested next-pass opening and K3 retained transitions are therefore reasonable bounded additions in a disposable workflow successor before a reserved checker is built.

H2 descriptor packaging remains untested end to end. Its later proof can use an explicitly scoped disposable local repository, without project Git mutation or network; no such test is released or represented as completed now. H5 real-model block compliance remains unknown.

## Additional independent findings — required checker acceptance cases
V01 — stage accepts the wrong first_return.return_bytes. Changing only that descriptor length by one still returns informed-launch-ready-as-declared. The prototype compares raw length to the seal, but not the descriptor's supplied length. Require equality across descriptor, local return slot, seal transition and actual raw bytes.

V02 — stage does not bind the supplied cut to the informed packet's actual targets. Changing the target SHA in the synthetic trusted source_map while leaving the descriptors unchanged still returns ready. These are imitation verifier facts, not a cryptographically tampered real package. The demonstrated gap is in the pure stage rule's comparisons. The actual checker must compare both stage descriptors with their digest-verified source maps/bindings, including target IDs, paths, lengths, hashes and relevant repository/book instance. It must not compare two declarations alone.

V03 — stage parses a first-findings fence without validating its schema/content. A consistently hash-bound synthetic return with schema not-findings and stage wrong still returns ready. Validate reserved-findings schema, stage, finding IDs/shape and required fields before opening the informed phase; later reconcile refusal is too late to establish launch readiness.

V04 — run_probe.py retains each run correctly, but always returns 0 even if a child test exits nonzero. Run 1's P2 error is honestly preserved in run.json and is not hidden in the submission. Nonetheless, the runner's overall status is not an all-tests-passed indicator. Require a failing aggregate exit/status when any required step fails in future reusable harnesses, without deleting earlier output. Do not repair the sealed runner in place.

These findings do not invalidate the architectural need for K1–K3, but the current prototype must not become a ready/blocked authority by copying it unchanged.

## Conditions for the first workflow build
Keep it isolated and disposable; preserve the active app, old workflow and all history. The chosen local return route serves ordinary and reserved N7NN jobs. Version the changed record/return shape explicitly. Preserve exact input return bytes, occupied-slot refusal and idempotent replay. Check record/return/transition consistency on reads and writes. Define the write sequence and interruption recovery for return file, record and seal; never report a partial write as complete. Retain prior transitions and their association with the exact package/pass/review. A hash chain is internal consistency with a recorded prefix, not external authentication or race/power-loss proof.

Do not claim the new workflow enforces reserved exposure before the reserved checker and its attach boundary are actually wired and reviewed. The first workflow slice may supply the custody/order substrate alone, labelled as such. The known review_pending ambiguity remains visible and must not become a completion signal. Legacy N1-backed placement remains history/compatibility coverage, not the selected route for new N7NN work.

## Next bounded action and Director attention
Prepare one isolated workflow-successor build for a Grok builder when its current work is reviewed. Its contract should include the conditions above; reserve V01–V03 for the later checker acceptance suite, and V04 for its harness. No additional Director decision is needed for D1. If a new policy/authority fork appears during that build, stop and elevate it under 0412. Claude's production-code restriction remains intact.

Evidence: evidence/prime-review05.06/checks.json, tests.stdout/stderr and review-check.py. Original design and prototype remain unchanged. Custody 0110 remains pending; no receipt, promotion, seating, app activation or new worker invocation is created here.
