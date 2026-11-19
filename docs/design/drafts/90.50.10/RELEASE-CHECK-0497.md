# Release check: draft pack 90.50.10.0497.05.01, the band's test lab, pass 1 (PACK-0497-05.01.md)

checklist: docs/design/RELEASE-CHECK.md @ c0e5b22 (with its v2 note: H1, A9), plus t425u.
checked: 2026-11-19, 2:00 PM EST, by Designer. Maker's own check, not proof (Axioms.md:29).

| Check | Source file:line | Seen | Result |
|---|---|---|---|
| A1 desk 10+ | t413u.md:7 | 90 | PASS |
| A2 shelf 10+ | t413u.md:7 | 50 | PASS |
| A3 book 10+, not 00 | t413u.md:7 | 10 | PASS |
| A4 page 0100+ | t413u.md:9 | 0497 | PASS |
| A5 band 0400 | t413u.md:9; t423u.md:11 | 0497 in 0400-0499 | PASS |
| A6 door 0400 | t420.md:4 | named in faces 01, 08 | PASS |
| A7 widths | seqAddr.md:14 | 90.50.10.0497 | PASS |
| A8 no override in 0001-0099 | DIRECTOR-RULINGS.md:84 | none | PASS |
| A9 not 99, PP99, 9999 | seqAddr.md:242, :325 | 0497 | PASS |
| H1 lab address | seqAddr.md:243; DIRECTOR-RULINGS.md:71-72; t424.md:16 | 0497, the same slot in every band, below 0498 | TENSION (no file names a lab slot; plan Q9) |
| H1 one lab for the band | t425u.md:3; Axioms.md:15 | one harness, one page | TENSION (plan Q9; files do not settle it) |
| Lab not in band 07NN | workflow-loop.003.md:48, :59 (draft); t413u.md:9; t423u.md:11 | inside 04xx | PASS (the draft does not govern; conflict stated in plan 12.2) |
| Harness moved, not copied | t425u.md:3 | w01: "Move into it, do not copy"; must not: no copy | PASS |
| No new test cases | STAGE-PLAN 12.5 | w03 "Add no other tests"; must not | PASS |
| 0405's job folded in | STAGE-PLAN 12.5 | w02 | PASS |
| Windows | t400u.md:7; tests/wf.rs:4, :820, :841, :954, :959, :1021, :1117 @ 60dd7e25 | w02 gates and names each | PASS |
| Ready for 0404 | t416u.md:7; wf src/cmd.rs:445-459 (only known keys read) | w03; stop if wf refuses the extra line | PASS |
| Links both ways | t422.md:6; Axioms.md:27 | face 08 "trials"; each work page writes "lab" back when made | PASS; TENSION (back-links wait until each page is made) |
| Pack on the page's own 05 | t420.md:6; t223u.md:8 | 0497.05.01 | PASS |
| Grant cites a recorded file | t425u.md:3; t424.md:14 | tests/ | PASS; TENSION (approves the plan and the lab idea, not named paths) |
| Grant covers may touch | wf src/cmd.rs:349 | tests/common/mod.rs, tests/wf.rs inside tests/ | PASS |
| X1, X2 axioms | Axioms.md:5, :9 | 1.7.8,2.9 | PASS |
| X6 why | Axioms.md:19 | t425u.md:3, t400u.md:7, t416u.md:7 | PASS |
| X7 frame | Axioms.md:21 | goal, may touch, must not, stop if, done when | PASS |
| MVP done-when | t423u.md:13 | face 01 pass 1 done when; same in `done when` | PASS |
| t416u line on the return | t416u.md:7; t424.md:10 | `noticed:` line by prompt | PASS |
| Every page gets a trial | DEV-WORK-LAB-PAGES.md:53; workflow-loop.003.md:200 (draft: labs for risky work) | face 01 lists every work page | TENSION (t425u links every page; the drafts trial fewer) |
| H1 habitual choices | t415u.md:5 | tests/common/mod.rs (the usual Rust shared-test layout) | PASS (traced: t425u.md:3 asks for one copy; a module every test file imports with `mod common;` is that one copy. Name is Rust's convention, said so) |
| Files and lines | wf @ 60dd7e25 | tests/wf.rs:4, :10-170, :94, :858 | TENSION (0403 moves them; re-read) |
| X11 hostile pass | Axioms.md:29 | not yet | TENSION |
| Start, hashes | - | TBD | N/A until pack time |

FAILs found and fixed: none found.

Verdict: PASS for review, with tensions (lab slot and shape wait on Q9; grant reads the
plan as approval of paths; back-links wait for each page; every page trialled where the
drafts trial fewer; line numbers move after 0403; no hostile pass).
