# First failures retained

These are the failures this successor was required to preserve. The passing author suite does not erase them. Historical modules were not edited.

1. The unmodified `labs/review-loop-convergence-pass01` author suite stops in `fresh_app` because the filed 05.17 pointer is no longer PENDING. It also expects the Review section to stay PENDING. That expectation fails after a normal Prime review, and no app case runs in that invocation. This successor leaves 05.17 and 05.18 as they are. The preserved record is `00.kernel/00.00.10.work/0522.review-construction/evidence/prime-review05.17/suite-first-failure.txt`.
2. Independent function probes of the pass01 reporter returned exit 0, state `readable`, and a current LAB-ONLY judgment for unsupported authority, a recover result that disagreed on stale, and a missing recover id. The record is `evidence/prime-review05.17/independent-reporter-probes.json`. The pass02 reporter withholds those cuts as state `noncurrent`.
3. The accepted freshness runner refused the pass01 candidate because `open_entry` `labs/review-loop-convergence-pass01/workbook.py` was not a declared candidate file. The record is `evidence/prime-review05.17/combined-run.json`. The pass02 identity declares the entry, the workbook, and the open entry inside the disposable root.
4. A reporter tamper aimed at the delivered canonical workbook was stopped by filesystem permissions. That was not a pin test. This suite tampers disposable copies and checks that the canonical pass01 workbook hash is unchanged.

## Preserved Prime cases

Prime reran four author cases in new external rooms: N7 lifecycle, fenced-boundary, missing-intake hold, and N5 copied-instance hold. That is not a 12/12 Prime pass. `tests_passed` on 06.38 remains false. The pass01 product failures stay in `evidence/build05.17/FAILURES.md`.

The pass02 author suite then exited 0 with `FAILED 0`. Sixteen cases passed.
