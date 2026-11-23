# Lab 0705: the report-system work order and its passes

Page 90.50.10.0705. Builder: Claude. Status: `9`. Rewritten in pass 05.02 for t531u and t533u.
Everything here is a **Claude proposal** unless it is quoted as Matthew's ruling. No page and no pass is packed by this lab. Packing waits until 0705 closes (docs/review/DIRECTOR-WORDS-t530.md:47; docs/plan/GROK-BUILDER-QUEUE.md:179 @04c13954).

Why this file changed: pass 05.01 proposed five pages, 0422-0426 (commit d7c505ba, BUILD-PAGES.md section 1). Matthew ruled that the build is one work order:
> "N4 is our dev band so the work for building the report system goes that is a work order page. The work order is building our report-system :)"
(t531u, docs/review/DIRECTOR-WORDS-t530.md:45)

So the build is one page with several passes. The five-page split is withdrawn.

## 1. Split

**One work-order page: 90.50.10.0422, title `report-system`.**
- 0422 is the next open, unused 04NN (docs/review/DIRECTOR-WORDS-t530.md:39-41, :47).
- The title is lowercase, as seqAddr.md:112@8e96151d requires.
- The page lists `Lab: 90.50.10.0705`, and this lab lists it back under Serves when it is packed (0705 face 01).

The page's grant, which Matthew gives at `init-page`, is the union of its passes' files:
- `src/report.rs`, `src/lib.rs`, `src/page.rs`, `src/cmd.rs`, `src/render.rs`, `src/status.rs`
- `docs/REPORTS.md`
- `tests/page_0422_01.rs` to `tests/page_0422_05.rs`

wf checks at pack time that each pass's may-touch sits inside the page grant (kit docs/DESIGN.md:54-55).

The passes, in order. Each is one claim, one return and one check, by one worker at a time (t533u):

| Pass | Title | Outcome (done when, short form) |
|---|---|---|
| 0422.05.01 | report module and config | `src/report.rs` exists and is declared in `src/lib.rs`. `wf setup` writes and checks `.wf/config.json` (SPEC.md section 1), adds `.wf/` to `.git/info/exclude`, and runs a `verify` smoke test. The outbox and `wf report --retry` push queued commits with merge-and-retry and never force (FAILURES.md sections 1-2). Tests cover config refusals and outbox order. |
| 0422.05.02 | `report` log kind | `"report"` is in `KINDS`, not in `PASS_KINDS`. `order()` enforces SPEC.md section 4: any tail, a valid `of`, the kind from the page band (`setup` on 0601-0698, `lab` on 0701-0798, `check`, `build`), one report per `of`, and no troubleshoot while another worker holds an open claim. Old logs still load. A bad report entry is refused, with the entry and the rule named. |
| 0422.05.03 | commands write and push reports | `return --push` and a refused return write their report and push once (commit, log and copy). **Every real `wf check` writes and pushes its check report** (t530u, DIRECTOR-WORDS-t530.md:25-27); `--dry-run` writes nothing. `wf report --kind troubleshoot` works. The lock is released before any fetch or push. `intake` says "up to date" on a prefix log. The last lines are as in SPEC.md section 2, step 7. |
| 0422.05.04 | report views and status | render prints `pages/<page>/05.NN/REPORT-<seq>-<worker>-<kind>.md`; `05.md` lists reports under their pass; `wf verify` covers them; `wf status` shows report lines. |
| 0422.05.05 | report docs and setup on N6 | A kit doc `docs/REPORTS.md` says how a worker is set up on its own N6 page (WORKER-SETUP.md section 1) and what wf prints. It names the stopgap (docs/plan/REPORTS.md on prima/build) as superseded. Prima marks that file herself; it is outside this grant. |

**Sub-pages: none.** wf does not require any, for three reasons:
- **Grants.** One page can carry a different grant on each pass: each pack has its own may-touch, checked against the page grant (kit docs/DESIGN.md:54-55). So no part of the build needs a page of its own just to get different files.
- **Order.** The passes are a strict sequence anyway: 05.03 calls what 05.01 and 05.02 add. t533u allows only one worker in a page at a time (DIRECTOR-WORDS-t533.md:5, :11), and a sequence never needs two at once.
- **Pass count.** Five passes are far below the 98-pass limit of one page (R9; src/cmd.rs:128-135).

The one reason to split into a sub-page would be to run two parts in parallel with two workers. That is not needed here, and t531u asks for one page. If 05.04 (render) ends up waiting a long time on `src/render.rs` while the rest is done, the pass simply waits. It does not move to a new page.

**Pages this proposal does not change.** 0420 stays the dead-lock page and 0421 stays the wf seat page (DIRECTOR-WORDS-t530.md:47). 0423 (`one-worker`) is the safety page, and goes first after 0408, ahead of 0422 (t533u, DIRECTOR-WORDS-t533.md:15).

## 2. Grants

Each pass's may-touch must be disjoint from every page still open when that pass is packed:
- 0407 holds `src/render.rs`;
- 0408 holds `src/cmd.rs`, `src/lib.rs` and `src/page.rs`;
- 0419 holds `src/git.rs`;
- 0423 holds `src/cmd.rs`, `src/page.rs` and `tests/page_0423.rs` (docs/plan/GROK-BUILDER-QUEUE.md:101 @04c13954).

The passes' may-touch lists are also disjoint from each other:

| Pass | May touch | Why these files only |
|---|---|---|
| 0422.05.01 | `src/report.rs` (new), `src/lib.rs`, `tests/page_0422_01.rs` | A new module must be declared in `src/lib.rs` (`mod report;`) to compile. The `setup` and `report` dispatch and `writes()` are there too (src/lib.rs:5-13, :113-122, :232-247). Pushing uses the existing public `git::git` (src/git.rs:8), so `src/git.rs` stays with 0419. |
| 0422.05.02 | `src/page.rs`, `tests/page_0422_02.rs` | `KINDS`, `order()` and `apply()` (src/page.rs:125-129, :204-280) |
| 0422.05.03 | `src/cmd.rs`, `tests/page_0422_03.rs` | `ret`, `check` and `intake` (src/cmd.rs:488-579, :605-667, :724-794) |
| 0422.05.04 | `src/render.rs`, `src/status.rs`, `tests/page_0422_04.rs` | views and verify (src/render.rs:611, :679-693); the feed in `src/status.rs`, which no open page lists (docs/plan/GROK-BUILDER-QUEUE.md:84-101 @04c13954) |
| 0422.05.05 | `docs/REPORTS.md` (new), `tests/page_0422_05.rs` | Docs only. Kit `AGENTS.md` is not granted: its hash is pinned in every pack, and changing it locks open passes (src/render.rs:225). `README.md` stays with 0498. |

Check of disjointness:
- No file appears in two passes, so no pass ever re-takes a file another pass released.
- Each source file is also in exactly one of 0407, 0408, 0419 or 0423 at most, which is why each pass waits for that holder (section 3).
- Each pass has its own test file (`_01` to `_05`), so a later pass never edits an earlier pass's tests.

## 3. Order

Nothing below is packed until lab 0705 closes (DIRECTOR-WORDS-t530.md:47).

The whole order:

```
0408 closed (+ its trial)
  -> 0423 one-worker (holds src/cmd.rs, src/page.rs; first after 0408, t533u)
  -> 0705 closed
  -> 0422 report-system, next in the queue (t530u/t531u reading, DIRECTOR-WORDS-t530.md:41, :47):
       05.01 -> 05.02 -> 05.03 -> 05.04 -> 05.05   (one pass at a time, t533u)
```

What each pass waits on:

| Pass | Waits on (files) | Waits on (passes and pages) |
|---|---|---|
| 0422.05.01 | `src/lib.rs` free: 0408 closed and its trial done (0423 does not hold `src/lib.rs`) | 0705 closed. 0423 packed first (t533u), even though 05.01 shares no file with it. |
| 0422.05.02 | `src/page.rs` free: 0423 closed and its trial done | 05.01 closed (one pass at a time) |
| 0422.05.03 | `src/cmd.rs` free: 0423 closed and its trial done. 0422 must not take `src/cmd.rs` before 0423 (pack overview; DIRECTOR-WORDS-t533.md:15). | 05.01 and 05.02 closed, because it calls `report::` and needs the `report` kind |
| 0422.05.04 | `src/render.rs` free: 0407's trial done, and no later holder (0413, 0406, 0414) open at that time | 05.02 closed (it renders the kind) and 05.03 closed (one pass at a time) |
| 0422.05.05 | none held | 05.03 closed, so the doc describes what wf really prints |

**Files are held per pass.**
- Today a page holds its files until its trial passes (docs/plan/GROK-BUILDER-QUEUE.md:108 @04c13954).
- Here, each 0422 pass holds only its own may-touch, until that pass's trial passes.
- But "next in the queue" (DIRECTOR-WORDS-t530.md:47) means Prima does not pack 0409, 0406, 0411 or 0412 on `src/cmd.rs`, `src/lib.rs` or `src/page.rs` until 0422.05.03's trial is done. Otherwise another page could take `src/cmd.rs` between 0422's passes.

**A queue conflict, raised, not resolved.**
- The queue doc at 04c13954 still has 0409 right after 0423 (docs/plan/GROK-BUILDER-QUEUE.md:131, :136), with 0422 "after 0705 and 0423" (:127).
- The t530u/t531u reading puts 0422 next once 0705 closes (DIRECTOR-WORDS-t530.md:41, :47).
- If 0423 and 0705 both close before 0409 is packed, the reading says 0422 goes before 0409. Prima should make the queue doc say so (axiom 1: the order is Matthew's).

**Retiring the stopgap.**
- Until 0422.05.03 closes, every worker keeps pushing the stopgap report (docs/plan/REPORTS.md).
- After 0422.05.03's trial passes, packs stop including the snippet, and the stopgap `reports/` tree stays as history.
- 0422.05.04 and 05.05 are the first passes whose own reports are written by wf.

**Trials.**
- Each 0422 pass gets a lab trial in the wave after it, as other work does (`tests/lab_0422_0N.rs` on 0701; docs/plan/GROK-BUILDER-QUEUE.md:104 @04c13954).
- The 05.03 trial must:
  - kill wf after the append, and show that no `.wf-lock` is left and `--retry` lands the report (FAILURES.md section 4);
  - show that a real `wf check` always pushes its report (t530u).
