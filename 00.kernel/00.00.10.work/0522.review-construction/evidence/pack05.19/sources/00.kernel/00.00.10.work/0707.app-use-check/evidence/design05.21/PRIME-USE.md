# PRIME-USE — acceptance harness (0707/05.21)
**Lab only.** Every room is external. **A READY verdict is test evidence, never a selection, approval or release.**

## Rebuild and run the baselines
```bash
python -B labs/loop-convergence-harness-pass01/test_verdict.py
```
```bash
python -B labs/loop-convergence-harness-pass01/make_candidate.py --kind proto-l --root D:/librarian/temp/lch-NEW/cand-proto-l
```
```bash
python -B labs/loop-convergence-harness-pass01/make_candidate.py --kind staged-g --root D:/librarian/temp/lch-NEW/cand-staged-g
```
```bash
python -B labs/loop-convergence-harness-pass01/make_inputs.py --candidate-root D:/librarian/temp/lch-NEW/cand-proto-l --name proto-l --out D:/librarian/temp/lch-NEW/inputs-proto-l.json
```
```bash
python -B labs/loop-convergence-harness-pass01/harness.py --candidate D:/librarian/temp/lch-NEW/cand-proto-l --inputs D:/librarian/temp/lch-NEW/inputs-proto-l.json --rooms D:/librarian/temp/lch-NEW/run-proto-l --out D:/librarian/temp/lch-NEW/proto-l.json
```
```bash
python -B labs/loop-convergence-harness-pass01/demo_hostile.py --candidate D:/librarian/temp/lch-NEW/cand-proto-l --inputs D:/librarian/temp/lch-NEW/inputs-proto-l.json --rooms D:/librarian/temp/lch-NEW/hostile --out D:/librarian/temp/lch-NEW/hostile.json
```

- **A rebuilt candidate has a new `CANDIDATE.json` hash** only if its bytes changed. RC-1 shows identical files, so the manifests in `inputs/` stay valid. Otherwise regenerate the inputs.
- **The repo copies of `inputs/*.json` name the candidates built in this pass.** The harness refuses them against any other root (HX-2).

## Reading a result
- **`ready`, `aggregate.reasons`** (every reason ready is false);
- **per case:** `records[].verdict`, `expected` versus `observed`, and `evidence` (the case room);
- **`<rooms>/<case>-inspect-checkpoint.json`:** what the automated checkpoint stored before publish. It is not a human read.

## Prime-run independent probes (suggested, not run by me)
1. Write your own `inputs` with a pending row filled by hand, and confirm refusal.
2. Add a case to `harness.py` that the baselines should fail, and confirm NOT READY.
3. Rerun ST-1..3 and LR-1..7 against your own fixture page.
