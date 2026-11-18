# DRAFT — Grok implementation pack: line/pass return enforcement and authorized cutover support
date: 2026-11-02 · drafted by: claude-opus-5-5 (Claude), 0709/05.01 lab · state: **DRAFT for Codex Prime; not released, not applied**

Every "before" hash below was measured on 2026-11-02 (`callers.json`, `inventory/`) and equals the 0521 integration-patch table. Nothing listed here has been edited.

## Two separately released slices
| Slice | Purpose | Touches live? |
|---|---|---|
| **A — new-work enforcement** | a declaring book stops sequential allocation; new N5NN passes file on the matching N1NN line; N7NN stays page-local | **no physical moves.** The only live write is one declaration, and only with a Director/Prime authorization file |
| **B — authorized cutover support** | `stage` / `adopt` / `retire-originals` / rollback on the live book, under an explicit per-book, per-plan authorization | tooling only; **running it is a third, separate release** (CUTOVER-CHECKLIST) |

## Slice A — enforcement (NEW successors; old bytes stay)
| Path (before sha256 / bytes) | Change |
|---|---|
| `labs/return-lines-pass01/return_lines.py` (863968c5… / 100897) | **unchanged.** NEW `labs/return-lines-pass02/return_lines.py` adds an authorization gate (below) for `init`, `reserve`, `capture` and `verify` on a book that holds `0100.band.returns`. Every other path, schema and descriptor stays byte-compatible with pass01 output (`return-line-descriptor/1`; `return-line-capture/1`; `legacy-relocated/1`) |
| `labs/return-capture-pass01/return_capture.py` (8f3da5c6… / 45767) | **unchanged.** NEW `labs/return-capture-pass02/return_capture.py`, or a wrapper: `reserve` **refuses** when the book has `return-line-layout.json` with `sequential_allocation: false`, naming the line tool. `verify` and `inspect` of legacy `01NN.slug` members are unchanged |
| `app/return_line_tools.py` (2605 bytes; pins pass01) | NEW `app/return_line_tools_v2.py` pinning the pass02 successors. The old door stays |
| `app/batch_tools.py` (555cd07d… / 11299), `app/boot_tools.py` (409901b1… / 9601), `app/handoff_tools.py` (f1d76a51… / 9901) | **re-pin only if** the helper successor replaces the helper path they pin. They do not allocate. The pack lists their exact before and after hashes |
| `labs/review-loop-pass03/review_loop.py` (47f47d16… / 55474), `labs/prime-cycle-pass03/prime_cycle.py` (496b4d72… / 76045) | **unchanged.** The 0709 seam check shows both accept real pass01 descriptors (new capture and relocated legacy). A pass02 producer must keep that byte shape; the regression test is the 0709 `seam.py` cases |
| `labs/colab-workflow-pass02/colab_workflow.py` (4a2ece9e…), `labs/colab-support-pass02/colab_support.py` (2b720434…) | **out of this pack.** N7NN page-local custody is the separate K1–K3 workflow lane (0510/05.06, 0511/05.05) |
| Lab demos calling helper `reserve`: `labs/capture-flow-rehearsal-pass01/rehearse.py` 588/595; `labs/capture-handoff-pass01/demo.py` 133; `labs/desk-app-integration-pass01/demo.py` 170/257/288; `labs/desk-loop-replay-pass01/replay.py` 194…; `labs/return-capture-pass01/demo.py` 108/255 | **frozen historical labs.** After A, the declaring live book refuses their `reserve`. Do not edit; record that they are superseded |

**Authorization gate (slice A).** This is not a guard removal: the pass01 refusal stays the default. A mutating command on a book that holds the door proceeds only with `--authorization ABS`, a file `return-line-authorization/1` stating:
- `book` (resolved absolute path);
- `operations` (subset of: init, reserve, capture);
- `release`: the verbatim Director/Prime words and their page;
- `layout_sha256` (the declaration it allows);
- an expiry: none, or a page-recorded revocation.

The tool refuses if the file is missing, linked, names another book, or names an operation not requested. The file is evidence, not authentication.

**A1 — the live declaration.** `init` writes `return-line-layout.json` (line-pass, bands 5 and 7, `sequential_allocation: false`) under that authorization. After it, any helper `reserve` on the live book refuses.

**A2 — first proper filing of the pending N5NN returns.** Blocked until slice B frees their numbers, because the target numbers are occupied:

| Source | Line | Current occupant | Freed by |
|---|---|---|---|
| 0510 | 0110 | 0110.return-inspection-0504 | B adopt (one of the 18) |
| 0511 | 0111 | 0111.prime-boot-design-0506 | B adopt |
| 0521 | 0121 | 0121.archive-resolution-0508 | **B retire-originals (not among the 18)** |
| 0522 | 0122 | 0122.bridge-overlap-0513 | B retire-originals |
| 0523 | 0123 | 0123.boot-validation-0508 | B retire-originals |
| 0524 | 0124 | 0124.clerk-seam-design-0503 | B retire-originals |
| 0525 | 0125 | 0125.mapping-capture-0509 | B retire-originals |

**Tests for A** (disposable books; the declaring fixture has the door present plus an authorization):
- two 05.NN passes on `0504.app-entry` land on one `0104.app-entry`;
- helper `reserve` refuses in a declaring book and still works in a book without the layout;
- `0701` and `1701` stay page-local; `0201`, `0301`, `0401`, `0601` and `1201` are refused;
- **authorization negatives:** missing, wrong book, wrong operation, linked file, and a door without authorization;
- legacy `verify` and `inspect` unchanged;
- the 0709 seam cases still give observation `complete`.

## Slice B — authorized cutover support (tooling; running it is separately released)
- **Allow `stage`, `stage-resume`, `adopt`, `rollback-*` on the live book only with an authorization** (operations: stage, adopt, rollback, retire-originals). It must name the exact plan sha256 (a fresh `plan`, not 52951e1d… unless re-derived to equal it), the audit sha256 and the external backup root, which must be outside the checkout.
- **NEW `retire-originals`.** After `adopt` verifies, move each **non-occupant** original `01NN.slug` directory (the 65 that rehearsal 0709 leaves in place) into `<backup>/retired/`, one at a time in ascending order, after a byte check against `<backup>/sources/<member>`. It writes a journal and is resumable. **Never delete.**
  - `0154` stays as reserved-only and incomplete. Its handling is an explicit Prime choice: retire it as incomplete, or keep it in place.
- **Legacy lookup after originals leave the book.** `lookup --member 01NN.slug` must still resolve through the line's `relocation.json` and the backup copy, and say where the original bytes now live.
  - **Not exercised by any rehearsal so far.** Today's rehearsal leaves the originals in the book.
- **The live guard is kept** for every unauthorized call. No blanket removal.

**Tests for B:**
- the full rehearsal on a copy **with** the door present plus an authorization (today's rehearsal used a copy without the door);
- an interrupted and resumed `retire-originals`;
- rollback restores the originals byte-identically;
- lookup by old member after retirement;
- `0154` handling;
- an occupied-destination refusal.

## Not applied, and called out
- **`0100.band.returns/01.md`** still instructs sequential `0101`–`0199` members (line 28). Its update (line-pass for N5NN, page-local for N7NN, legacy lookup index) is a separate Prime page edit, not this pack.
- **0525 dependency declarations** (v2 representation) need records for the pass02 successors and the new app door.
- **No `0184` allocation and no receipts in either slice.**
