# Submission - 0512.prime-review/05.08

date: 2026-11-03
executor: Grok-1
reviewer: Codex Prime
accepted: false
committed_by_this_builder: false
custody: pending
matching line: 0112.prime-review unfiled
readiness: returned for Codex Prime review

This is the builder return for the named invocation of 05.08. It is a claim. It is not acceptance, not custody, and not a release. Notes in 06.13.md were reread after the author suite and integrated there. The contract was not revised after tests. This file does not carry the artifact-manifest hash. That hash is written only on the 05.08 return pointer after the manifest exists.

## Did

Verified evidence/pack05.08/source-manifest.json before the notes. Schema prime-pack-inputs/1. Fifty-five files. bad 0. missing live 0. missing snapshot 0. live drift 0. snapshot mismatch 0. extra snapshots 0. Manifest sha256 bdfb3173f1f26a1aae7119790719be0c5343529276357da470ea3b1d2eae1d46, 15109 bytes. HEAD 960d20c5290656095df8457b1740d2d5e586b111. Branch workshop. Index empty. The freeze was not repinned.

Read 06.12.md. Reproduced both findings and kept the raw logs. R1: the 05.07 dispatcher written on disk as app/librarian.py, with the frozen v1 connector present, exits 2 with empty stdout and the stop line naming got 12792 bytes sha256 b253a89751a48b64089bb95c4fde3715de00e6dc3c61dd8bad8653051234f3fa, want 12204 bytes sha256 c3a5be3b612c021d95effaa5da4a151bf89026422b94f4cad98331014c7f0cd9. R2: the historical test_author_contract_and_dispatcher_stay_put fails because the 05.07 return pointer is no longer PENDING. The historical test was not edited. Neither reproduction is new coverage.

Built app/review_report_tools_v2.py, app/review-report-v2.json, and labs/review-report-deployment-pass01. The candidate dispatcher loads the v2 connector. The v2 connector pins that dispatcher and the deployment runtime, then starts labs/review-report-deployment-pass01/report.py. That runtime checks the same pins except its own file, then calls pass03 observe and the pass03-patched finish. It does not call pass01.check_pins and it does not launch pass03 main. Historical pass03 and v1 still refuse the candidate dispatcher.

The proof command was python -B on the external candidate's own app/librarian.py review-report. The candidate root is D:\librarian\temp\0512-0508-report\candidate. Its app/librarian.py is the deployment file, 12805 bytes, sha256 d37dd14ccb921f92ff1a05c00890d57ee0f3d9f27d766bd86d81861abdd80a52. The active app was not changed.

Candidate dispatcher sha256 d37dd14ccb921f92ff1a05c00890d57ee0f3d9f27d766bd86d81861abdd80a52, 12805 bytes. Runtime report.py sha256 0f7def8d353506b93c71d130d740cd1262717ce493a868fc356e09ab925f7506, 6294 bytes. v2 connector sha256 81993c712d74e1d9e5155011fa949731a492ca6a2c626d27c6bebd9591965aab, 13956 bytes. Declaration sha256 3e2f41e875c3f04850d5bd7eb1f0e692aeb9d03a186b4665f5764ada421969e4, 4080 bytes. CONTRACT.md sha256 773b65bcb33cf8378beff0786216611a69056a3ae44a3aeb876bb233a387432c, 6573 bytes. The author suite was 18 tests, 14.755 seconds, OK, exit 0, Python 3.14.0.

0512.prime-review pass 05.06 on that candidate: baseline and installed stdout match, exit 0, state readable, review wbf38837cf0fa9c6b, stale false, custody missing, authority none, disposition accepted, operation continue, publication published and class complete, observation stable, work_complete false, action_released false, accepted false, approved false, closes_work false, releases_action false, task_association not-established. tests_passed true is a supplied bounded assessment. tests_note is an object. Declared artifact entries 14, 149885 bytes. Measured artifact rows 14, 149885 bytes. Intake role rows 17, 169310 bytes. Addressed source paths 16, 157007 bytes. Content blobs 15, 127265 bytes. Verified physical files unknown. Artifact hash_match 14, hash_mismatch 0, not_verified 0. Attention lines 5. Stdout sha256 73aa1b38e77e010ea8fef74d3bc536b597a040b4317b9cf0da3788d9f0a53441, 22113 bytes. The only difference from the earlier active-tree object is code_root.

0521.return-placement pass 05.13: baseline and installed stdout match, exit 0, state readable, review webe8f0a86f3de800, stale false, custody missing, authority none, disposition accepted, operation continue, publication published and class complete, observation stable. The same release flags are false. tests_passed true is a supplied bounded assessment. tests_note is an object. Declared artifact entries 5, 81671 bytes. Measured artifact rows 5, 81671 bytes. Intake role rows 9, 95759 bytes. Addressed source paths 7, 90980 bytes. Content blobs 7, 90980 bytes. Verified physical files unknown. Artifact hash_match 5, hash_mismatch 0, not_verified 0. Attention lines 6. Stdout sha256 3938c5c090cbceccae78cf82868b5b7a23ea94f74a5638c890e4cbd08d881c89, 19924 bytes. The only difference from the earlier active-tree object is code_root.

Disposable fixtures under the same keep directory matched across baseline and installed commands. Missing review was not-recorded. The edited note was stale. The digest mismatch was held. Each fixture tree matched around the report calls. Setup prepare, record, and publish used the existing review-loop on those disposable books.

The fixed live helper root remains D:\Git\lib-build because labs/workbook-review-pass03/workbook.py sets REPO there and was not edited. A candidate copy of that module still uses that path.

## Blocked

Matching line 0112.prime-review is unfiled. This slice does not file it and does not invent a receipt. Custody on the live reviews stays missing. Verified physical-file identity stays unknown. The shared command is not selected. The 05.07 dispatcher bytes cannot succeed while v1 and pass01 stay frozen, because those bytes load v1 by filename. This pack does not edit those modules, skip a check, or place different bytes at the v1 path. Codex Prime has not reviewed this pack. This builder does not commit.

## Need

Codex Prime review of this return. The candidate command, the pin list, and the rollback are in evidence/build05.08/PRIME-USE.md and evidence/build05.08/INTEGRATION.md. Stop here.

## API and ownership

The caller supplies an absolute book, a source page id, and a pass. The connector derives the code root from the installed app and refuses a second root. It hashes the candidate dispatcher, the historical dependency cut, and the deployment runtime before the runtime starts. The runtime hashes that cut again, except its own file, before pass03 observe. Exit 0 is the reporter's readable state. Exit 0 is not approval. Exit 1 is the reporter's stale, held, not-recorded, or identity-mismatch result. A connector refusal is exit 2, empty stdout, and a stop: line. A runtime or historical reporter refusal keeps the JSON object and a refused: line.

Selection replaces app/librarian.py with the candidate file and requires the three new files to remain at their pinned paths. It does not change v1, pass01, pass02, or pass03. Those historical checks still refuse the replaced dispatcher. Rollback restores app/librarian.py from evidence/build05.08/rollback-librarian.py, sha256 c3a5be3b612c021d95effaa5da4a151bf89026422b94f4cad98331014c7f0cd9, 12204 bytes.

## Claim, case, result, limit

The table is evidence/build05.08/TEST-TABLE.md. The command hashes are evidence/build05.08/command-log.json. The no-write watch is evidence/build05.08/no-write.json. The candidate file list is evidence/build05.08/candidate-index.json.
