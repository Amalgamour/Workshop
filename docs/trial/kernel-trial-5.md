# Kernel trial 5 (TRIAL-K5): hostile pass on kernel pass 6, the hardened seat guard, and the published copy

Lane TRIAL-K5, 2026-11-11, about 4:40 PM EST. I'm a fresh session that did not build these faces. Under R20 (`DIRECTOR-RULINGS.md:78-80`) that counts as a different view, so a PASS here can qualify a face for an R2 seat (`DIRECTOR-RULINGS.md:7-9`).
I only report. Nothing in `kernel/`, `books/`, `crates/` or `app/` was changed, nothing was seated, nothing was pushed. New questions go to `kernel/QUESTIONS.md` as Q53-Q55, tagged `[TRIAL-K5]`.

**Target (HEAD `18b9cfa`):**
- A) the 10 draft faces pass 6 step 3 changed (`18b9cfa`): `0051.01`, `0051.05.01`, `0052.01`, `0052.04`, `0054.05.01`, `0054.05.02`, `00.00.axioms.05.01`, `10.11.21.0012.05.02`, `0013.05.01`, `0013.05.02`;
- B) the hardened seat guard (`4d7d502`, plus `SEATABLE_COUNTERS` in `18b9cfa`; `kernel/build.mjs:36-39`, `:126-238`, `:285-293`) and the 17 seats;
- C) portability: the seats in the published copy (`/workspace/workshop-build/publish`, branch `build`, filter-branched without `target/`, so its commit ids differ).

While I worked, HEAD moved to `c7bb4d6` (four FOLLOWUPS commits). `git diff 18b9cfa c7bb4d6 -- kernel books docs/trial docs/spec/DIRECTOR-RULINGS.md` is empty, so every blob below is the same at both.

**Judged against:** `DIRECTOR-RULINGS.md` R1-R22, `docs/spec/face00.md` (DRAFT), `kernel/QUESTIONS.md`, `docs/BUILD-LOG.md` (pass 6 entry, `:172-178`), `docs/design/DECISIONS-LOG.md`, `docs/trial/kernel-trial-4.md`.
**Rules used:** Q41 (which reading of R22) is applied, not held. A face is HELD-7 only when its verdict really hangs on another open Director question.

## Summary

| Verdict | A (pass-6 faces) |
|---|---|
| PASS (eligible for an R2 seat) | 7 |
| FAIL | 2 |
| HELD-7 (depends on an open question) | 1 |
| **total** | **10** |

| Severity | Findings |
|---|---|
| blocker | 0 |
| major | 2 (finding 1: published copy; finding 2: seat guard) |
| minor | 7 |

**PASS list, eligible for an R2 seat** (full git blob at HEAD `18b9cfa`, unchanged at `c7bb4d6`; a seat must name this trial and exactly this blob; any byte change needs a new trial):
- `00.00.00.0051.05.01` (blob `c160a4da9947eeeb3de88b512208ee9e7836011b`)
- `00.00.00.0052.01` (blob `88bce491bb2bffe645a5c6825096f41d8b86080f`)
- `00.00.00.0052.04` (blob `e9ca59a1d708acfd57b9e5f7e6b758e41e4fde6f`)
- `00.00.00.0054.05.01` (blob `aa07b61116572c9e25353a5e7f3b6ed97941d2a0`)
- `00.00.axioms.05.01` (blob `cbf5cba0d5429e2e0b14e56f5ed8a1eba1d06ad2`)
- `10.11.21.0012.05.02` (blob `dd89a5199d1a0b47f5cac3bce2ec0e8185ff1ce6`)
- `10.11.21.0013.05.01` (blob `16146a0fa073fc947138de43033f9e9a2b75ac09`)

**Before seating, note:**
- `0052.01` and `0052.04` are content faces, not counters, so `SEATABLE_COUNTERS` does not apply. Their seat lines go in the `0052.00` registry as `seat-01:` and `seat-04:`.
- Finding 1 means every seat that cites a local commit id fails in the published copy. Seating these 7 the same way adds 7 more seats that fail there. Fix finding 1 first, or accept that the published `--check` stays red until it is fixed.
- Finding 2 means the local guard can be fooled without a commit. That does not change any verdict here. The 17 seats were checked with `GIT_NO_REPLACE_OBJECTS=1` in a fresh clone that had no replace refs.

## TRIAL-K4 fixes: did they land?

| K4 # | Landed? | Evidence |
|---|---|---|
| 1 major (prefix) | yes | `SEAT_LINE` still parses 7-40 hex digits (`build.mjs:137`), but `verifySeat` refuses anything shorter than 40 (`:181`) and compares the full blob for equality (`:182`). My H3 was refused. A pre-K4 short PASS prefix must also be the face's file in that trial's tree (`:163-167`, `:204`). |
| 2 major (working-tree ruling) | yes | Rulings are read with `git show HEAD:` (`:187`). My H6 was refused: "not in DIRECTOR-RULINGS.md as committed at HEAD". A committed forged ruling is still accepted (H7, finding 4). |
| 3 major (face 00 can't be seated) | held | Q51 is open, and face 00 is still unseated. No change. |
| 4 minor (trial commit) | partly | An ancestor check was added (`:200`), and my H8 (side branch) was refused. A forged trial committed on the branch is still accepted (H4, H5; finding 4). |
| 5 minor (no git) | yes | `:183` makes it an error, and `priorSeats` errors too (`:214`). The test "with no git a seat is an error" passes. |
| 6 minor (books/ in working tree) | yes for the working tree | `priorSeats` reads `HEAD:books/` (`:215-217`). My H10 (`rm -rf books`) was refused. A committed books edit still hides an un-seat (H11, finding 3). |
| 7 minor (any counter seated) | yes | `SEATABLE_COUNTERS = { '05': 'R22' }` (`:39`), enforced at `:288`. My H9 (a 06 note with a real committed trial) was refused. |
| 8 minor (0051.01 reserved) | yes | `0051.01:53`. |
| 9 minor (Counted Faces) | yes | `0052.01:87` and `0052.04:92` now say face 05 only, with other counters open on Q35. |
| 10 minor (MAP) | yes | `MAP.md:239`. |
| 11 minor (0051.05.01) | yes | `0051.05.01:13` matches `kernel-trial.md:58` (about 20 in total; 10 lines on 0051.04, 4 on 0057.04). |
| 12 minor (stale line cites) | yes | `0054.05.01:5`, `:11`, `0054.05.02:32` and `00.00.axioms.05.01:5`, `:11` now name `CARD_TYPES`, `AXIOMS` and `AXIOMS_FILE`, which are at `build.mjs:26-27` and `:34`. |
| 13 minor (wrong D id) | yes | `0013.05.01:6` and `0013.05.02:13` cite DECISIONS-LOG D147 (`:84`), D267 (`:285`), D271 (`:289`) and D290 (`:313`). All four are on the topic. |
| 14 minor (0013 pack) | yes | w02 expects state `seated` (`0013.05.02:35`, true per R5 and `crates/compute/src/askq.rs:16-17`), and w03 depends on w01 (`:43`). |
| 15 minor (0012 pack) | yes | w01 done is concrete (`:25`), w03 now indexes every word (`:39-47`), w04 depends on w01 and w03 (`:53`), and the w05 seat is blocked by Q35 (`:64`). |
| 16, 17 (parked) | yes | `kernel/parked/README.md` says Q42. Door seat cards are blocked by Q51, and the desk/shelf lookup cards are unblocked. Report only. |

## Checks run (real output)

`/tmp/k5c` is a `git clone -b build` of the repo at `18b9cfa`, with full history. Hostile copies were fresh clones of `/tmp/k5c` (`/tmp/k5h`, `/tmp/k5r`). The published copy was cloned to `/tmp/k5p` (local clone), `/tmp/k5g` (`--no-local`), and `/tmp/k5gh` (from `https://github.com/Amalgamour/Workshop`, branch `prima/build`, read only).

**`node kernel/build.mjs --check`** (`/tmp/k5c`): exit 0.
```
finding  00.00.00.0051.01.draft.md: 04 full-address: why missing (4.7)
... (59 findings, all "why missing (4.7)")
checked  books/00.00.00.book  50 entries
checked  books/00.00.axioms.jsonl  7 entries
checked  books/10.00.00.book  1 entries
checked  books/10.11.00.book  1 entries
checked  books/10.11.21.book  15 entries
59 findings, 0 errors
```
The shared working tree at `c7bb4d6` gives the same: `59 findings, 0 errors`.

**17 seats, each blob equal to `git rev-parse HEAD:<path>`** (read from the `approved-by` entries in `books/` at `18b9cfa`):
```
00.00.00.0051.05.02 MATCH 7dbf70bd22af1bf0354edd82aff3ddb405ef892d kernel-trial-4.md@4b369fa
00.00.00.0052.05.01 MATCH 7993b14b830d12feb5a54509b41e74c931afe334 kernel-trial-4.md@4b369fa
00.00.00.0052.05.02 MATCH c82b1fc6d2d3d6ce6e5a44cf99cbc7bf93b62332 kernel-trial-4.md@4b369fa
00.00.00.0053.05.01 MATCH 77ee148ffd645b15b4aeeb1401ff6b72e05a35da kernel-trial-4.md@4b369fa
00.00.00.0053.05.02 MATCH 8499872db0d7551309befdbf12ce1d1c7fa821c4 kernel-trial-4.md@4b369fa
00.00.00.0055.05.01 MATCH 6582d3e56495ca93203e81871659da0481550d41 kernel-trial-4.md@4b369fa
00.00.00.0055.05.02 MATCH 596aa9ba0befffa6f9f6ca93364b9a6fea426478 kernel-trial-4.md@4b369fa
00.00.00.0056.01    MATCH 112c169ccd06d54c6d9ab607fee6c2d16004cc62 kernel-trial-2.md@ed82086
00.00.00.0056.05.01 MATCH 0914ebb8274c3e049440e11388b69da2b138f447 kernel-trial-4.md@4b369fa
00.00.00.0056.05.02 MATCH 93178adddeb2ec915a2c5d4cc070d0dc50c03d37 kernel-trial-4.md@4b369fa
00.00.00.0057.05.01 MATCH 67b3b9b6762af70a7494893fb7ff47e4e86e4281 kernel-trial-4.md@4b369fa
00.00.00.0057.05.02 MATCH 037eec2ff5e9c6c18020f06679358a13e9a62bb1 kernel-trial-4.md@4b369fa
00.00.axioms.05.02  MATCH 452be16b0536002a12279c5d485c68c5217fa6c8 kernel-trial-4.md@4b369fa
10.11.21.0012.05.01 MATCH 9aaed75fc8f0594a1289fa83e870a474d4d021d2 kernel-trial-4.md@4b369fa
10.11.21.1001.01    MATCH 5415cef2dd0a37f3c2ba4c9b6d2652262f0ef82d kernel-trial-2.md@ed82086
10.11.21.1001.05.01 MATCH 566071064f63a5c85fcb3bd87d9e375717bdbf51 kernel-trial-4.md@4b369fa
10.11.21.1001.05.02 MATCH 2aa3490239620604ce1bb13c34841a60ac8f7056 kernel-trial-4.md@4b369fa
seats 17
```

**`node kernel/build.test.mjs`** (`/tmp/k5c`): 26/26 `ok`, `all passed`, exit 0. This includes the 6 pass-6 step 1 tests and the new "R22: seating a 06 note counter is refused (K4 HK)".

**`CARGO_TARGET_DIR=target/k5-trial cargo test --workspace --no-fail-fast`**:
- In `/tmp/k5c` at `18b9cfa` (target dir `/workspace/workshop-build/repo/target/k5-trial`, gitignored by `.gitignore:1`): `EXIT=0`, `38 result lines, passed=409 failed=0`.
- Also in the shared tree: the same `409 passed, 0 failed`, exit 0.
- Includes `seqpage tests/face00.rs: 9 passed`, `trial-compute tests/binary.rs: 2 passed`, `trial-core tests/rules_hostile.rs: 20 passed; 2 ignored`.

**Published copy (part C), `node kernel/build.mjs --check`:**
- `/tmp/k5p`, a local clone of `publish` at `0665a54` (the publish copy of `18b9cfa`): **exit 1, `17 errors; nothing written`**. Every seat gets: `ERROR 00.00.00.0051.05.02.md: seat cites trial docs/trial/kernel-trial-4.md at commit 4b369fa, which is not an ancestor of HEAD; a trial must be on this branch's history (TRIAL-K4 finding 4, Q52 c)`. The other 16 are the same, citing `4b369fa` or `ed82086`. (The old ids still resolve here because `publish` keeps an `incoming` branch and `refs/original/`; see the observations.)
- `/tmp/k5gh`, a GitHub clone of `prima/build` at `0665a54`: **exit 1, 17 errors**, now worded `... at commit 4b369fa, which git cannot find; the seat is blocked`.

### Hostile seat tests (part B, scratch clones only)

| # | Hostile change | Result |
|---|---|---|
| H1 | append a line to seated `0051.05.02.md`, keep the seat | refused: "seated face changed since its trial" |
| H2 | same, and re-pin `seat-05.02` to the new blob citing the same trial | refused: "trial ... passed ... at blob 7dbf70bd..., not this blob" |
| H3 | seat line `blob: 7dbf70bd` (prefix) | refused: "is a short prefix" |
| H4 | commit a forged `docs/trial/kernel-trial-fake.md` with a full-blob PASS line for draft `0051.05.01`, then seat it citing that commit | **accepted**, exit 0 (finding 4) |
| H5 | edit the real `kernel-trial-4.md` to add a PASS line for `0051.05.01`, commit, and cite `kernel-trial-4.md@<new commit>` | **accepted**, exit 0 (finding 4) |
| H6 | uncommitted `## R99` naming the face in a seat line; seat with `approved-by: director; ruling: R99` | refused: "not in DIRECTOR-RULINGS.md as committed at HEAD" |
| H7 | the same R99, committed | **accepted**, exit 0 (finding 4) |
| H8 | trial committed on a side branch, cited from `build` | refused: "not an ancestor of HEAD" |
| H9 | seat note `0051.06.01` with a real committed trial | refused: "a 06 counter may not be seated: R22 allows only face 05 counters" |
| H10 | `rm -rf books`, then un-seat `0051.05.02` (rename to `.draft`) with no record | refused: "was seated ... in the last build but is not now; write unseat-05.02" |
| H11 | un-seat `0051.05.02` with no record; remove its line from `books/00.00.00.book`; commit | before the commit: refused. **After the commit: exit 0**, and a rebuild plus commit stays clean (finding 3) |
| H13 | un-seat with `unseat-05.02: 7dbf70bd` (prefix only, no reason) | **accepted**, exit 0 (finding 5) |
| H14 | delete all of page `0051` | refused: "00.00.00.0051.05.02 was seated ... in the last build but is not now" |
| H15 | `GIT_DIR=/tmp/k5evil/.git` (another clone holding a forged trial commit) with a changed seated face | **accepted**, exit 0. Without `GIT_DIR`: refused, "git cannot find" (finding 2) |
| H16 | delete `docs/trial/kernel-trial-4.md` from the working tree | refused, 15 errors: "which does not exist" |
| H17 | `approved-by: Build-stage (R2)` (case change) | refused: "is not in the R2 form" |
| HR | **`git replace` the blob of `kernel-trial-4.md` at `4b369fa` with a copy whose PASS line names the changed `0051.05.02` blob; edit the seated face; re-pin `seat-05.02` to the new blob, still citing `kernel-trial-4.md@4b369fa`** | **accepted**: `node kernel/build.mjs` exit 0, `59 findings, 0 errors`. The book shows `"approved-by":"build-stage (R2)","trial":"docs/trial/kernel-trial-4.md@4b369fa blob 49205ad5..."` over the changed body. The same tree with `GIT_NO_REPLACE_OBJECTS=1` is refused (finding 2) |

## Findings

### 1. major: no seat verifies in the published copy, because seats cite local commit ids
- **Evidence:**
  - Seat lines cite `docs/trial/<file>.md@<commit>`, for example `00.00.00.0051.00.draft.md:11` `@4b369fa`, and `0056.00.draft.md:11` `@ed82086`.
  - `verifySeat` reads the trial at that commit and requires it to be an ancestor of HEAD (`build.mjs:198-200`).
  - The publish copy is filter-branched to drop `target/`, so every commit id changes. `4b369fa` is `45398a1` there.
  - A clone of `publish`, and a clone of GitHub `prima/build`, both fail `--check` with 17 errors (above).
- **What still matches:** the trial file's own blob is the same in both histories. `git rev-parse 4b369fa:docs/trial/kernel-trial-4.md` (local) equals `git rev-parse HEAD:docs/trial/kernel-trial-4.md` in `/tmp/k5p`: `a5d253d5e12722956afea38e79cb7fc1cf492c7b`. The face blobs also match.
- **Breaks:**
  - R2 (`:9`): "so every such seat can be found and re-reviewed later". Anyone reviewing from GitHub sees a build that refuses every seat.
  - Any CI on the published branch fails.
- **Fix direction (builder lane, not done):**
  - Pin the trial by content, not by commit: `trial: docs/trial/kernel-trial-4.md#a5d253d5e12722956afea38e79cb7fc1cf492c7b`.
  - The guard then checks that some ancestor of HEAD has that path at that blob (`git log --format=%H HEAD -- <path>` plus `git rev-parse <c>:<path>`, or `git rev-list HEAD --objects`) and that its PASS list names the face at the full blob.
  - Blob ids survive filter-branch; commit ids don't.
  - For the existing 17 seats, either re-pin them in this form (face 00 is a draft, so no seat breaks), or accept `@<commit>` as a fallback when the commit is missing, as long as an ancestor has the trial file whose PASS list matches.
  - Add a test that filter-branches a scratch clone and runs `--check`.
  - Raised as Q53.

### 2. major: the local guard can be fooled without any commit, through `git replace` or `GIT_DIR`
- **Evidence:**
  - Every git call is `spawnSync('git', ['-C', ROOT, ...a])`, using the caller's environment and the repo's replace refs (`build.mjs:150`).
  - HR: `git replace <real trial blob> <forged blob>` makes `git show 4b369fa:docs/trial/kernel-trial-4.md` return the forged PASS list. A changed seated face then builds clean while citing the real trial commit.
  - The replace ref is in `refs/replace/`. It is not in any commit, `git log` doesn't show it, and `git status` shows only the face and seat-line edits.
  - H15: `GIT_DIR` pointed at another repo passes `hasGit()` (`:151-153`, the toplevel is still `ROOT`) and serves that repo's history.
- **Breaks:** R2 and axiom 9 on the shared box, where the local `--check` is the gate before commit and publish. It is the same class as TRIAL-K4 finding 1 (a seated face changed and still "seated"), now without the 2^32 search.
- **Limits:** a fresh clone (or the published copy) has no replace refs, so a committed result of HR fails there. That is why this is major and not a blocker.
- **Fix direction (not done):**
  - Run git with `--no-replace-objects` (or `GIT_NO_REPLACE_OBJECTS=1`).
  - Clear `GIT_DIR`, `GIT_WORK_TREE`, `GIT_INDEX_FILE`, `GIT_OBJECT_DIRECTORY`, `GIT_ALTERNATE_OBJECT_DIRECTORIES`, `GIT_NAMESPACE` and `GIT_CONFIG_*` in the child environment.
  - Make it an error if `git replace -l` lists anything or `.git/info/grafts` exists.
  - Add tests for HR and H15.
  - Raised in Q54.

### 3. minor: a committed edit to books/ still hides an un-seat
- **Evidence:** `priorSeats()` reads only `HEAD:books/` (`build.mjs:212-222`). In H11, the books line for `0051.05.02` was removed in a commit, and the next build found no past seat, so no `unseat-05.02:` was needed.
- **Breaks:** the comment at `build.mjs:211` ("so deleting or editing books/ hides nothing"), and R2's "every seat can be found". The removal is findable only in `git log -p books/`.
- **Fix direction:** collect past seats from history, not one snapshot. Every `seat-NN:` or `seat-00:` line ever added on an ancestor (`git log -p HEAD -G'^seat-' -- kernel/`) that is not now present needs an `unseat-` record. Raised in Q54.

### 4. minor: a forged trial or ruling that is committed on the branch is still accepted (TRIAL-K4 finding 4 residue)
- **Evidence:** H4 (new file), H5 (a PASS line added to the real `kernel-trial-4.md` in a later commit) and H7 (a committed `R99`) all build clean.
- **Effect:** each forgery is findable in git (R2 `:9`). H5 is the worst, because it looks like a seat on a real trial.
- **Fix direction (cheap and partial):**
  - Make trial files write-once: error if the cited path has any commit after the one that added it (`git log --diff-filter=M --format=%H -- <path>` not empty), or if the cited commit is not that adding commit.
  - Require the trial commit to touch only `docs/trial/` and `kernel/QUESTIONS.md`.
  - Make it an error if a commit that changes `DIRECTOR-RULINGS.md` also changes `kernel/`.
  - None of this proves who wrote a file. Raised in Q54.

### 5. minor: an un-seat record needs only an 8-hex prefix and no reason
- **Evidence:** `build.mjs:233-235` accepts any `unseat-NN:` text that contains `p.blob.slice(0, 8)`. In H13, `unseat-05.02: 7dbf70bd` (no reason) built clean.
- **Breaks:** the builder's own message asks for "<reason>; was blob ..." (`:234`). R2 re-review needs the reason. Seats now pin 40 hex digits, so the un-seat record should too.
- **Fix direction:** require the full old blob and some text besides it.

### 6. minor: the 0054 pack's outcome names seqpage and the builder, but no card covers them
- **Evidence:**
  - `0054.05.02:6` outcome: "the builder, core and seqpage read one list".
  - The only cards for the lists are w01 (`:25-26`, "core PAGE_TYPES matches", path `face.rs`) and w02 (card types: 0054.02, `build.mjs` CARD_TYPES, `seqaddr-core`).
  - `crates/seqpage/src/face00.rs:70` keeps its own page-type list (`TYPES`, with per-type registry fields: the R19 fields w01 is about), and no card or done test names it.
  - The builder has no page-type list at all (it does not check the stamp `type`).
- **Breaks:** R22: the pack must reach the page's MVP. This is the same class as TRIAL-K4 finding 15 ("the outcome's ... has no card").
- **Fix direction:** add `crates/seqpage/src/face00.rs` TYPES to w01's path and done ("core PAGE_TYPES and seqpage TYPES name the same types"). Either add a builder check of stamp `type`, or drop "the builder" from the outcome for page types.

### 7. minor: the 0013 pack's w01 done covers only half its title, and the app has no card
- **Evidence:**
  - w01 title: "rule the page number and the question card fields" (`0013.05.02:21`). Its blocker Q49 asks about both (`QUESTIONS.md:256-259`).
  - Its done (`:25`) tests only the card fields on 0054.02. If Q49 option B moves the page, nothing checks the move: the files, `crates/ask`, or the app's `READER_BOOK.0013` (`BUILD-LOG.md:161`).
  - The outcome (`:6`) says "end to end ... through /ask and the app". w02 tests `/ask` only, and no card covers the app.
- **Breaks:** R22 (the pack reaches the page's MVP), and the TRIAL-K4 standard of a concrete done test.
- **Fix direction:**
  - w01 done: "the common-questions page sits at the ruled number in books/, crates/ask config and the app's READER_BOOK page, and 00.00.00.0054.02 lists the question card type with its fields".
  - Add an app card (for example an app test or check that the Ask screen shows `bob` for "what is my name"), or drop "and the app" from the outcome.

### 8. minor: the pass-6 merges are not logged on their pages
- **Evidence:**
  - The three law edits in `18b9cfa` (`0051.01:53`, `0052.01:87`, `0052.04:92`) are logged only in `docs/BUILD-LOG.md:175-176`.
  - `0052.06.01` still records the pass-5 R22 merge result ("A counter of a counted face may be seated under R2 ...") as the current text, and that text was replaced in pass 6.
  - BUILD-LOG gives the reason: the 06.01 notes are HELD-7. But HELD-7 is a trial verdict, not a ban on editing a draft note.
- **Breaks:** axiom 6 (lineage is kept with the piece) and drafting.md:34-35 ("Every change traces to a note"; "The log keeps every note and merge"). drafting.md enforcement is proposed (`:3`), and the change can be traced through BUILD-LOG, so this does not change the 0052.01/.04 verdicts.
- **Fix direction:** copy the three BUILD-LOG merge lines into `0051.06.01` and `0052.06.01` in the next pass.

### 9. minor (class, no verdict change): pack grants do not cover the paths their own cards name
- **Evidence:**
  - `0054.05.02:9` grant: "kernel/00.00.00/00.00.00.0054.*.draft.md (faces 01, 02, 04 only ...); books/...". But w01 and w02 paths name `crates/seqaddr-core/src/face.rs`, `kernel/build.mjs` and `docs/spec/face00.md` (`:25-26`, `:36`), and w05 writes `0054.00` (`:66`).
  - `0012.05.02:9`: grant "(not face 00 or 05)", yet w05's path is `10.11.21.0012.00.draft.md` (`:66`), and w02's is `crates/compute/tests/` (`:36`).
  - The same pattern is in already-seated packs: `0053.05.02:9` vs `:26` (`crates/seqaddr-core/`), and `0055.05.02:9` vs `:26` and `:56` (`kernel/build.mjs`, `crates/compute/`).
- **Breaks:** `workflow-loop.003.md:237` (pack lint, hard): "intended targets and operations are inside the grant". `.003` is a draft (O7), and the trial and seat steps may be meant for other lanes, so this is a class question, not a verdict.
- **Raised as Q55.**

**Observations (no severity):**
- `00.00.axioms.05.01:16` says TRIAL-K3 found C3.2 unchecked on the axioms, but not that pass 5 (`7b08cbf`) fixed it (`build.mjs:310`, test "an axioms 01 card with no 04 card is refused (H3)"). True as history. Say "fixed in 7b08cbf" in the next 05 counter.
- `0012.05.02` w02 (`:35`): the `bob` half is already covered by `crates/compute/tests/http.rs:258` (`brands_and_cards_on_real_books`); `cats` is not.
- `0051.01:53`: "0020-0099 are working pages (R17)" uses the Read line of R17 (`DIRECTOR-RULINGS.md:69`), not the Director's words ("aren't just locations", `:68`). That is fine as a reading.
- **Publish copy hygiene:** `/workspace/workshop-build/publish` holds `refs/heads/incoming` (the unfiltered local history, so `4b369fa` is reachable there) and `refs/original/refs/heads/build`. Both carry `target/` history. A `git push --all` or `--mirror` would publish it. Push only `build:refs/heads/prima/build` as now, or delete `incoming` after each cherry-pick.

## Per-face verdicts

| Face | Blob (HEAD `18b9cfa`) | Verdict | Findings / open question |
|---|---|---|---|
| `00.00.00.0051.01` | `aba5a58a9072f8467b55ff2944927e75662e9aeb` | HELD-7 | K4 finding 8 landed (`:53`). Book Layout (`:184-197`) still shows five rows below 0100 as settled, while its own R17 note (`:201`) says the four-way split is `7`. That is Q30, the same hold K4 put on `0051.04`. Finding 8 (lineage). |
| `00.00.00.0051.05.01` | `c160a4da9947eeeb3de88b512208ee9e7836011b` | PASS | `:13` matches `kernel-trial.md:58`. Re-checked: `:10-12`, `:14-17` (`d37e532` is TRIAL-K3; `DESIGN.md:57`; 20/28 `why: 4.7` on 0051.04). |
| `00.00.00.0052.01` | `88bce491bb2bffe645a5c6825096f41d8b86080f` | PASS | `:87` narrows the law to face 05 and leaves Q35 open. Q32 (`:41`) is only quoted as open, so no hold. Finding 8 noted. |
| `00.00.00.0052.04` | `e9ca59a1d708acfd57b9e5f7e6b758e41e4fde6f` | PASS | `:92` agrees with `0052.01:87`. Its `why: 4.7` hole is a required absence. |
| `00.00.00.0054.05.01` | `aa07b61116572c9e25353a5e7f3b6ed97941d2a0` | PASS | Symbols are correct. `face.rs:99-111` is the CARD_TYPES array (`work`, no `question`). 2/3 `why: 4.7`. TRIAL-K3 `0054.00` HELD on Q33/F2/Q39 (`kernel-trial-3.md:212`). O35 is at `OPEN.md:241`. |
| `00.00.00.0054.05.02` | `637477074886e940eeee38fa8afccdccaa316588` | FAIL | 6 minor; 9 (class) |
| `00.00.axioms.05.01` | `cbf5cba0d5429e2e0b14e56f5ed8a1eba1d06ad2` | PASS | `:10` R6 quote is `DIRECTOR-RULINGS.md:25`. `:12` matches `drafting.md:40`. `:13` decisions.md:548 is cited by 9 of the 10 cards on axioms.04. `:15` checks out (`Axioms.md:3`, `decisions.md:531`, no `axioms/` in `docs/spec`). Observation on `:16`. |
| `10.11.21.0012.05.02` | `dd89a5199d1a0b47f5cac3bce2ec0e8185ff1ce6` | PASS | Every outcome part has a card. Each done is decidable by a file check or command. Order: w01, then w03, then trial w04, then seat w05 (blocked by Q35). D64, D68, D69 are on topic. Finding 9 (class), observation on w02. |
| `10.11.21.0013.05.01` | `16146a0fa073fc947138de43033f9e9a2b75ac09` | PASS | D147/D267/D271/D290 are on topic. `:11` matches `BUILD-LOG.md:138-139`. `:13` matches `:161`. |
| `10.11.21.0013.05.02` | `ed8b4f7ad210b1cd92923f8843359676ed801916` | FAIL | 7 minor; 9 (class) |

**What a PASS on a 05.02 pack checked** (as TRIAL-K4):
- Every header field of `workflow-loop.003.md:238` is present.
- Every work card has `reason`, `depends`, `blocked-by`, a decidable `done:`, and a `path`.
- The order is fix, then fill, then trial, then seat.
- Every part of the `outcome:` has a card.
- `design:` names a real DESIGN.md section and real DECISIONS ids on the topic.
- No card seats its own work, uses an override (R21), or answers an open Director question.

**What a PASS on a 05.01 counter checked:** every line was traced to its cited source (trial finding, commit, BUILD-LOG line, spec line, code symbol) and recounted where it gives a number.

## Method
- **Repo state:** the shared working tree was only read, apart from one `node kernel/build.mjs --check` (which doesn't write). One slip: a module import I used to test this file's PASS list also ran the builder once in write mode. It rewrote `books/` with identical bytes, and `git status` showed no change. My only writes are this file and Q53-Q55 in `kernel/QUESTIONS.md`.
- **Scratch copies:**
  - `/tmp/k5c` (clone at `18b9cfa`);
  - `/tmp/k5h` and `/tmp/k5r` (fresh clones per attack; script `/tmp/k5-hostile.sh`);
  - `/tmp/k5evil` (H15);
  - `/tmp/k5p`, `/tmp/k5g` and `/tmp/k5gh` (published copy).
- **Cargo target:** `target/k5-trial` (gitignored).
- **Blobs:** each is `git rev-parse HEAD:<path>` at `18b9cfa`, written in full and unchanged at `c7bb4d6`. Renaming `.draft.md` to `.md` to seat a face does not change its blob.
