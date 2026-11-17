# Workflow tools: the six steps

For Matthew. By Designer. A PROPOSAL (7) for how to build the tools. Only you approve.
created: Tue 17 Nov 2026, 12:30 PM EST
Updated: Tue 17 Nov 2026, 12:45 PM EST (your drawings t261u, t262u: Shape, no direct writes, several models, T5-T6).
Updated again: Tue 17 Nov 2026, 12:55 PM EST (your t263, t264u, t266u: checker and observer are two roles; T6 answered; step 7; T7, T8).

In one line: the compute does the checking and the record keeping; the lead (Prime) signs; the worker builds on its own branch.

## v-note (2026-11-17, 12:55 PM EST, Designer)

Folds docs/review/DIRECTOR-WORDS-t263-T6.md (2a9b165, e8f9a90, a8814ff). Nothing was renamed.
- The checker and the observer are two roles (t264u, :15).
- Checker: the lead's assistant (:25). Step 3 updated.
- Observer: watches the lead for drift, loops and stalls (:26). New step 7, build order 9.
- T6 answered: no. Designer's proposed "yes" was wrong; kept as asked. New questions T7, T8. T5 gains a note.

## Shape (your drawings t261u, t262u)

His words: "Thinking about it I think this is better." and "The page is the what the compute sits in.  person, model sit outside, sometimes multiple models can sit at this." (docs/review/DIRECTOR-WORDS-t262u.md:5-7). The record marks t262u as replacing t261u (:3, a recording note, not his words).

What t262u shows (docs/review/DIRECTOR-DRAWING-t262u.png, checked by eye):
- A hexagon: the page. "compute" in the middle.
- Black lines from the compute to each face, 01 to 06.
- Four coloured lines start outside the page and end at the compute: lead (green), observer (purple), Builder (blue), person (red). None ends at a face.
- Not drawn: faces 00, 07, 08, 09.

What t261u showed (DIRECTOR-DRAWING-t261u.png): the same hexagon and compute, no black lines. The four coloured lines ran from the compute to the page edge at one face each: lead 01, observer 06, Builder 05, person 04. 02 and 03 had none. Labels sat outside; lines stopped at the edge.

The rule this design takes from t262u (Designer reading, 7):
1. The page holds the compute.
2. A face is reached only through the compute.
3. People and models stay outside the page. Several models may work one page at once.

Roles (t266u, v-note 12:55):
- "The checker, is the assistant to the lead." and "The observer is to check that the lead isn't drifting from the goals and MVP.  Also makign sure the lead isn't stuck in a loop and stalled." (DIRECTOR-WORDS-t263-T6.md:25-26)
- The checker is not drawn in t261u or t262u. Read (Designer, 7): it works for the lead, outside the page, through the compute like the others.
- The page role "observer" is not the Observer bot that watches this build. Nothing in his words joins them.

## His words (t259u)

From docs/review/DIRECTOR-WORDS-t259u.md (c2a291c), lines 7-12. Answered, not ruled.
- 2.1: "Yes, but we need to make sure lead is checking the 04 face and 06 allow with the previous completed 05" (:7)
- 2.2: "I agree" (:8)
- 2.3: "I agree" (:9)
- 2.4: "Yes lead signed off on the work." (:10)
- 2.5: "Yes we need this to be part of it.  lead model and person need this part.  It's hard right now to keep in my mind everything that is going on. which is what we are doing." (:11)
- 2.6: "That is right, when a model finishes it's work it pings the compute so the compute can file the completed 05." (:12)

## Readings (not his words)

- Prima's reading: "06 allow" means "06 along" (DIRECTOR-WORDS-t259u.md:15). Designer uses it below, marked. Confirm in T2.
- Prima's mapping adds what 04 and 06 hold ("MVP goals, his responses, decisions"; "prime notes") (:15). That is from earlier words (t239u:10, t243u), not t259u.
- 2.4 is past tense ("signed off"). Read as: the lead signs off. This fits "Prime signs off the compute closes it." (DIRECTOR-WORDS-t249u.md:6).
- Prime is the team lead role (DIRECTOR-WORDS-t254u.md:7). The lead sits on face 00 (DIRECTOR-WORDS-t255u.md:7). Proposed field names: `prime` and `previous-primes` (ONE-PAGE-WORK.md, S1).
- 2.6 answers the finish ping. It does not name the going-up triggers. So E1 (which signals send work up) stays open. See "Where Prima's summary differs".
- "file the completed 05" read as: the compute records the return on that 05 pass (tail `open -> return`). The pass closes only at sign-off (step 4).

## The six steps at a glance

| Step | Who starts it | Compute does | Exists today | Build order |
|---|---|---|---|---|
| 1 Issue | Prime (lead) | checks the pack, pins, prints prompt box and AGENTS.md | tail move only; no pack check, no printer | 3 |
| 2 Work | worker | nothing until the ping | nothing (no branch code) | 4 |
| 2.6 Ping | worker, at finish | checks the commit and file, files the return on 05 | return tail, claim-holder only | 5 |
| 3 Check | compute, then checker, then lead | touched files, tests, figures | builder-not-reviewer rule only | 6 |
| 4 Sign-off | Prime | checks signer, writes close record, closes, merges | close by reviewer only; no merge | 7 |
| 5 Status | anyone, any time (read-only) | builds Now strip and board from history | /history, /page boards | 1 |
| 6 Going up | compute (triggers) | routes to Prime or to you | nothing | 8 |
| 7 Observer | compute (signals), then observer | builds the signals from history | history, board, outcomes only | 9 |

Overall build order (plain list):
1. Status view: Now strip, board, tail feed. Read-only. (His 2.5; W12, still open, proposes the read-only sheet and board go first.)
2. Face 00 `prime` and `previous-primes` fields (S1). Steps 1 and 4 need to know who the lead is.
3. Issue: pack check with pins, then the printer.
4. Work: branch name and return file path fixed in the printer.
5. Ping: the compute files the return on 05.
6. Check: tool checks, then the checker's review.
7. Sign-off: the close change, close record, merge.
8. Going up: trigger routing (waits on E1).
9. Observer: first the signal view (reads only, so it can ride with order 1), then findings and where they go (waits on T8; the drift signal waits on the T4 pins).

## Step 1. Issue

- **What it does.** Prime drafts the pass. The compute checks every field is filled, the paths sit inside the grant (S9), and the pins are current (see "The pre-draft check"). Only then does it move `draft -> pack`. It prints the prompt box and AGENTS.md from a fixed template, with versions pinned (S4).
- **Who triggers it.** Prime, by asking the compute to release the pack.
- **Exists today.**
  - Only the compute may move `draft -> pack`: crates/seqaddr-core/src/state.rs:548-552. The refusal text says "after checking the pack (section 8)", but no pack check is written. Nothing in crates/compute calls that move.
  - A page lint exists: POST /check.seq (crates/compute/src/lib.rs:177-182, route :256). It checks a page, not a pack.
  - Compute-only fields are refused from others: crates/seqaddr-core/src/validate.rs:236-245 (C8.7).
  - No template, prompt box or AGENTS.md printer exists. No grant or path check exists.
  - Face 03 outside pages 0001-0099 is refused: validate.rs:352-354. Face 07 is refused: validate.rs:231-234, face.rs:73-75. Both block the one-page layout (follow-on work, DECISIONS-WAITING.md).
- **To build.** Pack field check; path-inside-grant check; pin check; `draft -> pack` by the compute; the printer (SAMPLE-PAGE.md, "The prompt box" and "The printed AGENTS.md").
- **Order.** 3.

## The pre-draft check (his 2.1 "but")

**What the lead must read, before drafting pass NN:**
1. Face 04, the dev space (goals, your responses, decisions).
2. Face 06, Prime's notes (Prima's reading of "06 allow" as "06 along").
3. The previous completed 05 pass: its return, its checks, its close record.
- For 05.01 there is no earlier pass. The pin reads "none".

**How the compute can show it was done (proposal, Designer, 7):**
- The pack carries three pins, filled by the compute when Prime opens the draft: face 04 version, face 06 version, and the last closed 05 pass. Each pin is the log entry number plus a hash of the text.
- Prime writes one 06 note before the draft: what changed since the last pass, citing the three pins.
- At release (`draft -> pack`) the compute refuses the pack if any pin is not the current one. Example: you added a response on 04 after Prime drafted. The pack is refused until Prime re-reads and re-pins.
- The compute also refuses if the pinned 05 is not the newest closed pass on the page.
- Honest limit: pins prove which versions the pack was built against. They cannot prove a mind read them (axiom 9). The 06 note is the lead's own record; the checker can test it against the pins.
- Exists today: entry numbers per counter (state.rs:121, `entries`). No pin fields. Unknown fields on a log line are kept (crates/seqaddr-core/src/log.rs:93-95), so pins can ride on the entry before a format step names them (7).

## Step 2. Work (his 2.2: agreed)

- **What it does.** The worker builds on one branch per pass, writes its return in one file, and pushes.
- **Who triggers it.** The worker, after claiming the pack.
- **Exists today.**
  - The claim: first valid claim wins (state.rs:541-543, :560-561). The claim's `start` is the claim time (`e.at`), not a commit (state.rs:105, :561).
  - No git, branch or commit code anywhere in crates/ (searched: no `git`, `branch`, `commit`, `Command::new`).
- **To build.** The printer writes the branch name and the return path into the prompt box. Exact branch name is open detail (T1). Proposed: `pass/<page>.05.<NN>` (S12). Return path proposed: `.workshop/returns/<page>.05.<NN>.md` (SAMPLE-PAGE.md, prompt box).
- **Order.** 4.

## The finish ping (his 2.6)

**What the ping carries (proposal, Designer, 7):**
- pass address (example 10.20.30.1201.05.03)
- worker name (must be the claim holder)
- branch name
- commit SHA that holds the return file
- return file path
- the pack hash it worked from
- the one-job code from the prompt box (PACK-TEMPLATE.md, P6 part 2)

**How it ties to P6 (answered t239u, "3. Yes, see 2.", DIRECTOR-WORDS-t239u.md:11):**
- The ping is a pointer. The file in the commit is the carrier. The book entry is the record (WORK-BOOK-CONCEPT.md W10).
- On a ping, the compute: finds the commit on that branch; checks the file is at that path in that commit; checks the commit starts from the pack's start commit; checks the one-job code and the claim; reads the file once; then writes `open -> return` on 05.NN with the return as its body.
- If any check fails, the compute records only the refusal and why (SAMPLE-PAGE-PATHS.md, Path 2). Nothing is filed.
- A ping with no matching file files nothing. A file with no ping waits.
- **Exists today.** The return goes on the same counter as its pack (state.rs:573-575). Only the claim holder may return; the compute returns on another's claim only in recovery (state.rs:563-571). So "the compute files it" needs that rule changed for this path (P6 part 3 already named it).
- **The road problem.** The compute listens on this machine only (crates/compute/src/main.rs:4, :12; refusal :40-43). The worker has no writer token (crates/compute/src/identity.rs:1-9). So today the worker cannot ping directly. See T3.
- **Order.** 5.

## Step 3. Check (his 2.3: agreed)

- **What it does.** The compute checks which files the commit touched (against `may touch`), runs the pack's tests, and fills the figures (time, tries; tokens and dollars "not available" until an API record exists, S10). Then the checker reviews against "done when". The lead reads last.
- **Who triggers it.** The compute, on filing the return. Then the checker. Then Prime.
- **Exists today.**
  - The builder may not review its own return: state.rs:578-583 (policy `reviewer_not_builder`).
  - `return -> review` records the reviewer (state.rs:583).
  - No touched-file check, no test runner, no figures. Per-check results have no log fields (log.rs:64-96).
- **To build.** Touched-file check; test runner; figures from the log; per-check results on the review step (ONE-PAGE-WORK.md, "The checker"); the routing of `need` and `blocked` items to Prime at return (S13).
- **Order.** 6.
- S13 (Prime reads after the checker): answered in direction (t259u:9).

**The checker (t266u; v-note 12:55).**
- His words: "The checker, is the assistant to the lead." (DIRECTOR-WORDS-t263-T6.md:25). And: "It's a assistant to the lead.  Handed off by the compute.  So the lead which works directly with the person is able to not be stuck reviewing all the returns." (:7)
- He gave :7 when asked about the observer (:3). That it describes the checker is Prima's mapping (:28). It fits :15 and :25.
- So: the compute hands the checker each return. The checker confirms the work with tools ("a checker using tools to confirm the work was done correctly", t245u:10). The lead signs off (t259u:10; t249u:6).
- "Reports to the lead" is Prima's mapping, not his words. His words: assistant to the lead; the lead signs.
- Never the builder: state.rs:578-583 (refusal S10). Not in code: any rule that the checker is not the lead (7).
- Tension: 2.3 agreed the lead reads last (t259u:9). t263 says the lead should not be "stuck reviewing all the returns" (:7). S13 and S15 proposed the lead reads the whole return. See T7.

## Step 4. Sign-off (his 2.4: the lead signs)

- **What it does.** Prime signs. The compute checks the signer is face 00's `prime` at that log entry (by log order, not clock), writes the close record (S6), closes the pass, and merges the accepted work.
- **Who triggers it.** Prime.
- **Exists today.**
  - POST /close (crates/compute/src/lib.rs:260; crates/compute/src/store.rs:979-996).
  - Only the reviewer may ask: store.rs:991-992. This must change to "the current Prime".
  - The compute writes the close under its own name, recording who asked in `for`: store.rs:994-995.
  - Others may not move `review -> closed`: state.rs:553-555.
  - No `prime` field on face 00 (crates/seqpage/src/face00.rs has `lead` letters for a band only, :101). No close record fields (log.rs:64-96). No merge.
- **To build.** The signer check against `prime`; close record fields (S6); merge of accepted cards (S12, S7). Who merges is open detail (T1).
- **Order.** 7 (after face 00 `prime`, order 2).

## Step 5. Status (his 2.5: required)

- **What it does.** The Now strip and the board, always built from the history, never stored (W11). One view for the lead model, one plain view for you. His why: "It's hard right now to keep in my mind everything that is going on." (t259u:11)
- **Who triggers it.** Anyone, any time. Read-only.
- **Exists today.**
  - GET /history/:addr lists log entries for a page or face (lib.rs:144, :250; store.rs:542-569). It sorts by clock, then book, then entry number (store.rs:567).
  - GET /page/:addr returns each counted face's board: counter and tail (store.rs:434-444; state.rs:297-300).
  - No Now strip, no tail feed, no cards column, no plain view.
- **To build.** Now strip (newest open pass, its claim, unanswered `need`/`blocked`); tail feed newest first; board with cards column (SAMPLE-PAGE.md, "Now" and "The board").
- **Order.** 1. It reads only, so it changes nothing that is live.

## Step 6. Going up

- **What it does.** The compute watches the triggers and routes to Prime or to you (ONE-PAGE-WORK.md, "Elevation" table).
- **Who triggers it.** The compute, on a trigger.
- **Exists today.** Nothing. Outcomes `blocked` and `needs-authority` exist as close words (store.rs:981).
- **To build.** Trigger watch and routing, after E1 is answered.
- **Order.** 8. Not answered by t259u (see below).

## Step 7. Observer (t266u; v-note 12:55)

- **His words.** "The observer is to check that the lead isn't drifting from the goals and MVP.  Also makign sure the lead isn't stuck in a loop and stalled." (DIRECTOR-WORDS-t263-T6.md:26)
- **What it does.** Watches the lead, not the work. Two questions: is the lead drifting from the goals and MVP? Is the lead stuck in a loop, or stalled? It does not review returns (the checker does). It does not sign (the lead does).
- **Measured against.** His words name "the goals and MVP", no face. MVP goals sit on 04, stripped down on 01 for the agent (t245u:12). Prima's brief says "face 04 goals and face 01 MVP"; the record's mapping says "the face 04 goals and the MVP" (:28). Not picked here (7).
- **Who triggers it.** The compute builds the signals from the history. The observer reads them, read-only, through the compute.
- **Signals it could read.**

| Signal | Exists today | To build |
|---|---|---|
| passes on one frame | each pass is its own 05 counter (state.rs:110-121); the board lists them (state.rs:296-300); the spec rule: why questions at pass 4, halt at 6 (workflow-loop.003.md:258-267) | no frame field or count in code (searched crates/: no `frame`) |
| same blocker again | close outcome `blocked` (state.rs:14) | blocker identity (workflow-loop.003.md:260 marks it 7) |
| rework loops | close outcome `failed` (state.rs:14) | card fates (S7), to see the same card fail again |
| time since the last move | every entry has a number and a clock (log.rs:64-66); /history sorts by clock (store.rs:542-569); each counter lists its entries (state.rs:120-121) and claim time (state.rs:105) | a "time since" view and a limit; nothing exists |
| drift from goals and MVP | nothing | the 04 and 01 pins (T4) set against each pass's cards and touched files; the compute gives evidence, a model judges meaning |

- **When it finds something (proposal, Designer, 7).** It writes one finding: the signal, the entry numbers as evidence, one plain line. It hands that to the compute, which files it (no direct face writes). It stops nothing; the only automatic stop stays the pass-6 halt (workflow-loop.003.md:267). Where the finding goes: T8, not decided.
- **Not the lead (proposal, 7).** The observer is never the lead of the page it watches: a lead cannot catch its own drift (axiom 9). Nothing in code enforces this.
- **Face 06.** t261u put the observer on 06. Whether it reads 06 to judge drift is open (T5 note).
- **Order.** 9.

## No role writes a face directly (t262u check)

Rule: a role may hand the compute a file, but only the compute files it on a face.

**What already holds in code.**
- Every write over HTTP needs a token; the body's `by` is not trusted (crates/compute/src/lib.rs:85-94).
- Writes queue one at a time (lib.rs:74-84; the store sits behind one lock, lib.rs:42, :50).
- Every write goes through one path: `propose` (crates/compute/src/store.rs:731), which validates, then `append` (store.rs:914, :927). `/close` (:995), `/ask/link` (askq.rs:181) and a `.seq` page (store.rs:759-766) all go through `propose`.
- A `.seq` page file is already "input, filed by the compute": import turns it into a proposal and writes nothing (crates/seqpage/src/import.rs:1-4).
- While the compute runs, a book changed outside it is refused (store.rs:946-948) or its extra bytes are cut as a partial line (:950-951).

**Spots where a face can be written without the compute.**
1. **Book files in git.** books/*.book are tracked (git ls-files books/). A model can edit one in a commit. At start the compute reads books from disk and replays them (store.rs:1019-1033). Replay re-applies the tail rules, but `by` is only text in the file; no token is checked (state.rs:548 compares `e.by` to the compute's name). So a hand-written line naming `compute` would pass. Fits by: a check that refuses any push touching books/ (W10 already asks for it, 7), and the book read at start compared with the compute's own last length (7).
2. **Edits while the compute is stopped.** Same as 1, without git. Fits the same way.
3. **Kernel draft files.** kernel/00.00.00/*.draft.md are face drafts written as plain files. The compute does not read them; it loads only `DD.SS.BB.book` files (store.rs:123-130). They are input, not faces, until filed through `propose`. Not mine to change (kernel).
4. **Exported pages.** `seqpage` writes a page to a file (crates/seqpage/src/bin/seqpage.rs:72). That is a view out. Edits come back only as a `.seq` proposal (above). Holds.

**Each step against the rule.**
- Issue: Prime's draft goes in by `propose`. The pre-draft 06 note is a proposal to face 06; the compute files it. Holds once written that way.
- Work: the worker writes code and one return file in git. Code is not a face. The return file is input (P6).
- Ping: the compute reads the return file and files it on 05.NN itself. Holds; needs the state.rs:563-571 change named above.
- Check: check results are filed by the compute on the review step. The checker's review goes in by `propose`. Holds.
- Sign-off: Prime asks; the compute writes the close (store.rs:994-995). Holds.
- Status: reads only. Holds.
- Going up: the compute routes; any answer from you goes on 04 by `propose`. Holds.

## Several models on one page (t262u: "sometimes multiple models can sit at this")

**Already there.**
- Each pass is its own counter, 05.01, 05.02 and up (state.rs:110-121).
- The first claim on a pack wins; a second is refused (state.rs:541-543, :560-561).
- Only the claim holder may return (state.rs:563-571).
- The builder may not review its own return (state.rs:578-583).
- A tail move whose `from` is out of date is refused (state.rs:545).
- A face has only one draft at a time (state.rs:484-486), and a full `put` never replaces a seated face (:474-476).
- Writes are taken one at a time (lib.rs:74-84).
- Many names can hold tokens (crates/compute/src/identity.rs:3-4).

**Missing (7).**
- No lock on files: two open passes may both list src/steer.rs in `may touch`. Nothing warns.
- No branch conflict handling: two accepted passes may not merge cleanly. Who resolves is open (T1).
- No owner on a face draft: any token holder may note or promote it.
- Workers off this machine have no token and no road in (main.rs:4, :12; T3).
- The Now strip shows one open pass. It must list every open claim, with its worker and its `may touch`.
- Proposed (Designer, 7): at release, the compute refuses a pack whose `may touch` overlaps another open pass on the page, unless Prime names the overlap in the pack.

## S12 and S13

- **S12 (one branch per pass): answered in direction (t259u:8).** Open detail: exact branch name, and who merges (T1).
- **S13 (checker before the lead's read): answered in direction (t259u:9).** Open detail: none new.

## Where Prima's summary differs from his recorded words

1. "06 along" is Prima's reading of "06 allow" (marked in Prima's own mapping, t259u:15).
2. The meaning of 04 and 06 in Prima's mapping comes from earlier words (t239u:10, t243u), not t259u.
3. Prima's relay of 2.5 drops his why ("It's hard right now to keep in my mind everything..."). Prima's mapping in the file keeps it.
4. Prima labels 2.6 "Up path / finish". His words cover the finish ping only. The trigger routing of step 6 is not in them. E1 stays open.
5. 2.2 and 2.3 are "I agree" only. They answer direction, not the branch name or who merges.

6. Prima's description of t262u matches the drawing. One thing not in her description or reading: the drawing says "observer", while step 3 here says "checker". Whether they are the same role is T6.
7. The t262u relay matches the recorded words; the record has a line break after "better." (t262u:5-7).

From t263, t264u, t266u (v-note 12:55):
8. His t263 words (:7) answered a question about the observer (:3). Applying them to the checker is Prima's mapping (:28).
9. "Reports to the lead" is Prima's mapping. His words: "assistant to the lead" (:25); the lead signs (t259u:10).
10. Prima's brief: "face 04 goals and face 01 MVP". His words: "the goals and MVP" (:26). The record's mapping: "the face 04 goals and the MVP" (:28).
11. The t266u relay matches the record, except a line break after "lead." (:25-26). t264u is recorded in the same file (:15), not its own file.
12. The record's t264u mapping (:17) still calls the observer the lead's assistant. The t266u mapping (:28) withdraws that. This file follows :25-26.

## New open questions (rule t189u)

### T1. Branch name and who merges
1. **Question.** Each pass gets its own branch (t259u:8). What is it called, and who merges accepted work?
2. **Proposed (Designer, 7).** Branch `pass/<page>.05.<NN>`. The compute merges, at close, only cards marked accepted, after Prime signs.
3. **Why.** "Prime signs off the compute closes it." (t249u:6). A merge is part of closing. Who gets hurt otherwise: the next worker, building on work nobody accepted.
4. **Axioms checked.** 1 [Axioms.md:13] pass: Prime signs, the compute enforces. 3 [Axioms.md:17] pass: compute leads the mechanical step. 9 [Axioms.md:29] pass: nothing merges before review. 7 [Axioms.md:25] tension: not built.

### T2. "06 allow"
1. **Question.** You wrote "06 allow". Did you mean "06 along" (check 04 and 06 together with the last finished pass)?
2. **Proposed (Prima's reading).** Yes, "along".
3. **Why.** The pre-draft check pins exactly what you name. Who gets hurt otherwise: you, if the check proves the wrong thing.
4. **Axioms checked.** 7 [Axioms.md:25] pass: unknown stays unknown until you say. 4 [Axioms.md:19] pass: the why of the check is recorded.

### T3. How the ping reaches the compute
1. **Question.** The compute listens only on its own machine (main.rs:4, :12). The worker cannot reach it. How does the ping arrive?
2. **Proposed (Designer, 7).** Now: the push is the ping. When Prima pulls, the compute scans pass branches for a commit holding a return file and runs the ping checks. Later: once the Workshop runs on your machine, the worker calls the compute directly. Not proposed: opening the compute to the network.
3. **Why.** No new door to the network (P6 part 3). Who gets hurt otherwise: anyone who finds an open port.
4. **Axioms checked.** 1 [Axioms.md:13] pass: no new network grant. 8 [Axioms.md:27] tension: the return travels through git, then the book. 9 [Axioms.md:29] tension: untried.

### T4. Pre-draft pins
1. **Question.** Should the compute refuse a pack whose 04, 06 and last-closed-05 pins are not current?
2. **Proposed (Designer, 7).** Yes. Pins are entry number plus hash. Prime writes one 06 note citing them before the draft.
3. **Why.** It is the only proof a machine can give that the pack was built on the latest 04, 06 and 05 (t259u:7). Who gets hurt otherwise: you, when a pass ignores your newest response on 04.
4. **Axioms checked.** 6 [Axioms.md:23] pass: the pack names what it came from. 1 [Axioms.md:13] pass: the live record decides. 9 [Axioms.md:29] tension: pins show versions, not that they were read. 7 [Axioms.md:25] tension: new fields need a format step.

### T5. Does the t261u face pairing still hold?
1. **Question.** In t261u each role touched one face: lead 01, observer 06, Builder 05, person 04. In t262u every role ends at the compute. Does the pairing still say which face each role mostly reads or feeds, or is it gone?
2. **Proposed (Designer, 7).** Keep it only as "mostly reads or feeds", never as "writes": lead feeds 01, Builder 05, person 04. Hold 06 open: you called 06 "prime notes" (t243u), and t261u put the observer there.
3. **Why.** t262u ends every role at the compute, so no role owns a face. Who gets hurt otherwise: a model that reads "builder: 05" as leave to write face 05.
4. **Axioms checked.** 1 [Axioms.md:13] pass: the compute enforces. 3 [Axioms.md:17] pass: each role leads its part. 7 [Axioms.md:25] tension: 06 unclear. 2 [Axioms.md:15] tension: two drawings, one replaced.
- **Note (12:55, t266u).** The observer now watches the lead (:26). 06 holds prime notes (t243u), so 06 may be what the observer reads to judge drift. Open; not decided here.

### T6. Is the "observer" the checker?
- **Status: answered (t263, t264u, t266u): no.** "Sorry no the checker is different from an observer" (DIRECTOR-WORDS-t263-T6.md:15). The checker is the lead's assistant (:25); the observer watches the lead (:26). Designer's proposed "yes" below was wrong. The four parts stay as asked.
1. **Question.** Both drawings name an "observer". Step 3 names a checker that reviews against "done when". Same role?
2. **Proposed (Designer, 7).** Yes: the observer is the other view that checks the work, and it is never the builder.
3. **Why.** Only four roles are drawn, and step 3 needs a checker that is not the builder (state.rs:578-583). Who gets hurt otherwise: a pass with no one able to review it.
4. **Axioms checked.** 9 [Axioms.md:29] pass: another view tries to break it. 3 [Axioms.md:17] pass. 7 [Axioms.md:25] tension: your word, not yet defined.

### T7. What the checker hands the lead; may the lead skip the full return?
1. **Question.** You agreed the lead reads last (2.3, t259u:9). You also said the checker is there so the lead is "not stuck reviewing all the returns" (t263-T6.md:7). What does the checker hand back? When the checker passes a return, may the lead sign from that report without reading the whole return?
2. **Proposed (Designer, 7).** The checker hands back a short report: each check, pass or fail, with its commit; each "done when" line, met or not; anything outside the frame. If all pass and nothing is `need` or `blocked`, the lead reads the report and signs; the full return stays one click away. The lead reads in full when a check fails, the return says `need` or `blocked`, or "done when" changed. Occasional full reads follow a written rule (E4). This changes the S13 and S15 proposals ("reads the whole return").
3. **Why.** Your t263 reason: the lead "works directly with the person" (:7). Who gets hurt otherwise: you, waiting on a lead buried in returns.
4. **Axioms checked.** 9 [Axioms.md:29] pass: another view (never the builder) tries to break it first. 1 [Axioms.md:13] pass: the lead still signs; the compute enforces. 3 [Axioms.md:17] pass: each leads its part. 7 [Axioms.md:25] tension: the report's fields are not designed.

### T8. Where does the observer report, and can it stop work?
1. **Question.** When the observer sees the lead drifting, looping or stalled, who does it tell? Can it stop anything?
2. **Proposed (Designer, 7).** It tells you, the person, on the Now strip (which you asked for, 2.5), with a copy to the lead. It sends you a direct note only at pass 4 on one frame, or the same blocker twice. It stops nothing; the pass-6 halt (workflow-loop.003.md:267) stays the only automatic stop.
3. **Why.** Your ladder sends what the lead cannot solve to the person (t245u:8). The observer watches the lead, so telling only the lead would let a stuck lead hide it. But you want to be "involved when it comes to the big issues" only (t245u:8), hence the strip first. Who gets hurt otherwise: you, finding a stalled page late.
4. **Axioms checked.** 5 [Axioms.md:21] pass: "An observation outside the frame is permission to report, not to act". 1 [Axioms.md:13] pass: the observer holds no authority; it raises. 9 [Axioms.md:29] pass: another view watches the lead. 7 [Axioms.md:25] tension: where the finding is filed (06, or a view) is open (T5).

## Ties

- ONE-PAGE-WORK.md: S1, S4, S6, S7, S9, S10, S12, S13; E1 (Elevation table).
- SAMPLE-PAGE.md: Now strip, board, pack, prompt box, AGENTS.md. SAMPLE-PAGE-PATHS.md: refused return, rework, blocker.
- PACK-TEMPLATE.md P6 and WORK-BOOK-CONCEPT.md W10: the return file in the commit.
- DECISIONS-WAITING.md: the sheet.
- docs/review/DIRECTOR-WORDS-t261u.md, DIRECTOR-WORDS-t262u.md and their drawings: Shape.
- docs/review/DIRECTOR-WORDS-t263-T6.md: the checker (step 3), the observer (step 7), T6.
