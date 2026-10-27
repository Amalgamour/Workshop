# Return — claude-0507-0507 (0507.prime-support 05.07, recorded Prime boot prototype)

Submitter: claude-opus-5-5 (Anthropic), Colab, executor. Reviewer: Codex Prime. Date: 2026-10-27. Workshop at claim: db4629e48217a79d6f9839afd7ea105ec5ec8fb8. Fixture only.

## Did
- Verified pack05.07: 16 of 16 snapshots match their pins, and live matches all 16. The capture helper 8f3da5c6… and the contents checker fc16d2f6… are verified. Release and claim are recorded on the 05.07 Return pointer.
- Wrote the notes first (06.08.md), then CONTRACT.md, then the lab `labs/prime-boot-pass01/`, all standard library only:
  - prime_boot.py, with `prepare`, `check`, `judge` and `show`;
  - README.md;
  - tests/test_prime_boot.py, 18 tests;
  - demo.py.
- **PB-01:**
  - The attempt directory is allocated exclusively, and the raw request and intent are written before any fallible step.
  - Each of the ten stages writes its own write-once record, ok or failed. A failed attempt is kept.
  - An interruption leaves no outcome, and `show` reports it as interrupted.
  - A records root that is unusable or inside Git refuses with "nothing was recorded".
- **PB-02:** the O1 target must lie inside the declared scope and be cited. Every reported conflict must be acknowledged. Attention order is recorded as advice and has no role in checking.
- **PB-03:** O5 accepts `none_found`. Sources absent at the commit get citable absence records (A-ids).
- **PB-04:**
  - Packet text is the exact committed blob. The live observation is a separate field: same, differs with its hash, or absent.
  - Dirty paths are recorded.
  - HEAD, the branch, the registry and the tool hashes are re-read at the end. A change makes the attempt partial, so it can never be oriented.
- **PB-05:** included refs carry their full text within the caps of 12 refs and 128 KiB. Anything capped out gets an omission record with its hash; nothing is truncated. Members get capture integrity only. Every outcome says `authority: none`.
- **Tools:** the four tool hashes are fixed in code and checked before every launch. A mismatch never launches.
- **Unsupported:** Clerk jobs are refused as unsupported. return_inspect.py is not read or imported.
- **Tests:** dev and default modes both pass, 18 of 18. The first run failed one test (test_18's expected set) and is kept in tests.txt.
- **Demo:** attempt 1 is partial, its checks fail, and it is judged gap with remediations, giving not-oriented. Attempt 2 links attempt 1 and is oriented. Answers and judgements are fixtures.

## Blocked
Nothing.

## Need
- Prime's review.
- One residue for the Director's decision: test runs 1-3 left 56 disposable `pb-*` fixture folders in the system temp directory. The teardown is now fixed, and later runs leave none. The leftovers were not removed, because a broad temp sweep was not permitted in this session.

## Limits
- No model was called, and no claim is made that a model cold-booted.
- `oriented` means the recorded exercise passed. It does not resolve reported conflicts.
- The reviewer is a label, not authentication.
- Workshop HEAD moved from db4629e to b13c7ef while I worked. Those commits are other lanes' work; this batch made no commit or push.

## Declared outputs (sha256, bytes)
- labs/prime-boot-pass01/prime_boot.py: c3c194fc897e2108b0d67305345122363a68bc085051d92ba04c3c0f543e1582, 34184
- labs/prime-boot-pass01/README.md: b616777e5058b652f6c3bffe11ccf85fc63273a6e07872ed8e2d210b884f59e1, 3502
- labs/prime-boot-pass01/tests/test_prime_boot.py: b2e23fba99bd11afe2c66537fae63ef2cfad4e29578a77f4f229508a01da0a8f, 31255
- labs/prime-boot-pass01/demo.py: 6755577c97b03a5b2b539d0c7d152e913f3b8040713dacb1a58908a6a06304a6, 3637
- 00.kernel/00.00.10.work/0507.prime-support/06.08.md: 89bfc632f36e4aba2d19affde7e7fb6ccb535db968a30b91e905afed5decc558, 3389
- 00.kernel/00.00.10.work/0507.prime-support/evidence/build05.07/CONTRACT.md: d946e48b7afea2b501607a8a63cb0bdecab231e0304d19634e165338d81b3231, 7087
- 00.kernel/00.00.10.work/0507.prime-support/evidence/build05.07/tests.txt: d1c8193bb4757f79be271df9f2759ae4336a707b3e8a3f18b894fad40ef5ac61, 17342
- 00.kernel/00.00.10.work/0507.prime-support/evidence/build05.07/verification.json: 971075e161f3bee3484a06523ae5b4b021d6104bfb27d73a3bafa23e747a23e1, 4623
