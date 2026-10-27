# Return — claude-0507-0506 (0507.prime-support 05.06, smallest recorded Prime boot)

Submitter: claude-opus-5-5 (Anthropic), Colab, design executor. Reviewer: Codex Prime. Date: 2026-10-27. Workshop at claim: 3db0957a6bf8870ff6ac5978fffa152aed06972d. Design only.

## Did
- Verified pack05.06: 12 of 12 snapshots match their pins. Live 00.md and the 0100 door have changed since the pack, so the snapshots were used. Capture helper 8f3da5c6… verified.
- Wrote notes first (06.07.md), then BOOT.md, examples.json and verification.json under evidence/boot-design05.06/.
- **Inventory.** Built and accepted, fixture lab: prime_support.py 700d60d2…, clerk_adapter.py 2f30ba75…, return_capture.py 8f3da5c6…. Built, but its hash is not in this pack: the contents checker. Draft dependency: return_inspect.py (0508/05.04, Release PENDING, no hash). Missing and proposed: the boot request, the attempt record and the orientation runner.
- **One manually initiated boot**, steps B0 to B10:
  - it pins workspace, branch, commit, role label, model label, registry and member list;
  - compute verifies HEAD; reads the book pointer and contents (checker pin-gated); records seats and the canonical record as text; runs `prime_support status`; verifies members; and builds one capped packet of exact `path@commit#sha` or member#receipt references;
  - the model reads only the packet;
  - compute checks the citations and machine-readable fields, and a judge grades the explanations;
  - each attempt is written once and links the previous attempt.
- **Member returns** become subjects as (book, member, receipt sha256), through `verify --member` for integrity. Structured fields wait for the accepted, pinned inspector. The 05.NN Return pointer is never parsed as the submission.
- **Readiness:** a six-item orientation exercise (O1-O6) with an explicit compute/judge split. The outcome is oriented, partial or not-oriented. Anything below oriented stops dependent execution, while read-only investigation may continue. A gap becomes a recorded remediation (a reference or an owner question) plus a new attempt, never a pass.
- **Examples** E1-E5: clean (hypothetical); stale or contradictory assignment (real: canonical 1ee161c5… against goal page 42e5a587… against seats dbf2399d…, plus mojibake); new sealed return (real: 0107, receipt 5fbddb14…); missing tool pin (real: 0508/05.04 PENDING); unresolved Director decision (real: M01/M02 deferred).
- **One recommended slice:** `labs/prime-boot-pass01/` with prime_boot.py `prepare | check | judge | show`, a prime-boot/1 attempt record, pin-gated dependencies and a listed test set.

## Blocked
Nothing for the design. Implementation would be blocked on Prime-supplied pins for the contents checker, and, for structured member fields, for return_inspect.py.

## Need
Prime's review, and Director decisions on U01 (record location), U02 (judge), U03 (multi-lane assignment) and U05 (whether role 0063 must be seated). U04 (packet cap) is Prime's.

## Limits
- Free-text understanding is judged, not mechanically proved.
- Labels are not authentication.
- A boot is not the finish-line-3 cold-model test unless the Director says so.
- Nothing was built or run.

## Declared outputs (sha256, bytes)
- 00.kernel/00.00.10.work/0507.prime-support/06.07.md: 9c63eab5593a283d8ca04af53af31dd1fe2032dc6ca3ae638f03177e1589e66a, 4858
- evidence/boot-design05.06/BOOT.md: f88d9095526ca24e2bef5bcedf54dcc369c67b784a5aa3862a4885091c634ae1, 10211
- evidence/boot-design05.06/examples.json: 49dc7d87f523a5cbcb60f22a131a56594c453beaae14cc32587e99937c9c511a, 4795
- evidence/boot-design05.06/verification.json: 56d984dd501e2642c4053f266d7e827c1460079ac28b9204b3eb90c172e15d51, 3612
