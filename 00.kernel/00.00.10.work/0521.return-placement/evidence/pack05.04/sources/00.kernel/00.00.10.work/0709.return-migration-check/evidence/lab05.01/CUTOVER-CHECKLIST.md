# CUTOVER CHECKLIST — legacy 01NN → matching N1NN lines (proposed; not released)
date: 2026-11-02 · who: claude-opus-5-5 (Claude), 0709/05.01 lab

**Preconditions (all, in order):**
1. **Slices A and B** of the implementation pack are built, independently reviewed and accepted. The authorization file format is accepted.
2. **In-flight work reconciled.**
   - Grok-1's frozen repair pack has returned and Prime has reviewed it.
   - Every open N5NN return (0510, 0511, 0521–0525) and every pinned consumer (review loop pass03, cycle pass03, app doors, 0525 declarations) are reconciled to the post-cutover lookup.
   - No builder holds a pin to an old `01NN` path that cutover moves.
3. **A fresh audit and plan, taken immediately before cutover.**
   - `plan` against the live book writes a NEW file.
   - `change_count` must be 0 against the audit, or a new audit is taken.
   - `item_count` and occupants are compared with the 2026-11-02 facts (83 items, 18 occupants, 82 complete + 0154 reserved-only, 5 Colab tails byte-equal).
4. **A verified external backup of the whole work book,** outside the checkout and the page namespace. Its tree hash is recorded and independently re-read.
5. **The authorization file** for this book, plan sha256, audit sha256, backup root and operations is recorded with the Director/Prime release words.

**Steps:**
6. **Stage every source** (83) to `<backup>/sources`, lowest old capture first. On interruption, resume; never restart over a partial. Every staged file must equal its source by hash before continuing.
7. **Adopt.** Create the line pages, custody directories and relocation records. Retire **only** the 18 occupants, each only after its staged copy matches. 0154 stays incomplete. The 5 N7NN tails stay page-local: verify them, never re-file them to N1NN.
8. **Verify.** For all 83, lookup by old member and by origin must give the same descriptor and the original return bytes. Reservations must equal the staged originals. The `0104.app-entry` style multi-pass lines must have one page per line.
9. **Retire-originals** (the 65 non-occupants), each after a byte check, into `<backup>/retired`. Journal and resume. Lookup by old member must still resolve.
10. **Independent post-check** by a separate process or person: re-hash the backup, every relocated custody directory and every tail; compare with the stage journal; confirm that no original sealed byte changed and that relocation records say `reservation_destination_rewritten: false`.
11. **Only then file the pending N5NN returns** (0510→0110, 0511→0111, 0521→0121 … 0525→0125) with the line tool. Each is a first proper filing; it never relabels an old capture.

**Rollback:** `rollback-adopt` and `rollback-stage` (and a retire-originals rollback) restore the occupants and originals byte-identically from `<backup>`. Rollback material is kept until Prime verifies completion. **No step deletes the only copy.**

**Completion criteria:**
- all 83 resolve by old member and by origin;
- 0 problems;
- the 18 + 65 originals are preserved in the backup with hashes;
- 0154 is visibly incomplete;
- the layout is declared;
- helper `reserve` refuses on the live book;
- `0100.band.returns/01.md` is updated by Prime;
- the dependency records are updated;
- Prime's review is recorded.

**Preserved throughout:** the request, the reason and the Director answers (0417/06.01), the original custody bytes, and the old-to-new lookup.
