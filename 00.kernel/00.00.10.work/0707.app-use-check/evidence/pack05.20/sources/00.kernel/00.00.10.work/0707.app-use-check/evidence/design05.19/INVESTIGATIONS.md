# Two bounded hostile investigations (0707/05.19)
**Provenance:** these are MY cases, designed here.
- They are independent of the builders' author cases, NOT independent of my own lab prototype (the 05.18 root builder and adapter), and NOT Prime evidence.
- They ran against FROZEN baseline tools on disposable roots under `D:/librarian/temp/lcd-0719/`.
- "AS-PREDICTED" means the baseline did what I predicted. **It is never a claim that a repair works.**

## I — Source-list capacity seam and preservation of the supplied judgment
**Command:** `python -B labs/loop-convergence-design-pass01/inv1_capacity.py --rooms D:/librarian/temp/lcd-0719/inv1-run02 --out …/inv1-run02.json`. Raw output: `inv1-run01.*` (first run, kept) and `inv1-run02.*`.

| Case | Expected | Observed | Verdict |
|---|---|---|---|
| C1: actual 0512/05.09, Prime's EXACT judgment | complete; record refused `limit sources`; no review; judgment kept | complete, 29 book sources, exit 2 `refused: limit sources`, no `reviews/`, judgment found intact in `failed/…json` | as predicted |
| C2: synthetic N5, K = 21 / 22 / 23 book artifacts | 24 sources record, 25 refuse | 23 → 0; 24 → 0; 25 → 2 `limit sources` | as predicted; **the exact boundary is 24 sources** |
| C3: 40 CODE-root artifacts | not counted; records | 2 sources, exit 0, preliminary | as predicted |
| C4: actual N7 0707/05.17 through v8 | complete, but refused | complete, 26 sources, exit 2 `limit sources` | as predicted. **The capacity seam blocks Colab returns too** |
| C5: actual 0522/05.14 control (lab v8 root) | records (as Prime 06.31) | **incomplete:** `artifact-hash-mismatch` on `app/review-loop-v8.json` and `labs/workbook-review-pass04/workbook.py` | **UNEXPECTED, a finding:** 0522/05.14 declares the staged production files, so a root with the lab adapter at those paths is not faithful |
| C5b: the same, production bytes as evidence, faithful pass03 path | records | complete, 20 sources, exit 0, preliminary | as predicted (`inv1-c5b-run01.*`) |

- **First failure kept:** inv1-run01 crashed in MY helper (a dict used as a key) after C1.

## II — Parsing, first review, render and selection interaction
**Commands:** `inv2_interaction.py --rooms …/inv2-run01` and `inv2b_reporter.py --rooms …/inv2b-run01`.

| Case | Today (frozen baseline) | Required after successors | Observed | Verdict |
|---|---|---|---|---|
| X1: A-01 end-to-end. Manifest line + ` note`, and a self-consistent decoy `artifact-manifest.json,` listing 1 artifact | the decoy is bound; complete; recorded; **published** | intake blocked (Director decision) | decoy bound, 1 artifact, complete, record 0, publish 0 | as predicted; **documented failure** |
| X2: A-02. A refused hash attribution plus a second valid Returned line | the second line is bound; recorded | blocked | submission = 06.15.notes.md, record 0 | as predicted; documented failure |
| X3: the frozen 0521 successor workbook on a Colab N7 book | cannot parse N7 | W combines G with the F overlay | N7NN, incomplete, `submission-not-declared` | as predicted; **composition proof** |
| X4: Colab N7 first review on v8 | custody missing, so preliminary with the cycle not called; preliminary publish CREATES 06.15.review.md; 0521 refuses that | Director question | preliminary, `cycle.called` false, publish 0, target created; the 0521 refusal text is present in the frozen source | as predicted; **lane conflict** |
| X5: static inventory of frozen manifests | — | never repin | 5 manifests declare app/ or pass04 files; 1 declares `app/librarian.py` (0522/05.13) | inventory (bounded: frozen manifests only) |
| X6: a combined dispatcher (reporter hunk + v8 line) with the frozen reporter v3 | reporter refuses | R′ pins the combined bytes | `stop: dependency conflict app/librarian.py … want f1d23d45…`; review-loop still complete | as predicted |
| X7: the frozen reporter on a v8-recorded and published N7 review | not current | R′ observes through W | report exit 1, `stale: true`, core read/recover exit 1 | as predicted. **Reporter parity needs a re-cut, not a re-pin** |

## What this does NOT show
- **No repaired loop:** G and K are pending. I built none of them and claim none.
- **The cycle path with custody** (`cycle-committed`) is not run: no copy book has an N1 descriptor.
- **No concurrency, interruption or AR-01 testing.**
