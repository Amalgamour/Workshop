# Stage plan section 17 (draft note)

state: draft for Prima. Not part of STAGE-PLAN-90.50.10.md. Do not edit that file from this note.
made: 2026-11-23, 10:40 AM EST, by Cursor-C (Design).
read against: STAGE-PLAN-90.50.10.md section 15 at prima/build 78101fe6. The same sentences are at the same lines on cloud/design through 799a984c (section 16 was appended after them).
authority: Matthew, t461u, t462u, t463u (docs/review/DIRECTOR-WORDS-t461u.md on prima/build). The hostile pass is docs/trial/TRIAL-WORK-ORDER-1.md at cloud/test b11becea.

This note is what section 17 would say. Old sections stay as written (Axioms.md:23). Where this note and section 15 differ, this note is the later step, once Prima accepts it.

## 17.1 His words, quoted

t461u (DIRECTOR-WORDS-t461u.md:5): "so we don't need my words in a pack, other then when we find conflicts, forks, major issues.  You can design the packs yourself, using the WF to build them.  Then you bring to me any issues.  Otherwise if that loop can complete without me it should."

t461u (:7): "Only the core should be able to make pages with compute.  So right now yes, they can but that is temp, we are working for functionally connected prove the loop works.  We aren't looking at refining, polish or security yet."

t462u (:11): "My words live one the pages, that shape the work."

t463u (:14): "on*"

What the pages do with that: 0413 drops the pasted-quote field. His words stay on the page. 0414 prints the builder name.

Later ruling, Nov 23, 10:32 AM EST. Prima named it t492-t493u. No words file was on origin/prima/build at 78101fe6, so the lines below are his statement of the ruling, not a file quote.

1. A claim under a builder name not in the list of six (Cursor-1, Cursor-C, Codex, Claude, Grok-1, Grok-2) is not refused: wf prints it as a temp worker and assigns that worker a name (e.g. temp-1, temp-2, stable for that name), recorded in the log so the worker stays traceable. Page 0414. Files: src/cmd.rs, src/render.rs, templates/v5/prompt.txt, templates/v5/builder.txt.

2. Matthew's pages/<id>/05.NN folder on packs updates on every return, not only on publish after close. Page 90.50.10.0417, not 0413 and not 0414. Files: src/cmd.rs, src/git.rs. 0413 stays on src/render.rs (wave 6 beside 0409). Putting the push on 0413 would take cmd.rs and would push 0414 off wave 14.

## 17.2 Page 0416 joins wave 4

0405 stays parked. Its title stays on that address (DIRECTOR-RULINGS.md:129-130). Prima will pack the Windows test job as a new page, 90.50.10.0416.

- Title: "tests build and run on Windows". Titles may be reused at another address (R34, DIRECTOR-RULINGS.md:173). The address 0405 is not reused.
- Job text: the draft in docs/design/drafts/90.50.10.0405/. When it is packed, the address in those files is read as 90.50.10.0416, and the trial file is tests/lab_0416.rs. The five failures and the Linux meaning are unchanged.
- May change: tests/wf.rs only.
- Needs: 0701 pass 1 (closed) and 0415 (closed at 0e7708d3). The five failures are what that return left.
- Size: 1/2/3. Trial in lab 0701: 1/1/2.

Section 15.4 wave 4 is 0407 and 0408. 0407 changes src/render.rs. 0408 changes src/cmd.rs, src/lib.rs, and src/page.rs (section 13.5). 0416 changes tests/wf.rs. Neither needs the other. They change no shared files (t422.md:8).

| Wave | Runs | What changes from 15.4 |
|---|---|---|
| 4 | 0407, 0408, 0416 | 0416 added. render.rs; cmd.rs; tests/wf.rs |
| 5 | trials 0407, 0408, 0416 | tests/lab_0407.rs, tests/lab_0408.rs, tests/lab_0416.rs |

No other wave changes. Still 17. 0414 stays at wave 14.

## 17.3 The render.rs sentence is wrong

At prima/build 78101fe6 the sentence is lines 1226-1227. Line 1225 is blank. The job named 1225-1226. The words are:

"Exactly 17. 0414 cannot share a wave with any other cmd.rs page, and every render.rs slot before wave 14 is taken."

The first clause is right. 0414 changes src/cmd.rs, and cmd.rs is held from wave 2 through wave 13: 0404, then 0408, 0409, 0406, 0411, 0412, each until its trial. The second clause is wrong. render.rs is free in waves 10 through 13. 0411 and 0412 change src/cmd.rs and src/lib.rs only (section 13.5). They do not change src/render.rs. 0414 still cannot start in those waves, because of cmd.rs, not because render.rs is busy. The trial named this minor 1.

Replacement sentence, for when this note is accepted. Do not edit the plan file in this commit:

"Exactly 17. 0414 cannot share a wave with any other cmd.rs page. It waits on cmd.rs. render.rs is free in waves 10 through 13, and that does not let 0414 start earlier."

## 17.4 Door 0400 and lab 0701: list 0413 through 0416

These pages are not yet on the door face or on the lab's serves list. face-write of 01 and 08 replaces the whole face. This note does not ship a replacement. When Prima next writes those faces, add these lines and keep every line already there.

Door 90.50.10.0400, face 01, one line each:

- 0413  work order view: 05.NN reads as one record. Lab 0701, tests/lab_0413.rs.
- 0414  the pack and the prompt print the builder name. Lab 0701, tests/lab_0414.rs.
- 0415  a new log folder syncs on Windows. Lab 0701, tests/lab_0415.rs.
- 0416  tests build and run on Windows. Lab 0701, tests/lab_0416.rs.
- 0417  the packs folder updates on every return. Lab 0701, tests/lab_0417.rs. Needs 0413.

Lab 90.50.10.0701, serves, the same four, with the trial file named on face 01 and the address named on face 08. Each of those pages already says lab: 90.50.10.0701 on its own face 08. 0415's draft faces are in docs/design/drafts/90.50.10.0415/. 0416 uses the 0405 draft, address read as 0416.

0701.05.01 is closed, so a later face-write does not reopen that pass (src/cmd.rs:848-849 refuses a close when face 01 moves after signoff; the pass is already closed).

## 17.5 Waves that do not move

| Wave | Runs | Why it stays |
|---|---|---|
| 6 | 0409, 0413 | 0409 is cmd.rs. 0413 is src/render.rs only |
| 14 | 0414 | cmd.rs and render.rs; needs 0404, which is closed. Also the temp-worker name |
| 15 | trial 0414 | |
| 16 | 0417 | cmd.rs and git.rs; needs 0413 closed. Packs 05.NN updates on return |
| 17 | trial 0417 | |
| 18 | 0498 | last, after 0417 |
| 19 | trial 0498 | |

0413 does not take src/cmd.rs. A pass field on face-write would. That would clash with 0409 in wave 6 and would push 0414 off wave 14. The view lists notes by entry number instead. See the 0413 pack.

## 17.6 Totals, from section 15.3

Section 15 does not count 0415 or 0416. Section 16 on cloud/design counted 0415 only. This note counts both, once.

Section 15: work 11/21/32, lab 12/13/25, stage 23/34/57, plus 0403.

Add 0415, 0416, and 0417, each 1/2/3 plus a trial 1/1/2:

- work: 11+3 / 21+6 / 32+9 = 14/27/41
- lab: 12+3 / 13+3 / 25+6 = 15/16/31
- stage: 14+15 / 27+16 / 41+31 = 29/43/72 passes, plus 0403.

0413 and 0414 stay the sizes already inside the 11/21/32. They are not added again. Waves were 17. 0416 fits inside wave 4. 0417 adds two waves, so the count is 19, and 0414 is still wave 14.

## 17.7 Release check of this note

checklist: docs/design/RELEASE-CHECK.md @ prima/build 78101fe6 (blob ef4c77486bcfddbdf8a013c6ff5651bb3df11aea)

| Item | Source | Seen | Result |
|---|---|---|---|
| A1-A9 for 0416 | t413u.md:7, :9; seqAddr.md:14, :242 | 90.50.10.0416, band 0400, not 00 or 99 | PASS |
| 0405 not reused | DIRECTOR-RULINGS.md:129-130; Prima 10:30 AM EST | 0405 stays parked; the job moves to 0416 | PASS |
| Title reuse | R34, DIRECTOR-RULINGS.md:173 | same title at a new address | PASS |
| H1 wave 4 | t422.md:8; section 13.5 | tests/wf.rs beside render.rs and cmd.rs | PASS |
| Wrong sentence | STAGE-PLAN 1226-1227 at 78101fe6; trial minor 1 | 17.3 names it and the replacement | PASS |
| 0414 stays wave 14 | Prima, this job; section 15.4 row 14 | 17.5 | PASS |
| Serves both ways | t422.md:8 | 17.4 lists both the door and the lab; the live faces are not overwritten here | TENSION until Prima writes them |
| Quotes | DIRECTOR-WORDS-t461u.md:5, :7, :11, :14 | 17.1 | PASS |
| Totals | section 15.3 | arithmetic in 17.6 | PASS |
| Axiom 6 | Axioms.md:23 | this file is a new step; the plan file is not edited | PASS |
| Axiom 9 | Axioms.md:29 | no hostile pass of this note | TENSION |

Verdict: no FAIL. Prima can add it to the plan when he accepts it.

Questions:

1. The 0405 draft folder still says 0405. Should those files be copied under docs/design/drafts/90.50.10.0416/ with the address changed, or will Prima change the address at pack time?

2. t492-t493u has no words file in the repo yet. The quotes above are Prima's statement. Please record the file so the lines can be checked.

3. The ruling says the folder updates on every return. 0417 also updates it after check, signoff, and close, so it does not freeze. If he meant the return only, say so.
