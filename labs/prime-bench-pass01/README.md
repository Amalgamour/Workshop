# prime-bench-pass01 — bounded Prime benchmark harness (rules 2)

**batches:** `0513.bench-build/05.01.002.md` (rules 1), `0513.bench-build/05.02.md` (rules 2, current)
**contract:** `00.kernel/00.00.10.work/0513.bench-build/evidence/build05.02/CONTRACT.md`
**method:** `00.kernel/00.00.10.work/0414.bench/01.002.md` (read, not changed)
**run guide:** `00.kernel/00.00.10.work/0513.bench-build/evidence/build05.02/RUN-GUIDE.md`
**state:** experimental lab code until Prime reviews it. Standard library only.

This is an instrument for one bounded return-review cycle, run under two conditions:
- `baseline`: ordinary tools;
- `assisted`: the same tools, plus the reviewed `prime_review.py`.

What it does:
- seals a whole trial before any answer exists;
- rechecks the delivered inputs before launch, at collection and at comparison;
- records what a coordinator collected;
- runs labelled string checks;
- binds supplied rubric scores and action dispositions;
- tabulates every planned run.

It does not call a model, start or drive a session, use the network or Git, write a live page, or judge meaning. The eight cases are SYNTHETIC. Its self-tests show that the instrument works, not how any model performs.

## Layout
- `bench.json`: the sealed bench (`prime-bench-rules/2`, revision 2). Its sha256 is the bench version.
- `conditions.json`: the Tools paragraph and support copy list for each condition.
- `measures.json`: the operation unit, the session start and stop events, preparation timing, and the cost fields and units.
- `cases/<case_id>/`: four families, each in variants a and b, all at revision 2.
  - `candidate/`: the only material a tested session sees.
  - `evaluator/key.json`: string checks.
  - `evaluator/rubric.json`: rubric items.
  - `evaluator/commitments.json`: action commitments of kind required-action, hold, prohibited or no-further-edit.
  - `coordinator/meta.json`: family, matched variant, decisive evidence and provenance.

## Commands
```text
python -B prime_bench.py validate [--json]
python -B prime_bench.py manifest
python -B prime_bench.py seal         --plan ABS --investigation ABS --dest ABS-NEW-TRIAL [--json]
python -B prime_bench.py check-inputs --run-dir ABS [--json]
python -B prime_bench.py collect      --run-dir ABS --expect-run rNNNN --expect-condition C --status completed|failed|abandoned \
    [--reason TEXT] --label SYNTHETIC|ACTUAL --session-label TEXT --isolation-used fresh|shared|unknown \
    [--response ABS] [--tool-log ABS] [--tool-events ABS] [--usage ABS] [--costs ABS] [--started ISO] [--finished ISO] [--intervention TEXT] [--json]
python -B prime_bench.py event        --run-dir ABS --kind correction|intervention|note --text TEXT [--attachment ABS] [--json]
python -B prime_bench.py assess       --run-dir ABS [--json]
python -B prime_bench.py review       --run-dir ABS --record ABS [--json]
python -B prime_bench.py actions      --run-dir ABS --record ABS [--json]
python -B prime_bench.py rerun        --trial ABS --supersedes rNNNN --run-id rNNNN --reason TEXT [--json]
python -B prime_bench.py compare      --trial ABS [--json]
python -B prime_bench.py export       --trial ABS --dest ABS-NEW [--json]
python -B -X dev tests/test_prime_bench.py -v
```
Exit codes:
- 0: done;
- 1: bench drift, input drift from `check-inputs`, or a partial write (what was written is kept and listed);
- 2: refused.

## Rules the code enforces
- **One seal before answers.** The plan names every run, pair, case, condition, order and label, plus the allowed differences, the preparation owner and the amortization. `seal` prepares all of them at once. Its seal.json binds:
  - the plan and the investigation;
  - the bench, harness, conditions, measures and support hashes;
  - each case's key, rubric and commitments hashes;
  - every run.json and delivery manifest;
  - the pair parity;
  - the seal's own machine clock.

  The rules-1 `prepare` command is gone.
- **Parity inside a pair, not across variants.** Every file must be byte-identical except the assisted `support/*` copies and the PROMPT.md Tools paragraph and run id. A withheld or edited decisive file refuses the seal. The baseline gets every decisive file.
- **Delivered inputs are rechecked.** `check-inputs`, `collect` and `compare` each recompute the candidate folder against its delivery manifest. They report changed, missing, extra and linked files. Notes under `work/` are ignored.
  - A run with drift keeps its raw response and is never clean.
  - A corrected kit is a new, late run, made by `rerun`. The original stays, and the late run is reported but never clean.
- **The whole roster is compared.**
  - `compare` takes the trial folder, so every planned run is a row: missing and uncollected runs appear.
  - A pair is readable only when both its runs are clean.
  - The trial is complete only when every planned run is collected and every pair is readable.
- **Actions are separate from quotes.** A supplied assessor marks each commitment present, contradicted or absent. Evidence must be an exact substring of the collected response. Code validates only the record and its bindings. String checks and quote preservation are reported separately, under their own labels.
- **Costs keep unknowns.** Each run has a declared costs record. Null fields stay unknown, and the record is shown as incomplete. Preparation, setup and amortization come from the seal.
  - Every value is labelled mechanical, declared, or supplied judgment.
  - Nothing is computed as a ratio, a saving, a ranking or a score.
- **Legacy runs are refused.** A rules-1 run (`prime-bench-run/1`) is refused as `legacy-run` and never counts under rules 2.

## Not proven by code
- When a session started, or that the seal reached Prime before launch.
- Session freshness and confinement.
- The absence of outside help.
- Tool, usage and cost figures.
- Assessor and reviewer judgment.

Hashes show only that bytes are equal when checked. Capture is N1NN `return_capture.py`; `export` only prints the command.
