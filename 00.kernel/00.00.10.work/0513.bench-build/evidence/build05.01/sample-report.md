# Sample report — SYNTHETIC

Produced on 2026-10-29 by `prime_bench.py export` from 16 SYNTHETIC fixture runs (8 cases x 2 conditions) made through the CLI outside the repository. No model was called. Wrong answers were placed in two baseline and two assisted runs. One run is a deliberate failure, and two runs deliberately share a session. Both reviews are identical fixture scores. The figures show the format and the counting rules, not performance.

Below is `comparison.md` verbatim (sha256 8fb0eafe1d5fcf5cbf9d67246de59de7e2ed519b8100c10aeaacb55765602467).

---

# Prime bench comparison

**SYNTHETIC.** At least one run is labelled SYNTHETIC. These records demonstrate the harness and its report format. They show no model performance.

Bench version `f00c6f29f35edd27465b2bbf5e4023323d8f028c4c6d8291ef1fe85db39fe9d1`. Investigation 0790.bench-trial pass 05.01 (`41b39810730908aa8476a36c2281c6d6c16d085b0d6aee4fbb8d125ef89500a0`). Runs: 16.

## What is counted
- A run is clean only when it completed, fresh-session and workspace-confined were declared supported, the session was fresh and used by no other run here, no intervention, no evaluator leakage, and the run line matched.
- Deterministic pass: the run line, the outcome label, the decisive mentions, the exact quotes, the forbidden claims and the canary, all as string checks. It is not a judgment that the review is right.
- Reviewer scores are supplied records, summed per rubric item over clean reviewed runs, with the count.
- Elapsed time uses coordinator-supplied start and finish. Tool events and usage are as supplied. Missing values are `unavailable`, never 0.

## Runs

| run | case | family/variant | condition | model / effort | label | status | clean | outcome | deterministic | review | elapsed s | tool events | usage |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| r0001 | correction-a r1 | correction/a | baseline | SYNTHETIC-fixture / n/a | SYNTHETIC | completed | yes | continue | pass | R1=1, R2=1, R3=1, R4=1, R5=1 | 360 | unavailable | unavailable |
| r0002 | correction-a r1 | correction/a | assisted | SYNTHETIC-fixture / n/a | SYNTHETIC | completed | yes | complete | fail | R1=1, R2=1, R3=1, R4=1, R5=1 | 360 | unavailable | unavailable |
| r0003 | correction-b r1 | correction/b | baseline | SYNTHETIC-fixture / n/a | SYNTHETIC | completed | yes | continue | pass | unavailable | unavailable | unavailable | unavailable |
| r0004 | correction-b r1 | correction/b | assisted | SYNTHETIC-fixture / n/a | SYNTHETIC | completed | yes | continue | pass | unavailable | unavailable | unavailable | unavailable |
| r0005 | false-completion-a r1 | false-completion/a | baseline | SYNTHETIC-fixture / n/a | SYNTHETIC | completed | yes | complete | fail | unavailable | unavailable | unavailable | unavailable |
| r0006 | false-completion-a r1 | false-completion/a | assisted | SYNTHETIC-fixture / n/a | SYNTHETIC | completed | yes | continue | pass | unavailable | unavailable | unavailable | unavailable |
| r0007 | false-completion-b r1 | false-completion/b | baseline | SYNTHETIC-fixture / n/a | SYNTHETIC | completed | yes | continue | pass | unavailable | unavailable | unavailable | unavailable |
| r0008 | false-completion-b r1 | false-completion/b | assisted | SYNTHETIC-fixture / n/a | SYNTHETIC | completed | yes | continue | pass | unavailable | unavailable | unavailable | unavailable |
| r0009 | design-fork-a r1 | design-fork/a | baseline | SYNTHETIC-fixture / n/a | SYNTHETIC | completed | yes | director-input | pass | unavailable | unavailable | unavailable | unavailable |
| r0010 | design-fork-a r1 | design-fork/a | assisted | SYNTHETIC-fixture / n/a | SYNTHETIC | completed | yes | continue | fail | unavailable | unavailable | unavailable | unavailable |
| r0011 | design-fork-b r1 | design-fork/b | baseline | SYNTHETIC-fixture / n/a | SYNTHETIC | completed | yes | director-input | pass | unavailable | unavailable | unavailable | unavailable |
| r0012 | design-fork-b r1 | design-fork/b | assisted | SYNTHETIC-fixture / n/a | SYNTHETIC | failed | no | unavailable | fail | unavailable | unavailable | unavailable | unavailable |
| r0013 | complete-a r1 | complete/a | baseline | SYNTHETIC-fixture / n/a | SYNTHETIC | completed | yes | complete | pass | unavailable | unavailable | unavailable | unavailable |
| r0014 | complete-a r1 | complete/a | assisted | SYNTHETIC-fixture / n/a | SYNTHETIC | completed | yes | complete | pass | unavailable | unavailable | unavailable | unavailable |
| r0015 | complete-b r1 | complete/b | baseline | SYNTHETIC-fixture / n/a | SYNTHETIC | completed | no | continue | fail | unavailable | unavailable | unavailable | unavailable |
| r0016 | complete-b r1 | complete/b | assisted | SYNTHETIC-fixture / n/a | SYNTHETIC | completed | no | complete | pass | unavailable | unavailable | unavailable | unavailable |

## Counts by condition

- **baseline**: 8 runs (completed 8, failed 0, abandoned 0, uncollected 0); clean 7; clean with deterministic pass 6.
  - R1: 1 clean reviewed runs, score sum 1.
  - R2: 1 clean reviewed runs, score sum 1.
  - R3: 1 clean reviewed runs, score sum 1.
  - R4: 1 clean reviewed runs, score sum 1.
  - R5: 1 clean reviewed runs, score sum 1.
- **assisted**: 8 runs (completed 7, failed 1, abandoned 0, uncollected 0); clean 6; clean with deterministic pass 4.
  - R1: 1 clean reviewed runs, score sum 1.
  - R2: 1 clean reviewed runs, score sum 1.
  - R3: 1 clean reviewed runs, score sum 1.
  - R4: 1 clean reviewed runs, score sum 1.
  - R5: 1 clean reviewed runs, score sum 1.

## Not clean, failed or uncollected (kept, not dropped)

- r0012 (assisted): failed
- r0015 (baseline): shared session: r0015, r0016
- r0016 (assisted): shared session: r0015, r0016

## Corrections and interventions (separate from the original runs)

- r0001: corrections 1, interventions 0

## Not computed

No ratio between conditions, no time or token saving, no ranking and no pass score. A small fixed bench cannot establish general productivity.
