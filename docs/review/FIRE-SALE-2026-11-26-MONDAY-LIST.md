# Fire sale: Monday review list

state: review, not a ruling. By Prima's fire-sale worker, Thu Nov 26 2026, 12:34 AM EST. Updated 12:59 AM EST (job 19: H3, U1-U3 and the board survey default ranked in; job 20: consistency pass).
For: Prima first, then Matthew for the six questions. Nothing here was applied. No work page was edited.

Merged from:
- the Nov 30 fix proposal: docs/review/FIRE-SALE-2026-11-26-NOV30-FIX-PROPOSAL.md (Fix 1-17)
- the Done-when pass: docs/review/FIRE-SALE-2026-11-26-DONE-WHEN.md (DW1-DW11)
- the question sweep: docs/review/FIRE-SALE-2026-11-26-QUESTION-SWEEP.md
- the parked questions in the catch-log and stale-doc audits (Q1, Q2)
- the seqAddr.md fix proposal: docs/review/FIRE-SALE-2026-11-26-SEQADDR-SPEC-FIX-PROPOSAL.md (H1-H6; H3 is a question)
- the UI-1 check: docs/review/FIRE-SALE-2026-11-26-UI1-CHECK.md (U1-U6; U1-U3 are Medium)
- the board survey: docs/research/BOARD-DESIGN-ALTERNATIVES-2026-11-26.md (options A-C, Q1-Q11)

## Where the fix proposal and the Done-when pass don't line up

The fix proposal was written before the Done-when pass. Five gaps:

- G1. Fix 1 (Q13: hold, then withdraw and repack) does not fix DW1. A repacked 0426 still has Claude as Prime. Under t580u Claude can't sign off. WORK-PAGE-2026-11-25.md:65 already said Prima needs `wf set-prime 90.50.10.0426 prima` from Matthew. That ask was never answered, and the Nov 30 page dropped it.
- G2. Fix 2's start rule for X4 (0426: "after 0423.05.04 closes") ignores DW4. 0426's golden captures the book-board view, and 0424 changes it. Whichever lands second breaks the other.
- G3. X6 asks "can 0418 run as packed?" Fix 2 does not touch X6. Because of DW2 (no Done-when line needs the new test) and DW5 ("matches the proposal"), the honest answer is "it can run, but it can close with the job not done". X6 should be told to judge the Done-when lines as well.
- G4. DW8 (does a withdrawn pass count as closed on book-board?) depends on how Q13 is answered. Fix 1 and X5 say nothing about it.
- G5. DW3 and DW10 (Windows run vs box run) are in neither the fix proposal nor X4/X5.

Proposed text for Prima to add to the fix proposal (Prima decides; none of it changes a question to Matthew):
- X4, Done when, add: "Prime is prima, or the draft says 'waiting on set-prime' and stops (DW1). Start commit is after 0424.05.01 closes, or the golden excludes the book-board line (DW4). Golden is the same when made on Windows or on the box; CRLF is normalised (DW3)."
- X5, Done when, add: "Says whether a withdrawn pass shows as current (to match the Q13 answer) (DW8). Holder word is 'none' or 'nobody' on purpose, matching the page board (DW6)."
- X6, Job, add: "Also judge the Done-when lines: can a return with no tests/page_0418.rs pass them? (DW2, DW5)."
- All three packs: "The builder pastes the Windows run; the checker runs on the box; the box run decides (DW10)."

## Ranked list

| # | Item | Read | Who decides |
|---|---|---|---|
| 1 | 0426's Prime is Claude, so it can't be signed off (DW1, G1) | DONE-WHEN.md DW1; docs/plan/WORK-PAGE-2026-11-25.md:65 | **Matthew** (question M1) |
| 2 | Q13's default fails in the tool. Reshape it (F1, Fix 1, G4) | NOV30-FIX-PROPOSAL.md Fix 1; docs/quality/CATCH-LOG.md row 19 | **Matthew** answers the reshaped Q13 (question M2). Prima applies Fix 1 first |
| 3 | H3: once plain 05 is the seat, the 05 pass board has no address. seqAddr.md 5.7 line 202 says it "stays `05.00`", which R9 refuses at parse, and 0418 w01 copies that sentence. Blocks 0418 | docs/review/FIRE-SALE-2026-11-26-SEQADDR-SPEC-FIX-PROPOSAL.md section H3 (four-part question); PROTOTYPES.md H3 and P1 | **Prima or Matthew** (question M5). Default A: the board is derived from the log and has no address (R9, no new grammar) |
| 4 | Claude's check is promised but no pack does it (F4, Fix 4) | NOV30-FIX-PROPOSAL.md Fix 4 | Prima (adds 3 Codex packs, about 15% of Codex's week) |
| 5 | X3/X4/X6 repack text is stale or misses the Done-when findings (Fix 2-3, G2, G3, G5) | NOV30-FIX-PROPOSAL.md Fix 2-3; this file, proposed text above | Prima |
| 6 | UI-1 check U1-U3 (Medium): U1 invents a "pending" card state (wf has accepted, carried, discarded, candidate); U2 marks the job step "missing" before close, though return and signoff entries carry it; U3 repeats the stale DESIGN.md:15-16 "ids not checked" line, though 0403 passed. Claude changed no data | docs/review/FIRE-SALE-2026-11-26-UI1-CHECK.md U1-U3 and proposed catch rows P1-P3 (P4 is a self-catch) | Prima (route the fixes to labs/ui-scaffold/ in a fenced pack, with an independent check per t580u; write or drop rows P1-P4; returns docs/DESIGN.md:15-16 goes on the stale-doc list) |
| 7 | Claude and Codex sub-lead files still read as live (S2, S3) | STALE-DOCS.md S2, S3, Q2 | **Matthew** (question M3) |
| 8 | File the Nov 24-25 DIRECTOR-WORDS (S8) | docs/review/FIRE-SALE-2026-11-26-DIRECTOR-WORDS-DRAFT.md | Prima matches the t-numbers. Ask Matthew what "it" means in draft message M2, and what he meant in draft message M13 ("you should then your authority under me"). These are the draft's own M-numbers, not the M1-M6 questions below |
| 9 | Who writes a catch row when Prima made the mistake (A4) | CATCH-LOG-AUDIT.md A4, Q1 | **Matthew** (question M4) |
| 10 | Board survey default: Option A, wf makes the board as JSON (`wf board --json`, book board first) and the Next.js front only draws it, read-only until stage 7. Claude's UI-1 picked the same A on its own | docs/research/BOARD-DESIGN-ALTERNATIVES-2026-11-26.md sections 3-5 (Q1-Q11, each with a default) | **Matthew** (question M6, survey Q1). Nothing is built until 0424 closes, so it can wait |
| 11 | Old questions still shown open but answered: QD01/O6 (t512), QD22 (t541u), T1 (t401u), sample-page check (t267u), QD06 put off (t585u) | QUESTION-SWEEP.md top findings 1-6; STALE-DOCS.md S13-S15 | Prima (records fix) |
| 12 | Medium and Low text fixes on the Nov 30 page (Fix 5-17) | NOV30-FIX-PROPOSAL.md | Prima (Fix 9 changes a default: if Prima reads A as the design-following option, nothing changes for Matthew) |

Do 1 and 2 before the next stage1-route pack (X3 on), and 3 before 0418 is released. Do 4 before any Claude pack after C2 is used. Do 6 before UI-1 feeds a build page or item 10 is built on it.

## Questions for Matthew

### M1. Move 0426's Prime from Claude to prima?

**Question.** Page 90.50.10.0426 was set up on Nov 23 with Claude as Prime (returns log entry 1). May its Prime move to prima by a recorded `wf set-prime`?

**Why it matters.** Claude has no close or signoff authority under the Claude rules on WORK-PAGE-2026-11-30.md:37-42 (Prima's application of t580u, where Matthew said "we need to be careful with claude"). As packed, 0426.05.01 can't be signed off by anyone, so the pass would sit returned with no lawful signer. DECISIONS-WAITING S14 says a Prime is changed by you or by your grant.

**Options.**
- A (default): Yes. You run, or grant Prima to run, `wf set-prime 90.50.10.0426 prima` with your t-number as the ref. This is recorded in the log, and it follows the design: authority stays where it really sits (t567u), and a Prime change is yours (S14, t547u).
- B: Keep Claude as Prime and name another signer for this pass only. wf has no such path today, so this needs a wf change first.
- C: Withdraw 0426 for now and set it up again later with prima as Prime.

**What happens if no answer.** 0426 stays held and unclaimed. X4 stops at "waiting on set-prime". Nothing else is blocked.

### M2. The three held packs (Nov 30 Q13, reshaped)

**Question.** 0426, 0424 and 0418 .05.01 are packed but out of date. What should happen to them?

**Why it matters.** The current default (withdraw, then repack) does not work today: `wf draft` refuses a pass whose tail is not "closed" (catch row 19; Codex X1). If you approve it, the tool will refuse the next step.

**Options.**
- A (default): Keep the three held until a granted wf fix makes "withdrawn" final for drafting. Then the Prime withdraws each and repacks with the Done-when fixes. No pass is reopened by hand and wf stays in control (t528u).
- B: Approve a pinned build with withdraw now, and accept that the repack waits on that same fix.
- C: Keep them held with no fix planned.
- D (added by self-check SC2, WORK-PAGE-REVIEW.md): leave each 05.01 packed and have the Prime draft a fresh 05.02 with `--overlap-ok 1` and a why, which the pinned wf allows for an open (packed) pass. Tried in a sandbox by job 12 (PROTOTYPES.md, Job 12): it works, but 05.01 and 05.02 could then both be claimed by two builders. So 05.01 has to be withdrawn or closed right after, which hits the same wf gap as A.

**What happens if no answer.** All three stay held, as now. The replacement pack drafts (X4, X5) can still be written and wait.

### M3. Claude and Codex sub-lead roles (from STALE-DOCS Q2)

**Question.** SUB-LEADS.md (t560u) and CLAUDE-LEAD-0422.md (t554u) still make Claude a lead who runs wf. Do they still stand?

**Why it matters.** Both read as live rules. A new session would give Claude a lead job with wf, against the no-wf rule on WORK-PAGE-2026-11-30.md:40 (Prima's application of t580u). t572u said the trial was not a success.

**Options.**
- A (default): Pause both for Claude, under the Nov 30 page's Claude rules (t580u as applied). Claude does only fenced lab packs. Codex keeps lab and evidence work with no lead role. Prima leads 0422. This follows the latest rulings and the current work pages.
- B: Keep Codex as sub-lead (SUB-LEADS.md for Codex only). Pause Claude.
- C: Keep both files as they are.

**What happens if no answer.** Prima treats both as paused for Claude, as the Nov 30 page already does. Nothing is deleted.

### M4. Who writes a catch row when Prima made the mistake (from CATCH-LOG-AUDIT Q1)

**Question.** The rule is "the checker or the Prime, never the model that made the mistake" (t586u). When Prima is the Prime and made the mistake, who writes the row?

**Why it matters.** 6 of 19 rows are about Prima or her executor and were written by Prima. A maker writing its own row can soften it.

**Options.**
- A (default): Prima may write it, but the row quotes the catcher's own words with a cite, and a second view (Grok-Check or Codex) confirms it in its next report. The checker checks; the Prime keeps the record.
- B: The catcher writes the row text in its own report. Prima copies it word for word.
- C: Only Matthew writes rows about Prima.

**What happens if no answer.** Prima keeps writing them, each marked "written by the maker (Prima)" so it is easy to check later.

### M5. Where is the 05 pass board read once plain 05 is the seat? (H3)

Written in full, in four parts, in docs/review/FIRE-SALE-2026-11-26-SEQADDR-SPEC-FIX-PROPOSAL.md section H3. In short: A (default) the board is derived from the log and has no address; B plain 05 means board, then seat; C a new tail like `05.board`; D an R9 exception for `05.00`. If no answer, 0418 stays held and nothing else is blocked.

### M6. Which data flow builds the board front? (board survey Q1)

Written in full in docs/research/BOARD-DESIGN-ALTERNATIVES-2026-11-26.md section 5, Q1 (Q2-Q11 follow, each with a default). In short: A (default) wf makes the board as JSON and the front only draws it; B wf writes snapshot files and the front is static; C the web side reads the logs itself. If no answer, plan A and build nothing until 0424 closes.

## Not on this list

- Low Done-when wording (DW7, DW9, DW11): fold into the repacks with item 5.
- UI-1 check U4-U6 (Low) and seqAddr H1, H2, H4-H6: text fixes that follow rulings already given; they wait for 0418.05.01 to close (t381u).
- The 66 open rows of the question sweep: only the answered ones are listed (item 11). QUESTIONS-2026-11-19 should be re-checked against the chat record.
