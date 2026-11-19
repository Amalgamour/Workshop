# Release check: draft face 01 v1 for the lab band door 90.50.10.0700 (0700-face01-v1.md)

checklist: docs/design/RELEASE-CHECK.md @ c0e5b22, plus t432.
checked: 2026-11-19, 2:10 PM EST, by Designer. Maker's own check, not proof (Axioms.md:29).

| Check | Source file:line | Seen | Result |
|---|---|---|---|
| A1-A3 | t413u.md:7 | 90.50.10 | PASS |
| A4 page 0100+ | t413u.md:9 | 0700 | PASS |
| A6 door at PP00, no work | t420.md:4; seqAddr.md section 10 rule 4 | "No work is done on this page and it drafts no passes" | PASS |
| A9 0799 not a lab | seqAddr.md:242 | "0799 is the band's continuation, not a lab" | PASS |
| Making a PP00 page under 0403's guard | 0403 PACK.md:16 (w01 refuses NN00), :17 (w02 --system --system-ref) | note 1 | PASS; TENSION (a door is made as a system page; no rule names doors as system pages) |
| Honest that it is hand-written | t414u; 0400 v2 card 01.md:5 | "Temporary ... replaced when page 90.50.10.0407 closes passed" | PASS |
| The log governs the card | Axioms.md:27 | "the lab's log is right" | PASS |
| t432 labs in their own band | t432.md:16 | first line quotes it | PASS |
| t432 reusable | t432.md:16 | "Labs are reusable by every stage" | PASS |
| Links both ways, not numbers | Axioms.md:27; seqAddr.md:243 | "How a page uses a lab" | PASS |
| When a new lab is justified | Axioms.md:15 ("do not reinvent") | "Before a new lab" | PASS |
| Lists labs with status | STAGE-PLAN 13.4 | 0701 planned, serves list, hold | PASS |
| Plain words, ASCII | DIRECTOR-RULINGS.md:16 | checked with grep | PASS |
| H1 band number | plan Q11 | 0700 | TENSION (Q11) |
| Grant | 0400 00.md (grant docs/, a placeholder) | note 1 | TENSION (same as 0400) |

FAILs found and fixed: none found.

Verdict: PASS for review, with tensions (band number waits on Q11; a door made with
--system; grant placeholder).

## Addendum v4 (2026-11-19, 2:14 PM EST, Designer): re-check at c09fa60c

| Check | Source | Result |
|---|---|---|
| Guard refuses 0700 without --system | src/addr.rs:102, :177-178 @ c09fa60c | PASS (note 1 holds) |
| --system needs --system-ref | src/cmd.rs:166-177, :184-187 | PASS |
| Ref is only text-checked | src/cmd.rs:174 | TENSION (t432u is not checked to exist) |
| Pass 1 line | 0403 closed | changed in the final text |
| Lab band answered | t434.md:6 "Yes, the lab band is 0700-0799" | PASS; Q11 tension retired |

Verdict: PASS for review. Tensions: door made with --system and a text-only ref; grant
placeholder.
