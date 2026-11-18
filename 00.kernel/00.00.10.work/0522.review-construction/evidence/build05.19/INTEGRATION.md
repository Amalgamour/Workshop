# Code path

The generated `candidate/app/librarian.py` holds one trust-anchor hash. Before it loads either door, it checks `labs/review-loop-convergence-pass03/trust-anchor.json`, then the loop-door bytes and the report-door bytes named there.

The anchor stores those two door hashes. It stores no dispatcher hash. The report door stores the masked dispatcher hash: the hash of the dispatcher after its single `ANCHOR_SHA = "<64 hex>"` literal is replaced with 64 zeros. That swap keeps the same length, so the mask stays stable. The report door stores no anchor hash. A joint edit of the anchor literal and the anchor file is the trust-root limit. The author probes change one file at a time.

- `review-loop` loads `labs/review-loop-convergence-pass03/review_loop_tools.py` only after the anchor check. The door refuses a declaration whose workbook path is anything other than `labs/review-loop-convergence-pass03/workbook.py`, then runs that file. Fixture commands and unknown commands refuse. A missing door refuses before import. There is no live-app fallback and no `review_loop_tools_vN.py` name.
- `review-report` loads `labs/review-loop-convergence-pass03/review_report_tools.py` only after the same anchor check. That door refuses a wrong dispatcher by the masked hash and a wrong workbook by the workbook hash, then calls `report.py`.

`workbook.py` loads `labs/review-loop-convergence-pass02/workbook.py` by its absolute pin and refuses on mismatch. Pass02 still loads the frozen pass01 convergence workbook, which loads the instance workbook, pass05, pass04, pass03, pass02, and pass01. The capacity `prime_review` pin stays the frozen live file. The N7 prototype workbook is not imported.

`REPO` is `parents[2]` when the workbook path is `labs/review-loop-convergence-pass03/workbook.py`. A loose copy refuses. `locate_declared` reads the candidate root first. A path that is present there stays there, so a different dispatcher remains visible. A path absent from that root is read from the live checkout. `build_intake(book, page, pass_id)` pins form, return_access, review_loop, construct, prime_cycle, and prime_review, clears the source-kind hold, and calls the same preparation path as the CLI.

The reporter schema stays `review-report-convergence/2`. When measurement is complete and the read is current, a current judgment also requires prepare exit 0, inspect exit 0, inspect stale false, and inspect `current` equal to the read review id. A disagreement is state `noncurrent`, with judgment and authority null. History stays under `historical_supplied`. An incomplete measurement stays `held`. A consistent stale cut stays `stale`. An empty review stays `not-recorded`. `inspect_current` and `prepare_exit` are raw observations.

N7 custody on the recorded chain stays `not-applicable`. N5 custody on the synthetic same-instance record stays `missing`. A copied N5 book reads with instance reason `different-root`.
