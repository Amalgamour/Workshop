# Rollback and recovery: rehearsed results (0707/05.18)
**Evidence:** `rollback01.json`, `rollback01-n5-faithful.json`, hostile P12, matrix02. **These results come from copy roots only.**

## What rollback is
**The operation:** restore the live v7 bytes of `app/librarian.py` (c3a5be3b…, 12204 bytes).
- The v8 door, the v8 declaration and pass04 stay on disk, inert. Nothing loads them.
- All historical sources, evidence and records stay.

## What it actually does (measured)
| Case | Under v7 after rollback | Records |
|---|---|---|
| **N7** (0515, v8 record wfd2a21e…) | read and recover exit 1, `stale: true`. v7 re-measures without the N7 rows, so the live intake differs from the stored v8 intake. inspect is `incomplete`. A new v7 record is refused (`measurement is incomplete`). | v8 record files byte-unchanged; v7 adds only `failed/<id>.json` and `.correction.txt` |
| **N5** (0512, v8 record wb232d69…) | The real v7 entry on a COPY root shows `stale` with `ambiguous-declared-root`. This is the wrong-root effect of hard-coded `REPO`, not N5 semantics. **The faithful old-parser read and recover are byte-identical to v8** (exit 0, same review_id, not stale, no writes). | unchanged |
| **Re-select v8** | Both roots read fresh again (`stale: false`, exit 0) | unchanged |

- **So a one-line rollback restores v7 BEHAVIOR, but not v7 readability of N7 records written under v8.** Those show as stale. That is the correct, safe result, because nothing silently rebinds; but it is not "no consequence".
- **Old and new records stay distinguishable** by review id and by the stored `intake_id` (the v8 N7 intake has the declared rows; the v7 one does not).
- **The records carry no field naming the door version.** That is a gap: the builder should record the selected door identity if Prime wants version-labelled records. Proposed only, not built.

## Selection consequence that rollback does NOT undo
- 0522/05.13 declares `app/librarian.py` as an artifact. While v8 is selected, 0522/05.13 measures `incomplete` (`artifact-hash-mismatch`).
- Rolling back restores the bytes, and the measurement with them.
- **A review recorded for 0522/05.13 while v8 is selected would be refused** (incomplete), so no record is lost; it is only blocked.

## Safe holds
1. **Do not select v8 while a pending N5 review depends on a return that pins `app/librarian.py`** (0522/05.13 is one known case). Scan the work book for manifests listing `app/librarian.py` first.
2. **After any rollback, treat every N7 review recorded under v8 as stale-held under v7.** Do not re-record over them; re-select v8, or re-review under v7 manually.
3. **Never edit the v8 declaration in place.** A changed pin is refused by the door (P03), which is the intended hold.

## Exact recovery steps
| Situation | Steps |
|---|---|
| **v8 selected, but it misbehaves** | 1. Write the v7 dispatcher bytes back (c3a5be3b…, 12204 bytes). 2. Run `app/librarian.py review-loop read --book … --source … --pass …` for each review touched under v8, and record which are stale. 3. Keep every v8 record file; do not delete. |
| **v7 restored, and v8 must come back** | Write the candidate dispatcher bytes (5bc43806…). Reads return to fresh (rehearsed). |
| **The v8 declaration or pass04 was damaged** | The door refuses (P01–P04). Restore the files from the build commit; nothing else changes. |
