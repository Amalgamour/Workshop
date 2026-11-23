# Sub-leads under Prima

t560u (23 Nov 2026, 2:54 PM EST): Matthew said Codex and Claude should do most of the work as sub-leads under Prima, so we get more work out of the Grok builders and the best value from the remaining weekly usage.

This file is the standing rule for that. Claude's 0422 assignment stays in docs/plan/CLAUDE-LEAD-0422.md, now under this rule.

## Role

Claude and Codex are sub-leads under Prima.

They are not book Primes. They cannot break a lock, or override a lockout. That stays with the book's Prime or a higher authority, with a recorded reason (t541u, t542u). Until 0425 records the book Prime, only Matthew (the person) may override.

## What a sub-lead does

A sub-lead runs its own track, and reports up to Prima.

- Plan the track and split each page into passes, with one grant per pass, disjoint from every other open page and from each other.
- Write the pack texts and push them to `labs/<page>-plan/` on the `returns` branch. Leave start, predecessor and builder as `(set at pack)`.
- Draft the Grok builder prompts for Prima to hand out. The first line is `Builder: <name> (Matthew's PC, D:\Git\<folder>)`. The last block is the MANUAL RETURN text from docs/plan/MANUAL-RETURN.md. A sub-lead does not assign a worker by packing the name itself.
- After a Grok builder returns a pass, and after Grok-Check has checked it, review the return, the check and the diffs, and report up (recommend pass or fail, and name any issues).
- Push a short lead report to `reports/<page>/plan/` on `returns` (see docs/plan/REPORTS.md). For a multi-page track plan, use `reports/mvp/plan/`.

## What a sub-lead may not do

- Pack, publish-pack, claim, signoff, close or merge. Prima packs. Prima, or the cheap cloud chores agent, runs signoff and close.
- Approve a rule. Only Matthew approves rules.
- Break an abandoned lock, or override a lockout.
- Merge to `main`, or touch `main` at all.
- Force push, on any branch.
- `git add -A` or `git commit -a`. Stage files by path only.
- Print, copy or commit a token, password or key.
- Quietly change a grant, or pack a second page. Raise a conflict, a fork or a major issue, and stop.

## What Prima does

Prima packs, and only with wf built from `a823ee284574be3d9f6247925b9088137a27a539`. Prima, or the cheap cloud chores agent, runs signoff and close. Only Matthew approves rules. Prima only steps in on a conflict, a fork or a major issue.

## Tracks

**Claude** keeps 90.50.10.0422 (report-system). The assignment is docs/plan/CLAUDE-LEAD-0422.md. Workspace: `D:\Git\claude`.

**Codex** takes the MVP track, ending at 0498 (the MVP target; gaps G1-G8 are answered in docs/plan/MVP-GOAL-PROPOSAL.md). Workspace: `D:\Git\codex`. Its `wf.exe` is built from `a823ee284574be3d9f6247925b9088137a27a539`.

- 0423 (one-worker / lockout). The draft is at docs/design/drafts/90.50.10.0423/. Packing waits on the 0408 close (and its trial, if that trial still holds the files).
- 0425 (book-prime). Not drafted yet. Codex drafts the plan. This page records the book's Prime on `DD.SS.BB.0000` face 00. 0423 reads that Prime; it does not create it.
- The remaining steps to 0498, from the MVP proposal and the queue. 0424 (book-board) is already packed and does not share files with 0423 or 0425. 0422 is not an MVP blocker (t541u G8).

The packing order is in docs/plan/GROK-BUILDER-QUEUE.md, wave 3: 0423 first, then 0425 once it has a draft, then the 0422 passes (Claude's track), one at a time, ahead of 0409. 0425 may go before a 0422 pass on a shared file, and must not cut into an open 0422 pass. If 0425 is not yet drafted when 0422.05.01 is ready, 0422.05.01 may go first (docs/review/ANSWERS-0422-PLAN.md R2).

## Codex network

Codex's sandbox blocks the network by default. It uses a dead proxy at `127.0.0.1`. `git clone` and `git push` need network access turned on, or must run outside Codex. Trigger 7 in docs/plan/MANUAL-RETURN.md covers a blocked network that stops wf.

## First Codex job

The first deliverable is the MVP track plan only. Do not pack, claim, close or merge. Paste the block below to Codex.

```
Builder: Codex (Matthew's PC, D:\Git\codex)

Job: sub-lead, under Prima, for the MVP track (0423 lockout, 0425 book-prime, and the path to 0498). First deliverable only: the MVP track plan. Do not pack, draft with wf, claim, signoff, close, or merge.

Matthew (t560u) asked that you and Claude run as sub-leads under Prima, so Grok builders do the builds and remaining weekly usage lasts.

1. Use the wf.exe in D:\Git\codex, built from a823ee284574be3d9f6247925b9088137a27a539. If it is older, rebuild from a823 first. Set WF_AS=Codex. You will not run wf pack or wf claim in this job.
2. Pull prima/build and returns. Codex's sandbox blocks the network by default (a dead proxy at 127.0.0.1). Turn network access on for git pull and git push, or run those git steps outside Codex.
3. Read docs/plan/SUB-LEADS.md on prima/build end to end. That file is your assignment: role, tracks, what you may and may not do, and the reporting path.
4. Also read, on prima/build: docs/plan/MVP-GOAL-PROPOSAL.md (0498 is the target; G1-G8 are answered); docs/design/drafts/90.50.10.0423/ (README.md and FINAL-PACK-0423-05.01.txt — the pack-text shape to copy); docs/plan/GROK-BUILDER-QUEUE.md wave 3; docs/plan/MANUAL-RETURN.md; and docs/review/PENDING-RULES.md for t533u (one worker per page), t541u and t542u (lockout, the book's Prime, abandoned-lock override), t547u (handover), t557u (manual return) and t558u (report-system rollout). The director-words files named there are the verbatim source.
5. Write the plan. Start from wave 3: 0423 first (packing waits on the 0408 close), then 0425 once drafted, then the 0422 passes on Claude's track. Keep one grant per pass, disjoint from every other open page, and from each other. 0425's grant will likely include src/cmd.rs and src/page.rs; raise any conflict with 0423 or 0422, and do not quietly leave a grant. Do not rewrite the 0423 pack text unless a grant or rule has changed; say so in the README if you leave it as drafted. 0424's grant is only src/board.rs and tests/page_0424.rs, so it is not a conflict.
6. Push the plan to labs/mvp-plan/ on the returns branch:
   - labs/mvp-plan/README.md — the order and grants for 0423, 0425, and the remaining steps to 0498, with any change from the starting order, and the reasons.
   - labs/mvp-plan/PACK-0425-05.01.txt — pack text Prima can feed to wf pack, in the 0423 shape (repo, start, predecessor, builder, axioms, outcome, overview, w01…, may touch, checks, stop if). Leave start, predecessor and builder as "(set at pack)". Kit pin: a823ee28 unless a later kit is in force after 0423.
7. Write a short report to reports/mvp/plan/Codex-lead-<YYYYMMDD-HHMM>.md on returns (see docs/plan/REPORTS.md). Point at the folder and the commit. Commit with the trailer "Builder: Codex" and push.
Rules: stage files by path only (never add -A, never commit -a), never force push, never touch main, never print a token. Do not pack, close, or merge. This output stays a plan for Prima to pack.
Reply with the returns commit and the links to labs/mvp-plan/ and the report.

MANUAL RETURN (docs/plan/MANUAL-RETURN.md). If wf fails:
1. Stop. Retry the same wf command at most once. If it fails again, do not keep trying.
2. Never hand-edit .workshop logs or log.jsonl. Never fake a claim, return, check, or close. Never bypass wf by hand.
3. Record the exact command, exit code, full error text, the wf commit it was built from, and the OS.
4. Keep all work inside the grant. Stage files by path only (never add -A, never commit -a). Commit with trailer "Builder: <name>" to returns. Do not write under .workshop/.
5. Write reports/<page>/05.NN/<Builder>-MANUAL-RETURN-<stamp>.md with: page, pass, builder, pack hash, start commit, failing step, error, what was done, files touched, test results, and the code commit. Push to returns. Never force push.
6. If the push fails too, paste that same report to Matthew in one block (last resort only). You still hold the page. The report releases the face lock. This is not a handover. The pass never closes until the report is committed to returns and the checker reviews it.
```
