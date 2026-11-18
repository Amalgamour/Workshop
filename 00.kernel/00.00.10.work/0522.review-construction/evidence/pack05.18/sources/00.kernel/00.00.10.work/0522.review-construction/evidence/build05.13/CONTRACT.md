# CONTRACT - workbook review pass03
date: 2026-11-02
who: Grok-1
schema: workbook-review-contract/1
state: written before code; not revised after tests

This is the API, delta, failure, and ownership contract for 0522.review-construction/05.13. It repairs K1 and K2 from 06.24. It is a successor of the 05.12 workbook. It is not a workflow engine and not a kernel rewrite.

## Reuse

Pinned and not edited:

- labs/workbook-review-pass02/workbook.py sha256 6ce4a5ff2e7505a8b56a13c05af3f5f2e9d8648112a6bf67c0e6392ab043a49a, 52574 bytes. Pass03 loads this file and replaces functions on that module and on the pass01 module it already holds. The file bytes stay.
- labs/workbook-review-pass02/forms/workbook-review-v1.json sha256 66b3f8f70f8e5d2f940296918767ff0e712e7e144378ad8653259e83d3284645, 4532 bytes.
- labs/workbook-review-pass01/workbook.py sha256 60e040fa30f61348adac76a4f3bdfbfdb9aba859f25bacadf317937c167e9b0a, 79131 bytes.
- labs/workbook-review-pass01/forms/workbook-review-v1.json sha256 152b436bda8e19d15f252bb5208791c8eefd9a658789e2ab6e9789ffa362b49f, 4532 bytes.
- app/review_loop_tools_v6.py sha256 e2a5df36efe29f9dad8abd8fa0f842fd98941d58ca1eb3cd4be5227e20420a94, 9175 bytes.
- app/review-loop-v6.json sha256 c7f95d16f91644c6465fd3483e3db4d6fb9b9115aa6e20fc09a194fc5bb1f0aa, 2743 bytes.
- app/review_loop_tools_v5.py sha256 b1192daf5d265c66f10adfe2125ff0c92a08ccd3c797d229698ecc20e2fdeed9, 7875 bytes.
- app/review-loop-v5.json sha256 eaa9120bba2c7274f2218c875ec3ecfc84d291188557049240c30a1c2a430de3, 1964 bytes.
- app/review_loop_tools_v4.py sha256 0769179366a6c1659f38cb2c79c51981d5cb76fa8d48ee7325f9eaf00d14c296, 13381 bytes.
- app/review-loop-v4.json sha256 769f81321e19a9f3296020e3b0b4a4905ec1b3a66c1629bf53d9548b7182d723, 2519 bytes.
- labs/return-access-pass01/return_access.py sha256 501d40d7c7b08720d3ae061441284ac26d544e7b80100059b2ddce25f67358f5, 26561 bytes.
- labs/review-loop-pass03/review_loop.py sha256 47f47d16426e4d69987398a8244877de58b6089326874f3279003f696814450b, 55474 bytes.
- labs/review-construction-pass04/construct.py sha256 6d541d4225ed0f9ccdb6263b475a79f55e4312be80a7e9a810a3622e5bd8df20, 42582 bytes.
- labs/prime-cycle-pass03/prime_cycle.py sha256 496b4d721cfb136fa847d998d421209616c60508beb5cda5620af73041eed17c, 76045 bytes.
- labs/prime-review-pass02/prime_review.py sha256 80836a13278365de863ed8231cb8118ad14ddbad672dd02ec2ebf69beff3b44e, 58560 bytes.

The pass03 workbook hash is not hardcoded in app/review_loop_tools_v7.py. It is pinned only by app/review-loop-v7.json. Authoring-v2 and return-lines-v2 stay on their doors. prime_review.py, prime_cycle.py, construct.py, pass01, and pass02 are not edited.

The public commands stay prepare, form, record, inspect, publish, read, and recover. Stdout stays one JSON object, schema workbook-review-result/1. Exit 0 is not approval, filing, or release. Exit 1 means a judgment exists and publication or recovery is blocked. Exit 2 is a refusal before a record, or a bad call. The workbook prints `refused:`. The librarian wrapper prints `stop:`.

Filed custody still requires a complete return-line descriptor and a real receipt file from the pinned return-access lookup. Preliminary custody stays missing. operation complete is refused unless the cycle commits. closes_work, releases_action, and eligible completion stay false. No receipt is invented. A heading is not a grant. Director text is only the body under `## Director - verbatim` or the em-dash form. The live 05.10 page has neither. director_text stays null. Missing agreement.goal, agreement.scope, recorded_decisions, and receipt stay unknowns.

## Ownership

An owned book is the canonical work book `D:\Git\lib-build\00.kernel\00.00.10.work`, or a directory whose path and resolve stay outside `D:\Git\lib-build`. The repo root, any other directory inside the checkout, and a junction or link whose resolve lands inside the checkout are refused. There is no force flag and no allow-live flag. Writable permission is not judgment, approval, or custody. This builder does not record or publish on the live book. Prepare, form, and inspect may read it.

Writes this module performs stay under `workbook-review/` or the one derived review target. The pinned loop may also write `scratch/`, `trace/`, `partial/`, and `support/{review_identity}/` when a filed review calls it. The v4 fixture-root guard stays. A workbook command and `--fixture-root` together are refused, except describe-legacy, which stays on the pinned v4 door.

Pass02 ownership, freshness, pre-publish checks, and scoped cycle paths stay in force. This overlay does not replace those functions. Own publication does not by itself make the source stale. A later successor record keeps `published_target`. A read-only target moves the journal to `pointer-pending` and refuses before the temporary. A changed `rendered.md` is not published. A filled predecessor section still blocks successor publication and keeps the judgment. Two filed sources keep separate cycle directories. `scratch/envelope.json` remains the pinned loop's book-global working witness.

## Pointer grammar

A pointer line may be `Submission`, `Artifact manifest`, or `Verification`, then one path token, `sha256`, 64 lowercase hex digits, a comma, a byte count, and `bytes.` An optional suffix is accepted only when it starts with a space and contains neither another Submission, Artifact manifest, or Verification label nor another 64-hex digest.

An artifact-manifest line may instead end in `bytes, <digits> files.` The remainder after that period is empty, or exactly ` Excludes itself.`, or exactly ` Excludes itself and this page.` That count form is not accepted on Submission or Verification. Any other comma tail is unparsed. The integer is the declared entry count. It is compared with the number of file entries. A difference adds `manifest-count-mismatch` and marks measurement incomplete. The entries are still bound. The JSON `file_count` field is not a second authority. Historic manifest bytes are not rewritten.

A duplicate label clears only that label. An unknown or malformed line is `unparsed-return-line` and does not clear a valid label.

## Resolution

`locate_declared` receives the source page through the intake call. It considers, in order, and it does not search:

1. The declared path under the book.
2. When the declared path starts with `00.kernel/00.00.10.work/`, the remainder under the book.
3. The page-relative path `{page}/{declared}` only when the declared path does not already start with `{page}/` and does not start with `00.kernel/00.00.10.work/`.
4. The declared path under `D:\Git\lib-build`.

A path that is not a regular file, is a link, or escapes its root is not a candidate. The same resolved file is one candidate. The book root wins over the code root. Among book paths, the first book candidate wins. Two different files are ambiguous. Neither is chosen. There is no parent walk and no "whichever exists first" across different files.

Each bound row stores root `book` or `code`, the root-relative path, the declared path, the measured sha256, the measured byte count, and the declared sha256 and declared byte count when the declaration supplied them. A hash mismatch keeps the measured row and is a finding. A missing file adds no row. Code-root rows stay in the intake for drift. They are not passed to prime_review and they are not cycle fixture-root evidence.

On the live work book, a qualified `00.kernel/00.00.10.work/...` path and the code-root spelling are the same file, so the book wins. A disposable copy that plants a different file at the book remainder is ambiguous against the repository file. That ambiguity is kept. The four `labs/return-readiness-pass01/` entries in the real manifest do not start with the work prefix. On the live book they bind as code root when that is the only file.

`MAX_INDEX` is 12 and bounds only displayed artifact cuts. More than 12 entries adds `index-context-bounded` and does not drop a later row. That finding does not by itself make measurement incomplete. Custody missing does not by itself make measurement incomplete. An incomplete measurement blocks record. Prepare, form, and inspect still return the findings.

## Thin verification declaration

The real 05.10 submission is not a pointer Verification line. When the pointer did not supply a verification spec, and the submission text produced `verification-not-measured`, a checked four-line block is read from that submission:

- `Verification: `path``
- `Schema: `name``
- `sha256: `64 hex``
- `bytes: <integer>`

The four lines are consecutive after stripping. The path is checked with the same logical-path rule and the same locator. One well-formed block is measured as role `verification`. Two well-formed blocks are `ambiguous-verification`, measurement incomplete, and neither is chosen. A backtick Verification line that is not that block is `verification-declaration-malformed`, measurement incomplete, and it does not clear other fields.

When the file is measured, the generic `verification-not-measured` finding is removed. A `verification-declared` finding remains. Its fields are `path`, `schema`, `measured`, `hash_match`, `successful_run`, `sources`, and `limit`. `successful_run` is false. `limit` is `The lines are a declaration, not a successful verification run.` `sources` contains `submission-lines` and, when an artifact row is the same resolved file, `artifact-index`. A hash mismatch keeps `hash_match` false and measurement incomplete. A missing file keeps `verification-not-measured` and adds `declared-file-missing`. The declaration is not proof that a verifier ran.

## Validator identity

Intake rows keep every selected role: assignment, submission, verification, artifact-manifest, artifact, and return. `prime_record` emits one validator source per resolved file among the rows selected for that path. Preliminary selection is every book row. Filed selection, when a capture is present, is assignment, artifact, and return, which is the pass02 filter. Collapse rank is assignment, then the return row whose path is the capture return, then any other return, then submission, then verification, then artifact. The emitted identity stays a legal prime_review identity. Supplied text is exactly schema `supplied-text/1` and label `SUPPLIED`. No role field is added. The artifact-manifest role stays in the intake and is not a new validator source kind.

If the selected rows for one resolved file disagree on measured hash, measured length, declared hash, or declared length, the finding is `source-identity-conflict`, measurement is incomplete, and no identity is chosen. Different book instances stay distinct. The instance id includes the absolute book path. Code-root rows are not collapsed into book rows.

Freshness still compares root, role, path, and measured sha256. Extra declared fields do not change that comparison. Cycle ownership is unchanged.

## Failure

- Book inside the checkout, other than the canonical work book: exit 2, no review write.
- Two different files for one declaration: `ambiguous-declared-root`, no row, measurement incomplete.
- Manifest count differs from the entry array: entries stay bound, measurement incomplete, record exits 2.
- Same file, contradictory declarations: `source-identity-conflict`, measurement incomplete, record exits 2.
- Same file, agreeing roles: record can succeed, intake rows keep the roles, validator logical paths are unique.
- Incomplete measurement, omitted semantic_conflict, and a conflicting record without `--successor` stay refusals. The stored record is kept.
- Source drift that is not the journaled review write blocks record and publish. The old record stays.
- A declaration of verification is not a successful run and not custody.

## Reproduction already retained

K1 and K2 were reproduced through v6 before this contract's repair code. K1 prepare exit 0, measurement incomplete, assignment only, page sha256 af56727c4a29007d9a78b0a746af4c949774daf01632bf7c1b7258ce471963c5 unchanged. K2 record exit 2, correction `refused: duplicate id at sources`, intake 86f92dbb4a21e74e0eb40c248317b523bcb7239e685320b9425fa6fca92a1cc4. Evidence is evidence/build05.13/reproduce/. Those trees stay. Later author runs are separate. They are not Prime's acceptance.

## Delta

New lab labs/workbook-review-pass03. Its form id stays workbook-review-v1. The correction route is labs/workbook-review-pass03/PRIME-USE.md. New door app/review_loop_tools_v7.py and app/review-loop-v7.json, schema review-loop-pins/5. librarian.py loads v7 for the review-loop command only. README documents v7 and the retained v6, v5, v4, and pass02 pins. No return-route selection, no readiness repair, no whole-dispatcher restore, no band migration, and no allocator patch. Matching line 0122.review-construction stays pending.

## Tests

Known reproductions stay the saved v6 outputs. Author cases, on new disposable copies, are:

- Predecessor pins, v7 selection, book plus fixture-root refused, checkout record refused.
- Exact real 05.10 pointer, submission, and manifest copied under a disposable book. Page-relative submission, manifest, and the thin verification file bind as book files. Qualified entries that are also a different repository file stay ambiguous.
- Read-only prepare of the live work book. Qualified work paths bind as book. The readiness-lab paths bind as code when that is the only file. The thin declaration is reported with successful_run false. The page hash stays.
- A small valid source using the page-relative pointer, the count suffix, and a manifest that lists submission and verification as artifacts. Prepare, form, record, inspect, publish, and a new-process read and recover. Validator ids are unique. Intake roles remain.
- The frozen role-overlap fixture on a new copy records. The first-failure tree is not reused.
- Same-file alias records as one source. Two different files at the book root and the page-relative root are ambiguous.
- Missing and malformed inputs, a duplicate label, a count mismatch, and contradictory hashes.
- Own publication is not stale. A changed selected file makes read and recover exit 1 and inspect stay exit 0 with the judgment. A tampered render is not published. A read-only target becomes pointer-pending.
- Two filed sources keep distinct cycle paths. A successor judgment is kept. Publish onto a filled section exits 1 and does not replace it.

The current-book form and inspect are read-only and are recorded after the suite. No live record and no live publish.
