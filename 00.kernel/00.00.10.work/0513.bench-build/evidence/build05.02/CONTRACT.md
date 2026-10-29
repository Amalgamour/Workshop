# CONTRACT — prime-bench-pass01, rules 2 (batch 05.02)

Subject: the method-control correction of labs/prime-bench-pass01/prime_bench.py. Method: 0414.bench/01.002.md. Findings: evidence/prime-review05.01/REVIEW.md F01–F04.
The 05.01 contract (evidence/build05.01/CONTRACT.md) stays as the record of rules 1. Where the two differ, this file governs rules 2. Standard library only. This is a builder contract for a lab and seats no law.

## Unchanged from rules 1
- No model call, session launch, credentials, network, Git or live-page write.
- Strict JSON; absolute, non-UNC paths with no link ancestors; exclusive creates; `partial` (exit 1) keeps and lists what was written.
- Candidate, evaluator and coordinator trees are kept separate. The leakage gate scans for canaries and evaluator bytes.
- Deterministic checks are labelled "deterministic string checks". Reviewer rubric scores are a supplied record.
- Corrections and interventions are append-only events. Raw collected bytes are exact.
- No ratio, saving, ranking, pass score, provider API or subscription-cost conversion.

Exits: 0 done; 1 bench drift or partial; 2 refused.

## Versions
- Rules `prime-bench-rules/2`, bench revision 2, case revision 2.
- Run `prime-bench-run/2`, collection `prime-bench-collection/2`.
- New schemas: plan `prime-bench-plan/1`, seal `prime-bench-seal/1`, amendment `prime-bench-amendment/1`, commitments `prime-bench-commitments/1`, action assessment `prime-bench-action-assessment/1`, measures `prime-bench-measures/1`, costs `prime-bench-costs/1`, input check `prime-bench-input-check/1`, comparison `prime-bench-comparison/2`.
- **Legacy.** A `prime-bench-run/1` folder is refused with code `legacy-run` by every command that reads a run. It is never treated as satisfying rules 2.

## Commands
```text
prime_bench.py validate [--json]
prime_bench.py manifest
prime_bench.py seal         --plan ABS --investigation ABS --dest ABS-NEW-TRIAL [--json]
prime_bench.py check-inputs --run-dir ABS [--json]
prime_bench.py collect      --run-dir ABS --expect-run ID --expect-condition C --status S [--reason T] --label L --session-label T --isolation-used I [--response ABS] [--tool-log ABS] [--tool-events ABS] [--usage ABS] [--costs ABS] [--started ISO] [--finished ISO] [--intervention T] [--json]
prime_bench.py event        --run-dir ABS --kind correction|intervention|note --text T [--attachment ABS] [--json]
prime_bench.py assess       --run-dir ABS [--json]
prime_bench.py review       --run-dir ABS --record ABS [--json]
prime_bench.py actions      --run-dir ABS --record ABS [--json]
prime_bench.py rerun        --trial ABS --supersedes ID --run-id ID --reason T [--json]
prime_bench.py compare      --trial ABS [--json]
prime_bench.py export       --trial ABS --dest ABS-NEW [--json]
```
`prepare` (rules 1) is removed. A trial is prepared only by `seal`.

## Plan
`prime-bench-plan/1` has these keys, exactly:
- `trial_id`, matching `t[0-9]{4}`;
- `investigation_sha256`, which must equal the supplied investigation file;
- `capabilities`: the four declarations from rules 1;
- `allowed_differences`: must equal the harness list exactly, which is `PROMPT.md#tools-paragraph-and-run-id`, then each assisted `support/` path;
- `preparation`: `owner` (label), `reusable_setup_minutes` and `per_run_setup_minutes` (non-negative integer or null), and `amortization`, which is `not-amortized` or `equal-split-over-planned-runs`;
- `runs`.

Each run has `run_id` (`r[0-9]{4}`), `pair_id` (`p[0-9]{2,4}`), `case_id`, `condition`, `order` (integer), `model_label` and `effort_label`.

Rules:
- Run ids are unique, and orders are exactly 1..N.
- Each pair has exactly two runs, of one case: one baseline and one assisted, with equal model and effort labels.
- Every case must exist in the bench.

## seal
1. Validate the bench (drift refuses), the plan and the investigation. The destination is new, outside the repository, under an existing real parent.
2. Build every kit in memory:
   - `PROMPT.md` (fixed template), `TASK.md` and `sources/*`;
   - for assisted, `support/*` re-pinned;
   - an empty `work/` folder for candidate notes.
3. Run the leakage gate on every kit.
4. **Pair parity.** Within each pair:
   - the file sets must differ only by the assisted `support/*` paths;
   - every common file except PROMPT.md must be byte-identical;
   - each PROMPT.md must equal the template rendered with its own run id and condition Tools paragraph.

   Any failure refuses the seal and writes nothing. Variants of one family are not compared.
5. **Baseline reach.** TASK.md and every `sources/*` file must be in the baseline kit; this is recorded per pair.
6. Write `plan.json` and `investigation.json` (exact bytes), `candidates/<run>/`, `runs/<run>/run.json` and `COORDINATOR.md`. Re-read every candidate file, then write `seal.json` last.

`seal.json` binds:
- the plan and investigation sha256;
- the bench version and rules;
- sha256 of prime_bench.py, conditions.json and measures.json, plus the support pins;
- each case's key, rubric and commitments sha256;
- for each run: id, pair, order, case, condition, the run.json sha256 and the delivery manifest sha256;
- each pair's parity result and compared file count;
- the preparation owner, setup and amortization, copied from the plan;
- `seal_started_at` and `sealed_at` (machine UTC), and `preparation_machine_seconds`.

The seal digest is the sha256 of seal.json, and it is printed.

A trial without seal.json is unsealed. Compare and export refuse it. Collect records it.

## run.json (`prime-bench-run/2`)
It records:
- trial id, run id, pair, order, `late`, `supersedes`;
- bench version, investigation sha256 and page/pass;
- case and revision, condition, labels, capabilities;
- candidate folder;
- pins (task, key, rubric, commitments, measures);
- `delivery` (path, sha256 and bytes of every delivered file);
- `working_dir: "work"` and `prepared_at`.

## check-inputs
Read-only. It compares the candidate folder with run.json `delivery` and reports:
- `changed`: different bytes;
- `missing`;
- `extra`: any file or folder outside `work/` that was not delivered;
- `linked`: a symlink, junction or reparse point anywhere in the kit, a hard-link count above 1, or `work/` itself linked;
- `unavailable`: the candidate folder is gone.

The result is `intact` or `drift`. Exit 0 when intact, 1 when drift. Content under `work/` is ignored.

## collect (`prime-bench-collection/2`)
As rules 1, with these differences:
- The run must be `prime-bench-run/2`.
- It records `input_check` (the check above, run at collection) and `seal_check`, without ever refusing on them:
  - `sealed`: listed in seal.json with an equal run.json sha256;
  - `late`: listed in an amendment with an equal sha256;
  - `unsealed`: no seal.json;
  - `mismatch`: otherwise.
- It accepts `--costs` (`prime-bench-costs/1`).
- The raw response is kept whatever the checks say.

## rerun
- The original must be a sealed run of this trial. The new id must be unused in the trial.
- It prepares a fresh kit (same case, condition and labels; `late: true`, `supersedes`), with the same parity and leakage gates against the original's delivery.
- It appends `amendments/NNNN.json` with the reason, the new run.json sha256 and `prepared_at`. The original is never changed.
- A late run is reported but never clean.

## Action commitments
- `evaluator/commitments.json` (`prime-bench-commitments/1`): `case_id`, `revision`, and `items` (`id`, `kind`, `text`). Kind is `required-action`, `hold`, `prohibited` or `no-further-edit`. Each complete case has a `no-further-edit` item.
- `actions` takes `prime-bench-action-assessment/1`: `run_id`, `case_id`, `case_revision`, `commitments_sha256`, `assessor_label`, `blind_to_condition`, `dispositions`, `notes`.
- Each disposition has `commitment`, `status` (`present`, `contradicted` or `absent`) and `evidence`.
  - For present or contradicted, `evidence` must be a non-blank exact substring of the collected response.
  - For absent, `evidence` is null.
- There is exactly one disposition per commitment.
- Identity, revision and commitments sha256 must match the run, else `wrong-identity` or `commitments-changed`.
- The record is stored as exact bytes in `actions.json`. A replay refuses read-only: `already-assessed` when identical, `conflict` when different.
- Code checks structure and bindings only. The dispositions are supplied judgment.

## Measures and costs
`measures.json` (`prime-bench-measures/1`), sealed, fixes:
- the operation unit: one tool invocation, successful or failed, as recorded by the surface;
- session start (the first byte of PROMPT.md sent to the fresh session) and stop (the last byte of its final message);
- preparation timing (the seal command's own machine clock), and setup minutes as declared by the owner;
- the cost fields and their units.

`prime-bench-costs/1` (declared, per run) has these keys, exactly:
- `run_id`, `observer`;
- `launch_order`;
- `tool_operations`, `failed_tool_calls`;
- `request_repairs`, `repair_minutes`;
- `correction_loops`, `correction_minutes`;
- `director_attention_events`, `director_attention_minutes`;
- `cache_state` (`cold`, `warm` or `unknown`);
- `prior_involvement` (text or null).

Counts and minutes are non-negative integers or null. Null and `unknown` mean unknown and are reported as `unknown`, never 0. A record is complete only when it was supplied and no field is unknown.

## compare (`prime-bench-comparison/2`)
Input is the trial folder.
- It refuses when seal.json is missing, its plan or investigation hash differs, any run is `prime-bench-run/1`, or the key, rubric, task or commitments changed after the seal.
- Every planned run is a row; a missing run folder is `missing`, not dropped. Late runs are rows too.
- Input checks run again at compare time.

A run is **clean** only when every one of these holds:
- rules 1 cleanliness;
- seal_check `sealed` at collection and now;
- input check `intact` at collection and now;
- not late;
- its declared start is not before `sealed_at`.

Everything else is listed with reasons.

Reported:
- **Per run.** Deterministic string checks; reviewer rubric scores; action dispositions; declared costs with completeness and missing fields; planned order and declared launch order; elapsed time, tool events and usage. Each value is tagged mechanical or declared.
- **Per pair.** Readable only when both runs are clean, with the reasons otherwise; parity and baseline reach from the seal.
- **Per condition.**
  - Status counts, clean counts, and string-check passes among clean runs.
  - Commitment tallies by kind and status among clean runs with action records.
  - Rubric sums with counts.
  - Cost-complete runs.
- **Trial.** Planned, collected and readable pair counts; the preparation record with its amortization statement; the seal digest.

The report states plainly that a trial with any uncollected or unreadable pair is incomplete.

## export
Input is the trial folder.
- It writes `comparison.md`, `comparison.json`, `seal.json`, `plan.json`, `investigation.json` and `runs/` (every run's records), plus the return TEMPLATE and `CAPTURE.txt`.
- The expected capture outputs are `comparison.md`, `comparison.json` and `seal.json`, in that order.
- It never runs capture.

## What code verifies, and what stays declared
**Code verifies (mechanical):**
- byte equality of delivered inputs against the sealed manifests, at seal, before launch, at collection and at compare;
- pair parity and baseline reach;
- that the seal binds the roster, the definitions and the hashes;
- that run.json matches the seal;
- the schema and bindings of supplied records;
- that action evidence occurs in the response;
- the seal's own machine clock.

**Declared, not proven:**
- when a session actually started, or that the seal was published before it;
- session freshness and confinement;
- absence of external context or coaching;
- tool, usage and cost figures;
- the reviewer's and assessor's judgments.

Hashes do not prove chronology or isolation.
