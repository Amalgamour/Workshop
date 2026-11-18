# Code path

The generated `candidate/app/librarian.py` loads two doors from the candidate root.

- `review-loop` calls `labs/review-loop-convergence-pass02/review_loop_tools.py`. The door refuses a declaration whose workbook path is anything other than `labs/review-loop-convergence-pass02/workbook.py`, then runs that file. Fixture commands and unknown commands refuse. A missing door refuses. There is no live-app fallback.
- `review-report` calls `labs/review-loop-convergence-pass02/review_report_tools.py`. That door pins the candidate librarian, the candidate workbook, and the candidate reporter, then calls `report.py`.

`workbook.py` loads `labs/review-loop-convergence-pass01/workbook.py` by its absolute pin and refuses on mismatch. It replaces fence classification and pointer extraction on that loaded module. Pass01 still loads the instance workbook, which loads pass05, pass04, pass03, pass02, and pass01. `pin_file("prime_review")` remains the capacity successor. The N7 prototype is not imported.

Fence classification accepts a backtick run and a tilde run. A closing run must be the same marker, at least as long as the opener, and nothing else. An unclosed fence, a missing heading, a review before the pointer, or two real headings stays ambiguous or missing. `## Reviewer`, `## Reviews`, and `## Return pointer example` are not boundaries. The classifier does not choose the last heading.

The reporter schema is `review-report-convergence/2`. It validates the observed inspect, read, and recover envelope before emitting flags. An unsupported or cross-command-inconsistent observation is state `noncurrent`: judgment, next action, and the current authority fields are null, and the raw values stay under `historical_supplied`. A consistent stale cut stays `stale`. A consistent incomplete measurement stays `held`. An empty review stays `not-recorded`. A malformed core response refuses with exit 2.

N7 custody stays `not-applicable` on the recorded chain. N5 custody stays `missing` on the synthetic same-instance record. A copied N5 book reads with instance reason `different-root`.
