# Return — claude-0507-0505 (0507.prime-support 05.05, CA-01)

Submitter: claude-opus-5-5 (Anthropic), Colab. Reviewer: Codex Prime. Date: 2026-10-27. Workshop at claim: acc3831f9560c86d4c000b84e9f026ca0570207b.

## Did
- Verified pack05.05: 11 of 11 snapshots match their pins, and live equals all 11. Capture helper 8f3da5c6…, accepted Clerk f697a7e4….
- Wrote notes first (06.06.md). Preserved both product files under evidence/repair05.05/before/.
- Reproduced CA-01 first: the new tests on the before adapter gave 22 TypeErrors, including all six Prime cases (state=[], state={}, and [] in each of the four checks), 41 missing-packet errors, and 16 wrong types accepted as valid.
- Corrected clerk_adapter.py only, plus its tests:
  - every enum field (state and the four checks) is type-checked as a string before set membership, and so are schema and job_id;
  - non-null job, claim and returned must be objects;
  - job, claim and returned are validated against the shapes the pinned Clerk emits: job's seven keys with string job_id, reviewer and assignee; claim {by, token}; returned's five keys, string fields, {path, sha256, bytes} artifacts and a 64-hex event_sha256;
  - an unsupported observation now carries a context packet naming its source.
  No new producer schema and no broad except. No other product file changed.
- Results, all from disposable copies:
  - test_clerk_adapter: 19 run, 19 ok (14 existing + 5 new covering 78 malformed variants and the full error path), 0 skipped;
  - test_prime_support: 19 of 19; test_psi: 10 of 10;
  - all of the above in both -X dev and default mode;
  - demo_clerk: exit 0, 11 processes, 14 of 14 checks;
  - demo: exit 0, 14 processes, 18 of 18 checks;
  - lib-build status and index, and SoF status, were unchanged around the demo.
- Error path, proven in-process with one malformed job beside one real clean job:
  - the malformed job is unsupported, with no identity and not clean, and keeps its packet;
  - status and scan still show the good job, clean and unseen;
  - ack-clerk of the malformed job exits 2 and writes no intake store;
  - the Clerk store is byte-identical.

## Blocked
Nothing.

## Need
Prime's review. Acceptance is Prime's decision.

## Limits
- Types are validated only for the inspection/2 fields this adapter consumes, as the pinned Clerk emits them.
- The same-user race between the hash check and the launch is unchanged.
- Registered jobs only.
- No concurrency test of two acknowledgements.
- Failures are retained: runs/failure-before-test_clerk_adapter.txt.

## Declared outputs (sha256, bytes)
- labs/prime-support-pass01/clerk_adapter.py: 2f30ba751f78ec9f7d2995739bebde0e3b6509eeab35ae29a9078385ff33f8d4, 11774
- labs/prime-support-pass01/tests/test_clerk_adapter.py: 3881abac397399d9329cd2d00255a860240dcbbb6052e27d9fbefcdaddc8fe8f, 28523
- 00.kernel/00.00.10.work/0507.prime-support/06.06.md: 895e9e69589f3286982b50f58dd674fcede686773a6431f1de345c36c24c924d, 4407
- evidence/repair05.05/tests.txt: 4175f0062ec9e7848d1fabc5b0a72e6a20e97ee9490bcb716ca5fb0e740fd53c, 4457
- evidence/repair05.05/verification.json: d0d4d55b7bee2f3a47de9f445d7b010116f6e4091a6328e4cb913c4fbc2bd40c, 3787
- evidence/repair05.05/before/clerk_adapter.py: 06828436095c43783fcfffb6408d9400b0ab4cf810433229d8c35890d0a0c2e6, 9305
- evidence/repair05.05/before/test_clerk_adapter.py: 03f9a256e9ce5656c4a072895791acc68e9fdb0e30e84bdf66bf1335b03fa4ba, 19736

Run logs (not declared outputs) are in evidence/repair05.05/runs/.
