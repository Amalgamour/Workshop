# Kernel trial 9 (TRIAL-K9): hostile pass on kernel pass 10, the Q61 history walk, the Q62 face 00 and books/ checks, and the published copies

Lane TRIAL-K9, 2026-11-11, about 5:25 PM CST (6:25 PM EST). I'm a fresh session that did not build these faces or this builder. Under R20 (`DIRECTOR-RULINGS.md:78-80`) that counts as a different view (`DIRECTOR-RULINGS.md:7-9`, R2).
I only report. Nothing in `kernel/` (except Q63-Q66 in `kernel/QUESTIONS.md`), `books/`, `crates/` or `app/` was changed, nothing was seated, nothing was pushed, merged or deleted. New questions are tagged `[TRIAL-K9]`.

**Target (HEAD `6d3a0e6`; the shared branch moved to `a718c91` during the trial, a WHY-GAPS commit that touches only 04 drafts and `books/`, not the builder):**
- A) the pass 10 guard (`72ae0a1`): Q61 (the history walk follows a link at `kernel`, absolute and climbing links by path tails, link chains, root links) and Q62 (a face 00 with seat records must be the bytes git holds; past seats are also read from every committed `books/` version); plus the 26 seats;
- B) no new faces to seat;
- C) portability: a `--no-local --single-branch` clone of `/workspace/workshop-build/publish`, a clone of GitHub `prima/build`, and the publish copy's hygiene.

**Judged against:** `DIRECTOR-RULINGS.md` R1-R22, `kernel/QUESTIONS.md` (Q61, Q62), `docs/BUILD-LOG.md` (pass 10 entry), `docs/trial/kernel-trial-8.md`, `kernel/build.mjs`, `kernel/build.test.mjs`.
**Rules used:** Q41 is applied, not held. Q51 is open, so no face 00 is judged for a seat.

## Summary

| Verdict | B (faces) |
|---|---|
| PASS | 0 |
| FAIL | 0 |
| HELD-7 (depends on an open question) | 0 |
| **total** | **0** (no face changed this pass) |

| Severity | Findings |
|---|---|
| blocker | 0 |
| major | 1 (finding 1: a made-up seat line in face 00 lets a real seat be un-seated with a record that names a fake blob; builds clean in a fresh clone) |
| minor | 4 (finding 2: the books/ history walk skips a book committed with the exec bit; finding 3: the history walk misses paths git quotes; finding 4: un-seat records alone do not make face 00 "carry seat records"; finding 5: the forged-trial and gitfile residues, unchanged) |

**PASS list, eligible for an R2 seat:** none this pass (no face changed).

**Plain words:** every link shape the pass 10 notes promise is now followed: a link at `kernel`, absolute links from another checkout, links that climb out and back in, links to the repo root, and chains up to 16 hops (longer chains stop the build, which is the safe side). Every face 00 trick under `--check` is refused. The 26 seats all check out, here, in the publish copy and on GitHub. I found one real hole and three small ones. The real one: if face 00 has an extra, made-up `seat-NN:` line anywhere (even in its prose), the un-seat check takes that line's blob as "the old seat", so a real seat can be pulled with a record that names a fake fingerprint, and the result passes in a fresh clone. The small ones: a book file saved with the "executable" flag is skipped by the new books/ history check; file paths with a quote, backslash or non-ASCII letter are invisible to the history walk; and an un-seat record that lives only in an uncommitted face 00 is trusted locally.

## TRIAL-K8 fixes: did they land?

| K8 # | Landed? | Evidence |
|---|---|---|
| 1 minor (history walk: H1 kernel link, H2 absolute link, H5 chain) | yes, with gaps | `historySeats` walks `-- kernel` (`build.mjs:400`), `linkTargets` walks every tail of an absolute or climbing link (`:385-391`), a link at a face 00 target carries the page (`:413`), up to 16 rounds (`:422`). My L-cases below: all shapes the notes name are caught. Gap: paths git C-quotes (finding 3). |
| 2 minor (face 00 from the working tree; books/ HEAD only) | yes, with gaps | `gitEntry` on face 00 when it carries seat records (`:551-557`); `priorSeats` reads every committed book version (`:454-473`). Q1-Q8 below all refused. Gaps: exec bit (finding 2), un-seat-only face 00 (finding 4). |
| 3 minor (forged docs-only trial; gitfile swap) | still open, as admitted | A1 used a forged docs-only trial to make its seat (`seats 27`); GF below rebuilt the gitfile swap (`seats 25`, write mode and `--check`). Not worse. |

## Checks run (real output)

`/tmp/k9/repo` is a fresh `git clone --no-local -b build` of the shared repo at `6d3a0e6` (full history). Each hostile copy is a fresh `--no-local` clone of it under `/tmp/k9/<name>`. `find kernel books docs -type l` is empty at `6d3a0e6`.

**`node kernel/build.mjs --check`** (`/tmp/k9/repo`): exit 0.
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

**`node kernel/build.test.mjs`** (`/tmp/k9/repo`): exit 0. 55 `ok` lines, then `all passed`. The pass 10 ones:
```
ok    Q61: a seat written while the whole kernel was a link, then removed, is found in history (K8 H1)
ok    Q61: a seat written through an absolute face 00 link, then removed, is found in history (K8 H2)
ok    Q61: a seat written through a link to a link, then removed, is found in history (K8 H5)
ok    Q62: a face 00 with seat records that git does not hold is refused (K8 H3 C2)
ok    Q62: --check refuses a face 00 with seat records that is staged but not committed
ok    Q62: an un-seat hidden by keeping face 00 out of git is found in the history of books/ (K8 H3 C3)
all passed
```

**`CARGO_TARGET_DIR=target/k9-trial cargo test --workspace --no-fail-fast`** (in `/tmp/k9/repo`): `exit 0`; 38 `test result:` lines, `411 passed; 0 failed; 2 ignored`, every line `test result: ok.`.

**26 seats, each seat blob equal to `git rev-parse HEAD:<path>`, each mode `100644`, each a regular file on disk equal to its HEAD blob** (read from the `seat-NN:` lines of the face 00 files at `6d3a0e6`):
```
OK 00.00.00.0051.05.01 c160a4da9947eeeb3de88b512208ee9e7836011b 100644 | kernel-trial-5.md blob 86eb3a58e028d9b23e0a94cd4577329195300f99
OK 00.00.00.0051.05.02 7dbf70bd22af1bf0354edd82aff3ddb405ef892d 100644 | kernel-trial-4.md blob a5d253d5e12722956afea38e79cb7fc1cf492c7b
OK 00.00.00.0052.01 88bce491bb2bffe645a5c6825096f41d8b86080f 100644 | kernel-trial-5.md blob 86eb3a58e028d9b23e0a94cd4577329195300f99
OK 00.00.00.0052.04 e9ca59a1d708acfd57b9e5f7e6b758e41e4fde6f 100644 | kernel-trial-5.md blob 86eb3a58e028d9b23e0a94cd4577329195300f99
OK 00.00.00.0052.05.01 7993b14b830d12feb5a54509b41e74c931afe334 100644 | kernel-trial-4.md blob a5d253d5e12722956afea38e79cb7fc1cf492c7b
OK 00.00.00.0052.05.02 c82b1fc6d2d3d6ce6e5a44cf99cbc7bf93b62332 100644 | kernel-trial-4.md blob a5d253d5e12722956afea38e79cb7fc1cf492c7b
OK 00.00.00.0053.05.01 77ee148ffd645b15b4aeeb1401ff6b72e05a35da 100644 | kernel-trial-4.md blob a5d253d5e12722956afea38e79cb7fc1cf492c7b
OK 00.00.00.0053.05.02 8499872db0d7551309befdbf12ce1d1c7fa821c4 100644 | kernel-trial-4.md blob a5d253d5e12722956afea38e79cb7fc1cf492c7b
OK 00.00.00.0054.05.01 aa07b61116572c9e25353a5e7f3b6ed97941d2a0 100644 | kernel-trial-5.md blob 86eb3a58e028d9b23e0a94cd4577329195300f99
OK 00.00.00.0054.05.02 2bf1da6ff8c4bd77943150da2786f07d93fe824d 100644 | kernel-trial-6.md blob ca9c0b8f993a1061c97a4a12735f2e0f1b360a0e
OK 00.00.00.0055.05.01 6582d3e56495ca93203e81871659da0481550d41 100644 | kernel-trial-4.md blob a5d253d5e12722956afea38e79cb7fc1cf492c7b
OK 00.00.00.0055.05.02 596aa9ba0befffa6f9f6ca93364b9a6fea426478 100644 | kernel-trial-4.md blob a5d253d5e12722956afea38e79cb7fc1cf492c7b
OK 00.00.00.0056.01 112c169ccd06d54c6d9ab607fee6c2d16004cc62 100644 | kernel-trial-2.md blob da5d51424fee3bea1d8443c619fcba3c534a1ace
OK 00.00.00.0056.05.01 0914ebb8274c3e049440e11388b69da2b138f447 100644 | kernel-trial-4.md blob a5d253d5e12722956afea38e79cb7fc1cf492c7b
OK 00.00.00.0056.05.02 93178adddeb2ec915a2c5d4cc070d0dc50c03d37 100644 | kernel-trial-4.md blob a5d253d5e12722956afea38e79cb7fc1cf492c7b
OK 00.00.00.0057.05.01 67b3b9b6762af70a7494893fb7ff47e4e86e4281 100644 | kernel-trial-4.md blob a5d253d5e12722956afea38e79cb7fc1cf492c7b
OK 00.00.00.0057.05.02 037eec2ff5e9c6c18020f06679358a13e9a62bb1 100644 | kernel-trial-4.md blob a5d253d5e12722956afea38e79cb7fc1cf492c7b
OK 00.00.axioms.05.01 cbf5cba0d5429e2e0b14e56f5ed8a1eba1d06ad2 100644 | kernel-trial-5.md blob 86eb3a58e028d9b23e0a94cd4577329195300f99
OK 00.00.axioms.05.02 452be16b0536002a12279c5d485c68c5217fa6c8 100644 | kernel-trial-4.md blob a5d253d5e12722956afea38e79cb7fc1cf492c7b
OK 10.11.21.0012.05.01 9aaed75fc8f0594a1289fa83e870a474d4d021d2 100644 | kernel-trial-4.md blob a5d253d5e12722956afea38e79cb7fc1cf492c7b
OK 10.11.21.0012.05.02 dd89a5199d1a0b47f5cac3bce2ec0e8185ff1ce6 100644 | kernel-trial-5.md blob 86eb3a58e028d9b23e0a94cd4577329195300f99
OK 10.11.21.0013.05.01 16146a0fa073fc947138de43033f9e9a2b75ac09 100644 | kernel-trial-5.md blob 86eb3a58e028d9b23e0a94cd4577329195300f99
OK 10.11.21.0013.05.02 24a27e08bfb78ff75b1f7a2b91e82e2956a1163f 100644 | kernel-trial-7.md blob 377929b55738cb2477f4f3c3e88e484ae0031e22
OK 10.11.21.1001.01 5415cef2dd0a37f3c2ba4c9b6d2652262f0ef82d 100644 | kernel-trial-2.md blob da5d51424fee3bea1d8443c619fcba3c534a1ace
OK 10.11.21.1001.05.01 566071064f63a5c85fcb3bd87d9e375717bdbf51 100644 | kernel-trial-4.md blob a5d253d5e12722956afea38e79cb7fc1cf492c7b
OK 10.11.21.1001.05.02 2aa3490239620604ce1bb13c34841a60ac8f7056 100644 | kernel-trial-4.md blob a5d253d5e12722956afea38e79cb7fc1cf492c7b
```
26 of 26 OK.

### Part C: portability (real output)

**C1. `git clone -q --no-local --single-branch -b build /workspace/workshop-build/publish /tmp/k9/pub`:**
```
c910c68 WHY-GAPS: fill 15 of 22 grade A why lines in 04 drafts ... (publish HEAD; parent 0d4321e)
0d4321e KERNEL pass 10: BUILD-LOG entry and QUESTIONS Q61, Q62 decided (72ae0a1; ...)
4b369fa absent
8d29a0a absent
72ae0a1 absent
6d3a0e6 absent
git log --oneline --all -- target | wc -l: 0
0d4321e^{tree} 824fd37da9ff18d38ef3a0142ed3e5d8ce5dd078 = local 6d3a0e6^{tree} 824fd37da9ff18d38ef3a0142ed3e5d8ce5dd078
--check at c910c68: exit 0, "seats 26", "44 findings, 0 errors"
--check at 0d4321e: "seats 26", "59 findings, 0 errors"
node kernel/build.test.mjs: exit 0, 55 ok, "all passed"
```
HEAD is `c910c68`, later than `0d4321e` (the WHY-GAPS lane published since). 26 seats, 0 errors at both.

**C2. `git clone -q --single-branch -b prima/build https://github.com/Amalgamour/Workshop.git /tmp/k9/gh`:**
```
c910c68 WHY-GAPS: fill 15 of 22 grade A why lines in 04 drafts ...
0d4321e KERNEL pass 10: BUILD-LOG entry and QUESTIONS Q61, Q62 decided ...
HEAD c910c68bd284a59d9e180c0182328bd11c084533
4b369fa absent; 8d29a0a absent; 72ae0a1 absent; 6d3a0e6 absent
git log --oneline -- target | wc -l: 0
0d4321e^{tree} 824fd37da9ff18d38ef3a0142ed3e5d8ce5dd078
--check: exit 0, "seats 26", "44 findings, 0 errors"
node kernel/build.test.mjs: exit 0, 55 ok, "all passed"
```
GitHub has two branches: `claude` (`bcaaee8`, default HEAD) and `prima/build` (`c910c68`).

**C3. Publish copy hygiene (read only):**
```
branches: build (c910c68), remotes/origin/prima/build (c910c68)
refs/original: 0
remote.origin.push (only entry): refs/heads/build:refs/heads/prima/build
remote.origin.fetch: +refs/heads/prima/build:refs/remotes/origin/prima/build
.git/FETCH_HEAD: absent
rev-list --all -- target: 0      rev-list --all --reflog -- target: 2
```
- No `incoming` ref, a bare push goes only to `prima/build`, no `refs/original`. Yes to all three.
- Report only: the reflog still reaches 2 commits that touch `target/` (as in K8; `FETCH_HEAD` is now gone). Not a ref; `--all` and `--mirror` do not push it.

### Hostile tests (part A, scratch clones only)

Link cases (L-*): plumbing commits on a fresh clone. C1 adds the link(s) and a regular copy of page 1001's face 00 at the final target; C2 adds `seat-05.03: ... blob: 2222...` to that copy; C3 puts HEAD's tree back with no record. Script: `/tmp/k9/links.mjs`.

| # | Hostile change | Result |
|---|---|---|
| L-control | face 00 -> `../../../docs/x/f00.md` | caught: "10.11.21.1001.05.03 was seated ... write unseat-05.03" |
| L-absnoexist | face 00 -> `/nonexistent/other/checkout/docs/y/f00.md` (a link made in another checkout) | caught (path tails) |
| L-climbin, L-climbin2 | `../../../../repo-elsewhere/../repo/docs/z/f00.md`; `../../../../L-climbin2/docs/z/f00.md` (out of the repo and back in by its own folder name) | caught, both |
| L-rootlink | `kernel/samples/10.11.21/rt` -> `../../..` (the repo root); seat in `docs/r/10.11.21.1001.00.draft.md` | caught |
| L-trailing | `../../../docs/t//./f00.md/` | caught |
| L-space | target `docs/s x/f00.md` | caught |
| L-hops3 | face 00 -> `docs/h1` -> `h2` -> `h3` -> `h/f00.md` | caught |
| L-hops17 | a 19-link chain (17 middle hops) | fails closed: "kernel: git log could not read the history of seat lines, so un-seats cannot be checked" (the round limit; message is misleading, observation) |
| L-hops20abs | a 22-link chain of absolute links | fails closed, same message |
| **L-quote** | **target `docs/q"x/f00.md`** | **missed**: exit 0, `seats 26` (finding 3) |
| **L-backslash** | **target `docs/b\x/f00.md`** | **missed**: exit 0, `seats 26` (finding 3) |
| **L-nonascii** | **target `docs/<e-acute>/f00.md` (U+00E9 in the name)** | **missed**: exit 0, `seats 26` (finding 3) |
| **L-dirlink_kq** | **`kernel/samples/sx` -> `../../docs/k"q` (a folder link), seat in `docs/k"q/10.11.21.1001.00.draft.md`** | **missed**: exit 0, `seats 26` (finding 3) |
| L-windows | face 00 -> `..\..\..\docs\w\f00.md` (Windows separators) | not followed: exit 0. On Linux that text names a file with backslashes in its name, not `docs/w/f00.md`, so the walk matches the OS. Only a Windows checkout would read it as a path (observation) |
| L-winabs | face 00 -> `C:\other\docs\w2\f00.md` | not followed, same reason (observation) |
| SM | gitlink (160000) at `kernel/samples/sub`, then removed | at HEAD: refused ("sub: container has no door page 0000"); after removal: exit 0, `seats 26`. A submodule's files are another repo's objects, so nothing to follow (admitted in Q61; not worse) |
| LF | `git config log.follow true` in the clone | no effect: `--check` exit 0, same row counts for `books` (49) and `kernel` (437) |
| Q1 | 0013 face 00 `git rm --cached`, committed, file kept on disk | refused: "face 00 ... is not in git (untracked; not at HEAD)" |
| Q2 | the same, plus `.git/info/exclude` | refused, same message |
| Q3 | face 00 edited, not staged, `--check` | refused: "is blob 00172ac1... in git (HEAD), not the bytes on disk 32de6525..." |
| Q4 | face 00 edited and staged, books built in write mode, `--check` | refused, same message |
| Q5 | face 00 = HEAD, seated `0013.05.02.md` dirty | refused: "seated face changed since its trial" |
| Q6 | face 00 = HEAD, `books/10.11.21.book` dirty | `differs: .../books/10.11.21.book`, exit 1 |
| Q7 | index holds an edited face 00, working tree = HEAD | `--check` exit 0 (it checks HEAD, which is right); write mode refuses: "is blob 32de6525... in git (index), not the bytes on disk" |
| Q8 | `skip-worktree` on face 00, then edit it | refused: "is blob ... in git (HEAD), not the bytes on disk" |
| **Q9** | **page 0012: both seated 05s renamed to drafts, `unseat-05.01/02:` written in face 00 but face 00 left uncommitted; faces and books committed** | **local `--check` exit 0, `seats 24`.** Fresh clone of that commit: 3 errors (registry mismatch and both "was seated ... write unseat") (finding 4) |
| A1 (644) | forged docs-only trial passes `0013.01`; face 00 with `seat-01:` staged only for the write build (`seats 27`); face 00 unstaged; only `books/10.11.21.book` committed (100644). Then books put back without the seat and committed | caught: "10.11.21.0013.01 was seated ... write unseat-01: ... was blob bc8cfc48..." |
| **A1 (755)** | **the same, with `chmod +x books/10.11.21.book` before the commit (mode 100755)** | **missed**: `--check` exit 0, `seats 26`, also in a fresh clone (`/tmp/k9/a755c`; `git log --raw` shows `:100644 100755 4c8ffec cd84543 M books/10.11.21.book`) (finding 2) |
| AT | A1 (644) with committed `.gitattributes` `books/** binary -diff -text` and `*.book filter=hide diff=hide` (textconv `sed d`), plus `.git/info/attributes` `books/** -diff` | caught: attributes and textconv hide nothing |
| D1 | a made-up `seat-05.02: ... blob: 2c338d1d...` line in 0013 face 00's front matter (committed; `--check` exit 0, `seats 26`, no warning), then 05.02 un-seated with `unseat-05.02: pulled back for review; was blob 2c338d1d...` | **accepted**: `--check` exit 0, `seats 25`. The record names the fake blob, not the real `24a27e08...` (finding 1) |
| **D2** | **one commit: un-seat `0013.05.02` with `unseat-05.02: ...; was blob 2c338d1d...` and one prose line `seat-05.02: approved-by: build-stage (R2); trial: none; blob: 2c338d1d...` at the end of face 00's body; then books rebuilt and committed** | **accepted**: `--check` exit 0, `seats 25`, **also in a fresh clone** (`/tmp/k9/dec2c`). Before the commit, write mode asked for the real blob (`24a27e08...`); once the decoy is committed it is the "newest seat" (finding 1) |
| GF | `.git` replaced by a gitfile to a made-up history (base tree; every trial at its first-added blob, docs-only; trial edits; then the un-seated tree and books) | **accepted**: write mode and `--check` exit 0, `seats 25`. The real `.git` still shows the un-seat as changes. Known residue (finding 5) |

Not repeated: prefix-collision forges, shallow clones, replace refs, grafts, `GIT_*` env, merges and root commits (covered by passing tests in three clones).

## Findings

### 1. major: a made-up seat line in face 00 sets the blob an un-seat record must name
- **Evidence:**
  - `historySeats` scans every line of every face 00 blob with `SEAT_HIST` (`build.mjs:353`, `:437-443`) and keeps the first match per address, newest blob first (`:442`). It does not care where in the file the line is: the front matter, the registry, or the prose.
  - The live parser reads seats only from the registry fields (`registry`, `seatOf`), and nothing flags a `seat-NN:` line for a face that is not seated, or a `seat-NN:` line outside the registry.
  - `priorSeats` adds a `books/` seat only when history has none for that address (`!hist.has(e.addr)`, `:472`), so the real blob in the books history (`face blob 24a27e08...`) is never compared.
  - D2: in one commit, `0013.05.02` (a real seat, trial `kernel-trial-7.md`) is pulled back with `unseat-05.02: pulled back for review; was blob 2c338d1d...` and one made-up prose line. Builds clean, `seats 25`, in a fresh clone too.
- **Breaks:** TRIAL-K5 finding 5 / Q54 d (the un-seat record names the full old blob) for any real, published seat, and R2's "every seat can be found and re-reviewed": a re-reviewer is pointed at a fingerprint that never existed. The real line is still in git history, so nothing is lost, but the guard no longer checks it.
- **Fix direction (builder lane, not done):** an un-seat record must name the blob of every past seat seen for that address (history and `books/` history), or at least the books one; read `seat-NN:` history lines only from the registry card's field block (and `seat-00:` only from the stamp); and refuse a `seat-NN:` line for a face that is not listed as seated. Raised in Q63.

### 2. minor: the books/ history walk skips a book committed with the exec bit
- **Evidence:** both the HEAD read and the history read of `books/` match only mode `100644` (`build.mjs:462`, `:464`). `--check` compares bytes only, so a book with mode `100755` builds fine. A1 (755): a seat recorded only in a `100755` book is pulled with no record, exit 0, `seats 26`, also in a fresh clone. A1 (644) is caught.
- **Limits:** the seat state itself needs face 00 kept out of git (staged only for the write build, then unstaged), so a fresh clone at that commit fails ("differs"); it never verified anywhere but locally. Same class as K8 finding 2.
- **Breaks:** the pass 10 claim (Q62 decision (2), BUILD-LOG pass 10) that "keeping face 00 out of git cannot hide an un-seat". One `chmod +x` does.
- **Fix direction:** accept any blob mode for book paths in both reads (or refuse a book that is not `100644` at HEAD or in history, as G4 does for seated faces). Raised in Q64.

### 3. minor: the history walk misses paths that git quotes
- **Evidence:** `git log --raw` without `-z` C-quotes a path with `"`, `\`, a control byte, or (with the default `core.quotePath`) any non-ASCII byte: `"docs/q\"x/f00.md"`. `historySeats` matches that quoted text against unquoted targets (`:404`, `:430-433`), so the file is never read. L-quote, L-backslash, L-nonascii and L-dirlink_kq: a seat line written and removed through a link to such a path leaves no trace; exit 0.
- **Limits:** every such state has a live link, which the live refusal stops, so no seat was ever valid there (as in K8 finding 1). A live, buildable face path never needs quoting (book folders and face names are fixed ASCII).
- **Breaks:** the Q61 decision "cover the shapes, not best-effort"; this shape is not in its "still not followed" list.
- **Fix direction:** run both history walks with `-z` (and split on NUL), or unquote; add a test with a quote in the target. Raised in Q65.

### 4. minor: an un-seat record alone does not make face 00 "carry seat records"
- **Evidence:** `carries` (`build.mjs:556`) is true for a seated face on the page, a `seat-*` field, or a stamp `seat-00:`. A face 00 whose page has no seats left but holds `unseat-*` records is read from disk with no git check. Q9: page 0012's two seats pulled, the records only in an uncommitted face 00: local `--check` exit 0, `seats 24`.
- **Limits:** local only; a fresh clone refuses it (3 errors). Same class as K8 finding 2 before pass 10.
- **Fix direction:** count `unseat-*` fields (and a stamp `unseat-00:`) in `carries`, or check every face 00 against git under `--check`. Raised in Q66.

### 5. minor (class, no verdict change): the forged-trial and gitfile residues are unchanged
- A1 made its seat with a brand-new forged trial in a docs-only commit (`seats 27`, 0 errors), as in K8 T13r.
- GF: a local gitfile swap to a made-up history still builds clean (`seats 25`), in write mode and under `--check`. A fresh clone of the real repo refuses it.
- Neither got worse.

**Observations (no severity):**
- **Hop limit:** a chain past 16 rounds fails closed, which is right, but the message says git "could not read the history", not that the link chain is too long.
- **Windows separators:** link text with backslashes is not read as a path. On Linux that matches what the OS does; a Windows checkout would differ. Report only.
- **Submodules:** unchanged and admitted (Q61). At HEAD a gitlink under `kernel/samples/` is refused only by chance (an empty book folder has no door page).
- **Shared branch moved:** `a718c91` (WHY-GAPS) landed on `build` during this trial. It does not touch `kernel/build.mjs` or any seated face; publish and GitHub at `c910c68` (its published copy) check clean with 26 seats.

## Per-face verdicts

None. No face changed in pass 10, and no face is eligible for a seat.

## Method
- **Repo state:** the shared working tree was only read. My only writes are this file and Q63-Q66 in `kernel/QUESTIONS.md`, committed by pathspec (the index was empty first). The builder was never run in the shared tree.
- **Scratch copies:**
  - `/tmp/k9/repo` (fresh `--no-local` clone at `6d3a0e6`, cargo target `target/k9-trial` inside it);
  - `/tmp/k9/<test>` (one fresh clone per attack; `/tmp/k9/links.mjs` for L-*, `/tmp/k9/seat01.sh` for A1, `/tmp/k9/fake` for GF);
  - `/tmp/k9/pub` (publish, `--no-local --single-branch`) and `/tmp/k9/gh` (GitHub `prima/build`).
- **Publish copy:** read only. Nothing fetched into it, deleted or pushed.
- **Blobs:** each is `git rev-parse HEAD:<path>` at `6d3a0e6`, written in full.
