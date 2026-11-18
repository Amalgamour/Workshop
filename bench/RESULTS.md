# Bench results

Measures 1-4 and 6-9 were computed with `wf-bench` from this branch. Measures 5, 10 and 11 are marked manual, as designed.

The command, run read-only on the dogfood page:

```
CARGO_TARGET_DIR=/workspace/workshop-build/target-wf cargo build --release --manifest-path bench/wf-bench/Cargo.toml
CARGO_TARGET_DIR=/workspace/workshop-build/target-wf /workspace/workshop-build/target-wf/release/wf-bench /workspace/workshop-build/wf-run/pages 90.10.00.0001
```

## Baseline: page 90.10.00.0001 (passes 05.01-05.10)

Source: `/workspace/workshop-build/wf-run/pages/90.10.00.0001/log.jsonl` (85 entries). Plan: `docs/design/PLAN-2026-11-18-core-via-wf.md`, section 4.

```
page: 90.10.00.0001  (85 log entries)
#  Measure                  Value
1  First-try pass rate      3 of 6 (50%)
2  Passes per goal          10 / 6 = 1.7; longest 3 (05.07-05.09)
3  Cards carried            5 of 48 (10%); none carried twice
4  Who caught the fails     0 by commands, 4 by the checker
5  Checker misses           manual: look for "(audit) agree/disagree" in signoff notes (none in this log; baseline not measured)
6  Prime hand steps         5 merges and 5 pin actions in 06 notes; 1 after the last pass is not in the log (manual); 3 judgement call(s): safer reading (signoff 05.01); kept as is (06 entry 46); prime decision (06 entry 70)
7  Questions to you         0 in the log; 1 outside in 06 notes (Q-SA)
8  Observer findings        0 filed with wf; 1 written into a 06 note (entry 70); 0 loops
9  Time per pass            median 10.8 (5.6 to 13.1); builder 6.2; checker 2.7
10 Usage per pass           manual: weekly usage % moved / passes, and / passed passes, from the usage report
11 Fresh-model readiness    manual: give a new model only `wf status`, face 01 and AGENTS.md; score these 5 questions out of 5: goal? next pass? who acts next? what is open? is the page halted?
```

**Did this match the plan's baseline?** Yes, on every number the plan published:

| # | Plan | wf-bench |
|---|---|---|
| 1 | 3 of 6 (50%) | same |
| 2 | 10 / 6 = 1.7; longest 3 (05.07-05.09) | same |
| 3 | 5 of 48 (10%); none carried twice | same |
| 4 | 0 by commands, 4 by the checker | same |
| 5 | no audits recorded; not measured | same (manual) |
| 6 | 6 merges and 6 pin rebuilds (5 in 06 notes, 1 after the last pass); 3 judgement calls (05.01, 05.05, 05.09 halt plan) | same counts. The three calls are pointed at signoff 05.01, 06 entry 46 (the 05.05 "kept as is"), and 06 entry 70 (the 05.09 halt plan). The 6th merge and pin are not in the log; add them by hand as the plan did. |
| 7 | 0 in the log; 1 outside (Q-SA, recorded in 06 note entry 38) | same count and id. Q-SA is also mentioned in later 06 notes; the first record of the ruling is entry 38. |
| 8 | 0 filed with wf; 1 written into a 06 note (halt advice, entry 70); 0 loops | same |
| 9 | median 10.8 (5.6 to 13.1); builder 6.2; checker 2.7 | same |
| 10 | about 0.9 per pass, 1.6 per passed pass (estimate) | manual, not recomputed |
| 11 | not measured (the "halted?" answer is known to be wrong today) | manual, not recomputed |

## BENCH-01 runs

The setup script `bench/bench-01.sh` was run end to end against the pinned `wf` at 8eb1fdb. Part a packed the fixed plan. Part b staged the bad return: a dry-run `wf check` passed both check commands, and left the done-when for the checker to judge. No live builder or checker run is recorded yet. Add a row when one is done.

| Date (EST) | wf version | Part a first try | Part b trap caught | Minutes | Log entries | Usage points | Notes |
|---|---|---|---|---|---|---|---|
| — | — | — | — | — | — | — | no live run yet |
