# WORKING PATH: a recommendation for Prima, not a ruling.
# Tester (Grok Bot): what face 05 holds (D6).

Subject: D6 in docs/design/DEV-WORK-LAB-PAGES.md at 351fe49 (HEAD;
file unchanged). Mon 16 Nov 2026, 8:57 PM EST. Only Matthew rules.
D6 came from my own top issue in 2f06fd3. This is solving, not a
trial; options are judged on their merits.
Cites: D = that file at 351fe49 (D6 at D:167-171). RUL = docs/spec/
DIRECTOR-RULINGS.md. WL = docs/spec/workflow-loop.003.md. SA =
docs/spec/seqAddr.md. Axioms.md (docs/spec): 1 :13, 2 :15, 3 :17,
5 :21, 6 :23, 7 :25, 8 :27, 9 :29.

## The clash in plain words

- R22 (RUL:88): every page's face 05 holds "the work pack to
  reach that page's MVP". R23-R24 (RUL:90-97): it climbs 05.01,
  05.02 ..., and the best pack is seated when the page is done.
- S12 (WL:92): dev face 05 holds design questions. D:68 puts
  trials on lab face 05.
- SA:155 calls face 05 "tasks: passes, as counters". SA:199: "A
  counted face is never seated." The code agrees: a plain body
  on face 05 is refused (crates/seqaddr-core/src/state.rs:459-460).

Fact for every option that keeps R22: seating face 05 is not
possible today. SA:199 and state.rs:459 must change first.

## Options (one idea each)

A. R22 everywhere; questions leave the book. Face 05 is each
   page's own pack. Design questions stay in docs lists, as now
   (Designer's lean, D:169).
B. R22 everywhere; questions become cards. Dev face 05 holds the
   dev page's own design passes. Each design question is a work
   card in a pass. A card that needs Matthew ends `need` and is
   raised (WL:191). Lab face 05 holds trial passes.
C. All three on the work page. Questions and trials become typed
   slots on the work page's face 05 (cf. the pending task and
   ticket split, SA:307). No lab page needed.
D. Questions on dev face 06. Face 06 is already counted, "models
   leaving information" (SA:156). Questions sit beside notes.
E. Questions and trials on a new face, e.g. face 10 "questions"
   (faces 10-98 are "reserved for later customization", SA:159).
   Needs a kernel change.
F. Their own linked pages. Each question or trial gets a page,
   linked by face 08.
G. R22 per set, not per page. Read "each page" as "each piece of
   work": the work page's face 05 is the one MVP pack; dev and
   lab face 05 stay free for S12 and trials.
H. Face 05 meaning set by page type. A type carries "required or
   forbidden faces" (SA:193); a type may define its face 05.
I. (New, for every R22 option.) Plain 05 holds the seated best
   pack; counters 05.01-98 are the passes. R9 removed FF.00
   (RUL:37-38), so plain "05" no longer means the board (SA:199
   "Plain FF ... means FF.00"). The board stays a view.

## Axiom check per option

A. 1 :13 pass (R22 as ruled). 2 :15 pass. 6 :23 tension:
   questions outside the book lose their line. 7 :25 pass.
   R37 item 1 (RUL:195) tension: docs lists are a second record.
   R22-R24 pass. Retires S12 (WL:92).
B. 1 :13 pass. 2 :15 pass: face 05 has one shape, passes, on
   every page. 6 :23 pass: each question and its answer stay in
   the log. 3 :17 pass: a `need` card names who leads next. 8 :27
   pass. 9 :29 pass: lab trials are passes with their own review.
   R22-R24 pass. R37 items 1, 3 pass. Retires S12. SA:155 pass.
C. 2 :15 tension: one face, three shapes. 1 :13 tension: breaks
   R22 for dev and lab. 9 :29 tension: trial sits on the slot
   it tries. t226u:7 tension: Matthew liked three linked pages.
   SA:307 is not ruled (7).
D. 2 :15 tension: notes and questions mixed on one face. SA:156
   pass in words ("leaving information"). WL:93 tension: dev
   face 06 is the lead's notes. R22 pass. Trials still homeless
   (7 :25 tension).
E. 2 :15 pass: one face, one shape. 1 :13 tension: a new face
   needs Matthew and a kernel change (R21, RUL:82-84: built in,
   not overridden; so pass if built in). 7 :25 tension until
   defined. R22 pass.
F. 8 :27 pass. 2 :15 pass. R32 (RUL:153-154) tension: linked
   pages only retire, never delete; many small pages forever.
   7 :25 tension: "a hole nothing requires stays empty".
G. 1 :13 tension: a new reading of R22's "each page" by a model.
   Axiom 4 :19 tension: R22's why ("explain what you learned"
   per page) is lost for dev and lab. S12 pass.
H. 2 :15 pass if the type is named. R36 (RUL:189-190) tension:
   page type locks, so a wrong face 05 rule is locked in. Depends
   on W8. R22 tension unless every type keeps 05 as a pack.
I. 6 :23 pass: passes stay, seated best on top (R24). 2 :15
   pass. R9 pass. R23-R24 pass. SA:199 tension: needs a new step.
   Code change at state.rs:459-460 and resolve.rs:182-188.

## Best option: B with I

Plain words: face 05 means one thing on every page: that page's
own passes, with the best one seated. Questions are jobs in a
design pass. Trials are passes on the lab page.
Why:
- It keeps R22-R24 as Matthew ruled them, with no new reading
  (axiom 1 :13). Only S12's line on dev face 05 changes, and
  that goes to Matthew.
- One face, one shape (axiom 2 :15). A builder reading any
  face 05 knows what it holds. Hurt otherwise: every builder,
  reading one face two ways (D:170).
- Questions stay in the one log with their answers (R37 item 1,
  RUL:195; axiom 6 :23). Under A they live in docs lists.
- The seated lab 05 becomes the best hostile trial for that
  work, so the next trial starts from what broke last time.
  That is R23's reason (RUL:92), applied to trials.
- I is needed by any R22 option; it costs one SA step and a
  small code change.
Cost: S12 (WL:92) is a Director direction. B retires part of it.
Matthew must say yes. WL:6: .003 review is still due (9).

## D1 and D5 under B with I

D1 (lab page purpose): the lab page tries to break the work.
Each trial is a pass on lab face 05: claimed, returned, reviewed,
like a pack. Each names the exact return it tried. Only for
governing or higher-risk work (WL:200). The lab page is made at
the first trial (D:174-177). The best trial is seated on plain
lab 05 and re-run on the next return. D1 still waits on W9.

D5 (Prima's dev note): unchanged in place. The note stays on dev
face 06 (WL:93, SA:156), linking the return and trial it read.
New: a question the note raises becomes a card in the next dev
pass on dev face 05, not a loose item. The narrow gate stays:
only after an earlier pack on that work page has closed. D5
still waits on W13 and W9.

## Question for Matthew (t189u form)

1. Question: you ruled that every page's face 05 holds that
   page's own work pack, seated when done (R22-R24). The
   workflow puts design questions on the dev page's face 05
   (S12). Should face 05 mean the same thing on every page?
2. Proposed answer: yes. Face 05 is always the page's own
   passes, with the best pass seated on top. Design questions
   become jobs inside a design pass on the dev page. Trials
   become passes on the lab page. S12's line about dev face 05
   is replaced.
3. Why: one face, one meaning, so no builder reads it two ways.
   Your R22-R24 stay as you said them. Questions and their
   answers stay in the one record (R37 item 1). Who gets hurt
   otherwise: every builder, and you, reading two shapes.
4. Axioms checked: 1 [Axioms.md:13] pass: your ruling stands;
   2 [Axioms.md:15] pass: one shape; 6 [Axioms.md:23] pass:
   questions keep their line; 9 [Axioms.md:29] pass: trials are
   reviewed passes; 7 [Axioms.md:25] tension: seating face 05
   needs a spec step (SA:199) and a code change first.
