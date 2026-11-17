# Dev, work and lab pages: three pages, linked, for one piece of work

For Matthew. By Designer. A proposal (7), not a ruling. Nothing here is decided. Only you approve.
created: Mon 16 Nov 2026, 7:00 PM EST

## Cite key

- "t226u:7": docs/review/DIRECTOR-WORDS-t226u.md, line 7 (your recorded words).
- "WL": docs/spec/workflow-loop.003.md. "SA": docs/spec/seqAddr.md. "DR": docs/spec/DIRECTOR-RULINGS.md.
- "PT": docs/design/PACK-TEMPLATE.md (7579788). "WC": docs/design/WORK-BOOK-CONCEPT.md (54b737d).
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
- You approve the dev page.
- Prima hands a job to the compute. The compute puts the pack on the work page.
- A model does the job and hands back a return, on the same slot.
- A second model tests that return on the lab page.
- Prima reads it all and writes a note back on the dev page.

## What each page holds

All from WL:40-49 and WL:83-93 unless marked proposal (7).

**Dev page (04NN).**
- Face 04: the design, long form, for you. What the work is, its first goal, what we are trying to prove (WL:45, :87).
- Face 01: a short brief of the same thing, for models (WL:87).
- Face 05: design questions, as slots (WL:92, approved S12).
- Face 06: Prima's notes after each return. Each note names the return it read (WL:93).
- Face 08: links to the work page and the lab page, both ways (WL:60).
- Your approval is of one version of this page (WL:88, approved S01).

**Work page (05NN).**
- Face 05: the packs. One pack per slot: 05.01, 05.02 ... (WL:99).
- Each return goes on the same slot as its pack (WL:181). That is still W9.
- Face 08: links back to the dev page and on to the lab page.

**Lab page (07NN).**
- Holds cold trials of the work: another model tries to break it (WL:48; axiom 9).
- A trial is required before a governing change is promoted (WL:29, approved S10).
- Which face holds a trial is not written anywhere. Proposal (7): face 05 slots, one trial per slot, each naming the exact return it tried (D1).
- Face 08: links back to the work page and the dev page.

## How they link

Forward, each step points on:
- dev -> work: a pack names the dev page version it rests on (WL:106, `authorized`).
- work -> lab: a trial names the exact return it tried. A trial is tied to that version and goes stale if it changes (R37 item 4, DR:198).
- lab -> dev: Prima's note on dev face 06 names the return and trial it read (WL:93).

Back, each step points home:
- Each page's face 08 links to the other two, both ways (WL:60; axiom 8).
- A link points to the page, address plus title, not to a version (R32, DR:151-152).

One rule to remember: **the same number helps you find a page. Only a written link connects it.** "Matching counter numbers may help a reader but are never evidence of connection" (WL:93). Axiom 8: "two pieces that match are not connected by matching" (Axioms.md:27).

## Where each sits in seqaddr

- Bands (WL:40-49, approved S05): 03NN build, 04NN dev, 05NN jobs, 07NN colab (labs).
- One subject, one number across bands: "design `0401.timer`, packs and returns `0501.timer`, build `0301.timer`, labs `0701.timer`" (WL:59).
- Status lives only on slots: "Workflow state lives only on counters." (SA:140)
- A slot's steps (SA:128-137; WL:163): draft -> pack -> open -> return -> review -> closed (no tail word).
- On the work page these are the pack's steps. On the lab page, proposal (7): a trial uses the same steps (D1).
- Pages carry only draft or retired (SA:126). A page itself never moves through pack or review.
- The board is a view the compute builds, never a stored 05.00 (R9, DR:37-38; WC W11).
- Spec conflict, not fixed here: SA:243 calls 0523 "build". WL names 05NN jobs and 03NN build (D4).

## How it fits the pack template and the work book concept

Your rule: "The compute fills templates, bindings, and hashes, and the model writes only the judgment." (R37 item 3, DR:197)
Your words: "But you should hand the jobs to the compute, It basically gives you a constand template that won't drift. Otherwises you will." (docs/review/DIRECTOR-WORDS-t227u.md:5)

In plain words:
- Prima hands the job to the compute. The compute writes the pack in the fixed shape (PT part 1).
- Packs are not hand-written after pack 1. Pack 1 is the one bootstrap exception (PT:10; WC:146).
- The compute fills the links between the three pages. They are bindings, so they are the compute's job.
- Prima writes only the judgment: the why, the jobs, the stop point (PT rows 12-23).

Where the three pages show up:
- PT row 10, "matched pages: dev 04NN, lab 07NN", filled by the compute. This file keeps that. It adds one rule: show a page as matched only when face 08 links it both ways. A page that only shares the number is shown as "found by number, not linked" (D2). PT is not changed here; that waits for Tester's PACK-TEMPLATE-CHECK.
- The handoff sheet and prompt box already print "Dev page" and "Lab page" (PT part 2). Same rule.
- The check step (draft -> pack) is the compute's (WL:171). Proposal (7): it also checks the dev page link opens, else `7.8` (WL:61).
- The handoff sheet is a view, made fresh from the records (WL:220, approved S06).
- The templates are not seated yet (WL:232, "`7`"). See W13.

The return, in your order (t226u:11; PT part 3): what was done, what was created, what the model noticed, the job items, proof, what it did not do, unprompted, overflow. The order is still P1.

The return stays on the work page. The lab page tests it. It does not hold it.

## Worked example (EXAMPLE ONLY: made-up addresses, nothing real)

Subject: a handoff sheet. Number 42. Title "sheet". All addresses are EXAMPLE.

```
EXAMPLE 0442.sheet   dev page
  04  design: print one fixed-shape sheet per pack slot     (Prima drafts; you approve)
  01  brief for models                                      (Prima drafts; you approve)
  05.01      question: should the sheet show the reviewer?  (design question)
  06.01      note: read 0542.05.01 return and 0742.05.01 trial (Prima writes; compute fills the links)
  08  links: 0542.sheet, 0742.sheet (both ways)             (compute)

EXAMPLE 0542.sheet   work page
  05.01.pack    the compute writes it from Prima's judgment fields (PT part 1)
                authorized: <your approval of 0442 version N>  matched: 0442.sheet, 0742.sheet
  05.01.open    claimed by the builder (compute records who and when)
  05.01.return  the return, in t226u order, on the same slot (W9)
  05.01.review  a reviewer, not the builder, takes it
  05.01         closed, outcome: passed
  08  links: 0442.sheet, 0742.sheet (both ways)             (compute)

EXAMPLE 0742.sheet   lab page (face 05 here is proposal 7, D1)
  05.01         trial of 0542.05.01 return <hash>: tried to make the sheet guess a missing field
  08  links: 0442.sheet, 0542.sheet (both ways)             (compute)
```

Reading it: you approve 0442. The compute writes the pack on 0542. The builder returns on the same slot. A second model tries to break it on 0742. Prima writes a note on 0442 face 06. The next pack starts from that note.

## Exists today, and planned

- **Exists today:** tail rules and one-step moves (crates/seqaddr-core/src/tail.rs:79-99); claim, return on the same slot, and no self-review (crates/seqaddr-core/src/state.rs:543-581); a tail-only board view (state.rs:296-300). These work on any page's slots.
- **Planned:** the three-page set made in one step; face 08 links checked both ways; "matched" in the sheet; lab trials on slots; the templates (WL:232). No code creates or checks a set today, as far as I read.

## Where Prima's ask differs from your recorded words

- Prima wrote "work (jobs) page". You said "a work page" (t226u:7). WL calls it "jobs" (WL:46). Same page. I use "work page" in plain words, "N5 jobs" as the side label.
- Prima wrote "dev -> work packs -> lab results/returns". You did not say where returns go. WL puts the return on the work page, same slot as its pack (WL:181). The lab page holds trials (WL:48). So I keep returns on the work page (D1, W9).
- The old book's N7 was "inspect": "Man/model same space: DEMO, commands run, verify artifacts." (OWB 00.md:36). WL's N7 is cold-model trials. Which one you meant by "lab" is not recorded (D1).

## Open questions, top three first

Carried, not repeated: W8 (is a work page a system page; page type locks once set), W9 (return on the same slot), W11 (board is a view), W13 (seat templates first) in WC; P1 (return order), P5 (where the sheet shape lives) in PT.

### D1 (TOP). What is the lab page for, and where does a trial sit?
1. **Question.** Is the lab page for cold trials that try to break a return (WL:48), or for showing it working, like the old book's "inspect" page (OWB 00.md:36)? And where does a trial go?
2. **Proposed answer (Designer, 7).** Cold trials, as WL says. One trial per face 05 slot on the lab page, using the same steps as a pack. Each trial names the exact return version it tried. Returns stay on the work page (W9). A demo can be one kind of trial.
3. **Why.** The maker is the easiest one to convince (axiom 9). Keeping the return in one place stops two copies drifting. Who gets hurt otherwise: you, reading a return in two places that disagree.
4. **Axioms checked.** 9 [Axioms.md:29] pass: a trial from another view. 2 [Axioms.md:15] pass: one copy of the return. 8 [Axioms.md:27] pass: the trial links to the return it tried. 7 [Axioms.md:25] tension: no spec says which face holds a trial; this fills the hole by proposal only.

### D2 (TOP). When is a page "matched"?
1. **Question.** PT row 10 says the compute finds matched dev and lab pages by the same number. Is the same number enough?
2. **Proposed answer (Designer, 7).** No. The compute uses the number to find a page. It shows it as matched only when face 08 links it both ways. Otherwise the sheet says "found by number, not linked" and raises `7.8`. Fold into PT row 10 after Tester's PACK-TEMPLATE-CHECK.
3. **Why.** WL:93 says matching numbers are "never evidence of connection". Who gets hurt otherwise: a builder handed the wrong design page because it shared a number.
4. **Axioms checked.** 8 [Axioms.md:27] pass: "two pieces that match are not connected by matching". 6 [Axioms.md:23] pass: "Travel by written connections (8), not by what matches." 7 [Axioms.md:25] pass: an unlinked page is reported, not guessed. 2 [Axioms.md:15] tension: SA:243 still says same-number pages "form a set"; the both-ways rule is the proposed F.2 change (WL:60), not yet seated.

### D3 (TOP). Who makes the three pages and their links, and when?
1. **Question.** Who creates the work and lab pages and writes the links between all three?
2. **Proposed answer (Designer, 7).** The compute, in one change, when you approve the dev page version. It writes the work and lab pages and the face 08 links both ways. No model writes a link by hand. Page type waits for W8.
3. **Why.** Links are bindings, and "The compute fills templates, bindings, and hashes" (R37 item 3, DR:197). "Yes, books change through compute not by models." (R33, DR:159). Who gets hurt otherwise: you, if a model writes a one-way link that breaks the chain.
4. **Axioms checked.** 1 [Axioms.md:13] pass: you approve, the compute enforces. 3 [Axioms.md:17] pass: the compute leads the bindings. 8 [Axioms.md:27] pass: both ways, written. 7 [Axioms.md:25] tension: W8 (page type) is not ruled, and a set across separate books has no safe one-step write yet (WL:292).

### D4. Which number is the work page: 05NN "jobs" or "build"?
1. **Question.** SA:243 calls 0523 "build". WL (approved S05) calls 05NN jobs and 03NN build. Which stands?
2. **Proposed answer (Designer, 7).** WL's map. The spec owners fix SA:243 through its own drafting path (WL:53). This file does not edit seqAddr.md.
3. **Why.** You approved S05. Who gets hurt otherwise: a model reading SA alone and putting packs in the wrong band.
4. **Axioms checked.** 2 [Axioms.md:15] tension: the child map differs from the parent text until the named change is seated. 6 [Axioms.md:23] pass: the change is recorded as a new step, not a rewrite. 1 [Axioms.md:13] pass: your S05 approval.

### D5. Does Prima's note on the dev page come before the next pack?
1. **Question.** WL:216-217 has the lead read the return and write a dev face 06 note before each new pack. Should the compute refuse a new pack until that note exists?
2. **Proposed answer (Designer, 7).** Yes, after the check step is built (W13). The compute fills the note's links. Prima writes only what the return taught.
3. **Why.** The loop closes on the dev page, so the next pack starts from what was learned. Who gets hurt otherwise: you, if packs repeat the same detail (WL:280).
4. **Axioms checked.** 6 [Axioms.md:23] pass: each pass links to what it read. 5 [Axioms.md:21] pass: the next pack is framed by the note. 9 [Axioms.md:29] tension: untried.
