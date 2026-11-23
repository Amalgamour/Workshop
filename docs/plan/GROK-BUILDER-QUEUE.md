# Grok builder queue

t517u (23 Nov 2026): Grok builders are cheapest and best. They should do a lot of the work, especially the core's local infrastructure. The problem is how to get work to many of them at once.

t518u-t519u: add as many Grok builders as the waves need. A dedicated checker named Grok-Check does the checks.

t522u: 0419.05.01 goes to Grok-3 (`D:\Git\grok3`), not Grok-5. 0416 goes to Grok-4. 0418 goes to Grok-5 when it can be packed.

t523u: Matthew approved a second work folder on prima/build for core builders. That is also the grant-ref for core paths. See `docs/plan/CORE-RUN.md` and `docs/review/DIRECTOR-WORDS-t523-core-run.md`.

t524u: the next builder is Grok-4 (`D:\Git\grok4`). 0418 is packed for Grok-4, not Grok-5. 0416 goes to Grok-5 after 0415 closes.

t526u-t528u: builders push reports to GitHub so Prima can read them (docs/plan/REPORTS.md). Lab 90.50.10.0705 (Claude, `D:\Git\claude`) designs the built-in wf report system. Do not pack the implementation until that lab closes. Prompt boxes stay for brief troubleshooting; the normal loop is packs > returns > review through GitHub, with wf controlling it.

t530u-t531u: setup reports chain on a worker page in band N6, one page per worker, title the worker's name lowercase (docs/review/DIRECTOR-WORDS-t530.md; pending rule in docs/review/PENDING-RULES.md). Every real wf check writes and pushes its report. The report-system build is one page, 90.50.10.0422, titled report-system, at the next open unused 04NN; its 05 passes are the work orders (t541u). 0420 stays dead-lock; 0421 stays wf seat. 0422 still waits until 0705 closes, but it is no longer first after that (see t533u).

t533u: one worker per page at a time; many pages may run in parallel (docs/review/DIRECTOR-WORDS-t533.md; pending rule in docs/review/PENDING-RULES.md). Page 90.50.10.0423, title one-worker, enforces that in wf (claim refuses while any pass is claimed and not returned; check refuses while a claim is open) and makes `push_log` refuse unless the published log is a prefix of the local log. Grant is `src/cmd.rs`, `src/page.rs`, `tests/page_0423.rs`. It waits on 0408 close, then goes first in the queue, ahead of 0422. Pack text is drafted in docs/design/drafts/90.50.10.0423/. The 0701 repair plan is docs/review/0701-LOG-REPAIR.md (not done yet).

t541u: Matthew answered the MVP gaps (docs/review/DIRECTOR-WORDS-t541-mvp-gaps.md; docs/plan/MVP-GOAL-PROPOSAL.md). 0498 is the MVP target. The compute is wf plus one `seqaddr validate` step, recorded in the 0498 walkthrough, not a new wf page unless a later design says otherwise. A worker holds a page only while actively working on face 01, 04 or 05, and that face is locked; one model at a time; between steps the page is not held. The 0423 draft uses a session-long face lockout (LOTO): lockout, try-out, and release, with a recorded override for an abandoned lock. It is still not packed, and still waits on 0408. The grant grows to include `src/lib.rs` because those are new commands. A work order is a 05 pass, not the whole page; 0422 is the report-system page, and its 05 passes are the work orders. A small second-field trial comes after 0498, on its own later 04NN page once Matthew picks the field. The current report file is enough for the MVP, so 0422 is not a blocker for 0498. Pending, not packed: page 90.50.10.0424, title book-board, adds holder, step and next to each `wf board` book-board line (needed before the 0498 run). The GUI Workshop manager is the long-term direction, not MVP scope.

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

## Planning rule (t533u, t541u)

Never pack two open passes of one page for different workers. Many pages may run in parallel. A page gets at most one worker at a time. A worker holds the page only while actively working on a face (01, 04 or 05). The face is locked out for the whole work session, and released when the worker is done. Between sessions the page is not held. Do not pack, draft, or face-write a page while a lockout is held on it. Packing may stage a later pass only when no lockout is held. wf will enforce the lockout on page 90.50.10.0423; this queue rule is for Prima when packing.

## How a page is checked

Grok-Check, and only Grok-Check, runs a real check:

```
wf check <page> <NN> --as Grok-Check
```

Not a dry-run. Then push the page log to the returns branch, the same way a close log is pushed. Prima reads the report and signs off. Until wf itself sends that report, also push a markdown file as docs/plan/REPORTS.md says.

If a pack uses `git grep`, the pattern must have **no caret, no quotes, and no spaces**. A safe form is in `docs/design/drafts/WF-WINDOWS-QUOTING.md` (prima/build). The form that works under Linux `sh -c` and stays safe on Windows `cmd /C` is `git grep -q -E [#][#][[:space:]]3[.] -- labs/0703/LAB-0703-SEQ-STORAGE.md`. A bare `##` pattern is a comment under `sh -c` (git exits 128, no pattern given), so packs must not use that.

## Waiting now (no new pack)

Grok-Check's 0419.05.01, 0404.05.02 and 0702.05.03 checks landed, and Prima signed off and closed them. Details are in `docs/review/CLOSE-0419-0404-0702.md`.

- 90.50.10.0419.05.01 closed failed (lab trial not in the return; jobs w01 and w02 accepted). A later pass can add the trial.
- 90.50.10.0404.05.02 closed failed (packed `cargo test --test wf` auto-failed on Windows; jobs accepted). A Linux re-check is still needed.
- 90.50.10.0702.05.03 closed passed (no majors; three minors on line numbers and a short path).
- 90.50.10.0703.05.02 (returned, Codex) is still waiting on Grok-Check.

Claude's 90.50.10.0705.05.01 is closed passed (Grok-Check entry 9, Prima signoff and close). 05.02 is packed for Claude (start 32fc1f34e8efdb9dd609ed4679bdbc90a74e7998, pack hash 3340b0e5576e6fa5c658cef5f80464628d1fbc6f852835c36247101927b16b8c). Next: Claude claims `wf claim 90.50.10.0705 2`. 0422 report-system still waits until 0705 closes, and after 0423 if they share src/cmd.rs.

Codex's 90.50.10.0704.05.01 is closed passed (Grok-Check entry 9, Prima signoff and close). Do not pack 05.02; Matthew steers that lab directly. A lesson on the stage-plan path is in `docs/lessons/2026-11-23-stage-plan-path.md`. Prima's earlier response remains `docs/review/DRIFT-0704-RESPONSE.md`.

90.50.10.0701.05.02 shows as returned on the current tip, but do not check it until the 05.03 log is repaired (the live suffix is the displaced 05.02 events). 90.50.10.0701.05.03 was also returned by Grok-1 (commit b71ab3e0, 10:41 AM EST), then a later 05.02 return (a3a0f83a, 10:49 AM EST) overwrote those two log events. Both returns and both tests are still in git. Packs still has the 22-entry prefix; do not publish-pack 0701 until the log is repaired (append the 05.03 claim and return after the current head, do not rewrite entries 23-24). The steps are in `docs/review/0701-LOG-REPAIR.md`. Prefer to repair after 0423 lands. See also the drift response.

0415.05.01 already passed its check. Prima signs off and closes it, so 0416 can be packed.

## Inventory

Packable now means: pack text is ready, wf `a823ee28` can pack it (template 4 is known), and dependencies are met. The page still needs init, faces, draft and pack before a builder claims it. "New" pages have no pack text yet. 0418 and 0419 are assigned. 0420 (dead lock) and 0421 (wf seat) stay suggested. 0423 (t533u, t541u, title one-worker) is the safety page: one worker per page, a session-long face lockout on 01, 04 or 05 (lockout, try-out, release, and a recorded override), and the `push_log` prefix check. Grant is `src/cmd.rs`, `src/page.rs`, `src/lib.rs`, `tests/page_0423.rs` (lib.rs grows in because the new commands live there). Pack text is drafted. It waits on 0408 close, then goes first in the queue, ahead of 0422, 0409 and later `cmd.rs` or `lib.rs` pages. 0422 is the report-system page (t530u, t531u, t541u): one page, title report-system; its 05 passes are the work orders. Do not pack 0422 until 0705 closes (t528u), and not before 0423 if they would share `src/cmd.rs`. 0424 (book-board) is pending, not packed: holder, step and next on each book-board line, needed before 0498. 0498 is the MVP target and includes one `seqaddr validate` step.

| Page | Goal | Grant | Depends on | Packable now |
|---|---|---|---|---|
| 0407 | Band door face 00 prints `type: band` and a contents list | `src/render.rs`, `tests/page_0407.rs` | 0403 closed. Packed on packs, start `a823ee28` | Y, packed |
| 0408 | Prime can withdraw a packed unclaimed pass | `src/cmd.rs`, `src/lib.rs`, `src/page.rs`, `tests/page_0408.rs` | 0403 closed. Packed on packs, start `a823ee28` | Y, packed |
| 0416 | The five Windows `tests/wf.rs` fails are fixed; Linux still proves the same thing. Also watch `draft_refuses_a_99th_pass` timing at `:965` (must stay under 10s) | `tests/wf.rs`, `tests/page_0416.rs` | 0701.05.01 closed. 0415.05.01 must be closed. Held pack on cloud/pack. Assigned to Grok-5 (t524u) | N until 0415 is closed |
| 0413 | A pass is one work order printed from the log; no pasted quote in the pack | `src/render.rs` | Wait until 0407's trial frees `src/render.rs`. Draft on cloud/design | Y, after init, but not before wave 2 |
| 0414 | New packs print the builder name; a name outside the six becomes a stable temp worker | `src/cmd.rs`, `src/render.rs`, `templates/v5/prompt.txt`, `templates/v5/builder.txt` | 0404.05.01 closed. Wait for `src/cmd.rs`. Draft on cloud/design | Y, after init, but not before its wave |
| 0417 | A pushed return updates `pages/<page>/05.NN` on packs, with no force push | `src/cmd.rs`, `src/git.rs` | 0413 closed. Wait for `src/cmd.rs` and for the quoting page if it holds `src/git.rs`. Draft on cloud/design | N until 0413 is closed |
| 0409 | Prime can retire a page | `src/cmd.rs`, `src/lib.rs`, `src/page.rs`, `tests/page_0409.rs` | 0408 closed, and 0423 closed (0423 takes `cmd.rs`, `lib.rs` and `page.rs` first). No pack text yet | N, needs a pack |
| 0406 | One command writes needs-links both ways | `src/cmd.rs`, `src/lib.rs`, `src/page.rs`, `src/render.rs`, `tests/page_0406.rs` | 0409 closed (holds those files). No pack text yet | N, needs a pack |
| 0411 | The real runner starts a page; Matthew grants it | `src/cmd.rs`, `src/lib.rs`, `tests/page_0411.rs` | 0406 closed. No pack text yet | N, needs a pack |
| 0412 | The real runner records Matthew's grant | `src/cmd.rs`, `src/lib.rs`, `tests/page_0412.rs` | 0411 closed. No pack text yet | N, needs a pack |
| 0498 | MVP target (t541u G2): one working wf Matthew can install and run. The walkthrough on Matthew's PC covers the full loop in docs/plan/MVP-GOAL-PROPOSAL.md section 4, including one `seqaddr validate` step whose result is recorded (G1), finding and understanding the saved record from a fresh session, and `wf board` showing holder, step and next. | `README.md`, `docs/WALKTHROUGH.md`, `tests/page_0498.rs` | Every stage page above, including 0417, 0423, and 0424 (book-board). 0422 is not a blocker (G8). The small second-field trial is a later 04NN page after this run (G4). | N, last in dependency order, needs a pack. Priority: the stage is not done until this walkthrough is packed and run on Matthew's PC. |
| 0418 | Seated-05 in the compute core: a body on face 05 with no counter is the seat; 05.NN stays a pass; face 06 stays unseated | `crates/seqaddr-core/src/state.rs`, `resolve.rs`, `validate.rs`, `face.rs`, `tests/page_0418.rs` | t523 core run: start and return branch are `prima/build` `c1750c32`. Grant-ref t523. Assigned to Grok-4 (t524u). Packed on packs `98324515` | Y, packed |
| 0419 | Pack checks are safe on Windows (no caret, quotes or spaces in `git grep` patterns; harden `src/git.rs` if needed) | `src/git.rs`, `tests/page_0419.rs` | Packed on packs, start `a823ee28`. Assigned to Grok-3 (t522u). Must finish before 0417 takes `src/git.rs` | Y, packed |
| 0420 (suggest) | `wf verify --fix` takes over a dead `.wf-lock` (or a lock older than the last log entry) | `src/lib.rs` (lock at `Lock::acquire`), tests | After 0412 frees `src/lib.rs` | N, needs a pack |
| 0421 (suggest) | wf prints the seated 05 and updates face 01 | wf `src/` (likely `src/render.rs` and `src/cmd.rs`) | 0418 closed. Needs a later slot when those files are free | N, needs a pack and 0418 |
| 0422 (wait) | report-system: one page that builds wf worker reports. Its 05 passes are the work orders and carry the grants (0705.05.02 will name them). Not an MVP blocker (t541u G8). | wf `src/` as 0705.05.02 proposes (0408 holds `cmd.rs`, `lib.rs`, `page.rs`; 0407 holds `render.rs`; 0419 holds `git.rs`) | 0705 closed (t528u, t531u). After 0423 if they would share `src/cmd.rs`. Do not pack until then | N, waits on 0705 and 0423 |
| 0423 (wait) | one-worker: session-long face lockout on 01, 04 or 05 (lockout, try-out, release; abandoned-lock override by the current Prime or a higher authority); while a lockout is held every other worker is refused; a claimed, unreturned pass still blocks any other claim; `push_log` / `wf return --push` refuses unless the published log is a prefix of the local log (t533u, t541u, `docs/review/DRIFT-0704-RESPONSE.md`). Draft updated; not packed. | `src/cmd.rs`, `src/page.rs`, `src/lib.rs`, `tests/page_0423.rs` | 0408 closed (it holds `cmd.rs`, `lib.rs` and `page.rs`), including the 0408 trial if that trial still holds the files. Pack text drafted in `docs/design/drafts/90.50.10.0423/`. First in the queue after 0408, ahead of 0422 | N, waits on 0408 |
| 0424 (wait) | book-board: each `wf board` book-board line shows the page's holder, step and next (t541u G5). Needed before the 0498 MVP run. | likely `src/board.rs` and a test file; grant confirmed at pack. Help text may also need `src/lib.rs` | Needed before 0498. Does not wait on 0423 (different files). Not packed. WF-BOARD Q1 (column names) is still open. | N, not packed |
| 0705 | Worker-report lab: design the system end to end, then fold t530u/t531u into 05.02 | `labs/0705/` | 05.01 closed passed. 05.02 packed for Claude on packs `d16cf4ae`, start `32fc1f34e8efdb9dd609ed4679bdbc90a74e7998`, pack hash `3340b0e5576e6fa5c658cef5f80464628d1fbc6f852835c36247101927b16b8c` | 05.02 packed, not claimed |

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

**Wave 2** (t528u, t531u, t533u). Lab 90.50.10.0705 (Claude) is first among the report-system design work. 90.50.10.0423, title one-worker, is the safety page and goes first after 0408 closes, ahead of 0422, even if 0705 has already closed. After 0423, the report-system page is 90.50.10.0422 (t530u, t531u, t541u), still not packed until 0705 closes. 0424 (book-board) is pending and not in this wave. 0420 and 0421 stay reserved for dead lock and the wf seat. Wave 1 trials can run in parallel; they do not touch `labs/0705/`. Grok-Check checks 0705.05.01 (returned) before 05.02 is packed.

| Page | Goal | Builder | Packable now | Blocker |
|---|---|---|---|---|
| 0705.05.01 | Design wf worker reports | Claude | closed passed | done |
| 0705.05.02 | Fold in t530u/t531u and Grok-Check minors | Claude | Y, packed | Claude claims it |
| 0423 | one-worker (session lockout on 01, 04 or 05, and push_log prefix) | (after 0408) | N | 0408 closed; then first in the queue, ahead of 0422. Grant includes `src/lib.rs`. Draft updated; not packed. |
| 0422 | report-system page (05 passes are the work orders) | (after 0705 and 0423) | N | 0705 closed; 0423 first if they share src/cmd.rs. Not an MVP blocker. |

Then the wave 1 trials, same builders as before (Grok-1 on 0407, Grok-2 on 0408, Grok-3 on 0419, Grok-4 on 0418, Grok-5 on 0416), each on a different `tests/lab_*.rs` or core trial. The 0418 trial is a core trial; the 0416 trial is on the wf kit.

**Wave 3** — 0423 first if 0408 is already closed when this wave starts (safety, holds `src/cmd.rs` and `src/page.rs`). 0409 waits until 0423 has freed `src/cmd.rs`.

| Page | Goal | Builder | Packable now | Blocker |
|---|---|---|---|---|
| 0423 | one-worker | (after 0408) | N | 0408 closed; pack text drafted |
| 0409 | Retire a page | Grok-1 | N | 0423 closed (and 0408 closed); pack text |
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

**Wave 16** — 0498 (Grok-1), the MVP target (t541u G2), last in dependency order. The walkthrough on Matthew's PC must cover the full loop in docs/plan/MVP-GOAL-PROPOSAL.md section 4, including one `seqaddr validate` step whose result is recorded, `wf board` showing holder, step and next (so 0424 must already be closed), and finding and understanding the saved record from a fresh session. Then its trial. A small second-field trial follows on a later 04NN page (G4).

Waves 5-10 are a single-file queue on `src/cmd.rs`. Only one builder is busy there. The others can take 0701 trials, pack prep, or later-wave drafts, but they must not touch a file a live wave still holds.

## What Prima does before wave 1

1. Sign off and close 0415.05.01, then pack 0416 for Grok-5.
2. Add Grok-3, Grok-4, Grok-5 and Grok-Check folders, each with wf `a823ee28`. Grok-4's work folder for 0418 is on `prima/build` (`docs/plan/CORE-RUN.md`).
3. 0407, 0408 and 0419 are already packed and published on the wf kit.
4. 0418 is packed for Grok-4 on the core run (t523, t524u).
5. Hand each builder one prompt, first line `Builder: <name>`. For 0419 that line is `Builder: Grok-3 (Matthew's PC, D:\Git\grok3)`, even though the published pack text still says Grok-5. For 0418 that line is `Builder: Grok-4 (Matthew's PC, D:\Git\grok4)`.
6. Pack 0705 for Claude (t528u). 05.01 is closed passed. 05.02 is packed. Until 0705 closes, do not pack 0422 report-system (t531u). 0423 goes first after 0408, ahead of 0422 (t533u, t541u). Its grant includes `src/lib.rs`. Do not pack 0423 or 0424 in this turn. 0424 (book-board) is pending and needed before 0498. Until wf sends reports, builders use docs/plan/REPORTS.md (enough for the MVP, t541u G8).
