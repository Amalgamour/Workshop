# Lab 0705: the wf worker-report system, design

Page 90.50.10.0705, pass 05.01. Builder: Claude (Matthew's PC, D:\Git\claude). Checker: Grok-Check.
Made: 2026-11-23. Status: `9`. Nobody has run a hostile trial on it yet. Research only: no code changed.

How to read this lab:
- **Matthew** marks his words, quoted from docs/review/DIRECTOR-WORDS-t526-t528u.md on prima/build at 661732f5 (cited as `DW:N`).
- **Claude proposal** marks my design choices. They are not rulings.
- Code cites are wf at a823ee284574be3d9f6247925b9088137a27a539, read with `git show a823ee28:<path>`.
- Plan cites are docs/plan/*.md on prima/build 661732f5.

The other files in this lab:
- SPEC.md: the config, commands, report file format and hash-chain entry.
- WORKER-SETUP.md: how to add a worker.
- FAILURES.md: what happens when a push or lock fails.
- BUILD-PAGES.md: the proposed Grok build pages.
- LESSONS.md: lessons from this lab.

## 1. Goal

**Matthew** (t526u, DW:7):
> "Going forward they should be pushing reports to you on Github. We need a wf space for those to land in pages. So you can retrieve and see the reports there. We use github as our nexus for information for now."

**Matthew** (t527u, DW:11):
> "That needs to be built into wf so when the worker is done, the wf sending the report once it is taught where it should land them."

What "reports live in pages" means here (**Claude proposal**):

1. **The record.** A report is a page record, not a loose file. Each report is one entry in the page's hash-chained log (`pages/<page>/log.jsonl`). That log is "the only truth" (src/lib.rs:2-3; src/log.rs:1-3). So a report is ordered with the pass it belongs to, it is covered by the chain, and nobody can quietly edit it afterwards.
2. **The view.** Every report also has a readable view, printed by wf from that entry, under the pass it reports on: `pages/<page>/05.NN/REPORT-<seq>-<worker>-<kind>.md`. A view is never written by hand, the same rule as every other page file (src/lib.rs:2-3).
3. **The copy on GitHub.** wf pushes the log, and a plain copy of the report text, to the configured branch. Prima can read the report on GitHub without running wf, or run `wf intake` and see it in her own pages.

GitHub is the nexus, as Matthew said (DW:7). Nothing in this design needs a server, a chat channel or a shared disk. The only transport is git push and git fetch, which wf already uses for returns (src/cmd.rs:545-579).

Why the log entry is the record, and not just a file (**Claude proposal**):
- A file under `reports/` (today's stopgap, docs/plan/REPORTS.md:15-17) is not chained. It can be rewritten in a later commit with nothing on the page to show it (axiom 6, Axioms.md:23@8e96151d).
- It is not linked to the pass in the page's own record (axiom 8, Axioms.md:27@8e96151d).
- The page log already travels to GitHub on `return --push` (src/cmd.rs:558-564), so a report entry rides the same path at no extra cost.

## 2. Loop

**Matthew** (t528u, DW:15): "For brief fast messages like we are trouble shooting. prompt boxes are good. But for normal wf loops we use packs > returns > review through github with WF controlling it."

There are two channels. They do not mix.

| | Normal loop | Prompt box |
|---|---|---|
| What it is for | All planned work: build passes, checks, labs, worker setup | Brief, fast troubleshooting: a failed step, a stale lock, a one-line question |
| Who drives it | wf. Prima packs; the worker claims, works, returns; the checker checks; Prima signs off and closes (kit docs/DESIGN.md:57-74) | Matthew, by hand, between a worker and Prima |
| Where it goes | GitHub: `packs` carries packs, `returns` carries returns, logs and reports | The chat window. Nothing is pushed unless a later wf command records it. |
| What is recorded | Every step is a log entry. Every finished step writes a report entry and pushes it (section 4). | Nothing is required. If a fix changes work, the next wf step records it, or the worker files a `troubleshoot` report (SPEC.md section 2). |

What "wf controlling it" means for reports (**Claude proposal**):
- The worker does not choose to send a report, or where to send it. The wf command that finishes the step writes the report and pushes it.
- The worker supplies only the words wf cannot know: the return file it already writes (template at pages/<page>/05.NN/RETURN-TEMPLATE.md), or a short note for a check.

The loop, with reports:

```
Prima:   draft > pack > publish-pack ................................> packs branch
Worker:  pull packs > claim > work > return --push ..................> returns: commit + log + build/lab report
Checker: intake > check ................................................> returns: log + check report   (new: check pushes)
Prima:   intake > reads reports (GitHub or pages/<page>/05.NN/REPORT-*.md) > signoff > close
```

Today `wf check` appends to the log and reprints views, but pushes nothing (src/cmd.rs:786-793). A check is therefore lost unless someone pushes the log by hand. That happened in this run folder on 2026-11-23: the 0703 pass 2 check entry 18 never reached GitHub (labs/0702/LESSONS.md, lesson 7). Closing that gap is part of this design (section 4).

## 3. Where reports land

**Matthew** (t527u, DW:11): wf sends the report "once it is taught where it should land them".

"Taught once" (**Claude proposal**):
- Each run folder has one config file, written once when the worker is set up.
- Every later wf command in that run folder reads it. No prompt, pack or command line repeats it.
- The file is `<WF_ROOT>/.wf/config.json`. It sits beside `pages/`, never inside it, so `git checkout -- pages` and `wf verify` never touch it (src/lib.rs:150, :154; the views are under pages/<page>/).
- JSON is used because wf already depends on serde_json and nothing else (Cargo.toml @a823ee28: serde_json, sha2). No new dependency is needed.
- SPEC.md section 1 gives the fields. The two Matthew named are where reports land:

| Field | Meaning | Default |
|---|---|---|
| `report.branch` | the GitHub branch reports are pushed to | `returns` (`prima/build` for a core run folder, docs/plan/CORE-RUN.md:10) |
| `report.path` | the folder on that branch where readable report copies go | `.workshop/reports` |

Where a report lands, end to end:

| Place | What | Written by | Read by |
|---|---|---|---|
| `pages/<page>/log.jsonl` (worker's run folder) | the `report` entry, chained | wf, on the finishing command | wf |
| `<report.branch>:.workshop/logs/<page>/log.jsonl` | the page log, including the report entry | wf push (same as `return --push` today, src/cmd.rs:558-564) | `wf intake` (src/cmd.rs:605-667) |
| `<report.branch>:<report.path>/<page>/05.NN/<seq>-<worker>-<kind>.md` | the report text, plain markdown | wf push, the same commit | Prima on GitHub, with no wf needed |
| `pages/<page>/05.NN/REPORT-<seq>-<worker>-<kind>.md` (Prima's run folder) | the view, printed from the log entry | `wf intake`, then render | Prima, in her own pages |

Why `.workshop/reports` and not today's `reports/` (**Claude proposal**):
- `.workshop/` is already the folder wf owns on the returns branch (`.workshop/logs/`, `.workshop/returns/`; src/cmd.rs:559).
- The stopgap `reports/` (docs/plan/REPORTS.md:28) stays as history and is never rewritten.
- Once wf sends reports, the stopgap snippet stops (BUILD-PAGES.md section 3).

## 4. When wf writes

**Matthew** (t527u, DW:11): "when the worker is done, the wf sending the report".

"Done" is the end of each of the five kinds of work the pack names. In each case, the wf command that ends the work writes and pushes the report. The worker runs no extra step. (**Claude proposal**, detailed in SPEC.md section 2.)

| Kind | The worker is done when | Command that writes the report | Report body comes from |
|---|---|---|---|
| `build` | the builder files a return | `wf return <page> <NN> ... --push` | the return file the builder already wrote (`.workshop/returns/<page>.05.NN.md`), plus wf's facts: the commit, the changed files and the entry numbers |
| `lab` | a lab builder files a return | the same `wf return ... --push`; the kind is `lab` when the page is in the lab band 0700-0799 (seqAddr.md:351@8e96151d) | the same as build |
| `check` | the checker files a check | `wf check <page> <NN>` (not `--dry-run`) | the check report wf already prints (src/cmd.rs:688-723, :785) |
| `setup` | a new worker's run folder is ready | `wf setup` (new; WORKER-SETUP.md) | wf's own facts: worker name, wf build, branches, config, and the result of a `verify` of one page |
| `troubleshoot` | a prompt-box fix changed something that should be on record | `wf report <page> <NN> --kind troubleshoot --file F` (new) | a short note the worker writes |

What wf does each time:
1. Builds the report text.
2. Appends a `report` entry to the page log, under the page lock (src/lib.rs:83-110).
3. Reprints the views.
4. Releases the lock.
5. Commits the page log and the report copy by path on the configured branch.
6. Pushes, without ever forcing. A rejected push is fetched, merged and retried, as `push_log` does today (src/cmd.rs:565-578).

Steps 5 and 6 run after the lock is released. A push that hangs or is killed can then never leave a stale `.wf-lock` behind (FAILURES.md section 4).

A report is written only when the step succeeds. A refused return already writes a `return-refused` entry (src/cmd.rs:518-520). That entry is pushed as its own report of kind `build`, so Prima sees refusals too.

A check that fails still writes a check report: a failed check is finished work.

### 4.1 Questions for Matthew (t528u: "message me when your ready")

Each question has a proposed default. The default is a **Claude proposal**, not a decision.

1. **Setup reports have no page.** Where do they chain?
   - (a) Proposed default: no chain. The file goes to `<report.path>/setup/<worker>/<stamp>.md` on the branch, and the push commit is the only record.
   - (b) A workers page in the lab or system range that logs every setup.
2. **Report pages jump the `src/lib.rs` queue?** The build pages need `src/lib.rs` and `src/page.rs`. 0408, then 0409, 0406, 0411 and 0412, hold those files in waves 1-10 (docs/plan/GROK-BUILDER-QUEUE.md:79-82, :124-132). You said "We need this before we can setup more workers" (DW:15).
   - (a) Proposed default: let the report pages go right after 0408 closes, ahead of 0409.
   - (b) Keep the queue, and add workers on the stopgap until wave 11.
3. **Should `wf check` push?** Today it never pushes (src/cmd.rs:786-793).
   - (a) Proposed default: yes, always, when a config exists.
   - (b) Only with `--push`, like return.
