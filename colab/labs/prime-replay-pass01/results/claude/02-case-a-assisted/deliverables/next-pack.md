# LAB ONLY — NOT RELEASED. Proposed next pack (assisted run 02): 0513.bench-build 05.02 — accepted method controls

Proposed by claude-opus-5-5 in Colab run 02-case-a-assisted. This proposal is the same as run 01's, carried over: the assistance added no case A finding that would change it. Nobody executes it from this file.

## Problem
Bench f00c6f29 lacks the controls the accepted method requires (0414.bench 01.002; 0701 review F01–F04):
- pair-level parity, with a sealed allowed-difference list;
- re-verification of the candidate package at collect and compare;
- commitment-scored keys, instead of `must_quote` and `must_mention` wording checks;
- a preparation and repair cost record, with a declared operation unit and start/stop events.

## Scope
`labs/prime-bench-pass01` only, plus new pass notes and evidence. A new bench version; f00c6f29 kept readable.

## Exact sources
- 0414.bench/01.002.md;
- 0701.bench-method/05.01.return.md and 06.01.review.md;
- 0513 build05.01 CONTRACT.md;
- prime_bench.py 258727ee…;
- test_prime_bench.py 5c125c3b…;
- bench.json f00c6f29….

## Steps
1. Notes, then a contract delta.
2. Record a candidate package manifest at prepare. Re-hash it at collect and compare; a mismatch or an extra file is `package-changed`, and the run is not clean.
3. Add a pair check: equal bytes except the sealed allowed differences (the PROMPT Tools paragraph and `support/*`).
4. Key schema /2: commitments scored present, contradicted or absent from a supplied reviewer record. Wording preservation becomes a separate obligation. Migrate the 8 cases under a new version.
5. Add preparation, repair and unit fields; show blank as `unavailable`.
6. Add regression cases for each control and keep the old-version read path.

## Exclusions
- No model or session runs, and no spending.
- No changes to prime_review or return-capture.
- No AR-01 fixtures.
- No Git writes.
- No rewrite of the old cases.

## Verification
- The full suite with its support dependencies present;
- one mutation probe per new control;
- `validate` of the new version;
- an F01–F04 recheck against the code.

## Return expectations
Did, Blocked, Need; the contract delta; command exits; the new bench hash; the remaining unproven limits (isolation is declared). Prime reviews.

## Separate lab observation (not part of this pack)
The replay lab's assistance bundle needs `labs/prime-support-pass01/clerk_adapter.py` for its reader to run. That is a Prime lab preparation item, not a case A build.
