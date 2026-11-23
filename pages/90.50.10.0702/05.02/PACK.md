WORKSHOP PACK 90.50.10.0702.05.02
Printed by wf from templates/pack.txt. Do not edit.

page:        90.50.10.0702 (seq grammar lab: what a .seq file is and how it reads)
prime:       prima
predecessor: 05.01
repo:        work
start:       86770ec221da36d3edaed3d1399459b555a86fa3
branch:      returns
return file: .workshop/returns/90.50.10.0702.05.02.md
grant:       labs/0702/ (t452u)
axioms:      1.7.8
outcome:     the grammar report answers Codex's cross-check, and labs/0702/LESSONS.md lists the lessons
overview:    Builder: Claude. Checker: Codex. Pass 05.01 closed failed on Codex's cross-check (signoff entry 10). Start is returns 86770ec221da36d3edaed3d1399459b555a86fa3. Template 4. Grant is already labs/0702/. Cite the design files on prima/build: docs/spec/seqpage.md, DIRECTOR-RULINGS.md, crates/seqpage/src/parse.rs, crates/seqaddr-core/src/state.rs, crates/seqpage/src/derive.rs, and docs/spec/examples/real/10.11.21.1001.bob.seq. Do not write docs/lessons/ (outside the grant). The lessons file feeds that folder later (t506u). Check commands have no spaces inside a pattern.
jobs:
  w01: Restate the entry-number rule at lab:176 as one booked block and one matching history entry, in book order, with references allowed (seqpage.md:135, :199-201).
  w02: Fix lab:183 so it does not claim body text is never checked. seqpage.md:169 says a prefixed body cannot be mistaken for structure. seqpage.md:186 and crates/seqpage/src/parse.rs:366-370 do check the body's cards.
  w03: Write a value grammar for derived values, including lineage, source, faces and counters. source := uses a full book address.
  w04: In section 5, split superseded text from real open conflicts. Superseded: K2/R26, K4/R9, K5/R10, K7/R28, K9/R35, K10, K11 stale. Do not resolve a conflict that is still open.
  w05: Mark Q2, Q4, Q5, Q6 and Q7 answered, with the ruling or code cite (DIRECTOR-RULINGS.md:37-41, :113-115; state.rs:607-631; derive.rs:119-141, :204-206). Keep only what truly stays open.
  w06: Add coverage for escaped keys (seqpage.md:156), decoded ASCII checks (seqpage.md:44), and the stamp-versus-replay disagreement in examples/real/10.11.21.1001.bob.seq:85-88.
  w07: Write labs/0702/LESSONS.md. A short list of lessons so far: what went wrong, why, and what to do next time. Each item cites a file:line or a commit (t506u).
may touch:   labs/0702/
must not:    anything outside may touch (the return check refuses it)
checks:      git ls-files --error-unmatch labs/0702/LAB-0702-SEQ-GRAMMAR.md; git ls-files --error-unmatch labs/0702/LESSONS.md; git grep -q -E "^##[[:space:]]0[.]" -- labs/0702/LAB-0702-SEQ-GRAMMAR.md; git grep -q -E "^##[[:space:]]1[.]" -- labs/0702/LAB-0702-SEQ-GRAMMAR.md; git grep -q -E "^##[[:space:]]2[.]" -- labs/0702/LAB-0702-SEQ-GRAMMAR.md; git grep -q -E "^##[[:space:]]3[.]" -- labs/0702/LAB-0702-SEQ-GRAMMAR.md; git grep -q -E "^##[[:space:]]4[.]" -- labs/0702/LAB-0702-SEQ-GRAMMAR.md; git grep -q -E "^##[[:space:]]5[.]" -- labs/0702/LAB-0702-SEQ-GRAMMAR.md; git grep -q -E "^##[[:space:]]6[.]" -- labs/0702/LAB-0702-SEQ-GRAMMAR.md   (one command each, split by ;)
done when:   Done when: the entry-number rule (lab:176) is restated as one booked block and one matching history entry, in book order, with references allowed (seqpage.md:135, :199-201).
Done when: lab:183 no longer claims body text is never checked (seqpage.md:169, :186; crates/seqpage/src/parse.rs:366-370).
Done when: derived values have a written value grammar, and source := uses full book addresses.
Done when: section 5 splits superseded text (K2/R26, K4/R9, K5/R10, K7/R28, K9/R35, K10, K11 stale) from real open conflicts.
Done when: Q2, Q4, Q5, Q6 and Q7 are marked answered with the ruling or code cite (DIRECTOR-RULINGS.md:37-41, :113-115; state.rs:607-631; derive.rs:119-141, :204-206), and only what truly stays open remains open.
Done when: the report covers escaped keys (seqpage.md:156), decoded ASCII checks (seqpage.md:44), and the stamp-versus-replay disagreement in examples/real/10.11.21.1001.bob.seq:85-88.
Done when: labs/0702/LESSONS.md is a short list of lessons learned so far (what went wrong, why, what to do next time), each with a file:line or commit cite (t506u). Codex checks it in the cross-check. It feeds docs/lessons/ later.
stop if:     another file must change, including docs/lessons/ or src/. A check command has a space inside a quoted pattern. A real open conflict is marked answered. A rule above reads two ways.
pins (Prime read these before drafting; checked again at release):
  face 04:        none
  face 06:        entry 12, hash 1144e952d5de
  last closed 05: 05.01 closed at entry 11
sources:
  face 01:        v2 entry 13 hash 5168f283dad8
  docs/AXIOMS.md (in the kit folder, the folder with src/ and AGENTS.md; not beside pages/): hash 552014964d27
  docs/DESIGN.md (in the kit folder, same as AXIOMS.md; not beside pages/): hash 46be27fa22a7
