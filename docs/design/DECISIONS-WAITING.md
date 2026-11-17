# Decisions waiting for you

For Matthew. By Designer. An index, not a ruling. Only you approve.
made: Mon 16 Nov 2026, 9:00 PM EST. Updated: Tue 17 Nov 2026, 12:30 PM EST (your t259u: tool steps; S12, S13 answered in direction). Earlier update: SAMPLE-PAGE v2, t254u, t255u.

How to read this:
- One line for the question. One line for the answer we propose.
- "Unblocks": what can go ahead once you answer.
- "Waits on": answer that one first. "none marked" means the file marks nothing.
- "Full form": where the question, the answer, the why and the axiom marks are written.

Files: WC = docs/design/WORK-BOOK-CONCEPT.md. PT = docs/design/PACK-TEMPLATE.md.
D = docs/design/DEV-WORK-LAB-PAGES.md. SPEC = docs/design/WORK-BOOK-SPEC.md.
OPW = docs/design/ONE-PAGE-WORK.md (one page per piece; O1 answered yes, t246u:6).
SP = docs/design/SAMPLE-PAGE.md (EXAMPLE car steering page, three passes; v2). SPP = docs/design/SAMPLE-PAGE-PATHS.md (harder paths).
WT = docs/design/WORKFLOW-TOOLS.md (the six tool steps, build order, pre-draft check, finish ping; T1-T4).

## Top three

Picked by what blocks most.

1. **Check the sample page, version 2 (O5 and the whole layout).**
   - You asked to "check it before we build it" (t249u:11), with three passes (t250u:5). v2 folds the Codex and Claude reviews.
   - O5 status: yes, pending your look at the sample (t249u:7).
   - Why top: nothing gets built until you have checked it.
   - Unblocks: pack 1; the first fixture; the workflow branch; the tool build (WT). Sample: SP:1 ("Now" at SP:13). Harder paths: SPP:1. O5: OPW:290.
2. **S9. One rule for scope.**
   - Answer (Claude, relayed t253u): your grant is the ceiling; `may touch` is the frame, checked inside it; `must not` is derived; face 01 holds no scope.
   - Why top: the Issue step's path check and the Check step's touched-file check both depend on it (WT, steps 1 and 3).
   - Unblocks: the prompt box; the frame check. Waits on: none marked. Full form: OPW:402.
3. **T4. Pre-draft pins: refuse a pack built on old 04, 06 or 05?**
   - Answer (Designer): yes. The pack pins face 04, face 06 and the last closed 05 (entry number plus hash); Prime writes one 06 note citing them; the compute refuses a pack whose pins are not current.
   - Why top: it is how your 2.1 "but" gets checked (t259u:7). Every pack needs it.
   - Unblocks: the Issue step (WT build order 3). Waits on: T2 ("06 allow"). Full form: WT, "T4".

Moved down from the top three: S6 (still open, below). S12 answered in direction (t259u:8).

## Still open (OPW)

- **S6. What the close record holds?** Answer (Designer): the close event carries pack hash, return hash, commit, review entries, and each card's fate. Unblocks: the close change at store.rs:991-992. Waits on: S7. Full form: OPW:408.
- **T1. Branch name and who merges (open detail of S12).** Answer (Designer): `pass/<page>.05.<NN>`; the compute merges accepted cards at close, after Prime signs. Full form: WT, "T1".
- **T2. "06 allow": did you mean "06 along"?** Answer (Prima's reading): yes. Full form: WT, "T2".
- **T3. How the finish ping reaches the compute?** Answer (Designer): now, the push is the ping, checked when Prima pulls; later, direct to a local compute. Full form: WT, "T3".
- **E1. Which signals send work up?** You asked for more (t249u:5); Prima answered with the trigger list (per Prima, t249u:15). Still open after t259u: your 2.6 covers the finish ping, not the triggers (WT, step 6). Table: OPW:94. Full form: OPW:329.
- **S4. AGENTS.md sources?** Proposed this way (Codex, t252u): released pack + pinned 01 card + governing instructions, with revisions. Full form: OPW:391.
- **S5. Face 09: stored, or a view of the log?** Answer: a view. Full form: OPW:421.
- **S7. Words for each card's fate?** Answer: accepted, pending, discarded, carried. Full form: OPW:428.
- **S8. May Prime change face 01?** Answer: inside the grant, yes; "Done when" comes to you. Full form: OPW:434.
- **S10. Cost figures?** Answer: from records; worker note only. Full form: OPW:440.
- **S11. Face 02: design or description?** Answer: the design. Full form: OPW:446.
- **S14. Who may change the Prime?** Answer: you, or by your grant. Full form: OPW:459.
- **S15. A pass open across a change of Prime?** Answer: the Prime at sign-off signs, after reading in full. Full form: OPW:465.
- **S2. Face 00 `role` and `set` with no bands?** Answer: drop `set`; `role` becomes `work`. Full form: OPW:379.
- **S3. Where 02 drift goes in the return?** Answer: a short line after notes. Full form: OPW:385.
- **E3. How you review as it goes?** Answer: a feed and the board. Full form: OPW:344.
- **E4. Prima's "occasional checks"?** Answer: by a written rule, noted on 06. Full form: OPW:350.
- **E5. What "flex" means for 07 outside dev work?** Answer: set by page type. Full form: OPW:356.
- **O3 (partly answered, t245u:10).** Open part: who runs a face 07 trial. Full form: OPW:283.
- **O9 (partly answered, t245u:13).** Open part: each return noting mismatches (S3). Full form: OPW:319.
- **O6. Best pass seated on plain 05?** Full form: OPW:298.
- **O7. Decisions on 04, notes on 06?** Full form: OPW:305.
- **O8. The completing page?** Full form: OPW:312.
- F1-F7 (WC:266-308) are merged into O1-O8. Their full forms stay as history.
- Review table (Codex t252u, Claude t253u): OPW:221.

## Next (not started)

- Next: make this sample the first workflow fixture (Codex suggestion, t252u:17). Not started.
- Next: build the tools in the order in WT (status view first). Not started; waits on your look at the sample.
- Next: workflow branch for tools and templates (not started). Your words: "Then once it's good we'll start by setting up a branch for our workflow.  Where the tools and templates exist so I can pull them for future work any time for any model to use." (t249u:13)

## Follow-on work (not questions; not done)

- Face 07 as labs: seqAddr.md 5.1, 5.2, 5.7; decisions.md A4.3; face.rs:72-85; validate.rs:229-234.
- Face 03 per R35: seqAddr.md:189; validate.rs:352-354.
- Prime signs off, the compute closes: store.rs:991-992, checked against face 00 `prime` (S1). See OPW:116.
- Face 00 `prime` and `previous-primes`: a new step in docs/spec/face00.md 3.1 (S1).
- Dated "superseded" notes in each file on the list at OPW:209.

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

Moot: you said yes to O1 (t246u:6). D2 stays (OPW:471). Kept, not deleted.

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

## Answered by you, t259u (docs/review/DIRECTOR-WORDS-t259u.md)

Answered, not ruled. Tool steps in WT.
- **Step 1, Issue.** "2.1. Yes, but we need to make sure lead is checking the 04 face and 06 allow with the previous completed 05" (:7). "06 along" is Prima's reading (T2). The check: WT, "The pre-draft check".
- **S12, one branch per pass: answered in direction.** "2.2 I agree" (:8). Open detail: T1. Full form: OPW:414.
- **S13, checker before the lead's read: answered in direction.** "2.3 I agree" (:9). Full form: OPW:452.
- **Step 4, sign-off.** "2.4 Yes lead signed off on the work." (:10)
- **Step 5, status view.** "2.5 Yes we need this to be part of it.  lead model and person need this part.  It's hard right now to keep in my mind everything that is going on. which is what we are doing." (:11). Built first (WT build order 1).
- **Finish ping.** "2.6 That is right, when a model finishes it's work it pings the compute so the compute can file the completed 05." (:12). The step 6 triggers are not in these words; E1 stays open.

## Answered by you, t254u and t255u

Answered, not ruled.
- **Who Prime is.** "Sorry I ment you.  It's actually the team lead, I have called that position prime.  It seemed to work well with models." (DIRECTOR-WORDS-t254u.md:7). Prime is the team lead role; here Prima holds it.
- **S1.** "That should be a field for 00.  Current lead, along with previous leads." (DIRECTOR-WORDS-t255u.md:7). Full form: OPW:364.

## Answered by you, t249u

Answered, not ruled.
- **E2.** "2. Prime signs off the compute closes it." (DIRECTOR-WORDS-t249u.md:6). Full form: OPW:336.
- **One-page design.** "I liked the one-page work design.  it looks good." (t249u:9).

## Answered by you, t246u and t245u

Answered, not ruled. Full forms stay, marked answered.
- **O1.** "1. Yes I agree" (DIRECTOR-WORDS-t246u.md:6). One page per piece, faces 01-08. Face 07: "07 is a flex location, for dev work it's going to become labs." (DIRECTOR-WORDS-t245u.md:5). Full form: OPW:262.
- **O2.** "2. See previous response." (t246u:8). Read by Prima as t245u item 1: "If the worker can't solve it comes to you, if prime can't solve by giving improved frame and authority.  It comes to the person." (t245u:8). Full form: OPW:269.
- **O4.** "3. Yes I agree" (t246u:10). Face 03 per R35. Does not clearly cover O5. Full form: OPW:276.

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
