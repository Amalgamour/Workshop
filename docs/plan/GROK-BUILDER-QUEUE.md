# Grok builder queue

t517u (23 Nov 2026): Grok builders are cheapest and best. They should do a lot of the work, especially the core's local infrastructure. The problem is how to get work to many of them at once.

t518u-t519u: add as many Grok builders as the waves need. A dedicated checker named Grok-Check does the checks.

This note is the queue. It does not pack any page.

## How many

The widest work wave has five pages at once. So we need **five builders** (Grok-1 through Grok-5) plus **Grok-Check**.

Folders on Matthew's PC, same setup as Grok-1:

- Grok-1: `D:\Git\grok1`
- Grok-2: `D:\Git\grok2`
- Grok-3: `D:\Git\grok3` (add)
- Grok-4: `D:\Git\grok4` (add)
- Grok-5: `D:\Git\grok5` (add)
- Grok-Check: `D:\Git\grok-check` (add). This one never claims a build page. It only checks.

Each new terminal: set PATH to that folder's `wf-bin`, `WF_ROOT` to its `wf-run`, and `WF_AS` to that name. Use wf from `a823ee28`.

## How a builder picks up

One prompt per page. The first line is `Builder: <name>` (the machine and folder, for example `Builder: Grok-3 (Matthew's PC, D:\Git\grok3)`).

The builder: pulls packs and returns, claims that page only, follows `pages\<page>\05.NN\BUILDER-PROMPT.md`, returns with `--push`, then stops and tells Matthew.

It never claims a second page in the same wave. It never checks its own work.

## How a page is checked

Grok-Check, and only Grok-Check, runs a real check:

```
wf check <page> <NN> --as Grok-Check
```

Not a dry-run. Then push the page log to the returns branch, the same way a close log is pushed. Prima reads the report and signs off.

If a pack uses `git grep`, the pattern must have **no caret, no quotes, and no spaces**. A safe form is in `docs/design/drafts/WF-WINDOWS-QUOTING.md` (prima/build). Example: `git grep -q -E ##[[:space:]]3[.] -- labs/0703/LAB-0703-SEQ-STORAGE.md`.

## Waiting now (no new pack)

Grok-Check can start here today, after intake:

- 90.50.10.0404.05.02 (returned, Cursor-1)
- 90.50.10.0701.05.02 (returned, Grok-1)
- 90.50.10.0702.05.02 (returned, Claude)
- 90.50.10.0703.05.02 (returned, Codex)

0415.05.01 already passed its check. Prima signs off and closes it, so 0416 can be packed.

## Inventory

Packable now means: pack text is ready, wf `a823ee28` can pack it (template 4 is known), and dependencies are met. The page still needs init, faces, draft and pack before a builder claims it. "New" pages have no pack text yet. Suggested numbers 0418-0421 are free slots; Prima sets the address at pack time.

| Page | Goal | Grant | Depends on | Packable now |
|---|---|---|---|---|
| 0407 | Band door face 00 prints `type: band` and a contents list | `src/render.rs`, `tests/page_0407.rs` | 0403 closed. Held pack on cloud/pack, start `a823ee28` | Y, after init |
| 0408 | Prime can withdraw a packed unclaimed pass | `src/cmd.rs`, `src/lib.rs`, `src/page.rs`, `tests/page_0408.rs` | 0403 closed. Held pack on cloud/pack, start `a823ee28` | Y, after init |
| 0416 | The five Windows `tests/wf.rs` fails are fixed; Linux still proves the same thing. Also watch `draft_refuses_a_99th_pass` timing at `:965` (must stay under 10s) | `tests/wf.rs`, `tests/page_0416.rs` | 0701.05.01 closed. 0415.05.01 must be closed. Held pack on cloud/pack | N until 0415 is closed |
| 0413 | A pass is one work order printed from the log; no pasted quote in the pack | `src/render.rs` | Wait until 0407's trial frees `src/render.rs`. Draft on cloud/design | Y, after init, but not before wave 2 |
| 0414 | New packs print the builder name; a name outside the six becomes a stable temp worker | `src/cmd.rs`, `src/render.rs`, `templates/v5/prompt.txt`, `templates/v5/builder.txt` | 0404.05.01 closed. Wait for `src/cmd.rs`. Draft on cloud/design | Y, after init, but not before its wave |
| 0417 | A pushed return updates `pages/<page>/05.NN` on packs, with no force push | `src/cmd.rs`, `src/git.rs` | 0413 closed. Wait for `src/cmd.rs` and for the quoting page if it holds `src/git.rs`. Draft on cloud/design | N until 0413 is closed |
| 0409 | Prime can retire a page | `src/cmd.rs`, `src/lib.rs`, `src/page.rs`, `tests/page_0409.rs` | 0408 closed. No pack text yet | N, needs a pack |
| 0406 | One command writes needs-links both ways | `src/cmd.rs`, `src/lib.rs`, `src/page.rs`, `src/render.rs`, `tests/page_0406.rs` | 0409 closed (holds those files). No pack text yet | N, needs a pack |
| 0411 | The real runner starts a page; Matthew grants it | `src/cmd.rs`, `src/lib.rs`, `tests/page_0411.rs` | 0406 closed. No pack text yet | N, needs a pack |
| 0412 | The real runner records Matthew's grant | `src/cmd.rs`, `src/lib.rs`, `tests/page_0412.rs` | 0411 closed. No pack text yet | N, needs a pack |
| 0498 | One working wf Matthew can install and run | `README.md`, `docs/WALKTHROUGH.md`, `tests/page_0498.rs` | Every stage page above, including 0417 | N, last, needs a pack |
| 0418 (suggest) | Seated-05 in the compute core: a body on face 05 with no counter is the seat; 05.NN stays a pass; face 06 stays unseated | `crates/seqaddr-core/src/state.rs`, `resolve.rs`, `validate.rs`, `face.rs` (lines may have moved; proposal `e46126ec`) | t512 rule is on prima/build. Start is prima/build, not returns `a823ee28` | N, needs a pack |
| 0419 (suggest) | Pack checks are safe on Windows (no caret, quotes or spaces in `git grep` patterns; harden `src/git.rs` if needed) | `src/git.rs`, `tests/page_0419.rs` (if the fix is in wf) | `docs/design/drafts/WF-WINDOWS-QUOTING.md`. Must finish before 0417 takes `src/git.rs` | N, needs a pack |
| 0420 (suggest) | `wf verify --fix` takes over a dead `.wf-lock` (or a lock older than the last log entry) | `src/lib.rs` (lock at `Lock::acquire`), tests | After 0412 frees `src/lib.rs` | N, needs a pack |
| 0421 (suggest) | wf prints the seated 05 and updates face 01 | wf `src/` (likely `src/render.rs` and `src/cmd.rs`) | 0418 closed. Needs a later slot when those files are free | N, needs a pack and 0418 |

Lab trials (`tests/lab_PPPP.rs` on 0701) run in the wave after each work wave. Each trial is its own new file, so they can run in parallel. 0410 stays unused (security is parked). 0405 stays parked; its job moved to 0416.

## Waves

Pages in the same wave change no shared file. A page holds its files until its trial passes.

**Wave 1** (five builders, once 0415 is closed and the new packs exist):

| Page | Goal | Builder | Packable now | Blocker |
|---|---|---|---|---|
| 0407 | Door prints type and contents | Grok-1 | Y, after init | Prima inits and packs |
| 0408 | Withdraw an unclaimed pack | Grok-2 | Y, after init | Prima inits and packs |
| 0416 | Windows `tests/wf.rs` five fails | Grok-3 | N | Close 0415, then init and pack |
| 0418 | Seated-05 in seqaddr-core | Grok-4 | N | Write the pack (start prima/build) |
| 0419 | Windows-safe pack checks | Grok-5 | N | Write the pack |

**Wave 2** — trials 0407, 0408, 0416, 0418, 0419 (Grok-1 through Grok-5, each on a different `tests/lab_*.rs` or core trial). Grok-Check checks the wave 1 returns first.

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

**Wave 16** — 0498 (Grok-1), last. Then its trial.

Waves 5-10 are a single-file queue on `src/cmd.rs`. Only one builder is busy there. The others can take 0701 trials, pack prep, or later-wave drafts, but they must not touch a file a live wave still holds.

## What Prima does before wave 1

1. Sign off and close 0415.05.01.
2. Add Grok-3, Grok-4, Grok-5 and Grok-Check folders, each with wf `a823ee28`.
3. Init and pack 0407 and 0408 (held texts on cloud/pack). Then 0416 once 0415 is closed.
4. Write packs for 0418 and 0419 so wave 1 can fill all five seats. Until those packs exist, run wave 1 with the pages that are ready (two or three builders, not five).
5. Hand each builder one prompt, first line `Builder: <name>`.
