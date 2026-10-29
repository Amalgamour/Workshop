# Contract — pinned Prime review entry

0512.prime-review/05.02. Written after 06.02.md and before app code.
This file is development wiring. It is not kernel law.
A report, a guard result, and exit 0 do not release work.

## Files this batch may change

Edit:

- app/librarian.py
- app/README.md

Create:

- app/prime_review_tools.py
- app/prime-review.json
- app/tests/test_prime_review_tools.py
- 00.kernel/00.00.10.work/0512.prime-review/06.02.md
- 00.kernel/00.00.10.work/0512.prime-review/evidence/app05.02/CONTRACT.md
- 00.kernel/00.00.10.work/0512.prime-review/evidence/app05.02/verification.json
- 00.kernel/00.00.10.work/0512.prime-review/evidence/app05.02/REAL-USE.md
- 00.kernel/00.00.10.work/0512.prime-review/evidence/app05.02/artifact-manifest.json
- 00.kernel/00.00.10.work/0512.prime-review/evidence/app05.02/submission.md

submission.md is the return file. It is not one of the five expected capture outputs.
The return pointer on 05.02.md is filled only after capture, verify, and inspect succeed.
app/tests/test_entry.py is not in this edit set. It is a regression run.

## Files this batch does not change

- labs/prime-review-pass01/prime_review.py and the rest of that lab
- app/prime_tools.py, app/prime-tools.json
- app/prime_intake.py, app/prime-intake.json
- app/boot_tools.py, app/batch_tools.py, app/handoff_tools.py, app/context.py, app/clerk_seam.py, app/worker_bridge.py
- their declarations
- law pages, roles, 00.live, assignment registry, other labs
- Claude checker files and Grok-1 workflow files
- 05.01 notes, proposals, and the 0157 capture
- 0162.prime-review-entry-0502/reservation.json

## Pin

Declaration schema librarian-prime-review, version 1, file app/prime-review.json.
One tool, prime_review:

- path labs/prime-review-pass01/prime_review.py
- sha256 805995a1ea8ec3c0b62efad7b5d9ebc8991ba9fd3da75e200b8f626908f4edd0

The same path and hash are constants in app/prime_review_tools.py.
The declaration must match those constants. A different path, hash, tool name, schema, or version is a refusal.
The hash is checked before any launch. A mismatch does not start the process.
A symlink or junction on app/, the declaration, or any path component of the tool is refused and is not followed.
The caller cannot pass a module path, an executable, or a pin file.

## Commands

Only these three librarian commands are added:

- prime-review forwards to the pinned tool's report
- prime-guard forwards to guard
- prime-check-next forwards to check-next

Arguments, each at most once:

- --input ABS required
- --root ABS optional
- --json optional flag

A missing flag, a repeated flag, a missing value, an unknown flag, a relative path, a UNC path, a path containing `..`, or a linked input or root prints `stop:` on stderr, exits 2, writes empty stdout, and does not launch.
`--dest`, `--repo`, `--expect-sha256`, and a draft token are refused the same way. The lab draft writer is not exposed.
`--timeout` and a tool-path override are refused the same way.
There is no default input, no default root, and no registry discovery.

The child is the current Python executable with `-B` and an argument array. There is no shell. There is no outer timeout.
The working directory is the workspace that contains this entry, chosen by the entry, not by the caller.
Stdout and stderr bytes are copied unchanged. The child's integer exit is returned unchanged, including 0, 1, and 2.
Exit 0 is not read as release, readiness, approval, or closure.
Exit 1 remains the tool's attention, hold, or not-closed result.
Exit 2 from the tool stays the tool's own `refused:` or argparse text. It is not rewritten as `stop:`.
A wrapper refusal stays `stop:` and does not launch.

JSON and Markdown are the tool's bytes. This entry does not add a sentence that claims a release, enforcement beyond the check, authentication, or automatic closure.

## What the entry does not do

It does not import the review module on the refusal path.
It does not call a model, a clerk, a dispatcher, or another command.
It does not write a page, a draft, or a capture.
It does not change pack-check, prime-status, boot, batch-observe, capture-return, or `run`.
`run` and an unknown command still stop with `normal run is not activated`.
