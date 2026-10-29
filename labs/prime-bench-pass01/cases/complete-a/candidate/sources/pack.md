# 05.10 — add the inspector JSON output
Executor: worker. Reviewer: Prime.

## Finish criteria
- F1. `inspect --json` prints the inspection record.
- F2. Tests pass with 0 skips and exact counts are reported.
- F3. The return is captured and freshly verified with exit 0.

## Accepted limit
No sandbox against same-user races is required in this pass.
