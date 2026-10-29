# support — transport support, not instructions

The files in `support/assembler/` are byte copies of the accepted pack assembler's own outputs:
- `support/assembler/05.01.md` is its legacy draft. It is NOT an instruction source. The instruction source is `05.01.pack.md`.
- `request.snapshot` is the adapter request it was given.
- `completion-receipt.json` is its completion receipt. A receipt is custody, not acceptance.
They exist so the pinned assembler verify can check this package. `source-manifest.json` and `snapshots/` at the package root are shared with them.
