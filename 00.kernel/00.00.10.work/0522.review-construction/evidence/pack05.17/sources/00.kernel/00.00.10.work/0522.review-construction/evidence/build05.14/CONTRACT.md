# Contract — 0522.review-construction/05.14

Schema: `v8-review-intake-contract/0514`
Date: 2026-11-03
Executor: Grok-2
Reviewer: Codex Prime
Status: frozen when the first staged door or staged workbook process starts

## Source cut

evidence/pack05.14/source-manifest.json schema `prime-pack-inputs/1`, 210 files, 0 mismatches, sha256 `ae51a80ee3555b675c90869dbfa5dd7f3576e3c32e877abcb4066e4966c38438`, 64153 bytes.

The accepted production pins stay:

- `app/librarian.py` `c3a5be3b612c021d95effaa5da4a151bf89026422b94f4cad98331014c7f0cd9`, 12204 bytes
- `app/review_loop_tools_v7.py` `93a89939b6e6143eaffbb75c3b7cb60c38c60ad91902bd15d0b48c5bb35c382d`, 10291 bytes
- `app/review-loop-v7.json` `bf12aa7cdf67cc6f8e6ae9d674aa39929933293495c6857dc423dab4c1cab8f8`, 3515 bytes
- `labs/workbook-review-pass03/workbook.py` `9e66d7e4413e8f0aedcc4ff416080c549ce435b10103149ef73de493b245ff8c`, 19533 bytes
- `labs/workbook-review-pass02/workbook.py` `6ce4a5ff2e7505a8b56a13c05af3f5f2e9d8648112a6bf67c0e6392ab043a49a`, 52574 bytes
- `labs/workbook-review-pass01/workbook.py` `60e040fa30f61348adac76a4f3bdfbfdb9aba859f25bacadf317937c167e9b0a`, 79131 bytes

## What is staged

Three new files, and only if each path is absent:

- `labs/workbook-review-pass04/workbook.py`, the production candidate, sha256 `b7b8776c0da775509b21614fadc1b51a39123a946add76d0dfcc9ad3fe3016e2`, 6508 bytes
- `app/review_loop_tools_v8.py`, sha256 `0335da325abf0f0292807ddbcf6f96cc107e8224732ee4afcf3f35470a0f9fc3`, 11054 bytes
- `app/review-loop-v8.json`, schema `review-loop-pins/6`, sha256 `92a718d300e20a52b765c4f1ed795051013e32a86597522edffb9ff49255872e`, 4100 bytes

The implementation difference from the accepted production candidate is none. The one-line lab adapter that sets REPO to the copy root is not installed. The form pin stays pass03's `labs/workbook-review-pass03/forms/workbook-review-v1.json`. The door validates the new workbook and the pass03 predecessor. It does not disable a pin.

## Behavior this stage keeps

N5, and a call with no kind context, uses the pass03 parser object. N7 uses the two declared forms first, then the pass03 forms. The kind comes from `address_of`. The context resets in `finally`. The workbook refuses unless its own file is under `D:\Git\lib-build`. A copied tree is a refusal, not a mixed root.

## Checks

Read-only, on the live book `D:\Git\lib-build\00.kernel\00.00.10.work`, through `app/review_loop_tools_v8.py` directly: prepare and form for `0522.review-construction` `05.13`, `0512.prime-review` `05.06`, `0707.app-use-check` `05.15`, and `0707.app-use-check` `05.17`. The two N5 results match `app/librarian.py review-loop prepare` on intake_id, rows, cuts, and findings. The two N7 prepares are complete, with 26 and 33 artifact rows. Hashes of those source, review, and custody paths are recorded before and after. No record, publish, reserve, or capture runs on that book.

Disposable books hold the 12-case suite, the historical suite with G7 kept as the revised failure, pin and declaration refusals, two new hostile cases, and one N5 plus one N7 prepare/form/record/inspect/read/publish/read/recover sequence. N7 may stay preliminary. No review file is precreated. Manual Director text is preserved. The 0521 first-review repair is not imported.

## Custody and selection

Matching line `0122.review-construction`. Custody stays pending unless a native member is already present, and this pack does not create one. The legacy allocator is not called. No receipt is invented. `app/librarian.py` is not selected. The later dispatcher delta is a proposal for Prime, coordinated with the unfinished 0512 reporter pin, and it is not applied here.

## Stop

A source-cut mismatch, an occupied target path, an N5 difference, an N7 artifact count other than 26 or 33, a canonical-root guard refusal at the canonical root, or a write on a live source, review, or custody path stops the claim. The first such miss is the first failure. Later probes still run when they do not repair a live page.
