# Kernel trial 6 (TRIAL-K6): hostile pass on kernel pass 7, the portable seat guard, and the published copies

Lane TRIAL-K6, 2026-11-11, about 4:10 PM CST (5:10 PM EST). I'm a fresh session that did not build these faces. Under R20 (`DIRECTOR-RULINGS.md:78-80`) that counts as a different view, so a PASS here can qualify a face for an R2 seat (`DIRECTOR-RULINGS.md:7-9`).
I only report. Nothing in `kernel/`, `books/`, `crates/` or `app/` was changed, nothing was seated, nothing was pushed or deleted. New questions go to `kernel/QUESTIONS.md` as Q56-Q57, tagged `[TRIAL-K6]`.

**Target (HEAD `18dd576`):**
- A) the 6 draft faces pass 7 step 3 changed (`7f702a1`): `00.00.00.0054.05.02`, `10.11.21.0013.05.02`, and the notes `0051.06.01`, `0052.06.01`, `0054.06.01`, `00.00.axioms.06.01`;
- B) the portable seat guard (`99fec8c`, tests in `kernel/build.test.mjs`, test helper fix `f0486ff`) and the 24 seats;
- C) portability: a `--no-local --single-branch` clone of `/workspace/workshop-build/publish` and a clone of GitHub `prima/build`, plus the hygiene of the publish copy.

**Judged against:** `DIRECTOR-RULINGS.md` R1-R22, `docs/spec/face00.md` (DRAFT), `kernel/QUESTIONS.md`, `docs/BUILD-LOG.md` (pass 6 entry `:172-178`, pass 7 entry `:190-207`), `docs/trial/kernel-trial-5.md`, `kernel/build.mjs`, `kernel/build.test.mjs`.
**Rules used:** Q41 is applied, not held. Q55 (pack grants) is the Director's, so no pack fails only because its grant is narrow. Q35 (may a 06 note be seated) is open, so a note can PASS as a draft; it is not seatable, and the builder refuses to seat it (`SEATABLE_COUNTERS`, `build.mjs:41`).

## Summary

| Verdict | A (pass-7 faces) |
|---|---|
| PASS | 4 (1 pack eligible for an R2 seat, 3 notes that pass as drafts) |
| FAIL | 2 |
| HELD-7 (depends on an open question) | 0 |
| **total** | **6** |

| Severity | Findings |
|---|---|
| blocker | 0 |
| major | 1 (finding 1: a committed `.gitattributes` line hides an un-seat, also in clones) |
| minor | 4 |

**PASS list, eligible for an R2 seat** (full git blob at HEAD `18dd576`; a seat must name this trial by path and blob and exactly this face blob; any byte change needs a new trial):
- `00.00.00.0054.05.02` (blob `2bf1da6ff8c4bd77943150da2786f07d93fe824d`)

**Notes that pass as drafts, not seatable while Q35 is open** (the builder refuses a seated 06 counter; blobs for the record):
`00.00.00.0051.06.01` blob `d37965b88165bc00a637a7aa310b6bbb3bd88c1e`; `00.00.00.0052.06.01` blob `9b5ea002d135cc90ae512278744c358302c38283`; `00.00.axioms.06.01` blob `16145dd102eef0f92afaf20f1eacad3681dcc84b`.

**Before seating, note:**
- `0054.05.02` is a face 05 counter, so `SEATABLE_COUNTERS` allows it. Its seat line goes in the `0054.00` registry as `seat-05.02:`, and `why-05.02:` goes away.
- `git rev-parse HEAD:kernel/00.00.00/00.00.00.0054.05.02.draft.md` is `2bf1da6ff8c4bd77943150da2786f07d93fe824d`. Renaming `.draft.md` to `.md` does not change the blob.
- Findings 1 and 2 do not change any verdict and do not touch the 24 seats. All 24 were checked in fresh clones with no attributes file, no replace refs, and a linear history.

## TRIAL-K5 fixes: did they land?

| K5 # | Landed? | Evidence |
|---|---|---|
| 1 major (published copy) | yes | Seats cite `trial: docs/trial/<file>.md blob <40 hex>`. Both published clones give `seats 24`, `59 findings, 0 errors`, exit 0 (part C). |
| 2 major (replace, GIT_DIR) | yes | `build.mjs:160-162`: `--no-replace-objects`, `GIT_NO_REPLACE_OBJECTS=1`, every `GIT_*` var dropped. K09 (`GIT_DIR`), K10 (`GIT_ALTERNATE_OBJECT_DIRECTORIES`), K11 (`git replace`) and K12 (grafts) were all refused. The `.git` gitfile swap (K15) is still accepted; see the observations. |
| 3 minor (books edit hides un-seat) | yes for a linear history | `historySeats` (`:263-282`). K20 (H11 again) was refused. It is bypassed by `.gitattributes` (finding 1) and by a merge (finding 2). |
| 4 minor (forged trial or ruling) | partly, as BUILD-LOG says | K05 (H5) and K06 (trial commit plus kernel change) were refused. K07 (H4, a new forged trial in a docs-only commit) is still accepted, as stated at `BUILD-LOG.md:197`. A merge gets around write-once (finding 2b). |
| 5 minor (un-seat short or no reason) | yes | K18 (8-hex) and K19 (no reason) were refused. Any 3-letter word counts as a reason (K19b), see the observations. |
| 6 minor (0054 pack: seqpage, builder) | yes | `0054.05.02:6` drops "the builder" for page types, and says why (the builder checks no stamp `type`, which is true: `validate` reads `st.state`, `st.address` and `st.title` only). `:22`, `:25-26` name `crates/seqpage/src/face00.rs:70` `TYPES` (true) beside `crates/seqaddr-core/src/face.rs:132` `PAGE_TYPES` (true), with a comparing test. |
| 7 minor (0013 pack: w01 half, no app card) | yes, with a new flaw | w01 done (`0013.05.02:25`) now checks the page number in the sample file names, `books/`, `crates/compute/src/store.rs` (`:50`, true) and the app (`app/app/ask/page.tsx:14` `/page/${BOOK}.0013`, `app/components/AskBox.tsx:104`, true). New w03 is the app card. Its order is wrong (finding 4). |
| 8 minor (merges not logged on pages) | yes, with one wrong detail | The three pass 6 law merges are copied into `0051.06.01` and `0052.06.01`, word for word against `git show 18b9cfa`. Pass 6 and 7 lines were added to the `0054` and `00.00.axioms` notes. `0054.06.01:6` names two symbols that are not on 0054 (finding 5). |
| 9 (class) | not decided (Q55, the Director's) | No grant line changed (`7f702a1`). Not counted against any pack here. |

## Checks run (real output)

`/workspace/k6/repo` is a fresh `git clone` of the shared repo at `18dd576` (full history, branch `build`). Each hostile copy is a fresh clone of it under `/tmp/k6/` (helpers `/tmp/k6/lib.sh`).

**`node kernel/build.mjs --check`** (`/workspace/k6/repo`): exit 0.
```
finding  00.00.00.0055.01.draft.md: 04 dictionary-is-an-index: why missing (4.7)
... (59 findings, all "why missing (4.7)")
checked  books/00.00.00.book  50 entries
checked  books/00.00.axioms.jsonl  7 entries
checked  books/10.00.00.book  1 entries
checked  books/10.11.00.book  1 entries
checked  books/10.11.21.book  15 entries
seats 24
59 findings, 0 errors
```

**`node kernel/build.test.mjs`** (`/workspace/k6/repo`): exit 0. There are 36 `ok` lines, then `all passed`. The 11 pass 7 tests are among them, for example:
```
ok    Q53: seats still verify after a filter-branch rewrite changes every commit id (K5 finding 1)
ok    Q54 a: a git replace forge of a trial blob is refused (K5 HR)
ok    Q54 a: GIT_DIR pointing at a clone with a forged trial is ignored (K5 H15)
ok    Q54 b: an un-seat hidden by a committed books edit is refused (K5 H11)
ok    Q54 c: a PASS line added to a real trial in a later commit is refused (K5 H5)
ok    Q54 c: a trial added in a commit that also changes kernel/ is refused
ok    Q54: a shallow clone is refused
all passed
```

**`CARGO_TARGET_DIR=target/k6-trial cargo test --workspace --no-fail-fast`** (in `/workspace/k6/repo`, target dir inside that clone): `exit=0`, `38 result lines, passed=411 failed=0 ignored=2`. This includes `tests/face00.rs`, `tests/binary.rs` and `tests/rules_hostile.rs`.

**24 seats, each blob equal to `git rev-parse HEAD:<path>`.** These were read from the `seat-NN:` lines in the face 00 files at `18dd576`. The last column is the cited trial and the first 12 hex digits of its blob:
```
00.00.00.0051.05.01 MATCH c160a4da9947eeeb3de88b512208ee9e7836011b kernel-trial-5.md 86eb3a58e028
00.00.00.0051.05.02 MATCH 7dbf70bd22af1bf0354edd82aff3ddb405ef892d kernel-trial-4.md a5d253d5e127
00.00.00.0052.01 MATCH 88bce491bb2bffe645a5c6825096f41d8b86080f kernel-trial-5.md 86eb3a58e028
00.00.00.0052.04 MATCH e9ca59a1d708acfd57b9e5f7e6b758e41e4fde6f kernel-trial-5.md 86eb3a58e028
00.00.00.0052.05.01 MATCH 7993b14b830d12feb5a54509b41e74c931afe334 kernel-trial-4.md a5d253d5e127
00.00.00.0052.05.02 MATCH c82b1fc6d2d3d6ce6e5a44cf99cbc7bf93b62332 kernel-trial-4.md a5d253d5e127
00.00.00.0053.05.01 MATCH 77ee148ffd645b15b4aeeb1401ff6b72e05a35da kernel-trial-4.md a5d253d5e127
00.00.00.0053.05.02 MATCH 8499872db0d7551309befdbf12ce1d1c7fa821c4 kernel-trial-4.md a5d253d5e127
00.00.00.0054.05.01 MATCH aa07b61116572c9e25353a5e7f3b6ed97941d2a0 kernel-trial-5.md 86eb3a58e028
00.00.00.0055.05.01 MATCH 6582d3e56495ca93203e81871659da0481550d41 kernel-trial-4.md a5d253d5e127
00.00.00.0055.05.02 MATCH 596aa9ba0befffa6f9f6ca93364b9a6fea426478 kernel-trial-4.md a5d253d5e127
00.00.00.0056.01 MATCH 112c169ccd06d54c6d9ab607fee6c2d16004cc62 kernel-trial-2.md da5d51424fee
00.00.00.0056.05.01 MATCH 0914ebb8274c3e049440e11388b69da2b138f447 kernel-trial-4.md a5d253d5e127
00.00.00.0056.05.02 MATCH 93178adddeb2ec915a2c5d4cc070d0dc50c03d37 kernel-trial-4.md a5d253d5e127
00.00.00.0057.05.01 MATCH 67b3b9b6762af70a7494893fb7ff47e4e86e4281 kernel-trial-4.md a5d253d5e127
00.00.00.0057.05.02 MATCH 037eec2ff5e9c6c18020f06679358a13e9a62bb1 kernel-trial-4.md a5d253d5e127
00.00.axioms.05.01 MATCH cbf5cba0d5429e2e0b14e56f5ed8a1eba1d06ad2 kernel-trial-5.md 86eb3a58e028
00.00.axioms.05.02 MATCH 452be16b0536002a12279c5d485c68c5217fa6c8 kernel-trial-4.md a5d253d5e127
10.11.21.0012.05.01 MATCH 9aaed75fc8f0594a1289fa83e870a474d4d021d2 kernel-trial-4.md a5d253d5e127
10.11.21.0012.05.02 MATCH dd89a5199d1a0b47f5cac3bce2ec0e8185ff1ce6 kernel-trial-5.md 86eb3a58e028
10.11.21.0013.05.01 MATCH 16146a0fa073fc947138de43033f9e9a2b75ac09 kernel-trial-5.md 86eb3a58e028
10.11.21.1001.01 MATCH 5415cef2dd0a37f3c2ba4c9b6d2652262f0ef82d kernel-trial-2.md da5d51424fee
10.11.21.1001.05.01 MATCH 566071064f63a5c85fcb3bd87d9e375717bdbf51 kernel-trial-4.md a5d253d5e127
10.11.21.1001.05.02 MATCH 2aa3490239620604ce1bb13c34841a60ac8f7056 kernel-trial-4.md a5d253d5e127
```
That is 24 of 24 MATCH. The cited trial blobs are each file's first-added blob:
- kernel-trial-2 was added at `da5d51424fee3bea1d8443c619fcba3c534a1ace` (HEAD has `a4156612...`, after the `fae009a` appendix);
- kernel-trial-4 was added at `a5d253d5e12722956afea38e79cb7fc1cf492c7b` (same at HEAD);
- kernel-trial-5 was added at `86eb3a58e028d9b23e0a94cd4577329195300f99` (same at HEAD).

The 7 kernel-trial-5 seats are exactly the 7 blobs on its PASS list (`kernel-trial-5.md:32-38`).

### Part C: portability (real output)

**C1. `git clone --no-local --single-branch -b build /workspace/workshop-build/publish /tmp/k6/pub`:**
```
PUB HEAD: e2facc7 KERNEL pass 7: BUILD-LOG entry (99fec8c, 8ba452d, 7f
* build
  remotes/origin/HEAD -> origin/build
  remotes/origin/build
4b369fa absent
6a1fee5 absent
ed82086 absent
target/ in history: 0
false                      (is-shallow-repository)
check exit=0
checked  books/10.11.21.book  15 entries
seats 24
59 findings, 0 errors
0                          (ERROR lines)
test exit=0
36                         (ok lines)
all passed
```

**C2. `git clone --single-branch -b prima/build https://github.com/Amalgamour/Workshop.git /tmp/k6/gh`** (read only):
```
GH HEAD: e2facc7 KERNEL pass 7: BUILD-LOG entry (99fec8c, 8ba452d, 7f
4b369fa absent
6a1fee5 absent
ed82086 absent
target/ in history: 0
check exit=0
checked  books/10.11.21.book  15 entries
seats 24
59 findings, 0 errors
errors: 0
test exit=0
36
all passed
GH tree == publish tree
GH tree == local 18dd576 tree (minus target/)
```
`git ls-remote --heads origin` shows only `refs/heads/claude` (`bcaaee8c`) and `refs/heads/prima/build` (`e2facc78953c0e25bf41af02d9ed5d20a2ee448f`). So `prima/build` is the publish `build` HEAD.

**C3. Publish copy hygiene (`/workspace/workshop-build/publish`, report only, nothing deleted):**
```
refs/heads/build e2facc7                      commits touching target/: 0
refs/heads/incoming 18dd576                   commits touching target/: 2
refs/original/refs/heads/build af8cee9        commits touching target/: 2
refs/remotes/origin/build af8cee9             commits touching target/: 2
remote.origin.url https://github.com/Amalgamour/Workshop.git
remote.origin.fetch +refs/heads/build:refs/remotes/origin/build
branch.build.remote origin
branch.build.merge refs/heads/build
```
- Yes: `incoming` (the unfiltered local history, so `4b369fa` is reachable) and `refs/original/` still hold the `target/` history.
- So does a third ref that K5 did not name: `refs/remotes/origin/build` at `af8cee9`. It is a stale tracking ref left from the first clone of `../repo`. `origin` now points to GitHub, which has no `build` branch.
- `branch.build.merge` is `refs/heads/build`. A bare `git push` from `build` would make a new `build` branch on GitHub, with clean history but not approved. A `--all` or `--mirror` push would publish `incoming`, and so the `target/` history.
- The flow in use (`git push origin build:refs/heads/prima/build`) pushes only clean history.

### Hostile seat tests (part B, scratch clones only)

| # | Hostile change | Result |
|---|---|---|
| K01 | none (baseline fresh clone) | exit 0, `seats 24`, 0 errors |
| K02 | seat draft `0054.05.02` citing the real `kernel-trial-5.md blob 86eb3a58...`, which does not list it | refused: "its PASS list does not name 00.00.00.0054.05.02" |
| K03 | the same with the old `kernel-trial-5.md@6a1fee5` form | refused: "cites a commit id ... re-pin it" |
| K04 | trial blob given as the 8-hex prefix `86eb3a58` | refused: "is a short prefix" |
| K05 | add a PASS line for `0054.05.02` to the real `kernel-trial-5.md` in a later commit, and cite the new blob (H5) | refused: "was added at blob 86eb3a58... (commit 6a1fee5f8a1e), not 9271b00e..." |
| K06 | forged `kernel-trial-fake.md` added in a commit that also changes `kernel/MAP.md` | refused: "also changes kernel/MAP.md" |
| K07 | forged `kernel-trial-fake.md` in a commit that touches only `docs/trial/` (H4) | **accepted**: `seats 25`, `59 findings, 0 errors` (only `differs:` because books were not rebuilt). Known residue (`BUILD-LOG.md:197`) |
| K08 | the same forged trial, not committed | refused: "no commit reachable from HEAD adds" |
| K09 | `GIT_DIR=/tmp/k6/evil/.git` (a clone holding the K07 forged commit) | ignored, refused: "no commit reachable from HEAD adds" |
| K10 | `GIT_ALTERNATE_OBJECT_DIRECTORIES=/tmp/k6/evil/.git/objects` | ignored, refused (same message) |
| K11 | `git replace 86eb3a58... <copy listing 0054.05.02>` | refused, every seat: "the repo has replace refs (refs/replace/86eb3a58...)" |
| K12 | `.git/info/grafts` | refused, every seat: "the repo has a grafts file" |
| K13 | `git clone --depth 5` | refused, every seat: "the repo is a shallow clone" |
| K14 | `.git/objects/info/alternates` pointing at the evil objects (a file, not env) | refused: "no commit reachable from HEAD adds" (objects alone do not add history) |
| K15 | replace `.git` with a gitfile `gitdir: /tmp/k6/evil/.git` | **accepted**: `seats 25`, 0 errors (see the observations) |
| K16 | seat note `0051.06.01` citing a committed trial that passes it | refused: "a 06 counter may not be seated: R22 allows only face 05 counters" |
| K17 | un-seat `0051.05.02` (rename to `.draft`) with no record | refused: "was seated ... write unseat-05.02" |
| K18 | `unseat-05.02: re-trial needed; was blob 7dbf70bd` (prefix) | refused: "must name the full old blob" |
| K19 | `unseat-05.02: was blob <full 40 hex>` (no reason) | refused: "gives no reason" |
| K19b | `unseat-05.02: xyz <full 40 hex>` | accepted (any 3 letters count as a reason; see the observations) |
| K20 | un-seat with no record, books line removed, committed (H11) | refused: "was seated (build-stage (R2)) in the last build but is not now" |
| **K21** | **commit `.gitattributes` with `kernel/** -diff`; then un-seat `0051.05.02` with no record, books line removed, committed; rebuild, commit** | **accepted**: exit 0, `seats 23`, `59 findings, 0 errors`. **Also exit 0 in a fresh `--no-local` clone** (`/tmp/k6/h21c`). Control: the same commits with `.gitattributes` moved out of the working tree are refused (finding 1) |
| K22 | the same with `kernel/** -diff` only in the local `.git/info/attributes` (not committed) | **accepted**: 0 errors, `seats 23` (finding 1) |
| K23 | local `diff.evil.textconv` on `DIRECTOR-RULINGS.md` adding a forged `## R99` seat line; director seat for `0054.05.02` | refused: "R99, which is not in DIRECTOR-RULINGS.md as committed at HEAD" (`git show` does not apply textconv to a blob) |
| K24 | local textconv on `books/*` dropping the `0051.05.02` line, plus `kernel/** -diff`, uncommitted un-seat | refused: HEAD:books still names the seat |
| **K25** | **side branch from `d37e532^` adds a `docs/trial/kernel-trial-3.md` with an extra PASS line for `0054.05.02` (docs-only commit); merge into `build` taking the side's copy of that file; seat `0054.05.02` citing the new blob** | **accepted**: 0 errors, `seats 25`. The real `kernel-trial-3.md` gained 3 lines. `git log --full-history --diff-filter=A` finds the real add `d37e532`, and plain `git log` finds only the side commit (finding 2) |
| **K26** | **side branch from `99fec8c` (before the seat at `8ba452d`), commit `kernel/` as at HEAD but with `0054.05.01` un-seated and no record; merge into `build` taking the side's `kernel/` and dropping the books line; rebuild, commit** | **accepted**: exit 0, `seats 23`, also in a fresh `--no-local` clone. `git log --full-history -G seat-05.01` finds `8ba452d`, and plain `git log` finds nothing (finding 2) |

Not repeated by hand: a prefix-collision forge. The guard compares full blobs (`verifySeat`), and the test "R2: a prefix-collision forge of a seated face is refused (K4 HM)" passes in all three clones.

## Findings

### 1. major: one line in `.gitattributes` hides every past seat from the history check
- **Evidence:**
  - `historySeats` (`build.mjs:263-282`) finds past seats with `git log -p ... -G seat- HEAD -- kernel/` (`:265`).
  - When a path is marked binary (`-diff`), git prints "Binary files differ" and `-G` does not search it, so no `+seat-` line is ever seen.
  - With `kernel/** -diff` in a committed `.gitattributes`, the history check sees no past seats. A committed un-seat plus a books edit then builds clean (K21), the same hole as K5 H11, which pass 7 closed for a plain history.
  - It survives a fresh clone, so it would also pass in the published copy and on GitHub.
  - `.git/info/attributes` does the same locally, with nothing committed (K22).
- **Breaks:**
  - R2 (`:9`): "every such seat can be found and re-reviewed later".
  - The claim in `BUILD-LOG.md:195` and Q54 (b), "taken", that past seats come from history.
  - The attributes line looks harmless and sits far from `kernel/`.
- **Fix direction (builder lane, not done):**
  - Run the history read with `--text` and `--no-textconv` (`git log -p -a --no-textconv ...`). Attributes then cannot make the seat lines invisible.
  - Or read the face 00 files per commit with `git cat-file blob` and parse their seat lines.
  - Also consider an error when any `.gitattributes` or `info/attributes` line touches `kernel/`, `books/` or `docs/trial/`.
  - Add a test like K21.
- Raised in Q56.

### 2. minor: `git log` follows one parent at a merge, so a merge gets around two pass 7 checks
- **Evidence:**
  - `trialOrigin` (`:189-190`) and `historySeats` (`:265`) call `git log ... HEAD -- <path>` without `--full-history`.
  - With history simplification, at a merge whose result matches one parent for that path, git walks only that parent.
  - (a) K26: a merge that takes `kernel/` from a side branch cut before `8ba452d` drops the commit that added `seat-05.01` from the walk. `0054.05.01` is un-seated with no record, and the check passes, also in a fresh clone.
  - (b) K25: a merge that takes a side branch's copy of a real trial file makes the side commit its "oldest add". A PASS line added that way can be cited. This gets around Q54 (c) write-once, which K05 shows holds on a plain history.
  - With `--full-history`, both walks see the hidden commit (`8ba452d` and `d37e532`).
- **Limits:** both leave a merge commit in git history, so they are findable. That is the same class as K5 findings 3 and 4, which is why this is minor.
- **Fix direction:**
  - Add `--full-history` to both `git log` calls.
  - Also refuse a cited trial whose path differs between the parents of any merge on HEAD's history, or simply refuse merge commits that touch `kernel/` or `docs/trial/` (this branch is linear today).
  - Add tests like K25 and K26.
- Raised in Q56.

### 3. minor (class, no verdict change): the H4 residue is unchanged
- K07 shows a brand-new forged trial in a docs-only commit still seats a face. `BUILD-LOG.md:197` says so, and Q54 (c) residue covers it. It is listed here only so the count is complete.

### 4. minor: the 0013 pack's new w03 depends on a number only w01 can settle, but says it is not blocked
- **Evidence:**
  - w03 (`0013.05.02:39-47`): `depends: w02`, `blocked-by: none`. Its done ends "the common-questions list on the screen is read from the ruled page number".
  - The page number is ruled only by w01 (`:21-26`), which is `blocked-by: Q33, Q49`. So w03's done cannot be decided until w01 is done.
  - The app reads `.0013` today (`app/app/ask/page.tsx:14`, `app/components/AskBox.tsx:104`), and w01's done already checks the app.
- **Breaks:** the pack checks a PASS needs, as TRIAL-K4 and TRIAL-K5 applied them: a decidable done, and an order that matches the dependencies. TRIAL-K5 finding 14 failed this same pack for a missing `depends: w01`.
- **Fix direction:** either `depends: w01, w02` and `blocked-by: Q33, Q49` on w03, or drop the "ruled page number" clause from w03's done (w01 already covers the app).

### 5. minor: the 0054 note logs two symbol names that are not on 0054
- **Evidence:**
  - `0054.06.01:6` says "05.01 and 05.02 name code symbols (CARD_TYPES, AXIOMS, AXIOMS_FILE)".
  - The 0054 counters name only `CARD_TYPES` (`0054.05.01:5`, `:11`, `0054.05.02:32`, `:35`). `AXIOMS` and `AXIOMS_FILE` are on `00.00.axioms.05.01:5` and `:11`.
  - The pass 6 diff (`git show 18b9cfa`) changed `build.mjs:30-31` to `CARD_TYPES` on 0054. The wording looks copied from the grouped BUILD-LOG line (`:178`).
- **Breaks:** the note is the page's lineage (axiom 6), and here it is not accurate to its own page.
- **Fix direction:** write "(CARD_TYPES)" on `0054.06.01:6`.

**Observations (no severity):**
- **K15, `.git` swapped for a gitfile pointing at another repo:** accepted.
  - This is H15 done with a file instead of `GIT_DIR`.
  - A local guard can't tell a swapped `.git` from the real one, and anyone who can do that can also rewrite `.git/objects`.
  - The real gate is the check in a fresh clone or the published copy, and K15 fails there.
  - If wanted, the builder could refuse when `git rev-parse --absolute-git-dir` is not `<ROOT>/.git`.
- **Un-seat reason check (`build.mjs:311`):** any 3 letters count as a reason (`xyz`, K19b). That is fine as a guard against an empty record. A human still has to read the reason.
- **`0054.05.02` w04 reason (`:52`):** it says "TRIAL-K3 ... passed no face". That is true, but TRIAL-K3 gave a per-face verdict only on `0054.00` (`kernel-trial-3.md:212`). The last per-face verdicts on `0054.01`, `.02` and `.04` are TRIAL-K2's HELD-7 (`kernel-trial-2.md:212-214`). It is not false, so it is not a finding. Cite K2 in the next draft.
- **Publish hygiene:** see C3. Three refs hold `target/` history: `incoming`, `refs/original/refs/heads/build`, and the stale `refs/remotes/origin/build`. `branch.build.merge` points to a GitHub `build` branch that doesn't exist. Raised as Q57 (builder lane).

## Per-face verdicts

| Face | Blob (HEAD `18dd576`) | Verdict | Findings / open question |
|---|---|---|---|
| `00.00.00.0054.05.02` | `2bf1da6ff8c4bd77943150da2786f07d93fe824d` | PASS | K5 finding 6 landed. Every outcome part has a card: page types and fields go to w01, card types to w02, the seat to w04/w05. Every done can be decided. The order is fix, fill, trial, seat. `face.rs:99-111`, `:132` and `face00.rs:70` are correct. DESIGN.md section 2 is at `:61`. D36/D37 are on topic (`DECISIONS-INDEX.md:67-68`). `0054.04` has 3 cards, 2 with `why: 4.7` (`:11`, `:17`). Q33 and Q49 are named as blockers, not answered. The grant is Q55, not counted. Observation on the w04 reason. |
| `10.11.21.0013.05.02` | `55d9b12b9881d93a39a08308a5337d5680f4fb40` | FAIL | 4 minor. K5 finding 7 landed otherwise: `store.rs:50`, `ask/page.tsx:14`, `AskBox.tsx:104`, `askq.rs` `face_text` (`:16`), and the `1001.01` blob `5415cef2...` (seated, MATCH) are all true. `app/scripts/` exists. The grant is Q55, not counted. |
| `00.00.00.0051.06.01` | `d37965b88165bc00a637a7aa310b6bbb3bd88c1e` | PASS (draft; not seatable, Q35) | The pass 6 R17 R7 merge matches `git show 18b9cfa` word for word. The pass 7 line matches the seat at `0051.00` (c160a4da...) and the kernel-trial-5 blob. "01 stays a draft, HELD-7 on Q30" matches `kernel-trial-5.md:237`. |
| `00.00.00.0052.06.01` | `9b5ea002d135cc90ae512278744c358302c38283` | PASS (draft; not seatable, Q35) | Both pass 6 R22 merges (01 and 04) match `18b9cfa`, and now say they replace the pass 5 text (K5 finding 8). The pass 7 blobs `88bce491...` and `e9ca59a1...` equal the seats. |
| `00.00.00.0054.06.01` | `ed46a348c9a3e9eb74082db382b5759aa21510b6` | FAIL | 5 minor (`AXIOMS`, `AXIOMS_FILE` are not on 0054). The pass 7 line is true: seat blob `aa07b611...`, outcome change, w01 seqpage `TYPES`, Q55 not decided. |
| `00.00.axioms.06.01` | `16145dd102eef0f92afaf20f1eacad3681dcc84b` | PASS (draft; not seatable, Q35) | The pass 6 symbols are true (`00.00.axioms.05.01:5`, `:11`). The pass 7 seat blob `cbf5cba0...` matches. The C3.2 fix in `7b08cbf` is true: the test "an axioms 01 card with no 04 card is refused (H3)" was added there, and the claim that the seated 05.01 still says "found missing" is true (`:16`). |

**What a PASS on a 05.02 pack checked** (as TRIAL-K4 and TRIAL-K5):
- Every header field is present.
- Every work card has `reason`, `depends`, `blocked-by`, a decidable `done:`, and a `path`.
- The order is fix, then fill, then trial, then seat, and the dependencies match it.
- Every part of the `outcome:` has a card.
- `design:` names a real DESIGN.md section and real DECISIONS ids on the topic.
- No card seats its own work, uses an override (R21), or answers an open Director question.
- Every code or line cite was opened at `18dd576`.

**What a PASS on a 06.01 note checked:** every pass 6 or pass 7 line was traced to `git show 18b9cfa`, `git show 7f702a1`, the face 00 seat lines, and the trial PASS lists. Quoted before and after text was compared word for word.

## Method
- **Repo state:** the shared working tree was only read, with one slip. While checking this file I ran a stray `node -e "import('.../kernel/build.mjs')"` in the shared tree. That runs the builder once in write mode (the same slip TRIAL-K5 reported). It rewrote `books/` with identical bytes, and `git status --short books kernel` showed no change afterwards. The PASS-list parse of this file was then checked with a copy of `passList` (identical to `build.mjs`, checked with `diff`), not the builder. My only writes are this file and Q56-Q57 in `kernel/QUESTIONS.md`, committed by pathspec.
- **Scratch copies:**
  - `/workspace/k6/repo` (clone at `18dd576`, with cargo target `target/k6-trial`);
  - `/tmp/k6/h*` (one fresh clone per attack), `/tmp/k6/evil` (the forged-trial clone);
  - `/tmp/k6/pub` (publish, `--no-local --single-branch`) and `/tmp/k6/gh` (GitHub `prima/build`).
- **Publish copy:** read with `git log`, `git for-each-ref`, `git config` and `git ls-remote` only. Nothing was fetched into it, deleted or pushed.
- **Blobs:** each is `git rev-parse HEAD:<path>` at `18dd576`, written in full.
