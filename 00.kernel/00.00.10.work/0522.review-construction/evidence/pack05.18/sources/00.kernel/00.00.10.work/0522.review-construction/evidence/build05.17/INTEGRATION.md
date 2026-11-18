# Code path

`candidate/app/librarian.py` loads two doors.

- `review-loop` sets the code root to `D:\Git\lib-build` and calls `labs/review-loop-convergence-pass01/review_loop_tools.py`. Workbook commands run `labs/review-loop-convergence-pass01/workbook.py`.
- `review-report` sets the code root to the candidate root and calls `labs/review-loop-convergence-pass01/review_report_tools.py`, which pins that dispatcher and the canonical workbook and reporter, then calls `report.py`.

`workbook.py` loads `labs/review-instance-binding-pass01/workbook.py`. That module loads pass05, which loads pass04, pass03, pass02, and pass01. The N7 prototype is pinned in the declaration and is not imported.

Wrappers on the loaded chain:

- `pin_file("prime_review")` returns `labs/review-source-capacity-pass03/prime_review.py` after a byte check.
- `pointer_block` uses the unfenced heading pair when a fence is present and the structure is clear.
- `locate_declared` binds the book copy when the book file and the helper-root file differ only by path and their bytes are equal. Different bytes stay ambiguous.
- `build_intake` adds the N7 exchange and replaces `custody-missing` with `n1-not-applicable` for N7 only.
- `source_changed` holds a missing or non-object comparison intake when a current review record exists, then calls the instance hold, then applies the N7 bound-region exemption.
- `render_body` and the record result set N7 custody `not-applicable` when the predecessor label is `missing` and the mode is not `cycle-committed`.
- `perform` blocks publish when that comparison hold is set, and keeps the stored judgment on the refusal.
- `open` writes `exchange-open.json` for an N7 pack before the return exists.

N5 custody stays `missing` on the synthetic same-instance record. A copied N5 book reads with instance reason `different-root`.
