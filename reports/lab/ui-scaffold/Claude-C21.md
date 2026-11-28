# Report: pack C21

- Builder: Claude (Matthew's PC, D:\Git\claude\wf-run\work)
- Pack: C21, from docs/plan/WORK-PAGE-2026-11-30.md:101 @ prima/build 5d26b448.
- Kind: lab (not a wf page; no pass)
- Check fixed: docs/review/FIRE-SALE-2026-11-26-UI1-CHECK.md @5d26b448, findings U1-U3 (lines 26-28).
- wf source read on returns eab873bb.

## Files touched

- labs/ui-scaffold/README.md (2 lines changed)
- labs/ui-scaffold/CONTRACT.md (2 lines changed)
- this report (new)
- QUESTIONS.md was not edited. Every other line was kept as it was.

## Each changed line

### U1: README.md:38

- Old: `| Pass | one pass, for example 05.03 | its jobs w01, w02 ... | pending, accepted, discarded (close `cards`, 0404 log entry 12 and 22) |`
- New: `| Pass | one pass, for example 05.03 | its jobs w01, w02 ... | the wf card words: accepted, carried, discarded, candidate (src/cmd.rs:14; signoff and close `cards`, 0404 log entry 12 and 22) |`
- Now matches: src/cmd.rs:14, `CARD_WORDS = ["accepted", "carried", "discarded", "candidate"]`. "pending" is gone.

### U2: CONTRACT.md:24, pass-level step

- Old: `**partial.** Only after close: the close entry's `cards` (0404 log entry 22: `w01 accepted`). Before close: **missing**`
- New: `**partial.** From return on: each job's text from the return entry's `jobs` (src/board.rs:412-413; 0423 log entry 19). From signoff on: the signoff `cards` (src/board.rs:432; 0404 log entry 21). At close: the close `cards` (0404 log entry 22: `w01 accepted`). Before return: no job step`
- Now matches: src/board.rs:412-413 prints each return job. src/board.rs:432 prints the signoff cards. Checked on packs c697e035: 0404 entry 21 is a signoff with cards `w01 accepted, w02 accepted`. 0423 entry 19 is a return with `jobs`.

### U3: README.md:24

- Old: `- **wf page ids are not checked as SeqAddr yet** (docs/DESIGN.md:15-16).`
- New: `- **wf checks the form of a work address, DD.SS.BB.PPPP, at init.** It uses rules copied from seqaddr-core (src/addr.rs:1-4, :108-123), called at src/cmd.rs:187. It does not look the address up in a compute book.`
- Now matches: src/addr.rs:1-4 (rules copied from seqaddr-core), src/addr.rs:108-123 (`check_work`), src/cmd.rs:187 (called by init-page when there is no system ref).

### U3: CONTRACT.md:44

- Old: `| join of a wf page to its compute book | **missing.** wf ids are not checked as SeqAddr | docs/DESIGN.md:15-16 |`
- New: `| join of a wf page to its compute book | **missing.** wf checks only the form of a work address at init. It does not look it up in a compute book | src/addr.rs:108-123; src/cmd.rs:187 |`
- Now matches: the same lines as above. The join stays **missing**, because `check_work` checks the form only and reads no book (src/addr.rs:108-123).

## Done when

| Line | Where it is met |
|---|---|
| Each fix cites the wf file and line it now matches | Each section above, and the cites inside each new line |
| Nothing outside labs/ui-scaffold/ changes | `git diff --stat` shows only README.md and CONTRACT.md, plus this report |

## Left for Prima (not fixed here)

- U4 (Low): CONTRACT.md:64 and README.md:49 read as one lock per face. A page has one hold at a time, and only faces 01, 04 and 05 lock (check lines 29).
- U5 (Low): README.md:23 cites compute route handlers for `books/`. The folders are in crates/compute/src/main.rs:38, and `kernel/` is read too (check line 30).
- U6 (Low): QUESTIONS.md:22 leaves out `/ask/link` (check line 31).
- The check also says DESIGN.md:15-16 is itself stale. That file is outside my lane (check line 56).

## Every cite

- src/cmd.rs:14, :187; src/board.rs:412-413, :432; src/addr.rs:1-4, :108-123 (returns eab873bb).
- 0404 log entries 12, 21, 22 and 0423 log entry 19 (packs c697e035).
- docs/review/FIRE-SALE-2026-11-26-UI1-CHECK.md:26-31, :56 (prima/build 5d26b448).

## Questions for Matthew

- New, from U1: the pass board's columns are now the four wf card words. "candidate" is a word wf allows, but no log I read uses it. Should the pass board show a "candidate" column? Default: yes, since wf allows it (src/cmd.rs:14). This does not change QUESTIONS.md Q1-Q8.

## Stop rules

- None hit. Nothing needed wf.
