# Kernel trial 10 (TRIAL-K10): hostile pass on kernel pass 11, the Q63 structured seat read and books/ join, the live face 00 seat rules, Q64, Q65 and Q66, and the published copies

Lane TRIAL-K10, 2026-11-11, about 5:50-6:10 PM CST (6:50-7:10 PM EST). I'm a fresh session that did not build pass 11 or these faces. Under R20 (`DIRECTOR-RULINGS.md:78-80`) that counts as a different view (`DIRECTOR-RULINGS.md:7-9`, R2).
I only report. Nothing in `kernel/` (except Q67-Q69 in `kernel/QUESTIONS.md`), `books/`, `crates/` or `app/` was changed, nothing was seated or un-seated, nothing was pushed, merged or deleted. New questions are tagged `[TRIAL-K10]`. This report does not approve any seat.

**Target (pass 11: `bbdc1a9` builder and tests, `3092f7b` BUILD-LOG and QUESTIONS; the shared branch was at `10d6a70` (R25) when I started; between them only rulings and 04-draft lanes landed: `5f2f43d` R23, `d4b46ae` TRIAL-WHYS-2, `385052b` R24, `10d6a70` R25; none touches `kernel/build.mjs`):**
- A) the pass 11 guard: Q63 (past seats only from structured fields; the retiring version is skipped; newest face 00 history seat and newest `books/` `approved-by` are both read and both must be named; a last-seat blob git does not hold is "made up"), the four new live face 00 rules, Q64 (books read in any mode; a current book must be 100644), Q65 (`-z` walks; updated "not followed" list; the 16-hop message), Q66 (un-seat records count as seat records); plus the 26 seats;
- B) no new faces to seat;
- C) portability: a `--no-local --single-branch` clone of `/workspace/workshop-build/publish` and a clone of GitHub `prima/build`.

**Judged against:** `DIRECTOR-RULINGS.md` R1-R25, `kernel/QUESTIONS.md` (Q63-Q66), `docs/BUILD-LOG.md` (pass 11 entry, `:259-270`), `docs/trial/kernel-trial-9.md`, `kernel/build.mjs`, `kernel/build.test.mjs`.
**Rules used:** Q41 is applied, not held. R25 answers Q51 (face 00 is the registry root, not seated the same way), so no face 00 is judged for a seat.

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
| major | 1 (finding 1: "newest" seat is not the last seat. DO: after a re-seat, a merge with a future-dated copy of an old commit makes the un-seat record name only the *older* real seat, with every commit's tree building clean; F1: one never-built commit that rewrites both the face 00 seat line and the book line makes the record name any blob git holds. Both build clean in a fresh clone) |
| minor | 4 (finding 2: a live face 00 may hold `unseat-NN:` beside a still-seated face, which blinds the face 00 history side for that face; finding 3: the "made up" check accepts an unreachable loose object locally; finding 4: test K4 HG hard-codes `R23` as a fake ruling, R23 is now real, so the suite is 66/67 at `3092f7b` and later; finding 5: the forged-trial and gitfile residues, unchanged) |

**PASS list, eligible for an R2 seat:** none this pass (no face changed).

**Plain words:** every TRIAL-K9 attack that pass 11 said it closed is closed: the prose decoy (D2), the stamp decoy (D1), the executable book (A1 755), the quote, backslash and accented-letter paths, and the un-seat kept only on disk (Q9). The four new face 00 rules each refuse their case. The 26 seats check out here, in a scratch copy of the publish repo and on GitHub. I found one real hole, in a new shape. Pass 11 asks for "the newest seat" in two histories, and "newest" just means "first in `git log` output". `git log` orders by commit date, and a merge can bring in a side commit with a date in the future. So once a face has been seated twice (R24 makes re-seats normal), an un-seat can name the old seat instead of the one being pulled, and every commit in the branch still builds. A cruder version needs one commit that never built, which rewrites both the face 00 line and the book line to some other blob. The small ones: an `unseat-NN:` line may sit beside a face that is still seated; the "git holds this blob" test also counts a loose object that a fresh clone would not have; and one old test now fails only because R23 became a real ruling.

## TRIAL-K9 fixes: did they land?

| K9 # | Landed? | Evidence |
|---|---|---|
| 1 major (D1, D2: made-up seat line sets the un-seat blob) | yes for D1 and D2; the class is open (finding 1) | `seatFields` reads only the stamp and the `## Registry` field block (`build.mjs:383-399`); `blobSeats` skips the retiring version (`:403-415`); `priorSeats` joins the newest `books/` blob (`:538-550`); `unseatChecks` refuses a blob git does not hold (`:571`). D2 and D1 below are refused. F1 and DO beat the "newest" rule (finding 1). |
| 2 minor (A1 755) | yes | `isBook` mode check at HEAD and index (`:513-519`), executable-on-disk check (`:811`), history read in any mode except 160000 (`:531`). A1 755 refused with 4 errors; A1 755 flipped back to 644 still asks for `unseat-01` (history holds it). |
| 3 minor (quoted paths) | yes | every walk `--raw -z` read by `rawZ` (`:234-246`); `lsZ` for ls-tree/ls-files. L-quote, L-backslash, L-nonascii, L-dirlink_kq caught, and four new path shapes (newline, a leading newline plus `C <hex>`, tab, `:100644 ...`) caught. |
| 4 minor (un-seat-only face 00) | yes | `carries` counts `unseat-*` and a stamp `unseat-00:` (`:642`). Q9 refused: "face 00 ... is blob 2b232d46... in git (HEAD), not the bytes on disk 64549dad...". |
| 5 minor (forged docs-only trial; gitfile swap) | still open, as admitted | DO and A1 used forged docs-only trials to make seats (`seats 27`). GF not re-run (no code on that path changed). Not worse. |

## Checks run (real output)

`/tmp/k10/repo` is a fresh `git clone --no-local -b build` of the shared repo at `10d6a70` (full history). Each hostile copy is a fresh `--no-local` clone of it under `/tmp/k10/<name>`; helpers `/tmp/k10/lib.sh`, `/tmp/k10/links.mjs` (K9's script plus four cases), `/tmp/k10/seat01.sh`, `/tmp/k10/dateorder.sh`, `/tmp/k10/seats.sh`. The builder strips every `GIT_*` variable and runs `--no-replace-objects`; my scripts unset `GIT_DIR`, `GIT_WORK_TREE`, `GIT_OBJECT_DIRECTORY`, `GIT_ALTERNATE_OBJECT_DIRECTORIES`, `GIT_INDEX_FILE`. No clone has replace refs, grafts, or a shallow history.

**`node kernel/build.mjs --check`** (`/tmp/k10/repo`, `10d6a70`): exit 0.
```
finding  ... (48 findings)
checked  books/10.11.00.book  1 entries
checked  books/10.11.21.book  15 entries
seats 26
48 findings, 0 errors
```

**`node kernel/build.test.mjs`:**
```
bbdc1a9 (worktree): 67 ok, all passed
3092f7b (worktree): 66 ok; FAIL  R2: a director seat citing an uncommitted ruling is refused (K4 HG)
10d6a70 (/tmp/k10/repo), publish 9e4e37b, GitHub 9e4e37b: 66 ok, the same FAIL, exit 1
```
The FAIL is finding 4: the test appends a fake `## R23` and expects "R23 ... is not in DIRECTOR-RULINGS.md as committed at HEAD", but R23 is now a real ruling (`5f2f43d`), so the builder says "R23 does not name 10.11.21.0013.01" instead. Still refused. With an unused number (`R99`, scratch `/tmp/k10/hg`) the original message comes back: "seat cites R99, which is not in DIRECTOR-RULINGS.md as committed at HEAD; the seat is blocked". The guard holds; the test is stale.

**Cargo:** not re-run; pass 11 changed only `kernel/build.mjs` and `kernel/build.test.mjs`.

**26 seats, each seat blob equal to `git rev-parse HEAD:<path>`, each mode `100644`, each a regular file on disk equal to its HEAD blob, each cited trial blob held by git** (read from the `seat-NN:` lines of the face 00 files at `10d6a70`, `/tmp/k10/seats.sh`):
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
26 of 26 OK; the same 26 blobs as TRIAL-K9.

### Part C: portability (real output)

**C1. `git clone -q --no-local --single-branch -b build /workspace/workshop-build/publish /tmp/k10/pub`** (the real publish dir was only read):
```
HEAD 9e4e37b 2026-11-11 17:46:41 -0600 Director ruling R24 ...   tree 7ded5feb508bd95370872a2aeaa4ef6c2daf2dec
local 385052b^{tree} 7ded5feb508bd95370872a2aeaa4ef6c2daf2dec   (equal)
bbdc1a9 absent (publish history is rewritten; seats cite blobs, not commits)
--check: exit 0, "seats 26", "48 findings, 0 errors"
seats.sh: 26 / 26 OK, the same 26 blobs as the repo
node kernel/build.test.mjs: 66 ok, 1 FAIL (K4 HG, finding 4)
```
Publish is one commit behind the shared branch (R25 `10d6a70` is not published yet); R25 touches only `DIRECTOR-RULINGS.md`.

**C2. `git clone -q --single-branch -b prima/build https://github.com/Amalgamour/Workshop.git /tmp/k10/gh`:**
```
HEAD 9e4e37b   tree 7ded5feb508bd95370872a2aeaa4ef6c2daf2dec (= local 385052b)
--check: exit 0, "seats 26", "48 findings, 0 errors"
seats.sh: 26 / 26 OK, the same 26 blobs as the repo
node kernel/build.test.mjs: 66 ok, 1 FAIL (K4 HG, finding 4)
```
Only `prima/build` was cloned; the `claude` branch was not touched.

### Hostile tests (part A, scratch clones only)

`R` = the real seat of `10.11.21.0013.05.02`, `24a27e08bfb78ff75b1f7a2b91e82e2956a1163f` (trial `kernel-trial-7.md`). "Un-seat" = rename `0013.05.02.md` to `.draft.md`, `faces: ... 05.02 draft`, replace `seat-05.02:` with `unseat-05.02: <record>` and a `why-05.02:`, stage, write build, commit everything.

| # | Hostile change | Result |
|---|---|---|
| D2 (K9) | one commit: un-seat with `was blob 2c338d1d...` and a prose `seat-05.02: ... blob: 2c338d1d...` line at the end of face 00 | **closed**: write mode and `--check` refuse: "unseat-05.02: must name the full old blob 24a27e08... (the last seat ... in face 00 history ...)" |
| D2 control | the same with `was blob R` | builds: `seats 25`, 0 errors (the prose line is ignored, as Q63 says) |
| D1 (K9) | step 1: stamp `seat-05.02: ... blob: 2c338d1d...` committed | **closed**: step 1 refused: "stamp has seat-05.02:; a seat record for face 05.02 lives on the registry"; step 2 (un-seat naming the fake) refused, asks for `24a27e08...` |
| LR-repeat | `seat-05.02:` line written twice | refused: "seat-05.02: is written more than once" |
| LR-notseated | registry `seat-04:` (04 is a draft), committed | refused: "registry has seat-04:, but 04 is not listed as seated"; also "10.11.21.0013.04 was seated ... write unseat-04" (the committed line is read as a past seat; fail safe) |
| LR-regseat00 | registry `seat-00:` | refused: "registry has seat-00:; face 00's own seat record lives in the stamp" |
| A1 755 (K9) | `/tmp/k10/seat01.sh 755`: forged docs-only trial seats `0013.01` (`seats 27`), only a `100755` book committed, then pulled back with no record | **closed**: 4 errors (book mode at HEAD, in the index, on disk, and "10.11.21.0013.01 was seated ... write unseat-01: ... was blob bc8cfc48...") |
| A1 755 flip | the same, then `chmod -x` and the book committed `100644` | refused: "10.11.21.0013.01 was seated ... write unseat-01" (the 755 history blob is read) |
| L-quote, L-backslash, L-nonascii, L-dirlink_kq (K9) | K9's link cases (`/tmp/k10/links.mjs`) | **closed**: all CAUGHT ("10.11.21.1001.05.03 was seated ... write unseat-05.03") |
| L-newline, L-lead_nl, L-tab, L-colonmeta (new) | link targets `docs/n<LF>x/f00.md`, `<LF>C deadbeef/f00.md`, `docs/t<TAB>x/f00.md`, `:100644 100644 x` (to confuse `rawZ`) | all CAUGHT |
| L-control, L-space, L-hops3, L-rootlink | as in K9 | all CAUGHT |
| L-hops17 | 19-link chain | fails closed; the message is now right: "a symlink chain in history is longer than 16 hops (the round limit)" (K9 observation closed) |
| L-windows | `..\..\..\docs\w\f00.md` | not followed, exit 0, `seats 26`; now listed in the Q61/Q65 "not followed" list (admitted) |
| Q9 (K9) | page 0012: both seats pulled, records only in an uncommitted face 00; faces and books committed | **closed**: `--check` refuses: "face 00 ... is blob 2b232d46... in git (HEAD), not the bytes on disk 64549dad...; face 00 carries seat records" |
| F1c (pass 11 test shape) | never-built commit A rewrites only face 00's `seat-05.02` blob to `X` = `c82315cc...` (the blob of `0013.04.draft.md`, held by git); B un-seats naming `X` | refused: "must name the full old blob 24a27e08... (... in books/ history ...)" |
| **F1** | **never-built commit A (`bb5308f`) rewrites face 00's `seat-05.02` blob to `X` AND the `0013.05.02` book line's `face blob` to `X` (2 lines, 2 files); B (`3964d6b`) un-seats with `unseat-05.02: pulled back for review; was blob c82315cc...`** | **accepted**: write mode, `--check` exit 0, `seats 25`, **also in a fresh clone** (`/tmp/k10/f1-fresh`). The real seat `24a27e08...` is never asked for (finding 1) |
| F1b | F1 with `Y` = an unreachable loose object (`git hash-object -w`, content "made up face") | local `--check` exit 0, `seats 25`; fresh clone refuses: "names blob de87e66e..., which git does not hold, so that seat line is made up" (finding 3) |
| **DO** | **`/tmp/k10/dateorder.sh` (finished by hand): t1 forged trial; C1 seats `0013.01` at `B1` = `bc8cfc48...` (`seats 27`); t2 forged trial; C2 re-seats it at `B2` = `c78b86e3...` (a changed face, `seats 27`); S = a copy of C1 (same tree, same parent t1) with dates `2030-01-01`; M = a merge of C2 and S whose tree un-seats `0013.01` with `unseat-01: pulled back for review; was blob bc8cfc48...` (B1 only). M's books were written once with `unseatChecks` switched off in a scratch copy of the builder (`kernel/build-x.mjs`, deleted after), then committed** | **accepted**: `--check` exit 0, `seats 26`, **also in a fresh clone** (`/tmp/k10/doc`). The seat being pulled is `B2`; the record names only the older `B1`. Every commit's tree builds (S's tree is C1's). Before M existed, the real builder asked for `c78b86e3...` from both histories (finding 1) |
| U1 | `unseat-05.02: not really; was blob R` added beside the still-seated `seat-05.02:`; books rebuilt and committed | **accepted**: `--check` exit 0, `seats 26` (finding 2) |
| HG | test K4 HG by hand with `R99` instead of `R23` | refused with the original message (finding 4) |

Not repeated: prefix-collision forges, shallow clones, replace refs, grafts, `GIT_*` env, root commits, attributes and textconv, GF (no code on those paths changed in pass 11; covered by passing tests).

## Findings

### 1. major: "the newest seat" is the first one `git log` prints, not the last seat of the face
- **Evidence:**
  - `historySeats` keeps, per address, the first face 00 blob in `git log` output that holds a structured seat (`build.mjs:499-506`). `priorSeats` keeps the first `books/` line with `approved-by` (HEAD's books, then log order; `:538-544`). `unseatChecks` then asks only for those one or two blobs (`:572-573`).
  - `git log` (no `--topo-order`, no `--first-parent`) prints by commit date as it walks. A side parent of a merge with a future committer date is printed before the main line.
  - **DO:** after a real re-seat (`B1` then `B2`), a merge of the re-seat commit with a future-dated copy of the old seat commit makes both walks print the `B1` state first. An un-seat that names only `B1` builds clean: `--check` exit 0, `seats 26`, also in a fresh clone. No commit in the branch is broken: S has the tree of C1, which built. (I used forged docs-only trials only to make the two seats in scratch; real trials work the same.)
  - **F1:** one commit that never built rewrites the face 00 line and the book line to the same blob `X` that git holds (any committed file's blob). The un-seat names `X` and builds clean, also in a fresh clone. Pass 11's own test rewrites only the face 00 line, so the books join catches it (F1c); writing the book line too defeats it.
- **Limits:** DO needs a face that has been seated twice at different blobs (none at HEAD; every seat in history today has one blob). R24 (`DIRECTOR-RULINGS.md:94-97`) makes that the normal path ("reseat an update to 05"). F1 needs a commit that never built in the branch history; nothing checks past commits.
- **Breaks:** Q63's decision "an un-seat record must name the exact full blob of the seat being retired: the last real seat", and its claim "a made-up blob never satisfies it" (`build.mjs:568`). R2 re-review is pointed at the wrong fingerprint. With DO it is a real, older fingerprint, which looks right on sight.
- **Fix direction (builder lane, not done):** Q63 option A taken fully: the record names every distinct seat blob ever seen for that address in face 00 history and in `books/` history (not the first one printed). Or take "last" from a first-parent walk with `--topo-order`, and still name every `books/` blob. Raised in Q67.

### 2. minor: a live face 00 may hold `unseat-NN:` beside a face that is still seated
- **Evidence:** the live rules (`build.mjs:643-655`, the not-seated rule at `:653`) refuse a `seat-NN:` for a non-seated face unless an `unseat-NN:` sits beside it, but nothing refuses an `unseat-NN:` for a face that is still seated. U1: `unseat-05.02: not really; was blob 24a27e08...` beside the live `seat-05.02:` builds clean (`seats 26`). `blobSeats` treats every such version as "retiring" and skips its seat line (`:405-411`), so while the line stays, the face 00 history never records that face's seat, including a re-seat made meanwhile.
- **Limits:** the `books/` history still records every built seat, so the un-seat check still asks for it unless finding 1 is also used.
- **Fix direction:** refuse an `unseat-NN:` for a face listed as seated (or for a face with a live `seat-NN:`). Raised in Q68.

### 3. minor: the "git does not hold it" test counts loose objects that no clone has
- **Evidence:** `git cat-file -e <b>^{blob}` (`build.mjs:571`) is true for an unreachable loose object. F1b with `Y` from `git hash-object -w`: local `--check` exit 0, `seats 25`; a fresh clone refuses ("de87e66e... which git does not hold").
- **Limits:** local only; a fresh clone catches it. A blob in any committed file passes everywhere (F1), so the real fix is finding 1.
- **Fix direction:** require the blob to be reachable from HEAD (for example, present in `git rev-list --objects HEAD`), or drop the test once Q67 is taken. Folded into Q67.

### 4. minor: test K4 HG uses `R23` as its fake ruling; R23 is now real, so the suite fails 66/67
- **Evidence:** `kernel/build.test.mjs:205-208` appends `## R23 - fake` uncommitted and expects "R23, which is not in DIRECTOR-RULINGS.md as committed at HEAD". R23 landed in `5f2f43d` (before `3092f7b`), so the builder answers "seat cites R23, but that ruling does not name 10.11.21.0013.01". 67/67 at `bbdc1a9`; 66/67 at `3092f7b`, `10d6a70`, publish and GitHub `9e4e37b`.
- **Limits:** the guard is fine (R99 gives the expected message). The BUILD-LOG's "67/67" is true only at `bbdc1a9`, not at `3092f7b`, the commit that records it.
- **Fix direction:** use a ruling number that will never be written (for example `R9999`) or compute the next number from the file. Tests are not mine to change. Raised in Q69.

### 5. minor (class, no verdict change): the forged-trial and gitfile residues are unchanged
- DO and A1 made seats with brand-new forged trials in docs-only commits (`seats 27`, 0 errors), as in K8 T13r and K9 A1.
- GF was not re-run; pass 11 did not change the trust or gitfile path.
- Neither got worse. A seat line in a file git never held, a link inside a submodule, Windows `\` link text and non-UTF-8 path names stay "not followed", as listed.

**Observations (no severity):**
- **Hop limit:** fixed; the message now names the 16-hop limit.
- **Stale publish:** publish and GitHub are at `9e4e37b` (= local `385052b`); R25 `10d6a70` (rulings only) is not published yet.
- **Retiring skip works as designed:** a prose or stamp decoy in the same commit as the un-seat is ignored (D2), and a committed registry `seat-NN:` for a draft is read as a past seat (LR-notseated), which fails safe.

## Per-face verdicts

None. No face changed in pass 11, and no face is eligible for a seat.

## Method
- **Repo state:** the shared working tree was only read. My only writes are this file and Q67-Q69 in `kernel/QUESTIONS.md`, committed by pathspec (the index was empty first). The builder was never run in the shared tree.
- **Scratch copies:**
  - `/tmp/k10/repo` (fresh `--no-local` clone at `10d6a70`), with worktrees `/tmp/k10/wt-bbdc1a9` and `/tmp/k10/wt-3092f7b` for the test counts;
  - `/tmp/k10/<test>` (one fresh clone per attack; `f1`, `f1b`, `f1c` (the F1c control), `do`, `d1`, `d2`, `d2ok`, `lr-*`, `a755`, `q9`, `u1`, `hg`, `L-*`) and a fresh clone of each final state (`<test>c`) for the "fresh clone" rows (`f1-fresh` for F1, `f1bc`, `doc`);
  - `/tmp/k10/pub` (publish, `--no-local --single-branch`) and `/tmp/k10/gh` (GitHub `prima/build`).
- **Publish copy:** read only. Nothing fetched into it, deleted or pushed.
- **Blobs:** each is `git rev-parse HEAD:<path>` at `10d6a70`, written in full.
