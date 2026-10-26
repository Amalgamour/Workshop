# Draft assignment: preserve the unique worktree material

**state:** draft, for the Director's review. Not released. Nothing here has been run, apart from the read-only `--check` in step P0.
**who drafted:** claude-opus-5-5 (Colab), 2026-10-26
**seat:** a Builder, or Prime, at the Director's word (D7)
**branches:**
- `archive/librarian-worktree-2026-10-26` (from `14676ca`)
- `archive/rebuild-worktree-2026-10-26` (from `de3b8eb`)
- tags `archive/main-14676ca`, `archive/rebuild-de3b8eb`

## Why

Some of the Director's decisions exist only as untracked files: `1008.app-plan` and `1009.calling`. Other unique work is the same: the Research paper, tool versions, the redraft pages and the Codex assessment. A disk fault or a clean-up would lose them. This assignment puts each listed file, byte for byte, on a pushed archive branch. It **does not** touch either old checkout: they are only read.

## Scope

**In scope:** exactly the 118 rows of `preservation-manifest.tsv`, groups P1–P7.

**Out of scope:**
- any other file;
- `10.workshop.zip`, held in `preservation-held.tsv` until the Director decides;
- the 264 deleted files.

**Never:** `git add -A`, `git add .`, or `git commit -a`.

## Steps

All commands run in a new, empty temp folder. `$T` stands for it, for example `C:\Users\<you>\AppData\Local\Temp\lib-preserve`. Neither old checkout is the current folder at any point.

**P0. Baseline, read-only**

```text
git -C D:\Git\Librarian status --porcelain -uall      > $T\before-librarian.txt
git -C D:\Git\Librarian-rebuild status --porcelain -uall > $T\before-rebuild.txt
python -B -I preserve.py --manifest preservation-manifest.tsv --groups P1,P2,P3,P4,P5,P6 --workspace Librarian --source D:\Git\Librarian --check
python -B -I preserve.py --manifest preservation-manifest.tsv --groups P7 --workspace Librarian-rebuild --source D:\Git\Librarian-rebuild --check
```

Expect `source matches: 90 file(s)` and `source matches: 28 file(s)`. These both passed on 2026-10-26. Any `changed:` line stops the assignment. Report it, and wait for a new manifest.

**P1. Temp clone from GitHub**

It shares no objects with the old checkouts.

```text
git clone https://github.com/Amalgamour/Librarian.git $T\pres
git -C $T\pres switch -c archive/librarian-worktree-2026-10-26 14676ca3c01833cc1b472198e62e3451ef706ec3
```

**P2. Copy and verify, groups P1–P6**

```text
python -B -I preserve.py --manifest preservation-manifest.tsv --groups P1,P2,P3,P4,P5,P6 --workspace Librarian --source D:\Git\Librarian --dest $T\pres
```

Stage exactly the paths it prints, by name, for example `git -C $T\pres add -- <path> <path> ...`. Then:

```text
git -C $T\pres status --short          # expect only those paths
git -C $T\pres commit -m "Preserve unique main-worktree material, 2026-10-26 (P1-P6, 90 files)" -m "Manifest: preservation-manifest.tsv. Byte-verified by preserve.py." -m "Model: <your model>"
```

**P3. The rebuild assessment, group P7**

```text
git -C $T\pres switch -c archive/rebuild-worktree-2026-10-26 de3b8ebc3df3e1da28c4d675963699644b78afab
python -B -I preserve.py --manifest preservation-manifest.tsv --groups P7 --workspace Librarian-rebuild --source D:\Git\Librarian-rebuild --dest $T\pres
```

Stage the printed paths by name, then commit: `Preserve 1001.assessment (Codex, untracked), 28 files`, with a `Model:` line.

**P4. Tags, then push only the archive branches and tags**

```text
git -C $T\pres tag archive/main-14676ca 14676ca3c01833cc1b472198e62e3451ef706ec3
git -C $T\pres tag archive/rebuild-de3b8eb de3b8ebc3df3e1da28c4d675963699644b78afab
git -C $T\pres push origin archive/librarian-worktree-2026-10-26 archive/rebuild-worktree-2026-10-26 archive/main-14676ca archive/rebuild-de3b8eb
```

Never push `main` or `rebuild`.

**P5. Verify from GitHub, in a second fresh clone**

```text
git clone --branch archive/librarian-worktree-2026-10-26 https://github.com/Amalgamour/Librarian.git $T\verify
python -B -I preserve.py --manifest preservation-manifest.tsv --groups P1,P2,P3,P4,P5,P6 --workspace Librarian --source $T\verify --check
git -C $T\verify switch archive/rebuild-worktree-2026-10-26
python -B -I preserve.py --manifest preservation-manifest.tsv --groups P7 --workspace Librarian-rebuild --source $T\verify --check
```

Expect 90 and 28 matches.

**P6. Old workspaces unchanged**

```text
git -C D:\Git\Librarian status --porcelain -uall        > $T\after-librarian.txt
git -C D:\Git\Librarian-rebuild status --porcelain -uall > $T\after-rebuild.txt
```

The before and after files must be identical. `git -C D:\Git\Librarian for-each-ref` must also be unchanged: the temp clone wrote no refs into the old repositories.

## Return

Write the return on the work book once it exists, or else as a chat report. It gives:
- the two archive commits and both tags, by full hash;
- the P5 match counts;
- the P6 comparison;
- any stopped step, quoted.

Don't delete the temp folders until the Director has read the return.
