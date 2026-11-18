# PRIME-USE — execution proof v2 and harness pass04 (0707/05.25)
**Lab only.**
- **External rooms are explicitly retained** (no system temp).
- **A pass or READY is test evidence,** never approval, selection or release.
- **Automated inspect captures are not Prime's read.**

Run from `D:\Git\lib-build`. Use a NEW rooms path for each run.

## Equipment tests (no app; scripted dummies are labelled)
```bash
python -B labs/freshness-boundary-tests-pass03/test_proof.py
```
```bash
python -B labs/loop-convergence-harness-pass04/test_pass04.py
```
- **14 proof tests.** P01 reproduces Prime's checked-only false positive on the frozen pass02 proof, then shows `verified-pin-check`.
- **17 pass04 tests:** registry, v7 closure, builder side effects, reporter v2.

## Frozen normal commands for the reviewed successor (Prime fills the identity; equipment and expectations unchanged)
**Required input fields** (`harness-inputs/3`, see 05.24 `IDENTITY-TEMPLATE.json` and this CONTRACT):
- `entry`, `workbook_entry`, `open_entry`, `reporter_entry`;
- every executed local file, with its role;
- `candidate_json_sha256`;
- `builder {path, sha256, bytes, args}` (for 06.59: `make_candidate.py` with `--root` appended by the harness);
- optional `loop_door` / `report_door`;
- the six dependency rows (R and W pending) with `review_ref` for accepted rows; `fixture_source`; `judgments`.

```bash
python -B labs/freshness-boundary-tests-pass03/run.py --candidate ROOT --identity IDENTITY.json --rooms D:/librarian/temp/NEW/fbt --out D:/librarian/temp/NEW/fbt.json
```
```bash
python -B labs/loop-convergence-harness-pass04/harness.py --candidate ROOT --inputs IDENTITY.json --rooms D:/librarian/temp/NEW/h4 --out D:/librarian/temp/NEW/h4.json
```
- **Read first:** `execution_proof.<role>.class`. Only `executed` lets cases run. Then `binding`, `tamper.corroboration` and `audit_logs`.
- **Then read:** `records[].verdict/observed`, `aggregate.reasons` and `exit_meaning`.
- **Full suites only** (no `--cases`/`--suite`) count. A subset is diagnostic.

## Baselines and the 05.18 cut (as run here)
```bash
python -B labs/loop-convergence-harness-pass01/make_candidate.py --kind proto-l --root D:/librarian/temp/NEW/cand-proto-l
```
- **Identity for the baselines:** `labs/loop-convergence-harness-pass02/inputs/inputs-proto-l.json` (legacy, labelled).
- **The 05.18 cut:** an exact copy of `D:/librarian/temp/prime-morning-1105/candidate` with `evidence/design05.25/fixtures/identity-0518-with-doors.json` (Prime's identity plus the door fields only).

## Suggested independent Prime probes (not run by me)
1. **Reuse Prime's checked-only door probe** with `identity3.execution_proof`. Expect `verified-pin-check`, refused.
2. **Remove the tracer from `PYTHONPATH`** in a probe. Expect `no-audit-evidence`, refused.
3. **Hand pass04 a candidate whose builder writes beside itself.** Expect RC-1 `fail` listing the side effects.
