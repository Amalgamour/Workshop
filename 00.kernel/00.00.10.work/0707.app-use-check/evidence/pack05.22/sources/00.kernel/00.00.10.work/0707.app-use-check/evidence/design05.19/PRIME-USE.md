# PRIME-USE — 0707/05.19

## What Prime can use NOW
- **The selected v7 core** for N5 returns with **at most 24 book sources**.
  - Count: book-root assignment + submission + return + artifacts.
  - Code-root `labs/` and `app/` rows do not count (inv1 C2, C3).
- **The staged v8 door, called directly for read-only measurement** of N7 returns:
  ```bash
  python -B app/review_loop_tools_v8.py prepare --book D:\Git\lib-build\00.kernel\00.00.10.work --source PAGE --pass 05.NN
  ```
  - **Read every declaration line yourself first.** A-01 and A-02 are open: X1 shows a decoy manifest bound silently.
  - Do NOT record with v8: a malformed line can bind the wrong evidence, and N7 returns over 24 sources are refused anyway.
- **The reporter hardening candidate** (external dispatcher) for read-only reports on v7-recorded pages.

## What prevents daily use
1. **Capacity:** normal returns exceed 24 sources (0512/05.09: 29; 0707/05.17: 26).
2. **A-01 / A-02:** the strict grammar is pending.
3. **No combined selection:** the reporter and loop dispatchers are mutually exclusive today (X6), and the reporter does not see v8 N7 records as current (X7).
4. **The first-target rule** is undecided for Colab N7 (X4).

## Rerun my investigations (NEW room names)
```bash
python -B labs/loop-convergence-design-pass01/inv1_capacity.py --rooms D:/librarian/temp/lcd-NEW/inv1 --out D:/librarian/temp/lcd-NEW/inv1.json
```
```bash
python -B labs/loop-convergence-design-pass01/inv1_c5b.py --room D:/librarian/temp/lcd-NEW/c5b --out D:/librarian/temp/lcd-NEW/c5b.json
```
```bash
python -B labs/loop-convergence-design-pass01/inv2_interaction.py --rooms D:/librarian/temp/lcd-NEW/inv2 --out D:/librarian/temp/lcd-NEW/inv2.json
```
```bash
python -B labs/loop-convergence-design-pass01/inv2b_reporter.py --rooms D:/librarian/temp/lcd-NEW/inv2b --out D:/librarian/temp/lcd-NEW/inv2b.json
```

- **The exit codes are honest:** inv1 and inv2 exit 1 if any case is not as predicted. inv2b exits 0 always, so check its `as_predicted` fields. That is the same lesson as matrix.py, noted in 06.18.review.
- **Read `as_predicted` per case.** A prediction is a documented baseline behavior, not a repair.
