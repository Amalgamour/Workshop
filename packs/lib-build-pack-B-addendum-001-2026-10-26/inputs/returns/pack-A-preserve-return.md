# Pack A return: preserve before establishing the workspace

**pack:** `packs/lib-build-bootstrap-pass01-2026-10-26/PACK-A-preserve.md`
**executor:** claude-opus-5-5
**date:** 2026-10-26
**release:** the Director in chat, `>run.pack`. Pack A only. Pack B was not started.
**state:** returned for Prime review. This return approves and seats nothing.
**location:** the pack names `notes/returns/pack-A-preserve-return.md`. The Director said in chat that returns now go to `lib-build/returns/`. This file follows the Director, so the two faces disagree and Prime should settle it.

## Result

Every archived file matches its source, verified from a fresh clone: 167 of 167 rows, by destination, length and SHA-256, plus 39 of 39 evidence files and both tags. The old checkouts are unchanged by fingerprint. The baseline lab and notes are byte-exact.

One defect was found, and fixed forward without a force push: line endings on 29 CRLF files (finding F1). The first verification that caught it is kept.

| Archive ref (GitHub) | Full hash | Rows | Bytes |
|---|---|---|---|
| `refs/heads/archive/librarian-worktree-2026-10-26` | `e8b1a994da07000fa576fd771e455a94718ed431` | P1–P6, 90 | 3,585,368 |
| `refs/heads/archive/rebuild-worktree-2026-10-26` | `586cfa4ae055c29a98c1106bb70143901c57cc11` | P7, 28 | 181,478 |
| `refs/heads/archive/lib-build-bootstrap-2026-10-26` | `fe42b017b5e8c288f70878d696cb227b09ab5a8e` | P8–P9, 49 | 738,210 |
| `refs/tags/archive/main-14676ca` | `14676ca3c01833cc1b472198e62e3451ef706ec3` | baseline | — |
| `refs/tags/archive/rebuild-de3b8eb` | `de3b8ebc3df3e1da28c4d675963699644b78afab` | baseline | — |

**Commits on each branch** (base, then rows, evidence, exact bytes):

| Branch | Base | Rows | Evidence | Exact bytes |
|---|---|---|---|---|
| librarian-worktree | `14676ca` | `c94ce49e0257f253a0504edcac37ede979557f98` | `733d7fc942715ca42f740a0e9f0b407ebac68885` | `e8b1a994…` |
| rebuild-worktree | `de3b8eb` | `cf7b45628cb05459f05275c5dbd55d0447dc6e8d` | `1a63b4a446f24718838c734d505d0feea018abae` | `586cfa4a…` |
| lib-build-bootstrap | `14676ca` | `1e638e11b8edc3b74e8114e6ef3c8c4df026c494` | `c86b78a5976a2b3f1ba1c0ad619f0b97d12c29c7` | `fe42b017…` |

**Not pushed or changed:** `main` (still `14676ca`) and `rebuild` (still `de3b8eb`). No wildcard refs, no force pushes, no merges. `evidence/remote-refs-final.txt` holds the full remote ref list.

## #01 Capture and preflight: pass

- **Pack self-check:** all 18 files in `manifest.sha256.tsv` match.
- **Sources:** all 167 preservation rows match by length and SHA-256.
- **Baseline:** all 39 `workspace-baseline.tsv` files match.
- **Old checkouts, fingerprinted with `GIT_OPTIONAL_LOCKS=0`** (HEAD, `status --porcelain=v1 -uall`, `for-each-ref`, stash list, worktree list, plus the SHA-256 of every file the status names):
  - `D:\Git\Librarian`: HEAD `38a037ea`, 943 entries, 679 hashed files.
  - `D:\Git\Librarian-rebuild`: HEAD `de3b8ebc`, 28 entries, 28 hashed files.
- No fetch and no maintenance ran in either old repository.
- **Evidence:** `evidence/preflight-before.txt`, `evidence/fingerprint-before.json`.
- **Note:** reads in earlier sessions, before this pack, ran `git status` on the old repositories without `GIT_OPTIONAL_LOCKS=0`. Those can refresh stat data in `.git/index`. They change no file and no status output.

## #02 The preservation helper: built and tested

`preserve_copy.py` (sha256 `cbbe1993a1c502c34d86a3c3dc82539f6cec53f62d8d4da7a4fb15bc62a8c478`) checks the whole batch before its first write:
- **Sources:** pinned length and SHA-256, inside a named root, regular files, no link or reparse point on the path.
- **Destination repository:** its own top level, `.git` a plain directory, no alternates or `commondir`, the expected full HEAD.
- **No alias:** neither a source root nor the destination sits inside the other.
- **Destination paths:** relative and `/`-only, unique ignoring case, spelled the way any existing entry is spelled. No `..`, drive letter, stream, reserved name, trailing dot or space, `.git`, forbidden character, or reparse point.
- **Each destination is one of:** absent; already the exact bytes; or listed as an allowed replacement and clean in HEAD, index and worktree.
- **Index and worktree:** no change except batch destinations already at their exact bytes.

**How it writes:**
1. It copies the source bytes into a staging folder and checks them again.
2. It re-checks every destination condition.
3. It writes the journal.
4. It installs each file through a temp file, flush and replace, then verifies the file and marks it in the journal.
5. Success is reported only when every row is installed and verified.

An interruption leaves the journal incomplete. Only `--resume`, with the same rows, HEAD and destination, continues it. All-files atomicity is not promised, and nothing is cleaned up. `--stage` stages exactly the manifest destinations, with literal pathspecs.

**Tests:** `python -B test_preserve_copy.py -v` (sha256 `2935f0ef…`), run on Windows with Python 3.14. **20 run: 19 pass, 1 skipped.** Output: `evidence/test-output.txt`.

- **Passed, success cases:** new file; identical retry; allowed clean-base replacement; staging only the listed paths.
- **Passed, refusals of destination state:** tracked file not allowed; dirty tracked file; conflicting untracked file; staged conflict; unrelated untracked file; wrong HEAD; alternates (shared objects).
- **Passed, refusals of sources and names:** changed source; duplicate destination and case collision, including a different-case existing directory; 11 bad names (`..`, `C:/`, absolute, backslash, stream, `CON.txt`, `lpt1`, trailing dot, trailing space, `.git/`, `?`); source outside its root; source and destination alias; junction escape (and nothing was written through it).
- **Passed, batch and recovery:** an invalid late row leaves every earlier destination unchanged and writes no journal; a simulated interruption after 2 of 4 installs exits 2, never reports success, and leaves the journal `installing` 2/4; a rerun without `--resume` refuses; a resume with other rows refuses; the resume with the same rows completes 4/4.
- **Skipped, not passed:** a source given as a symlink. Windows refused to create the symlink (WinError 1314: privilege not held). Reparse handling is still covered by the junction test.

**One test fault on the first run, mine:** the interruption test overwrote its own manifest file before resuming, so the tool's refusal ("other rows") was correct. The test was fixed and the whole suite re-run.

The drafts in `inputs/claude-pass02` (`preserve.py`, `import.py`) were not run in copy mode, as the pack required.

## #03 Archive only the pinned rows: pass, after F1

**Setup.**
- Three independent HTTPS clones: `labs/bootstrap-preservation-pass01/clones/{librarian-worktree,rebuild-worktree,lib-build-bootstrap}`. No local shared-object clone, and no worktree.
- Both baseline commits verified present by full id in each clone.
- No `archive/*` refs existed on the remote beforehand.

**Copying.**
- **Allowed replacements:** only for the librarian-worktree branch, and exactly 8. Those are the destination rows already tracked in `14676ca`, which are the 8 files modified in that worktree: solo `journal`, `menu`, `nav`, `page`, `reader` and `slot.py`; solo `00.md`; `0601.face/05.01.md`. The lists are in `evidence/allow-replace-*.txt`. The other two branches allowed none.
- **Copy results:**
  - librarian-worktree: 90 rows (82 new, 8 replaced)
  - rebuild-worktree: 28 new
  - lib-build-bootstrap: 49 new
- In each clone exactly those paths were staged, with nothing else in the index or worktree.

**Evidence on each branch, `archive-evidence/`:**
- 12 files: the pinned manifest, the tool and its tests, `preflight.py`, `make_evidence.py`, the test output, the preflight, the allow-list, the copy output, the journal and the commit message.
- `HASHES.tsv`, listing every other evidence file by SHA-256 and length.
- These were installed by the same helper from a pinned evidence manifest, as a separate commit.

**Commits** carry a `Model: claude-opus-5-5` line and the co-author trailer. Git's author is the machine's configured name (Mathias); the `Model:` line identifies the executor.

## #04 Independent verification: pass

**First verification failed.** `clones/verify` found 29 files whose stored bytes differed (`evidence/verify-remote-first-FAIL.txt`). That's F1.

**F1, the line-ending defect.**
- **Cause:** the repository's `.gitattributes` begins `* text=auto eol=lf` and lists byte-exact files as `-text`, and Git for Windows sets `core.autocrlf=true` system-wide. So CRLF files were stored with LF.
- **Files affected:** 4, 17 and 4 preserved rows, plus 4 evidence files on each branch.
- **The working copies were always exact**, and so were the helper's checks of the installed file. The defect is that the helper verified the installed file, not the stored blob.
- **The fix**, in each clone:
  1. A local, uncommitted `.git/info/attributes` holding `* -text`.
  2. `git add --renormalize` on exactly the manifest and evidence paths (`evidence/paths-*.txt`). That restaged 4, 21 and 4 files.
  3. Each staged blob checked against the file.
  4. A third commit on each branch, pushed as a fast-forward.
- **What wasn't changed:** `.gitattributes` on any branch. Pack A forbids staging inherited files.

**Second verification, from `clones/verify2`, a new clone** (`verify_remote.py`, sha256 `3d3eebf7…`; output `evidence/verify-remote.txt`), **PASS:**
- Every remote ref equals its expected commit, three commits on its base.
- Every row matches by destination, length and SHA-256: 90 + 28 + 49 = 167.
- All 12 evidence files plus `HASHES.tsv` match on each branch.
- Each branch changes no path beyond its manifest and its evidence.
- Both tags point at the baselines.

**Old workspaces, before and final** (`evidence/compare-final.txt`): **unchanged.** HEAD, status, refs, stash list, worktree list and all 707 hashed status files are identical. The 167 sources and 39 baseline files still match, so no concurrent drift was detected.

## Journals

`labs/bootstrap-preservation-pass01/evidence/journals/`: every journal is `complete` with all rows installed.

| Branch | Rows | Evidence |
|---|---|---|
| librarian-worktree | 90/90 | 13/13 |
| rebuild-worktree | 28/28 | 13/13 |
| lib-build-bootstrap | 49/49 | 13/13 |

The staging folders (`*.stage`) are kept as evidence.

## Held zip

`D:\Git\Librarian\10.workshop.zip`: 3,038,941 bytes, sha256 `f163fcbd914f39371629f0edc5ffcf2d5f22994eb58d91ff7cdd9217f7c72ff0`. It's untracked, and it was left in place. It was not archived, copied or discarded. Custody stays with the Director (`inputs/claude-pass02/preservation-held.tsv`).

## New paths in lib-build

All of these are in `D:\Git\lib-build\labs\bootstrap-preservation-pass01\`:
- **Code:** `preflight.py`, `preserve_copy.py`, `test_preserve_copy.py`, `make_evidence.py`, `verify_remote.py`.
- **Evidence:** `evidence/`, with stdout and stderr for every step in separate files.
- **Scratch:** `evidence-out/`, the per-branch evidence staging.
- **Test scratch:** `tests-tmp/`, the repositories from the last test run, kept.
- **Clones:** `clones/`, five independent clones, 93 MB.
- **This return:** `D:\Git\lib-build\returns\pack-A-preserve-return.md`.

## Findings for Prime

1. **F1 matters for Pack B.**
   - Any import into a clone of this repository passes through `* text=auto eol=lf`.
   - The kernel books include files listed `-text` precisely to stay byte-exact.
   - Pack B's import has to check stored blobs (`git cat-file`), not only written files.
   - It also has to choose, by a Director-visible rule, between the repository's `-text` convention (editing `.gitattributes`) and local attributes.
   - Recommended: the helper gains a check that "the stored blob equals the bytes" whenever it stages.
2. **The return location disagrees.** The pack says `notes/returns/`; the Director says `lib-build/returns/`. This return used the latter.
3. **Clones inside the lab.** `clones/` holds five full repositories inside `D:\Git\lib-build\labs\`. If Pack B turns `lib-build` into a repository, these become nested repositories. Exclude them or remove them deliberately; this pack did neither.
4. **The tool on the branches predates F1.** `archive-evidence/tool/` holds the helper exactly as it ran. The fix was a procedure, not a code change. `verify_remote.py` isn't on the branches; it's only in the lab.
5. **Author identity.** Every commit's git author is the configured machine identity. Only the `Model:` line distinguishes executors, which is the same limit Worldcraft sync recorded.

One thing I'd have done differently: I'd have made the helper compare the stored blob before the first commit. That would have caught F1 before anything was pushed.
