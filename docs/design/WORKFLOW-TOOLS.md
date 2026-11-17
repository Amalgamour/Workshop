# Workflow tools: the six steps

For Matthew. By Designer. A PROPOSAL (7) for how to build the tools. Only you approve.
created: Tue 17 Nov 2026, 12:30 PM EST

In one line: the compute does the checking and the record keeping; the lead (Prime) signs; the worker builds on its own branch.

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

Overall build order (plain list):
1. Status view: Now strip, board, tail feed. Read-only. (His 2.5; W12, still open, proposes the read-only sheet and board go first.)
2. Face 00 `prime` and `previous-primes` fields (S1). Steps 1 and 4 need to know who the lead is.
3. Issue: pack check with pins, then the printer.
4. Work: branch name and return file path fixed in the printer.
5. Ping: the compute files the return on 05.
6. Check: tool checks, then the checker's review.
7. Sign-off: the close change, close record, merge.
8. Going up: trigger routing (waits on E1).

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

## S12 and S13

- **S12 (one branch per pass): answered in direction (t259u:8).** Open detail: exact branch name, and who merges (T1).
- **S13 (checker before the lead's read): answered in direction (t259u:9).** Open detail: none new.

## Where Prima's summary differs from his recorded words

1. "06 along" is Prima's reading of "06 allow" (marked in Prima's own mapping, t259u:15).
2. The meaning of 04 and 06 in Prima's mapping comes from earlier words (t239u:10, t243u), not t259u.
3. Prima's relay of 2.5 drops his why ("It's hard right now to keep in my mind everything..."). Prima's mapping in the file keeps it.
4. Prima labels 2.6 "Up path / finish". His words cover the finish ping only. The trigger routing of step 6 is not in them. E1 stays open.
5. 2.2 and 2.3 are "I agree" only. They answer direction, not the branch name or who merges.

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

## Ties

- ONE-PAGE-WORK.md: S1, S4, S6, S7, S9, S10, S12, S13; E1 (Elevation table).
- SAMPLE-PAGE.md: Now strip, board, pack, prompt box, AGENTS.md. SAMPLE-PAGE-PATHS.md: refused return, rework, blocker.
- PACK-TEMPLATE.md P6 and WORK-BOOK-CONCEPT.md W10: the return file in the commit.
- DECISIONS-WAITING.md: the sheet.
