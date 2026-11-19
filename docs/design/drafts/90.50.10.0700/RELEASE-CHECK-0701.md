# Release check: draft pack 90.50.10.0701.05.01, wf loop lab, pass 1 (PACK-0701-05.01.md)

checklist: docs/design/RELEASE-CHECK.md @ c0e5b22 (with its v2 note: H1, A9), plus t425u
and t432. Replaces RELEASE-CHECK-0497.md (b63116d), which stays as history.
checked: 2026-11-19, 2:10 PM EST, by Designer. Maker's own check, not proof (Axioms.md:29).

| Check | Source file:line | Seen | Result |
|---|---|---|---|
| A1 desk 10+ | t413u.md:7 | 90 | PASS |
| A2 shelf 10+ | t413u.md:7 | 50 | PASS |
| A3 book 10+, not 00 | t413u.md:7 | 10 | PASS |
| A4 page 0100+ | t413u.md:9 | 0701 | PASS |
| A5 band | t413u.md:9 ("for this"); t432.md:16 ("its own band") | lab band 0700-0799 | PASS (t432u asks for a separate band; plan Q11) |
| A6 door at PP00, labs from PP01 | t420.md:4; seqAddr.md:241 | door 0700, lab 0701 | PASS |
| A7 widths | seqAddr.md:14 | 90.50.10.0701 | PASS |
| A8 no override in 0001-0099 | DIRECTOR-RULINGS.md:84 | none | PASS |
| A9 not 99, PP99, 9999 | seqAddr.md:242, :325 | 0701 | PASS |
| H1 lab band number | workflow-loop.003.md:48 (draft); WORK-BOOK-CONCEPT.md:71; t245u.md:5 | 0700 | TENSION (draft map; plan Q11) |
| H1 first lab slot | seqAddr.md section 10 rule 4 (jobs on PP01-PP98) | 0701, first job slot | PASS |
| H1 lab title by subject | t432.md:16 (reusable) | "wf loop lab" | PASS |
| HOLD on 0403 | t422.md:7; 0403 PACK.md:19 (tests/wf.rs); t381u.md:8 | state line, step 1, face 08 needs | PASS |
| t432 lab in its own band | t432.md:16 | yes | PASS |
| t432 reusable | t432.md:16 | face 01: "later stages' pages are added the same way" | PASS |
| Harness moved, not copied | t425u.md:3 | w01, must not | PASS |
| No new test cases | STAGE-PLAN 12.5, 13.5 | w03, must not | PASS |
| Windows | t400u.md:7; tests/wf.rs:4, :820, :841, :954, :959, :1021, :1117 @ 60dd7e25 | w02 | PASS |
| Ready for 0404 | t416u.md:7; src/cmd.rs:445-459 | w03; stop if | PASS |
| Links both ways, not by number | t422.md:6; Axioms.md:27; seqAddr.md:243 | face 08 "serves"; each page writes "lab: 90.50.10.0701" back | PASS; TENSION (back-links wait until each page is made) |
| Pack on the page's own 05 | t420.md:6 | 0701.05.01 | PASS |
| Grant cites a recorded file | t432.md:16; t425u.md:3; t424.md:14 | tests/ | PASS; TENSION (approves the lab, not named paths) |
| Grant covers may touch | wf src/cmd.rs:349 | both paths under tests/ | PASS |
| X1, X2 axioms | Axioms.md:5, :9 | 1.7.8,2.9 | PASS |
| X6 why | Axioms.md:19 | t432.md:16, t425u.md:3, t400u.md:7 quoted | PASS |
| X7 frame | Axioms.md:21 | goal, may touch, must not, stop if, done when | PASS |
| MVP done-when | t423u.md:13 | pass 1 done when, and per trial | PASS |
| t416u line on the return | t416u.md:7; t424.md:10 | `noticed:` line by prompt | PASS |
| Every page gets a trial | DEV-WORK-LAB-PAGES.md:53; workflow-loop.003.md:200 (drafts) | serves every stage 1 page | TENSION (drafts trial fewer) |
| H1 tests/common/mod.rs | t415u.md:5 | Rust's shared-test layout | PASS (traced to t425u.md:3: one copy, imported) |
| Files and lines | wf @ 60dd7e25 | tests/wf.rs:4, :10-170, :94, :858 | TENSION (0403 moves them) |
| X11 hostile pass | Axioms.md:29 | not yet | TENSION |
| Start, hashes | - | TBD | N/A until pack time |

FAILs found and fixed: none found.

Verdict: PASS for review, HOLD for release until 0403 closes. Tensions: lab band from a
draft map (Q11); grant reads approval of the lab as approval of paths; back-links wait;
every page trialled where drafts trial fewer; line numbers move after 0403; no hostile
pass.
