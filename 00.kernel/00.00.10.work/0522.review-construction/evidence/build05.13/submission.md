# Submission - 0522.review-construction/05.13

date: 2026-11-02
executor: Grok-1
reviewer: Codex Prime
accepted: false
committed_by_this_builder: false
custody: pending
matching line: 0122.review-construction unfiled
readiness: returned for Codex Prime review

This is the builder return for the named invocation of 05.13. It is a claim. It is not acceptance, not custody, and not a release. Notes in 06.25.md were reread at close and integrated below. The contract was not revised after tests. This file does not carry the artifact-manifest hash. That hash is written only on the 05.13 return pointer after the manifest exists.

## Did

Verified evidence/pack05.13/source-manifest.json before the notes. Schema prime-pack-inputs/1. 74 files. bad 0. missing live 0. missing snapshot 0. live drift 0. snapshot mismatch 0. extra snapshots 0. Manifest sha256 8671da3bc8344119466628f88a505937f4b9386269d158891bccc5dc7b3e0ed7, 29400 bytes. The manifest is LF-only. The row hashes were not rewritten.

Read 06.24.md. Reproduced K1 and K2 through the then-current v6 door before repair code. K1 was a read-only prepare of the live 0521/05.10 page. K2 was a new copy of the frozen reproducer at D:/librarian/temp/0522-0513-repro/book. Evidence is evidence/build05.13/reproduce/summary.json. The retained reviewer book D:/librarian/temp/prime-two-returns-0512-0510 was not modified. Claude's remaining 0707 acceptance cases were not read. The unfinished Grok-2 repair was not read.

K1 exit 0. Measurement incomplete. Stderr empty. Findings: unparsed-return-line, declared-file-missing, custody-missing, return-missing. The unparsed text is the artifact line through "Excludes itself and thi". The missing path is evidence/build05.10/submission.md. The only row role is assignment. Intake id 6ae3839653bc8a3d1148cd647cade813d64997960a51f8e5322e54f09dbd1742. The page stayed sha256 af56727c4a29007d9a78b0a746af4c949774daf01632bf7c1b7258ce471963c5, 8076 bytes.

K2 prepare exited 0 and measurement was complete. The intake kept submission and verification and also kept those same paths as artifacts. Record exit 2. Recorded false. Stderr empty. Correction: refused: duplicate id at sources. Failed input workbook-review/0599.fixture-review/05.01/failed/6429cac0f00012d9.json. Intake id 86f92dbb4a21e74e0eb40c248317b523bcb7239e685320b9425fa6fca92a1cc4. That tree stays.

Built labs/workbook-review-pass03. It loads the pinned pass02 workbook and replaces pointer parsing, declared-path resolution, declared measurement, intake assembly, and validator source identity. The replacements are installed on the pass02 module and on the pass01 module that pass02 already holds. Pass02, pass01, v6, v5, and v4 stay byte-for-byte. app/librarian.py loads app/review_loop_tools_v7.py for the review-loop command only. The declaration is app/review-loop-v7.json, schema review-loop-pins/5. Fixture commands and --fixture-root stay on the pinned v4 door. Authoring-v2 and return-lines stay on their doors.

The form id stays workbook-review-v1. The only form change from pass02 is correction_help.route, now labs/workbook-review-pass03/PRIME-USE.md. Form sha256 4b8cf0e8c81cc421fd0212ae169ba1557998bf526c5f6d87ee170c9d038cbb0b, 4532 bytes.

The operator suite is labs/workbook-review-pass03/tests/test_workbook.py. The cited run is 6 tests, 192.541 seconds, OK, exit 0, through app/librarian.py. Python 3.14.0. Retained books are under D:/librarian/temp/0522-0513-pass03. The live current-book demonstration was prepare, form, and inspect of the returned 05.10 page. Record and publish were not called there.

## Blocked

Matching line 0122.review-construction is unfiled. This slice does not file it, allocate 0184, or invent a receipt. Custody on the live page stays missing. The live return file 0121.return-placement/05.10.return.md is absent.

Codex Prime has not reviewed this pack. The independent acceptance cases and the real-use gate were not run. This builder does not commit.

Incomplete measurement still blocks record. The live 05.10 prepare is measurement complete, so that block is not the live result. The suite's count-mismatch case and the contradictory-hash case each exited 2 before a record. The grammar book has no journal.

## Need

Codex Prime review of this return. Prime then runs independent acceptance and the real-use gate on a selected actual return. The forms are in evidence/build05.13/PRIME-USE.md and labs/workbook-review-pass03/PRIME-USE.md. Those two files are the same bytes. Stop here.

## API, forms, ownership, and reuse

The public commands stay prepare, form, record, inspect, publish, read, and recover. The caller supplies an absolute book, a source page id, and a pass. Compute derives the assignment, the rows, the form, the target, and the review id. Stdout is one JSON object, schema workbook-review-result/1. Exit 0 is a completed command. Exit 1 means a judgment exists and publication or recovery is blocked. Exit 2 is a refusal before a record, or a bad call. The workbook prints refused:. The librarian wrapper prints stop: for a door refusal.

An owned book is the canonical work book D:/Git/lib-build/00.kernel/00.00.10.work, or a directory whose path and resolve stay outside D:/Git/lib-build. The repo root, any other checkout directory, and a junction whose resolve lands inside the checkout are refused. There is no force flag and no allow-live flag. Writable permission is not judgment, approval, or custody.

Writes this module performs stay under workbook-review/ of that book, or the one derived target: {page}/{pass}.md for N5NN, or {page}/06.{tail}.review.md for N7NN. A filed call also lets the pinned loop write scratch/, trace/, partial/, and support/{review_identity}/ under the book. The v4 fixture-root guard stays. A workbook command with --fixture-root is refused. describe-legacy stays on v4.

A pointer line for Submission, Artifact manifest, or Verification keeps a path, a 64-hex digest, and a byte count ending in bytes. An explanatory suffix is accepted when it starts with a space and contains neither another of those labels nor another 64-hex digest. An artifact-manifest line may instead end in bytes, N files. The remainder is empty, or exactly " Excludes itself.", or exactly " Excludes itself and this page." That count is compared with the number of file entries. A difference adds manifest-count-mismatch and marks measurement incomplete. The entries stay bound. The JSON file_count field is not a second authority. A duplicate label clears only that label. An unknown line is a finding and does not clear a valid label.

locate_declared considers, in order, the declared path under the book, the book remainder of a 00.kernel/00.00.10.work/ prefix, the page-relative path when the declared path does not already start with the page id or that prefix, and the declared path under D:/Git/lib-build. The same resolved file is one candidate and the book wins. Two different files are ambiguous and neither is chosen. There is no parent walk and no search. A hash mismatch keeps the measured row. A missing file adds no row. Code-root rows stay in the intake for drift and are not sent to prime_review.

On the live work book, a qualified work path and the code-root spelling are the same file, so the book wins. A disposable copy that plants a different file at the book remainder stays ambiguous against the repository file. The four labs/return-readiness-pass01 entries bind as code root on the live book. MAX_INDEX bounds only displayed artifact cuts. More than 12 adds index-context-bounded and does not by itself make measurement incomplete. Custody missing does not by itself make measurement incomplete.

When the pointer has no Verification line, four consecutive submission lines are read: Verification, Schema, sha256, and bytes, each in the checked backtick form. One block is measured as role verification. The generic verification-not-measured finding is removed only when that file was measured. A verification-declared finding stays, with successful_run false and the limit "The lines are a declaration, not a successful verification run." sources lists submission-lines and, when an artifact row is the same file, artifact-index. Two well-formed blocks choose neither. The word verification in other prose does not discard a valid pointer field and is not proof that a verifier ran.

Intake rows keep every role: assignment, submission, verification, artifact-manifest, artifact, and return. prime_record emits one validator source per resolved file. Preliminary selection uses the book rows. Filed selection uses assignment, artifact, and return, which is the pass02 filter, and then the same collapse. Rank is assignment, then a return whose path is the capture return path, then another return, then submission, then verification, then artifact. artifact-manifest stays in the intake and is not a validator source kind. Supplied text stays schema supplied-text/1 and label SUPPLIED. bind is true only when capture is absent, including a capture-kind source, which is the pass02 rule. Rows for one file that disagree on measured or declared hash or length add source-identity-conflict, mark measurement incomplete, and the record path refuses with source identity conflict before an id is chosen. Different book instances stay distinct because the instance id includes the absolute book path. Freshness still compares root, role, and path to sha256. Own publication, successor published_target, pointer-pending, tampered render, and source-scoped cycle paths stay on the pass02 functions this overlay does not replace.

Director text is only the body under the Director verbatim heading. The live 05.10 page has Goal, method, and ownership headings and has no Director verbatim heading. director_text stays null. Unknowns stay agreement.goal, agreement.scope, recorded_decisions, and receipt. Member space for 0521 stays 0121.return-placement. A heading is not a grant.

Reuse, pinned and not edited: pass02 workbook and form, pass01 workbook and form, v6 door and declaration, v5 door and declaration, v4 door and declaration, return-access-pass01, review-loop-pass03, review-construction-pass04, prime-cycle-pass03, and prime-review-pass02. The return backend was not upgraded. The band was not migrated. labs/return-lines-pass04 was not imported.

## Pins

| Path | sha256 | bytes |
|---|---|---|
| labs/workbook-review-pass03/workbook.py | 9e66d7e4413e8f0aedcc4ff416080c549ce435b10103149ef73de493b245ff8c | 19533 |
| labs/workbook-review-pass03/forms/workbook-review-v1.json | 4b8cf0e8c81cc421fd0212ae169ba1557998bf526c5f6d87ee170c9d038cbb0b | 4532 |
| app/review_loop_tools_v7.py | 93a89939b6e6143eaffbb75c3b7cb60c38c60ad91902bd15d0b48c5bb35c382d | 10291 |
| app/review-loop-v7.json | bf12aa7cdf67cc6f8e6ae9d674aa39929933293495c6857dc423dab4c1cab8f8 | 3515 |
| app/librarian.py | c3a5be3b612c021d95effaa5da4a151bf89026422b94f4cad98331014c7f0cd9 | 12204 |
| app/README.md | 3c2125aa0cebd7ddc1604de2a823c1250edf40a8e97bd7dbd2eb09ca91155920 | 39687 |
| labs/workbook-review-pass02/workbook.py | 6ce4a5ff2e7505a8b56a13c05af3f5f2e9d8648112a6bf67c0e6392ab043a49a | 52574 |
| labs/workbook-review-pass02/forms/workbook-review-v1.json | 66b3f8f70f8e5d2f940296918767ff0e712e7e144378ad8653259e83d3284645 | 4532 |
| labs/workbook-review-pass01/workbook.py | 60e040fa30f61348adac76a4f3bdfbfdb9aba859f25bacadf317937c167e9b0a | 79131 |
| labs/workbook-review-pass01/forms/workbook-review-v1.json | 152b436bda8e19d15f252bb5208791c8eefd9a658789e2ab6e9789ffa362b49f | 4532 |
| app/review_loop_tools_v6.py | e2a5df36efe29f9dad8abd8fa0f842fd98941d58ca1eb3cd4be5227e20420a94 | 9175 |
| app/review-loop-v6.json | c7f95d16f91644c6465fd3483e3db4d6fb9b9115aa6e20fc09a194fc5bb1f0aa | 2743 |
| app/review_loop_tools_v5.py | b1192daf5d265c66f10adfe2125ff0c92a08ccd3c797d229698ecc20e2fdeed9 | 7875 |
| app/review-loop-v5.json | eaa9120bba2c7274f2218c875ec3ecfc84d291188557049240c30a1c2a430de3 | 1964 |
| app/review_loop_tools_v4.py | 0769179366a6c1659f38cb2c79c51981d5cb76fa8d48ee7325f9eaf00d14c296 | 13381 |
| app/review-loop-v4.json | 769f81321e19a9f3296020e3b0b4a4905ec1b3a66c1629bf53d9548b7182d723 | 2519 |

CONTRACT.md sha256 685b1e86e4a8fb321251c61fa0e65df398ef0c0acddf495f03f00d77ae26a057, 14580 bytes. It was not revised after tests. 06.25.md sha256 0480da3242a46b30cf04cc5456c345b2a766e4e5f28ad8c5b85cc4115e438c87, 9600 bytes. The operator test sha256 e7de8740d3262ed843e52bef173b3fea8c87ea486dfaa3e07e715c4026f37fe0, 41446 bytes. The correction route file sha256 8a280550deb366e08c0b595f92ef87db1b2044da403a40cb2c4f22ea6640fe6d, 4178 bytes. Verification sha256 8c85afe9ec3f290a2604997c3e78876f4a02e8d9404f4d7873000032307139f7, 5018 bytes.

Before this slice, librarian.py was sha256 b15919adb7664f993373fbc6eaaaf86d66100f396b3401845900734f920248ea, 12204 bytes. README.md was sha256 471f689adcfc89b44c2c455500924702bcf8f9eadfc83f8ae9eaa344775a65b6, 39210 bytes. The librarian file is still 12204 bytes. Its hash changed because the review-loop load names v7.

## K1 and K2

K1. Actual return intake. The pre-repair prepare left the page-relative submission unbound and left the count-suffix artifact line unparsed. The repaired live prepare binds that submission as a book row at 0521.return-placement/evidence/build05.10/submission.md and accepts the line that ends in bytes, 16 files. Excludes itself and this page. The exact-copy author case plants those same bytes only at the page-relative paths. That prepare binds the submission as a book file, marks the qualified work path ambiguous against the repository file, and binds an unplanted work path such as 06.20.md as code root. Measurement on that copy stays incomplete. verification-declared sources on that copy are submission-lines only. Limit: the ambiguity between a planted book remainder and the repository file is kept.

K2. Duplicate physical source roles. The pre-repair record on the copied valid fixture refused with duplicate id at sources. The repaired overlap book is wb0513-overlap-lq9emwp7, review w16575353a0a89dda. The intake kept submission and verification and the same paths as artifacts. The validator source list has four unique logical paths: 0599.fixture-review/05.01.md, 0599.fixture-review/evidence/build05.01/submission.md, 0599.fixture-review/evidence/build05.01/VERIFICATION.md, and 0599.fixture-review/evidence/build05.01/payload/parser.py. The contradictory declared-hash case kept both the submission role and the artifact role, marked source-identity-conflict, and exited 2 before a record. Two disposable books with the same page id prepared instance ids bad46e61e45be7232955cc9d78b9ca7072a68b963dec47863d5d7f77ab632541 and d26f9cc0095ced32fb85ffe3f84fe54db7b3a5ebcb1b28393888012da6d3d1c9. Limit: this is the author case. The pre-repair tree was not reused as the repaired record.

## Commands, exits, and first failures

Cited operator command, from D:/Git/lib-build, with PYTHONDONTWRITEBYTECODE=1:

```text
python -B labs/workbook-review-pass03/tests/test_workbook.py
```

Ran 6 tests in 192.541s. OK. Exit 0. The cited suite passed on the first run. The known failures are the K1 and K2 reproductions above. No failed tree was deleted.

Claim to case. The first two are the known reproductions. The rest are new author cases.

- Known K1 reproduction, before repair, through v6: librarian.py review-loop prepare on the live book, source 0521.return-placement, pass 05.10. Result above. Raw stdout is evidence/build05.13/reproduce/k1-prepare.stdout. Stderr is empty.
- Known K2 reproduction, before repair, through v6, on D:/librarian/temp/0522-0513-repro/book. Prepare measurement complete. Record exit 2, refused: duplicate id at sources. Raw stdout files are evidence/build05.13/reproduce/k2-prepare.stdout and k2-record.stdout. The failed input file is still 6429cac0f00012d9.json.
- Predecessor pins, door selection, distinct instances, and the junction: test_pins_and_doors. describe-legacy without --member exited 2 with stop:. Book plus fixture-root exited 2. Record on the repo root exited 2 and the refusal text contains checkout. return-lines status on an outside book exited 0, accepted false, task_association not-established. The two instance ids are the pair above. A close probe created a junction from a disposable directory to D:/Git/lib-build/labs and called record. mklink exited 0. Record exited 2. The stderr text was refused: book is not a directory. labs/workbook-review was not created. The junction was then removed. The suite asserted the same exit and the absent store. This overlay does not rewrite that pinned link check.
- Exact real 05.10 bytes on a disposable copy, plus the live read inside the suite: test_exact_copy_and_live_book. The copy is the K1 limit above. The suite's live prepare matched the later saved current-book run: measurement complete, sixteen artifacts, twelve artifact cuts, verification-declared sources submission-lines and artifact-index, and the page bytes unchanged.
- Overlap fixture, positive page-relative record, alias, and two-root clash: test_overlap_alias_and_positive_record. Overlap review w16575353a0a89dda, mode preliminary, publication status recorded. Positive book wb0513-positive-8xnqa2ma, review wf69ac77259e3c2a4, publication published, target 0591.intake-repair/05.01.md. The finding stayed "The disposable note is present." Read and recover exited 0 with stale false. The kept prime-input paths are 0591.intake-repair/05.01.md, 0591.intake-repair/evidence/build05.01/submission.md, 0591.intake-repair/evidence/build05.01/verification.json, 0591.intake-repair/evidence/build05.01/payload.txt. Alias book wb0513-alias-_tw5i6n5, review w4a5c4edb8508e9b4, publication status recorded. The kept alias prime-input paths are 0590.alias-file/05.02.md, evidence/submission.md, 0590.alias-file/evidence/note.md. Clash book wb0513-clash-nyvz4j7p has no journal. The suite asserted ambiguous-declared-root, measurement incomplete, and no submission row.
- Unparsed line, duplicate label, missing file, count mismatch, and contradictory hashes: test_grammar_holds. Book wb0513-grammar-vs_oy455. The Note line left the submission row in place. The duplicate Submission label cleared only that label and left the artifact-manifest row. The missing file added no submission row. The count of 2 files against one entry added manifest-count-mismatch, kept the artifact row, and the record exited 2 with recorded false. The contradictory declared hash added source-identity-conflict and the record exited 2. The book has no journal.
- Own publication, stale selected source, tampered render, and read-only target: test_publish_seams. Fresh book wb0513-fresh-p0_kcb1j, review wb99ab80970ff0db5, publication published. After note.md changed, read and recover exited 1 with stale true, and inspect exited 0 with stale true. The finding stayed. Tamper book wb0513-tamper-gqvucckq, review w9f0388f5734728a7, publication published. The second publish exited 1 with published false. The target sha256 75cdcc1328254881cc1fd5723e1577474f45b3221e763cccf43e21429644b6e1 does not contain UNRECORDED ALTERATION. Pending book wb0513-pending-m6ysdaah, review w875dd81faea5a515. The 05.07 journal status is pointer-pending. Recover returned that target_state and the stored next action.
- Two filed sources and a successor: test_filed_sources_stay_scoped. Book wb0513-filed-knidhxyz. First source 0596.synth-filed review wdf19dda73993b697 is the published_target on 0596.synth-filed/05.01.md. Successor review w7b1729382e7822f1 is the journal current, status recorded, and its finding is "The Director reply is recorded and the finding stays open." The stored record has successor_of and has no closes_work field. The suite asserted the command result closes_work false and asserted the successor publish exited 1 with the first page bytes unchanged. Second source 0595.synth-filed review we94ec8a37632549f, publication published. Cycle directories are 05.01-wdf19dda73993b697, 05.01-w7b1729382e7822f1, and 05.02-we94ec8a37632549f. workbook-review/cycle/decision.json was not written. The second source's suite recover kept the finding and closes_work false. Limit: the pinned constructor's refusal to replace a filled review section is the successor publish result. This module does not overwrite that section.

Current-book commands, after review-loop-v7.json existed:

```text
python -B app/librarian.py review-loop prepare --book D:/Git/lib-build/00.kernel/00.00.10.work --source 0521.return-placement --pass 05.10
python -B app/librarian.py review-loop form --book D:/Git/lib-build/00.kernel/00.00.10.work --source 0521.return-placement --pass 05.10
python -B app/librarian.py review-loop inspect --book D:/Git/lib-build/00.kernel/00.00.10.work --source 0521.return-placement --pass 05.10
```

Exits 0, 0, 0. Stdout 26418, 16510, and 17604 bytes. Stderr empty. Intake 9d5c5d898b3c75233d285a6823856073d4d30c6a61c6689f125f3a5b78993a48. Page sha256 af56727c4a29007d9a78b0a746af4c949774daf01632bf7c1b7258ce471963c5, 8076 bytes, before and after. No workbook-review/0521.return-placement directory was created. Copies are evidence/build05.13/current-book.

## Actual real-format read-only result

The returned 05.10 pointer was read through v7. It was not PENDING. The submission row is root book, path 0521.return-placement/evidence/build05.10/submission.md, declared path evidence/build05.10/submission.md, sha256 ddccb9110a02d82df300adffc25870c8ebf24d0815dab2651c67ececfaf36de8, 874 bytes. The artifact-manifest row is root book, path 0521.return-placement/evidence/build05.10/artifact-manifest.json, sha256 bbd4e5a33279105f0177491c7eff2ecfa70e172cd0fd6a266d70c2c3b93e809d, 3867 bytes. The count suffix was accepted and the declared count 16 matches the entry count. Sixteen artifact rows are bound. Twelve are book files, including the submission and the verification as artifact rows in addition to their own roles. Four are code-root rows: labs/return-readiness-pass01/README.md, contracts.json, readiness.py, and tests/run_suite.py. Displayed artifact cuts are 12. The findings are index-context-bounded, custody-missing, return-missing, and verification-declared. verification-declared path evidence/build05.10/verification.json, schema return-route-readiness-verification/0510, measured true, hash_match true, successful_run false, sources submission-lines and artifact-index. The verification row is root book, sha256 99497147811cdd4009cfafca11be8594c943971ac63add170b032f9408d81f45, 5177 bytes. There is no unparsed-return-line, declared-file-missing, verification-not-measured, manifest-count-mismatch, source-identity-conflict, ambiguous-declared-root, or artifact-hash-mismatch. Measurement is complete. Custody is missing. Unknowns are agreement.goal, agreement.scope, recorded_decisions, and receipt. The form id is workbook-review-v1. The correction route is labs/workbook-review-pass03/PRIME-USE.md. Director text is null. Inspect judgment is null. Inspect accepted, approved, closes_work, eligible_for_custody_completion, published_work, and releases_action are false. Inspect stale is false. The form command returned the same intake id and an empty findings list. The historical manifest was not rewritten.

## Manual steps remaining

Codex Prime reviews this return. Codex Prime runs the independent acceptance cases and the real-use gate on a selected actual return. Filing 0122.review-construction stays on the accepted route. This builder does not commit, seat, lock, publish a live judgment, or activate a model.

At the close check before the 05.13 pointer fill, frozen snapshots still matched all 74 rows. Live drift was only app/librarian.py and app/README.md. 05.13.md was still the pending page, sha256 48ed137bc886a8cd05c410540ce756d375e579a4df1131919b7ce3387fb50365, 5470 bytes. HEAD 960d20c5290656095df8457b1740d2d5e586b111, branch workshop. The index was empty. This builder did not commit.

## Factfind

The pre-repair outputs still show the incomplete live intake and the duplicate-id refusal. The repaired suite records the overlap fixture with one validator id per resolved file and keeps every intake role. The live inspection binds the real 05.10 submission, the count-suffix manifest, the thin verification declaration, and all 16 artifacts. Custody stays missing. A heading was not treated as a grant. The verification lines stay a declaration.

## Hostile

A green suite is a command result. accepted stays false. successful_run stays false on the live declaration. The successor reply did not close the work. The own review write is not source drift while its published hash still matches. A later change outside that attestation is stale and the judgment stays. The live inspection is an address reading of the returned 05.10 page. It is not a judgment of this pack. The exact copy stays ambiguous where its planted book remainder differs from the repository file. Subst drives and 8.3 names were not exercised.

## Overflow

0122 filing, 0184 allocation, return-backend upgrade, band migration, live review publication, workflow adoption, independent acceptance, and the real-use gate stay outside this build. The 05.12 product and its evidence stay sealed. The contract was not revised after the suite. labs/return-lines-pass04 was not imported. No 06.24 readiness-encoding note was added.

## Unprompted

The one next step is Codex Prime's review. The artifact manifest lists the files for this return and excludes itself. Its hash is written on 05.13 after this submission is frozen. The verification file is evidence/build05.13/verification.json. This pointer does not declare a Verification line.
