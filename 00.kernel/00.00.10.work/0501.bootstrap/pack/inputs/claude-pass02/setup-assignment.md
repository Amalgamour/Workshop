# Draft assignment: set up D:\Git\lib-build

**state:** draft, for the Director's review. Not released. Nothing has been run.
**who drafted:** claude-opus-5-5 (Colab), 2026-10-26
**seat:** Prime (Codex), or a Builder at the Director's word
**branch:** `workshop`, in a separate repository at `D:\Git\lib-build` whose remote is `Amalgamour/Librarian`
**waits on:** `preservation-assignment.md`, finished and its return read. Decisions D1–D4 and D7 (`proposal.md`, section 7).

## What this does, and what it doesn't

It makes `D:\Git\lib-build` a repository with the Librarian history, without disturbing the lab already there. It clears the inherited tree from branch `workshop`, commits the lab unchanged, imports the minimum manifest from git objects, and writes the new drafts and the entry.

It doesn't:
- seat, approve, lock or promote anything;
- adapt tool code, beyond the stamp lines named in S6;
- run pending packs;
- touch either old checkout;
- merge anything.

## Why not a worktree or a clone

- `git worktree add` and `git clone` both need an empty or missing destination, and `D:\Git\lib-build` holds `labs\`.
- A worktree would also register inside `D:\Git\Librarian\.git`, which would change an old workspace.

So the repository is made in place, and its history comes from GitHub.

## Steps

Commands are given for any shell. `LB` stands for `D:\Git\Librarian`, `RB` for `D:\Git\Librarian-rebuild`, and `W` for `D:\Git\lib-build`.

**S0. Baseline (A1, A2)**

```text
git -C LB status --porcelain -uall > %TEMP%\lb-before.txt     (and stash list, worktree list, for-each-ref)
git -C RB status --porcelain -uall > %TEMP%\rb-before.txt     (the same three extra lists)
```

Then record the lab: the sha256 of every file under `W\labs\clerk-handoff-pass01` must equal the 36 `worktree-inventory.tsv` rows for workspace `lib-build`.

**S1. A repository in place, with nothing written to the working folder**

```text
git -C W init --initial-branch=workshop
git -C W remote add origin https://github.com/Amalgamour/Librarian.git
git -C W fetch origin "+refs/heads/*:refs/remotes/origin/*" --tags
git -C W update-ref refs/heads/workshop 14676ca3c01833cc1b472198e62e3451ef706ec3
git -C W read-tree --empty
git -C W status --short | more        # expect: the inherited files listed as staged deletions, and ?? labs/
```

The working folder still holds only `labs\`. Check A1.

**S2. Clear the floor**

```text
git -C W commit -m "workshop: clear the floor. The inherited tree stays in history, on rebuild, and under the archive tags." -m "Model: <you>"
git -C W ls-tree HEAD                  # expect empty
git -C W log --oneline | tail -1       # expect bf5f04d Initial commit
```

**S3. The lab, unchanged**

```text
git -C W add -- labs/clerk-handoff-pass01
git -C W status --short                # expect 36 new files, nothing else
git -C W commit -m "Keep labs/clerk-handoff-pass01 as found (experimental evidence, 36 files)." -m "Model: <you>"
```

Check A1: `git -C W diff HEAD -- labs` is empty, and every hash matches.

**S4. Minimum imports, from git objects only**

```text
copy import.py and import-manifest.tsv to W\imports\   (then stage them with the S4 commit)
python -B -I W\imports\import.py --manifest W\imports\import-manifest.tsv --tier minimum --repo W --check
python -B -I W\imports\import.py --manifest W\imports\import-manifest.tsv --tier minimum --repo W
```

The `--check` must print `ready: 688 row(s)`. For the P1 rows (`1008` and `1009` from the archive branch), add their rows to the manifest from `git -C W ls-tree -r origin/archive/librarian-worktree-2026-10-26`, then run again with `--ids P1`.

Stage the destinations by the manifest list, not with `-A`. Commit: `Import minimum manifest (M1-M8, P1): N files, bytes from git objects`, with a `Model:` line. Check A3.

**S5. New drafts**

Write these with the candidate tools in development mode (`--candidate … --sha256 …`), or by hand where no candidate tool can write them, marked as a hand form:
- **Work book:** `00.kernel/00.00.10.work/00.md`, `0010.about`, `0011.contents`, `0014.design`; doors `0100.band.returns`, `0400.band.dev`, `0500.band.packs`, `0600.band.notes`; pages `0401.goal`, `0408.seats`, `0409.decisions` (the register: verbatim reply, path@rev), `0410.imports` (the manifest, the collisions, and the lab reference from the lab README), `0611.findings` (`1001.assessment` F01–F05 and the open lines of returns `0101`–`0106`, cited).
- **Law:** new pages `0041.handoff`, `0062.role-director`, `0063.role-prime`, `0064.role-colab`, `0065.role-builder` and the door `0300.band.compute`, each as `FF.md`, `state: draft`. Drafts beside existing seats: `0057.bands/01.VVV.md` (runtime band, space 0), `0018.seqaddr/01.VVV.md` (desk books, D1), and law `00.md` (spaces declaration). Seats are never overwritten.
- **Runtime cards:** `02.md` for `0302`, `0303`, `0304`, `0305` and `0307`, with `runs:`, `uses:` and `args:` only. Each names the active file `02.<name>.py`, which doesn't exist yet, so normal mode refuses, as intended.
- **Stamps:** stamp lines on the M5 candidates (`PPPP`, `book`, `keyword`, `source path`, `source hash`). The bytes below the stamp stay exact. `02.face.001.py` gets its first stamp. Record each before and after sha256 in `0410.imports`.
- **Boot:** `AGENTS.004.md` beside `AGENTS.md`. It points to desk `00.kernel` and the entry.

Commit with the `Model:` line. Check A3: candidates still identifiable, no active `02.<name>.py`.

**S6. The entry and the acceptance tests**

- `app/librarian.py` (`where`, `--context`, development `--candidate/--sha256/--scope`), following section 3 of `proposal.md`.
- `app/tests/` holding A1 and A3–A6.
- `.gitignore`.

Commit. Run A4 (fresh clone under `%TEMP%`), A5 and A6.

**S7. Push and report**

```text
git -C W push -u origin workshop
```

Never push `main`. Check A2 against S0. The return lists:
- every commit;
- the A1–A6 results, verbatim;
- the counts against the manifest;
- every refusal;
- what waits on the Director: D5, D6, D8 and D9.

## Stop conditions

Stop and write a `>stop` if any of these happens:
- an A2 fingerprint changes;
- a lab hash changes;
- `import.py --check` reports any problem;
- a destination already exists;
- a decision this assignment waits on is not yet answered;
- a step would need `-A`, a worktree, or a write in an old checkout.
