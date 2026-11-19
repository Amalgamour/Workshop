# Release check v2: draft pack 90.50.10.0404.05.01 (PACK-0404-v2.md)

checklist: docs/design/RELEASE-CHECK.md @ c0e5b22 (with its v2 note: H1, A9), plus t425u.
checked: 2026-11-19, 1:59 PM EST, by Designer. Replaces RELEASE-CHECK-0404.md (699fa07),
which stays as history. Maker's own check, not proof (Axioms.md:29).

Address checks A1-A9 and H1 page number: unchanged from RELEASE-CHECK-0404.md, all PASS
(90.50.10.0404).

| Check | Source file:line | Seen in v2 | Result |
|---|---|---|---|
| Page links its lab | t425u.md:3 | face 01 "Lab:" line; face 08 "lab:"; overview | PASS |
| Back-link on the lab | t422.md:6; Axioms.md:27 | step 3 writes it on 0497 faces 01 and 08 | PASS |
| No own test file | t425u.md:3 (corrects t424.md:8) | may touch has no tests/ path | PASS |
| No copied harness | t425u.md:3 | must not: "no copy of test harness code into src" | PASS |
| Unit tests in src | STAGE-PLAN 12.5 | w02 tests in cmd.rs's own test module | PASS (code's own unit tests, no harness) |
| tests/wf.rs not touched | STAGE-PLAN 12.7 | the two strings moved to 0497.05.01 w03 | PASS |
| Needs 0497 pass 1 | STAGE-PLAN 12.6 | face 08 needs; start after 0497.05.01 | PASS |
| Grant narrowed | wf src/cmd.rs:349 | src/, templates/ covers all three paths | PASS |
| Grant cites a recorded file | t424.md:14; t416u.md:7 | grant line | PASS; TENSION: t424 approves the plan, not named paths |
| Relay's t416u.md:4 | t416u.md:4 | not cited | N/A: :4 approves fix plan steps 1-3 only (Axioms.md:13) |
| X1, X2 axioms | Axioms.md:5, :9 | 1.7.8,5.9.4 | PASS |
| X6 why | Axioms.md:19 | t416u.md:7, t424.md:10, t425u.md:3, t381u.md:8 quoted | PASS |
| X7 frame | Axioms.md:21 | goal, may touch, stop if, done when | PASS |
| X8 old packs unchanged | Axioms.md:23; t381u.md:8 | templates 1-3 kept | PASS |
| t416u line on the return | t416u.md:7; t424.md:10 | `noticed:` line by prompt for this pass | PASS |
| MVP done-when names the lab trial | t423u.md:13; t425u.md:3 | done when | PASS |
| Checks the builder can run | wf `checks` runs at check time | cargo test --lib; cargo test --test wf | PASS; TENSION: lab_0404 is run by the checker after the lab writes it, not by this pack's `checks` line (the file does not exist at pack time) |
| H1 habitual choices | t415u.md:5 | lab file name tests/lab_0404.rs; refusal wording | PASS (name traced to STAGE-PLAN 12.3, wording names t416u) |
| Files and lines | wf @ 60dd7e25 | cmd.rs:15, :383, :445, :462, :493; render.rs:29, :37-51 | TENSION (move after 0403; re-read at pack time) |
| X10 back-link to 0498 | Axioms.md:27 | waits until 0498 is made | TENSION |
| X11 hostile pass | Axioms.md:29 | not yet | TENSION |
| Start, hashes | - | TBD | N/A until pack time |

FAILs found and fixed: none in v2. (v1's two fixes stay: cold set added; cite :493.)
Also noted: v1's "made" and "checked" times were later than its commit; corrected in the
v2 headers.

Verdict: PASS for review, with tensions (grant reads t424 as approval of the plan's
paths; the lab trial is outside the pack's own checks line; line numbers move after 0403;
0498 back-link waits; no hostile pass). Not releasable until 0403 and 0497.05.01 close.
