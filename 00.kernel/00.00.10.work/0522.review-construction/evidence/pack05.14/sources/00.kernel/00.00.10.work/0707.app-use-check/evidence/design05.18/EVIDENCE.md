# Commands, evidence and provenance (0707/05.18)
**Labels:**
- **AT** = author test (mine);
- **KR** = known-failure reproduction;
- **ADAPTED** = a historical author case run through the documented adapter;
- **REVISED** = an expectation changed by K1;
- **FI** = lab fault injection.

All runs are mine, in new processes, on disposable roots. **No independent probe ran.** Prime's future independent probes are listed at the end.

| Run (evidence) | Command (from `D:\Git\lib-build`) | Result | Label |
|---|---|---|---|
| smoke01 / 02 / 03 (notes only) | `rie.py --room …/smoke0N --fixture n7-0515`, then `<root>/app/librarian.py review-loop prepare` | 01: builder crash (my N5 pattern on an N7 line). 02: a patch script mangled by the heredoc. 03: complete, 30 rows | first failures kept |
| matrix01.json | `matrix.py --rooms …/matrix01` | N5 0522: C incomplete (dispatcher artifact); the others as matrix02 | AT, first run kept |
| matrix02.json | `matrix.py --rooms …/matrix02` (adds D, the door-direct step) | N5 parity on the same state; 0522 selection coupling; N7 26/26 and 33/33 | AT + KR (W, B) |
| cases-v2-run01.json | `RIE_CANDIDATE_ROOT=…/matrix02/n5-0512 cases/tests/test_n7v2.py` | 12/12 against the candidate pass04 | AT + KR |
| cases-compat17-run01.json | same env, `cases/compat17/tests/test_n7.py` | 16/17; G7 REVISED | ADAPTED |
| reconciliation.json | (derived) | per-case PRESERVED or REVISED; G7: 1 sub-assertion preserved, 2 revised | — |
| ctx01.json / ctx02.json | `ctx_test.py --room …/ctx0N` | X1–X4 pass (ctx01 had an and/or slip in X4, fixed in 02) | AT + FI |
| life01.json | `lifecycle.py --rooms …/life01` | L1–L4 as in CONTRACT; idempotent; stale held; records preserved | AT + FI |
| hostile01.json / hostile02.json | `hostile.py --rooms …/hostile0N` | 01: 4 test defects (kept); 02: 15 PASS + 1 cross-reference | AT + FI |
| rollback01.json, rollback01-n5-faithful.json | `rollback.py --rooms …/rollback01` + the faithful read | N7 stale under v7, no overwrite; N5 faithful byte-equal | AT |
| reconstruct01.json | `python -I -B bundle/reconstruct.py --index bundle/INDEX.json --room …/reconstruct01` | 4/4 equal, 293 files verified | AT (reproducibility, not a cold review) |
| retention.json | (derived) | tree digests of the 14 temp rooms | — |

## Per-case table: hostile02
| ID | Label | Case | Result |
|---|---|---|---|
| P01 | PACK | wrong v8 tool hash (review_loop) | refused `pinned tool hash does not match` |
| P02 | PACK | pass02 / pass03 altered | refused `pass02 pin mismatch` / `pass03 pin mismatch` |
| P03 | PACK | schema, extra key, length, missing tool name | refused (4/4) |
| P04 | PACK | prime_cycle removed | refused `pinned tool is missing` |
| P05 | PACK | 0517 artifact missing or tampered | `artifact-missing` / `artifact-hash-mismatch`, incomplete |
| P06 | PACK | two Returned lines | `ambiguous-submission`, nothing bound |
| P07 | PACK | `Returned: evidence/../../x.md` | `malformed-declared-path`, incomplete |
| P08 | PACK | hash or label in the attribution | `attribution-not-descriptive`, nothing bound |
| P09 | PACK | source change between prepare and record | record exit 2, `recorded: false` |
| P10 | PACK | existing manual review | see life01 L3 |
| P11 | PACK | manual target appears before publish | held; text byte-preserved |
| P12 | PACK | rollback leaves v8 inert | the v7 door runs; N7 incomplete again |
| P13 | PACK | CRLF pack page | non-assignment rows identical; complete |
| N01 | NEW | production pass04 + production v8 JSON in a copied root | the door accepts the pins; the workbook refuses (canonical-root guard) |
| N02 | NEW | decoy `artifact-manifest.json,` | never bound; complete |
| D01 | DISPATCH | authoring, return-lines, review-loop, unknown, run: no-argument calls | identical under v7 and v8; no writes (limit: same missing-pin stop) |

## First failures (raw, kept)
- **smoke01 / 02:** notes, checkpoint 1.
- **matrix01:** `matrix01.json`.
- **ctx01:** `ctx01.json`.
- **hostile01:** `hostile01.json`.
- **None was a candidate defect** except the real 0522 finding, which is not a candidate defect but a selection consequence.

## Limits
- **The production pass04 bytes' success path is not executed.** It cannot be without a canonical-root install. The one-line diff is the only difference from the executed adapter.
- **pass02 and pass01 code is imported from live in every lab run** (hash-checked).
- **Helper modules keep `ROOT = live`:**
  - return_access custody lookup;
  - the review_loop and prime_cycle fixture-root guards.
  - So the copy roots, being outside live, are not refused where production books (inside live) would be. The cycle path was never called, so the divergence is unexercised.
- **No concurrency, interruption, hard-link or race testing** (AR-01 is out of scope).
- **The reporter route and the N7 absent-target cycle seam** (Grok-1 and Grok-2 lanes) were not touched or tested.

## Prime's future independent probes (not run)
1. Rerun the matrix with Prime's own fixture builder.
2. Build pass04 from BUILD-PACK and run hostile N01 in reverse: the production bytes at the canonical root in a sandbox clone.
3. Independent N5 replays beyond 0522 and 0512.
4. A combined v8 plus reporter dispatcher once Grok-1's successor exists.
