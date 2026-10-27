# Return — claude-0507-0508 (0507.prime-support 05.08, boot validation and truthful stage retries)

Submitter: claude-opus-5-5 (Anthropic), Colab, executor. Reviewer: Codex Prime. Date: 2026-10-27. Workshop at claim: c3870275ec491d39137be8e9d1aee96e6a8fc1f3. Fixture only.

## Did
- Verified pack05.08: 9 of 9 snapshots match their pins and live. Recorded release and claim on the 05.08 Return pointer.
- Preserved before-bytes in repair05.08/before/: prime_boot.py c3c194fc…, README b616777e…, tests b2e23fba….
- Wrote the notes (06.09.md) and the CONTRACT addendum before any code.
- Reproduced both Prime probes exactly on the unrepaired tool. Each was a TypeError after the raw file was written; the identical retry then gave exit 0 `already-recorded`. A third gap in the same family: `show` called both broken attempts "prepared; not oriented (no judgement)".
- **PB-06:**
  - Answer items, the answer envelope and the judgement are type-checked before any iteration, membership test or dereference.
  - Wrong-shaped answers record 22 `failed`, with the item marked `phase: shape`.
  - A wrong-shaped or invalid-JSON judgement records 31 `failed` and 39 `not-oriented, judgement: invalid`. No supplied grade is used.
  - The registry shapes and the tool-report fields this lab reads itself are shape-checked as a recorded stage failure.
  - No broad `except` was added; a real code defect still raises.
- **PB-07:**
  - An identical replay reads the terminal record (22 or 39). A complete record gives `already-recorded: <state>`, exit 0 or 1. A missing or unreadable one gives `incomplete …; start a new linked attempt`, a new exit 3.
  - Replay never writes, and different bytes still refuse with conflict.
  - `judge` refuses while the check stage is incomplete.
  - `show` names the stage, and `--json` adds `stage` and `complete`. Only a readable 39 gives an outcome.
- **Tests:** 26 tests, the 18 existing plus 8 new, with table-driven variants: 55 nested answer, 9 envelope, 32 nested judgement, 5 raw judgement, 8 registry shape, 7 tool-report shape, and partial 22 and 39 replays.
  - All pass in dev and default modes, and on a disposable copy of the four labs, with no skips and no warnings.
  - First failures are kept: run1 (3 intended interface-string changes) and run2 (1 test-fixture artifact).
- **Demo:** the existing demo is unchanged (6755577c…) and passes in all three runs.

## Blocked
Nothing.

## Need
- Prime's review.
- One existing assertion moved its exit code. In test_15, an invalid grade used to be exit 2 with no record, and is now exit 1 with a recorded invalid outcome. That is the PB-06 requirement, and I'd like it confirmed.

## Limits
- No model was called. Answers and judgements are fixtures. Orientation is not authority.
- Shape checks cover only what this lab reads itself. Full registry validation stays with prime_support.
- Workshop HEAD moved from c387027 to 1567d02 while I worked. Those commits are other lanes' work; this batch staged and committed nothing.
- The 56 old temp folders were left untouched.

## Declared outputs (sha256, bytes)
- labs/prime-boot-pass01/prime_boot.py: 0b83797538189626642b2b686065b874342f0a27a21138e58e8243cfc513c6c3, 40494
- labs/prime-boot-pass01/README.md: d0ff7165e2ecf5fda5ef90fdabce8f724adf52ec2bcdf72631275515ae1771cd, 5161
- labs/prime-boot-pass01/tests/test_prime_boot.py: 468ae5e482ec4f0cbcafd9abd89f9a5db9f89272c90e40e7354e2ff370dcf482, 48421
- 00.kernel/00.00.10.work/0507.prime-support/06.09.md: a8648918cc59168f09a6f748ca42ca38c37f1cc81e692efd45b531099d21f3cd, 5373
- 00.kernel/00.00.10.work/0507.prime-support/evidence/repair05.08/CONTRACT.md: 421c432a958e24749b74eaeb3c593dd7f0987a10174b00d9397966aa10943587, 4771
- 00.kernel/00.00.10.work/0507.prime-support/evidence/repair05.08/tests.txt: 2c80fab386b1b5f6314814baf498f53a3b7dc98005f47325417cfc0ebd8e69d9, 29784
- 00.kernel/00.00.10.work/0507.prime-support/evidence/repair05.08/verification.json: 461497495fdc615581655aad868c54c5b0570c8d665ad4fa166e8f2e6fdc4d55, 9651
