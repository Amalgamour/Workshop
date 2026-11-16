# Pack template: the fixed shape the compute fills

For Matthew. By Designer. A proposal (7), not a ruling. Nothing here is decided. Only you approve.
created: Mon 16 Nov 2026, 5:54 PM EST

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
4. **The return.** What the builder hands back, in the order you set (t226u:11).

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

In plain words: Prima fills the left part (what and why). The compute fills the right part (where, when, from which code). Each field has one owner.

| # | Field | Filled by | Why that owner | Source | SPEC B2 section |
|---|---|---|---|---|---|
| 1 | address (page, face 05, counter NN) | compute | the compute gives out the next free slot | WL:105-116; seqAddr.md:128 | 1 Header |
| 2 | tail | compute | only the compute moves draft -> pack and review -> closed | crates/seqaddr-core/src/state.rs:548-556 | 1 Header |
| 3 | by (who made it) | compute | the gate knows who is calling; a model cannot claim to be someone else | WL:105 | 1 Header |
| 4 | made at | compute | real clock, not typed | proposal (7) | 1 Header |
| 5 | pack hash | compute | a hash is a binding (R37 item 3) | DIRECTOR-RULINGS.md:197 | 1 Header |
| 6 | claim owner | compute | first claim wins, recorded at pack -> open | state.rs:543, :561 | 1 Header |
| 7 | repository baseline: repo, branch, start commit | compute | read from GitHub at pack time: Amalgamour/Workshop, prima/build | WL:116 (`7` on format) | 1 Header |
| 8 | files to pull from GitHub | compute | taken from the frame paths (field 15), checked to exist | R37 item 7, DIRECTOR-RULINGS.md:201 | 8 Links |
| 9 | predecessor (earlier pack or return) | compute | it is in the records | WL:115 | 8 Links |
| 10 | matched pages: dev 04NN, lab 07NN | compute | same NN; the compute finds them (W11 board, concept) | WL:59 | 8 Links |
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

All 24 rows are a proposal (7). Rows 4, 5, 7, 8, 22, 23, 24 add to Prima's list (see Differences).

## 2. The handoff sheet template

In plain words: before each handoff the compute reads the live records and prints this sheet. It is a view. It is never stored as a new authority (WL:220). If a record changes, the sheet is made again.

| Field | Filled by | From |
|---|---|---|
| door label: "door open: not proof" until K8 step 1 lands | compute | WORK-BOOK-CONCEPT-CHECK.md:126 |
| sheet made at, and the last log line read | compute | the log |
| pack text (fields 1-24) | compute | the pack counter |
| tail | compute | the counter |
| claim holder, or "not claimed" | compute | state.rs:561 |
| dev page 04NN and lab page 07NN | compute | matching NN, WL:59 |
| earlier returns on this slot and its predecessor: "none" only if looked and empty; "not available" if it could not look; a stale review is marked stale | compute | state.rs:575; R37 items 4, 6 |
| repo, branch, start commit | compute | GitHub; "not available" if not reached |
| approved design revision and grant | compute | WL:220; "not available" until built |
| AGENTS.md version and hash | compute | part 4 |
| prompt box text | compute | this template |

**The prompt box.** You paste this as it is. Nothing in it is typed by Prima. Angle brackets show what the compute fills.

```
=== WORKSHOP JOB <page>.05.<NN> ===
Sheet: made <time EST> from log line <n>. Pack hash <hash>.
Door: open (K8 step 1 not done). Records are not proof.
You are: <builder>. Claim: <claim owner | not claimed>.
Repo: Amalgamour/Workshop  Branch: prima/build  Start: <commit>
Read first: AGENTS.md (version <v>, hash <hash>)
Pack: <page>.05.<NN>  Tail: <tail>
Dev page: <04NN.keyword>  Lab page: <07NN.keyword>
Earlier returns: <list | none>
Jobs: <w01 title>; <w02 title>
Stop if: <stop if>
Not available: <fields | none>
Hand back: one return, in the return template order,
as a proposal through the gate. Do not edit AGENTS.md.
=== END JOB ===
```

## 3. The return template

Your words: "Yes returns, must state what was done, what was created, what the model noticed, an unprompted and overflow from the model should be captured for review at the end of the return. After the job items." (t226u:11)

In plain words, in order:

| # | Part | Filled by | Source |
|---|---|---|---|
| 1 | what was done | builder | t226u:11 |
| 2 | what was created: exact file paths | builder | t226u:11; WL:189 |
| 3 | what the model noticed | builder | t226u:11 |
| 4 | job items: w01, w02 ... each done, blocked or need, with its evidence | builder | WL:189-191 |
| 5 | proof: commit SHA(s) and test output | builder | your yes on change 3 (t226u:11); WL:189 |
| 6 | what it did not do | builder | R37 item 10, DIRECTOR-RULINGS.md:204 |
| 7 | unprompted | builder | t226u:11; WL:193 |
| 8 | overflow | builder | t226u:11; WL:193 |

**Who sends it.** Only the model that holds the claim (crates/seqaddr-core/src/state.rs:563-567). The compute returns only in recovery (:566-571). Prima does not relay it. The return text goes in once, through the gate. Git holds the code and the commit hash, never the return text and never books/ (W10).

Parts 7 and 8 come last, after the job items. Each may be empty, with a why (WL:245).

**What the compute adds or checks** (all planned, 7):
- **delivery id:** the builder sends one. A retry with the same id gets the first answer back, and the id can never carry new content (R37 item 2, DIRECTOR-RULINGS.md:196; docs/design/CORE-AND-TOOLS-SPEC.md:264).
- **return hash:** the compute hashes the return when it moves open -> return. A review is tied to that hash (R37 item 4, DIRECTOR-RULINGS.md:198).
- **commit exists:** the compute checks each SHA in part 5 is on Amalgamour/Workshop. A missing one blocks acceptance (WL:244).
- **shape:** all eight parts present, in order (WL:244-245).

## 4. The AGENTS.md slot per work page (W2, proposal 7)

W2 is still open. This is a proposal only.

- **Stored on the page.** The work page keeps one AGENTS.md, written only through the compute.
- **A copy per job.** For each job, the compute writes a copy at the root of a fresh worktree. The copy carries the page version it came from and a hash (SPEC B2; docs/design/WORK-BOOK-SPEC.md:381-388).
- **One shape.** The copy is the pack's fields in SPEC B2 order (the last column of part 1). AGENTS.md adds nothing the pack does not hold.
- **No edits.** The builder never edits it. If the page changes, old copies go stale (R37 item 4).

## 5. Filled example: the first pack

The first pack from the concept: the handoff sheet and the board, read-only. Values in <...> are placeholders. No real SHA is shown.

**Bootstrap exception (proposal, 7; the approval is yours).** Pack 1 cannot pass through the tool it builds. Prima writes its text and AGENTS.md by hand, and it goes in as `pack` with no check (crates/seqaddr-core/src/tail.rs:95-99). It is the first real use of the claim route while the K8 door is open. One time only.

```
address:     <page>.05.<NN>                      (compute)
tail:        pack (entered unchecked: bootstrap exception) (compute)
by:          <Prima's token name>                (compute)
made at:     <time EST>                          (compute)
pack hash:   <not available: no hashing yet>     (compute)
claim:       not claimed                         (compute)
baseline:    Amalgamour/Workshop prima/build <commit>   (compute)
pull:        crates/compute/src/lib.rs, crates/compute/src/store.rs,
             crates/seqaddr-core/src/state.rs,
             crates/compute/tests/               (compute)
predecessor: none                                (compute)
matched:     <04NN.keyword>, <07NN.keyword>      (compute)
authorized:  <approval id, after your 7 to go>   (Prima; compute checks)
lead:        <lead letters>                      (Prima)
outcome:     the compute prints the handoff sheet and the board (Prima)
overview:    t227u:5, t226u:9                    (Prima)
may touch:   the four paths above                (Prima)
must not:    books/, kernel/, docs/              (Prima)
stop if:     a field needs a stored 05.00 (R9), or any write (Prima)
grant:       read-only; add one route, board columns, one test file (Prima)
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

- **Exists today:** the tail rules (crates/seqaddr-core/src/tail.rs:79-99). The claim and one-step tail move through the gate, with first claim wins, claim recorded, the return on the same counter, and no builder reviewing its own return (crates/seqaddr-core/src/state.rs:543-581; crates/compute/tests/http.rs:134, :139). A board of tails, built from the counters, never stored (crates/seqaddr-core/src/state.rs:296-300; crates/seqaddr-core/src/resolve.rs:182-188).
- **Planned, not seated:** every template in this file; the check step (WL:171, :236-245); the handoff sheet; the board's claim, reviewer and outcome columns; the prompt box; hashes; delivery ids; the commit check; the AGENTS.md copy. WL:232 still says `7`. No hash or delivery-id code exists in crates/compute or crates/seqaddr-core today.

## 7. Open questions, top three first

Carried, not repeated: W2 (AGENTS.md slot), W9 (return on the same counter), W11 (board is a view), W12 (which piece first), W13 (seat templates first), all in docs/design/WORK-BOOK-CONCEPT.md and docs/design/WORK-BOOK-SPEC.md.

### P1 (TOP). Which order does a return use?
1. **Question.** Your sentence lists done, created, noticed, then unprompted and overflow "After the job items" (t226u:11). The concept lists the job items first (docs/design/WORK-BOOK-CONCEPT.md:155-162). Which order?
2. **Proposed answer (Designer, 7).** Your sentence order, as in part 3. Then fix the concept to match, so there is one order.
3. **Why.** You read what was done before the detail. Two orders would drift (t227u:5). Who gets hurt otherwise: you, reading two return shapes.
4. **Axioms checked.** 2 [Axioms.md:15] pass: one shape. 5 [Axioms.md:21] pass. 9 [Axioms.md:29] tension: untried.

### P2 (TOP). Who fills "authorized"?
1. **Question.** Prima's list gives authority to Prima. Should Prima write the approval, or only name it?
2. **Proposed answer (Designer, 7).** Prima names the approval id. The compute resolves it to your approved revision, and keeps the pack at draft if it does not resolve (WL:239).
3. **Why.** Authority is granted, never claimed (Axioms.md:13). Who gets hurt otherwise: you, if a model writes its own authority.
4. **Axioms checked.** 1 [Axioms.md:13] pass. 6 [Axioms.md:23] pass: the pack names its approval. 7 [Axioms.md:25] tension: no approval ids exist yet.

### P3 (TOP). Where does the start commit come from?
1. **Question.** Prima's list says the start commit is on Amalgamour/Workshop prima/build. The compute has no GitHub read today. What does the sheet show?
2. **Proposed answer (Designer, 7).** The compute reads the tip of prima/build at pack time and records it in the pack. Until it can, the sheet says "not available".
3. **Why.** A builder starting from the wrong commit builds on the wrong code. Who gets hurt: the reviewer, comparing against the wrong base.
4. **Axioms checked.** 6 [Axioms.md:23] pass: the start is recorded. 7 [Axioms.md:25] pass: "not available", not a guess. 1 [Axioms.md:13] tension: the compute needs a read grant to GitHub.

### P4. What is hashed, and when?
1. **Question.** Which hashes does the compute keep?
2. **Proposed answer (Designer, 7).** Three: the pack at draft -> pack, the AGENTS.md copy, and the return at open -> return. The method is `7`.
3. **Why.** A review must match what it read (R37 item 4). Who gets hurt: you, approving a page that changed after review.
4. **Axioms checked.** 6 [Axioms.md:23] pass. 9 [Axioms.md:29] pass: review binds to a version. 7 [Axioms.md:25] tension: method not chosen.

### P5. Where does the sheet shape live?
1. **Question.** The sheet shape belongs with the seated templates (W13; Tester, WORK-BOOK-CONCEPT-CHECK.md:137-138). Pack 1 needs it before they are seated. What then?
2. **Proposed answer (Designer, 7).** Seat it in the W13 set. For Pack 1 only, a code copy that names this file, as part of the bootstrap exception, ending the day the template is seated (Tester's option, WORK-BOOK-CONCEPT-CHECK.md:155-156).
3. **Why.** You get the prompt box sooner, and the copy has an end. Who gets hurt otherwise: every worker, if the code copy outlives the seated one.
4. **Axioms checked.** 2 [Axioms.md:15] tension: a second copy, for a time. 1 [Axioms.md:13] pass: you approve the exception. 8 [Axioms.md:27] pass: it names this file. 7 [Axioms.md:25] pass: marked `7`.

## Differences from Prima's list

- Prima's list has the compute fill address, counter, tail, hashes, claim owner and files to pull. Kept. I added made-at, by, predecessor, matched pages, and the fixed hand-back line to the compute, each with a reason in part 1.
- Prima's list gives "authority" to Prima. I split it: Prima names the approval, the compute checks it (P2).
- Prima's list gives "scope" to Prima. Kept, as frame, stop if and grant; the compute checks the grant (WL:241).
- Risk is shared: Prima proposes, the compute records the floor (WL:114). It is the one field with two writers, as WL says.
- Hashes: no hash code exists today. They are planned.
- The return order Prima gave matches your sentence, but not the concept's list (P1).
- Prima's add-on says the sheet shape goes in a seated template, not code. Agreed as the goal. For Pack 1 only, I keep Tester's option of a named code copy with an end date (WORK-BOOK-CONCEPT-CHECK.md:155-156), since nothing is seated yet (P5).
