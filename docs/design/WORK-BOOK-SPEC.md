# Work book: how work is given out

Draft by Designer, for Matthew (Director). Not a ruling. Nothing here closes a question.
created: Mon 16 Nov 2026, 2:56 PM EST (Designer)

## Change note (Mon 16 Nov 2026, 2:56 PM EST)

New file. Asked in Prima's relay at 2:55 PM EST. It describes a book for giving out work. Each work page is one job for Cursor or Grok Builder. Tester's research (docs/review/WORK-BOOK-RESEARCH.md, ab152b6) landed while this was drafted; it is folded in (Part D and marked lines). Tester calls the product "Grok Build" (docs/review/WORK-BOOK-RESEARCH.md:1, :63); the old work book called the role "Grok Builder". This file uses "Grok Builder" for the role.

**How to read the cites.**
- A cite with no prefix is this repo, branch `build`.
- `LIB:` means the earlier Workshop: repo `Amalgamour/Librarian`, branch `workshop`, at commit 960d20c, cloned read-only at `/workspace/librarian-review/repo` (CODEX-LIBRARIAN-TOOLS-REVIEW.md:7, :15).
- `LIB:W/` is short for `LIB:00.kernel/00.00.10.work/`.
- Labels: EXISTS TODAY, PLANNED, and NEW (proposal). `7` means open. `9` means untried.

---

## Part A. In plain words

**What Matthew asked for.** I searched DIRECTOR-RULINGS.md, docs/review/ and docs/BUILD-LOG.md for "Grok Builder", "work page", "agents.md" and "book for giving out work". None of them holds his words for this request. So the request below is **quoted as relayed by Prima**, not in his own words:

> the workflow system is set up as a book for giving out work. Each work page is one piece of work he can hand to Cursor or to Grok Builder. Each work page carries an agents.md saying what the model needs to know and which files to read for that page. Grok Builder is built back into the Workshop design because it is cheap.

**His own earlier words that come close** (from the earlier Workshop, quoted exactly, spelling kept):
- On cheap models: "Yes that is where cheap models come it. We don't have to just haev compute. I see it executing prompts on it's own before handing work back. Likely we can get the cheap models to over perform once the compute is working right. ... You can give compute work, the compute gets the cheap compute to do it, if it's wrong it does it again. We need to start a page on this. How we plan to break up work." [LIB:W/0413.assistants/06.01.md:11]. He does not name Grok here.
- On stamping the agents file: "Agreed, AGENTS.VVV needs to be stamped just like our faces. we stamp them in the header. So we now what model did the work when what version we are on." [LIB:W/0409.decisions/01.md:168].
- On books: "Yes, books change through compute not by models." [DIRECTOR-RULINGS.md:159].

**The idea, in short.**
1. There is one book whose pages are jobs. It is called the work book.
2. One work page is one job. It is small enough to hand to one builder.
3. Each work page carries a short `AGENTS.md`. It tells the builder what to know, what to read, what it may touch, how to tell it is done, and what to hand back.
4. The builder works in the code, not in the books. Books change only through the compute.
5. When the builder finishes, it hands back a return. A different view checks it before anything is accepted.

**Grok Builder has been here before.** The earlier Workshop had a work book called `00.00.10.work`. Its first job was "Work-book first use and Grok Builder onboarding" [LIB:W/0118.workflow-start-0501/return.md:1]. Grok 4.7 sat as Builder for a scoped job [LIB:W/0408.seats/01.md:19]. 16 returns there name Grok Builder (git grep, LIB at 960d20c). In this repo, Prima's review notes the old desk core was built by the "grok.com builder" (CODEX-LIBRARIAN-TOOLS-REVIEW.md:211). So this design brings it back. It is not new.

---

## Part B. The parts

### B1. What a work page is

**In plain words.** One job, one page. The page says what the job is for. It points at the files. It holds the builder's return.

**EXISTS TODAY (in our spec, not built).** The workflow already has this shape. N4 "states the work ... Written on face 04, with an agents.md-style face 01 to go with it" [workflow-loop.003.md:87]. A pack is "an agents.md-style build list for a builder" [workflow-loop.003.md:99]. Work cards are `w01`, `w02` [workflow-loop.003.md:122]. Every page in the kernel already has an MVP pack on face 05.02 (for example kernel/00.00.00/00.00.00.0057.05.02.md:17).

**EXISTED BEFORE (LIB).** Each old work page had an assignment, a scope, a release, a claim and a return [LIB:W/0118.workflow-start-0501/return.md:14-80]. Files it was expected to make were listed in `reservation.json` (`expected_outputs`) [LIB:W/0118.workflow-start-0501/reservation.json]. The return was "Did / Blocked / Need" [LIB:W/0101.app-entry-0506/return.md:34-38].

**NEW (proposal, 7).** A work page is an ordinary page in the work book. Its face 04 is the job in plain words. Its faces 01 and 05 are printed as the job's `AGENTS.md` (B2). Its face 05 holds the returns, one counter each (05.01, 05.02). Its face 09 holds who claimed it and when. The book's address is not chosen here (W1).

**Three checks (claims, 9).**
- **Axioms:** 2 [Axioms.md:15] pass: a work page is the same shape as any page. 5 [Axioms.md:21] pass: the page frames the job: what, why, where to stop, what done is.
- **Better:** better than the old work book, where a page was a folder of loose files (return.md, reservation.json, receipt.json) [LIB:W/0118.workflow-start-0501/]. Here it is one page with faces.
- **Three leads:** Person: releases the job. Model: does the job. Compute: keeps the page and checks the done-check.

### B2. The AGENTS.md for a work page

**In plain words.** A short sheet the builder reads first. Six parts, always in this order. It is named `AGENTS.md` in capitals: Grok Build's list of names has no all-lowercase `agents.md`, and both builders read `AGENTS.md` (docs/review/WORK-BOOK-RESEARCH.md:11, :15-16).

**NEW (proposal, 7).**

| Part | What it holds | Rule |
|---|---|---|
| 1. Goal | One or two sentences: what this job is for, and why | Frame the work to the spirit of the goal [Axioms.md:21] |
| 2. Must-know rules | Only the rulings and axioms this job touches, quoted with their line | Quote, never summarise a ruling |
| 3. Files to read | Exact paths, with line ranges where it helps | No folders, no "and so on" |
| 4. Files it may touch | Exact paths or path patterns. Everything else is read-only | Same as the pack's `grant` [workflow-loop.003.md:112] |
| 5. Done-check | A command or a short list that says yes or no | Same as the pack's `outcome` [workflow-loop.003.md:109]; a test is best |
| 6. Hand back | Did / Blocked / Need, the commit SHA, the done-check output, and what it did not do | R37 items 8 and 10 [DIRECTOR-RULINGS.md:202, :204] |

Two extra lines go in the header:
- `stop if`: where the builder stops and raises [workflow-loop.003.md:111].
- A stamp: who wrote this AGENTS.md, when, and its version. Matthew asked for this kind of stamp for AGENTS files [LIB:W/0409.decisions/01.md:168].

**How it is given to the builder.** NEW (proposal, 7, matching Tester's best option, docs/review/WORK-BOOK-RESEARCH.md:17-19, :109-116): the compute makes `AGENTS.md` from the page's face 01 and the one face 05 pack for this job, as an export. It writes it at the root of a fresh worktree, one job per worktree, because both builders always load a root file and nest by where the code is, not where the task is (docs/review/WORK-BOOK-RESEARCH.md:138-142). The builder never edits it. If it thinks the sheet is wrong, it says so in its return.

**Size (from Tester, docs/review/WORK-BOOK-RESEARCH.md:132-136).** Root `AGENTS.md` under 40 lines. Job `AGENTS.md` under 150. Rulings are linked, not pasted: both builders open a linked file when they need it (docs/review/WORK-BOOK-RESEARCH.md:32-34, :79-80).

**Three checks (claims, 9).**
- **Axioms:** 5 [Axioms.md:21] pass: goal, where, what to do, where to stop, what done is. 7 [Axioms.md:25] pass: a missing file to read is a defect to report, not to guess. 8 [Axioms.md:27] pass: paths are written links, not "the usual files".
- **Better:** better than one long AGENTS.md for every job. The builder reads only what this job needs. That matches R35's idea that a model "only gets what it needs" [DIRECTOR-RULINGS.md:179], though R35 was about menus, not jobs.
- **Three leads:** Person: can read the sheet in a minute. Model: knows exactly what to open. Compute: can check that every listed path exists before the job starts (R37 item 7 [DIRECTOR-RULINGS.md:201]).

### B3. How a work page ties to the core spec

**In plain words.** Builders change code and make exports. They never change books. The compute is the only door into a book.

**Rulings this rests on.**
- R33 item 1: "Yes, books change through compute not by models." Read: "Books change only through the compute's gate." [DIRECTOR-RULINGS.md:159-160].
- R26: whole books are an export [DIRECTOR-RULINGS.md:103].
- R37 item 8: "Refuse with a handback, and stop rather than invent a meaning." [DIRECTOR-RULINGS.md:202].
- R37 item 10: "Every packet says what it gathered and what it didn't." [DIRECTOR-RULINGS.md:204].
- R37 item 2: "a delivery id can't change its content." [DIRECTOR-RULINGS.md:196].

**What this means for a work page.**
- "Files it may touch" never lists `books/`. If a job needs a book changed, the return holds a proposal for the compute. The compute decides (CORE-AND-TOOLS-SPEC.md B1, B12, at 9b555a2).
- If the builder cannot do the job, it refuses with a handback: what stopped it, and what it would need. It does not guess.
- The return says what it read and what it did not read. That is R37 item 10 applied to a return.

**The honest gap (EXISTS TODAY).** Today the rule is not a lock. Any program on the box can still write `books/` directly, and the token file sits in `books/` too (CORE-AND-TOOLS-SPEC.md B1; crates/compute/src/store.rs:59, :297). So a builder could break the rule and the compute might not notice. Until K8 step 1 is built, the review must check each return's diff for `books/` paths. That is why the worked example (Part C) is that job.

**Three checks (claims, 9).**
- **Axioms:** 1 [Axioms.md:13] tension: "Compute enforces it" is true only through the gate today (CORE-SPEC-HOSTILE-PASS.md:212). 3 [Axioms.md:17] pass: code work goes to a model; book writes stay with compute.
- **Better:** better than the old Brand Clerk, where "clerk-mediated write so a model cannot bypass `check`" was left as future work (CODEX-LIBRARIAN-TOOLS-REVIEW.md:221).
- **Three leads:** Person: sees one door. Model: proposes, never writes books. Compute: books the change or refuses it.

### B4. Grok Builder next to Cursor

**In plain words.** Both are builders. Each gets one work page at a time. The page decides who gets it, not the brand.

**What the sources say about each.**

| | Grok Builder | Cursor |
|---|---|---|
| Built before here | Many scoped jobs in the old work book; 16 returns name it (LIB at 960d20c) | A whole small Workshop in about two hours on 11 Nov (CURSOR-BUILD-REVIEW.md:12); Brand Clerk (CODEX-LIBRARIAN-TOOLS-REVIEW.md:223) |
| Worked from | One page with a scope and a release [LIB:W/0101.app-entry-0506/return.md:11-30] | Without our rulings R1-R25 (CURSOR-BUILD-REVIEW.md:17) |
| Known weak spots | Missed 19 nested evidence files because top-level checks passed [LIB:W/0703.prime-replay/REPORT.md:15-16]. Needed a Prime checkpoint [LIB:W/0703.prime-replay/REPORT.md:24] | Brand Clerk had no tests (CODEX-LIBRARIAN-TOOLS-REVIEW.md:223). Working without the rulings "cost them" (CURSOR-BUILD-REVIEW.md:95) |
| Price (Tester's dated snapshot, 16 Nov; not re-checked by Designer) | grok-build-0.1: $1 in, $2 out per 1M tokens; grok-4.7: $2 in, $6 out; past 200k prompt tokens the whole request bills double (docs/review/WORK-BOOK-RESEARCH.md:87-91) | Plus $8/month, Grok models only, no cloud agents; Premium $30/month for cloud agents (docs/review/WORK-BOOK-RESEARCH.md:51-54) |
| Limits | `--max-turns` exists; "grok has no budget feature" (docs/review/WORK-BOOK-RESEARCH.md:95-96) | Cloud agents need a hosted repo; our branch has no remote (docs/review/WORK-BOOK-RESEARCH.md:20-21, :59) |
| Strong at | Lowest xAI rate listed (docs/review/WORK-BOOK-RESEARCH.md:94) | Many cloud agents in parallel, each with its own VM, tests and screenshots (docs/review/WORK-BOOK-RESEARCH.md:57-58) |
| Cost per accepted job | Unknown. Old replay: "Tokens, provider cache, and cost are unknown." [LIB:W/0173.prime-replay-grok-02/return.md:17]. **9** | Unknown. **9** |
| Measured as better or worse | No. "No general assistance benefit or model ranking can be measured from this first delivery." [LIB:W/0703.prime-replay/REPORT.md:5-6] | Same |

**NEW (proposal, 7): how to pick.** Pick by the page:
1. If the done-check is a command the compute can run (a test, a build), the page can go to the cheaper builder first. Matthew's own words fit this: "if it's wrong it does it again" [LIB:W/0413.assistants/06.01.md:11].
2. If it fails the done-check twice, stop. Raise it to Prima, who may give it to the other builder. No endless retries (the old design said the same: "not infinite reruns" [LIB:W/0413.assistants/06.01.md:19]).
3. If the job needs judgment that no command can check (design, wording, a ruling's meaning), it does not go to either builder alone. It goes to a lead with a review.
4. Cheapness never moves a decision. The old page said: "Cheapness alone is not grounds to move semantic authority" [LIB:W/0413.assistants/01.md:34-35].

Tester's option D is close: small bounded cards to Grok Build, jobs that need a VM, browser or parallel runs to Cursor cloud (docs/review/WORK-BOOK-RESEARCH.md:166-168). Whether Grok Builder is in fact cheaper per accepted job is **9 (untried)**: "Which builder writes better code for which task. None found." (docs/review/WORK-BOOK-RESEARCH.md:203). The work book should record it per page (W5).

**Three checks (claims, 9).**
- **Axioms:** 3 [Axioms.md:17] pass: the work goes to whoever leads that kind of work; "A lead is not authority". 9 [Axioms.md:29] pass: every return faces a hostile pass, whichever builder made it. 4 [Axioms.md:19] pass: the reason for each pick is written on the page.
- **Better:** better than the old work book, where the builder was named per job with no written rule [LIB:W/0408.seats/01.md:24].
- **Three leads:** Person: releases the page to a builder. Model: does it. Compute: runs the done-check and counts tries.

### B5. Release, claim and return

**In plain words.** A page waits until someone with authority releases it. One builder claims it. The builder hands back on the same page.

**EXISTED BEFORE (LIB).** Matthew released a page in his own words, for example: "Read and execute: ... I release this batch. ... Return on that page for Codex Prime review." [LIB:W/0101.app-entry-0506/return.md:21-29]. The claim named the model, session, date and commit [LIB:W/0101.app-entry-0506/return.md:14]. "No other Builder may edit this batch while a claim is active. There is no automatic claim enforcement." [LIB:W/0118.workflow-start-0501/return.md:79-80].

**NEW (proposal, 7).**
- States, kept apart (R37 item 5 [DIRECTOR-RULINGS.md:199]): drafted, released, claimed, returned, accepted.
- The compute enforces one claim at a time, which the old book could not.
- A return is tied to the exact version of the page it worked from. If the page changes, the return goes stale (R37 item 4 [DIRECTOR-RULINGS.md:198]).
- Who may release is W3.

**Three checks (claims, 9).**
- **Axioms:** 1 [Axioms.md:13] pass: authority is granted by release, never claimed. 6 [Axioms.md:23] pass: each step is a new line on face 09.
- **Better:** better than the old book's honour-system claim.
- **Three leads:** Person: releases and accepts. Model: claims and returns. Compute: keeps the claim and the states.

---

## Part C. Worked example: K8 step 1, closing the direct-write door

**This is an example of a proposal (7), not a ruling.** K8 is open (CORE-AND-TOOLS-SPEC.md, K8). Tester's answer to K8 is a recommendation, not a ruling (CORE-SPEC-HOSTILE-PASS.md:243-256). The page shows the shape only. It is not released.

```text
work page: (address not chosen, W1)        title: close-the-door
state: drafted (example only; K8 is open)
builder: either (done-check is a test, B4 rule 1)

## AGENTS.md (export of faces 01 + 05.01)
stamp: Designer, Mon 16 Nov 2026, 2:56 PM EST, version 001

1. Goal
   Make the compute the only program that can change books/.
   Why: today a forged "director" line written straight into a
   book is loaded at start (CORE-SPEC-HOSTILE-PASS.md:22-23).

2. Must-know rules
   - R33 item 1: "Yes, books change through compute not by models."
     [docs/spec/DIRECTOR-RULINGS.md:159]
   - Refuse at runtime, cut only at start-up repair
     [docs/design/SEQ-FILE-PLAN.md:592]
   - Axiom 1: "Compute enforces it." [docs/spec/Axioms.md:13]

3. Files to read
   - docs/design/CORE-AND-TOOLS-SPEC.md (section B1)
   - docs/review/CORE-SPEC-HOSTILE-PASS.md lines 21-30, 56-62, 243-256
   - docs/design/SEQ-FILE-PLAN.md lines 590-597
   - crates/compute/src/store.rs lines 55-60, 270-300, 735-753, 940-975
   - crates/compute/src/identity.rs lines 1-10

4. Files it may touch
   - crates/compute/src/store.rs
   - crates/compute/src/identity.rs
   - crates/compute/src/main.rs
   - crates/compute/tests/  (new test files only)
   Never: books/, kernel/, docs/spec/, docs/design/

5. Done-check
   cargo test --workspace --offline   (all pass, none removed)
   plus new tests that show:
   a. a line appended to a book while the compute runs is refused
      and raised, not cut (today it is cut: store.rs:950-951);
   b. the token file is read from outside books/ (today it is
      books/.identities: store.rs:59, :297; identity.rs:3);
   c. a same-length edit is caught after a restart
      (today it is served: CORE-SPEC-HOSTILE-PASS.md:29-30);
   d. .queue is fsynced, so an id is not reused
      (today: store.rs:744-749).

6. Hand back
   Did / Blocked / Need. Commit SHA. Done-check output.
   Which of a-d it did not do, and why.
   Anything in books/ it found changed. Say it; do not fix it.

stop if: the fix needs a new OS account or file permissions on the
box (SEQ-FILE-PLAN.md:596). That is outside the code. Hand back.
```

**The facts (EXISTS TODAY, CORE-AND-TOOLS-SPEC.md B1):** the write folder is the first books folder (crates/compute/src/store.rs:59); the token file is read from it (:297; crates/compute/src/identity.rs:3); any book that parses is loaded at boot (:270-284); a longer file is cut at the next write, with no report (:950-951).

**Three checks (claims, 9).**
- **Axioms:** 5 [Axioms.md:21] pass: the page says where to stop. 7 [Axioms.md:25] pass: a found change is reported, not fixed. 9 [Axioms.md:29] tension: a done-check written by the person who wrote the job is not a hostile pass. Tester still reviews.
- **Better:** better than K8's text alone, which says "close the door" but not how to tell it is closed.
- **Three leads:** Person: releases it once K8 is answered. Model: writes code and tests. Compute: runs the done-check.

---

## Part D. Tester's research

Tester's file is `docs/review/WORK-BOOK-RESEARCH.md` (ab152b6, "Working path, not a ruling", :3). Folded in above: the capital name (B2), faces 01 + 05 as the source, worktree root, size budget (B2), prices and limits (B4), option D (B4). Not folded in as design, listed here as options for Matthew (Tester's, :157-175):
- A. Hash the printout and store the hash in the return and face 09 (R37 item 4).
- B. One name only: forbid CLAUDE.md and AGENT.md copies, since Grok loads every variant (:67-69).
- C. No file: pass the pack as the prompt. Harder to audit.
- E. Stay under 200k tokens per request (doubling).
- F. Compute lint: refuse a job AGENTS.md over budget, with pasted rulings, or with no stop-if.
- G. Set `--max-turns` on Grok, since it has no dollar cap.

Tester's own questions are carried by reference, not answered: Q1 (stored or printout, :179-184) is the same as W2 here. Q2 (host the repo for Cursor cloud agents, :186-191) is a separate Director question: pushing is Matthew's call. Tester's "No source found" list (:193-203) stays open.

---

## Part E. Open questions

Matthew's four-part form (t189u). Proposed answers only. Top three first.

### W1 (TOP). Is the work book a real book, written through the compute?

1. **Question.** Should work pages be real pages in a real book, changed only through the compute, like every other book?
2. **Proposed answer.** Yes. Give it its own book. Until the compute can write it safely (K8 step 1), keep drafts as export files marked draft, and let Prima keep the state by hand.
3. **Why.** R33 item 1: books change through compute [DIRECTOR-RULINGS.md:159]. Who gets hurt otherwise: you, if two builders both think they hold the same job.
4. **Axioms checked.** 1 [Axioms.md:13] tension: the gate is not a lock yet. 2 [Axioms.md:15] pass: same shape as any book. 6 [Axioms.md:23] pass: claims and returns become lines. 7 [Axioms.md:25] pass.

### W2 (TOP). Is a job's AGENTS.md a printout or a stored file?

1. **Question.** Should a job's `AGENTS.md` be a printout the compute makes from faces 01 and 05, not a file stored in the book? (Same as Tester's Q1, docs/review/WORK-BOOK-RESEARCH.md:179-184.)
2. **Proposed answer.** Yes. Face 01 is "agents.md-style" [workflow-loop.003.md:87] and the pack is "an agents.md-style build list" [workflow-loop.003.md:99]. The compute prints both into one file per job. The builder never edits it.
3. **Why.** One source, no drift between the page and the sheet. Who gets hurt otherwise: a builder that reads an old copy.
4. **Axioms checked.** 2 [Axioms.md:15] pass. 8 [Axioms.md:27] pass: the file points back to its page. 6 [Axioms.md:23] pass: each version is stamped (LIB:W/0409.decisions/01.md:168). 9 [Axioms.md:29] tension: untried on either builder.

### W3 (TOP). Who may release a work page to a builder?

1. **Question.** Do you release every work page yourself, or may Prima release pages inside a scope you approve?
2. **Proposed answer.** You release the first few yourself. After that, Prima may release pages inside an approved scope, as delegation already allows ("only to the extent delegated" [workflow-loop.003.md:89]). Every release is a line with who and when.
3. **Why.** Authority is granted, never claimed [Axioms.md:13]. Who gets hurt otherwise: you, if every small job waits on you; or you, if a job goes out you did not mean to send.
4. **Axioms checked.** 1 [Axioms.md:13] pass. 6 [Axioms.md:23] pass. 3 [Axioms.md:17] tension: "A lead is not authority", so Prima releasing needs a written grant.

### W4. What decides Cursor or Grok Builder for a page?

1. **Question.** Should the rule in B4 decide (a runnable done-check goes to the cheaper builder first; two fails, stop and raise)?
2. **Proposed answer.** Yes, as a starting rule, written on each page with its reason.
3. **Why.** Your words: "if it's wrong it does it again" [LIB:W/0413.assistants/06.01.md:11]. Who gets hurt otherwise: you, paying more, or getting a weaker job with no check.
4. **Axioms checked.** 3 [Axioms.md:17] pass. 4 [Axioms.md:19] pass: the reason is written. 9 [Axioms.md:29] tension: "cheaper" is untried.

### W5. Do we record cost per job?

1. **Question.** Should each return record time, tries and cost, so "cheap" can be checked?
2. **Proposed answer.** Yes, when the builder can report it. "Unknown" is a fine answer; never a guess.
3. **Why.** No source has a cost today [LIB:W/0173.prime-replay-grok-02/return.md:17]. Who gets hurt: you, choosing builders on a feeling.
4. **Axioms checked.** 7 [Axioms.md:25] pass: unknown stays unknown. 9 [Axioms.md:29] pass.

### W6. Who reviews a return?

1. **Question.** Should every return get a hostile pass from a different model before it is accepted?
2. **Proposed answer.** Yes. Tester by default. The builder's own done-check is not enough.
3. **Why.** The old replay: two builders missed files "because their top-level artifact checks passed" [LIB:W/0703.prime-replay/REPORT.md:15-16].
4. **Axioms checked.** 9 [Axioms.md:29] pass. 1 [Axioms.md:13] pass.

---

## Part F. Marked NEW or 9, because no source says it

- Grok Builder is cheap: Prima's relay of Matthew; the only prices are Tester's dated snapshot (docs/review/WORK-BOOK-RESEARCH.md:87-91), not re-checked here. Cheap per accepted job: **9.**
- Grok Builder is cheaper than Cursor per accepted job: **9.**
- Either builder is better at a kind of work: no source measures it [LIB:W/0703.prime-replay/REPORT.md:5-6]. **9.**
- The six parts of AGENTS.md, the printout from faces 01 + 05, the worktree root, the pick rule, the two-fail stop, the states list, compute-enforced claims: **NEW (7).**
- The work book's address: not chosen. **7.**

## Sources

- docs/spec/DIRECTOR-RULINGS.md: 103, 159-160, 179, 196, 198, 199, 201, 202, 204.
- docs/spec/Axioms.md: 13, 15, 17, 19, 21, 23, 25, 27, 29.
- docs/spec/workflow-loop.003.md: 87, 89, 99, 109, 111, 112, 122.
- docs/design/CORE-AND-TOOLS-SPEC.md at 9b555a2: B1, B12, K8.
- docs/design/SEQ-FILE-PLAN.md: 590-597.
- docs/review/CORE-SPEC-HOSTILE-PASS.md: 21-30, 56-62, 212, 243-256.
- docs/review/CODEX-LIBRARIAN-TOOLS-REVIEW.md: 7, 15, 221, 223.
- docs/review/CURSOR-BUILD-REVIEW.md: 12, 17, 95.
- docs/review/WORK-BOOK-RESEARCH.md (ab152b6): 1-21, 32-34, 51-59, 63-69, 79-96, 109-142, 157-203.
- crates/compute/src/store.rs: 59, 270-284, 297, 744-749, 950-951; crates/compute/src/identity.rs: 3.
- LIB (Amalgamour/Librarian, branch workshop, 960d20c): W/0118.workflow-start-0501/return.md and reservation.json; W/0101.app-entry-0506/return.md; W/0408.seats/01.md; W/0409.decisions/01.md:168; W/0413.assistants/01.md and 06.01.md; W/0173.prime-replay-grok-02/return.md:17; W/0703.prime-replay/REPORT.md.
