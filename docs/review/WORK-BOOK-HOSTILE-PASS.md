# Work book spec: hostile pass

WORKING PATH. Hostile pass by Tester (Grok Bot). Not a ruling.
Tested: docs/design/WORK-BOOK-SPEC.md at a990738 (Designer).
"spec:NNN" is a line of it. RULINGS is DIRECTOR-RULINGS.md.
A bare ":NN" after an axiom is Axioms.md. Matthew alone rules.

## Verdict: holds with fixes

The idea holds: one job per page, builders never touch books.
Five things need fixing before it goes to Matthew.

## Top findings

1. The worked example does not close the door its title names.
   - Spec:179 "closing the direct-write door". Its stop-if
     (spec:205): "the fix needs a new OS account or file
     permissions". Core spec: "Only the OS permission stops
     that" (CORE-AND-TOOLS-SPEC.md:236).
   - So a job that passes still leaves the door open.
   - Fix: call it "narrow the door"; the OS account is a later
     page.
2. The example's frame is too small for card w02.
   - w02 moves the token file out of books/ (spec:210). That path
     also sits in scripts/dev.sh:14, crates/compute/src/lib.rs:94
     and :117, and crates/trial-compute/src/lib.rs:64-66.
   - "may touch" (spec:202-203) lists none of them. The builder
     must stop or break the frame. Axiom 5 tension (:21).
3. "Check the diff" cannot see the worst write.
   - Spec:123: "the review must check each return's diff for
     books/ paths". But .gitignore:5 ignores books/.identities.
   - A builder that adds a director token leaves no diff.
   - Fix: hash books/.identities and books/.queue before and
     after each job.
4. A third set of state names.
   - Spec:167: "drafted, released, claimed, returned, accepted".
   - Code: "draft -> pack -> open -> return -> review -> closed"
     (crates/seqaddr-core/src/tail.rs:80).
   - Core B15: selected, pending, review, accepted
     (CORE-AND-TOOLS-SPEC.md:570-578).
   - The work list has no "review", yet W6 needs one. Axiom 2
     (:15): "do not reinvent what already exists".
5. The interim plan keeps the truth by hand.
   - W1, spec:265: "let Prima keep the state by hand".
   - R37 item 1 (DIRECTOR-RULINGS.md:195): "One append-only log
     is the only source of truth". Axiom 1 (:13): "a memory does
     not outrank it".
   - Today's gate works for any book; the open door is the same
     risk for all. Fix: write state lines through the gate now.

## Gaps

- Page type. R36 makes it a locked field (RULINGS:190). The spec
  gives a work page none. 7.
- System page or not (new question). R34: "system pages freeze
  once linked (faces 00-04)" (RULINGS:170). If a work page is
  one, a stored face 01 AGENTS.md (W2) freezes too, and spec:169
  "If the page changes" cannot happen.
- Return plus next step. R37 item 2 (RULINGS:196): "A return and
  its next step are saved together". Spec:116 cites only the
  delivery-id half.
- Lost reply. Returns go through the gate (spec:95). A retried
  proposal books twice today (CORE-AND-TOOLS-SPEC.md:342, K4).
- Done-check is half machine. "none removed" and "failed before
  the fix" (spec:194) are not shown by the check command
  (spec:215). I ran it at f460153: 418 passed, 0 failed; it
  shows neither half. Yet B2 row 6 says it "says yes or no"
  (spec:94), and B4 rule 1 (spec:148) sends it to the cheaper
  builder first.
- Matthew's own asks. His recorded words (DIRECTOR-WORDS-t212u
  .md:6, :10; f460153, after a990738) include "build a localized
  version of this in my local space" and "Tell me what you need
  from me". The spec has no "what we need from you" list. 7.
- Retry evidence. Spec:149 quotes "not infinite reruns". The
  source line starts "Retry wrong outputs with diagnostic
  evidence" (LIB 960d20c, W/0413.assistants/06.01.md:19).
- Addresses. R31 item 8: "back end only". W2 (spec:273) has
  Matthew read the copy, whose header holds the address (spec:89).
  Show him the title.

## Contradictions with rulings

- W6 vs R20. Spec:299: "a different model". R20 (RULINGS:79):
  "a fresh session of the same model counts as a different
  view." The spec narrows a ruling without saying so.
- W2 vs R33 item 2. W2 (spec:272) stores AGENTS.md as face 01.
  RULINGS:162: "On normal pages, faces 01 and 02 usually hold
  only key words." Tension: workflow-loop.003.md:87 allows "an
  agents.md-style face 01" on an N4 page. Say which applies.
- W1 vs R37 item 1: finding 5.

## Contradictions with CORE-AND-TOOLS-SPEC (9b555a2)

- States: finding 4.
- Door: core K8 answer is "First close the direct-write door (OS
  account, refuse-not-cut)" (CORE-AND-TOOLS-SPEC.md:873). The
  example drops the OS account but keeps the name (finding 1).
- No other break found. B3 matches core B1 and B12.

## Code claims checked (HEAD f460153; crates/ same as a990738)

- store.rs:59, :297, :270-284, :744-749, :950-951 and
  identity.rs:3 say what the spec says. True.
- spec:60 "Every page in the kernel already has an MVP pack on
  face 05.02": true for 0051-0057 and 00.00.axioms; door 0000
  has none, as R10 allows.
- workflow-loop.003.md:87, :89, :99, :111-112, :122. True.
- LIB at 960d20c: 06.01.md:11, :19; 01.md:34-35; REPORT.md:5-6,
  :15-16, :24; 0173 return.md:17; 0118 return.md:1, :79-80;
  0408 01.md:19, :24; 0409 01.md:168; 0101 return.md:14, :21-29,
  :34-38. All match.
- FALSE: "16 returns name Grok Builder" (spec:50).
  `git grep -l "Grok Builder" 960d20c` gives 19 return.md files,
  or 25 *return.md in the work book. 16 does not reproduce.
- "No recorded version" of t212u (spec:32): true at a990738,
  stale now. Spec:34 matches the record except spacing.
- Old no-remote premise: NOT carried. Spec:12 and :252 drop it;
  spec:142 names Amalgamour/Workshop, prima/build.

## W1-W6 (t189u form)

W1. Should the work book be a real book, written by the compute?
- Answer: yes, through today's gate from day one. One book per
  build, retired to the shelf when the build is done.
- Why: R37 item 1, one log. R31 item 6: a book is "a working
  journal" (RULINGS:139). Hurt: Matthew, if notes and book differ.
- Axioms: 1 :13 pass; 2 :15 pass; 6 :23 pass; 7 :25 pass.
  Tension on 1: the door is open for every book.
- New option: one work book per build, not one forever.

W2. Does AGENTS.md live in the page or get made fresh per job?
- NOT INDEPENDENT: one side is Tester's research. A fresh view
  must trial W2 (axiom 9, :29). No answer from me.
- On Designer's "both" only: changes what face 01 holds (R33
  item 2); freezes if a system page (R34); axiom 2 tension, which
  Designer marks himself.
- New option (also mine, untried): keep the brief in the face 05
  pack, which workflow-loop.003.md:99 calls "an agents.md-style
  build list". That is "an agents.md in it" without touching 01.

W3. Who may release a work page to a builder?
- Answer: Matthew releases the first few. Then Prima, inside a
  written grant naming the scope and a spending cap.
- Why: a release spends money; spending is Matthew's call.
  Hurt: Matthew, by a surprise bill.
- Axioms: 1 :13 pass; 3 :17 pass with the grant ("A lead is not
  authority"); 6 :23 pass.
- New option: a cap per page (turns or dollars) set by Matthew.

W4. What decides Cursor or Grok Builder for a page?
- Answer: the B4 rule, plus: a check that is part judgment counts
  as judgment; the second try carries the first failure.
- Why: "Retry wrong outputs with diagnostic evidence"
  (06.01.md:19). Hurt: Matthew pays twice for the same miss.
- Axioms: 3 :17 pass; 4 :19 pass; 9 :29 tension (cheaper is
  untried).

W5. Do we record cost per job?
- Answer: yes: time, tries, tokens, dollars. Keep "not reported"
  apart from "zero".
- Why: R37 item 6, "Couldn't look" apart from "isn't there"
  (RULINGS:200). Hurt: Matthew, reading a blank as free.
- Axioms: 7 :25 pass; 9 :29 pass (lets "cheap" be tried).

W6. Does every return get a hostile pass first?
- Answer: yes, by a different view as R20 defines it (a fresh
  session counts). Not only Tester.
- Why: R20 ruled it. One reviewer is a queue. Hurt: every job.
- Axioms: 9 :29 pass; 1 :13 pass.
- New option: the reviewer must not be the page's writer
  (Designer wrote the example's done-check).

## Not trialed here: Tester's own input

From WORK-BOOK-RESEARCH.md (ab152b6, 877bc1e) and
CORE-SPEC-HOSTILE-PASS.md (60fe60b). Not graded here:
- B2 table: `AGENTS.md` name, made fresh from 01 + 05, eight
  sections, size budget, one worktree per job (spec:77-96).
- B2 "link, do not paste" (spec:98).
- B4 price, limits, strong-at rows; option D (spec:141-153);
  Part F price line (spec:308).
- Part D options A-G and Q1/Q2 (spec:241-249).
- W2's "fresh per job" side, and my W2 option.
- Example cards w01-w04 and its "Why" (spec:198-212). I checked
  only that the code lines match, not that the cards are right.
Recommend: another model, or a fresh session, trials these.
Designer's reading of it: quotes at spec:79, :82, :142, :252
match. W2's cite "option A, :160-162" is a stretch: option A
keeps a hash in the hand back and face 09, not a header. "Store
as face 01" changes the research's face 01, "the page's meaning,
in model cards" (877bc1e:116).

## Not checked

- Public builder docs (no web checks this pass).
- Whether either builder obeys the worked example.
- Core spec beyond B1, B6, B12, B15, K4, K8, K9, Q-A.
- LIB W/0101 return.md:11-30 and W/0118 reservation.json.
- CURSOR-BUILD-REVIEW and CODEX review past the cited lines.
- R2-R18 in detail.
