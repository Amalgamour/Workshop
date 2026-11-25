# Open questions: the draft-page kernel

Builder: Claude. 2026-11-25.
These are choices for Matthew. None of them is decided here.
Each has 2 or 3 options and a default. The default is what the design in README.md assumes until Matthew answers.
The section numbers point to labs/draft-page/README.md.

---

## Q1. Is the replacement a whole draft page, or a draft branch on the work-order page?

Section 4.

- **A. A draft branch on the work-order page.** (default)
  - The page stays live as a page. Only its product is a draft, on `draft/<page>`.
  - wf can do this today with `pack --branch` (src/cmd.rs:389-391).
- **B. A separate page in state `draft`.**
  - A new page, with `state: draft` and a `why-draft:` line (docs/spec/face00.md:103, :107-111 @dcdab638).
  - It is promoted by a new recorded step.
  - wf has no page state today, so this needs new code.
- **C. A draft face on a kernel page.**
  - The kernel gets its own page, and its schema face is drafted as `02.draft` (docs/spec/seqAddr.md:151, :206 @dcdab638).
  - It uses copy, note, merge and promote (docs/spec/drafting.md:24-31 @dcdab638), none of which wf has yet.

Why A is the default: it needs no new wf code, and it can be tried on 0426 next week.

---

## Q2. Where is the live pin recorded?

Section 2. Today no single record says which wf build is live. The pin is only named in prompts, for example "Use wf from a823" (WORK-PAGE-2026-11-25.md:61 @dcdab638).

- **A. A line on face 08 of the band door, 90.50.10.0400.** (default)
  - The line is `live wf: <commit>, since <date>, by <switch pass>`.
  - The Prime writes it after each switch. No new code is needed.
  - Face 08 holds links to exact commits (docs/DESIGN.md:29).
- **B. Each worker's own config.**
  - That is the `wf_rev` field in the 0705 report-system design (labs/0705/SPEC.md:20).
  - It is per worker, so it records what each worker runs, not what is meant to be live.
- **C. A new kernel page.**
  - One page whose log records every pin move as an entry.
  - It needs a new page and probably a new entry kind.

---

## Q3. Who approves the switch from live to draft?

Section 6, step 5.

- **A. The Prime signs off the switch pass, and Matthew approves the merge and the pin move.** (default)
  - Why: a switch changes what is live for every page, and authority is held by the person (docs/AXIOMS.md:15).
- **B. The Prime alone, after a passed check.**
  - This is how every other pass closes today (docs/DESIGN.md:66-70).
  - It is faster, but nobody above the Prime sees a change that touches everyone.
- **C. The book's Prime.**
  - That is the lead one step below the person, recorded on the book identity page by page 0425 (docs/review/PENDING-RULES.md:40, :54 @dcdab638, t541u).
  - It waits for 0425 to land.

---

## Q4. While a draft is open, does it hold its files on returns?

Section 5. This is how t569u is read: "No two workers may need the same locked files" (WORK-PAGE-2026-11-25.md:31 @dcdab638).

- **A. No. A pass on a `draft/` branch holds its files only on that branch, until its switch pass.** (default)
  - Live lanes on returns keep working. The switch pass freezes them only for the catch-up (section 6, step 1).
  - This is what lets the live kernel keep working (WORK-PAGE-2026-11-25.md:190 @dcdab638).
- **B. Yes. It holds them on returns too, as any pass does today.**
  - It is safer, but there is no gain over today: everyone waits again.

---

## Q5. A draft pass's page log lands on the draft branch. Where should it live?

Section 5. `return --push` pushes the log to the pack's branch (src/cmd.rs:716-718, :773-797). So the draft page's log is split across `returns` and `draft/<page>`.

- **A. Leave it on the draft branch, and intake with `--branch draft/<page>`.** (default)
  - It works today (src/cmd.rs:832).
  - At the switch merge, the draft page's log comes back to returns with the code. The prefix rule still holds (src/cmd.rs:771-794).
  - Risk: this is safe only if every entry of the draft page goes to the draft branch while it is open. If the Prime also pushes a face write of that page to returns, the two log files differ, and the switch merge conflicts on that file.
  - So, under A, all of the draft page's work goes to the draft branch until the switch.
- **B. A later wf change: the code goes to the pack's branch, and the log always goes to returns.**
  - There is one home for every log. It needs a change in `push_log`.
- **C. Keep the draft page's own faces and passes on returns, and put only the code on the draft branch, by hand.**
  - The lead pushes the log copy with the byte-prefix check. It is more hand steps.

---

## Q6. When a draft is dropped, is its branch kept?

Section 8, step 5.

- **A. Keep the branch, and mark it dropped on face 08.** (default)
  - Nothing is lost, and the tried code stays readable (docs/AXIOMS.md:25).
- **B. Delete the branch after the close.**
  - The log still names the commit, but git may drop the commit later, so the trail can go stale.
- **C. Tag the tip, for example `dropped/<page>.<NN>`, and then delete the branch.**
  - The tag keeps the commit. The branch list stays short.

---

## Q7. Should wf check overlapping files across pages?

Section 5. Today it checks only within one page (src/cmd.rs:344).

- **A. Not now. The lead keeps the cross-page rule by hand, with the freeze list (TEST-PLAN.md, D11).** (default)
- **B. Yes, in a later page. `wf pack` reads every page in the run folder and refuses an overlap with an open pass on another page.**
  - It needs every page's log to be present and current in the run folder.
- **C. Yes, but only as a warning, so a lead can still pack with a reason.**

---

## Q8. Should wf refuse a pack whose start is older than the last switch?

Section 6, step 7. Today wf refuses stale face pins only (src/cmd.rs:382).

- **A. Not now. The lead lists stale packs by hand after each switch (TEST-PLAN.md, D10).** (default)
- **B. Yes, once the pin record exists (Q2). `wf claim` refuses a pass whose start is not a descendant of the live pin, when its may-touch overlaps the switched files.**
- **C. Yes, but at pack time only, not at claim time.**

---

## Not a question, but raised

- The pinned a823 tool has neither `withdraw` (src/cmd.rs:460) nor the 0423 lockout (src/cmd.rs:575) (WORK-PAGE-2026-11-25.md:61 @dcdab638). Prima's steps for today still say to sign off and pack "with a823" (WORK-PAGE-2026-11-25.md:71, :74 @dcdab638).
- So until the pin moves, the lock rules in this design are not enforced by the tool that workers run.
- Moving the pin past 0423 is itself the first live-to-draft switch. It may be the right first trial of this design.
