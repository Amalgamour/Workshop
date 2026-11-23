# Claude leads 90.50.10.0422 (report-system)

t554u (23 Nov 2026, 2:33 PM EST): Matthew said Claude can be assigned a larger piece of work, and use Grok workers to build it.

Lab 90.50.10.0705.05.02 (Claude's report-system design) closed passed on 23 Nov 2026 at 2:32 PM EST: returns `efadd4d28af6a0d39d856a7ff186b6b2ae52051d`, packs `c439cbdc83a1c3c7dfde775da4fb4c7979e3a5b7`. The lab outputs are on returns under `labs/0705/` (DESIGN.md, SPEC.md, BUILD-PAGES.md, FAILURES.md, WORKER-SETUP.md, LESSONS.md).

This file is Claude's assignment as project lead of page 90.50.10.0422, under Prima. It starts from that lab. It does not pack 0422, and it does not pack 0423.

## Role

Claude is project lead of the report-system page, 90.50.10.0422, under Prima. Prima stays the page's Prime and keeps every wf pack, signoff and close. Claude splits the build, writes the pack text for each piece, reviews what the Grok builders and Grok-Check return, and reports up to Prima.

This is a page lead, not the book's Prime. The book's Prime (the lead, one step below the Director / person) is a book-level role on `DD.SS.BB.0000`. That record is pending page 90.50.10.0425. Claude cannot break an abandoned lock.

## Scope (from lab 0705)

Build the report system into wf, as designed in lab 0705. GitHub stays the nexus. The normal loop is packs > returns > review through GitHub, with wf controlling it (t528u). Prompt boxes stay for brief troubleshooting only.

What "reports live in pages" means (DESIGN.md section 1):

1. **The record.** Each report is one `report` entry in the page's hash-chained log (`pages/<page>/log.jsonl`). It is ordered with the pass it belongs to and cannot be quietly edited afterwards.
2. **The view.** wf prints a readable view from that entry: `pages/<page>/05.NN/REPORT-<seq>-<worker>-<kind>.md`. A view is never written by hand.
3. **The copy on GitHub.** wf pushes the log, and a plain copy of the report text, to the configured branch. Prima can read it on GitHub, or run `wf intake` and see it in her own pages.

The main outcomes, from SPEC.md and BUILD-PAGES.md:

- `wf setup` writes and checks `.wf/config.json` in the run folder, and a worker's setup is a pass on that worker's N6 page (t530u).
- A new `report` log kind, with the order rules in SPEC.md section 4.
- `wf return --push`, a refused return, and every real `wf check` write and push their report. `--dry-run` writes nothing (t530u). `wf report --kind troubleshoot` and `wf report --retry` work. The lock is released before any fetch or push.
- Render, `05.md`, `wf verify` and `wf status` show the reports.
- A kit doc `docs/REPORTS.md` (new, in the wf kit, not `docs/plan/REPORTS.md` on prima/build) says how a worker is set up and what wf prints. After the commands land, Prima marks the stopgap on prima/build as superseded. That mark is outside this grant.

0422 is not a blocker for the 0498 MVP run (t541u G8). The current report file (`docs/plan/REPORTS.md`) is enough until 0422.05.03's trial passes.

## Starting split

Matthew already ruled the unit of work (t531u): one work-order page, 90.50.10.0422, title `report-system`, in the N4 dev band. Its 05 passes are the work orders (t541u). Lab 0705 pass 05.01's five-page split (0422-0426) is withdrawn (BUILD-PAGES.md; LESSONS.md lesson 7).

Claude writes pack text for each pass, each with its own may-touch (one grant per pass). Prima packs them with wf, one at a time. Each piece goes to one Grok builder at a time. Grok-Check checks every return. Claude reviews the results and reports up.

Claude may refine the pass list, the job lines, the tests and the done-when text. Claude may not pack a different split. A second page is only for genuine parallel work with two workers (t533u: one worker per page; many pages may run in parallel). That would need Prima to take it to Matthew, because t531u already chose one page.

The starting split is the five passes in `labs/0705/BUILD-PAGES.md`, with one grant change recorded below.

The page grant, given at `init-page`, is the union of the passes' files:

- `src/report.rs`, `src/lib.rs`, `src/page.rs`, `src/cmd.rs`, `src/render.rs`, `src/status.rs`
- `docs/REPORTS.md` (new kit doc)
- `tests/page_0422_01.rs` through `tests/page_0422_05.rs`

wf checks at pack time that each pass's may-touch sits inside the page grant.

| Pass | Title | May touch | Outcome (short) | Waits on |
|---|---|---|---|---|
| 0422.05.01 | report module and config | `src/report.rs` (new), `src/lib.rs`, `tests/page_0422_01.rs` | `src/report.rs` exists and is declared in `src/lib.rs`. `wf setup` writes and checks `.wf/config.json`, adds `.wf/` to `.git/info/exclude`, and runs a `verify` smoke test. The outbox and `wf report --retry` push queued commits with merge-and-retry and never force. Tests cover config refusals and outbox order. | 0705 closed (done). 0408 closed and its trial done. **0423 closed and its trial done** (see conflict 1). |
| 0422.05.02 | `report` log kind | `src/page.rs`, `tests/page_0422_02.rs` | `"report"` is in `KINDS`, not in `PASS_KINDS`. `order()` enforces SPEC.md section 4. Old logs still load. A bad report entry is refused, with the entry and the rule named. | 05.01 closed. 0423 closed and its trial done (`src/page.rs`). |
| 0422.05.03 | commands write and push reports | `src/cmd.rs`, `tests/page_0422_03.rs` | `return --push` and a refused return write their report and push once. Every real `wf check` writes and pushes its check report; `--dry-run` writes nothing. `wf report --kind troubleshoot` works. The lock is released before any fetch or push. `intake` says "up to date" on a prefix log. | 05.01 and 05.02 closed. 0423 closed and its trial done (`src/cmd.rs`). |
| 0422.05.04 | report views and status | `src/render.rs`, `src/status.rs`, `tests/page_0422_04.rs` | render prints `pages/<page>/05.NN/REPORT-<seq>-<worker>-<kind>.md`; `05.md` lists reports under their pass; `wf verify` covers them; `wf status` shows report lines. | 05.02 and 05.03 closed. 0407 closed and its trial done (`src/render.rs`). No later render holder (0413, 0406, 0414) open at pack time. |
| 0422.05.05 | report docs and setup on N6 | `docs/REPORTS.md` (new kit doc), `tests/page_0422_05.rs` | The kit doc says how a worker is set up on its own N6 page (WORKER-SETUP.md) and what wf prints. It names the stopgap (`docs/plan/REPORTS.md` on prima/build) as superseded. Prima marks that stopgap file herself; it is outside this grant. Do not take kit `AGENTS.md` (its hash is pinned in every pack) or `README.md` (stays with 0498). | 05.03 closed, so the doc describes what wf really prints. No source file is held. |

Each pass also gets a lab trial in the wave after it (`tests/lab_0422_0N.rs` on 0701), as other work does. The 05.03 trial must kill wf after the append and show that no `.wf-lock` is left and `--retry` lands the report (FAILURES.md section 4), and show that a real `wf check` always pushes its report (t530u). Those trial files are not in the 0422 grants.

## Order, and files already held

Nothing in 0422 is packed until the files for that pass are free. 0423, title `one-worker`, still waits on 0408 close, then goes first in the queue, ahead of 0422 (t533u, t541u). Pack text for 0423 is already drafted in `docs/design/drafts/90.50.10.0423/`.

The whole order:

```
0408 closed (and its trial)
  -> 0423 one-worker (holds src/cmd.rs, src/lib.rs, src/page.rs)
  -> 0423 closed (and its trial)
  -> 0422.05.01 -> 05.02 -> 05.03 -> 05.04 -> 05.05
     (one pass at a time, t533u / t541u)
```

Rules for packing and holding:

1. **One worker per page at a time** (t533u). Many pages may run in parallel. Never pack two open 0422 passes at once. A worker holds a face only while actively working on it; the face is locked out for the whole work session and released when the worker is done (t541u). Packing may stage a later pass only when no lockout is held.
2. **No two overlapping grants open at once.** Each 0422 pass's may-touch must be disjoint from every page still open when that pass is packed, and disjoint from every other 0422 pass (BUILD-PAGES.md section 2).
3. **Respect the current holders.** As of this writing (23 Nov 2026, after 2:33 PM EST):
   - 0408 is packed and returned by Grok-2, not yet closed. Its grant is `src/cmd.rs`, `src/lib.rs`, `src/page.rs`, `tests/page_0408.rs`. 0423 waits on that close (and the 0408 trial if the trial still holds the files).
   - 0423 is not packed. Once packed, its grant is `src/cmd.rs`, `src/page.rs`, `src/lib.rs`, `tests/page_0423.rs`.
   - 0407 is packed (grant `src/render.rs`, `tests/page_0407.rs`). No 0407 return had reached GitHub at the time of this note. 0422.05.04 waits on 0407's trial.
   - 0419.05.02 may-touch is only `tests/lab_0419.rs`, so it does not hold `src/git.rs`. 0422 does not take `src/git.rs` (it uses the existing public `git::git`).
4. **Keep 0422 ahead of 0409 on those files.** Do not pack 0409, 0406, 0411 or 0412 on `src/cmd.rs`, `src/lib.rs` or `src/page.rs` until 0422.05.03's trial is done. Otherwise another page could take `src/cmd.rs` between 0422's passes (BUILD-PAGES.md section 3).
5. **Until 0422.05.03's trial passes**, every worker keeps pushing the stopgap report in `docs/plan/REPORTS.md`. After that trial, packs stop including the snippet, and the stopgap `reports/` tree stays as history. 0422.05.04 and 05.05 are the first passes whose own reports are written by wf.

### Conflicts Claude must carry in the pack texts

1. **`src/lib.rs` is now held by 0423.** BUILD-PAGES.md (0705.05.02) said 0423 does not hold `src/lib.rs`, so 0422.05.01 could start after 0408 closed, while 0423 was still open. t541u grew 0423's grant to include `src/lib.rs`, because lockout, try-out and release are new commands and their dispatch lives there (`docs/design/drafts/90.50.10.0423/README.md`; `docs/plan/GROK-BUILDER-QUEUE.md`). 0422.05.01 still needs `src/lib.rs` for `mod report;` and the `setup` / `report` dispatch (LESSONS.md lesson 4). So 05.01, 05.02 and 05.03 all wait until 0423 is closed and its trial has freed those files. Do not pack 0422.05.01 against an open 0423.
2. **Queue order.** The queue doc at `ca9e05800` still lists 0409 right after 0423 in wave 3, and 0705.05.02 as waiting on Grok-Check. 0705 is now closed. The t530u/t531u reading, and BUILD-PAGES.md, put 0422 next once 0423 has freed the files, ahead of 0409. Prima should make the queue doc say so; Claude should write the pack texts as if that order holds, and raise it if the queue has not been updated when a pack is due.
3. **Start commit is set at pack time.** The kit pin today is `a823ee284574be3d9f6247925b9088137a27a539`. 0423 will land first and may move the kit. Pack texts should say "start: (set at pack; after 0423 is closed; kit a823ee28 unless a later kit is in force)".

## What Claude may do

- Read lab 0705, this file, the queue, `docs/plan/REPORTS.md`, `docs/review/PENDING-RULES.md` (t533u, t541u, t547u), and the 0423 draft.
- Refine the pass split and write the pack text for each pass (jobs, may-touch, checks, stop-if, done-when). Use the shape in `docs/design/drafts/90.50.10.0423/FINAL-PACK-0423-05.01.txt` (repo, start, predecessor, builder, axioms, outcome, overview, w01…, may touch, checks, stop if).
- Push that plan to `labs/0422-plan/` on the `returns` branch, and a short report as below.
- After Prima packs a pass and a Grok builder returns it, and after Grok-Check has checked it, review the return, the check and the diffs, and write a review report to Prima (recommend pass or fail, name any issues).
- Draft builder prompts for Prima to hand to a free Grok builder, first line `Builder: <name> (Matthew's PC, D:\Git\<folder>)`. Prima hands them out. Claude does not assign a worker by packing the name itself.
- Raise a conflict, a grant change, or a need for a second page, and stop. Do not quietly leave the grant.

## What Claude may not do

- Pack, publish-pack, signoff or close any page. Prima keeps those wf steps.
- Claim or build any 0422 pass. Those go to one Grok builder at a time. Claude does not check them either; Grok-Check does.
- Merge to `main`, or touch `main` at all.
- Force push, on any branch.
- `git add -A` or `git commit -a`. Stage files by path only.
- Break an abandoned lock, or override a lockout. That is the book's Prime or a higher authority, with a recorded reason (t541u). Until 0425 records the book Prime, only Matthew (the person) may override.
- Edit kit `docs/DESIGN.md`, `AXIOMS.md`, `DIRECTOR-RULINGS.md`, `decisions.md`, or `docs/spec/seqAddr.md` while an open pass pins or cites them (t381u). Pending rules stay in `docs/review/PENDING-RULES.md` until Prima can apply them.
- Push a late local claim after leaving a page (t547u handover).

## Reporting path

Until 0422.05.03's trial lands, reports use the stopgap in `docs/plan/REPORTS.md`:

    reports/<page>/05.NN/<Builder>-<kind>-<YYYYMMDD-HHMM>.md

on the `returns` branch. Stage by path, commit with trailer `Builder: Claude`, never force push. If the push is rejected, fetch and rebase onto the tip, then push again, and still never force.

For this lead job:

- The plan (split, grant table, and each pack text) lives at `labs/0422-plan/` on `returns`. Suggested layout:
  - `labs/0422-plan/README.md` — the split, grants, order, and any change from this starting split, with reasons.
  - `labs/0422-plan/PACK-0422-05.01.txt` through `PACK-0422-05.05.txt` — pack texts ready for Prima to feed to `wf pack`.
- A short lead report also goes to `reports/90.50.10.0422/plan/Claude-lead-<YYYYMMDD-HHMM>.md` on `returns`, pointing at that folder and the commit.
- After each later return and check, Claude writes `reports/90.50.10.0422/05.NN/Claude-review-<YYYYMMDD-HHMM>.md` on `returns`.

The plan folder is not a packed page. Prima reads it and packs. Do not run `wf pack` or `wf draft` from that folder.

## Done when

This assignment has two finishes. The first one is the start of the work; the second is the end of the build.

**Plan (first deliverable), done when:**

1. `labs/0422-plan/` is on `returns` and contains the split and one pack text per pass.
2. Each pack text has a disjoint may-touch, names who it waits on, and does not overlap 0408 or 0423 on `src/cmd.rs`, `src/lib.rs` or `src/page.rs` while those pages are open.
3. The lead report on `returns` points at that folder. Claude has not packed, closed, or merged anything.
4. Prima can pack 0422.05.01 from that text once 0408 and 0423 (and their trials) have freed the files.

**Build (the lead job), done when:**

1. Each 0422 pass has been packed by Prima, built by one Grok builder, checked by Grok-Check, reviewed by Claude, and signed off and closed by Prima.
2. No two overlapping grants were open at the same time. One worker at a time was in the page.
3. After 05.03's trial, a real `wf check` writes and pushes its report, `return --push` does the same, and the stopgap is marked superseded by Prima.
4. Claude's review reports are on `returns` for every pass.

## Prompt for Claude

Paste the block below to Claude. Do not pack from this prompt. The output stays a plan for Prima to pack.

```
Builder: Claude (Matthew's PC, D:\Git\claude)

Job: project lead, under Prima, for page 90.50.10.0422 (report-system). First deliverable only: the page split and pack texts. Do not pack, draft, claim, signoff, close, or merge.

Lab 90.50.10.0705.05.02 closed passed (returns efadd4d2, packs c439cbdc). Matthew (t554u) asked that you lead this larger piece and use Grok workers to build it.

1. Use the wf.exe built from a823ee284574be3d9f6247925b9088137a27a539. Set WF_AS=Claude. You will not run wf pack or wf claim in this job.
2. Pull prima/build and returns. Read docs/plan/CLAUDE-LEAD-0422.md on prima/build end to end. That file is your assignment: scope, starting split, grants, order, what you may and may not do, the reporting path, and done-when.
3. Also read, on returns, labs/0705/DESIGN.md, BUILD-PAGES.md, SPEC.md, FAILURES.md, WORKER-SETUP.md and LESSONS.md. On prima/build, read docs/plan/GROK-BUILDER-QUEUE.md, docs/plan/REPORTS.md, docs/review/PENDING-RULES.md (t533u, t541u, t547u), and docs/design/drafts/90.50.10.0423/ (README.md and FINAL-PACK-0423-05.01.txt). The 0423 pack text is the shape to copy.
4. Write the plan. Start from the five-pass split in CLAUDE-LEAD-0422.md (one page, 90.50.10.0422, title report-system; t531u). Keep one grant per pass, disjoint from every other open page, and from each other. 0422.05.01, 05.02 and 05.03 must wait until 0423 has closed and freed src/cmd.rs, src/lib.rs and src/page.rs (t541u grew 0423's grant to include src/lib.rs; this is a change from BUILD-PAGES.md). Raise any further conflict; do not quietly leave a grant. If you believe a second page is needed for genuine parallel work, say so and stop: do not pack it.
5. Push the plan to labs/0422-plan/ on the returns branch:
   - labs/0422-plan/README.md — the split, grants, order, and any change from the starting split, with reasons.
   - labs/0422-plan/PACK-0422-05.01.txt through PACK-0422-05.05.txt — pack texts Prima can feed to wf pack. Leave start, predecessor and builder as "(set at pack)". Kit pin: a823ee28 unless a later kit is in force after 0423.
6. Write a short report to reports/90.50.10.0422/plan/Claude-lead-<YYYYMMDD-HHMM>.md on returns (see docs/plan/REPORTS.md). Point at the folder and the commit. Commit with the trailer "Builder: Claude" and push.
Rules: stage files by path only (never add -A, never commit -a), never force push, never touch main, never print a token. Do not pack, close, or merge. This output stays a plan for Prima to pack.
Reply with the returns commit and the links to labs/0422-plan/ and the report.
```
