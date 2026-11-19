# Release check: draft pack 90.50.10.0404.05.01 (PACK-0404.md)

checklist: docs/design/RELEASE-CHECK.md @ c0e5b22 (with the v2 note: H1, A9)
checked: 2026-11-19, 2:10 PM EST, by Designer, against the draft in this folder.
limit: this is the maker's own check (Axioms.md:29). It is not proof; the checker and a
hostile pass still come before release. Fields marked TBD are checked again at pack time.

## Hard address checks

| Check | Source file:line | Seen | Result |
|---|---|---|---|
| A1 desk 10+ | t413u.md:7; seqAddr.md:30 | 90 | PASS |
| A2 shelf 10+ | t413u.md:7 | 50 | PASS |
| A3 book 10+, not 00 | t413u.md:7; seqAddr.md:29 | 10 | PASS |
| A4 page 0100+ | t413u.md:9 | 0404 | PASS |
| A5 band 0400 | t413u.md:9; seqAddr.md:323 | 0404 in 0400-0499 | PASS |
| A6 door 0400, jobs from 0401 | t420.md:4; seqAddr.md:241 | door 0400 named in face 01 and 08 | PASS |
| A7 widths | seqAddr.md:14 | 90.50.10.0404 | PASS |
| A8 no override in 0001-0099 | DIRECTOR-RULINGS.md:84 | none | PASS |
| A9 not 99, PP99, 9999 | seqAddr.md:242, :325 | 0404 | PASS |
| H1 page number | seqAddr.md:323; STAGE-PLAN 11.3 | next free after 0403, in plan order | PASS |

## The pack against the files

| Check | Source file:line | Seen in the draft | Result |
|---|---|---|---|
| Goal | t416u.md:7; STAGE-PLAN 11.3 | face 01 Goal; outcome | PASS |
| MVP done-when | t423u.md:13; STAGE-PLAN 11.3 | face 01 Done when, same text in `done when` | PASS |
| X1 axioms parse | Axioms.md:5 | 1.7.8,5.9.4 (two pieces, each dot-ordered) | PASS |
| X2 cold set before a write | Axioms.md:9 | 1.7.8 is the first piece | PASS |
| X6 every rule has its why | Axioms.md:19 | overview quotes t416u.md:7, t424.md:10, t381u.md:8 | PASS |
| X7 frame | Axioms.md:21 | goal, why, may touch, stop if, done when | PASS |
| X8 nothing earlier rewritten | Axioms.md:23; t381u.md:8 | templates 1-3 unchanged; old packs print the same (w01, stop if) | PASS |
| X9 unknowns marked | Axioms.md:25 | start, hashes, entries: TBD, said why | PASS |
| X10 links both ways | Axioms.md:27; t422.md:6 | face 08: door, needed by 0498 (back-link written when 0498 is made) | TENSION (0498 not made yet, so the back-link waits) |
| X11 hostile pass | Axioms.md:29 | not yet | TENSION (before release) |
| Pack on the page's own 05 | t223u.md:8; t420.md:6 | 90.50.10.0404.05.01 | PASS |
| May touch includes own test file | t424.md:8 | tests/page_0404.rs | PASS |
| Own test file only for new tests | t424.md:8; t422.md:7 | tests/wf.rs: two strings changed, no new tests | TENSION (tests/wf.rs is still a shared changed file; it keeps 0405 out of wave 1, plan 11.8) |
| New test file builds on Windows | t400u.md:7; tests/wf.rs:4 (known gap) | w03 forbids std::os::unix and true/grep/test | PASS |
| Return order | t226u.md:11 | design review line goes before not done; unprompted, overflow stay last | PASS |
| t416u line required on the return | t416u.md:7; t424.md:10 | wf checks it from template 4 on; this pass (packed on 3) states it in `noticed:` by prompt | PASS |
| Grant cites a recorded file | t424.md:14 (plan replaces stage 1); t416u.md:7 (the rule) | grant line | PASS; TENSION: t424 approves the plan, it does not name paths. Matthew still runs the grant (t424.md:6) |
| Grant not t413u | relay | t413u not cited for the grant | PASS |
| Relay asked for t416u.md:4 | t416u.md:4 "1-3 is good, remove the old WF pages, or mark them as retired." | not cited | N/A: :4 approves fix plan steps 1-3 (retire, repack, address guard), not this page; citing it would claim more authority than it gives (Axioms.md:13) |
| Grant covers may touch | wf src/cmd.rs:349 (pack refuses may touch outside the grant); grant src/, tests/, templates/ | all five paths inside | PASS |
| Template version bump | render.rs:29, :37-51 @ 60dd7e25 | "4" added, "1"-"3" kept | PASS |
| Files and lines | wf source @ 60dd7e25 | cmd.rs:15, :383, :445, :462, :493; render.rs:29, :37-51; tests/wf.rs:94, :858 | TENSION (move when 0403 lands; re-read at pack time, step 5) |
| H1 habitual choices | t415u.md:5 | test file name tests/page_0404.rs; line placed after proof; refusal wording | PASS (name traced to t424.md:8 one file per page; placement traced to t226u.md:11; wording names t416u) |
| Start commit | 0403 PACK.md:8 shape | TBD | N/A until 0403 closes |
| Base commit verified | RELEASE-CHECK-90.50.10.md (0403 start check) | TBD | N/A until pack time |

## FAILs found and fixed before this report

- First draft cited only `5.9.4`: no cold set before a write (X2, Axioms.md:9). Fixed:
  `1.7.8,5.9.4`.
- First draft cited the refusal record at src/cmd.rs:497-500; the line is :493. Fixed.

Verdict: PASS for review, with tensions (back-link waits for 0498, tests/wf.rs still
shared, grant reads t424 as approval of the plan's paths, line numbers move after 0403,
no hostile pass yet). Not releasable until 0403 closes and the TBD fields are filled.

## Version note (2026-11-19, 2:01 PM EST, Designer): superseded for t425u

Superseded by RELEASE-CHECK-0404-v2.md in this folder (t425u: each page links to the band's test lab,
0497, and copies no test code; STAGE-PLAN-90.50.10.md v4, 5389d13). This file stays as
history (Axioms.md:23). Its "made" or "checked" time is later than its commit (699fa07);
it was written about 1:50 PM EST.

## Version note (2026-11-19, 2:11 PM EST, Designer): superseded for t432

Superseded by RELEASE-CHECK-0404-v3.md in this folder (t432u: labs in their own band; the lab is
90.50.10.0701, door 0700; STAGE-PLAN-90.50.10.md v5, f74397f). This file stays as history
(Axioms.md:23).
