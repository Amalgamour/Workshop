# BUILD-PACK — invoke the acceptance harness on the combined candidate (UNAPPLIED proposal)
from: claude-opus-5-5 (Colab 0707/05.21) · for: the later integration builder · state: **PROPOSED. Prime places and releases it. No number, branch, selection or release.**

## Preconditions
1. **K (capacity) and I (N5 instance)** are reviewed and accepted by Prime, and their files are frozen in a new pack manifest.
2. **The reporter successor R** (observing the combined chain) is built and accepted.
3. **The combined candidate W** is built per the 05.19/05.20 plans. It must be:
   - G (pass05) as the grammar;
   - the L functions over G;
   - K's validator;
   - N7 records with `custody: not-applicable` (N5 enums unchanged);
   - a door with `open`;
   - R on the same chain.
   - **Explicit lab adapters only where a lab root needs them, listed in its `CANDIDATE.json`.**

## Tasks
1. **Add a `--kind combined` builder** to `make_candidate.py` that copies ONLY files frozen in the new manifest, plus declared lab adapters. **No hand-placed bytes.**
2. **`make_inputs.py`:** fill K, I, R and W from the new manifest by the replacement procedure (INPUTS.md). Do not edit other rows.
3. **Implement the four reserved cases** (CAP-4, RP-1, RP-2, IN-2) in `harness.py`. Their requirements are fixed in MATRIX.md. They currently return `not-run` and stay blocked until K, R and I are accepted.
4. **Run, in order:**
   1. `test_verdict.py`: 16/16 required;
   2. `demo_hostile.py`: 6/6;
   3. `harness.py` (full suite).
5. **Keep all first failures and raw stdout, stderr and exits.**

## Acceptance
- **The full suite exits 0 with `ready: true` on the combined candidate,** with every required case `pass`, every dependency `accepted`, and the three KF records `known-failure-not-reproduced` for capacity, reporter and instance (the fixed behaviors).
- **The baseline candidates** (proto-l, staged-g) still give NOT READY: the regression guard.
- **The live book:** only Prime-authorized read-only prepare/form on the named cuts. **The harness never targets the live book.**

## Stop conditions
- any refusal in validation;
- any `error` record;
- a required case passing only because a field was absent;
- a need to edit a frozen or historical file, or a pinned predecessor, in place;
- a dependency without a Prime review.

## Return shape
Did / Blocked / Need, then:
- the candidate identity and lab differences;
- the inputs manifest hash;
- the full result JSON;
- the unit and hostile results;
- first failures;
- what stays pending.

The artifact manifest excludes itself. **Follow the assigned route.**
