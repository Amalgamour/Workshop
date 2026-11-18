# Submission - 0512.prime-review/05.05

date: 2026-11-03
executor: Grok-1
reviewer: Codex Prime
accepted: false
committed_by_this_builder: false
custody: pending
matching line: 0112.prime-review unfiled
readiness: returned for Codex Prime review

This is the builder return for the named invocation of 05.05. It is a claim. It is not acceptance, not custody, and not a release. Notes in 06.07.md were reread after the author suite and integrated there. The contract was not revised after tests. This file does not carry the artifact-manifest hash. That hash is written only on the 05.05 return pointer after the manifest exists.

## Did

Verified evidence/pack05.05/source-manifest.json before the notes. Schema prime-pack-inputs/1. 81 files. bad 0. missing live 0. missing snapshot 0. live drift 0. snapshot mismatch 0. extra snapshots 0. Manifest sha256 64f351bd93eb483149daa2523e8ddd9d0ba2782454eb6e04e6920bb7a1fc865c, 30349 bytes. HEAD 960d20c5290656095df8457b1740d2d5e586b111. Branch workshop. Index empty. The freeze was not repinned.

Read 06.06.md. Reproduced both disclosed probes on preserved pass01 before any pass02 module existed. P1 returned ok and exposed UNVERIFIED SECOND-CUT ATTENTION. The constructed second record sha256 is d49ec3f342665abd5b18fe46e819f28c6bcdce5eab9ee844c7828d611d300b06, the disclosed second hash. P2 returned count 4 and bytes 64. Those results are known failures, retained under D:/librarian/temp/0512-0505-report/known-failures/ and evidence/build05.05/known-failures/.

Built labs/review-report-pass02. The command is python -B labs/review-report-pass02/report.py --code-root ABS --book ABS --source PAGE --pass 05.NN. Stdout is one JSON object, schema review-report/2, including the ordinary projection of that same object. It calls librarian review-loop inspect, read, and recover. It does not prepare, record, publish, or approve. Pass01, the app, the README, the core, and the live review bytes stay in place. The successor is staged and is not activated.

report.py sha256 d13d8d4f54d79cbdb22e1a40fdffb89bd26b85a611bf8620dc36854be9eb852e, 38323 bytes. tests/test_report.py sha256 eee970c6940872c742c93c2d3cb0019a6beea93cb027d6dac15fa5de2d03b559, 31995 bytes. CONTRACT.md sha256 5b01827e5d1c6e39603dedee3bacd59168cc8e2d344c001c65971b081247cd4a, 15306 bytes. 06.07.md sha256 9fdadc895702161cb0c4716cb8b147f2b331165a458e079763eacf7ff6b15b9c, 5442 bytes. README.md sha256 f824ef4f6f0c35232da5a884a953906541243454b1c048c8106c94e6e07c61ed, 529 bytes. PRIME-USE.md sha256 b10374134889e35e7b8f0b36435d7aa6e72b811fee4387fb577b1c3fea1a60a3, 1603 bytes.

The recorded author run was 15 tests, 3.103 seconds, OK, exit 0. Python 3.14.0. The log is evidence/build05.05/author-suite.txt. No product failure occurred. The cases are author cases. The two disclosed probes are known failures of pass01, not independent coverage of pass02.

The live observation used two processes on the current book, source 0522.review-construction, pass 05.13. Both exited 0 with the same stdout and empty stderr. Review w4c5ae945c250d823. State readable. Observation coherent and stable. Stale false. Publication class complete. Disposition accepted. Custody missing. Authority none. work_complete false. action_released false. The six agreement attention lines and the bounded tests_note are in the ordinary projection. tests_passed true is a supplied bounded assessment. Declared artifact entries 29, 314945 bytes. Measured artifact rows 29, 314945 bytes. Unique physical files 25, 325080 bytes. Intake role rows 32, 354914 bytes. Artifact hash_match 29. The saved stdout is evidence/build05.05/current-review/report.json.

0512.prime-review/05.04 review weffe9a51780b52b3 was observed in a separate process. State readable, exit 0, stale false, disposition correction-required, custody missing, work_complete false, action_released false. That observation is not a product pass. The saved stdout is evidence/build05.05/current-review/correction-required.json. Frozen source bytes, pass01, and app/README.md sha256 3c2125aa0cebd7ddc1604de2a823c1250edf40a8e97bd7dbd2eb09ca91155920 stayed unchanged.

## Blocked

Matching line 0112.prime-review is unfiled. This slice does not file it and does not invent a receipt. Custody on the live reviews stays missing. The six agreement fields stay unknown. The proposed core exposure is not applied. Pass02 is not selected as a renderer. Codex Prime has not reviewed this pack. This builder does not commit.

## Need

Codex Prime review of this return. The integration delta is in the contract and in labs/review-report-pass02/PRIME-USE.md. Stop here.

## API and ownership

The caller supplies an absolute code root, an absolute book, a source page id, and a pass. The process checks the pass01 pins, binds journal current, record digest, and publication identity, then inspects, reads, and recovers that one address. It rechecks the binding before record metadata and again before the projection is attached. Exit 0 means that bound cut stayed stable, the record checked out, and the core stale flag is false. Exit 1 returns the report for stale, held, not-recorded, or identity-mismatch. Exit 2 is a bad call, a pin mismatch, or a non-JSON core result. Exit 0 is not approval.

A digest that is missing, not a string, or different from the bound digest is rejected before record.json is read. A change during the observation yields state held, observation status unstable, and leaves judgment, attention, and custody unexposed. The bound id stays the selected id. There is no rebaseline and no retry. The reporter has no lock, no concurrency control, and no power-loss guarantee.

Declared artifact entries, measured artifact-role rows, unique physical files, and full intake role rows are separate counters with scope and provenance. Unknown totals stay null. A missing submission finding is not a missing payload. Claims stay not-recorded. Historical rendered.md stays the published bytes.

Pins are the pass01 table, checked by the same function. app/librarian.py stayed the frozen bytes. app/README.md stayed sha256 3c2125aa0cebd7ddc1604de2a823c1250edf40a8e97bd7dbd2eb09ca91155920, 39687 bytes. The lab does not edit them.

The proposed later core change is to add attention, prime_review_effective, journal current, record digest, and publication identity from the same journal-checked record to inspect, read, and recover. This pack does not edit the core.

## Claim, case, result, limit

| Claim | Case | Result | Limit |
|---|---|---|---|
| Pass01 exposes a different string digest | known P1 file and retained probe | pass01 result ok, second_cut_exposed true; pass02 digest-mismatch before the record read | known failure of pass01, not new coverage |
| Pass01 counts every intake role as an artifact | known P2 file | pass01 count 4, bytes 64 | known failure of pass01 |
| A different expected digest is held | expected-digest mismatch | digest-mismatch; missing, non-string, and different string all stop before a missing record file | author reproduction of the disclosed probe |
| A cut already coherent at the start is reported | coherent-before | exit 0; attention shown; bound digest is that cut | author case; one observation only |
| Journal current moved during the read | current-changed | exit 1; held; unstable; review id stays the bound id; other attention absent | author case; final recheck, not a lock |
| Publication identity moved while the id stayed | publication-changed | exit 1; held; class unknown; bound status kept; judgment unexposed | author case |
| Record metadata moved during the observation | metadata-changed | exit 1; held; new attention absent | author case |
| Four roles are not four artifacts | four-role fixture | declared 1 and 4 bytes; intake 4 and 64 bytes; unique 4 and 64 bytes | author case on the disclosed rows |
| Overlapping roles are one unique file | aliases | unique count 1, bytes 4; intake count 3, bytes 12; three role rows remain | author case |
| A missing submission is not a missing payload | submission versus artifact | submission-missing leaves the payload total; artifact-missing is the only missing payload and makes the declared total unknown | author case; the missing path is not created |
| Null totals stay unknown | null counts | count null; a null byte is not zero; incomplete measurement does not sum a total | author case |
| A historical judgment stays with stale intake | historical stale | exit 1; stale true; correction-required finding kept; declared total unknown | author case |
| Finish rechecks before the projection | finish | a publication change after observe clears the attention before the projection | author case; a change after that recheck is outside the observation |
| A newer folder is not selected | hostile-newer-folder | exit 0; bound id kept; NEWER FOLDER WINS absent | author hostile; not independent |
| A mid-observation matching pair is not adopted | hostile-rebaseline | exit 1; unstable; SECOND CUT ADOPTED absent; bound digest differs from the recheck | author hostile; not independent |
| The live 05.13 review can be read without writes | live, two processes | exit 0 twice; objects match; six lines; note; accepted; custody missing; scoped counts | observation only |
| The 05.04 correction-required record can be observed | 05.04 observation | exit 0; disposition correction-required; custody missing | not a product pass |

## Factfind, hostile, overflow, unprompted

Factfind: the pass01 condition accepts a different string because inequality and the type test are joined so a string skips the rejection. A non-string already returned journal-mismatch on pass01 and exposed nothing. The live 05.13 intake has 32 role rows, 29 of them artifacts, and 25 unique physical files under the successor rules. The stored render remains a separate historical view.

Hostile: newer-folder and rebaseline are above. Raw JSON is evidence/build05.05/hostile/. The known-failure probe record is evidence/build05.05/known-failures/p1-book/.

Overflow: none. Reasons, findings, rows, and render coverage stay in the JSON object. The ordinary projection names those fields and does not repeat them. No padding count was added.

Unprompted: ten frozen prime-review05.04 evidence files contain CR and were left unchanged. The wider worktree already differed from commit 960d20c. Frozen rows matched their snapshots. app/README.md is a neighbor, not a 05.05 freeze row, and its hash stayed 3c2125aa0cebd7ddc1604de2a823c1250edf40a8e97bd7dbd2eb09ca91155920.

## Reread

06.07.md states the freeze, the two reproductions, the repair, the live counts, and the 05.04 observation. It does not carry this file's hash or the manifest hash.
