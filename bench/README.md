# WF bench

This folder is the scorecard for the workflow tool (`wf`).

It lives on the `bench` branch so we can run the same checks later, on new versions of `wf`, and compare.

Matthew is not expected to run these commands. The steps are here so Prima and later models can.

## What it is

A page of work with `wf` leaves a log. The bench reads that log and scores how well `wf` (and the team using it) did.

There are 11 measures. Most come from the log. Three need a person.

There is also one fixed practice task, **BENCH-01**. It uses the car-steering example that ships with the kit. Run it on each new `wf` version and add a row to `RESULTS.md`.

## The 11 measures

"Fresh goal" means a pass that does not follow a failed pass.

| # | Measure | How it is computed |
|---|---|---|
| 1 | First-try pass rate | Fresh goals that passed, over all fresh goals. |
| 2 | Passes per goal | All signed-off passes, over fresh goals. Also the longest run of a fail plus its fix-ups. |
| 3 | Cards carried | Cards marked `carried` at signoff, over all cards. "Carried twice" means the same card id was carried on two signoffs in a row (a loop). |
| 4 | Who caught the fails | Failed checks where a listed check command failed, versus failed checks where the commands passed and the checker still failed it. |
| 5 | Checker misses | **Manual.** Prima audits 1 pass in 3 and writes `(audit) agree` or `(audit) disagree` in the signoff note. The tool only reports whether those notes exist. |
| 6 | Prime hand steps | Completed merges and pin-rebuilds mentioned in 06 notes (`merged by Prime`, `merged and pushed`, `merged (`, `pin rebuilt`, `pinned binary`). A merge after the last pass is not in the log: count it by hand. Judgement calls are notes that say `Prime decision`, `safer reading`, or `kept as is`. |
| 7 | Questions to you | `elevate` entries in the log. Plus question ids like `Q-SA` written into 06 notes (questions asked outside `wf`). |
| 8 | Observer findings | `observe` entries in the log. 06 notes that file a finding (`Observer:`, `Observer (`, or `wf observe`), not later notes that only refer back. Loops as in measure 3. |
| 9 | Time per pass | Pack to close, in minutes, median and range. Also builder (claim to return) and checker (return to check), medians. |
| 10 | Usage per pass | **Manual.** Weekly usage % moved, divided by passes, and by passed passes, from the usage report. |
| 11 | Fresh-model readiness | **Manual.** Give a new model only `wf status`, face 01 and `AGENTS.md`. Score 5 questions out of 5: goal? next pass? who acts next? what is open? is the page halted? |

The first baseline is page `90.10.00.0001` (the ten dogfood passes). See `RESULTS.md`.

## Run the measures on any page

From the kit root (this worktree), using the existing build folder so the disk stays small:

```
CARGO_TARGET_DIR=/workspace/workshop-build/target-wf cargo build --release --manifest-path bench/wf-bench/Cargo.toml
CARGO_TARGET_DIR=/workspace/workshop-build/target-wf /workspace/workshop-build/target-wf/release/wf-bench /path/to/pages 90.10.00.0001
```

`wf-bench` does not change the `wf` crate. It only reads `<pages-dir>/<page>/log.jsonl`.

On another machine you can drop `CARGO_TARGET_DIR` and run `cargo build --release --manifest-path bench/wf-bench/Cargo.toml`, then `./target/release/wf-bench <pages-dir> <page>`.

## Re-run BENCH-01 on a new wf version

1. On this `bench` branch only, merge the new `workflow` tip in (never merge into `main` or `workflow`).
2. Rebuild `wf` from that tip.
3. Run the setup script with the new binary:

```
bench/bench-01.sh /path/to/wf
```

It makes a fresh temp copy of the car-steering example and prints two folders.

4. **Part a, a builder pass.** The plan is fixed: "clamp the angle at -30 and +30, and test both edges". Point a builder at the part-a folder. They claim pass 05.01 and do the job.
5. **Part b, a checker trap.** A ready-made bad return clamps only +30. Its check commands pass, but its done-when (both edges) fails. Point a checker at the part-b folder. They must fail it.
6. Record in `RESULTS.md`: passed first try (yes/no), trap caught (yes/no), minutes, log entries, usage points, and the `wf-bench` table for the part-a page. Compare to earlier rows.

The trap files are in `bench/BENCH-01/`. The script stages them; you do not apply them by hand.

## What this branch is for

Keep the harness here. Add new reference tasks as `BENCH-02` and so on. Add a results row after each run. Do not put Workshop core work on this branch.
