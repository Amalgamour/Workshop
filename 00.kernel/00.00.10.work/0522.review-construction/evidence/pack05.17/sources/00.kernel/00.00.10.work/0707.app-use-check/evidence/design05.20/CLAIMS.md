# Claims, cases and evidence (0707/05.20)
**Labels:**
- **PT** = my prototype test (author case on NEW external roots);
- **KF** = known failure / current behavior reproduced;
- **RH** = rerun of historical material.

**There are no independent Prime probes yet;** suggestions are at the end. Final run: `matrix-run04.json` (9/9) and `replay-run01.json`.

| # | Claim | Case | Observed | Label |
|---|---|---|---|---|
| 1 | A fresh N7 exchange (pack opened first, matching return, no N1) reaches its local first review | T1 | exchange `matched`, chronology `recorded-before-return`, `n1-not-applicable`, no `custody-missing`; record exit 0 (preliminary); separate publish exit 0 creates `06.01.review.md`; read/recover ×2 byte-equal, no writes; accepted/approved false, authority none, closes_work/releases_action/published_work false | PT |
| 2 | An orphan return is not a matched return, and its bytes are kept | T2 orphan-return | `orphan-return`, incomplete, record exit 2, return bytes unchanged, `unfiled_return_preserved` true | PT |
| 3 | Pointer pending, or pack missing, gives no match | T2 | `pointer-pending` (with `return-pending`), `pack-missing` | PT |
| 4 | Wrong pass is refused (**staged pass04 binds it**) | T2 wrong-pass | overlay `return-not-local`, incomplete; pass04 binds `05.01.return.md` complete | PT + KF |
| 5 | Wrong page: no nearby pack chosen | T2 wrong-page | `orphan-return`, `assignment` none | PT |
| 6 | Another book instance does not inherit a record | T2f | read exit 1 `stale: true` (run01: exit 0 not stale, **a real defect, fixed for N7**) | PT |
| 7 | A changed pack body, return or artifact, or a missing artifact, after record is stale; no publication | T3 | all four: read exit 1 stale, publish exit 1 "source changed after intake", no target | PT |
| 8 | Manual text at the destination, or a target that appears after inspect, is protected; the judgment is kept | T4 | publish exit 1 `manual-review`, bytes equal, read judgment canonically equal to the supplied one | PT |
| 9 | A second pass binds only itself; pass 1 is preserved | T5 | 05.02 matched to `05.02.return.md` → `06.02.review.md`; pass-1 files byte-equal; pass-1 read is the same review id, fresh | PT |
| 10 | N5 unchanged | T6 | overlay and pass04 prepare/form stdout byte-identical; `custody-missing` still reported; record preliminary/missing | PT |
| 11 | Prime's page-local pack Review summary does not stale the exchange (**pass04 does stale it**) | H1 (mine) | overlay exit 0 fresh; pass04 exit 1 stale; a task-body edit is still stale under the overlay | PT + KF |
| 12 | A basename match in another folder is not the return (**pass04 binds it**) | H2 (mine) | overlay `return-not-local`; pass04 binds `evidence/05.01.return.md` complete | PT + KF |
| 13 | Historical N7 pairs match; chronology is honestly unverified | R1 | real 0707/05.15 and 05.17: `matched`, `unverified`, complete, 26/33 artifact rows equal to pass04 | RH |
| 14 | The N5 copied-book weakness is unchanged (not fixed, by design) | R2 | N5 record read in book B: exit 0, not stale, under both the overlay and pass04 | KF |

## Raw first failures (kept)
- **matrix-run01 (4/9):**
  - `exchange` not emitted;
  - `open` crashed (owned book);
  - T2f copied-book defect (real).
- **matrix-run02 (4/9): invalid** (stale adapter after a failed heredoc regeneration).
- **matrix-run03 (8/9):** a harness CRLF write changed the pack body; the overlay correctly reported `open-record-mismatch`.
- Each has its `.stdout`, `.exit` and `.json`.

## Not shown
- the strict grammar;
- capacity;
- a cycle with custody;
- reporter parity on the overlay chain;
- production bytes at the canonical root (the overlay's production-shaped file refuses outside it, by guard, as pass04 does);
- concurrency.

## Suggested independent Prime probes (not run)
1. Hand-build an N7 page with a pack, then a return, and run `open` → prepare → record → inspect → publish on a NEW root of your own.
2. Rename a return to `05.01.return.md` under another pass's pack.
3. Edit the pack Review section, then the task body, and read after each.
4. Copy a book with records and read in the copy.
