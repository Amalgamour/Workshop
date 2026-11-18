# Submission - 0522.review-construction/05.12

date: 2026-11-02
executor: Grok-1
reviewer: Codex Prime
accepted: false
committed_by_this_builder: false
custody: pending
matching line: 0122.review-construction unfiled
readiness: returned for Codex Prime review

This is the builder return for the named invocation of 05.12. It is a claim. It is not acceptance, not custody, and not a release. Notes in 06.23.md were reread at close and integrated below. The contract was not revised after tests. This file does not carry the artifact-manifest hash. That hash is written only on the 05.12 return pointer after the manifest exists.

## Did

Verified evidence/pack05.12/source-manifest.json before the notes. Schema prime-pack-inputs/1. 92 files. bad 0. missing live 0. missing snapshot 0. live drift 0. snapshot mismatch 0. extra snapshots 0. Manifest sha256 7e6a6366bb87cb06c46b5eea8e133c8eaf2b1bae9ae8095d4cbdcd32c5de4563, 34288 bytes. The manifest is LF-only. The row hashes were not rewritten.

Read 06.22.md. Reproduced R3 and R4 on disposable copies through the then-current v5 door before repair code. The trees are D:/librarian/temp/0522-0512-repro/r3/book and D:/librarian/temp/0522-0512-repro/r4/book. Evidence is evidence/build05.12/reproduce/summary.json. The retained reviewer book D:/librarian/temp/0522-0511-prime/book was not modified. Claude's 0707/05.10 cases were not read.

R3 review wd8d1ad845807c24b. Changed return sha256 50071197731bf76999d74c6984659be52d577b4b0449e753d0018b249c654c5d. source-inspect exit 0, stale true. source-recover exit 0, stale false. source-read exit 0, and the result had no stale field. The finding stayed "Reviewer probe judgment ONE; preserve these exact words."

R4 review wb60bbc93f6ad4e75. tamper-publish exit 0, published true. The target 0796.prime-probe/06.01.review.md contained UNRECORDED ALTERATION, sha256 c701a5e8e9ee4ca59fb0fcf7bace10354a6b9091ebd968ff54b9b0d6628ac55c. tamper-recover exit 1, stale true. The finding stayed the same. Those trees stay. They are the pre-repair failures.

Built labs/workbook-review-pass02. It loads the pinned pass01 workbook and replaces ownership, pointer parsing, root mapping, freshness, the pre-publish render check, and the cycle identity scope. Pass01, v5, and v4 stay byte-for-byte. app/librarian.py loads app/review_loop_tools_v6.py for the review-loop command only. The declaration is app/review-loop-v6.json, schema review-loop-pins/4. Fixture commands and --fixture-root stay on the pinned v4 door. Authoring-v2 and return-lines-v2 stay on their doors.

The form id stays workbook-review-v1. The only form change from pass01 is correction_help.route, now labs/workbook-review-pass02/PRIME-USE.md. Form sha256 66b3f8f70f8e5d2f940296918767ff0e712e7e144378ad8653259e83d3284645, 4532 bytes.

The operator suite is labs/workbook-review-pass02/tests/test_workbook.py. The cited run is 6 tests, 184.929 seconds, OK, exit 0, through app/librarian.py. Python 3.14.0. Retained books are under D:/librarian/temp/0522-0512-pass02. The live current-book demonstration was prepare, form, and inspect of the returned 05.11 page. Record and publish were not called there.

## Blocked

Matching line 0122.review-construction is unfiled. This slice does not file it, allocate 0184, or invent a receipt. Custody on the live page stays missing. The live return file 0122.review-construction/05.11.return.md is absent.

The historical 05.11 artifact manifest names app/librarian.py and app/README.md at their pre-repair hashes. This slice edited those two files. The live prepare keeps the measured rows and reports artifact-hash-mismatch. Measurement is incomplete. Incomplete measurement blocks record. This builder did not record or publish on the live book, so that block was not executed there. The synthetic incomplete intake in the suite did block record.

Codex Prime has not reviewed this pack. The independent acceptance cases and the real-use gate were not run. This builder does not commit.

## Need

Codex Prime review of this return. Prime then runs independent acceptance and the real-use gate. The forms are in evidence/build05.12/PRIME-USE.md and labs/workbook-review-pass02/PRIME-USE.md. Those two files are the same bytes. Stop here.

## API, forms, ownership, and reuse

The public commands stay prepare, form, record, inspect, publish, read, and recover. The caller supplies an absolute book, a source page id, and a pass. Compute derives the assignment, the rows, the form, the target, and the review id.

An owned book is the canonical work book D:/Git/lib-build/00.kernel/00.00.10.work, or a directory whose path and resolve stay outside D:/Git/lib-build. The repo root, any other checkout directory, and a junction whose resolve lands inside the checkout are refused. There is no force flag and no allow-live flag. Writable permission is not judgment, approval, or custody.

Writes this module performs stay under workbook-review/ of that book, or the one derived target: {page}/{pass}.md for N5NN, or {page}/06.{tail}.review.md for N7NN. A filed call also lets the pinned loop write scratch/, trace/, partial/, and support/{review_identity}/ under the book. The v4 fixture-root guard stays. A workbook command with --fixture-root is refused. describe-legacy stays on v4.

Pointer lines for Submission, Artifact manifest, and Verification keep a declared path, a 64-hex digest, and a byte count. An explanatory suffix is accepted when it starts with a space and contains neither another of those labels nor another 64-hex digest. A duplicate label clears only that label. An unknown line is a finding and does not clear a valid label. A declared path is book-relative, or the book remainder of a 00.kernel/00.00.10.work/ prefix, or a code-root path. The same resolved file is one candidate and the book wins. Two different files are ambiguous and neither is chosen. No parent walk and no search. A hash mismatch keeps the measured row and is a finding. A missing file is a finding and adds no row. Every manifest entry is bound. MAX_INDEX bounds only displayed artifact cuts. More than 12 adds index-context-bounded and does not drop a later row from the intake id. Code-root rows bind for drift and are not sent to the cycle as book files.

One freshness result covers read, inspect, and recover. The journaled publication whose after_sha256 still matches the current target is this module's own review write and does not by itself make the source stale. A successor record keeps that attestation on published_target. Any other assignment, return, artifact, or source change is stale. Fresh read includes stale false. Stale read and recover exit 1 and still return the stored judgment and next action. Inspect exits 0 with the same boolean.

Before any target write, stored rendered.md must equal the record's rendered field and a fresh render of that record, and the record file hash must equal the journal. A difference exits 1 and leaves the target and the journal unchanged. A read-only target moves the journal to pointer-pending and then refuses. The record stays.

Cycle descriptor, registration, request, and decision for one review live under workbook-review/{page}/{pass}/{review_id}/cycle/. The cycle review location for one source and pass is workbook-review/{page}/{pass}/cycle-records/. Registration review_identity is the public w+16 hex id. The decision and cycle record id is {pass}-{that id}. A successor on the same source uses the same review location, a new id, and the cycle template's supersedes. The pinned constructor does not replace a review section that is already filled. That publish exits 1, the target bytes stay, and both records stay. This module does not write the successor text over that section. A reply does not set closes_work or release.

Reuse, pinned and not edited: pass01 workbook and form, v5 door and declaration, v4 door and declaration, return-access-pass01, review-loop-pass03, review-construction-pass04, prime-cycle-pass03, and prime-review-pass02. The return backend was not upgraded. The band was not migrated. labs/return-lines-pass04 was not imported.

## Pins

| Path | sha256 | bytes |
|---|---|---|
| labs/workbook-review-pass02/workbook.py | 6ce4a5ff2e7505a8b56a13c05af3f5f2e9d8648112a6bf67c0e6392ab043a49a | 52574 |
| labs/workbook-review-pass02/forms/workbook-review-v1.json | 66b3f8f70f8e5d2f940296918767ff0e712e7e144378ad8653259e83d3284645 | 4532 |
| app/review_loop_tools_v6.py | e2a5df36efe29f9dad8abd8fa0f842fd98941d58ca1eb3cd4be5227e20420a94 | 9175 |
| app/review-loop-v6.json | c7f95d16f91644c6465fd3483e3db4d6fb9b9115aa6e20fc09a194fc5bb1f0aa | 2743 |
| app/librarian.py | b15919adb7664f993373fbc6eaaaf86d66100f396b3401845900734f920248ea | 12204 |
| app/README.md | 471f689adcfc89b44c2c455500924702bcf8f9eadfc83f8ae9eaa344775a65b6 | 39210 |
| labs/workbook-review-pass01/workbook.py | 60e040fa30f61348adac76a4f3bdfbfdb9aba859f25bacadf317937c167e9b0a | 79131 |
| labs/workbook-review-pass01/forms/workbook-review-v1.json | 152b436bda8e19d15f252bb5208791c8eefd9a658789e2ab6e9789ffa362b49f | 4532 |
| app/review_loop_tools_v5.py | b1192daf5d265c66f10adfe2125ff0c92a08ccd3c797d229698ecc20e2fdeed9 | 7875 |
| app/review-loop-v5.json | eaa9120bba2c7274f2218c875ec3ecfc84d291188557049240c30a1c2a430de3 | 1964 |
| app/review_loop_tools_v4.py | 0769179366a6c1659f38cb2c79c51981d5cb76fa8d48ee7325f9eaf00d14c296 | 13381 |
| app/review-loop-v4.json | 769f81321e19a9f3296020e3b0b4a4905ec1b3a66c1629bf53d9548b7182d723 | 2519 |

CONTRACT.md sha256 18f6372b76e4ac73086f30b22e7676f04a763a58f0fd0a6e01bfee3ba652e728, 10559 bytes. It was not revised after tests. 06.23.md sha256 ec7e4ff1a7534dc95c5ca12e455eed11f0aafb4fe435df31084a050c04437c01, 4911 bytes. The operator test sha256 4047821c14112cd1c73aa55c8d8227c9855d9385903e107ad9e560721dad1054, 35497 bytes. The correction route file sha256 205c3a7d1892b323ef0284a8539a624bc49f81fc202bf873b99a21e21daef596, 4443 bytes. Verification sha256 ff0396fc9d3ae06e10e4c6b2a38aa125ead0cee0a3532990d021a21024c45272, 4322 bytes.

Before this slice, librarian.py was sha256 e2d85b1b641d8a1113b0afaa67a9b8203eb58e9f1028308be922a806fffa5f90, 12204 bytes. README.md was sha256 d30d68d47cf90475f7f4b7abe9215c3ad2b323535494e2000bfc306f302f6c16, 38352 bytes. The librarian file is still 12204 bytes. Its hash changed because the review-loop load names v6.

## R1-R5

R1. Actual operating book. The overlay allows the canonical work book and an outside book. Record on the repo root exited 2 and the refusal text contains checkout. A close probe created a junction from a disposable directory to D:/Git/lib-build/labs and called record. The pinned book check treats that reparse point as a link and refuses it before following the link. The refusal text was "book is not a directory". Probe exit 2. labs/workbook-review was not created. The junction was then removed. The retained probe directory is D:/librarian/temp/0522-0512-pass02/wb0512-junction-fgf9erq7. This overlay does not rewrite that pinned link check. Limit: this builder did not record or publish on the live book. Prepare, form, and inspect of that book are the read-only demonstration below.

R2. Real published return formats. The suite's real-format page kept an explanatory manifest suffix, raised unparsed-return-line for a separate Note line, raised verification-not-measured, bound 16 artifact rows, capped artifact cuts at 12, mapped a repository-qualified path onto the book remainder, and bound app/review-loop-v5.json as a code-root row. Measurement on that page was complete. A different book file and the real repo file for the same declared path were ambiguous-declared-root, measurement incomplete, and no artifact row was stored. The frozen build05.06 submission is 757 bytes, sha256 2a245a1736c828644cbbdbe4930d705499522c5bd40f116d01ca54c2ed26ed0f. The suite raised thin-submission only if that file was under 400 bytes. It is not under 400 bytes, so thin-submission was not raised. Limit: these are author cases. The live 05.11 result is the separate read-only section below. Missing custody stays missing.

R3. Changed selected return after publication. The pre-repair tree still shows recover exit 0 with stale false and read with no stale field. The repaired author case is a new book, wb0512-source-_37k6t6n. After the return change, inspect exited 0 with stale true, and read and recover exited 1 with stale true. The stored next action stayed. Limit: this is not the retained reviewer book and not Prime's independent case.

R4. Tampered rendered.md before a second publish. The pre-repair tree still contains the unrecorded sentence in the target. The repaired author case is wb0512-tamper-u29z4b0j. The second publish exited 1 with published false. The target does not contain UNRECORDED ALTERATION. The finding stayed. Limit: author-executed. The check runs before the target write.

R5. Filed identity. The repaired book is wb0512-filed-z6j1lmni. Two filed sources recorded and published as cycle-committed. Their public review ids differ. Their request paths differ. workbook-review/cycle/decision.json was not written. The successor record stored the reply and did not set closes_work. The successor publish exited 1 and the first page bytes stayed equal to the bytes saved after the first publish. The second source still recovered its original finding with closes_work false. The first source's reviews are w7b1ecc1614ace9a5 and successor wbdeeed781eb6d9d7. Journal current is the successor, and its publication status is recorded because the successor publish did not complete. published_target still records the first review w7b1ecc1614ace9a5 as published on 0596.synth-filed/05.01.md. The second source's review is w80a16eb31f70a7cd and its publication status is published. Limit: the pinned constructor's refusal to replace a filled review section is the successor publish result. This module does not overwrite that section. The pinned cycle and constructor were not edited. R5 was not an independently executed collision before this repair. The collision proof is this author case.

## Commands, exits, and first failures

Cited operator command, from D:/Git/lib-build, with PYTHONDONTWRITEBYTECODE=1:

```text
python -B labs/workbook-review-pass02/tests/test_workbook.py
```

Ran 6 tests in 184.929s. OK. Exit 0.

The first full run of that file exited 1 after 101.954s. Five tests passed. test_filed_two_sources_and_successor raised KeyError: cycle. Record had exited 0 and mode was cycle-committed. The result object did not include the cycle object that the record file already stored. The overlay's record result now includes that object. app/review-loop-v6.json was regenerated from the new workbook bytes. The filed case alone then passed in 93.467s. The cited suite is the rerun after that regeneration. The failed book's copy remains under D:/librarian/temp/0522-0512-pass02. No failed tree was deleted.

Claim to case, all author-executed:

- Owned book and predecessor pins: test_predecessors_and_doors. describe-legacy without --member exited 2 with stop:. Book plus fixture-root exited 2. Undeclared band 0499.other exited 2 and missing contains route. return-lines status on an outside book exited 0, accepted false, task_association not-established. Authoring form on the five seeded profile files exited 0 with schema authoring-form/1.
- Real pointer suffix, bounded index, code root, and ambiguous root: test_real_format_binding. CRLF page text still returned director text Pack it up. without a carriage return. Null tests_passed stayed null. Same-byte record returned the same review id.
- Duplicate submission, missing artifact, omitted semantic_conflict, and incomplete record block: test_ambiguous_incomplete_and_omission. Both record calls exited 2. The omitted field named semantic_conflict. The complete judgment against the incomplete intake was not recorded.
- Own publication stays fresh, an outside assignment word is stale, tampered render is not published, and a changed return is stale on read and recover: test_publish_freshness_and_tamper. Fresh book wb0512-fresh-qfsmdw5o, review w5d4889b704dc422c, publication published. Tamper book wb0512-tamper-u29z4b0j, review w88667a2812f74091, publication published, and the unrecorded sentence is absent from the target. Source book wb0512-source-_37k6t6n, review w92bd4a34e9f3c13a, publication published.
- Read-only target and conflicting retry: test_interrupt_conflict_and_manual. Book wb0512-block-rqiw40ea. The 05.07 journal moved to pointer-pending. Recover returned that target_state and the stored next action. A different judgment without --successor exited 2 and was not recorded. Review w97e49d8a961e1993. The 05.07 publication status is pointer-pending.
- Two filed sources and a successor: test_filed_two_sources_and_successor, as in R5.

Current-book commands, after review-loop-v6.json existed:

```text
python -B app/librarian.py review-loop prepare --book D:/Git/lib-build/00.kernel/00.00.10.work --source 0522.review-construction --pass 05.11
python -B app/librarian.py review-loop form --book D:/Git/lib-build/00.kernel/00.00.10.work --source 0522.review-construction --pass 05.11
python -B app/librarian.py review-loop inspect --book D:/Git/lib-build/00.kernel/00.00.10.work --source 0522.review-construction --pass 05.11
```

Exits 0, 0, 0. Stdout 24222, 15285, and 16601 bytes. Stderr empty. Intake 3967e58683f55ad50f71ada8ecde4f6726c131069232e6237e09f00a5e072f3d. Page sha256 531482b4b7a0c14cc2a6aba7014089972636a54e013cbc75ed3cedd786f32ef2, 11646 bytes, before and after. No workbook-review/0522.review-construction directory was created. Copies are evidence/build05.12/current-book.

## Actual real-format read-only result

The returned 05.11 pointer was read through v6. It was not PENDING. The submission row is root book, path 0522.review-construction/evidence/build05.11/submission.md, declared path 00.kernel/00.00.10.work/0522.review-construction/evidence/build05.11/submission.md, sha256 409b983fd58f6432b356ebecb716f250cec4e2406c0c443d5a0fa3e91fe6c96c, 16825 bytes. The artifact-manifest row is root book, path 0522.review-construction/evidence/build05.11/artifact-manifest.json, sha256 ec7ff7fbc7cf1e2939439ff85c82e7a0f3ab46f0b2d4cf4649c870e5faa4ed3e, 4637 bytes. The explanatory suffix on that historical line was accepted. Twenty artifact rows are bound, including the code-root rows for app/librarian.py, app/README.md, app/review-loop-v5.json, app/review_loop_tools_v5.py, and the pass01 lab files. Displayed artifact cuts are 12. The findings are verification-not-measured, index-context-bounded, artifact-hash-mismatch for app/README.md, artifact-hash-mismatch for app/librarian.py, custody-missing, and return-missing. Measured README sha256 471f689adcfc89b44c2c455500924702bcf8f9eadfc83f8ae9eaa344775a65b6, 39210 bytes. Measured librarian.py sha256 b15919adb7664f993373fbc6eaaaf86d66100f396b3401845900734f920248ea, 12204 bytes. Measurement is incomplete. Custody is missing. The form id is workbook-review-v1. The correction route is labs/workbook-review-pass02/PRIME-USE.md. Director text is null because the returned 05.11 page has no Director verbatim heading. Inspect judgment is null. The historical manifest was not rewritten.

## Manual steps remaining

Codex Prime reviews this return. Codex Prime runs the independent acceptance cases and the real-use gate. Filing 0122.review-construction stays on the accepted route. This builder does not commit, seat, lock, publish a live judgment, or activate a model.

At the close check before the 05.12 pointer fill, frozen snapshots still matched all 92 rows. Live drift was only app/librarian.py and app/README.md. 05.12.md was still the pending page, sha256 b7efdbc0e56d760b3f74cc35a25c6a09a9e1a5c9ac24e0d6d5170ebbcc55f8e7, 7460 bytes. HEAD 960d20c5290656095df8457b1740d2d5e586b111, branch workshop. The index was empty. This builder did not commit.

## Factfind

The pre-repair trees still show the two independent failures from 06.22. The repaired suite shows one freshness flag on read, inspect, and recover, and it refuses a tampered render before the target write. The filed book shows two source-scoped cycle locations and a successor that does not overwrite the filled review section. The live inspection bound the real 05.11 submission and the full artifact index, and it left the hash mismatches and the missing custody visible. A heading was not treated as a grant.

## Hostile

A green suite is a command result. accepted stays false. The successor reply did not close the work. The own review write is not source drift while its published hash still matches. A later change outside that attestation is stale and the judgment stays. The live inspection is an address reading of the returned 05.11 page. It is not a judgment of this pack. Subst drives and 8.3 names were not exercised.

## Overflow

0122 filing, 0184 allocation, return-backend upgrade, band migration, live review publication, workflow adoption, independent acceptance, and the real-use gate stay outside this build. The 05.11 product and its evidence stay sealed. The contract was not revised to hide the first suite failure. labs/return-lines-pass04 was not imported.

## Unprompted

The one next step is Codex Prime's review. The artifact manifest lists the files for this return and excludes itself. Its hash is written on 05.12 after this submission is frozen. The verification file is evidence/build05.12/verification.json. This pointer does not declare a Verification line.
