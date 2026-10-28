# batch-observation-pass01

Read-only observation of one batch page. The captured 05.13 contract remains `00.kernel/00.00.10.work/0508.return-capture/evidence/reader05.13/CONTRACT.md`. The 05.14 repair contract is `00.kernel/00.00.10.work/0508.return-capture/evidence/repair05.14/CONTRACT.md`.

The lab keeps the pinned `parse_source` result exact and, separately, inventories unfenced return headings and `Member` / `Receipt` lines. Optional custody reads use the pinned inspector. The output is `batch-observation/1`. It grants no release, acceptance, closure, or seat.

The 05.15 header contract is `00.kernel/00.00.10.work/0508.return-capture/evidence/header05.15/CONTRACT.md`. An opening level-1 title stays inside the initial header until the next unfenced heading. A later title does not reopen that header.

Eligible `state`, `Executor`, `Release`, and `Claim` lines come from the header, Assignment, or a return pointer. Fenced examples, blockquotes, and other sections do not fill those fields. Duplicate eligible lines stay listed and leave the raw value empty. A malformed declaration exits 2 with no observation document. A well-formed declaration stays unauthenticated and does not bind review. A live file read and each inspector call record UTC timestamps. A Git blob keeps those times empty, and `package_at_commit` stays `not-established`.

```text
python -B batch_observe.py observe --json --repo REPO --commit HEX40 --path REL [--members-book ABS]
python -B batch_observe.py observe --json --repo REPO --live --path REL
python -B batch_observe.py observe --json --supplied FILE [--path REL]
```

Git use is limited to `rev-parse --verify` and `cat-file` on the named repository. A worktree file and a supplied file are not reported as Git blobs. A pin mismatch stops the run before import, Git, or inspect.
