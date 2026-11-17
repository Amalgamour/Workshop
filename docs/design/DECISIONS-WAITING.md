# Decisions waiting for you

For Matthew. By Designer. An index, not a ruling. Only you approve.
made: Mon 16 Nov 2026, 9:00 PM EST. Updated: Tue 17 Nov 2026, 12:20 PM EST (your t249u and t250u; SAMPLE-PAGE.md).

How to read this:
- One line for the question. One line for the answer we propose.
- "Unblocks": what can go ahead once you answer.
- "Waits on": answer that one first. "none marked" means the file marks nothing.
- "Full form": where the question, the answer, the why and the axiom marks are written.

Files: WC = docs/design/WORK-BOOK-CONCEPT.md. PT = docs/design/PACK-TEMPLATE.md.
D = docs/design/DEV-WORK-LAB-PAGES.md. SPEC = docs/design/WORK-BOOK-SPEC.md.
OPW = docs/design/ONE-PAGE-WORK.md (one page per piece; O1 answered yes, t246u:6).
SP = docs/design/SAMPLE-PAGE.md (EXAMPLE car steering page, three passes).

## Top three

Picked by what blocks most.

1. **Check the sample page (O5 and the whole layout).**
   - You asked: "What I want is the designer to layout a sample for me.  So I can check it before we build it." (t249u:11). Three passes, as you asked (t250u:5).
   - O5 status: yes, pending your look at the sample (t249u:7).
   - Why top: nothing gets built until you have checked it.
   - Unblocks: pack 1; the workflow branch. Waits on: none. Sample: SP:1. O5 full form: OPW:243.
2. **E1. Which signals send work up?**
   - You asked for more: "1. Tell me more." (t249u:5). Prima answered with the trigger list (per Prima, t249u:15).
   - Why top: the ladder (t245u:8) can't run without its triggers.
   - Unblocks: elevation. Waits on: none marked. Table: OPW:80. Full form: OPW:282.
3. **S1. How does the compute know who may sign off?**
   - Answer (Designer): the pack's `lead` is copied onto the pass at draft -> pack; only that lead signs off, and only what the checks support.
   - Why top: your "Prime signs off the compute closes it" (t249u:6) needs it in the code.
   - Unblocks: the close change at store.rs:991-992. Waits on: none marked. Full form: OPW:317.

## Still open (OPW)

- **S2. Face 00 `role` and `set` with no bands?** Answer: drop `set`; `role` becomes `work`. Full form: OPW:323.
- **S3. Where 02 drift goes in the return?** Answer: a short line after notes. Full form: OPW:329.
- **S4. AGENTS.md: the 01 card or the pack fields?** Answer: the 01 card only. Full form: OPW:335.
- **E3. How you review as it goes; does your comment stop work?** Answer: a feed and the board; a comment halts only if you call it a conflict. Full form: OPW:297.
- **E4. Prima's "occasional checks"?** Answer: the work and the checker, picked by a written rule, noted on 06. Full form: OPW:303.
- **E5. What "flex" means for 07 outside dev work?** Answer: set by page type; reserved elsewhere. Full form: OPW:309.
- **O3 (partly answered, t245u:10).** Open part: who runs a face 07 trial. Full form: OPW:236.
- **O9 (partly answered, t245u:13).** Open part: each return noting mismatches (S3). Full form: OPW:272.
- **O6. Best pass seated on plain 05?** Still open. Full form: OPW:251.
- **O7. Decisions on 04, notes on 06?** Still open; t245u:12 puts MVP goals on 04. Full form: OPW:258.
- **O8. The completing page?** Still open. Full form: OPW:265.
- F1-F7 (WC:266-308) are merged into O1-O8. Their full forms stay as history.

## Next (not started)

- Workflow branch for tools and templates (not started). Your words: "Then once it's good we'll start by setting up a branch for our workflow.  Where the tools and templates exist so I can pull them for future work any time for any model to use." (t249u:13)

## Follow-on work (not questions; not done)

- Face 07 as labs: seqAddr.md 5.1, 5.2, 5.7; decisions.md A4.3; face.rs:72-85; validate.rs:229-234.
- Face 03 per R35: seqAddr.md:189; validate.rs:352-354.
- Prima signs off, the compute closes: store.rs:991-992, plus a lead field on the pass (S1). See OPW:102.
- Dated "superseded" notes in each file on the list at OPW:194.

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

Moot: you said yes to O1 (t246u:6). D2 stays (OPW:341). Kept, not deleted.

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

## Answered by you, t249u

Answered, not ruled.
- **E2.** "2. Prime signs off the compute closes it." (DIRECTOR-WORDS-t249u.md:6). Full form: OPW:289.
- **One-page design.** "I liked the one-page work design.  it looks good." (t249u:9).

## Answered by you, t246u and t245u

Answered, not ruled. Full forms stay, marked answered.
- **O1.** "1. Yes I agree" (DIRECTOR-WORDS-t246u.md:6). One page per piece, faces 01-08. Face 07: "07 is a flex location, for dev work it's going to become labs." (DIRECTOR-WORDS-t245u.md:5). Full form: OPW:215.
- **O2.** "2. See previous response." (t246u:8). Read by Prima as t245u item 1: "If the worker can't solve it comes to you, if prime can't solve by giving improved frame and authority.  It comes to the person." (t245u:8). Full form: OPW:222.
- **O4.** "3. Yes I agree" (t246u:10). Face 03 per R35. Does not clearly cover O5. Full form: OPW:229.

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
