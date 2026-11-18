# PRIME-USE — explicit-identity test adapters (0707/05.24)
**Lab only.**
- **Rooms are external and explicitly retained** (no system temp directories).
- **A pass or READY is test evidence,** never approval, selection or release.
- **Automated inspect captures are not Prime's read.**

Run from `D:\Git\lib-build`. Use a NEW rooms path for each run.

## Equipment tests (no app)
```bash
python -B labs/freshness-boundary-tests-pass02/test_identity.py
```
```bash
python -B labs/loop-convergence-harness-pass03/test_pass03.py
```
- **26 identity and adapter controls,** using SCRIPTED DUMMY candidates (never an app).
- **21 pass03 checks:** registry preservation, the CLI gate, and the reporter-obligation judge (proposed RP-3).

## Baselines (labelled legacy v2 inputs)
```bash
python -B labs/loop-convergence-harness-pass01/make_candidate.py --kind proto-l --root D:/librarian/temp/fbt2-NEW/cand-proto-l
```
```bash
python -B labs/freshness-boundary-tests-pass02/run.py --candidate D:/librarian/temp/fbt2-NEW/cand-proto-l --identity labs/loop-convergence-harness-pass02/inputs/inputs-proto-l.json --rooms D:/librarian/temp/fbt2-NEW/fbt --out D:/librarian/temp/fbt2-NEW/fbt.json
```
```bash
python -B labs/loop-convergence-harness-pass03/harness.py --candidate D:/librarian/temp/fbt2-NEW/cand-proto-l --inputs labs/loop-convergence-harness-pass02/inputs/inputs-proto-l.json --rooms D:/librarian/temp/fbt2-NEW/h3 --out D:/librarian/temp/fbt2-NEW/h3.json
```
- **Result fields:** `identity_mode`, `workbook_entry`, `execution_proof.*.verdict/evidence`, then the unchanged case records.
- **The proof rooms** are `<rooms>-proof/`: control-1, control-2 and tamper, at one stable path.

## The OLD combined candidate (expected: refused, three ways)
```bash
python -B labs/freshness-boundary-tests-pass02/demo_old_combined.py --rooms D:/librarian/temp/fbt2-NEW/old --out D:/librarian/temp/fbt2-NEW/old.json
```
It reads Prime's frozen copy `D:/librarian/temp/prime-night-0517-0723/combined-copy` without changing it.

## The Grok-1 successor (later, unchanged equipment and expectations)
1. **Freeze the successor root and fill `IDENTITY-TEMPLATE.json`** (harness-inputs/3; R and W stay pending until reviewed).
2. **Run `freshness-boundary-tests-pass02/run.py` and `loop-convergence-harness-pass03/harness.py`** with `--identity` / `--inputs` pointing at that file. Run the full suites (no `--cases`/`--suite`).
3. **Expectations:**
   - the execution proof says `executed` for the workbook (and open/reporter if declared);
   - all 32 freshness and 37 convergence required cases pass;
   - C4 executes, because `kind` is `combined`.
   - **A refusal or any non-pass is the result. Do not adjust expectations.**

## Suggested independent Prime probes (not run by me)
1. Build a v3 identity whose `workbook_entry` names an extra copied file that the dispatcher never imports. **Expect a DECOY refusal (exit 2).**
2. Hand a v2 input for any non-baseline root. **Expect a refusal naming the legacy limit.**
3. Make a probe nondeterministic (e.g. a time-stamped output). **Expect INCONCLUSIVE and a refusal.**
