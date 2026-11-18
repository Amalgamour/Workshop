# Acceptance and replay matrix — combined loop candidate (0707/05.19)
**Every required claim is paired with a case and an evidence obligation.** All mutations happen on disposable books. On the live book, ONLY read-only prepare and form on the named cuts (per 06.18.review).

## Replay matrix (each source × each step, through the candidate's own `app/librarian.py`)
| Source | Kind | Book sources | prepare/form | record | inspect (full) | publish (separate) | read/recover ×2 | review-report |
|---|---|---|---|---|---|---|---|---|
| 0522/05.13 | N5 | 32 rows | complete under v7; **incomplete after selection** (dispatcher artifact) → stale, reported | refused (incomplete), judgment kept | — | — | exact | stale with reason |
| 0512/05.06 | N5 | 17 rows | equal to v7 (intake_id, rows, cuts, findings) | preliminary | ✓ | held `stale-own-review` (its page carries wbf38837…) | exact | current |
| 0512/05.09 | N5 | 29 | complete | **records with Prime's retained judgment** (K) | ✓ | publish into the PENDING review section | exact | current |
| 0522/05.14 | N5 | 20 | complete (staged files present as evidence) | preliminary | ✓ | ✓ | exact | current |
| 0707/05.15 | N7 | ~20 | complete, 26/26 | preliminary | ✓ | held `manual-review` (Prime's 06.15) / absent copy: per the Director answer | exact | current |
| 0707/05.17 | N7 | 26 | complete, 33/33 | **records** (K) | ✓ | held `manual-review` (Prime's 06.17) | exact | current |
| synthetic K-boundary | N5 | bound, bound+1 | complete | record at the bound; a clear oversize diagnostic above it, judgment kept | — | — | — | — |

## Claim → case → evidence
| # | Required claim | Case | Evidence obligation |
|---|---|---|---|
| A1 | N5 grammar and intake unchanged | the 0512/05.06 and 0522/05.14 rows above; the 12-case suite; the historical 17 reconciled individually | same-cut diff of `form.bindings.rows`, cuts, findings and intake_id against v7 |
| A2 | N7 complete for valid forms | 0707/05.15 and 05.17 | 26/26 and 33/33; measured hash = manifest hash; no lost rows |
| A3 | Malformed N7 blocks (Director) | inv2 X1 and X2 shapes, plus G's own cases | intake `blocked`; record refused; no publish; raw bytes kept |
| A4 | Capacity: real returns record; oversize is explicit | 0512/05.09 with Prime's EXACT judgment (`0512/evidence/prime-review05.09/core-review/judgment.json`); 0707/05.17; the K boundary | `reviews/<id>/judgment.json` canonically equal to the supplied one; oversize → named diagnostic and judgment in `failed/` |
| A5 | Full inspect before a separate publish | every publish row | saved `inspect.full-read.txt`, then the publish as its own process |
| A6 | Director/manual text protected | 0707/05.15 and 05.17 (Prime reviews present), plus a target-appears-before-publish case | byte-equal before and after; publish exit 1, held |
| A7 | Stale, tampered and missing sources refused | submission changed after read; artifact tampered/missing; pointer changed | read/recover/publish held; re-record refused; no rebinding |
| A8 | Pin refusal | wrong hash and missing tool for vN, W, G, K, F and R′; wrong schema | door exit 2 with the named pin |
| A9 | First absent N7 target | absent 06.NN on a copy, per the Director answer: (yes) preliminary creates it, labelled; (no) refused until cycle | file bytes plus journal; a second publish/recover returns `already-rendered` or equal output |
| A10 | Repeat and recovery | read and recover twice; recover after a render | equal stdout; no writes |
| A11 | Reporter parity | review-report on every row | report `current` where the loop is current; stale where the loop is stale; X6/X7 no longer reproduce |
| A12 | Dispatch unchanged for the other routes | authoring, return-lines, unknown: no-argument calls | identical to c3a5be3b output |
| A13 | Reconstruction | an index of every pinned file → a NEW root → replay of rows/cuts/findings | 05.18 `bundle/reconstruct.py` pattern; equality on root-independent fields |
| A14 | Rollback | select, record N5 and N7, then restore c3a5be3b, then read | N7 records stale-held, N5 equal, no overwrite; review-report absent again |
| A15 | History preserved | 0522/05.13 and 0522/05.14 under the candidate | stale with cause; their files byte-unchanged; nothing repinned |

## Not required (and not claimed)
- custody or `cycle-committed` on real Colab returns;
- 01NN migration;
- concurrency, interruption or AR-01;
- unlimited capacity.
