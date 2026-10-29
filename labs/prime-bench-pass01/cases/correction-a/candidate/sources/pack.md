# 05.03 — add a --limit option to tally.py
Executor: worker. Reviewer: Prime.

## Finish criteria
- F1. `--limit N` accepts 1 to 1000 inclusive. 0, negative or larger values refuse with exit 2.
- F2. Tests cover each boundary; the suite passes with 0 skips.
- F3. The return reports exact test counts.
