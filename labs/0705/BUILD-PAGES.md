# Lab 0705: proposed Grok build pages

Page 90.50.10.0705, pass 05.01. Builder: Claude. Status: `9`.
Everything here is a **Claude proposal**. No page is packed by this lab. Packing waits until 0705 closes. The rule is Prima's effect note on t528u (docs/review/DIRECTOR-WORDS-t526-t528u.md:17) and docs/plan/GROK-BUILDER-QUEUE.md:88.

## 1. Split

Numbers start at 0422, as the pack asks. 0420 (dead lock) and 0421 (wf seat) stay as suggested (docs/plan/GROK-BUILDER-QUEUE.md:86-87). All five pages are in the dev band, 0400-0499, the stage 1 band for wf (seqAddr.md:323@8e96151d). Every page lists `Lab: 90.50.10.0705`, and this lab lists them back under Serves when they are packed (face 01 of 0705).

| Page | Title | Outcome (done when, short form) |
|---|---|---|
| 0422 | report module and config | `src/report.rs` exists and is declared. `wf setup` writes and checks `.wf/config.json` (SPEC.md section 1) and adds `.wf/` to `.git/info/exclude`. The outbox and `wf report --retry` push queued commits with merge-and-retry and never force (FAILURES.md sections 1-2). Unit tests cover config refusals and outbox order. |
| 0423 | `report` log kind | `"report"` is in `KINDS`, not in `PASS_KINDS`. `order()` enforces the rules in SPEC.md section 4: any tail, a valid `of`, a matching kind, one report per `of`. `apply()` keeps a pass's reports. Old logs still load. A log with a bad report entry is refused with entry and rule named. |
| 0424 | commands write reports | `return --push` and a refused return write a `build`/`lab` report and push once, with the commit, the log and the copy. `check` writes a `check` report and pushes it; `--dry-run` still writes nothing. `wf report --kind troubleshoot` works. The lock is released before any fetch or push. `intake` says "up to date" on a prefix log. Each command's last lines are as in SPEC.md section 2, step 7. |
| 0425 | report views and status | render prints `pages/<page>/05.NN/REPORT-<seq>-<worker>-<kind>.md` from each entry. `05.md` lists them under their pass. `wf verify` covers them. `wf status` shows report lines in the feed. |
| 0426 | report docs and stopgap retirement | A kit doc for reports (proposed: `docs/REPORTS.md`) says how workers are set up and what wf prints. Worker setup follows WORKER-SETUP.md section 1. The stopgap section of `docs/plan/REPORTS.md` on prima/build is marked superseded by Prima. That is Prima's docs, not this page's grant. |

## 2. Grants

Each grant is disjoint from the others in this split, and from the open pages 0407 (`src/render.rs`), 0408 (`src/cmd.rs`, `src/lib.rs`, `src/page.rs`) and 0419 (`src/git.rs`) (docs/plan/GROK-BUILDER-QUEUE.md:73-74, :85).

| Page | May touch | Why these files only |
|---|---|---|
| 0422 | `src/report.rs` (new), `src/lib.rs`, `tests/page_0422.rs` | A new module must be declared in `src/lib.rs` (`mod report;`) to compile. The `setup` and `report` dispatch and `writes()` are there too (src/lib.rs:5-13, :113-122, :232-247). Pushing uses the existing public `git::git` (src/git.rs:8), so `src/git.rs` is not needed, and 0419 keeps it. |
| 0423 | `src/page.rs`, `tests/page_0423.rs` | `KINDS`, `order()` and `apply()` all live in page.rs (src/page.rs:125-129, :204-280). |
| 0424 | `src/cmd.rs`, `tests/page_0424.rs` | `ret`, `check` and `intake` are in cmd.rs (src/cmd.rs:488-579, :605-667, :724-794). |
| 0425 | `src/render.rs`, `src/status.rs`, `tests/page_0425.rs` | Views and verify are in render.rs (src/render.rs:611, :679-693). The feed is in status.rs. No open page lists `src/status.rs` (docs/plan/GROK-BUILDER-QUEUE.md:71-89). |
| 0426 | `docs/REPORTS.md` (new kit doc), `tests/page_0426.rs` | Docs only. Kit `AGENTS.md` is not in the grant: its sha256 is pinned in every pack, and changing it locks open passes mid pass (src/render.rs:225; kit AGENTS.md "Read first"). `README.md` is left to 0498 (docs/plan/GROK-BUILDER-QUEUE.md:83). |

Check of disjointness:
- No file appears twice in the table above.
- `src/lib.rs` (0422), `src/page.rs` (0423) and `src/cmd.rs` (0424) are each still held by 0408 today, so each of those pages waits on 0408, not on each other's files (section 3).
- `src/render.rs` (0425) is held by 0407, then 0413, 0406 and 0414 (docs/plan/GROK-BUILDER-QUEUE.md:73, :76-77, :80).

## 3. Order

No page here is packed until lab 0705 closes (t528u; docs/plan/GROK-BUILDER-QUEUE.md:88).

Each page waits on:

| Page | Waits on (files) | Waits on (pages) | Can run beside |
|---|---|---|---|
| 0422 | `src/lib.rs` free: 0408 closed and its trial done | 0705 closed | 0423 (disjoint files) |
| 0423 | `src/page.rs` free: 0408 closed and its trial done | 0705 closed | 0422 |
| 0424 | `src/cmd.rs` free | 0422 and 0423 closed. It calls `report::` and needs the `report` kind. | 0425, if render is free by then |
| 0425 | `src/render.rs` free: 0407's trial done, and no later holder open | 0423 closed. It renders the kind. | 0424 |
| 0426 | none held | 0424 closed. The doc describes what wf really prints. | the 0424 and 0425 trials |

**The queue question** (DESIGN.md 4.1, Q2; for Matthew):
- Today `src/lib.rs`, `src/page.rs` and `src/cmd.rs` stay held after 0408 by 0409, 0406, 0411 and 0412 through wave 10 (docs/plan/GROK-BUILDER-QUEUE.md:119-134).
- If those pages keep their places, 0422-0424 cannot start until wave 11. Workers would use the stopgap (docs/plan/REPORTS.md) until then.
- Proposed default: put 0422 and 0423 right after 0408's trial, ahead of 0409, then 0424 next. Matthew said "We need this before we can setup more workers" (docs/review/DIRECTOR-WORDS-t526-t528u.md:15).
- 0409, 0406, 0411 and 0412 each then start one wave later. Whether to move them is Matthew's call, not this lab's (axiom 1).

**Retiring the stopgap.**
- Until 0424 closes, every worker keeps pushing the stopgap report (docs/plan/REPORTS.md:30-74).
- After 0424's trial passes, packs stop including the snippet, and the stopgap `reports/` tree is kept as history, not moved.
- The first pass of 0426 is the first page whose own reports are written by wf.

Trials:
- Each page gets its lab trial in the wave after it, as other work pages do: `tests/lab_0422.rs` and so on, on 0701 (docs/plan/GROK-BUILDER-QUEUE.md:91).
- The trial for 0424 should include a killed push. Kill wf after the append; no lock may be left, and `--retry` must land the report. That is the case that went wrong on 2026-11-23 (FAILURES.md section 4).
