# Prima's review: "Workshop Manager and the First Desk Trial" (Codex, Draft 01, shared by Matthew t304u, Nov 18 2026 1:56 PM EST)

The draft itself was pasted by Matthew in chat (t304u). This file is Prima's review of it, checked against wf at workflow 8eb1fdb, kit/docs/DESIGN.md, and the real pages 90.10, 90.20, 90.30.

## 1. What can be shown today from existing records
| Draft piece | Already there? | Where |
|---|---|---|
| Responsible person (Shop Manager) and lead model (Floor Manager) per page | Yes | face 00 stamp: person, current Prime, previous Primes (DESIGN.md:21); `wf set-prime --ref` keeps the history |
| Work order = 05.NN with draft > pack > open > return > review > closed | Yes, same states | face 05, DESIGN.md section 5; `wf status` BOARD per page |
| Work order assignee | Yes | the claim holder; the checker is shown too |
| "The next decision" indicator | Partly | `wf status` "waiting" and "next"; `wf elevate --to person` and `wf answer` are logged |
| Open a card, see every face | Yes, as files | pages/<id>/00.md-08.md are views printed from log.jsonl |
| Work orders never disappear | Yes | log.jsonl is append-only and hash-chained; `wf verify` |
| xlink back to the original | Partly | face 08 connections (files and commits); a log entry can be named by page id + entry number + hash; no xlink format is fixed yet |
| Board of PAGES for a book | No | `wf status` is one page at a time |
| Desk > Shelf > Book levels | No | wf v0 page ids are temporary labels (ruling Q-SA, t275s1034); SeqAddr levels come later through seqaddr-core |
| Lessons extracted from orders | No record type | today lessons live by hand in BUILD-LOG, docs/journal (t303u), Prima's notes |
| Labs / trials (face 07) | No | not built in wf v0 |

Real records, not fixtures: steps 1 and 2 of the trial can run on real pages today. Page 90.20.00.0001 "core: write once" is a full Steering-sized story: 5 orders, one failed and fixed, 13 draft choices waiting on Matthew (K4), a spec and a journal. Only step 3's second book needs a fixture.

## 2. Where the portal could duplicate a governing record
1. The board's card summary must be printed from log.jsonl, the way faces are (DESIGN.md section 3, no direct writes). The draft says the same; keep it a rule, not a preference.
2. Moving a card or assigning a model must be a wf/compute command that writes a log entry (claim, set-prime, a future assign). A drag that only changes the board would be a second record.
3. Lessons: a lesson must link to its source entries, not copy their content as the authority. The order stays the record; the lesson is a pointer plus a why.
4. Shelf guidance vs a book's own decisions: if both hold the same number (the +-30 degrees example), the book's face 04 decision governs; shelf text may only cite it.

## 3. Authority decisions still needed (Matthew)
- A. What a new book on a shelf inherits automatically, and what it only sees as reference (the draft's first question). Proposed below.
- B. Who may promote a draft lesson to shelf guidance, and what test is enough (the draft says: tried on another project, with where it stops applying).
- C. Can the lead model (Floor Manager) assign or move work on its own page, or does each assignment need the person? Proposed: Prime may assign within the grant; changing Prime or widening the grant stays with the person (as wf does today).
- D. Retention and archive policy (the draft leaves it open; axiom 6 says identity and xlink must survive).
- E. The xlink format (page id + entry + hash is a candidate).

## 4. Proposed answer to question A (inheritance)
- Question: what does a new book inherit automatically from its shelf?
- Proposed answer: it inherits HOW to work (the shelf's checks, templates, test lists, roles) automatically; it inherits no decisions. Every number or choice from another book (the +-30 degrees) is reference only, shown with its why and an xlink, and the new book decides afresh in its own face 04.
- Why: process carries over safely; a decision depends on that project's goals. This is the draft's own steering example, and it keeps each choice where its why lives.
- Axioms check: 1 Authority (each book's person decides its own choices), 4 Why (a reference arrives with its why), 6 Lineage (xlink to the original), 7 Missing (a gap is marked, not filled by inheritance), 9 Trial (shelf guidance only after a test on another book).

## 5. How it fits Prima's portal page (autohound research)
Codex's board-of-pages at book level is better than Prima's card-per-05.NN at book level. Combined: the book board shows a card per page; opening a page shows its own board of 05.NN orders (today's `wf status` BOARD). Stage 1 of the roadmap can be a read-only `wf board` over pages/ that prints the page cards from the logs, with no new record.
