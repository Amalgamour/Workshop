# Decisions waiting for you

For Matthew. By Designer. An index, not a ruling. Only you approve.
made: Mon 16 Nov 2026, 9:00 PM EST. Updated: Tue 17 Nov 2026, 11:30 AM EST (your t239u answers).

How to read this:
- One line for the question. One line for the answer we propose.
- "Unblocks": what can go ahead once you answer.
- "Waits on": answer that one first. "none marked" means the file marks nothing.
- "Full form": where the question, the answer, the why and the axiom marks are written.

Files: WC = docs/design/WORK-BOOK-CONCEPT.md. PT = docs/design/PACK-TEMPLATE.md.
D = docs/design/DEV-WORK-LAB-PAGES.md. SPEC = docs/design/WORK-BOOK-SPEC.md.

## Top three

New from your t239u page layout. Each one blocks the first work page.

1. **F1. One page per piece, or three pages per piece?**
   - Answer: one page per piece, with faces 01-05, as you described.
   - Unblocks: D1; D3; the first work page.
   - Waits on: none marked. Full form: WC:265.
2. **F2. Who acts at each step, and do you review every pass?**
   - Answer: prime, worker, prime, you, prime, as in the table. You may hand a review to a review bot.
   - Unblocks: the tail steps; who closes a pass.
   - Waits on: none marked (W6 is near it). Full form: WC:271. Table: WC:226.
3. **F3. Face 03 menus on work pages, and the workflow page type**
   - Answer: yes; fix seqAddr.md and the code to follow your R35.
   - Unblocks: a work page the code will accept.
   - Waits on: none marked. Full form: WC:277.

## Your page layout (F, in WC)

- **F4. Is the face 01 card the only stored AGENTS.md?**
  - Answer: yes; the per-job file is a copy printed from it.
  - Unblocks: W2; PT part 4. Waits on: none marked. Full form: WC:283.
- **F5. Is the best pass seated on plain 05?**
  - Answer: yes, as in your R23-R24, after a spec and code change.
  - Unblocks: seating 05. Waits on: none marked. Full form: WC:289.
- **F6. Decisions on 04, or notes on 06?**
  - Answer: decisions on 04, as you said; session notes on 06.
  - Unblocks: D5. Waits on: none marked. Full form: WC:295.
- **F7. What is "a page for completing the work"?**
  - Answer: one page per project that knows when every piece has passed.
  - Unblocks: the closing step of a project. Waits on: none marked (F1 is near it). Full form: WC:301.

## The work book (WC)

- **W9. Does the return sit on the same slot as its pack?**
  - Answer: yes, the same slot.
  - Unblocks: D1; D5; the return template. Waits on: none marked. Full form: WC:320.
- **W11. Is the board only a view, never stored?**
  - Answer: yes, built from the log each time.
  - Unblocks: the board columns in pack 1. Waits on: none marked. Full form: WC:340.
- **W12. Does the read-only sheet and board go first?**
  - Answer: yes, ahead of the template check and K8 step 1.
  - Unblocks: pack 1. Waits on: none marked. Full form: WC:349.
- **W13. Seat the templates before the check step?**
  - Answer: yes.
  - Unblocks: the check step; D5; P5. Waits on: none marked. Full form: WC:355.

## The pack template (PT)

- **P1. In what order does a return go?**
  - Answer: job items first, with a short summary on top. You pick.
  - Unblocks: the return template. Waits on: none (PT:247). Full form: PT:258.
- **P8. How is pack 1 made, if not by the tool?**
  - Answer: a script fills it, an outside view checks it, and your one-time yes is recorded.
  - Unblocks: pack 1 can go in. Waits on: W8 (PT:247), now answered. Full form: PT:264.
- **P7. Are pages linked by number, or by a written link?**
  - Answer: the number finds the page. Only a link both ways connects it.
  - Unblocks: the linked-pages row. Waits on: none (PT:247). Full form: PT:270.
- **P2. Who fills "authorized"?**
  - Answer: Prima names it, the compute checks it.
  - Unblocks: the authorized field. Waits on: none (PT:247). Full form: PT:276.
- **P3. Where does the start commit come from?**
  - Answer: from Prima's push, checked, and fixed at claim time.
  - Unblocks: the start-commit field. Waits on: none (PT:247). Full form: PT:282.
- **P4. What is hashed, and when?**
  - Answer: five things, listed in the file. The method is still open.
  - Unblocks: the hash design. Waits on: none (PT:247). Full form: PT:288.
- **P5. When does the code copy of the sheet end?**
  - Answer: when pack 2 closes passed.
  - Unblocks: the sheet shape. Waits on: none (PT:247). Full form: PT:294.

## Dev, work and lab pages (D)

- **D1. What is the lab page for?**
  - Answer: trying to break risky work only. Made only when needed.
  - Unblocks: the lab page. Waits on: W9, F1 (D:174). Full form: D:185.
- **D3. Who makes the pages and links, and when?**
  - Answer: the compute, before you approve the dev page.
  - Unblocks: making a set of pages. Waits on: F1 (D:174). Full form: D:191.
- **D2. When is a page linked?**
  - Same question as P7. Full form: PT:270 (pointer at D:197).
- **D4. Is 05NN "jobs" or "build"?**
  - Answer: jobs. 03NN is build. seqAddr.md is fixed later.
  - Unblocks: the seqAddr.md:243 fix. Waits on: none (D:173). Full form: D:200.
- **D5. Must Prima's note come before the next pack?**
  - Answer: yes, but only after an earlier pack has closed.
  - Unblocks: the check before each new pack. Waits on: W13, W9, F6 (D:173-174). Full form: D:206.

## Answered by you, t239u (docs/review/DIRECTOR-WORDS-t239u.md)

Answered, not ruled. The full forms stay, marked answered.
- **W8.** "1. I agree" (:9). Not a system page. The `workflow` type is not in your words (F3). Full form: WC:311.
- **D6.** "2.  Yes that is the purpose of 05.counter ..." (:10). Face 05 is the page's own passes. Full form: D:176.
- **W10 and P6.** "3. Yes, see 2." (:11). The pushed file only carries the return; the compute records it once. Full forms: WC:326, PT:249.
- Your line 5 asks Prima whether the workflow document is pushed. That is for Prima to answer.

## Also open (found in these files, not in the list above)

- **W1-W7.** Full forms in SPEC: W1 :382, W2 :390, W3 :409, W4 :417, W5 :425, W6 :433, W7 :441.
  - WC lists W1, W2, W3, W6, W7 as "still open for you to confirm" (WC:370-374).
  - WC has its own full forms for W4 (WC:379) and W5 (WC:386). W4 says the same rule as SPEC W4, in other words.
- **"6" and "8".** WC asks what you meant by "6 framing the work, with 8 returning" (WC:375).
  - It has no proposed answer and no axiom marks.
- **K8.** "In what order should we build?" Full form: docs/design/CORE-AND-TOOLS-SPEC.md:870.
  - W12 and PT both wait on its step 1 for the door label.
- **R37 item 5.** Where "selected, pending, accepted" show is marked open (7) at PT:114.
  - It has no full form yet.

## Disagreements settled (2026-11-16)

The newer, checked file won. Old text is kept, marked superseded.
- **Pack 1.** WC:160 now follows PT P8 (PT:264).
- **The return in git.** W10 (WC:326) now fits P6 (PT:249). Answered in t239u.
- **Return order.** WC:182 now marks the order open, per PT P1 (PT:258).
- **Dev face 05.** D:62 now says what D6 means there.
- **W4.** Not a real disagreement: SPEC:417 and WC:379 give the same rule in other words. Both are shown side by side.
- **W8.** docs/design/WORK-BOOK-BRIEF.md:13 and SPEC:398 now carry Tester's `workflow` option, as WC:311 does.
