# Contract — 0522.review-construction/05.15

Schema: `v9-n7-declaration-block-contract/0515`
Date: 2026-11-04
Executor: Grok-2
Reviewer: Codex Prime
Status: frozen when the first staged door or staged workbook process starts

## Source cut

evidence/pack05.15/source-manifest.json schema `prime-pack-inputs/1`, 253 files, 0 missing, 0 mismatches, sha256 `4fc6743611c8ba8f6e33c3d5245b288351828b17d2564c845c6917a52918bd47`, 77912 bytes, 0 CR characters.

The predecessor pins this stage keeps are the live bytes measured before the successor:

- `app/librarian.py` `c3a5be3b612c021d95effaa5da4a151bf89026422b94f4cad98331014c7f0cd9`, 12204 bytes
- `app/review_loop_tools_v8.py` `0335da325abf0f0292807ddbcf6f96cc107e8224732ee4afcf3f35470a0f9fc3`, 11054 bytes
- `app/review-loop-v8.json` `92a718d300e20a52b765c4f1ed795051013e32a86597522edffb9ff49255872e`, 4100 bytes
- `labs/workbook-review-pass04/workbook.py` `b7b8776c0da775509b21614fadc1b51a39123a946add76d0dfcc9ad3fe3016e2`, 6508 bytes
- `labs/workbook-review-pass03/workbook.py` `9e66d7e4413e8f0aedcc4ff416080c549ce435b10103149ef73de493b245ff8c`, 19533 bytes
- `labs/workbook-review-pass02/workbook.py` `6ce4a5ff2e7505a8b56a13c05af3f5f2e9d8648112a6bf67c0e6392ab043a49a`, 52574 bytes
- `labs/workbook-review-pass01/workbook.py` `60e040fa30f61348adac76a4f3bdfbfdb9aba859f25bacadf317937c167e9b0a`, 79131 bytes

## What is staged

Four new paths, and only while each path is absent:

- `labs/workbook-review-pass05/workbook.py`
- `app/review_loop_tools_v9.py`
- `app/review-loop-v9.json`, schema `review-loop-pins/7`
- `labs/review-entry-staging-pass02/` for the copied suites and the new adapter

The form pin stays `labs/workbook-review-pass03/forms/workbook-review-v1.json`. The door validates the new workbook, the pass04 workbook, the v8 door, and the predecessor tools already pinned by v8. It does not disable a pin. The production `REPO` stays `D:\Git\lib-build`. A copied workbook is a refusal.

## Parse, measurement, record

06.32 is the grammar. Recognized labels are `Returned:`, `Submission:`, `Artifact manifest:`, and `Verification:`. Accepted N7 forms remain the exact Returned form, the exact N7 manifest form, the pass03 counted form with its three tails, and the pass03 field form when the suffix is allowed.

A recognized N7 line that is a non-descriptive attribution, a label with no accepted value, or an `Artifact manifest:` line that contains `, sha256 ` and fails the exact N7 manifest form produces `malformed-n7-declaration`, state `blocked`, and no bound fields. A valid sibling line does not stay bound. The double comma is that manifest near-match in N7 context. Notes and other non-declaration prose stay `unparsed-return-line` and do not block. Duplicate valid lines stay on the existing ambiguous codes.

N5NN and an empty kind call the captured pass03 parser object. Comma, semicolon, and parenthesis filenames stay pass03 filenames. The pass03 reading of a trailing note on `Artifact manifest: m.json, sha256` stays `m.json,` in N5 context.

`build_intake` sets the measured kind, resets it in `finally`, and resets the block flag in `finally`. When the kind is N7NN and the parse blocked, the wrapper sets `measurement` to `incomplete` and recomputes `intake_id`. Record then returns exit 2 and the correction `The artifact measurement is incomplete. The judgment was not recorded.` Prepare shows the incomplete measurement. Form shows the finding on `form.bindings.findings` and the same intake id. The record writes no review judgment and no publication.

## Checks

Read-only, on the live book `D:\Git\lib-build\00.kernel\00.00.10.work`, through `app/review_loop_tools_v9.py` directly: prepare and form for `0522.review-construction` `05.13`, `0512.prime-review` `05.06`, `0707.app-use-check` `05.15`, and `0707.app-use-check` `05.17`. The two N5 results match `app/librarian.py review-loop prepare` on `form.bindings.rows`, cuts, findings, and intake_id, and the form command matches on `form.bindings.rows`, findings, and intake_id. The two N7 prepares stay complete, with 26 and 33 artifact rows, and their Notes lines stay `unparsed-return-line`. Hashes of those source trees and the frozen modules are recorded before and after. No record, publish, reserve, or capture runs on that book.

Disposable books hold the copied 12-case suite, the copied historical 17-case suite reconciled case by case, two new hostile cases (a malformed manifest before a valid Returned line, and a valid manifest before a non-descriptive Returned line), pin and declaration and dependency refusals, one malformed prepare plus record refusal that keeps the source bytes, and one N5 plus one N7 prepare, form, record, inspect, read, separate publish, read, and recover sequence. Manual Director text stays in place. A changed disposable source is refused. No review file is precreated. The 0521 absent-target repair is not imported.

Historical I4, H2, and I6 may still fail because a fixture path also exists under the canonical root. That failure stays labelled as canonical-root ambiguity. G7 may still fail because the N5 trailing-comma filename stays accepted. The double-comma N7 line is a block under this contract. The copied assertion is not edited. A new code is not renamed to `unrecognized-path-punctuation`.

## Custody and selection

Matching line `0122.review-construction`. Custody stays pending unless a native member is already present, and this pack does not create one. The legacy allocator is not called. No receipt is invented. `app/librarian.py` is not selected. The unapplied proposal is a later coherent dispatcher that carries this v9 pin and the unfinished reporter pin together. It is not applied here. Historical `0522/05.13` evidence is not repinned.

## Stop

A source-cut mismatch, an occupied target path, an N5 difference against the current v7 door, an N7 artifact count other than 26 or 33, a live N7 measurement that is incomplete, a canonical-root guard refusal at the canonical root, or a write on a live source, review, or custody path stops the claim. The first such miss is the first failure. Later probes still run when they do not repair a live page. This file is not revised after the first staged door or staged workbook process.
