# return-lines pass02

Successor to frozen `labs/return-lines-pass01`. It reconstructs corrected return pages, verifies those links, then publishes and retires on a disposable book. Pass01 `adopt` is refused here. It retires only colliding occupants into `backup/retired`.

The live work book is refused. A book that still has `0100.band.returns` needs an explicit synthetic `return-line-authorization/1` file. That fixture is not a live release. See `00.kernel/00.00.10.work/0521.return-placement/evidence/build05.04/CONTRACT.md`.

```text
python -B labs/return-lines-pass02/return_lines.py plan --book BOOK --audit AUDIT --out PLAN
python -B labs/return-lines-pass02/return_lines.py init --book BOOK --name 00.00.10.work --authorization AUTH --audit AUDIT --plan PLAN --backup BACKUP --staging STAGING --retired RETIRED
python -B labs/return-lines-pass02/return_lines.py stage --book BOOK --authorization AUTH --audit AUDIT --plan PLAN --backup BACKUP --staging STAGING --retired RETIRED
python -B labs/return-lines-pass02/return_lines.py reconstruct --book BOOK --authorization AUTH --audit AUDIT --plan PLAN --backup BACKUP --staging STAGING --retired RETIRED
python -B labs/return-lines-pass02/return_lines.py publish --book BOOK --authorization AUTH --audit AUDIT --plan PLAN --backup BACKUP --staging STAGING --retired RETIRED
python -B labs/return-lines-pass02/return_lines.py retire --book BOOK --authorization AUTH --audit AUDIT --plan PLAN --backup BACKUP --staging STAGING --retired RETIRED
```

`lookup` adds `new_home` and `retained_original` beside the pass01 descriptor. `descriptor` prints the descriptor alone. `--interrupt-after` stops between writes. A partial test fault is `arm_fault`, not a CLI flag. Rehearsal `rehearse.py` keeps its work roots.

This tool does not edit app modules, callers, pass01, or the band door.
