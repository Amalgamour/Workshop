# Submission — 0523/05.01 desk core
date: 2026-10-31
who: Grok Build (xAI), grok.com GitHub-connected builder
state: prototype submitted for Prime review; not accepted and not production-ready

## Did
Built `app/desk_core/`, invoked as `python3.11 -B -m app.desk_core`.
It runs the assignment loop on an explicit disposable book: record a task,
register a supplied release and claim, show that task to a new process, capture
a return, retrieve it, render a supplied Prime judgment in full, and recover
the next actor and action after restart.
N5NN `0523.sample` captures both pass 01 and pass 02 on `0123.sample` only.
N7NN keeps pack, return, and review on the Colab page and allocates no N1NN line.
Undeclared bands are refused. An occupied return number is not overwritten.
Expected negative cases refuse: done-without-capture, changed bytes, wrong line,
wrong pass, wrong source hash, stale release/claim, stale review, conflicting
claim, review without a return, interrupted write, assignment projection conflict.
Source pins: 33 of 33. Existing app modules and pinned labs were not edited and
are not imported. Runtime dependency: Python standard library only.
Tests: 9 run, 0 failed, 0 skipped, 0 errors, about 4.6 seconds, interpreter
Python 3.11.2. Command and transcript: evidence/build05.01/unittest.txt.
Demo exits `[0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0]`: evidence/build05.01/demo-transcript.txt.
Implementation commit: 6024a4245a87471a68cb85230172b333cc8c1549.
Notes checkpoint: 2c8a72b93b4782915ea0cbbcede4fadf4a33b3c5.
Preparation commit: 17ad02453edde4a2f65f6a0d78686004bf4e5fe1.

## Blocked
Live matching-line custody for this batch. `0123.boot-validation-0508` already
occupies 0123. This submission stays on 0523 until a reviewed migration.
Python 3.12 is not installed here. The pack said not to install. The same
standard-library code was executed with Python 3.11.2.
No production integration. `app/librarian.py` was left byte-identical on purpose.

## Need
Prime review of branch `builder/grok-core-pass01` before any integration.
A reviewed decision for the occupied 0123 line before any live move.
No other input is required to inspect or rerun the disposable prototype.

## Not claimed
This is not production-ready. Tests do not prove semantic correctness, a real
model session, OS isolation, authenticated roles, or race freedom. `accepted`
is false on every result. A receipt is not a review. A review is not approval,
seating, migration completion, or permission to launch a model.
