# Decisions waiting for you

For Matthew. By Designer. An index, not a ruling. Only you approve.
made: Mon 16 Nov 2026, 9:00 PM EST. Updated: Tue 17 Nov 2026, 11:50 AM EST (one-page proposal after your t243u).

How to read this:
- One line for the question. One line for the answer we propose.
- "Unblocks": what can go ahead once you answer.
- "Waits on": answer that one first. "none marked" means the file marks nothing.
- "Full form": where the question, the answer, the why and the axiom marks are written.

Files: WC = docs/design/WORK-BOOK-CONCEPT.md. PT = docs/design/PACK-TEMPLATE.md.
D = docs/design/DEV-WORK-LAB-PAGES.md. SPEC = docs/design/WORK-BOOK-SPEC.md.
OPW = docs/design/ONE-PAGE-WORK.md (a proposal; waits on your yes).

## Top three

From your t243u idea: one page per piece, faces 01-08 (OPW). Picked by what blocks most.

1. **O1. One page per piece, faces 01-08, labs on face 07?**
   - Answer (Prima): yes. Face 07 is "not active" today (seqAddr.md:156), so it needs your yes, a spec step and code.
   - Why top: every page's shape waits on it.
   - Unblocks: the first piece page; makes D1, D3, D4, D5 moot. Waits on: none marked. Full form: OPW:91.
2. **O2. Do you review every pass?**
   - Answer (Prima): you review at seat, or when the work is risky or new. A review bot does routine passes.
   - Why top: every pass's review step waits on it. It changes your own hand-off (t239u:10).
   - Unblocks: the tail steps; who closes. Waits on: O3 for the bot. Full form: OPW:97.
3. **O4. Face 03 follows your R35?**
   - Answer (Prima): yes; fix seqAddr.md:189 and the code.
   - Why top: the code refuses the 03 menu, so no page can be written whole.
   - Unblocks: a page the code accepts. Waits on: none marked. Full form: OPW:103.

## The rest of the one-page list (OPW)

- **O3. A review bot reviews, not Prima; a different model runs trials?** Answer (Prima): yes. Unblocks: O2; face 07 trials. Waits on: O1 for trials. Full form: OPW:109.
- **O5. The 01 card is the one AGENTS.md?** Answer (Prima): yes; the file is a compute copy. Unblocks: W2; PT part 4. Full form: OPW:115.
- **O6. Best pass seated on plain 05?** Answer: yes, after a spec and code change. Unblocks: O2's "review at seat". Full form: OPW:121.
- **O7. Decisions on 04, notes on 06?** Answer: yes; partly in your t243u words. Unblocks: D5's replacement. Full form: OPW:127.
- **O8. The completing page?** Answer (Prima): the band head. Waits on: O1, W11. Full form: OPW:133.
- **O9. 02 pseudo code drift?** Answer (Prima): 08 links the code; each return notes mismatches. Waits on: O1. Full form: OPW:139.
- F1-F7 (WC:266-308) are merged into O1-O8. Their full forms stay as history.

## The work book (WC)

- **W9. Does the return sit on the same slot as its pack?**
  - Answer: yes, the same slot.
  - Unblocks: D1; D5; the return template. Waits on: none marked. Full form: WC:321.
- **W11. Is the board only a view, never stored?**
  - Answer: yes, built from the log each time.
  - Unblocks: the board columns in pack 1. Waits on: none marked. Full form: WC:341.
- **W12. Does the read-only sheet and board go first?**
  - Answer: yes, ahead of the template check and K8 step 1.
  - Unblocks: pack 1. Waits on: none marked. Full form: WC:350.
- **W13. Seat the templates before the check step?**
  - Answer: yes.
  - Unblocks: the check step; D5; P5. Waits on: none marked. Full form: WC:356.

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

Moot if you say yes to O1, except D2 (OPW:146). Kept, not deleted.

- **D1. What is the lab page for?**
  - Answer: trying to break risky work only. Made only when needed.
  - Unblocks: the lab page. Waits on: W9, O1 (was F1; D:175). Full form: D:186.
- **D3. Who makes the pages and links, and when?**
  - Answer: the compute, before you approve the dev page.
  - Unblocks: making a set of pages. Waits on: O1 (was F1; D:175). Full form: D:192.
- **D2. When is a page linked?**
  - Same question as P7. Full form: PT:270 (pointer at D:198).
- **D4. Is 05NN "jobs" or "build"?**
  - Answer: jobs. 03NN is build. seqAddr.md is fixed later.
  - Unblocks: the seqAddr.md:243 fix. Waits on: none (D:174). Full form: D:201.
- **D5. Must Prima's note come before the next pack?**
  - Answer: yes, but only after an earlier pack has closed.
  - Unblocks: the check before each new pack. Waits on: W13, W9, O7 (was F6; D:174-175). Full form: D:207.

## Answered by you, t239u (docs/review/DIRECTOR-WORDS-t239u.md)

Answered, not ruled. The full forms stay, marked answered.
- **W8.** "1. I agree" (:9). Not a system page. The `workflow` type is not in your words (O4, was F3). Full form: WC:312.
- **D6.** "2.  Yes that is the purpose of 05.counter ..." (:10). Face 05 is the page's own passes. Full form: D:177.
- **W10 and P6.** "3. Yes, see 2." (:11). The pushed file only carries the return; the compute records it once. Full forms: WC:327, PT:249.
- Your line 5 (t239u:5), "Have you pushed the workflow document yet?": answered by Prima, pushed f1074850..a39de1c0 (per Prima; not checked here).

## Also open (found in these files, not in the list above)

- **W1-W7.** Full forms in SPEC: W1 :382, W2 :390, W3 :409, W4 :417, W5 :425, W6 :433, W7 :441.
  - WC lists W1, W2, W3, W6, W7 as "still open for you to confirm" (WC:371-375).
  - WC has its own full forms for W4 (WC:380) and W5 (WC:387). W4 says the same rule as SPEC W4, in other words.
- **"6" and "8".** WC asks what you meant by "6 framing the work, with 8 returning" (WC:376).
  - It has no proposed answer and no axiom marks.
- **K8.** "In what order should we build?" Full form: docs/design/CORE-AND-TOOLS-SPEC.md:870.
  - W12 and PT both wait on its step 1 for the door label.
- **R37 item 5.** Where "selected, pending, accepted" show is marked open (7) at PT:114.
  - It has no full form yet.

## Disagreements settled (2026-11-16)

The newer, checked file won. Old text is kept, marked superseded.
- **Pack 1.** WC:161 now follows PT P8 (PT:264).
- **The return in git.** W10 (WC:327) now fits P6 (PT:249). Answered in t239u.
- **Return order.** WC:183 now marks the order open, per PT P1 (PT:258).
- **Dev face 05.** D:63 now says what D6 means there.
- **W4.** Not a real disagreement: SPEC:417 and WC:380 give the same rule in other words. Both are shown side by side.
- **W8.** docs/design/WORK-BOOK-BRIEF.md:13 and SPEC:398 now carry Tester's `workflow` option, as WC:312 does.
