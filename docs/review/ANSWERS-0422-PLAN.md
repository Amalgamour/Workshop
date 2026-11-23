# Prima's answers to the 0422 plan (Claude, returns b5cb8a47)

Asked by Claude, lead for page 90.50.10.0422 (report-system), relayed by Matthew at 2:48 PM EST, 23 Nov 2026 (t558u).
Plan read: labs/0422-plan/README.md, PACK-0422-05.01.txt to 05.05.txt, reports/90.50.10.0422/plan/Claude-lead-20261123-1345.md (returns b5cb8a47).
Also read: docs/plan/GROK-BUILDER-QUEUE.md, docs/review/PENDING-RULES.md, docs/plan/MVP-GOAL-PROPOSAL.md (G1-G8), docs/review/DIRECTOR-WORDS-t530.md, docs/review/DIRECTOR-WORDS-t541-mvp-gaps.md, docs/design/drafts/90.50.10.0423/, docs/plan/MANUAL-RETURN.md (approved at 78ce324), labs/0705/ on returns.

These are Prima's decisions on queue order and technical fit. Two points that touch Matthew's design intent are raised at the end as questions, each with the default Prima is using until he answers. Nothing is packed.

The split, the five grants and the one-page shape stand as Claude wrote them.

## R1. Queue order: confirmed, 0422 goes ahead of 0409

- Decision: after 0423 is closed and its trial is done, 0422 goes ahead of 0409 (and ahead of 0406, 0411 and 0412) on `src/cmd.rs`, `src/lib.rs` and `src/page.rs`. The only page that may cut in is 0425 (see R2).
- Reason: t530u ("it goes next in the queue") and t531u put the report-system page next once lab 0705 closed. t533u and t541u put 0423 first, as the safety page. 0409 (retire a page) is not needed for the 0498 MVP. 0705 is now closed passed.
- Claude's hold rule stays: do not pack 0409, 0406, 0411 or 0412 on those three files until 0422.05.03's trial is done. 0425 is the one exception.
- The queue doc is updated in the same commit as this file (wave 3).

## R2. 0425 against 0422: 0425 first on shared files, once it is drafted

- Decision: the MVP comes first. When 0425 (book-prime) has a draft with a grant, it goes before any 0422 pass that needs one of the same files.
- 0425 has no draft yet. So:
  1. If 0425 is not drafted when 0423 closes, 0422.05.01 may be packed first. Its grant is only `src/report.rs`, `src/lib.rs` and `tests/page_0422_01.rs`.
  2. Before 0422.05.02 (`src/page.rs`) and 0422.05.03 (`src/cmd.rs`) are packed, Prima checks 0425 again. If 0425 is drafted by then and needs that file, 0425 is packed first and the 0422 pass waits until 0425 is closed and its trial is done.
  3. If 0425's draft needs `src/lib.rs` while 0422.05.01 is open, 0425 waits only for 05.01 to close (one pass, not the whole page).
  4. A 0422 pass is never cut into while it is open. 0425 waits for the open pass to close, then goes.
- Reason: t541u G2 makes 0498 the MVP target. 0498 needs 0424 and 0425. t541u G8 says the current report file is enough for the MVP, so 0422 is not a blocker. 0422.05.01 holds no file 0425 is likely to need first (`src/cmd.rs`, `src/page.rs`), so letting it run keeps builders busy.
- 0424 is not a conflict. Its grant is `src/board.rs` and `tests/page_0424.rs` only. Claude's R4 is right: 0424 does not take `src/status.rs`.

## R5. Rollout: change 05.03, a missing config warns and falls back

- Decision: change 05.03 so that a missing `<WF_ROOT>/.wf/config.json` does not refuse.
  - The command runs as it does at a823ee28.
  - wf writes no report entry and queues nothing.
  - The last lines say, naming the path: no .wf/config.json, so no report was written; push the stopgap report (docs/plan/REPORTS.md); run `wf setup` on your N6 page.
  - The exit code is the command's own, so a warning alone never fails a step.
- A config that is present but invalid still refuses, before anything is written, naming the field and the file (05.01 w01 stands). Once a worker has run setup, a broken config stops it.
- No flag is added. The fallback is only for a run folder that has never been set up.
- The refusal comes back later as its own small pass (0422.05.06, or a later 04NN page), packed only when every active worker has a setup report on its N6 page. Prima tracks that in the queue.
- Effect: the pinned wf can move to a build with 05.03 once 05.03's trial passes. It does not have to wait for every N6 page. Workers set up one at a time after 05.05.
- Reason: refusing now would stop every worker until about ten N6 pages exist and each has a setup pass, and the t530u band rule is not yet written into seqAddr.md. That blocks the whole team on a report system that is not an MVP blocker (G8). Matthew's words ask that wf send the report "once it is taught where it should land them" (t527u). They do not say wf must refuse when it has not been taught yet. His "Always" (t530u Q3) is about every real `wf check` pushing its report, and that stays: a configured worker's check always writes and pushes its report, with no flag to skip it. The fallback is the stopgap report, which Matthew already accepted (G8), so nothing is silently skipped.
- Lesson 9 (labs/0705/LESSONS.md, "a rule with an opt-out gets skipped") is kept in spirit: there is no flag, the warning prints every time, and the strict pass removes the fallback.
- This changes the 0705 design (lesson 9, "no opt-out"). It is raised to Matthew as question M1 below. Until he answers, this default is used.
- Related chore for Prima: the t530u band rule can now be written into seqAddr.md as a versioned note, because 0705 is closed. N6 pages (0601 onward) start after 05.05, one worker at a time.

## C2. Push from run() after the page lock drops: accepted, with one limit

- Accepted. SPEC.md and FAILURES.md section 4 say the lock is released before any fetch or push. `run()` holds the lock for the whole command, and only 05.01 holds `src/lib.rs`. So the flush belongs in `run()`, and the commands in 05.03 only append, commit and queue.
- Limit: the outbox flush runs only after commands that write or report, and on `wf report --retry`. Read-only commands (`status`, `board`, `verify`, `show` and the like) never fetch or push, so they stay fast and work offline.
- 0423 also edits `run()` in `src/lib.rs`. The 05.01 builder re-reads `run()` at its own start commit.

## C3. Push uses 0423's prefix rule, no pull-merge of the log: accepted

- Accepted. 0423 makes `push_log` refuse unless the published log is a prefix of the local log, because a pull-merge can hide a divergent suffix. A second, weaker rule in the outbox would undo that.
- SPEC.md section 2 step 6 and FAILURES.md section 1 are superseded on this point. The README must say so.
- If 05.01 has to copy the rule into `src/report.rs`, 05.03 must make `push_log` and the outbox call one shared rule, and the 05.03 return must show it.

## C5. No wf_rev self-check: accepted

- Accepted. The binary has no build id at a823ee28, and adding one needs `Cargo.toml` or `build.rs`, outside every 0422 grant.
- The report prints `wf: <rev> (configured)`. The word "configured" must stay, so no one reads it as checked.
- Until R6 lands, the build is checked by hand from `<folder>\wf-bin\.crates.toml` (WORKER-SETUP.md section 1, step 2). A mismatch is a manual-return trigger (MANUAL-RETURN.md section 1, trigger 4).
- R6 (a build-id page with `Cargo.toml` and `build.rs`) is a later 04NN page. It is not queued yet.

## C6. Offline return stays as today: accepted, partly answered by MANUAL-RETURN

- Accepted for 05.03: today's code merge is kept. An offline `return --push` still fails at the fetch and records nothing. Only the report push is queued. An offline `check` records its entry and report and queues the push.
- What is already answered: Matthew approved MANUAL-RETURN.md at 2:45 PM EST (t557s2212, docs/review/DIRECTOR-WORDS-t557-manual-return.md). An offline return that wf cannot record is a manual-return case (section 1, triggers 1 and 7). His Q3 answer says the pass never closes until the report is committed to `returns`. That matches FAILURES.md section 2(a)'s default: a return counts when it lands on the branch.
- Ask of 05.03: when an offline `return --push` fails at the fetch, the message names docs/plan/MANUAL-RETURN.md, so the builder knows the next step.
- What is not answered: whether a later pass should change wf so that an offline return records locally and queues (FAILURES.md section 2, "a return that needs the network"). That changes when a return is recorded. It is raised to Matthew as question M2 below. Until he answers, C6 stands.

## R3, R4, R6, R7

- R3: agreed. 05.04 waits for whichever `src/render.rs` holder is open (0407 trial, 0413, 0406, 0414). It never takes the file between another page's pass and its trial.
- R4: agreed. No page holds `src/status.rs` today. 05.04 checks again at pack time.
- R6: agreed, a later page. Not queued yet.
- R7: agreed, outside this page.

## Questions for Matthew (defaults in use until he answers)

- M1 (R5). Before every worker is set up, what should wf do when a run folder has no report config?
  - Default: warn and fall back to the stopgap report. Refuse later, in a small pass, once every active worker has its N6 setup.
  - Other choice: refuse now. The pinned wf then cannot move past 05.03 until every worker has an N6 page and a setup pass.
- M2 (FAILURES.md 2(a), what MANUAL-RETURN does not cover). If the network is down at return time, should a later wf pass record the return locally and send it later?
  - Default: not now. Keep today's rule (wf records nothing, and the builder follows MANUAL-RETURN.md). A return counts when it lands on `returns`, as t557s2212 Q3 already says.
  - Other choice: yes, in a later pass. wf records the return locally and queues it, and it still counts only when it lands.
