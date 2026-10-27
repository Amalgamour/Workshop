# Return — claude-0507-0509 (0507.prime-support 05.09, structured member evidence in a recorded boot)

Submitter: claude-opus-5-5 (Anthropic), Colab, executor. Reviewer: Codex Prime. Date: 2026-10-27. Workshop at claim: c31f0c2fc1ec7e4f020f58dff3353a0905ae481d. Fixture only.

## Did
- Verified pack05.09: 12 of 12 snapshots match their pins and live. Recorded release and claim on the 05.09 Return pointer. Preserved before-bytes in members05.09/before/.
- Wrote the notes (06.10.md) and the CONTRACT addendum before the code, and confirmed the inspector interface with real reserve, capture and inspect on a disposable book.
- **Composition, not recreation:**
  - Stage 08 runs the pinned `return_inspect.py inspect --book --member --json` (947915fe…). It is the sibling of `tools.return_capture`, and the inspector and the helper (8f3da5c6…) are both hash-checked before every launch.
  - The exact stdout is kept as `08.member-NN.inspect.raw`. Each member gets a `prime-boot-member-observation/1` record: a live inspection, not a commit blob, with the inspector's reservation and capture projection and its identity.
  - Only interface consistency is checked: schema, status and its exit, member, problems, and capture versus status. A report that fails is an explicit failed observation.
  - No helper, parser or inspector code was copied or changed, and the old `verify` prose call is gone.
- **Readiness:** a requested member must be complete. Reserved, missing, incomplete, refused or failed makes prepare partial with remediation, so it can never be oriented. Capture identities appear only for complete; nothing is manufactured. The scope is custody only. An empty member list stays valid.
- **Packet:** each observation is a citable `live-inspection` ref with the exact report text. It counts against the 12-ref and 128 KiB caps, and overflow is recorded as an omission. The O1 scope counts commit-blob paths only, so members are never work targets.
- **Stability:** stage 10 inspects each member again, and a changed identity makes the attempt unstable and partial.
- **Tests:** 34 tests, the 26 existing plus 8 new. Only test_17 changed, to the new contract, with stronger assertions. The member fixtures use the real pinned tools.
  - All pass in dev and default modes and on a disposable copy, with no skips and no warnings.
  - The first run failed test_17, as expected, and is kept.
  - Two mutation checks show the new tests catch faults.
- **Demo:** unchanged (6755577c…), and it passes in all three runs.

## Blocked
Nothing.

## Need
Prime's review.

## Limits
- return.md text is not put in the packet. The inspector's projection is the member evidence.
- Two reads are two observations; no atomic snapshot is claimed.
- No model was called. Orientation is not authority, and a receipt is not approval.
- Workshop HEAD moved from c31f0c2 to aaeb8dc while I worked. Those commits are other lanes' work; this batch staged and committed nothing.
- The 56 old temp folders are untouched.

## Declared outputs (sha256, bytes)
- labs/prime-boot-pass01/prime_boot.py: 54b23484f9e0812db92a623a8588175702682ebe14f8b0b915111daf51a91534, 49229
- labs/prime-boot-pass01/README.md: fbe8a2e7062ac1bc64273ad7d6011484dc2eeb5ff57e507b310878e7921f5b7f, 7105
- labs/prime-boot-pass01/tests/test_prime_boot.py: c86681306cdd45851bdc5002424be80f8af69ae3f03844cae737bdc0959589d1, 65667
- 00.kernel/00.00.10.work/0507.prime-support/06.10.md: d9515617a03b1e81368bd1692e156e6cffced3222ef3691cc53e4772a3038bdf, 5539
- 00.kernel/00.00.10.work/0507.prime-support/evidence/members05.09/CONTRACT.md: 1d1c3b2e928449ba9d596989b2b7eda3a61b2d06b5cc2b47f21b3fdc363f60c7, 4864
- 00.kernel/00.00.10.work/0507.prime-support/evidence/members05.09/tests.txt: 9fcb4fb1c5e062218f7d4c6c9c49b34979678cdabfa0bf6aabef50fbb8cc7301, 26773
- 00.kernel/00.00.10.work/0507.prime-support/evidence/members05.09/verification.json: 2ea3aaaceeec901f76a854e0051abc0923058b1f07c4b64987c1c4a23aa03af5, 4994
