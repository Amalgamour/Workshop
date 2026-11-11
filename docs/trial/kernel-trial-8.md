# Kernel trial 8 (TRIAL-K8): hostile pass on kernel pass 9, the no-symlink guard, the git-entry check, root commits, and the published copies

Lane TRIAL-K8, 2026-11-11, about 5:00 PM CST (6:00 PM EST). I'm a fresh session that did not build these faces or this builder. Under R20 (`DIRECTOR-RULINGS.md:78-80`) that counts as a different view (`DIRECTOR-RULINGS.md:7-9`, R2).
I only report. Nothing in `kernel/` (except Q61-Q62 and a Q60 note in `kernel/QUESTIONS.md`), `books/`, `crates/` or `app/` was changed, nothing was seated, nothing was pushed, merged or deleted. New questions are tagged `[TRIAL-K8]`.

**Target (HEAD `697dfbe`):**
- A) the pass 9 guard (`5809243`, tests in `4b94caf`): no symlinks, a seated face must be a committed regular file at the seat blob, history follows links, root commits are parsed, and the merge-carry rule; plus the 26 seats;
- B) the only changed draft face, `10.11.21.0013.00.draft` (the new `seat-05.02:` line, `why-05.02:` removed);
- C) portability: a `--no-local --single-branch` clone of `/workspace/workshop-build/publish`, a clone of GitHub `prima/build`, and the publish copy's hygiene after the Q60 change.

**Judged against:** `DIRECTOR-RULINGS.md` R1-R22, `kernel/QUESTIONS.md` (Q51, Q58-Q60), `docs/BUILD-LOG.md` (pass 9 entry), `docs/trial/kernel-trial-7.md`, `kernel/build.mjs`, `kernel/build.test.mjs`.
**Rules used:** Q41 is applied, not held. Q55 and Q35 are the Director's. Q51 (where seat records live, so face 00 can never match a trialed blob) is open, so face 00 is judged as a draft only; this trial makes no seat recommendation for it.

## Summary

| Verdict | B (pass-9 faces) |
|---|---|
| PASS | 1 (as a draft; face 00 is not seatable while Q51 is open) |
| FAIL | 0 |
| HELD-7 (depends on an open question) | 0 |
| **total** | **1** |

| Severity | Findings |
|---|---|
| blocker | 0 |
| major | 0 |
| minor | 3 (finding 1: the history fallback misses three link shapes; finding 2: face 00 is read from the working tree only; finding 3: the forged-trial and gitfile residues, unchanged) |

**PASS list, eligible for an R2 seat:** none this pass (no 05 pack changed).

**Faces that pass as drafts, not seatable while Q51 is open** (blob for the record, not a PASS list entry):
`10.11.21.0013.00.draft` blob `00172ac104606281bcd7de2df9d70e8eede263bb`.

**Plain words:** every symlink trick I tried on a live build is refused, and every seat-hiding trick that could build clean in a clone is refused. The 26 seats all check out, in this repo, in the publish copy and on GitHub. What I found is smaller: the backup history search behind the symlink refusal has three blind spots that the front-line refusal already covers, and a seat can be made locally while face 00 is kept out of git, which a fresh clone catches. The two old leftovers are unchanged.

## TRIAL-K7 fixes: did they land?

| K7 # | Landed? | Evidence |
|---|---|---|
| 1 major (symlinks hide seats) | yes | `linkIn`/`noLink` (`build.mjs:66-84`) check every step from the repo root with `lstat`; `sources` (`:119-128`) and `loadBook` (`:130-138`) refuse linked folders and faces; `priorSeats` (`:422-428`) refuses any mode `120000` at HEAD or in the index under `kernel`, `books`, `docs/trial`, `docs/spec`; `gitEntry` (`:294-303`) makes every seated face a `100644` entry whose blob is the seat blob. L1-L13 and G1-G4, H4 below are all refused. T18, T18b, T18c (and H1b) are refused or found in history. |
| 2 minor (root commit crash) | yes | `trialOrigin` header regex allows the trailing space (`:246`); `HIST` has `--root` (`:223`); the touch rule uses `diff-tree --root`. No crash in O1-O6. |
| 3 minor (H4 forged trial, gitfile) | still open, as admitted | T13r and T20r below. Not worse. |
| 4 minor (publish `incoming`) | yes | C3: no `incoming` ref; Q60 option A was taken. |

## Checks run (real output)

`/tmp/k8/repo` is a fresh `git clone --no-local` of the shared repo at `697dfbe` (full history, branch `build`). Each hostile copy is a fresh clone of it under `/tmp/k8/<name>` (helpers in `/tmp/k8/lib.sh`). `find kernel books docs -type l` is empty at `697dfbe`.

**`node kernel/build.mjs --check`** (`/tmp/k8/repo`): exit 0.
```
finding  00.00.00.0051.01.draft.md: 04 full-address: why missing (4.7)
... (59 findings, all "why missing (4.7)")
checked  books/00.00.00.book  50 entries
checked  books/00.00.axioms.jsonl  7 entries
checked  books/10.00.00.book  1 entries
checked  books/10.11.00.book  1 entries
checked  books/10.11.21.book  15 entries
seats 26
59 findings, 0 errors
```

**`node kernel/build.test.mjs`** (`/tmp/k8/repo`): exit 0. 49 `ok` lines, then `all passed`. The pass 9 ones:
```
ok    Q58: a symlinked face 00 is refused (K7 T18)
ok    Q58: a seat written through a face 00 link and removed later is still found in history (K7 T18)
ok    Q58: a symlinked book folder is refused (K7 T18b)
ok    Q58: a seat written through a book folder link into kernel/parked is still found in history (K7 T18b)
ok    Q58: a seated face that is a symlink to an untracked copy is refused (K7 T18c)
ok    Q58: a seated face committed as a symlink is refused though the working file has the seated bytes (K7 T18c)
ok    Q58: a seated face that git does not hold (untracked) is refused
ok    Q59: an orphan root commit adding an edited trial copy is refused, not a crash (K7 T11)
ok    Q59: a trial added by an orphan root commit (trial only) is a valid origin
all passed
```

**`CARGO_TARGET_DIR=target/k8-trial cargo test --workspace --no-fail-fast`** (in `/tmp/k8/repo`): `exit=0`; 38 `test result:` lines, `411 passed; 0 failed; 2 ignored`, every line `test result: ok.`.

**26 seats, each blob equal to `git rev-parse HEAD:<path>`, each mode `100644`** (read from the `seat-NN:` lines of the face 00 files at `697dfbe`):
```
OK 00.00.00.0051.05.01 c160a4da9947eeeb3de88b512208ee9e7836011b 100644 | kernel-trial-5.md blob 86eb3a58e028d9b23e0a94cd4577329195300f99
OK 00.00.00.0051.05.02 7dbf70bd22af1bf0354edd82aff3ddb405ef892d 100644 | kernel-trial-4.md blob a5d253d5e12722956afea38e79cb7fc1cf492c7b
OK 00.00.00.0052.01 88bce491bb2bffe645a5c6825096f41d8b86080f 100644 | kernel-trial-5.md
OK 00.00.00.0052.04 e9ca59a1d708acfd57b9e5f7e6b758e41e4fde6f 100644 | kernel-trial-5.md
OK 00.00.00.0052.05.01 7993b14b830d12feb5a54509b41e74c931afe334 100644 | kernel-trial-4.md
OK 00.00.00.0052.05.02 c82b1fc6d2d3d6ce6e5a44cf99cbc7bf93b62332 100644 | kernel-trial-4.md
OK 00.00.00.0053.05.01 77ee148ffd645b15b4aeeb1401ff6b72e05a35da 100644 | kernel-trial-4.md
OK 00.00.00.0053.05.02 8499872db0d7551309befdbf12ce1d1c7fa821c4 100644 | kernel-trial-4.md
OK 00.00.00.0054.05.01 aa07b61116572c9e25353a5e7f3b6ed97941d2a0 100644 | kernel-trial-5.md
OK 00.00.00.0054.05.02 2bf1da6ff8c4bd77943150da2786f07d93fe824d 100644 | kernel-trial-6.md blob ca9c0b8f993a1061c97a4a12735f2e0f1b360a0e
OK 00.00.00.0055.05.01 6582d3e56495ca93203e81871659da0481550d41 100644 | kernel-trial-4.md
OK 00.00.00.0055.05.02 596aa9ba0befffa6f9f6ca93364b9a6fea426478 100644 | kernel-trial-4.md
OK 00.00.00.0056.01 112c169ccd06d54c6d9ab607fee6c2d16004cc62 100644 | kernel-trial-2.md blob da5d51424fee3bea1d8443c619fcba3c534a1ace
OK 00.00.00.0056.05.01 0914ebb8274c3e049440e11388b69da2b138f447 100644 | kernel-trial-4.md
OK 00.00.00.0056.05.02 93178adddeb2ec915a2c5d4cc070d0dc50c03d37 100644 | kernel-trial-4.md
OK 00.00.00.0057.05.01 67b3b9b6762af70a7494893fb7ff47e4e86e4281 100644 | kernel-trial-4.md
OK 00.00.00.0057.05.02 037eec2ff5e9c6c18020f06679358a13e9a62bb1 100644 | kernel-trial-4.md
OK 00.00.axioms.05.01 cbf5cba0d5429e2e0b14e56f5ed8a1eba1d06ad2 100644 | kernel-trial-5.md
OK 00.00.axioms.05.02 452be16b0536002a12279c5d485c68c5217fa6c8 100644 | kernel-trial-4.md
OK 10.11.21.0012.05.01 9aaed75fc8f0594a1289fa83e870a474d4d021d2 100644 | kernel-trial-4.md
OK 10.11.21.0012.05.02 dd89a5199d1a0b47f5cac3bce2ec0e8185ff1ce6 100644 | kernel-trial-5.md
OK 10.11.21.0013.05.01 16146a0fa073fc947138de43033f9e9a2b75ac09 100644 | kernel-trial-5.md
OK 10.11.21.0013.05.02 24a27e08bfb78ff75b1f7a2b91e82e2956a1163f 100644 | kernel-trial-7.md blob 377929b55738cb2477f4f3c3e88e484ae0031e22
OK 10.11.21.1001.01 5415cef2dd0a37f3c2ba4c9b6d2652262f0ef82d 100644 | kernel-trial-2.md blob da5d51424fee3bea1d8443c619fcba3c534a1ace
OK 10.11.21.1001.05.01 566071064f63a5c85fcb3bd87d9e375717bdbf51 100644 | kernel-trial-4.md
OK 10.11.21.1001.05.02 2aa3490239620604ce1bb13c34841a60ac8f7056 100644 | kernel-trial-4.md
```
26 of 26 OK. The new seat `0013.05.02` cites `docs/trial/kernel-trial-7.md blob 377929b55738cb2477f4f3c3e88e484ae0031e22`, which is both its HEAD blob and its only add (`7eb27d0`, touching only `docs/trial/kernel-trial-7.md` and `kernel/QUESTIONS.md`).

### Part B: the changed face 00

`git rev-parse HEAD:kernel/samples/10.11.21/10.11.21.0013.00.draft.md` is `00172ac104606281bcd7de2df9d70e8eede263bb`, as expected. `git show e713c27` changes it in exactly three lines:
- `faces:` now says `05.02 seated` (`:10`); the file `10.11.21.0013.05.02.md` exists with no tail (renamed from `.draft.md` in the same commit, blob unchanged).
- `seat-05.02: approved-by: build-stage (R2); trial: docs/trial/kernel-trial-7.md blob 377929b55738cb2477f4f3c3e88e484ae0031e22; blob: 24a27e08bfb78ff75b1f7a2b91e82e2956a1163f` (`:12`). Both blobs are full, both are true (the face blob equals `HEAD:<path>`; the trial blob equals HEAD and the first add), and the trial's PASS list (`kernel-trial-7.md:29-30`) names `10.11.21.0013.05.02` at that exact blob. Same form as `seat-05.01` on `:11`.
- `why-05.02:` is removed. No other mention of 05.02 or Q41 is left in the file; `why-01:` and `why-04:` are unchanged.
- `books/10.11.21.book` entry `n:11` changed from `10.11.21.0013.05.02.draft` to `10.11.21.0013.05.02` with `approved-by` and `trial` keys; entry `n:7` carries the new face 00 body. `--check` matches.

### Part C: portability (real output)

**C1. `git clone -q --no-local --single-branch /workspace/workshop-build/publish /tmp/k8/pub`:**
```
07829d1 KERNEL pass 9: BUILD-LOG entry (5809243, e713c27, 4b94caf; 26 seats; checks pass in repo and published
4b369fa absent
7eb27d0 absent
ed82086 absent
697dfbe absent
0 (commits touching target/)
false                      (is-shallow-repository)
check-exit=0
checked  books/00.00.00.book  50 entries
checked  books/00.00.axioms.jsonl  7 entries
checked  books/10.00.00.book  1 entries
checked  books/10.11.00.book  1 entries
checked  books/10.11.21.book  15 entries
seats 26
59 findings, 0 errors
0 (ERROR lines)
tests-exit=0
49                         (ok lines; 0 FAIL)
all passed
07829d10020496ac5aeaae87fb26d13769fbfd18   (HEAD)
465eb4201a85d890debaecbd2d7b2c439499c068   (HEAD tree)
465eb4201a85d890debaecbd2d7b2c439499c068   (local 697dfbe tree)
```

**C2. `git clone -q --single-branch -b prima/build https://github.com/Amalgamour/Workshop.git /tmp/k8/gh`** (read only):
```
07829d1 KERNEL pass 9: BUILD-LOG entry (5809243, e713c27, 4b94caf; 26 seats; checks pass in repo and published
07829d10020496ac5aeaae87fb26d13769fbfd18
465eb4201a85d890debaecbd2d7b2c439499c068
4b369fa absent
7eb27d0 absent
ed82086 absent
697dfbe absent
0 (commits touching target/)
false
check-exit=0
checked  books/00.00.00.book  50 entries
checked  books/00.00.axioms.jsonl  7 entries
checked  books/10.00.00.book  1 entries
checked  books/10.11.00.book  1 entries
checked  books/10.11.21.book  15 entries
seats 26
59 findings, 0 errors
0 (ERROR lines)
tests-exit=0
49
all passed
```
GitHub `prima/build` is the publish `build` HEAD `07829d1`, and its tree equals the local `697dfbe` tree.

**C3. Publish copy hygiene (`/workspace/workshop-build/publish`, read only: `branch -vv`, `for-each-ref`, `config`, `rev-list`, `cat-file -e`, `push --dry-run`):**
```
* build 07829d1 [origin/prima/build] KERNEL pass 9: BUILD-LOG entry ...
refs/heads/build
refs/remotes/origin/prima/build
remote.origin.push refs/heads/build:refs/heads/prima/build
git push --dry-run --porcelain:
To https://github.com/Amalgamour/Workshop.git
=	refs/heads/build:refs/heads/prima/build	[up to date]
Done
.git/refs/original: empty folder; for-each-ref refs/original: 0
build commits touching target/: 0
all refs touching target/: 0
FETCH_HEAD: 697dfbe6... branch 'build' of ../repo
rev-list FETCH_HEAD -- target/: 2      rev-list --reflog -- target/: 2
4b369fa, 697dfbe: objects present in the object store (no ref)
```
- No `incoming` ref (Q60 option A landed). A bare push goes only to `prima/build`. No `refs/original`. Yes to all three.
- Report only: `.git/FETCH_HEAD` and the reflogs still reach 2 commits that touch `target/`. Neither is a ref that `--all` or `--mirror` pushes, so this is an observation, not a finding; only an explicit `git push origin FETCH_HEAD:<ref>` would publish them.

### Hostile tests (part A, scratch clones only)

Seat fixture used in H*, S*, O*, G1: a new face `10.11.21.0013.05.03.md` (a copy of the seated `0013.05.01` plus one line, blob `ea4df21d...`), passed by a forged trial in a docs-only commit, with a `seat-05.03:` line on the 0013 face 00. Un-seat (U00, T20r): `1001.05.02` renamed to `.draft.md`, its seat line removed, no `unseat-05.02:`, its `books/` keys dropped.

| # | Hostile change | Result |
|---|---|---|
| U00 | control: un-seat `1001.05.02`, committed | refused: "10.11.21.1001.05.02 was seated (build-stage (R2)) in the last build but is not now; write unseat-05.02" |
| S00 | seat 05.03 with the face file not added to git (write mode) | refused: "seated face ... is not in git (untracked; not at HEAD or in the index)" |
| L1 | face 00 replaced by a relative link inside the repo (`../../../docs/x/f00.md`) | refused: "is a symlink" |
| L2 | seated `1001.05.02.md` replaced by a link to a committed copy with the seat bytes (uncommitted, then committed) | refused both times: "is a symlink", and once committed also "is a symlink in git (HEAD)" / "(index)" |
| L3, L4 | `kernel/samples`, `kernel/00.00.00` replaced by a link to a sibling folder | refused: "kernel/samples: is a symlink" / "kernel/00.00.00: is a symlink" (plus the un-seat errors for every seat in them) |
| L5, L6 | `books/`, `books/10.11.21.book` replaced by a link | refused: "books: is a symlink" / "books/10.11.21.book: is a symlink" |
| L7 | `docs/trial/kernel-trial-4.md` committed as a link (mode 120000) to a copy | refused: "seat cites trial docs/trial/kernel-trial-4.md, and that path is or goes through a symlink" (every kernel-trial-4 seat) |
| L8, L9 | `docs/trial`, then all of `docs`, replaced by a link | refused: "...goes through a symlink"; L9 also "docs: is a symlink" |
| L10 | `docs/spec/DIRECTOR-RULINGS.md` committed as a link | refused: "is a symlink", "is a symlink in git (HEAD)", "(index)" |
| L11 | a cited `why:` source `docs/spec/drafting.md` replaced by a link | refused: "docs/spec/drafting.md: is a symlink" |
| L12 | a face 00 committed as a link, then cloned with `core.symlinks=false` (the link arrives as a plain file holding the link text) | refused: "is a symlink in git (HEAD)" and "(index)" |
| L13 | the whole `kernel/` committed as a link to `k2/` | refused: "kernel: is a symlink in git (HEAD)" / "(index)" |
| L13b | the same, uncommitted (`kernel` link in the working tree only) | refused: every seat "seated face k2/... is not in git" |
| G1 | 05.03 staged in the index, not committed | write mode accepts (`seats 27`, by design, Q58 B); `--check` refuses: "not in git (untracked; not at HEAD)" |
| G2 | `--check` with the index holding a different blob for `1001.05.02` (HEAD and worktree = seat blob) | `--check` exit 0 (HEAD is what it checks, and HEAD is right); write mode refuses: "is blob 0b341c80... in git (index), not the seat blob" |
| G3 | `assume-unchanged` on `1001.05.02`, then edit it | refused: "seated face changed since its trial" |
| G4 | seated face committed with mode 100755 | refused: "is mode 100755 in git (HEAD), not a regular file (100644)" (fails closed) |
| H4 | `kernel/samples/10.11.21` replaced by a git submodule (mode 160000) holding the same files | refused: every seat in it "is not in git (untracked; not at HEAD)" |
| H1b | `kernel/samples` committed as a link to `kernel/s2`; seat 05.03 through it; un-seat; link removed | found in history: "10.11.21.0013.05.03 was seated ... write unseat-05.03" |
| **H1** | **the whole `kernel` committed as a link to `k2/` (C1); seat line written in `k2/.../0013.00` (C2); un-seated (C3); `kernel/` restored (C4)** | **not found**: `--check` exit 0, `seats 26`. The C1-C3 states never build (L13), so no clean seat existed (finding 1) |
| **H2** | **face 00 committed as an absolute link to `/tmp/k8/h2/docs/x/f00.md` (inside the repo); seat, un-seat, restore** | **not found**: exit 0, `seats 26`. `historySeats` skips absolute links (`:391`). C2 is refused live: "is a symlink" (finding 1) |
| **H5** | **two-hop chain: face 00 -> `docs/a` (a link) -> `docs/b/f00.md`; seat, un-seat, restore** | **not found**: exit 0, `seats 26`. The second hop's target is filed as a folder (`''`, `:395`), not as page 0013's face 00 (finding 1) |
| **H3** | **face 00 removed from git and listed in `.git/info/exclude`, seat line written in the untracked file, books built and committed (C2); later face 00 re-added without the seat, books line dropped (C3)** | **local `--check` at C2: exit 0, `seats 27`.** A fresh clone at C2 refuses ("no face 00"). At C3: exit 0, `seats 26`, also in a fresh clone; the seat is only in `books/` history at C2, which the guard does not walk (finding 2) |
| O1 | orphan root adds a new trial plus `kernel/junk.txt`, merged in; seat cites it | refused: "the commit that added trial ... also changes kernel/junk.txt" (no crash) |
| O2 | evil merge (main + an empty side commit) whose tree adds a brand-new trial no parent has | refused: "is added only by a merge commit" |
| O2b | the same with an orphan side | refused: "is added only by a merge commit" |
| O3 | legit appendix to `kernel-trial-2.md` in a docs-only commit (with a fake PASS line) | the 2 kernel-trial-2 seats still verify: exit 0, `seats 26`; the appendix cannot be cited (only the first-added blob is) |
| O4 | O3, then merge an unrelated orphan history | still exit 0, `seats 26` (the merge-carry rule works: the orphan side's "add" of the edited blob is the main parent's blob) |
| O5 | evil orphan merge whose result also edits `kernel-trial-2.md` | refused, both kernel-trial-2 seats: "added more than once ... with different blobs". Fails closed |
| O6 | orphan root re-adds the same real blob of `kernel-trial-4.md` (docs only), merged | exit 0, `seats 26` (same blob, nothing new) |
| T13r | brand-new forged `kernel-trial-99.md` in a docs-only commit seats 05.03 | **accepted**: exit 0, `seats 27`, `--check` exit 0. Known residue (finding 3) |
| U01 | then un-seat 05.03 with no record and its books line dropped | refused: "10.11.21.0013.05.03 was seated ... write unseat-05.03" |
| T20r | `.git` replaced by a gitfile to a made-up history (root: the two TRIAL-K2 face blobs; then every trial at its first-added blob, docs-only; then the un-seated tree) | **accepted** in write mode: exit 0, `seats 25`. Real `.git` back: refused (U00 message). Known residue (finding 3) |

Not repeated: a prefix-collision forge, shallow clones, replace refs, grafts, attributes and `GIT_*` env (all still covered by passing tests in three clones).

## Findings

### 1. minor: the history fallback behind the symlink refusal has three blind spots
- **Evidence:**
  - `historySeats` walks `-- kernel/` plus link targets (`build.mjs:378`). A link at `kernel` itself is not under `kernel/`, so it is never seen (H1).
  - Absolute links are skipped on purpose (`:391`), even when they point inside the repo (H2).
  - A link's target is filed as page's face 00 only if the link's own name is a face 00 name (`:394-395`). On a second hop (`docs/a` -> `b/f00.md`), the name is `a`, so the target is filed as a folder `''`, and a file is never under it (H5).
  - In all three, a seat line added and removed through the link leaves no trace the guard reads; the final state builds clean, also in a fresh clone.
- **Limits:** none of these states can build. The live refusal (`noLink`, the `120000` check at HEAD and index) stops the build at every commit where the link exists (L1, L13), so no seat was ever valid there, and none of the 26 seats is touched. The seat lines stay in git history for a person to find.
- **Breaks:** only the pass 9 claim (`BUILD-LOG.md` pass 9 step 1, Q58 note) that "a symlink ever committed under `kernel/` is followed in history". It holds for one-hop relative links under `kernel/` (T18, T18b, H1b).
- **Fix direction (builder lane, not done):** either walk `-- kernel` (no slash) too, resolve absolute targets that land inside the repo, and carry the page through chains; or say plainly that the fallback is best-effort and the live refusal is the guard. Raised in Q61.

### 2. minor: face 00 is read from the working tree and never checked against git
- **Evidence:** `gitEntry` (`:294-303`) checks only the seated face. Face 00, which holds the seat line, is read from disk (`loadBook`, `:130`). In H3, with face 00 untracked and excluded, a seat is built and `books/` committed, and the local `--check` passes with `seats 27`. Later face 00 is put back in git without the seat and the books line dropped: exit 0, `seats 26`, also in a fresh clone. `priorSeats` reads only `HEAD:books/` (`:430-437`), not the history of `books/`, where the seat is recorded.
- **Limits:** the seat state (C2) fails in any fresh clone ("no face 00"), so it never reached a published copy as a working seat. It is local only, the same class as the gitfile swap (K6 K15). A modified-but-uncommitted face 00 gives the same effect and shows in `git status`.
- **Fix direction:** under `--check`, require every file the builder reads under `kernel/` to be tracked and equal to its HEAD blob (at least face 00); and/or read past seats from the history of `books/` too, as the face 00 history is read. Raised in Q62.

### 3. minor (class, no verdict change): the H4 and gitfile residues are unchanged
- T13r: a brand-new forged trial in a docs-only commit still seats a face (`seats 27`, 0 errors).
- T20r: a local gitfile swap to a made-up history still builds clean in write mode (`seats 25`). Since Q59, a root commit that adds only trials is a valid origin, so the made-up history no longer needs an empty root, but that is the same residue, not a new one. A fresh clone of the real repo refuses it.
- Neither got worse.

**Observations (no severity):**
- **O5 fails closed:** an evil merge of an orphan that edits a cited trial in the merge result blocks every seat that cites that trial. That is the right side to fail on; a person would have to undo the merge.
- **G1 is by design:** write mode accepts a seated face that is only staged (Q58 B, "so a seat can be built before its commit"); `--check` refuses it until it is committed.
- **Publish leftovers:** `FETCH_HEAD` and reflogs still reach 2 `target/` commits (C3). Not a ref; report only.
- **Order in `historySeats`:** as in K7, "newest seat" follows `git log` order across merges. Not tried; the branch is linear.

## Per-face verdicts

| Face | Blob (HEAD `697dfbe`) | Verdict | Findings / open question |
|---|---|---|---|
| `10.11.21.0013.00.draft` | `00172ac104606281bcd7de2df9d70e8eede263bb` | PASS (draft; not seatable, Q51) | The `faces:` line, the new `seat-05.02:` line and the removed `why-05.02:` are accurate (part B): both cited blobs are full and true, the trial's PASS list names the face at that blob, the books entry matches. Nothing else changed. Face 00 stays a draft: Q51 is open, so no seat recommendation is made. |

**What a PASS on this face 00 checked:** `git show e713c27` line by line; the `faces:` list against the files on disk; each seat line's two blobs against `git rev-parse HEAD:<path>` and the trial's first add; the trial's PASS list; the books entries `n:7` and `n:11`; and that `--check` passes in the repo, publish and GitHub clones.

## Method
- **Repo state:** the shared working tree was only read. My only writes are this file and Q61-Q62 plus a short Q60 note in `kernel/QUESTIONS.md`, committed by pathspec (the index was empty first). The builder was never run in the shared tree.
- **Scratch copies:**
  - `/tmp/k8/repo` (fresh `--no-local` clone at `697dfbe`, cargo target `target/k8-trial` inside it);
  - `/tmp/k8/<test>` (one fresh clone per attack), `/tmp/k8/evil` (made-up history for T20r), `/tmp/k8/sub` (H4 submodule);
  - `/tmp/k8/pub` (publish, `--no-local --single-branch`) and `/tmp/k8/gh` (GitHub `prima/build`).
- **Publish copy:** read only. Nothing fetched into it, deleted or pushed.
- **Blobs:** each is `git rev-parse HEAD:<path>` at `697dfbe`, written in full.
