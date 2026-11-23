# Plan: 90.50.10.0422 report-system

Lead: Claude, under Prima (docs/plan/CLAUDE-LEAD-0422.md on prima/build, t554u). 2026-11-23.
This folder is a plan, not a packed page. Prima packs each pass with wf, one at a time. Claude has not run `wf pack`, `wf draft`, `wf claim`, signoff, close or merge for this plan.

Sources:
- the assignment, docs/plan/CLAUDE-LEAD-0422.md (prima/build 23c510be);
- the closed design lab labs/0705/ (returns; 05.02 closed passed, returns efadd4d2, packs c439cbdc);
- the 0423 draft docs/design/drafts/90.50.10.0423/ (prima/build);
- docs/plan/GROK-BUILDER-QUEUE.md, docs/plan/REPORTS.md, docs/review/PENDING-RULES.md (t533u, t541u, t547u).

Code cites are wf at a823ee28. 0408 (returned, not closed) and 0423 (not packed) both change `src/cmd.rs`, `src/lib.rs` and `src/page.rs` first, so every builder re-reads the cited lines at its own start commit.

Everything below is a **Claude proposal** unless it is quoted as Matthew's ruling.

## 1. Page and split

One page, `90.50.10.0422`, title `report-system`, in the N4 dev band. Its five 05 passes are the work orders (t531u, t541u). The split is the starting split in CLAUDE-LEAD-0422.md. Its files are unchanged. The job lines are refined (section 3).

Page grant, given at `init-page`: the union of the pass grants.
- `src/report.rs`, `src/lib.rs`, `src/page.rs`, `src/cmd.rs`, `src/render.rs`, `src/status.rs`
- `docs/REPORTS.md`
- `tests/page_0422_01.rs` to `tests/page_0422_05.rs`

| Pass | Title | May touch | Pack text | Waits on |
|---|---|---|---|---|
| 0422.05.01 | report module and config | `src/report.rs` (new), `src/lib.rs`, `tests/page_0422_01.rs` | PACK-0422-05.01.txt | 0408 and **0423** closed, with their trials done (`src/lib.rs`) |
| 0422.05.02 | report log kind | `src/page.rs`, `tests/page_0422_02.rs` | PACK-0422-05.02.txt | 05.01 closed. 0423 closed, with its trial done (`src/page.rs`) |
| 0422.05.03 | commands write and push reports | `src/cmd.rs`, `tests/page_0422_03.rs` | PACK-0422-05.03.txt | 05.01 and 05.02 closed. 0423 closed, with its trial done (`src/cmd.rs`) |
| 0422.05.04 | report views and status | `src/render.rs`, `src/status.rs`, `tests/page_0422_04.rs` | PACK-0422-05.04.txt | 05.02 and 05.03 closed. 0407's trial done. No other `src/render.rs` or `src/status.rs` holder open (R3, R4) |
| 0422.05.05 | report docs and setup on N6 | `docs/REPORTS.md` (new kit doc), `tests/page_0422_05.rs` | PACK-0422-05.05.txt | 05.03 closed (so the doc describes what wf really prints) and 05.04 closed (one pass at a time). Holds no source file |

**Disjointness:**
- No file appears in two passes.
- Each pass has its own test file.
- At pack time, each pass's may-touch must be free of every open page:
  - 0408 holds `src/cmd.rs`, `src/lib.rs`, `src/page.rs`;
  - 0423 will hold `src/cmd.rs`, `src/page.rs`, `src/lib.rs`;
  - 0407 holds `src/render.rs`;
  - 0413, 0414 and 0406 take `src/render.rs` later;
  - 0409, 0406, 0411 and 0412 take `src/cmd.rs` and `src/lib.rs` later;
  - 0419.05.02 holds only `tests/lab_0419.rs`.
- 0422 takes no `src/git.rs`, `src/board.rs`, `templates/`, `AGENTS.md`, `README.md` or `docs/DESIGN.md`.

**A second page: not needed.** Every pass needs the one before it:
- 05.02's order rules check what 05.01's module writes;
- 05.03 calls both;
- 05.04 renders the kind that 05.02 adds and the entries that 05.03 writes;
- 05.05 documents what 05.03 prints.

No two parts could run at the same time with two workers, so t531u's one page stands (t533u: one worker per page).

## 2. Order

```
0408 closed (and its trial)
  -> 0423 one-worker, then 0423 closed (and its trial)       frees src/cmd.rs, src/lib.rs, src/page.rs
  -> 0422.05.01 -> 05.02 -> 05.03 -> 05.04 -> 05.05          one pass at a time, one worker at a time
```

Rules from the assignment, kept in every pack:
- Never pack two open 0422 passes at once. Pack a pass only when no lockout is held on the page (t541u).
- Do not pack 0409, 0406, 0411 or 0412 on `src/cmd.rs`, `src/lib.rs` or `src/page.rs` until 0422.05.03's trial is done. Otherwise another page could take a file between 0422's passes.
- Until 0422.05.03's trial passes, every worker keeps pushing the stopgap report (docs/plan/REPORTS.md). Each pack says so.

**Lab trials** come in the wave after each pass: `tests/lab_0422_0N.rs` on 0701. They are not in the 0422 grants. The 05.03 trial must:
- kill wf after the append, and show that no `.wf-lock` is left and that `wf report --retry` lands the report (FAILURES.md section 4);
- show that a real `wf check` always pushes its report (t530u).

## 3. Changes from the starting split, with reasons

C1 to C7 change the job wording. None of them changes a pass's files.

**C1. 05.01 waits on 0423, not only 0408.** This change was given in the assignment.
- t541u grew 0423's grant to include `src/lib.rs`, because lockout, try-out and release are new commands (0423 README, conflict 1).
- 05.01 needs `src/lib.rs` for `mod report;` and its dispatch (labs/0705/LESSONS.md lesson 4).
- So 05.01, 05.02 and 05.03 all wait until 0423 has closed and its trial has freed the three files. BUILD-PAGES.md (0705) said 05.01 could start while 0423 was open; that line is withdrawn.

**C2. The report push runs after the page lock is released, in `run()` (05.01), not inside `ret` (05.03).**
- The design says "the lock is released before any fetch or push" (SPEC.md section 2, step 4; FAILURES.md section 4).
- But at a823ee28, `run()` in `src/lib.rs` takes the page lock for the whole command (src/lib.rs:154). `writes()`, which decides that, is also in `src/lib.rs` (:113-122).
- 05.03 holds only `src/cmd.rs`, so it cannot release that lock early.
- The fix: 05.01 adds an outbox flush to `run()`, which runs after the lock guard is dropped. The commands in 05.03 (`return`, a refused return, `check`) append, commit locally and queue. They never push inside the lock.
- This keeps the pass grants disjoint, and it also gives "every later command tries the outbox first" (FAILURES.md section 2) for free.

**C3. The push follows 0423's prefix rule, not "merge and retry like push_log".**
- 0423 w05 makes `push_log` fetch the published log and refuse unless it is a prefix of the local log, and stop pull-merging the log file (src/cmd.rs:574 today), because a merge can hide a divergent suffix.
- SPEC.md section 2 step 6 and FAILURES.md section 1 copied today's `push_log`. They are superseded on this point.
- The outbox push (05.01):
  1. fetches the branch;
  2. checks the published page log is a prefix of the queued log;
  3. only then merges the branch tip (no rebase, so the recorded commit SHA stays, FAILURES.md section 1) and pushes;
  4. on a rejection, it fetches again and repeats the check, up to 3 times.
- It never forces. A conflict aborts the merge and leaves the item queued.
- If 0423's helper can be called from `src/report.rs` without editing `src/cmd.rs`, 05.01 calls it. Otherwise 05.01 writes the same rule in `src/report.rs`, and 05.03 makes `push_log` and the outbox use one rule.

**C4. "Open claim" becomes "unreleased lockout" (0423, t541u).**
- SPEC.md section 4 refused a troubleshoot report "while another worker holds an open claim". After 0423 the page is held by a lockout.
- So:
  - a `report` entry's actor must hold the unreleased lockout at that point in the log (face 05 for build, lab, setup and check; any face for troubleshoot);
  - `wf setup` checks that `--as` holds the lockout on its N6 page;
  - "took" for a check runs from the checker's lockout entry to the check entry, instead of "from intake".
- Reports therefore never bring a second worker into a page.

**C5. No `wf_rev` self-check refusal.**
- SPEC.md section 2 step 1 has wf refuse "if this wf's build is not `wf_rev`".
- At a823ee28 the binary does not know its own commit: Cargo.toml has no build script, and there is no `--version`. Teaching it would need `build.rs` or `Cargo.toml`, which are outside the grant.
- So `wf setup` takes `--rev <40 hex>`, stores it, and every report prints it as `wf: <rev> (configured)`.
- A real build-id check is raised for a later page (R6).

**C6. An offline return behaves as today.**
- At a823ee28, `return --push` fetches during `merge_into_shared`, before any entry is written (src/cmd.rs:496-499), so an offline return records nothing.
- FAILURES.md section 2(a) proposed that an offline return should record locally and count when it lands. That was raised to Matthew and is not answered.
- So 05.03 keeps today's rule for the code merge. Only the report push is queued.
- An offline `check` records its entry and report, and queues the push.

**C7. Where each piece is tested.**
- The report-text builder and the outbox are unit-tested inside `src/report.rs` (`cargo test --lib`).
- 05.01 dispatches `wf report <page> <NN> --kind troubleshoot --file F`, but that command can only append once 05.02 adds the `report` kind. So it is tested end to end in `tests/page_0422_02.rs`.
- The "every `check` is followed by its report" rule is not put in `Page::order`. Old logs have checks with no report and must still load. 05.03 makes `check` always append it, and its test and trial prove that.

## 4. Raised, not resolved (for Prima, and Matthew where it is his order)

- **R1. Queue order.** The queue doc still has 0409 right after 0423 in wave 3 (docs/plan/GROK-BUILDER-QUEUE.md, wave 3). The t530u/t531u reading and the assignment put 0422 next once 0423 frees the files. The packs here are written as if that order holds. If the queue is unchanged when 05.01 is due, Claude raises it again before handing out a prompt.
- **R2. 0425 against 0422 on shared files.**
  - 0425 (book-prime) likely takes `src/cmd.rs` and `src/page.rs`. It is needed before the 0498 MVP run, and 0422 is not (t541u G8).
  - If it is packed while a 0422 pass needs the same file, one waits. The plan does not choose. Matthew's order decides, through Prima.
  - Claude's view: 0425 goes first on those files if it is ready first, because the MVP needs it.
  - 0424 (book-board) is not a conflict. It was packed as 0424.05.01 (returns a0c08c1f) with grant `src/board.rs` and `tests/page_0424.rs` only.
- **R3. `src/render.rs` holders.** 0413 (wave 3), 0414 (wave 11) and 0406 (wave 5) all take `src/render.rs`. 05.04 waits on whichever of them is open, and must not take the file between another page's pass and its trial.
- **R4. `src/status.rs`.** The 0423 README says that showing the lockout on `wf status` or `wf board` is "for 0424 and later". 0424.05.01's grant does not take `src/status.rs` (returns a0c08c1f). If a later page takes it, 05.04 waits for that page's trial.
- **R5. Rolling out the new wf.**
  - After 05.03, a reporting command with no `.wf/config.json` refuses, by design (lesson 9 in 0705: no opt-out). The refusal names the file and `wf setup`.
  - So Prima must not move the pinned build every worker runs to a build with 05.03 until each active worker (Grok-1 to Grok-5, Grok-Check, Claude, Codex, Cursor) has an N6 page.
  - Each worker then runs its setup pass with that build, as WORKER-SETUP.md section 1 says.
  - This needs N6 pages 0601 and later, which are not started. The t530u band rule is still pending in PENDING-RULES.md.
- **R6. Build id.** A later page with `Cargo.toml` (and a new `build.rs`) in its grant could print wf's own commit, and let reports refuse on a mismatch (C5).
- **R7. The worker-name stamp field** is still marked 7 (SPEC.md section 4, last paragraph). It is not in this page.

## 5. How each pass runs

1. Prima packs it from the pack text.
   - The `start` line says "(set at pack)": that is the tip after 0423 is closed, with kit a823ee28 unless a later kit is in force.
   - `predecessor` and `builder` are also set at pack.
2. Prima hands one Grok builder the prompt. Claude can draft that prompt on request. The first line is `Builder: <name> (Matthew's PC, D:\Git\<folder>)`.
3. The builder runs lockout, try-out and claim, works, and returns with `--push`. Then it releases the lockout (0423) and pushes its report: the stopgap report, until the wf it runs includes 05.03.
4. Grok-Check takes its own lockout, runs `wf check`, releases, and pushes its report.
5. Claude reviews the return, the check and the diff from start to return. Claude writes `reports/90.50.10.0422/05.NN/Claude-review-<YYYYMMDD-HHMM>.md` on returns, recommending pass or fail.
6. Prima signs off and closes.
7. The pass's lab trial comes in the next wave.

A handover follows t547u: published logs, returns, commits and reports count, and dirty local files do not.
