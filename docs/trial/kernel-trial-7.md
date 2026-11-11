# Kernel trial 7 (TRIAL-K7): hostile pass on kernel pass 8, the history guard, and the published copies

Lane TRIAL-K7, 2026-11-11, about 4:35 PM CST (5:35 PM EST). I'm a fresh session that did not build these faces. Under R20 (`DIRECTOR-RULINGS.md:78-80`) that counts as a different view, so a PASS here can qualify a face for an R2 seat (`DIRECTOR-RULINGS.md:7-9`).
I only report. Nothing in `kernel/`, `books/`, `crates/` or `app/` was changed, nothing was seated, nothing was pushed or deleted. New questions go to `kernel/QUESTIONS.md` as Q58-Q60, tagged `[TRIAL-K7]`.

**Target (HEAD `2db15dd`):**
- A) the 2 draft faces pass 8 step 3 changed (`02e4c89`): `10.11.21.0013.05.02` and the note `00.00.00.0054.06.01`;
- B) the history guard (`ed694f6`, tests in `kernel/build.test.mjs`) and the 25 seats;
- C) portability: a `--no-local --single-branch` clone of `/workspace/workshop-build/publish` and a clone of GitHub `prima/build`, plus the hygiene of the publish copy after Prima's Q57 cleanup.

**Judged against:** `DIRECTOR-RULINGS.md` R1-R22, `docs/spec/face00.md` (DRAFT), `kernel/QUESTIONS.md`, `docs/BUILD-LOG.md` (pass 8 entry), `docs/trial/kernel-trial-6.md`, `kernel/build.mjs`, `kernel/build.test.mjs`.
**Rules used:** Q41 is applied, not held. Q55 (pack grants) is the Director's, so no pack fails only because its grant is narrow. Q35 (may a 06 note be seated) is open, so a note can PASS as a draft; it is not seatable, and the builder refuses to seat it (`SEATABLE_COUNTERS`, `build.mjs:42`).

## Summary

| Verdict | A (pass-8 faces) |
|---|---|
| PASS | 2 (1 pack eligible for an R2 seat, 1 note that passes as a draft) |
| FAIL | 0 |
| HELD-7 (depends on an open question) | 0 |
| **total** | **2** |

| Severity | Findings |
|---|---|
| blocker | 0 |
| major | 1 (finding 1: a symlinked face 00 or book folder hides later seats from the history check, also in clones) |
| minor | 3 |

**PASS list, eligible for an R2 seat** (full git blob at HEAD `2db15dd`; a seat must name this trial by path and blob and exactly this face blob; any byte change needs a new trial):
- `10.11.21.0013.05.02` (blob `24a27e08bfb78ff75b1f7a2b91e82e2956a1163f`)

**Notes that pass as drafts, not seatable while Q35 is open** (the builder refuses a seated 06 counter; blob for the record):
`00.00.00.0054.06.01` blob `1d2bcf01efb525ba6016fe8f415c9b68b0618a19`.

**Before seating, note:**
- `0013.05.02` is a face 05 counter, so `SEATABLE_COUNTERS` allows it. Its seat line goes in the `0013.00` registry as `seat-05.02:`, and `why-05.02:` goes away.
- `git rev-parse HEAD:kernel/samples/10.11.21/10.11.21.0013.05.02.draft.md` is `24a27e08bfb78ff75b1f7a2b91e82e2956a1163f`. Renaming `.draft.md` to `.md` does not change the blob.
- Finding 1 does not change any verdict and does not touch the 25 seats. No file under `kernel/`, `books/` or `docs/` is a symlink at `2db15dd` (`find kernel books docs -type l` is empty), and all 25 seats match `git rev-parse HEAD:<path>`.

## TRIAL-K6 fixes: did they land?

| K6 # | Landed? | Evidence |
|---|---|---|
| 1 major (attributes hide past seats) | yes | `HIST` (`build.mjs:184`) is `-a --no-textconv --no-ext-diff --full-history -m --no-abbrev --no-renames --no-color`. `historySeats` (`:302-324`) lists face 00 blobs with `--raw` and reads them with `git cat-file --batch` (`:286-301`). T01-T05 below: committed `.gitattributes` (`-diff`, `binary`, `-text`), `.git/info/attributes`, a textconv driver, `diff.external`, and odd log config all fail to hide an un-seat. |
| 2 minor (merges) | yes | T06 (merge from a side branch cut before `679d49e`, side parent first) and T07 (evil merge, main parent first) are both refused. Plain `git log -- <face 00>` shows only the side commit in T06, so the guard really needs `--full-history`, and has it. T09-T11: an edited copy of a real trial brought in by a merge, by delete-and-re-add, or by an unrelated orphan history is refused (T11 crashes, finding 2). |
| 3 minor (H4 forged trial residue) | still open, as admitted | T13: a brand-new forged trial in a docs-only commit still seats a face (`seats 26`, 0 errors). T12 is the same residue: rename a real trial to a new path while editing it. Not worse than K6 (finding 3 below). |
| 4 minor (0013 w03 order) | yes | `0013.05.02:43-44`: `depends: w01, w02`, `blocked-by: Q33, Q49 (through w01)`; the reason (`:42`) says why. |
| 5 minor (0054 note symbols) | yes | `0054.06.01:6` names `CARD_TYPES` only; that matches the pass 6 diff (`git show 18b9cfa`, `build.mjs:30-31` became `CARD_TYPES` on both 0054 counters). |
| K15 observation (gitfile swap) | still open, as admitted | T20 below. Local only; a fresh clone catches it. |
| Q57 (publish hygiene) | mostly | See C3: push is locked to `prima/build`, `refs/original` and the stale `origin/build` are gone, but `incoming` still reaches `target/` history (finding 4). |

## Checks run (real output)

`/tmp/k7/repo` is a fresh `git clone --no-local` of the shared repo at `2db15dd` (full history, branch `build`). Each hostile copy is a fresh clone of it under `/tmp/k7/h*` (helpers `/tmp/k7/lib.sh`).

**`node kernel/build.mjs --check`** (`/tmp/k7/repo`): exit 0.
```
finding  00.00.00.0057.02.draft.md: 04 why-questions: why missing (4.7)
... (59 findings, all "why missing (4.7)")
checked  books/00.00.00.book  50 entries
checked  books/00.00.axioms.jsonl  7 entries
checked  books/10.00.00.book  1 entries
checked  books/10.11.00.book  1 entries
checked  books/10.11.21.book  15 entries
seats 25
59 findings, 0 errors
```

**`node kernel/build.test.mjs`** (`/tmp/k7/repo`): exit 0. 40 `ok` lines, then `all passed`. The last five:
```
ok    Q54: a shallow clone is refused
ok    Q56 a: a committed .gitattributes kernel/** -diff does not hide an un-seat (K6 K21)
ok    Q56 a: .git/info/attributes kernel/** -diff does not hide an un-seat (K6 K22)
ok    Q56 b: a merge from a side branch cut before a seat does not hide an un-seat (K6 K26)
ok    Q56 c: a merge citing an edited copy of a real trial from the side branch is refused (K6 K25)
all passed
```

**`CARGO_TARGET_DIR=target/k7-trial cargo test --workspace --no-fail-fast`** (in `/tmp/k7/repo`): `exit=0`; 38 `test result:` lines, `411 passed; 0 failed; 2 ignored`, every line `test result: ok.`.

**25 seats, each blob equal to `git rev-parse HEAD:<path>`** (read from the `seat-NN:` lines of the face 00 files at `2db15dd`; none of the paths is a symlink):
```
OK 00.00.00.0051.05.01 c160a4da9947eeeb3de88b512208ee9e7836011b
OK 00.00.00.0051.05.02 7dbf70bd22af1bf0354edd82aff3ddb405ef892d
OK 00.00.00.0052.01 88bce491bb2bffe645a5c6825096f41d8b86080f
OK 00.00.00.0052.04 e9ca59a1d708acfd57b9e5f7e6b758e41e4fde6f
OK 00.00.00.0052.05.01 7993b14b830d12feb5a54509b41e74c931afe334
OK 00.00.00.0052.05.02 c82b1fc6d2d3d6ce6e5a44cf99cbc7bf93b62332
OK 00.00.00.0053.05.01 77ee148ffd645b15b4aeeb1401ff6b72e05a35da
OK 00.00.00.0053.05.02 8499872db0d7551309befdbf12ce1d1c7fa821c4
OK 00.00.00.0054.05.01 aa07b61116572c9e25353a5e7f3b6ed97941d2a0
OK 00.00.00.0054.05.02 2bf1da6ff8c4bd77943150da2786f07d93fe824d
OK 00.00.00.0055.05.01 6582d3e56495ca93203e81871659da0481550d41
OK 00.00.00.0055.05.02 596aa9ba0befffa6f9f6ca93364b9a6fea426478
OK 00.00.00.0056.01 112c169ccd06d54c6d9ab607fee6c2d16004cc62
OK 00.00.00.0056.05.01 0914ebb8274c3e049440e11388b69da2b138f447
OK 00.00.00.0056.05.02 93178adddeb2ec915a2c5d4cc070d0dc50c03d37
OK 00.00.00.0057.05.01 67b3b9b6762af70a7494893fb7ff47e4e86e4281
OK 00.00.00.0057.05.02 037eec2ff5e9c6c18020f06679358a13e9a62bb1
OK 00.00.axioms.05.01 cbf5cba0d5429e2e0b14e56f5ed8a1eba1d06ad2
OK 00.00.axioms.05.02 452be16b0536002a12279c5d485c68c5217fa6c8
OK 10.11.21.0012.05.01 9aaed75fc8f0594a1289fa83e870a474d4d021d2
OK 10.11.21.0012.05.02 dd89a5199d1a0b47f5cac3bce2ec0e8185ff1ce6
OK 10.11.21.0013.05.01 16146a0fa073fc947138de43033f9e9a2b75ac09
OK 10.11.21.1001.01 5415cef2dd0a37f3c2ba4c9b6d2652262f0ef82d
OK 10.11.21.1001.05.01 566071064f63a5c85fcb3bd87d9e375717bdbf51
OK 10.11.21.1001.05.02 2aa3490239620604ce1bb13c34841a60ac8f7056
```
25 of 25 OK. The new seat is `0054.05.02` at `2bf1da6f...`, citing `docs/trial/kernel-trial-6.md blob ca9c0b8f993a1061c97a4a12735f2e0f1b360a0e`, which is both the HEAD blob and the first-added blob of that file (`86aaa9d`).

### Part C: portability (real output)

**C1. `git clone -q --no-local --single-branch /workspace/workshop-build/publish /tmp/k7/pub`:**
```
a9b31c4 KERNEL pass 8: BUILD-LOG entry (ed694f6, 0beabc3, 02e4c89; 25 seats; checks pass in repo and
4b369fa absent
86aaa9d absent
ed82086 absent
0                          (commits touching target/)
false                      (is-shallow-repository)
check-exit=0
checked  books/10.11.21.book  15 entries
seats 25
59 findings, 0 errors
0                          (ERROR lines)
tests-exit=0
40                         (ok lines)
all passed
```

**C2. `git clone -q --single-branch -b prima/build https://github.com/Amalgamour/Workshop.git /tmp/k7/gh`** (read only):
```
a9b31c4 KERNEL pass 8: BUILD-LOG entry (ed694f6, 0beabc3, 02e4c89; 25 seats; checks pass in repo and
a9b31c41b5ca2e2f921dce46224b5b5b9f24c1c3
4b369fa absent
86aaa9d absent
ed82086 absent
0                          (commits touching target/)
check-exit=0
seats 25
59 findings, 0 errors
tests-exit=0
40
all passed
a9b31c41b5ca2e2f921dce46224b5b5b9f24c1c3   (publish clone HEAD)
trees identical                            (GitHub tree == publish tree)
tree == local 2db15dd
```
GitHub `prima/build` is the publish `build` HEAD, and its tree equals the local `2db15dd` tree.

**C3. Publish copy hygiene (`/workspace/workshop-build/publish`, read only: `git branch -vv`, `for-each-ref`, `config`, `push --dry-run`; nothing fetched into it, deleted or pushed):**
```
* build    a9b31c4 [origin/prima/build] KERNEL pass 8: BUILD-LOG entry ...
  incoming 2db15dd KERNEL pass 8: BUILD-LOG entry ...
refs/heads/build
refs/heads/incoming
refs/remotes/origin/prima/build
remote.origin.url https://github.com/Amalgamour/Workshop.git
remote.origin.fetch +refs/heads/prima/build:refs/remotes/origin/prima/build
remote.origin.push refs/heads/build:refs/heads/prima/build
branch.build.remote origin
branch.build.merge refs/heads/prima/build
git push --dry-run --porcelain:
To https://github.com/Amalgamour/Workshop.git
=	refs/heads/build:refs/heads/prima/build	[up to date]
Done
.git/refs/original: empty folder, no refs/original/* refs
commits on build touching target/: 0
538cfc6a... has target/ (and others), reachable from incoming
4b369fa, 86aaa9d: objects present in the publish object store (not on any pushed ref)
```
- A bare `git push` from `build` goes only to `prima/build`: `remote.origin.push` is an explicit `build:prima/build` refspec, and the dry run lists only that ref. Yes.
- `refs/original/*` is gone (the folder is empty). The stale `refs/remotes/origin/build` is gone. Yes.
- `refs/heads/incoming` (`2db15dd`, the local unfiltered history) is still there and still reaches the `target/` commits. A `git push --all`, `--mirror` or `git push origin incoming` would publish them. The Q57 note in QUESTIONS says "the leftover refs that held the original `target/` history were removed"; that is true for `refs/original` and `origin/build`, not for `incoming` (finding 4). `incoming` is needed by the cherry-pick flow, so this may be on purpose.

### Hostile seat tests (part B, scratch clones only)

Un-seat used in T00-T08, T21: `10.11.21.1001.05.02` renamed to `.draft.md`, its `seat-05.02:` line removed, a `why-05.02:` added, no `unseat-05.02:` record, and its `approved-by`/`trial` keys dropped from `books/10.11.21.book` so HEAD:books forgets it; committed; then the builder is run in write mode. A seat used in T09-T13: draft `10.11.21.0013.05.02` (`24a27e08...`) seated citing an edited copy of `kernel-trial-6.md` with an extra PASS line for it.

| # | Hostile change | Result |
|---|---|---|
| T00 | control: the un-seat alone, committed | refused: "10.11.21.1001.05.02 was seated (build-stage (R2)) in the last build but is not now; write unseat-05.02" |
| T01 | committed `.gitattributes` `kernel/** -diff`, then the un-seat | refused (same message) |
| T02 | committed `.gitattributes` `kernel/** binary` and `* -text` | refused (same) |
| T03 | `.git/info/attributes` `* -diff` and `* binary` (not committed) | refused (same) |
| T04 | `.git/info/attributes` `* diff=blank`, `diff.blank.textconv`, `diff.blank.binary true`, `diff.external true` | refused (same) |
| T05 | repo config `log.diffMerges off`, `color.ui always`, `diff.renames copies`, `core.abbrev 7` | refused (same); the 25 real seats still verify under that config |
| T06 | side branch from `679d49e^` (before the seat); side commits `kernel/` and `books/` as un-seated; merge commit with tree = the un-seated tree, parents (side, main) | refused (same). Plain `git log -1 -- <1001 face 00>` shows only `side copy`, so default simplification is blinded and `--full-history` is what catches it |
| T07 | evil merge: tree = un-seated, parents (main, an empty side commit) | refused (same) |
| T08 | rename the whole page 1001 to 1002 (with rename detection on by default) | refused: the old seats "do not name 10.11.21.1002.01 ..." and "10.11.21.1001.01 was seated ... write unseat-01" |
| T09 | edit the real `kernel-trial-6.md` in place in a docs-only commit; cite the new blob | refused: "was added at blob ca9c0b8f... (commit 86aaa9d1d0e1), not ea681e50..." |
| T10 | side branch from `86aaa9d^` adds the edited copy (docs-only), merged with `-X theirs`; cite the merged blob | refused: "added more than once on HEAD's full history with different blobs" (also for the real `0054.05.02` seat) |
| T11 | orphan branch adds the edited copy at the same path; merged with `--allow-unrelated-histories -X theirs` | refused, but by a crash: `TypeError: Cannot read properties of null (reading 'slice')` at `build.mjs:211` (finding 2). Exit 1, nothing written |
| T12 | `git rm` the real trial and add the edited copy as `kernel-trial-6b.md` in one docs-only commit; cite it | the `0013.05.02` seat is **accepted**; only `0054.05.02` errors, because its trial file is gone. The same residue as T13 |
| T13 | brand-new forged `kernel-trial-99.md` in a docs-only commit (K6 K07, H4) | **accepted**: exit 0, `seats 26`, `59 findings, 0 errors`. Known residue (finding 3) |
| T14 | shallow clone (`--depth 3`) | refused, every seat: "the repo is a shallow clone" |
| T15 | `git replace ca9c0b8f... <edited copy>` | refused, every seat: "the repo has replace refs (refs/replace/ca9c0b8f...)" |
| T16 | `.git/info/grafts` | refused, every seat: "the repo has a grafts file" |
| T17 | `GIT_DIR` and `GIT_WORK_TREE` pointing at a bare clone, `GIT_CONFIG_GLOBAL=/dev/null` | ignored; refused with the T00 message |
| **T18** | **commit 1: move `0013.00` to `docs/x/f00.md` and leave a symlink at `kernel/samples/10.11.21/10.11.21.0013.00.draft.md` (builds clean, `seats 25`). Commit 2: a docs-only trial passing `0013.05.02`. Commit 3: seat `0013.05.02` by editing `docs/x/f00.md` through the symlink (`seats 26`). Commit 4: un-seat it with no record, books line dropped. Commit 5: rebuilt books** | **accepted**: exit 0, `seats 25`, `59 findings, 0 errors`; `--check` exit 0. **Also exit 0 in a fresh `--no-local` clone** (`/tmp/k7/h14c`). The seat line is in history only under `docs/x/f00.md`, which the `-- kernel/` walk never reads (finding 1) |
| T18b | `kernel/samples/10.11.21` replaced by a symlink to `kernel/parked/10.11.21-real` (a folder `historySeats` skips, `build.mjs:310`) | builds clean, `seats 25`; every later seat line in that book would sit under `/parked/` and be skipped (finding 1) |
| T18c | the seated `1001.05.02.md` replaced by a symlink to an untracked file with the same bytes | builds clean, `seats 25`, though `git rev-parse HEAD:<path>` is now `a20da385...` (the link text), not the seat blob (finding 1) |
| T19 | `.git/objects/info/alternates`: not repeated (K6 K14 refused it; objects alone add no history) | - |
| T20 | `.git` replaced by a gitfile `gitdir: /tmp/k7/evil/.git`, where `evil` is a new history (empty root, the two TRIAL-K2 face blobs, every trial at its first-added blob in a docs-only commit, then the un-seated tree) | **accepted**: exit 0, `seats 24`, `--check` exit 0. Putting the real `.git` back: refused (T00 message). Known residue (K6 K15), not worse |

Not repeated by hand: a prefix-collision forge (`verifySeat` compares full blobs; the test "R2: a prefix-collision forge of a seated face is refused (K4 HM)" passes in all three clones).

## Findings

### 1. major: a symlink moves a page's seat lines out of the history check's sight
- **Evidence:**
  - The builder reads face files with `readdirSync` and `readFileSync` (`build.mjs:101`), and book folders with `statSync(...).isDirectory()` (`:93`). Both follow symlinks, and nothing checks for one.
  - `historySeats` (`:302-324`) reads only face 00 blobs committed under `kernel/` (`-- kernel/`, `:305`) and skips any path with `/parked/` (`:310`). A symlinked face 00 is committed as a link (mode 120000), so its blob is the link text, with no seat lines.
  - T18: with `0013.00` a symlink to `docs/x/f00.md`, a seat added and later removed through the link leaves no trace the guard reads. The un-seat with no record builds clean, also in a fresh clone, so it would pass in the published copy and on GitHub.
  - T18b does the same for a whole book (a symlinked folder into `kernel/parked/`). T18c shows a seated face whose bytes are not in git at all (a link to an untracked file); the seat blob no longer equals `git rev-parse HEAD:<path>`.
- **Limits:** it hides only seats made after the link exists. The 25 seats at `2db15dd` are in `kernel/` history as regular files and stay protected. The link commit and the seat lines under `docs/x/` stay in git history, so a person can find them. There are no symlinks in the repo today.
- **Breaks:** R2 (`:9`): "every such seat can be found and re-reviewed later", and the pass 8 claim (`BUILD-LOG.md`, step 1) that the walk sees "every face 00 blob ever committed under kernel/". This is the K6 finding 1 class again: one harmless-looking change, surviving clones.
- **Fix direction (builder lane, not done):**
  - Refuse a symlink anywhere under the sources: `lstatSync` on each book folder and face file, or check `git ls-tree HEAD` mode `100644` for every face that is committed.
  - For each seated face, also check that `git rev-parse HEAD:<path>` equals the seat blob, so the seated bytes are the committed bytes.
  - Add tests like T18, T18b and T18c.
- Raised in Q58.

### 2. minor: a root commit's header line is not parsed, so an orphan history crashes the builder
- **Evidence:** `trialOrigin` formats each commit as `C %H %P` (`:200`). For a root commit `%P` is empty, so the line is `C <sha> ` with a trailing space, and the regex `^C ([0-9a-f]{40})((?: [0-9a-f]{40})*)$` (`:205`) does not match. The add is then filed under the commit parsed before it, or under `null`. T11 (an orphan branch that adds an edited trial, merged in) crashes at `:211` with `TypeError: Cannot read properties of null (reading 'slice')`.
- **Limits:** it fails closed (exit 1, nothing written), and the branch has one root today. A misfiled add could make the touch rule (`:215-219`) look at the wrong commit, but the forged-trial residue (finding 3) is already easier.
- **Fix direction:** allow trailing space (`\s*$`) or `trim()` the line, and give a clear error, not a stack trace. Add a test like T11. Raised in Q59.

### 3. minor (class, no verdict change): the H4 and gitfile residues are unchanged
- T13 shows a brand-new forged trial in a docs-only commit still seats a face (K6 K07). T12 is the same thing done by renaming a real trial while editing it.
- T20 shows a local `.git` gitfile swap to a made-up history still builds clean (K6 K15). A fresh clone of the real repo refuses it.
- Neither got worse. They are listed so the count is complete.

### 4. minor (report only): the publish copy's `incoming` branch still holds the `target/` history
- See C3. A bare push is safe, but `incoming` (`2db15dd`) reaches commits that touch `target/`, so `--all`, `--mirror` or a push of `incoming` would publish them. The Q57 note says the leftover refs "were removed"; two of three were. Raised in Q60. Nothing was changed.

**Observations (no severity):**
- **`depends: the trial step`:** every 05.02 pack's seat card (`0013.05.02:63`, and the 8 seated packs) names its dependency in words, not by card id (`w04`). It is the house style and was passed before, so it is not counted.
- **Commit order in `historySeats`:** "newest seat" (`:321`) is the first one in `git log` order, which follows commit dates across merges. A merge with skewed dates could make an older seat blob the one an `unseat-NN:` record must name. Not tried; the branch is linear.

## Per-face verdicts

| Face | Blob (HEAD `2db15dd`) | Verdict | Findings / open question |
|---|---|---|---|
| `10.11.21.0013.05.02` | `24a27e08bfb78ff75b1f7a2b91e82e2956a1163f` | PASS | K6 finding 4 landed: w03 `depends: w01, w02`, `blocked-by: Q33, Q49 (through w01)` (`:43-44`), and the reason says why (`:42`). Every outcome part has a card: number and fields w01, `/ask` w02, app w03, seated question cards w04/w05. Order is fix, test, trial, seat, and the depends match it. Every done can be decided. Cites checked: `DESIGN.md` section 7 at `:168`; DECISIONS-INDEX D89 (unresolved goes to the user); DECISIONS-LOG D147, D267, D271, D290 (all on common questions / 0013); MAP hole 15 (`MAP.md:105`); CONFLICTS D14; Q33, Q49, O18 exist; `store.rs:50`, `ask/page.tsx:14`, `AskBox.tsx:104`, `askq.rs:16` `face_text` are true; `1001.01` blob `5415cef2...` is seated and matches. The grant is Q55, not counted. |
| `00.00.00.0054.06.01` | `1d2bcf01efb525ba6016fe8f415c9b68b0618a19` | PASS (draft; not seatable, Q35) | K6 finding 5 landed: the pass 6 line names `CARD_TYPES` only, matching `git show 18b9cfa` (the `build.mjs:30-31` cites on 0054.05.01 and 05.02 became `CARD_TYPES`; the `face.rs:99-111` line cites were not in K4 finding 12's scope). The pass 8 line is true: `0054.00:12` seats 05.02 at `2bf1da6ff8c4bd77943150da2786f07d93fe824d` citing `docs/trial/kernel-trial-6.md blob ca9c0b8f993a1061c97a4a12735f2e0f1b360a0e`, both equal to `git rev-parse HEAD:<path>`; the reason (AXIOMS, AXIOMS_FILE are on `00.00.axioms.05.01`) is true. The pass 7 line is unchanged and still true. |

**What a PASS on a 05.02 pack checked** (as TRIAL-K4 to K6):
- Every header field is present.
- Every work card has `reason`, `depends`, `blocked-by`, a decidable `done:`, and a `path`.
- The order is fix, then fill, then trial, then seat, and the dependencies match it.
- Every part of the `outcome:` has a card.
- `design:` names a real DESIGN.md section and real DECISIONS ids on the topic.
- No card seats its own work, uses an override (R21), or answers an open Director question.
- Every code or line cite was opened at `2db15dd`.

**What a PASS on a 06.01 note checked:** every pass 6 and pass 8 line was traced to `git show 18b9cfa`, `git show 02e4c89`, the `0054.00` seat lines and the TRIAL-K6 PASS list. Quoted text was compared word for word.

## Method
- **Repo state:** the shared working tree was only read. My only writes are this file and Q58-Q60 in `kernel/QUESTIONS.md`, committed by pathspec (the index was empty first). The builder was never run in the shared tree.
- **Scratch copies:**
  - `/tmp/k7/repo` (fresh `--no-local` clone at `2db15dd`, cargo target `target/k7-trial` inside it);
  - `/tmp/k7/h*` (one fresh clone per attack), `/tmp/k7/evil` (the made-up history for T20), `/tmp/k7/evilgit` (T17);
  - `/tmp/k7/pub` (publish, `--no-local --single-branch`) and `/tmp/k7/gh` (GitHub `prima/build`).
- **Publish copy:** read with `git branch`, `git for-each-ref`, `git config`, `git rev-list`, `git cat-file -e` and `git push --dry-run` only. Nothing was fetched into it, deleted or pushed.
- **Blobs:** each is `git rev-parse HEAD:<path>` at `2db15dd`, written in full.
