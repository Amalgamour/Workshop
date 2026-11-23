WORKSHOP PACK 90.50.10.0702.05.03
Printed by wf from templates/pack.txt. Do not edit.

page:        90.50.10.0702 (seq grammar lab: what a .seq file is and how it reads)
prime:       prima
predecessor: 05.02
repo:        work
start:       9c669caecce46cc94622d744e8698ea1e79899da
branch:      returns
return file: .workshop/returns/90.50.10.0702.05.03.md
grant:       labs/0702/ (t452u)
axioms:      1.7.8
outcome:     the grammar report answers Codex's manual check of pass 2, and labs/0702/LESSONS.md is tightened as Codex said
overview:    Builder: Claude (Matthew's PC, D:\Git\claude). Checker: Grok-Check (wf check --as Grok-Check). Pass 05.02 closed failed on Codex's manual check (check entry 18, signoff entry 19, close entry 20). Start is returns 9c669caecce46cc94622d744e8698ea1e79899da. Template 4. Grant is already labs/0702/. Cite the design files on prima/build (same line numbers at 8e96151d and ca649c54 for these cites): docs/spec/seqpage.md, docs/spec/DIRECTOR-RULINGS.md, docs/spec/face00.md, docs/spec/seqAddr.md, docs/design/SEQ-FILE-PLAN.md, crates/seqpage/src/derive.rs, crates/seqpage/src/import.rs. Do not write docs/lessons/ (outside the grant). The lessons file feeds that folder later (t506u). Check commands use the Windows-safe form: no caret, no quotes, and no spaces inside a git grep pattern. The bare ## form is a comment under sh -c (src/git.rs:111), so the pattern is [#][#][[:space:]]N[.].
jobs:
  w01: Define the text production used at lab :231-232 (why-draft-v and stamp-v). Write it from the code that prints those values. Do not leave text undefined.
  w02: Add counters := to the registry (face 00) row at lab :205, for face 00 counter history. derive.rs:247-249 keeps that value when rendering face 00, for losslessness, even though the core does not treat it as legal.
  w03: Narrow the open-conflict table. O2 must separate the v1 ASCII page view from the proposed whole-book format, which explicitly frames binary faces (SEQ-FILE-PLAN.md:315-327). O6 must acknowledge the settled 0700-0799 allocation (seqAddr.md:345-351). O9 is parked by R21 (DIRECTOR-RULINGS.md:82-84); do not treat it as a live conflict.
  w04: Q2 already states R9's general rule. Mark that general rule answered, and carry the R16 dictionary 03.00 exception as open (DIRECTOR-RULINGS.md:65-66, face00.md:470).
  w05: Tighten two implementation claims. Q6's fallback is the first nonblank trimmed note line (derive.rs:137-138). Lab :343 calls Bob's booked body imported; import checks booked bodies when a book is supplied and sends only new blocks as proposals (import.rs:45-51, 64-87). Fix the wording.
  w06: Tighten lessons 3, 4, 6 and 7 as Codex said. Lesson 3: carry the R16 exception. Lesson 4: distinguish current implementation from an open design decision. Lesson 6: cite a dry-run transcript for the actual error, and note that avoiding spaces alone leaves the Windows caret issue. Lesson 7: the builder prompt supports the sequencing rule, but the cited material does not independently establish the reported intake incident. Keep lessons 1, 2, 5 and 8.
may touch:   labs/0702/
must not:    anything outside may touch (the return check refuses it)
checks:      git ls-files --error-unmatch labs/0702/LAB-0702-SEQ-GRAMMAR.md; git ls-files --error-unmatch labs/0702/LESSONS.md; git grep -q -E [#][#][[:space:]]0[.] -- labs/0702/LAB-0702-SEQ-GRAMMAR.md; git grep -q -E [#][#][[:space:]]1[.] -- labs/0702/LAB-0702-SEQ-GRAMMAR.md; git grep -q -E [#][#][[:space:]]2[.] -- labs/0702/LAB-0702-SEQ-GRAMMAR.md; git grep -q -E [#][#][[:space:]]3[.] -- labs/0702/LAB-0702-SEQ-GRAMMAR.md; git grep -q -E [#][#][[:space:]]4[.] -- labs/0702/LAB-0702-SEQ-GRAMMAR.md; git grep -q -E [#][#][[:space:]]5[.] -- labs/0702/LAB-0702-SEQ-GRAMMAR.md; git grep -q -E [#][#][[:space:]]6[.] -- labs/0702/LAB-0702-SEQ-GRAMMAR.md   (one command each, split by ;)
done when:   Done when: the text production used at lab :231-232 is defined, and the registry row at lab :205 includes counters := for face 00 counter history (derive.rs:247-249).
Done when: the open-conflict table is narrowed: O2 separates the v1 ASCII page view from the proposed whole-book format (SEQ-FILE-PLAN.md:315-327); O6 acknowledges the settled 0700-0799 allocation (seqAddr.md:345-351); O9 is parked by R21 (DIRECTOR-RULINGS.md:82-84), not treated as a live conflict.
Done when: Q2 marks R9's general rule answered and carries the R16 dictionary 03.00 exception as open (DIRECTOR-RULINGS.md:65-66, face00.md:470).
Done when: Q6's fallback is the first nonblank trimmed note line (derive.rs:137-138).
Done when: lab :343 no longer calls Bob's booked body imported; import checks booked bodies when a book is supplied and sends only new blocks as proposals (import.rs:45-51, 64-87).
Done when: lessons 3, 4, 6 and 7 are tightened as Codex said: lesson 3 carries the R16 exception; lesson 4 distinguishes current implementation from an open design decision; lesson 6 cites a dry-run transcript for the actual error and notes that avoiding spaces alone leaves the Windows caret issue; lesson 7's intake incident is not independently established by the cited material.
Done when: what pass 2 already met stays true (entry numbers, body checks, added cases, and lessons 1, 2, 5 and 8).
stop if:     another file must change, including docs/lessons/ or src/. A check command has a caret, quotes, or a space inside a git grep pattern. A real open conflict is marked answered. A rule above reads two ways.
pins (Prime read these before drafting; checked again at release):
  face 04:        none
  face 06:        entry 22, hash 6d4b6d42475b
  last closed 05: 05.02 closed at entry 20
sources:
  face 01:        v3 entry 21 hash 4c8a9af16551
  docs/AXIOMS.md (in the kit folder, the folder with src/ and AGENTS.md; not beside pages/): hash 552014964d27
  docs/DESIGN.md (in the kit folder, same as AXIOMS.md; not beside pages/): hash 46be27fa22a7
