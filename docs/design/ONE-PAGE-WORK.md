# One page per piece of work: a proposal

For Matthew. By Designer. Started as a PROPOSAL (7). Parts are now answered by you (t245u, t246u). Answered, not ruled.
created: Tue 17 Nov 2026, 11:45 AM EST

## Change note (2026-11-17, 12:00 PM EST, Designer)

Folds your t245u and t246u answers (docs/review/DIRECTOR-WORDS-t245u.md, f2b2ede; DIRECTOR-WORDS-t246u.md, db1fbae).
- O1, O2 and O4 are marked answered. O3 and O9 are partly answered. O5 is "Prima proposal sent, awaiting his OK". O6, O7 and O8 are still open.
- New sections: elevation, the checker, and face 07 flex. New tail table. New questions E1-E5.
- Old text is kept and marked superseded (axiom 6).

## His words

- t240u: "Please review this again.  I think it's stronger then what is on page.  I want your critical opinion." (DIRECTOR-WORDS-t240u-t241u.md:7)
- t241u: "Sorry copy paste didn't work correctly.  I wanted you to look at 2. mostly." (:11)
- t243u: "So here is what i see using N4-N7 might not be needed.  Think about this.  We compress into a single page." (DIRECTOR-WORDS-t243u.md:18)
- t243u faces: "01 is the agents.md basically / 02 psedo code / 03 menu / 04 the dev space / 05 work / 06 prime notes / 07 labs / 08 connections" (:20-27)
- Context (Designer): his "2." reads as point 2 of t239u: "We would break it into pages, each on to achieve a different piece." Also: "So each 05 goes from prime > worker > prime > person > prime" (DIRECTOR-WORDS-t239u.md:10).

## Readings (Designer, 7). Not his words.

- (Superseded 2026-11-17: he said yes to O1 in t246u:6.) He asked for an opinion. He approved no layout. t243u says "might not be needed" and "Think about this".
- "a single page" reads as one page per piece, each page holding everything for that piece. This follows t239u:10 ("break it into pages"). It does not mean one page for the whole game. Raised in O1.
- "N4-N7" reads as the dev, jobs and colab bands (workflow-loop.003.md:45-48). It does not cover N3, the build band (:44).
- t243u adds faces 06, 07 and 08, which t239u did not name. It moves "decisions" to "the dev space" (04) and puts prime notes on 06.

## His t245u answers

**His words** (docs/review/DIRECTOR-WORDS-t245u.md):
- :5 "07 is a flex location, for dev work it's going to become labs."
- :8 "1. How we solve this is we need to improve the elevate design.  If the worker can't solve it comes to you, if prime can't solve by giving improved frame and authority.  It comes to the person.  I should only need to be involved when it comes to the big issues.  When a deliverable isn't possible under the current design.  A conflict is found.  That kind of thing.  If you are able to reach the goal you should give moving with me reviewing as the work is on going.   I am here the whole day.  As a good director should be."
- :10 "2. You have a checker using tools to confirm the work was done correctly, then you do occasional checks to make sure it's working."
- :11 "3. 07"
- :12 "4. We need to establish the MVP goals in the 04 face, with it being stripped down in the 01 for the agent."
- :13 "5. Yes it should link to the exact files and locations."
- :14 "6. How would you fix it?"

**Prima's mapping** (t245u:16, not a ruling):
- 1 = the review bottleneck. 2 = independence. 3 = trials on face 07.
- 4 = the completing page, and MVP goals on 04 stripped down on 01. 5 = face 08 links. 6 = face 03 and the 01 card.
- Prima's answer to 6: a compute-only 03 menu on any page, and the 01 card as the source of a version-stamped AGENTS.md per job. Sent as the first real pack, awaiting his OK.

**Designer reading (7).** Not his words.
- "you" in :8 and :10 is Prima. The ladder is worker, then Prima, then him.
- "give moving" reads as "keep moving".
- His two triggers are examples: "That kind of thing" (:8). The list is not closed (E1).
- He does not say "this replaces review on every pass". It is read from "I should only need to be involved when it comes to the big issues" (:8).
- "occasional checks to make sure it's working" (:10) may mean checking the work, or checking that the checker works (E4).
- Item 4 (:12) names MVP goals, not a completing page. O8 stays open.
- Item 3 is only "07". With :5, trials go on 07 for dev work. Who runs a trial is not said.

## His t246u answers (the top three)

**His words** (docs/review/DIRECTOR-WORDS-t246u.md):
- :5 "one page work"
- :6 "1. Yes I agree"
- :8 "2. See previous response."
- :10 "3. Yes I agree"

**Prima's mapping** (t246u:12, not a ruling): 1 = O1 yes; 2 = O2, answered by t245u item 1; 3 = O4 yes.

**Designer reading (7).**
- His "1., 2., 3." follow the order of Prima's top three (t246u:3), which was O1, O2, O4. His words do not name O-numbers.
- "See previous response" reads as t245u item 1 (Prima's reading; his words do not say which).
- His yes to O4 covers O4 as written: the face 03 menu per R35, with seqAddr.md:189 and validate.rs fixed. It does not clearly cover O5 (the 01 card as one source, a compute-printed AGENTS.md per job) or Prima's offer to make it the first real pack. Those stay "Prima proposal sent, awaiting his OK".
- O1's yes includes labs on face 07. That is not done. Follow-on work, each through its own path:
  - seqAddr.md 5.1 (:156), 5.2 (:163) and 5.7 (:200); decisions.md A4.3.
  - face.rs:72-85 (`is_active_face`, `is_content_face`, `always_counted`); validate.rs:229-234 then stops refusing 07.
  - The O4 fix: seqAddr.md:189 and validate.rs:352-354.
  - The SUPERSEDES list below: dated notes in each file.

## Elevation (proposal, Designer, 7)

Based on his two named triggers (t245u:8): "a deliverable isn't possible under the current design", and "A conflict is found". Signals the compute or the checker can raise:

| Signal | Trigger | Raised by | Goes to | Recorded |
|---|---|---|---|---|
| return ends `need` or `blocked` (workflow-loop.003.md:191) | not possible | worker | Prima; Prima to him if it needs a new grant or a design change | the card on the slot; outcome `needs-authority` or `blocked` (:166) |
| design change needed on 02 or 04 | not possible | Prima | him: a material design change needs a renewed grant (:249) | a 06 note naming the pass; his answer on 04 |
| pass 6 on one frame, or the same blocker again (:260, :267) | not possible | compute | him: "Halt before release" (:267) | the frame count and blocker history |
| failed check (tests, lint, hash, commit) | neither, at first | checker | worker reworks; second fail on the same check goes to Prima | the check result on the review step |
| lint or template refusal of a pack | neither | compute | Prima fixes the pack | the refusal with its why (PT row 25) |
| two live claims, or two records that disagree | conflict | compute or checker | halt, then raise to whoever holds more: "Do not choose." (Axioms.md:13) | both records, linked; no pick |
| spec, code or ruling disagree (like O4) | conflict | anyone | him | a question in DECISIONS-WAITING |
| governing change (:152) | conflict-class, always | Prima | him; a face 07 trial first | the change and its trial |

- Nothing below "him" stops the work. Above, only that pass halts. Other pages keep moving.

**How he reviews as it goes.**
- A read-only tail feed: each tail move, newest first, from the log. It is a view, never stored (W11).
- The board view per page (05.00 columns, :160).
- A comment from him goes on 04 as his response, linked to the pass. It does not halt work unless he marks it a conflict (E3).

**How a pass closes without his review.**
- The checker takes the review step and records its checks. It must not be the builder (crates/seqaddr-core/src/state.rs:579-581).
- Prima closes after a passing review, keeping his "prime" last step (t239u:10).
- Code change: today only the reviewer may close (crates/compute/src/store.rs:991-992). Allow the pack's lead to close too, but only after a passing review by a non-builder is recorded (E2).

## The checker (proposal, Designer, 7)

- "using tools to confirm the work was done correctly" (t245u:10) reads as: tests run, lint passes, the return hash matches, the commit exists and changed only the paths named, and the template shape holds.
- Each check result is recorded on the review step with the commit it ran against.
- The checker is not the builder (state.rs:579-581). A fresh session counts as another view (R20, DIRECTOR-RULINGS.md:79).
- Prima's occasional checks: picked by a rule written down before the passes run, not by feel (E4). Each check is a 06 note linking the pass it checked and what was found.

## Face 07: flex (his word, t245u:5)

- For dev work, 07 holds labs (t245u:5, :11).
- It still needs, from "Face 07 today" above: a spec step for seqAddr.md 5.1, 5.2 and 5.7 (and decisions.md A4.3), and code changes in face.rs (`is_active_face`, `is_content_face`, `always_counted`). validate.rs:229-234 then allows it.
- What "flex" means for pages that are not dev work is open (E5).

## What each face holds (proposal)

| Face | His word | Holds | Spec today |
|---|---|---|---|
| 01 | agents.md | the one agents.md card for the piece (O5) | law (seqAddr.md:150) |
| 02 | pseudo code | light pseudo code of the design; drift noted (O9) | schema (:151) |
| 03 | menu | a compute-written menu of the page (R35, DIRECTOR-RULINGS.md:179-180) | refused off 0001-0099 (O4) |
| 04 | dev space | concept, your responses, the decisions that follow you | user (:153) |
| 05 | work | passes, 05.01 up; each pack and its return on one slot (W9) | tasks (:154) |
| 06 | prime notes | Prima's notes, one counter per session (O7) | notes (:155) |
| 07 | labs | trials, each by a model other than the builder (O1, O3) | "reserved / not active" (:156) |
| 08 | connections | links to code files, the completing page, other pieces | map (:157) |

## Face 07 today (Prima's catch a, checked)

- seqAddr.md section 5.1: "| `07` | reserved | not active |" (seqAddr.md:156). Confirmed.
- seqAddr.md:163: "Face 07 does not count" toward a page's required faces.
- The kernel refuses it. The validator rejects any write to a face that is not active: "face {:02} is reserved and not active", rule A4.3 (crates/seqaddr-core/src/validate.rs:229-234).
- `is_active_face` allows only 00-06 and 08 (crates/seqaddr-core/src/face.rs:72-75). `is_content_face` leaves 07 out (:77-80).
- Only 05 and 06 are always counted (face.rs:82-85; seqAddr.md:200). Trials as counters on 07 also need 07 counted.
- So labs on 07 need: your yes, a new step for seqAddr.md 5.1, 5.2 and 5.7 (and decisions.md A4.3), and code changes in face.rs. Each goes through its own path.

## The tail and who acts (proposal; changes the WC:227-236 table)

Superseded 2026-11-17 by "The tail after t245u" below. Kept as history.

| Step | Who acts | Faces touched |
|---|---|---|
| draft | Prima writes the pack | 05 slot; 01 and 02 read |
| pack | Prima releases; compute checks the template | 05 |
| open | worker claims and works | 05 |
| return | worker hands back; Prima reads (a read, not the review) | 05 |
| review | a review bot, not Prima and not the builder (O3); you at seat, or when risky or new (O2) | 05; 07 if a trial runs |
| closed | Prima closes, then writes a note on 06 and any decision on 04 | 05, 06, 04 |

- Today only the reviewer may ask the compute to close (crates/compute/src/store.rs:991-992). "Prima closes" needs a code change, as WC F2 noted.
- Trials on 07 run before review where risk calls for one. The trial names the return version it tried.

## The tail after t245u (proposal, Designer, 7)

| Step | Who acts | Faces touched | Goes up if |
|---|---|---|---|
| draft | Prima writes the pack from 04 (MVP goals) and 01 (stripped down, t245u:12) | 05 slot | lint or template refusal: Prima fixes |
| pack | Prima releases; compute checks the template | 05 | refusal: Prima fixes |
| open | worker claims and works | 05 | worker can't solve: `need` or `blocked`, to Prima (t245u:8) |
| return | worker hands back; Prima reads (a read, not the review) | 05 | Prima can't solve with a better frame or authority: to you (t245u:8) |
| review | the checker, not the builder, runs its tool checks; a face 07 trial for dev work when risk calls for one | 05; 07 | failed check: worker reworks; a second fail goes to Prima |
| closed | Prima closes after a passing review (E2); a note on 06; any decision on 04 | 05, 06, 04 | a conflict at any step: halt that pass and raise it |

- You review as it goes, from the feed and the board (E3). You are not a step.

## Where your review sits (proposal, O2)

Superseded 2026-11-17 by your t245u:8 answer (see "Elevation"). Kept as history.

- Your words put you on every pass ("prime > worker > prime > person > prime", t239u:10).
- Prima proposes that you review when the page's best pass is seated, or when the work is risky or new. Routine passes go to a review bot. You read those returns later.
- This changes your stated hand-off. Only you can say yes.

## Worked example (example only, not a design)

Driving game. Fifty pieces, so fifty pages in one work band, plus a completing page. Band number open (7); 12NN is used here only as an example.
- 1201.steering. 01: "Steer with arrow keys; max turn 30 degrees." 02: "on key: angle += rate; clamp to 30". 03: menu, by the compute. 04: concept, your note "feels too stiff", Prima's decision "rate 2 to 3".
- 05.01: pack "add steering"; return; review bot passes it; closed.
- 05.02: pack "rate 3"; trial on 07.01 by another model tries a 31-degree turn; reviewed; you review at seat.
- 06: Prima's note "rate 3 felt right; see 05.02". 08: links to src/steer.rs and to the completing page.
- 1200 (band head) as the completing page, if O8 is yes: its 03 menu lists the 50 pages and their states; its passes do the final assembly with Cursor.

## SUPERSEDES if you say yes

You said yes to O1 (t246u:6). Each item below now needs its dated note, as follow-on work. Not done yet.

Nothing here is deleted. Each item gets a dated "superseded" note through its own path (axiom 6).
- workflow-loop.003.md: band map rows N4, N5, N7 (:45-48); section 4, the N4 page and its approval (:83-93), including S12's dev face 05 (:92) and N4 face 06 notes (:93); the pack "on the N5 page" (:99); the lead's read and note on N4 (:216-217); "mandatory N7" (:247, :284, :314) becomes a face 07 trial.
- DEV-WORK-LAB-PAGES.md: the whole three-page split; the dev face 05 line (D:63; Prima cited D:58); D6's B+I lab parts ("Trials become passes on the lab page", D:182; "If D6 goes Tester's way", D:188).
- PACK-TEMPLATE.md: row 10 "linked pages: dev 04NN, lab 07NN" (PT:95); "Lab page ... not yet made" (PT:15); the sheet lines (PT:127, :146, :219).
- WORK-BOOK-CONCEPT.md: F1's "Lab pages stay only for risky trials" (WC:268); F7's "dev band (04NN)" candidate (WC:304); the tail table's "linked pages" (WC:231).
- Also found: DESIGN.md:265 ("one identified N4 revision"); WORK-BOOK-SPEC.md:94 (N4 shape); seqAddr.md:243 (a set by number across bands). Your R18 (DIRECTOR-RULINGS.md:71-72) matches pages across bands; it would have less use, but only you change a ruling.
- Spec and code to change, not superseded: seqAddr.md:156, :163, :200; face.rs:72-85; validate.rs:229-234.

## Questions (one list; F1-F7 and Prima's six merged)

Full four-part forms. "Moot if yes" means moot if you say yes to O1.

Top three, picked by what blocks most (superseded 2026-11-17: you answered these in t246u; the new top three are in DECISIONS-WAITING.md):
- O1 blocks every page's shape.
- O2 blocks every pass's review step.
- O4: the code refuses the 03 menu, so no page can be written whole. Independence (O3) can wait, because you review meanwhile.

### O1 (TOP). One page per piece, faces 01-08, labs on face 07? (merges F1, critique 3)
- **Status: answered** (t246u:6, "1. Yes I agree"; with t245u:5, :11 for 07). Face 07 spec and code steps are follow-on work, not done.
1. **Question.** t243u says N4-N7 "might not be needed" and "compress into a single page" (DIRECTOR-WORDS-t243u.md:18). Does each piece live on one page with faces 01-08 as you listed, with trials on face 07, and no dev, work or lab pages?
2. **Proposed (Prima).** Yes. One page per piece, faces 01-08 as you listed. Trials go on face 07. That needs your yes to make 07 active, a spec step, and a code change (see "Face 07 today").
3. **Why.** One place per piece, so the concept, design and passes cannot drift. Fifty pieces make 50 pages, not 150. Who gets hurt otherwise: every builder, reading one piece across three pages.
4. **Axioms checked.** 2 [Axioms.md:15] pass: one page, nothing copied. 8 [Axioms.md:27] pass: 08 still connects. 6 [Axioms.md:23] pass: old text kept and marked. 1 [Axioms.md:13] tension: 07 is "not active" by the spec you hold; only you can open it. 7 [Axioms.md:25] tension: which band holds the pages is open.

### O2 (TOP). Do you review every pass? (merges F2, critique 1)
- **Status: answered** by t245u:8, via t246u:8 ("2. See previous response."). That it refers to t245u item 1 is Prima's reading. His answer is the elevation ladder, not Prima's proposal below. Open details: E1, E2, E3.
1. **Question.** You wrote "So each 05 goes from prime > worker > prime > person > prime" (DIRECTOR-WORDS-t239u.md:10). Should you review only when a page's best pass is seated, or when the work is risky or new?
2. **Proposed (Prima).** Yes. You review at seat, or when the work is risky or new. Routine passes are reviewed by a review bot (O3) and closed by Prima. You read the return later.
3. **Why.** A person review on every pass makes you the bottleneck. You allowed "you check the work, or assign a review bot" (t223u:12). Review can be delegated "only to the extent delegated" (workflow-loop.003.md:89, S04). Who gets hurt otherwise: you, with every small pass waiting on you.
4. **Axioms checked.** 1 [Axioms.md:13] tension: this changes your own stated hand-off, and only you grant it. 9 [Axioms.md:29] pass only with O3: another view still reviews. 3 [Axioms.md:17] pass: each step names its lead. 6 [Axioms.md:23] pass: the return stays on record for you.

### O4 (TOP). Face 03 follows R35 (merges F3, critique 6a)
- **Status: answered** (t246u:10, "3. Yes I agree"). Covers O4 as written here. Spec and code steps are follow-on work, not done.
1. **Question.** R35 approved a compute-written 03 menu on any page (DIRECTOR-RULINGS.md:179-180). seqAddr.md:189 still limits 03 to 0001-0099 in a normal book, and the code refuses it (validate.rs:352-354). Should both follow R35?
2. **Proposed (Prima).** Yes. Each gets a new step through its own path, citing R35.
3. **Why.** Your ruling is newer. Who gets hurt otherwise: the first piece page, refused for a face you approved.
4. **Axioms checked.** 1 [Axioms.md:13] pass: R35 governs. 6 [Axioms.md:23] pass: a new step, not a rewrite. 2 [Axioms.md:15] tension: spec and code contradict R35 until fixed.

### O3. Who reviews: a review bot, and a different model for trials? (critique 2, catch b)
- **Status: partly answered** (t245u:10): a checker with tools, then Prima's occasional checks. Who runs a face 07 trial is not said. Open: E4, and the trial runner.
1. **Question.** Should a review bot, not Prima, take the review step? Should every face 07 trial be run by a model other than the builder?
2. **Proposed (Prima).** Yes to both.
3. **Why.** "its maker is the easiest one to convince" (Axioms.md:29). The reviewer is "a view other than the builder" (workflow-loop.003.md:29, S10). A fresh session counts as a different view (R20, DIRECTOR-RULINGS.md:79). Who gets hurt otherwise: you, trusting a pass its own author approved.
4. **Axioms checked.** 9 [Axioms.md:29] pass. 1 [Axioms.md:13] pass: you allowed a review bot (t223u:12). 7 [Axioms.md:25] tension: the code checks only reviewer is not builder (crates/seqaddr-core/src/state.rs:579-581); not "not Prima", and nothing for 07 yet.

### O5. The 01 card is the one AGENTS.md source (F4, critique 6b)
- **Status: Prima proposal sent, awaiting his OK** (t245u:14, "6. How would you fix it?"; Prima's answer t245u:16). His t246u yes to O4 does not clearly cover this or the "first real pack" offer. t245u:12 says 01 is "stripped down" for the agent.
1. **Question.** Is the 01 card the one stored AGENTS.md, with the per-job file only a compute copy (PACK-TEMPLATE part 4)?
2. **Proposed (Prima).** Yes. The compute prints the file from the card, with version and hash.
3. **Why.** The builder reads files on your machine (t223u:6). One source stops drift. Who gets hurt otherwise: a builder reading a stale file.
4. **Axioms checked.** 2 [Axioms.md:15] pass. 6 [Axioms.md:23] pass: the copy names its version. 8 [Axioms.md:27] pass. 9 [Axioms.md:29] tension: untried.

### O6. Is the best pass seated on plain 05? (F5)
- **Status: still open.** Not in t245u or t246u.
1. **Question.** Your R23-R24 seat the best pass on plain 05 (DIRECTOR-RULINGS.md:90-97). t239u and t243u do not mention it. Does it stand?
2. **Proposed (Designer, 7).** Yes, after seqAddr.md:199 and state.rs:459-460 change.
3. **Why.** The next model starts from the best pass. O2's "review at seat" needs a seat. Who gets hurt otherwise: the next model, starting from a weak pass.
4. **Axioms checked.** 1 [Axioms.md:13] pass. 6 [Axioms.md:23] pass. 7 [Axioms.md:25] tension: spec and code first.

### O7. Decisions on 04, notes on 06? (F6; partly met by t243u)
- **Status: still open.** t245u:12 puts MVP goals on 04; decisions and notes are not named.
1. **Question.** t239u put the prime's decisions on 04 (t239u:10). t243u says "04 the dev space" and "06 prime notes" (DIRECTOR-WORDS-t243u.md:23, :25). Do decisions go on 04, and Prima's session notes on 06?
2. **Proposed (Designer, 7).** Yes. Each decision on 04 links to the pass it came from.
3. **Why.** You read 04 (seqAddr.md:153). Who gets hurt otherwise: you, looking in two places.
4. **Axioms checked.** 4 [Axioms.md:19] pass. 6 [Axioms.md:23] pass. 2 [Axioms.md:15] tension: two faces for what was learned.

### O8. The completing page (F7, critique 4)
- **Status: still open.** Prima's mapping links his item 4 to the completing page (t245u:16), but his words name only MVP goals (t245u:12).
1. **Question.** "With a page for completing the work" (t239u:10). What is it?
2. **Proposed (Prima).** The band head. Its 03 menu lists every page and its state. Its passes do the final assembly with Cursor (t223u:10; t212u:6).
3. **Why.** A band head holds "the band's definition and contents" (seqAddr.md:241). Who gets hurt otherwise: you, if 50 pages pass and nothing says the game works.
4. **Axioms checked.** 8 [Axioms.md:27] pass. 5 [Axioms.md:21] pass: it says what done means. 2 [Axioms.md:15] tension: states must be a view (W11), not stored copies.

### O9. The 02 pseudo code drifts from the code (critique 5)
- **Status: partly answered** (t245u:13, "Yes it should link to the exact files and locations."). Each return noting mismatches is not addressed.
1. **Question.** How do we notice when 02 and the real code part ways?
2. **Proposed (Prima).** Face 08 links to the code files. Each return notes where they no longer match.
3. **Why.** "code lives in the repo, not in the book" (workflow-loop.003.md:70); links record the commit checked (:74). Who gets hurt otherwise: a builder trusting a stale 02.
4. **Axioms checked.** 8 [Axioms.md:27] pass. 6 [Axioms.md:23] pass. 9 [Axioms.md:29] tension: the builder's note is self-report; the review checks it.
- Designer note: N3's face 02 means "the module's files described" (workflow-loop.003.md:44, :72). That differs from 02 as pseudo code here (7).

### New questions from t245u (Designer, 7)

### E1 (TOP). Are these the signals that send work up?
1. **Question.** You named two triggers: "When a deliverable isn't possible under the current design.  A conflict is found.  That kind of thing." (DIRECTOR-WORDS-t245u.md:8). Are the signals in the elevation table the right ones, and does each go to the right place?
2. **Proposed (Designer, 7).** Yes, as in the table. Worker to Prima for `need`, `blocked` and a second failed check. Prima to you for a design change on 02 or 04, pass 6, a conflict between records or rulings, and any governing change. Two live claims halt and go up, never picked.
3. **Why.** You asked to be involved only for big issues (t245u:8). Each signal is something the compute or checker can see, so nothing depends on a model's mood. Who gets hurt otherwise: you, pulled in for small things, or not told about a big one.
4. **Axioms checked.** 1 [Axioms.md:13] pass: "raise it to whoever holds more. Do not choose." 5 [Axioms.md:21] pass: each signal frames when to stop. 3 [Axioms.md:17] pass: each signal names who raises it. 7 [Axioms.md:25] tension: "That kind of thing" leaves the list open, and the risk levels are still `7` (workflow-loop.003.md:154).

### E2 (TOP). Who closes a pass you did not review?
1. **Question.** You said work should keep moving "with me reviewing as the work is on going" (t245u:8). Today only the reviewer may ask the compute to close (crates/compute/src/store.rs:991-992). Who closes a routine pass?
2. **Proposed (Designer, 7).** The checker takes the review step. Prima closes after a passing review, as the last "prime" in your hand-off (t239u:10). Code change: allow the pack's lead to close too, only once a passing review by a non-builder is recorded.
3. **Why.** Work keeps moving without you on every pass. The close still rests on a recorded review. Who gets hurt otherwise: you, if every pass waits; or the book, if a pass closes with no check.
4. **Axioms checked.** 1 [Axioms.md:13] pass: the compute enforces the rule. 9 [Axioms.md:29] pass: another view checks first. 3 [Axioms.md:17] pass. 6 [Axioms.md:23] pass: the review and close are both logged. 7 [Axioms.md:25] tension: the code change is not made.
- Designer note: the simpler choice is that the checker closes, with no code change. That drops Prima's last step.

### E3. How do you review as it goes, and does your comment stop work?
1. **Question.** "I am here the whole day." (t245u:8). What do you watch, and what happens when you comment?
2. **Proposed (Designer, 7).** You watch a read-only tail feed and each page's board, built from the log (W11). Your comment goes on 04 as your response, linked to the pass. It does not halt work unless you mark it a conflict; then the elevation rule applies.
3. **Why.** You keep sight of everything without being a gate. Who gets hurt otherwise: you, chasing what changed; or a builder, stopped by a passing remark.
4. **Axioms checked.** 2 [Axioms.md:15] pass: a view, not a copy. 4 [Axioms.md:19] pass: your why lands on 04. 8 [Axioms.md:27] pass: linked to the pass. 7 [Axioms.md:25] tension: the feed is not built.

### E4. What are Prima's "occasional checks"?
1. **Question.** "then you do occasional checks to make sure it's working" (t245u:10). Does Prima check the work, or check that the checker works? How are they picked?
2. **Proposed (Designer, 7).** Both. Prima re-checks the first pass on each new page, and one closed pass in every five, picked by a rule written down first. Each check is a 06 note linking the pass and what was found. A check that finds a miss counts as a failed check and goes up.
3. **Why.** A checker can drift too (axiom 9). A rule stops picking only easy passes. Who gets hurt otherwise: you, trusting a checker nobody checked.
4. **Axioms checked.** 9 [Axioms.md:29] pass: the checker faces a trial too. 6 [Axioms.md:23] pass: each check is noted. 7 [Axioms.md:25] tension: "one in five" is my number, not yours.

### E5. What does "flex" mean for face 07 outside dev work?
1. **Question.** "07 is a flex location, for dev work it's going to become labs." (t245u:5). What does 07 hold on other pages?
2. **Proposed (Designer, 7).** Set by page type. On pages of the work it is labs. On every other type it stays reserved until you name a use.
3. **Why.** One face, one meaning per page type, so no builder reads it two ways. Who gets hurt otherwise: a builder guessing what a flex face holds.
4. **Axioms checked.** 2 [Axioms.md:15] pass: a type carries its rule. 1 [Axioms.md:13] pass: you name each use. 7 [Axioms.md:25] tension: page types for the work are not settled (W8 type part, O4).

### Moot if yes (kept, not deleted)

O1 is now answered yes (t246u:6), so these are moot, kept as history.
- D1 (lab page): moot; replaced by face 07 (O1).
- D3 (who makes the set of pages): moot; one page, links on 08.
- D4 (05NN jobs or build): moot as asked; the open part is O1's band.
- D5 (dev note before the next pack): replaced by O7.
- D6's B+I lab parts: moot. D6 itself stays answered.
- F1-F7: merged into O1-O8 above. Their full forms stay in WORK-BOOK-CONCEPT.md as history.
- Not moot: D2 / P7 (linking, used by 08), W9, W11, W13, P1-P5, P8.
