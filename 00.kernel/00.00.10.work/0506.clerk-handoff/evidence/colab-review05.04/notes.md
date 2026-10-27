# Initial notes — Claude lead review of the Clerk correction (05.02) and inspection (05.04)
Date: 2026-10-27, written before reading clerk.py and before any test run.
Reviewer: claude-opus-5-5, independent Colab/technical lead. Batch 0506/05.05.

## Source identities (pack05.05 at 3642f6c53eec08fde1a2de3f13aa535d73604208)
All 14 snapshots match their pins and their blobs at the pinned commit, and the live bytes equal all 14 at claim time (workshop 282c1f6).
- clerk.py e3918dae…, 51612 bytes (schema-2 plus show --json)
- README.md 8d97f815…
- demo.py ae6653a9… (unchanged since pass01)
- tests/test_clerk.py 25b05724…
- lab evidence/SHA256SUMS.pass03.txt 62891eb4…
- pages: 01, 05.02, 05.04, 06.02 (my 05.01 review), 06.03, 06.05, 06.06 (my seam notes), 06.07, prime-review05.04/review.md

## What I am reviewing against
- My own 06.02 findings CR-01 to CR-05.
- Prime's 05.02 contract: witness, OSError → exit 2, blank evidence and empty outputs refused, a portable git test, LF manifests.
- 05.04's inspection contract: schema clerk-handoff-inspection/1; fields schema, job_id, state, job, claim, returned, checks, problems; no writes; structural failure never yields a clean returned document.
- The consumer I designed in 06.06 / SEAM.md, which needs from Clerk: job (assignee, reviewer, instructions sha, expected_outputs), claim token, returned delivery, artifact hashes, completion state.

## Builder and Prime claims, to verify rather than accept
B1. 32 tests, 31 ok, 1 symlink skip (05.04 return). Demo: 17 processes, codes 0 0 0 0 0 2 2 0 0 0 0 0 0 0 1 1 1.
B2. Inspection is read-only on every path, including failure.
B3. Incomplete, corrupt and unknown documents carry null job, claim and returned.
B4. The witness detects an isolated missing or changed half of the returned pair. It does not detect coherent loss or rewrite of both files.
P1. Prime: an independent verification pass, and the earlier terminal-loss probe passed (05.02 review).

## Questions I expect to test
Q1. Does a returned document report `instructions: usable` only when a base was given and matched? Without a base, what does it say?
Q2. Do the returned artifacts in the JSON come from the recorded 0003 event, or from rescanning the outbox?
Q3. A witness with the right digest but a wrong job id, schema or keys: is it detected?
Q4. Does `state: returned` with checks.artifacts `changed` exit 1? A consumer must not read it as clean, so is there one field that says "clean"?
Q5. Are "not-checked" and "not-applicable" distinguishable from "ok" in every check?
Q6. Do read errors at every step produce valid JSON, exit 2, and no traceback?
Q7. Is the resend after a deleted return refused, so the witness blocks a different re-return?
Q8. Does the human `show` still print the token, which my seam design's replay path relies on (SEAM S4)?
Q9. Is the inspection interface enough for the seam consumer, or does the consumer still need raw events (06.06 dependency P02)?

## Unknowns at this point
- I have not read the correction code. Earlier-session recollection is not evidence.
- The Prime's probe scripts are not in the pack: only its review text.
