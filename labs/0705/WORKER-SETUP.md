# Lab 0705: setting up a worker so reports work

Page 90.50.10.0705, pass 05.01. Builder: Claude. Status: `9`.
"Today" means wf at a823ee28, the build every worker runs now (docs/plan/GROK-BUILDER-QUEUE.md:30). Steps marked **(after build)** need the pages in BUILD-PAGES.md. Until then, a worker uses the stopgap in docs/plan/REPORTS.md.

**Matthew** (t528u, DW:15): "We need this before we can setup more workers." So setting up a worker is the first thing that must produce a report.

## 1. New worker

Steps to add a worker named `<Name>` on a machine. Today's steps follow docs/plan/GROK-BUILDER-QUEUE.md:21-30 and docs/plan/CORE-RUN.md:25-43; the new ones are marked.

1. **Folder.** One folder per worker, for example `D:\Git\grok6`. One worker never shares a run folder with another: the page lock and the log are per run folder (src/lib.rs:83-110).
2. **wf build.** Install wf from the pinned commit into `<folder>\wf-bin`:
   `cargo install --git https://github.com/Amalgamour/Workshop.git --rev <rev> --locked --root <folder>\wf-bin wf`.
   The builder must never build into this copy (kit AGENTS.md, "The tool you run").
   - wf has no `--version` today. `wf.exe --version` answers "give the page address" (src/lib.rs:148).
   - Cargo's install record `<folder>\wf-bin\.crates.toml` names the rev. Check it there until wf prints its own build.
3. **Run folder.**
   - `git clone -c core.autocrlf=false -b packs https://github.com/Amalgamour/Workshop.git <folder>\wf-run`.
   - Then the work clone: `... -b returns ... <folder>\wf-run\work`, or `-b prima/build` for a core worker (docs/plan/CORE-RUN.md:30-32).
4. **Config, once (after build).** In the run folder, with `WF_ROOT` set:
   `wf setup --as <Name> --where "<machine>, <folder>" --branch returns`
   - For a core worker, use `--branch prima/build`.
   - Add `--no-push` for a worker whose shell has no git network (FAILURES.md section 3).
   - This writes `.wf/config.json` (SPEC.md section 1) and runs a `verify` smoke test.
   - It pushes a `setup` report, which Prima reads on GitHub at `.workshop/reports/setup/<Name>/`.
5. **Name.** The name in the config is the name wf writes in every entry. It must match the first line of every prompt: `Builder: <Name> (<machine>, <folder>)` (docs/plan/GROK-BUILDER-QUEUE.md:34).
   - wf does not check a pack's named builder at claim. The first claim wins (docs/plan/GROK-BUILDER-QUEUE.md:40).
   - The setup report is where Prima learns the name exists.
6. **Prima's side.** Prima adds the worker to the queue (docs/plan/GROK-BUILDER-QUEUE.md:21-28) only after the setup report has landed. That is the proof the worker's push works.

Until the build pages land, steps 1-3 and 5 are done as today. Step 4 is replaced by setting `PATH`, `WF_ROOT` and `WF_AS` in each new terminal, and by pushing a setup report with the stopgap snippet (docs/plan/REPORTS.md:30-74, with `$page = "setup"`).

## 2. Config once

What is set once per run folder, and never again per prompt (**Claude proposal**; fields in SPEC.md section 1):

| Set once in `.wf/config.json` | Why it is not per prompt |
|---|---|
| `worker` (the name) | It is the same for every pass the worker takes. Today `WF_AS` must be set in every terminal (docs/plan/GROK-BUILDER-QUEUE.md:30), and a typo there writes a wrong actor into a chained log that cannot be edited (src/log.rs:1-3). |
| `where` | It is the same for every prompt's first line. |
| `wf_rev` | It pins the tool that judges the work (kit AGENTS.md, "The tool you run"). It is changed only by a deliberate update, which writes a setup report. |
| `report.repo`, `report.branch`, `report.path` | This is "taught where it should land them" (t527u, DW:11). |
| `report.push` | It is a property of the shell (network or not), not of the task. |

What stays per terminal: `WF_ROOT`, because it is how wf finds the run folder and therefore the config (src/lib.rs:127), and `PATH` to `wf-bin`.

What stays per prompt: only the task. That is the page, the pass, and anything Matthew says for this one job.

## 3. Prompt vs pack

**Matthew** (t528u, DW:15): "For brief fast messages like we are trouble shooting. prompt boxes are good. But for normal wf loops we use packs > returns > review through github with WF controlling it."

| Use a prompt box when | Use the normal loop (pack > return > review) when |
|---|---|
| A step failed and the worker stopped, as the rules say. Examples: a refused intake, a stale `.wf-lock`, a rejected push. | Any change to a file under a grant |
| Matthew approves a one-off action the rules otherwise forbid. Example: removing a stale lock and running `verify --fix` for one page on 2026-11-23. | Any build, lab, check or setup |
| A question can be answered in a line | Anything Prima must later read, sign off or close |
| The worker must report what it saw before it does anything else | Anything that needs a record in a page's log |

Rules that keep the two apart (**Claude proposal**):
- A prompt box never carries pack content: no new jobs, grants or done-when lines. If the answer to a troubleshooting question is "do more work", Prima packs it.
- A prompt box never replaces a report. If a troubleshooting step changed a page, a branch or a run folder, the worker files `wf report --kind troubleshoot` (SPEC.md section 2), so the fix is in the page's record. Until that exists, the stopgap snippet with `$kind = "other"` does it (docs/plan/REPORTS.md:19).
- The first line of every prompt, box or loop, stays `Builder: <Name> (<machine>, <folder>)`. Then whoever reads it can match it to the worker's config.
