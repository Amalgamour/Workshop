# Lab 0705: worker-report spec

Page 90.50.10.0705, pass 05.01. Builder: Claude. Status: `9`.
Every item here is a **Claude proposal** for the build pages in BUILD-PAGES.md, unless it is cited as existing behaviour.
Code cites are wf at a823ee28. "Today" means a823ee28.

## 1. Config

**File.** `<WF_ROOT>/.wf/config.json`.
- One per run folder. `WF_ROOT` is the run folder; today wf reads it from the environment (src/lib.rs:127).
- The `.wf/` folder is added to the run folder's `.git/info/exclude` at setup. It is never staged, published or pushed, and `git checkout -- pages` never touches it.

**Fields** (JSON object, all strings unless noted):

| Field | Required | Meaning | Example |
|---|---|---|---|
| `version` | yes | config format version, number | `1` |
| `worker` | yes | the worker's name. It is the default for `--as` when `WF_AS` is not set (today: src/lib.rs:128). | `"Claude"` |
| `where` | yes | the machine and folder, printed on the prompt's first line (docs/plan/GROK-BUILDER-QUEUE.md:34) | `"Matthew's PC, D:\\Git\\claude"` |
| `wf_rev` | yes | the wf build the run folder expects. wf refuses to write a report if its own build differs (section 2). | `"a823ee284574be3d9f6247925b9088137a27a539"` |
| `report.repo` | yes | the work clone under `WF_ROOT` that pushes. It is the same folder intake reads (src/cmd.rs:606). | `"work"` |
| `report.branch` | yes | the branch reports are pushed to | `"returns"`, or `"prima/build"` for a core run folder (docs/plan/CORE-RUN.md:10-12) |
| `report.path` | yes | the folder on that branch for readable report copies | `".workshop/reports"` |
| `report.push` | no, default `true` | `false` records the report locally and queues the push (FAILURES.md section 2). Use it for a worker with no git network, such as Codex in a sandbox (FAILURES.md section 3). | `true` |

**Who writes it, once.**
- `wf setup` writes it when Matthew or Prima sets up the worker (WORKER-SETUP.md section 1).
- After that, only `wf setup --update` changes it. That command shows the old and new values and writes a `setup` report.
- Prompts never carry these values again.
- A hand edit is allowed, since the file is not a page view. But wf checks the file on every command that reports, and refuses an unknown field or a missing required one, naming the field.

Why a file and not environment variables: `WF_ROOT` and `WF_AS` must be set again in every new terminal (docs/plan/GROK-BUILDER-QUEUE.md:30). That is exactly the "per prompt" repetition t527u asks to remove. `WF_ROOT` stays, because it is how wf finds the run folder. Everything else moves into the file.

## 2. Commands

Common steps for every reporting command ("the report steps"):
1. Load the config. Refuse with a named field if it is missing or invalid. Refuse if this wf's build is not `wf_rev`.
2. Sync the page log from the packs branch before appending, so the report extends the newest log. This matters because Prima's packs entries otherwise make intake refuse the worker's log (src/cmd.rs:629; see FAILURES.md section 1).
   - If the local log is a prefix of the packs log, take the packs log.
   - If the two logs have diverged, stop and write nothing.
3. Under the page lock (src/lib.rs:83-110): append one `report` entry (section 4), then reprint the views (src/render.rs:685-690).
4. Release the lock.
5. In `report.repo`:
   - check out `report.branch` at `origin/<branch>`;
   - copy the page log to `.workshop/logs/<page>/log.jsonl` (as src/cmd.rs:559-562 does today);
   - write the report copy to `<report.path>/<page>/05.NN/<seq>-<worker>-<kind>.md`;
   - `git add --` both paths, and commit with the message `wf: report <page>.05.NN <kind> <worker>` and a `Builder: <worker>` trailer (docs/plan/REPORTS.md:26).
6. Push. If rejected: fetch, merge and retry up to 3 times, as `push_log` does today (src/cmd.rs:565-578). Never force. On final failure, see FAILURES.md section 1.
7. Print, as the last lines:
   - `report <seq> written (<kind>)`
   - `pushed <branch> <commit>`, or `report recorded locally; not pushed: <why>. Run: wf report --retry`

Steps 5-7 run when `report.push` is true. When it is false, step 5 still commits locally, and the push is queued (FAILURES.md section 2).

| Command | Today (a823ee28) | With reports |
|---|---|---|
| `wf return <page> <NN> --branch B --commit C --file F --push` | records `return`, merges the commit, pushes the log (src/cmd.rs:488-540) | after the `return` entry, runs the report steps with kind `build`, or `lab` on pages 0700-0799. The report body is the return file text (it is already in the `return` entry, src/cmd.rs:524-525) plus wf's facts. One push carries the commit, the log and the report copy, replacing today's separate `push_log`. |
| a refused return | records `return-refused` (src/cmd.rs:518-520) and pushes nothing | runs the report steps with kind `build`, and the refusal text as the body. Prima then sees refusals without asking. |
| `wf check <page> <NN>` | appends `check`, reprints the views, pushes nothing (src/cmd.rs:786-793) | after the `check` entry, runs the report steps with kind `check`. The body is the check report (src/cmd.rs:785). `--dry-run` still writes and pushes nothing (src/cmd.rs:758-762). |
| `wf setup --as <name> --where W --branch B [--repo work] [--path P] [--no-push]` | does not exist | writes `.wf/config.json` (section 1) and adds `.wf/` to `.git/info/exclude`. It fetches `packs` and `report.branch`, runs `verify` on one page as a smoke test, and pushes a `setup` report to `<report.path>/setup/<worker>/<stamp>.md`. There is no page log entry (DESIGN.md 4.1 Q1). |
| `wf report <page> <NN> --kind troubleshoot --file F` | does not exist | runs the report steps with kind `troubleshoot` and the file's text as the body. It is for a prompt-box fix that should be on record (DESIGN.md section 2). |
| `wf report --retry` | does not exist | pushes any queued report commits (FAILURES.md section 2) and prints what it pushed. Reports run no lock. |
| `wf intake` | takes a returned log only if it continues the local log (src/cmd.rs:625-632) | unchanged rule. Report entries come in with the log, and their views print. Also: when the returned log is a prefix of the local log, intake says "up to date", not "does not continue". Today it refuses with the same words as a real divergence (seen on 0702 on 2026-11-23). |

**Is a separate `wf report` command needed?** Yes, but only for two cases that no other command ends:
- `--kind troubleshoot`, and `--retry`.
- Build, lab and check reports are written by `return` and `check` themselves. That is what makes the report automatic (t527u, DW:11).

## 3. Report file

**Path on the branch:** `<report.path>/<page>/05.NN/<seq>-<worker>-<kind>.md`, for example `.workshop/reports/90.50.10.0705/05.01/0009-Claude-lab.md`.
- `<seq>` is the report entry's log number, padded to 4 digits. It is unique on the page and ordered, and needs no clock.
- The stopgap names used a local timestamp (docs/plan/REPORTS.md:17, :22). Two reports made in the same minute would collide, and clocks differ across machines.
- Setup reports: `<report.path>/setup/<worker>/<YYYYMMDDTHHMMSSZ>.md` (UTC, from src/log.rs:46-59).

**The copy on the page's pass:** `pages/<page>/05.NN/REPORT-<seq>-<worker>-<kind>.md`.
- It is a view printed from the log entry by render (BUILD-PAGES.md, page 0425), the same as PACK.md and PROMPT.md (src/render.rs:89).
- `wf verify` checks it against the log, like every other view (src/render.rs:611).

**Format.** Plain markdown. The first block is fields that wf fills; the body follows.

```
# Report 90.50.10.0705.05.01 lab by Claude
page:    90.50.10.0705
pass:    05.01
kind:    lab                     (build | lab | check | setup | troubleshoot)
worker:  Claude
where:   Matthew's PC, D:\Git\claude
wf:      a823ee284574be3d9f6247925b9088137a27a539
entry:   9                       (this report's log entry)
of:      8                       (the return or check entry it reports, if any)
commit:  <the worker's commit>   (build and lab)
verdict: pass | fail             (check)
time:    2026-11-23T18:10:00Z    (UTC, src/log.rs:46)
took:    <minutes, from the claim entry to this entry>   (build and lab)

<body: the return file, the check report, or the --file text>
```

Required fields by kind:

| Field | build / lab | check | setup | troubleshoot |
|---|---|---|---|---|
| page, pass, kind, worker, where, wf, entry, time | yes | yes | page and pass absent; the rest yes | yes |
| of | the `return` (or `return-refused`) entry | the `check` entry | - | - |
| commit | yes | the checked commit | - | - |
| verdict | - | yes | - | - |
| took | yes | yes, from intake to check | - | - |
| body | the return file | the check report | config, the verify result, the branches | the `--file` text |

**Characters.** wf applies the same refusals it applies to every flag and field today (kit AGENTS.md "Command flags and pack fields are checked in one place"). A body that came from a worker is shown escaped in the views, as return text is today.

## 4. Hash chain

**New entry kind: `report`.** Fields under `data`:

| Field | Type | Meaning |
|---|---|---|
| `pass` | number | the pass, 1-98. Absent only for a page-level troubleshoot. |
| `kind` | string | `build`, `lab`, `check` or `troubleshoot`. `setup` never chains (DESIGN.md 4.1 Q1). |
| `of` | number | the entry this report reports (`return`, `return-refused` or `check`). Absent for troubleshoot. |
| `worker` | string | as in the config |
| `where` | string | as in the config |
| `wf` | string | the build that wrote it |
| `path` | string | the branch path of the readable copy |
| `text` | string | the full report file text |
| `hash` | string | the sha256 of `text` (src/log.rs:23-26) |

The entry's own `actor` is the worker, and its `role` is `builder` or `checker`, as for `return` and `check` (src/cmd.rs:524, :786). The entry is chained like every other entry: its `prev` is the sha256 of the line before it (src/log.rs:1-3, :96-99).

There is no "pushed" field. A push happens after the append, so the entry cannot hold the commit that contains it. Whether a report reached GitHub is shown by the branch itself: `wf intake` on Prima's side either takes the entry or does not.

**Order rules** (in `Page::order`, src/page.rs:204-280):
- `report` is allowed at any tail of an existing pass. A report records something that already happened; it changes no tail.
- `of`, when given, must name an earlier entry of kind `return`, `return-refused` or `check` for the same pass.
- `kind` must match that entry: `check` for a check; `build` or `lab` for a return.
- One report per `of`. A second one is refused, so a retry cannot double-log. This follows the existing rule that "a retry is not mistaken for a no-op" (src/render.rs:683-684).

**Hooks needed later.** Each hook names the file that holds it and the build page that takes it (BUILD-PAGES.md).

| File | Hook | Page |
|---|---|---|
| src/page.rs | add `"report"` to `KINDS` (page.rs:125-126, a closed list of 17); do not add it to `PASS_KINDS` (:129), since it changes no tail; the order rules above in `order()`; `apply()` folds reports into the pass so status and render can list them | 0423 |
| src/report.rs (new) | load and check the config; build the report text; write the entry through `Page::add`; commit and push with the existing `git::git` helper (src/git.rs:8 is `pub`), so src/git.rs needs no change; the outbox and `--retry` | 0422 |
| src/lib.rs | `mod report;`; dispatch `setup` and `report`; `writes()` (lib.rs:113-122): `report --retry` takes no page lock, and `setup` takes none (no page); the config default for `--as` (lib.rs:128) | 0422 |
| src/cmd.rs | `ret` calls the report steps after the `return` or `return-refused` entry, in place of `push_log` (cmd.rs:533-536, :558-579); `check` calls them after its append (:786-793); `intake` says "up to date" on a prefix (:629-632) | 0424 |
| src/render.rs | print `05.NN/REPORT-<seq>-<worker>-<kind>.md` views; list reports in `05.md` under their pass; `verify` covers the new views (render.rs:611, :693) | 0425 |
| src/status.rs | show `report` lines in the status feed | 0425 (status.rs is not held by any open page) |
