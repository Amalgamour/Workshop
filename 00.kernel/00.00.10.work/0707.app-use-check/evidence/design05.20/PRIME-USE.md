# PRIME-USE — N7-local lifecycle prototype (0707/05.20)
**Lab only. Never pass the live book to record, publish or open.** Use NEW room names.

## Rerun the evidence
```bash
python -B labs/n7-local-lifecycle-pass01/make_adapter.py
```
```bash
python -B labs/n7-local-lifecycle-pass01/run_matrix.py --rooms D:/librarian/temp/n7l-NEW/matrix --out D:/librarian/temp/n7l-NEW/matrix.json
```
```bash
python -B labs/n7-local-lifecycle-pass01/replay_history.py --rooms D:/librarian/temp/n7l-NEW/replay --out D:/librarian/temp/n7l-NEW/replay.json
```

- **`make_adapter.py` rewrites the two LAB files from `workbook.py`.** Check that their hashes match BUILD-PACK before trusting a run.
- **`run_matrix.py` exits 1 on any FAIL;** `replay_history.py` exits 1 if R1 or R2 differ.

## By hand on a lab root (after a matrix run, for example `…/matrix/T1`)
```bash
python -B ROOT/labs/n7-local-lifecycle-pass01/workbook.py open --book ROOT/00.kernel/00.00.10.work --source 0799.n7-local-lab --pass 05.03
```
```bash
python -B ROOT/app/librarian.py review-loop prepare --book ROOT/00.kernel/00.00.10.work --source 0799.n7-local-lab --pass 05.03
```

**Read `exchange.state`, `exchange.chronology` and `findings`.** Then record, inspect (read the full output), publish as a separate command, and read.

## What Prime can use now
- **Nothing new on the live book.** The prototype is lab-only.
- **For a manual N7 review today, check by eye:**
  - the pack is `05.NN.pack.md`;
  - its pointer names exactly `05.NN.return.md` with a matching hash;
  - the destination `06.NN.review.md` is yours alone.
  - That is the rule the prototype automates.
