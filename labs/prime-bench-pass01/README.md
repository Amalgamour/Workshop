# prime-bench-pass01 — bounded Prime benchmark harness

**batch:** `00.kernel/00.00.10.work/0513.bench-build/05.01.002.md`
**contract:** `00.kernel/00.00.10.work/0513.bench-build/evidence/build05.01/CONTRACT.md`
**method:** `00.kernel/00.00.10.work/0414.bench/01.md` (read, not changed)
**run guide:** `00.kernel/00.00.10.work/0513.bench-build/evidence/build05.01/RUN-GUIDE.md`
**state:** experimental lab code until Prime reviews it. Standard library only.

An instrument for one bounded return-review cycle, run under two conditions: `baseline` (ordinary tools) and `assisted` (the same, plus the reviewed prime_review.py). It prepares fixed cases into fresh run folders, records what a coordinator collected, runs deterministic string checks, binds a supplied reviewer record, and tabulates runs.

It does not call a model, start or drive a session, use the network or Git, write a live page, or judge semantic quality. The eight cases are SYNTHETIC. Its self-tests show the instrument working, not model performance.

## Layout
- `bench.json`: the sealed bench. Its sha256 is the bench version.
- `conditions.json`: the Tools paragraph and support copy list for each condition.
- `cases/<case_id>/`, for each of the four families (`correction`, `false-completion`, `design-fork`, `complete`) in variants `a` and `b`:
  - `candidate/`: the only material a tested session sees;
  - `evaluator/key.json` and `evaluator/rubric.json`: fixed before any answer;
  - `coordinator/meta.json`: family, matched variant, decisive evidence, ambiguity and rule provenance.

## Commands
```text
python -B prime_bench.py validate [--json]
python -B prime_bench.py manifest
python -B prime_bench.py prepare --investigation ABS --run-id rNNNN --case ID --condition baseline|assisted \
    --model-label TEXT --effort-label TEXT --fresh-session S --workspace-confined S --tool-log S --usage S \
    --run-dir ABS --candidate-dir ABS [--json]
python -B prime_bench.py collect --run-dir ABS --expect-run rNNNN --expect-condition C --status completed|failed|abandoned \
    [--reason TEXT] --label SYNTHETIC|ACTUAL --session-label TEXT --isolation-used fresh|shared|unknown \
    [--response ABS] [--tool-log ABS] [--tool-events ABS] [--usage ABS] [--started ISO] [--finished ISO] [--intervention TEXT] [--json]
python -B prime_bench.py event   --run-dir ABS --kind correction|intervention|note --text TEXT [--attachment ABS] [--json]
python -B prime_bench.py assess  --run-dir ABS [--json]
python -B prime_bench.py review  --run-dir ABS --record ABS [--json]
python -B prime_bench.py compare --run-dir ABS [--run-dir ABS ...] [--json]
python -B prime_bench.py export  --run-dir ABS [...] --investigation ABS --dest ABS [--json]
python -B -X dev tests/test_prime_bench.py -v
```
S is `supported`, `unsupported` or `unknown`. Every path is absolute. Run and candidate folders must be new and outside the repository.

Exits: 0 done; 1 bench drift or a partial write (what was written is kept and listed); 2 refused.

## Rules the code enforces
- **Fixed criteria.** `prepare` pins the key, rubric and task. `assess`, `review` and `compare` refuse when those bytes have changed.
- **Separation.** The candidate folder gets `PROMPT.md`, `TASK.md`, `sources/`, and for assisted only, `support/`. It never gets a case id, family, key, rubric, coordinator note or canary; `prepare` scans for these and refuses on a hit.
- **Equal sources.** Task and sources are byte-identical across conditions. PROMPT.md differs only in its Tools paragraph.
- **Exact collection.** Raw bytes are kept as supplied. Missing usage, times or tool events are `unavailable`, never 0.
- **Identity.**
  - A response naming another run is refused.
  - A mismatched run folder or condition is refused.
  - A second collect or review is a read-only refusal: `already-collected` or `already-reviewed` when identical, `conflict` when different.
  - `compare` refuses mixed bench versions or investigations, and duplicate runs.
- **Clean runs.** A run counts as clean only when all of these hold:
  - it completed;
  - isolation was declared supported and used fresh;
  - no other run shares its session label;
  - there was no intervention and no leakage;
  - its identity matched.

  Everything else stays in the report, with its reasons.
- **Separate events.** Corrections and interventions are separate append-only events. The original collection never changes.

## Not done here
- No ratio, saving, ranking or pass score is computed.
- Isolation, confinement, times, usage and tool events are coordinator declarations, not observations.
- Capture is N1NN `return_capture.py`; `export` only prints the command.
