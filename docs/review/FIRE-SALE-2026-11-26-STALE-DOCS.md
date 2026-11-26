# Stale-doc audit: docs/plan/ and docs/design/

Written by the Prima fire-sale worker, Thu Nov 26 2026, about 12:21 AM EST.
All times are EST. This audit does not edit any of the docs it names.

## How I checked

- Listed every file in docs/plan/ (12) and docs/design/ (83 top-level .md) with its last-change date.
  docs/design/: 35 last changed Nov 11, 14 Nov 12, 5 Nov 16, 9 Nov 17, 6 Nov 18, 14 Nov 19. None after Nov 19.
- Searched them for claims that newer rulings or the current repo state contradict.
- Rulings used: docs/review/DIRECTOR-WORDS-*.md, and the newer rulings cited in the Nov 25 work pages.
- State used: returns ec78461d, packs 88be5702, prima/build 5201b243 (read-only clone).

This is a targeted pass, not a line-by-line read of all 95 files. The big old design files (QUESTIONS-FOR-DIRECTOR.md, OPEN.md, DECISIONS-WAITING.md) were only skimmed.

## Findings

### S1. High. WORKFLOW-TOOLS.md still says several models may work one page at once.
- Doc: docs/design/WORKFLOW-TOOLS.md:33 "Several models may work one page at once." Section at :241 "Several models on one page (t262u ...)".
- Newer ruling: t533u, docs/review/DIRECTOR-WORDS-t533.md:5-9: no more than one pass running on a page; once a worker is in, no other worker may use the page. t541u (docs/plan/MVP-GOAL-PROPOSAL.md:42), MVP item 9.
- Also built: 0423 lockout, 05.02 closed passed.
- The same old line sits on returns at docs/DESIGN.md:14 (EOW page issue 3).
- Fix: add a dated note at the top of both: "t262u multi-model line replaced by t533u one worker per page".

### S2. High. SUB-LEADS.md gives Claude a lead role that t580u takes away.
- Doc: docs/plan/SUB-LEADS.md:3, :9 (Claude and Codex are sub-leads, t560u). :19 drafts Grok builder prompts. :20 reviews Grok returns and recommends pass or fail.
- Newer: t580u (Nov 25), as applied in docs/plan/WORK-PAGE-2026-11-30.md:37-42: narrow fenced lane, no wf at all, no close/signoff/pack authority, every Claude change checked by another view. t572u (Nov 24): the Claude/Codex sub-lead trial "was not as successful as hoped".
- Nothing in SUB-LEADS.md says it is paused or replaced.
- Why it matters: a new session that reads SUB-LEADS.md would give Claude a lead job.
- Fix: add a dated note: "Paused for Claude by t580u; see WORK-PAGE-2026-11-30.md". What stays for Codex needs a ruling (Q2 below).

### S3. High. CLAUDE-LEAD-0422.md keeps Claude as project lead of 0422, running wf.
- Doc: docs/plan/CLAUDE-LEAD-0422.md:3 (t554u, "use Grok workers"), :7, :11 (project lead), :162 "Use the wf.exe ... Set WF_AS=Claude".
- Newer: t580u (no wf for Claude, as applied in WORK-PAGE-2026-11-30.md:40). t572u.
- State: 0422 is "Initialized, faces written, no pack" (returns labs/stage1-route/PAGES.csv:21).
- Fix: depends on Q2 below. Until then, add a dated note: "On hold under t580u".

### S4. Medium. GROK-BUILDER-QUEUE.md status lines are out of date.
- docs/plan/GROK-BUILDER-QUEUE.md (last change 429d4c4, Nov 23).
- :69 "0416.05.01 packed for Grok-5". Now closed failed (returns 49654b6a, Mon 3:37 PM).
- :70 "0419 ... 05.02 is packed for Grok-3". Now closed passed (returns ee40448d, Wed 1:07 PM).
- :107 "0423 (wait)" and :134 "N" (not packed). 0423.05.01 closed failed, 05.02 closed passed, 05.03 closed failed (returns ec78461d, Wed 5:41 PM).
- Codex's map (returns labs/stage1-route/PAGES.csv) has taken over this job, but the queue file does not say so.
- Fix: add a dated note at the top: "Status here stops at Nov 23; live status is labs/stage1-route/PAGES.csv on returns".

### S5. Medium. WORKER-ROLES.md (Nov 19) no longer matches the team.
- docs/plan/WORKER-ROLES.md:16 "Grok-1 and Grok-2 are not set up." Since t517u-t524u (GROK-BUILDER-QUEUE.md:3-11) there are Grok-1 to Grok-5 and Grok-Check.
- :8 queue (Cursor-1: 0404, 0415, then 0406-0409 ...) is from Nov 19.
- :3 "Codex and Claude are about 20 a month each" reads as a dollar plan. t588u (Nov 25) plans about 20 packs a week each. t578u: Grok Bot and Cursor are one merged $100 a month account; Claude $20; Codex $20. The unit is unclear.
- Fix: add a dated note pointing to the current lineup, and write "$20 a month plan; about 20 packs a week (t588u)".

### S6. Medium. TEAM-ROLES-PROPOSAL.md (Nov 19) is an open draft that t572u overtook.
- docs/plan/TEAM-ROLES-PROPOSAL.md:1 "draft for Matthew's Monday review". :31-34 Designer, Researcher, Observer on call.
- Newer: t572u (Nov 24): all Grok bots stop doing work other than timer-based control tasks; Grok workers on Matthew's console do the work.
- No outcome of the proposal is recorded.
- Fix: add a dated note: "Overtaken by t572u".

### S7. Medium. The a823 pin is written in 10 places, with no single record.
- docs/plan/SUB-LEADS.md:36, :65; docs/plan/CORE-RUN.md:27, :29; docs/plan/GROK-BUILDER-QUEUE.md:36, :87, :189; docs/plan/CLAUDE-LEAD-0422.md:93, :162; docs/plan/REPORTS.md:28.
- This is true today. But catch row 14 (docs/quality/CATCH-LOG.md:36) says the pin must move past 0423, and Nov 30 packs C4-C7 plan that move.
- When it moves, every one of these lines goes stale at once.
- Fix: when the pin record exists (Claude Q2, default face 08 of door 90.50.10.0400), replace each line with a pointer to it.

### S8. Medium. The newest rulings have no DIRECTOR-WORDS file.
- The newest file in docs/review/ is DIRECTOR-WORDS-t558-report-system.md.
- t560u has SUB-LEADS.md. But t572u, t578u, t580u, t585u, t586u, t588u, t593u have no words file. A search for "t572u", "t578u" or "t580u" across docs/ finds only the two Nov 25 work pages.
- Why it matters: this audit (and any later check) cannot cite Matthew's own words for the rules that changed this week. The Claude limits (t580u) are the most important.
- Fix: Prima records them as DIRECTOR-WORDS files from the transcript, as before (t335s1296 practice).

### S9. Low. Report paths in practice are not in REPORTS.md.
- docs/plan/REPORTS.md:17, :21 list only reports/<page>/05.NN/ and reports/setup/.
- In use on returns: reports/lab/<folder>/ (work pages, 6 folders), reports/mvp/lead/ (14 Codex lead reports).
- docs/plan/SUB-LEADS.md:21 and :73 say reports/mvp/plan/. The real files are in reports/mvp/lead/.
- Fix: add the two real paths to REPORTS.md; note the SUB-LEADS mismatch.

### S10. Low. WORK-PAGE-2026-11-25.md still carries the wrong 0418 claim.
- docs/plan/WORK-PAGE-2026-11-25.md:67 "Its start (c1750c32) is 4 core commits behind on the same four files."
- Catch row 15 (CATCH-LOG.md:37) shows this is wrong. The diff is empty.
- Fix: a one-line note under the table pointing to row 15.

### S11. Low. LOCAL-BUILDER-FLOW-t400u.md predates t528u.
- docs/design/LOCAL-BUILDER-FLOW-t400u.md:6, :20-21: Prima hands Matthew one prompt per pass to paste.
- t528u (Nov 23): prompt boxes only for brief troubleshooting; normal wf work runs as packs, then returns, then review on GitHub, and wf pushes worker reports.
- The work pages still use one prompt per run, so the flow is half-true.
- Fix: a dated note pointing to t528u and docs/plan/REPORTS.md.

### S12. Low. WF-BOARD.md has no holder, step or next.
- docs/design/WF-BOARD.md (last change 5295850, Nov 18) has no "holder" field.
- t541u G5 (GROK-BUILDER-QUEUE.md:108, page 0424): each book-board line shows holder, step and next.
- The EOW page (issue 4) already flags it. UI-1 (returns d7da9e80) designs the new card.
- Fix: none now. Mark WF-BOARD.md "replaced by labs/ui-scaffold once checked".

## Part 2: the old question lists

Added later the same night, after jobs 1-3 were done and usage remained.
I checked the three question lists in docs/design/ against newer rulings.

### S13. Medium. QD01 (seated face 05) is listed open, but Matthew approved it.
- Doc: docs/design/QUESTIONS-FOR-DIRECTOR.md:23 "QD01. Is face 05 a seated face now, or does it stay a task list?" under "Open" (:21). Last change f867b08, Nov 12.
- Same question: docs/design/DECISIONS-WAITING.md:64 "O6. Best pass seated on plain 05?" (last change decdd2c, Nov 17).
- Newer: docs/review/DIRECTOR-WORDS-t512-seated05-approval.md:7 "Yes, approve the seated-05 rule change" (Nov 23). Built as page 0418 (GROK-BUILDER-QUEUE.md:102: "a body on face 05 with no counter is the seat; 05.NN stays a pass").
- Fix: mark QD01 and O6 "answered t512" with a pointer.

### S14. Low. QD06 (sign-in) is listed open and blocking, but Matthew put it off.
- Doc: docs/design/QUESTIONS-FOR-DIRECTOR.md:86-95. "Blocks: every write path".
- Newer: t585u (Nov 25): proper sign-in for each model and person comes at a later dev stage. For now, typed-for notes stand in. (No DIRECTOR-WORDS file yet, see S8.)
- Fix: mark QD06 "deferred by t585u; not blocking now".

### S15. Medium. QD22 (taking back an abandoned task) is listed open, but t541u answered it.
- Doc: docs/design/QUESTIONS-FOR-DIRECTOR.md:220-225. "Refused until you decide."
- Newer: docs/review/DIRECTOR-WORDS-t541-mvp-gaps.md:67-79: the book's Prime (project lead) or a higher authority may break an abandoned lock, always with a recorded reason. Built into 0423 (lockout, abandoned-lock override).
- This is close to QD22's Option A (a written decision with an approval). It rules out a time-out.
- Fix: mark QD22 "answered t541u (book Prime or higher, with reason)".

### S16. Low. None of the three question lists has an "answered since" marker.
- docs/design/QUESTIONS-FOR-DIRECTOR.md (Nov 12, 519 lines), docs/design/OPEN.md (Nov 11, 255 lines), docs/design/DECISIONS-WAITING.md (Nov 17, 210 lines).
- Many rulings came after (t333u to t593u). I checked only QD01, QD06, QD16, QD22 and O6. QD16 (after task 98) is still truly open: R9 removed slot 99 (docs/spec/DIRECTOR-RULINGS.md:37-38) but did not say what comes after 98.
- Why it matters: a session that reads these lists will ask Matthew questions he already answered.
- Fix: one Codex lab pack: "sweep the three lists; mark each item answered (cite), deferred (cite) or still open". Read only, outside src/ and pages/.

## Count

16 findings: 3 High, 7 Medium, 6 Low.
(Part 1: S1-S12. Part 2: S13-S16.)

## Parked question for Matthew

### Q2. What is left of the Claude and Codex sub-lead roles?

**Question.** SUB-LEADS.md (t560u) and CLAUDE-LEAD-0422.md (t554u) make Claude a lead with wf. t580u fences Claude, and t572u said the trial was not a success. Do those two files still stand, in whole or in part?

**Why it matters.** Both files read as live rules. A new session or worker would follow them and give Claude a lead job with wf. 0422 has no lead in practice.

**Options.**
- A (default): Pause both files for Claude under t580u. Claude does only fenced lab packs from the work page. Codex keeps lab and evidence work, no lead role. Prima leads 0422 herself, or packs it from Claude's lab text after an independent check. This follows the latest rulings and the current work pages.
- B: Keep Codex as sub-lead (SUB-LEADS.md for Codex only). Pause Claude.
- C: Keep both files as they are.

**What happens if no answer.** Prima treats both files as paused for Claude (as the Nov 30 page already does) and does not hand out 0422 lead work. Nothing is deleted.
