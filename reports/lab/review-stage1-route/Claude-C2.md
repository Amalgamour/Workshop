# Report: pack C2

- Builder: Claude (Matthew's PC, D:\Git\claude\wf-run\work)
- Pack: C2, from docs/plan/WORK-PAGE-2026-11-30.md:82 @ prima/build 5d26b448.
- Kind: lab (not a wf page; no pass)
- Heads read: returns ec78461d, packs c697e035, prima/build 5d26b448.

## Files touched

- labs/review-stage1-route/C2-REVIEW.md (new)
- this report (new)

## What I did

- Step 0: remote is Amalgamour/Workshop, branch is returns, status was clean.
- Read QUEUE.md and QUESTIONS.md (Codex, only commit cc5f95fa).
- For each group, read the real file lists on origin/packs: each page's `init` grant, later `grant` entries, and the `may touch` line of each `pack` entry.
- Checked each QUEUE and QUESTIONS claim against the logs and the cited lines.
- Read with git show and a small Python JSON reader in my scratch folder. No wf command was run. Nothing was checked out.

## Done when

| Line | Where it is met |
|---|---|
| Every finding cites a log entry or file line | C2-REVIEW.md, every row |
| Each claim is marked holds, wrong or unclear | Parts 2 and 3: 18 QUEUE claims, 10 QUESTIONS claims |
| Each group marked free or clash, with the file | Part 1: 8 rows |

## What I found

1. Every group is free by its real file lists. The only shared file, tests/wf.rs for 0404 and 0416, is already booked one at a time (QUEUE:77).
2. Group 1 is not done: 0423.05.03 closed failed, with work carried to a 05.04 that needs tests/page_0407.rs (P0423 e33). Its helper commit f1e2481a is not on returns. So QUEUE:45-51 is stale.
3. QUESTIONS Q5's default fails: `wf draft` refuses while a withdrawn pass is open (src/cmd.rs:293-299; catch log row 19).
4. Group 2 is free by file, but 0426's golden records `wf board` output, which 0424 changes (PACK-0426-05.01.txt:8).
5. The 0422 grant does not cover src/cmd/ or src/page/ (P0422 e1). Groups 5a and 5b need a new grant after the move.

## Every cite

- Logs on packs c697e035: P0423 e23, e27, e33; P0426 e1, e8; P0424 e1, e7; P0418 e1, e6; P0408 e11; P0404 e14, e17; P0416 e1, e7; P0419 e17, e20, e22; P0407 e9, e10, e12; P0701 e1, e40-42; P0422 e1.
- Files on returns: src/cmd.rs:293-299, :459; labs/0426-plan/PACK-0426-05.01.txt:8, :10; labs/0426-plan/PACK-0426-05.02.txt:12, :14; labs/mvp-plan/PACK-0425-05.01.txt (may touch line); labs/stage1-route/QUEUE.md and QUESTIONS.md lines as listed in C2-REVIEW.md.
- On prima/build dcdab638: docs/design/STAGE-PLAN-90.50.10.md:984, :1010, :1158-1163; docs/plan/GROK-BUILDER-QUEUE.md:94-95; docs/review/ANSWERS-0422-PLAN.md:13-14; docs/plan/MVP-GOAL-PROPOSAL.md:149-150, :183-191; docs/design/WF-BOARD.md:132-136; docs/plan/WORK-PAGE-2026-11-25.md:61.
- On prima/build 5d26b448: docs/quality/CATCH-LOG.md:41 (row 19); docs/plan/WORK-PAGE-2026-11-30.md:165.
- Git checks: `merge-base --is-ancestor f1e2481a origin/returns` no; `merge-base --is-ancestor c1750c32 origin/prima/build` yes; `git diff c1750c32 origin/prima/build` on the four core files is empty.

## Questions for Matthew

- Q-C2a: which close opens group 2? Default A: the carried 0423.05.04 closes and its helper code is on returns first.
- Q-C2b: may 0426.05.01 and 0424.05.01 run at the same time? Default A: no, run 0424 first.

## Stop rules

- None hit. No file outside the two allowed files was needed.
- Nothing needed wf.
- An earlier start of this pack was stopped by Matthew before anything was written. This run started again from step 0.
