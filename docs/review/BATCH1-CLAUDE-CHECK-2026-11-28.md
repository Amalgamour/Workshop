# Batch 1 check: Claude's C2, C3 and C21

Checked by Prima on Sat Nov 28 2026, about 12:00 PM EST. Read only. Matthew asked for it (t611u): "claude is done I guess those prompts didn't actually take much work. You should check them."

## Short answer

- C2: **PASS**
- C3: **PASS**
- C21: **PASS**
- All three followed their prompts. No overreach. No faked claims.
- Claude was fast because these packs are small. It was not because the work was thin.
- Two small new catches, and three older ones that were never logged. All Low. None blocks anything. See the end.

Nothing was sent to Claude or Matthew from this check.

## What was read

- Returns tip: `a82a04887fdcdbf71628c72f835c08a12448101d`. Fetched with FETCH_HEAD. No new refs were left in the box clone.
- Prompts: `/workspace/workshop-build/scratch/labprompts/batch1-C2.txt`, `batch1-C3.txt`, `batch1-C21.txt`.
- Work page and queues: prima/build `5d26b4484067c776dfcf2e58f8255847d2385755`.
- Page logs: packs `c697e0353c34e41a46ebf029f7b417479e5485fa`.
- wf source: returns, at the commit named in each section.

## The four commits on returns today

Times are Matthew's PC clock (CST, -0600). EST is one hour later.

| Pack | Commit | PC time | EST | Files | Trailer |
|---|---|---|---|---|---|
| C2 | ded9a5b504dff99b022e0e02107dd2551065e5ff | 10:47:53 AM | 11:47:53 AM | 2 | Builder: Claude |
| C3 | eab873bbac0238d814e047eda88b6823d0061329 | 10:48:44 AM | 11:48:44 AM | 2 | Builder: Claude |
| C21 | 8ac8c9e7af10bd12c48dc27a46e4197f6b018a40 | 10:49:49 AM | 11:49:49 AM | 3 | Builder: Claude |
| X2 (Codex) | a82a04887fdcdbf71628c72f835c08a12448101d | 10:49:45 AM | 11:49:45 AM | 2 | Builder: Codex |

Same checks for all three Claude commits:

- Branch: all on `returns`. Each commit's parent is the one before it, so Claude pulled before each pack (step 1 of the prompt).
- Files: every file is inside the pack's allowed list. Nothing else changed. No `.workshop/`, no `src/`, no `tests/`, no `pages/`.
- Staged by path: yes. Each commit has exactly the files named in step 8.
- Commit messages: the exact messages the prompts gave.
- Trailer: `Builder: Claude` on all three.
- Protected branches: `claude` is still `bcaaee8`, dated Nov 11. `prima/build` is still `5d26b4484`. `main` is not in the remote list. Nothing was pushed to them.
- No wf command: the reports say none was run. No log or test was touched, so nothing contradicts it.
- Line endings: no stray carriage returns in the new files.

One thing to know about time. The gaps between the commits are 51 seconds and 65 seconds. That fits C3 and C21, which are small. The start time of C2 is not recorded anywhere, so I cannot say how long C2 took. Matthew may know when he pasted it.

## C2: PASS

Prompt: hostile review of Codex's QUEUE.md and QUESTIONS.md. Mark each claim holds, wrong or unclear. Mark each group free or clash, with the file.

Files: [C2-REVIEW.md](https://github.com/Amalgamour/Workshop/blob/ded9a5b504dff99b022e0e02107dd2551065e5ff/labs/review-stage1-route/C2-REVIEW.md) (102 lines) and [Claude-C2.md](https://github.com/Amalgamour/Workshop/blob/ded9a5b504dff99b022e0e02107dd2551065e5ff/reports/lab/review-stage1-route/Claude-C2.md) (54 lines).

Done-when, part by part:

- **Every finding cites a log entry or file line.** Met. I opened about 45 of its cites. All were right. See the list below.
- **Each claim marked holds, wrong or unclear.** Met. 18 queue claims (C2-1 to C2-18) and 10 question claims (Q-1 to Q-10), each with one mark.
- **Each group marked free or clash, with the file.** Met. Part 1 has 8 rows. Free, free by file but unclear by behaviour, or clash on `tests/wf.rs` (0404 and 0416, which QUEUE:77 already says).

Real content, not a stub. Examples I checked:

- **C2-4 (stale):** "group 1 ran and closed failed". True. 0423 entry 33 is a `close`, outcome `failed`, with w02 `carried`. Its note says w02 "carry to a later 05.04 pass, which needs a grant for tests/page_0407.rs".
- **C2-5 (stale):** "0423.05.03's commit is not on returns". True. The close record names `f1e2481a05a95cb506c3f22dec2e35326dbb437a on pass/90.50.10.0423.05.03 (not merged by wf v0)`. I fetched that branch and ran `merge-base --is-ancestor f1e2481a a82a04887`. Answer: no.
- **C2-2 (stale):** "0407.05.01 is already closed failed". True. 0407 entry 10 is a check. Entry 12 is a `close`, outcome `failed`.
- **Q-9 (wrong):** "withdraw then repack is refused". True. `src/cmd.rs:293-299` refuses while any pass tail is not "closed". Same as catch log row 19. Work page line 165 already says it.
- **C2-9:** `c1750c32` is an ancestor of prima/build. I ran the diff on `src` and `crates`. It is empty.
- **C2-15:** the 0422 grant (entry 1) names `src/cmd.rs` and `src/page.rs` but not `src/cmd/` or `src/page/`. True.
- **Group check:** I read the grants on packs for 0423, 0426, 0424, 0418, 0701, 0404, 0416, 0422. They match what C2 says. No page folder exists on packs for 0425, 0406, 0409, 0411-0414, 0417, 0498. So C2 is right to say those grants cannot be checked.

Cites I opened and found correct:

- Page logs: 0423 entries 9, 19, 23, 27, 33. 0407 entries 9, 10, 12. 0701 entries 1, 42. 0426 entries 1, 8. 0424 entries 1, 7. 0418 entries 1, 6. 0419 entries 17, 20, 22. 0404 entries 14, 17. 0416 entries 1, 7. 0408 entry 11. 0422 entry 1.
- wf source: `src/cmd.rs:293-299`, `:459`.
- Docs at dcdab638: STAGE-PLAN:1010 and :1158-1163. ANSWERS-0422-PLAN:13-14. MVP-GOAL-PROPOSAL:149-150 and :183. WF-BOARD:132-134. WORK-PAGE-2026-11-25:61. GROK-BUILDER-QUEUE:94-95.
- Pack text: PACK-0426-05.01:8 and :10. PACK-0426-05.02:12 and :14.
- Catch log row 19 at CATCH-LOG.md:41. Work page line 165.

Stale is not a Codex mistake. Codex committed QUEUE.md at 12:10 PM PC time on Nov 25 (18:10 UTC). The 0407 close is at 18:37 UTC and the 0423.05.03 close is later still. So those claims were true when written. No catch row for them.

Two questions C2 raised for Matthew. Both have defaults. Neither is decided:

- Q-C2a: which close opens group 2? Default A: the carried 0423.05.04 closes first.
- Q-C2b: may 0426.05.01 and 0424.05.01 run together? Default A: no, run 0424 first.

What C2 left out, and says so: grants for pages that do not exist yet, and whether one pack's test reads a file another pack writes.

## C3: PASS

Prompt: SUMMARY-FOR-MATTHEW.md, Q1-Q8 in plain words. Each question in 3 lines or less, with its default.

Files: [SUMMARY-FOR-MATTHEW.md](https://github.com/Amalgamour/Workshop/blob/eab873bbac0238d814e047eda88b6823d0061329/labs/draft-page/SUMMARY-FOR-MATTHEW.md) (38 lines) and [Claude-C3.md](https://github.com/Amalgamour/Workshop/blob/eab873bbac0238d814e047eda88b6823d0061329/reports/lab/draft-page/Claude-C3.md) (44 lines).

Done-when:

- **3 lines or less.** Met. Each question is a title plus 2 or 3 short lines.
- **With its default.** Met. All eight have a "Default:" line.

Evidence:

- I compared every cite with `labs/draft-page/QUESTIONS.md`. All 13 line cites match: :14, :17-23, :31, :33, :50, :65, :77, :93, :94, :104, :106, :115, :117.
- The defaults match QUESTIONS.md for all eight (A for each).
- The work page cites match: WP:146, :152-158.
- Q5 is the one place the work page and QUESTIONS.md differ. QUESTIONS.md says default A. The work page puts the star on B (line 155). The prompt said to say so in one line and not change the default. Claude did exactly that, and asked which to follow.
- The prompt said "Questions 3 to 9 on the work page". That left out work page question 2, which is Claude's Q2. Claude saw it, read lines 145-148 as well, and said so in its report (Claude-C3.md:31). See catch row below.
- Only the two allowed files changed. README.md, QUESTIONS.md and TEST-PLAN.md were not touched.
- Plain words: short lines, one idea each. It reads well for Matthew.

What looks thin, not a fail:

- The summary gives only the default for each question. It does not name the other options (B and C). The prompt asked for "its default" only, so this meets the line. But Matthew cannot choose an answer from this file alone. He has to open QUESTIONS.md for the other choices.
- Q5 leaves out the risk that QUESTIONS.md:80-81 gives (all log work must go to the draft branch).
- Suggest: a later pack adds one line per question for B and C.

## C21: PASS

Prompt: fix U1, U2, U3 from the UI-1 check. Each fix cites the wf file and line it now matches. Nothing outside `labs/ui-scaffold/` changes.

Files: [README.md](https://github.com/Amalgamour/Workshop/blob/8ac8c9e7af10bd12c48dc27a46e4197f6b018a40/labs/ui-scaffold/README.md), [CONTRACT.md](https://github.com/Amalgamour/Workshop/blob/8ac8c9e7af10bd12c48dc27a46e4197f6b018a40/labs/ui-scaffold/CONTRACT.md) and [Claude-C21.md](https://github.com/Amalgamour/Workshop/blob/8ac8c9e7af10bd12c48dc27a46e4197f6b018a40/reports/lab/ui-scaffold/Claude-C21.md) (68 lines).

The change is exactly 4 lines in 2 files (`git show 8ac8c9e7a`: 4 insertions, 4 deletions in README and CONTRACT). Every other line is untouched. QUESTIONS.md is untouched.

Each fix, against the wf source on returns:

- **U1, README.md:38.** "pending" is gone. The new words are `accepted, carried, discarded, candidate`. `src/cmd.rs:14` is `const CARD_WORDS: [&str; 4] = ["accepted", "carried", "discarded", "candidate"];`. Match.
- **U2, CONTRACT.md:24.** "missing before close" is now "partial" from return on. It cites `src/board.rs:412-413` (prints each return job: `for (k, v) in r["jobs"]...`) and `src/board.rs:432` (prints signoff cards). Match. On packs, 0404 entry 21 is a `signoff` with cards `w01 accepted, w02 accepted`. 0423 entry 19 is a `return` with `jobs`. Match.
- **U3, README.md:24 and CONTRACT.md:44.** The "ids not checked" line is replaced. It cites `src/addr.rs:1-4` (rules copied from seqaddr-core), `src/addr.rs:108-123` (`check_work`, lines 108 to 123 exactly), and `src/cmd.rs:187` (`crate::addr::check_work(addr)?;` inside `init_page`, when there is no system ref). Match. The join stays "missing", because `check_work` checks form only.
- **Left alone as told:** U4, U5, U6 are listed "left for Prima" in the report.
- **Leftover search:** I searched all three ui-scaffold files for "pending", "not checked", "DESIGN.md:15" and "before close". None remain.
- **Good extra:** Claude raised one new question for Matthew (should the pass board show a "candidate" column; default yes). It did not edit QUESTIONS.md to do it. That is the right way.

## Codex status (one line each)

- **X2: landed.** Commit `a82a04887fdcdbf71628c72f835c08a12448101d`. It rates all 15 tests D1 to D15 (2 useful, 6 weak, 7 missing a case), does not review SUMMARY-FOR-MATTHEW.md, and stays in its lane. Coverage looks complete. I did not check its findings in depth. That is X21 to X24 and a later look.
- **X3: not landed yet.** No X3 commit on returns. PAGES.csv is still the Nov 25 version.
- **X6: not landed yet.** No X6 commit on returns. No X6 note file.

## Catches

Two new small ones, and three older ones that were never logged. Five rows, 20 to 24, in `docs/quality/CATCH-LOG.md`.

1. **(row 20) Prima's C3 prompt gave the wrong question range.** Near-miss. It said "Questions 3 to 9" for Q1-Q8. Q2 is work page question 2. Claude saw it and covered it. Fix: say "questions 2 to 9" in any prompt that cites this block.
2. **(row 21) C21 cite label.** In the new README line 38, "signoff and close `cards`, 0404 log entry 12 and 22". Both 12 and 22 are `close` entries. The signoff entries are 11 and 21. The CONTRACT line cites 21 right. Low. The words still hold. No change needed now.
3. **U1, U2, U3 were never put in the catch log (rows 22, 23, 24).** The UI-1 check of Nov 26 proposed rows P1 to P3 and left the writing to Prima or a checker. They were not written. They are now, as rows with the fix evidence (C21, 8ac8c9e7).

Not a catch: C3 gives defaults only. That meets its Done-when. Noted above as thin.

## What to do next

- No rework needed on C2, C3 or C21.
- Open for Prima, small: U4, U5, U6 (Low), and `docs/DESIGN.md:15-16`, which is stale. Not in Claude's lane. Not urgent.
- C2's questions Q-C2a and Q-C2b need Matthew's pick. They affect when group 2 can start.
- C20 is now unblocked. X2 has landed.

## Claude batch 2: ready to release

No-blanks check (`noblanks.sh`) run again today on the repo: `hits=0`.

- **C8** (labs/delegated-grant/): ready now. No wait.
- **C20** (labs/draft-page/): ready now. Its input X2 is on returns (`a82a04887`).
- **C9** (labs/delegated-grant/): ready, but only after C8 is returned and pulled. Its prompt says "if missing, stop".

Other Claude packs with no wait, if Matthew wants more in the same go. They sit in separate folders from each other: C10, C12, C14, C16, C18. Their second packs (C11, C13, C15, C17, C19) wait for the first.

Still held: C4, C5, C6, C7. They wait for work page question 2.

Folders do not clash between C8, C20 and the others, so one Claude lane can take them one after another.
