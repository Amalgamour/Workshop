# 05.NN DRAFT — Grok-1: active return-writer integration (line-pass routing, legacy reads)
date: 2026-11-02 · drafted by: claude-opus-5-5 (Claude), 0709/05.02 · for: Codex Prime to adapt and release
state: **DRAFT. Not released.** No live migration in this pack. **Live state stays untouched:** no sentinel, layout or authorization is written live.

## Goal
Make the supported routes file N5NN returns on the matching N1NN line and stop sequential allocation, using the two stops that already exist:
- the pass01 helper's own lock refusal;
- the line tool's per-book authorization (Grok-2).

Legacy reads keep working after the originals move to a book-shaped archive.

**Not a goal:**
- reconstruction, publication, retirement or rollback tooling (Grok-2, 0521/05.04);
- the review loop (unchanged; the 0709 seam check passed);
- any v3/v4 door.

## Depends on Grok-2's returned and reviewed contract (do not guess; stub only behind a named test double)
- **C1:** the pass02 line-tool path, sha256 and bytes.
- **C2:** its authorized-book interface for a book **with** `0100.band.returns`: argument names and refusal codes.
- **C3:** `lookup --member` output after retirement, including the archive path field.
- **C4:** whether pass02 itself writes and verifies the sentinel, or only checks it.

The tests below marked **[C]** wait for C1–C4. Everything else can be built now.

## File ownership
| File | Owner | Act |
|---|---|---|
| `app/return_line_tools_v2.py` | Grok-1 | NEW door. Pins C1, plus helper `return_capture.py` 8f3da5c6…/45767 and `return_inspect.py` 947915fe…/11402 **for reading only** |
| `app/return-lines-v2.json` | Grok-1 | NEW declaration for the door, in the existing `*.json` door style |
| `app/librarian.py` | Grok-1 (already under its repair) | Register the v2 door **only**. `capture-return` (handoff), boot and batch registrations are unchanged |
| `app/return_line_tools.py` (pass01 door, unregistered) | — | **unchanged**; stays unregistered |
| `labs/return-capture-pass01/*`, `labs/capture-handoff-pass01/*`, `app/handoff_tools.py`, `app/boot_tools.py`, `app/batch_tools.py` | — | **unchanged bytes and pins** (109 pin sites, `helper-pin-sites.txt`) |
| `0100.band.returns/01.md` | **Prime applies** at cutover step 8 | Grok-1 delivers the proposed text as `evidence/build05.NN/0100-instructions.md` |
| 0525 declarations | the 0525 owner, coordinated by Prime | Grok-1 delivers the needed declaration records as `evidence/build05.NN/declarations/`, in the v2 representation of `labs/app-dependencies-pass02` |

## v2 door commands (supported route; narrow)
- `librarian return-lines status --book B` (read-only) reports:
  - whether the layout is present, with its sha;
  - the sentinel: present or absent, its sha, and whether it equals the pinned bytes;
  - the phase: `sequential` (no layout, no sentinel), `frozen` (sentinel, no layout), `line-pass` (both) or `inconsistent` (layout without sentinel);
  - the door: present or absent.
- `reserve` / `capture` / `verify` / `lookup --page --batch | --member | --submission` forward to C1 with argument arrays (no shell). The door enforces the following before forwarding:
  - in the `line-pass` phase, writes proceed only with the authorization argument C2 requires;
  - **in the `frozen` and `inconsistent` phases, writes are refused** and lookups work;
  - **in the `sequential` phase, line writes are refused**, so line-pass filing never starts in an undeclared book;
  - source band 05 is routed to the matching N1NN; band 07 to the page-local tail; any other band is refused.
- **No** stage, adopt, publish, retire or rollback through the app. Those are Prime's bound operations, run directly with the authorization.

## Sentinel bytes (fixed, pinned in the door and in the 0100 text)
```
return-line-allocation-stop/1
This book is declared line-pass. Sequential return_capture.py reserve is refused here.
Not a crash leftover: do not delete. Use the line tool. See 0100.band.returns/01.md.
```
- **It works because pass01 `allocation_lock` uses `O_CREAT|O_EXCL`.** It refuses "allocation lock held" after 5 s, and it never removes a lock it did not create (return_capture.py 368–388; probe H4).
- **It confines no one:** any same-user process can delete it, write a `01NN.*` folder, or run other code. It stops the **supported** old command only. The status phase `inconsistent` (layout without sentinel) is how a deletion is detected.

## Proposed 0100.band.returns/01.md text (Prime applies at step 8; preserve the old text below a dated line)
- New N5NN returns are filed on the matching N1NN line: pass `05.NN` goes to `{N1NN.subject}/05.NN.return.md` and `05.NN.custody/`, through `librarian return-lines`.
- N7NN returns stay on their Colab page.
- **`return_capture.py reserve` is retired in this book.** The `.allocation.lock` here is a deliberate stop, not a crash leftover.
- Old members `0101`–`0183` are archived under their old names at `<archive_root>`. Look one up with `librarian return-lines lookup --member 01NN.slug`. To read it with the old tools, pass `members_book = <archive_root>`.
- `0154.colab-support-first-0501` is archived as incomplete. Its return is missing.

## Declarations for 0525 (records only; v2 representation)
- `return-lines-pass02` (from C1): role `line writer and reader`; requires the authorization for a book with the door.
- `app/return_line_tools_v2.py`: pins, commands, phases, and the sentinel sha.
- `return-capture-pass01`: annotation `reserve refused on declared books by sentinel; capture/verify/inspect legacy only`. **Its pin is unchanged.**
- `return-inspect-pass01`: annotation `reads archive with members_book`.

## Acceptance tests (disposable books under `D:\librarian\temp\…`; the declaring fixtures contain the door)
| # | Test | Pass |
|---|---|---|
| G1 | unchanged pass01 `reserve` with the sentinel present (new submission, and an in-flight repeat) | exit 2, "allocation lock held"; tree unchanged; lock bytes unchanged |
| G2 | unchanged pass01 `capture`, `verify`, `inspect` of an in-flight legacy reservation with the sentinel present | exit 0; complete |
| G3 | `status` in each phase: sequential, frozen, line-pass, inconsistent (sentinel deleted), and a sentinel with wrong bytes | the exact phase; an inconsistent phase or wrong bytes refuses writes |
| G4 [C] | v2 `reserve`+`capture` for `0504.app-entry/05.21` and `/05.22` in a line-pass book with the door and an authorization | one line page, two passes, receipts verified |
| G5 [C] | first filings after a fixture retirement of `0121.*`–`0125.*`: `0521`–`0525` pass `05.01` | lines `0121.return-placement` … `0125.app-dependencies` are created; no sequential member |
| G6 | sources `0201`, `0301`, `0401`, `0601`, `1201` | refused; nothing written |
| G7 | `0701`, `1701` | routed page-local; no N1NN written |
| G8 [C] | authorization negatives: missing, linked, another book, operation not listed, stale fingerprint, revoked | each refused, with its own code |
| G9 [C] | `lookup --member 0121.archive-resolution-0508` after fixture retirement | the line, the pass and the archive path |
| G10 | unchanged `return_inspect`, `prime_boot` and `batch_observe` with `members_book = <fixture archive>` | the same status as before archiving for a sample: one complete member, `0154` reserved |
| G11 | the unchanged helper on a line page (`verify`/`inspect 0104.app-entry`) | refuses or reports missing, as probe H3 recorded. **Documented, not fixed:** line pages are read through `lookup` |
| G12 | `app/librarian.py` | lists `return-lines`; refuses `stage`/`adopt`/`publish`/`retire`/`rollback` through the app; every old door's bytes equal their pins |
| G13 | a v2 door pin mismatch on any pinned file | refuses before running |

## Preservation and rollback
- New files only, plus one registration edit in `app/librarian.py`.
- **Rollback is to unregister.** No old file and no pin changes. Every test runs on a copy; first failures are kept.
- The live sentinel, layout and door text are cutover acts, Prime's under the Director's release. **This pack does none of them.**
