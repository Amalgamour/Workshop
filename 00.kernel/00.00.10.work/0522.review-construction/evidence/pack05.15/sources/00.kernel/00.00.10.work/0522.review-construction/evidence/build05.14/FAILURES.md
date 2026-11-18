# Failures and limits — 0522.review-construction/05.14

Proof stamp: `D:\librarian\temp\0522-0514\20261103T235828680Z`

## Kept

Historical suite `labs/review-entry-staging-pass01/suite/compat17/tests/test_n7.py` exited 1. Aggregate PASS 13, FAIL 4, ERROR 0. First failure G7.

G7 is the revised grammar assertion from the accepted design. The staged N7 parser returned:

- semicolon: `submission-not-declared`, `unparsed-return-line`
- double-comma: no finding codes
- N5 trailing comma: no finding codes

The copied test still requires a refusal on the double comma and `unrecognized-path-punctuation` on the N5 trailing comma. Semicolon stays refused. Double comma and the trailing comma are accepted as the current pass03 forms. This pack did not edit the test and did not change the parser to satisfy G7.

I4, H2, and I6 are the other three failures. Patched prepare on the fixture exited 0 and measured incomplete, with `ambiguous-declared-root`. H2's unpatched prepare, which retargets the code root to the fixture, still reports `declared-hash-mismatch`. I6's patched measurement is incomplete. I1, I2, I3, and I5 passed. The failing paths are declared work-tree paths that exist both in the disposable copy and under `D:\Git\lib-build`. The staged workbook refuses to collapse those two roots. The lab adapter that would point REPO at the copy was not installed.

## Suites that passed

`suite/tests/test_n7v2.py` exited 0. PASS 12, FAIL 0, ERROR 0. First failure null. The three N5 punctuation integrations ran the staged workbook at its canonical path with `--book` pointed at an external book.

## Driver attempt before the cited stamp

`D:\librarian\temp\0522-0514\20261103T235800792Z` started prepare for `0522.review-construction/05.13` and raised `FileNotFoundError` while saving stdout, because the log folder did not exist yet. No suite, record, or publish ran in that attempt. The driver now creates the folder first. The staged product bytes were not edited after that prepare.

## Lifecycle limit

On the disposable N7 book, publish exited 0 and created `0799.staging-n7/06.01.review.md`. The file was absent before the cycle. Stored `cycle.called` is false, `cycle.committed` is false, and the mode is preliminary. `published_work` stayed false. This is the current preliminary publish of an absent N7 file. It is not cycle commitment, and the 0521 repair was not applied.

The disposable N5 assignment hash changed from `ddf6c1aa58c1b84f93652bf2ce43a74d419c0f42619c4bc72f872f9ff78cc5c0` to `335a53673aa0a1cc05a525684af95fe336de60855d0cd4d007346fb4f4f00dd3` across the whole cycle. The review section started as `PENDING.` and publish wrote the supplied review there. The live work book did not change.

## Not claimed

Concurrency and interruption were not tested. Authoring and return-lines routes were not re-run as a v8 selection comparison, because this pack does not select the dispatcher. A review recorded through v8 has no door-version field.
