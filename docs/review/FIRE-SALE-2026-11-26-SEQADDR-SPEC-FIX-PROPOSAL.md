# Fire sale: seqAddr.md fix proposal for H1-H6

Prima fire-sale worker, Thu Nov 26 2026, 12:52 AM EST. Draft only. **`docs/spec/seqAddr.md` was not edited.**

Source of H1-H6: job 13 in `docs/review/FIRE-SALE-2026-11-26-PROTOTYPES.md` (scratch commit `07cd904`, tests/hostile.rs, 40 of 40 pass).
Spec text quoted from `docs/spec/seqAddr.md` on build (last changed 46aac4d, Nov 23). Line numbers are that file.

## When this may go in

- 0418.05.01 is packed and cites `seqAddr.md:199-204` (PENDING-RULES.md:9). By t381u, seqAddr.md does not change while that pass is open. So these edits wait until 0418.05.01 is closed or withdrawn, or Matthew says they may go in now.
- H3 needs a ruling first (question below). H1, H2 (except the 05 sentence), H4, H5 and H6 only bring the text up to rulings already given.

## Rulings used

- **R9** (DIRECTOR-RULINGS.md:37): "Faces do not have sentinels. Only pages, books, shelves and desks." Read (:38): no `FF.00` and no `FF.99`; counters run 01-98; sentinels only on desk, shelf, book and page axes.
- **R10** (:40-41): face 00 is the page's registry, not a sentinel.
- **t511 / t512** (SEATED-05-PROPOSAL.md:5; DIRECTOR-WORDS-t512-seated05-approval.md): "Change the rule so face 05 can be seated." Approved.
- **A4.4** as the code applies it: counters live only on counted faces (05, 06 and `Policy.extra_counted`, today `0012.03`), state.rs:417-420.
- **What follows counter 98** is still held `7` (CONFLICTS.md:148, D1). It is not R16. R16 is the dictionary `03.00` door (DIRECTOR-RULINGS.md:65, Q29).

Correction to the prototypes doc: H4 there says "R16 (overflow) is still held". The held item is D1 "what follows counter 98", not R16. The prototypes doc was not changed; this note is the fix.

## H1. 1.4 table, line 53 (Medium)

Current:
```
| `FF.00` | a counted face's board |
```
Proposed: delete the row. Add under the table:
```
Faces have no sentinels (R9): there is no `FF.00`. A counted face's list of counters is derived from the log; it is not an address. Face `00` is the page's registry (R10), not a sentinel.
```

## H2. 5.7, lines 197-200 and the example, lines 208-214 (Medium)

Current (197-200):
```
- A face is counted if and only if `FF.00` exists. `FF.00` is the board: every counter and its current tail.
- A counter without a board is invalid.
- A counted face is never seated. Plain `FF` on a counted face means `FF.00`. (History; t511 and t512 change this for face 05.)
Face 06 is counted and is never seated. Plain 06 means 06.00, the board of its notes.
```
Proposed:
```
- A face is counted when the kernel says so: faces 05 and 06 always, and others only where a page type names them (for example the dictionary's 03). It is not shown by an address: there is no `FF.00` (R9).
- A counter on a face that is not counted is invalid.
- The board of a counted face is the list of its counters and their current tails. It is derived from the log and has no address of its own (R9; resolve.rs:182).
- A counted face is never seated, except face 05 (t511, t512).
Face 06 is counted and is never seated. Plain 06 reads the board of its notes.
```
Current example (208-214), first line:
```
1523.05.00   board
```
Proposed:
```
1523.05      board (derived; no address of its own)
```
The `1523.05` line depends on H3. If H3 picks option B or D, the example changes with it.

## H3. 5.7, line 202: the 05 board once plain 05 is the seat (High, blocks 0418) — needs a ruling

Current (202):
```
Face 05 stays counted for its passes. A pass address is `DD.SS.BB.PPPP.05.NN`, from 05.01 through 05.98. Face 05 also carries a seat. The seat address is `DD.SS.BB.PPPP.05`, the page address plus face 05, with no counter. The board of the passes stays `05.00`. Plain `05` is the seat, not the board.
```
The problem: "The board of the passes stays `05.00`" can't be written. `05.00` is refused at parse (R9; addr.rs:835-837). Today plain `05` reads the derived board (resolve.rs:182-188). Once plain `05` is the seat (t511), the board of the passes has no address at all. 0418 w01 and face 01 copy the `05.00` sentence (FINAL-0418-face01.txt:4; FINAL-PACK-0418-05.01.txt:7), so a builder would be told to build something the parser refuses.

### Question for Matthew or Prima: where is the 05 board read once plain 05 is the seat?

**Question.** After t511, plain `DD.SS.BB.PPPP.05` is the seat. R9 says `05.00` does not exist. How is the list of a page's passes reached?

**Why it matters.** 0418.05.01 can't be released with the `05.00` sentence (P1, H3). The 0418 test file (scratch fd453dd) stays red on the seat case until this is set. The front design (UI-1 and the board survey) also reads the pass list.

**Options.**
- **A (default): the board is derived and has no address.** Plain `05` is the seat. The pass list is what `wf board` and the compute show, built from the log, as every counted face's board already is (R9; resolve.rs:182; derived lists, decisions.md:301). Proposed line 202 ending: "The board of the passes is derived from the log and has no address of its own (R9). Plain `05` is the seat." This follows the design: no new grammar, no exception to R9.
- B: plain `05` reads the board until a seat exists, then the seat. One address means two things over time, so a reader can't tell which without looking.
- C: give the board a tail word, for example `05.board`. New grammar (seqAddr 8) and a new tail; it needs its own ruling.
- D: make `05.00` an exception to R9 for face 05 only, as R16 asks for `03.00`. It reopens R9 and joins Q29.

**What happens if no answer.** 0418 stays held. Nothing else is blocked: seqaddr-core already refuses `05.00`, and the board still prints from the log.

## H4. 7, line 259 and 7.1, line 262 (Medium)

Current (259):
```
- Missing is a valid state: no `FF.00` means not counted, no `FF.99`, `PP99` or `9999` means no continuation. [A4.6]
```
Proposed:
```
- Missing is a valid state: no `PP99` or `9999` means no continuation. [A4.6] Faces have no `FF.00` or `FF.99` (R9).
```
Current (262):
```
- **Counters:** once `FF.98` exists, `FF.99` points to the same face on the next free page in the same band. Counting restarts at `01`. Old counters never move.
```
Proposed:
```
- **Counters:** counters run 01-98 (R9). There is no `FF.99`. What follows `FF.98` is held `7` (CONFLICTS.md D1). Until it is ruled, a 99th counter can't be written.
```

## H5. 8 grammar, line 282, and rules, lines 293-294 (Medium)

Current (282):
```
counter    = 2DIGIT                       ; 00 board, 01-98, 99 continuation
```
Proposed:
```
counter    = 2DIGIT                       ; 01-98 only (R9)
```
Current (293-294):
```
- A counter requires its face's `00` board.
- Counter `00` is the board itself; write it as `FF.00`.
```
Proposed:
```
- A counter is legal only on a counted face (A4.4; 5.7).
- Counters `00` and `99` do not exist (R9).
```

## H6. 1.2 table, lines 26-31 (Low)

Current (26, 30):
```
### 1.2 Reserved values on every axis
| `01-09` / `0001-0099` | reserved |
```
Proposed:
```
### 1.2 Reserved values on the desk, shelf, book and page axes
```
and add under the table:
```
Faces and counters have no reserved values (R9). Faces are read as in 5.1; counters run 01-98.
```
Note: the `00` row still says "owner"; R1 says to call it the door. Not in H1-H6, left for Prima.

## Not touched

seqAddr.md, the 0418 drafts, the prototypes doc, code. H7-H9 are code notes, not spec, and are not here.
