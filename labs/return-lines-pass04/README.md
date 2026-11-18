# return-lines pass04

Successor to frozen `labs/return-lines-pass03`. It loads that tool by pin and does not edit it. Reconstruction publishes corrected return pages, then retires colliding occupants into `retired/occupants` and every remaining audited old member into `retired/originals`. Retirement is the whole audited set.

A recorded release is evaluated with one validator for a disposable copy and for the canonical book. The preconditions are the book identity, the operation list, the plan, audit, and layout bindings, the three roots, the current source bytes, and the exact release-file bytes. No in-process designation step is required or provided. The synthetic fixture never authorizes the canonical book. A candidate record never executes. `preflight` checks a record and writes nothing.

```text
python -B labs/return-lines-pass04/return_lines.py preflight --book BOOK --authorization AUTH --audit AUDIT --plan PLAN --backup BACKUP --staging STAGING --retired RETIRED
python -B labs/return-lines-pass04/return_lines.py plan --book BOOK --audit AUDIT --out PLAN
python -B labs/return-lines-pass04/return_lines.py init --book BOOK --name 00.00.10.work --authorization AUTH --audit AUDIT --plan PLAN --backup BACKUP --staging STAGING --retired RETIRED
```

The other pass02 commands use the same arguments. There is no `--force` and no `--allow-live`. This build does not create a release for the real workbook and does not run that workbook's mutators.

See `00.kernel/00.00.10.work/0521.return-placement/evidence/build05.06/CONTRACT.md`.

This tool does not edit app modules, callers, pass01, pass02, pass03, or the band door. It does not install a sentinel.
