# Reconstruction

From `D:\Git\lib-build`, with `PYTHONDONTWRITEBYTECODE=1`:

1. `python -B labs/review-loop-convergence-pass01/make_candidate.py` rewrites only `labs/review-loop-convergence-pass01/candidate/`. It refuses unless `app/librarian.py` is still sha256 `c3a5be3b612c021d95effaa5da4a151bf89026422b94f4cad98331014c7f0cd9`, 12204 bytes.
2. `python -B labs/review-loop-convergence-pass01/make_doors.py` rewrites the review-loop door and `review-loop.json` from the instance door text and the live workbook hash. After a workbook or reporter edit, the report door's `WORKBOOK_SHA`, `WORKBOOK_BYTES`, `REPORT_SHA`, and `REPORT_BYTES` must be updated to the new bytes. The door does not pin itself.
3. `python -B labs/review-loop-convergence-pass01/tests/test_convergence.py` is the author suite. It creates books under `D:\librarian\temp\0522-0517-report`. Those books are not part of this evidence set.

The proposed harness inputs are `labs/review-loop-convergence-pass01/harness-inputs.json`, schema `harness-inputs/2`. They were checked with `labs/loop-convergence-harness-pass02/inputs_check.py` `shape_problems`. The frozen harness was not edited and was not given these inputs as a ready combined run. R and W are pending, so a harness run that honors those rows stays blocked.
