# Face lifecycle v2 — readable template (proposal, 0710/05.04)
who: claude-opus-5-5 · state: draft, nonproduction. **This is not an authority source;** each stage cites its law. Machine form: `lifecycle2.template.json`. Fixture: `lifecycle_sim2.py`, run once into `runs/` (35 of 35 as expected). **Fixture approvals and rollback decisions are SYNTHETIC.** It succeeds `design05.03/lifecycle/` (preserved, with its 13-case result).

## What changed from v1
1. **Completion is re-checked.** A restart never trusts a step label, including J7 "complete". It re-reads the seat, warehouse and draft files and compares them with the recorded plan. A mismatch is held as `completed-drift`, with no write (Prime's L-P1, case PP1).
2. **Rollback preflights before the first rename.** It needs a Director decision (SYNTHETIC in the fixture) that names the seated, retired and restore identities. The current seat, the current retired file, the draft name and the raw images are all checked first. Any difference is held with no write (L-P2, case PP2), so changed or new work is never moved.
3. **Raw before-images.** Every identity is kept as raw bytes keyed by sha256 **before** the step that replaces it. Restore writes those bytes; no stamp is reconstructed from fixture strings.
4. **State comes from hashes.** The `(seat, warehouse, draft)` hashes must match one planned state. Any other combination holds: `restart-state-unknown` or `rollback-state-unknown`. A malformed journal holds as `journal-malformed`. **Nothing is guessed.**
5. **The ledger is typed and append-only:** `planned` → `retired`; `rollback-planned` → `rolled-back`. A stop after `planned` never shows `retired` (case LG1).

## Seat steps and states
| Step | Does | State after |
|---|---|---|
| J1 | plan and raw images | S-ready: (before, –, approved) |
| J2 | ledger `planned` | S-ready |
| J3 | rename the seat into the warehouse | S-moved: (–, before, approved) |
| J4 | write the retired image (partial file, then replace) | S-retired: (–, retired, approved) |
| J5 | rename the draft to the seat | S-installed: (approved, retired, –) |
| J6 | write the seated image (partial file, then replace) | S-seated: (seated, retired, –) |
| J7 | ledger `retired`; complete | S-seated, re-verified on every later restart |

## Rollback steps and states
| Step | Does | State after |
|---|---|---|
| preflight | decision bound to the plan; seat = seated; warehouse = retired; draft name free; images present | R-ready, or held with no write |
| R1 | record the decision; ledger `rollback-planned` | R-ready |
| R2 | rename the seated face to the draft name | R-moved |
| R3 | write the approved (signed) image | R-draft |
| R4 | rename the retired face to the seat name | R-returned |
| R5 | write the before image | R-restored |
| R6 | ledger `rolled-back`; **the seated bytes are kept as an image** | done |

**Compute owns the byte checks. It never decides to discard or reinterpret a changed version;** that goes to the Director.

## Interruption windows
**Shown:** a stop after J1, J2, J3, J4 (including between the partial write and the replace), J5, and J6 (both points); a stop after R1–R5. Each restart reaches the same final bytes.

**Not shown, and held or out of scope:**
- power loss inside an OS rename or replace;
- two seating processes at once (no lock is modelled);
- a release of more than two faces;
- any stamp-line change other than `Authorization` and `state`. **Whether `version` or `who` change at seating needs approval;**
- lock and promote.

## Cases (run once; `runs/results.json`)
| Group | Cases | Outcome |
|---|---|---|
| carried from 05.03 | L1 (now with completed-restart re-verify), L2, L2b, L3 (no-write check), L5, L7, L7b, L8, L9, L10 | as before |
| **Prime's probes** | **PP1** completed restart after a changed seat → held `completed-drift`, no write; **PP2** rollback after a changed seat → held `rollback-current-changed`, no write | repaired |
| interruptions | W1–W8 (each seat window) → the same final bytes; one `planned` and one `retired` ledger line | ok |
| ledger | LG1 a stop after J2 → `planned` only | ok |
| malformed or unknown | M1 unknown journal entry → held; M2 draft removed mid-run → held | no write |
| rollback | RB0 ok (both versions restored, seated image kept); RB1 changed retired file; RB2 missing before-image; RB3 no decision; RB4 decision naming other identities; RB5 draft name occupied by new work | held, no write |
| rollback interruptions | RW1–RW5 restart restores both versions; RW6 the moved file changed during the interruption → held | ok / held |

**Mapping from 05.03:**
- L4 (stop after J3) is now W3.
- L4b (draft altered before restart) is covered by M2 and RW6.
- L6 (rollback) is now RB0 with its preflight.
