# Prima response to 0704.05.01

Codex returned 90.50.10.0704.05.01 (builder commit `b1a9c3ca`, returns tip at intake `641f75aa`). Prima intaked the page in a clean clone and published only 0704 to packs (`c6657ff0`, `wf: publish 90.50.10.0704`). Prima did not check or close the lab. That waits on Grok-Check: `wf check 90.50.10.0704 1 --as Grok-Check`.

Times below are America/Toronto (EST, UTC-5).

## 1. A later 0701 return displaced an earlier return on another counter

**Finding.** Grok-1 returned 90.50.10.0701.05.03 first, then 05.02 a few minutes later. Both passes were by Grok-1. The shared page log on `returns` now shows the 05.02 claim and return as entries 23 and 24, and it no longer shows the 05.03 claim or return.

The 05.03 work is still there. The return file `.workshop/returns/90.50.10.0701.05.03.md` and `tests/lab_0415.rs` are on the current `returns` tip, and the 05.03 pack is still in the log (entries 20-21). The missing piece is only the 05.03 claim and return events.

What happened, in order:

- Entries 1-22 are a shared prefix, through the pack of 05.02 and 05.03 and the face after that pack.
- At 10:38 AM EST Grok-1 claimed 05.03. At 10:41 AM EST Grok-1 returned it. That log was committed as `b71ab3e0` (`wf: return 90.50.10.0701.05.03 (log)`). The work commit is `b142884d` (`90.50.10.0701.05.03: add the outside 0415 Windows trial`).
- At 10:47 AM EST Grok-1 claimed 05.02. At 10:49 AM EST Grok-1 returned it. That log was committed as `a3a0f83a` (`wf: return 90.50.10.0701.05.02 (log)`). The work commit is `018892ba` (`90.50.10.0701.05.02: add the outside 0404 design-review trial`).
- `b71ab3e0` is an ancestor of `a3a0f83a` and of `origin/returns`. This was not a history rewrite. At `111c2199` (the merge that brought in the 05.02 work) the log file still had the 05.03 claim and return as entries 23-24. `push_log` then copied a stale or parallel local log, which still ended at a 05.02 claim and return as 23-24, over the published file and committed `a3a0f83a` on top. That is a normal fast-forward overwrite of the file.

`push_log` (`src/cmd.rs` at a823ee28) copies the run-folder log over `.workshop/logs/<page>/log.jsonl`, commits by path, and pushes. It does not require the published log to be a prefix of the local one. Intake already refuses the opposite direction: a remote log that does not continue the local prefix. The damage happens on the way out, before intake can catch it.

Views printed from the current tip would be wrong in one place: 05.03 would look packed but never claimed or returned, and 05.02 would look returned, even though 05.03 was claimed and returned first. The 05.02 views are otherwise in line with the surviving suffix. Packs still has only the 22-entry prefix, so neither return suffix has been intake-published yet.

**Prima's action.** Investigated the two return commits, the work commits, and the log at `111c2199`. Did not publish-pack 0701 (that would put the displaced suffix on packs). Proposed recovery: append the preserved 05.03 claim and return as new entries after the current head (25-26), and never rewrite 23-24, because the log is a hash chain. Do not hand-edit the log in this turn. Proposed a wf work page, suggested 0423 (next open unused 04NN after 0422): `push_log` and `wf return --push` must fetch the published log and refuse to publish unless that log is a prefix of the local log. The builder then intakes and re-returns so new events append. Parallel open passes that would write different suffixes at the same sequence numbers must not collide.

**Status.** Diagnosed. The wf fix is not packed (0408 holds `src/cmd.rs`). The 0701 log is not yet repaired. Packs 0701 is unchanged.

## 2. The 0702 check record names the reviewer, not who filed the judgment

**Finding.** The 90.50.10.0702.05.02 check (log entry 18) has `actor=Codex`, `role=checker`, `verdict=fail`. Its data keys are `commit`, `pass`, `report`, `results`, and `verdict`. There is no field for who typed the command. An executor recorded Codex's manual verdict with `wf check ... --as Codex --fail`. Matthew said the reviewer and the filer should both be named (`labs/0704/MATTHEW-RESPONSES.md`).

**Prima's action.** Proposed a `filed_by` field on the check event, on a later wf work page once `src/cmd.rs` is free (not packed in this turn). Noted the gap in `docs/lessons/2026-11-23-check-filer.md`. Until wf records both names, the typist can be named in the check `--note` when that person is not the reviewer.

**Status.** Lesson written. Code change not started. 0702 was not restaged.

## 3. The lesson book recommended a Windows heading pattern the queue rejects

**Finding.** `docs/lessons/2026-11-23-first-labs.md` still told builders to use `git grep -q -E "^##[[:space:]]3[.]" -- <file>`. The later queue and the 0419 pack require the form with no caret, no quotes, and no spaces: `git grep -q -E [#][#][[:space:]]3[.] -- <file>`.

**Prima's action.** Changed that lesson, on prima/build, to the `[#][#]` form, and pointed at the queue and 0419. Docs only. No rule or spec file was edited.

**Status.** Done.

## 4. Stage 1 still needs the 0498 walkthrough on Matthew's PC

**Finding.** Stage 1 has evidence for the individual steps. The 0498 walkthrough still has to prove the full loop on Matthew's PC, including finding and understanding the saved record from a fresh session. Matthew's words are in `labs/0704/MATTHEW-RESPONSES.md`. The proposed walkthrough is in the drift review.

**Prima's action.** Added a priority note on 0498 in `docs/plan/GROK-BUILDER-QUEUE.md`. 0498 stays last in dependency order (it still depends on the earlier stage pages) and is not packed in this turn. The note says the stage is not done until that walkthrough is packed and run on Matthew's PC.

**Status.** Queue updated. Walkthrough not yet packed.

## After t533u

Page 90.50.10.0423 is now drafted as title one-worker: the claim and check occupancy rule (t533u) and the `push_log` prefix check. Pack text is in `docs/design/drafts/90.50.10.0423/`. It waits on 0408, then goes first in the queue, ahead of 0422. The 0701 repair steps are in `docs/review/0701-LOG-REPAIR.md`. The repair has not been done. 0701 has not been published to packs.

## After the 05.01 check (t537u)

Grok-Check passed 05.01 (entry 9). Prima signed off and closed it. The four findings still hold; the actions above stand. Grok-Check also noted that the pack cited `docs/plan/STAGE-PLAN*`, which does not exist; the real path is `docs/design/STAGE-PLAN-90.50.10.md`. That is recorded in `docs/lessons/2026-11-23-stage-plan-path.md`. 05.02 is not packed; Matthew steers that lab directly.

