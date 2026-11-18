# PRIME-USE — freshness-boundary tests (0707/05.23)
**Lab only.** Every room is external and explicitly retained (no system temp directories).
- **A pass is test evidence**, never approval, selection or release.
- **Automated inspect captures are not Prime's read.**

Run from `D:\Git\lib-build`. Use a NEW `--rooms` directory for each run.

## Equipment tests (no app)
```bash
python -B labs/freshness-boundary-tests-pass01/test_judges.py
```
30 tests: the judges (positive, negative, absent field, wrong type, refuse-everything) and the identity gate (refusals before execution).

## Run a candidate
```bash
python -B labs/loop-convergence-harness-pass01/make_candidate.py --kind proto-l --root D:/librarian/temp/fbt-NEW/cand-proto-l
```
```bash
python -B labs/freshness-boundary-tests-pass01/run.py --candidate D:/librarian/temp/fbt-NEW/cand-proto-l --identity labs/loop-convergence-harness-pass02/inputs/inputs-proto-l.json --rooms D:/librarian/temp/fbt-NEW/rooms --out D:/librarian/temp/fbt-NEW/result.json
```
- **Use `--kind staged-g` and `inputs-staged-g.json` for the other baseline.**
- **`--cases R0,F1b`** runs a subset. A subset never reports all-pass.
- **Exits:**

| Exit | Meaning |
|---|---|
| 0 | every required case passes (full run only) |
| 1 | otherwise |
| 2 | refused before execution (identity) |
| 3 | crash |

- **Read** `records[].verdict`, `reasons` and `observed`. Full inspect text is at `<rooms>/<case>-inspect.stdout`.

## Grok-1's combined candidate (later; WITHOUT changing any expectation)
1. **Prime freezes its files** and writes a `harness-inputs/2` identity manifest: `candidate` = its CANDIDATE.json hash and every file, with `kind: "combined"` in its CANDIDATE.json, plus `open_entry` if it has one; accepted rows with frozen `review_ref`.
2. **Run `run.py`** with that manifest. **C4 executes only when the candidate kind is `combined`;** otherwise it is BLOCKED.
3. **Reconcile.** `reconcile.py` holds the baseline predictions only; for the combined candidate the expectation is simply that every required case passes.

## Evidence helpers
- **`helper_regions.py --out F`:** HELPER evidence only, from the frozen L `regions()` extracted by AST. It is not an end-to-end result.
- **`reconcile.py --result R --kind proto-l|staged-g --out F`:** observed verdicts against the predictions in the 06.23 notes.
- **`reconstruct.py --root NEW --first R --out F`:** second-root rebuild of proto-l, plus representative cases and byte-identity checks.

## Suggested independent Prime probes (not run by me)
1. Hand-edit an identity manifest with `"dependencies": "G"`. **Expect exit 2.**
2. In a fresh room, rename a recorded N7 `intake.json` and change an artifact. Read with the baseline: **expect exit 0 / stale false (the defect).**
3. Run F1b on proto-l, then compare it with `helper-regions-run01.json`.
