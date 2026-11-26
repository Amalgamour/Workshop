# Fire sale: independent check of Claude's UI-1 return

Prima fire-sale worker, Thu Nov 26 2026, about 1:00 AM EST. Read only. Checked per t580u (any Claude change to data, logs or tests gets an independent check).

## What was checked

- Return: commit `d7da9e80` on `returns` (parent `755d046e`), "lab: UI-1 kanban front design". Author field `Mathias`, body "Builder: Claude", Co-Authored-By Claude.
- Read from the box's read-only bare copy `/workspace/firesale-notes/ws.git`. `git ls-remote` shows returns `ec78461d` and prima/build `5201b243` there match GitHub. Nothing was fetched, written or pushed there.
- Files: `labs/ui-scaffold/README.md` (109 lines), `CONTRACT.md` (105), `QUESTIONS.md` (73), `reports/lab/ui-scaffold/Claude-20261125-1608.md` (33).
- Pins Claude names, all exist and are ancestors of today's tips: returns `755d046e`, prima/build `5201b243`, packs `88be5702` (packs tip is now `c697e035`).
- Every `file:line` cite and every log-entry cite was opened at the pinned commit. About 60 cites.

## Data safety (t580u)

- **No data, log or test was changed.** The commit adds 4 new files and nothing else (`git show --stat`). No `app/`, `src/`, `tests/`, `pages/`, `.workshop/` or log file. The two later commits on returns (`6fca9e2f` Codex UI-2, `ec78461d` Prima's close log) do not touch `labs/ui-scaffold/`.
- No log entry was written by Claude. No wf command trace.
- The report's file list and "no stop rule hit" match the commit.
- Identity: the git author is Matthew's PC name, with Claude named in the body and trailer. That is the typed-for stand-in allowed until sign-in (t585u). Noted, not a finding.

## Result

Most claims hold. **6 findings: 0 High, 3 Medium, 3 Low.** None changes data. Two could seed wrong data if built as written (U1, U2), so they should be fixed before UI-1 feeds a build page.

| id | sev | where | Claude says | repo shows | kind |
|---|---|---|---|---|---|
| U1 | Medium | README.md:38 | Pass-level columns are "pending, accepted, discarded" (close `cards`) | wf's card words are `accepted`, `carried`, `discarded`, `candidate` (src/cmd.rs:14; :1046 sets `carried`). "pending" is not a wf word. | wrong; would seed an invented state into the board contract |
| U2 | Medium | CONTRACT.md:24 (pass-level step) | Job step exists "Only after close: the close entry's `cards`. Before close: **missing**" | The `signoff` entry already carries `cards` (0404 entries 11 and 21; 0423 entries 11 and 21), and the card prints them (src/board.rs:432). The `return` entry carries per-job text (`jobs`, 0423 entries 9, 19, 29; src/board.rs:412-413). So the field is partial from return on, not missing until close. | wrong; a field with a source is marked missing |
| U3 | Medium | README.md:24, CONTRACT.md:44 | "wf page ids are not checked as SeqAddr yet (docs/DESIGN.md:15-16)", given as the reason the wf-to-books join is missing | DESIGN.md:15-16 does say that, but it is stale. 0403 ("init-page refuses invalid work addresses") closed **passed** (0403 entry 12). `src/addr.rs` on 755d046e checks work addresses with rules copied from seqaddr-core, called at src/cmd.rs:187. Not a full SeqAddr parse, but not "not checked". | stale doc repeated without checking code |
| U4 | Low | CONTRACT.md:64, README.md:49 | "each face: who holds its lock" | A page has one hold at a time (`hold: Option<Hold>`, src/page.rs:78), and only faces 01, 04, 05 can be locked (src/cmd.rs:577). The row reads as a lock per face. | overstated |
| U5 | Low | README.md:23 | The compute crate reads `books/` (cites crates/compute/src/lib.rs:130-131, :246-261) | True, but those lines are route handlers. The folders are in crates/compute/src/main.rs:38 (`books/` then `kernel/`). The compute also reads `kernel/`. | weak cite |
| U6 | Low | QUESTIONS.md:22 | Compute writes are `/propose`, `/ask`, `/close` (lib.rs:258-261) | The cited range also has `/ask/link` (post, :260), left out of the list. | incomplete |

## Claims that hold (checked)

- `wf board [<page>]` with no page is the book board (src/lib.rs:49-50). "read only, built from the log" (src/board.rs:285).
- Six columns with tails, side labels and owners (src/board.rs:25-32); Ready owner "any builder: wf claim" (:27). CAP 40 (:16); 3 closed shown (:18); footer (:338-340); stale rules (:174-217); attention lines (:220-260).
- `--card NN` (src/board.rs:347-448); "held by" is the claimant (:368); next from `pass_next` (src/status.rs:24; board.rs:371). Text only: no JSON output anywhere in wf src (only `json_kind` for messages).
- Book board: counts per tail, attention, halted, title cut to 30, unreadable lines (src/board.rs:466-497).
- `Hold` fields (src/page.rs:38-46); lockout and release entries (src/cmd.rs:582, :624); lock checks since 0423 (src/page.rs:369-386).
- app/ last changed Nov 11, `9f5500f3` (prima/build); `COMPUTE_URL` default port 7700 (app/lib/compute.ts:2); `get` (:10-13); write route `app/app/api/post/[...path]/route.ts` and desk screen `app/app/desk/[dd]/page.tsx` exist; token check (crates/compute/src/lib.rs:95); routes (:244-261); `app/mock/fixtures/` exists.
- Log cites on packs 88be5702: 0403 entry 1 `grant_ref` t413u; 0403 entry 2 face 04 goals; 0423 entry 23 grant `ref` t584s2361; 0423 entry 27 pack keys have no `ref`; `branch` in the pack entry; 0404 entries 12 and 22 close `cards`; 0416 entry 12 "not merged by wf v0"; `pages/90.50.10.0423/01.md` lines 2 and 4; faces 00.md-08.md exist.
- 0403: 12 entries on packs, 9 on returns `.workshop/logs/` (counted); C1-REVIEW.md:40 R9 says the same.
- DESIGN.md:14 (several models) and :21-29 (faces); brief W:21, :23, :66-84; WORK-PAGE-2026-11-25.md:66 @dcdab638; labs/draft-page/QUESTIONS.md Q2.
- Done-when: 3 options with costs and a ★ default (A); CONTRACT tables; Q1-Q8 each with a default; no app/ file edited. Met, apart from U2 (one field wrongly marked missing).

Design note, not a finding: Claude's default A (wf gives the board as JSON, the front draws it) is the same as the research worker's board survey default A (docs/research/BOARD-DESIGN-ALTERNATIVES-2026-11-26.md). Two separate views agree.

## Proposed CATCH-LOG rows (for a checker or Prime to write; CATCH-LOG.md not touched)

Same 11 columns as docs/quality/CATCH-LOG.md:21. Row numbers are placeholders (P1-P4); the writer numbers them.

| # | Date (EST) | Page.pass | Kind | What happened | Who made it | Caught by | How caught | Why it matters (axiom) | Outcome / fix | Evidence |
|---|---|---|---|---|---|---|---|---|---|---|
| P1 | 2026-11-26 | lab UI-1 | catch | UI-1 README names pass-level columns "pending, accepted, discarded"; wf has no "pending" and has "carried", "candidate" | Claude (UI-1) | Prima fire-sale worker | opened src/cmd.rs:14 against README.md:38 | axiom 7 (no guess as fact); t580u check | fix README.md:38 before UI-1 feeds a build | d7da9e80; this doc U1 |
| P2 | 2026-11-26 | lab UI-1 | catch | UI-1 CONTRACT marks the job step "missing" before close, though signoff and return entries carry it | Claude (UI-1) | Prima fire-sale worker | read 0404 and 0423 logs on packs 88be5702 and src/board.rs:412-432 | axiom 9 (check what really exists) | fix CONTRACT.md:24 to "partial" with the sources | d7da9e80; this doc U2 |
| P3 | 2026-11-26 | lab UI-1 | catch | UI-1 repeats stale DESIGN.md:15-16 ("ids not checked as SeqAddr") though 0403 passed and src/addr.rs checks work addresses | Claude (UI-1); stale source DESIGN.md | Prima fire-sale worker | read 0403 close entry 12 and src/cmd.rs:187 | axiom 9 | fix README.md:24 and CONTRACT.md:44; DESIGN.md:15-16 is a stale-doc item for Prima | d7da9e80; this doc U3 |
| P4 | 2026-11-26 | fire sale job 13 | mistake (self-catch) | Fire-sale prototypes doc called the held overflow item "R16"; it is CONFLICTS D1 (R16 is the 03.00 door) | Prima fire-sale worker | Prima fire-sale worker (self-check) | read DIRECTOR-RULINGS.md:65 and CONFLICTS.md:148 | axiom 7 | corrected in the seqAddr fix proposal | 4e94864; SEQADDR-SPEC-FIX-PROPOSAL.md |

P4 is a self-catch. Under t586u the model that made the mistake does not write its row, so Prima or a checker should write it, or drop it.

U4-U6 are Low and need no rows unless Prima wants them.
