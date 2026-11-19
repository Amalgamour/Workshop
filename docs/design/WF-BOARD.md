# `wf board`: a read-only work-order board (design plan)

state: plan for a future wf pass. Not built. Not a ruling.
made: Wed 18 Nov 2026, about 3:30 PM EST, by Prima.
asked for: Matthew t296u-t297u (body-shop work orders, each 05.NN a card); ROADMAP-2026-11-18.md U4, U6 step 1, U7.
builds on: LIB-MINE-M1.md piece 3 (attention first, under a minute, stale shown as stale);
CODEX-LIB-BUILD-REPORT-t323u.md:43 ("a read-only page board that opens the actual evidence").
cites: wf as `file:line @a00bc53` (workflow branch tip).

## 1. What it is
- A new command: `wf board`. It only reads. It never writes.
- `wf board <page>` prints the **page board**: one card per 05.NN work order.
- `wf board` with no page prints the **book board**: one line per page under `pages/` (U4).
- It is built only from `log.jsonl`. Page files are not trusted (the log is the truth).
- Why: Matthew should see what needs him, what is moving, and what passed, in under a minute (U6 step 1).
- Why read-only: assign and move come in stage 7, after the locked door (U7). A board that writes now would write around the compute.

## 2. Layout, top to bottom
1. **Header**: page, title, person, Prime, log entries, last entry time, head hash.
2. **ATTENTION**: what needs someone, most urgent first (section 4).
3. **COLUMNS**: the cards, left to right (section 3).
4. **Footer**: what was cut off, with the command to see it (`wf board <page> --all`).
- Default view: at most 40 lines. Plain text, no colour, no cursor codes.
- Why: under a minute to read (M1 piece 3, `LIB:W/0420.prime-desk/01.md:50-52`).

## 3. Columns
Tool words first. The body-shop word is a side label only.

| Column | Pass tail(s) | Side label | Who owes the next move |
|---|---|---|---|
| Draft | draft | estimate | Prime: `wf pack` |
| Ready | pack | ready for a bay | any builder: `wf claim` |
| Working | open | in the bay | the builder who claimed it |
| Waiting check | return | waiting QC | a checker who is not the builder |
| Checked | review | QC done | Prime: `wf signoff`, then `wf close` |
| Closed | closed | delivered | nobody; split by outcome: passed, failed, blocked, needs-authority |

- The "next move" text reuses `status::pass_next` (src/status.rs:24), so board and status never disagree.
- Closed cards show only the last 3 by default. The footer counts the rest.

## 4. Attention rules
Shown first, in this order. One line each. Each line names its log entry.
1. Questions to the person with no answer (elevations `to: person`). **Never cut off.**
2. Page halted: who, why, entry, and how to resume (`status::how_to_resume`, src/status.rs:9). **Never cut off.**
3. A page file differs from the log (`render::edited`, src/render.rs:293). Board still prints from the log and says "the log wins; run wf verify <page> --fix".
4. Returns waiting for a check.
5. Checked passes waiting for signoff or close.
6. Questions to Prime with no answer.
7. Observer signals (reuse `status::observe`, src/status.rs:67).
8. Stale items (section 5).
- Rules 1 and 2 are never hidden by the 40-line cap. Why: "No hard budget may conceal an affected hold" (M1 piece 3, :50-52).
- If nothing needs anyone, print "attention: none found in the log". Not "all clear". Why: unregistered does not mean none (axiom 7; M1 piece 3, :22).

## 5. Stale shown as stale
A card or attention line gets the word `STALE` and the reason. Nothing is silently re-pointed.
- **Waiting too long**: no log entry on an open pass for 24 hours (same default as `observe --stall-hours`, src/lib.rs:172).
- **Drift**: packed against an older face 01 or 04 (reuse the checks at src/status.rs:99-110). Shows both entry numbers.
- **Old check**: the check was filed on a different return commit than the latest return.
- **Old signoff**: face 01 changed after the signoff entry.
- Why: axiom 6 (stale shows as stale); M1 piece 3 :48 ("no silent repinning"); Codex :39 (a summary can disagree with its records: show the disagreement, never pick one).

## 6. Card fields
Short card (one or two lines on the board):
- `05.NN`, the outcome line from the pack (cut to fit), the tail.
- Who holds it, and who owes the next move.
- Age since the pass's last entry. `STALE` if section 5 applies.
- Counts: open questions, refused returns, failed checks.

Full card (`wf board <page> --card NN`): every field, plus the evidence (section 7).
- If the log does not hold a field, print `unknown (not in the log)`. Not `-`. Why: unknown stays unknown (axiom 7).

## 7. Evidence links (how each card opens its proof)
Every line on a full card names where it came from. Codex :43; axiom 8.

| Evidence | Where the full card points |
|---|---|
| Pack | `pages/<page>/05.NN/PACK.md`, plus `PROMPT.md`, `AGENTS.md`, `RETURN-TEMPLATE.md`; pack hash; pack entry number |
| Return | `git -C <repo> show <commit>:.workshop/returns/<page>.05.NN.md`; branch `pass/<page>.05.NN`; return hash; entry number (src/cmd.rs:350, :459) |
| Refused returns | entry numbers and the escaped reason |
| Check report | `pages/<page>/05.md` section `## 05.NN`; checker; verdict; check entry number (src/cmd.rs:581) |
| Signoff | entry number; outcome; cards |
| Close record | `pages/<page>/05.md` section `## 05.NN`; `record_hash` from the close entry (src/cmd.rs:661) |

- The board prints the commands and paths. It does not run git. Why: no new dependency, nothing can change, and it is fast. A git check is open question Q3.

## 8. Escaping
- Every string from the log goes through `escape_line` (src/chars.rs:273) before it prints. Names too.
- Why: old log entries were written before the input check (README.md:88). The escape is a no-op on clean text, so normal cards look normal (README.md:90).
- Cut a long line **after** escaping, on a character boundary. Never cut inside a `\u{...}`.
- The board's own words use plain ASCII.

## 9. Tests to add (tests/wf.rs, plus unit tests in the new module)
1. **Writes nothing**: sha256 of every page file and the log is the same before and after; no lock file is made.
2. **Columns**: a fixture page with one pass at each tail shows each card in the right column.
3. **Attention order**: person questions come first; a halt comes second.
4. **Never cut**: with 60 open items, person questions and the halt still print; the footer count is right.
5. **Stale**: with `WF_NOW` moved 25 hours ahead (as in examples/car-steering.sh), the open pass shows `STALE`; drift shows both entry numbers.
6. **Old check**: fail, re-return, then the board marks the check as against the older commit.
7. **Hand edit**: change `05.md` by hand; board still prints from the log, exits 0, shows the attention line, writes nothing.
8. **Hostile text**: plant ESC, `ESC[2K\r`, U+2028, U+0085, bidi, a tag character and U+3164 in return lines and file names. No raw `bad_char` in any output.
9. **Evidence paths**: every `PACK.md` path on a full card exists.
10. **Book board**: two pages listed; a page with a broken log shows `unreadable: <reason>` and the board still prints the rest.
11. **Real pages, read-only**: 90.10, 90.20, 90.30 copies print, hashes unchanged. If the pages are absent, print that the test skipped (Tester's 05.04 note).
12. **Short**: the default board for 90.10 (10 passes) is 40 lines or fewer.

## 10. Ready-to-pack jobs (for a future wf pass)
```
repo: workflow
start: workflow (fast-forward to the tip before packing)
outcome: a read-only wf board: book board and page board, attention first, stale shown, evidence named
w01: page board: wf board <page> prints header, columns and short cards from the log only; writes() returns false for board
w02: attention block: rules 1-8 in order; 40-line cap; rules 1-2 never cut; footer count and --all
w03: stale and disagreement: STALE marks for wait, drift, old check, old signoff; hand-edited views shown, log wins
w04: full card: --card NN prints every field and the evidence paths and commands; unknown fields say unknown
w05: book board: wf board with no page lists every page; an unreadable page is shown, not fatal
w06: escaping: every log string through escape_line; cut after escape on a char boundary
w07: docs: README and AGENTS command rows, help text, and why lines
may touch: src/board.rs, src/lib.rs, src/status.rs, tests/wf.rs, README.md, AGENTS.md
checks: cargo test
stop if: the board needs a new log entry kind, a write, or a git call
```
Done when:
- w01: tests 1, 2 pass. `wf board 90.10.00.0001` prints and writes nothing.
- w02: tests 3, 4 pass.
- w03: tests 5, 6, 7 pass.
- w04: test 9 passes; every full-card line names a path, command or entry number.
- w05: test 10 passes. The no-page form works without a page address (today src/lib.rs:127 demands one).
- w06: test 8 passes on every view the board prints.
- w07: README and AGENTS list `board` under "Anyone may run"; tests 11 and 12 pass.

## 11. Open questions for Matthew (four parts each)
**Q1. Column names.**
- Question: Should the columns use the tool words (Draft, Ready, Working, Waiting check, Checked, Closed), with the body-shop words only as side labels?
- Proposed answer: yes.
- Why: the tools, docs and logs already use these words. Two sets of names would drift.
- Axioms check: 2 pass (inherit, do not reinvent); 8 pass (one name points to one thing); 5 pass (the side label keeps your picture).

**Q2. When is waiting "stale"?**
- Question: Should an open pass show STALE after 24 hours with no log entry?
- Proposed answer: yes, 24 hours by default, changeable with `--stall-hours`, the same as the observer.
- Why: one number already in the tool, so board and observer agree.
- Axioms check: 6 pass (stale shown); 2 pass (inherits the observer's default); 7 pass (an old item is marked, not hidden).

**Q3. Should the board look inside git?**
- Question: Should the first board read only the log, and print the git commands to open the evidence, instead of running git itself?
- Proposed answer: yes for now. A later `--deep` flag could check that each commit and file still exists.
- Why: the board stays fast and cannot change anything. Each card still says exactly how to open its proof.
- Axioms check: 3 pass (compute assembles, the person reads); 7 pass (an unchecked link is marked "not checked", not assumed fine); 8 tension (a printed link is not proof it opens, until `--deep`).
