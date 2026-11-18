# PRIME-USE — v8 review-entry integration lab (0707/05.18)
**Lab only. Never pass the live book.** Every tool refuses a room inside `D:\Git\lib-build`. Use NEW room names for every rerun.

## What Prime can use now
- **The live v7 core** for N5 preliminary reviews, as today.
- **For an N7 return, a disposable v8 candidate root** that measures it fully, for evidence or a second look. Records written there are copy-only and are not live records.
  ```bash
  python -B labs/review-entry-integration-pass01/rie.py --room D:/librarian/temp/rie-NEW/n7 --fixture n7-0517
  ```
  ```bash
  python -B D:/librarian/temp/rie-NEW/n7/app/librarian.py review-loop prepare --book D:/librarian/temp/rie-NEW/n7/00.kernel/00.00.10.work --source 0707.app-use-check --pass 05.17
  ```
  (Fixtures: n5-0522, n5-0512, n7-0515, n7-0517. `--dispatcher v7` builds the same root with the live dispatcher; `--omit FILE` leaves a page file out.)

## Rerun the evidence
```bash
python -B labs/review-entry-integration-pass01/matrix.py --rooms D:/librarian/temp/rie-NEW/matrix --out D:/librarian/temp/rie-NEW/matrix.json
```
```bash
python -B labs/review-entry-integration-pass01/lifecycle.py --rooms D:/librarian/temp/rie-NEW/life --out D:/librarian/temp/rie-NEW/life.json
```
```bash
python -B labs/review-entry-integration-pass01/hostile.py --rooms D:/librarian/temp/rie-NEW/hostile --out D:/librarian/temp/rie-NEW/hostile.json
```
```bash
python -B labs/review-entry-integration-pass01/rollback.py --rooms D:/librarian/temp/rie-NEW/rollback --out D:/librarian/temp/rie-NEW/rollback.json
```
```bash
python -B labs/review-entry-integration-pass01/ctx_test.py --room D:/librarian/temp/rie-NEW/ctx --out D:/librarian/temp/rie-NEW/ctx.json
```
```bash
python -I -B labs/review-entry-integration-pass01/bundle/reconstruct.py --index labs/review-entry-integration-pass01/bundle/INDEX.json --room D:/librarian/temp/rie-NEW/reconstruct --out D:/librarian/temp/rie-NEW/reconstruct.json
```

**The cases run against the candidate pass04.** They need a built root, for example the matrix's `n5-0512` root:
```bash
RIE_CANDIDATE_ROOT=D:/librarian/temp/rie-NEW/matrix/n5-0512 python -B labs/review-entry-integration-pass01/cases/tests/test_n7v2.py --root D:/librarian/temp/rie-NEW/v2 --out D:/librarian/temp/rie-NEW/v2.json
```
```bash
RIE_CANDIDATE_ROOT=D:/librarian/temp/rie-NEW/matrix/n5-0512 python -B labs/review-entry-integration-pass01/cases/compat17/tests/test_n7.py --root D:/librarian/temp/rie-NEW/c17 --out D:/librarian/temp/rie-NEW/c17.json
```

## Reading results
- **matrix columns:**
  - **W** = the real v7 entry on a copy (the wrong-root reference, never the baseline);
  - **B / B2** = the faithful pass03 baseline;
  - **D** = the v8 door directly, with the v7 dispatcher bytes;
  - **C** = the real v8 entry.
- **N5 parity is B == D and B2 == C.**
- **The intake_id carries the book path,** so compare ids only within one root.
- **Read the full inspect output** (`<run>-evidence/inspect.full-read.txt`) before any publish, and publish only as a separate command.
