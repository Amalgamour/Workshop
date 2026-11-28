# Work page, week of Thu Nov 26 to Thu Dec 3 2026 (startup plan)

For Matthew to review. Nothing on this page runs until he says so (t580u).

Written by Prima on Thu Nov 26, about 11:45 AM EST, after the weekly reset (10:42 AM EST). All times are EST.

This is a plan page. It is not a wf page. It opens no pass by itself.

Status: **published to prima/build on Sat Nov 28** with the 27 fire-sale commits and the usage report (Matthew's push OK, t599u). Matthew is back at work today. He asked for the lab prompts to run (t599u). Only the Claude and Codex lab packs (section 7) are released, as batch 1. Everything else on this page still waits for his answers.

The Grok prompts in section 11 (P1-P4) now have their MANUAL RETURN blocks filled in. P5 and P6 moved to docs/plan/queues/ (see section 11).

---

## 1. Last week, in short

Sources: the box usage report (`/workspace/workshop-build/usage-reports/WEEKLY-2026-11-26.md`, box only), the wf board read on the box at 11:33 AM EST (returns `ec78461d`, packs `c697e035`), and the lead roll on returns.

- Weekly usage: 97.6% on the Super plan. $0 extra credits. It reset at 10:42 AM EST today.
- The Grok builder share against the 50% goal is not known. Matthew has to give that number.
- Stage 1: 4 of 24 pages closed passed.
- On the board now: **no pass is being worked, none waits for a check.** Three passes sit packed and held: 0426.05.01, 0424.05.01, 0418.05.01.
- 0423.05.03 closed failed, with cards w01, w03 and w04 accepted. w02 was carried to a later 05.04.
- 0701.05.04 (the black-box trial of the 0423 lockout) closed passed. 0419.05.02 closed passed. 0407.05.01 closed failed.
- The lead roll (`reports/lead/WORKERS-USED-week-2026-11-26.md` on returns) covers Nov 23 and 24 only. Its last change was Nov 24, 3:10 PM EST. Some rows still say "pending" for work that has since closed (for example 0701.05.04).
- Grok builders used last week: Grok-1, Grok-2, Grok-3, Grok-Check. Grok-4 and Grok-5 were named but did no build pass that closed.

---

## 2. Usage target for this week

- Total weekly usage: up to the 98% mark (t349u, t573u). Never stop early on a projection.
- Grok builders: 50% of weekly usage (t548u).
- Claude and Codex: about 20 packs each. One pack is about 30 minutes and about 5% of their weekly usage (t588u).
- The Wednesday midnight burn (Dec 2) fills what is left, unless usage is already at 98% or more (t573u).
- The Thursday pre-reset report (Dec 3) counts the week. The next reset is Thu Dec 3, 10:42 AM EST.
- Matthew gives the Grok console number. It goes in the Google Sheet "Workshop Weekly Metrics". Prima does not fill the sheet unless he asks.

**Honest risk.** Grok build work is blocked until Monday's answers. Waves 1 and 2 are one builder at a time, because the wf source fixes must chain. So the 50% goal is at risk early in the week. Two things help:
- If Matthew picks option D for 0418 only (Monday question M2), Grok-4 can start 0418 in Wave 1.
- Wave 3 opens three Grok lanes at once, after the pin move.

---

## 3. Issues

1. **Closed is not live.** Builders still run the pinned a823 wf. It has no lockout and no withdraw. Nothing records the live pin. (Catch row 14.)
2. **0423 is not finished.** 0423.05.04 needs a grant for `tests/page_0407.rs`. That file does not have the grant yet.
   - Left to fix: 20 failures in `tests/wf.rs`, `tests/page_0407.rs` line 45, and the Linux-only test `reprint_failure_after_append_says_logged_as` (catch row 16).
3. **Accepted code is not on returns.** 0423.05.03's accepted work (`f1e2481a`) is only on `pass/90.50.10.0423.05.03`. I checked: it is not an ancestor of returns. Same as 0416's `c5bde1e2` (catch row 18). New question N2 below.
4. **Withdraw blocks the next draft.** `wf draft` refuses while any pass tail is not "closed". "withdrawn" is not "closed" (`src/cmd.rs` lines 291-299 on returns). So the three held packs cannot be repacked yet. (Catch row 19.)
5. **Two pages have Claude as Prime.** 0426 (known, Monday question M1). Also **0422 report-system**: its init entry 1 names Claude as Prime. Claude has no signoff (t580u), so nobody could sign off 0422 either. New, folded into M1.
6. **H3 blocks 0418.** Where the 05 pass board is read once plain 05 is the seat (Monday question M5).
7. **DW4.** 0426's golden file records the book-board view. 0424 changes that view. Whichever lands second breaks the other. So 0424 goes before 0426.
8. **Prompt blanks.** Last week's prompts had blanks for the pack number and the start commit (catch row 17). Every prompt has its pack number filled. Builders read the start commit and pack hash from PACK.md. Nothing is left to fill in.

---

## 4. Rules for every lane

- One worker per page. A page has at most one open pass (t533u).
- No two lanes write the same file at the same time.
- A checker never checks its own build. Only Grok-Check runs a real `wf check`.
- Prima packs only with the a823 wf until a recorded pin move says otherwise.
- Stage by path only. Never `add -A`, never `commit -a`. Never force push. Never merge into main.
- Never print, copy or commit a token, password or key.
- Rust only for the compute core.
- Gameatron and Workers A and B stay stopped.

---

## 5. Grok builder lanes

A lane is free only if no other open pass may touch its files. Files come from each page's grant on the box board.

### Wave 1 (Monday, after Matthew's OK and the grant)

| Worker | Pass | Files it may touch | Why this worker | Blocked on |
|---|---|---|---|---|
| Grok-2 | 0423.05.04 | `tests/common/mod.rs`, `tests/wf.rs`, `tests/page_0407.rs` | Built 0423.05.01 to 05.03. Knows the helpers. | Grant for `tests/page_0407.rs` (Matthew). N1. N2. |
| Grok-4 | 0418.05.02 (only if M2 = D for 0418) | `crates/seqaddr-core/src/{state,resolve,validate,face}.rs`, `crates/seqaddr-core/tests/page_0418.rs` | Named for 0418 (t524u). Core run on prima/build. No file shared with wf. | M5 (H3). M2. |

- 0423.05.04 does **not** touch `tests/page_0408.rs` or `tests/lab_0404.rs`. They are green. That keeps them free for 0408.05.02.
- 0423.05.04 start: the accepted 05.03 return `f1e2481a05a95cb506c3f22dec2e35326dbb437a`, so the accepted helpers carry (N2 default A).

### Wave 2 (after 0423.05.04 closes)

| Worker | Pass | Files it may touch | Why | Blocked on |
|---|---|---|---|---|
| Grok-3 | 0408.05.02 | `src/cmd.rs`, `tests/page_0408.rs` | Fresh eyes on the withdraw code (Grok-2 built 0408.05.01). Inside 0408's own grant. No new grant. | M2 = A. 0423.05.04 closed. |
| Grok-1 | 0701.05.05, trial of 0408.05.02 | `tests/lab_0408.rs` | Grok-1 ran the 0701 trials. It did not build 0408. | 0408.05.02 closed. Codex X13 pack text. |

- 0408.05.02 job: `wf draft` treats a "withdrawn" tail as final, like "closed". A packed or claimed pass still blocks the next draft. The board and status are not changed in this pass.
- 0408.05.02 start: 0423.05.04's accepted return commit (chain, N2 default A).

### Pin move (after Wave 2)

1. Prima names the pin commit: the last accepted commit in the chain (0408.05.02's return).
2. Grok-Check runs the whole suite at that commit on Windows. Prima runs it on Linux on the box. The box run decides (DW10, catch row 16).
3. Matthew approves the pin. Prima records it where Matthew rules (Monday question on the live pin; default: face 08 of band door 90.50.10.0400).
4. Each Grok folder rebuilds its wf-bin at the pin. Grok-Check confirms each folder's wf version. Prima writes these setup prompts once the pin commit exists.

### Wave 3 (after the pin move)

| Worker | Pass | Files | Blocked on |
|---|---|---|---|
| Grok-1 | 0424.05.02, after the Prime withdraws 05.01 | `src/board.rs`, `tests/page_0424.rs` | Pin. M2. Codex X5 text. |
| Grok-4 | 0418.05.02, if not run in Wave 1 | seqaddr-core files above | Pin. M2. M5. Codex X6. |
| Grok-5 | 0416.05.02, the Windows-only failures in `tests/wf.rs` | `tests/wf.rs`, `tests/page_0416.rs` | Pin. N2 (0416's `c5bde1e2` is not on returns). |

### Wave 4 (after 0424.05.02 closes)

| Worker | Pass | Files | Blocked on |
|---|---|---|---|
| Grok-3 | 0426.05.02 (golden test only) | `tests/page_0426.rs` | M1 (set-prime to prima). M2. 0424 closed (DW4). Codex X4. |

Not this week: 0425 (waits on 0426), 0422 (waits on 0426, 0425, and a Prime move), 0409 (Monday question), 0406 onward.

---

## 6. Grok-Check jobs

Grok-Check does them one at a time, in this order.

| # | Job | When | Plus |
|---|---|---|---|
| K1 | Check 0423.05.04 | After Grok-2 returns | Prima runs the same checks on Linux (catch row 16). |
| K2 | Check 0418.05.02 | If Wave 1 runs it | Core run: intake on prima/build. |
| K3 | Check 0408.05.02 | After Grok-3 returns | |
| K4 | Check 0701.05.05 | After Grok-1 returns | |
| K5 | Whole suite at the pin commit, report only | Before Matthew approves the pin | Not a wf check. A report by docs/plan/REPORTS.md. |
| K6 | Confirm each Grok folder's wf version | After the pin move | Report only. |
| K7-K9 | Check 0424.05.02, 0416.05.02, then 0426.05.02 | Waves 3 and 4 | |

---

## 7. Claude and Codex lab lanes

They use the published batch on `docs/plan/WORK-PAGE-2026-11-30.md` (prima/build). Only C1 and X1 have run.

Done on Sat Nov 28: Prima applied the fire-sale fix proposal (Fix 1-17, docs/review/FIRE-SALE-2026-11-26-NOV30-FIX-PROPOSAL.md) to the Nov 30 page, except Fix 5 (the MANUAL RETURN block stays) and Fix 9 (a default, so it waits for Matthew). Order and status of every pack: docs/plan/queues/CLAUDE-QUEUE.md and docs/plan/queues/CODEX-QUEUE.md. One filled prompt per pack: docs/plan/queues/CLAUDE-PROMPTS.md and docs/plan/queues/CODEX-PROMPTS.md.

Batch 1 changed from the order below: Claude C2, C3, C21 (C4 and C5 wait for question 2). Codex X2, X3, X6 (X4 waits for 0423.05.04 and M1). The reasons are in the queue files.

### Claude (20 packs, fenced, design only)

- No wf commands. No close, signoff or pack authority (t580u).
- Touches no data, logs, tests or datasets.
- Every Claude pack is "not usable until checked". Codex checks each one (X21-X24).

| Order | Packs | Why this order |
|---|---|---|
| 1 | C2 | Finishes the C1 review pair. Runs on the page as published now. |
| 2 | C4-C7 | Pin record and pin move. Feeds this week's pin move. |
| 3 | C8-C9 | Option C spec only. It decides nothing (t584u). |
| 4 | C20, C3 | Answers Codex X1-X2. Plain summary of Q1-Q8. |
| 5 | C21 (new) | Fix UI-1 findings U1-U3 in `labs/ui-scaffold/` only. |
| 6 | C10-C19 | Overlap, stale pack, 0409 options, catch-log flow, prompt check. |

New row for the Nov 30 page:

| Pack | Folder | Job | Done when |
|---|---|---|---|
| C21 | labs/ui-scaffold/ | Fix U1-U3 from the UI-1 check: drop the invented "pending" card state; do not mark the job step "missing" before close; drop the stale "ids not checked" line. | Each fix cites the wf file and line it now matches. Nothing outside labs/ui-scaffold/ changes. |

### Codex (20 packs, evidence and route)

- No wf commands. Internet is off by default. No signoff or close.

| Order | Packs | Why this order |
|---|---|---|
| 1 | X2 | Finishes the X1 review pair. Runs on the page as published now. |
| 2 | X3 | Refresh the Stage 1 map, with a "code on returns" column (catch row 18). |
| 3 | X4-X6 | Replacement pack texts for 0426, 0424, 0418. Feeds Waves 3 and 4. X4 stops at "waiting on set-prime" if M1 is not answered. |
| 4 | X13 | Lab trial text for 0408. Feeds Wave 2 (0701.05.05). |
| 5 | X21 | Check Claude C4-C9. C8 first: it widens Prima's authority. |
| 6 | X19, X20 | Log audit. Why intake refuses 0001 and 0403. |
| 7 | X7-X12, X14, X15 | Later Stage 1 pack texts and the 0498 acceptance map. |
| 8 | X22, X23, X24 (new) | Check C10-C19, then C21. |

- X16-X18 (master map) move to next week. That keeps Codex at 20.
- New row X24: `labs/review-claude-specs/` | Hostile check of C21 against the UI-1 check (U1-U3). | Each fix marked holds, breaks or unclear, with cites.
- Add `labs/review-claude-specs/` to the Codex lane list, and `labs/ui-scaffold/` to the Claude lane list, so lanes stay apart.

---

## 8. Done when (this week)

- 0423.05.04 is closed. Passed, or failed with its cards accepted and every leftover named.
- 0408.05.02 and its trial 0701.05.05 are closed.
- If Matthew approves: the pin has moved past 0423 and is recorded (closes catch row 14).
- Every Grok pass has a Grok-Check report on returns.
- Claude: about 20 packs pushed. Each has a Codex check row.
- Codex: about 20 packs pushed.
- The Thursday Dec 3 report has the board numbers per worker. Matthew's Grok number goes in the sheet.
- Total usage reached up to 98% by the Dec 3 reset.

---

## 9. What Matthew decides (Monday first)

### Already queued. Answer these first.

Pointers only. Full text is in the local fire-sale Monday list (`docs/review/FIRE-SALE-2026-11-26-MONDAY-LIST.md`) and the files named.

1. **0409 scope**, and **where the live pin is recorded**. Nov 30 page questions 1 and 2.
2. **M1.** Move 0426's Prime from Claude to prima. (Also 0422 now: issue 5.)
3. **M2.** The three held packs (0426, 0424, 0418). The old default does not work (catch row 19).
4. **M5 / H3.** Where the 05 pass board is read. Blocks 0418.
5. **M3.** Claude and Codex sub-lead roles.
6. **M4.** Who writes a catch row when Prima made the mistake.
7. **M6.** Board data flow (default: `wf board` gives JSON, a Next.js front only draws it).
8. Claude labs: draft-page Q1-Q8 (`labs/draft-page/QUESTIONS.md`), C1's Q-C1a and Q-C1b (`labs/review-stage1-route/C1-REVIEW.md`), UI-1 Q1-Q8 (`labs/ui-scaffold/QUESTIONS.md`). All on returns.
9. Codex labs: route Q1-Q6 (`labs/stage1-route/QUESTIONS.md`), X1's 7 questions (`labs/review-draft-page/X1-README-REVIEW.md`), UI-2's 4 questions (`labs/ui-evidence/GAPS.md`). All on returns.

### New from this plan

**N1. In 0423.05.04, may the builder change assertion text that the 0423 rule made false?**
- Why: 10 of the 20 `tests/wf.rs` failures only moved entry numbers (the lockout adds log lines). 4 are race tests (lines 482, 607, 648, 663) where one holder now wins by lockout, not by the old file lock.
- A ★ (default): Yes, only where the meaning stays the same. Each change cites the lockout lines that moved it. A race test still wants exactly one winner, now through the lockout.
- B: No. The builder names them and stops. They stay failing.
- If no answer: 0423.05.04 is packed with option B. Nothing else is blocked.

**N2. How does accepted code that sits only on a pass branch reach the pin?**
- Why: 0423.05.03 (`f1e2481a`) and 0416 (`c5bde1e2`) are not on returns. `wf close` does not merge.
- A ★ (default): Chain. The next pass on the same files starts from the accepted return commit. The pin is the last commit in the chain. No merge.
- B: Prima makes one recorded merge commit on a pin branch (never main). Grok-Check tests it.
- If no answer: chain. 0416.05.02 waits.

**N3. After the pin moves, Prima packs with the new pin, not a823.**
- A ★ (default): Yes. Matthew's pin approval covers it.
- B: Keep packing with a823 until a separate OK.

### Grants and records only Matthew can give

- `tests/page_0407.rs` for 0423 (the person's command; ref is the t-number of his OK):
  `wf.exe grant 90.50.10.0423 --paths "tests/page_0407.rs" --ref (his t-number) --as matthew`
  (This is a command for Matthew, not a builder prompt. Prima writes the real command with the t-number when he says yes.)
- `wf set-prime 90.50.10.0426 prima` (M1), and the same for 0422 if he agrees.
- The pin move.

---

## 10. Blocked until Matthew

- Every Grok pass on this page. Nothing is packed yet. (The Claude and Codex lab packs are released as batch 1, t599u.)
- The 0423 grant. The Prime moves. The pin move. Option C (t584u).

---

## 11. Ready prompts

Each prompt is complete. Prima relays each one only after its pass is packed and Matthew has run the page.

### P1: Grok-2, build 0423.05.04

```
Builder: Grok-2 (Matthew's PC, D:\Git\grok2)

Build 90.50.10.0423.05.04: finish the old test suites under the live lock rule. Prime: Prima. Checker: Grok-Check.
Follow pages\90.50.10.0423\05.04\BUILDER-PROMPT.md step by step. In short:
1. cd D:\Git\grok2\wf-run; git checkout -- pages; git pull --ff-only origin packs; git -C work fetch origin. Set WF_ROOT to this folder and WF_AS=Grok-2.
2. If pages\90.50.10.0423\05.04\PACK.md does not exist, stop and tell Matthew "0423.05.04 is not packed yet".
3. wf.exe claim 90.50.10.0423 04
4. Read the start commit on the "start" line of pages\90.50.10.0423\05.04\PACK.md. Fetch it if needed: git -C work fetch origin pass/90.50.10.0423.05.03. Then: git -C work switch -c work/90.50.10.0423.05.04 at that start commit.
5. Touch only the files on the pack's "may touch" line. Never touch src/. Never weaken the live lock rule. Do not delete, skip or ignore a test.
6. Do each job on face 05 of the pack, in order (w01 first, then w02, and so on). Follow the pack's rule on changing assertion text exactly. If a change is not allowed by the pack, stop and name the test with its line.
7. Set your own CARGO_TARGET_DIR (D:\Git\grok2\target-builder). Never build into wf-bin.
8. Run every check on the pack's "checks" line. Then run cargo test --no-fail-fast once and paste every "test result" line in proof:.
9. Fill .workshop/returns/90.50.10.0423.05.04.md from RETURN-TEMPLATE.md. Copy the pack hash from PACK.md. Include the design review line. Commit by path with the trailer "Builder: Grok-2".
10. wf.exe return 90.50.10.0423 04 --branch returns --commit (git -C work rev-parse HEAD) --file .workshop/returns/90.50.10.0423.05.04.md --push
11. Push your report with docs/plan/REPORTS.md (page 90.50.10.0423, pass 05.04, kind build).
12. Tell Matthew "returned 90.50.10.0423.05.04" and paste wf's last lines.
Never pipe or filter wf output.

MANUAL RETURN (docs/plan/MANUAL-RETURN.md). If wf fails:
1. Stop. Retry the same wf command at most once. If it fails again, do not keep trying.
2. Never hand-edit .workshop logs or log.jsonl. Never fake a claim, return, check, or close. Never bypass wf by hand.
3. Record the exact command, exit code, full error text, the wf commit it was built from, and the OS.
4. Keep all work inside the grant. Stage files by path only (never add -A, never commit -a). Commit with trailer "Builder: Grok-2" to returns. Do not write under .workshop/.
5. Write reports/90.50.10.0423/05.04/Grok-2-MANUAL-RETURN.md with: page, pass, builder, pack hash, start commit, failing step, error, what was done, files touched, test results, and the code commit. Push to returns. Never force push.
6. If the push fails too, paste that same report to Matthew in one block (last resort only). You still hold the page. The report releases the face lock. This is not a handover. The pass never closes until the report is committed to returns and the checker reviews it.
```

### P2: Grok-Check, check 0423.05.04 (K1)

```
Builder: Grok-Check (Matthew's PC, D:\Git\grokcheck)

Check 90.50.10.0423.05.04 (Grok-2's test-suite pass under the live lock rule). Do not sign off or close. Prima does that.
1. cd D:\Git\grokcheck\wf-run; git checkout -- pages; git pull --ff-only origin packs; git -C work fetch origin; git -C work pull --ff-only origin returns. Set WF_ROOT to this folder and WF_AS to Grok-Check.
2. wf.exe intake. The known refusals are 90.50.00.0001 and 90.50.10.0403. Any other refusal: stop and report it.
3. wf.exe board 90.50.10.0423 --card 04. If the card is not in "Waiting check", stop and tell Matthew. Read the return commit and the start commit from that card. Read pages\90.50.10.0423\05.04\PACK.md and the diff from the start to the return commit. Only the files on the "may touch" line and the return file may change.
4. Run every check on the pack's "checks" line at the return commit, in your own CARGO_TARGET_DIR (D:\Git\grokcheck\target-check). Then run cargo test --no-fail-fast once.
5. Judge each Done when line yourself. For every changed assertion, say whether its meaning stayed the same, as the pack's rule says. Name any test that was deleted, skipped, ignored or weakened.
6. Say which failures are Windows-only. The Linux-only test reprint_failure_after_append_says_logged_as cannot run on Windows; write "not judged on Windows" for it. Prima runs it on Linux.
7. wf.exe check 90.50.10.0423 4 --dry-run, then the real run: wf.exe check 90.50.10.0423 4, with --fail "why" for any Done when line that is not met.
8. Push the page log: confirm that origin/returns:.workshop/logs/90.50.10.0423/log.jsonl is a byte prefix of your local pages/90.50.10.0423/log.jsonl. Then copy it, git add -- that path, commit "wf: check 90.50.10.0423.05.04 (log)" with the trailer "Builder: Grok-Check", and push to returns. Never force.
9. Push your report with docs/plan/REPORTS.md (page 90.50.10.0423, pass 05.04, kind check).
10. Tell Matthew "checked 90.50.10.0423.05.04" and paste wf's last lines.
Never pipe or filter wf output.

MANUAL RETURN (docs/plan/MANUAL-RETURN.md). If wf fails:
1. Stop. Retry the same wf command at most once. If it fails again, do not keep trying.
2. Never hand-edit .workshop logs or log.jsonl. Never fake a claim, return, check, or close. Never bypass wf by hand.
3. Record the exact command, exit code, full error text, the wf commit it was built from, and the OS.
4. Keep all work inside the grant. Stage files by path only (never add -A, never commit -a). Commit with trailer "Builder: Grok-Check" to returns. Do not write under .workshop/.
5. Write reports/90.50.10.0423/05.04/Grok-Check-MANUAL-RETURN.md with: page, pass, builder, pack hash, start commit, failing step, error, what was done, files touched, test results, and the code commit. Push to returns. Never force push.
6. If the push fails too, paste that same report to Matthew in one block (last resort only). You still hold the page. The report releases the face lock. This is not a handover. The pass never closes until the report is committed to returns and the checker reviews it.
```

### P3: Grok-3, build 0408.05.02 (Wave 2)

```
Builder: Grok-3 (Matthew's PC, D:\Git\grok3)

Build 90.50.10.0408.05.02: a withdrawn pass no longer blocks the next draft. Prime: Prima. Checker: Grok-Check.
Follow pages\90.50.10.0408\05.02\BUILDER-PROMPT.md step by step. In short:
1. cd D:\Git\grok3\wf-run; git checkout -- pages; git pull --ff-only origin packs; git -C work fetch origin. Set WF_ROOT to this folder and WF_AS=Grok-3.
2. If pages\90.50.10.0408\05.02\PACK.md does not exist, stop and tell Matthew "0408.05.02 is not packed yet".
3. wf.exe claim 90.50.10.0408 02
4. Read the start commit on the "start" line of PACK.md. Fetch it if needed (git -C work fetch origin, and the pass branch the pack names). Then: git -C work switch -c work/90.50.10.0408.05.02 at that start commit.
5. Touch only the files on the pack's "may touch" line. Do not change board or status code. Do not weaken the live lock rule or any test.
6. Do each job on face 05 of the pack, in order.
7. Set your own CARGO_TARGET_DIR (D:\Git\grok3\target-builder). Never build into wf-bin.
8. Run every check on the pack's "checks" line. Then run cargo test --no-fail-fast once and paste every "test result" line in proof:.
9. Fill .workshop/returns/90.50.10.0408.05.02.md from RETURN-TEMPLATE.md. Copy the pack hash from PACK.md. Include the design review line. Commit by path with the trailer "Builder: Grok-3".
10. wf.exe return 90.50.10.0408 02 --branch returns --commit (git -C work rev-parse HEAD) --file .workshop/returns/90.50.10.0408.05.02.md --push
11. Push your report with docs/plan/REPORTS.md (page 90.50.10.0408, pass 05.02, kind build).
12. Tell Matthew "returned 90.50.10.0408.05.02" and paste wf's last lines.
Never pipe or filter wf output.

MANUAL RETURN (docs/plan/MANUAL-RETURN.md). If wf fails:
1. Stop. Retry the same wf command at most once. If it fails again, do not keep trying.
2. Never hand-edit .workshop logs or log.jsonl. Never fake a claim, return, check, or close. Never bypass wf by hand.
3. Record the exact command, exit code, full error text, the wf commit it was built from, and the OS.
4. Keep all work inside the grant. Stage files by path only (never add -A, never commit -a). Commit with trailer "Builder: Grok-3" to returns. Do not write under .workshop/.
5. Write reports/90.50.10.0408/05.02/Grok-3-MANUAL-RETURN.md with: page, pass, builder, pack hash, start commit, failing step, error, what was done, files touched, test results, and the code commit. Push to returns. Never force push.
6. If the push fails too, paste that same report to Matthew in one block (last resort only). You still hold the page. The report releases the face lock. This is not a handover. The pass never closes until the report is committed to returns and the checker reviews it.
```

### P4: Grok-4, build 0418.05.02 (core run; Wave 1 only if M2 = D for 0418, else Wave 3)

```
Builder: Grok-4 (Matthew's PC, D:\Git\grok4)

Build 90.50.10.0418.05.02: the compute core accepts a seat at plain 05. This is a core page. It runs on prima/build, not returns (docs/plan/CORE-RUN.md). Prime: Prima. Checker: Grok-Check.
Follow pages\90.50.10.0418\05.02\BUILDER-PROMPT.md step by step. In short:
1. cd D:\Git\grok4\wf-run; git checkout -- pages; git pull --ff-only origin packs. In work: git -C work checkout prima/build; git -C work pull --ff-only origin prima/build. Set WF_ROOT to this folder and WF_AS=Grok-4.
2. If pages\90.50.10.0418\05.02\PACK.md does not exist, stop and tell Matthew "0418.05.02 is not packed yet". Do not claim 05.01.
3. wf.exe claim 90.50.10.0418 02
4. Read the start commit on the "start" line of PACK.md. Then: git -C work switch -c work/90.50.10.0418.05.02 at that start commit.
5. Touch only the files on the pack's "may touch" line. They are all under crates/seqaddr-core/. Rust only.
6. Do each job on face 05 of the pack, in order. Where the pack names the board address rule (H3), follow it exactly. If it does not, stop and ask.
7. Set your own CARGO_TARGET_DIR (D:\Git\grok4\target-builder). Never build into wf-bin.
8. Run every check on the pack's "checks" line and paste every "test result" line in proof:.
9. Fill .workshop/returns/90.50.10.0418.05.02.md from RETURN-TEMPLATE.md. Copy the pack hash from PACK.md. Include the design review line. Commit by path with the trailer "Builder: Grok-4".
10. wf.exe return 90.50.10.0418 02 --branch prima/build --commit (git -C work rev-parse HEAD) --file .workshop/returns/90.50.10.0418.05.02.md --push
11. Push your report with docs/plan/REPORTS.md (page 90.50.10.0418, pass 05.02, kind build).
12. Tell Matthew "returned 90.50.10.0418.05.02" and paste wf's last lines.
Never pipe or filter wf output.

MANUAL RETURN (docs/plan/MANUAL-RETURN.md). If wf fails:
1. Stop. Retry the same wf command at most once. If it fails again, do not keep trying.
2. Never hand-edit .workshop logs or log.jsonl. Never fake a claim, return, check, or close. Never bypass wf by hand.
3. Record the exact command, exit code, full error text, the wf commit it was built from, and the OS.
4. Keep all work inside the grant. Stage files by path only (never add -A, never commit -a). Commit with trailer "Builder: Grok-4" to returns. Do not write under .workshop/.
5. Write reports/90.50.10.0418/05.02/Grok-4-MANUAL-RETURN.md with: page, pass, builder, pack hash, start commit, failing step, error, what was done, files touched, test results, and the code commit. Push to returns. Never force push.
6. If the push fails too, paste that same report to Matthew in one block (last resort only). You still hold the page. The report releases the face lock. This is not a handover. The pass never closes until the report is committed to returns and the checker reviews it.
```

### P5 and P6: Claude and Codex lab packs

Moved. Each lab pack has its own filled prompt: docs/plan/queues/CLAUDE-PROMPTS.md and docs/plan/queues/CODEX-PROMPTS.md. Batch 1 is C2, C3, C21 and X2, X3, X6.

### Prompts written later (not blanks: they cannot exist yet)

- Grok-Check K2-K9, Grok-1 0701.05.05 and 0424.05.02, Grok-5 0416.05.02, Grok-3 0426.05.02: Prima writes each one, in full, when its pass is packed.
- Pin-move setup prompts: Prima writes them once the pin commit exists.
- The Claude and Codex packs: already written, one filled prompt per pack, in docs/plan/queues/ (t592u). Prima gives Matthew one per run.

---

## 12. Sources checked for this page

- wf board (a823, read only) on the box at 11:33 AM EST: returns `ec78461d`, packs `c697e035`. Both match GitHub.
- Page grants from each page's log on the box (0408, 0416, 0418, 0422, 0423, 0424, 0426).
- `src/cmd.rs` lines 285-300 on returns (draft refusal).
- 0423.05.03 return file in `f1e2481a`; `git merge-base --is-ancestor` for `f1e2481a` (not on returns) and `bf520780` (on returns).
- `reports/lead/WORKERS-USED-week-2026-11-26.md` on returns.
- `docs/usage/` on prima/build: **not found** (GitHub returns 404).
