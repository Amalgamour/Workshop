# Decisions waiting for you

For Matthew. By Designer. An index, not a ruling. Only you approve.
made: Mon 16 Nov 2026, 9:00 PM EST

How to read this:
- One line for the question. One line for the answer we propose.
- "Unblocks": what can go ahead once you answer.
- "Waits on": answer that one first. "none marked" means the file marks nothing.
- "Full form": where the question, the answer, the why and the axiom marks are written.

Files: WC = docs/design/WORK-BOOK-CONCEPT.md. PT = docs/design/PACK-TEMPLATE.md.
D = docs/design/DEV-WORK-LAB-PAGES.md. SPEC = docs/design/WORK-BOOK-SPEC.md.

## Top three

Each file has its own top three. I picked the three that block the most other questions.

1. **W8. Is a work page a system page?**
   - Answer: no. You read work pages.
   - Unblocks: the first work page; P8; D3.
   - Waits on: none. Rule it first (WC:198).
   - Full form: WC:200.
2. **D6. What does face 05 hold?**
   - Answer: one meaning on every page: that page's own passes, best one seated. Questions become jobs in a design pass. (Tester's "B with I"; still your choice.)
   - Unblocks: D1; D5. Needs a seqAddr.md step and a code change first.
   - Waits on: none (D:169).
   - Full form: D:171.
3. **P6. How does the builder hand back?**
   - Answer: a one-job pass, and a return file in the push that the compute reads.
   - Unblocks: pack 1 can finish.
   - Waits on: none (PT:242). It needs a change to W10.
   - Full form: PT:244.

## The work book (WC)

- **W9. Does the return sit on the same slot as its pack?**
  - Answer: yes, the same slot.
  - Unblocks: D1; D5; the return template. Waits on: none marked. Full form: WC:206.
- **W10. Is a pushed return a book change?**
  - Answer: no, if the push holds only code and proof.
  - Unblocks: P6. Waits on: none marked. Full form: WC:212.
- **W11. Is the board only a view, never stored?**
  - Answer: yes, built from the log each time.
  - Unblocks: the board columns in pack 1. Waits on: none marked. Full form: WC:218.
- **W12. Does the read-only sheet and board go first?**
  - Answer: yes, ahead of the template check and K8 step 1.
  - Unblocks: pack 1. Waits on: none marked. Full form: WC:227.
- **W13. Seat the templates before the check step?**
  - Answer: yes.
  - Unblocks: the check step; D5; P5. Waits on: none marked. Full form: WC:233.

## The pack template (PT)

- **P1. In what order does a return go?**
  - Answer: job items first, with a short summary on top. You pick.
  - Unblocks: the return template. Waits on: none (PT:242). Full form: PT:250.
- **P8. How is pack 1 made, if not by the tool?**
  - Answer: a script fills it, an outside view checks it, and your one-time yes is recorded.
  - Unblocks: pack 1 can go in. Waits on: W8 (PT:242). Full form: PT:256.
- **P7. Are pages linked by number, or by a written link?**
  - Answer: the number finds the page. Only a link both ways connects it.
  - Unblocks: the linked-pages row. Waits on: none (PT:242). Full form: PT:262.
- **P2. Who fills "authorized"?**
  - Answer: Prima names it, the compute checks it.
  - Unblocks: the authorized field. Waits on: none (PT:242). Full form: PT:268.
- **P3. Where does the start commit come from?**
  - Answer: from Prima's push, checked, and fixed at claim time.
  - Unblocks: the start-commit field. Waits on: none (PT:242). Full form: PT:274.
- **P4. What is hashed, and when?**
  - Answer: five things, listed in the file. The method is still open.
  - Unblocks: the hash design. Waits on: none (PT:242). Full form: PT:280.
- **P5. When does the code copy of the sheet end?**
  - Answer: when pack 2 closes passed.
  - Unblocks: the sheet shape. Waits on: none (PT:242). Full form: PT:286.

## Dev, work and lab pages (D)

- **D1. What is the lab page for?**
  - Answer: trying to break risky work only. Made only when needed.
  - Unblocks: the lab page. Waits on: W9, D6 (D:169). Full form: D:177.
- **D3. Who makes the pages and links, and when?**
  - Answer: the compute, before you approve the dev page.
  - Unblocks: making a set of pages. Waits on: W8 (D:169). Full form: D:183.
- **D2. When is a page linked?**
  - Same question as P7. Full form: PT:262 (pointer at D:189).
- **D4. Is 05NN "jobs" or "build"?**
  - Answer: jobs. 03NN is build. seqAddr.md is fixed later.
  - Unblocks: the seqAddr.md:243 fix. Waits on: none (D:169). Full form: D:192.
- **D5. Must Prima's note come before the next pack?**
  - Answer: yes, but only after an earlier pack has closed.
  - Unblocks: the check before each new pack. Waits on: W13, W9, D6 (D:169). Full form: D:198.

## Also open (found in these files, not in the list above)

- **W1-W7.** Full forms in SPEC: W1 :373, W2 :381, W3 :396, W4 :404, W5 :412, W6 :420, W7 :428.
  - WC lists W1, W2, W3, W6, W7 as "still open for you to confirm" (WC:246-251).
  - WC has its own full forms for W4 (WC:257) and W5 (WC:263).
- **"6" and "8".** WC asks what you meant by "6 framing the work, with 8 returning" (WC:253).
  - It has no proposed answer and no axiom marks.
- **K8.** "In what order should we build?" Full form: docs/design/CORE-AND-TOOLS-SPEC.md:870.
  - W12 and PT both wait on its step 1 for the door label.
- **R37 item 5.** Where "selected, pending, accepted" show is marked open (7) at PT:109.
  - It has no full form yet.

## Where the files disagree

- **Pack 1.** WC:146 says pack 1 is hand-written. PT P8 (PT:256) says a script fills it and an outside view checks it.
- **The return in git.** W10 (WC:212) says the return text never goes in git. P6 (PT:244) puts it in a pushed file. P6 says so.
- **Return order.** WC:167-174 lists the job items first, as settled. PT P1 (PT:250) leaves the order open.
- **Dev face 05.** D:58 lists design questions on dev face 05 (WL S12). D6's proposed answer turns them into jobs in design passes there.
- **W4.** SPEC:404 answers "yes, as a starting rule". WC:257 answers "the cheaper builder goes first if a test can check it".
- **W8.** docs/design/WORK-BOOK-BRIEF.md:11 and SPEC:389 say only "no". WC:200 adds Tester's `workflow` page-type option.
