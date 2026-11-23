# Workshop MVP goal: proposal for Matthew

state: proposal, with gaps G1-G8 answered by Matthew (t541u). The goal and criteria below follow those answers. Not a close of the MVP.
made: 2026-11-23, about 1:00 PM EST, by Prima.
updated: 2026-11-23, after Matthew answered the gaps (t541u, about 12:51 PM EST).
source: Codex's message, relayed by Matthew (t540u). Verbatim in docs/review/CODEX-MVP-t540.md. Gap answers: docs/review/DIRECTOR-WORDS-t541-mvp-gaps.md.
pins: prima/build files at 14098406 when first written. wf kit files on `returns` at 231bbe79.

How to read this:
- "Matthew (via Codex)" means Matthew's direction as Codex wrote it. Not his own recorded words.
- "Matthew (tNNNu)" means his own words, recorded in docs/review.
- "Codex" means Codex's proposal.
- "Prima" means my proposal.

## 1. Matthew's directions

From Codex's message (CODEX-MVP-t540.md:11-17), via Codex:
- Workshop is "body-shop management software for a workshop where people and AI work together." (via Codex, :11)
- The same system should "work across fields through desks, shelves, and books." (via Codex, :11)
- It uses "the universal grammar and design from the kernel." (via Codex, :11)
- "The car is the page." (via Codex, :13)
- A car may need body work, paint, electrical work, tires and alignment. (via Codex, :13)
- "Each 05.NN is a work order on that page." (via Codex, :13)
- Another coat of paint gets the next counter. (via Codex, :13)
- "The earlier pass stays in the record with the reason the work continued." (via Codex, :13)
- MVP rule, as Codex relayed it: "One worker at a time owns the whole page." (via Codex, :15)
- That relay held "whether that worker is writing the pack, building, checking, reviewing, or leading." (via Codex, :15)
- "Independent pages can move in parallel." (via Codex, :15)
- "Finer-grained ownership is a later design question." (via Codex, :15)
- Prima puts "a real pack through the core." (via Codex, :17)
- "The compute validate as much as it can." (via Codex, :17)
- "The worker use the compute's guidance to continue." (via Codex, :17)
- Records are "saved, searchable, and understandable enough for a fresh person or model to pick up the work." (via Codex, :17)

t541u refines the holding rule in that relay. The page is held only while one worker is actively working on a face. See G3 and G7 below.

Matthew's own words that back this:
- Matthew (0704 lab, labs/0704/MATTHEW-RESPONSES.md:11 on returns): "I want to see prima dropping packs through the core, with the compute checking and validing as much as it can."
- Same line: "All records being saved, searched and understandable."
- Matthew (0704 lab, MATTHEW-RESPONSES.md:6): "if a 05.03 is taken then go to 05.04".
- Matthew (t533u, DIRECTOR-WORDS-t533.md:5): "Once a worker is in a page, no other workers can use it."
- Same line: "We can run many pages in parralel but no more then one worker per page at a time."
- Matthew (t423u, DIRECTOR-WORDS-t423u.md:7): "With kanban style boards to integrate our kernel, pages, desk, faces, seqaddr designs."
- Same line: "So whys can be captured and reused to strengthen over time."
- Matthew (t541u, DIRECTOR-WORDS-t541-mvp-gaps.md): the eight gap answers. Verbatim there. In short: the compute is wf plus one seqaddr validate step; 0498 is the MVP target; a worker holds the page only while actively working on face 01, 04 or 05, and that face is locked, one model at a time; a small second-field trial comes after 0498; the board is wf board with holder, step and next; GitHub search is enough for now, with a GUI Workshop manager as the long-term direction; work orders are the 05 face; the current report file is enough.

## 2. Codex's proposals

From CODEX-MVP-t540.md:19, by Codex:
- Make this the design goal.
- Use 0498 to test it.
- The Kanban board shows who owns each page.
- It shows what step each page is in.
- It shows what comes next.
- The walkthrough shows the compute recording a handoff.
- It shows the work-order history kept across passes.
- A fresh session finds the completed work.
- That session explains why a decision was made.
- Try the same loop on a job from a different field.
- That tests whether the kernel grammar carries over.

Codex's earlier 0704 proposal for 0498 (labs/0704/DRIFT-REVIEW.md:32 on returns), by Codex:
- Exercise one refusal with a reason, then a valid retry.
- Compare the searchable view with the raw records.
- Record the commands actually run and every hand step.
- Name which core path 0498 really uses (DRIFT-REVIEW.md:34).

## 3. Prima's proposed MVP goal

Prima proposes:
Workshop's MVP is one working shop on Matthew's PC, run with wf, plus one seqaddr validate step.
The target is page 0498.
Prima drops a real pack.
The compute checks it and tells the worker the next step.
A page is held only while one worker is actively working on a face (01, 04 or 05).
That face is locked, and the compute refuses anyone else.
One model works on the page at a time.
Between steps the page is not held.
Each 05 pass is a work order with its own counter.
A new pass never replaces an old one, and the record says why work continued.
The board is wf board. It shows each page's holder, step and next move.
Every record is saved in git and can be found on GitHub and read cold.
A fresh session can find a closed page and explain why a decision was made.
A small second-field trial runs after 0498, on a job Matthew picks.
Matthew runs the 0498 walkthrough himself and says go, hold or redo.
The current report file is enough for this run. Page 0422, where wf itself sends reports, can land later.
A GUI Workshop manager, where pages are the cars and 05 passes are the work orders, is the long-term direction. It is not part of the MVP.

## 4. Acceptance criteria

Each line says what must happen, who checks it, and the evidence.
"The run" means page 0498 taken from pack to close on Matthew's PC.

1. Real pack through the core.
   - What: Prima packs and publishes a real job page; the compute validates it before the worker claims.
   - Who checks: Grok-Check.
   - Evidence: the pack and publish-pack log entries; the wf output and the `seqaddr validate` output, both saved in the page record. The compute is wf plus that one seqaddr validate step.
2. Compute validates as much as it can.
   - What: the run includes at least one refusal with a reason (for example a bad return), then a fixed retry that is taken.
   - Who checks: Grok-Check.
   - Evidence: the refusal text and the retry entry, both in the log or the run record.
3. Worker follows the compute's guidance.
   - What: after each step the worker runs the "Next:" line wf printed, with no extra prompt from Prima.
   - Who checks: Codex (independent of Grok code).
   - Evidence: the run transcript; each command matches the previous "Next:" line; every hand step is listed.
4. Handoff recorded.
   - What: each change of holder (Prima to builder, builder to checker, checker to Prima) is a log entry naming who and when.
   - Who checks: Grok-Check.
   - Evidence: claim, return, check, signoff and close entries in log.jsonl; `wf verify <page>` says ok.
5. Work-order history kept across passes.
   - What: the run needs a second pass (for example a failed check). The new pass gets the next counter. The first pass stays, with the reason. The work orders are the 05 passes.
   - Who checks: Codex.
   - Evidence: both 05.NN passes in the log; the first pass's failed check or signoff note gives the reason; no published entry rewritten.
6. Board shows holder, step and next.
   - What: during the run, `wf board` shows each page's holder, step and next move, including on the book board.
   - Who checks: Matthew, by eye.
   - Evidence: `wf board` (book) and `wf board <page>` output saved at each step. The book-board change is pending page 0424, not packed yet.
7. Records saved and searchable.
   - What: every log, return, check and report is pushed to GitHub. A GitHub search or `git grep` finds the page by address, title or a word from its why. A built-in search or GUI is later, not MVP.
   - Who checks: Grok-Check.
   - Evidence: the pushed commits; the search command and its hits.
8. Fresh session finds the work and explains a decision.
   - What: a new model session, given only the page address, finds the closed page and explains why one decision was made.
   - Who checks: Matthew judges the answer. Codex checks it against the record.
   - Evidence: the session's answer with file:line cites; each cite opens to the right entry.
9. One worker per page enforced.
   - What: while a worker is actively working on a face (01, 04 or 05), that face is locked. A second worker's claim, face-write, draft, pack, check, signoff or close on that page is refused by wf. When no one is actively working, the page is not held. Another page runs in parallel at the same time.
   - Who checks: Grok-Check.
   - Evidence: the refusal texts; tests in 0423 pass; the parallel page's log shows it moved meanwhile.
10. Second-field trial.
    - What: after the 0498 run, one small non-code job (field picked by Matthew) runs through the same loop on the same grammar: page, faces, passes, board. Its own later 04NN page, so 0498 does not grow.
    - Who checks: Codex and Matthew.
    - Evidence: that page's log and board; a short list of any word or step that did not fit.
11. Matthew's go.
    - What: Matthew runs the 0498 walkthrough himself.
    - Who checks: Matthew.
    - Evidence: his go, hold or redo, recorded in docs/review (DIRECTOR-WORDS-t422.md:12).

## 5. Gaps, answered (t541u)

Each gap: the fact, the question, Prima's default at the time, Matthew's answer, and the effect. Verbatim answers are in docs/review/DIRECTOR-WORDS-t541-mvp-gaps.md.

G1. Which compute does the validating?  Resolved.
- Fact: wf does not use the core crate. Its only dependencies are serde_json and sha2 (wf Cargo.toml:12-14 on returns).
- Fact: the core has its own tool, `seqaddr validate` (crates/seqaddr-core/src/bin/seqaddr.rs:71).
- Fact: the roadmap moves WF inside the compute at stage 6 (ROADMAP-2026-11-18.md:102). The work board on the real compute is stage 7 (:107).
- Question: for the MVP, is "the compute" wf as it is today?
- Default: yes. wf is the compute for the MVP. Add one step that also runs `seqaddr validate` on the page and records the result. Moving wf into the core stays at stage 6.
- Answer (t541u, verbatim): "wf, plus one seqaddr validate step"
- Effect: the default stands. The 0498 walkthrough includes that validate step and records the result. The queue notes it on 0498. It is a walkthrough step, not a new wf command, unless a later design says otherwise.

G2. Is 0498 re-scoped to this MVP?  Resolved.
- Fact: 0498 done-when today is a box test, a walkthrough doc, and Matthew's run (STAGE-PLAN-90.50.10.md:351-357).
- Fact: the queue already adds "finding and understanding the saved record from a fresh session" (GROK-BUILDER-QUEUE.md:95).
- Question: does 0498's done-when become the criteria in section 4?
- Default: yes. Stage 1 closes only when section 4 passes. Criterion 10 may be its own page (see G4).
- Answer (t541u, verbatim): "Its part of our goals for MVP it's what we are aimign for."
- Effect: 0498 is the MVP target. Section 4 is its done-when. Criterion 10 stays on its own later page.

G3. Does "owns the whole page" cover pack-writing, checking and signoff?  Resolved.
- Fact: Matthew (t533u) said one worker per page at a time (DIRECTOR-WORDS-t533.md:5).
- Fact: Prima's reading and the earlier 0423 draft held the page only from claim to return (DIRECTOR-WORDS-t533.md:9).
- Fact: under that reading a packed, unclaimed pass is not held. A returned pass waiting for check is not held (:9).
- Fact: the checker enters after return. A check is refused while a claim is open (:11).
- Fact: Prima may stage later passes while a builder holds the page (:13).
- Fact: the earlier 0423 draft followed that reading (docs/design/drafts/90.50.10.0423/README.md).
- Difference: Codex's relay says the holder covers writing the pack, checking, reviewing and leading too (CODEX-MVP-t540.md:15).
- Difference: under that, Prima could not pack a later pass while a builder holds the page.
- Difference: two checkers could not check the same pass at once; today nothing stops that.
- Difference: the page would always have exactly one named holder, even between steps.
- Question: does every step hold the page (pack, build, check, signoff, close), or only the build?
- Default: every step holds the page. wf passes the page from holder to holder and the board names the holder. Widen 0423 to this before it is packed. Prima stops staging later passes while someone else holds the page.
- Answer (t541u, verbatim): "A worker only holds the page when they are activelly working on it. If it's being updated as 01 or more work on 05 or just the human readable version of the page's scope and design as 04. One model should be working on it at a time."
- Effect: neither the old t533 reading nor Codex's "always a named holder" stands as written. A page is held only while one worker is actively working on face 01, 04 or 05, and that face is locked. One model at a time. Between steps the page is not held. The 0423 draft is widened to that lock, and is still not packed. Prima may stage a later pass only when no one holds the page. Conflicts with the t533 pending-rule reading are flagged in the 0423 draft README. An open question remains: wf has no session-long hold for 01 or 04 today (`face-write` is one command). 0423 must not invent a new command; if a lasting 01/04 hold is needed, stop and raise it before packing.

G4. Is the second-field trial in the MVP?  Resolved.
- Fact: no current page or plan covers a non-code job (STAGE-PLAN-90.50.10.md:444-457 lists only wf pages).
- Question: in the MVP, or later? And which field?
- Default: in, kept small. One page after the 0498 code run, on a job Matthew picks (for example a body-shop job or a recipe). Its own page in the 04NN band, so 0498 does not grow.
- Answer (t541u, verbatim): "yes, small, after 0498"
- Effect: the default stands. The field and the page number are still open. The page is chosen when Matthew picks the field.

G5. Which Kanban board?  Resolved, with Q1 still open.
- Fact: `wf board` exists and is read only (wf src/lib.rs:45-46 on returns).
- Fact: the page board shows each pass's holder and next move ("held by ... next", wf src/board.rs:272).
- Fact: the book board (all pages) shows only counts per column. It shows no holder and no next move (board.rs:487-489).
- Fact: column names are still a pending question (WF-BOARD.md:132; board.rs:23-24).
- Question: is `wf board` the MVP board, with the book board fixed to show holder, step and next per page?
- Default: yes. A small wf page adds holder, step and next to each book-board line. Also answer WF-BOARD Q1: tool words as columns, body-shop words as side labels.
- Answer (t541u, verbatim): "wf board with holder, step and next"
- Effect: `wf board` is the MVP board. Pending page 0424, title book-board, adds holder, step and next to each book-board line. It is not packed in this turn. It is needed before the 0498 run. WF-BOARD Q1 (column names) was not answered and stays open.

G6. What does "searchable" mean for the MVP?  Resolved.
- Fact: wf has no search command (wf src/lib.rs:21-47 on returns lists every command).
- Question: is a plain search over the pushed records enough for the MVP?
- Default: yes. GitHub search or `git grep` over logs, returns and reports. A wf or core search command is later (roadmap stage 6 tools).
- Answer (t541u, verbatim): "GitHub is enough for now, we want it build into code for a gui I can sit at and use with models being able to see and use the Workshop manager. With pages as the cars and 05 as the workorders on them."
- Effect: GitHub (or `git grep`) is enough for the MVP. The GUI Workshop manager is the stated long-term direction, not MVP scope. In that manager, pages are the cars and 05 passes are the work orders.

G7. "Work order" means two things today.  Resolved.
- Fact: Matthew (t531u) called the report-system page itself a work order (GROK-BUILDER-QUEUE.md:15, before this update).
- Fact: the body-shop picture makes the page the car and each 05.NN a work order (CODEX-MVP-t540.md:13).
- Question: which name do we use?
- Default: the page is the job (the car). Each 05.NN pass is a work order. Fix the queue wording for 0422.
- Answer (t541u, verbatim): "It's the 05 face, 01 is the agents and scope, 04 is the planned out work we are doing on it. So the face must be locked while it's being worked on."
- Effect: a work order is a 05 pass, not the whole page. Face 01 is the agents and scope. Face 04 is the planned work. The face being worked on is locked. Queue wording that called 0422 a "work-order page" is corrected: 0422 is the report-system page; its 05 passes are the work orders.

G8. Do worker reports sent by wf count for the MVP?  Resolved.
- Fact: Matthew wants wf to send each worker's report (t527u). That build is page 0422, not packed yet (GROK-BUILDER-QUEUE.md:100).
- Question: must 0422 be done before the MVP run?
- Default: no. The stopgap report file (docs/plan/REPORTS.md) counts for the MVP. 0422 lands when it lands.
- Answer (t541u, verbatim): "no, the current report file is enough"
- Effect: the default stands. 0422 is not a blocker for 0498.
