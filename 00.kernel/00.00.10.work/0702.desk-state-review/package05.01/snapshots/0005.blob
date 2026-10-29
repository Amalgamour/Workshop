# desk-state-pass01

One experimental command that reads a `desk-state/1` record and writes a derived Prime view. Standard library only. It is not seated runtime, and it does not select, release, accept, complete, or dispatch work.

The contract is `00.kernel/00.00.10.work/0508.return-capture/evidence/deskstate05.19/CONTRACT.md`.

```text
python -B labs/desk-state-pass01/desk_state.py view --input ABS [--json] [--out DIR] [--candidate ABS]
python -B labs/desk-state-pass01/desk_state.py revise --record ABS --expected SHA256 --submission ABS --out ABS
python -B -m unittest labs/desk-state-pass01/tests/test_desk_state.py
```

Run these from the repository root.

Exit 0 means the view has no attention item and no unknown. Exit 1 means attention or an unknown is visible. Exit 2 means the record, a pin, a path, or an output was refused.

`--json` prints the view. The default prints the same facts as readable text: desk goal, milestone, each lane, returns, unresolved decisions, and the recorded next step. `elected` is null. A null worker is unrecorded, not available.

`revise` checks the expected hash, writes a new record, and leaves the old file in place. The new file is not a worker command.
