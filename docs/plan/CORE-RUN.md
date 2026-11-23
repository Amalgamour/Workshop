# Core run

t523u: core builders get a second work folder on prima/build.

The wf kit lives on `returns`. The core crates live on `prima/build`. Those two branches do not share a history, so a core pack must not start on `returns`.

## What goes where

- Pack files (the page, the prompt, `PACK.md`) still go to the `packs` branch, as usual. Prima publishes them with `wf publish-pack`.
- The builder's code, and the page log wf writes on return, go to `prima/build`. The pack uses `repo: work` (that folder is a prima/build clone) and `wf pack --branch prima/build`.

Intake for a core page: `wf intake --repo work --branch prima/build`.

## Prima's publish must not collide with a return

Prima still publishes docs the usual way: the `publish` folder fetches from `../repo` branch `build`, cherry-picks, and pushes to `prima/build`. Never force push. Never merge to main.

A core builder's `return --push` also merges onto `prima/build`. If that return lands first, pull it before Prima publishes the next docs.

1. Fetch `origin prima/build`.
2. Fast-forward the `publish` folder to that tip.
3. Bring the local `repo` branch `build` up to date with that same tree (fast-forward if you can; otherwise rebase any unpublished Prima commits on top of it).
4. Only then add new docs and publish, as usual.

## Builder setup (Grok-4, page 0418)

Folder: `D:\Git\grok4`. Use wf from commit `a823ee28`, same as the other Grok builders.

1. Put `wf.exe` in `D:\Git\grok4\wf-bin` (built from `a823ee28`).
2. Make a run folder `D:\Git\grok4\wf-run`:
   - Clone this repo and check out the `packs` branch. That folder is `WF_ROOT`. It holds `pages\`.
   - Clone this repo again into `D:\Git\grok4\wf-run\work` and check out the `prima/build` branch.
3. In that terminal, set:
   - `PATH` so it finds `D:\Git\grok4\wf-bin`
   - `WF_ROOT=D:\Git\grok4\wf-run`
   - `WF_AS=Grok-4`
4. Fetch before you claim: in `WF_ROOT`, `git pull` the `packs` branch. In `work`, `git checkout prima/build` and `git pull`.
5. Prima starts the page and packs it. The builder does not run `wf init-page` or `wf intake`.
6. Claim: `wf claim 90.50.10.0418 01 --as Grok-4`
7. Do the work in `work\` on `prima/build`, from the pack's start commit. Stay inside the grant.
8. Return: `wf return 90.50.10.0418 01 --branch prima/build --commit <SHA> --file .workshop/returns/90.50.10.0418.05.01.md --push`

The first line of the prompt is `Builder: Grok-4 (Matthew's PC, D:\Git\grok4)`.

Grok-Check still runs `wf check --as Grok-Check`, from a run folder whose `work` is also on `prima/build`, then Prima signs off.
