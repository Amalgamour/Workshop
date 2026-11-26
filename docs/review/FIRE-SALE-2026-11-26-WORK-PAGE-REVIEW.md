# Hostile review: the two open work pages

Pages checked:
- docs/plan/WORK-PAGE-2026-11-30.md (local 514b850 + f6d47b0; published 4e57df04 + d83fbc16)
- docs/plan/WORK-PAGE-2026-11-25-EOW.md (local 7fe0dbf; published 5201b243)

Written by the Prima fire-sale worker, Thu Nov 26 2026, finished 12:18 AM EST (log time; was "about 12:17", see SC5).
All times are EST.

This review does not edit the work pages. Each finding has a suggested fix.

## How I checked

- The local repo (branch build) for docs.
- A read-only bare clone of the public repo, made in my scratch folder, for returns, packs and pass branches.
  Tips used: returns ec78461d, prima/build 5201b243, packs 88be5702.
- No wf command was run. Nothing was pushed.

Severity: **High** = could send a worker the wrong way or break a rule. **Medium** = gap a worker may trip on. **Low** = wording or tidy-up.

## Big picture first

- Both pages are already in use.
- EOW is done: UI-1 returned d7da9e80 (5:08 PM Wed), UI-2 returned 6fca9e2f (5:12 PM Wed).
- Nov 30 has started: C1 returned 128a541b (3:47 PM Wed), X1 returned bf7014ad (3:52 PM Wed).
- Since then, 0423.05.03 closed **failed** at 5:41 PM Wed (returns ec78461d, w02 carried to a later 05.04).
- So parts of the Nov 30 page were already stale when the week ended.

## Findings

### F1. High. Q13 default is now known not to work.
- Where: WORK-PAGE-2026-11-30.md:147. Q5 (Codex) default ★ A: "approve a pinned build with withdraw, then the Prime withdraws each and repacks."
- Evidence: catch log row 19 (docs/quality/CATCH-LOG.md:41, added d675cb6 after the page). Codex X1 (returns bf7014ad, labs/review-draft-page/X1-README-REVIEW.md:64) marks withdraw-then-repack **Breaks**. `wf draft` refuses any pass tail that is not "closed" (src/cmd.rs@1e0d74c6 lines 293-298).
- Why it matters: Matthew may approve a default that the tool will refuse.
- Fix: add a note under Q13 pointing to row 19. Re-shape the options (for example, X1's option A: hold the packs until a granted fix makes "withdrawn" final for drafting). Keep the design-following option as the default.

### F2. High. X3 and X4 are stale after 0423.05.03 closed failed.
- Where: WORK-PAGE-2026-11-30.md:99 says "Add ... 0423.05.03 packed". Line 100 says "at the post-0423.05.03 head".
- Evidence: returns ec78461d "wf: close 90.50.10.0423.05.03 failed (log)", 5:41 PM Wed. w02 carried to a later 05.04.
- Also: line 99 says "Add 0419 closed passed". PAGES.csv already says it (returns labs/stage1-route/PAGES.csv:18 "05.02 closed passed").
- Why it matters: Codex would write the wrong state, and X4 has no real start head.
- Fix: X3 should say "0423.05.03 closed failed (ec78461d); 05.04 to come". X4 should name an exact start commit, or wait for 0423.05.04.

### F3. High. X3 does not carry catch row 18 (0416 code not on returns).
- Where: WORK-PAGE-2026-11-30.md:99.
- Evidence: CATCH-LOG.md:40 says "Codex X3 should mark where accepted code sits". c5bde1e2 is only on pass/90.50.10.0416.05.01, not on returns (checked with merge-base). C1-REVIEW.md:88 (P14).
- Why it matters: a builder may plan as if 0416's code landed.
- Fix: add to X3: "mark, for each closed page, whether its accepted code is on returns".

### F4. High. Claude's independent check is promised but not assigned.
- Where: WORK-PAGE-2026-11-30.md:42 "Codex checks the design labs." EOW:46 "Your design is checked by another view before anyone uses it."
- Evidence: Codex packs X1-X2 (lines 97-98) check only labs/draft-page/. No Codex pack checks C3-C20 (pin-record, pin-move, delegated-grant, overlap-check, stale-pack, retire-0409, catch-log-flow, prompt-check). No pack anywhere checks EOW UI-1 (d7da9e80).
- Why it matters: t580u says any Claude change needs an independent check. C8 (delegated grant, line 75) designs a widening of Prima's authority. That most needs a check.
- Fix: add Codex check packs (for example X21+: check C4-C9, check UI-1), or name Prima/Grok-Check as checker with a row per pack. Mark "not usable until checked" on each Claude pack.

### F5. Medium. The MANUAL RETURN block tells no-wf workers how to retry wf.
- Where: WORK-PAGE-2026-11-30.md:169-175 and :197-203; EOW:122-128 and :149-155.
- Evidence: the same prompts say "Run no wf command" (30-Nov:27, :164; EOW:32, :117). The block says "Retry the same wf command at most once" and "You still hold the page".
- Why it matters: for Claude this reads as a door to run wf. It is noise for every lab worker.
- Fix: drop the block from lab prompts. Or replace it with one line: "You run no wf. If anything needs wf, stop and report."

### F6. Medium. The page does not show which packs are done.
- Where: WORK-PAGE-2026-11-30.md:66-116 has no status column. Line 210 says "Nothing goes to Claude or Codex until you say so."
- Evidence: C1 (128a541b) and X1 (bf7014ad) are already on returns. Catch row 17 (CATCH-LOG.md:39): the prompt went out with `C<NN>` blank.
- Why it matters: Matthew fills in the pack number by hand. Without a status column the next number is guesswork.
- Fix: add a Done column (commit id) or a short "Next: C2, X2" line at the top.

### F7. Medium. Claude's prompt does not read the packs branch.
- Where: WORK-PAGE-2026-11-30.md:159 reads only origin/prima/build. Codex's prompt (:187) reads origin/packs too.
- Evidence: C1-C2 must judge state claims that cite packs log entries (PAGES.csv cites "P0404 e12" and so on).
- Why it matters: Claude can't check a packs entry it never fetched.
- Fix: add "Also read origin/packs (read only)" to step 1 of the Claude prompt.

### F8. Medium. C20 lets Claude dispute findings on its own work, with no judge.
- Where: WORK-PAGE-2026-11-30.md:87.
- Evidence: t580u (memory, Nov 25): Claude has no close or signoff authority, and its changes are checked independently.
- Why it matters: "Accept or dispute" with no named judge leaves the dispute open. Row 19 is already one such dispute.
- Fix: add "Prima rules on each disputed finding; record any reversal in the catch log".

### F9. Medium. Q6 (Claude Q5) default and ★ point at different options.
- Where: WORK-PAGE-2026-11-30.md:137. "A, default ... B ★".
- Evidence: line 120 says ★ marks the option that best fits axiom 2. t384u (memory): the design-following option must be the default.
- Why it matters: the page breaks its own rule on one question.
- Fix: Prima picks one and marks it both "(default)" and ★, with one line of why. If that needs Matthew, ask it as a question.

### F10. Medium. C19 says "8 prompts". WORK-PAGE-2026-11-25.md has 6.
- Where: WORK-PAGE-2026-11-30.md:86.
- Evidence: WORK-PAGE-2026-11-25.md prompt headings at lines 78, 104, 129, 154, 258, 285 (A1-A4, B1, B2). 12 fence lines = 6 blocks.
- Fix: say "the 6 prompts (A1-A4, B1, B2)", or name the extra 2.

### F11. Low. C18 misses catch row 17.
- Where: WORK-PAGE-2026-11-30.md:85 "catch log rows 12-13".
- Evidence: row 17 (CATCH-LOG.md:39) is a prompt mistake too (blank pack number).
- Fix: "rows 12, 13 and 17".

### F12. Low. Some Done-when lines can't be tested as written.
- X3 (line 99): "Repeat X3 at the start of any day after a close" is a standing duty, not a done line.
- X4, X5 (lines 100-101): "ready for Prima" has no test. Say what ready means (start commit named, grant paths, may-touch, done-when, files confirmed free against QUEUE.md).
- X7-X12 (lines 103-108): "Files confirmed free" against what? Name the freeze list or QUEUE.md commit.
- C10, C12 (lines 77, 79): "the cost of each option" with no count. Say "2 or 3 options".
- X16, X17 (lines 112-113): "every piece" is not defined. Give a list or a count.
- X19 (line 115): "fix options" with no count.
- Fix: rewrite those cells as yes/no checks.

### F13. Low. "This week" is ambiguous on a page for the week of Nov 30.
- Where: WORK-PAGE-2026-11-30.md:15, :84, :85.
- Fix: say "the week of Nov 23".

### F14. Low. Report path for packs/ subfolder is unclear.
- Where: WORK-PAGE-2026-11-30.md:35 (report path rule) vs X4-X14 folder labs/stage1-route/packs/.
- Fix: say "reports/lab/stage1-route/" for all X3-X14.

### F15. Low. X15 does not name the 11 items' source.
- Where: WORK-PAGE-2026-11-30.md:111.
- Evidence: the 11 items are in docs/plan/MVP-GOAL-PROPOSAL.md (item 11 at line 134). Count matches.
- Fix: cite that file.

### F16. Low. X20 page id is short.
- Where: WORK-PAGE-2026-11-30.md:116 "0001". The page is 90.50.00.0001 (band 00), not 90.50.10.0001.
- Evidence: returns .workshop/logs/90.50.00.0001/log.jsonl; Grok-Check report f2178076 line 44.
- Fix: write the full address once.

### F17. Low. EOW "DESIGN.md line 14" names no path or branch.
- Where: WORK-PAGE-2026-11-25-EOW.md:23.
- Evidence: the claim is true for returns docs/DESIGN.md:14 ("Several models may work one page at once", last changed 8eb1fdb6, Nov 17). prima/build has a different file, docs/design/DESIGN.md, where line 14 is about BUILD-LOG.
- Fix: "returns: docs/DESIGN.md:14".

### F18. Low. EOW src/board.rs exists only on returns.
- Where: WORK-PAGE-2026-11-25-EOW.md:92.
- Evidence: src/board.rs is on returns, not on prima/build or packs.
- Fix: say "src/board.rs on returns".

### F19. Low. Claude's Nov 30 prompt drops the "touch no data, logs" line.
- Where: EOW:44 and :115 have it. WORK-PAGE-2026-11-30.md:37-42 and :161-164 do not.
- Why it matters: t580u warns about data poisoning. The folder fence covers it, but the explicit line is cheap.
- Fix: add "Touch no data, logs or test files" to step 5.

## What holds (checked, no finding)

- Lanes are disjoint. Nov 30: 10 Claude folders, 6 Codex folders, no shared name or prefix (lines 57-58). EOW: ui-scaffold vs ui-evidence (lines 61-62).
- Nov 30 issues 1-4 match the repo: catch rows 13, 14, 15 (CATCH-LOG.md:35-37); c1750c32 is an ancestor of prima/build and the four core files have no diff to 5201b243; PAGES.csv:6 really says 0407 "05.01 returned"; bbb7d956 is the 0407 close at 1:37 PM Wed.
- Claude's return clone path D:\Git\claude\wf-run\work matches the report at returns reports/lab/draft-page/Claude-20261125-1203.md:45.
- Q numbering matches the lab files: Claude Q1-Q8 (labs/draft-page/QUESTIONS.md:10-113), Codex Q1-Q6 (labs/stage1-route/QUESTIONS.md:7-70).
- No wf, no close, no signoff are in every Claude prompt (30-Nov:164; EOW:117).
- EOW claims: app/ last changed Nov 11 (9514d97); README.md Nov 11 (3291593); docs/design/WF-BOARD.md Nov 18 (5295850); app/lib/compute.ts, rules.ts, seq.ts and app/mock/ exist.
- About 20 packs each matches t588u (5% per 30-minute run).

## Count

19 findings: 4 High, 6 Medium, 9 Low.

## Self-check

Second hostile view of this review, by the same fire-sale worker, Thu Nov 26 2026, 12:36 AM EST.
Every line and commit cite above was re-checked against the local repo (build) and a read-only clone of the public repo (packs c697e035, returns ec78461d, prima/build 5201b243).
**The findings above are left as written.** Corrections are listed here.

Result: 15 of 19 findings hold as written. F1 holds but overclaims and missed an option (SC1, SC2). F4 and F8 cite t580u for more than Matthew said (SC3). F16 has a wrong line cite (SC4). The header time and the packs tip were wrong (SC5, SC6).

### SC1. Medium. F1 overclaims what `wf draft` refuses.
- F1 says `wf draft` "refuses any pass tail that is not closed (src/cmd.rs@1e0d74c6 lines 293-298)".
- Exact: it refuses unless the Prime names that pass with `--overlap-ok` and a why, and the named pass has an open tail: pack, open, return or review (src/cmd.rs@1e0d74c6:290-299, overlap_ok_flag at :329-342; src/page.rs@1e0d74c6:226-228). The refusal spans 293-299, not 293-298.
- "withdrawn" is not an open tail, so `--overlap-ok` can't name a withdrawn pass. **F1's conclusion stands**: withdraw-then-repack is refused.

### SC2. High. F1 and Nov 30 Fix 1 missed an option for Q13.
- The three held passes are at tail "pack", which is open. The pinned a823 wf has the same rule (src/cmd.rs@a823ee28:286-294, src/page.rs@a823ee28:151-153).
- So the Prime may be able to run `wf draft <page> --pass 2 --overlap-ok 1 --why "..."` today and draft a fresh 05.02 with no withdraw at all.
- **Not tried.** I did not check whether claim, pack or close of 05.02 refuse while 05.01 is still packed. The risk: a stale 05.01 stays claimable unless every prompt says not to claim it. It also sets a precedent of open passes stacking on one page (t533u: one worker per page).
- So it is not a default. But Matthew should see it as an option, marked untested. Added as option D to M2 in docs/review/FIRE-SALE-2026-11-26-MONDAY-LIST.md.

### SC3. Medium. F4 and F8 cite t580u for rules Matthew did not state.
- F4: "t580u says any Claude change needs an independent check." F8: "t580u (memory, Nov 25): Claude has no close or signoff authority, and its changes are checked independently."
- Matthew's own words (M9 in docs/review/FIRE-SALE-2026-11-26-DIRECTOR-WORDS-DRAFT.md): "I also see we have issues with claude being able to poison datasets it decides it doesn't like so we need to be careful with claude moving into the future."
- The independent check, no wf and no signoff rules are **Prima's application** of t580u on WORK-PAGE-2026-11-30.md:37-42. I cited them from a memory summary as if they were his words.
- The findings still hold, because the page sets those rules itself. The right cite is "t580u as applied on WORK-PAGE-2026-11-30.md:37-42".
- The same slip is in DONE-WHEN DW1 and STALE-DOCS S2 and S3. It is corrected in the Monday list (M1, M3). F19's cite ("t580u warns about data poisoning") is right.

### SC4. Low. F16 has a wrong line cite.
- F16 says "Grok-Check report f2178076 line 44". In that commit the report is reports/90.50.10.0701/05.04/Grok-Check-check-20261125-1157.md. The intake refusal of 90.50.00.0001 and 90.50.10.0403 is at **line 30**. Line 44 is "Face 01 drift".

### SC5. Low. The header time, and a log line that overclaimed a fix.
- The log line at 12:22 AM EST says the "about ... EST" times were fixed in the three review headers. This file (line 7) and CATCH-LOG-AUDIT.md (line 3) still said "about". Both are fixed now, to the log's finish times.

### SC6. Low. The packs tip in "How I checked" was one commit stale.
- I recorded packs 88be5702. The packs head was already c697e035 ("wf: publish 90.50.10.0423.05.03", Wed 5:41 PM EST), the only commit after 88be5702.
- No finding changes: the 0423.05.03 failure was read from returns ec78461d. But DONE-WHEN's line "Nothing moved since the first round" is wrong against this record. The first round's packs tip was what was stale.

### SC7. Low (in the Nov 30 fix proposal, also my first-round work). Fix 6 names the wrong heading line.
- Fix 6 says the heading "## Claude packs (design and hostile review)" is at line 61. At f6d47b0 line 61 is blank and the heading is line 62. "Insert after line 60" still lands in the right place.

### What holds on re-check
- F2, F3, F5, F6, F7, F9-F15, F17, F18, F19: every line and commit cite matches. Times of 128a541b, bf7014ad, d7da9e80, 6fca9e2f, ec78461d and bbb7d956 match their commit times in EST. 0419 at PAGES.csv:18 and 0407 at :6 match. c5bde1e2 is on pass/90.50.10.0416.05.01 and not on returns. C1-REVIEW.md:88 is P14. The 12 fence lines and 6 prompt headings match. The 10 + 6 lane folders match.

### Proposed catch-log rows (for a checker to write; not written here)

The maker and the catcher are the same here (the fire-sale worker checking its own work). That is the Q1/M4 case. A checker should confirm each row before it goes into docs/quality/CATCH-LOG.md.

| Date (EST) | Page.pass | Kind | What happened | Who made it | Caught by | How caught | Why it matters (axiom) | Outcome / fix | Evidence |
|---|---|---|---|---|---|---|---|---|---|
| Thu Nov 26, 12:36 AM | Nov 30 Q13 | catch | The review said `wf draft` refuses any unclosed tail. It missed `--overlap-ok` on open (packed) passes, so it also missed an untested option for the held packs. | Prima fire-sale worker (round 1) | Prima fire-sale worker (self-check) | re-read src/cmd.rs at 1e0d74c6 and a823ee28 | 9: trial; a question to Matthew must show every option the tool allows | Option D (untested) added to Monday list M2; F1's conclusion stands | WORK-PAGE-REVIEW.md SC1, SC2 |
| Thu Nov 26, 12:36 AM | review cites | mistake | Rules written by Prima on the Nov 30 page (Claude: independent check, no signoff) were cited as Matthew's t580u words, from a memory summary. | Prima fire-sale worker (round 1) | Prima fire-sale worker (self-check) | compared with Matthew's verbatim M9 | 6: lineage, authority must trace to its real source | Monday list M1/M3 recited; DW1, S2 and S3 noted | WORK-PAGE-REVIEW.md SC3; DIRECTOR-WORDS-DRAFT M9 |
| Thu Nov 26, 12:36 AM | review F16 | mistake | Wrong line cite (44 for 30) in a Grok-Check report. | Prima fire-sale worker (round 1) | Prima fire-sale worker (self-check) | re-read f2178076 | cite must match evidence | Noted in SC4 | WORK-PAGE-REVIEW.md SC4 |
| Thu Nov 26, 12:36 AM | fire-sale log | mistake | The log claimed header times were fixed in three review files. Two were not. | Prima fire-sale worker (round 1) | Prima fire-sale worker (self-check) | re-read the headers | a log line must be true when written | Headers fixed in this commit | WORK-PAGE-REVIEW.md SC5; log line at 12:22 AM EST |

