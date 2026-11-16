# WORKING PATH, not a ruling. Tester (Grok Bot) check of the
# work book concept, W8-W13 and the first pack.

Checked docs/design/WORK-BOOK-CONCEPT.md at 08625be (HEAD, file
unchanged). Mon 16 Nov 2026, 5:53 PM EST. Proposed answers only.
Only Matthew rules.
Cites: C = the concept at 08625be. RUL = DIRECTOR-RULINGS.md.
WL = docs/spec/workflow-loop.003.md. SA = docs/spec/seqAddr.md.
Axioms.md lines confirmed (docs/spec/Axioms.md): 1 :13, 2 :15,
3 :17, 4 :19, 5 :21, 6 :23, 7 :25, 8 :27, 9 :29.
t223u, t226u, t227u = docs/review/DIRECTOR-WORDS-*.md.

## Verdict: holds, with fixes

The plan is sound: one slot per job, compute moves the status,
the board is not stored. Three things need fixing first.

## Top issues

1. The board already exists. C:96 says nothing shows all slots.
   Wrong: state.rs:296-300 builds a derived board, and
   GET /resolve on a plain 05 face returns it (resolve.rs:182-188;
   store.rs:158-159; test tails.rs:223). It shows tail only.
   So w02 is "add claim, reviewer, outcome", not a new route.
2. First pack fails t227u as written (see last section). The
   sheet's shape "lives in code for now" (C:135): an unseated
   template, the drift C:221 itself warns about.
3. W10 hole: books/ is in git (git ls-files books: 5 files), so
   "never books/" (C:202) is a promise, not a check. And only the
   claim holder may return (state.rs:563-567): a model on
   Matthew's machine that cannot reach the compute cannot return.

## W8. Is a work page a system page?

1. Plain: system pages freeze once linked. Is a work page one?
2. Answer in C:190 ("No") came from Tester's own check
   (WORK-BOOK-AXIOM-CHECK.md:27-34). Not trialed here, needs a
   different view (axiom 9 :29). Not graded.
3. New fact for that view: SA:192 already lists a page type
   `workflow`, beside `system` and `general`. A type carries its
   own rules: who may write, required faces (SA:193).
4. Option Matthew may not have thought of: type `workflow`. Not
   system, so R34 freeze does not apply; not general either.
   But no ruling says whether a workflow page locks (7).
5. Axioms (for the new option only): 2 :15 pass (reuse a type
   that exists); 7 :25 tension (lock rule for it is missing).
6. Conflicts: none yet. Must be ruled before the first work page:
   type is a locked field (RUL:189-190). R31 (RUL:134) and R34
   (RUL:169-170) only name system and general pages.

## W9. Does the return go on the same slot as the pack?

1. Plain: is the return the next step on pack slot 05.NN, or its
   own file?
2. Answer: same slot. Agree with Designer (C:196).
3. Why: one slot, one history; nobody matches files by hand.
   The code already writes the return body in the same log line
   as the open -> return move (state.rs:575). That is one change,
   so it meets R37 item 2 (RUL:196) and partly closes WL:181 7.
4. Options: show "side by side" (t226u:7) as an export view,
   pack above, return below (R26, RUL:106). Rework gets a new
   slot with a back-link, never a second return (WL:202).
5. Axioms: 2 :15 pass; 6 :23 pass (pack text kept, not
   rewritten); 8 :27 pass; 1 :13 pass; 9 :29 tension (E9 placement
   not seated, WL:181).
6. Conflicts: none. R37 item 1 (RUL:195) pass: one log.
   Fix: C:198 should cite state.rs:575 as the same-line proof.

## W10. Is a pushed return a book change?

1. Plain: the model commits and pushes (t223u:10). Books change
   only through the compute (RUL:159). Does a push break that?
2. Answer: a push may hold code and proof only. The return text
   goes in once, through the gate. Git keeps only a commit hash.
3. Why: C:202 lets return text sit in git AND the book. Two
   copies, two truths: conflicts R37 item 1 (RUL:195). Hurt:
   Matthew, reading a git copy that differs from the record.
4. Holes in C:202:
   - books/ is tracked in git. A pushed book file changes a
     book outside the gate unless something refuses it.
   - "The compute books the return" is wrong: the claim holder
     returns; the compute only in recovery (state.rs:563-571,
     WL:174). If Prima relays, the gate refuses her, or the record
     names the wrong builder (axiom 6 :23).
5. Options: (a) a merge check that refuses any push touching
   books/; (b) take books/ out of the worker's branch, give the
   model export/ only (R33, RUL:160); (c) workers push to their
   own branch, Prima merges (keeps "only Prima pushes"); (d) a
   per-pack writer token so the model returns as itself.
6. Axioms: 1 :13 tension (gate not checked on push); 2 :15
   tension (two copies); 6 :23 tension (who returned); 8 :27
   pass if git holds only the hash.
   Conflicts: R33 item 1 (RUL:159-160), R37 item 1 (RUL:195).

## W11. Is the board a view?

1. Plain: should the board be built fresh from the log, never
   saved as a 05.00?
2. Answer: yes. It is already built that way (issue 1).
3. Why: R9 bans FF.00 (RUL:37-38); the code refuses it
   (state.rs:530). A view cannot disagree with the slots.
4. Options: also offer it as an export file (R26) for reading
   off-box; mark stale reviews (R37 item 4, RUL:198) and "couldn't
   look" apart from "none" (R37 item 6, RUL:200).
5. Axioms: 2 :15 pass; 8 :27 pass (a view never becomes what it
   points to); 1 :13 pass; 6 :23 tension, see 6.
6. Conflicts: SA:197-198 still says a face is counted only if
   FF.00 exists, and "a counter without a board is invalid".
   WL:160 still says "N5 05.00 board". R9 governs, but the spec
   needs a written new step saying so (axiom 6 :23), not silence.
   Code marks this 7 already (resolve.rs:182).

## W12. First pack read-only, ahead of K8 step 1?

1. Plain: build the read-only sheet and board first, before the
   direct-write door is closed (CORE-AND-TOOLS-SPEC.md:870-873)?
2. Answer: yes, with two conditions.
   - Pack 1 is the first real use of the claim route on an open
     door. Say so; do not call it "no new way in" (C:144, C:215).
   - Pack 1 must be put in as `pack` with no check step
     (tail.rs:95-97). Record that skip as a named one-time
     override Matthew approves (axiom 2 :15).
3. Why: reading adds no write path, but the board will show
   forged lines as real (C:145-146). Hurt: Matthew, trusting a
   claim nobody made.
4. Options: label every sheet and board "door open: not proof"
   until K8 step 1 lands; or run K8 step 1 first, it is small.
5. Axioms: 1 :13 tension; 2 :15 tension (lint skipped); 7 :25
   pass ("not available" fields, C:133); 9 :29 pass.
6. Conflicts: R37 item 7, check before each run (RUL:201): no
   check step exists yet. Tension, not a break.

## W13. Seat templates before the check step?

1. Plain: put the pack, work card and return shapes in the
   kernel, approved, before the compute checks packs against them?
2. Answer: yes. Agree (C:220). Add the handoff sheet shape to
   that same set.
3. Why: a shape in code is a second copy (axiom 2 :15). Hurt:
   every worker, checked against a shape nobody approved.
4. Options: hold templates as rules of the `workflow` page type
   (SA:193; R19, RUL:75-76: each type has its own fields). Open
   the predecessor 0117.pack-lint read-only first (axiom 9 :29;
   WL:232).
5. Axioms: 1 :13 pass (Matthew approves); 2 :15 pass; 6 :23
   pass; 9 :29 tension (untried).
6. Conflicts: C:135 (sheet shape in code first) contradicts this
   answer. R37 item 3 (RUL:197) pass only once seated.

## First pack vs t227u: FAIL as written, fixable

t227u:5: "hand the jobs to the compute ... a constand template
that won't drift. Otherwises you will."
- Fail: sheet shape is hard-coded (C:135), not a seated template.
  Fix: seat the sheet shape first, or name the code shape a
  one-time override with an end date.
- Fail: Pack 1 text and its AGENTS.md (C:132-138) are written by
  hand. Unavoidable for the first pack, but must be named as the
  bootstrap exception, not left silent.
- Fail: no check step, so Pack 1 enters as `pack` unchecked
  (tail.rs:95-97; WL:171).
- Pass: missing fields say "not available", never guessed (C:133,
  R37 item 6, RUL:200). Pass: the model writes only judgment
  (R37 item 3, RUL:197) once the sheet prints the prompt box.

## Not trialed here, needs a different view

- W8's "No" (Tester's own, WORK-BOOK-AXIOM-CHECK.md:27-34).
- C's "AX:" marks for W1-W7 (C:233-237): Tester's own.
