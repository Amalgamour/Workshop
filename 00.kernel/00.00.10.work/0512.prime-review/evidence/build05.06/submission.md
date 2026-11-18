# Submission - 0512.prime-review/05.06

date: 2026-11-03
executor: Grok-1
reviewer: Codex Prime
accepted: false
committed_by_this_builder: false
custody: pending
matching line: 0112.prime-review unfiled
readiness: returned for Codex Prime review

This is the builder return for the named invocation of 05.06. It is a claim. It is not acceptance, not custody, and not a release. Notes in 06.09.md were reread after the author suite and integrated there. The contract was not revised after tests. This file does not carry the artifact-manifest hash. That hash is written only on the 05.06 return pointer after the manifest exists.

## Did

Verified evidence/pack05.06/source-manifest.json before the notes. Schema prime-pack-inputs/1. Six files. bad 0. missing live 0. missing snapshot 0. live drift 0. snapshot mismatch 0. extra snapshots 0. Manifest sha256 ec86755ffab3753492e588652989d76bf9ed43e8612fea7fefd0fbb4d399c5ef, 1733 bytes. HEAD 960d20c5290656095df8457b1740d2d5e586b111. Branch workshop. Index empty. The freeze was not repinned. 06.08.md is untracked relative to that commit and its bytes match the manifest.

Read 06.08.md. Reproduced the disclosed two-file collapse on preserved pass02 before any pass03 module existed. unique_files returned scope unique-physical-files, provenance current-measured, count 1, bytes 4. The disclosed rows are two paths and 8 bytes, one shared sha256. matches_disclosed_report true. The result is a known failure, retained at D:/librarian/temp/0512-0506-report/known-failures/identical-files-pass02.json and evidence/build05.06/known-failures/identical-files-pass02.json. sha256 e72b2e2e0b8d8edb8510413eaefa6c7a07e47e442e72878680934de451eacabb, 953 bytes.

Built labs/review-report-pass03. The command is python -B labs/review-report-pass03/report.py --code-root ABS --book ABS --source PAGE --pass 05.NN. Stdout is one JSON object, schema review-report/3, including the ordinary projection of that same object. It calls librarian review-loop inspect, read, and recover through the pass02 reader. It does not prepare, record, publish, or approve. Pass02, the app, the README, the core, and the live review bytes stay in place. The successor is staged and is not activated.

report.py sha256 70028dfe97bc6178a3497c814cf585476bb0b41650ce67fc79dd3d5b118dfade, 8091 bytes. tests/test_report.py sha256 f477fd4e4dac922435fac822a5b85ee34b34d731583a730842b08f5c110e18de, 32678 bytes. CONTRACT.md sha256 e5849352644b63c8f249546d4f5bd7ccad575218d9c2062db2f4814a55babc6c, 12396 bytes. 06.09.md sha256 2e4c96d051383422ba762e6fd205b3d439b3e8316b429d7039e0c21a6118fc73, 6961 bytes. README.md sha256 7eda7f1b02c79c72d301c411de0de3f6bb98e6ba280cad6663cff69ac09e9cb2, 594 bytes. PRIME-USE.md sha256 0faa0ddb5029b5b857de5c1847caf8991aa109ca4ea693d4e985958d60b318ee, 1972 bytes.

The recorded author run was 18 tests, 2.263 seconds, OK, exit 0. Python 3.14.0. The log is evidence/build05.06/author-suite.txt. No product failure occurred. The cases are author cases. The identical-file collapse is a known failure of pass02, not independent coverage of pass03.

The live observation used two processes on the current book, source 0522.review-construction, pass 05.13. Both exited 0 with the same stdout and empty stderr. Review w4c5ae945c250d823. State readable. Observation coherent and stable. Stale false. Publication class complete, status published. Disposition accepted. Custody missing. Authority none. work_complete false. action_released false. accepted, approved, closes_work, and releases_action are false. The six agreement attention lines and the bounded tests_note are in the ordinary projection. tests_passed true is a supplied bounded assessment. claims stay not-recorded.

Declared artifact entries 29, 314945 bytes, scope manifest-declared-artifact-entries, provenance declared. Measured artifact rows 29, 314945 bytes, scope current-measured-artifact-role-rows, provenance current-measured. Addressed source paths 31, 329258 bytes, scope addressed-source-paths, provenance current-measured. Content blobs 25, 325080 bytes, scope content-sha256, provenance current-measured. Verified physical files unknown, scope verified-physical-files, provenance not-established. Intake role rows 32, 354914 bytes, scope full-intake-role-rows, provenance current-measured. Artifact hash_match 29, hash_mismatch 0, not_verified 0. Measurement complete. The saved stdout is evidence/build05.06/current-review/report.json, sha256 170028a6a6ee8817ac091d5e2c9642b8c250c32d6ac728fe89a554f526c8a06d, 29742 bytes. summary.json is an extract of that object.

Preserved pass02 unique_files, called on those 32 saved rows, still returns count 25 and bytes 325080, scope unique-physical-files. One address, book and 0522.review-construction/evidence/build05.13/submission.md, has two roles, submission and artifact. Six addressed sources share the 0-byte content hash e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855. Two addressed sources share 8a280550deb366e08c0b595f92ef87db1b2044da403a40cb2c4f22ea6640fe6d at 4178 bytes. Addressed bytes include that 4178 twice. Content bytes include it once. The old unique-file total is the content-blob total. It is not a verified physical-file count.

Frozen source bytes matched the pack05.06 manifest before and after the live pair. app/README.md stayed sha256 3c2125aa0cebd7ddc1604de2a823c1250edf40a8e97bd7dbd2eb09ca91155920, 39687 bytes. The reader did not record, publish, or approve. 0512/05.04 was not observed again.

## Blocked

Matching line 0112.prime-review is unfiled. This slice does not file it and does not invent a receipt. Custody on the live review stays missing. The six agreement fields stay unknown. Verified physical-file identity cannot be established from the accepted intake keys. The proposed core exposure is not applied. Pass03 is not selected as a renderer and is not added to the pin table. Codex Prime has not reviewed this pack. This builder does not commit.

## Need

Codex Prime review of this return. The counter delta is in the contract and in labs/review-report-pass03/PRIME-USE.md. Stop here.

## API and ownership

The caller supplies an absolute code root, an absolute book, a source page id, and a pass. The process checks the pass01 pins, binds journal current, record digest, and publication identity, then inspects, reads, and recovers that one address. It rechecks the binding before record metadata and again before the projection is attached. Exit 0 means that bound cut stayed stable, the record checked out, and the core stale flag is false. Exit 1 returns the report for stale, held, not-recorded, or identity-mismatch. Exit 2 is a bad call, a pin mismatch, or a non-JSON core result. Exit 0 is not approval.

A digest that is missing, not a string, or different from the bound digest is rejected before record.json is read. A change during the observation yields state held, observation status unstable, and leaves judgment, attention, and custody unexposed. The bound id stays the selected id. There is no rebaseline and no retry. The reporter has no lock, no concurrency control, and no power-loss guarantee.

Declared artifact entries, measured artifact-role rows, and full intake role rows keep the pass02 scopes. unique_files is not emitted. Addressed sources are exact root and path strings, with no slash folding, no case folding, and no dot-segment resolution. Content blobs are 64-character lowercase sha256 values and prove content equality only. Verified physical files stay unknown, with the reason that accepted intake metadata has no physical-file identity. The counters do not stat, list, open, or re-hash the paths, and they do not claim a hard link. Unknown totals stay null. A missing submission finding is not a missing payload. Claims stay not-recorded. Historical rendered.md stays the published bytes.

Pins are the pass01 table, checked by the same function. app/librarian.py was not edited. app/README.md stayed sha256 3c2125aa0cebd7ddc1604de2a823c1250edf40a8e97bd7dbd2eb09ca91155920, 39687 bytes. The lab does not edit them. core_call remains the pass03 module global.

## Claim, case, result, limit

| Claim | Case | Result | Limit |
|---|---|---|---|
| Pass02 unions equal hashes into one physical file | known identical-file file | pass02 count 1, bytes 4, scope unique-physical-files | known failure of pass02, not new coverage |
| Two distinct equal-content paths stay distinct | author two-file | addressed 2 and 8 bytes; content 1 and 4 bytes; physical unknown | author case on the disclosed rows |
| Repeated roles share one addressed source | repeated roles | addressed 1 and 4; intake 2 and 8; declared 1 and 4 | author case |
| The same relative path in two roots is two addresses | two roots | addressed 2 and 8; content 1 and 4 | author case |
| A missing path blocks the addressed total | missing path | addressed unknown; content 2 and 8; intake still 2 and 8 | a partial addressed sum is not a total |
| Identical hashes without paths have no addressed total | no paths | addressed unknown; content 1 and 4; physical unknown | author case |
| Distinct contents stay distinct | two hashes | addressed 2 and 12; content 2 and 12 | author case |
| Null measurement and empty rows | null and empty | incomplete stays unknown; empty complete is addressed 0 and content 0; physical stays unknown | zero rows is not zero physical files |
| Path strings are exact | unnormalized | four addresses and one content blob | no slash, case, or dot folding |
| Disagreeing sizes leave bytes unknown | sizes and a boolean | count measured; bytes unknown | a boolean is not an int |
| An uppercase hash is not a content id | uppercase | addressed 2 and 8; content unknown | hex case is not folded |
| A different expected digest is held before the record read | digest | digest-mismatch; record.json was not read | author regression of the pass02 guard |
| Journal current moved during the read | current-changed | held; unstable; bound id kept; attention unexposed | author case; final recheck, not a lock |
| Finish rechecks before the projection | finish | held; attention withheld | a change after that recheck is outside the observation |
| Four-role row totals keep their scopes | four-role fixture | declared 1 and 4; intake 4 and 64; addressed 4 and 64; content 4 and 64; physical unknown | equal counts are not a physical-file total |
| A bad call does not reach the core | usage and pin mismatch | exit 2; schema review-report/3 | author case |
| The counters do not stat | patched filesystem probes | addressed 2 and 8; probes uncalled | author case |
| The live 05.13 review can be read without writes | live, two processes | exit 0 twice; objects match; six lines; note; custody missing; no release; physical unknown | observation only; 31 addressed sources and 25 content blobs |

## Counts and provenance

The live counts above are one observation of the current intake. Addressed identity is the exact root string plus the exact path string. Content identity is a 64-character lowercase sha256. Physical identity is not established. Row totals use the pass02 rules: declared entries are role artifact with a declared sha256 string and declared int size; measured artifact rows are role artifact; intake rows are every role. The pass02 call on the saved rows is provenance for the retired total. It is not a second live observation and it is not independent coverage.

## First failures

None. The recorded author run is the first run. Exit 0. The held-cut JSON under evidence/build05.06/hostile/ is the passing author result for the journal-current change, saved from that run.

## Limits

The physical counter stays unknown on every report, including an empty complete intake. The lab does not probe the filesystem and does not claim a hard link. The observation limit is the pass02 sentence: no lock, no concurrency control, and no power-loss guarantee. Pass03 is not activated. The author suite is not an independent run and it does not rerun Prime's suite. Custody remains missing. Matching line 0112.prime-review remains unfiled. This builder does not commit.

## Reread

06.09.md states the freeze, the reproduction, the three identities, the repair, and the live counts. It does not carry this file's hash or the manifest hash.
