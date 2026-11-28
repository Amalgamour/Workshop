# Claude lab prompts

One filled prompt per pack. Written by Prima on Sat Nov 28 2026 (t599u). Nothing here has a blank.

Rules for using this file:
- Give Matthew one prompt at a time, in its own code box.
- Release only the packs that the queue file marks "batch 1" until batch 1 is reviewed. Later prompts are written now but are not released. Status and order: docs/plan/queues/CLAUDE-QUEUE.md.
- Each prompt names its fixed report file. Nobody fills in a time.
- A prompt for a held pack says what it waits for in the queue file. Do not release it before that is true.

## C2 (batch 1)

```
Builder: Claude (Matthew's PC, D:\Git\claude\wf-run\work)

Lab pack C2. Do only this one pack. Your brief is docs/plan/WORK-PAGE-2026-11-30.md on prima/build. Everything below is filled in. Nothing is left for you to fill in.
Pack: C2
Lab folder: labs/review-stage1-route/
Allowed files (your free lane). Write only these:
- labs/review-stage1-route/C2-REVIEW.md (new)
- reports/lab/review-stage1-route/Claude-C2.md (new, your report)
Job: Hostile review of Codex's QUEUE.md and QUESTIONS.md. Check that each group really shares no file.
Done when: Same as C1. Each group marked free or clash, with the file.
Inputs (read only):
- labs/stage1-route/QUEUE.md (Codex, read only)
- labs/stage1-route/QUESTIONS.md (Codex, read only)
- labs/review-stage1-route/C1-REVIEW.md (your own C1 return, for the format)
Note: Do not review PAGES.csv. C1 did that, and Codex pack X3 is changing it now.
Note: Group means each group of passes in QUEUE.md that is said to share no file. For each group, open the real file lists (the pack grants on origin/packs) and mark the group free or clash, naming the file.

Steps:
0. cd D:\Git\claude\wf-run\work. Check first: git remote -v shows Amalgamour/Workshop, git branch --show-current says returns, and git status --short shows nothing. If not, stop and report.
1. git fetch origin; git pull --ff-only origin returns.
2. Read the brief: git show origin/prima/build:docs/plan/WORK-PAGE-2026-11-30.md. Read the sections "Rules for both", "Extra rules for Claude", "Stop rules" and "Lanes", then the row for pack C2. You may also read origin/packs and origin/prima/build with git show. Do not check them out.
3. Read the inputs above. If an input that is not marked as your own is missing, stop and tell Matthew which one.
4. Write only the allowed files above. Create a missing lab folder if it is yours.
5. Meet the Done when line. Cite a file and line, or a commit and log entry for every claim. In your report, list: the pack, what you did, files touched, every cite, questions for Matthew, and any stop rule you hit.
6. Put any rule conflict as a question for Matthew. Do not decide it. Do not weaken any rule. You have design and lab authority only. You have no close, signoff or pack authority. Touch no data, logs, tests or Workshop code, and write nothing outside the allowed files (t580u).
7. You run no wf command. If anything seems to need wf, stop and write it as a question in your report.
8. Commit by path only: git add -- labs/review-stage1-route/C2-REVIEW.md reports/lab/review-stage1-route/Claude-C2.md. Then: git commit -m "lab: review Codex QUEUE.md and QUESTIONS.md (C2)" -m "Builder: Claude". Never add -A. Never commit -a.
9. Push: git push origin returns. If the push is refused, run git pull --rebase origin returns and push once more. Never force push. Never merge into main.
10. Stop after about 30 minutes, or when done. Stop early on any stop rule on the work page.
11. Tell Matthew "pack C2 pushed" with the commit id and 3 lines on what you found.

MANUAL RETURN (docs/plan/MANUAL-RETURN.md). You run no wf command, so use this block only if a git step fails or a step seems to need wf:
1. Stop. Retry the same command at most once. If it fails again, do not keep trying.
2. Never hand-edit .workshop logs or log.jsonl. Never fake a claim, return, check, or close. Never bypass wf by hand.
3. Record the exact command, exit code, full error text, and the OS.
4. Keep all work inside the allowed files above. Stage files by path only (never add -A, never commit -a). Commit with trailer "Builder: Claude" to returns. Do not write under .workshop/.
5. Write reports/lab/review-stage1-route/Claude-C2-MANUAL-RETURN.md with: pack C2, builder Claude, the failing step, the error, what was done, files touched, and the commit id. Push to returns. Never force push.
6. If the push fails too, paste that same report to Matthew in one block (last resort only). Nothing closes because of it. Prima reviews it.
```

## C3 (batch 1)

```
Builder: Claude (Matthew's PC, D:\Git\claude\wf-run\work)

Lab pack C3. Do only this one pack. Your brief is docs/plan/WORK-PAGE-2026-11-30.md on prima/build. Everything below is filled in. Nothing is left for you to fill in.
Pack: C3
Lab folder: labs/draft-page/
Allowed files (your free lane). Write only these:
- labs/draft-page/SUMMARY-FOR-MATTHEW.md (new)
- reports/lab/draft-page/Claude-C3.md (new, your report)
Job: SUMMARY-FOR-MATTHEW.md: Q1-Q8 in plain words.
Done when: Each question in 3 lines or less, with its default.
Inputs (read only):
- labs/draft-page/QUESTIONS.md (your own, read only)
- labs/draft-page/README.md (your own, read only)
- Questions 3 to 9 on the work page (they are your Q1, Q3, Q4, Q5, Q6, Q7 and Q8, with page numbers)
Note: Create SUMMARY-FOR-MATTHEW.md only. Do not edit README.md, QUESTIONS.md or TEST-PLAN.md. Codex pack X2 is reviewing them now.
Note: Use the defaults as QUESTIONS.md gives them. Where the work page and QUESTIONS.md name a different default, say so in one line. Do not change any default.
Note: Write in plain words, short lines, one idea per line. Matthew is dyslexic.

Steps:
0. cd D:\Git\claude\wf-run\work. Check first: git remote -v shows Amalgamour/Workshop, git branch --show-current says returns, and git status --short shows nothing. If not, stop and report.
1. git fetch origin; git pull --ff-only origin returns.
2. Read the brief: git show origin/prima/build:docs/plan/WORK-PAGE-2026-11-30.md. Read the sections "Rules for both", "Extra rules for Claude", "Stop rules" and "Lanes", then the row for pack C3. You may also read origin/packs and origin/prima/build with git show. Do not check them out.
3. Read the inputs above. If an input that is not marked as your own is missing, stop and tell Matthew which one.
4. Write only the allowed files above. Create a missing lab folder if it is yours.
5. Meet the Done when line. Cite a file and line, or a commit and log entry for every claim. In your report, list: the pack, what you did, files touched, every cite, questions for Matthew, and any stop rule you hit.
6. Put any rule conflict as a question for Matthew. Do not decide it. Do not weaken any rule. You have design and lab authority only. You have no close, signoff or pack authority. Touch no data, logs, tests or Workshop code, and write nothing outside the allowed files (t580u).
7. You run no wf command. If anything seems to need wf, stop and write it as a question in your report.
8. Commit by path only: git add -- labs/draft-page/SUMMARY-FOR-MATTHEW.md reports/lab/draft-page/Claude-C3.md. Then: git commit -m "lab: plain summary of draft-page Q1-Q8 (C3)" -m "Builder: Claude". Never add -A. Never commit -a.
9. Push: git push origin returns. If the push is refused, run git pull --rebase origin returns and push once more. Never force push. Never merge into main.
10. Stop after about 30 minutes, or when done. Stop early on any stop rule on the work page.
11. Tell Matthew "pack C3 pushed" with the commit id and 3 lines on what you found.

MANUAL RETURN (docs/plan/MANUAL-RETURN.md). You run no wf command, so use this block only if a git step fails or a step seems to need wf:
1. Stop. Retry the same command at most once. If it fails again, do not keep trying.
2. Never hand-edit .workshop logs or log.jsonl. Never fake a claim, return, check, or close. Never bypass wf by hand.
3. Record the exact command, exit code, full error text, and the OS.
4. Keep all work inside the allowed files above. Stage files by path only (never add -A, never commit -a). Commit with trailer "Builder: Claude" to returns. Do not write under .workshop/.
5. Write reports/lab/draft-page/Claude-C3-MANUAL-RETURN.md with: pack C3, builder Claude, the failing step, the error, what was done, files touched, and the commit id. Push to returns. Never force push.
6. If the push fails too, paste that same report to Matthew in one block (last resort only). Nothing closes because of it. Prima reviews it.
```

## C4 (held, batch 3)

```
Builder: Claude (Matthew's PC, D:\Git\claude\wf-run\work)

Lab pack C4. Do only this one pack. Your brief is docs/plan/WORK-PAGE-2026-11-30.md on prima/build. Everything below is filled in. Nothing is left for you to fill in.
Pack: C4
Lab folder: labs/pin-record/
Allowed files (your free lane). Write only these:
- labs/pin-record/SPEC.md (new)
- reports/lab/pin-record/Claude-C4.md (new, your report)
Job: Spec: how the live wf build (the pin) is recorded on the band door 90.50.10.0400.
Done when: Spec names where, who writes it, and what each line holds.
Inputs (read only):
- labs/draft-page/README.md and QUESTIONS.md (your Q2 on the live wf build)
- docs/quality/CATCH-LOG.md on origin/prima/build, row 14 (closed is not live)
- The band door 90.50.10.0400 pages on origin/packs, if present (read only)
Note: Matthew has not answered work page question 2 (where the live wf build is recorded). Write the spec for the default: one line on face 08 of the band door 90.50.10.0400, written by Prima after Matthew approves a pin. Put a short section at the end, 8 lines or fewer, on what changes if he picks option B (each worker config) or C (a new kernel page).

Steps:
0. cd D:\Git\claude\wf-run\work. Check first: git remote -v shows Amalgamour/Workshop, git branch --show-current says returns, and git status --short shows nothing. If not, stop and report.
1. git fetch origin; git pull --ff-only origin returns.
2. Read the brief: git show origin/prima/build:docs/plan/WORK-PAGE-2026-11-30.md. Read the sections "Rules for both", "Extra rules for Claude", "Stop rules" and "Lanes", then the row for pack C4. You may also read origin/packs and origin/prima/build with git show. Do not check them out.
3. Read the inputs above. If an input that is not marked as your own is missing, stop and tell Matthew which one.
4. Write only the allowed files above. Create a missing lab folder if it is yours.
5. Meet the Done when line. Cite a file and line, or a commit and log entry for every claim. In your report, list: the pack, what you did, files touched, every cite, questions for Matthew, and any stop rule you hit.
6. Put any rule conflict as a question for Matthew. Do not decide it. Do not weaken any rule. You have design and lab authority only. You have no close, signoff or pack authority. Touch no data, logs, tests or Workshop code, and write nothing outside the allowed files (t580u).
7. You run no wf command. If anything seems to need wf, stop and write it as a question in your report.
8. Commit by path only: git add -- labs/pin-record/SPEC.md reports/lab/pin-record/Claude-C4.md. Then: git commit -m "lab: spec for recording the live wf pin (C4)" -m "Builder: Claude". Never add -A. Never commit -a.
9. Push: git push origin returns. If the push is refused, run git pull --rebase origin returns and push once more. Never force push. Never merge into main.
10. Stop after about 30 minutes, or when done. Stop early on any stop rule on the work page.
11. Tell Matthew "pack C4 pushed" with the commit id and 3 lines on what you found.

MANUAL RETURN (docs/plan/MANUAL-RETURN.md). You run no wf command, so use this block only if a git step fails or a step seems to need wf:
1. Stop. Retry the same command at most once. If it fails again, do not keep trying.
2. Never hand-edit .workshop logs or log.jsonl. Never fake a claim, return, check, or close. Never bypass wf by hand.
3. Record the exact command, exit code, full error text, and the OS.
4. Keep all work inside the allowed files above. Stage files by path only (never add -A, never commit -a). Commit with trailer "Builder: Claude" to returns. Do not write under .workshop/.
5. Write reports/lab/pin-record/Claude-C4-MANUAL-RETURN.md with: pack C4, builder Claude, the failing step, the error, what was done, files touched, and the commit id. Push to returns. Never force push.
6. If the push fails too, paste that same report to Matthew in one block (last resort only). Nothing closes because of it. Prima reviews it.
```

## C5 (held, batch 3)

```
Builder: Claude (Matthew's PC, D:\Git\claude\wf-run\work)

Lab pack C5. Do only this one pack. Your brief is docs/plan/WORK-PAGE-2026-11-30.md on prima/build. Everything below is filled in. Nothing is left for you to fill in.
Pack: C5
Lab folder: labs/pin-record/
Allowed files (your free lane). Write only these:
- labs/pin-record/TEST-PLAN.md (new)
- reports/lab/pin-record/Claude-C5.md (new, your report)
Job: Test plan for C4.
Done when: At least 5 tests, each with steps and expected result, Windows-safe.
Inputs (read only):
- labs/pin-record/SPEC.md (your C4 return; if it is missing after the pull, stop and tell Matthew)
Note: Every test must run on Windows and on Linux. No test may depend on a path with backslashes only.

Steps:
0. cd D:\Git\claude\wf-run\work. Check first: git remote -v shows Amalgamour/Workshop, git branch --show-current says returns, and git status --short shows nothing. If not, stop and report.
1. git fetch origin; git pull --ff-only origin returns.
2. Read the brief: git show origin/prima/build:docs/plan/WORK-PAGE-2026-11-30.md. Read the sections "Rules for both", "Extra rules for Claude", "Stop rules" and "Lanes", then the row for pack C5. You may also read origin/packs and origin/prima/build with git show. Do not check them out.
3. Read the inputs above. If an input that is not marked as your own is missing, stop and tell Matthew which one.
4. Write only the allowed files above. Create a missing lab folder if it is yours.
5. Meet the Done when line. Cite a file and line, or a commit and log entry for every claim. In your report, list: the pack, what you did, files touched, every cite, questions for Matthew, and any stop rule you hit.
6. Put any rule conflict as a question for Matthew. Do not decide it. Do not weaken any rule. You have design and lab authority only. You have no close, signoff or pack authority. Touch no data, logs, tests or Workshop code, and write nothing outside the allowed files (t580u).
7. You run no wf command. If anything seems to need wf, stop and write it as a question in your report.
8. Commit by path only: git add -- labs/pin-record/TEST-PLAN.md reports/lab/pin-record/Claude-C5.md. Then: git commit -m "lab: test plan for the pin record spec (C5)" -m "Builder: Claude". Never add -A. Never commit -a.
9. Push: git push origin returns. If the push is refused, run git pull --rebase origin returns and push once more. Never force push. Never merge into main.
10. Stop after about 30 minutes, or when done. Stop early on any stop rule on the work page.
11. Tell Matthew "pack C5 pushed" with the commit id and 3 lines on what you found.

MANUAL RETURN (docs/plan/MANUAL-RETURN.md). You run no wf command, so use this block only if a git step fails or a step seems to need wf:
1. Stop. Retry the same command at most once. If it fails again, do not keep trying.
2. Never hand-edit .workshop logs or log.jsonl. Never fake a claim, return, check, or close. Never bypass wf by hand.
3. Record the exact command, exit code, full error text, and the OS.
4. Keep all work inside the allowed files above. Stage files by path only (never add -A, never commit -a). Commit with trailer "Builder: Claude" to returns. Do not write under .workshop/.
5. Write reports/lab/pin-record/Claude-C5-MANUAL-RETURN.md with: pack C5, builder Claude, the failing step, the error, what was done, files touched, and the commit id. Push to returns. Never force push.
6. If the push fails too, paste that same report to Matthew in one block (last resort only). Nothing closes because of it. Prima reviews it.
```

## C6 (held, batch 3)

```
Builder: Claude (Matthew's PC, D:\Git\claude\wf-run\work)

Lab pack C6. Do only this one pack. Your brief is docs/plan/WORK-PAGE-2026-11-30.md on prima/build. Everything below is filled in. Nothing is left for you to fill in.
Pack: C6
Lab folder: labs/pin-move/
Allowed files (your free lane). Write only these:
- labs/pin-move/REHEARSAL.md (new)
- reports/lab/pin-move/Claude-C6.md (new, your report)
Job: Rehearsal plan: move the pin past 0423 as the first recorded switch.
Done when: Steps, checks and who approves each step.
Inputs (read only):
- labs/pin-record/SPEC.md (C4 return; if missing, stop)
- docs/plan/WORK-PAGE-2026-11-26-WEEK.md on origin/prima/build, section "Pin move"
- docs/quality/CATCH-LOG.md row 14 on origin/prima/build
Note: You plan only. You do not move any pin and run no wf command. Matthew approves the pin, and each step names who approves it.

Steps:
0. cd D:\Git\claude\wf-run\work. Check first: git remote -v shows Amalgamour/Workshop, git branch --show-current says returns, and git status --short shows nothing. If not, stop and report.
1. git fetch origin; git pull --ff-only origin returns.
2. Read the brief: git show origin/prima/build:docs/plan/WORK-PAGE-2026-11-30.md. Read the sections "Rules for both", "Extra rules for Claude", "Stop rules" and "Lanes", then the row for pack C6. You may also read origin/packs and origin/prima/build with git show. Do not check them out.
3. Read the inputs above. If an input that is not marked as your own is missing, stop and tell Matthew which one.
4. Write only the allowed files above. Create a missing lab folder if it is yours.
5. Meet the Done when line. Cite a file and line, or a commit and log entry for every claim. In your report, list: the pack, what you did, files touched, every cite, questions for Matthew, and any stop rule you hit.
6. Put any rule conflict as a question for Matthew. Do not decide it. Do not weaken any rule. You have design and lab authority only. You have no close, signoff or pack authority. Touch no data, logs, tests or Workshop code, and write nothing outside the allowed files (t580u).
7. You run no wf command. If anything seems to need wf, stop and write it as a question in your report.
8. Commit by path only: git add -- labs/pin-move/REHEARSAL.md reports/lab/pin-move/Claude-C6.md. Then: git commit -m "lab: rehearsal plan for the first recorded pin move (C6)" -m "Builder: Claude". Never add -A. Never commit -a.
9. Push: git push origin returns. If the push is refused, run git pull --rebase origin returns and push once more. Never force push. Never merge into main.
10. Stop after about 30 minutes, or when done. Stop early on any stop rule on the work page.
11. Tell Matthew "pack C6 pushed" with the commit id and 3 lines on what you found.

MANUAL RETURN (docs/plan/MANUAL-RETURN.md). You run no wf command, so use this block only if a git step fails or a step seems to need wf:
1. Stop. Retry the same command at most once. If it fails again, do not keep trying.
2. Never hand-edit .workshop logs or log.jsonl. Never fake a claim, return, check, or close. Never bypass wf by hand.
3. Record the exact command, exit code, full error text, and the OS.
4. Keep all work inside the allowed files above. Stage files by path only (never add -A, never commit -a). Commit with trailer "Builder: Claude" to returns. Do not write under .workshop/.
5. Write reports/lab/pin-move/Claude-C6-MANUAL-RETURN.md with: pack C6, builder Claude, the failing step, the error, what was done, files touched, and the commit id. Push to returns. Never force push.
6. If the push fails too, paste that same report to Matthew in one block (last resort only). Nothing closes because of it. Prima reviews it.
```

## C7 (held, batch 4)

```
Builder: Claude (Matthew's PC, D:\Git\claude\wf-run\work)

Lab pack C7. Do only this one pack. Your brief is docs/plan/WORK-PAGE-2026-11-30.md on prima/build. Everything below is filled in. Nothing is left for you to fill in.
Pack: C7
Lab folder: labs/pin-move/
Allowed files (your free lane). Write only these:
- labs/pin-move/RISKS.md (new)
- reports/lab/pin-move/Claude-C7.md (new, your report)
Job: Risks and rollback for C6.
Done when: Each risk has a sign to watch for and a way back.
Inputs (read only):
- labs/pin-move/REHEARSAL.md (C6 return; if missing, stop)
Note: Each risk has a sign to watch for and a way back. No way back may need a force push or a hand edit of a log.

Steps:
0. cd D:\Git\claude\wf-run\work. Check first: git remote -v shows Amalgamour/Workshop, git branch --show-current says returns, and git status --short shows nothing. If not, stop and report.
1. git fetch origin; git pull --ff-only origin returns.
2. Read the brief: git show origin/prima/build:docs/plan/WORK-PAGE-2026-11-30.md. Read the sections "Rules for both", "Extra rules for Claude", "Stop rules" and "Lanes", then the row for pack C7. You may also read origin/packs and origin/prima/build with git show. Do not check them out.
3. Read the inputs above. If an input that is not marked as your own is missing, stop and tell Matthew which one.
4. Write only the allowed files above. Create a missing lab folder if it is yours.
5. Meet the Done when line. Cite a file and line, or a commit and log entry for every claim. In your report, list: the pack, what you did, files touched, every cite, questions for Matthew, and any stop rule you hit.
6. Put any rule conflict as a question for Matthew. Do not decide it. Do not weaken any rule. You have design and lab authority only. You have no close, signoff or pack authority. Touch no data, logs, tests or Workshop code, and write nothing outside the allowed files (t580u).
7. You run no wf command. If anything seems to need wf, stop and write it as a question in your report.
8. Commit by path only: git add -- labs/pin-move/RISKS.md reports/lab/pin-move/Claude-C7.md. Then: git commit -m "lab: risks and rollback for the pin move rehearsal (C7)" -m "Builder: Claude". Never add -A. Never commit -a.
9. Push: git push origin returns. If the push is refused, run git pull --rebase origin returns and push once more. Never force push. Never merge into main.
10. Stop after about 30 minutes, or when done. Stop early on any stop rule on the work page.
11. Tell Matthew "pack C7 pushed" with the commit id and 3 lines on what you found.

MANUAL RETURN (docs/plan/MANUAL-RETURN.md). You run no wf command, so use this block only if a git step fails or a step seems to need wf:
1. Stop. Retry the same command at most once. If it fails again, do not keep trying.
2. Never hand-edit .workshop logs or log.jsonl. Never fake a claim, return, check, or close. Never bypass wf by hand.
3. Record the exact command, exit code, full error text, and the OS.
4. Keep all work inside the allowed files above. Stage files by path only (never add -A, never commit -a). Commit with trailer "Builder: Claude" to returns. Do not write under .workshop/.
5. Write reports/lab/pin-move/Claude-C7-MANUAL-RETURN.md with: pack C7, builder Claude, the failing step, the error, what was done, files touched, and the commit id. Push to returns. Never force push.
6. If the push fails too, paste that same report to Matthew in one block (last resort only). Nothing closes because of it. Prima reviews it.
```

## C8 (ready, batch 2)

```
Builder: Claude (Matthew's PC, D:\Git\claude\wf-run\work)

Lab pack C8. Do only this one pack. Your brief is docs/plan/WORK-PAGE-2026-11-30.md on prima/build. Everything below is filled in. Nothing is left for you to fill in.
Pack: C8
Lab folder: labs/delegated-grant/
Allowed files (your free lane). Write only these:
- labs/delegated-grant/SPEC.md (new)
- reports/lab/delegated-grant/Claude-C8.md (new, your report)
Job: Spec for Option C: Matthew records once, on door 0400, that Prima may widen grants inside the approved stage.
Done when: Spec names the record, its scope, and how the log shows "delegated".
Inputs (read only):
- docs/plan/WORK-PAGE-2026-11-26-WEEK.md on origin/prima/build (search for "Option C" and "t584u")
- The grant and set-prime commands in the wf source on returns (src/cmd.rs, read only)
Note: Option C is not decided (t584u). Your spec decides nothing and does not widen any authority by itself. If the spec would widen Prima's authority anywhere, list each place as a question for Matthew.

Steps:
0. cd D:\Git\claude\wf-run\work. Check first: git remote -v shows Amalgamour/Workshop, git branch --show-current says returns, and git status --short shows nothing. If not, stop and report.
1. git fetch origin; git pull --ff-only origin returns.
2. Read the brief: git show origin/prima/build:docs/plan/WORK-PAGE-2026-11-30.md. Read the sections "Rules for both", "Extra rules for Claude", "Stop rules" and "Lanes", then the row for pack C8. You may also read origin/packs and origin/prima/build with git show. Do not check them out.
3. Read the inputs above. If an input that is not marked as your own is missing, stop and tell Matthew which one.
4. Write only the allowed files above. Create a missing lab folder if it is yours.
5. Meet the Done when line. Cite a file and line, or a commit and log entry for every claim. In your report, list: the pack, what you did, files touched, every cite, questions for Matthew, and any stop rule you hit.
6. Put any rule conflict as a question for Matthew. Do not decide it. Do not weaken any rule. You have design and lab authority only. You have no close, signoff or pack authority. Touch no data, logs, tests or Workshop code, and write nothing outside the allowed files (t580u).
7. You run no wf command. If anything seems to need wf, stop and write it as a question in your report.
8. Commit by path only: git add -- labs/delegated-grant/SPEC.md reports/lab/delegated-grant/Claude-C8.md. Then: git commit -m "lab: spec for option C delegated grants (C8)" -m "Builder: Claude". Never add -A. Never commit -a.
9. Push: git push origin returns. If the push is refused, run git pull --rebase origin returns and push once more. Never force push. Never merge into main.
10. Stop after about 30 minutes, or when done. Stop early on any stop rule on the work page.
11. Tell Matthew "pack C8 pushed" with the commit id and 3 lines on what you found.

MANUAL RETURN (docs/plan/MANUAL-RETURN.md). You run no wf command, so use this block only if a git step fails or a step seems to need wf:
1. Stop. Retry the same command at most once. If it fails again, do not keep trying.
2. Never hand-edit .workshop logs or log.jsonl. Never fake a claim, return, check, or close. Never bypass wf by hand.
3. Record the exact command, exit code, full error text, and the OS.
4. Keep all work inside the allowed files above. Stage files by path only (never add -A, never commit -a). Commit with trailer "Builder: Claude" to returns. Do not write under .workshop/.
5. Write reports/lab/delegated-grant/Claude-C8-MANUAL-RETURN.md with: pack C8, builder Claude, the failing step, the error, what was done, files touched, and the commit id. Push to returns. Never force push.
6. If the push fails too, paste that same report to Matthew in one block (last resort only). Nothing closes because of it. Prima reviews it.
```

## C9 (ready, batch 2)

```
Builder: Claude (Matthew's PC, D:\Git\claude\wf-run\work)

Lab pack C9. Do only this one pack. Your brief is docs/plan/WORK-PAGE-2026-11-30.md on prima/build. Everything below is filled in. Nothing is left for you to fill in.
Pack: C9
Lab folder: labs/delegated-grant/
Allowed files (your free lane). Write only these:
- labs/delegated-grant/TEST-PLAN.md (new)
- reports/lab/delegated-grant/Claude-C9.md (new, your report)
Job: Test plan for C8.
Done when: At least 5 tests, including a refusal outside the stage.
Inputs (read only):
- labs/delegated-grant/SPEC.md (C8 return; if missing, stop)
Note: At least 5 tests. One of them must be a refusal outside the approved stage.

Steps:
0. cd D:\Git\claude\wf-run\work. Check first: git remote -v shows Amalgamour/Workshop, git branch --show-current says returns, and git status --short shows nothing. If not, stop and report.
1. git fetch origin; git pull --ff-only origin returns.
2. Read the brief: git show origin/prima/build:docs/plan/WORK-PAGE-2026-11-30.md. Read the sections "Rules for both", "Extra rules for Claude", "Stop rules" and "Lanes", then the row for pack C9. You may also read origin/packs and origin/prima/build with git show. Do not check them out.
3. Read the inputs above. If an input that is not marked as your own is missing, stop and tell Matthew which one.
4. Write only the allowed files above. Create a missing lab folder if it is yours.
5. Meet the Done when line. Cite a file and line, or a commit and log entry for every claim. In your report, list: the pack, what you did, files touched, every cite, questions for Matthew, and any stop rule you hit.
6. Put any rule conflict as a question for Matthew. Do not decide it. Do not weaken any rule. You have design and lab authority only. You have no close, signoff or pack authority. Touch no data, logs, tests or Workshop code, and write nothing outside the allowed files (t580u).
7. You run no wf command. If anything seems to need wf, stop and write it as a question in your report.
8. Commit by path only: git add -- labs/delegated-grant/TEST-PLAN.md reports/lab/delegated-grant/Claude-C9.md. Then: git commit -m "lab: test plan for the delegated grant spec (C9)" -m "Builder: Claude". Never add -A. Never commit -a.
9. Push: git push origin returns. If the push is refused, run git pull --rebase origin returns and push once more. Never force push. Never merge into main.
10. Stop after about 30 minutes, or when done. Stop early on any stop rule on the work page.
11. Tell Matthew "pack C9 pushed" with the commit id and 3 lines on what you found.

MANUAL RETURN (docs/plan/MANUAL-RETURN.md). You run no wf command, so use this block only if a git step fails or a step seems to need wf:
1. Stop. Retry the same command at most once. If it fails again, do not keep trying.
2. Never hand-edit .workshop logs or log.jsonl. Never fake a claim, return, check, or close. Never bypass wf by hand.
3. Record the exact command, exit code, full error text, and the OS.
4. Keep all work inside the allowed files above. Stage files by path only (never add -A, never commit -a). Commit with trailer "Builder: Claude" to returns. Do not write under .workshop/.
5. Write reports/lab/delegated-grant/Claude-C9-MANUAL-RETURN.md with: pack C9, builder Claude, the failing step, the error, what was done, files touched, and the commit id. Push to returns. Never force push.
6. If the push fails too, paste that same report to Matthew in one block (last resort only). Nothing closes because of it. Prima reviews it.
```

## C10 (ready, batch 4)

```
Builder: Claude (Matthew's PC, D:\Git\claude\wf-run\work)

Lab pack C10. Do only this one pack. Your brief is docs/plan/WORK-PAGE-2026-11-30.md on prima/build. Everything below is filled in. Nothing is left for you to fill in.
Pack: C10
Lab folder: labs/overlap-check/
Allowed files (your free lane). Write only these:
- labs/overlap-check/SPEC.md (new)
- reports/lab/overlap-check/Claude-C10.md (new, your report)
Job: Spec: wf checks file overlap across pages (draft-page Q7).
Done when: Spec with 2 or 3 options, each with its cost (files touched, new tests).
Inputs (read only):
- labs/draft-page/QUESTIONS.md, your Q7 (file overlap across pages)
- labs/stage1-route/QUEUE.md (Codex, read only) for real overlap examples
Note: Give 2 or 3 options, each with its cost: files touched and new tests.

Steps:
0. cd D:\Git\claude\wf-run\work. Check first: git remote -v shows Amalgamour/Workshop, git branch --show-current says returns, and git status --short shows nothing. If not, stop and report.
1. git fetch origin; git pull --ff-only origin returns.
2. Read the brief: git show origin/prima/build:docs/plan/WORK-PAGE-2026-11-30.md. Read the sections "Rules for both", "Extra rules for Claude", "Stop rules" and "Lanes", then the row for pack C10. You may also read origin/packs and origin/prima/build with git show. Do not check them out.
3. Read the inputs above. If an input that is not marked as your own is missing, stop and tell Matthew which one.
4. Write only the allowed files above. Create a missing lab folder if it is yours.
5. Meet the Done when line. Cite a file and line, or a commit and log entry for every claim. In your report, list: the pack, what you did, files touched, every cite, questions for Matthew, and any stop rule you hit.
6. Put any rule conflict as a question for Matthew. Do not decide it. Do not weaken any rule. You have design and lab authority only. You have no close, signoff or pack authority. Touch no data, logs, tests or Workshop code, and write nothing outside the allowed files (t580u).
7. You run no wf command. If anything seems to need wf, stop and write it as a question in your report.
8. Commit by path only: git add -- labs/overlap-check/SPEC.md reports/lab/overlap-check/Claude-C10.md. Then: git commit -m "lab: spec for a cross-page file overlap check (C10)" -m "Builder: Claude". Never add -A. Never commit -a.
9. Push: git push origin returns. If the push is refused, run git pull --rebase origin returns and push once more. Never force push. Never merge into main.
10. Stop after about 30 minutes, or when done. Stop early on any stop rule on the work page.
11. Tell Matthew "pack C10 pushed" with the commit id and 3 lines on what you found.

MANUAL RETURN (docs/plan/MANUAL-RETURN.md). You run no wf command, so use this block only if a git step fails or a step seems to need wf:
1. Stop. Retry the same command at most once. If it fails again, do not keep trying.
2. Never hand-edit .workshop logs or log.jsonl. Never fake a claim, return, check, or close. Never bypass wf by hand.
3. Record the exact command, exit code, full error text, and the OS.
4. Keep all work inside the allowed files above. Stage files by path only (never add -A, never commit -a). Commit with trailer "Builder: Claude" to returns. Do not write under .workshop/.
5. Write reports/lab/overlap-check/Claude-C10-MANUAL-RETURN.md with: pack C10, builder Claude, the failing step, the error, what was done, files touched, and the commit id. Push to returns. Never force push.
6. If the push fails too, paste that same report to Matthew in one block (last resort only). Nothing closes because of it. Prima reviews it.
```

## C11 (ready, batch 4)

```
Builder: Claude (Matthew's PC, D:\Git\claude\wf-run\work)

Lab pack C11. Do only this one pack. Your brief is docs/plan/WORK-PAGE-2026-11-30.md on prima/build. Everything below is filled in. Nothing is left for you to fill in.
Pack: C11
Lab folder: labs/overlap-check/
Allowed files (your free lane). Write only these:
- labs/overlap-check/TEST-PLAN.md (new)
- reports/lab/overlap-check/Claude-C11.md (new, your report)
Job: Test plan for C10.
Done when: At least 4 tests.
Inputs (read only):
- labs/overlap-check/SPEC.md (C10 return; if missing, stop)
Note: At least 4 tests.

Steps:
0. cd D:\Git\claude\wf-run\work. Check first: git remote -v shows Amalgamour/Workshop, git branch --show-current says returns, and git status --short shows nothing. If not, stop and report.
1. git fetch origin; git pull --ff-only origin returns.
2. Read the brief: git show origin/prima/build:docs/plan/WORK-PAGE-2026-11-30.md. Read the sections "Rules for both", "Extra rules for Claude", "Stop rules" and "Lanes", then the row for pack C11. You may also read origin/packs and origin/prima/build with git show. Do not check them out.
3. Read the inputs above. If an input that is not marked as your own is missing, stop and tell Matthew which one.
4. Write only the allowed files above. Create a missing lab folder if it is yours.
5. Meet the Done when line. Cite a file and line, or a commit and log entry for every claim. In your report, list: the pack, what you did, files touched, every cite, questions for Matthew, and any stop rule you hit.
6. Put any rule conflict as a question for Matthew. Do not decide it. Do not weaken any rule. You have design and lab authority only. You have no close, signoff or pack authority. Touch no data, logs, tests or Workshop code, and write nothing outside the allowed files (t580u).
7. You run no wf command. If anything seems to need wf, stop and write it as a question in your report.
8. Commit by path only: git add -- labs/overlap-check/TEST-PLAN.md reports/lab/overlap-check/Claude-C11.md. Then: git commit -m "lab: test plan for the overlap check (C11)" -m "Builder: Claude". Never add -A. Never commit -a.
9. Push: git push origin returns. If the push is refused, run git pull --rebase origin returns and push once more. Never force push. Never merge into main.
10. Stop after about 30 minutes, or when done. Stop early on any stop rule on the work page.
11. Tell Matthew "pack C11 pushed" with the commit id and 3 lines on what you found.

MANUAL RETURN (docs/plan/MANUAL-RETURN.md). You run no wf command, so use this block only if a git step fails or a step seems to need wf:
1. Stop. Retry the same command at most once. If it fails again, do not keep trying.
2. Never hand-edit .workshop logs or log.jsonl. Never fake a claim, return, check, or close. Never bypass wf by hand.
3. Record the exact command, exit code, full error text, and the OS.
4. Keep all work inside the allowed files above. Stage files by path only (never add -A, never commit -a). Commit with trailer "Builder: Claude" to returns. Do not write under .workshop/.
5. Write reports/lab/overlap-check/Claude-C11-MANUAL-RETURN.md with: pack C11, builder Claude, the failing step, the error, what was done, files touched, and the commit id. Push to returns. Never force push.
6. If the push fails too, paste that same report to Matthew in one block (last resort only). Nothing closes because of it. Prima reviews it.
```

## C12 (ready, batch 5)

```
Builder: Claude (Matthew's PC, D:\Git\claude\wf-run\work)

Lab pack C12. Do only this one pack. Your brief is docs/plan/WORK-PAGE-2026-11-30.md on prima/build. Everything below is filled in. Nothing is left for you to fill in.
Pack: C12
Lab folder: labs/stale-pack/
Allowed files (your free lane). Write only these:
- labs/stale-pack/SPEC.md (new)
- reports/lab/stale-pack/Claude-C12.md (new, your report)
Job: Spec: refuse a pack whose start is older than the last switch (Q8).
Done when: Spec with 2 or 3 options, each with its cost (files touched, new tests).
Inputs (read only):
- labs/draft-page/QUESTIONS.md, your Q8 (stale pack)
- docs/quality/CATCH-LOG.md row 14 on origin/prima/build
Note: Give 2 or 3 options, each with its cost: files touched and new tests.

Steps:
0. cd D:\Git\claude\wf-run\work. Check first: git remote -v shows Amalgamour/Workshop, git branch --show-current says returns, and git status --short shows nothing. If not, stop and report.
1. git fetch origin; git pull --ff-only origin returns.
2. Read the brief: git show origin/prima/build:docs/plan/WORK-PAGE-2026-11-30.md. Read the sections "Rules for both", "Extra rules for Claude", "Stop rules" and "Lanes", then the row for pack C12. You may also read origin/packs and origin/prima/build with git show. Do not check them out.
3. Read the inputs above. If an input that is not marked as your own is missing, stop and tell Matthew which one.
4. Write only the allowed files above. Create a missing lab folder if it is yours.
5. Meet the Done when line. Cite a file and line, or a commit and log entry for every claim. In your report, list: the pack, what you did, files touched, every cite, questions for Matthew, and any stop rule you hit.
6. Put any rule conflict as a question for Matthew. Do not decide it. Do not weaken any rule. You have design and lab authority only. You have no close, signoff or pack authority. Touch no data, logs, tests or Workshop code, and write nothing outside the allowed files (t580u).
7. You run no wf command. If anything seems to need wf, stop and write it as a question in your report.
8. Commit by path only: git add -- labs/stale-pack/SPEC.md reports/lab/stale-pack/Claude-C12.md. Then: git commit -m "lab: spec for refusing a stale pack (C12)" -m "Builder: Claude". Never add -A. Never commit -a.
9. Push: git push origin returns. If the push is refused, run git pull --rebase origin returns and push once more. Never force push. Never merge into main.
10. Stop after about 30 minutes, or when done. Stop early on any stop rule on the work page.
11. Tell Matthew "pack C12 pushed" with the commit id and 3 lines on what you found.

MANUAL RETURN (docs/plan/MANUAL-RETURN.md). You run no wf command, so use this block only if a git step fails or a step seems to need wf:
1. Stop. Retry the same command at most once. If it fails again, do not keep trying.
2. Never hand-edit .workshop logs or log.jsonl. Never fake a claim, return, check, or close. Never bypass wf by hand.
3. Record the exact command, exit code, full error text, and the OS.
4. Keep all work inside the allowed files above. Stage files by path only (never add -A, never commit -a). Commit with trailer "Builder: Claude" to returns. Do not write under .workshop/.
5. Write reports/lab/stale-pack/Claude-C12-MANUAL-RETURN.md with: pack C12, builder Claude, the failing step, the error, what was done, files touched, and the commit id. Push to returns. Never force push.
6. If the push fails too, paste that same report to Matthew in one block (last resort only). Nothing closes because of it. Prima reviews it.
```

## C13 (ready, batch 5)

```
Builder: Claude (Matthew's PC, D:\Git\claude\wf-run\work)

Lab pack C13. Do only this one pack. Your brief is docs/plan/WORK-PAGE-2026-11-30.md on prima/build. Everything below is filled in. Nothing is left for you to fill in.
Pack: C13
Lab folder: labs/stale-pack/
Allowed files (your free lane). Write only these:
- labs/stale-pack/TEST-PLAN.md (new)
- reports/lab/stale-pack/Claude-C13.md (new, your report)
Job: Test plan for C12.
Done when: At least 4 tests.
Inputs (read only):
- labs/stale-pack/SPEC.md (C12 return; if missing, stop)
Note: At least 4 tests.

Steps:
0. cd D:\Git\claude\wf-run\work. Check first: git remote -v shows Amalgamour/Workshop, git branch --show-current says returns, and git status --short shows nothing. If not, stop and report.
1. git fetch origin; git pull --ff-only origin returns.
2. Read the brief: git show origin/prima/build:docs/plan/WORK-PAGE-2026-11-30.md. Read the sections "Rules for both", "Extra rules for Claude", "Stop rules" and "Lanes", then the row for pack C13. You may also read origin/packs and origin/prima/build with git show. Do not check them out.
3. Read the inputs above. If an input that is not marked as your own is missing, stop and tell Matthew which one.
4. Write only the allowed files above. Create a missing lab folder if it is yours.
5. Meet the Done when line. Cite a file and line, or a commit and log entry for every claim. In your report, list: the pack, what you did, files touched, every cite, questions for Matthew, and any stop rule you hit.
6. Put any rule conflict as a question for Matthew. Do not decide it. Do not weaken any rule. You have design and lab authority only. You have no close, signoff or pack authority. Touch no data, logs, tests or Workshop code, and write nothing outside the allowed files (t580u).
7. You run no wf command. If anything seems to need wf, stop and write it as a question in your report.
8. Commit by path only: git add -- labs/stale-pack/TEST-PLAN.md reports/lab/stale-pack/Claude-C13.md. Then: git commit -m "lab: test plan for the stale pack check (C13)" -m "Builder: Claude". Never add -A. Never commit -a.
9. Push: git push origin returns. If the push is refused, run git pull --rebase origin returns and push once more. Never force push. Never merge into main.
10. Stop after about 30 minutes, or when done. Stop early on any stop rule on the work page.
11. Tell Matthew "pack C13 pushed" with the commit id and 3 lines on what you found.

MANUAL RETURN (docs/plan/MANUAL-RETURN.md). You run no wf command, so use this block only if a git step fails or a step seems to need wf:
1. Stop. Retry the same command at most once. If it fails again, do not keep trying.
2. Never hand-edit .workshop logs or log.jsonl. Never fake a claim, return, check, or close. Never bypass wf by hand.
3. Record the exact command, exit code, full error text, and the OS.
4. Keep all work inside the allowed files above. Stage files by path only (never add -A, never commit -a). Commit with trailer "Builder: Claude" to returns. Do not write under .workshop/.
5. Write reports/lab/stale-pack/Claude-C13-MANUAL-RETURN.md with: pack C13, builder Claude, the failing step, the error, what was done, files touched, and the commit id. Push to returns. Never force push.
6. If the push fails too, paste that same report to Matthew in one block (last resort only). Nothing closes because of it. Prima reviews it.
```

## C14 (ready, batch 5)

```
Builder: Claude (Matthew's PC, D:\Git\claude\wf-run\work)

Lab pack C14. Do only this one pack. Your brief is docs/plan/WORK-PAGE-2026-11-30.md on prima/build. Everything below is filled in. Nothing is left for you to fill in.
Pack: C14
Lab folder: labs/retire-0409/
Allowed files (your free lane). Write only these:
- labs/retire-0409/OPTIONS.md (new)
- reports/lab/retire-0409/Claude-C14.md (new, your report)
Job: Options for 0409 (retire a page), to help Matthew decide Codex Q1.
Done when: 2 or 3 options, each with cost and what it unblocks.
Inputs (read only):
- labs/stage1-route/QUESTIONS.md, Q1 on 0409 (Codex, read only)
- labs/stage1-route/QUEUE.md (Codex, read only)
Note: This helps Matthew decide work page question 1. Do not decide it. Mark your preferred option, but make clear that Matthew decides.

Steps:
0. cd D:\Git\claude\wf-run\work. Check first: git remote -v shows Amalgamour/Workshop, git branch --show-current says returns, and git status --short shows nothing. If not, stop and report.
1. git fetch origin; git pull --ff-only origin returns.
2. Read the brief: git show origin/prima/build:docs/plan/WORK-PAGE-2026-11-30.md. Read the sections "Rules for both", "Extra rules for Claude", "Stop rules" and "Lanes", then the row for pack C14. You may also read origin/packs and origin/prima/build with git show. Do not check them out.
3. Read the inputs above. If an input that is not marked as your own is missing, stop and tell Matthew which one.
4. Write only the allowed files above. Create a missing lab folder if it is yours.
5. Meet the Done when line. Cite a file and line, or a commit and log entry for every claim. In your report, list: the pack, what you did, files touched, every cite, questions for Matthew, and any stop rule you hit.
6. Put any rule conflict as a question for Matthew. Do not decide it. Do not weaken any rule. You have design and lab authority only. You have no close, signoff or pack authority. Touch no data, logs, tests or Workshop code, and write nothing outside the allowed files (t580u).
7. You run no wf command. If anything seems to need wf, stop and write it as a question in your report.
8. Commit by path only: git add -- labs/retire-0409/OPTIONS.md reports/lab/retire-0409/Claude-C14.md. Then: git commit -m "lab: options for retiring page 0409 (C14)" -m "Builder: Claude". Never add -A. Never commit -a.
9. Push: git push origin returns. If the push is refused, run git pull --rebase origin returns and push once more. Never force push. Never merge into main.
10. Stop after about 30 minutes, or when done. Stop early on any stop rule on the work page.
11. Tell Matthew "pack C14 pushed" with the commit id and 3 lines on what you found.

MANUAL RETURN (docs/plan/MANUAL-RETURN.md). You run no wf command, so use this block only if a git step fails or a step seems to need wf:
1. Stop. Retry the same command at most once. If it fails again, do not keep trying.
2. Never hand-edit .workshop logs or log.jsonl. Never fake a claim, return, check, or close. Never bypass wf by hand.
3. Record the exact command, exit code, full error text, and the OS.
4. Keep all work inside the allowed files above. Stage files by path only (never add -A, never commit -a). Commit with trailer "Builder: Claude" to returns. Do not write under .workshop/.
5. Write reports/lab/retire-0409/Claude-C14-MANUAL-RETURN.md with: pack C14, builder Claude, the failing step, the error, what was done, files touched, and the commit id. Push to returns. Never force push.
6. If the push fails too, paste that same report to Matthew in one block (last resort only). Nothing closes because of it. Prima reviews it.
```

## C15 (ready, batch 6)

```
Builder: Claude (Matthew's PC, D:\Git\claude\wf-run\work)

Lab pack C15. Do only this one pack. Your brief is docs/plan/WORK-PAGE-2026-11-30.md on prima/build. Everything below is filled in. Nothing is left for you to fill in.
Pack: C15
Lab folder: labs/retire-0409/
Allowed files (your free lane). Write only these:
- labs/retire-0409/TEST-IDEAS.md (new)
- reports/lab/retire-0409/Claude-C15.md (new, your report)
Job: Test ideas for 0409 if it stays on the route.
Done when: At least 4 tests.
Inputs (read only):
- labs/retire-0409/OPTIONS.md (C14 return; if missing, stop)
Note: At least 4 tests.

Steps:
0. cd D:\Git\claude\wf-run\work. Check first: git remote -v shows Amalgamour/Workshop, git branch --show-current says returns, and git status --short shows nothing. If not, stop and report.
1. git fetch origin; git pull --ff-only origin returns.
2. Read the brief: git show origin/prima/build:docs/plan/WORK-PAGE-2026-11-30.md. Read the sections "Rules for both", "Extra rules for Claude", "Stop rules" and "Lanes", then the row for pack C15. You may also read origin/packs and origin/prima/build with git show. Do not check them out.
3. Read the inputs above. If an input that is not marked as your own is missing, stop and tell Matthew which one.
4. Write only the allowed files above. Create a missing lab folder if it is yours.
5. Meet the Done when line. Cite a file and line, or a commit and log entry for every claim. In your report, list: the pack, what you did, files touched, every cite, questions for Matthew, and any stop rule you hit.
6. Put any rule conflict as a question for Matthew. Do not decide it. Do not weaken any rule. You have design and lab authority only. You have no close, signoff or pack authority. Touch no data, logs, tests or Workshop code, and write nothing outside the allowed files (t580u).
7. You run no wf command. If anything seems to need wf, stop and write it as a question in your report.
8. Commit by path only: git add -- labs/retire-0409/TEST-IDEAS.md reports/lab/retire-0409/Claude-C15.md. Then: git commit -m "lab: test ideas if 0409 stays on the route (C15)" -m "Builder: Claude". Never add -A. Never commit -a.
9. Push: git push origin returns. If the push is refused, run git pull --rebase origin returns and push once more. Never force push. Never merge into main.
10. Stop after about 30 minutes, or when done. Stop early on any stop rule on the work page.
11. Tell Matthew "pack C15 pushed" with the commit id and 3 lines on what you found.

MANUAL RETURN (docs/plan/MANUAL-RETURN.md). You run no wf command, so use this block only if a git step fails or a step seems to need wf:
1. Stop. Retry the same command at most once. If it fails again, do not keep trying.
2. Never hand-edit .workshop logs or log.jsonl. Never fake a claim, return, check, or close. Never bypass wf by hand.
3. Record the exact command, exit code, full error text, and the OS.
4. Keep all work inside the allowed files above. Stage files by path only (never add -A, never commit -a). Commit with trailer "Builder: Claude" to returns. Do not write under .workshop/.
5. Write reports/lab/retire-0409/Claude-C15-MANUAL-RETURN.md with: pack C15, builder Claude, the failing step, the error, what was done, files touched, and the commit id. Push to returns. Never force push.
6. If the push fails too, paste that same report to Matthew in one block (last resort only). Nothing closes because of it. Prima reviews it.
```

## C16 (ready, batch 6)

```
Builder: Claude (Matthew's PC, D:\Git\claude\wf-run\work)

Lab pack C16. Do only this one pack. Your brief is docs/plan/WORK-PAGE-2026-11-30.md on prima/build. Everything below is filled in. Nothing is left for you to fill in.
Pack: C16
Lab folder: labs/catch-log-flow/
Allowed files (your free lane). Write only these:
- labs/catch-log-flow/TEMPLATE.md (new)
- reports/lab/catch-log-flow/Claude-C16.md (new, your report)
Job: How a checker turns a check report into a catch-log row (docs/quality/CATCH-LOG.md on prima/build).
Done when: A fill-in template, field by field.
Inputs (read only):
- docs/quality/CATCH-LOG.md on origin/prima/build (read the header and the 11 columns)
- docs/plan/REPORTS.md on origin/prima/build
Note: The template is field by field, one line per column, with what to copy from the check report into each.

Steps:
0. cd D:\Git\claude\wf-run\work. Check first: git remote -v shows Amalgamour/Workshop, git branch --show-current says returns, and git status --short shows nothing. If not, stop and report.
1. git fetch origin; git pull --ff-only origin returns.
2. Read the brief: git show origin/prima/build:docs/plan/WORK-PAGE-2026-11-30.md. Read the sections "Rules for both", "Extra rules for Claude", "Stop rules" and "Lanes", then the row for pack C16. You may also read origin/packs and origin/prima/build with git show. Do not check them out.
3. Read the inputs above. If an input that is not marked as your own is missing, stop and tell Matthew which one.
4. Write only the allowed files above. Create a missing lab folder if it is yours.
5. Meet the Done when line. Cite a file and line, or a commit and log entry for every claim. In your report, list: the pack, what you did, files touched, every cite, questions for Matthew, and any stop rule you hit.
6. Put any rule conflict as a question for Matthew. Do not decide it. Do not weaken any rule. You have design and lab authority only. You have no close, signoff or pack authority. Touch no data, logs, tests or Workshop code, and write nothing outside the allowed files (t580u).
7. You run no wf command. If anything seems to need wf, stop and write it as a question in your report.
8. Commit by path only: git add -- labs/catch-log-flow/TEMPLATE.md reports/lab/catch-log-flow/Claude-C16.md. Then: git commit -m "lab: catch log row template from a check report (C16)" -m "Builder: Claude". Never add -A. Never commit -a.
9. Push: git push origin returns. If the push is refused, run git pull --rebase origin returns and push once more. Never force push. Never merge into main.
10. Stop after about 30 minutes, or when done. Stop early on any stop rule on the work page.
11. Tell Matthew "pack C16 pushed" with the commit id and 3 lines on what you found.

MANUAL RETURN (docs/plan/MANUAL-RETURN.md). You run no wf command, so use this block only if a git step fails or a step seems to need wf:
1. Stop. Retry the same command at most once. If it fails again, do not keep trying.
2. Never hand-edit .workshop logs or log.jsonl. Never fake a claim, return, check, or close. Never bypass wf by hand.
3. Record the exact command, exit code, full error text, and the OS.
4. Keep all work inside the allowed files above. Stage files by path only (never add -A, never commit -a). Commit with trailer "Builder: Claude" to returns. Do not write under .workshop/.
5. Write reports/lab/catch-log-flow/Claude-C16-MANUAL-RETURN.md with: pack C16, builder Claude, the failing step, the error, what was done, files touched, and the commit id. Push to returns. Never force push.
6. If the push fails too, paste that same report to Matthew in one block (last resort only). Nothing closes because of it. Prima reviews it.
```

## C17 (ready, batch 6)

```
Builder: Claude (Matthew's PC, D:\Git\claude\wf-run\work)

Lab pack C17. Do only this one pack. Your brief is docs/plan/WORK-PAGE-2026-11-30.md on prima/build. Everything below is filled in. Nothing is left for you to fill in.
Pack: C17
Lab folder: labs/catch-log-flow/
Allowed files (your free lane). Write only these:
- labs/catch-log-flow/EXAMPLES.md (new)
- reports/lab/catch-log-flow/Claude-C17.md (new, your report)
Job: Two worked examples from real checks in the week of Nov 23.
Done when: Both examples cite their check entry.
Inputs (read only):
- labs/catch-log-flow/TEMPLATE.md (C16 return; if missing, stop)
- Check reports under reports/ on returns and the page logs, from the week of Nov 23
Note: Use two real checks. Each example cites its check log entry.

Steps:
0. cd D:\Git\claude\wf-run\work. Check first: git remote -v shows Amalgamour/Workshop, git branch --show-current says returns, and git status --short shows nothing. If not, stop and report.
1. git fetch origin; git pull --ff-only origin returns.
2. Read the brief: git show origin/prima/build:docs/plan/WORK-PAGE-2026-11-30.md. Read the sections "Rules for both", "Extra rules for Claude", "Stop rules" and "Lanes", then the row for pack C17. You may also read origin/packs and origin/prima/build with git show. Do not check them out.
3. Read the inputs above. If an input that is not marked as your own is missing, stop and tell Matthew which one.
4. Write only the allowed files above. Create a missing lab folder if it is yours.
5. Meet the Done when line. Cite a file and line, or a commit and log entry for every claim. In your report, list: the pack, what you did, files touched, every cite, questions for Matthew, and any stop rule you hit.
6. Put any rule conflict as a question for Matthew. Do not decide it. Do not weaken any rule. You have design and lab authority only. You have no close, signoff or pack authority. Touch no data, logs, tests or Workshop code, and write nothing outside the allowed files (t580u).
7. You run no wf command. If anything seems to need wf, stop and write it as a question in your report.
8. Commit by path only: git add -- labs/catch-log-flow/EXAMPLES.md reports/lab/catch-log-flow/Claude-C17.md. Then: git commit -m "lab: two worked catch log examples (C17)" -m "Builder: Claude". Never add -A. Never commit -a.
9. Push: git push origin returns. If the push is refused, run git pull --rebase origin returns and push once more. Never force push. Never merge into main.
10. Stop after about 30 minutes, or when done. Stop early on any stop rule on the work page.
11. Tell Matthew "pack C17 pushed" with the commit id and 3 lines on what you found.

MANUAL RETURN (docs/plan/MANUAL-RETURN.md). You run no wf command, so use this block only if a git step fails or a step seems to need wf:
1. Stop. Retry the same command at most once. If it fails again, do not keep trying.
2. Never hand-edit .workshop logs or log.jsonl. Never fake a claim, return, check, or close. Never bypass wf by hand.
3. Record the exact command, exit code, full error text, and the OS.
4. Keep all work inside the allowed files above. Stage files by path only (never add -A, never commit -a). Commit with trailer "Builder: Claude" to returns. Do not write under .workshop/.
5. Write reports/lab/catch-log-flow/Claude-C17-MANUAL-RETURN.md with: pack C17, builder Claude, the failing step, the error, what was done, files touched, and the commit id. Push to returns. Never force push.
6. If the push fails too, paste that same report to Matthew in one block (last resort only). Nothing closes because of it. Prima reviews it.
```

## C18 (ready, batch 7)

```
Builder: Claude (Matthew's PC, D:\Git\claude\wf-run\work)

Lab pack C18. Do only this one pack. Your brief is docs/plan/WORK-PAGE-2026-11-30.md on prima/build. Everything below is filled in. Nothing is left for you to fill in.
Pack: C18
Lab folder: labs/prompt-check/
Allowed files (your free lane). Write only these:
- labs/prompt-check/CHECKLIST.md (new)
- reports/lab/prompt-check/Claude-C18.md (new, your report)
Job: A checklist of prompt mistakes, from the prompts of the week of Nov 23 and catch log rows 12, 13 and 17.
Done when: Each item has an example and how to catch it.
Inputs (read only):
- docs/plan/WORK-PAGE-2026-11-25.md on origin/prima/build (the prompts of that week)
- docs/quality/CATCH-LOG.md rows 12, 13 and 17 on origin/prima/build
Note: Each checklist item has a real example and a way to catch it, such as a search for an unfilled field.

Steps:
0. cd D:\Git\claude\wf-run\work. Check first: git remote -v shows Amalgamour/Workshop, git branch --show-current says returns, and git status --short shows nothing. If not, stop and report.
1. git fetch origin; git pull --ff-only origin returns.
2. Read the brief: git show origin/prima/build:docs/plan/WORK-PAGE-2026-11-30.md. Read the sections "Rules for both", "Extra rules for Claude", "Stop rules" and "Lanes", then the row for pack C18. You may also read origin/packs and origin/prima/build with git show. Do not check them out.
3. Read the inputs above. If an input that is not marked as your own is missing, stop and tell Matthew which one.
4. Write only the allowed files above. Create a missing lab folder if it is yours.
5. Meet the Done when line. Cite a file and line, or a commit and log entry for every claim. In your report, list: the pack, what you did, files touched, every cite, questions for Matthew, and any stop rule you hit.
6. Put any rule conflict as a question for Matthew. Do not decide it. Do not weaken any rule. You have design and lab authority only. You have no close, signoff or pack authority. Touch no data, logs, tests or Workshop code, and write nothing outside the allowed files (t580u).
7. You run no wf command. If anything seems to need wf, stop and write it as a question in your report.
8. Commit by path only: git add -- labs/prompt-check/CHECKLIST.md reports/lab/prompt-check/Claude-C18.md. Then: git commit -m "lab: checklist of prompt mistakes (C18)" -m "Builder: Claude". Never add -A. Never commit -a.
9. Push: git push origin returns. If the push is refused, run git pull --rebase origin returns and push once more. Never force push. Never merge into main.
10. Stop after about 30 minutes, or when done. Stop early on any stop rule on the work page.
11. Tell Matthew "pack C18 pushed" with the commit id and 3 lines on what you found.

MANUAL RETURN (docs/plan/MANUAL-RETURN.md). You run no wf command, so use this block only if a git step fails or a step seems to need wf:
1. Stop. Retry the same command at most once. If it fails again, do not keep trying.
2. Never hand-edit .workshop logs or log.jsonl. Never fake a claim, return, check, or close. Never bypass wf by hand.
3. Record the exact command, exit code, full error text, and the OS.
4. Keep all work inside the allowed files above. Stage files by path only (never add -A, never commit -a). Commit with trailer "Builder: Claude" to returns. Do not write under .workshop/.
5. Write reports/lab/prompt-check/Claude-C18-MANUAL-RETURN.md with: pack C18, builder Claude, the failing step, the error, what was done, files touched, and the commit id. Push to returns. Never force push.
6. If the push fails too, paste that same report to Matthew in one block (last resort only). Nothing closes because of it. Prima reviews it.
```

## C19 (ready, batch 7)

```
Builder: Claude (Matthew's PC, D:\Git\claude\wf-run\work)

Lab pack C19. Do only this one pack. Your brief is docs/plan/WORK-PAGE-2026-11-30.md on prima/build. Everything below is filled in. Nothing is left for you to fill in.
Pack: C19
Lab folder: labs/prompt-check/
Allowed files (your free lane). Write only these:
- labs/prompt-check/RUN-C18.md (new)
- reports/lab/prompt-check/Claude-C19.md (new, your report)
Job: Run the C18 checklist against the 6 prompts on WORK-PAGE-2026-11-25.md (A1-A4, B1, B2).
Done when: A table: prompt, item, pass or fail, with all 6 prompts present.
Inputs (read only):
- labs/prompt-check/CHECKLIST.md (C18 return; if missing, stop)
- docs/plan/WORK-PAGE-2026-11-25.md on origin/prima/build: prompts A1, A2, A3, A4, B1 and B2
Note: All 6 prompts must be in your table.

Steps:
0. cd D:\Git\claude\wf-run\work. Check first: git remote -v shows Amalgamour/Workshop, git branch --show-current says returns, and git status --short shows nothing. If not, stop and report.
1. git fetch origin; git pull --ff-only origin returns.
2. Read the brief: git show origin/prima/build:docs/plan/WORK-PAGE-2026-11-30.md. Read the sections "Rules for both", "Extra rules for Claude", "Stop rules" and "Lanes", then the row for pack C19. You may also read origin/packs and origin/prima/build with git show. Do not check them out.
3. Read the inputs above. If an input that is not marked as your own is missing, stop and tell Matthew which one.
4. Write only the allowed files above. Create a missing lab folder if it is yours.
5. Meet the Done when line. Cite a file and line, or a commit and log entry for every claim. In your report, list: the pack, what you did, files touched, every cite, questions for Matthew, and any stop rule you hit.
6. Put any rule conflict as a question for Matthew. Do not decide it. Do not weaken any rule. You have design and lab authority only. You have no close, signoff or pack authority. Touch no data, logs, tests or Workshop code, and write nothing outside the allowed files (t580u).
7. You run no wf command. If anything seems to need wf, stop and write it as a question in your report.
8. Commit by path only: git add -- labs/prompt-check/RUN-C18.md reports/lab/prompt-check/Claude-C19.md. Then: git commit -m "lab: run the prompt checklist on 6 prompts (C19)" -m "Builder: Claude". Never add -A. Never commit -a.
9. Push: git push origin returns. If the push is refused, run git pull --rebase origin returns and push once more. Never force push. Never merge into main.
10. Stop after about 30 minutes, or when done. Stop early on any stop rule on the work page.
11. Tell Matthew "pack C19 pushed" with the commit id and 3 lines on what you found.

MANUAL RETURN (docs/plan/MANUAL-RETURN.md). You run no wf command, so use this block only if a git step fails or a step seems to need wf:
1. Stop. Retry the same command at most once. If it fails again, do not keep trying.
2. Never hand-edit .workshop logs or log.jsonl. Never fake a claim, return, check, or close. Never bypass wf by hand.
3. Record the exact command, exit code, full error text, and the OS.
4. Keep all work inside the allowed files above. Stage files by path only (never add -A, never commit -a). Commit with trailer "Builder: Claude" to returns. Do not write under .workshop/.
5. Write reports/lab/prompt-check/Claude-C19-MANUAL-RETURN.md with: pack C19, builder Claude, the failing step, the error, what was done, files touched, and the commit id. Push to returns. Never force push.
6. If the push fails too, paste that same report to Matthew in one block (last resort only). Nothing closes because of it. Prima reviews it.
```

## C20 (ready, batch 2)

```
Builder: Claude (Matthew's PC, D:\Git\claude\wf-run\work)

Lab pack C20. Do only this one pack. Your brief is docs/plan/WORK-PAGE-2026-11-30.md on prima/build. Everything below is filled in. Nothing is left for you to fill in.
Pack: C20
Lab folder: labs/draft-page/
Allowed files (your free lane). Write only these:
- labs/draft-page/RESPONSE.md (new)
- reports/lab/draft-page/Claude-C20.md (new, your report)
Job: RESPONSE.md: answer Codex's hostile review (X1-X2). Accept or dispute each finding. Prima rules on each dispute.
Done when: Every finding answered with a cite. No rule weakened. Each dispute listed for Prima's ruling; any reversal goes in the catch log (written by Prima, not Claude).
Inputs (read only):
- labs/review-draft-page/X1-README-REVIEW.md (Codex)
- labs/review-draft-page/X2-REVIEW.md (Codex X2 return; if missing after the pull, stop and tell Matthew X2 has not returned)
- Your own labs/draft-page/README.md, QUESTIONS.md and TEST-PLAN.md (read only)
Note: Create RESPONSE.md only. Do not edit your earlier files.
Note: Prima rules on each dispute. List every dispute for Prima. Do not weaken any rule to make a dispute go away. A reversal goes in the catch log, and Prima writes that row, not you.

Steps:
0. cd D:\Git\claude\wf-run\work. Check first: git remote -v shows Amalgamour/Workshop, git branch --show-current says returns, and git status --short shows nothing. If not, stop and report.
1. git fetch origin; git pull --ff-only origin returns.
2. Read the brief: git show origin/prima/build:docs/plan/WORK-PAGE-2026-11-30.md. Read the sections "Rules for both", "Extra rules for Claude", "Stop rules" and "Lanes", then the row for pack C20. You may also read origin/packs and origin/prima/build with git show. Do not check them out.
3. Read the inputs above. If an input that is not marked as your own is missing, stop and tell Matthew which one.
4. Write only the allowed files above. Create a missing lab folder if it is yours.
5. Meet the Done when line. Cite a file and line, or a commit and log entry for every claim. In your report, list: the pack, what you did, files touched, every cite, questions for Matthew, and any stop rule you hit.
6. Put any rule conflict as a question for Matthew. Do not decide it. Do not weaken any rule. You have design and lab authority only. You have no close, signoff or pack authority. Touch no data, logs, tests or Workshop code, and write nothing outside the allowed files (t580u).
7. You run no wf command. If anything seems to need wf, stop and write it as a question in your report.
8. Commit by path only: git add -- labs/draft-page/RESPONSE.md reports/lab/draft-page/Claude-C20.md. Then: git commit -m "lab: answer Codex X1 and X2 reviews (C20)" -m "Builder: Claude". Never add -A. Never commit -a.
9. Push: git push origin returns. If the push is refused, run git pull --rebase origin returns and push once more. Never force push. Never merge into main.
10. Stop after about 30 minutes, or when done. Stop early on any stop rule on the work page.
11. Tell Matthew "pack C20 pushed" with the commit id and 3 lines on what you found.

MANUAL RETURN (docs/plan/MANUAL-RETURN.md). You run no wf command, so use this block only if a git step fails or a step seems to need wf:
1. Stop. Retry the same command at most once. If it fails again, do not keep trying.
2. Never hand-edit .workshop logs or log.jsonl. Never fake a claim, return, check, or close. Never bypass wf by hand.
3. Record the exact command, exit code, full error text, and the OS.
4. Keep all work inside the allowed files above. Stage files by path only (never add -A, never commit -a). Commit with trailer "Builder: Claude" to returns. Do not write under .workshop/.
5. Write reports/lab/draft-page/Claude-C20-MANUAL-RETURN.md with: pack C20, builder Claude, the failing step, the error, what was done, files touched, and the commit id. Push to returns. Never force push.
6. If the push fails too, paste that same report to Matthew in one block (last resort only). Nothing closes because of it. Prima reviews it.
```

## C21 (batch 1)

```
Builder: Claude (Matthew's PC, D:\Git\claude\wf-run\work)

Lab pack C21. Do only this one pack. Your brief is docs/plan/WORK-PAGE-2026-11-30.md on prima/build. Everything below is filled in. Nothing is left for you to fill in.
Pack: C21
Lab folder: labs/ui-scaffold/
Allowed files (your free lane). Write only these:
- labs/ui-scaffold/README.md (edit)
- labs/ui-scaffold/CONTRACT.md (edit)
- reports/lab/ui-scaffold/Claude-C21.md (new, your report)
Job: Fix U1-U3 from the independent check of UI-1 (docs/review/FIRE-SALE-2026-11-26-UI1-CHECK.md): drop the invented "pending" card state; do not mark the job step "missing" before close; drop the stale "ids not checked" line.
Done when: Each fix cites the wf file and line it now matches. Nothing outside labs/ui-scaffold/ changes.
Inputs (read only):
- docs/review/FIRE-SALE-2026-11-26-UI1-CHECK.md (on origin/prima/build: read it with git show origin/prima/build:docs/review/FIRE-SALE-2026-11-26-UI1-CHECK.md)
- labs/ui-scaffold/README.md and labs/ui-scaffold/CONTRACT.md (your own UI-1 files)
- The wf source on returns: src/cmd.rs, src/board.rs, src/addr.rs (read only)
Note: Fix only U1, U2 and U3. They are at README.md:38, CONTRACT.md:24, and README.md:24 with CONTRACT.md:44. Do not fix U4, U5 or U6. List them in your report as left for Prima.
Note: Do not edit labs/ui-scaffold/QUESTIONS.md. If a fix changes what a question asks, write that as a new question in your report.
Note: You edit existing files here. Keep every other line as it is. Your report lists each changed line, old and new text, and the wf file and line it now matches.

Steps:
0. cd D:\Git\claude\wf-run\work. Check first: git remote -v shows Amalgamour/Workshop, git branch --show-current says returns, and git status --short shows nothing. If not, stop and report.
1. git fetch origin; git pull --ff-only origin returns.
2. Read the brief: git show origin/prima/build:docs/plan/WORK-PAGE-2026-11-30.md. Read the sections "Rules for both", "Extra rules for Claude", "Stop rules" and "Lanes", then the row for pack C21. You may also read origin/packs and origin/prima/build with git show. Do not check them out.
3. Read the inputs above. If an input that is not marked as your own is missing, stop and tell Matthew which one.
4. Write only the allowed files above. Create a missing lab folder if it is yours.
5. Meet the Done when line. Cite a file and line, or a commit and log entry for every claim. In your report, list: the pack, what you did, files touched, every cite, questions for Matthew, and any stop rule you hit.
6. Put any rule conflict as a question for Matthew. Do not decide it. Do not weaken any rule. You have design and lab authority only. You have no close, signoff or pack authority. Touch no data, logs, tests or Workshop code, and write nothing outside the allowed files (t580u).
7. You run no wf command. If anything seems to need wf, stop and write it as a question in your report.
8. Commit by path only: git add -- labs/ui-scaffold/README.md labs/ui-scaffold/CONTRACT.md reports/lab/ui-scaffold/Claude-C21.md. Then: git commit -m "lab: fix UI-1 findings U1-U3 (C21)" -m "Builder: Claude". Never add -A. Never commit -a.
9. Push: git push origin returns. If the push is refused, run git pull --rebase origin returns and push once more. Never force push. Never merge into main.
10. Stop after about 30 minutes, or when done. Stop early on any stop rule on the work page.
11. Tell Matthew "pack C21 pushed" with the commit id and 3 lines on what you found.

MANUAL RETURN (docs/plan/MANUAL-RETURN.md). You run no wf command, so use this block only if a git step fails or a step seems to need wf:
1. Stop. Retry the same command at most once. If it fails again, do not keep trying.
2. Never hand-edit .workshop logs or log.jsonl. Never fake a claim, return, check, or close. Never bypass wf by hand.
3. Record the exact command, exit code, full error text, and the OS.
4. Keep all work inside the allowed files above. Stage files by path only (never add -A, never commit -a). Commit with trailer "Builder: Claude" to returns. Do not write under .workshop/.
5. Write reports/lab/ui-scaffold/Claude-C21-MANUAL-RETURN.md with: pack C21, builder Claude, the failing step, the error, what was done, files touched, and the commit id. Push to returns. Never force push.
6. If the push fails too, paste that same report to Matthew in one block (last resort only). Nothing closes because of it. Prima reviews it.
```
