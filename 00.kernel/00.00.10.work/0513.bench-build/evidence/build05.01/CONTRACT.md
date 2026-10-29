# CONTRACT — prime-bench-pass01

Subject: the bounded Prime benchmark harness for 0513.bench-build/05.01.002. Design: 0414.bench/01.md.
Module: labs/prime-bench-pass01/prime_bench.py. Standard library only. Builder contract for a lab; it seats no law.

## What it is, and is not
It prepares fixed cases into fresh run folders, records what a coordinator collected, checks deterministic evidence, binds a supplied reviewer record, and tabulates runs.
It does not call a model, launch or drive a session, hold credentials, use the network or Git, write a live page, run an app fixture, or decide semantic quality.
It does not reserve, capture or inspect a return. The N1NN tools do that; `export` prints the capture command and does not run it.
Fixture tests use labelled SYNTHETIC responses and demonstrate the instrument only, never model performance.

## Bench version
`bench.json` (`prime-bench/1`) lists, each with sha256 and bytes:
- every case file under `cases/<case_id>/candidate/`, `evaluator/` and `coordinator/`;
- `conditions.json`;
- the support files the assisted condition copies, by repository path.

The bench version is the sha256 of the exact bench.json bytes. `validate` re-hashes every listed file, checks that no unlisted file is present in a case folder, and checks the support pins against the live repository. Any drift is exit 1. A case's revision changes only with a new bench.json.

## Case files
- `candidate/TASK.md` and `candidate/sources/*`: the only case material a tested session sees. No case id, family, variant, key or canary.
- `evaluator/key.json` (`prime-bench-key/1`): `case_id`, `revision`, `canary`, `outcomes` (acceptable outcome labels), `must_mention` (groups of alternatives; each group needs one case-insensitive hit), `must_quote` (exact strings), `must_not` (regular expressions).
- `evaluator/rubric.json` (`prime-bench-rubric/1`): `case_id`, `revision`, `scale` (allowed integer scores), `items` (`id`, `text`).
- `coordinator/meta.json` (`prime-bench-case-meta/1`): `case_id`, `revision`, `family`, `variant`, `matched_with`, `label` SYNTHETIC, `decisive_evidence`, `ambiguity`, `provenance` (repository path, sha256 and the rule each case relies on).

Families: `correction`, `false-completion`, `design-fork`, `complete`. Each has variants `a` and `b`, matched to each other.

## Conditions
`conditions.json` (`prime-bench-conditions/1`). `baseline`: ordinary read, search and command tools inside the candidate folder. `assisted`: the same, plus the copied reviewed prime_review.py (805995a1…) with its README and CONTRACT under `support/`. Task text and sources are byte-identical across conditions. The generated PROMPT.md differs only in its Tools paragraph.

## Commands
Every path argument is absolute, local, not UNC, and has no link, junction or reparse point in itself or any ancestor. JSON input is strict (no duplicate keys, no non-finite numbers, exact keys, size limits).

```text
python -B prime_bench.py validate [--json]
python -B prime_bench.py prepare --investigation ABS --run-id ID --case ID --condition baseline|assisted --model-label TEXT --effort-label TEXT
                                 --fresh-session S --workspace-confined S --tool-log S --usage S --run-dir ABS --candidate-dir ABS [--json]
python -B prime_bench.py collect --run-dir ABS --expect-run ID --expect-condition C --status completed|failed|abandoned [--reason TEXT]
                                 --label SYNTHETIC|ACTUAL --session-label TEXT --isolation-used fresh|shared|unknown
                                 [--response ABS] [--tool-log ABS] [--tool-events ABS] [--usage ABS] [--started ISO] [--finished ISO] [--intervention TEXT] [--json]
python -B prime_bench.py event   --run-dir ABS --kind correction|intervention|note --text TEXT [--attachment ABS] [--json]
python -B prime_bench.py assess  --run-dir ABS [--json]
python -B prime_bench.py review  --run-dir ABS --record ABS [--json]
python -B prime_bench.py compare --run-dir ABS [--run-dir ABS ...] [--json]
python -B prime_bench.py export  --run-dir ABS [...] --investigation ABS --dest ABS
```
S is `supported`, `unsupported` or `unknown`.

Exits: 0 done or a shaped result; 1 bench drift, a deterministic mismatch reported by validate, or a partial write; 2 refused input. No traceback on bad input.

## Investigation record
`prime-bench-investigation/1`: `page` (07NN.slug in 0701–0799), `pass` (05.NN), `question`, `director_replies` (each `reply` kept byte-exact, `source_path`, `source_sha256`), `sources` (path and sha256), `coordinator_label`. `prepare` binds its sha256 into run.json. `compare` and `export` refuse runs bound to different investigations, and `export` refuses an investigation file whose sha256 differs from the runs'.

## prepare
- Run id `^r[0-9]{4}$`. Labels are 1–80 printable characters.
- Run and candidate folders must both be absent, under an existing real parent, outside the repository, and neither inside the other.
- `validate` runs first; drift refuses.
- The candidate folder gets `PROMPT.md`, `TASK.md`, `sources/` and, for assisted only, `support/`. Copied support files are re-hashed against their pins.
- Leakage gate: no canary of any case and no evaluator or coordinator file's bytes may appear in any candidate file. A hit refuses and is reported.
- The run folder gets `COORDINATOR.md` and, written last, `run.json` (`prime-bench-run/1`): run id, bench version, investigation sha256, case id and revision, condition, labels, declared capabilities, candidate folder, key, rubric, task and candidate file pins, and a `prepared_at` UTC clock reading.
- Files are created exclusively. A failure leaves what was written, reports `partial` (exit 1) and lists it. A run folder without run.json is never collected. A retry into an existing folder refuses. Nothing is deleted or resumed.

## collect
- The run folder must hold a valid run.json whose run id and condition equal `--expect-run` and `--expect-condition`; otherwise `wrong-identity`, exit 2.
- A `completed` run needs `--response`. `failed` and `abandoned` need `--reason` and may carry a partial response.
- Response: exact bytes copied, at most 1 MiB. If its first non-blank line is `Run: <id>` for another run, `wrong-identity` refuses. A missing run line is recorded as `identity: missing`.
- Optional raw tool log (exact bytes, 8 MiB), normalized tool events (`prime-bench-tool-event/1` JSONL: `tool`, `at` or null), usage JSON (non-negative integer fields only, `source` text). Missing means `unavailable`.
- `--started` and `--finished` are ISO-8601 with offset, recorded as coordinator-supplied.
- Any canary in the response or raw tool log sets `leakage: true`.
- Written as `collected/` plus `collection.json` (`prime-bench-collection/1`), last. A second collect refuses read-only: `already-collected` when every supplied byte and field is identical, otherwise `conflict`.

## event
Appends `events/NNNN.json` (`prime-bench-event/1`) with kind, text, an optional exact attachment, and the sha256 of collection.json it follows. The original collection is never changed. An `intervention` event makes the run unclean.

## assess (read-only)
Refuses (`key-changed`, exit 2) if the live key, rubric or task differs from the pins in run.json. Otherwise prints `prime-bench-assessment/1`:
- `run_line`: matched or missing;
- `outcome`: the first `Outcome: <label>` line, and whether it is in the key's `outcomes`;
- `must_mention`, `must_quote`, `must_not`: per entry pass or fail;
- `canary_absent`;
- `deterministic_pass`: all of the above pass.

These are string checks. They are not a judgment that the review is right.

## review
Supplied `prime-bench-review/1`: `run_id`, `case_id`, `case_revision`, `rubric_sha256`, `reviewer_label`, `blind_to_condition` (true, false or null), `scores` (exactly one per rubric item, each in the scale), `reviewer_minutes`, `director_attention_events` (null or non-negative), `notes`. Identity, case revision and rubric sha256 must equal run.json, else `wrong-identity` or `rubric-changed`, exit 2. Stored as exact bytes in `review.json`; a second record is `already-reviewed` when identical, otherwise `conflict`.

## compare and what is counted
Refuses mixed bench versions, mixed investigations, a run folder given twice, two folders with one run id, and any key change.
For each run: status, label, condition, labels, clean or the reasons it is not, deterministic results, reviewer scores when supplied, elapsed seconds when both times were supplied, tool-event count when events were supplied, usage fields as supplied, correction and intervention event counts.

A run is **clean** only when: status completed; fresh-session and workspace-confined declared `supported`; isolation used `fresh`; its session label is used by no other run in the comparison; no intervention in collection or events; no leakage; identity matched. Unclean, failed, abandoned and uncollected runs are listed with reasons and counted; they are never dropped.

Counted, exactly:
- runs per condition by status and by clean;
- clean runs whose deterministic checks all pass;
- per rubric item, the number of clean reviewed runs and the sum of their supplied scores;
- elapsed, tool events and usage per run, or `unavailable`.

Not computed: ratios between conditions, time or token savings, rankings, a pass score. A SYNTHETIC label is printed on the report whenever any run is SYNTHETIC.

## export (Colab adapter)
Writes a new folder outside the repository: `comparison.md`, `comparison.json`, `investigation.json` (exact bytes), `runs/<run_id>/` copies of each run's records (run.json, collection.json, collected/, events/, review.json; never the candidate's evaluator material, which it does not have), `05.NN.return.TEMPLATE.md` (Did/Blocked/Need headings left for the coordinator, marked TEMPLATE), and `CAPTURE.txt` with the `return_capture.py capture` command for a Prime-reserved member. It does not run capture, write a live book or name a member. Exclusive creates; partial handling as in prepare.

## Dependencies (pinned, unchanged, not imported)
prime_review.py 805995a1…, its README 44b6b0c5… and the 0512 build CONTRACT 4235ff83… are copied for the assisted condition. return_capture.py 8f3da5c6… and return_inspect.py 947915fe… are named for coordinator custody only. None is modified.

## Limits
- Isolation and confinement are declarations by the coordinator. The harness cannot observe a session.
- Timestamps, usage and tool events are as supplied.
- Deterministic checks are string checks; semantic quality is only a reviewer record.
- Eight synthetic cases cannot establish general productivity; repeated balanced runs and unseen cases are needed first.
- No sandbox is claimed against a same-user race between a check and a write.
