# LAB ONLY — NOT RELEASED. Proposed next pack: 0513.bench-build 05.02 — implement the accepted method controls

Proposed by claude-opus-5-5 in Colab run 01-case-a-manual. This is a lab output, not a release. Nobody executes it from this file.

## Problem
prime-bench-pass01 (bench f00c6f29) predates the accepted method revision (0414.bench 01.002; 0701 review F01–F04). Four controls are missing or contradicted:
- **F01:** no pair-level parity check;
- **F02:** wording-based deterministic keys, with no commitment scoring;
- **F03:** no candidate-package re-hash after prepare;
- **F04:** no preparation and repair cost record.

A live trial on it could read measurement bias as support benefit.

## Scope
`labs/prime-bench-pass01` code, tests, cases and README, plus new notes and evidence for this pass. A new bench version; f00c6f29 and its records stay readable and distinguishable.

## Exact sources (pin before the claim)
- 0414.bench/01.002.md;
- 0701.bench-method/05.01.return.md and 06.01.review.md;
- 0513.bench-build/evidence/build05.01/CONTRACT.md;
- labs/prime-bench-pass01/prime_bench.py (258727ee…);
- tests/test_prime_bench.py (5c125c3b…);
- bench.json (f00c6f29…).

## Steps
1. Write notes, then a contract delta, before code.
2. **Parity (F01).** At prepare, record a candidate package manifest. Add a `pair` check, in compare, or as a separate command, refusing to read a baseline/assisted pair as comparable unless every candidate file has an equal sha256 and length, except a sealed allowed-difference list: the PROMPT Tools paragraph and `support/*`. Seal that list in conditions.json and bench.json.
3. **Package integrity (F03).** At collect, and again at compare, re-hash every candidate file against `run.json` `candidate_files`. On a mismatch or an extra file, the run is not clean: `package-changed`. Keep the original record.
4. **Commitments (F02).** Add a key schema `prime-bench-key/2` with `commitments` (id, text, the action it constrains), scored present, contradicted or absent from a supplied reviewer record. Keep `must_quote` only as a separate preservation obligation that cannot satisfy or cancel a commitment. Migrate the 8 cases under the new bench version, keeping the old keys.
5. **Cost fields (F04).** In run.json, a preparation record: preparer label, prepared-at, and repairs as events. Declare the operation unit and the start/stop event definitions in conditions.json. Compare shows them, with blank or unavailable kept visible.
6. **Regression cases:**
   - an assisted package edited after collect of the baseline gives not clean;
   - a parity mismatch in a non-allowed file gives parity-fail;
   - a paraphrase that keeps the commitments, against a quote that contradicts the action, scores correctly;
   - a blank preparation record shows as unavailable;
   - the old bench version is still readable.

## Exclusions
- No model runs, no sessions, no spending, no live N7 trial.
- No change to prime_review or return-capture.
- No AR-01 fixtures.
- No Git writes.
- No rewrite of the f00c6f29 cases.

## Verification
- The full suite with the support dependencies present: report the count, skips and exits.
- Mutation probes for each new control.
- `validate` on the new bench version.
- One SYNTHETIC end-to-end pair per family.
- The F01–F04 table above, rechecked against the code, not the contract.

## Return expectations
Did, Blocked, Need. A contract delta naming the schema versions. A verification record of the commands and their exits. The new bench version hash. Explicitly: what is still unproven (isolation is still declared, not observed). Prime reviews; the Director is not needed unless a control forces a design fork.
