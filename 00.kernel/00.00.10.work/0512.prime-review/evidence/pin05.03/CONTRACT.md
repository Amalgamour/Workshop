# Contract — stale 0014 regression pin

0512.prime-review/05.03.002. Written after 06.03.md and before the test edit.
This file records one expectation change. It does not edit the design page and it does not release held fixtures.

## Files this batch may change

Edit:

- app/tests/test_entry.py

The only product change is the stored digest for 00.kernel/00.00.10.work/0014.design/01.001.md, and the comment that distinguishes the historical routing cut from the current bytes.

Create:

- 00.kernel/00.00.10.work/0512.prime-review/06.03.md
- 00.kernel/00.00.10.work/0512.prime-review/evidence/pin05.03/CONTRACT.md
- 00.kernel/00.00.10.work/0512.prime-review/evidence/pin05.03/verification.json
- 00.kernel/00.00.10.work/0512.prime-review/evidence/pin05.03/artifact-manifest.json
- 00.kernel/00.00.10.work/0512.prime-review/evidence/pin05.03/submission.md

submission.md is the return file. It is not one of the four expected capture outputs.
The return pointer on 05.03.002.md is filled only after capture, verify, and inspect succeed.

## Files this batch does not change

- 00.kernel/00.00.10.work/0014.design/01.001.md
- the other eight paths in PINNED
- app/librarian.py, app/prime_review_tools.py, app/prime-review.json
- labs/prime-review-pass01/prime_review.py
- app/tests/test_prime_review_tools.py
- law, 00.live, other lanes, and sealed returns

## The one expectation

Historical source pin, commit 96785c39b9c58ba32a54398f4b1fe6fbf144edbb:

- sha256 20ba376e05a5ab09fed5d6e9644e3e74a6db954d7e476ff94f76b6469c780d0a
- 1448 bytes
- the return-routing addendum

Current workspace invariant, commit c406b2a9a3d8d9cc1c67c2c79a8e336989cc0eb1, equal to the live file:

- sha256 852ab07d54c1bc77143ddcf0e833c817211bd2336ccf7fdce4d22c5b8867f4f1
- 1828 bytes
- the same page plus the Colab investigation band section

The test stores the current digest. It does not store the historical routing digest, and it does not adopt whatever other files happen to contain.

## Runs

Allowed:

- test_pins() only, not test_entry main
- python -B app/tests/test_prime_review_tools.py

Not run:

- test_entry main
- test-run
- bridge-test
- held inventory or bridge fixtures
- race probes

AR-01 stays in force. Broader execution coverage remains held.
