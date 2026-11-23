# Proposal: face 05 can be seated

state: draft. No rule file was edited. Nothing built.
made: 2026-11-23, 11:20 AM EST, by Cursor-C (Design).
authority: Matthew, t511, verbatim: "Change the rule so face 05 can be seated."
Asked: how the finished, rerunnable version of a page should be kept, given seqAddr.md:199 says a counted face is never seated.
Record: docs/design/drafts/DIRECTOR-WORDS-t506-t511.md.

## 1. The rule today

The sentence that blocks the seat is seqAddr.md:199, in section 5.7:

"A counted face is never seated. Plain `FF` on a counted face means `FF.00`."

The next line, seqAddr.md:200, says faces 05 and 06 are always counted. So face 05 cannot be seated.

The same ban is written in these places:

| File:line | Text |
|---|---|
| docs/spec/decisions.md:198 | "A counted face is never seated. Plain `FF` on a counted face means `FF.00`. The seated address `DD.SS.BB.PPPP.FF` applies only to faces without counters." |
| docs/spec/review.md:55, item 26 | "A counted face is never seated; plain `FF` on a counted face means `FF.00`. [A4.4]" |
| docs/design/DECISIONS-INDEX.md D53 | "A counted face is never seated, and plain `FF` means `FF.00`." The index cites seqAddr.md:199 and decisions.md:198 |
| docs/design/DECISIONS-LOG.md D53 | Same sentence. The log already says "never seated" was superseded for face 05 by R22, R23, R24, and that notes and the dictionary are the leftover |
| docs/design/DECISIONS-LOG.md D225 | "A counted face (05, 06, dictionary sections) is not seated by R2 while 'a counted face is never seated' stands; R22 asks for a seated 05." |
| docs/design/WHY-GAPS.md:69 and row 29 | Names the clash between decisions.md:198 and R22. Open as kernel QUESTIONS Q41 |
| kernel/QUESTIONS.md Q41 | "R22 asks for a seated face 05 on each page; the kernel law says a counted face is never seated. Which holds?" It cites seqAddr.md:199-201 and decisions.md:198-199 |
| docs/design/DEV-WORK-LAB-PAGES.md:102 and :182 | seqAddr says a counted face is never seated (SA:199). Seating needs that line, and the code, to change first |
| docs/design/QUESTIONS-FOR-DIRECTOR.md:25 | "a task list is never seated (seqAddr.md:199, decisions.md:198)" |
| docs/design/notes-and-dictionary-seating.md:24 | Quotes seqAddr.md:199 and says it is already in tension with a seated 05 |

R22 already asked for the seat (DIRECTOR-RULINGS.md:86-88): "the seated 05 for each page should explain what you learned and become the seated pack of work." R23 (line 91) says the seated 05 is the best version of the pack. R24 (line 95) says we climb 05.CC, then seat 05, and we do not rewrite the older pack. t511 is the rule change those rulings were waiting on. Q41 is answered: the rule changes so face 05 can be seated.

## 2. Where the code refuses it

wf does not seat faces. src/lib.rs on origin/returns has halt (line 36) and no seat command. The refusal is in the kernel crate.

crates/seqaddr-core/src/state.rs:459-460. A write with no counter, on a counted face, is refused:

"face {:02} is counted: it holds counters only, so write a counter `FF.NN` (01-98); it has no door of its own (R9)"

The check is `if counted` at line 459. Faces 05 and 06 are always counted (crates/seqaddr-core/src/face.rs:82-84, `always_counted`).

crates/seqaddr-core/src/resolve.rs:182-183. A plain face with no counter, when the face is counted, returns the derived board of the counters. It does not return a seat. The comment says there is no `FF.00` (R9). seqAddr.md:199 still says plain `FF` means `FF.00`. Those two readings already differ. This proposal does not settle R9. It only says where the seat sits.

crates/seqaddr-core/src/validate.rs:345. When checking an inherited face, a counted face is skipped (`is_counted`), so a seat on face 05 would not be seen.

No other crate file contains the error string "holds counters only". A search of the repo's Rust found that string only at state.rs:460.

## 3. Proposed wording

Replace the ban for face 05 only. Face 06 stays as it is.

Proposed text, for seqAddr.md section 5.7, in place of line 199 for face 05. The old sentence stays in the file as history when this is applied. It is not applied in this draft.

"Face 06 is counted and is never seated. Plain 06 means 06.00, the board of its notes.

Face 05 stays counted for its passes. A pass address is `DD.SS.BB.PPPP.05.NN`, from 05.01 through 05.98. Face 05 also carries a seat. The seat address is `DD.SS.BB.PPPP.05`, the page address plus face 05, with no counter. The board of the passes stays `05.00`. Plain `05` is the seat, not the board.

The seat holds the reviewer-built pass that can be run again, and the lessons learned. It is a copy of that pass. It does not rewrite any 05.NN. The last closed pass stays in the line. Face 01 is updated to name the seat, so a builder can be handed face 01 and run that 05 again."

The same change belongs in decisions.md:198, and in review.md item 26, when those files are next drafted. Not now.

How an address reads, on page 90.50.10.0404:

- 90.50.10.0404.05 is the seat. The rerunnable pack and the lessons.
- 90.50.10.0404.05.03 is pass 3. A counter. History.
- 90.50.10.0404.05.00 is the board of the passes.
- 90.50.10.0404.01 is face 01. It names the seat.

How the seat relates to the last pass: the last pass is the last counter that closed. The seat is built after that, by the reviewer, from that finished work plus the lessons (t509 Q4). The last pass is not deleted and not renamed. The seat records which pass it was built from.

How it relates to face 01: the reviewer updates face 01 so the meaning of the page points at the seat. A later builder is handed face 01 and runs the seat, not an older 05.NN.

## 4. What would have to change later

Rule text, in a later drafting pass, not this one:

- docs/spec/seqAddr.md:199, and the face 05 half of line 200's consequence
- docs/spec/decisions.md:198
- docs/spec/review.md:55, item 26
- docs/design/DECISIONS-INDEX.md D53 and docs/design/DECISIONS-LOG.md D53 and D225, as a new log row, not a rewrite
- kernel/QUESTIONS.md Q41, marked answered by t511

Code, when a page is authorized to build it:

- crates/seqaddr-core/src/state.rs:459-460. A body on face 05 with no counter is stored as the seat. 05.NN still creates counters. Face 06 with no counter is still refused.
- crates/seqaddr-core/src/resolve.rs:182-183. Plain 05 returns the seat when one exists. The board is still reached at 05.00. Plain 06 stays the board.
- crates/seqaddr-core/src/validate.rs:345. A seat on face 05 is visible to the inherited-face check. Face 06 stays skipped.
- crates/seqaddr-core/src/face.rs:82-84. Face 05 stays counted. No change to that fact. The comment should say face 05 is counted and may also be seated.

wf, today: no line to edit. There is no seat command. A later wf page would print the seat next to the passes and would update face 01. That page does not exist. This proposal does not start it.

## 5. Axioms

- 1 Authority (docs/spec/Axioms.md:13). t511 grants the change. This draft does not apply it.
- 2 Fractal (Axioms.md:15). Face 05 is the one difference. Face 06 keeps the old rule. The passes keep their shape.
- 5 Frame (Axioms.md:21). The seat is the rerunnable pack plus the lessons. It is not a new kind of pass.
- 6 Lineage (Axioms.md:23). The seat is a new step. 05.01 and the later passes stay. R24 already says the older pack is not rewritten (DIRECTOR-RULINGS.md:97).
- 8 Connection (Axioms.md:27). Face 01 names the seat. The link is written. Matching the number 05 is not the link.
- 9 Trial (Axioms.md:29). R2 seats a face only after a hostile pass (DIRECTOR-RULINGS.md:7-8). The reviewer's pack is that check. The seat is not written before the check has passed.

No open fork. t511 names face 05. Face 06 stays unseated. Plain 05 is the seat. 05.00 stays the board.
