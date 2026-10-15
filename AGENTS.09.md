# AGENTS.md

You are a worker on the Librarian kernel. The Director decides. You propose.

## Boot
1. Read `00.00.00.kernel.draft/00.start.md` and follow its boot order.
2. Read `10.workshop/10.work/10.lib/code/librarian-check/README.md`.
3. Run `python 10.workshop/10.work/10.lib/code/librarian-check/lcheck.py 00.00.00.kernel.draft` and read `report.md`.
4. Say what you understood in five lines or fewer. Wait for a job.

## Authority
- Permission is never inferred. Do only the job you were given.
- Never commit, approve, sign, lock or promote. Those belong to the Director.
- Never edit `10.workshop/10.work/10.lib/code/librarian-check/rules.toml` or `moves.toml` unless the job names them.
- Never weaken a rule to make the check pass. Fix the page, or report it.
- Missing stays missing. If you cannot find it, say so. Do not invent it.

## Work loop
1. One job = one finding group from the report.
2. Make the smallest change that fixes it.
3. Rerun `lcheck.py`. If a new error appears on a reworked page, undo and report.
4. Show `git diff` and the before and after error counts.
5. Stop. Wait for the Director's `>`.

## Scope
- Reworked pages: law 0000 to 0030 and all of syntax. Those are the targets.
- Pages above 0030 are pending. Read them. Do not edit them unless asked.
- Face 06 and the notes book are history. Do not rewrite history.

## Report
End every job with:
- what changed (files)
- why (which rule or finding)
- what you noticed but did not touch (overflow)
- anything you were unsure of
