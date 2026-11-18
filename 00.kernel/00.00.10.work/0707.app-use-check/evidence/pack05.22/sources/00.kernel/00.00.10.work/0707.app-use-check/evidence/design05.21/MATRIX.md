# Requirement → case matrix and baseline results (0707/05.21)
**Runs:** `harness-proto-l-run02.json`, `harness-staged-g-run02.json` (first failures: `harness-proto-l-run01.json`).

| Case | Group | Requirement (short) | Needs | proto-l | staged-g |
|---|---|---|---|---|---|
| N5-1 | n5-same-cut | 0512/05.06 candidate == faithful baseline (id, rows, cuts, findings) | — | pass | pass |
| N5-2 | n5-same-cut | 0522/05.13 same-state equality; the selection-induced `app/librarian.py` change appears iff the dispatcher differs (collision recorded) | — | pass | pass |
| N5-3 | n5-same-cut | N5 `return.md,` `;` `)` bind as before | — | pass | pass |
| N7-1 | n7-valid | 0707/05.15: complete, 26/26, matched, N1 not-applicable | G, L | pass | **fail** (no exchange) |
| N7-2 | n7-valid | 0707/05.17: complete, 33/33, matched, N1 not-applicable | G, L | pass | **fail** (no exchange) |
| ST-1 | strict-n7 | trailing-text manifest with a self-consistent decoy blocks intake/record/publish | G | **fail** (A-01) | pass |
| ST-2 | strict-n7 | refused declaration beside a valid one blocks | G | pass* | pass |
| ST-3 | strict-n7 | `Verification:` with no value blocks | G | **fail** | pass |
| LR-1 | n7-local | orphan return: not matched, record refused, bytes kept | L | pass | **fail** |
| LR-2 | n7-local | wrong pass is not a local match | L | pass | **fail** (binds, complete) |
| LR-3 | n7-local | wrong page does not borrow a pack | L | pass | **fail** |
| LR-4 | n7-local | an N7 record in a copied book is not current there | L | pass | **fail** (reads current) |
| LR-5 | n7-local | history 0707/05.15: matched, chronology `unverified` (Director 06.20) | L | pass | **fail** |
| LR-6 | n7-local | new work: pack observed before return, same `.NN` | L | pass | **fail** (no open) |
| LR-7 | n7-local | second pass binds only itself; pass 1 kept and current | L | pass | **fail** (no exchange state) |
| CAP-0 | capacity | harness self-check: independent source counts = Prime's 29 / 20 / 44 | — | pass | pass |
| CAP-1 | capacity | 29-source retained judgment records, canonically equal | **K** | blocked | blocked |
| CAP-2 | capacity | 20-source retained judgment records | **K** | blocked | blocked |
| CAP-3 | capacity | 44-source retained judgment (judgment-open) records | **K** | blocked | blocked |
| CAP-4 | capacity | bound 64 records, 65 refused, other limits unchanged | **K** | blocked | blocked |
| KF-CAP | capacity | KNOWN FAILURE: 29 and 44 refused `limit sources` | (non-required) | reproduced | reproduced |
| LC-1 | lifecycle | form → record → inspect checkpoint → separate publish → read/recover ×2 equal, no writes, no authority | L | pass | pass |
| PR-1 | preservation | manual text at the destination: held, bytes kept, judgment equal | L | pass | pass |
| PR-2 | preservation | a target appearing after inspect: held | L | pass | pass |
| PR-3 | preservation | task-body change: stale, held | L | pass | pass |
| PR-4 | preservation | return change: stale, held | L | pass | pass |
| PR-5 | preservation | artifact changed or missing: stale, held | L | pass | pass |
| PR-6 | preservation | review-region-only edit stays current; task edit stale | L | pass | **fail** (review edit stale) |
| PR-7 | preservation | tampered pinned tool refused (door) | — | pass | pass |
| CTX-1 | preservation | in-process N5 → N7 → N5 ids equal fresh-process ids | L | pass | pass |
| RP-1 | reporter | combined-chain report current/stale/held parity | **R** | blocked | blocked |
| RP-2 | reporter | combined reporter refuses wrong pins; envelope intact | **R** | blocked | blocked |
| KF-RP | reporter | KNOWN FAILURE: frozen reporter v3 cannot serve this candidate's dispatcher | (non-required) | reproduced | reproduced |
| IN-1 | instance | N5 same book: record → read current | — | pass | pass |
| IN-2 | instance | N5 copied book: current applicability held | **I** | blocked | blocked |
| KF-IN | instance | KNOWN FAILURE: an N5 copied book reads current | (non-required) | reproduced | reproduced |
| RC-1 | reconstruction | a rebuilt root (declared builder, frozen sources) has identical files and identical N7 rows/cuts | — | pass | pass |
| RB-1 | rollback | v7 dispatcher restored: N7 record non-current, records kept; re-select current | L | pass | pass |

\* On proto-l, ST-2 holds through the local pair rule (`return-not-local`), not through grammar blocking.

**Readiness:**
- **proto-l: NOT READY** (2 fail, 7 blocked, deps K/I/R/W pending).
- **staged-g: NOT READY** (10 fail, 7 blocked, same deps).
- **combined: NOT READY** (every case blocked; candidate PENDING).

**No candidate passes both the strict and the local groups.** The combined candidate W does not exist yet.
