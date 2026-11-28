# Codex lab prompts

One filled prompt per pack. Written by Prima on Sat Nov 28 2026 (t599u). Nothing here has a blank.

Rules for using this file:
- Give Matthew one prompt at a time, in its own code box.
- Release only the packs that the queue file marks "batch 1" until batch 1 is reviewed. Later prompts are written now but are not released. Status and order: docs/plan/queues/CODEX-QUEUE.md.
- Each prompt names its fixed report file. Nobody fills in a time.
- A prompt for a held pack says what it waits for in the queue file. Do not release it before that is true.

## X2 (batch 1)

```
Builder: Codex (Matthew's PC, D:\Git\codex\wf-run\work)

Lab pack X2. Do only this one pack. Your brief is docs/plan/WORK-PAGE-2026-11-30.md on prima/build. Everything below is filled in. Nothing is left for you to fill in.
Pack: X2
Lab folder: labs/review-draft-page/
Allowed files (your free lane). Write only these:
- labs/review-draft-page/X2-REVIEW.md (new)
- reports/lab/review-draft-page/Codex-X2.md (new, your report)
Job: Hostile review of Claude's TEST-PLAN.md and QUESTIONS.md.
Done when: Each test marked useful, weak or missing a case.
Inputs (read only):
- labs/draft-page/TEST-PLAN.md (Claude, read only)
- labs/draft-page/QUESTIONS.md (Claude, read only)
- labs/review-draft-page/X1-README-REVIEW.md (your own X1 return, for the format)
Note: Do not review SUMMARY-FOR-MATTHEW.md if it appears in labs/draft-page/. Claude is writing it now (pack C3).
Note: Rate each test useful, weak or missing a case. Name the missing case.

Steps:
0. cd D:\Git\codex\wf-run\work. Check first: git remote -v shows Amalgamour/Workshop, git branch --show-current says returns, and git status --short shows nothing. If not, stop and report.
1. The Codex command line blocks the internet by default. Run: git fetch origin; git pull --ff-only origin returns. If this fails because there is no network, stop. Tell Matthew: "Network access is off. Turn it on for Codex, or run git fetch origin and git pull --ff-only origin returns outside Codex, then start me again." Do not work from old files.
2. Read the brief: git show origin/prima/build:docs/plan/WORK-PAGE-2026-11-30.md. Read the sections "Rules for both", "Stop rules" and "Lanes", then the row for pack X2. You may also read origin/packs and origin/prima/build with git show. Do not check them out.
3. Read the inputs above. If an input that is not marked as your own is missing, stop and tell Matthew which one.
4. Write only the allowed files above. Create a missing lab folder if it is yours.
5. Meet the Done when line. Cite a log entry, or a file and line for every claim. In your report, list: the pack, what you did, files touched, every cite, questions for Matthew, and any stop rule you hit.
6. Put any scope or rule conflict as a question for Matthew. Do not decide it. Pack texts are text files only. Do not pack, sign off or close. Write nothing outside the allowed files.
7. You run no wf command. If anything seems to need wf, stop and write it as a question in your report.
8. Commit by path only: git add -- labs/review-draft-page/X2-REVIEW.md reports/lab/review-draft-page/Codex-X2.md. Then: git commit -m "lab: review Claude TEST-PLAN.md and QUESTIONS.md (X2)" -m "Builder: Codex". Never add -A. Never commit -a.
9. Push: git push origin returns. If the push is refused, run git pull --rebase origin returns and push once more. Never force push. Never merge into main. If the push fails because there is no network, do not retry. Tell Matthew: "pack X2 committed on this clone, push blocked", give the commit id, and say: run git push origin returns in D:\Git\codex\wf-run\work outside Codex (or turn network access on for Codex and tell me to push).
10. Stop after about 30 minutes, or when done. Stop early on any stop rule on the work page.
11. Tell Matthew "pack X2 pushed" with the commit id and 3 lines on what you found.

MANUAL RETURN (docs/plan/MANUAL-RETURN.md). You run no wf command, so use this block only if a git step fails or a step seems to need wf:
1. Stop. Retry the same command at most once. If it fails again, do not keep trying.
2. Never hand-edit .workshop logs or log.jsonl. Never fake a claim, return, check, or close. Never bypass wf by hand.
3. Record the exact command, exit code, full error text, and the OS.
4. Keep all work inside the allowed files above. Stage files by path only (never add -A, never commit -a). Commit with trailer "Builder: Codex" to returns. Do not write under .workshop/.
5. Write reports/lab/review-draft-page/Codex-X2-MANUAL-RETURN.md with: pack X2, builder Codex, the failing step, the error, what was done, files touched, and the commit id. Push to returns. Never force push.
6. If the push fails too, paste that same report to Matthew in one block (last resort only). Nothing closes because of it. Prima reviews it.
```

## X3 (batch 1)

```
Builder: Codex (Matthew's PC, D:\Git\codex\wf-run\work)

Lab pack X3. Do only this one pack. Your brief is docs/plan/WORK-PAGE-2026-11-30.md on prima/build. Everything below is filled in. Nothing is left for you to fill in.
Pack: X3
Lab folder: labs/stage1-route/
Allowed files (your free lane). Write only these:
- labs/stage1-route/PAGES.csv (edit)
- reports/lab/stage1-route/Codex-X3.md (new, your report)
Job: Refresh PAGES.csv. Fix 0407 (closed failed, returns bbb7d956). Fix 0423: 05.03 closed failed (returns ec78461d), w02 carried to a later 05.04. Add a column "code on returns": for each closed page, yes or no, with the commit (0416's c5bde1e2 is only on pass/90.50.10.0416.05.01, catch log row 18).
Done when: Every row matches the latest entry in the returns log, with its commit. Every closed page has "code on returns" filled.
Inputs (read only):
- labs/stage1-route/PAGES.csv (your own, to edit)
- The page logs on origin/returns (.workshop/logs) and origin/packs, read with git show
- docs/quality/CATCH-LOG.md rows 17 and 18 on origin/prima/build
Note: Edit PAGES.csv only. Do not edit QUEUE.md or QUESTIONS.md. Claude is reviewing them now (pack C2).
Note: 0407 is closed failed (returns bbb7d956). 0423.05.03 is closed failed (returns ec78461d) and w02 is carried to a later 05.04. 0419 is closed passed.
Note: Add the column "code on returns": for each closed page, yes or no, with the commit. 0416's c5bde1e2 is only on the branch pass/90.50.10.0416.05.01, so it is no.
Note: You are editing an existing file. Keep its column order and add the new column last.

Steps:
0. cd D:\Git\codex\wf-run\work. Check first: git remote -v shows Amalgamour/Workshop, git branch --show-current says returns, and git status --short shows nothing. If not, stop and report.
1. The Codex command line blocks the internet by default. Run: git fetch origin; git pull --ff-only origin returns. If this fails because there is no network, stop. Tell Matthew: "Network access is off. Turn it on for Codex, or run git fetch origin and git pull --ff-only origin returns outside Codex, then start me again." Do not work from old files.
2. Read the brief: git show origin/prima/build:docs/plan/WORK-PAGE-2026-11-30.md. Read the sections "Rules for both", "Stop rules" and "Lanes", then the row for pack X3. You may also read origin/packs and origin/prima/build with git show. Do not check them out.
3. Read the inputs above. If an input that is not marked as your own is missing, stop and tell Matthew which one.
4. Write only the allowed files above. Create a missing lab folder if it is yours.
5. Meet the Done when line. Cite a log entry, or a file and line for every claim. In your report, list: the pack, what you did, files touched, every cite, questions for Matthew, and any stop rule you hit.
6. Put any scope or rule conflict as a question for Matthew. Do not decide it. Pack texts are text files only. Do not pack, sign off or close. Write nothing outside the allowed files.
7. You run no wf command. If anything seems to need wf, stop and write it as a question in your report.
8. Commit by path only: git add -- labs/stage1-route/PAGES.csv reports/lab/stage1-route/Codex-X3.md. Then: git commit -m "lab: refresh the Stage 1 map and add code on returns (X3)" -m "Builder: Codex". Never add -A. Never commit -a.
9. Push: git push origin returns. If the push is refused, run git pull --rebase origin returns and push once more. Never force push. Never merge into main. If the push fails because there is no network, do not retry. Tell Matthew: "pack X3 committed on this clone, push blocked", give the commit id, and say: run git push origin returns in D:\Git\codex\wf-run\work outside Codex (or turn network access on for Codex and tell me to push).
10. Stop after about 30 minutes, or when done. Stop early on any stop rule on the work page.
11. Tell Matthew "pack X3 pushed" with the commit id and 3 lines on what you found.

MANUAL RETURN (docs/plan/MANUAL-RETURN.md). You run no wf command, so use this block only if a git step fails or a step seems to need wf:
1. Stop. Retry the same command at most once. If it fails again, do not keep trying.
2. Never hand-edit .workshop logs or log.jsonl. Never fake a claim, return, check, or close. Never bypass wf by hand.
3. Record the exact command, exit code, full error text, and the OS.
4. Keep all work inside the allowed files above. Stage files by path only (never add -A, never commit -a). Commit with trailer "Builder: Codex" to returns. Do not write under .workshop/.
5. Write reports/lab/stage1-route/Codex-X3-MANUAL-RETURN.md with: pack X3, builder Codex, the failing step, the error, what was done, files touched, and the commit id. Push to returns. Never force push.
6. If the push fails too, paste that same report to Matthew in one block (last resort only). Nothing closes because of it. Prima reviews it.
```

## X4 (held, batch 5)

```
Builder: Codex (Matthew's PC, D:\Git\codex\wf-run\work)

Lab pack X4. Do only this one pack. Your brief is docs/plan/WORK-PAGE-2026-11-30.md on prima/build. Everything below is filled in. Nothing is left for you to fill in.
Pack: X4
Lab folder: labs/stage1-route/packs/
Allowed files (your free lane). Write only these:
- labs/stage1-route/packs/PACK-0426-DRAFT.md (new)
- reports/lab/stage1-route/Codex-X4.md (new, your report)
Job: Replacement pack text for 0426.05.01. Start commit: the returns head after 0423.05.04 closes. If 05.04 is not closed when you start, write "waiting on 0423.05.04" and stop.
Done when: A full draft file that names: start commit, grant paths, may-touch, done-when lines, and files confirmed free against labs/stage1-route/QUEUE.md (with its commit). Prime is prima, or the draft says "waiting on set-prime" and stops (DW1). Start commit is after 0424.05.01 closes, or the golden excludes the book-board line (DW4). Golden is the same when made on Windows or on the box; CRLF is normalised (DW3). The builder pastes the Windows run; the checker runs on the box; the box run decides (DW10).
Inputs (read only):
- labs/stage1-route/QUEUE.md and PAGES.csv (your own)
- The 0426 page log on origin/packs and the old pack text on origin/packs
- docs/review/FIRE-SALE-2026-11-26-DONE-WHEN.md (DW1, DW3, DW4, DW10) on origin/prima/build
Note: Start commit: the returns head after 0423.05.04 closes. If 0423.05.04 is not closed when you start, write the report line "waiting on 0423.05.04", create no draft file, and stop.
Note: If the Prime of 0426 is still Claude, the draft says "waiting on set-prime" at the top and stops there. Prima asks Matthew for wf set-prime.
Note: The builder pastes the Windows run, the checker runs on the box, and the box run decides (DW10, docs/review/FIRE-SALE-2026-11-26-DONE-WHEN.md on origin/prima/build).

Steps:
0. cd D:\Git\codex\wf-run\work. Check first: git remote -v shows Amalgamour/Workshop, git branch --show-current says returns, and git status --short shows nothing. If not, stop and report.
1. The Codex command line blocks the internet by default. Run: git fetch origin; git pull --ff-only origin returns. If this fails because there is no network, stop. Tell Matthew: "Network access is off. Turn it on for Codex, or run git fetch origin and git pull --ff-only origin returns outside Codex, then start me again." Do not work from old files.
2. Read the brief: git show origin/prima/build:docs/plan/WORK-PAGE-2026-11-30.md. Read the sections "Rules for both", "Stop rules" and "Lanes", then the row for pack X4. You may also read origin/packs and origin/prima/build with git show. Do not check them out.
3. Read the inputs above. If an input that is not marked as your own is missing, stop and tell Matthew which one.
4. Write only the allowed files above. Create a missing lab folder if it is yours.
5. Meet the Done when line. Cite a log entry, or a file and line for every claim. In your report, list: the pack, what you did, files touched, every cite, questions for Matthew, and any stop rule you hit.
6. Put any scope or rule conflict as a question for Matthew. Do not decide it. Pack texts are text files only. Do not pack, sign off or close. Write nothing outside the allowed files.
7. You run no wf command. If anything seems to need wf, stop and write it as a question in your report.
8. Commit by path only: git add -- labs/stage1-route/packs/PACK-0426-DRAFT.md reports/lab/stage1-route/Codex-X4.md. Then: git commit -m "lab: draft replacement pack text for 0426.05.01 (X4)" -m "Builder: Codex". Never add -A. Never commit -a.
9. Push: git push origin returns. If the push is refused, run git pull --rebase origin returns and push once more. Never force push. Never merge into main. If the push fails because there is no network, do not retry. Tell Matthew: "pack X4 committed on this clone, push blocked", give the commit id, and say: run git push origin returns in D:\Git\codex\wf-run\work outside Codex (or turn network access on for Codex and tell me to push).
10. Stop after about 30 minutes, or when done. Stop early on any stop rule on the work page.
11. Tell Matthew "pack X4 pushed" with the commit id and 3 lines on what you found.

MANUAL RETURN (docs/plan/MANUAL-RETURN.md). You run no wf command, so use this block only if a git step fails or a step seems to need wf:
1. Stop. Retry the same command at most once. If it fails again, do not keep trying.
2. Never hand-edit .workshop logs or log.jsonl. Never fake a claim, return, check, or close. Never bypass wf by hand.
3. Record the exact command, exit code, full error text, and the OS.
4. Keep all work inside the allowed files above. Stage files by path only (never add -A, never commit -a). Commit with trailer "Builder: Codex" to returns. Do not write under .workshop/.
5. Write reports/lab/stage1-route/Codex-X4-MANUAL-RETURN.md with: pack X4, builder Codex, the failing step, the error, what was done, files touched, and the commit id. Push to returns. Never force push.
6. If the push fails too, paste that same report to Matthew in one block (last resort only). Nothing closes because of it. Prima reviews it.
```

## X5 (held, batch 6)

```
Builder: Codex (Matthew's PC, D:\Git\codex\wf-run\work)

Lab pack X5. Do only this one pack. Your brief is docs/plan/WORK-PAGE-2026-11-30.md on prima/build. Everything below is filled in. Nothing is left for you to fill in.
Pack: X5
Lab folder: labs/stage1-route/packs/
Allowed files (your free lane). Write only these:
- labs/stage1-route/packs/PACK-0424-DRAFT.md (new)
- reports/lab/stage1-route/Codex-X5.md (new, your report)
Job: Replacement pack text for 0424.05.01. Holder means the lock holder. Start commit as for X4.
Done when: A full draft file that names: start commit, grant paths, may-touch, done-when lines, and files confirmed free against labs/stage1-route/QUEUE.md (with its commit). The builder pastes the Windows run; the checker runs on the box; the box run decides (DW10). Says whether a withdrawn pass shows as current (to match the Q13 answer) (DW8). Holder word is "none" or "nobody" on purpose, matching the page board (DW6).
Inputs (read only):
- labs/stage1-route/QUEUE.md and PAGES.csv (your own)
- The 0424 page log and old pack text on origin/packs
- docs/review/FIRE-SALE-2026-11-26-DONE-WHEN.md (DW6, DW8, DW10) on origin/prima/build
Note: Holder means the lock holder, not the claimant (catch log row 19 area and the UI-1 check U4).
Note: Start commit as for X4: the returns head after 0423.05.04 closes. If it is not closed when you start, write the report line "waiting on 0423.05.04", create no draft file, and stop.
Note: The builder pastes the Windows run, the checker runs on the box, and the box run decides (DW10, docs/review/FIRE-SALE-2026-11-26-DONE-WHEN.md on origin/prima/build).

Steps:
0. cd D:\Git\codex\wf-run\work. Check first: git remote -v shows Amalgamour/Workshop, git branch --show-current says returns, and git status --short shows nothing. If not, stop and report.
1. The Codex command line blocks the internet by default. Run: git fetch origin; git pull --ff-only origin returns. If this fails because there is no network, stop. Tell Matthew: "Network access is off. Turn it on for Codex, or run git fetch origin and git pull --ff-only origin returns outside Codex, then start me again." Do not work from old files.
2. Read the brief: git show origin/prima/build:docs/plan/WORK-PAGE-2026-11-30.md. Read the sections "Rules for both", "Stop rules" and "Lanes", then the row for pack X5. You may also read origin/packs and origin/prima/build with git show. Do not check them out.
3. Read the inputs above. If an input that is not marked as your own is missing, stop and tell Matthew which one.
4. Write only the allowed files above. Create a missing lab folder if it is yours.
5. Meet the Done when line. Cite a log entry, or a file and line for every claim. In your report, list: the pack, what you did, files touched, every cite, questions for Matthew, and any stop rule you hit.
6. Put any scope or rule conflict as a question for Matthew. Do not decide it. Pack texts are text files only. Do not pack, sign off or close. Write nothing outside the allowed files.
7. You run no wf command. If anything seems to need wf, stop and write it as a question in your report.
8. Commit by path only: git add -- labs/stage1-route/packs/PACK-0424-DRAFT.md reports/lab/stage1-route/Codex-X5.md. Then: git commit -m "lab: draft replacement pack text for 0424.05.01 (X5)" -m "Builder: Codex". Never add -A. Never commit -a.
9. Push: git push origin returns. If the push is refused, run git pull --rebase origin returns and push once more. Never force push. Never merge into main. If the push fails because there is no network, do not retry. Tell Matthew: "pack X5 committed on this clone, push blocked", give the commit id, and say: run git push origin returns in D:\Git\codex\wf-run\work outside Codex (or turn network access on for Codex and tell me to push).
10. Stop after about 30 minutes, or when done. Stop early on any stop rule on the work page.
11. Tell Matthew "pack X5 pushed" with the commit id and 3 lines on what you found.

MANUAL RETURN (docs/plan/MANUAL-RETURN.md). You run no wf command, so use this block only if a git step fails or a step seems to need wf:
1. Stop. Retry the same command at most once. If it fails again, do not keep trying.
2. Never hand-edit .workshop logs or log.jsonl. Never fake a claim, return, check, or close. Never bypass wf by hand.
3. Record the exact command, exit code, full error text, and the OS.
4. Keep all work inside the allowed files above. Stage files by path only (never add -A, never commit -a). Commit with trailer "Builder: Codex" to returns. Do not write under .workshop/.
5. Write reports/lab/stage1-route/Codex-X5-MANUAL-RETURN.md with: pack X5, builder Codex, the failing step, the error, what was done, files touched, and the commit id. Push to returns. Never force push.
6. If the push fails too, paste that same report to Matthew in one block (last resort only). Nothing closes because of it. Prima reviews it.
```

## X6 (batch 1)

```
Builder: Codex (Matthew's PC, D:\Git\codex\wf-run\work)

Lab pack X6. Do only this one pack. Your brief is docs/plan/WORK-PAGE-2026-11-30.md on prima/build. Everything below is filled in. Nothing is left for you to fill in.
Pack: X6
Lab folder: labs/stage1-route/packs/
Allowed files (your free lane). Write only these:
- labs/stage1-route/packs/X6-0418-NOTE.md (new)
- reports/lab/stage1-route/Codex-X6.md (new, your report)
Job: Note on 0418: can it run as packed? Confirm start, files and line cites. Also judge the Done-when lines: can a return with no tests/page_0418.rs pass them? (DW2, DW5)
Done when: A yes or no, with evidence. The builder pastes the Windows run; the checker runs on the box; the box run decides (DW10).
Inputs (read only):
- The 0418 pack text and log on origin/packs
- crates/seqaddr-core/src/{state,resolve,validate,face}.rs on origin/prima/build (read only)
- docs/review/FIRE-SALE-2026-11-26-DONE-WHEN.md (DW2, DW5) and FIRE-SALE-2026-11-26-SEQADDR-SPEC-FIX-PROPOSAL.md (H3) on origin/prima/build
Note: Answer yes or no in the first line, then the evidence. Also judge the Done-when lines: can a return with no tests/page_0418.rs pass them?
Note: Note where H3 (the 05 pass board address) blocks 0418. Do not decide H3.
Note: The builder pastes the Windows run, the checker runs on the box, and the box run decides (DW10, docs/review/FIRE-SALE-2026-11-26-DONE-WHEN.md on origin/prima/build).

Steps:
0. cd D:\Git\codex\wf-run\work. Check first: git remote -v shows Amalgamour/Workshop, git branch --show-current says returns, and git status --short shows nothing. If not, stop and report.
1. The Codex command line blocks the internet by default. Run: git fetch origin; git pull --ff-only origin returns. If this fails because there is no network, stop. Tell Matthew: "Network access is off. Turn it on for Codex, or run git fetch origin and git pull --ff-only origin returns outside Codex, then start me again." Do not work from old files.
2. Read the brief: git show origin/prima/build:docs/plan/WORK-PAGE-2026-11-30.md. Read the sections "Rules for both", "Stop rules" and "Lanes", then the row for pack X6. You may also read origin/packs and origin/prima/build with git show. Do not check them out.
3. Read the inputs above. If an input that is not marked as your own is missing, stop and tell Matthew which one.
4. Write only the allowed files above. Create a missing lab folder if it is yours.
5. Meet the Done when line. Cite a log entry, or a file and line for every claim. In your report, list: the pack, what you did, files touched, every cite, questions for Matthew, and any stop rule you hit.
6. Put any scope or rule conflict as a question for Matthew. Do not decide it. Pack texts are text files only. Do not pack, sign off or close. Write nothing outside the allowed files.
7. You run no wf command. If anything seems to need wf, stop and write it as a question in your report.
8. Commit by path only: git add -- labs/stage1-route/packs/X6-0418-NOTE.md reports/lab/stage1-route/Codex-X6.md. Then: git commit -m "lab: note on whether 0418 can run as packed (X6)" -m "Builder: Codex". Never add -A. Never commit -a.
9. Push: git push origin returns. If the push is refused, run git pull --rebase origin returns and push once more. Never force push. Never merge into main. If the push fails because there is no network, do not retry. Tell Matthew: "pack X6 committed on this clone, push blocked", give the commit id, and say: run git push origin returns in D:\Git\codex\wf-run\work outside Codex (or turn network access on for Codex and tell me to push).
10. Stop after about 30 minutes, or when done. Stop early on any stop rule on the work page.
11. Tell Matthew "pack X6 pushed" with the commit id and 3 lines on what you found.

MANUAL RETURN (docs/plan/MANUAL-RETURN.md). You run no wf command, so use this block only if a git step fails or a step seems to need wf:
1. Stop. Retry the same command at most once. If it fails again, do not keep trying.
2. Never hand-edit .workshop logs or log.jsonl. Never fake a claim, return, check, or close. Never bypass wf by hand.
3. Record the exact command, exit code, full error text, and the OS.
4. Keep all work inside the allowed files above. Stage files by path only (never add -A, never commit -a). Commit with trailer "Builder: Codex" to returns. Do not write under .workshop/.
5. Write reports/lab/stage1-route/Codex-X6-MANUAL-RETURN.md with: pack X6, builder Codex, the failing step, the error, what was done, files touched, and the commit id. Push to returns. Never force push.
6. If the push fails too, paste that same report to Matthew in one block (last resort only). Nothing closes because of it. Prima reviews it.
```

## X7 (ready, batch 3)

```
Builder: Codex (Matthew's PC, D:\Git\codex\wf-run\work)

Lab pack X7. Do only this one pack. Your brief is docs/plan/WORK-PAGE-2026-11-30.md on prima/build. Everything below is filled in. Nothing is left for you to fill in.
Pack: X7
Lab folder: labs/stage1-route/packs/
Allowed files (your free lane). Write only these:
- labs/stage1-route/packs/PACK-0406-DRAFT.md (new)
- reports/lab/stage1-route/Codex-X7.md (new, your report)
Job: Pack text for 0406.
Done when: Full draft. Files confirmed free against labs/stage1-route/QUEUE.md, citing its commit.
Inputs (read only):
- labs/stage1-route/QUEUE.md and PAGES.csv (your own)
- The 0406 page log and any old pack text on origin/packs
Note: Confirm every file in the may-touch list is free against labs/stage1-route/QUEUE.md, and cite its commit.
Note: Write a full draft: start commit, grant paths, may-touch, done-when lines, checks. Prima packs it. You do not.

Steps:
0. cd D:\Git\codex\wf-run\work. Check first: git remote -v shows Amalgamour/Workshop, git branch --show-current says returns, and git status --short shows nothing. If not, stop and report.
1. The Codex command line blocks the internet by default. Run: git fetch origin; git pull --ff-only origin returns. If this fails because there is no network, stop. Tell Matthew: "Network access is off. Turn it on for Codex, or run git fetch origin and git pull --ff-only origin returns outside Codex, then start me again." Do not work from old files.
2. Read the brief: git show origin/prima/build:docs/plan/WORK-PAGE-2026-11-30.md. Read the sections "Rules for both", "Stop rules" and "Lanes", then the row for pack X7. You may also read origin/packs and origin/prima/build with git show. Do not check them out.
3. Read the inputs above. If an input that is not marked as your own is missing, stop and tell Matthew which one.
4. Write only the allowed files above. Create a missing lab folder if it is yours.
5. Meet the Done when line. Cite a log entry, or a file and line for every claim. In your report, list: the pack, what you did, files touched, every cite, questions for Matthew, and any stop rule you hit.
6. Put any scope or rule conflict as a question for Matthew. Do not decide it. Pack texts are text files only. Do not pack, sign off or close. Write nothing outside the allowed files.
7. You run no wf command. If anything seems to need wf, stop and write it as a question in your report.
8. Commit by path only: git add -- labs/stage1-route/packs/PACK-0406-DRAFT.md reports/lab/stage1-route/Codex-X7.md. Then: git commit -m "lab: draft pack text for 0406 (X7)" -m "Builder: Codex". Never add -A. Never commit -a.
9. Push: git push origin returns. If the push is refused, run git pull --rebase origin returns and push once more. Never force push. Never merge into main. If the push fails because there is no network, do not retry. Tell Matthew: "pack X7 committed on this clone, push blocked", give the commit id, and say: run git push origin returns in D:\Git\codex\wf-run\work outside Codex (or turn network access on for Codex and tell me to push).
10. Stop after about 30 minutes, or when done. Stop early on any stop rule on the work page.
11. Tell Matthew "pack X7 pushed" with the commit id and 3 lines on what you found.

MANUAL RETURN (docs/plan/MANUAL-RETURN.md). You run no wf command, so use this block only if a git step fails or a step seems to need wf:
1. Stop. Retry the same command at most once. If it fails again, do not keep trying.
2. Never hand-edit .workshop logs or log.jsonl. Never fake a claim, return, check, or close. Never bypass wf by hand.
3. Record the exact command, exit code, full error text, and the OS.
4. Keep all work inside the allowed files above. Stage files by path only (never add -A, never commit -a). Commit with trailer "Builder: Codex" to returns. Do not write under .workshop/.
5. Write reports/lab/stage1-route/Codex-X7-MANUAL-RETURN.md with: pack X7, builder Codex, the failing step, the error, what was done, files touched, and the commit id. Push to returns. Never force push.
6. If the push fails too, paste that same report to Matthew in one block (last resort only). Nothing closes because of it. Prima reviews it.
```

## X8 (ready, batch 3)

```
Builder: Codex (Matthew's PC, D:\Git\codex\wf-run\work)

Lab pack X8. Do only this one pack. Your brief is docs/plan/WORK-PAGE-2026-11-30.md on prima/build. Everything below is filled in. Nothing is left for you to fill in.
Pack: X8
Lab folder: labs/stage1-route/packs/
Allowed files (your free lane). Write only these:
- labs/stage1-route/packs/PACK-0411-DRAFT.md (new)
- reports/lab/stage1-route/Codex-X8.md (new, your report)
Job: Pack text for 0411.
Done when: Full draft. Files confirmed free against labs/stage1-route/QUEUE.md, citing its commit.
Inputs (read only):
- labs/stage1-route/QUEUE.md and PAGES.csv (your own)
- The 0411 page log and any old pack text on origin/packs
Note: Confirm every file in the may-touch list is free against labs/stage1-route/QUEUE.md, and cite its commit.
Note: Write a full draft: start commit, grant paths, may-touch, done-when lines, checks. Prima packs it. You do not.

Steps:
0. cd D:\Git\codex\wf-run\work. Check first: git remote -v shows Amalgamour/Workshop, git branch --show-current says returns, and git status --short shows nothing. If not, stop and report.
1. The Codex command line blocks the internet by default. Run: git fetch origin; git pull --ff-only origin returns. If this fails because there is no network, stop. Tell Matthew: "Network access is off. Turn it on for Codex, or run git fetch origin and git pull --ff-only origin returns outside Codex, then start me again." Do not work from old files.
2. Read the brief: git show origin/prima/build:docs/plan/WORK-PAGE-2026-11-30.md. Read the sections "Rules for both", "Stop rules" and "Lanes", then the row for pack X8. You may also read origin/packs and origin/prima/build with git show. Do not check them out.
3. Read the inputs above. If an input that is not marked as your own is missing, stop and tell Matthew which one.
4. Write only the allowed files above. Create a missing lab folder if it is yours.
5. Meet the Done when line. Cite a log entry, or a file and line for every claim. In your report, list: the pack, what you did, files touched, every cite, questions for Matthew, and any stop rule you hit.
6. Put any scope or rule conflict as a question for Matthew. Do not decide it. Pack texts are text files only. Do not pack, sign off or close. Write nothing outside the allowed files.
7. You run no wf command. If anything seems to need wf, stop and write it as a question in your report.
8. Commit by path only: git add -- labs/stage1-route/packs/PACK-0411-DRAFT.md reports/lab/stage1-route/Codex-X8.md. Then: git commit -m "lab: draft pack text for 0411 (X8)" -m "Builder: Codex". Never add -A. Never commit -a.
9. Push: git push origin returns. If the push is refused, run git pull --rebase origin returns and push once more. Never force push. Never merge into main. If the push fails because there is no network, do not retry. Tell Matthew: "pack X8 committed on this clone, push blocked", give the commit id, and say: run git push origin returns in D:\Git\codex\wf-run\work outside Codex (or turn network access on for Codex and tell me to push).
10. Stop after about 30 minutes, or when done. Stop early on any stop rule on the work page.
11. Tell Matthew "pack X8 pushed" with the commit id and 3 lines on what you found.

MANUAL RETURN (docs/plan/MANUAL-RETURN.md). You run no wf command, so use this block only if a git step fails or a step seems to need wf:
1. Stop. Retry the same command at most once. If it fails again, do not keep trying.
2. Never hand-edit .workshop logs or log.jsonl. Never fake a claim, return, check, or close. Never bypass wf by hand.
3. Record the exact command, exit code, full error text, and the OS.
4. Keep all work inside the allowed files above. Stage files by path only (never add -A, never commit -a). Commit with trailer "Builder: Codex" to returns. Do not write under .workshop/.
5. Write reports/lab/stage1-route/Codex-X8-MANUAL-RETURN.md with: pack X8, builder Codex, the failing step, the error, what was done, files touched, and the commit id. Push to returns. Never force push.
6. If the push fails too, paste that same report to Matthew in one block (last resort only). Nothing closes because of it. Prima reviews it.
```

## X9 (ready, batch 3)

```
Builder: Codex (Matthew's PC, D:\Git\codex\wf-run\work)

Lab pack X9. Do only this one pack. Your brief is docs/plan/WORK-PAGE-2026-11-30.md on prima/build. Everything below is filled in. Nothing is left for you to fill in.
Pack: X9
Lab folder: labs/stage1-route/packs/
Allowed files (your free lane). Write only these:
- labs/stage1-route/packs/PACK-0412-DRAFT.md (new)
- reports/lab/stage1-route/Codex-X9.md (new, your report)
Job: Pack text for 0412.
Done when: Full draft. Files confirmed free against labs/stage1-route/QUEUE.md, citing its commit.
Inputs (read only):
- labs/stage1-route/QUEUE.md and PAGES.csv (your own)
- The 0412 page log and any old pack text on origin/packs
Note: Confirm every file in the may-touch list is free against labs/stage1-route/QUEUE.md, and cite its commit.
Note: Write a full draft: start commit, grant paths, may-touch, done-when lines, checks. Prima packs it. You do not.

Steps:
0. cd D:\Git\codex\wf-run\work. Check first: git remote -v shows Amalgamour/Workshop, git branch --show-current says returns, and git status --short shows nothing. If not, stop and report.
1. The Codex command line blocks the internet by default. Run: git fetch origin; git pull --ff-only origin returns. If this fails because there is no network, stop. Tell Matthew: "Network access is off. Turn it on for Codex, or run git fetch origin and git pull --ff-only origin returns outside Codex, then start me again." Do not work from old files.
2. Read the brief: git show origin/prima/build:docs/plan/WORK-PAGE-2026-11-30.md. Read the sections "Rules for both", "Stop rules" and "Lanes", then the row for pack X9. You may also read origin/packs and origin/prima/build with git show. Do not check them out.
3. Read the inputs above. If an input that is not marked as your own is missing, stop and tell Matthew which one.
4. Write only the allowed files above. Create a missing lab folder if it is yours.
5. Meet the Done when line. Cite a log entry, or a file and line for every claim. In your report, list: the pack, what you did, files touched, every cite, questions for Matthew, and any stop rule you hit.
6. Put any scope or rule conflict as a question for Matthew. Do not decide it. Pack texts are text files only. Do not pack, sign off or close. Write nothing outside the allowed files.
7. You run no wf command. If anything seems to need wf, stop and write it as a question in your report.
8. Commit by path only: git add -- labs/stage1-route/packs/PACK-0412-DRAFT.md reports/lab/stage1-route/Codex-X9.md. Then: git commit -m "lab: draft pack text for 0412 (X9)" -m "Builder: Codex". Never add -A. Never commit -a.
9. Push: git push origin returns. If the push is refused, run git pull --rebase origin returns and push once more. Never force push. Never merge into main. If the push fails because there is no network, do not retry. Tell Matthew: "pack X9 committed on this clone, push blocked", give the commit id, and say: run git push origin returns in D:\Git\codex\wf-run\work outside Codex (or turn network access on for Codex and tell me to push).
10. Stop after about 30 minutes, or when done. Stop early on any stop rule on the work page.
11. Tell Matthew "pack X9 pushed" with the commit id and 3 lines on what you found.

MANUAL RETURN (docs/plan/MANUAL-RETURN.md). You run no wf command, so use this block only if a git step fails or a step seems to need wf:
1. Stop. Retry the same command at most once. If it fails again, do not keep trying.
2. Never hand-edit .workshop logs or log.jsonl. Never fake a claim, return, check, or close. Never bypass wf by hand.
3. Record the exact command, exit code, full error text, and the OS.
4. Keep all work inside the allowed files above. Stage files by path only (never add -A, never commit -a). Commit with trailer "Builder: Codex" to returns. Do not write under .workshop/.
5. Write reports/lab/stage1-route/Codex-X9-MANUAL-RETURN.md with: pack X9, builder Codex, the failing step, the error, what was done, files touched, and the commit id. Push to returns. Never force push.
6. If the push fails too, paste that same report to Matthew in one block (last resort only). Nothing closes because of it. Prima reviews it.
```

## X10 (ready, batch 4)

```
Builder: Codex (Matthew's PC, D:\Git\codex\wf-run\work)

Lab pack X10. Do only this one pack. Your brief is docs/plan/WORK-PAGE-2026-11-30.md on prima/build. Everything below is filled in. Nothing is left for you to fill in.
Pack: X10
Lab folder: labs/stage1-route/packs/
Allowed files (your free lane). Write only these:
- labs/stage1-route/packs/PACK-0413-DRAFT.md (new)
- reports/lab/stage1-route/Codex-X10.md (new, your report)
Job: Pack text for 0413.
Done when: Full draft. Files confirmed free against labs/stage1-route/QUEUE.md, citing its commit.
Inputs (read only):
- labs/stage1-route/QUEUE.md and PAGES.csv (your own)
- The 0413 page log and any old pack text on origin/packs
Note: Confirm every file in the may-touch list is free against labs/stage1-route/QUEUE.md, and cite its commit.
Note: Write a full draft: start commit, grant paths, may-touch, done-when lines, checks. Prima packs it. You do not.

Steps:
0. cd D:\Git\codex\wf-run\work. Check first: git remote -v shows Amalgamour/Workshop, git branch --show-current says returns, and git status --short shows nothing. If not, stop and report.
1. The Codex command line blocks the internet by default. Run: git fetch origin; git pull --ff-only origin returns. If this fails because there is no network, stop. Tell Matthew: "Network access is off. Turn it on for Codex, or run git fetch origin and git pull --ff-only origin returns outside Codex, then start me again." Do not work from old files.
2. Read the brief: git show origin/prima/build:docs/plan/WORK-PAGE-2026-11-30.md. Read the sections "Rules for both", "Stop rules" and "Lanes", then the row for pack X10. You may also read origin/packs and origin/prima/build with git show. Do not check them out.
3. Read the inputs above. If an input that is not marked as your own is missing, stop and tell Matthew which one.
4. Write only the allowed files above. Create a missing lab folder if it is yours.
5. Meet the Done when line. Cite a log entry, or a file and line for every claim. In your report, list: the pack, what you did, files touched, every cite, questions for Matthew, and any stop rule you hit.
6. Put any scope or rule conflict as a question for Matthew. Do not decide it. Pack texts are text files only. Do not pack, sign off or close. Write nothing outside the allowed files.
7. You run no wf command. If anything seems to need wf, stop and write it as a question in your report.
8. Commit by path only: git add -- labs/stage1-route/packs/PACK-0413-DRAFT.md reports/lab/stage1-route/Codex-X10.md. Then: git commit -m "lab: draft pack text for 0413 (X10)" -m "Builder: Codex". Never add -A. Never commit -a.
9. Push: git push origin returns. If the push is refused, run git pull --rebase origin returns and push once more. Never force push. Never merge into main. If the push fails because there is no network, do not retry. Tell Matthew: "pack X10 committed on this clone, push blocked", give the commit id, and say: run git push origin returns in D:\Git\codex\wf-run\work outside Codex (or turn network access on for Codex and tell me to push).
10. Stop after about 30 minutes, or when done. Stop early on any stop rule on the work page.
11. Tell Matthew "pack X10 pushed" with the commit id and 3 lines on what you found.

MANUAL RETURN (docs/plan/MANUAL-RETURN.md). You run no wf command, so use this block only if a git step fails or a step seems to need wf:
1. Stop. Retry the same command at most once. If it fails again, do not keep trying.
2. Never hand-edit .workshop logs or log.jsonl. Never fake a claim, return, check, or close. Never bypass wf by hand.
3. Record the exact command, exit code, full error text, and the OS.
4. Keep all work inside the allowed files above. Stage files by path only (never add -A, never commit -a). Commit with trailer "Builder: Codex" to returns. Do not write under .workshop/.
5. Write reports/lab/stage1-route/Codex-X10-MANUAL-RETURN.md with: pack X10, builder Codex, the failing step, the error, what was done, files touched, and the commit id. Push to returns. Never force push.
6. If the push fails too, paste that same report to Matthew in one block (last resort only). Nothing closes because of it. Prima reviews it.
```

## X11 (held, batch 4)

```
Builder: Codex (Matthew's PC, D:\Git\codex\wf-run\work)

Lab pack X11. Do only this one pack. Your brief is docs/plan/WORK-PAGE-2026-11-30.md on prima/build. Everything below is filled in. Nothing is left for you to fill in.
Pack: X11
Lab folder: labs/stage1-route/packs/
Allowed files (your free lane). Write only these:
- labs/stage1-route/packs/PACK-0414-DRAFT.md (new)
- reports/lab/stage1-route/Codex-X11.md (new, your report)
Job: Pack text for 0414.
Done when: Full draft. Files confirmed free against labs/stage1-route/QUEUE.md, citing its commit.
Inputs (read only):
- labs/stage1-route/QUEUE.md and PAGES.csv (your own)
- The 0414 page log and any old pack text on origin/packs
Note: Confirm every file in the may-touch list is free against labs/stage1-route/QUEUE.md, and cite its commit.
Note: Write a full draft: start commit, grant paths, may-touch, done-when lines, checks. Prima packs it. You do not.
Note: Matthew has not answered Codex Q4 (the 0414 builder name rule). Use its default A (the v5 proposal for new packs) and say so at the top of the draft.

Steps:
0. cd D:\Git\codex\wf-run\work. Check first: git remote -v shows Amalgamour/Workshop, git branch --show-current says returns, and git status --short shows nothing. If not, stop and report.
1. The Codex command line blocks the internet by default. Run: git fetch origin; git pull --ff-only origin returns. If this fails because there is no network, stop. Tell Matthew: "Network access is off. Turn it on for Codex, or run git fetch origin and git pull --ff-only origin returns outside Codex, then start me again." Do not work from old files.
2. Read the brief: git show origin/prima/build:docs/plan/WORK-PAGE-2026-11-30.md. Read the sections "Rules for both", "Stop rules" and "Lanes", then the row for pack X11. You may also read origin/packs and origin/prima/build with git show. Do not check them out.
3. Read the inputs above. If an input that is not marked as your own is missing, stop and tell Matthew which one.
4. Write only the allowed files above. Create a missing lab folder if it is yours.
5. Meet the Done when line. Cite a log entry, or a file and line for every claim. In your report, list: the pack, what you did, files touched, every cite, questions for Matthew, and any stop rule you hit.
6. Put any scope or rule conflict as a question for Matthew. Do not decide it. Pack texts are text files only. Do not pack, sign off or close. Write nothing outside the allowed files.
7. You run no wf command. If anything seems to need wf, stop and write it as a question in your report.
8. Commit by path only: git add -- labs/stage1-route/packs/PACK-0414-DRAFT.md reports/lab/stage1-route/Codex-X11.md. Then: git commit -m "lab: draft pack text for 0414 (X11)" -m "Builder: Codex". Never add -A. Never commit -a.
9. Push: git push origin returns. If the push is refused, run git pull --rebase origin returns and push once more. Never force push. Never merge into main. If the push fails because there is no network, do not retry. Tell Matthew: "pack X11 committed on this clone, push blocked", give the commit id, and say: run git push origin returns in D:\Git\codex\wf-run\work outside Codex (or turn network access on for Codex and tell me to push).
10. Stop after about 30 minutes, or when done. Stop early on any stop rule on the work page.
11. Tell Matthew "pack X11 pushed" with the commit id and 3 lines on what you found.

MANUAL RETURN (docs/plan/MANUAL-RETURN.md). You run no wf command, so use this block only if a git step fails or a step seems to need wf:
1. Stop. Retry the same command at most once. If it fails again, do not keep trying.
2. Never hand-edit .workshop logs or log.jsonl. Never fake a claim, return, check, or close. Never bypass wf by hand.
3. Record the exact command, exit code, full error text, and the OS.
4. Keep all work inside the allowed files above. Stage files by path only (never add -A, never commit -a). Commit with trailer "Builder: Codex" to returns. Do not write under .workshop/.
5. Write reports/lab/stage1-route/Codex-X11-MANUAL-RETURN.md with: pack X11, builder Codex, the failing step, the error, what was done, files touched, and the commit id. Push to returns. Never force push.
6. If the push fails too, paste that same report to Matthew in one block (last resort only). Nothing closes because of it. Prima reviews it.
```

## X12 (ready, batch 4)

```
Builder: Codex (Matthew's PC, D:\Git\codex\wf-run\work)

Lab pack X12. Do only this one pack. Your brief is docs/plan/WORK-PAGE-2026-11-30.md on prima/build. Everything below is filled in. Nothing is left for you to fill in.
Pack: X12
Lab folder: labs/stage1-route/packs/
Allowed files (your free lane). Write only these:
- labs/stage1-route/packs/PACK-0417-DRAFT.md (new)
- reports/lab/stage1-route/Codex-X12.md (new, your report)
Job: Pack text for 0417.
Done when: Full draft. Files confirmed free against labs/stage1-route/QUEUE.md, citing its commit.
Inputs (read only):
- labs/stage1-route/QUEUE.md and PAGES.csv (your own)
- The 0417 page log and any old pack text on origin/packs
Note: Confirm every file in the may-touch list is free against labs/stage1-route/QUEUE.md, and cite its commit.
Note: Write a full draft: start commit, grant paths, may-touch, done-when lines, checks. Prima packs it. You do not.

Steps:
0. cd D:\Git\codex\wf-run\work. Check first: git remote -v shows Amalgamour/Workshop, git branch --show-current says returns, and git status --short shows nothing. If not, stop and report.
1. The Codex command line blocks the internet by default. Run: git fetch origin; git pull --ff-only origin returns. If this fails because there is no network, stop. Tell Matthew: "Network access is off. Turn it on for Codex, or run git fetch origin and git pull --ff-only origin returns outside Codex, then start me again." Do not work from old files.
2. Read the brief: git show origin/prima/build:docs/plan/WORK-PAGE-2026-11-30.md. Read the sections "Rules for both", "Stop rules" and "Lanes", then the row for pack X12. You may also read origin/packs and origin/prima/build with git show. Do not check them out.
3. Read the inputs above. If an input that is not marked as your own is missing, stop and tell Matthew which one.
4. Write only the allowed files above. Create a missing lab folder if it is yours.
5. Meet the Done when line. Cite a log entry, or a file and line for every claim. In your report, list: the pack, what you did, files touched, every cite, questions for Matthew, and any stop rule you hit.
6. Put any scope or rule conflict as a question for Matthew. Do not decide it. Pack texts are text files only. Do not pack, sign off or close. Write nothing outside the allowed files.
7. You run no wf command. If anything seems to need wf, stop and write it as a question in your report.
8. Commit by path only: git add -- labs/stage1-route/packs/PACK-0417-DRAFT.md reports/lab/stage1-route/Codex-X12.md. Then: git commit -m "lab: draft pack text for 0417 (X12)" -m "Builder: Codex". Never add -A. Never commit -a.
9. Push: git push origin returns. If the push is refused, run git pull --rebase origin returns and push once more. Never force push. Never merge into main. If the push fails because there is no network, do not retry. Tell Matthew: "pack X12 committed on this clone, push blocked", give the commit id, and say: run git push origin returns in D:\Git\codex\wf-run\work outside Codex (or turn network access on for Codex and tell me to push).
10. Stop after about 30 minutes, or when done. Stop early on any stop rule on the work page.
11. Tell Matthew "pack X12 pushed" with the commit id and 3 lines on what you found.

MANUAL RETURN (docs/plan/MANUAL-RETURN.md). You run no wf command, so use this block only if a git step fails or a step seems to need wf:
1. Stop. Retry the same command at most once. If it fails again, do not keep trying.
2. Never hand-edit .workshop logs or log.jsonl. Never fake a claim, return, check, or close. Never bypass wf by hand.
3. Record the exact command, exit code, full error text, and the OS.
4. Keep all work inside the allowed files above. Stage files by path only (never add -A, never commit -a). Commit with trailer "Builder: Codex" to returns. Do not write under .workshop/.
5. Write reports/lab/stage1-route/Codex-X12-MANUAL-RETURN.md with: pack X12, builder Codex, the failing step, the error, what was done, files touched, and the commit id. Push to returns. Never force push.
6. If the push fails too, paste that same report to Matthew in one block (last resort only). Nothing closes because of it. Prima reviews it.
```

## X13 (ready, batch 2)

```
Builder: Codex (Matthew's PC, D:\Git\codex\wf-run\work)

Lab pack X13. Do only this one pack. Your brief is docs/plan/WORK-PAGE-2026-11-30.md on prima/build. Everything below is filled in. Nothing is left for you to fill in.
Pack: X13
Lab folder: labs/stage1-route/packs/
Allowed files (your free lane). Write only these:
- labs/stage1-route/packs/LAB-0408-DRAFT.md (new)
- reports/lab/stage1-route/Codex-X13.md (new, your report)
Job: Lab trial pack text for 0408 (tests/lab_0408.rs on 0701).
Done when: Test spec and done-when lines for tests/lab_0408.rs.
Inputs (read only):
- docs/plan/WORK-PAGE-2026-11-26-WEEK.md on origin/prima/build (section 5, "0408.05.02 job")
- The 0408 and 0701 page logs on origin/packs
- tests/lab_0404.rs and tests/page_0408.rs on origin/returns (read only)
Note: Write the test spec and Done-when lines for tests/lab_0408.rs on page 0701. The trial is for the job: wf draft treats a withdrawn tail as final, like closed.
Note: This text is used only if Matthew answers M2 with option A. Say so at the top.

Steps:
0. cd D:\Git\codex\wf-run\work. Check first: git remote -v shows Amalgamour/Workshop, git branch --show-current says returns, and git status --short shows nothing. If not, stop and report.
1. The Codex command line blocks the internet by default. Run: git fetch origin; git pull --ff-only origin returns. If this fails because there is no network, stop. Tell Matthew: "Network access is off. Turn it on for Codex, or run git fetch origin and git pull --ff-only origin returns outside Codex, then start me again." Do not work from old files.
2. Read the brief: git show origin/prima/build:docs/plan/WORK-PAGE-2026-11-30.md. Read the sections "Rules for both", "Stop rules" and "Lanes", then the row for pack X13. You may also read origin/packs and origin/prima/build with git show. Do not check them out.
3. Read the inputs above. If an input that is not marked as your own is missing, stop and tell Matthew which one.
4. Write only the allowed files above. Create a missing lab folder if it is yours.
5. Meet the Done when line. Cite a log entry, or a file and line for every claim. In your report, list: the pack, what you did, files touched, every cite, questions for Matthew, and any stop rule you hit.
6. Put any scope or rule conflict as a question for Matthew. Do not decide it. Pack texts are text files only. Do not pack, sign off or close. Write nothing outside the allowed files.
7. You run no wf command. If anything seems to need wf, stop and write it as a question in your report.
8. Commit by path only: git add -- labs/stage1-route/packs/LAB-0408-DRAFT.md reports/lab/stage1-route/Codex-X13.md. Then: git commit -m "lab: draft lab trial text for 0408 (X13)" -m "Builder: Codex". Never add -A. Never commit -a.
9. Push: git push origin returns. If the push is refused, run git pull --rebase origin returns and push once more. Never force push. Never merge into main. If the push fails because there is no network, do not retry. Tell Matthew: "pack X13 committed on this clone, push blocked", give the commit id, and say: run git push origin returns in D:\Git\codex\wf-run\work outside Codex (or turn network access on for Codex and tell me to push).
10. Stop after about 30 minutes, or when done. Stop early on any stop rule on the work page.
11. Tell Matthew "pack X13 pushed" with the commit id and 3 lines on what you found.

MANUAL RETURN (docs/plan/MANUAL-RETURN.md). You run no wf command, so use this block only if a git step fails or a step seems to need wf:
1. Stop. Retry the same command at most once. If it fails again, do not keep trying.
2. Never hand-edit .workshop logs or log.jsonl. Never fake a claim, return, check, or close. Never bypass wf by hand.
3. Record the exact command, exit code, full error text, and the OS.
4. Keep all work inside the allowed files above. Stage files by path only (never add -A, never commit -a). Commit with trailer "Builder: Codex" to returns. Do not write under .workshop/.
5. Write reports/lab/stage1-route/Codex-X13-MANUAL-RETURN.md with: pack X13, builder Codex, the failing step, the error, what was done, files touched, and the commit id. Push to returns. Never force push.
6. If the push fails too, paste that same report to Matthew in one block (last resort only). Nothing closes because of it. Prima reviews it.
```

## X14 (ready, batch 5)

```
Builder: Codex (Matthew's PC, D:\Git\codex\wf-run\work)

Lab pack X14. Do only this one pack. Your brief is docs/plan/WORK-PAGE-2026-11-30.md on prima/build. Everything below is filled in. Nothing is left for you to fill in.
Pack: X14
Lab folder: labs/stage1-route/packs/
Allowed files (your free lane). Write only these:
- labs/stage1-route/packs/LAB-0407-DRAFT.md (new)
- reports/lab/stage1-route/Codex-X14.md (new, your report)
Job: Lab trial pack text for 0407 (tests/lab_0407.rs on 0701).
Done when: Test spec and done-when lines for tests/lab_0407.rs.
Inputs (read only):
- The 0407 and 0701 page logs on origin/packs
- docs/quality/CATCH-LOG.md row 10 on origin/prima/build
Note: Write the test spec and Done-when lines for tests/lab_0407.rs on page 0701. It is the lab trial that 0407.05.01 lacked.

Steps:
0. cd D:\Git\codex\wf-run\work. Check first: git remote -v shows Amalgamour/Workshop, git branch --show-current says returns, and git status --short shows nothing. If not, stop and report.
1. The Codex command line blocks the internet by default. Run: git fetch origin; git pull --ff-only origin returns. If this fails because there is no network, stop. Tell Matthew: "Network access is off. Turn it on for Codex, or run git fetch origin and git pull --ff-only origin returns outside Codex, then start me again." Do not work from old files.
2. Read the brief: git show origin/prima/build:docs/plan/WORK-PAGE-2026-11-30.md. Read the sections "Rules for both", "Stop rules" and "Lanes", then the row for pack X14. You may also read origin/packs and origin/prima/build with git show. Do not check them out.
3. Read the inputs above. If an input that is not marked as your own is missing, stop and tell Matthew which one.
4. Write only the allowed files above. Create a missing lab folder if it is yours.
5. Meet the Done when line. Cite a log entry, or a file and line for every claim. In your report, list: the pack, what you did, files touched, every cite, questions for Matthew, and any stop rule you hit.
6. Put any scope or rule conflict as a question for Matthew. Do not decide it. Pack texts are text files only. Do not pack, sign off or close. Write nothing outside the allowed files.
7. You run no wf command. If anything seems to need wf, stop and write it as a question in your report.
8. Commit by path only: git add -- labs/stage1-route/packs/LAB-0407-DRAFT.md reports/lab/stage1-route/Codex-X14.md. Then: git commit -m "lab: draft lab trial text for 0407 (X14)" -m "Builder: Codex". Never add -A. Never commit -a.
9. Push: git push origin returns. If the push is refused, run git pull --rebase origin returns and push once more. Never force push. Never merge into main. If the push fails because there is no network, do not retry. Tell Matthew: "pack X14 committed on this clone, push blocked", give the commit id, and say: run git push origin returns in D:\Git\codex\wf-run\work outside Codex (or turn network access on for Codex and tell me to push).
10. Stop after about 30 minutes, or when done. Stop early on any stop rule on the work page.
11. Tell Matthew "pack X14 pushed" with the commit id and 3 lines on what you found.

MANUAL RETURN (docs/plan/MANUAL-RETURN.md). You run no wf command, so use this block only if a git step fails or a step seems to need wf:
1. Stop. Retry the same command at most once. If it fails again, do not keep trying.
2. Never hand-edit .workshop logs or log.jsonl. Never fake a claim, return, check, or close. Never bypass wf by hand.
3. Record the exact command, exit code, full error text, and the OS.
4. Keep all work inside the allowed files above. Stage files by path only (never add -A, never commit -a). Commit with trailer "Builder: Codex" to returns. Do not write under .workshop/.
5. Write reports/lab/stage1-route/Codex-X14-MANUAL-RETURN.md with: pack X14, builder Codex, the failing step, the error, what was done, files touched, and the commit id. Push to returns. Never force push.
6. If the push fails too, paste that same report to Matthew in one block (last resort only). Nothing closes because of it. Prima reviews it.
```

## X15 (ready, batch 5)

```
Builder: Codex (Matthew's PC, D:\Git\codex\wf-run\work)

Lab pack X15. Do only this one pack. Your brief is docs/plan/WORK-PAGE-2026-11-30.md on prima/build. Everything below is filled in. Nothing is left for you to fill in.
Pack: X15
Lab folder: labs/0498-accept/
Allowed files (your free lane). Write only these:
- labs/0498-accept/ACCEPTANCE-MAP.md (new)
- reports/lab/0498-accept/Codex-X15.md (new, your report)
Job: Map each of the 11 Stage 1 acceptance items (docs/plan/MVP-GOAL-PROPOSAL.md) to its evidence.
Done when: All 11 items listed. Every item has a source, or is marked missing.
Inputs (read only):
- docs/plan/MVP-GOAL-PROPOSAL.md on origin/prima/build (the 11 Stage 1 acceptance items)
- labs/stage1-route/PAGES.csv (your own)
Note: List all 11 items. Each has a source (file and line, or log entry), or says "missing".

Steps:
0. cd D:\Git\codex\wf-run\work. Check first: git remote -v shows Amalgamour/Workshop, git branch --show-current says returns, and git status --short shows nothing. If not, stop and report.
1. The Codex command line blocks the internet by default. Run: git fetch origin; git pull --ff-only origin returns. If this fails because there is no network, stop. Tell Matthew: "Network access is off. Turn it on for Codex, or run git fetch origin and git pull --ff-only origin returns outside Codex, then start me again." Do not work from old files.
2. Read the brief: git show origin/prima/build:docs/plan/WORK-PAGE-2026-11-30.md. Read the sections "Rules for both", "Stop rules" and "Lanes", then the row for pack X15. You may also read origin/packs and origin/prima/build with git show. Do not check them out.
3. Read the inputs above. If an input that is not marked as your own is missing, stop and tell Matthew which one.
4. Write only the allowed files above. Create a missing lab folder if it is yours.
5. Meet the Done when line. Cite a log entry, or a file and line for every claim. In your report, list: the pack, what you did, files touched, every cite, questions for Matthew, and any stop rule you hit.
6. Put any scope or rule conflict as a question for Matthew. Do not decide it. Pack texts are text files only. Do not pack, sign off or close. Write nothing outside the allowed files.
7. You run no wf command. If anything seems to need wf, stop and write it as a question in your report.
8. Commit by path only: git add -- labs/0498-accept/ACCEPTANCE-MAP.md reports/lab/0498-accept/Codex-X15.md. Then: git commit -m "lab: map the 11 Stage 1 acceptance items to evidence (X15)" -m "Builder: Codex". Never add -A. Never commit -a.
9. Push: git push origin returns. If the push is refused, run git pull --rebase origin returns and push once more. Never force push. Never merge into main. If the push fails because there is no network, do not retry. Tell Matthew: "pack X15 committed on this clone, push blocked", give the commit id, and say: run git push origin returns in D:\Git\codex\wf-run\work outside Codex (or turn network access on for Codex and tell me to push).
10. Stop after about 30 minutes, or when done. Stop early on any stop rule on the work page.
11. Tell Matthew "pack X15 pushed" with the commit id and 3 lines on what you found.

MANUAL RETURN (docs/plan/MANUAL-RETURN.md). You run no wf command, so use this block only if a git step fails or a step seems to need wf:
1. Stop. Retry the same command at most once. If it fails again, do not keep trying.
2. Never hand-edit .workshop logs or log.jsonl. Never fake a claim, return, check, or close. Never bypass wf by hand.
3. Record the exact command, exit code, full error text, and the OS.
4. Keep all work inside the allowed files above. Stage files by path only (never add -A, never commit -a). Commit with trailer "Builder: Codex" to returns. Do not write under .workshop/.
5. Write reports/lab/0498-accept/Codex-X15-MANUAL-RETURN.md with: pack X15, builder Codex, the failing step, the error, what was done, files touched, and the commit id. Push to returns. Never force push.
6. If the push fails too, paste that same report to Matthew in one block (last resort only). Nothing closes because of it. Prima reviews it.
```

## X19 (ready, batch 2)

```
Builder: Codex (Matthew's PC, D:\Git\codex\wf-run\work)

Lab pack X19. Do only this one pack. Your brief is docs/plan/WORK-PAGE-2026-11-30.md on prima/build. Everything below is filled in. Nothing is left for you to fill in.
Pack: X19
Lab folder: labs/log-audit/
Allowed files (your free lane). Write only these:
- labs/log-audit/AUDIT.md (new)
- reports/lab/log-audit/Codex-X19.md (new, your report)
Job: Compare packs and returns logs. List closes that sit only on packs (0403 and others).
Done when: A list, and 2 or 3 fix options for Matthew, each written in four parts.
Inputs (read only):
- Page logs on origin/packs (pages/*/log.jsonl) and origin/returns (.workshop/logs/*/log.jsonl), read with git show
- docs/quality/CATCH-LOG.md row 9 on origin/prima/build
Note: List every close that sits only on packs (0403 and others).
Note: Write 2 or 3 fix options for Matthew. Write each as one question in four parts: Question, Why it matters, Options (A is the default), and What happens if there is no answer. docs/review/FIRE-SALE-2026-11-26-MONDAY-LIST.md, question M1, shows the form.

Steps:
0. cd D:\Git\codex\wf-run\work. Check first: git remote -v shows Amalgamour/Workshop, git branch --show-current says returns, and git status --short shows nothing. If not, stop and report.
1. The Codex command line blocks the internet by default. Run: git fetch origin; git pull --ff-only origin returns. If this fails because there is no network, stop. Tell Matthew: "Network access is off. Turn it on for Codex, or run git fetch origin and git pull --ff-only origin returns outside Codex, then start me again." Do not work from old files.
2. Read the brief: git show origin/prima/build:docs/plan/WORK-PAGE-2026-11-30.md. Read the sections "Rules for both", "Stop rules" and "Lanes", then the row for pack X19. You may also read origin/packs and origin/prima/build with git show. Do not check them out.
3. Read the inputs above. If an input that is not marked as your own is missing, stop and tell Matthew which one.
4. Write only the allowed files above. Create a missing lab folder if it is yours.
5. Meet the Done when line. Cite a log entry, or a file and line for every claim. In your report, list: the pack, what you did, files touched, every cite, questions for Matthew, and any stop rule you hit.
6. Put any scope or rule conflict as a question for Matthew. Do not decide it. Pack texts are text files only. Do not pack, sign off or close. Write nothing outside the allowed files.
7. You run no wf command. If anything seems to need wf, stop and write it as a question in your report.
8. Commit by path only: git add -- labs/log-audit/AUDIT.md reports/lab/log-audit/Codex-X19.md. Then: git commit -m "lab: audit packs logs against returns logs (X19)" -m "Builder: Codex". Never add -A. Never commit -a.
9. Push: git push origin returns. If the push is refused, run git pull --rebase origin returns and push once more. Never force push. Never merge into main. If the push fails because there is no network, do not retry. Tell Matthew: "pack X19 committed on this clone, push blocked", give the commit id, and say: run git push origin returns in D:\Git\codex\wf-run\work outside Codex (or turn network access on for Codex and tell me to push).
10. Stop after about 30 minutes, or when done. Stop early on any stop rule on the work page.
11. Tell Matthew "pack X19 pushed" with the commit id and 3 lines on what you found.

MANUAL RETURN (docs/plan/MANUAL-RETURN.md). You run no wf command, so use this block only if a git step fails or a step seems to need wf:
1. Stop. Retry the same command at most once. If it fails again, do not keep trying.
2. Never hand-edit .workshop logs or log.jsonl. Never fake a claim, return, check, or close. Never bypass wf by hand.
3. Record the exact command, exit code, full error text, and the OS.
4. Keep all work inside the allowed files above. Stage files by path only (never add -A, never commit -a). Commit with trailer "Builder: Codex" to returns. Do not write under .workshop/.
5. Write reports/lab/log-audit/Codex-X19-MANUAL-RETURN.md with: pack X19, builder Codex, the failing step, the error, what was done, files touched, and the commit id. Push to returns. Never force push.
6. If the push fails too, paste that same report to Matthew in one block (last resort only). Nothing closes because of it. Prima reviews it.
```

## X20 (ready, batch 2)

```
Builder: Codex (Matthew's PC, D:\Git\codex\wf-run\work)

Lab pack X20. Do only this one pack. Your brief is docs/plan/WORK-PAGE-2026-11-30.md on prima/build. Everything below is filled in. Nothing is left for you to fill in.
Pack: X20
Lab folder: labs/intake-0001-0403/
Allowed files (your free lane). Write only these:
- labs/intake-0001-0403/CAUSE.md (new)
- reports/lab/intake-0001-0403/Codex-X20.md (new, your report)
Job: Read-only: why does intake always refuse 90.50.00.0001 and 90.50.10.0403?
Done when: Cause, with cites, and 2 or 3 repair options.
Inputs (read only):
- The wf intake code in src/cmd.rs on origin/returns (read only)
- The 90.50.00.0001 and 90.50.10.0403 logs on origin/packs and origin/returns
- docs/quality/CATCH-LOG.md row 9 on origin/prima/build
Note: Read only. Do not run wf, even intake. Give the cause with cites and 2 or 3 repair options. Do not apply any repair.

Steps:
0. cd D:\Git\codex\wf-run\work. Check first: git remote -v shows Amalgamour/Workshop, git branch --show-current says returns, and git status --short shows nothing. If not, stop and report.
1. The Codex command line blocks the internet by default. Run: git fetch origin; git pull --ff-only origin returns. If this fails because there is no network, stop. Tell Matthew: "Network access is off. Turn it on for Codex, or run git fetch origin and git pull --ff-only origin returns outside Codex, then start me again." Do not work from old files.
2. Read the brief: git show origin/prima/build:docs/plan/WORK-PAGE-2026-11-30.md. Read the sections "Rules for both", "Stop rules" and "Lanes", then the row for pack X20. You may also read origin/packs and origin/prima/build with git show. Do not check them out.
3. Read the inputs above. If an input that is not marked as your own is missing, stop and tell Matthew which one.
4. Write only the allowed files above. Create a missing lab folder if it is yours.
5. Meet the Done when line. Cite a log entry, or a file and line for every claim. In your report, list: the pack, what you did, files touched, every cite, questions for Matthew, and any stop rule you hit.
6. Put any scope or rule conflict as a question for Matthew. Do not decide it. Pack texts are text files only. Do not pack, sign off or close. Write nothing outside the allowed files.
7. You run no wf command. If anything seems to need wf, stop and write it as a question in your report.
8. Commit by path only: git add -- labs/intake-0001-0403/CAUSE.md reports/lab/intake-0001-0403/Codex-X20.md. Then: git commit -m "lab: why intake refuses 0001 and 0403 (X20)" -m "Builder: Codex". Never add -A. Never commit -a.
9. Push: git push origin returns. If the push is refused, run git pull --rebase origin returns and push once more. Never force push. Never merge into main. If the push fails because there is no network, do not retry. Tell Matthew: "pack X20 committed on this clone, push blocked", give the commit id, and say: run git push origin returns in D:\Git\codex\wf-run\work outside Codex (or turn network access on for Codex and tell me to push).
10. Stop after about 30 minutes, or when done. Stop early on any stop rule on the work page.
11. Tell Matthew "pack X20 pushed" with the commit id and 3 lines on what you found.

MANUAL RETURN (docs/plan/MANUAL-RETURN.md). You run no wf command, so use this block only if a git step fails or a step seems to need wf:
1. Stop. Retry the same command at most once. If it fails again, do not keep trying.
2. Never hand-edit .workshop logs or log.jsonl. Never fake a claim, return, check, or close. Never bypass wf by hand.
3. Record the exact command, exit code, full error text, and the OS.
4. Keep all work inside the allowed files above. Stage files by path only (never add -A, never commit -a). Commit with trailer "Builder: Codex" to returns. Do not write under .workshop/.
5. Write reports/lab/intake-0001-0403/Codex-X20-MANUAL-RETURN.md with: pack X20, builder Codex, the failing step, the error, what was done, files touched, and the commit id. Push to returns. Never force push.
6. If the push fails too, paste that same report to Matthew in one block (last resort only). Nothing closes because of it. Prima reviews it.
```

## X21 (held, batch 6)

```
Builder: Codex (Matthew's PC, D:\Git\codex\wf-run\work)

Lab pack X21. Do only this one pack. Your brief is docs/plan/WORK-PAGE-2026-11-30.md on prima/build. Everything below is filled in. Nothing is left for you to fill in.
Pack: X21
Lab folder: labs/review-claude-specs/
Allowed files (your free lane). Write only these:
- labs/review-claude-specs/X21-CHECK.md (new)
- reports/lab/review-claude-specs/Codex-X21.md (new, your report)
Job: Hostile check of C4-C9 (pin-record, pin-move, delegated-grant). C8 first: it widens Prima's authority.
Done when: Each spec marked holds, breaks or unclear, with cites. Any widening of authority listed as a question for Matthew.
Inputs (read only):
- labs/pin-record/ (SPEC.md, TEST-PLAN.md), labs/pin-move/ (REHEARSAL.md, RISKS.md), labs/delegated-grant/ (SPEC.md, TEST-PLAN.md): Claude, read only. If any is missing after the pull, stop and tell Matthew which.
Note: Check C8 first: it widens Prima's authority. List every widening as a question for Matthew.
Note: Create labs/review-claude-specs/ if it does not exist.

Steps:
0. cd D:\Git\codex\wf-run\work. Check first: git remote -v shows Amalgamour/Workshop, git branch --show-current says returns, and git status --short shows nothing. If not, stop and report.
1. The Codex command line blocks the internet by default. Run: git fetch origin; git pull --ff-only origin returns. If this fails because there is no network, stop. Tell Matthew: "Network access is off. Turn it on for Codex, or run git fetch origin and git pull --ff-only origin returns outside Codex, then start me again." Do not work from old files.
2. Read the brief: git show origin/prima/build:docs/plan/WORK-PAGE-2026-11-30.md. Read the sections "Rules for both", "Stop rules" and "Lanes", then the row for pack X21. You may also read origin/packs and origin/prima/build with git show. Do not check them out.
3. Read the inputs above. If an input that is not marked as your own is missing, stop and tell Matthew which one.
4. Write only the allowed files above. Create a missing lab folder if it is yours.
5. Meet the Done when line. Cite a log entry, or a file and line for every claim. In your report, list: the pack, what you did, files touched, every cite, questions for Matthew, and any stop rule you hit.
6. Put any scope or rule conflict as a question for Matthew. Do not decide it. Pack texts are text files only. Do not pack, sign off or close. Write nothing outside the allowed files.
7. You run no wf command. If anything seems to need wf, stop and write it as a question in your report.
8. Commit by path only: git add -- labs/review-claude-specs/X21-CHECK.md reports/lab/review-claude-specs/Codex-X21.md. Then: git commit -m "lab: hostile check of Claude C4-C9 (X21)" -m "Builder: Codex". Never add -A. Never commit -a.
9. Push: git push origin returns. If the push is refused, run git pull --rebase origin returns and push once more. Never force push. Never merge into main. If the push fails because there is no network, do not retry. Tell Matthew: "pack X21 committed on this clone, push blocked", give the commit id, and say: run git push origin returns in D:\Git\codex\wf-run\work outside Codex (or turn network access on for Codex and tell me to push).
10. Stop after about 30 minutes, or when done. Stop early on any stop rule on the work page.
11. Tell Matthew "pack X21 pushed" with the commit id and 3 lines on what you found.

MANUAL RETURN (docs/plan/MANUAL-RETURN.md). You run no wf command, so use this block only if a git step fails or a step seems to need wf:
1. Stop. Retry the same command at most once. If it fails again, do not keep trying.
2. Never hand-edit .workshop logs or log.jsonl. Never fake a claim, return, check, or close. Never bypass wf by hand.
3. Record the exact command, exit code, full error text, and the OS.
4. Keep all work inside the allowed files above. Stage files by path only (never add -A, never commit -a). Commit with trailer "Builder: Codex" to returns. Do not write under .workshop/.
5. Write reports/lab/review-claude-specs/Codex-X21-MANUAL-RETURN.md with: pack X21, builder Codex, the failing step, the error, what was done, files touched, and the commit id. Push to returns. Never force push.
6. If the push fails too, paste that same report to Matthew in one block (last resort only). Nothing closes because of it. Prima reviews it.
```

## X22 (held, batch 7)

```
Builder: Codex (Matthew's PC, D:\Git\codex\wf-run\work)

Lab pack X22. Do only this one pack. Your brief is docs/plan/WORK-PAGE-2026-11-30.md on prima/build. Everything below is filled in. Nothing is left for you to fill in.
Pack: X22
Lab folder: labs/review-claude-specs/
Allowed files (your free lane). Write only these:
- labs/review-claude-specs/X22-CHECK.md (new)
- reports/lab/review-claude-specs/Codex-X22.md (new, your report)
Job: Hostile check of C10-C15 (overlap-check, stale-pack, retire-0409).
Done when: Each spec marked holds, breaks or unclear, with cites. Any widening of authority listed as a question for Matthew.
Inputs (read only):
- labs/overlap-check/, labs/stale-pack/, labs/retire-0409/ (Claude, read only). If any file is missing after the pull, stop and tell Matthew which.
Note: Mark each spec holds, breaks or unclear, with cites. List any widening of authority as a question for Matthew.

Steps:
0. cd D:\Git\codex\wf-run\work. Check first: git remote -v shows Amalgamour/Workshop, git branch --show-current says returns, and git status --short shows nothing. If not, stop and report.
1. The Codex command line blocks the internet by default. Run: git fetch origin; git pull --ff-only origin returns. If this fails because there is no network, stop. Tell Matthew: "Network access is off. Turn it on for Codex, or run git fetch origin and git pull --ff-only origin returns outside Codex, then start me again." Do not work from old files.
2. Read the brief: git show origin/prima/build:docs/plan/WORK-PAGE-2026-11-30.md. Read the sections "Rules for both", "Stop rules" and "Lanes", then the row for pack X22. You may also read origin/packs and origin/prima/build with git show. Do not check them out.
3. Read the inputs above. If an input that is not marked as your own is missing, stop and tell Matthew which one.
4. Write only the allowed files above. Create a missing lab folder if it is yours.
5. Meet the Done when line. Cite a log entry, or a file and line for every claim. In your report, list: the pack, what you did, files touched, every cite, questions for Matthew, and any stop rule you hit.
6. Put any scope or rule conflict as a question for Matthew. Do not decide it. Pack texts are text files only. Do not pack, sign off or close. Write nothing outside the allowed files.
7. You run no wf command. If anything seems to need wf, stop and write it as a question in your report.
8. Commit by path only: git add -- labs/review-claude-specs/X22-CHECK.md reports/lab/review-claude-specs/Codex-X22.md. Then: git commit -m "lab: hostile check of Claude C10-C15 (X22)" -m "Builder: Codex". Never add -A. Never commit -a.
9. Push: git push origin returns. If the push is refused, run git pull --rebase origin returns and push once more. Never force push. Never merge into main. If the push fails because there is no network, do not retry. Tell Matthew: "pack X22 committed on this clone, push blocked", give the commit id, and say: run git push origin returns in D:\Git\codex\wf-run\work outside Codex (or turn network access on for Codex and tell me to push).
10. Stop after about 30 minutes, or when done. Stop early on any stop rule on the work page.
11. Tell Matthew "pack X22 pushed" with the commit id and 3 lines on what you found.

MANUAL RETURN (docs/plan/MANUAL-RETURN.md). You run no wf command, so use this block only if a git step fails or a step seems to need wf:
1. Stop. Retry the same command at most once. If it fails again, do not keep trying.
2. Never hand-edit .workshop logs or log.jsonl. Never fake a claim, return, check, or close. Never bypass wf by hand.
3. Record the exact command, exit code, full error text, and the OS.
4. Keep all work inside the allowed files above. Stage files by path only (never add -A, never commit -a). Commit with trailer "Builder: Codex" to returns. Do not write under .workshop/.
5. Write reports/lab/review-claude-specs/Codex-X22-MANUAL-RETURN.md with: pack X22, builder Codex, the failing step, the error, what was done, files touched, and the commit id. Push to returns. Never force push.
6. If the push fails too, paste that same report to Matthew in one block (last resort only). Nothing closes because of it. Prima reviews it.
```

## X23 (held, batch 7)

```
Builder: Codex (Matthew's PC, D:\Git\codex\wf-run\work)

Lab pack X23. Do only this one pack. Your brief is docs/plan/WORK-PAGE-2026-11-30.md on prima/build. Everything below is filled in. Nothing is left for you to fill in.
Pack: X23
Lab folder: labs/review-claude-specs/
Allowed files (your free lane). Write only these:
- labs/review-claude-specs/X23-CHECK.md (new)
- reports/lab/review-claude-specs/Codex-X23.md (new, your report)
Job: Hostile check of C16-C19 (catch-log-flow, prompt-check).
Done when: Each spec marked holds, breaks or unclear, with cites. Any widening of authority listed as a question for Matthew.
Inputs (read only):
- labs/catch-log-flow/ and labs/prompt-check/ (Claude, read only). If any file is missing after the pull, stop and tell Matthew which.
Note: Mark each spec holds, breaks or unclear, with cites. List any widening of authority as a question for Matthew.

Steps:
0. cd D:\Git\codex\wf-run\work. Check first: git remote -v shows Amalgamour/Workshop, git branch --show-current says returns, and git status --short shows nothing. If not, stop and report.
1. The Codex command line blocks the internet by default. Run: git fetch origin; git pull --ff-only origin returns. If this fails because there is no network, stop. Tell Matthew: "Network access is off. Turn it on for Codex, or run git fetch origin and git pull --ff-only origin returns outside Codex, then start me again." Do not work from old files.
2. Read the brief: git show origin/prima/build:docs/plan/WORK-PAGE-2026-11-30.md. Read the sections "Rules for both", "Stop rules" and "Lanes", then the row for pack X23. You may also read origin/packs and origin/prima/build with git show. Do not check them out.
3. Read the inputs above. If an input that is not marked as your own is missing, stop and tell Matthew which one.
4. Write only the allowed files above. Create a missing lab folder if it is yours.
5. Meet the Done when line. Cite a log entry, or a file and line for every claim. In your report, list: the pack, what you did, files touched, every cite, questions for Matthew, and any stop rule you hit.
6. Put any scope or rule conflict as a question for Matthew. Do not decide it. Pack texts are text files only. Do not pack, sign off or close. Write nothing outside the allowed files.
7. You run no wf command. If anything seems to need wf, stop and write it as a question in your report.
8. Commit by path only: git add -- labs/review-claude-specs/X23-CHECK.md reports/lab/review-claude-specs/Codex-X23.md. Then: git commit -m "lab: hostile check of Claude C16-C19 (X23)" -m "Builder: Codex". Never add -A. Never commit -a.
9. Push: git push origin returns. If the push is refused, run git pull --rebase origin returns and push once more. Never force push. Never merge into main. If the push fails because there is no network, do not retry. Tell Matthew: "pack X23 committed on this clone, push blocked", give the commit id, and say: run git push origin returns in D:\Git\codex\wf-run\work outside Codex (or turn network access on for Codex and tell me to push).
10. Stop after about 30 minutes, or when done. Stop early on any stop rule on the work page.
11. Tell Matthew "pack X23 pushed" with the commit id and 3 lines on what you found.

MANUAL RETURN (docs/plan/MANUAL-RETURN.md). You run no wf command, so use this block only if a git step fails or a step seems to need wf:
1. Stop. Retry the same command at most once. If it fails again, do not keep trying.
2. Never hand-edit .workshop logs or log.jsonl. Never fake a claim, return, check, or close. Never bypass wf by hand.
3. Record the exact command, exit code, full error text, and the OS.
4. Keep all work inside the allowed files above. Stage files by path only (never add -A, never commit -a). Commit with trailer "Builder: Codex" to returns. Do not write under .workshop/.
5. Write reports/lab/review-claude-specs/Codex-X23-MANUAL-RETURN.md with: pack X23, builder Codex, the failing step, the error, what was done, files touched, and the commit id. Push to returns. Never force push.
6. If the push fails too, paste that same report to Matthew in one block (last resort only). Nothing closes because of it. Prima reviews it.
```

## X24 (held, batch 6)

```
Builder: Codex (Matthew's PC, D:\Git\codex\wf-run\work)

Lab pack X24. Do only this one pack. Your brief is docs/plan/WORK-PAGE-2026-11-30.md on prima/build. Everything below is filled in. Nothing is left for you to fill in.
Pack: X24
Lab folder: labs/review-claude-specs/
Allowed files (your free lane). Write only these:
- labs/review-claude-specs/X24-CHECK.md (new)
- reports/lab/review-claude-specs/Codex-X24.md (new, your report)
Job: Hostile check of C21 against the UI-1 check (U1-U3).
Done when: Each fix marked holds, breaks or unclear, with cites.
Inputs (read only):
- labs/ui-scaffold/README.md and CONTRACT.md (Claude C21 return, read only)
- reports/lab/ui-scaffold/Claude-C21.md
- docs/review/FIRE-SALE-2026-11-26-UI1-CHECK.md (U1-U3) on origin/prima/build
Note: Mark each of the three fixes holds, breaks or unclear, with the wf file and line.

Steps:
0. cd D:\Git\codex\wf-run\work. Check first: git remote -v shows Amalgamour/Workshop, git branch --show-current says returns, and git status --short shows nothing. If not, stop and report.
1. The Codex command line blocks the internet by default. Run: git fetch origin; git pull --ff-only origin returns. If this fails because there is no network, stop. Tell Matthew: "Network access is off. Turn it on for Codex, or run git fetch origin and git pull --ff-only origin returns outside Codex, then start me again." Do not work from old files.
2. Read the brief: git show origin/prima/build:docs/plan/WORK-PAGE-2026-11-30.md. Read the sections "Rules for both", "Stop rules" and "Lanes", then the row for pack X24. You may also read origin/packs and origin/prima/build with git show. Do not check them out.
3. Read the inputs above. If an input that is not marked as your own is missing, stop and tell Matthew which one.
4. Write only the allowed files above. Create a missing lab folder if it is yours.
5. Meet the Done when line. Cite a log entry, or a file and line for every claim. In your report, list: the pack, what you did, files touched, every cite, questions for Matthew, and any stop rule you hit.
6. Put any scope or rule conflict as a question for Matthew. Do not decide it. Pack texts are text files only. Do not pack, sign off or close. Write nothing outside the allowed files.
7. You run no wf command. If anything seems to need wf, stop and write it as a question in your report.
8. Commit by path only: git add -- labs/review-claude-specs/X24-CHECK.md reports/lab/review-claude-specs/Codex-X24.md. Then: git commit -m "lab: hostile check of Claude C21 (X24)" -m "Builder: Codex". Never add -A. Never commit -a.
9. Push: git push origin returns. If the push is refused, run git pull --rebase origin returns and push once more. Never force push. Never merge into main. If the push fails because there is no network, do not retry. Tell Matthew: "pack X24 committed on this clone, push blocked", give the commit id, and say: run git push origin returns in D:\Git\codex\wf-run\work outside Codex (or turn network access on for Codex and tell me to push).
10. Stop after about 30 minutes, or when done. Stop early on any stop rule on the work page.
11. Tell Matthew "pack X24 pushed" with the commit id and 3 lines on what you found.

MANUAL RETURN (docs/plan/MANUAL-RETURN.md). You run no wf command, so use this block only if a git step fails or a step seems to need wf:
1. Stop. Retry the same command at most once. If it fails again, do not keep trying.
2. Never hand-edit .workshop logs or log.jsonl. Never fake a claim, return, check, or close. Never bypass wf by hand.
3. Record the exact command, exit code, full error text, and the OS.
4. Keep all work inside the allowed files above. Stage files by path only (never add -A, never commit -a). Commit with trailer "Builder: Codex" to returns. Do not write under .workshop/.
5. Write reports/lab/review-claude-specs/Codex-X24-MANUAL-RETURN.md with: pack X24, builder Codex, the failing step, the error, what was done, files touched, and the commit id. Push to returns. Never force push.
6. If the push fails too, paste that same report to Matthew in one block (last resort only). Nothing closes because of it. Prima reviews it.
```
