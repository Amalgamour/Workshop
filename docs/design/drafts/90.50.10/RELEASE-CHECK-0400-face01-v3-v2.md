# Release check v2: draft face 01 v3 for the door 90.50.10.0400 (0400-face01-v3-v2.md)

checklist: docs/design/RELEASE-CHECK.md @ c0e5b22, plus t425u.
checked: 2026-11-19, 2:00 PM EST, by Designer. Replaces RELEASE-CHECK-0400-face01-v3.md
(699fa07), which stays as history. Maker's own check, not proof (Axioms.md:29).

Every row of the v1 check still holds (all PASS but two TENSIONs: grant placeholder,
"planned" is a plain word). New rows:

| Check | Source file:line | Seen in v2 | Result |
|---|---|---|---|
| Lab listed | t425u.md:3; STAGE-PLAN 12.3 | 0497 line | PASS |
| Every work page needs the lab | t425u.md:3; STAGE-PLAN 12.6 | "Needs 0497" on 0404, 0406-0409, 0411; 0498 needs 0497 | PASS |
| 0405 not used, why | STAGE-PLAN 12.5 | 0405 line | PASS |
| A9 for 0497 | seqAddr.md:242 | 0497 is not 0499 | PASS |
| Plan version named | STAGE-PLAN v4 (5389d13) | "(v4)" | PASS |
| Lab slot | plan Q9 | 0497 | TENSION (Q9 open) |

FAILs found and fixed: the first v2 text still said "STAGE-PLAN-90.50.10.md (v3)"; fixed
to v4.

Verdict: PASS for review, with tensions (grant placeholder; plain-word states; lab slot
waits on Q9).

## Version note (2026-11-19, 2:11 PM EST, Designer): superseded for t432

Superseded by RELEASE-CHECK-0400-face01-v3-v3.md in this folder (t432u: labs in their own band; the lab is
90.50.10.0701, door 0700; STAGE-PLAN-90.50.10.md v5, f74397f). This file stays as history
(Axioms.md:23).
