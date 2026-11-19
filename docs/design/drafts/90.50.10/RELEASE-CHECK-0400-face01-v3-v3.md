# Release check v3: draft face 01 v3 for the door 90.50.10.0400 (0400-face01-v3-v3.md)

checklist: docs/design/RELEASE-CHECK.md @ c0e5b22, plus t425u and t432.
checked: 2026-11-19, 2:11 PM EST, by Designer. Replaces RELEASE-CHECK-0400-face01-v3-v2.md
(b63116d); v1 and v2 stay as history. Maker's own check, not proof (Axioms.md:29).

Every v1 and v2 row still holds (PASS, with TENSIONs: grant placeholder; plain-word
states). Changed and new rows:

| Check | Source file:line | Seen in v3 | Result |
|---|---|---|---|
| Lab named in its own band | t432.md:16 | "How it runs" names door 0700 and lab 0701 | PASS |
| Every work page needs the lab | STAGE-PLAN 13.6 | "Needs lab 0701" on 0404, 0406-0409, 0411, 0412; 0498 | PASS |
| 0403 needed by the lab | STAGE-PLAN 13.4, 13.6 | 0403 line | PASS |
| 0412 listed | t432.md:7; STAGE-PLAN 13.5 | 0412 line | PASS |
| 0497 not used, why | STAGE-PLAN 13.4 | 0497 line | PASS |
| 0403 builder | t432.md:13 | "(Cursor-1)" | PASS |
| Plan version | STAGE-PLAN v5 (f74397f) | "(v5)" | PASS |
| A9 no work at 0499 | seqAddr.md:242 | 0498 last | PASS |
| H1 lab band | plan Q11 | 0700 | TENSION (Q11) |

FAILs found and fixed: none found.

Verdict: PASS for review, with tensions (grant placeholder; plain-word states; lab band
waits on Q11).
