# Fire sale: hostile pass on Done-when lines of open passes

state: review, not a ruling. By Prima's fire-sale worker, Thu Nov 26 2026, 12:31 AM EST.
Read only. Source: a bare clone of the public repo in my scratch folder, fetched 12:30 AM EST.
Tips: packs c697e035, returns ec78461d (Wed 5:41 PM EST), prima/build 5201b243. Nothing moved since the first round.
No wf command was run. Nothing was pushed. No pack was edited.

## Which passes are open

I read every PACK.md on packs (28 passes) and the last log entry for each pass on packs and on returns.

- Open (packed, not claimed): **0418.05.01**, **0424.05.01**, **0426.05.01**. These are the three held packs of Nov 30 Q13.
- Every other pass is closed (passed or failed).
- Carried work with no pass yet: 0423 w02 (to a later 05.04), 0701 Windows suite work (05.02, 05.03 closed failed on 8 baseline Windows failures outside the grant), and the failed passes of 0404, 0407, 0408, 0416, 0419.05.01, 0702, 0703.
- Side note: 90.50.00.0001 and 90.50.10.0403 end on returns with an `elevate` entry after their close passed on packs. That is the intake refusal Nov 30 X20 looks at. Not a Done-when matter.

Severity: **High** = the pass can't close as written, or a pass could close with the job not done. **Medium** = a checker could read the line two ways. **Low** = wording.

## Count

11 findings: 3 High, 5 Medium, 3 Low.

| Page | High | Medium | Low |
|---|---|---|---|
| 0418.05.01 | 1 | 1 | 1 |
| 0424.05.01 | 0 | 2 | 1 |
| 0426.05.01 | 2 | 2 | 1 |

## What holds (checked, no finding)

- 0418 cites are right at start c1750c32: state.rs:459-460 is the counted-face refusal ("it has no door of its own (R9)"); resolve.rs:182-183 is the R9 derived listing for plain FF; face.rs:82-84 is `always_counted` (5 and 6); validate.rs:345 skips counted faces. docs/design/drafts/SEATED-05-PROPOSAL.md exists at the start and on prima/build. docs/spec/seqAddr.md:199-204 holds the t511/t512 seat text.
- 0424 cites are right at start a823ee28: src/board.rs:272 is the page-board "held by ... | next: ..." line; tests/wf.rs has the "  10.10.10.0401  t  entries 4" checks at :1751, :1804, :1936.
- 0426 start bcf0680e is on returns, and 0424's start is its ancestor.
- All three packs name a checker (Grok-Check) and a stop-if that covers files outside may-touch.

## Findings

### DW1. High. 0426: the Prime is Claude, so the pass can't be signed off under t580u.
- Where: packs pages/90.50.10.0426/05.01/PACK.md:5 "prime: Claude". Log: returns .workshop/logs/90.50.10.0426/log.jsonl entry 1 (init by matthew, Nov 23 3:22 PM EST, sets prime), entries 2-8 by actor "Claude", role prime (faces, draft, pack).
- Rulings: t580u (Nov 25): Claude has no close or signoff authority. t567u: acting leads type wf as prima with a note and do not become page Prime. wf signoff is by the face 00 prime (close records say "signed off: prima, face 00 prime at entry N").
- Why it matters: when this pass returns, only Claude can sign it off. Under t580u that is not allowed. The pass would sit returned with no lawful signer.
- Fix: before release, Prime moves from Claude by a recorded set-prime under Matthew's authority (t547u handover; S14 in DECISIONS-WAITING asks who may change a Prime). Or repack 0426 with prime prima. This is also a Q13 matter: holding the pack does not fix it.

### DW2. High. 0418: no Done-when line needs the new test.
- Where: PACK.md:21-25. Job w02 (:17) asks for crates/seqaddr-core/tests/page_0418.rs with four cases. The Done-when lines only ask that `cargo test` passes (:25).
- Why it matters: `cargo test` passes with no new test file at all. A return with only w01 meets every Done-when line, and the checker has no line to refuse it on.
- Fix (for the repack): add "Done when: tests/page_0418.rs exists and shows: a seat at plain 05 is accepted; 05.NN is still a pass; plain 06 is still not a seat; face 06 has no door of its own. Each case is its own test."

### DW3. High. 0426: the golden copy is made on Windows and checked on the box.
- Where: PACK.md:14 (builder Grok-3 on Matthew's PC), :17 (normalise only times, hex, the temp root, and backslashes under the root; "Nothing else changes"), :30 ("pass on the box").
- Evidence: wf runs check commands through `cmd /C` on Windows and `sh -c` elsewhere (src/git.rs:129 at bcf0680e). src/log.rs has a `#[cfg(windows)]` branch (:131). Line endings (CRLF) are not in the normalise list.
- Why it matters: a golden captured on Windows can differ from the box run in shell error text, line endings, or paths outside the root. Then the test fails on the box with nothing wrong, or the builder "fixes" it by widening the normaliser, which w02 forbids.
- Fix: add "Done when: the golden region is identical whether regenerated on Windows or on the box; the checker regenerates on the box and git diff shows no change." Add CRLF to the normalise list, or say the test must run with LF output only. Add to stop-if: "the capture differs between Windows and the box".

### DW4. Medium. 0426 and 0424 touch the same output.
- Where: 0426 PACK.md:13, :16 (golden includes the `board` view and wf help). 0424 PACK.md:13 (changes each book-board line).
- Why it matters: whichever lands second breaks the other. If 0424 lands after 0426, 0426's golden fails until regenerated. 0426.05.02 then can't prove "unchanged" across that change. The page plan names no order.
- Fix: name the order on face 06 of both pages (0424 first, then 0426 regenerates at its own start), or exclude the book-board view from 0426's golden. Add to 0426's Done-when: "the start commit is after 0424 closes, or the golden excludes the book-board line."

### DW5. Medium. 0418: "matches the proposal" is a judgment, not a check.
- Where: PACK.md:24 "the change matches docs/design/drafts/SEATED-05-PROPOSAL.md and seqAddr.md:199-204 on prima/build."
- Why it matters: the proposal is a design draft, not a test. Two checkers can disagree. Also "seqAddr.md" has no folder (it is docs/spec/seqAddr.md).
- Fix: replace with the rule lines it means, each testable: "plain 05 with a body is the seat; the seat does not rewrite any 05.NN; 06 stays counted and unseated" (docs/spec/seqAddr.md:199-204). Keep the proposal as a source, not a Done-when line.

### DW6. Medium. 0424: "none" here, "nobody" on the page board.
- Where: PACK.md:23 (holder is the word none). src/board.rs:272 at a823ee28 prints "held by nobody".
- Why it matters: the Done-when says "using the same data the page board already shows". Two views of the same holder will say different words. A checker could refuse either way.
- Fix: say which word on purpose: "holder is none (the page board's 'nobody' stays as it is)", or use "nobody" in both.

### DW7. Medium. 0426: "views" and "today's layout" are not defined.
- Where: PACK.md:26 ("log and views"), :30 ("on today's layout").
- Why it matters: w01 (:16) lists status and board. The Done-when does not. "Today's layout" moves every day.
- Fix: "views (status and board)" and "at start bcf0680e, before any 0426.05.02 move".

### DW8. Medium. 0424: the "highest-numbered pass whose tail is not closed" rule misses a withdrawn pass.
- Where: PACK.md:23.
- Why it matters: catch log row 19 and Codex X1 show "withdrawn" is not a closed tail for `wf draft`. If a page has a withdrawn pass, book-board will show it as the current pass with step "withdrawn". That may be right, but the Done-when does not say.
- Fix: add "a withdrawn pass counts as not closed (it shows step withdrawn)" or the opposite, to match whatever Q13 decides.

### DW9. Low. 0418: "Code is not applied by hand outside the grant" is a rule, not a Done-when.
- Where: PACK.md:24, second sentence.
- Fix: move it to stop-if (it is already covered there by "another file must change").

### DW10. Low. 0418 and 0424 Done-when lines are not listed for the Windows builder.
- Where: 0418 :25, 0424 :21 say "on the box". Both builders are on Matthew's PC.
- Why it matters: 0701.05.02 and 05.03 closed failed because a required whole Windows suite had 8 baseline failures outside the grant. These packs ask only for the box run, which is better. But the builder can't prove a box run.
- Fix: say "the builder pastes the Windows run; the checker runs it on the box. The box run decides." This makes clear the Windows baseline failures do not fail the pass.

### DW11. Low. 0426: the normaliser's unit test is in a Done-when line but in no job.
- Where: PACK.md:27 "its own unit test shows two runs give the same output". Jobs w01-w06 (:16-21) do not ask for a normaliser unit test.
- Fix: add it to w02, or drop it from the Done-when and rely on w04 (two regenerate runs, no diff).

## What Prima could do

- DW1 first. 0426 can't close as packed while t580u stands. Raise the Prime change with Matthew as a question, with "move Prime to prima by recorded set-prime (t547u)" marked (default).
- DW2, DW3 and DW4 should go into the Q13 answer: when the held packs are withdrawn and repacked, fix these lines in the same repack.
- Nov 30 X4 (0426 replacement pack text) and X5 (0424) are the natural place: add DW1-DW8 to those two Codex packs.
