# RESULTS — 0707/05.25 (all Claude author runs; rooms under D:/librarian/temp/fbt3-0525)

## Equipment (no app; scripted dummies labelled)
| Suite | Result |
|---|---|
| `test_proof.py` (proof v2) | 14/14. **P01:** the frozen pass02 proof says `executed=true` for Prime's checked-only shape (reproduced); v2 says `verified-pin-check`, and the gate refuses it by name. |
| `test_pass04.py` | 17/17: registry, v7 closure, builder side effects, reporter v2 (Prime's three observations) |
| Preserved | fbt1 30, fbt2 26, h2 40/24/29, h3 21. All pass, with files byte-identical to pack05.25. |

## Execution evidence classes (actual runs, audit-traced)
| Candidate | Workbook | Open | Reporter |
|---|---|---|---|
| proto-l | executed (`run_file` of the overlay in the probe's own subprocess) | executed | — |
| staged-g | executed (lab pass05) | — | — |
| 05.18 copy | executed (local `review-loop-convergence-pass02/workbook.py` subprocess) | executed | executed (exec of the local report module) |

**Every `executed` is bound to a pid, the process argv and the probe argv** (`execution_proof.*.binding`).

## Baselines (subset groups; reconciliation vs 05.22 harness and 05.23 freshness)
| Run | Exit | Counts | Reconcile |
|---|---|---|---|
| h4 proto-l (n5, preservation, reconstruction, strict, door-proposed) | 1 | 13 pass, 5 fail, 2 blocked | 16 same, 4 new DD, **0 unexpected** |
| h4 staged-g | 1 | 15 pass, 3 fail, 2 blocked | 16 same, 4 new DD, **0 unexpected** |
| fbt3 proto-l / staged-g (10 cases) | 1 / 1 | as 05.23 | 10/10 same, both |

- **N5-1..3, PR-7, CTX-1 and RC-1 pass on both baselines,** against real successful baselines and real refusals.
- **PR-7** gives `stop: pinned tool hash does not match: <declared workbook>` (exit 2).

## The 05.18 cut (exact copy of Prime's frozen candidate; Prime's identity plus door fields only)
| Suite | Exit | Counts | vs Prime's morning run |
|---|---|---|---|
| fbt3 full (34) | 0 | 32 pass, 1 not-reached (F4, non-required), 1 deferred | 34/34 same |
| h4 full (44 records, 37 required) | 1 | 34 pass, 5 fail, 3 KF-not-reproduced, 2 blocked | 36 same; 4 intended changes; 4 new DD; **0 unexpected** |

**Required non-pass on 05.18 (5):**

| Case | Verdict | Reason |
|---|---|---|
| **N5-2** | fail | A **measured difference against a successful baseline.** On 0522/05.13, whose return declares `app/librarian.py` as an artifact, the baseline reports `artifact-hash-mismatch` / incomplete for the candidate's different dispatcher. The candidate reports complete with no mismatch and does not detect the changed declared artifact (`selection_delta_observed: false`). This is consistent with resolving code-root artifact rows against the canonical repository rather than the candidate root. **Not proven; for Prime and Grok-1 triage.** |
| **CTX-1** | fail | The declared workbook exposes no `build_intake(book, page, pass_id)` hook (0420/06.59). |
| **RC-1** | fail | No declared builder. The 05.18 builder CLI writes under the delivered lab (0522/06.40), so it is **not executed** here. |
| RP-1, RP-2 | blocked | R is pending |

**Intended changes vs the morning run:**
- **N5-1 and N5-3:** fail → pass. The v7 closure was installed (all 18 files added; none present, no collisions), and the baseline succeeded.
- **PR-7:** error → pass. The real dispatcher refuses the altered declared workbook: `workbook pin mismatch`.
- **CTX-1:** error → fail, with the reason above.

**Proposed door diagnostics (not required):**

| Case | Result | Detail |
|---|---|---|
| DD-1 | **fail** | the altered loop door still prepares (exit 0, its code executed); confirms 0522/06.40 |
| DD-2 | pass | missing loop door: `review-loop door is missing` (exit 2) |
| DD-3 | **fail** | altered report door still runs |
| DD-4 | pass | missing report door refused |

**On the baselines,** DD-1 also fails (the v8/v9 doors are not pinned by the dispatcher), and **DD-2 fails with a traceback** (a crash, not a refusal).

## Reconstruction (second root)
- proto-l rebuilt; R0, F1b, N5-1..3, PR-*, CTX-1 and RB-1 verdicts are equal.
- Proof classes are all `executed`.
- 62 preserved rows (earlier labs, inputs, `app/`) show 0 drift; no `app/` file changed after pack05.25.

## First failures (kept)
1. **audit-check run01 (tracer):** the log was written inside the audited root, so the hook re-entered itself, logging its own writes. Fixed with a re-entrancy guard and the log kept outside the root.
2. **tracer v1 detail:** `<frozen …>` pseudo-filenames appeared as root paths, and the Windows Popen argument was a single string. Both are filtered.
