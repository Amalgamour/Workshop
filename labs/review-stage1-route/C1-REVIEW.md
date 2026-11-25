# C1: hostile review of Codex's Stage 1 map

Builder: Claude. 2026-11-25.
Pack C1 from docs/plan/WORK-PAGE-2026-11-30.md @ prima/build 4e57df04.
Reviewed: labs/stage1-route/README.md and labs/stage1-route/PAGES.csv, at returns cc5f95fa.
QUEUE.md and QUESTIONS.md are pack C2, not this one.

## How to read this

- Each claim gets one mark: **holds**, **wrong** or **unclear**.
- "Stale" means it held at Codex's snapshot but no longer holds now.
  Stale claims are marked wrong, with the snapshot noted.
- Codex's pins: packs a72be090 (P) and returns ee40448d (R).
- My heads: packs 931f4ca6, returns 1e0d74c6, prima/build 4e57df04.
- "P0407 e9" means entry 9 of pages/90.50.10.0407/log.jsonl on packs.
  "R0407 e9" means .workshop/logs/90.50.10.0407/log.jsonl on returns.
- I read the logs with git show and a small JSON reader. I ran no wf command.

## Summary

- Most state claims hold. I found 0 wrong entry numbers in the log cites.
- 3 claims are now stale: 0407, 0423 and "the first open gate".
- 1 cite points at the wrong lines (0418, W:47-53).
- 3 claims are unclear: 0418's "legal replacement", 0416's accepted code not on returns, and the 24-page set that leaves out 0426.

---

## Part 1: README.md claims

| # | README line | Claim | Mark | Evidence |
|---|---|---|---|---|
| R1 | 13 | PAGES.csv covers all 24 addresses, 0403 to 0425 and 0498 | holds | PAGES.csv:2-25 is 24 rows. 23 addresses (0403-0425) plus 0498. The 24 matches W:194 @dcdab638. |
| R2 | 15 | Four have a passing close | holds, but see U3 | P0403 e12, P0415 e11, P0419 e22, P0423 e22 are each `close` with outcome passed. No other page in 0403-0425 has a passed close. |
| R3 | 15 | The brief counted three | holds | W:194 @dcdab638: "3 of 24 pages closed passed". |
| R4 | 15 | 4 of 24 is about 16.7% | holds | 4 / 24 = 16.67%. |
| R5 | 19-21 | Eleven slots have no log on either branch: 0405, 0406, 0409-0414, 0417, 0420, 0421 | holds | None is in `git ls-tree a72be090 pages/` or `ee40448d .workshop/logs/`. Same at the heads 931f4ca6 and 1e0d74c6. |
| R6 | 23 | 0405 and 0410 have an unused disposition | holds | STAGE-PLAN:980 and :985 @dcdab638 say "not used". |
| R7 | 27, 31 | 0425 and 0498 have no log; 13 in all with none | holds | Not in either tree. 11 + 2 = 13. |
| R8 | 41 | 0419, 0426, 0701 and 0705 logs match on both branches | holds | Same blob ids at a72be090 and ee40448d. Also true for 0404, 0408, 0415, 0416, 0423 and 0424, which the line does not name. Not wrong, only partial. |
| R9 | 45 | 0403: packs 12 entries, returns 9 | holds | Counted. The returns copy is a byte prefix of packs: `cmp` stops at end of the returns copy, line 9, byte 18021. |
| R10 | 46 | 0407: packs 6, returns 9 | holds at snapshot | Counted. The packs copy is a byte prefix of returns, at line 6. Now both have 12 (heads). |
| R11 | 47 | 0418: packs 6, no returns log | holds | P0418 e6 is the pack. No 0418 log on returns. Also none on prima/build, even though the pack's branch is prima/build (P0418 e6 `branch`). Only draft text sits there, under docs/design/drafts/90.50.10.0418/. |
| R12 | 48 | 0422: packs 5, no returns log | holds | P0422 e1-5: init and four face writes. No pack entry. |
| R13 | 55 | 0423 passed, then 0701.05.04 closed passed | holds | P0423 e22 close passed. P0701 e42 close passed, pass 4. |
| R14 | 53 | 0403 passed, then the 0701 harness passed | holds | P0403 e12. P0701 e12 close passed, pass 1. |
| R15 | 74 | The first open critical gate is Matthew's grant for 0423.05.03 | **wrong (stale)** | True at the snapshot. Now granted: R0423 e23 `grant`, paths tests/common/mod.rs, tests/wf.rs, tests/page_0408.rs, tests/lab_0404.rs, ref t584s2361 (returns 4203dc0f). Then packed: R0423 e27, pass 3, branch pass/90.50.10.0423.05.03 (returns 1e0d74c6). The gate is now the 05.03 claim and return. |
| R16 | 80 | The 0408 trial is outstanding | holds | P0408 e11 close note: "Carry tests/lab_0408.rs forward". 0701 has passes 1-4 only (P0701 e6, e18, e21, e37); none is the 0408 trial. tests/lab_0408.rs is not on returns. |
| R17 | 94 | 0415's close stands; its lab card was accepted | holds | P0415 e11 passed. P0701 e32: cards w01 accepted, for tests/lab_0415.rs. |
| R18 | 94 | 0419.05.02 is closed passed | holds | P0419 e22. Its commit fa82cf29 is on returns (`merge-base --is-ancestor` yes). |

### Audit table (README lines 116-134)

| # | Row | Claim | Mark | Evidence |
|---|---|---|---|---|
| A1 | 18 | 0408.05.01 failed with two accepted cards; 0701 trial missing | holds | P0408 e11: outcome failed, w01 and w02 accepted. See R16. |
| A2 | 19 | 0423.05.01 failed on old replay and a past override | holds | P0423 e10 check fail, e12 close failed. |
| A3 | 20-22 | Prima's signoff and close are 0423 entries 21 and 22 | holds | P0423 e21 signoff, e22 close, both passed. The test counts (52 and 17) come from the return report, not the log. I did not re-run them. |
| A4 | 26, 36-37 | 0701.05.04: pack 37, return 39, check pass 40, signoff 41, close passed 42 | holds | P0701 e37-42, in that order. |
| A5 | 32-34 | The recovery kept the first 60,426 bytes | holds | Entries 1-24 of the 0701 log are exactly 60,426 bytes. Entries 25-26 are the 05.03 claim and return. |
| A6 | 35 | Both 0701 trials passed check and closed failed with accepted cards | holds | P0701 e27-28 check pass. e30 and e32 close failed, w01 accepted each. |
| A7 | 42 | 0426 pack is stale if read as ready | holds | P0426 e8 start bcf0680e. 0423's lock landed later (P0423 e22). Same as W:65 @dcdab638. |
| A8 | 50-51 | 0407 is returned | **wrong (stale)** | Now closed failed: R0407 e10 check fail, e11 signoff, e12 close failed (returns bbb7d956). Prima's new work page says the same (WORK-PAGE-2026-11-30.md, issue 4). |
| A9 | 52 | No log for the listed slots | holds | Same as R5. |

---

## Part 2: PAGES.csv rows

The `state` and `sources` columns were checked for every row.
The `next_pass_files` column was checked where a log entry names files.
`waits_on` is planning. It is marked holds when the cited line says it.

| # | Page | Mark | Finding |
|---|---|---|---|
| P1 | 0403 | holds | P0403 e10-12: check pass, signoff and close passed. |
| P2 | 0404 | holds | P0404 e12 close failed (cards discarded). e22 close failed, w01 and w02 accepted. R0701 e27 check pass, e30 close failed, "eight baseline failures". |
| P3 | 0405 | holds | No log. STAGE-PLAN:980 "not used (12.5)". |
| P4 | 0406 | holds | No log. STAGE-PLAN:981 names src/cmd.rs, src/lib.rs, src/page.rs, src/render.rs, the same as the CSV. |
| P5 | 0407 | **wrong (stale)** | State says "05.01 returned". Now closed failed, R0407 e12 (returns bbb7d956). The "dropped-page proof" claim holds: R0407 e9 `elevate`, item w02 says "The log has no dropped state (retire is page 0409, later)". Codex pack X3 already owns this fix. |
| P6 | 0408 | holds | P0408 e11: failed, w01 and w02 accepted, the trial carried. |
| P7 | 0409 | holds | No log. STAGE-PLAN:984 names src/cmd.rs, src/lib.rs, src/page.rs, the same as the CSV. |
| P8 | 0410 | holds | No log. STAGE-PLAN:985 "not used (11.4)". |
| P9 | 0411 | holds | No log. STAGE-PLAN:986 names src/cmd.rs, src/lib.rs. |
| P10 | 0412 | holds | No log. STAGE-PLAN:987 names src/cmd.rs, src/lib.rs, and the grant rule the CSV gives. |
| P11 | 0413 | holds | No log. Files are planning only. |
| P12 | 0414 | holds | No log. Files wait on Codex Q4, as the row says. |
| P13 | 0415 | holds | P0415 e9-11 pass. R0701 e28 check pass, e31-32 close failed. |
| P14 | 0416 | **unclear** | State holds: P0416 e12 close failed, all four cards accepted. But the close record says commit c5bde1e2 "on pass/90.50.10.0416.05.01 (not merged by wf v0)". That commit is **not** on returns (`merge-base --is-ancestor` no). tests/page_0416.rs is not on returns either. The row does not say the accepted code is off returns. A builder could plan as if it landed. |
| P15 | 0417 | holds | No log. |
| P16 | 0418 | **wrong cite, unclear need** | State holds (P0418 e6). But: (1) The `sources` cite W:47-53 @dcdab638 is about Grok-2 and 0423.05.03, not 0418. The 0418 hold is at W:67 and W:253. (2) `missing_evidence` asks for a "legal replacement at current prima/build head". That rests on W:67, the drift claim Prima has now withdrawn (WORK-PAGE-2026-11-30.md, issue 3). I checked: c1750c32 is an ancestor of prima/build 4e57df04, and `git diff c1750c32 origin/prima/build` on the four core files is empty. So a replacement may not be needed. Codex pack X6 asks this. |
| P17 | 0419 | holds | P0419 e11 failed, cards accepted. e22 passed. |
| P18 | 0420 | holds | No log. "Suggested" matches GROK-BUILDER-QUEUE:104 @dcdab638. |
| P19 | 0421 | holds | No log. "Suggested" matches GROK-BUILDER-QUEUE:105. |
| P20 | 0422 | holds | P0422 e1-5, no pack. P0705 e21 close passed. |
| P21 | 0423 | **wrong (stale)** | State holds to entry 22. Now R0423 e23 grant and e27 pack for 05.03. The `next_pass_files` column matches the e23 grant paths exactly, so that part holds. `waits_on` "Matthew grants the four paths" is done. |
| P22 | 0424 | holds | P0424 e7 pack, start a823ee28, never claimed. |
| P23 | 0425 | holds | No log. |
| P24 | 0498 | holds | No log. STAGE-PLAN:989 names README.md and docs/WALKTHROUGH.md. |

---

## Part 3: things the map misses

### U1. 0426 has no row

- The route runs through 0426 three times (README:56-62).
- But the 24 rows stop at 0425 and 0498, so 0426 has no row.
- 0426 has a real log: P0426 e1-8, packed and unclaimed.
- 0426 is not in the stage plan page list at all. `grep 042[2-6]` on STAGE-PLAN @dcdab638 finds nothing.
- So the route's main gate is a page outside the 24 it counts.
- This is not wrong. It is unclear whether 0426 counts toward Stage 1.

### U2. A passed close is not code on returns

- wf v0 does not merge a pass branch. Every close record I read says "(not merged by wf v0)". For example P0419 e22 and P0416 e12.
- 0419.05.02's commit did land on returns. 0416.05.01's did not.
- The CSV state column says what the log says. It does not say where the code is.
- This is the same gap as "closed is not live" (WORK-PAGE-2026-11-30.md, issue 1).

### U3. "4 of 24" counts passes, not pages

- 0423 has a passed close on 05.02, but 05.03 is now packed (R0423 e27).
- So 0423 is not finished. It is counted as one of the 4.
- Whether a page counts as done after one passed pass is a rule question. I do not decide it here.

---

## Questions for Matthew

None of these is decided here.

- **Q-C1a. Does 0426 count toward Stage 1?** (U1)
  - A, default: no. It stays a gate outside the 24, as the map has it.
  - B: yes. Add a row, and the count becomes 25.
- **Q-C1b. When does a page count as "closed passed" in the Stage 1 number?** (U3)
  - A, default: when any pass closes passed, as the map counts today.
  - B: only when no later pass is open, and its code is on returns.

## What I did not check

- Test counts that come only from return reports (A3). I did not re-run them.
- Planning claims with no log behind them, in `waits_on`. I checked only that the cited line says it.
- QUEUE.md and QUESTIONS.md. Those are pack C2.
