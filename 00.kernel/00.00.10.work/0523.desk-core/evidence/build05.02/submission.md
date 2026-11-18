# Submission — 0523/05.02 desk-core repair
date: 2026-10-31
who: Grok Build (xAI), grok.com GitHub-connected builder
state: repair submitted for Prime review; not accepted and not production-ready

## Did
Kept the desk-core prototype and repaired the five review findings on
`builder/grok-core-pass01`.
Implementation commit: bb64c537f01c370b5bd9aaf925db63a55bc5b406.
Fast-forward base: 5e0040e1598db3b9d9b6584e4d0b19a629356ad1. No force and no
reset. `main` and `workshop` were not written.

1. Portable writes. `atomic_write` and `exclusive_write` use `O_BINARY` where
   that flag exists and write the whole buffer. An existing `name.tmp` is
   refused with `temp-occupied` and is not truncated. `file_lock` uses
   `fcntl.flock` on POSIX and one-byte blocking `msvcrt.locking` on Windows.
   The Windows path is not a no-op. Locks are not claimed to be race freedom.
2. Revision history. `revise-task` requires a supplied `reason` and
   `authorizing_reference`. Exact prior task and face bytes are stored under
   `05.PP.history/<revision>/` before replacement. `revision.json` is not
   rewritten. `05.PP.selected.json` is written last. The same request hash
   does not add another history row. `--interrupt` exits 3, keeps the prior
   bytes, and records `05.PP.revision-partial.json`.
3. Stale returns. A receipt keeps the task binding it was captured under.
   Reviewing a later task with that return is refused `stale-return`. The
   receipt bytes stay. Recover reports `return-stale`, `review_fresh` false,
   and `derived` true. Stale release and claim do not supply the review's
   next action.
4. Source identity. The leading workflow digit is kept. `1523.sample` returns
   on `1123.sample`. `1702` stays page-local and allocates no `1102`. Task
   binding version 2 includes page, subject, pass, and kind. Equal text at
   two addresses does not share a hash. Version 1 task preimages still
   recompute and are not treated as version 2.
5. Traces. Open-pass results and the stale-return refusal name contract
   `desk-core/2`, the check, the input hash, the outcome, the next route, and
   a durable `05.PP.trace` record. The refused review request is kept under
   `05.PP.refusals/`.

Tests: 15 run, 0 failed, 0 skipped, 0 errors, 6.980 seconds, Python 3.11.2.
Command transcript: evidence/build05.02/unittest.txt.
The same 15 tests also passed on the host's Python 3.10.22
(evidence/build05.02/unittest-py310.txt). That run is not Windows acceptance.
Demo exits `[0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0]`:
evidence/build05.02/demo-transcript.txt.
Pack 05.02 pins: 16 of 16. Pins command: 33 of 33.
`app/librarian.py` was not edited. No dependency was installed.

## Blocked
Native Windows Python 3.12+ was not run. It remains Prime's acceptance check.
No runtime was installed and no paid CI was started.
Live matching-line custody. `0123.boot-validation-0508` still occupies 0123.
This repair does not migrate that line and does not claim it.
No production integration.

## Need
Prime review of `builder/grok-core-pass01`, including a native Windows
Python 3.12+ rerun of the unmodified source.
A reviewed decision before any live move onto the occupied 0123 line.
No other input is required to inspect the disposable books or the traces.

## Not claimed
This is not production-ready. Tests do not prove semantic correctness, a real
model session, OS isolation, authenticated roles, or race freedom. `accepted`
is false on every result. A receipt is not a review. A review is not approval,
seating, migration completion, or permission to launch a model.
Linux Python 3.11.2 and 3.10.22 are the only interpreters that ran this
repair. Windows is pending, not passed.
