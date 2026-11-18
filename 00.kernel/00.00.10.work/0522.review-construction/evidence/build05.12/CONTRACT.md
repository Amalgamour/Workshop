# CONTRACT - workbook review pass02
date: 2026-11-02
who: Grok-1
schema: workbook-review-contract/1
state: written before code; not revised after tests

This is the API, delta, failure, and ownership contract for 0522.review-construction/05.12. It repairs R1-R5 from 06.22. It is a successor of the 05.11 workbook. It is not a workflow engine and not a kernel rewrite.

## Reuse

Pinned and not edited:

- labs/workbook-review-pass01/workbook.py sha256 60e040fa30f61348adac76a4f3bdfbfdb9aba859f25bacadf317937c167e9b0a, 79131 bytes. Pass02 loads this file and replaces functions on that module. The file bytes stay.
- labs/workbook-review-pass01/forms/workbook-review-v1.json sha256 152b436bda8e19d15f252bb5208791c8eefd9a658789e2ab6e9789ffa362b49f, 4532 bytes.
- app/review_loop_tools_v5.py sha256 b1192daf5d265c66f10adfe2125ff0c92a08ccd3c797d229698ecc20e2fdeed9, 7875 bytes.
- app/review-loop-v5.json sha256 eaa9120bba2c7274f2218c875ec3ecfc84d291188557049240c30a1c2a430de3, 1964 bytes.
- app/review_loop_tools_v4.py sha256 0769179366a6c1659f38cb2c79c51981d5cb76fa8d48ee7325f9eaf00d14c296, 13381 bytes.
- app/review-loop-v4.json sha256 769f81321e19a9f3296020e3b0b4a4905ec1b3a66c1629bf53d9548b7182d723, 2519 bytes.
- labs/return-access-pass01/return_access.py sha256 501d40d7c7b08720d3ae061441284ac26d544e7b80100059b2ddce25f67358f5, 26561 bytes.
- labs/review-loop-pass03/review_loop.py sha256 47f47d16426e4d69987398a8244877de58b6089326874f3279003f696814450b, 55474 bytes.
- labs/review-construction-pass04/construct.py sha256 6d541d4225ed0f9ccdb6263b475a79f55e4312be80a7e9a810a3622e5bd8df20, 42582 bytes.
- labs/prime-cycle-pass03/prime_cycle.py sha256 496b4d721cfb136fa847d998d421209616c60508beb5cda5620af73041eed17c, 76045 bytes.
- labs/prime-review-pass02/prime_review.py sha256 80836a13278365de863ed8231cb8118ad14ddbad672dd02ec2ebf69beff3b44e, 58560 bytes.
- Authoring-v2 and return-lines-v2 stay on their doors.

The public commands stay prepare, form, record, inspect, publish, read, and recover. Stdout stays one JSON object, schema workbook-review-result/1. Exit 0 is not approval, filing, or release. Exit 1 means a judgment exists and publication or recovery is blocked. Exit 2 is a refusal before a record, or a bad call. The workbook prints `refused:`. The librarian wrapper prints `stop:`.

Filed custody still requires a complete return-line descriptor and a real receipt file from the pinned return-access lookup. Preliminary custody stays missing. operation complete is refused unless the cycle commits. closes_work, releases_action, and eligible completion stay false. No receipt is invented.

## Ownership

An owned book is the canonical work book `D:\Git\lib-build\00.kernel\00.00.10.work`, or a directory whose path and resolve stay outside `D:\Git\lib-build`. The repo root, any other directory inside the checkout, and a junction or link whose resolve lands inside the checkout are refused. A linked ancestor is refused and is not followed. There is no force flag and no allow-live flag.

Writable permission is not judgment, approval, or custody. This builder still does not record or publish on the live book. Prepare, form, and inspect may read it.

Writes this module performs are only under `workbook-review/` of that book, or the one derived review target: `{page}/{pass}.md` for N5NN, or `{page}/06.{tail}.review.md` for N7NN. The pinned loop, when called, also writes `scratch/`, `trace/`, `partial/`, and `support/{review_identity}/` under the book. Those names are working files of the pinned tools. They are not a caller destination.

The v4 fixture-root guard stays. A workbook command and `--fixture-root` together are refused, except describe-legacy, which stays on the pinned v4 door.

## Pointers and roots

A pointer line may be `Submission`, `Artifact manifest`, or `Verification`, then a path, `sha256`, 64 hex digits, a comma, a byte count, and `bytes.` An optional suffix is accepted when it starts with a space and does not contain another Submission, Artifact manifest, or Verification label, and does not contain another 64-hex digest. A duplicate label clears only that label. An unknown or malformed line is a finding and does not clear a valid label.

A declared path is relative, with no `..`, no backslash, and no drive. The book candidate is that path under the book. When the declared path starts with `00.kernel/00.00.10.work/`, the book candidate is also the remainder under the book. The code candidate is the same declared path under `D:\Git\lib-build`. The same resolved file is one candidate, and the book root wins. Two different files are ambiguous and neither is chosen. No parent walk and no search.

Each bound row stores root `book` or `code`, the root-relative path, the declared path, the measured sha256, and the measured byte count. A hash mismatch keeps the measured row and is a finding. A missing file is a finding and adds no row. Code-root rows bind for drift. They are not passed to the cycle as fixture-root evidence and they are not sent to prime_review as book files.

Every manifest entry is bound. `MAX_INDEX` bounds only the displayed artifact cuts. More than 12 entries adds the finding `index-context-bounded` and does not drop a later row from the intake id. An incomplete measurement, including a missing selected file, an ambiguous root, or a hash mismatch, blocks record. Prepare, form, and inspect still return the findings.

A heading is not a grant. Director text is the body under `## Director - verbatim` or the em-dash form. A carriage return on a heading line is ignored for that comparison. The file bytes are not rewritten by the read.

## Freshness

Read, inspect, and recover use one freshness result. The stored intake rows are compared by root, role, path, and sha256 to the live rows. The comparison also includes the record hash, the rendered body, the cycle record when the mode is cycle-committed, and the published target bytes.

The journaled publication whose `after_sha256` still matches the current target is this module's own review write. That write does not, by itself, make the source stale. A later successor record keeps that attestation on `published_target` so the own write still does not count as drift. Any other assignment, return, artifact, or source change is stale.

When the review is fresh, read includes `stale` false. When it is stale, read and recover exit 1 and still return the stored judgment and next action. Inspect exits 0 with the same boolean.

## Publication

Before any target write, and before the pinned loop render, the stored `rendered.md` must equal the record's rendered field and a fresh render of that record, and the record file hash must equal the journal. A difference exits 1, leaves the target and the journal unchanged, and keeps the judgment. The altered rendering is not copied.

Same-byte replay of a verified publication stays idempotent. A read-only target still moves the journal to `pointer-pending` and then refuses before creating the temporary. The record stays. Recovery shows `pointer-pending`. No cleanup deletes that state.

## Identity

Cycle descriptor, registration, request, and decision files for a review live under `workbook-review/{page}/{pass}/{review_id}/cycle/`. The cycle review location for one source and pass is `workbook-review/{page}/{pass}/cycle-records/`. The registration `review_identity` is the public `w` plus 16 hex id. The decision and cycle record id is `{pass}-{that id}`. The constant `wb` is not used. Two source pages do not share a review location. A successor on the same source uses the same review location, a new id, and the cycle template's `supersedes`. The old cycle record and the old workbook record stay. Journal `current` selects the successor.

The pinned constructor refuses to replace a review section that is not vacant. Publish of a filed successor calls that render. On `existing review conflicts`, publish exits 1, the target bytes stay, both records stay, and the journal current remains the successor. This module does not write the successor text over that section. A reply does not set closes_work or release.

`scratch/envelope.json` remains the pinned loop's book-global working witness. A later review overwrites that witness. Workbook recovery reads the scoped cycle record and does not require the witness to still match an older review.

## Failure

- Book inside the checkout, other than the canonical work book: exit 2, no review write.
- Junction or linked book: exit 2, the link is not followed.
- Incomplete artifact measurement: exit 2, failed input kept, no review record.
- Ambiguous pointer label: that label is unbound. A valid other label stays.
- Omitted semantic_conflict: exit 2, failed input kept.
- tests_passed null stays null.
- Same-byte record: exit 0, same review id.
- Conflicting record without `--successor`: exit 2, old record kept.
- Source drift that is not the journaled review write: record exits 2 and does not repin. Publish exits 1. The old record stays.
- Rendered body differs from the durable judgment: publish exits 1, target unchanged.
- Changed selected return after publication: read and recover exit 1, inspect exits 0, all stale, judgment kept.
- Route undeclared: exit 2, missing contains route.

## Stop

If the pinned cycle or constructor refuses a public review id, a scoped review location, or a scoped request path, this repair stops. The refusal text and the retained book are the seam. Coverage is not narrowed and the authority contract of those tools is not rewritten.

## Reproduction already retained

R3 and R4 were reproduced through the current v5 door before this contract's repair code. R3 review wd8d1ad845807c24b: inspect stale true, recover stale false exit 0, read stale null. R4 review wb60bbc93f6ad4e75: tamper publish exit 0 and the unrecorded sentence was in the target, then recover stale true exit 1. Evidence is evidence/build05.12/reproduce/summary.json. Those trees stay. The repaired cases are separate author runs. They are not Prime's acceptance.

## Delta

New lab labs/workbook-review-pass02. Its form id stays workbook-review-v1. The correction route is labs/workbook-review-pass02/PRIME-USE.md. New door app/review_loop_tools_v6.py and app/review-loop-v6.json, schema review-loop-pins/4. librarian.py loads v6 for the review-loop command only. README documents v6, the retained v4 fixture commands, and the retained v5 and pass01 pins. No return-backend upgrade, no band migration, no allocator patch. Matching line 0122.review-construction stays pending.
