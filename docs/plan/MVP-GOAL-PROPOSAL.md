# Workshop MVP goal: proposal for Matthew

state: proposal. Not a ruling. Matthew decides section 5.
made: 2026-11-23, about 1:00 PM EST, by Prima.
source: Codex's message, relayed by Matthew (t540u). Verbatim in docs/review/CODEX-MVP-t540.md.
pins: prima/build files at 14098406. wf kit files on `returns` at 231bbe79.

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
- MVP rule: "One worker at a time owns the whole page." (via Codex, :15)
- That holds "whether that worker is writing the pack, building, checking, reviewing, or leading." (via Codex, :15)
- "Independent pages can move in parallel." (via Codex, :15)
- "Finer-grained ownership is a later design question." (via Codex, :15)
- Prima puts "a real pack through the core." (via Codex, :17)
- "The compute validate as much as it can." (via Codex, :17)
- "The worker use the compute's guidance to continue." (via Codex, :17)
- Records are "saved, searchable, and understandable enough for a fresh person or model to pick up the work." (via Codex, :17)

Matthew's own words that back this:
- Matthew (0704 lab, labs/0704/MATTHEW-RESPONSES.md:11 on returns): "I want to see prima dropping packs through the core, with the compute checking and validing as much as it can."
- Same line: "All records being saved, searched and understandable."
- Matthew (0704 lab, MATTHEW-RESPONSES.md:6): "if a 05.03 is taken then go to 05.04".
- Matthew (t533u, DIRECTOR-WORDS-t533.md:5): "Once a worker is in a page, no other workers can use it."
- Same line: "We can run many pages in parralel but no more then one worker per page at a time."
- Matthew (t423u, DIRECTOR-WORDS-t423u.md:7): "With kanban style boards to integrate our kernel, pages, desk, faces, seqaddr designs."
- Same line: "So whys can be captured and reused to strengthen over time."

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
Workshop's MVP is one working shop on Matthew's PC, run with wf.
Prima drops a real pack.
The compute checks it and tells the worker the next step.
One worker at a time holds the page, and the compute refuses anyone else.
Each pass is a work order with its own counter.
A new pass never replaces an old one, and the record says why work continued.
The board shows each page's holder, step and next move.
Every record is saved in git and can be found and read cold.
A fresh session can find a closed page and explain why a decision was made.
The same loop works on one job from a second field.
Matthew runs it himself and says go, hold or redo.

## 4. Acceptance criteria

Each line says what must happen, who checks it, and the evidence.
"The run" means one real page taken from pack to close on Matthew's PC.

1. Real pack through the core.
   - What: Prima packs and publishes a real job page; the compute validates it before the worker claims.
   - Who checks: Grok-Check.
   - Evidence: the pack and publish-pack log entries; the validate output saved in the page record; the compute named (see gap G1).
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
   - What: the run needs a second pass (for example a failed check). The new pass gets the next counter. The first pass stays, with the reason.
   - Who checks: Codex.
   - Evidence: both 05.NN passes in the log; the first pass's failed check or signoff note gives the reason; no published entry rewritten.
6. Board shows holder, step and next.
   - What: during the run, the board shows each page's holder, column and next move.
   - Who checks: Matthew, by eye.
   - Evidence: `wf board` (book) and `wf board <page>` output saved at each step (see gap G5).
7. Records saved and searchable.
   - What: every log, return, check and report is pushed to GitHub. A plain search finds the page by address, title or a word from its why.
   - Who checks: Grok-Check.
   - Evidence: the pushed commits; the search command and its hits (see gap G6).
8. Fresh session finds the work and explains a decision.
   - What: a new model session, given only the page address, finds the closed page and explains why one decision was made.
   - Who checks: Matthew judges the answer. Codex checks it against the record.
   - Evidence: the session's answer with file:line cites; each cite opens to the right entry.
9. One worker per page enforced.
   - What: while a page is held, a second claim, and a check during a claim, are refused by wf. Another page runs in parallel at the same time.
   - Who checks: Grok-Check.
   - Evidence: the refusal texts; tests in 0423 pass; the parallel page's log shows it moved meanwhile (see gap G3).
10. Second-field trial.
    - What: one non-code job (field picked by Matthew) runs through the same loop on the same grammar: page, faces, passes, board.
    - Who checks: Codex and Matthew.
    - Evidence: that page's log and board; a short list of any word or step that did not fit (see gap G4).
11. Matthew's go.
    - What: Matthew runs the walkthrough himself.
    - Who checks: Matthew.
    - Evidence: his go, hold or redo, recorded in docs/review (DIRECTOR-WORDS-t422.md:12).

## 5. Gaps that need Matthew's decision

Each gap: the fact, the question, and Prima's default.

G1. Which compute does the validating?
- Fact: wf does not use the core crate. Its only dependencies are serde_json and sha2 (wf Cargo.toml:12-14 on returns).
- Fact: the core has its own tool, `seqaddr validate` (crates/seqaddr-core/src/bin/seqaddr.rs:71).
- Fact: the roadmap moves WF inside the compute at stage 6 (ROADMAP-2026-11-18.md:102). The work board on the real compute is stage 7 (:107).
- Question: for the MVP, is "the compute" wf as it is today?
- Default: yes. wf is the compute for the MVP. Add one step that also runs `seqaddr validate` on the page and records the result. Moving wf into the core stays at stage 6.

G2. Is 0498 re-scoped to this MVP?
- Fact: 0498 done-when today is a box test, a walkthrough doc, and Matthew's run (STAGE-PLAN-90.50.10.md:351-357).
- Fact: the queue already adds "finding and understanding the saved record from a fresh session" (GROK-BUILDER-QUEUE.md:95).
- Question: does 0498's done-when become the criteria in section 4?
- Default: yes. Stage 1 closes only when section 4 passes. Criterion 10 may be its own page (see G4).

G3. Does "owns the whole page" cover pack-writing, checking and signoff?
- Fact: Matthew (t533u) said one worker per page at a time (DIRECTOR-WORDS-t533.md:5).
- Fact: Prima's reading and the 0423 draft hold the page only from claim to return (DIRECTOR-WORDS-t533.md:9).
- Fact: under that reading a packed, unclaimed pass is not held. A returned pass waiting for check is not held (:9).
- Fact: the checker enters after return. A check is refused while a claim is open (:11).
- Fact: Prima may stage later passes while a builder holds the page (:13).
- Fact: the 0423 draft follows that reading (docs/design/drafts/90.50.10.0423/README.md:3).
- Difference: Codex's relay says the holder covers writing the pack, checking, reviewing and leading too (CODEX-MVP-t540.md:15).
- Difference: under that, Prima could not pack a later pass while a builder holds the page.
- Difference: two checkers could not check the same pass at once; today nothing stops that.
- Difference: the page would always have exactly one named holder, even between steps.
- Question: does every step hold the page (pack, build, check, signoff, close), or only the build?
- Default: every step holds the page. wf passes the page from holder to holder and the board names the holder. Widen 0423 to this before it is packed. Prima stops staging later passes while someone else holds the page.

G4. Is the second-field trial in the MVP?
- Fact: no current page or plan covers a non-code job (STAGE-PLAN-90.50.10.md:444-457 lists only wf pages).
- Question: in the MVP, or later? And which field?
- Default: in, kept small. One page after the 0498 code run, on a job Matthew picks (for example a body-shop job or a recipe). Its own page in the 04NN band, so 0498 does not grow.

G5. Which Kanban board?
- Fact: `wf board` exists and is read only (wf src/lib.rs:45-46 on returns).
- Fact: the page board shows each pass's holder and next move ("held by ... next", wf src/board.rs:272).
- Fact: the book board (all pages) shows only counts per column. It shows no holder and no next move (board.rs:487-489).
- Fact: column names are still a pending question (WF-BOARD.md:132; board.rs:23-24).
- Question: is `wf board` the MVP board, with the book board fixed to show holder, step and next per page?
- Default: yes. A small wf page adds holder, step and next to each book-board line. Also answer WF-BOARD Q1: tool words as columns, body-shop words as side labels.

G6. What does "searchable" mean for the MVP?
- Fact: wf has no search command (wf src/lib.rs:21-47 on returns lists every command).
- Question: is a plain search over the pushed records enough for the MVP?
- Default: yes. GitHub search or `git grep` over logs, returns and reports. A wf or core search command is later (roadmap stage 6 tools).

G7. "Work order" means two things today.
- Fact: Matthew (t531u) called the report-system page itself a work order (GROK-BUILDER-QUEUE.md:15).
- Fact: the body-shop picture makes the page the car and each 05.NN a work order (CODEX-MVP-t540.md:13).
- Question: which name do we use?
- Default: the page is the job (the car). Each 05.NN pass is a work order. Fix the queue wording for 0422.

G8. Do worker reports sent by wf count for the MVP?
- Fact: Matthew wants wf to send each worker's report (t527u). That build is page 0422, not packed yet (GROK-BUILDER-QUEUE.md:100).
- Question: must 0422 be done before the MVP run?
- Default: no. The stopgap report file (docs/plan/REPORTS.md) counts for the MVP. 0422 lands when it lands.
