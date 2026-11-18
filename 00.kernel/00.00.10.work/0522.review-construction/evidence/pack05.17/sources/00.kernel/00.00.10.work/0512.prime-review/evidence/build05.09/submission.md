# Submission - 0512.prime-review/05.09

date: 2026-11-03
executor: Grok-1
reviewer: Codex Prime
accepted: false
committed_by_this_builder: false
custody: pending
matching line: 0112.prime-review unfiled
readiness: returned for Codex Prime review

This is the builder return for the named invocation of 05.09. It is a claim. It is not acceptance, not custody, and not a release. Notes in 06.15.md were reread after the author suite and integrated there. The contract was corrected once after the first author failure, then locked. It was not revised after the passing run. This file does not carry the artifact-manifest hash. That hash is written only on the 05.09 return pointer after the manifest exists.

## Did

Verified evidence/pack05.09/source-manifest.json before the notes. Schema prime-pack-inputs/1. Ninety-seven files. bad 0. missing live 0. missing snapshot 0. Manifest sha256 114cadf253a8b23b6841d7868059d2919f3d7629e68142b8f5e8661f0e9c74c2, 28421 bytes. 05.09.md is outside that manifest. HEAD 960d20c5290656095df8457b1740d2d5e586b111. Branch workshop. Index empty. The freeze was checked again before this filing and remained clean. The freeze was not repinned.

Read 06.14.md. Reproduced B-05 and B-01 through labs/review-report-deployment-pass01/report.py on synthetic data before the repair. The logs are evidence/build05.09/known-reproductions/b05.json and b01.json. B-05 left authority "Director" and action_released {"x": 1} in place after mark_unstable. B-01 kept one dict from four rows and still reported a measured intake count of 1. Those logs are known reproductions. They are not evidence that the validated core emitted the values or granted authority.

Built app/review_report_tools_v3.py, app/review-report-v3.json, and labs/review-report-hardening-pass01. The candidate dispatcher loads the v3 connector. The v3 connector pins that dispatcher, every pin v2 pinned, and the hardening runtime. The librarian pin changes from the 05.08 candidate to this candidate. The hardening runtime is the one added path. The exact rows are evidence/build05.09/pin-delta.json. The runtime checks that set except its own file, then loads pass03 and patches the loaded envelope, row, and observation functions in that process only. It does not call pass01.check_pins and it does not launch pass03 main. Historical pass03, v1, v2, and the 05.08 deployment runtime still refuse this candidate dispatcher.

The proof command was python -B on the external candidate's own app/librarian.py review-report. The candidate root is D:\librarian\temp\0512-0509-report\candidate. Its app/librarian.py is the hardening file, 12804 bytes, sha256 f1d23d455f20319e3f430d345b2893bda039fd8c84be4f3691b4e4be123b8983. The active app was not changed.

Candidate dispatcher sha256 f1d23d455f20319e3f430d345b2893bda039fd8c84be4f3691b4e4be123b8983, 12804 bytes. Runtime report.py sha256 27e513f462b241e9c7298d3077d50d08ea5ac703a6f2d0769dc5935fcb51b58b, 18139 bytes. v3 connector sha256 be29de7daa00b84f79a0f403f2c5eaea3cf035d51e1b405d2fbf2f6ba5f7e73f, 14156 bytes. Declaration sha256 a27bf702c0eb87b4608ff60929467126e78fd7e60b7353644321468043a25817, 4276 bytes. CONTRACT.md sha256 1ac2b93a03e5a17a38c0deb3046b78324d374e3cec9d6239830d006019917f5b, 7827 bytes. The author suite was 25 tests, 15.932 seconds, OK, exit 0, Python 3.14.0. The first failure log remains evidence/build05.09/author-suite-first.txt.

0512.prime-review pass 05.06 on that candidate: baseline and installed stdout match, exit 0, state readable, review wbf38837cf0fa9c6b, stale false, custody missing, authority none, disposition accepted, operation continue, publication published and class complete, observation stable, work_complete false, action_released false, accepted false, approved false, closes_work false, releases_action false, task_association not-established. tests_passed true is a supplied bounded assessment. tests_note is an object. Declared artifact entries 14, 149885 bytes. Measured artifact rows 14, 149885 bytes. Intake role rows 17, 169310 bytes. Addressed source paths 16, 157007 bytes. Content blobs 15, 127265 bytes. Verified physical files unknown. Artifact hash_match 14, hash_mismatch 0, not_verified 0. Attention lines 5. Stdout sha256 207fef4235d4f2b2484692618c39cb5910ce0487cac2300ed381440ca7ef4f91, 22113 bytes. code_root is the external candidate root.

0521.return-placement pass 05.13: baseline and installed stdout match, exit 0, state readable, review webe8f0a86f3de800, stale false, custody missing, authority none, disposition accepted, operation continue, publication published and class complete, observation stable. The same release flags are false. tests_passed true is a supplied bounded assessment. tests_note is an object. Declared artifact entries 5, 81671 bytes. Measured artifact rows 5, 81671 bytes. Intake role rows 9, 95759 bytes. Addressed source paths 7, 90980 bytes. Content blobs 7, 90980 bytes. Verified physical files unknown. Artifact hash_match 5, hash_mismatch 0, not_verified 0. Attention lines 6. Stdout sha256 59910e74d971c85ebe93bc5f4741a19365afa0f0f0abf35c61289ae63965796c, 19924 bytes. code_root is the external candidate root.

Disposable fixtures under the same keep directory: the missing review stayed not-recorded and kept authority none. The edited note stayed stale, coherent, with authority none. The digest mismatch stayed held. The installed command withheld the seven current-cut fields. The baseline still projected authority none and accepted false. The unreadable journal cut left stable other than true. Each compared tree matched around the report calls. Setup prepare, record, and publish used the existing review-loop on those disposable books.

The fixed live helper root remains D:\Git\lib-build because labs/workbook-review-pass03/workbook.py sets REPO there and was not edited. A candidate copy of that module still uses that path. The candidate index lists 247 files.

## Blocked

Matching line 0112.prime-review is unfiled. This slice does not file it and does not invent a receipt. Custody on the live reviews stays missing. Verified physical-file identity stays unknown. The shared command is not selected. Codex Prime has not reviewed this pack. This builder does not commit. Production activation remains held.

## Need

Codex Prime review of this return. The candidate command, the pin list, and the rollback are in evidence/build05.09/PRIME-USE.md and evidence/build05.09/INTEGRATION.md. Stop here.

## API and ownership

The caller supplies an absolute book, a source page id, and a pass. The connector derives the code root from the installed app and refuses a second root. It hashes the candidate dispatcher, the historical dependency cut, and the hardening runtime before the runtime starts. The runtime hashes that cut again, except its own file, before pass03 observe. Exit 0 is the reporter's readable state. Exit 0 is not approval. Exit 1 is the reporter's stale, held, not-recorded, or identity-mismatch result. A connector refusal is exit 2, empty stdout, and a stop: line. A runtime or historical reporter refusal keeps the JSON object and a refused: line.

Selection replaces app/librarian.py with the candidate file and requires the three new files to remain at their pinned paths. It does not change v1, v2, pass01, pass02, pass03, or the 05.08 deployment files. Those historical checks still refuse the replaced dispatcher. Rollback restores app/librarian.py from evidence/build05.09/rollback-librarian.py, sha256 c3a5be3b612c021d95effaa5da4a151bf89026422b94f4cad98331014c7f0cd9, 12204 bytes. v3 then refuses the restored dispatcher. v1 and pass03 main accept that restored dispatcher again. v2 and the 05.08 deployment runtime still expect the 05.08 candidate dispatcher, sha256 d37dd14ccb921f92ff1a05c00890d57ee0f3d9f27d766bd86d81861abdd80a52, 12805 bytes.

## Claim, case, result, limit

The table is evidence/build05.09/TEST-TABLE.md. The supported types are evidence/build05.09/supported-schema.md. The invalid and held behavior is evidence/build05.09/invalid-held.md. The pin delta is evidence/build05.09/pin-delta.json. The command hashes are evidence/build05.09/command-log.json. The no-write watch is evidence/build05.09/no-write.json. The candidate file list is evidence/build05.09/candidate-index.json.
