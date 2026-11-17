# Dev, work and lab pages: three pages, linked, for one piece of work

For Matthew. By Designer. A proposal (7), not a ruling. Nothing here is decided. Only you approve.
created: Mon 16 Nov 2026, 7:00 PM EST
2026-11-17 (Designer): proposed superseded by ONE-PAGE-WORK.md if Matthew says yes.

## Change note (2026-11-17, 11:30 AM EST, Designer)

D6 marked answered by Matthew, t239u (docs/review/DIRECTOR-WORDS-t239u.md:10). Not ruled. His face layout puts all faces on one page per piece; that may change the three-page split here (WORK-BOOK-CONCEPT.md F1, open).

## Change note (Mon 16 Nov 2026, 9:05 PM EST)

Folds Tester's D6 options (docs/review/FACE-05-D6-CHECK.md, e94668e). D6 stays open for you. Its proposed answer changes to Tester's "B with I", with the reason given there. D1, D5 and the dev face 05 line note what B with I would mean.

## Change note (Mon 16 Nov 2026, 8:05 PM EST)

Folds Tester's check (docs/review/DEV-WORK-LAB-PAGES-CHECK.md, 2f06fd3, "holds, with fixes").
- New D6 (TOP): face 05 is used two ways, against your R22-R24.
- Lab trials only for governing or higher-risk work (WL:29, :200). The lab page is made only when the first trial is needed.
- D3: links are written before you approve, and the approval covers faces 01 and 04, so it does not go stale (R37 item 4).
- D5 narrowed. Cite fixes: PT commit, WL:87-93, WL:200, "return template order".
- Earlier note (7:12 PM): R18 quoted; D2 points to PT P7; return order open (PT P1).

## Cite key

- "t226u:7": docs/review/DIRECTOR-WORDS-t226u.md, line 7 (your recorded words).
- "WL": docs/spec/workflow-loop.003.md. "SA": docs/spec/seqAddr.md. "DR": docs/spec/DIRECTOR-RULINGS.md.
- "PT": docs/design/PACK-TEMPLATE.md (7d11343 and the fold of 2f06fd3). "WC": docs/design/WORK-BOOK-CONCEPT.md (54b737d).
- "OWB": old work book (zip from you), /tmp/oldwb/10.10.13.brand-clerk.

## Why this file

Your words: "I did like how we had a dev page, a work page and a lab page all linked together." (t226u:7)

Your words, same line: "Mostly look up how tails work. I think it's in the sequence addressing .md" (t226u:7)

I searched your recorded words (DR and every docs/review/DIRECTOR-WORDS-*.md) for dev, work, jobs and lab pages. t226u:7 is the only place you speak about the three pages. You have not said what goes on the lab page, or how the links are made. So those parts below are proposals (7).

## The three pages, in plain words

One piece of work gets three pages. They share one number.

1. **The dev page.** What we want and why. You and the model talk here. (Side label: N4 dev, 04NN.)
2. **The work page.** The jobs. Each job is a pack. Each pack gets its return on the same slot. (Side label: N5 jobs, 05NN.)
3. **The lab page.** Where another model tries to break the work. (Side label: N7 colab, 07NN.)

The flow, one step at a time:
- The compute makes the dev and work pages and links them, while the dev page is still a draft.
- You approve the dev page.
- Prima hands a job to the compute. The compute puts the pack on the work page.
- A model does the job and hands back a return, on the same slot.
- A reviewer, not the builder, checks it there.
- Only for risky or rule-changing work: the compute makes the lab page, and a second model tries to break the return there.
- Prima reads it all and writes a note back on the dev page.

## What each page holds

All from WL:40-49 and WL:87-93 unless marked proposal (7).

**Dev page (04NN).**
- Face 04: the design, long form, for you. What the work is, its first goal, what we are trying to prove (WL:45, :87).
- Face 01: a short brief of the same thing, for models (WL:87).
- Face 05: design questions, as slots (WL:92, approved S12). This clashes with your R22 (DR:88): see D6 (answered t239u: face 05 is the page's own passes). Under D6's proposed answer, face 05 here would hold the dev page's own design passes, and each question would be a job in a pass.
- Face 06: Prima's notes after each return. Each note names the return it read (WL:93).
- Face 08: links to the work page and the lab page, both ways (WL:60).
- Your approval is of one version of this page (WL:88, approved S01). Proposal (7): it covers faces 01 and 04, the design (D3).

**Work page (05NN).**
- Face 05: the packs. One pack per slot: 05.01, 05.02 ... (WL:99).
- Each return goes on the same slot as its pack (WL:181). That is still W9.
- Face 08: links back to the dev page and on to the lab page.

**Lab page (07NN).**
- Holds cold trials of the work: another model tries to break it (WL:48; axiom 9).
- Not every return. N7 is for "required higher-risk trials" (WL:29). A governing change must have one before promotion (WL:200, approved S10). Routine work gets a separate reviewer on the work slot (WL:200, "R1"). Which risk levels beyond governing need a trial is still `7` (WL:200).
- So the lab page is made only when the first trial is needed. Until then the link says "not yet made". A linked page can never be deleted, only retired (R32, DR:153-154), so an empty lab page would stay forever.
- Which face holds a trial is not written anywhere. Proposal (7): face 05 slots, one trial per slot, each naming the exact return it tried (D1, D6).
- Face 08: links back to the work page and the dev page.

## How they link

Forward, each step points on:
- dev -> work: a pack names the dev page version it rests on (WL:106, `authorized`).
- work -> lab: a trial names the exact return it tried. A trial is tied to that version and goes stale if it changes (R37 item 4, DR:198).
- lab -> dev: Prima's note on dev face 06 names the return and trial it read (WL:93).

Back, each step points home:
- Each page's face 08 links to the other two, both ways (WL:60; axiom 8).
- A link points to the page, address plus title, not to a version (R32, DR:151-152).

Your rule for finding a set: "They are matched by the CC and the title." (R18, DIRECTOR-RULINGS.md:71)

One rule to remember: **the same number and title help you find a page. Only a written link connects it.** "Matching counter numbers may help a reader but are never evidence of connection" (WL:93). Axiom 8: "two pieces that match are not connected by matching" (Axioms.md:27).

## Where each sits in seqaddr

- Bands (WL:40-49, approved S05): 03NN build, 04NN dev, 05NN jobs, 07NN colab (labs).
- One subject, one number across bands: "design `0401.timer`, packs and returns `0501.timer`, build `0301.timer`, labs `0701.timer`" (WL:59).
- Status lives only on slots: "Workflow state lives only on counters." (SA:140)
- A slot's steps (SA:128-137; WL:163): draft -> pack -> open -> return -> review -> closed (no tail word).
- On the work page these are the pack's steps. On the lab page, proposal (7): a trial uses the same steps (D1).
- Your R22-R24 add a seated face 05 on every page (DR:88-97). seqAddr says a counted face is never seated (SA:199). Both are raised in D6.
- Pages carry only draft or retired (SA:126). A page itself never moves through pack or review.
- The board is a view the compute builds, never a stored 05.00 (R9, DR:37-38; WC W11).
- Spec conflict, not fixed here: SA:243 calls 0523 "build". WL names 05NN jobs and 03NN build. SA:243 needs a fix through its own drafting path (D4).

## How it fits the pack template and the work book concept

Your rule: "The compute fills templates, bindings, and hashes, and the model writes only the judgment." (R37 item 3, DR:197)
Your words: "But you should hand the jobs to the compute, It basically gives you a constand template that won't drift. Otherwises you will." (docs/review/DIRECTOR-WORDS-t227u.md:5)

In plain words:
- Prima hands the job to the compute. The compute writes the pack in the fixed shape (PT part 1).
- Packs are not hand-written after pack 1. Pack 1 is the one bootstrap exception: a script fills it from the template, and an outside view checks it (PT part 5, PT P8; WC:146).
- The compute fills the links between the three pages. They are bindings, so they are the compute's job.
- Prima writes only the judgment: the why, the jobs, the stop point (PT rows 12-23).

Where the three pages show up:
- PT row 10, "linked pages: dev 04NN, lab 07NN", filled by the compute. It finds them by number and title (R18), and shows them as linked only when face 08 links them both ways. Otherwise "found, not linked" (`7.8`). Same rule here (PT P7).
- The handoff sheet and prompt box already print "Dev page" and "Lab page" (PT part 2). Same rule. A lab page not yet made shows "not yet made".
- The check step (draft -> pack) is the compute's (WL:171). Proposal (7): it also checks the dev page link opens, else `7.8` (WL:61).
- The handoff sheet is a view, made fresh from the records (WL:220, approved S06).
- The templates are not seated yet (WL:232, "`7`"). See W13.

The return (PT part 3): what was done, what was created, what the model noticed, the job items, proof, questions, what it did not do, notes, cost, unprompted, overflow. Your words fix only that unprompted and overflow come after the job items (t226u:11). The rest of the order is open (PT P1).

The return stays on the work page. The lab page tests it. It does not hold it.

## Worked example (EXAMPLE ONLY: made-up addresses, nothing real)

Subject: a handoff sheet. Number 42. Title "sheet". All addresses are EXAMPLE.

```
EXAMPLE 0442.sheet   dev page
  04  design: print one fixed-shape sheet per pack slot     (Prima drafts; you approve)
  01  brief for models                                      (Prima drafts; you approve)
  05  (what face 05 holds here is D6)
  06.01      note: read 0542.05.01 return (Prima writes one line; compute fills the links)
  08  links: 0542.sheet (both ways), written before your approval;
             lab: not yet made                              (compute)

EXAMPLE 0542.sheet   work page
  05.01.pack    the compute writes it from Prima's judgment fields (PT part 1)
                authorized: <your approval of 0442 version N>
                linked: 0442.sheet; lab: not yet made
  05.01.open    claimed by the builder (compute records who and when)
  05.01.return  the return, in the return template order, on the same slot (W9; order is PT P1)
  05.01.review  a reviewer, not the builder, takes it (routine: no lab trial)
  05.01         closed, outcome: passed
  08  links: 0442.sheet (both ways)                         (compute)

EXAMPLE 0742.sheet   lab page: made only if a later pack is governing or higher-risk
  05.01         trial of 0542.05.NN return <hash>: tries to break it (face 05 here is D1, D6)
  08  links: 0442.sheet, 0542.sheet (both ways)             (compute)
```

Reading it: the compute makes 0442 and 0542 and links them. You approve 0442. The compute writes the pack on 0542. The builder returns on the same slot, and a reviewer checks it there. This job is routine, so there is no lab page. Prima writes a note on 0442 face 06. The next pack starts from that note.

## Exists today, and planned

- **Exists today:** tail rules and one-step moves (crates/seqaddr-core/src/tail.rs:79-99); claim, return on the same slot, and no self-review (crates/seqaddr-core/src/state.rs:543-581); a tail-only board view (state.rs:296-300). These work on any page's slots.
- **Planned:** the dev and work pages made and linked in one step, before approval; the lab page made on the first trial; face 08 links checked both ways; "linked" or "found, not linked" in the sheet; lab trials on slots; the templates (WL:232). No code creates or checks a set today, as far as I read.

## Where Prima's ask differs from your recorded words

- Prima wrote "work (jobs) page". You said "a work page" (t226u:7). WL calls it "jobs" (WL:46). Same page. I use "work page" in plain words, "N5 jobs" as the side label.
- Prima wrote "dev -> work packs -> lab results/returns". You did not say where returns go. WL puts the return on the work page, same slot as its pack (WL:181). The lab page holds trials (WL:48). So I keep returns on the work page (D1, W9).
- The old book's N7 was "inspect": "Man/model same space: DEMO, commands run, verify artifacts." (OWB 00.md:36). WL's N7 is cold-model trials. Which one you meant by "lab" is not recorded (D1).

## Open questions, top three first

Carried, not repeated: W8 (page type locks once set), W9 (return on the same slot), W11 (board is a view), W13 (seat templates first) in WC; P1 (return order), P5 (sheet shape), P7 (linked pages), P8 (pack 1) in PT.

Which wait: D1 waits on W9. D3 waits on W8. D5 waits on W13 and W9. D1 and D5 also wait on D6. D4 and D6 wait on none.
Update 2026-11-17: W8 and D6 are answered (t239u). D1 and D3 now wait on F1, D5 on F6 (WORK-BOOK-CONCEPT.md).

### D6 (TOP). What does face 05 hold? (ANSWERED, t239u)
**Answered by Matthew, t239u (DIRECTOR-WORDS-t239u.md:10).** Answered, not ruled; no R-number.
- His words: "2.  Yes that is the purpose of 05.counter so we can track now many passes was done and what was learned." He goes on to describe each page's faces; that whole line is quoted in WORK-BOOK-CONCEPT.md, "Work-page faces".
- Designer reading (7): yes to one meaning of face 05 on every page: that page's own passes, from 05.01. Seating the best pass (option I) is not in his words (WORK-BOOK-CONCEPT.md F5). His layout puts all faces on one page per piece, which affects this file's three-page split (F1). The four parts below are kept as asked.
1. **Question.** You ruled that every page's face 05 holds that page's own work pack, seated when done (R22, DR:88; R23-R24, DR:90-97). The workflow puts design questions on dev face 05 (WL:92, S12). Should face 05 mean the same thing on every page?
2. **Proposed answer (Tester, FACE-05-D6-CHECK.md; Designer agrees, 7).** Yes. Face 05 is always the page's own passes, with the best pass seated on top. Design questions become jobs inside a design pass on the dev page; one that needs you ends `need` and is raised (WL:191). Trials become passes on the lab page. S12's line about dev face 05 is replaced, which needs your yes. Seating face 05 is not possible today: SA:199 ("A counted face is never seated") and the code (crates/seqaddr-core/src/state.rs:459-460) must change first. Other options in the check: A, questions stay in docs lists (my earlier lean); C, all on the work page; D, questions on dev face 06; E, a new face; F, a page per question; G, R22 per set, not per page; H, face 05 set by page type (waits on W8). I (plain 05 holds the seated best pack; 05.01-98 are the passes) goes with every R22 option.
3. **Why.** One face, one meaning, so no builder reads it two ways. Your R22-R24 stay as you said them. Questions and their answers stay in the one record (R37 item 1, DR:195); under A they would live in docs lists. Who gets hurt otherwise: every builder, and you, reading two shapes. This is raised, not chosen: "Do not choose." (Axioms.md:13).
4. **Axioms checked (Tester's marks, FACE-05-D6-CHECK.md).** 1 [Axioms.md:13] pass: your ruling stands. 2 [Axioms.md:15] pass: one shape. 6 [Axioms.md:23] pass: questions keep their line. 9 [Axioms.md:29] pass: trials are reviewed passes. 7 [Axioms.md:25] tension: seating face 05 needs a spec step (SA:199) and a code change first. Designer's earlier mark kept until you rule: 1 [Axioms.md:13] tension: it retires part of S12, a direction you approved.

### D1 (TOP). What is the lab page for, and when is it used? (waits on W9 and D6)
1. **Question.** Is the lab page for trials that try to break a return (WL:48), or for showing the work running, like the old book's "inspect" page (OWB 00.md:36)? And does every return get one?
2. **Proposed answer (Designer, 7).** Trials that try to break it, as WL says. Only for governing or higher-risk work (WL:29, :200). Routine work is checked by a separate reviewer on the work slot. Each trial names the exact return version it tried. A demo, run with you, can be one kind of trial. The lab page is made only when the first trial is needed. If D6 goes Tester's way: each trial is a pass on lab face 05, claimed, returned and reviewed like a pack, and the best trial is seated on plain lab 05 and re-run on the next return.
3. **Why.** The maker is the easiest one to convince (axiom 9), but WL asks for a lab trial only where risk calls for it. Who gets hurt otherwise: you, paying a second model for every small job (Tester).
4. **Axioms checked.** 9 [Axioms.md:29] pass: a trial from another view where it is required. 2 [Axioms.md:15] pass: the return stays in one place. 8 [Axioms.md:27] pass: the trial links to the return it tried. 7 [Axioms.md:25] tension: no spec says which face holds a trial (D6), and the risk levels beyond governing are still `7` (WL:200).

### D3 (TOP). Who makes the pages and links, and when? (waits on W8)
1. **Question.** Who creates the work and lab pages and writes the face 08 links, and at what point?
2. **Proposed answer (Designer, 7).** The compute, never a model. It makes the dev and work pages and their links both ways while the dev page is still a draft, before you approve it. Your approval covers faces 01 and 04, the design (WL:87). Face 08 belongs to the compute, so a later link (the lab page, made on the first trial) does not change what you approved. Page type waits for W8.
3. **Why.** You approve one version of the dev page (WL:88, S01). If the compute wrote links on it after that, your approval would go stale: a review "goes stale when the page changes" (R37 item 4, DR:198). Links are bindings: "The compute fills templates, bindings, and hashes" (R37 item 3, DR:197). "Yes, books change through compute not by models." (R33, DR:159). Who gets hurt otherwise: you, re-approving a page because a link was added.
4. **Axioms checked.** 1 [Axioms.md:13] pass: you approve, the compute enforces. 3 [Axioms.md:17] pass: the compute leads the bindings. 8 [Axioms.md:27] pass: both ways, written. 6 [Axioms.md:23] tension: an approval that covers only some faces is new and needs your yes. 7 [Axioms.md:25] tension: W8 is not ruled, and a set across separate books has no safe one-step write yet (WL:292).

### D2. When is a page linked?
Now PACK-TEMPLATE.md P7, not repeated here. In short: number and title find the page (R18, DR:71); only face 08 links both ways make it linked; otherwise "found, not linked" (`7.8`). SA:243 still makes a set by number, and F.2 (WL:60) is not seated (WL:53). It narrows R18, so it needs your yes. Axiom marks are in P7.

### D4. Which number is the work page: 05NN "jobs" or "build"?
1. **Question.** SA:243 calls 0523 "build". WL (approved S05) calls 05NN jobs and 03NN build. Which stands?
2. **Proposed answer (Designer, 7).** WL's map: 05NN jobs, 03NN build. SA:243 is fixed by a new step through its own drafting path (WL:53). This file does not edit seqAddr.md. One line from you would confirm it: your R18 names "a workflow from N3-N7" (DR:71) but not the band roles.
3. **Why.** You approved S05 (WL:6). Who gets hurt otherwise: a model reading SA alone and putting packs in the build band. Note: review and trial of WL `.003` are still due (WL:6).
4. **Axioms checked.** 2 [Axioms.md:15] tension: the child map differs from the parent text until SA is fixed. 6 [Axioms.md:23] pass: the fix is a new step, not a rewrite. 1 [Axioms.md:13] pass: your S05 approval.

### D5. Must Prima's dev note come before the next pack? (waits on W13, W9 and D6)
1. **Question.** WL:216-217 has the lead read the return and write a dev face 06 note before each new pack. Should the compute refuse a new pack until that note exists?
2. **Proposed answer (Designer, 7).** Yes, but narrowly. Only when an earlier pack on the same work page has closed; pack 1 has nothing to note, and packs running side by side do not block each other. The compute fills the note's frame (links, return hash, outcome). Prima writes one judgment line. "Nothing learned" is allowed, with a why. If D6 goes Tester's way: the note stays on dev face 06, and a question it raises becomes a job in the next design pass on dev face 05.
3. **Why.** The loop closes on the dev page, so the next pack starts from what was learned (WL:217). A forced note with no room for "nothing" invites empty filler. Who gets hurt otherwise: you, reading notes that say nothing; or packs repeating the same detail (WL:280).
4. **Axioms checked.** 6 [Axioms.md:23] pass: each note links to the exact return it read. 5 [Axioms.md:21] pass: the next pack is framed by the note. 4 [Axioms.md:19] pass: "nothing learned" keeps its why. 9 [Axioms.md:29] tension: untried.

## Check points declined

- None declined. One narrowed: Tester's D3 option of a set record in the band's door page is not taken, because it adds a second place for links (axiom 2); face 08 stays the one place.
