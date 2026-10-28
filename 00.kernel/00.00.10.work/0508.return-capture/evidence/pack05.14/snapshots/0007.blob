# batch-observation-pass01

Read-only observation of one batch page. The contract is `00.kernel/00.00.10.work/0508.return-capture/evidence/reader05.13/CONTRACT.md`.

The lab keeps the pinned `parse_source` result exact and, separately, inventories unfenced return headings and `Member` / `Receipt` lines. Optional custody reads use the pinned inspector. The output is `batch-observation/1`. It grants no release, acceptance, closure, or seat.

```text
python -B batch_observe.py observe --json --repo REPO --commit HEX40 --path REL [--members-book ABS]
python -B batch_observe.py observe --json --repo REPO --live --path REL
python -B batch_observe.py observe --json --supplied FILE [--path REL]
```

Git use is limited to `rev-parse --verify` and `cat-file` on the named repository. A worktree file and a supplied file are not reported as Git blobs. A pin mismatch stops the run before import, Git, or inspect.
