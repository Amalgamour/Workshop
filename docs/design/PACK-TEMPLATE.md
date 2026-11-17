# Pack template: the fixed shape the compute fills

For Matthew. By Designer. A proposal (7), not a ruling. Nothing here is decided. Only you approve.
created: Mon 16 Nov 2026, 5:54 PM EST

## Change note (2026-11-17, 11:30 AM EST, Designer)

- P6 marked answered by Matthew, t239u (docs/review/DIRECTOR-WORDS-t239u.md:11). Not ruled. The four parts stay.
- Part 4: his words put AGENTS.md on face 01 as a card; see WORK-BOOK-CONCEPT.md F4.

## Change note (Mon 16 Nov 2026, 8:05 PM EST)

Folds the parts of Tester's check of the dev, work and lab pages (docs/review/DEV-WORK-LAB-PAGES-CHECK.md, 2f06fd3) that touch this file.
- P8: the override page is withdrawn. Your R21 says "No overrides for now" (DIRECTOR-RULINGS.md:83). Pack 1 is recorded instead as a one-time grant from you, plus the outside check's note.
- Lab page: shown as "not yet made" until a trial is needed (DEV-WORK-LAB-PAGES.md D1, D3).
- Face 05 clash with R22-R24 is raised there as D6; the packs here sit on work-page face 05 either way.

## Change note (Mon 16 Nov 2026, 7:10 PM EST)

Folds Tester's check (docs/review/PACK-TEMPLATE-CHECK.md, 3078e0f, "holds, with fixes"). Every cite in it was opened; see "Cites in Tester's check" at the end.
- New P6 (TOP): the builder has no road back to the compute (crates/compute/src/main.rs:4, :12).
- P1 reopened: your words fix only that unprompted and overflow come after the job items. Both orders are shown.
- The return gets the approved parts it lacked: deviations and their why, questions and permission asked, notes, and cost (W5).
- Matched pages: by written link both ways, not by number alone (new P7; R18, WL:60, axiom 8).
- Bootstrap: Tester's A (a script fills it) then B (an outside check) (new P8). Waits on W8. (The override page first proposed here was withdrawn at 8:05 PM: R21.)
- P3: start commit pinned at claim. P4: two more hashes. P5: the code copy ends at a pack, not "the day".
- Smaller: a refusal row (R37 item 8), two-writer rows named, branch filled as a value, example says "no book writes".

## Change note (Mon 16 Nov 2026, 5:56 PM EST)

Made consistent with Tester's check (docs/review/WORK-BOOK-CONCEPT-CHECK.md, 093c64a) and the concept fix (54b737d). It landed just after the first version of this file.
- The board exists, tail only (crates/seqaddr-core/src/state.rs:296-300). w02 adds columns.
- Pack 1 is a bootstrap exception: hand-written, entered as `pack` with no check. Needs your `7`.
- Every sheet and prompt box says "door open: not proof" until K8 step 1.
- Only the claim holder sends a return (state.rs:563-567). Git keeps only the commit hash.
- The sheet shape joins the W13 set (P5).

## Change note (Mon 16 Nov 2026, 5:54 PM EST)

New file. It holds the pack template, the handoff sheet, the return template and the AGENTS.md slot, for the first pack in docs/design/WORK-BOOK-CONCEPT.md (08625be). Tester's check (docs/review/WORK-BOOK-CONCEPT-CHECK.md) had not landed when this was written, so nothing from it is folded in.

## Cite key

- "t226u:N", "t227u:N": lines of your recorded words, docs/review/DIRECTOR-WORDS-t226u.md and docs/review/DIRECTOR-WORDS-t227u.md.
- "WL": docs/spec/workflow-loop.003.md. "R37 item N": docs/spec/DIRECTOR-RULINGS.md:195-204.
- "OWB": old work book (zip from Matthew), /tmp/oldwb/10.10.13.brand-clerk. "OWC": old Workshop clone (Amalgamour/Librarian, branch rebuild, de3b8eb), 10.workshop/10.10.work/10.10.12.rebuild/0117.pack-lint.
- "SPEC B2": docs/design/WORK-BOOK-SPEC.md:96-131 (Tester's eight AGENTS.md sections).

## Why this file

Your words: "But you should hand the jobs to the compute, It basically gives you a constand template that won't drift. Otherwises you will." (t227u:5)

In plain words:
- Prima hands each job to the compute.
- The compute gives back the job in a fixed shape. The shape is the same every time.
- Prima writes only the thinking parts. The compute writes the rest.

You also ruled it: "The compute fills templates, bindings, and hashes, and the model writes only the judgment." (R37 item 3, DIRECTOR-RULINGS.md:197)

## The four sheets, in plain words

1. **The pack.** The job. Prima writes what to do and why. The compute adds where it lives, its step, and the start point in the code.
2. **The handoff sheet.** What the builder gets. The compute makes it fresh from the records. Nobody types it. (Side label: S06 manifest, WL:220.)
3. **The prompt box.** The part of the handoff sheet you paste into Cursor or Grok Builder.
4. **The return.** What the builder hands back. Your words put unprompted and overflow last (t226u:11). The rest of the order is open (P1).

One rule for all four: if the compute cannot find a value, it writes "not available". It never guesses. ("Couldn't look" is kept separate from "isn't there", R37 item 6, DIRECTOR-RULINGS.md:200.)

## Where the shape comes from

- The pack header and work cards: WL:101-118 (sections 5.1, 5.2).
- The templates and the check list: WL:228-245 (section 8). The templates are not seated yet: "`7`: seat the workflow card types and templates through the kernel's drafting path." (WL:232)
- The handoff sheet: WL:220 (S06).
- The steps a pack moves through: docs/spec/seqAddr.md:128-140 (section 4, tails); crates/seqaddr-core/src/tail.rs:79-91.
- The return: WL:185-193 (section 6.2); t226u:11.
- The old work book used the same parts: Overview, Do, Stop if, a return file, and numbered jobs with Ask and status (OWB 0501.brand-clerk/05.02.md:17-36). Its return had Did, Blocked, Need, Evidence (OWB 0101.brand-clerk/05.02.return.md:11-23).
- The old pack-lint page wanted this and never built it: "Not the lint command. That command is a later pack." (OWC 01.md:26). Its returns drifted by hand: "This file is 05.01.pack.md. It is ready." (OWC 05.01.return.md:21).
- The builder's first sheet: SPEC B2, eight sections. They map onto pack fields below, so there is one shape, not two.

## 1. The pack template

In plain words: Prima fills the left part (what and why). The compute fills the right part (where, when, from which code). Most fields have one owner. Rows 11, 18 and 20 have two: Prima writes, the compute checks.

| # | Field | Filled by | Why that owner | Source | SPEC B2 section |
|---|---|---|---|---|---|
| 1 | address (page, face 05, counter NN) | compute | the compute gives out the next free slot | WL:105-116; seqAddr.md:128 | 1 Header |
| 2 | tail | compute | only the compute moves draft -> pack and review -> closed | crates/seqaddr-core/src/state.rs:548-556 | 1 Header |
| 3 | by (who made it) | compute | the gate knows who is calling; a model cannot claim to be someone else | WL:105 | 1 Header |
| 4 | made at | compute | real clock, not typed | proposal (7) | 1 Header |
| 5 | pack hash | compute | a hash is a binding (R37 item 3). Taken at draft -> pack; pack 1 skips that step, so it is hashed when it is put (P4) | DIRECTOR-RULINGS.md:197 | 1 Header |
| 6 | claim owner | compute | first claim wins, recorded at pack -> open | state.rs:543, :561 | 1 Header |
| 7 | repository baseline: repo, branch, start commit | compute | repo and branch are values the compute fills, not fixed text. The start commit is pinned at claim, not at pack time (P3) | WL:116 (`7` on format) | 1 Header |
| 8 | files to pull from GitHub | compute | taken from the frame paths (field 15), checked to exist | R37 item 7, DIRECTOR-RULINGS.md:201 | 8 Links |
| 9 | predecessor (earlier pack or return) | compute | it is in the records | WL:115 | 8 Links |
| 10 | linked pages: dev 04NN, lab 07NN | compute | the compute finds them by number and title (R18), then follows face 08 links both ways. Only a page linked both ways is shown as linked. Otherwise "found, not linked" (`7.8`), never a lookalike (P7). A lab page made only when a trial is needed shows "not yet made" until then | WL:59-61; DIRECTOR-RULINGS.md:71-72; Axioms.md:27 | 8 Links |
| 11 | authorized (the approval the job rests on) | Prima names it; compute checks it | only you grant authority; the compute refuses a name that does not resolve | WL:106, :239; Axioms.md:13 | 1 Header |
| 12 | lead | Prima | a judgment | WL:107 | 1 Header |
| 13 | axioms | Prima | a judgment | WL:108 | 1 Header |
| 14 | outcome (done looks like) | Prima | a judgment | WL:109 | 2 Done looks like |
| 15 | overview (why) | Prima | a judgment; links to dev page face 04 | WL:110 | 3 Why |
| 16 | frame: may touch, must not touch | Prima | scope; the compute checks it sits inside the grant | WL:111-112, :241 | 4 Frame |
| 17 | stop if | Prima | a judgment | WL:111 | 4 Frame |
| 18 | grant (allowed operations and targets) | Prima writes; compute checks | must sit inside your approval | WL:112, :241 | 4 Frame |
| 19 | frame id | Prima | names the approved work frame | WL:113 | 1 Header |
| 20 | risk: proposed / floor / effective | Prima proposes; compute records floor and effective | WL says so | WL:114 | 1 Header |
| 21 | jobs list: w01, w02 ... (type, title, reason, target, ask) | Prima | the work itself | WL:118-124, :240 | 5 Work cards |
| 22 | checks (commands that say pass or fail) | Prima | a judgment; the reviewer-only items are listed apart | SPEC B2 row 6 | 6 Checks |
| 23 | read first (rulings, files) | Prima | a judgment; the compute checks each link opens | SPEC B2 row 8; R37 item 7 | 8 Links |
| 24 | hand back | compute | fixed text: "return by the return template (part 3)" | t226u:11 | 7 Hand back |
| 25 | refusal | compute | a pack that fails its check stays draft. The compute hands back the rule, the field, and why (R37 item 8: refuse with a handback) | DIRECTOR-RULINGS.md:202; WL:171 | 7 Hand back |

All 25 rows are a proposal (7). Rows 4, 5, 7, 8, 22, 23, 24, 25 add to Prima's list (see Differences).

Not yet in the table: R37 item 5, "Selected, pending, and accepted are separate states" (DIRECTOR-RULINGS.md:199). The board shows outcome only. Where those states show is open (7).

## 2. The handoff sheet template

In plain words: before each handoff the compute reads the live records and prints this sheet. It is a view. It is never stored as a new authority (WL:220). If a record changes, the sheet is made again.

| Field | Filled by | From |
|---|---|---|
| door label: "door open: not proof" until K8 step 1 lands | compute | WORK-BOOK-CONCEPT-CHECK.md:126 |
| sheet made at, and the last log line read | compute | the log |
| pack text (fields 1-24) | compute | the pack counter |
| tail | compute | the counter |
| claim holder, or "not claimed" | compute | state.rs:561 |
| dev page 04NN and lab page 07NN: "linked", "found, not linked", or for the lab "not yet made" | compute | row 10; P7 |
| earlier returns on this slot and its predecessor: "none" only if looked and empty; "not available" if it could not look; a stale review is marked stale | compute | state.rs:575; R37 items 4, 6 |
| repo, branch, start commit (pinned at claim) | compute | P3; "not available" if not reached |
| approved design revision and grant | compute | WL:220; "not available" until built |
| AGENTS.md version and hash | compute | part 4 |
| sheet hash: the sheet as given | compute | P4 |
| prompt box text | compute | this template |

**The prompt box.** You paste this as it is. Nothing in it is typed by Prima. Angle brackets show what the compute fills.

```
=== WORKSHOP JOB <page>.05.<NN> ===
Sheet: made <time EST> from log line <n>. Pack hash <hash>.
Door: open (K8 step 1 not done). Records are not proof.
You are: <builder>. Claim: <claim owner | not claimed>.
Repo: <repo>  Branch: <branch>  Start: <commit pinned at claim>
Read first: AGENTS.md (version <v>, hash <hash>)
Pack: <page>.05.<NN>  Tail: <tail>
Dev page: <04NN.keyword> <linked | found, not linked>
Lab page: <07NN.keyword> <linked | found, not linked | not yet made>
Earlier returns: <list | none>
Jobs: <w01 title>; <w02 title>
Stop if: <stop if>
Not available: <fields | none>
Hand back: one return, in the return template order,
by the road back in P6 (not settled). Do not edit AGENTS.md.
=== END JOB ===
```

## 3. The return template

Your words: "Yes returns, must state what was done, what was created, what the model noticed, an unprompted and overflow from the model should be captured for review at the end of the return. After the job items." (t226u:11)

What your words fix: unprompted and overflow come at the end, after the job items. They do not say where done, created and noticed go. So the order is open (P1). Both orders are shown. Every part is in both.

| Part | Filled by | Source | Order A (earlier) | Order B (Tester) |
|---|---|---|---|---|
| what was done | builder | t226u:11 | 1 | inside each job item |
| what was created: exact file paths | builder | t226u:11; WL:189 | 2 | inside each job item |
| what the model noticed | builder | t226u:11 | 3 | 3 |
| job items: w01, w02 ... each done, blocked or need, with its evidence, and any deviation with its why | builder | WL:189-191 (deviations: S02, WL:189) | 4 | 1 |
| proof: commit SHA(s) and test output | builder | your yes on change 3 (t226u:11); WL:189 | 5 | inside each job item |
| questions, permission asked, solutions proposed to what blocked it | builder | WL:192 | 6 | 2 |
| what it did not do | builder | R37 item 10, DIRECTOR-RULINGS.md:204 | 7 | 4 |
| notes, with a why | builder | WL:193 | 8 | 5 |
| cost: time, tries, tokens, dollars; "not reported" is not zero | builder | W5, WORK-BOOK-CONCEPT.md:263-267 (still open) | 9 | 6 |
| unprompted | builder | t226u:11; WL:193 | 10 | 7 |
| overflow | builder | t226u:11; WL:193 | 11 | 8 |

Order B option (Tester): a one-line summary on top, made by the compute from the job results, not typed.

**Who sends it.** Only the model that holds the claim (crates/seqaddr-core/src/state.rs:563-567). Today that model cannot reach the compute (P6). The compute returns only in recovery (:566-571). Prima does not relay it. The return text goes in once, through the gate. Git holds the code and the commit hash, never the return text and never books/ (W10).

Unprompted and overflow come last, after the job items. Notes, unprompted and overflow may each be empty, with a why (WL:245).

**What the compute adds or checks** (all planned, 7):
- **delivery id:** the builder sends one. A retry with the same id gets the first answer back, and the id can never carry new content (R37 item 2, DIRECTOR-RULINGS.md:196; docs/design/CORE-AND-TOOLS-SPEC.md:264).
- **return hash:** the compute hashes the return when it moves open -> return. A review is tied to that hash (R37 item 4, DIRECTOR-RULINGS.md:198).
- **commit exists:** the compute checks each SHA in part 5 is on Amalgamour/Workshop. A missing one blocks acceptance (WL:244).
- **shape:** all eleven parts present, in the order you pick (P1) (WL:244-245).

## 4. The AGENTS.md slot per work page (W2, proposal 7)

W2 is still open. This is a proposal only.

- **Stored on the page.** The work page keeps one AGENTS.md, written only through the compute. Matthew, t239u: "01 holds the agents.md as a card." (DIRECTOR-WORDS-t239u.md:10). Whether the per-job file stays as a copy is WORK-BOOK-CONCEPT.md F4.
- **A copy per job.** For each job, the compute writes a copy at the root of a fresh worktree. The copy carries the page version it came from and a hash (SPEC B2; docs/design/WORK-BOOK-SPEC.md:381-388).
- **One shape.** The copy is the pack's fields in SPEC B2 order (the last column of part 1). AGENTS.md adds nothing the pack does not hold.
- **No edits.** The builder never edits it. If the page changes, old copies go stale (R37 item 4).

## 5. Filled example: the first pack

The first pack from the concept: the handoff sheet and the board, read-only. Values in <...> are placeholders. No real SHA is shown.

**Bootstrap exception (proposal, 7; the approval is yours; waits on W8).** Pack 1 cannot pass through the tool it builds. It goes in as `pack` with no check (crates/seqaddr-core/src/tail.rs:95-97). To keep hand-typed shape out (t227u:5), Tester's way (P8):
- A. A one-off script reads the field rows of part 1 as its only shape. It fills the compute rows from real sources and leaves Prima's rows empty for Prima.
- B. A different view (not Prima, Designer or Tester) checks it field by field against WL:238-250, and the check is recorded before it goes in.
- No override page (R21, DIRECTOR-RULINGS.md:83). The exception is recorded as your one-time grant (a t-number) and B's check note, both named in the pack (P8).
- It is the first real use of the claim route while the K8 door is open. One time only.

```
address:     <page>.05.<NN>                      (compute)
tail:        pack (bootstrap: filled by script A, checked by B, P8) (compute)
by:          <Prima's token name>                (compute)
made at:     <time EST>                          (compute)
pack hash:   <taken when put; not available: no hashing yet> (compute)
claim:       not claimed                         (compute)
baseline:    <repo> <branch> <commit pinned at claim>   (compute)
pull:        crates/compute/src/lib.rs, crates/compute/src/store.rs,
             crates/seqaddr-core/src/state.rs,
             crates/compute/tests/               (compute)
predecessor: none                                (compute)
linked:      <04NN.keyword>; lab: not yet made (by link only, P7) (compute)
authorized:  <a fresh t-number from you, P2>     (Prima; compute checks)
lead:        <lead letters>                      (Prima)
outcome:     the compute prints the handoff sheet and the board (Prima)
overview:    t227u:5, t226u:9                    (Prima)
may touch:   the four paths above                (Prima)
must not:    books/, kernel/, docs/              (Prima)
stop if:     a field needs a stored 05.00 (R9), or any book write (Prima)
grant:       no book writes; code edits in the four paths only: one route, board columns, one test file (Prima)
risk:        proposed <low>; floor <compute>; effective <compute>
w01:         handoff sheet route, one slot, fixed shape (Prima)
w02:         add claim, reviewer, outcome to the existing board
             (state.rs:296-300), still from the log (Prima)
checks:      cargo test --workspace; reviewer: no test removed,
             routes write nothing                (Prima)
read first:  docs/design/PACK-TEMPLATE.md; WL:160, :220 (Prima)
hand back:   return by part 3                    (compute)
```

## 6. Exists today, and planned

- **Exists today:** the tail rules (crates/seqaddr-core/src/tail.rs:79-99). The compute answers only on its own machine, 127.0.0.1, unless started with --allow-remote (crates/compute/src/main.rs:4, :12). The claim and one-step tail move through the gate, with first claim wins, claim recorded, the return on the same counter, and no builder reviewing its own return (crates/seqaddr-core/src/state.rs:543-581; crates/compute/tests/http.rs:134, :139). A board of tails, built from the counters, never stored (crates/seqaddr-core/src/state.rs:296-300; crates/seqaddr-core/src/resolve.rs:182-188).
- **Planned, not seated:** every template in this file; the check step (WL:171, :236-245); the handoff sheet; the board's claim, reviewer and outcome columns; the prompt box; hashes; delivery ids; the commit check; the AGENTS.md copy. WL:232 still says `7`. No hash or delivery-id code exists in crates/compute or crates/seqaddr-core today.

## 7. Open questions, top three first

Carried, not repeated: W2 (AGENTS.md slot), W8 (page type), W9 (return on the same counter), W10 (a push is not a book change), W11 (board is a view), W12 (which piece first), W13 (seat templates first), all in docs/design/WORK-BOOK-CONCEPT.md and docs/design/WORK-BOOK-SPEC.md. D1-D5 in docs/design/DEV-WORK-LAB-PAGES.md.

Which wait on W8: P8 waits on W8 (pack 1 needs a page, and its type locks once set: R36, DIRECTOR-RULINGS.md:189-190). The others do not.

### P6 (TOP). How does the builder hand back? (ANSWERED, t239u)
**Answered by Matthew, t239u (DIRECTOR-WORDS-t239u.md:11).** Answered, not ruled; no R-number.
- His words: "3. Yes, see 2."
- Designer reading (7): yes to P6 with WORK-BOOK-CONCEPT W10, per Prima's mapping (DIRECTOR-WORDS-t239u.md:13). "see 2" reads as: the return lands on the 05 pass he describes in item 2. The two changes named in part 2 are read as covered by this yes (7: confirm). The four parts below are kept as asked.
1. **Question.** The builder runs on your computer. The compute answers only on its own machine (127.0.0.1), unless started with --allow-remote (crates/compute/src/main.rs:4, :12). The builder also has no writer token (crates/compute/src/identity.rs:3-7). So it cannot claim or return. How does the return get back?
2. **Proposed answer (Designer, 7).** Now: when the compute records the claim, it makes a one-job pass (a single-use code) and prints it in the prompt box. The builder puts its return in one file at a fixed path in its pushed commit, outside books/. After Prima pulls, the compute (not Prima) reads that file, checks the pass and the claim, and records it as the claim holder's return. The pass then dies. Later: once the local Workshop runs on your machine (t212u:6), the builder hands back to that compute directly. Not proposed: opening the compute to the network with --allow-remote.
3. **Why.** No new door to the network (your Host check, R33 item 4, DIRECTOR-RULINGS.md:165-166). Who gets hurt otherwise: you, queueing a model that can never hand back (Tester); or, with an open port, anyone who finds it. Two changes this needs, both for your yes: W10 said the return text never goes in git; and today only the claim holder's own token may return (crates/seqaddr-core/src/state.rs:563-571).
4. **Axioms checked.** 1 [Axioms.md:13] pass: no new network grant; the compute grants one job only. 3 [Axioms.md:17] pass: the compute leads the transfer. 6 [Axioms.md:23] pass: the return names its claim and commit. 8 [Axioms.md:27] tension: the return travels through git, then the book; two places for a time. 9 [Axioms.md:29] tension: untried.

### P1 (TOP). Which order does a return use?
1. **Question.** Your words: "what was done, what was created, what the model noticed, an unprompted and overflow from the model should be captured for review at the end of the return. After the job items." (t226u:11). They fix one thing: unprompted and overflow go last, after the job items. Do done, created and noticed go before the job items (order A), or inside and after them (order B)?
2. **Proposed answer (Designer, 7, now with Tester).** Order B, with a one-line summary on top made by the compute from the job results, not typed. You still read "what was done" first, and each done-line sits next to its job. Earlier this file said order A was your order. That was too strong: your sentence does not place done, created or noticed. You pick. Tester's way to pick: see both orders filled for one small job.
3. **Why.** WL:189-193 and the concept (WORK-BOOK-CONCEPT.md:167-174) put job items first. Who gets hurt otherwise: the reviewer, matching a done-line to its job by hand; or you, reading two shapes.
4. **Axioms checked.** 2 [Axioms.md:15] pass: one order, once picked. 4 [Axioms.md:19] pass: the why is recorded. 5 [Axioms.md:21] pass. 9 [Axioms.md:29] tension: untried.

### P8 (TOP). How is pack 1 made, if not by the tool? (waits on W8)
1. **Question.** Pack 1 cannot pass through the tool it builds. Hand-writing it is the drift you warned about (t227u:5), and it goes in with no check (crates/seqaddr-core/src/tail.rs:95-97). How do we make it safely?
2. **Proposed answer (Designer, 7, Tester's A then B).** A: a one-off script reads the field rows of part 1 as its only shape. It fills the compute rows from real sources (token name, clock, git SHA, the next free slot) and leaves Prima's rows empty for Prima. B: a different view (not Prima, Designer or Tester) checks it field by field against WL:238-250, and the check is recorded before it goes in as `pack`. No override page: "No overrides for now" (R21, DIRECTOR-RULINGS.md:83). Pack 1 changes no rule. The code already lets a pack be put as `pack` (tail.rs:95-97); what it skips is a check step that is not built yet. So it is recorded as a one-time grant, in three parts: (1) your yes, in your words, recorded by Prima in docs/review/DIRECTOR-WORDS-tNNNu.md, naming pack 1 only and its end; (2) pack 1's `authorized` names that t-number (P2); (3) B's field-by-field check, recorded as a note on the work page's face 06 and named in pack 1's read-first. The compute's log line for the put says "bootstrap: unchecked, grant tNNNu". It is hashed when put (P4). The grant ends when pack 1 closes.
3. **Why.** The script is not a second template: it reads this one. Who gets hurt otherwise: every later pack that copies a bad first one.
4. **Axioms checked.** 1 [Axioms.md:13] pass: granted by you and recorded, not claimed. 2 [Axioms.md:15] pass: one shape, read not copied; no override page (R21). 6 [Axioms.md:23] pass: the pack and the log line link back to your grant. 9 [Axioms.md:29] pass: an outside check before it goes in. 7 [Axioms.md:25] tension: no approval ids exist, so `authorized` names a t-number the compute can only check as text. 8 [Axioms.md:27] tension: the grant lives in a docs/review file, not a book line.

### P7. Are pages linked by number, or by a written link?
1. **Question.** You ruled pages "are matched by the CC and the title" (R18, DIRECTOR-RULINGS.md:71). The workflow draft adds: a set needs face 08 links both ways (WL:60, proposed F.2). Which does the compute use?
2. **Proposed answer (Designer, 7).** Both, in order. The number and title find the pages (R18). Only face 08 links both ways make them "linked". A page found but not linked is shown as "found, not linked" and raised (`7.8`), never used as if linked. Tester's version says "not available"; I keep "found" so you can see the page exists. This narrows R18, so it needs your yes.
3. **Why.** Axiom 8: "two pieces that match are not connected by matching" (Axioms.md:27). Who gets hurt otherwise: a builder handed the wrong design page because it shared a number.
4. **Axioms checked.** 8 [Axioms.md:27] pass. 6 [Axioms.md:23] pass: "Travel by written connections (8), not by what matches." 7 [Axioms.md:25] pass: an unlinked page is reported, not guessed. 1 [Axioms.md:13] tension: it narrows your R18. 2 [Axioms.md:15] tension: seqAddr.md:243 still makes a set by number; F.2 is not seated.

### P2. Who fills "authorized"?
1. **Question.** Prima's list gives authority to Prima. Should Prima write the approval, or only name it?
2. **Proposed answer (Designer, 7).** Prima names the approval id. The compute resolves it to your approved revision, and keeps the pack at draft if it does not resolve (WL:239). Until approval ids exist, Prima names the ruling or your t-number, and the compute checks the text exists in DIRECTOR-RULINGS.md or docs/review (Tester). Weak, but not a guess. Pack 1 needs a fresh t-number, not an old one stretched.
3. **Why.** Authority is granted, never claimed (Axioms.md:13). Who gets hurt otherwise: you, if a model writes its own authority.
4. **Axioms checked.** 1 [Axioms.md:13] pass. 6 [Axioms.md:23] pass: the pack names its approval. 7 [Axioms.md:25] tension: no approval ids exist yet. 8 [Axioms.md:27] tension (Tester): the name points to a file, not a book line.

### P3. Where does the start commit come from, and when?
1. **Question.** The compute cannot read GitHub. What does the sheet show for the start commit?
2. **Proposed answer (Designer, 7, with Tester).** Prima's push step sends the SHA it pushed through the gate. The compute checks that SHA exists in the local repo, then pins it at claim time, not pack time, because the branch may move in between. The builder's return states the commit it really started from. A mismatch blocks acceptance (WL:244). Until then, "not available".
3. **Why.** No new outside door for the compute (R33 item 4, DIRECTOR-RULINGS.md:165-166). Who gets hurt otherwise: the reviewer, comparing against the wrong base.
4. **Axioms checked.** 6 [Axioms.md:23] pass: the start is recorded. 7 [Axioms.md:25] pass: "not available", not a guess. 1 [Axioms.md:13] pass: no new grant. 8 [Axioms.md:27] tension: git and the book hold different halves.

### P4. What is hashed, and when?
1. **Question.** Which hashes does the compute keep?
2. **Proposed answer (Designer, 7).** Five: the pack at draft -> pack; the pack when put, for pack 1, which skips that step; the handoff sheet as given; the AGENTS.md copy; and the return at open -> return. The method is `7`. Tester's larger option, each log line carrying the hash of the one above, is its own later pack.
3. **Why.** A review must match what it read (R37 item 4, DIRECTOR-RULINGS.md:198). The builder reads the sheet, not the pack. Who gets hurt: you, approving work done from a sheet nobody can replay.
4. **Axioms checked.** 6 [Axioms.md:23] pass. 9 [Axioms.md:29] pass: review binds to a version. 2 [Axioms.md:15] pass: a hash is not a copy. 7 [Axioms.md:25] tension: method not chosen.

### P5. Where does the sheet shape live, and when does the code copy end?
1. **Question.** The sheet shape belongs with the seated templates (W13). Pack 1 needs it first. "Ends the day the template is seated" has no date, because nothing is seated (WL:232 is still `7`). When does the code copy end?
2. **Proposed answer (Designer, 7).** Seat it in the W13 set. For pack 1 only, a code copy that names this file. It ends when pack 2 closes passed; pack 2 seats the templates (WORK-BOOK-CONCEPT.md:152). If pack 2 does not pass, the copy stays and is raised, not left quietly.
3. **Why.** You get the prompt box sooner, and the copy has a real end. Who gets hurt otherwise: every worker, if the code copy outlives the seated one.
4. **Axioms checked.** 2 [Axioms.md:15] tension: a second copy, for a time. 1 [Axioms.md:13] pass: you approve the exception. 8 [Axioms.md:27] pass: it names this file. 7 [Axioms.md:25] pass: marked `7`, with a stated end.

## Differences from Prima's list

- Prima's list has the compute fill address, counter, tail, hashes, claim owner and files to pull. Kept. I added made-at, by, predecessor, matched pages, and the fixed hand-back line to the compute, each with a reason in part 1.
- Prima's list gives "authority" to Prima. I split it: Prima names the approval, the compute checks it (P2).
- Prima's list gives "scope" to Prima. Kept, as frame, stop if and grant; the compute checks the grant (WL:241).
- Risk is shared: Prima proposes, the compute records the floor (WL:114). It is the one field with two writers, as WL says.
- Hashes: no hash code exists today. They are planned.
- The return order Prima gave is one reading of your sentence. Your sentence fixes only that unprompted and overflow come after the job items (P1).
- Prima's add-on says the sheet shape goes in a seated template, not code. Agreed as the goal. For Pack 1 only, I keep Tester's option of a named code copy (WORK-BOOK-CONCEPT-CHECK.md:155-156), ending when pack 2 closes (P5).

## Cites in Tester's check, opened

- Pass: crates/compute/src/main.rs:4 (non-loopback refused unless --allow-remote) and :12 (default 127.0.0.1:7700). WL:189, :192, :193. WORK-BOOK-CONCEPT.md:167-174 (jobs first). R18 (DIRECTOR-RULINGS.md:71-72). R33 item 4 (:165-166). tail.rs:95-97. WL:238-250.
- Close: store.rs:731-733 for `by` from the token; the comment is at :730, the code at :731-733. W5 is at WORK-BOOK-CONCEPT.md:263-267 (Tester wrote 264-267).
- Differs: Tester placed the R7 override page in the behavior range 0020-0049; R7's own reading (DIRECTOR-RULINGS.md:32) puts it in 0001-0009. Moot now: Tester withdrew the override page under R21 (DEV-WORK-LAB-PAGES-CHECK.md, 2f06fd3), and P8 no longer uses one.
- Not here: Tester's note that WORK-BOOK-CONCEPT.md says "three paths" where four are listed is a fix for that file, not this one.
