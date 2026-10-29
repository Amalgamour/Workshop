# Sample report — SYNTHETIC (rules 2)

Produced on 2026-10-29 by `prime_bench.py export` from one disposable SYNTHETIC trial, made through the CLI outside the repository: 8 sealed pairs (16 runs) and one late rerun. No model was called. All responses, times, costs, assessor dispositions and reviewer scores are fixture values.

What the trial deliberately contains:
- a hint planted in one assisted kit after the seal (Prime's F01 probe). It is kept, and the run is not clean.
- the 0701 C02 specimens: B, a correct quote followed by a contradicting action (baseline r0009), and C, a faithful paraphrase (assisted r0010).
- an unneeded edit on a complete case (assisted r0016).
- a wrong outcome (baseline r0005).
- one failed run, one late rerun, two runs without a costs record, and three runs with unknown cost fields.

Wrong answers are split two per condition. The figures show the format and the counting rules, not performance.

Below is `comparison.md` verbatim (sha256 8913ceaf9e86aab5a039d3b01fe6baa012d27da379b411081671c46fd27e6ca4).

---

# Prime bench comparison

**SYNTHETIC.** At least one run is labelled SYNTHETIC. These records demonstrate the harness and its report format. They show no model performance.

Rules `prime-bench-rules/2`. Bench version `ba17e1218eb27316d209784d51ba8e236a80967bdd6faa29b64f7161d82146db`. Investigation 0790.bench-trial pass 05.01. Trial t0001, seal `042b84d0c1e03e5349850fbcb3a6c3dafdcba1e6b5c54f2bce4dd400fbf15314`, sealed 2026-10-29T22:07:49Z (machine clock).

**Trial INCOMPLETE.** Planned runs 16; collected 16; late runs 1 (reported, never clean). Pairs 8; readable 6; assisted first in 4. A trial is complete only when every planned run is collected and every pair is readable.

## Kinds of fact
- **mechanical**: computed by the harness: hashes, pair parity, baseline reach, input checks, seal binding, record bindings, string checks, the seal's own clock.
- **declared**: supplied by people: session times, isolation and confinement, tool events, usage, costs, launch order, cache state.
- **supplied judgment**: rubric scores and action dispositions. Code checked only their shape, identity and that action evidence occurs in the response.
- Hashes do not prove when a session started or what else it could see.

## What is counted
- A run is clean only when it was sealed before answers, its inputs were intact at collection and at compare, it completed, isolation was declared supported and used fresh, its session was used by no other run, there was no intervention or leakage, its run line matched, and its declared start is not before the seal.
- A pair is readable only when both its runs are clean.
- String checks: run line, outcome label, mentions, exact quotes, forbidden patterns, canary. They are not a semantic or action verdict. Quote preservation is reported on its own.
- Action commitments: per kind, the count of present, contradicted and absent dispositions among clean runs with a supplied record. No universal score.
- Unknown values are shown as `unknown`, never 0. A cost record is complete only when every field is known.

## Pairs

| pair | case | baseline | assisted | parity | baseline reach | readable |
|---|---|---|---|---|---|---|
| p01 | correction-a | r0001 | r0002 | identical-except-allowed | all decisive files delivered to baseline | yes |
| p02 | correction-b | r0003 | r0004 | identical-except-allowed | all decisive files delivered to baseline | yes |
| p03 | false-completion-a | r0005 | r0006 | identical-except-allowed | all decisive files delivered to baseline | yes |
| p04 | false-completion-b | r0007 | r0008 | identical-except-allowed | all decisive files delivered to baseline | yes |
| p05 | design-fork-a | r0009 | r0010 | identical-except-allowed | all decisive files delivered to baseline | no: r0010 not clean |
| p06 | design-fork-b | r0011 | r0012 | identical-except-allowed | all decisive files delivered to baseline | no: r0012 not clean |
| p07 | complete-a | r0013 | r0014 | identical-except-allowed | all decisive files delivered to baseline | yes |
| p08 | complete-b | r0015 | r0016 | identical-except-allowed | all decisive files delivered to baseline | yes |

## Runs

| run | pair | order (plan / launch) | case | condition | label | status | clean | inputs (collect / now) | outcome | string checks | quotes | actions | review | elapsed s | costs |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| r0001 | p01 | 1 / 1 | correction-a r2 | baseline | SYNTHETIC | completed | yes | intact / intact | continue | pass | n/a | unknown | R1=1, R2=1, R3=1, R4=1, R5=1 | 360 | complete |
| r0002 | p01 | 2 / 2 | correction-a r2 | assisted | SYNTHETIC | completed | yes | intact / intact | continue | pass | n/a | unknown | R1=1, R2=1, R3=1, R4=1, R5=1 | 420 | complete |
| r0004 | p02 | 3 / unknown | correction-b r2 | assisted | SYNTHETIC | completed | yes | intact / intact | continue | pass | n/a | unknown | unknown | 480 | not supplied |
| r0003 | p02 | 4 / unknown | correction-b r2 | baseline | SYNTHETIC | completed | yes | intact / intact | continue | pass | n/a | unknown | unknown | 300 | not supplied |
| r0005 | p03 | 5 / 5 | false-completion-a r2 | baseline | SYNTHETIC | completed | yes | intact / intact | complete | fail | n/a | unknown | unknown | 360 | complete |
| r0006 | p03 | 6 / 6 | false-completion-a r2 | assisted | SYNTHETIC | completed | yes | intact / intact | continue | pass | n/a | unknown | unknown | 420 | complete |
| r0008 | p04 | 7 / 7 | false-completion-b r2 | assisted | SYNTHETIC | completed | yes | intact / intact | continue | pass | n/a | unknown | unknown | 480 | complete |
| r0007 | p04 | 8 / 8 | false-completion-b r2 | baseline | SYNTHETIC | completed | yes | intact / intact | continue | pass | n/a | unknown | unknown | 300 | incomplete: repair_minutes, cache_state |
| r0009 | p05 | 9 / 9 | design-fork-a r2 | baseline | SYNTHETIC | completed | yes | intact / intact | director-input | pass | kept | A1=contradicted, A2=contradicted, A3=absent | unknown | 360 | complete |
| r0010 | p05 | 10 / 10 | design-fork-a r2 | assisted | SYNTHETIC | completed | no | drift / drift | director-input | fail | not kept | A1=present, A2=present, A3=present | unknown | 420 | complete |
| r0012 | p06 | 11 / 11 | design-fork-b r2 | assisted | SYNTHETIC | failed | no | intact / intact | unknown | fail | n/a | unknown | unknown | unknown | complete |
| r0011 | p06 | 12 / 12 | design-fork-b r2 | baseline | SYNTHETIC | completed | yes | intact / intact | director-input | pass | kept | unknown | unknown | 300 | incomplete: repair_minutes, cache_state |
| r0013 | p07 | 13 / 13 | complete-a r2 | baseline | SYNTHETIC | completed | yes | intact / intact | complete | pass | n/a | unknown | unknown | 360 | complete |
| r0014 | p07 | 14 / 14 | complete-a r2 | assisted | SYNTHETIC | completed | yes | intact / intact | complete | pass | n/a | unknown | unknown | 420 | complete |
| r0016 | p08 | 15 / 15 | complete-b r2 | assisted | SYNTHETIC | completed | yes | intact / intact | complete | pass | n/a | A1=contradicted, A2=contradicted | unknown | 480 | complete |
| r0015 | p08 | 16 / 16 | complete-b r2 | baseline | SYNTHETIC | completed | yes | intact / intact | complete | pass | n/a | A1=present, A2=present | unknown | 300 | incomplete: repair_minutes, cache_state |
| r0910 (late) | p05 | 10 / unknown | design-fork-a r2 | assisted | SYNTHETIC | completed | no | intact / intact | director-input | pass | kept | A1=present, A2=present, A3=present | unknown | unknown | not supplied |

## Costs (declared unless marked)

| run | tool ops | failed calls | repairs (n / min) | corrections (n / min) | Director (n / min) | cache | tool events | usage |
|---|---|---|---|---|---|---|---|---|
| r0001 | 6 | 1 | 0 / 0 | 0 / 0 | 0 / 0 | cold | unknown | unknown |
| r0002 | 7 | 0 | 0 / 0 | 0 / 0 | 0 / 0 | cold | unknown | unknown |
| r0004 | unknown | unknown | unknown / unknown | unknown / unknown | unknown / unknown | unknown | unknown | unknown |
| r0003 | unknown | unknown | unknown / unknown | unknown / unknown | unknown / unknown | unknown | unknown | unknown |
| r0005 | 7 | 1 | 0 / 0 | 0 / 0 | 0 / 0 | cold | unknown | unknown |
| r0006 | 5 | 0 | 0 / 0 | 0 / 0 | 0 / 0 | cold | unknown | unknown |
| r0008 | 6 | 1 | 0 / 0 | 0 / 0 | 0 / 0 | cold | unknown | unknown |
| r0007 | 7 | 0 | 0 / unknown | 0 / 0 | 0 / 0 | unknown | unknown | unknown |
| r0009 | 5 | 1 | 0 / 0 | 0 / 0 | 0 / 0 | cold | unknown | unknown |
| r0010 | 6 | 0 | 0 / 0 | 0 / 0 | 0 / 0 | cold | unknown | unknown |
| r0012 | 7 | 1 | 0 / 0 | 0 / 0 | 0 / 0 | cold | unknown | unknown |
| r0011 | 5 | 0 | 0 / unknown | 0 / 0 | 0 / 0 | unknown | unknown | unknown |
| r0013 | 6 | 1 | 0 / 0 | 0 / 0 | 0 / 0 | cold | unknown | unknown |
| r0014 | 7 | 0 | 0 / 0 | 0 / 0 | 0 / 0 | cold | unknown | unknown |
| r0016 | 5 | 1 | 0 / 0 | 0 / 0 | 0 / 0 | cold | unknown | unknown |
| r0015 | 6 | 0 | 0 / unknown | 0 / 0 | 0 / 0 | unknown | unknown | unknown |
| r0910 | unknown | unknown | unknown / unknown | unknown / unknown | unknown / unknown | unknown | unknown | unknown |

Preparation: owner SYNTHETIC coordinator; seal took 0.392 s (mechanical); reusable setup 40 min and per-run setup 2 min (declared); amortization equal-split-over-planned-runs, reusable share per planned run 2.5 min.

## Counts by condition (planned runs; late runs excluded)

- **baseline**: 8 planned (completed 8, failed 0, abandoned 0, uncollected 0, missing 0); clean 8; clean with string checks passing 7; clean with an action record 2; cost records complete 4.
  - hold: present 0, contradicted 1, absent 0.
  - no-further-edit: present 1, contradicted 0, absent 0.
  - prohibited: present 1, contradicted 1, absent 0.
  - required-action: present 0, contradicted 0, absent 1.
  - rubric R1: 1 clean reviewed runs, score sum 1.
  - rubric R2: 1 clean reviewed runs, score sum 1.
  - rubric R3: 1 clean reviewed runs, score sum 1.
  - rubric R4: 1 clean reviewed runs, score sum 1.
  - rubric R5: 1 clean reviewed runs, score sum 1.
- **assisted**: 8 planned (completed 7, failed 1, abandoned 0, uncollected 0, missing 0); clean 6; clean with string checks passing 6; clean with an action record 1; cost records complete 7.
  - no-further-edit: present 0, contradicted 1, absent 0.
  - prohibited: present 0, contradicted 1, absent 0.
  - rubric R1: 1 clean reviewed runs, score sum 1.
  - rubric R2: 1 clean reviewed runs, score sum 1.
  - rubric R3: 1 clean reviewed runs, score sum 1.
  - rubric R4: 1 clean reviewed runs, score sum 1.
  - rubric R5: 1 clean reviewed runs, score sum 1.

## Not clean, failed, late or missing (kept, not dropped)

- r0010 (assisted): input drift at collection: changed: sources/consumer-note.md
- r0012 (assisted): failed
- r0910 (assisted): late-prepared after the seal (supersedes r0010)

## Corrections and interventions (separate from the original runs)

- r0001: corrections 1, interventions 0

## Not computed

No ratio between conditions, no time or token saving, no ranking, no pass score and no provider or subscription cost conversion. One trial of fixed cases cannot establish general productivity.
