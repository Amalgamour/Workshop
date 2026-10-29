# RUN-GUIDE — a disposable Prime bench trial (rules 2)

For: the Director, the separate Codex bench coordinator and, optionally, a separate collector.
Tool: `labs/prime-bench-pass01/prime_bench.py`. This replaces the 05.01 guide, which stays as the rules-1 record.
This guide authorizes nothing. The harness makes no model call and launches no session; people do that by hand.

## What the Director decides first
These choices remain open in 0414.bench/01.002.md:
1. Which models and effort labels to use, how many pairs, and the spending.
2. The session surface. It must start a **fresh** session with no earlier context and **confine** it to one candidate folder, so the session cannot read lib-build (where the keys live), the trial's run folders or another candidate. If it cannot, declare that honestly; those runs are then reported as not clean.
3. Prime's N7NN investigation page and pass, and a reserved member for the coordinator's return.
4. Whether to use a separate collector. This is optional extra isolation, not a required role.

## Files the coordinator writes before sealing
- **`investigation.json`** (`prime-bench-investigation/1`): the page, pass and question; every Director reply kept **exactly**, with its source path and sha256; the source references; and the coordinator's label.
- **`plan.json`** (`prime-bench-plan/1`), with these keys:
  - `trial_id`, for example `t0001`;
  - `investigation_sha256`;
  - `capabilities`, the four declarations;
  - `allowed_differences`, which must be exactly `["PROMPT.md#tools-paragraph-and-run-id", "support/prime_review.py", "support/README.md", "support/CONTRACT.md"]`;
  - `preparation`: `owner`, `reusable_setup_minutes`, `per_run_setup_minutes` (null if unknown), and `amortization` (`not-amortized` or `equal-split-over-planned-runs`);
  - `runs`: one object per run with `run_id`, `pair_id`, `case_id`, `condition`, `order`, `model_label` and `effort_label`.

  Each pair is one case with one baseline run and one assisted run, and identical labels. Orders run from 1 to N. Balance them so that half the pairs launch assisted first.

## Steps
1. **Check the bench:** `python -B labs/prime-bench-pass01/prime_bench.py validate`. It must print `valid` and the bench version.
2. **Seal the whole trial at once,** before any answer exists:
   ```text
   python -B labs/prime-bench-pass01/prime_bench.py seal --plan D:\bench-trials\plan.json --investigation D:\bench-trials\investigation.json --dest D:\bench-trials\t0001
   ```
   This writes `candidates\rNNNN\` (the kits, each with an empty `work\`), `runs\rNNNN\` (run.json and COORDINATOR.md), the plan and investigation copies, and **seal.json**, written last. It prints `seal_sha256`.
3. **Publish the seal digest** to Prime (for example in the investigation notes) before the first launch. Code cannot prove this happened in that order; the record held by someone other than the coordinator is the evidence.
4. **For each run, in planned order,** follow `runs\rNNNN\COORDINATOR.md`:
   1. Run `check-inputs --run-dir …`. It must say `intact`. If it says `drift`, do not repair the kit. Collect the run as failed with the reason, then use `rerun` (step 7).
   2. Open one fresh, confined session on `candidates\rNNNN` and paste `PROMPT.md`. That is the session start.
   3. Give no help.
   4. Save the final message exactly. That is the session stop.
   5. Export the tool log and usage if the surface offers them.
   6. Fill a `prime-bench-costs/1` record. Unknown fields stay null.
5. **Collect** with the exact command in COORDINATOR.md. Use `--label ACTUAL`, pass `--costs`, and give the declared start and finish. A failed or abandoned run is collected with `--status failed|abandoned --reason TEXT`; it stays in the trial. Collect re-runs the input check and the seal check and records both. It never throws the answer away.
6. **Assess after collection.** Do this blind to the condition where possible.
   - An assessor writes a `prime-bench-action-assessment/1` record. It holds one disposition per commitment in the case's `commitments.json` (present, contradicted or absent), and the evidence must be quoted exactly from the response. Then run `actions --run-dir … --record …`.
   - A reviewer may also score the rubric with `review`.
   - Later corrections go in as `event --kind correction`. The original answer never changes.
7. **Repair by new identity only:** `rerun --trial … --supersedes rNNNN --run-id rMMMM --reason TEXT`. The original stays, and the new run is reported as late and never clean. A clean replacement needs a new sealed trial.
8. **Compare** with `compare --trial D:\bench-trials\t0001`. Every planned run appears. Read these sections first: "Trial complete/INCOMPLETE", "Pairs", "Kinds of fact" and "Not clean".
9. **Export** with `export --trial … --dest D:\bench-trials\t0001-export`. Keep the candidate folders until the export is done, because compare rechecks them.

## Where the return lands
1. The coordinator writes `05.NN.return.md` in the export folder from the TEMPLATE, starting with Did, Blocked, Need.
2. Prime reserves a member whose expected outputs are `comparison.md`, `comparison.json` and `seal.json`, in that order.
3. The coordinator runs the two commands in `CAPTURE.txt` from the repository root: capture, then verify. The receipt is custody, not acceptance.
4. Prime places the captured return into the N7NN page as `05.NN.return.md` with the reviewed workflow, then writes `06.NN.review.md`. The harness writes no live page.

## What the harness verifies, and what stays declared
- **Mechanical (verified by code):**
  - delivered bytes against the seal, at four points (seal, before launch, collection, compare);
  - pair parity and baseline reach;
  - the seal's binding of the roster, definitions and hashes;
  - run.json against the seal;
  - record shapes and identities, and that action evidence appears in the response;
  - the seal's own machine clock.
- **Declared:**
  - session times, freshness and confinement;
  - tool events, usage, costs, launch order and cache state;
  - publication of the seal before launch.
- **Supplied judgment:** the rubric scores and the action dispositions.

## What a trial can and cannot say
- **It can say:** for every planned run, what was answered and whether its inputs stayed intact. For each commitment, whether the assessor found it present, contradicted or absent. Which costs are known and which are unknown, and which pairs are readable.
- **It cannot say:** a productivity multiple, a saving, a ranking or a pass score. One trial of fixed synthetic cases is a first slice; repeated balanced runs and unseen cases come first.
- **Self-test data:** the fixture tests and `sample-report.md` are SYNTHETIC. They show the format, not performance.
