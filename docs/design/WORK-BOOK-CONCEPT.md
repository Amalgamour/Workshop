# The work book: a concept to read before we go ahead

For Matthew. By Designer. A concept, not a ruling. Nothing here is decided. Only you approve.
created: Mon 16 Nov 2026, 4:58 PM EST (e6a0f39)

## Change note (Mon 16 Nov 2026, 5:55 PM EST)

Fixes from Tester's check (docs/review/WORK-BOOK-CONCEPT-CHECK.md, 093c64a). Only findings that checked out in the code or files:
- The board already exists, tail only (crates/seqaddr-core/src/state.rs:296-300). w02 now adds columns to it.
- Pack 1 is the first real use of the claim route on an open door. "No new way in" is gone.
- Pack 1 is a named bootstrap exception: hand-written, entered as `pack` with no check, its sheet shape in code. Each needs your `7`.
- W10: the claim holder sends the return, not the compute (state.rs:563-571). books/ is tracked in git today.
- W8, W11: Tester's options and spec conflicts added; W11 holds proposed change-note text for seqAddr.md:197-198 and workflow-loop.003.md:160 (those files are not edited). W9-W13 now show Tester's check.
The pack, sheet and return shapes are in docs/design/PACK-TEMPLATE.md.

## Change note (Mon 16 Nov 2026, 5:07 PM EST)

Revised for your answers to the six changes (t226u, recorded at docs/review/DIRECTOR-WORDS-t226u.md, ceec44f), and for your t227u words on handing jobs to the compute (docs/review/DIRECTOR-WORDS-t227u.md, f52debb).
- Built on what our design files already have: counter tails, the dev / jobs / lab pages, the return shape. Every cite was opened and checked.
- One surprise from the code: today's compute already claims a pack and moves its tail one step, through the gate. Prima's note said it could not. So the first build is smaller than planned.
- One conflict found: a stored "05.00 board" is not allowed by R9 (faces have no doors). The board becomes a view.
- t227u: the compute fills the pack template and the handoff sheet, and your prompt box comes from that sheet. There is now one first pack: the handoff sheet and the board, both read-only.
- Questions updated. The ones your answers settle are shown as "answered in t226u".

**How to read the cites.**
- "t223u:N", "t226u:N" and "t227u:N" are lines of your recorded words: docs/review/DIRECTOR-WORDS-t223u.md (2461a19), docs/review/DIRECTOR-WORDS-t226u.md (ceec44f), docs/review/DIRECTOR-WORDS-t227u.md (f52debb).
- OWB means "old work book (zip from Matthew)", a path inside 10.10.13.brand-clerk. It stays outside the repo.
- AX is Tester's axiom check, docs/review/WORK-BOOK-AXIOM-CHECK.md (c5cbf0d). SPEC is docs/design/WORK-BOOK-SPEC.md (6bcc1c0).
- EXISTS TODAY, PLANNED, and proposal (7). `9` means untried.

---

## What you asked for

"I want the concept I can read before we go ahead." (t223u:14)

"Does this make a solid base for running our work? What changes would you make?" (t223u:16)

Short answer: yes. Six changes were proposed, and you said yes to all six (t226u:7-17). Most of what they need is already in our design. Some of it already runs.

## Where the work lives

Your words: "you'll host it on github then when you give the instruction prompt for me to que up the model. It can go pull down the files it needs locally. Because you don't have access to my local files." (t223u:6)

- The code and the books live on GitHub.
- Prima writes a short prompt. You paste it to start the model.
- The model pulls what it needs onto your machine.

## Three pages per piece of work

Your words: "I did like how we had a dev page, a work page and a lab page all linked together." (t226u:7)

Our workflow already has this (workflow-loop.003.md:40-49):
- **Dev page**, 04NN. The design: what the work is and what it must prove. (Side label: N4 dev.)
- **Jobs page**, 05NN. The packs and returns. (Side label: N5 jobs.)
- **Lab page**, 07NN. Cold trials of the work. (Side label: N7 colab.)
- A build page, 03NN, can hold the finished modules (N3 build, :44).

They share the same last two digits. Example: 0401, 0501, 0701 (workflow-loop.003.md:59). Under the proposed F.2 rule they also link to each other both ways (:60).

This replaces the old book's seven matched pages (OWB, 00.md:26-36).

## A pack is the job

Your words: "You write a pack. It goes into the page 05.NN next open counter. Then in the pack is the jobs list, the model then returns what it did on each." (t223u:8)

- Prima writes the pack on the jobs page.
- It goes in the next free slot: 05.01, then 05.02. (Side label: a counter.)
- The pack lists the jobs.
- The model answers each job in its return.

## Tails: how a pack moves

Your words: "Mostly look up how tails work. I think it's in the sequence addressing .md" (t226u:7)

It is. Each pack slot carries one word for where it is (seqAddr.md:128-137):
- **draft**: being written.
- **pack**: ready to run.
- **open**: a model is working on it.
- **return**: the model has handed back.
- **review**: being checked.
- no word: closed.

"Workflow state lives only on counters." (seqAddr.md:140)

Tails move one step at a time. The code refuses a skip (crates/seqaddr-core/src/tail.rs:79-91).

When a pack closes, it gets an outcome: passed, failed, blocked, needs-authority, or abandoned (workflow-loop.003.md:166; what each means, :201).

When a model takes a pack, the claim records who, when, and an id (workflow-loop.003.md:206).

## The compute fills the status

Your words: "Yes I agree, can we make that work now? I wasn't sure we could do it at this stage, but yes the workshop design is for this workflow to be fully automated with compute doing status and prompting models to work. We use prompts between model and compute to run the work. This is a forunning to that system." (t226u:9)

The tail is the status. Nobody types it. The old book shows why: pack 05.16 says "state: ready" while its return says "state: complete" (OWB, 0501.brand-clerk/05.16.md:6; 0101.brand-clerk/05.16.return.md:3).

**EXISTS TODAY** (checked in the code, not only the plan). Through the gate (/propose, op "tail"):
- A model claims a pack: pack -> open. The first claim wins; the claim is recorded (crates/seqaddr-core/src/state.rs:543, :561). Eight racing claims give one winner (crates/compute/tests/http.rs:134).
- The model returns: open -> return, and the return text is kept on the same counter (state.rs:575).
- A reviewer takes it: return -> review. The builder cannot review its own work (state.rs:581; http.rs:139).
- The reviewer asks the compute to close it, with an outcome (/close, crates/compute/src/store.rs:979-995).

**Not there yet.**
- **draft -> pack.** Only the compute may make this move (state.rs:548), and the compute has no route to do it. Today a pack can be written straight in as "pack", which skips the check (crates/seqaddr-core/src/tail.rs:95-99).
- **The board, in full.** A board already exists: the compute lists every slot on a face with its tail, built fresh, never stored (crates/seqaddr-core/src/state.rs:296-300). Asking for a plain 05 face returns it (crates/seqaddr-core/src/resolve.rs:182-188; test crates/seqaddr-core/tests/tails.rs:219-226). It shows the tail only: no claim, reviewer or outcome. (Found by Tester.)
- **Prompting models.** Not built. This book is its forerunner, in your words.

**The board must be a view.** seqAddr.md:197 calls "FF.00" the board. But you ruled "Faces do not have sentinels" (R9, DIRECTOR-RULINGS.md:37-38), and the code refuses FF.00 (state.rs:530). So the board cannot be a stored 05.00. Proposal (7): the compute shows it as a view, built from the log. (W11)

## The compute hands out the job

Your words: "We want to use the tools and compute when you make the tools. I want you to use them and make the workers use them. I think we have a basic idea of a tool to do this. But you should hand the jobs to the compute, It basically gives you a constand template that won't drift. Otherwises you will." (t227u:5)

In plain words:
- Prima hands each job to the compute.
- The compute puts it in a fixed shape. The shape does not drift. Prima, writing by hand, would.
- Prima and every worker use these tools once they exist.

**The idea is already in our workflow.**
- "Compute uses templates for packs, work cards and returns." (workflow-loop.003.md:232). The templates are not seated yet (same line, "`7`").
- You ruled it too: "The compute fills templates, bindings, and hashes, and the model writes only the judgment." (R37 item 3, DIRECTOR-RULINGS.md:197)
- The check step moves a pack from draft to pack only if it fits its template (workflow-loop.003.md:171; what it checks, :234-245).
- Before each handoff, the compute builds a read-only sheet from the live records: the approved design, the grant, the pack, earlier returns, the source commits, blockers, what must be read, the done criteria, and when to stop (workflow-loop.003.md:220). (Side label: handoff manifest.)
- The board shows each pack as one card, in the column of its tail. The compute records each handoff, and "The board derives its current view from that history." (workflow-loop.003.md:160)
- It was tried before. The old Workshop had a pack-lint page, worked by Grok Builder ("who: grok-builder", OWC 01.md:5). It held returns only: "Not the lint command. That command is a later pack." (OWC 01.md:26). Its returns show the drift you warn about: a return file says "This file is 05.01.pack.md. It is ready." (OWC 05.01.return.md:21). OWC is the old Workshop clone (Amalgamour/Librarian, branch rebuild, de3b8eb), 10.workshop/10.10.work/10.10.12.rebuild/0117.pack-lint.

**So:**
- The compute fills the pack template and the handoff sheet.
- The prompt box Prima gives you is printed from that sheet. Prima does not hand-write it.

**What exists and what is planned.**
- EXISTS TODAY: the tail rules (crates/seqaddr-core/src/tail.rs:79-99). The claim and the one-step tail move, through the gate (state.rs:543-581; http.rs:134-139). The reviewer's close (store.rs:979-995).
- PLANNED: the templates (seated as kernel card types, workflow-loop.003.md:232), the check step (draft -> pack), the handoff sheet, the board's claim, reviewer and outcome columns, and printing the prompt box. The tail-only board EXISTS (state.rs:296-300).

## The first real work pack (proposal, 7)

One first pack, not two. It joins the t226u idea (show the board) and the t227u idea (the compute fills the handoff sheet).

**Why this piece.** The claim and the tail move already exist, so they need no pack. The template check needs templates, and those are not seated yet (workflow-loop.003.md:232). The handoff sheet and the board only read what the compute already holds. They write nothing. And they give you the thing you asked for first: a prompt box the compute makes.

**Pack 1: the handoff sheet and the board.** For Cursor or Grok Builder.
- **w01, handoff sheet:** a read-only route that, for one pack slot, prints a fixed-shape sheet: the pack text, its tail, who holds the claim, the matching dev and lab pages, earlier returns on the slot, and the prompt box text. Any field the compute cannot fill yet (approved design, grant, start commit) says "not available". It is never guessed (R37: "Couldn't look" is kept separate from "isn't there", DIRECTOR-RULINGS.md:200).
- **w02, board:** add claim, reviewer and outcome to the board that already exists (state.rs:296-300). Still built from the log, never stored (R9; W11).
- **Crates and files:** crates/compute/src/lib.rs (one route), crates/compute/src/store.rs (the reads), crates/seqaddr-core/src/state.rs (board columns), crates/compute/tests/ (one new test file).
- **Bootstrap exception (needs your `7`).** Pack 1 cannot pass through the tool it builds. So: its text and AGENTS.md are written by hand; it goes in as `pack` with no check step (tail.rs:95-99); and the sheet's shape lives in code until the template is seated (W13). Proposal (7): one named, one-time override, ending when the templates are seated.
- **Tests:** walk a pack draft -> pack -> open -> return -> review -> closed. The board shows the right tail at each step. The sheet shows the claim owner after the claim. The same slot always gives the same sheet. A missing dev page shows "not available". A face with no slots answers "missing".
- **Done-check:** cargo test --workspace passes, with the new tests. The reviewer checks that no test was removed, and that the routes write nothing.
- **AGENTS.md, short:** Goal: the compute prints the handoff sheet and the board. Why: t227u:5, t226u:9. May touch: the three paths above. Must not touch: books/, kernel/, docs/. Stop if: a field needs a stored 05.00 (R9), or a write. Hand back: per job, what was done and created, proof (commit, test output), what it did not do, what it noticed, then unprompted and overflow.

**Next packs, later.**
- Pack 2: seat the pack, work card and return templates as kernel card types (workflow-loop.003.md:232). (W13)
- Pack 3: the check step, draft -> pack, by the compute (:171). It writes as the compute.

**Risks from the open door** (CORE-AND-TOOLS-SPEC.md B1, B6). Pack 1's routes only read. But Pack 1 is the first real use of the claim route while the door is open (found by Tester). And the sheet and the board will show what is in the books, and today the books can be faked:
- The token file sits in books/ (crates/compute/src/store.rs:297). Anyone with a shell on the box can add a token and claim a pack.
- A line written straight into a book is loaded at start. A forged claim would show on the board as real (CORE-AND-TOOLS-SPEC.md B1).
- A lost reply can double a change (CORE-AND-TOOLS-SPEC.md:342). For a claim, a retry is refused, but the caller cannot tell "mine" from "someone else's".
- Proposal (7), from Tester: label every sheet and board "door open: not proof" until K8 step 1 lands.

**Wait for K8 step 1, or go first?** Proposal (7): Pack 1 goes first, because its routes only read, with the label above and the bootstrap exception. Packs 2 and 3 wait for K8 step 1, because Pack 3 writes as the compute. (W12)

## What a return must say

Your words: "Yes returns, must state what was done, what was created, what the model noticed, an unprompted and overflow from the model should be captured for review at the end of the return. After the job items." (t226u:11)

Our workflow already has most of this (workflow-loop.003.md:189-193). A return, in order:
1. Each job: done, blocked, or needs something. (:189)
2. What was done.
3. What was created: exact file paths.
4. Proof: the commit, and the test output. (Prima's change 3; also :189)
5. What it did not do. ("Every packet says what it gathered and what it didn't", R37, DIRECTOR-RULINGS.md:204)
6. What the model noticed.
7. Then, at the end: **unprompted** and **overflow**, for review. (:193)

## Where AGENTS.md fits next to the pack (W2)

- The pack is the job list. It is the source (t223u:8).
- AGENTS.md is the sheet the model reads first (SPEC B2).
- Proposal (7): the compute makes AGENTS.md from the pack and the dev page. The model never edits it.

## The other three changes: your yes

- **Each pack names its exact starting commit on GitHub.** "4. Yes" (t226u:13). Your local path goes only in the queue-up prompt.
- **Receipts become lines in the one log.** "5. Yes." (t226u:15)
- **A real gate.** "6. Yes." (t226u:17). That is K8 step 1 (CORE-AND-TOOLS-SPEC.md:873).

## How it ties to the core spec

- "Yes, books change through compute not by models." (R33, DIRECTOR-RULINGS.md:159). See W10.
- The open door: K8 step 1 (CORE-AND-TOOLS-SPEC.md:873, B1).
- "Refuse with a handback, and stop rather than invent a meaning." (R37, DIRECTOR-RULINGS.md:202)

---

## Open questions, top three first

Proposed answers only. The top three are W8, W9 and W10. W8 must be ruled before the first work page exists, because page type is locked once set (R36, DIRECTOR-RULINGS.md:190; AX:33-34).

### W8 (TOP). Is a work page a system page?
1. **Question.** System pages freeze once linked (R34, DIRECTOR-RULINGS.md:170). Is a work page one?
2. **Proposed answer (Designer and Tester).** No. You read work pages. Tester's added option: seqAddr.md:192 already lists a page type `workflow`. It is not system, so the R34 freeze would not apply, but no ruling says whether it locks (7) (WORK-BOOK-CONCEPT-CHECK.md:39-44). System pages are not for users (DIRECTOR-RULINGS.md:169).
3. **Why.** A wrong pack can then be fixed in place. Who gets hurt otherwise: you.
4. **Axioms checked (AX:31-32).** 1 [Axioms.md:13] pass. 2 [Axioms.md:15] pass. 7 [Axioms.md:25] pass. 9 [Axioms.md:29] tension. The spec also marks 6 [Axioms.md:23] pass (SPEC:394).

### W9 (TOP). Is the return a step on the same slot, or a separate file?
1. **Question.** You said yes to pack and return side by side (t226u:7). Should the return live on the same counter as the pack, as its "return" step, or as its own 05.NN.return file?
2. **Proposed answer (Designer, 7).** The same counter. That is how the workflow plans it (workflow-loop.003.md:181) and how the code does it today (state.rs:575). The return body is written on the same tail move as open -> return, so it is one change (state.rs:575; R37 item 2, DIRECTOR-RULINGS.md:196). An export can still show it as two files side by side. Seating this placement is still open in the workflow (:181, "`7`").
3. **Why.** One slot, one history. A return and its pack cannot drift apart. Who gets hurt otherwise: a reviewer matching files by hand.
4. **Axioms checked (Designer's marks; Tester checked, WORK-BOOK-CONCEPT-CHECK.md).** 2 [Axioms.md:15] pass: no second copy. 6 [Axioms.md:23] pass: the pack stays in the log below the return. 8 [Axioms.md:27] pass. 9 [Axioms.md:29] tension: the placement is not yet seated.

### W10 (TOP). Does a pushed return count as a book change?
1. **Question.** You said the model will "commit and push" (t223u:10). R33 says "books change through compute not by models" (DIRECTOR-RULINGS.md:159). Does a push count as a book change?
2. **Proposed answer (Designer, 7).** No, as long as the push holds only code and proof, never books/ and never the return text. The model that holds the claim sends the return once, through the gate (open -> return, which exists today), naming the commit. The compute returns only in recovery (state.rs:563-571). Git keeps only the commit hash. Today books/ is tracked in git, so "never books/" needs a check that refuses such a push (7) (found by Tester).
3. **Why.** It keeps your push-and-check flow and R33 both. Who gets hurt otherwise: you, if a push quietly changes a book.
4. **Axioms checked (Designer's marks; Tester checked, WORK-BOOK-CONCEPT-CHECK.md).** 1 [Axioms.md:13] pass. 6 [Axioms.md:23] pass. 8 [Axioms.md:27] pass. 2 [Axioms.md:15] pass: one copy of the return. 1 [Axioms.md:13] tension (Tester): no check on push yet. 6 [Axioms.md:23] tension (Tester): a relayed return names the wrong builder.

### W11. Is the board a view, not a stored 05.00?
1. **Question.** seqAddr.md:197 calls FF.00 the board, but R9 says faces have no doors (DIRECTOR-RULINGS.md:37-38). Is the board a view the compute builds?
2. **Proposed answer (Designer, 7).** Yes. Never stored. Built from the log each time.
3. **Why.** It keeps R9 and still shows status. It is already built that way, tail only (state.rs:296-300). Spec conflict to write down, not leave silent (Tester): seqAddr.md:197-198 and workflow-loop.003.md:160 still name a 05.00 board; R9 governs. Who gets hurt otherwise: you, if a stored board and the slots disagree.
4. **Axioms checked (Designer's marks, 9).** 2 [Axioms.md:15] pass: no copy. 8 [Axioms.md:27] pass: "a menu ... never becomes what it points to". 1 [Axioms.md:13] pass: your R9 stands.
   **Proposed change-note text (7), for the spec owners to add after your yes. This file does not edit either spec:**
   - For docs/spec/seqAddr.md:197-198: "Change note. R9 (DIRECTOR-RULINGS.md:37-38): faces have no sentinels, so FF.00 does not exist. A face is counted by kernel rule (policy), not by FF.00. The board is a view the compute builds from the counters; it is never stored. A counter on a counted face is valid without a board entry."
   - For docs/spec/workflow-loop.003.md:160: "Change note. Read "the N5 05.00 board" as the board view of N5 face 05. Per R9 there is no 05.00. The compute builds the view from the counters and their recorded handoffs (crates/seqaddr-core/src/state.rs:296-300)."

### W12. Which piece goes first, and does it wait for K8 step 1?
1. **Question.** Should the first pack be the read-only handoff sheet and board, ahead of the template check, and ahead of K8 step 1?
2. **Proposed answer (Designer, 7).** Yes. The claim route already exists. The templates are not seated. The sheet and the board only read. The template check comes after the templates and after K8 step 1.
3. **Why.** You get a compute-made prompt box first (t227u:5). Its routes add no write path, but it is the first real use of the claim route on an open door (Tester). Who gets hurt otherwise: you, waiting on templates for status you could have now; or you, if a writing route opens before the door narrows.
4. **Axioms checked (Designer's marks; Tester checked, WORK-BOOK-CONCEPT-CHECK.md).** 1 [Axioms.md:13] tension: the door is still open for the claim route that exists. 2 [Axioms.md:15] pass: the sheet is derived, not a copy. 7 [Axioms.md:25] pass: missing fields say "not available". 9 [Axioms.md:29] pass: each pack gets its own review.

### W13. Are the templates seated in the kernel before the check step?
1. **Question.** The pack, work card and return templates are proposed as kernel card types, still `7` (workflow-loop.003.md:232). Seat them before building the check step?
2. **Proposed answer (Designer, 7).** Yes. Seat them through the kernel's drafting path first, with the handoff sheet shape in the same set (Tester). Pack 1's code shape is the one named exception above. The check step then reads the seated template, not a copy in code.
3. **Why.** A template in code is a second copy that can drift, which is what you warned about (t227u:5). Who gets hurt otherwise: every worker, checked against a shape nobody approved.
4. **Axioms checked (Designer's marks; Tester checked, WORK-BOOK-CONCEPT-CHECK.md).** 2 [Axioms.md:15] pass: one shape, inherited. 1 [Axioms.md:13] pass: you approve the template. 9 [Axioms.md:29] tension: untried.

## Answered in t226u (your words, not rulings)

- **Pack and return side by side.** "yes we are compressing the idea now." (t226u:7). Where the return sits is W9.
- **The compute fills status.** "Yes I agree, can we make that work now?" (t226u:9). See "The first real work pack".
- **Returns carry proof.** "Yes returns, must state what was done, what was created, what the model noticed ..." (t226u:11).
- **Starting commit, one log, a real gate.** "4. Yes", "5. Yes.", "6. Yes." (t226u:13-17).

## Still open for you to confirm (from t223u)

- **W1, a real book?** You: "It goes into the page 05.NN next open counter." (t223u:8). Tester: 1 tension; 2, 6, 7 pass (AX:12-14).
- **W2, where AGENTS.md lives.** You: "in the pack is the jobs list" (t223u:8). Tester: axiom 2 tension; R33 item 2 tension (AX:19-25).
- **W3, who releases.** You: "the scope and authority coming from you" (t223u:8). The spending cap is open. Tester: 1, 6 pass; 3 pass only with a written grant (AX:40-42).
- **W6, who checks.** You: "you check the work, or assign a review bot" (t223u:12). The code already stops a builder reviewing its own return (state.rs:581). Tester: 9, 1, R20, R2 pass (AX:64).
- **W7, your local space.** Please name the folder. Tester: 1, 6, 7 pass; 2, 8 tension (AX:70-74).
- **"6" and "8".** You wrote "6 framing the work, with 8 returning the record" (t223u:8). In Axioms.md frame is axiom 5 [Axioms.md:21]. What did you mean?

## Not settled by your answers

### W4. Cursor or Grok Builder for a page?
1. **Question.** You queue up the model (t223u:6). Who picks which one?
2. **Proposed answer.** If a test can check the job, the cheaper builder goes first. Two fails: stop and hand back (SPEC B4).
3. **Why.** A test lets a cheap try fail safely. Who gets hurt otherwise: you, paying twice for one miss.
4. **Axioms checked (AX:49-50).** 3 [Axioms.md:17] pass. 4 [Axioms.md:19] pass. 9 [Axioms.md:29] tension. R37 item 8 pass.

### W5. Do we record what each job cost?
1. **Question.** Should each return record time, tries, tokens and dollars?
2. **Proposed answer.** Yes, when reported. "Not reported" is not "zero".
3. **Why.** R37 item 6 (DIRECTOR-RULINGS.md:200). Who gets hurt otherwise: you, reading a blank as free.
4. **Axioms checked (AX:58).** 7 [Axioms.md:25] pass. 9 [Axioms.md:29] pass.

---

## Prima's summaries and your words

**t226u (this revision).**
- "All six are yes": true. Each item starts with "yes" or "Yes" (t226u:7-17).
- Your item 1 is a hedged pointer: "I think this is in there for how workflow should work. as least some starting point for it." (t226u:7). It held: tails, bands and the return shape are all there.
- Prima's note said today's compute has no route that moves a tail or records a claim. The code says otherwise: /propose with op "tail" does both (state.rs:543-575; http.rs:134-139). Only draft -> pack and a board view are missing.
- Prima's "05.00 board" meets R9, which forbids FF.00 (W11).

**t227u.**
- Prima's summary: the compute hands out the jobs from a fixed template. Your words: "you should hand the jobs to the compute, It basically gives you a constand template that won't drift. Otherwises you will." (t227u:5). So Prima hands jobs to the compute, and the compute gives Prima the fixed shape. The drift you name is Prima's ("Otherwises you will").
- Prima's summary: Prima and every worker must use the tools once they exist. Your words: "We want to use the tools and compute when you make the tools. I want you to use them and make the workers use them." (t227u:5). This matches. You add that Prima makes the tools.
- You also say "I think we have a basic idea of a tool to do this." (t227u:5). It is in workflow-loop.003.md section 8 and S06.
- Prima's note marks the claim and tail-move route PLANNED. The code has it today (state.rs:543-581).

**t223u (kept from the first draft).**
- "for you to check the work on Github" (t223u:10) and "you check the work, or assign a review bot" (t223u:12): "you" is Prima, not you.
- "YOu can pull the work and have cursor do the finally assembly on my computer" (t223u:10): Prima pulls; Cursor assembles.
- "6" and "8" are not called axioms in your words.
