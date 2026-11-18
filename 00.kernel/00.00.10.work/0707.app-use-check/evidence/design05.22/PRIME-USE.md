# PRIME-USE — harness successor (0707/05.22)
**Lab only.** Every room is external. **A READY verdict is test evidence. It is never selection, approval or release.** The inspect checkpoint is not a human read; Prime's actual read stays a separate gate.

## Rebuild from nothing
Run from `D:\Git\lib-build`:
```bash
python -B labs/loop-convergence-harness-pass02/reconstruct.py --root D:/librarian/temp/lch2-NEW/recon --out D:/librarian/temp/lch2-NEW/recon.json
```
This does all of the following:
- rebuilds both baselines with the frozen pass01 builder;
- regenerates the input manifests and requires them to be byte-identical to `inputs/`;
- runs the three unit suites;
- runs strict-n7 on the rebuilt staged-g;
- checks that there were no production writes.

## Harness-unit checks (no app)
```bash
python -B labs/loop-convergence-harness-pass02/test_verdict.py
```
```bash
python -B labs/loop-convergence-harness-pass02/test_shapes.py
```
```bash
python -B labs/loop-convergence-harness-pass02/test_callbacks.py
```
Expected results: 40, 24 and 29 tests. Each script exits 0 only if the count matches and every test passes. `test_callbacks.py` uses **labelled scripted command responses**, so it tests the harness only.

## Full suite on a candidate
```bash
python -B labs/loop-convergence-harness-pass02/harness.py --candidate D:/librarian/temp/lch2-NEW/recon/cand-staged-g --inputs labs/loop-convergence-harness-pass02/inputs/inputs-staged-g.json --rooms D:/librarian/temp/lch2-NEW/run-g --out D:/librarian/temp/lch2-NEW/g.json
```
- **Read** `ready`, `exit_meaning`, `aggregate.scope`, `aggregate.reasons`, `aggregate.coverage_missing`, and per case `expected`, `observed` and `observed.judge_reasons`.
- **`--suite strict-n7`** (or any group list) gives a subset result. It is never READY. It exits 4 or 1.

## Callback probes on a baseline (never readiness; always exit 1)
```bash
python -B labs/loop-convergence-harness-pass02/probe.py --candidate D:/librarian/temp/lch2-NEW/recon/cand-proto-l --inputs labs/loop-convergence-harness-pass02/inputs/inputs-proto-l.json --rooms D:/librarian/temp/lch2-NEW/probe --out D:/librarian/temp/lch2-NEW/probe.json --cases CAP-4,RP-1,RP-2,IN-2
```

## Hostile and reconciliation
```bash
python -B labs/loop-convergence-harness-pass02/demo_hostile.py --proto-l D:/librarian/temp/lch2-NEW/recon/cand-proto-l --staged-g D:/librarian/temp/lch2-NEW/recon/cand-staged-g --rooms D:/librarian/temp/lch2-NEW/hostile --out D:/librarian/temp/lch2-NEW/hostile.json
```
`reconcile.py --old <05.21 result> --new <successor result> --kind proto-l|staged-g --out FILE` classifies every case:
- unchanged;
- revised, under H1, H3 or #04;
- new;
- UNEXPECTED, against expectations written before the run.

## Suggested independent Prime probes (not run by me)
1. Hand-edit `inputs-staged-g.json` with `"dependencies": {"G": …}`. **Expect exit 2.**
2. Write a fake registry or inputs where every row is accepted, and run `--suite strict-n7`. **Expect exit 4, not 0.**
3. Point the ST-2 judge at the 05.21 proto-l observation (`judges.strict`). **Expect fail.**
4. Run `probe.py` on your own fixture copy for IN-2. **Expect "copy reads current" on both baselines.**
