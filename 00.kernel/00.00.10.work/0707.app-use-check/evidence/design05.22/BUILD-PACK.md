# BUILD-PACK (updated) — run the harness successor on the combined candidate (UNAPPLIED proposal)
from: claude-opus-5-5 (Colab 0707/05.22) · supersedes: `evidence/design05.21/BUILD-PACK.md` (kept) · state: **PROPOSED. Prime places and releases it. No number, branch, selection or release.**

## Preconditions (all four from Prime, not the builder)
1. **K and I** are reviewed and accepted, and their files and review pages are frozen in a new pack manifest.
2. **R** is built and accepted. It exposes `review-report --book --source --pass` through the candidate dispatcher, with the CONTRACT.md fields (`state`, `stale`, safe flags, `review_id`, `custody`, `exchange`). If R uses other names, Prime amends CONTRACT and `judges.rp1` first.
3. **W, the combined candidate,** is G (pass05) as the grammar, the L functions over it, K's validator, N7 records with custody `not-applicable`, a door with `open`, and R on the same chain. Only explicit lab adapters, each listed in its `CANDIDATE.json`.
4. **The harness successor is reviewed by Prime** (06.22).

## Tasks
1. **Builder:** a NEW `make_candidate` successor with `--kind combined`. It copies ONLY files frozen in the new manifest, plus declared adapters. **pass01's builder stays frozen.**
2. **`make_inputs.py`:** fill K, I, R and W by the DEPENDENCIES.md replacement procedure (`status`, `files`, `review_ref`, and R's `interface`). No other row is edited.
3. **Run, in order, keeping stdout, stderr and exits:**
   1. `test_verdict.py` (40);
   2. `test_shapes.py` (24);
   3. `test_callbacks.py` (29);
   4. `demo_hostile.py` (14/14);
   5. the full suite on W;
   6. the full suite again on both baselines;
   7. `reconcile.py`;
   8. `reconstruct.py`.
4. **No callback is edited to make W pass.** A judge or contract change is a Prime decision, recorded with its reason.

## Acceptance
- **W:** the full suite exits **0** with `ready: true`, `scope: full`, all 37 required cases `pass`, all six rows accepted, and KF-CAP, KF-RP and KF-IN `known-failure-not-reproduced`.
- **Baselines:** still NOT READY, with the same reconciled verdicts (the regression guard).
- **The live book:** only Prime-authorized read-only prepare/form. **The harness never targets it.**

## Stop conditions
- a refusal;
- any `error`;
- a pass caused by an absent field;
- a need to edit frozen, historical or pinned files in place;
- a dependency without a frozen Prime review reference;
- a subset run presented as readiness.

## Return shape
Did / Blocked / Need, then:
- the candidate identity and lab differences;
- the inputs hash;
- the full result JSON;
- the unit, hostile, reconcile and reconstruct results;
- first failures;
- what stays pending.

The artifact manifest excludes itself. **Follow the assigned route.**
