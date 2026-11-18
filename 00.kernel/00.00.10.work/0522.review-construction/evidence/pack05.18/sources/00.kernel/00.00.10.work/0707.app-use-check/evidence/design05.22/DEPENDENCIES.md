# Dependency protocol — harness successor (0707/05.22)
**Schema `harness-inputs/2`.** Writer: `labs/loop-convergence-harness-pass02/make_inputs.py`. Checker: `inputs_check.py` (shapes), then `harness.validate` (bytes).

## Current rows (all `required: true`)
| Id | Role | Status | Evidence the harness checks |
|---|---|---|---|
| G | strict N7 parser (pass05, v9 door) | **accepted** | 3 frozen files; `review_ref` = `0522.review-construction/06.33.md` (debbb405…) |
| L | N7-local prototype over pass04 | **accepted** (a bounded prototype) | 1 frozen file; `review_ref` = `0707.app-use-check/06.20.review.md` (0f547990…) |
| K | source capacity, bound 64 | **pending** | `PENDING`. Requirement: frozen snapshot of 0512/05.11. The live page has drifted, and **I did not read it.** |
| I | N5 copied-book instance binding | **pending** | `PENDING`. Requirement: frozen snapshot of 0522/05.16. The live page has drifted, and **I did not read it.** |
| R | reporter on the combined chain, route `review-report` | **pending** | `PENDING`; not assigned |
| W | combined workbook + door + dispatcher | **pending** | `PENDING`; not built |

## What each pending row blocks (verdict `blocked`, never executed)
| Row | Blocks |
|---|---|
| K | CAP-1, CAP-2, CAP-3, CAP-4 |
| R | RP-1, RP-2 |
| I | IN-2 |
| W | **All readiness.** No baseline candidate is W, and the aggregate lists every pending row as a reason. |

## Replacing a PENDING row (Prime only, after review)
1. **Freeze the reviewed files and the review page in a new pack manifest.**
2. **Edit only that row:**
   - `status: "accepted"`;
   - `files: [{path, sha256, bytes}, …]` from the manifest;
   - `review_ref: {path, sha256, bytes}` of the review page;
   - **for R only:** `interface: {"route": "review-report"}`.
3. **Run `test_shapes.py` and `demo_hostile.py`, then the full suite.**

## The harness refuses (exit 2, before any room exists)
- the collection is not a list, is empty, or a row is missing, unknown or duplicated;
- `required` is not exactly `true`;
- an unknown status;
- an accepted row without files or a `review_ref`;
- any pin that differs from live bytes;
- a pending row with pins or a `review_ref`;
- an accepted R row without the interface.

**The harness never guesses a path or hash, never repins, and never falls back to an older module.**

## Fixture source
- **The pack05.21 source manifest (ee502ce6…),** which is itself frozen in pack05.22. Fixtures come from its snapshots, or from manifest rows verified by hash.
- **A declared artifact at a candidate-owned path is recorded as a collision and never overwritten** (the 05.21 rule, unchanged).
