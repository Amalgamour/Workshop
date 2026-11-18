# Submission - 0522.review-construction/05.11

date: 2026-11-02
executor: Grok-1
reviewer: Codex Prime
accepted: false
committed_by_this_builder: false
custody: pending
matching line: 0122.review-construction unfiled
readiness: returned for Codex Prime review and the actual-use test

This is the builder return for the named invocation of 05.11. It is a claim. It is not acceptance, not custody, and not a release. Notes in 06.21.md were reread at close and integrated below. The contract was not revised after tests. This file does not carry the artifact-manifest hash. That hash is written only on the 05.11 return pointer after the manifest exists.

## Did

Verified evidence/pack05.11/source-manifest.json before the notes. Schema prime-pack-inputs/1. 44 files. bad 0. missing live 0. missing snapshot 0. live drift 0. snapshot mismatch 0. extra snapshots 0. Manifest sha256 f8df756c6c35d74ced7473038b424fe01d1352aabda831dcb7bc7b0074bbf1b5, 14782 bytes. The manifest file is not LF-only. Its row hashes were not rewritten.

Built labs/workbook-review-pass01. The public commands are prepare, form, record, inspect, publish, read, and recover. The first request supplies an absolute book, a source page id, and a pass. Compute derives the assignment, the measured rows, the typed form, the publication target, and the review id. The judgment file contains only the declaration fields. Prime copies `intake_id` and `review_id` from the results.

The form declaration is labs/workbook-review-pass01/forms/workbook-review-v1.json, sha256 152b436bda8e19d15f252bb5208791c8eefd9a658789e2ab6e9789ffa362b49f, 4532 bytes. Its correction route is labs/workbook-review-pass01/PRIME-USE.md. Validation reads that declaration. Null `tests_passed` stays null. An omitted `semantic_conflict` is a missing field. A missing decision is not consent. Director text measured on the page stays verbatim.

app/librarian.py loads app/review_loop_tools_v5.py for the review-loop command only. The declaration is app/review-loop-v5.json, schema review-loop-pins/3. Fixture commands and `--fixture-root` stay on the pinned v4 door. v4 and its declaration stay byte-for-byte. Authoring-v2 and return-lines-v2 stay on their own doors and stay byte-for-byte.

A looked-up descriptor of schema return-line-descriptor/1 or /2, state complete, with the receipt file present, is the filed path. The workbook stores that descriptor and a registration, then calls the pinned loop. The cycle record is workbook-review/cycle-records/{pass}-wb/record.json. The public review id is `w` plus 16 hex characters. Those two ids are different. Recover re-reads the cycle bytes.

Any missing piece of that filed test is preliminary. The workbook stores the judgment, calls prime_review.report, and does not write a receipt. `operation` complete is refused. closes_work stays false.

The operator suite is labs/workbook-review-pass01/tests/test_workbook.py. The cited run is 6 tests, 100.902 seconds, OK, exit 0. It ran through app/librarian.py on disposable books under D:\librarian\temp\0522-0511. The live current-book demonstration was prepare, form, and inspect only, while 05.11 still said PENDING.

## Blocked

Matching line 0122.review-construction is unfiled. This slice does not file it, allocate 0184, or invent a receipt. Custody on the live page stays missing.

prime_cycle.record_review requires observation state complete, which requires a real return-line-capture/1 or legacy-relocated/1 receipt chain. The pinned cycle and constructor were not edited. A fixture receipt was not written. The early filed tree wb0511-filed-386u0mgi kept the judgment and the refusal `bind requires --root`. Its journal stayed `recorded`. Later code calls prime_review without `--root` on the cycle path, because that cycle invocation has no root flag. The clean filed tree is wb0511-filed-__vwjn9s.

A second filed constructor publish that reuses registration review_identity `wb` is outside this slice. The Director-input successor in the suite stays on the preliminary book.

Codex Prime has not reviewed this pack. The actual-use gate was not run. This builder does not commit.

## Need

Codex Prime review of this return, then the actual-use test on the next returned assignment. The forms are in evidence/build05.11/PRIME-USE.md. Stop here.

## API, forms, ownership, and reuse

Book, source page, and pass are the caller inputs. N5NN assignment is `{page}/{pass}.md`. The derived member is `{space}1{nn}.{subject}`. The derived return is `{member}/{pass}.return.md`. The review target is the assignment section `## Review - Codex Prime` or the same heading with U+2014. N7NN assignment is `{page}/{pass}.pack.md` when that is the only candidate. Both `{page}/{pass}.md` and `{page}/{pass}.pack.md` are an ambiguous assignment and neither row is chosen. The N7NN review file is `{page}/06.{tail}.review.md`. The return file is not moved. Any other band exits 2 and `missing` contains `route`.

Instance identity is the sha256 of the canonical object `{book, source, pass}` with the absolute book path. The same page id in another directory is another instance.

Commands, through the app:

```text
python -B app/librarian.py review-loop prepare --book ABSOLUTE-BOOK --source PAGE --pass 05.NN
python -B app/librarian.py review-loop form --book ABSOLUTE-BOOK --source PAGE --pass 05.NN
python -B app/librarian.py review-loop record --book ABSOLUTE-BOOK --source PAGE --pass 05.NN --intake INTAKE --judgment ABS-JSON
python -B app/librarian.py review-loop inspect --book ABSOLUTE-BOOK --source PAGE --pass 05.NN
python -B app/librarian.py review-loop publish --book ABSOLUTE-BOOK --source PAGE --pass 05.NN --review REVIEW
python -B app/librarian.py review-loop read --book ABSOLUTE-BOOK --source PAGE --pass 05.NN
python -B app/librarian.py review-loop recover --book ABSOLUTE-BOOK --source PAGE --pass 05.NN
```

Stdout is one JSON object, schema workbook-review-result/1. A wrapper refusal prints `stop:` and exits 2. The workbook prints `refused:` on its own stderr.

Intelligence owns finding, reasons, operation, disposition, terminals, next action, semantic conflict, findings, sections, holds, answers, passes, and gaps. Compute owns intake id, review id, instance id, source rows, byte counts, digests, custody mode, destination, legal unknowns, and the journal.

Reuse, pinned and not edited: return-access-pass01 lookup; review-loop-pass03 for the filed path; prime-cycle-pass03 and review-construction-pass04 only through that loop; prime-review-pass02 report for the judgment check. The form follows the authoring field-list shape. pack_author.py is not imported. No parallel committed-review ledger. COMMITTED.json is written only by the cycle.

On the filed path the cycle owns prime-cycle-review/3. The workbook owns workbook-review-record/1 and the publication journal, and the record points at the cycle file. On the preliminary path the workbook record is the preserved judgment. It is not a committed cycle review.

## Pins

| Path | sha256 | bytes |
|---|---|---|
| labs/workbook-review-pass01/workbook.py | 60e040fa30f61348adac76a4f3bdfbfdb9aba859f25bacadf317937c167e9b0a | 79131 |
| labs/workbook-review-pass01/forms/workbook-review-v1.json | 152b436bda8e19d15f252bb5208791c8eefd9a658789e2ab6e9789ffa362b49f | 4532 |
| app/review_loop_tools_v5.py | b1192daf5d265c66f10adfe2125ff0c92a08ccd3c797d229698ecc20e2fdeed9 | 7875 |
| app/review-loop-v5.json | eaa9120bba2c7274f2218c875ec3ecfc84d291188557049240c30a1c2a430de3 | 1964 |
| app/librarian.py | e2d85b1b641d8a1113b0afaa67a9b8203eb58e9f1028308be922a806fffa5f90 | 12204 |
| app/README.md | d30d68d47cf90475f7f4b7abe9215c3ad2b323535494e2000bfc306f302f6c16 | 38352 |
| app/review_loop_tools_v4.py | 0769179366a6c1659f38cb2c79c51981d5cb76fa8d48ee7325f9eaf00d14c296 | 13381 |
| app/review-loop-v4.json | 769f81321e19a9f3296020e3b0b4a4905ec1b3a66c1629bf53d9548b7182d723 | 2519 |
| labs/return-access-pass01/return_access.py | 501d40d7c7b08720d3ae061441284ac26d544e7b80100059b2ddce25f67358f5 | 26561 |
| labs/review-loop-pass03/review_loop.py | 47f47d16426e4d69987398a8244877de58b6089326874f3279003f696814450b | 55474 |
| labs/review-construction-pass04/construct.py | 6d541d4225ed0f9ccdb6263b475a79f55e4312be80a7e9a810a3622e5bd8df20 | 42582 |
| labs/prime-cycle-pass03/prime_cycle.py | 496b4d721cfb136fa847d998d421209616c60508beb5cda5620af73041eed17c | 76045 |
| labs/prime-review-pass02/prime_review.py | 80836a13278365de863ed8231cb8118ad14ddbad672dd02ec2ebf69beff3b44e | 58560 |
| app/authoring-v2.json | 14965030b2344f77e196a1d6a29b8cb74400cc3cf237e4f5ecc44c2adf332d11 | 2106 |
| app/return-lines-v2.json | 9fc16cc49d87c7455cc56aebb87897252807a426654dbe45d7e575df5f081e52 | 1598 |

The v5 declaration matches the workbook, form, and tool rows above. CONTRACT.md sha256 34bbaa25bcfa35bcf1b6ad43d2dccbc070c83cd8848d8aa740e6a184228d405c, 9944 bytes. 06.21.md sha256 a5fa7f66c5a70fb0d2c224160d16e917a0b74c6ae575fa62b4d1dfe586607ae5, 3780 bytes. The operator test sha256 3abdf099655ebc561f2f33826a518944e152966ee0ac348cbbc2928b8f103cc1, 27581 bytes.

Before this slice, librarian.py was sha256 826167161000ac3eab78c466ae47e31b37ff435ea33f4104caf7651ecd21436e, 12153 bytes. README.md was sha256 2886188717bc62008397754f8ab3155dc2188e30b69344ef6b70d70d8f0ab9db, 38242 bytes.

## Preliminary and filed states

Preliminary. Custody is `missing`. The record mode is `preliminary`. Eligible completion is false. The clean tree wb0511-n5-q2d1x6l4 published review `w151d3f2a09e4bf7d` on 0599.synth-review/05.01.md. OUTSIDE and TAIL stayed. A later outside change of the assignment made recover exit 1 with stale true, and the stored finding stayed.

Filed. The clean tree wb0511-filed-__vwjn9s prepared custody `complete-descriptor` through return-access. Record mode is `cycle-committed`. Public review id `w98ef7e1f082fd0a8`. Cycle review id `05.01-wb`, schema prime-cycle-review/3. Journal status `published`. The stored record has eligible_for_custody_completion false. The suite recover result had closes_work false and returned the stored finding. The receipt is the one the seeded return-lines capture wrote. The workbook did not invent one.

Director hold. Tree wb0511-hold-qgwtnfev recorded `w0ad60b5453b67dcf` as director-input and successor `w4a77d49a24bc847a`. The page contains the reply `Stay on this page.` The old record stays. closes_work is false.

## Live-write scope

The live checkout gained the new lab, the v5 door and declaration, the review-loop load in librarian.py, the review-loop section of README.md, and one sentence in the return-lines section. That sentence now says authoring v2 stays on its own door, review-loop selection is v5, and fixture commands stay on the pinned v4 door. The rest of that section is unchanged.

Prepare, form, and inspect of the live 05.11 page wrote nothing. Record, publish, read, and recover refuse a book inside D:\Git\lib-build. No live review section was published. The return pointer on 05.11 is filled after this submission and the manifest exist. The Review section stays PENDING. The state line stays the prepared line.

At the close check before that pointer, frozen snapshots still matched all 44 rows. Live drift was only app/librarian.py and app/README.md.

## Commands, exits, and first failures

Cited operator command, from D:\Git\lib-build, with PYTHONDONTWRITEBYTECODE=1:

```text
python -B labs/workbook-review-pass01/tests/test_workbook.py
```

Ran 6 tests in 100.902s. OK. Exit 0. The same command earlier in this build, before the cycle re-read, ran 6 tests in 98.761s and exited 0. An isolated route test after the authoring seed exited 0 in 3.608s. The suite was not rerun after the README sentence, because that sentence is not a door pin.

Current-book command, while the pointer said PENDING:

```text
python -B app/librarian.py review-loop prepare --book D:\Git\lib-build\00.kernel\00.00.10.work --source 0522.review-construction --pass 05.11
python -B app/librarian.py review-loop form --book D:\Git\lib-build\00.kernel\00.00.10.work --source 0522.review-construction --pass 05.11
python -B app/librarian.py review-loop inspect --book D:\Git\lib-build\00.kernel\00.00.10.work --source 0522.review-construction --pass 05.11
```

Exits 0, 0, 0. Stdout 7708, 6504, and 7079 bytes. Stderr empty. Intake `90208e4640ae12ef7966b319323d90391ce4c83139d478b1cbb90c6990e7ee13`. Page sha256 `22c7cdde7e847b6e15e7c31e621e4e49fc0466539496abaa80814d6e6cb10ed6`, 10286 bytes, before and after. Copies are evidence/build05.11/current-book. This demonstration was not repeated after the pointer fill.

First failures retained under D:\librarian\temp\0522-0511:

- The test mapped `pass_` to `--pass-`. Every command exited 2 with `refused: unknown argument`.
- An ambiguous assignment left the pointer unparsed. A second `Submission:` line that was not 64 hex was counted as unparsed-return-line.
- The filed record stayed preliminary. Tree wb0511-filed-386u0mgi kept `bind requires --root`.
- Undeclared band `0499.other` did not copy `route` onto `missing`.
- Filed publish exited 1 because the cycle id was the public `w` id. The loop required `05.01-wb`.
- Authoring form on an empty outside book exited 2 with `stop: missing source 00.kernel/00.00.10.work/0526.dev-authoring`.
- The same form pointed at the live work book exited 2 with `stop: book root must stay outside D:\Git\lib-build`.

The clean route case seeds the five profile files into the outside book and receives schema authoring-form/1, kind intent. return-lines status on that book exited 0 with accepted false and task_association not-established. describe-legacy without `--member` exited 2 and stderr started with `stop:`.

## Publication and recovery

Clean preliminary publish of `w151d3f2a09e4bf7d` left OUTSIDE and TAIL in place. The same-byte record returned that id. A conflicting record exited 2 and the stored finding stayed. Recover after changing `Intro OUTSIDE` to `Intro CHANGED` exited 1, stale true, with the finding kept.

The hold successor published `w4a77d49a24bc847a`. The reply is on the page. The first record's answers stayed empty and its finding disposition stayed elevated.

Manual review on 0597.synth-bad/05.03.md stayed in place. Publish of `w72efbace4363254a` exited 1. The journal stayed `recorded`. Read returned the finding. A bad judgment that omitted `finding` exited 2, and the original bytes stayed under `failed/`.

Pass 05.04 was made read-only after record `w5d35e315c7be32f7`. Publish exited 1. The journal status is `pointer-pending`. Recover returned the stored next action and target_state `pointer-pending`. A later assignment change made a repeat record exit 2 with stale true. The old record stayed.

N7 page 0798.synth-local published `wbe5ea87b3ba527ea` to 06.03.review.md. The return hash stayed. `operation` complete with `--successor` exited 2. The correction contains `ineligible`. Page 0799.synth-face reported ambiguous-assignment and ambiguous-submission and chose no assignment row.

Filed publish of `w98ef7e1f082fd0a8` exited 0. The target kept OUTSIDE and TAIL. The cycle file review_id is `05.01-wb`.

## Manual steps remaining

Codex Prime reviews this return. Codex Prime runs the actual-use gate on the next returned assignment, using the forms above. Filing 0122.review-construction stays on the accepted route. This builder does not commit, seat, lock, or activate a model.

## Factfind

The clean filed book shows that a real captured descriptor is enough for the pinned loop to commit prime-cycle-review/3, and that the workbook record points at those bytes. The preliminary books show a stored judgment with cycle not committed. The early bind refusal remained on disk with the judgment. The live inspection, taken while the pointer said PENDING, reported the missing return and the missing custody as findings.

## Hostile

A green suite is a command result. accepted stays false. The Director reply on the preliminary book did not close the work. Recover after an outside byte change returns the stored judgment with exit 1. A declared review write that matches the stored body is the published target. The live inspection is an address reading of an unfinished page. It is not a judgment of this pack. Subst drives and 8.3 names were not exercised.

## Overflow

0122 filing, 0184 allocation, return-backend upgrade, band migration, live review publication, workflow adoption, and the actual-use gate stay outside this build. The 05.07 product and its evidence stay sealed. labs/return-lines-pass04 was not imported.

## Unprompted

The one next step is Codex Prime's review and the actual-use test. The artifact manifest lists the files for this return and excludes itself. Its hash is written on 05.11 after this submission is frozen. Verification is evidence/build05.11/verification.json.
