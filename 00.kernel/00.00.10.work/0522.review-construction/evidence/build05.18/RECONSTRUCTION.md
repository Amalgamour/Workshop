# Reconstruction

From `D:\Git\lib-build`, with `PYTHONDONTWRITEBYTECODE=1`:

1. `python -B labs/review-loop-convergence-pass02/make_candidate.py --output <empty directory outside D:\Git\lib-build>` writes a new root. It refuses an existing output and it refuses an output inside the repo. It refuses unless `app/librarian.py` is still sha256 `c3a5be3b612c021d95effaa5da4a151bf89026422b94f4cad98331014c7f0cd9`, 12204 bytes.
2. The passing suite command is `python -B labs/review-loop-convergence-pass02/tests/test_convergence.py`. It rebuilds `D:\librarian\temp\0522-0518-report\candidate`, refuses an occupied sample root, and writes books under `D:\librarian\temp\0522-0518-report`. Those books are not part of this evidence set. The same command rewrites the lab doors, `review-loop.json`, and `harness-inputs.json` from the current proposal.
3. The sealed candidate identity is `CANDIDATE.json` sha256 `9232557d1107917b9fecfddebd0ca78fcda3de2129f653402fca94d1dad0d96d`, 4872 bytes, at the suite root above. An unused `labs/decoy-workbook.py` may sit beside it. That file is not declared and it is not executed.

The proposed harness inputs are `labs/review-loop-convergence-pass02/harness-inputs.json`, schema `harness-inputs/2`, sha256 `b7d6a7ab11ff71c7233f9e6195f715a43c79ff2cd69116a9c1b68424991d7f86`, 10033 bytes. They were checked with `labs/loop-convergence-harness-pass02/inputs_check.py` `shape_problems` when `make_candidate.py` wrote them. The frozen harness was not edited. R and W are pending, so a harness run that honors those rows stays blocked.
