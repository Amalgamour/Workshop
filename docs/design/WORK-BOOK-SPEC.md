# Work book: how work is given out

Draft by Designer, for Matthew (Director). Not a ruling. Nothing here closes a question.
created: Mon 16 Nov 2026, 2:56 PM EST (Designer)

## Change note (2026-11-16, 9:10 PM EST, Designer)

- W8: adds Tester's `workflow` page-type option, from WORK-BOOK-CONCEPT.md W8 (54b737d; WORK-BOOK-CONCEPT-CHECK.md:39-44). The rest of W8 is unchanged.
- W4: notes that WORK-BOOK-CONCEPT.md W4 gives the same B4 rule in other words.

## Change note (Mon 16 Nov 2026, 4:55 PM EST)

Fixes from Tester's axiom check of 6fbba08 (docs/review/WORK-BOOK-AXIOM-CHECK.md, c5cbf0d). Only these lines changed:
- W7 and C2: axiom 2 is now tension, not pass. A full pinned copy is what axiom 2 warns against. seqAddr.md:104 says books follow the kernel "live", and a pinned copy does not, so that cite no longer backs the mark (:71-73). Tester's child-desk option is added to W7 (:75-77).
- W3: the spending cap is now in the proposed answer, not only in Tester's note (:43).

## Change note (Mon 16 Nov 2026, 4:04 PM EST)

Folds in Tester's hostile pass on a990738 (docs/review/WORK-BOOK-HOSTILE-PASS.md, a32fd7c; verdict "holds with fixes", :8). Each finding was checked against the code and rulings first. All were taken. One was taken in part: `.queue` is tracked by git (`git ls-files books`), so only `.identities` is invisible to a diff.
- Part C is retitled "narrowing" the door. Its frame now covers every file that holds the token-file path. Its done-check is split into a machine part and a reviewer part.
- States now use the tail steps the code already has (crates/seqaddr-core/src/tail.rs:80).
- W1's interim answer now writes state through today's gate, not by hand.
- B3 adds the `.identities` hash, R37 item 2 in full, and the lost-reply risk.
- W6 follows R20. W2 says which face-01 rule applies, and fixes the option-A cite. "16 returns" is now 19.
- The stale "no recorded version" lines are fixed: t212u is at docs/review/DIRECTOR-WORDS-t212u.md (f460153).
- Added: W8 (is a work page a system page?), "What we need from you" in Part A, and Tester's recommendations on W1 and W3-W6. Nothing is decided.
- Top three are now W1, W2, W8, because W8 decides whether W2's stored face can change.
- C2 checked against the same faults and fixed (see C2).

## Change note (Mon 16 Nov 2026, 3:00 PM EST)

Add-on from Prima (2:59 PM EST), committed on top of 8b75b43:
- Built on Tester's research, now at 877bc1e (Tester revised it after ab152b6). All research cites below are to 877bc1e.
- B2 now uses Tester's eight fixed sections and size budget, as proposals (7). The name `AGENTS.md`, the per-job printout from faces 01 + 05, and one fresh worktree per job are also proposals (7). Each was checked against the research file's own lines (B2).
- Matthew's t212u words are in Part A. (At 3:00 PM no recorded version existed; Prima recorded it at docs/review/DIRECTOR-WORDS-t212u.md, f460153.) His idea (AGENTS.md in the page) and Tester's (made fresh per job) are now W2, a top-3 question. Not decided.
- The "no remote" claim is removed from B4. See the differences line in Part D.

## Change note (Mon 16 Nov 2026, 2:56 PM EST)

New file. Asked in Prima's relay at 2:55 PM EST. It describes a book for giving out work. Each work page is one job for Cursor or Grok Builder. Tester's research (docs/review/WORK-BOOK-RESEARCH.md, ab152b6) landed while this was drafted; it is folded in (Part D and marked lines). Tester calls the product "Grok Build" (docs/review/WORK-BOOK-RESEARCH.md:1, :66 at 877bc1e); the old work book called the role "Grok Builder". This file uses "Grok Builder" for the role.

**How to read the cites.**
- A cite with no prefix is this repo, branch `build`.
- `LIB:` means the earlier Workshop: repo `Amalgamour/Librarian`, branch `workshop`, at commit 960d20c, cloned read-only at `/workspace/librarian-review/repo` (CODEX-LIBRARIAN-TOOLS-REVIEW.md:7, :15).
- `LIB:W/` is short for `LIB:00.kernel/00.00.10.work/`.
- Labels: EXISTS TODAY, PLANNED, and NEW (proposal). `7` means open. `9` means untried.

---

## Part A. In plain words

**What Matthew asked for.** I searched DIRECTOR-RULINGS.md, docs/review/ and docs/BUILD-LOG.md for "Grok Builder", "work page", "agents.md" and "book for giving out work". None of them holds his words for this request. So the request below is **quoted as relayed by Prima**, not in his own words:

> the workflow system is set up as a book for giving out work. Each work page is one piece of work he can hand to Cursor or to Grok Builder. Each work page carries an agents.md saying what the model needs to know and which files to read for that page. Grok Builder is built back into the Workshop design because it is cheap.

**His words in t212u**, recorded verbatim by Prima (docs/review/DIRECTOR-WORDS-t212u.md:10, f460153; spacing normalised):

> When you build a page you'll include an agents.md in it for explaining what it needs to know. What files it should reference for that page of work.

He puts the agents.md **in the page**. Tester proposes the compute **makes it fresh for each job** (docs/review/WORK-BOOK-RESEARCH.md:17-19). Both are kept; which one is W2.

**What we need from you** (he asked: "Tell me what you need from me to make this possible", docs/review/DIRECTOR-WORDS-t212u.md:10). NEW (proposal, 7):
1. Answers to the top three: W1, W2, W8.
2. Who may release pages, and a spending cap (W3).
3. Where "my local space" is (W7).
4. Your OK before any push, paid plan, or cloud run (Tester's Q2, WORK-BOOK-RESEARCH.md:189-203).

**His own earlier words that come close** (from the earlier Workshop, quoted exactly, spelling kept):
- On cheap models: "Yes that is where cheap models come it. We don't have to just haev compute. I see it executing prompts on it's own before handing work back. Likely we can get the cheap models to over perform once the compute is working right. ... You can give compute work, the compute gets the cheap compute to do it, if it's wrong it does it again. We need to start a page on this. How we plan to break up work." [LIB:W/0413.assistants/06.01.md:11]. He does not name Grok here.
- On stamping the agents file: "Agreed, AGENTS.VVV needs to be stamped just like our faces. we stamp them in the header. So we now what model did the work when what version we are on." [LIB:W/0409.decisions/01.md:168].
- On books: "Yes, books change through compute not by models." [DIRECTOR-RULINGS.md:159].

**The idea, in short.**
1. There is one book whose pages are jobs. It is called the work book.
2. One work page is one job. It is small enough to hand to one builder.
3. Each work page carries a short `AGENTS.md`. It tells the builder what to know, what to read, what it may touch, how to tell it is done, and what to hand back.
4. The builder works in the code, not in the books. Books change only through the compute.
5. The builder hands back a return. A different view checks it before anything is accepted.

**Grok Builder has been here before.** The earlier Workshop had a work book called `00.00.10.work`. Its first job was "Work-book first use and Grok Builder onboarding" [LIB:W/0118.workflow-start-0501/return.md:1]. Grok 4.7 sat as Builder for a scoped job [LIB:W/0408.seats/01.md:19]. 19 files named `return.md` there name Grok Builder (`git grep -l`, LIB at 960d20c; Tester's count, docs/review/WORK-BOOK-HOSTILE-PASS.md:112-114, which reproduces; my earlier 16 does not). In this repo, Prima's review notes the old desk core was built by the "grok.com builder" (CODEX-LIBRARIAN-TOOLS-REVIEW.md:211). So this design brings it back. It is not new.

---

## Part B. The parts

### B1. What a work page is

**In plain words.** One job, one page. The page says what the job is for. It points at the files. It holds the builder's return.

**EXISTS TODAY (in our spec, not built).** The workflow already has this shape. N4 "states the work ... Written on face 04, with an agents.md-style face 01 to go with it" [workflow-loop.003.md:87]. A pack is "an agents.md-style build list for a builder" [workflow-loop.003.md:99]. Work cards are `w01`, `w02` [workflow-loop.003.md:122]. Every page in the kernel already has an MVP pack on face 05.02 (for example kernel/00.00.00/00.00.00.0057.05.02.md:17).

**EXISTED BEFORE (LIB).** Each old work page had an assignment, a scope, a release, a claim and a return [LIB:W/0118.workflow-start-0501/return.md:14-80]. Files it was expected to make were listed in `reservation.json` (`expected_outputs`) [LIB:W/0118.workflow-start-0501/reservation.json]. The return was "Did / Blocked / Need" [LIB:W/0101.app-entry-0506/return.md:34-38].

**NEW (proposal, 7).** A work page is an ordinary page in the work book. Its face 04 is the job in plain words. Its faces 01 and 05 are printed as the job's `AGENTS.md` (B2). Its face 05 holds the returns, one counter each (05.01, 05.02). Its face 09 holds who claimed it and when. Its page type is a locked face 00 field (R36 [DIRECTOR-RULINGS.md:190]); the type's name is `7`, and whether it is a system page is W8. The book's address is not chosen here (W1).

**Three checks (claims, 9).**
- **Axioms:** 2 [Axioms.md:15] pass: a work page is the same shape as any page. 5 [Axioms.md:21] pass: the page frames the job: what, why, where to stop, what done is.
- **Better:** better than the old work book, where a page was a folder of loose files (return.md, reservation.json, receipt.json) [LIB:W/0118.workflow-start-0501/]. Here it is one page with faces.
- **Three leads:** Person: releases the job. Model: does the job. Compute: keeps the page and checks the done-check.

### B2. The AGENTS.md for a work page

**In plain words.** A short sheet the builder reads first. Eight parts, always in this order. Short enough to read in a minute.

**Proposals from Tester (7), each checked against the research file at 877bc1e:**

| Proposal | Research line | Checked |
|---|---|---|
| Name it `AGENTS.md` exactly, in capitals | "Name it AGENTS.md in capitals. Grok Build's list of names has no all-lowercase "agents.md"." (docs/review/WORK-BOOK-RESEARCH.md:15-16); the list itself is at :70-71 | yes: the list at :70-71 has AGENTS.md, Agents.md, AGENT.md, but no `agents.md`. Whether Cursor finds lowercase is unknown (:208) |
| The compute makes it fresh for each job, from faces 01 and 05 | "the compute makes AGENTS.md from the page's faces 01 and 05, as an export, one per job" (:17-18); "Compute fills it from 01 + one 05 pack" (:118) | yes |
| Eight fixed sections | :121-133 | yes: eight, numbered 1-8 |
| Size budget | "about 100 lines, hard stop 150" (:121); root under 40, job under 150, whole chain under 300 (:135-139) | yes |
| One fresh worktree per job | "compute writes the job AGENTS.md at the root of a fresh worktree, one job per worktree" (:143-144) | yes; the reason is that builders nest by where the code is (:141-142) |

**The eight sections (Tester's order, :121-133), with what my first draft called them:**

| # | Section | Holds | My first draft |
|---|---|---|---|
| 1 | Header (compute-filled) | page address.title, pack 05.NN, approval id, base hash, lead, axioms; plus a stamp of who and when [LIB:W/0409.decisions/01.md:168] | stamp line |
| 2 | Done looks like | 3-5 lines | goal |
| 3 | Why | 2-3 lines, then a link to face 04 | goal |
| 4 | Frame | may touch (exact paths), must not touch, stop if [workflow-loop.003.md:111-112] | files it may touch, stop if |
| 5 | Work cards | w01, w02 ... [workflow-loop.003.md:122] | (new) |
| 6 | Checks | exact commands that say pass or fail; any part no command can show (for example "no test removed") is listed separately for the reviewer | done-check |
| 7 | Hand back | Did / Blocked / Need, commit SHA, check output; through the gate as a proposal; what was gathered and what was not (R37 items 6, 10 [DIRECTOR-RULINGS.md:200, :204]) | hand back |
| 8 | Links | rulings, axioms and files to read, by address or exact path, opened when needed, not pasted in | must-know rules, files to read |

One change from my first draft: I had "quote the ruling". Tester says link, do not paste, because both builders open a linked file when they need it (docs/review/WORK-BOOK-RESEARCH.md:34-36, :82-83). NEW (proposal, 7): link it, and quote only the one line the job turns on.

**Where it lives** is open (W2): stored on the page, as Matthew's t212u words say, or made fresh for each job, as Tester proposes.

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
- R37 item 2: "A return and its next step are saved together, and a delivery id can't change its content." [DIRECTOR-RULINGS.md:196]. So a return and the page's next step go in as one change (NEW, 7).

**What this means for a work page.**
- "Files it may touch" never lists `books/`. If a job needs a book changed, the return holds a proposal for the compute. The compute decides (CORE-AND-TOOLS-SPEC.md B1, B12, at 9b555a2).
- If the builder cannot do the job, it refuses with a handback: what stopped it, and what it would need. It does not guess.
- The return says what it read and what it did not read. That is R37 item 10 applied to a return.

**The honest gap (EXISTS TODAY).** Today the rule is not a lock. Any program on the box can still write `books/` directly, and the token file sits in `books/` too (CORE-AND-TOOLS-SPEC.md B1; crates/compute/src/store.rs:59, :297). So a builder could break the rule and the compute might not notice. Until K8 step 1 is built, the review checks each return's diff for `books/` paths. A diff cannot see everything: `books/.identities` is ignored by git (.gitignore:5), so a builder that adds a director token leaves no diff (docs/review/WORK-BOOK-HOSTILE-PASS.md:29-34). NEW (proposal, 7): the compute records the sha256 of `books/.identities` before and after each job, and the review compares them. `books/.queue` is tracked by git, so the diff shows it; it also changes on every compute write (crates/compute/src/store.rs:744-749), so a hash of it alone proves nothing. Returns also go through the gate, and a retried proposal books twice today (CORE-AND-TOOLS-SPEC.md:342, K4). That is why the worked example (Part C) is that job.

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
| Price (Tester's dated snapshot, 16 Nov; not re-checked by Designer) | grok-build-0.1: $1 in, $2 out per 1M tokens; grok-4.7: $2 in, $6 out; past 200k prompt tokens the whole request bills double (docs/review/WORK-BOOK-RESEARCH.md:90-94) | Plus $8/month, Grok models only, no cloud agents; Premium $30/month for cloud agents (docs/review/WORK-BOOK-RESEARCH.md:53-56) |
| Limits | `--max-turns` exists; "grok has no budget feature" (docs/review/WORK-BOOK-RESEARCH.md:98-99) | Needs Premium; sees only pushed commits, so it can lag the local build branch (docs/review/WORK-BOOK-RESEARCH.md:61-62). The code is hosted at Amalgamour/Workshop, branch prima/build (docs/review/WORK-BOOK-RESEARCH.md:20-23) |
| Strong at | Lowest xAI rate listed (docs/review/WORK-BOOK-RESEARCH.md:97) | Many cloud agents in parallel, each with its own VM, tests and screenshots (docs/review/WORK-BOOK-RESEARCH.md:59-60) |
| Cost per accepted job | Unknown. Old replay: "Tokens, provider cache, and cost are unknown." [LIB:W/0173.prime-replay-grok-02/return.md:17]. **9** | Unknown. **9** |
| Measured as better or worse | No. "No general assistance benefit or model ranking can be measured from this first delivery." [LIB:W/0703.prime-replay/REPORT.md:5-6] | Same |

**NEW (proposal, 7): how to pick.** Pick by the page:
1. If the whole done-check is a command the compute can run (a test, a build), the page can go to the cheaper builder first. A check that is partly judgment counts as judgment (Tester, docs/review/WORK-BOOK-HOSTILE-PASS.md:151-152). Matthew's own words fit this: "if it's wrong it does it again" [LIB:W/0413.assistants/06.01.md:11].
2. The second try carries the first failure. If it fails twice, stop. Raise it to Prima, who may give it to the other builder. The old design: "Retry wrong outputs with diagnostic evidence, not infinite reruns" [LIB:W/0413.assistants/06.01.md:19].
3. If the job needs judgment that no command can check (design, wording, a ruling's meaning), it does not go to either builder alone. It goes to a lead with a review.
4. Cheapness never moves a decision. The old page said: "Cheapness alone is not grounds to move semantic authority" [LIB:W/0413.assistants/01.md:34-35].

Tester's option D is close: small bounded cards to Grok Build, jobs that need a VM, browser or parallel runs to Cursor cloud (docs/review/WORK-BOOK-RESEARCH.md:169-171). Whether Grok Builder is in fact cheaper per accepted job is **9 (untried)**: "Which builder writes better code for which task. None found." (docs/review/WORK-BOOK-RESEARCH.md:215). The work book should record it per page (W5).

**Three checks (claims, 9).**
- **Axioms:** 3 [Axioms.md:17] pass: the work goes to whoever leads that kind of work; "A lead is not authority". 9 [Axioms.md:29] pass: every return faces a hostile pass, whichever builder made it. 4 [Axioms.md:19] pass: the reason for each pick is written on the page.
- **Better:** better than the old work book, where the builder was named per job with no written rule [LIB:W/0408.seats/01.md:24].
- **Three leads:** Person: releases the page to a builder. Model: does it. Compute: runs the done-check and counts tries.

### B5. Release, claim and return

**In plain words.** A page waits until someone with authority releases it. One builder claims it. The builder hands back on the same page.

**EXISTED BEFORE (LIB).** Matthew released a page in his own words, for example: "Read and execute: ... I release this batch. ... Return on that page for Codex Prime review." [LIB:W/0101.app-entry-0506/return.md:21-29]. The claim named the model, session, date and commit [LIB:W/0101.app-entry-0506/return.md:14]. "No other Builder may edit this batch while a claim is active. There is no automatic claim enforcement." [LIB:W/0118.workflow-start-0501/return.md:79-80].

**NEW (proposal, 7).**
- States, kept apart (R37 item 5 [DIRECTOR-RULINGS.md:199]): use the tail steps the code already has, "draft -> pack -> open -> return -> review -> closed" (crates/seqaddr-core/src/tail.rs:80), not new names (axiom 2, "do not reinvent what already exists" [Axioms.md:15]). NEW (7): a release is the line that moves a pack to `open`; a claim is a face 09 line on an `open` page, not a state. How these map to core B15's selected, pending and accepted is CORE-AND-TOOLS-SPEC.md B15.
- The compute enforces one claim at a time, which the old book could not.
- A return is tied to the exact version of the page it worked from. If the page changes, the return goes stale (R37 item 4 [DIRECTOR-RULINGS.md:198]).
- Who may release is W3.

**Three checks (claims, 9).**
- **Axioms:** 1 [Axioms.md:13] pass: authority is granted by release, never claimed. 6 [Axioms.md:23] pass: each step is a new line on face 09.
- **Better:** better than the old book's honour-system claim.
- **Three leads:** Person: releases and accepts. Model: claims and returns. Compute: keeps the claim and the states.

---

## Part C. Worked example: K8 step 1, narrowing the direct-write door

**This is an example of a proposal (7), not a ruling.** K8 is open (CORE-AND-TOOLS-SPEC.md, K8). Tester's answer to K8 is a recommendation, not a ruling (CORE-SPEC-HOSTILE-PASS.md:243-256). The page shows the shape only. It is not released. It **narrows** the door; it does not close it. Only OS permissions close it (CORE-AND-TOOLS-SPEC.md:236), and that needs the box, not code, so it is a later page (docs/review/WORK-BOOK-HOSTILE-PASS.md:15-22).

```text
work page: (address not chosen, W1)        title: narrow-the-door
state: draft (example only; K8 is open)
builder: not chosen (part of the done-check is judgment, B4 rule 1)

## AGENTS.md (sections per B2; where it lives is W2)
1. Header: page (not chosen).narrow-the-door, pack 05.01, approval
   (none: K8 open), base hash (filled by compute), lead 3MC (example)
   stamp: Designer, Mon 16 Nov 2026, version 001

2. Done looks like
   machine: all tests pass; each card w01-w04 has a new test.
   reviewer: no test removed; each new test failed before the fix
   (the test command shows neither: HOSTILE-PASS:64-69).

3. Why
   A forged "director" line written straight into a book is loaded
   at start (CORE-SPEC-HOSTILE-PASS.md:22-23). Face 04 has the rest.

4. Frame
   may touch: crates/compute/src/store.rs, crates/compute/src/identity.rs,
              crates/compute/src/main.rs, crates/compute/src/lib.rs,
              crates/trial-compute/src/lib.rs, scripts/dev.sh
              (all hold the token-file path: lib.rs:94, :117;
              trial-compute lib.rs:64-66; dev.sh:14),
              crates/compute/tests/ (new files)
   must not touch: books/, kernel/, docs/spec/, docs/design/
   stop if: the fix needs a new OS account or file permissions on the
            box (docs/design/SEQ-FILE-PLAN.md:596). Hand back.

5. Work cards
   w01 refuse, do not cut, a longer book at runtime (store.rs:950-951)
   w02 read the token file from outside books/ (store.rs:59, :297)
   w03 catch a same-length edit after restart (HOSTILE-PASS:29-30)
   w04 fsync .queue so an id is not reused (store.rs:744-749)

6. Checks
   cargo test --workspace --offline

7. Hand back
   Did / Blocked / Need. Commit SHA. Check output. Which cards it
   did not do, and why. sha256 of books/.identities before and
   after (never its contents). Anything found changed in books/:
   say it, do not fix it. What it read and what it did not.

8. Links (open when needed)
   docs/spec/DIRECTOR-RULINGS.md:159 (R33 item 1); docs/spec/Axioms.md:13
   docs/design/CORE-AND-TOOLS-SPEC.md B1; docs/design/SEQ-FILE-PLAN.md:590-597
   docs/review/CORE-SPEC-HOSTILE-PASS.md:21-30, :56-62, :243-256
   crates/compute/src/store.rs:55-60, :270-300, :735-753, :940-975
   crates/compute/src/identity.rs:1-10
```

**The facts (EXISTS TODAY, CORE-AND-TOOLS-SPEC.md B1):** the write folder is the first books folder (crates/compute/src/store.rs:59); the token file is read from it (:297; crates/compute/src/identity.rs:3); any book that parses is loaded at boot (:270-284); a longer file is cut at the next write, with no report (:950-951).

**Three checks (claims, 9).**
- **Axioms:** 5 [Axioms.md:21] pass: the page says where to stop. 7 [Axioms.md:25] pass: a found change is reported, not fixed. 9 [Axioms.md:29] tension: a done-check written by the person who wrote the job is not a hostile pass. Tester still reviews.
- **Better:** better than K8's text alone, which says "close the door" but not how to tell it is closed.
- **Three leads:** Person: releases it once K8 is answered. Model: writes code and tests. Compute: runs the done-check.

---

## Part C2. Worked example: a local Workshop, built by Cursor

**This whole example is an example of a proposal (7), not a ruling.** It is not released. W1-W6 stay open.

**His words** (recorded verbatim by Prima, docs/review/DIRECTOR-WORDS-t212u.md:6): "I want cursor to build a localized version of this in my local  space." Nothing in the repo says what "my local space" is. It is `7` here, written `<LOCAL-SPACE>`, a placeholder for a place he names. No path on his machine is guessed (W7).

**What "localized" may mean.** In our address words, a book is a "localized environment" [seqAddr.md:20], and "anything not overridden locally is found in the kernel" [seqAddr.md:104]. So NEW (proposal, 7): a local Workshop runs its own compute and its own books, and reads the kernel from its export.

```text
work page: (address not chosen, W1)        title: local-workshop
state: draft (example only)       builder: Cursor (his words, t212u:6)

## AGENTS.md (sections per B2; where it lives is W2)
1. Header: page (not chosen).local-workshop, pack 05.01, approval (none),
   base: a named commit on Amalgamour/Workshop prima/build (NEW),
   lead 3MC (example). stamp: Designer, Mon 16 Nov 2026, version 001

2. Done looks like (NEW)
   machine, in <LOCAL-SPACE>: all tests pass; /health answers; the
   w05 change reads back; the kernel builder writes export/.
   reviewer: the boot report lists every book as loaded or refused,
   and none refused without a reason.

3. Why
   He asked for it: t212u:6. Books change only through the compute
   (R33 item 1, docs/spec/DIRECTOR-RULINGS.md:159-160).

4. Frame
   may touch: files inside <LOCAL-SPACE> only (placeholder, 7).
   must not touch: books/ by hand, ever; the source repo; any remote.
     No push, no merge, no pull request (pushes are his call).
   leave out (do not read or copy):
     docs/trial/, docs/review/, docs/design/WORKING-PATH-*.md,
     kernel/parked/, target/, export/ from the source repo (NEW:
     history and reviews, not needed to run)
   stop if: <LOCAL-SPACE> is not named; a step needs a book written
     by hand; a step needs the token file shared from our box; a tool
     (Rust, Node) or a download cache must be written outside
     <LOCAL-SPACE> (cargo and npm caches live there; needs his OK,
     W7). Hand back.

5. Work cards (NEW)
   w01 get the code at the named commit into <LOCAL-SPACE>
   w02 build and test: cargo test --workspace (--offline works only
       once the crates are already fetched)
   w03 start it with scripts/dev.sh (makes its own books/.identities;
       known gap: that file sits in books/, CORE-AND-TOOLS-SPEC.md B1)
   w04 run the kernel builder to export/ (kernel/build.mjs:31, :842)
   w05 send one test change through /propose; read it back

6. Checks
   cargo test --workspace --offline; the compute's /health answers;
   the boot report; the w05 read-back

7. Hand back (R37 items 8 and 10, DIRECTOR-RULINGS.md:202, :204)
   Did / Blocked / Need, with the start commit and check output.
   Refusal: if it cannot go on, it stops and says what stopped it and
   what it needs. It does not guess a path or a meaning.
   Packet: what it read, what it left out (the list in 4, and anything
   else), what it did not run, and what it found but did not fix;
   that books/.identities was made, and its sha256, never its contents.

8. Links (open when needed)
   README.md; docs/spec/AGENTS.md; docs/spec/format.md;
   docs/design/CORE-AND-TOOLS-SPEC.md (Part A, B1, B11, B12);
   docs/spec/DIRECTOR-RULINGS.md:159-160, :195-204; docs/spec/seqAddr.md:20, :104;
   scripts/dev.sh; kernel/build.mjs:31, :842
```

**R33 check.** Cursor builds code and runs the exporter. It never writes a book. The tracked books arrive with the code as a byte-for-byte copy (`git ls-files books`), which changes nothing. The only book writes are the local compute's own, through `/propose`. The one honest gap is B1's: the local compute's door is no more closed than ours until K8 step 1 is built.

**Three checks (claims, 9).**
- **Axioms:** 2 [Axioms.md:15] tension: a pinned full copy, not a live inheritance (Tester, docs/review/WORK-BOOK-AXIOM-CHECK.md:71-73). 7 [Axioms.md:25] pass: the unnamed place stays `7`, not guessed. 8 [Axioms.md:27] tension: a second copy of the kernel on his machine is a copy; how it stays in step is not designed (W7).
- **Better:** better than Cursor's 11 Nov build, made "without your rulings" (CURSOR-BUILD-REVIEW.md:17): this page links them.
- **Three leads:** Person: names the place and releases the page. Model (Cursor): builds and tests. Compute: the only writer of the local books.

---

## Part D. Tester's research

Tester's file is `docs/review/WORK-BOOK-RESEARCH.md` (ab152b6, revised at 877bc1e; "Working path, not a ruling", :3). Folded in above: the name, the per-job printout, eight sections, size budget, worktree (all B2, as proposals); prices and limits (B4); option D (B4). Not folded in as design, listed here as options for Matthew (Tester's, :160-178):
- A. Hash the printout and store the hash in the return and face 09 (R37 item 4).
- B. One name only: forbid CLAUDE.md and AGENT.md copies, since Grok loads every variant (:70-72).
- C. No file: pass the pack as the prompt. Harder to audit.
- E. Stay under 200k tokens per request (doubling).
- F. Compute lint: refuse a job AGENTS.md over budget, with pasted rulings, or with no stop-if.
- G. Set `--max-turns` on Grok, since it has no dollar cap.

Tester's own questions are carried by reference, not answered: Q1 (stored or printout, :182-187) is part of W2 here. Q2 (should Cursor cloud agents work from prima/build, :189-203) is a separate Director question: pushes, merges and the paid plan are Matthew's call. Tester's "No source found" list (:205-215) stays open.

**Differences.**
- t212u is recorded verbatim at docs/review/DIRECTOR-WORDS-t212u.md:6-10 (Prima, f460153). Part A and the 3:00 PM change note now cite it.
- Tester's hostile pass (docs/review/WORK-BOOK-HOSTILE-PASS.md, a32fd7c) tested a990738, not C2 or W7. Its own inputs (research, B2 table, W2's fresh side) were "Not trialed here" and need another view (:173-186).
- Remote: at ab152b6 the research said "Our build branch has no remote" (docs/review/WORK-BOOK-RESEARCH.md:21 at ab152b6). Prima says the code is on GitHub at Amalgamour/Workshop, branch prima/build. Tester fixed it at 877bc1e (:20-23: "Only the local copy has no remote"). This file does not repeat the no-remote claim. The local clone has no remote set (`git remote -v` is empty), which fits Tester's fix.
- Where AGENTS.md lives: Matthew (t212u, relayed) says in the page; Tester says made fresh per job (:17-19, :112-113). Held as W2.
- Name: Prima's relay and Matthew write "agents.md"; Tester proposes `AGENTS.md` (:15-16). Same file; the case is a proposal (7).

---

## Part E. Open questions

Matthew's four-part form (t189u). Proposed answers only. Top three first: W1, W2, W8 (re-ranked after Tester's pass; W8 decides whether W2's stored face can change). Then W3-W7.

### W1 (TOP). Is the work book a real book, written through the compute?

1. **Question.** Should work pages be real pages in a real book, changed only through the compute, like every other book?
2. **Proposed answer.** Yes. Give it its own book, and write its state lines through today's gate from day one. The open door is the same risk for every book; keeping state by hand would put a memory above the log (R37 item 1, "One append-only log is the only source of truth" [DIRECTOR-RULINGS.md:195]; docs/review/WORK-BOOK-HOSTILE-PASS.md:43-49).
   **Tester's recommendation (docs/review/WORK-BOOK-HOSTILE-PASS.md:122-129):** yes, through today's gate; one work book per build, retired to the shelf when done (R31 item 6, a book is "a working journal" [DIRECTOR-RULINGS.md:139]).
3. **Why.** R33 item 1: books change through compute [DIRECTOR-RULINGS.md:159]. Who gets hurt otherwise: you, if two builders both think they hold the same job.
4. **Axioms checked.** 1 [Axioms.md:13] tension: the gate is not a lock yet. 2 [Axioms.md:15] pass: same shape as any book. 6 [Axioms.md:23] pass: claims and returns become lines. 7 [Axioms.md:25] pass.

### W2 (TOP). Does the AGENTS.md live in the page, or is it made fresh for each job?

1. **Question.** You said a page should "include an agents.md in it" (t212u, as relayed by Prima). Tester proposes the compute makes it fresh for each job from faces 01 and 05, and nothing is stored (docs/review/WORK-BOOK-RESEARCH.md:17-19, :182-187). Which should it be?
2. **Proposed answer (serves both; a proposal, 7).** Both, with one source. The page stores its `AGENTS.md` as face 01, written only through the compute, as you said. That fits the workflow, which already has "an agents.md-style face 01" on an N4 page [workflow-loop.003.md:87]. It does not fit a normal page, where "faces 01 and 02 usually hold only key words" (R33 item 2 Read, held 7 [DIRECTOR-RULINGS.md:162]), nor the research's face 01, "the page's meaning, in model cards" (WORK-BOOK-RESEARCH.md:116). So this answer treats a work page as a workflow page. For each job, the compute writes a copy into that job's worktree: face 01 plus the job's face 05 pack, with the page's version and a hash in the header. (Tester's option A keeps the hash in the hand back and face 09, WORK-BOOK-RESEARCH.md:160-162; the header is mine, NEW.) If W8 makes a work page a system page, face 01 freezes once linked [DIRECTOR-RULINGS.md:170].
   **Tester's option, not an answer (docs/review/WORK-BOOK-HOSTILE-PASS.md:131-139):** keep the brief in the face 05 pack, "an agents.md-style build list" [workflow-loop.003.md:99], which gives "an agents.md in it" without touching face 01. Tester gave no answer to W2, because one side of it is Tester's own research. The builder never edits either. If the page changes, old copies go stale (R37 item 4 [DIRECTOR-RULINGS.md:198]).
3. **Why.** You can open the page, by its title, and read what the builder was told; the address stays back end (R31 item 8 [DIRECTOR-RULINGS.md:143-144]). The builder gets the job's part only. Who gets hurt otherwise: you, if the only copy is a file that is gone after the job (stored nowhere); or the builder, if it reads a stored file that has gone out of date (stored only).
4. **Axioms checked.** 1 [Axioms.md:13] pass: the stored face governs; the copy never outranks it. 2 [Axioms.md:15] tension: a copy is what axiom 2 warns about; the hash and the no-edit rule limit the drift but do not remove it. 6 [Axioms.md:23] pass: each copy names the page version it came from. 8 [Axioms.md:27] pass: "a copy ... never becomes what it points to". 9 [Axioms.md:29] tension: untried on either builder.

### W8 (TOP). Is a work page a system page?

1. **Question.** System pages "freeze once linked (faces 00-04)" (R34 [DIRECTOR-RULINGS.md:170]), and page type is a locked face 00 field (R36 [DIRECTOR-RULINGS.md:190]). Is a work page a system page? (Raised by Tester, docs/review/WORK-BOOK-HOSTILE-PASS.md:55-58; Tester gave no answer.)
2. **Proposed answer (Designer's, 7).** No. A work page is persistent work in a book (kernel-design.md:83), and you read it, while system pages are "backend and designed for control not for user to access" [DIRECTOR-RULINGS.md:169]. Its type gets its own locked name (`7`). Tester's added option (2026-11-16, from WORK-BOOK-CONCEPT.md W8): seqAddr.md:192 already lists a page type `workflow`. It is not system, so the R34 freeze would not apply, but no ruling says whether it locks (7) (WORK-BOOK-CONCEPT-CHECK.md:39-44). Its brief can change until a pack is released; each return is bound to the version it read (R37 item 4 [DIRECTOR-RULINGS.md:198]).
3. **Why.** If it were a system page, a stored face 01 brief (W2) would freeze once linked, and "if the page changes" could not happen. Who gets hurt: you, unable to fix a wrong brief except by a new page.
4. **Axioms checked.** 1 [Axioms.md:13] pass: you decide the type. 2 [Axioms.md:15] pass: same shape as other content pages. 6 [Axioms.md:23] pass: returns bind to versions. 7 [Axioms.md:25] pass: the type name stays `7`. 9 [Axioms.md:29] tension: untried.

### W3. Who may release a work page to a builder?

1. **Question.** Do you release every work page yourself, or may Prima release pages inside a scope you approve?
2. **Proposed answer.** You release the first few yourself. After that, Prima may release pages inside an approved scope, as delegation already allows ("only to the extent delegated" [workflow-loop.003.md:89]). Every release is a line with who and when. The grant names the scope and a spending cap (Tester, docs/review/WORK-BOOK-AXIOM-CHECK.md:37-43).
3. **Why.** Authority is granted, never claimed [Axioms.md:13]. Who gets hurt otherwise: you, if every small job waits on you; or you, if a job goes out you did not mean to send.
4. **Axioms checked.** 1 [Axioms.md:13] pass. 6 [Axioms.md:23] pass. 3 [Axioms.md:17] tension: "A lead is not authority", so Prima releasing needs a written grant.
5. **Tester's recommendation (docs/review/WORK-BOOK-HOSTILE-PASS.md:141-148):** you release the first few; then Prima, inside a written grant that names the scope and a spending cap, because a release spends money. Option: a cap per page (turns or dollars) set by you.

### W4. What decides Cursor or Grok Builder for a page?

1. **Question.** Should the rule in B4 decide (a runnable done-check goes to the cheaper builder first; two fails, stop and raise)?
2. **Proposed answer.** Yes, as a starting rule, written on each page with its reason. (2026-11-16, Designer: WORK-BOOK-CONCEPT.md W4 says the same rule in other words: "If a test can check the job, the cheaper builder goes first. Two fails: stop and hand back." You can take either wording.)
3. **Why.** Your words: "if it's wrong it does it again" [LIB:W/0413.assistants/06.01.md:11]. Who gets hurt otherwise: you, paying more, or getting a weaker job with no check.
4. **Axioms checked.** 3 [Axioms.md:17] pass. 4 [Axioms.md:19] pass: the reason is written. 9 [Axioms.md:29] tension: "cheaper" is untried.
5. **Tester's recommendation (docs/review/WORK-BOOK-HOSTILE-PASS.md:150-156):** the B4 rule, plus: a check that is partly judgment counts as judgment, and the second try carries the first failure. (Both are now in B4.)

### W5. Do we record cost per job?

1. **Question.** Should each return record time, tries and cost, so "cheap" can be checked?
2. **Proposed answer.** Yes, when the builder can report it. "Unknown" is a fine answer; never a guess.
3. **Why.** No source has a cost today [LIB:W/0173.prime-replay-grok-02/return.md:17]. Who gets hurt: you, choosing builders on a feeling.
4. **Axioms checked.** 7 [Axioms.md:25] pass: unknown stays unknown. 9 [Axioms.md:29] pass.
5. **Tester's recommendation (docs/review/WORK-BOOK-HOSTILE-PASS.md:158-163):** yes: time, tries, tokens, dollars; keep "not reported" apart from "zero" (R37 item 6 [DIRECTOR-RULINGS.md:200]).

### W6. Who reviews a return?

1. **Question.** Should every return get a hostile pass from a different view before it is accepted?
2. **Proposed answer.** Yes, by a different view as R20 defines it: "a fresh session of the same model counts as a different view" [DIRECTOR-RULINGS.md:79]. Tester by default. The builder's own done-check is not enough.
3. **Why.** The old replay: two builders missed files "because their top-level artifact checks passed" [LIB:W/0703.prime-replay/REPORT.md:15-16].
4. **Axioms checked.** 9 [Axioms.md:29] pass. 1 [Axioms.md:13] pass.
5. **Tester's recommendation (docs/review/WORK-BOOK-HOSTILE-PASS.md:165-171):** yes, by a different view as R20 defines it, not only Tester, since one reviewer is a queue. Option: the reviewer must not be the page's writer.

### W7. What is "my local space", and does it stay in step with ours?

1. **Question.** "My local space" (t212u:6) is not defined. Is it a folder on your own machine with a fresh copy of the Workshop, and should its books ever flow back to ours?
2. **Proposed answer (NEW, 7).** A folder you name, holding a copy of prima/build at a named commit, with its own compute and books. Kernel updates arrive only as new commits you pull. Nothing flows back except a return on the work page, as a proposal through our compute.
3. **Why.** Books change only through the compute (R33 item 1, DIRECTOR-RULINGS.md:159). Who gets hurt otherwise: you, if two Workshops write the same book and drift apart.
4. **Axioms checked.** 1 [Axioms.md:13] pass: you name the place and release it. 2 [Axioms.md:15] tension: a full pinned copy is what axiom 2 warns against; seqAddr.md:104 says books follow the kernel "live", which a pinned copy does not (Tester, docs/review/WORK-BOOK-AXIOM-CHECK.md:71-73). 6 [Axioms.md:23] pass: the start commit is named. 8 [Axioms.md:27] tension: two copies of the kernel; the link between them is a commit, not a lawful connection yet.
5. **Tester's option (docs/review/WORK-BOOK-AXIOM-CHECK.md:75-77):** make it a child desk with a written 99 link (decisions.md:218-232), which is a lawful connection. Child desks are deferred (R21 [DIRECTOR-RULINGS.md:84]), so you must say yes first.

---

## Part F. Marked NEW or 9, because no source says it

- Grok Builder is cheap: Prima's relay of Matthew; the only prices are Tester's dated snapshot (docs/review/WORK-BOOK-RESEARCH.md:90-94), not re-checked here. Cheap per accepted job: **9.**
- Grok Builder is cheaper than Cursor per accepted job: **9.**
- Either builder is better at a kind of work: no source measures it [LIB:W/0703.prime-replay/REPORT.md:5-6]. **9.**
- The eight sections, size budget, per-job printout and worktree (Tester's proposals); the stored face 01 plus copy (W2); the pick rule, the two-fail stop, the release and claim lines on the tail steps, compute-enforced claims, the `.identities` hash, "What we need from you", W8's answer: **NEW (7).**
- The work book's address: not chosen. **7.**

## Sources

Every cite is inline. Files opened: docs/spec/DIRECTOR-RULINGS.md, docs/spec/Axioms.md (13-29), docs/spec/workflow-loop.003.md, docs/design/CORE-AND-TOOLS-SPEC.md (9b555a2), docs/design/SEQ-FILE-PLAN.md, docs/review/CORE-SPEC-HOSTILE-PASS.md, docs/review/CODEX-LIBRARIAN-TOOLS-REVIEW.md, docs/review/CURSOR-BUILD-REVIEW.md, docs/review/WORK-BOOK-RESEARCH.md (877bc1e; line 21 at ab152b6), crates/compute/src/store.rs and identity.rs, and LIB (Amalgamour/Librarian, branch workshop, 960d20c): W/0101, W/0118, W/0173, W/0408, W/0409, W/0413, W/0703.
