# Grok builder queue

t517u (23 Nov 2026): Grok builders are cheapest and best. They should do a lot of the work, especially the core's local infrastructure. The problem is how to get work to many of them at once.

t518u-t519u: add as many Grok builders as the waves need. A dedicated checker named Grok-Check does the checks.

t522u: 0419.05.01 goes to Grok-3 (`D:\Git\grok3`), not Grok-5. 0416 goes to Grok-4. 0418 goes to Grok-5 when it can be packed.

t523u: Matthew approved a second work folder on prima/build for core builders. That is also the grant-ref for core paths. See `docs/plan/CORE-RUN.md` and `docs/review/DIRECTOR-WORDS-t523-core-run.md`.

t524u: the next builder is Grok-4 (`D:\Git\grok4`). 0418 is packed for Grok-4, not Grok-5. 0416 goes to Grok-5 after 0415 closes.

t526u-t528u: builders push reports to GitHub so Prima can read them (docs/plan/REPORTS.md). Lab 90.50.10.0705 (Claude, `D:\Git\claude`) designs the built-in wf report system. Do not pack the implementation until that lab closes. Prompt boxes stay for brief troubleshooting; the normal loop is packs > returns > review through GitHub, with wf controlling it.

t530u-t531u: setup reports chain on a worker page in band N6, one page per worker, title the worker's name lowercase (docs/review/DIRECTOR-WORDS-t530.md; pending rule in docs/review/PENDING-RULES.md). Every real wf check writes and pushes its report. The report-system build is one work-order page, 90.50.10.0422, titled report-system, at the next open unused 04NN, and it goes next in the queue once 0705 closes. 0420 stays dead-lock; 0421 stays wf seat.

This note is the queue. It does not pack any page.

## How many

The widest work wave has five pages at once. So we need **five builders** (Grok-1 through Grok-5) plus **Grok-Check**.

Folders on Matthew's PC, same setup as Grok-1:

- Grok-1: `D:\Git\grok1`
- Grok-2: `D:\Git\grok2`
- Grok-3: `D:\Git\grok3` (add)
- Grok-4: `D:\Git\grok4` (add)
- Grok-5: `D:\Git\grok5` (add)
- Grok-Check: `D:\Git\grokcheck` (add; no dash). This one never claims a build page. It only checks.

Each new terminal: set PATH to that folder's `wf-bin`, `WF_ROOT` to its `wf-run`, and `WF_AS` to that name. Use wf from `a823ee28`. A core page (0418 and later core work) uses a second work folder on `prima/build`, not `returns`. Setup is in `docs/plan/CORE-RUN.md`.

## How a builder picks up

One prompt per page. The first line is `Builder: <name>` (the machine and folder, for example `Builder: Grok-3 (Matthew's PC, D:\Git\grok3)`).

The builder: pulls packs and the work branch named in the pack (`returns` for wf pages, `prima/build` for core pages), claims that page only, follows `pages\<page>\05.NN\BUILDER-PROMPT.md`, returns with `--push`, then stops and tells Matthew.

It never claims a second page in the same wave. It never checks its own work.

`wf claim` does not check the builder name written in the pack (src/cmd.rs at a823ee28: first claim wins). So Grok-3 may claim the published 0419.05.01 pack, even though that pack's face 01 and overview still say Grok-5. Do not republish that pack to change the name. The prompt's first line is still `Builder: Grok-3 (Matthew's PC, D:\Git\grok3)`.

## How a page is checked

Grok-Check, and only Grok-Check, runs a real check:

```
wf check <page> <NN> --as Grok-Check
```

Not a dry-run. Then push the page log to the returns branch, the same way a close log is pushed. Prima reads the report and signs off. Until wf itself sends that report, also push a markdown file as docs/plan/REPORTS.md says.

If a pack uses `git grep`, the pattern must have **no caret, no quotes, and no spaces**. A safe form is in `docs/design/drafts/WF-WINDOWS-QUOTING.md` (prima/build). The form that works under Linux `sh -c` and stays safe on Windows `cmd /C` is `git grep -q -E [#][#][[:space:]]3[.] -- labs/0703/LAB-0703-SEQ-STORAGE.md`. A bare `##` pattern is a comment under `sh -c` (git exits 128, no pattern given), so packs must not use that.

## Waiting now (no new pack)

Grok-Check can start here today, after intake:

- 90.50.10.0404.05.02 (returned, Cursor-1)
- 90.50.10.0701.05.02 (returned, Grok-1)
- 90.50.10.0702.05.02 (returned, Claude)
- 90.50.10.0703.05.02 (returned, Codex)

Claude returned 90.50.10.0705.05.01. Next: Grok-Check runs `wf check 90.50.10.0705 1 --as Grok-Check` (not a dry-run), then Prima signs off and closes, then 05.02 can be packed (fold in t530u/t531u). 0422 report-system waits until 0705 closes.

Codex returned 90.50.10.0704.05.01. Intake is on packs. Do not check or close 0704 until Grok-Check runs `wf check 90.50.10.0704 1 --as Grok-Check`. Prima's response is `docs/review/DRIFT-0704-RESPONSE.md`.

90.50.10.0701.05.03 was also returned by Grok-1 (commit b71ab3e0, 10:41 AM EST), then a later 05.02 return (a3a0f83a, 10:49 AM EST) overwrote those two log events. Both returns and both tests are still in git. Packs still has the 22-entry prefix; do not publish-pack 0701 until the log is repaired (append the 05.03 claim and return after the current head, do not rewrite entries 23-24). See the drift response.

0415.05.01 already passed its check. Prima signs off and closes it, so 0416 can be packed.

## Inventory

Packable now means: pack text is ready, wf `a823ee28` can pack it (template 4 is known), and dependencies are met. The page still needs init, faces, draft and pack before a builder claims it. "New" pages have no pack text yet. 0418 and 0419 are assigned. 0420 (dead lock) and 0421 (wf seat) stay suggested. 0422 is the report-system work-order page (t530u, t531u): one page, title report-system, next in the queue once 0705 closes. Do not pack it until 0705 closes (t528u). 0423 is suggested for the 0701 log-overwrite fix: `push_log` must refuse a log that is not a prefix-extension of the published returns log (`docs/review/DRIFT-0704-RESPONSE.md`).

| Page | Goal | Grant | Depends on | Packable now |
|---|---|---|---|---|
| 0407 | Band door face 00 prints `type: band` and a contents list | `src/render.rs`, `tests/page_0407.rs` | 0403 closed. Packed on packs, start `a823ee28` | Y, packed |
| 0408 | Prime can withdraw a packed unclaimed pass | `src/cmd.rs`, `src/lib.rs`, `src/page.rs`, `tests/page_0408.rs` | 0403 closed. Packed on packs, start `a823ee28` | Y, packed |
| 0416 | The five Windows `tests/wf.rs` fails are fixed; Linux still proves the same thing. Also watch `draft_refuses_a_99th_pass` timing at `:965` (must stay under 10s) | `tests/wf.rs`, `tests/page_0416.rs` | 0701.05.01 closed. 0415.05.01 must be closed. Held pack on cloud/pack. Assigned to Grok-5 (t524u) | N until 0415 is closed |
| 0413 | A pass is one work order printed from the log; no pasted quote in the pack | `src/render.rs` | Wait until 0407's trial frees `src/render.rs`. Draft on cloud/design | Y, after init, but not before wave 2 |
| 0414 | New packs print the builder name; a name outside the six becomes a stable temp worker | `src/cmd.rs`, `src/render.rs`, `templates/v5/prompt.txt`, `templates/v5/builder.txt` | 0404.05.01 closed. Wait for `src/cmd.rs`. Draft on cloud/design | Y, after init, but not before its wave |
| 0417 | A pushed return updates `pages/<page>/05.NN` on packs, with no force push | `src/cmd.rs`, `src/git.rs` | 0413 closed. Wait for `src/cmd.rs` and for the quoting page if it holds `src/git.rs`. Draft on cloud/design | N until 0413 is closed |
| 0409 | Prime can retire a page | `src/cmd.rs`, `src/lib.rs`, `src/page.rs`, `tests/page_0409.rs` | 0408 closed. No pack text yet | N, needs a pack |
| 0406 | One command writes needs-links both ways | `src/cmd.rs`, `src/lib.rs`, `src/page.rs`, `src/render.rs`, `tests/page_0406.rs` | 0409 closed (holds those files). No pack text yet | N, needs a pack |
| 0411 | The real runner starts a page; Matthew grants it | `src/cmd.rs`, `src/lib.rs`, `tests/page_0411.rs` | 0406 closed. No pack text yet | N, needs a pack |
| 0412 | The real runner records Matthew's grant | `src/cmd.rs`, `src/lib.rs`, `tests/page_0412.rs` | 0411 closed. No pack text yet | N, needs a pack |
| 0498 | One working wf Matthew can install and run. This is the Stage 1 proof: a walkthrough on Matthew's PC that covers the full loop, including finding and understanding the saved record from a fresh session (0704 finding 4). | `README.md`, `docs/WALKTHROUGH.md`, `tests/page_0498.rs` | Every stage page above, including 0417 | N, last in dependency order, needs a pack. Priority: the stage is not done until this walkthrough is packed and run on Matthew's PC. |
| 0418 | Seated-05 in the compute core: a body on face 05 with no counter is the seat; 05.NN stays a pass; face 06 stays unseated | `crates/seqaddr-core/src/state.rs`, `resolve.rs`, `validate.rs`, `face.rs`, `tests/page_0418.rs` | t523 core run: start and return branch are `prima/build` `c1750c32`. Grant-ref t523. Assigned to Grok-4 (t524u). Packed on packs `98324515` | Y, packed |
| 0419 | Pack checks are safe on Windows (no caret, quotes or spaces in `git grep` patterns; harden `src/git.rs` if needed) | `src/git.rs`, `tests/page_0419.rs` | Packed on packs, start `a823ee28`. Assigned to Grok-3 (t522u). Must finish before 0417 takes `src/git.rs` | Y, packed |
| 0420 (suggest) | `wf verify --fix` takes over a dead `.wf-lock` (or a lock older than the last log entry) | `src/lib.rs` (lock at `Lock::acquire`), tests | After 0412 frees `src/lib.rs` | N, needs a pack |
| 0421 (suggest) | wf prints the seated 05 and updates face 01 | wf `src/` (likely `src/render.rs` and `src/cmd.rs`) | 0418 closed. Needs a later slot when those files are free | N, needs a pack and 0418 |
| 0422 (wait) | report-system: one work-order page that builds wf worker reports. Passes under this page carry the grants (0705.05.02 will name them). | wf `src/` as 0705.05.02 proposes (0408 holds `cmd.rs`, `lib.rs`, `page.rs`; 0407 holds `render.rs`; 0419 holds `git.rs`) | 0705 closed (t528u, t531u). Next in the queue after that. Do not pack until then | N, waits on 0705 |
| 0423 (suggest) | `push_log` / `wf return --push` refuses to publish a log that is not a prefix-extension of the log already on returns, so a later return on one counter cannot replace an earlier return on another (`docs/review/DRIFT-0704-RESPONSE.md`) | likely `src/cmd.rs`, tests | After 0408 frees `src/cmd.rs`. Suggested next open unused 04NN after 0422 | N, needs a pack |
| 0705 | Worker-report lab: design the system end to end, then fold t530u/t531u into 05.02 | `labs/0705/` | 05.01 packed and returned (Claude). 05.02 pack text is drafted; packing waits on a Grok-Check of 05.01, then signoff and close | 05.01 returned; 05.02 not packed |

Lab trials (`tests/lab_PPPP.rs` on 0701) run in the wave after each work wave. Each trial is its own new file, so they can run in parallel. 0410 stays unused (security is parked). 0405 stays parked; its job moved to 0416.

## Waves

Pages in the same wave change no shared file. A page holds its files until its trial passes.

**Wave 1** (t524u assignments). 0407, 0408 and 0419 are packed on the wf kit. 0418 is packed on the core run (`docs/plan/CORE-RUN.md`). 0416 still waits on 0415.

| Page | Goal | Builder | Packable now | Blocker |
|---|---|---|---|---|
| 0407 | Door prints type and contents | Grok-1 | Y, packed | none |
| 0408 | Withdraw an unclaimed pack | Grok-2 | Y, packed | none |
| 0419 | Windows-safe pack checks | Grok-3 | Y, packed | The published pack still says Grok-5. Grok-3 may claim it (see above). Do not republish the pack. |
| 0418 | Seated-05 in seqaddr-core | Grok-4 | Y, packed | Work clone is `prima/build` (t523). Setup in `docs/plan/CORE-RUN.md`. Pack hash `5f94dd5099e30e7363f9877baadab3e4fc1286be7788eeb7e247f90f46172163`. |
| 0416 | Windows `tests/wf.rs` five fails | Grok-5 | N | Close 0415, then init and pack |

**Wave 2** (t528u, t531u). Lab 90.50.10.0705 (Claude) is first. After it closes, the next work order is 90.50.10.0422, title report-system: one page, its passes carry the build (t530u, t531u). 0420 and 0421 stay reserved for dead lock and the wf seat. Wave 1 trials can run in parallel; they do not touch `labs/0705/`. Grok-Check checks 0705.05.01 (returned) before 05.02 is packed.

| Page | Goal | Builder | Packable now | Blocker |
|---|---|---|---|---|
| 0705.05.01 | Design wf worker reports | Claude | returned | Grok-Check, then signoff and close |
| 0705.05.02 | Fold in t530u/t531u | Claude | pack text drafted | 05.01 closed |
| 0422 | report-system work order | (after 0705) | N | 0705 closed; then next in the queue |

Then the wave 1 trials, same builders as before (Grok-1 on 0407, Grok-2 on 0408, Grok-3 on 0419, Grok-4 on 0418, Grok-5 on 0416), each on a different `tests/lab_*.rs` or core trial. The 0418 trial is a core trial; the 0416 trial is on the wf kit.

**Wave 3**

| Page | Goal | Builder | Packable now | Blocker |
|---|---|---|---|---|
| 0409 | Retire a page | Grok-1 | N | 0408 closed; pack text |
| 0413 | Work order view | Grok-2 | Y, after init | 0407 trial done (frees `src/render.rs`) |

**Wave 4** — trials 0409 and 0413.

**Wave 5** — 0406 (Grok-1). Holds cmd, lib, page and render. No partner in this wave.

**Wave 6** — trial 0406.

**Wave 7** — 0411 (Grok-1).

**Wave 8** — trial 0411.

**Wave 9** — 0412 (Grok-1).

**Wave 10** — trial 0412.

**Wave 11**

| Page | Goal | Builder | Packable now | Blocker |
|---|---|---|---|---|
| 0414 | Builder name and temp workers | Grok-1 | Y, after init | 0412 trial done; 0404.05.01 closed |
| 0420 | Dead `.wf-lock` and `--fix` | Grok-2 | N | 0412 trial done (frees `src/lib.rs`); pack text |

**Wave 12** — trials 0414 and 0420.

**Wave 13** — 0417 (Grok-1). Needs 0413 closed and 0419's trial done if 0419 holds `src/git.rs`.

**Wave 14** — trial 0417.

**Wave 15** — 0421, wf seat (Grok-1), after 0418 is closed and when `src/cmd.rs` and `src/render.rs` are free.

**Wave 16** — 0498 (Grok-1), last in dependency order, but the Stage 1 proof: the walkthrough on Matthew's PC must cover the full loop, including finding and understanding the saved record from a fresh session (0704 finding 4). Then its trial.

Waves 5-10 are a single-file queue on `src/cmd.rs`. Only one builder is busy there. The others can take 0701 trials, pack prep, or later-wave drafts, but they must not touch a file a live wave still holds.

## What Prima does before wave 1

1. Sign off and close 0415.05.01, then pack 0416 for Grok-5.
2. Add Grok-3, Grok-4, Grok-5 and Grok-Check folders, each with wf `a823ee28`. Grok-4's work folder for 0418 is on `prima/build` (`docs/plan/CORE-RUN.md`).
3. 0407, 0408 and 0419 are already packed and published on the wf kit.
4. 0418 is packed for Grok-4 on the core run (t523, t524u).
5. Hand each builder one prompt, first line `Builder: <name>`. For 0419 that line is `Builder: Grok-3 (Matthew's PC, D:\Git\grok3)`, even though the published pack text still says Grok-5. For 0418 that line is `Builder: Grok-4 (Matthew's PC, D:\Git\grok4)`.
6. Pack 0705 for Claude (t528u). 05.01 is returned. Grok-Check is not yet available for the check. Until 0705 closes, do not pack 0422 report-system (t531u). Until wf sends reports, builders use docs/plan/REPORTS.md.
