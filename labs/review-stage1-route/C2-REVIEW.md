# C2: hostile review of Codex's QUEUE.md and QUESTIONS.md

Builder: Claude. 2026-11-28.
Pack C2 from docs/plan/WORK-PAGE-2026-11-30.md:82 @ prima/build 5d26b448.
Reviewed: labs/stage1-route/QUEUE.md and labs/stage1-route/QUESTIONS.md, at returns cc5f95fa (their only commit).
PAGES.csv is not reviewed here. C1 did that.

## How to read this

- Each claim gets one mark: **holds**, **wrong** or **unclear**.
- "Stale" means it held when Codex wrote it (Nov 25) but no longer holds. Stale claims are marked wrong.
- Each group gets one mark: **free** or **clash**, naming the file.
- A group is free when no two packs in it may write the same file.
- The file lists come from the pack grants on origin/packs c697e035:
  - the `init` entry `grant`;
  - any later `grant` entry `paths`;
  - the `may touch` line in each `pack` entry's text.
- "P0423 e27" means entry 27 of pages/90.50.10.0423/log.jsonl on packs c697e035.
- "QUEUE:33" means labs/stage1-route/QUEUE.md line 33.
- I read with git show and a small JSON reader in my scratch folder. I ran no wf command.

## Summary

- Every group in QUEUE.md is **free** by its real file lists. I found no clash.
- But group 1 is not done. 0423.05.03 **closed failed**, and it carries work that needs `tests/wf.rs` and `tests/page_0407.rs` (P0423 e33). That gate holds back the later groups.
- Group 2 is free by file, but two of its packs touch the same **behaviour**: 0426's golden test records `wf board` output, and 0424 changes it.
- QUESTIONS Q5's default no longer works. `wf draft` refuses while a withdrawn pass is open (src/cmd.rs:293-299; catch log row 19).

---

## Part 1: the groups

| Group | Packs | Real files (source) | Mark | Why |
|---|---|---|---|---|
| G1 (QUEUE:29-41) | 0423.05.03 | tests/common/mod.rs, tests/wf.rs, tests/page_0408.rs, tests/lab_0404.rs (P0423 e23 grant; e27 may touch) | **free** | One pack only. The four files match QUEUE:33 exactly. |
| G2 (QUEUE:43-65) | 0426.05.01, 0424.05.01, 0418.05.01 | 0426: tests/page_0426.rs (P0426 e8). 0424: src/board.rs, tests/page_0424.rs (P0424 e7). 0418: crates/seqaddr-core/src/state.rs, resolve.rs, validate.rs, face.rs, crates/seqaddr-core/tests/page_0418.rs (P0418 e6) | **free** by file; **unclear** by behaviour | No file is in two lists. But see C2-3. |
| G2 side: 0408 trial (QUEUE:67-69) | 0701 trial on tests/lab_0408.rs | 0701 grant is all of `tests/` (P0701 e1) | **free** | It runs alone, in its own slot. The wide `tests/` grant means it would clash with any other tests/ writer, which QUEUE:69 says. |
| G2 side: 0404 and 0416 (QUEUE:77) | 0404 and 0416 follow-ups | 0404: tests/wf.rs (P0404 e14 grant, e17 may touch). 0416: tests/wf.rs, tests/page_0416.rs (P0416 e1, e7) | **clash on tests/wf.rs** | QUEUE:77 already says so, and books them one at a time. So the claim holds. |
| G3 (QUEUE:87-101) | 0426 source move | src/cmd.rs, src/cmd/, src/lib.rs, src/page.rs, src/page/, tests/page_0426.rs (P0426 e1 grant; labs/0426-plan/PACK-0426-05.02.txt:14) | **free** | One pack only. The files match QUEUE:91 exactly. |
| G4 (QUEUE:103-114) | 0425, 0422.05.01 | 0425: src/cmd/start.rs, src/page/rules/start.rs, tests/page_0425.rs (labs/mvp-plan/PACK-0425-05.01.txt, may touch line). 0422.05.01: src/report.rs, src/lib.rs, tests/page_0422_01.rs (QUEUE:108) | **free** by the lists; **unclear** | No file is in both lists. But 0425 has no page on packs, so it has no grant yet (`git ls-tree origin/packs pages/`). Its list is draft text only. See C2-5. |
| G5a-G9 (QUEUE:124-134) | one pack per line, run in order | no page, so no grant, for 0406, 0409, 0411-0414, 0417, 0498 (`git ls-tree origin/packs pages/`) | **free** as written | Each line is one pack, or runs after the one before. |
| G6 (QUEUE:128) | 0409 and 0413 "only if both are free" | 0409: src/cmd.rs, src/lib.rs, src/page.rs (STAGE-PLAN:984 @dcdab638). 0413: src/render.rs (GROK-BUILDER-QUEUE:94 @dcdab638) | **free** by plan; **unclear** | No shared file in the plan. Neither page exists, so no grant can be checked. After the 0426 move, the 0409 files will have new names. |

---

## Part 2: QUEUE.md claims

| # | Line | Claim | Mark | Evidence |
|---|---|---|---|---|
| C2-1 | QUEUE:21 | Prima closed 0701.05.04 passed at entry 42 | holds | P0701 e42, close, outcome passed. |
| C2-2 | QUEUE:23 | 0419.05.02 checked passed at 20, closed passed at 22; Grok-Check next checks 0407.05.01 | **wrong (stale)** | 0419 holds: P0419 e20, e22. But 0407.05.01 is already checked and closed failed: P0407 e10 check, e12 close failed. |
| C2-3 | QUEUE:61 | The three group 2 lanes share no listed file | holds for files; **unclear** for behaviour | Files: see G2. Behaviour: 0426.05.01's golden runs "verify, status and board" and records the output (labs/0426-plan/PACK-0426-05.01.txt:8, :10). 0424 changes the book board output (P0424 e1, t541u; MVP-GOAL-PROPOSAL:183-191 @dcdab638). If both run at once, whichever lands second can make the other's result stale. 0426.05.02 refreshes the golden at its own start (PACK-0426-05.02.txt:12), so this may be safe. That is for Prima to judge. |
| C2-4 | QUEUE:33, :45 | Group 1 opens when Matthew records the grant; group 2 starts after group 1 closes | **wrong (stale)** | The grant is recorded (P0423 e23). Group 1 ran and **closed failed** (P0423 e33). w02 is carried to a later 05.04 pass "which needs a grant for tests/page_0407.rs" (P0423 e33, note). So "after group 1 closes" is unclear. Is 05.03's failed close enough, or the carried 05.04? |
| C2-5 | QUEUE:49, :51 | Use the post-helper returns head for wf. The future returns start will include 0423.05.03 | **wrong (stale)** | 0423.05.03's commit f1e2481a is on its pass branch, "not merged by wf v0" (P0423 e33). It is not on returns (`merge-base --is-ancestor` says no). So a returns start does not include the helpers yet. |
| C2-6 | QUEUE:57 | 0426.05.01: tests/page_0426.rs, at P0426 e8 | holds | P0426 e8 may touch tests/page_0426.rs, start bcf0680e. |
| C2-7 | QUEUE:58 | 0424.05.01: src/board.rs, tests/page_0424.rs, at P0424 e7 | holds | P0424 e7. Same as the init grant, P0424 e1. |
| C2-8 | QUEUE:59 | 0418.05.01: five core files, P0418 e1, e6; grant ref t523 | holds | P0418 e1 grant_ref t523; e6 may touch the same five files; branch prima/build. |
| C2-9 | QUEUE:63-65 | c1750c32 is an ancestor; the core diff is empty; "the re-pin still stands" | first two hold; third **unclear** | Checked again at prima/build 5d26b448: ancestor yes, and `git diff c1750c32 origin/prima/build` on the four files is empty. With no drift, the reason for a re-pin is gone (WORK-PAGE-2026-11-30.md, issue 3). QUEUE gives no other reason. Codex pack X6 asks this. |
| C2-10 | QUEUE:69 | The 0408 trial's only test file is tests/lab_0408.rs, while 0701 holds the wider tests/ grant | holds | P0408 e11 close note: "Carry tests/lab_0408.rs forward". P0701 e1 grant `tests/`. |
| C2-11 | QUEUE:73 | The closed 0419.05.02 trial used tests/lab_0419.rs | holds | P0419 e17 may touch tests/lab_0419.rs. |
| C2-12 | QUEUE:77 | 0404 and 0416 follow-ups share tests/wf.rs | holds | P0404 e14, P0416 e1. |
| C2-13 | QUEUE:91 | The 0426 move files | holds | P0426 e1 grant, and PACK-0426-05.02.txt:14. |
| C2-14 | QUEUE:107 | 0425 files: tests/page_0425.rs, src/cmd/start.rs, src/page/rules/start.rs | holds as a draft | labs/mvp-plan/PACK-0425-05.01.txt, may touch line. There is no 0425 page and no grant yet. |
| C2-15 | QUEUE:108 | 0422.05.01 needs "Matthew records the relocated grant" | holds, and it is bigger than it says | The 0422 grant names src/cmd.rs and src/page.rs, but not src/cmd/ or src/page/ (P0422 e1). The 0426 move puts code in src/cmd/ and src/page/ (PACK-0426-05.02.txt:14). So groups 5a and 5b also need a new grant: src/page/rules/mod.rs, src/page/rules/report.rs, src/cmd/build.rs, src/cmd/check.rs and src/cmd/sync.rs (QUEUE:126-127) are outside P0422 e1. |
| C2-16 | QUEUE:110-112 | The lists do not cross; 0425 first if its final grant overlaps | holds | See G4. It follows R1 and R2 (ANSWERS-0422-PLAN.md:13 @dcdab638: "The only page that may cut in is 0425"). |
| C2-17 | QUEUE:146 | 0422.05.04 needs src/render.rs, src/status.rs, tests/page_0422_04.rs | holds | All three are in P0422 e1. |
| C2-18 | QUEUE:15 | 0701 runs one trial at a time | holds | P0701 e1 grant is all of `tests/`, so two 0701 trials would hold the same files. |

---

## Part 3: QUESTIONS.md claims

| # | Question | Claim | Mark | Evidence |
|---|---|---|---|---|
| Q-1 | Q1 | The stage plan lists 0409 as a 0498 prerequisite | holds | STAGE-PLAN:1010 @dcdab638: 0498 needs "0406-0409". |
| Q-2 | Q1 | R1 says retire-a-page is outside the MVP, but still books 0422 ahead of 0409 | holds | ANSWERS-0422-PLAN.md:13-14 @dcdab638: "0409 (retire a page) is not needed for the 0498 MVP", and 0422 goes ahead of 0409. |
| Q-3 | Q1 | 0407 raised that its dropped-page test needs 0409 | holds | P0407 e9 elevate: "retire is page 0409, later". 0407.05.01 has since closed failed (P0407 e12). Q1 should say so. |
| Q-4 | Q2 | 0423 has a recorded override path, and its independent trial closed passed | holds | P0701 e42 close passed. Its card covers the old override case (P0701 e40-42). |
| Q-5 | Q3 | The answered MVP asks for one recorded seqaddr validate step | holds | MVP-GOAL-PROPOSAL.md:149-150 @dcdab638: "wf, plus one seqaddr validate step". |
| Q-6 | Q4 | The stage plan names v4 and refuses names outside its list | holds | STAGE-PLAN:1158-1163 @dcdab638: "a name not on the list is refused at pack"; templates/v4. |
| Q-7 | Q4 | The builder queue names v5 and a stable temporary worker | holds | GROK-BUILDER-QUEUE.md:95 @dcdab638: templates/v5; "a name outside the six becomes a stable temp worker". |
| Q-8 | Q5 | The pinned a823 build has no withdraw; the returns source has it | holds | src/cmd.rs:459 on returns. WORK-PAGE-2026-11-25.md:61 @dcdab638. |
| Q-9 | Q5 | Default A: withdraw each, then repack at the next legal counter | **wrong** | `wf draft` refuses while any other pass's tail is not "closed" (src/cmd.rs:293-299). A withdrawn pass is not "closed". So withdraw-then-repack is refused. Catch log row 19 (docs/quality/CATCH-LOG.md:41 @5d26b448). The new work page already changes this default (WORK-PAGE-2026-11-30.md:165). |
| Q-10 | Q6 | The MVP needs holder, step and next; column words are a separate choice | holds | MVP-GOAL-PROPOSAL.md:183-191 @dcdab638. WF-BOARD.md:132-136 @dcdab638. |

---

## Questions for Matthew

None is decided here.

- **Q-C2a. Which close opens group 2?** (C2-4, C2-5)
  - A, default: the carried 0423.05.04 must close, and the helper code must be on returns, before group 2 packs.
  - B: 0423.05.03's failed close is enough, and group 2 starts from the 0423.05.03 pass branch.
- **Q-C2b. May 0426.05.01 and 0424.05.01 run at the same time?** (C2-3)
  - A, default: no. Run 0424 first, so 0426's golden records the new board.
  - B: yes. 0426.05.02 refreshes the golden at its own start (PACK-0426-05.02.txt:12).

## What I did not check

- Grants for pages that do not exist yet (0406, 0409, 0411-0414, 0417, 0425, 0498). Their files are plan text only.
- Whether a pack's test reads a file another pack writes. I checked only writes, and the one golden case in C2-3.
