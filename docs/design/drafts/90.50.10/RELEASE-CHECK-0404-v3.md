# Release check v3: draft pack 90.50.10.0404.05.01 (PACK-0404-v3.md)

checklist: docs/design/RELEASE-CHECK.md @ c0e5b22 (with its v2 note: H1, A9), plus t425u
and t432. Replaces RELEASE-CHECK-0404-v2.md (b63116d); v1 and v2 stay as history.
checked: 2026-11-19, 2:11 PM EST, by Designer. Maker's own check, not proof (Axioms.md:29).

Unchanged from v2 and still PASS: A1-A9 and H1 page number (90.50.10.0404); goal; X1, X2
(1.7.8,5.9.4); X6; X7; X8; no own test file; no copied harness; tests/wf.rs not touched;
grant src/, templates/ covers may touch; t416u line by prompt; MVP done-when names the
lab trial. Unchanged and still TENSION: grant reads t424 as approval of the plan's paths;
the lab trial runs outside the pack's `checks` line; line numbers move after 0403; 0498
back-link waits; no hostile pass. Unchanged N/A: t416u.md:4 not cited (approves fix plan
steps 1-3 only); start and hashes TBD.

New rows for v3:

| Check | Source file:line | Seen in v3 | Result |
|---|---|---|---|
| Lab is in its own band | t432.md:16 | Lab: 90.50.10.0701, lab band 0700 | PASS |
| Lab address A1-A9 | t413u.md:7, :9; seqAddr.md:241-242 | 0701 on PP01 of band 0700 | PASS |
| Link both ways | t422.md:6; Axioms.md:27 | face 01 and 08 here; step 3 writes "Serves" on 0701 | PASS |
| Not linked by number | seqAddr.md:243; Axioms.md:27 | written links only; 0701 and 0404 share no number | PASS |
| Needs 0701 pass 1 | STAGE-PLAN 13.6 | face 08 needs; start after 0701.05.01 | PASS |
| 0701 is held on 0403 | STAGE-PLAN 13.4 | step 1 waits for both | PASS |
| No 0497 left in live lines | STAGE-PLAN 13.4 | only in "what changed" | PASS |
| H1 lab band number | plan Q11 | 0700 | TENSION (Q11) |
| Wave | STAGE-PLAN 13.7 | wave 2 | PASS |

FAILs found and fixed: none found.

Verdict: PASS for review, with the v2 tensions plus the lab band number (Q11). Not
releasable until 0403 and 0701.05.01 close and the TBD fields are filled.

## Addendum v4 (2026-11-19, 2:14 PM EST, Designer): re-check at c09fa60c

| Check | Source | Result |
|---|---|---|
| src/ cites | cmd.rs:15, :405, :467-482, :484, :515, :371; render.rs:29, :37-51 @ c09fa60c | PASS (corrected) |
| Return strings | tests/wf.rs five strings | PASS (0701 w03 covers all five) |
| HOLD until 0701.05.01 closes | STAGE-PLAN 13.6 | PASS (stated) |
| Lab band | t434.md:6 | PASS; Q11 tension retired |

Verdict: PASS for review, ON HOLD until 0701.05.01 closes.
