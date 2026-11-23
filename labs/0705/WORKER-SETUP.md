# Lab 0705: setting up a worker so reports work

Page 90.50.10.0705. Builder: Claude. Status: `9`. Updated in pass 05.02 for t530u: every worker gets its own page in band N6.
"Today" means wf at a823ee28, the build every worker runs now (docs/plan/GROK-BUILDER-QUEUE.md:30). Steps marked **(after build)** need the report-system work order 90.50.10.0422 (BUILD-PAGES.md). Until then, a worker uses the stopgap in docs/plan/REPORTS.md.

**Matthew** (t530u): "N6 is where worker pages should live." "One page per worker" "The title should be the worker's name." (docs/review/DIRECTOR-WORDS-t530.md:11, :15, :19). The band rule is pending in docs/review/PENDING-RULES.md:5-18 until it can be written into seqAddr.md.

**Matthew** (t528u, DW:15): "We need this before we can setup more workers." So setting up a worker is the first thing that must produce a report.

## 1. New worker

Steps to add a worker named `<Name>` on a machine. Today's steps follow docs/plan/GROK-BUILDER-QUEUE.md:21-30 and docs/plan/CORE-RUN.md:25-43; the new ones are marked.

0. **The worker's page, in band N6** (t530u). Prima starts it, before anything else, as for any page (`wf init-page`, run by Matthew or by Prima as the real runner, as on 0705's face 06).
   - **Address:** `90.50.10.06NN`, the first open slot after 0600. 0600 is the band door and 0699 is the band's continuation, so worker pages sit on 0601-0698 (docs/review/PENDING-RULES.md:13, :16; docs/review/DIRECTOR-WORDS-t530.md:21). No 06NN page exists today, so the first worker page is 0601.
   - **Title:** the worker's name in lowercase. Titles allow only lowercase letters, digits and hyphens, and start with a letter (seqAddr.md:112@8e96151d). So Grok-Check is `grok-check` and Grok-6 is `grok-6`. A name that cannot become a legal title (for example, one that starts with a digit) is raised to Matthew, never changed silently (seqAddr.md:116@8e96151d).
   - **The exact name** (capitals included) is kept in the page stamp and in the worker config (PENDING-RULES.md:15). At a823ee28 the init entry has no worker-name field (src/cmd.rs:204-206: address, title, person, prime, grant). Until a later pass adds one (SPEC.md section 4), Prima writes the exact name in the page's face 01, and `wf setup` writes it to `.wf/config.json` (`worker`).
   - **One page per worker,** never shared (DIRECTOR-WORDS-t530.md:15). A page has one worker at a time (t533u, DIRECTOR-WORDS-t533.md:5), which matches a page that belongs to one worker.
   - **What chains there:** every setup report for that worker. The first setup is pass `06NN.05.01`, and each later change to the worker's setup is a later pass (steps 4 and 6).
1. **Folder.** One folder per worker, for example `D:\Git\grok6`. One worker never shares a run folder with another: the page lock and the log are per run folder (src/lib.rs:83-110).
2. **wf build.** Install wf from the pinned commit into `<folder>\wf-bin`:
   `cargo install --git https://github.com/Amalgamour/Workshop.git --rev <rev> --locked --root <folder>\wf-bin wf`.
   The builder must never build into this copy (kit AGENTS.md, "The tool you run").
   - wf has no `--version` today. `wf.exe --version` answers "give the page address" (src/lib.rs:148).
   - Cargo's install record `<folder>\wf-bin\.crates.toml` names the rev. Check it there until wf prints its own build.
3. **Run folder.**
   - `git clone -c core.autocrlf=false -b packs https://github.com/Amalgamour/Workshop.git <folder>\wf-run`.
   - Then the work clone: `... -b returns ... <folder>\wf-run\work`, or `-b prima/build` for a core worker (docs/plan/CORE-RUN.md:30-32).
4. **Setup pass on the worker's page (after build).** Prima packs `06NN.05.01` (set up <Name>). The pass needs to commit only its return file, which a return always allows (kit AGENTS.md, "As a builder", step 3), so its may-touch can be as small as the grant Prima gives the page. The worker then:
   1. pulls packs and claims it: `wf claim 90.50.10.06NN 01 --as <Name>`;
   2. runs, in the run folder with `WF_ROOT` set: `wf setup --as <Name> --where "<machine>, <folder>" --branch returns`
      - for a core worker, use `--branch prima/build`;
      - add `--no-push` for a worker whose shell has no git network (FAILURES.md section 3);
      - this writes `.wf/config.json` (SPEC.md section 1) and runs a `verify` smoke test on the worker's own page;
   3. fills the return file and runs `wf return 90.50.10.06NN 01 --branch returns --commit <sha> --file <return> --push`.
   - That return writes and pushes the `setup` report. It chains on the worker's page (t530u). Prima reads it on GitHub at `.workshop/reports/90.50.10.06NN/05.01/`, or in her own pages after `wf intake`.
   - Grok-Check checks the setup pass like any other. Its check report is pushed too (t530u Q3).
5. **Name.** The name in the config is the name wf writes in every entry. It must match the first line of every prompt: `Builder: <Name> (<machine>, <folder>)` (docs/plan/GROK-BUILDER-QUEUE.md:34).
   - wf does not check a pack's named builder at claim. The first claim wins (docs/plan/GROK-BUILDER-QUEUE.md:40).
   - The setup report is where Prima learns the name exists.
6. **Prima's side.** Prima adds the worker to the queue (docs/plan/GROK-BUILDER-QUEUE.md:21-28) only after the setup pass has closed. That proves the worker's claim, return, push and check all work.
   - A later change to the worker (a new wf build, a new branch, a move to another folder) is a new pass on the same page (`06NN.05.02`, and so on), with `wf setup --update`.
   - The old setup stays in the page's line (axiom 6).

Until the report-system work order lands:
- Step 0 can be done today, because `wf init-page` exists (src/lib.rs:138-144). The page and its setup pass give the setup a home in the chain now.
- Steps 1-3 and 5 are done as today.
- In step 4, `wf setup` does not exist yet. The worker sets `PATH`, `WF_ROOT` and `WF_AS` in each new terminal instead, and still claims and returns the setup pass.
- The return pushes the log (src/cmd.rs:533-536). The stopgap snippet adds a readable report (docs/plan/REPORTS.md:30-74, with `$page = "90.50.10.06NN"`, `$pass = "05.01"`, `$kind = "setup"`).
- Once worker pages exist, the snippet's page-less `$page = "setup"` branch (REPORTS.md:21, :42-44) is no longer needed. A setup report has a page.

## 2. Config once

What is set once per run folder, and never again per prompt (**Claude proposal**; fields in SPEC.md section 1):

| Set once in `.wf/config.json` | Why it is not per prompt |
|---|---|
| `worker` (the name) | It is the same for every pass the worker takes. Today `WF_AS` must be set in every terminal (docs/plan/GROK-BUILDER-QUEUE.md:30), and a typo there writes a wrong actor into a chained log that cannot be edited (src/log.rs:1-3). |
| `where` | It is the same for every prompt's first line. |
| `wf_rev` | It pins the tool that judges the work (kit AGENTS.md, "The tool you run"). It is changed only by a deliberate update: a new setup pass on the worker's N6 page, whose return writes the setup report. |
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
