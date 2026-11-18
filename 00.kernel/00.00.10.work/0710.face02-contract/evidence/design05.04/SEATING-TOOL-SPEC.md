# Seating tool — bounded engineering specification (proposal, 0710/05.04)
who: claude-opus-5-5 · state: draft for Prime review. **Not a release and not a builder assignment.** It is derived from `lifecycle/lifecycle2.template.json` and the behaviour shown in `lifecycle/runs/`.

## Scope
**One small CLI** that runs, for a named release of 1–2 law faces in one book:
- stage, sign-check, seat (with retirement), restart, rollback and rollback-restart;
- status, read-only.

**Out of scope:** approval by a model; lock; promote; a registry; a workflow engine; a UI; other books.

## Inputs (all explicit; no discovery by newest file)
| Input | Owner |
|---|---|
| release file: `{book, faces: [{page, face, candidate_path, reviewed_sha256, source_seat_sha256}], warehouse_layout}` | Prime, from reviewed work |
| sign request: `{page, face, requested_by}` | model |
| approval record: `{by, words, ref, approved_sha256 per face}` | **Director** (recorded by Prime) |
| rollback decision: `{by, page, seated_sha256, retired_sha256, restore_seat_sha256, restore_draft_sha256}` | **Director** |

## Outputs
- the stage, sign, approve and seat records per face;
- raw images keyed by sha256;
- the journal (J1–J7, R1–R6);
- the typed ledger lines in `00.retire.09/09.md`;
- exit codes: **0** done or verified · **1** held, with a code and the observed hashes · **2** refused input.

## Transitions and required checks
**Exactly those in `lifecycle2.template.json`:**
- the stage `requires` lists;
- the seat states S-ready → S-seated, and the rollback states R-ready → R-restored;
- the partial-file rule;
- the mutable stamp whitelist `Authorization`, `state`.

**Any observed state not in the tables holds with no write.**

## Measurable finish (a builder is done when all of these hold)
1. **A test corpus reproduces all 35 fixture cases** of `lifecycle/runs/results.json` against the tool on disposable books, with the same outcome and code, plus no-write proof for every held case.
2. **Every held or refused outcome writes nothing**, checked by a tree hash before and after.
3. **Restart from each window W1–W8 and RW1–RW5** reaches byte-identical final files.
4. **Completed restart re-verifies:** PP1 is held.
5. **Rollback preflight:** PP2 and RB1–RB5 are held before any rename.
6. **No path outside** the release's book is written. The kernel itself is used only under a separate released seating pack.
7. **CRLF and raw bytes are preserved:** no text-mode writes (`O_BINARY` or binary file modes).

## Unknowns, exposed (each needs a decision before the build or during review)
| ID | Unknown | Whose |
|---|---|---|
| U1 | **warehouse layout:** page folders inside `00.retire.09` (proposal) versus another collision-free layout. 0009 is silent | Prime, then the Director with the kernel update |
| U2 | **the stamp lines that change at seating:** only `Authorization`/`state`, or also `version`/`who` | Prime |
| U3 | **where records, images and journals live** for the real kernel (on the work page evidence, beside the book, or elsewhere), and whether they are Git-tracked | Prime |
| U4 | **concurrency:** a lock file for one seating at a time (not modelled) | builder proposal |
| U5 | **OS guarantees:** rename and replace atomicity on the target filesystem (NTFS assumed, not shown) | builder evidence |
| U6 | **the text of the `09.md` statement** beyond the ledger lines (0009: "The statement inside is `09.md`") | Prime |
| U7 | **how the app exposes it:** one pinned door, or a lab CLI only | Prime |
