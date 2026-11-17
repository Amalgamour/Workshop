# One page per piece of work: a proposal

For Matthew. By Designer. A PROPOSAL (7). It waits on your yes. Not a ruling.
created: Tue 17 Nov 2026, 11:45 AM EST

## His words

- t240u: "Please review this again.  I think it's stronger then what is on page.  I want your critical opinion." (DIRECTOR-WORDS-t240u-t241u.md:7)
- t241u: "Sorry copy paste didn't work correctly.  I wanted you to look at 2. mostly." (:11)
- t243u: "So here is what i see using N4-N7 might not be needed.  Think about this.  We compress into a single page." (DIRECTOR-WORDS-t243u.md:18)
- t243u faces: "01 is the agents.md basically / 02 psedo code / 03 menu / 04 the dev space / 05 work / 06 prime notes / 07 labs / 08 connections" (:20-27)
- Context (Designer): his "2." reads as point 2 of t239u: "We would break it into pages, each on to achieve a different piece." Also: "So each 05 goes from prime > worker > prime > person > prime" (DIRECTOR-WORDS-t239u.md:10).

## Readings (Designer, 7). Not his words.

- He asked for an opinion. He approved no layout. t243u says "might not be needed" and "Think about this".
- "a single page" reads as one page per piece, each page holding everything for that piece. This follows t239u:10 ("break it into pages"). It does not mean one page for the whole game. Raised in O1.
- "N4-N7" reads as the dev, jobs and colab bands (workflow-loop.003.md:45-48). It does not cover N3, the build band (:44).
- t243u adds faces 06, 07 and 08, which t239u did not name. It moves "decisions" to "the dev space" (04) and puts prime notes on 06.

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

## Where your review sits (proposal, O2)

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

Nothing here is deleted. Each item gets a dated "superseded" note through its own path (axiom 6).
- workflow-loop.003.md: band map rows N4, N5, N7 (:45-48); section 4, the N4 page and its approval (:83-93), including S12's dev face 05 (:92) and N4 face 06 notes (:93); the pack "on the N5 page" (:99); the lead's read and note on N4 (:216-217); "mandatory N7" (:247, :284, :314) becomes a face 07 trial.
- DEV-WORK-LAB-PAGES.md: the whole three-page split; the dev face 05 line (D:63; Prima cited D:58); D6's B+I lab parts ("Trials become passes on the lab page", D:182; "If D6 goes Tester's way", D:188).
- PACK-TEMPLATE.md: row 10 "linked pages: dev 04NN, lab 07NN" (PT:95); "Lab page ... not yet made" (PT:15); the sheet lines (PT:127, :146, :219).
- WORK-BOOK-CONCEPT.md: F1's "Lab pages stay only for risky trials" (WC:268); F7's "dev band (04NN)" candidate (WC:304); the tail table's "linked pages" (WC:231).
- Also found: DESIGN.md:265 ("one identified N4 revision"); WORK-BOOK-SPEC.md:94 (N4 shape); seqAddr.md:243 (a set by number across bands). Your R18 (DIRECTOR-RULINGS.md:71-72) matches pages across bands; it would have less use, but only you change a ruling.
- Spec and code to change, not superseded: seqAddr.md:156, :163, :200; face.rs:72-85; validate.rs:229-234.

## Questions (one list; F1-F7 and Prima's six merged)

Full four-part forms. "Moot if yes" means moot if you say yes to O1.

Top three, picked by what blocks most:
- O1 blocks every page's shape.
- O2 blocks every pass's review step.
- O4: the code refuses the 03 menu, so no page can be written whole. Independence (O3) can wait, because you review meanwhile.

### O1 (TOP). One page per piece, faces 01-08, labs on face 07? (merges F1, critique 3)
1. **Question.** t243u says N4-N7 "might not be needed" and "compress into a single page" (DIRECTOR-WORDS-t243u.md:18). Does each piece live on one page with faces 01-08 as you listed, with trials on face 07, and no dev, work or lab pages?
2. **Proposed (Prima).** Yes. One page per piece, faces 01-08 as you listed. Trials go on face 07. That needs your yes to make 07 active, a spec step, and a code change (see "Face 07 today").
3. **Why.** One place per piece, so the concept, design and passes cannot drift. Fifty pieces make 50 pages, not 150. Who gets hurt otherwise: every builder, reading one piece across three pages.
4. **Axioms checked.** 2 [Axioms.md:15] pass: one page, nothing copied. 8 [Axioms.md:27] pass: 08 still connects. 6 [Axioms.md:23] pass: old text kept and marked. 1 [Axioms.md:13] tension: 07 is "not active" by the spec you hold; only you can open it. 7 [Axioms.md:25] tension: which band holds the pages is open.

### O2 (TOP). Do you review every pass? (merges F2, critique 1)
1. **Question.** You wrote "So each 05 goes from prime > worker > prime > person > prime" (DIRECTOR-WORDS-t239u.md:10). Should you review only when a page's best pass is seated, or when the work is risky or new?
2. **Proposed (Prima).** Yes. You review at seat, or when the work is risky or new. Routine passes are reviewed by a review bot (O3) and closed by Prima. You read the return later.
3. **Why.** A person review on every pass makes you the bottleneck. You allowed "you check the work, or assign a review bot" (t223u:12). Review can be delegated "only to the extent delegated" (workflow-loop.003.md:89, S04). Who gets hurt otherwise: you, with every small pass waiting on you.
4. **Axioms checked.** 1 [Axioms.md:13] tension: this changes your own stated hand-off, and only you grant it. 9 [Axioms.md:29] pass only with O3: another view still reviews. 3 [Axioms.md:17] pass: each step names its lead. 6 [Axioms.md:23] pass: the return stays on record for you.

### O4 (TOP). Face 03 follows R35 (merges F3, critique 6a)
1. **Question.** R35 approved a compute-written 03 menu on any page (DIRECTOR-RULINGS.md:179-180). seqAddr.md:189 still limits 03 to 0001-0099 in a normal book, and the code refuses it (validate.rs:352-354). Should both follow R35?
2. **Proposed (Prima).** Yes. Each gets a new step through its own path, citing R35.
3. **Why.** Your ruling is newer. Who gets hurt otherwise: the first piece page, refused for a face you approved.
4. **Axioms checked.** 1 [Axioms.md:13] pass: R35 governs. 6 [Axioms.md:23] pass: a new step, not a rewrite. 2 [Axioms.md:15] tension: spec and code contradict R35 until fixed.

### O3. Who reviews: a review bot, and a different model for trials? (critique 2, catch b)
1. **Question.** Should a review bot, not Prima, take the review step? Should every face 07 trial be run by a model other than the builder?
2. **Proposed (Prima).** Yes to both.
3. **Why.** "its maker is the easiest one to convince" (Axioms.md:29). The reviewer is "a view other than the builder" (workflow-loop.003.md:29, S10). A fresh session counts as a different view (R20, DIRECTOR-RULINGS.md:79). Who gets hurt otherwise: you, trusting a pass its own author approved.
4. **Axioms checked.** 9 [Axioms.md:29] pass. 1 [Axioms.md:13] pass: you allowed a review bot (t223u:12). 7 [Axioms.md:25] tension: the code checks only reviewer is not builder (crates/seqaddr-core/src/state.rs:579-581); not "not Prima", and nothing for 07 yet.

### O5. The 01 card is the one AGENTS.md source (F4, critique 6b)
1. **Question.** Is the 01 card the one stored AGENTS.md, with the per-job file only a compute copy (PACK-TEMPLATE part 4)?
2. **Proposed (Prima).** Yes. The compute prints the file from the card, with version and hash.
3. **Why.** The builder reads files on your machine (t223u:6). One source stops drift. Who gets hurt otherwise: a builder reading a stale file.
4. **Axioms checked.** 2 [Axioms.md:15] pass. 6 [Axioms.md:23] pass: the copy names its version. 8 [Axioms.md:27] pass. 9 [Axioms.md:29] tension: untried.

### O6. Is the best pass seated on plain 05? (F5)
1. **Question.** Your R23-R24 seat the best pass on plain 05 (DIRECTOR-RULINGS.md:90-97). t239u and t243u do not mention it. Does it stand?
2. **Proposed (Designer, 7).** Yes, after seqAddr.md:199 and state.rs:459-460 change.
3. **Why.** The next model starts from the best pass. O2's "review at seat" needs a seat. Who gets hurt otherwise: the next model, starting from a weak pass.
4. **Axioms checked.** 1 [Axioms.md:13] pass. 6 [Axioms.md:23] pass. 7 [Axioms.md:25] tension: spec and code first.

### O7. Decisions on 04, notes on 06? (F6; partly met by t243u)
1. **Question.** t239u put the prime's decisions on 04 (t239u:10). t243u says "04 the dev space" and "06 prime notes" (DIRECTOR-WORDS-t243u.md:23, :25). Do decisions go on 04, and Prima's session notes on 06?
2. **Proposed (Designer, 7).** Yes. Each decision on 04 links to the pass it came from.
3. **Why.** You read 04 (seqAddr.md:153). Who gets hurt otherwise: you, looking in two places.
4. **Axioms checked.** 4 [Axioms.md:19] pass. 6 [Axioms.md:23] pass. 2 [Axioms.md:15] tension: two faces for what was learned.

### O8. The completing page (F7, critique 4)
1. **Question.** "With a page for completing the work" (t239u:10). What is it?
2. **Proposed (Prima).** The band head. Its 03 menu lists every page and its state. Its passes do the final assembly with Cursor (t223u:10; t212u:6).
3. **Why.** A band head holds "the band's definition and contents" (seqAddr.md:241). Who gets hurt otherwise: you, if 50 pages pass and nothing says the game works.
4. **Axioms checked.** 8 [Axioms.md:27] pass. 5 [Axioms.md:21] pass: it says what done means. 2 [Axioms.md:15] tension: states must be a view (W11), not stored copies.

### O9. The 02 pseudo code drifts from the code (critique 5)
1. **Question.** How do we notice when 02 and the real code part ways?
2. **Proposed (Prima).** Face 08 links to the code files. Each return notes where they no longer match.
3. **Why.** "code lives in the repo, not in the book" (workflow-loop.003.md:70); links record the commit checked (:74). Who gets hurt otherwise: a builder trusting a stale 02.
4. **Axioms checked.** 8 [Axioms.md:27] pass. 6 [Axioms.md:23] pass. 9 [Axioms.md:29] tension: the builder's note is self-report; the review checks it.
- Designer note: N3's face 02 means "the module's files described" (workflow-loop.003.md:44, :72). That differs from 02 as pseudo code here (7).

### Moot if yes (kept, not deleted)
- D1 (lab page): moot; replaced by face 07 (O1).
- D3 (who makes the set of pages): moot; one page, links on 08.
- D4 (05NN jobs or build): moot as asked; the open part is O1's band.
- D5 (dev note before the next pack): replaced by O7.
- D6's B+I lab parts: moot. D6 itself stays answered.
- F1-F7: merged into O1-O8 above. Their full forms stay in WORK-BOOK-CONCEPT.md as history.
- Not moot: D2 / P7 (linking, used by 08), W9, W11, W13, P1-P5, P8.
