# Kernel trial 4 (TRIAL-K4): hostile pass on kernel pass 5, the R22 face 05 counters, and the seat guard

Lane TRIAL-K4, 2026-11-11, about 4:20 PM EST. I'm a fresh session that did not build these faces. Under R20 (`DIRECTOR-RULINGS.md:78-80`) that counts as a different view, so a PASS here can qualify a face for an R2 seat (`DIRECTOR-RULINGS.md:7-9`).
I only report. Nothing in `kernel/`, `books/` or `app/` was changed, nothing was seated, nothing was pushed. New questions go to `kernel/QUESTIONS.md` as Q51-Q52, tagged `[TRIAL-K4]`.

**Target (HEAD `7b08cbf`):**
- A) the 9 faces kernel pass 5 changed (`7b08cbf`): `0051.01`, `0051.04`, `0051.06.01`, `0052.01`, `0052.02`, `0052.04`, `0052.06.01`, `0057.04`, `0057.06.01`, plus `0057.01` (failed in TRIAL-K3 only because its 04 disagreed);
- B) the 22 face 05 counters from PACKS (`0823ae3`): `05.01` and `05.02` on `00.00.00.0051`-`0057`, `00.00.axioms`, `10.11.21.0012`, `.0013`, `.1001`; the 8 parked door packs are reported only (R10);
- C) the builder's seat checks (`kernel/build.mjs:126-283`, `kernel/build.test.mjs`).

**Judged against:** `DIRECTOR-RULINGS.md` R1-R22, `docs/spec/face00.md` (DRAFT), `kernel/QUESTIONS.md`, `docs/design/DECISIONS-LOG.md`, `docs/trial/kernel-trial-3.md`.
**R22 rule used:** a face 05 counter may be seated under R2. Q41 (which reading of R22), Q44 (05 or 06 for "what we learned") and Q45 (what authorizes a pack) are the same R22 family. None of them changes the text of a 05 counter, so none of them holds one. A face whose verdict really depends on another open Director question is HELD-7.

## Summary

| Verdict | A (pass-5 faces) | B (face 05 counters) | Total |
|---|---|---|---|
| PASS (eligible for an R2 seat) | 0 | 15 | 15 |
| FAIL | 3 | 7 | 10 |
| HELD-7 (depends on an open question) | 7 | 0 | 7 |
| **total** | **10** | **22** | **32** |

| Severity | Findings |
|---|---|
| blocker | 0 |
| major | 3 (all in the seat guard, part C) |
| minor | 14 |

**PASS list, eligible for an R2 seat** (full git blob at HEAD `7b08cbf`; a seat must name this trial and exactly this blob; any byte change needs a new trial):
- `00.00.00.0052.05.01` (blob `7993b14b830d12feb5a54509b41e74c931afe334`)
- `00.00.00.0052.05.02` (blob `c82b1fc6d2d3d6ce6e5a44cf99cbc7bf93b62332`)
- `00.00.00.0053.05.01` (blob `77ee148ffd645b15b4aeeb1401ff6b72e05a35da`)
- `00.00.00.0053.05.02` (blob `8499872db0d7551309befdbf12ce1d1c7fa821c4`)
- `00.00.00.0055.05.01` (blob `6582d3e56495ca93203e81871659da0481550d41`)
- `00.00.00.0055.05.02` (blob `596aa9ba0befffa6f9f6ca93364b9a6fea426478`)
- `00.00.00.0056.05.01` (blob `0914ebb8274c3e049440e11388b69da2b138f447`)
- `00.00.00.0056.05.02` (blob `93178adddeb2ec915a2c5d4cc070d0dc50c03d37`)
- `00.00.00.0057.05.01` (blob `67b3b9b6762af70a7494893fb7ff47e4e86e4281`)
- `00.00.00.0057.05.02` (blob `037eec2ff5e9c6c18020f06679358a13e9a62bb1`)
- `00.00.00.0051.05.02` (blob `7dbf70bd22af1bf0354edd82aff3ddb405ef892d`)
- `00.00.axioms.05.02` (blob `452be16b0536002a12279c5d485c68c5217fa6c8`)
- `10.11.21.0012.05.01` (blob `9aaed75fc8f0594a1289fa83e870a474d4d021d2`)
- `10.11.21.1001.05.01` (blob `566071064f63a5c85fcb3bd87d9e375717bdbf51`)
- `10.11.21.1001.05.02` (blob `2aa3490239620604ce1bb13c34841a60ac8f7056`)

Seat with the full 40-character blob, not a prefix (finding 1). Seating a counter adds a `seat-05.NN:` line to that page's face 00, which is a draft, so no seat breaks (Q47 is still open).
**Before seating, note:** the `w01` card in the `0051`, `0052`, `0056`, `0057` and `00.00.axioms` packs is the TRIAL-K3 fix list, and pass 5 (`7b08cbf`) has already done it; its `done:` test passes today. That is not a defect, because a pack card is closed by the loop and not by editing the pack. But if you would rather close it in the text first, that edit needs a new trial.

**The two seated faces** are intact: `00.00.00.0056.01.md` is blob `112c169ccd06d54c6d9ab607fee6c2d16004cc62`, and `10.11.21.1001.01.md` is blob `5415cef2dd0a37f3c2ba4c9b6d2652262f0ef82d`. Both are the blobs TRIAL-K2 passed (`kernel-trial-2.md:25-26`), and both seat lines verify against `kernel-trial-2.md@ed82086`. But they are pinned by 8 hex digits only, and finding 1 shows that is not enough.

## TRIAL-K3 fixes: did they land?

| K3 # | Landed? | Evidence |
|---|---|---|
| 1 major | yes | Face 00 and counters now need a seat record (`build.mjs:259-267`); test "a face 00 seated with no seat-00 record is refused". My HL: refused. Residue: finding 3 (face 00 can't satisfy it at all). |
| 2 major | yes, with holes | The trial file, commit, PASS list and blob are checked (`build.mjs:159-182`). My HB, HD, HE, HF, HH were all refused. Holes: findings 1, 2, 4, 5. |
| 3 major | yes | Axioms C3.2 is checked locally again (`build.mjs:280-283`); test "an axioms 01 card with no 04 card is refused (H3)". |
| 4 major | yes | `0057.04:11` now reads "pages in different bands are one set when their `NN` (the CC counter space) and their title both match (R18)"; logged at `0057.06.01:29-30`. No F.2 reciprocal-link rule is left in `0057.01`/`.04`. |
| 5 minor | yes | `0051.01:148`, `0051.04:184` say "matched by number and title (R18)"; the builder maps the merge (`build.mjs:43`). |
| 6 minor | yes | `0051.01:119`, `0051.04:140`, `:160`. |
| 7 minor | yes, with residue | `0052.01:82`, `0052.04:86`. Residue: `0051.01:53` (finding 8). |
| 8 minor | yes | `0052.01:20`. |
| 9 minor | yes | `0051.04:122`. |
| 10 minor | yes | `0052.02:3` equals `face00.md` section 4.5's stamp exactly (address `10.11.40.0000`, title `workshop`, state `live`); the title-only line is struck and logged (`0052.06.01:37`). The form comes from a DRAFT (see 0052.02 verdict). `MAP.md:239` still names `format.md:74` (finding 10). |
| 11 minor | yes, with a hole | An un-seat needs `unseat-NN:` naming the old blob (`build.mjs:199-212`); my HI was refused. Hole: finding 6. |
| 12 minor | not claimed, not landed | `build.mjs:39` still uses `changing/there/needed/achieve`; moot under R21. |
| 13, 14 | held (not claimed) | Q39, Q40 unchanged. |
| 15 minor | yes | `crates/trial-compute/tests/binary.rs:10-15` honors `CARGO_TARGET_DIR`; both tests pass with it set (below). |
| 16 minor | yes | `MAP.md:39-40`, `:82`. |

## Checks run (real output)

All runs are on clean copies of HEAD `7b08cbf`. `/tmp/k4c` is a `git clone` checked out at `7b08cbf` (it has history, so the seat checks can reach `ed82086`). `/tmp/k4n` is a `git archive` with no `.git`. `/tmp/k4` is a `git archive` with a fresh one-commit repo.

**`node kernel/build.mjs --check`**
- `/tmp/k4c` (clone): exit 0, `59 findings, 0 errors`. All 59 are `why missing (4.7)`. `checked books/00.00.00.book 50 entries`, `00.00.axioms.jsonl 7`, `10.00.00.book 1`, `10.11.00.book 1`, `10.11.21.book 15`.
- `/tmp/k4n` (archive, no git): exit 0, `61 findings, 0 errors`. The two extra findings are `00.00.00.0056.01.md: seat trial docs/trial/kernel-trial-2.md: no git here, so commit ed82086 was not checked; the working file was read`, and the same for `10.11.21.1001.01.md`.
- `/tmp/k4` (archive plus a fresh repo, no `ed82086`): exit 1. `ERROR 00.00.00.0056.01.md: seat cites trial docs/trial/kernel-trial-2.md at commit ed82086, which git cannot find; the seat is blocked`, and the same for `1001.01`, then `2 errors; nothing written`. That is correct (it fails closed), but it means a trial run on a `git archive` plus `git init` cannot pass `--check`. Use a clone.

**`node kernel/build.test.mjs`** (clone): 19/19 `ok`, `all passed`, exit 0. The list includes the new R2 tests (H1, H1b, counter, H2 x2, real-trial-not-passed, director-no-ruling, director-ruling-not-naming, bad approved-by, H3, H7 x2).

**`CARGO_TARGET_DIR=target/k4-trial cargo test --workspace --no-fail-fast`** (archive): exit 0, 38 result lines, **409 passed, 0 failed**. This includes `trial-compute tests/binary.rs: 2 passed` with `CARGO_TARGET_DIR` set (K3 finding 15 landed), `compute tests/http.rs: 14 passed`, and `seqpage tests/face00.rs: 9 passed`.

**Copy check:** `docs/trial/kernel-trial-copycheck.mjs`, adapted in `/tmp` (root `/tmp/k4c`; skips non-`.md` spec entries; maps R4 dashes, quotes and section signs). Every "not found" sentence in a pass-5 face is a ruling merge logged in its 06.01 note, an appended ruling quote, or a `7` hole. The only new sentence in `0057.04` is the R18 merge at `:11`, logged at `0057.06.01:29-30`.

**Counts claimed in the 05.01 faces, recounted:**
- `why: 4.7` cards: `0051.04` 20/28, `0052.04` 13/17, `0053.04` 5/6, `0054.04` 2/3, `0055.04` 10/12, `0056.04` 2/4, `0057.04` 7/19.
- `` `7` `` marks in `0057.01`: 12.
- All match.

**References in the 05 counters:**
- Every commit id cited resolves: `8c8f780`, `ceb8fd2`, `ef28051`, `fae009a`, `42ffbc9`, `d37e532`.
- Every Qnn cited is in `kernel/QUESTIONS.md`, and every Onn in `docs/design/OPEN.md`.
- Every `DIRECTOR-RULINGS.md:N` cite is the right ruling.
- Every `DESIGN.md (:N)` cite is the named section heading (`:33, :61, :88, :112, :132, :168, :192, :210, :234`).
- Every DECISIONS id cited exists. Ids D01-D129 are the same in DECISIONS-INDEX and DECISIONS-LOG. One link is the wrong topic: finding 13.

### Hostile seat tests (part C, scratch copies of `/tmp/k4c` only)

| # | Hostile change | Result |
|---|---|---|
| HA | commit a forged `docs/trial/forged.md` with a PASS line for `10.11.21.0013.01` at its blob, then seat it citing `forged.md@<that commit>` | **accepted**, exit 0 (finding 4) |
| HB | the same forged file, uncommitted, citing `@7b08cbf` | refused: "git cannot find" |
| HC | the same in a copy with no `.git`, citing `@0000000` | **accepted**, exit 0, with only a finding "no git here" (finding 5) |
| HD | seat line `blob: deadbeef` | refused: "seated face changed since its trial" |
| HE | the trial file exists, but the cited commit `ed82086` doesn't have it | refused |
| HF | cite the real `kernel-trial-2.md@ed82086` for a face it did not pass | refused: "PASS list does not name" |
| HG | append `## R23 - fake / Director approves 10.11.21.0013.01.` to the working-tree `DIRECTOR-RULINGS.md` and seat with `approved-by: director; ruling: R23` | **accepted**, exit 0; the book entry says `approved-by: director` (finding 2) |
| HH | `approved-by: director; ruling: R11` (a real ruling that does not name the face) | refused |
| HI | un-seat `0056.01` (rename to `.draft`, registry `01 draft`) with no record | refused; **accepted** if `books/` is deleted first (finding 6) |
| HJ | the same un-seat, after removing `approved-by` from `books/00.00.00.book` | **accepted** (finding 6) |
| HK | seat note counter `0051.06.01` with a committed forged trial | accepted (finding 7: any counter can be seated; R22 names face 05) |
| HL | seat face 00 `10.11.21.1001.00` with a trial of its pre-seat blob and a `seat-00:` stamp line | refused: "blob 57d0389c is not 70cc70a8". The seat line itself changes the blob (finding 3) |
| HM | change the law in seated `0056.01.md` ("is calculated and never drafted." -> "may be rewritten from memory when a model is confident."), then append `<!-- k4 nonce l8uyjcaaaaaa -->`, found by a 20-second search on 8 cores so the new blob starts `112c169c` (`112c169c7834147249d4594c4bb9bc341ac680c9`) | **accepted**: `node kernel/build.mjs` exit 0, and `books/00.00.00.book` keeps `"approved-by":"build-stage (R2)","trial":"docs/trial/kernel-trial-2.md@ed82086 blob 112c169c"` over the changed body (finding 1) |

## Findings

### 1. major: a seat is pinned by a short blob prefix, which takes seconds to forge
- **Evidence:**
  - `kernel/build.mjs:131` (`SEAT_LINE`) and `:152` (`passList`) accept 7-40 hex digits.
  - `:160` and `:180` compare with `startsWith`.
  - Both real seats use 8 digits (`0056.00.draft.md:11` `blob: 112c169c`, `1001.00.draft.md:11` `blob: 5415cef2`), as does the trial they cite (`kernel-trial-2.md:25-26`).
- **In HM**, I changed the seated `0056.01` Never From Memory law to allow rewrites from memory. Then I appended a nonce found in about 20 seconds (2^32 SHA-1 tries, 8 cores), so the new blob starts `112c169c`. The build passed, and the book still shows the R2 seat.
- **Breaks:**
  - R2 (`:9`): the seat is for the trialed face.
  - Axiom 9: any change needs a new trial.
  - The builder's own claim at `:159-160` ("seated face changed since its trial ... is refused").
  - `build.test.mjs` "a seated face changed after its trial is refused" only covers a change that shifts the prefix.
- **Fix direction (not done):**
  - Require the full 40-digit blob in `seat-NN:` lines and in trial PASS lists, and compare for equality.
  - Re-pin the two existing seats with full blobs. This report records them in full above, and they are unchanged since TRIAL-K2.
  - Raised as Q52.

### 2. major: a Director seat can be written by any lane, through the working-tree rulings file
- **Evidence:** `build.mjs:164-167` reads `docs/spec/DIRECTOR-RULINGS.md` from the working tree (not from a commit), and accepts any `## ` section whose text contains the face address. In HG, two appended lines that nobody committed made `approved-by: director` build clean.
- **Breaks:**
  - Only the Director approves (R2 `:9`: the build-stage path is the only seat without his eyes).
  - The TRIAL-K3 finding 2 fix, which was meant to stop a source file from claiming `director`.
- **Fix direction (not done):**
  - Read the rulings file at a cited, committed revision.
  - Require the ruling to name the face in a seat-approval sentence, not just mention it.
  - Raised in Q52.

### 3. major: face 00 can never be lawfully seated, and a seated face 00 would be broken by the next seat on its page
- **Evidence:**
  - A face 00 seat record lives in face 00's own stamp (`seat-00:`, `build.mjs:128-129`, `:227`). Writing it changes face 00's blob.
  - So the trial's blob can never match the seated file: the trial would have to name a blob that includes the trial's own commit id.
  - HL shows this. Every other seat on the page (`seat-NN:` on the face 00 registry, `:228-230`) also edits face 00.
  - The parked door packs plan exactly this step ("trial and seat 00.00.00.0000.00 ... its seat-00 stamp line names the trial and blob", `kernel/parked/doors/00.00.00.0000.05.02.draft.md:41-45`).
- **Breaks:**
  - TRIAL-K3 finding 1's intent: a face 00 seat can be made and checked.
  - R14 (`:59-60`) and R22 (each page reaches a seated MVP) assume face 00 can be seated some day.
- **Effect today:** no face 00 is seated, so nothing is wrong yet. Raised as Q51, linked to Q34 and Q47.

### 4. minor: a committed forged trial is accepted
- **Evidence:** `build.mjs:174-182` checks that the file exists at the cited commit and that its PASS list names the face. It does not check:
  - that the commit is an ancestor of HEAD;
  - that it differs from the commit that made the face;
  - that the trial names a fresh session (R20, `:80`: "The builder's own session never trials its own work").
- **Effect:** in HA, a two-line file committed in the same lane seated a face. This is inherent to a text-file guard, but every such seat is at least findable in git (R2 `:9`).

### 5. minor: with no git, an unverifiable seat becomes a finding, not an error
- **Evidence:**
  - `build.mjs:139-140` says "Anything that cannot be verified blocks the seat".
  - But `:142-143` and `:177` fall back to the working file with only a finding when `git rev-parse --show-toplevel` is not `ROOT`.
  - HC: a forged trial citing commit `0000000` built clean (exit 0).
- **Note:** the shared repo is a git checkout whose toplevel equals `ROOT` (`/workspace/workshop-build/repo`), so the real gate is not affected.

### 6. minor: the un-seat check trusts `books/` in the working tree
- **Evidence:** `priorSeats()` (`build.mjs:188-197`) reads past seats from `books/` on disk.
  - Deleting `books/` (HI) first lets a seated face be un-seated with no `unseat-NN:` record.
  - So does dropping `approved-by` from the book (HJ).
  - Only `git diff` shows it.
- **Fix direction:** read past seats from `books/` at HEAD (`git show HEAD:books/...`).

### 7. minor: the builder seats any counter, but R22 names only face 05
- **Evidence:** `build.mjs:259-267` accepts a seat record on any counter. In HK, note counter `0051.06.01` was seated.
- **Breaks:**
  - R22 (`:86-88`) asks for "the seated 05".
  - Q35 (can an R2 seat apply to `06.01` notes or `03.14` dictionary sections?) is still open.
  - R2 (`:9`): "This does not let anyone answer an open Director question."
- **Face side:** finding 9.

### 8. minor: "inherited reserved pages (0020-0049)" remains
- **Evidence:** `0051.01:53` ("This matters for the inherited reserved pages (0020-0049)", copied from `decisions.md:55`).
- **Breaks:**
  - R17 (`:68-69`): "0020-0099 aren't just locations".
  - R7 (`:32`): the reserved override range is 0001-0009 only.
- **Note:** this is the same class as TRIAL-K3 finding 7, which pass 5 fixed at `0052.01:82` and `0052.04:86`. It was missed by pass 5 and by TRIAL-K3. `0051.04` has no copy of this line.

### 9. minor: the Counted Faces law widens R22 from face 05 to any counter
- **Evidence:**
  - `0052.01:87`: "A counter of a counted face may be seated under R2 after a hostile trial; each page's face 05 is seated this way (R22)."
  - `0052.04:92` says the same.
  - The merge log (`0052.06.01:34-35`) and Q41's note call this "applied R22".
  - R22 says only "the seated 05 for each page" (`:87`).
- **Breaks:**
  - It answers open Q35 for `06.NN` and `03.NN` counters (R2 `:9`).
  - The builder follows it (finding 7).
- **Fix direction:** "A face 05 counter may be seated under R2 ... (R22)", and leave other counters to Q35.

### 10. minor (MAP, no verdict): a stale source line
- **Evidence:** `kernel/MAP.md:239` still lists `format.md:74` as a source of `0052.02` Stamp, which pass 5 dropped (`0052.02:2`).
- **Breaks:** axiom 8.

### 11. minor: one 05.01 line overstates its source
- **Evidence:** `0051.05.01:13`: "TRIAL-K found about 20 whys with no line number on 0051.04".
- **The source says otherwise:** `docs/trial/kernel-trial.md:58` says about 20 in all, with examples on both `0051.04` (10 lines) and `0057.04` (4 lines).
- **Breaks:** R22's 05 "explains what you learned" from its sources; axiom 6.

### 12. minor: stale `build.mjs` line cites in the 05 counters
- **Evidence:**
  - `0054.05.01:5`, `:11` and `0054.05.02:32` cite `build.mjs:30-31` for `CARD_TYPES`. At HEAD, `:30-31` are `TAIL_WORDS`/`CONTENT_FACES`, and `CARD_TYPES` is at `:33-34`.
  - `00.00.axioms.05.01:5`, `:11` cite `build.mjs:20-23` for the axioms storage form. At HEAD those lines are `BY`/`AT`, and the storage lines are `:23-26`.
  - All of these were right at `0823ae3`; pass 5 (`7b08cbf`) moved the lines.
- **Breaks:** axiom 6 (lineage must lead to the line). Use a symbol name (`CARD_TYPES`, `AXIOMS_FILE`) or a commit-pinned cite.

### 13. minor: the common-questions pack links the wrong decision
- **Evidence:** `10.11.21.0013.05.01:6` and `0013.05.02:13` link `DECISIONS-INDEX D89, D126`. D126 is "A concordance (word to page)" (`DECISIONS-LOG.md`, D126 row).
- **The right decisions:** D147 ("The common questions list lives on page 0013", `DECISIONS-LOG.md:84`), D267 (`:285`), D271 (`:289`) and D290 (`:313`).
- **Breaks:** R22 "links back to the overall design".

### 14. minor: a common-questions work card has a done test that can't be true, and a trial ordered too early
- **Evidence:**
  - `0013.05.02:35` (w02) expects `/ask "what is my name"` to return `10.11.21.1001.01.bob` "with draft state shown". But `1001.01` is seated (blob `5415cef2`), and the compute reports a seated face first (`crates/compute/src/askq.rs:17`; R5 `:20` "the seated face wins").
  - w03 (`:43`) trials `0013.01`/`.04` with `depends: none`, although w01 (`:21-25`) changes those card fields.

### 15. minor: the sample dictionary pack has no seat step, and one done test that isn't concrete
- **Evidence:** `10.11.21.0012.05.02` has three cards (w01-w03) and no seat step, though its outcome (`:6`) asks for the sections to be reviewed.
  - w01's done (`:25`), "the page follows the ruled answers", can't be checked.
  - w03 (`:43`) has `depends: none`, though w01 may change the sections it trials.
  - The outcome's "indexes every word the samples use" has no card.

### 16. minor (parked, report only): wrong question number in the parked README
- **Evidence:** `kernel/parked/README.md:17` says door packs wait on "QUESTIONS Q39". The door-pack question is Q42; Q39 is the `faces:` form.

### 17. minor (parked, report only): two door-pack cards can't be met as written
- **Evidence:**
  - The "trial and seat face 00" cards in all four door packs (for example `kernel/parked/doors/10.11.21.0000.05.02.draft.md:41-45`) can't be met while finding 3 stands.
  - `10.00.00.0000.05.02` and `10.11.00.0000.05.02` w03 say the desk/shelf lookup step is "blocked-by: R21 ...; in-place replacement is refused". But `crossChecks` refuses only a face at a spot an ancestor already fills (`build.mjs:365-367`). A desk or shelf page the kernel doesn't have can be found by a book lookup without any override.

**Observations (no severity):**
- `0055.05.01:11` and `1001.05.01:11` say the compute test "still expected" the removed bob 04 and "failed ... routed to COMPUTE". They don't say it was fixed: `brands_and_cards_on_real_books` passes, 14/14 (TRIAL-K3 table row 20, and this run).
- `0051.04` Book Layout (`:226-241`) shows the five-row split below 0100 without `0051.01:201`'s R17 note that the four-way split is `7` (Q30).

## Per-face verdicts

### A) Faces changed by kernel pass 5, plus 0057.01

| Face | Blob (HEAD) | Verdict | Findings / open question |
|---|---|---|---|
| `0051.01` | `74bb79dad85e8b65bd8d72d37aa5d743f3308865` | FAIL | 8 minor; also Q30 (four-way split, `:201`) |
| `0051.04` | `9d78c5f11b0d919b8a8e859c4a8db3bf9d9b29af` | HELD-7 | K3 5, 6, 9 landed; Book Layout's five rows wait on Q30 (R17 split) |
| `0051.06.01` | `31ac053876d03c4ed8bbd1c6bd9b519605520f78` | HELD-7 | counted note (Q35). Log checked: each pass-5 edit in 0051.01/04 has one merge line (`:51-57`) |
| `0052.01` | `37cdc39155e39d310ceb9c78508d50cb7b918bd1` | FAIL | 9 minor; also Q32 (`:41`), Q41 |
| `0052.02` | `cc339e0a734e8972b82de8bed66adcf1edb675d9` | HELD-7 | K3 10 landed. Its form is face00.md 4.5, a DRAFT that R19 says is "never as settled law" (`:76`); door type F10 `7` |
| `0052.04` | `3e7e1b9fb52d1c55b25e020bf7f12fd90fe79dff` | FAIL | 9 minor; also Q41 |
| `0052.06.01` | `152988b707bf1d0771380024bb9027c1bcb7b5f6` | HELD-7 | counted note (Q35). Log checked (`:30-37`) |
| `0057.01` | `60e9b9d7ca5d9b90a920268b431c813d5503523b` | HELD-7 | K3 4 resolved (its 04 now agrees). The source `workflow-loop.003.md` is a draft (O7), the same hold TRIAL-K2 put on 0057.02/.04 (`kernel-trial-2.md:228-229`) |
| `0057.04` | `30dacb86b111050a814c79b76da9d272305ed901` | HELD-7 | K3 4 landed (`:11`); `.003` is a draft (O7) |
| `0057.06.01` | `8d4d262bf512cbebafc85dd47c6b12c8cef09179` | HELD-7 | counted note (Q35). Log checked (`:29-30`) |

### B) Face 05 counters (PACKS, `0823ae3`; unchanged by `7b08cbf`)

| Face | Blob (HEAD) | Verdict | Findings |
|---|---|---|---|
| `00.00.00.0051.05.01` | `6efdad797efb2cf0e441976f985b8eba15d2aad4` | FAIL | 11 minor |
| `00.00.00.0051.05.02` | `7dbf70bd22af1bf0354edd82aff3ddb405ef892d` | PASS | w01 already done by `7b08cbf` (observation) |
| `00.00.00.0052.05.01` | `7993b14b830d12feb5a54509b41e74c931afe334` | PASS | every line checked against its cited trial, commit, BUILD-LOG line and count |
| `00.00.00.0052.05.02` | `c82b1fc6d2d3d6ce6e5a44cf99cbc7bf93b62332` | PASS | w05 is blocked on Q20/Q35/Q41, as it should be |
| `00.00.00.0053.05.01` | `77ee148ffd645b15b4aeeb1401ff6b72e05a35da` | PASS | |
| `00.00.00.0053.05.02` | `8499872db0d7551309befdbf12ce1d1c7fa821c4` | PASS | |
| `00.00.00.0054.05.01` | `bf402b617c328b1e4a93f623e6dfb90275d13041` | FAIL | 12 minor |
| `00.00.00.0054.05.02` | `ed7a136caa76af602c63d46bb130e77c22281fb4` | FAIL | 12 minor |
| `00.00.00.0055.05.01` | `6582d3e56495ca93203e81871659da0481550d41` | PASS | (observation on `:11`) |
| `00.00.00.0055.05.02` | `596aa9ba0befffa6f9f6ca93364b9a6fea426478` | PASS | |
| `00.00.00.0056.05.01` | `0914ebb8274c3e049440e11388b69da2b138f447` | PASS | its `:10` claim about the blob check is true of the test; finding 1 is about the guard, not this face |
| `00.00.00.0056.05.02` | `93178adddeb2ec915a2c5d4cc070d0dc50c03d37` | PASS | w01 already done by `7b08cbf` (observation) |
| `00.00.00.0057.05.01` | `67b3b9b6762af70a7494893fb7ff47e4e86e4281` | PASS | |
| `00.00.00.0057.05.02` | `037eec2ff5e9c6c18020f06679358a13e9a62bb1` | PASS | w02 "approve .003" is the Director's, and is correctly blocked by O7 |
| `00.00.axioms.05.01` | `d9f4ed9330ec9ba395b9aac61cc7504e04dafe66` | FAIL | 12 minor |
| `00.00.axioms.05.02` | `452be16b0536002a12279c5d485c68c5217fa6c8` | PASS | w01 already done by `7b08cbf` (observation) |
| `10.11.21.0012.05.01` | `9aaed75fc8f0594a1289fa83e870a474d4d021d2` | PASS | |
| `10.11.21.0012.05.02` | `7c952e44c9956f38df8e9c5c1e9e1055ecbd8a07` | FAIL | 15 minor |
| `10.11.21.0013.05.01` | `c40dcf8dfec20991f75c60e890ea8197e7da7723` | FAIL | 13 minor |
| `10.11.21.0013.05.02` | `d440a2214fc6adae82dcc24745ae2582a346355a` | FAIL | 13, 14 minor |
| `10.11.21.1001.05.01` | `566071064f63a5c85fcb3bd87d9e375717bdbf51` | PASS | (observation on `:11`) |
| `10.11.21.1001.05.02` | `2aa3490239620604ce1bb13c34841a60ac8f7056` | PASS | |

**What a PASS on a 05.02 pack checked:**
- Every header field of `workflow-loop.003.md:238` is present (`authorized` and `frame` are `7`, Q45).
- Every work card has `reason`, `depends`, `blocked-by`, a `done:` that a command or file check can decide, and a `path`.
- The order is fix, then fill, then trial, then seat, and each trial depends on the steps that change its faces.
- `design:` names a real DESIGN.md section and real DECISIONS ids on the page's topic.
- No card seats its own work, uses an override (R21), or answers an open Director question. Each such step is `blocked-by` its question.

### Parked door packs (report only; R10 forbids a 05 on page 0000, Q42)
- `kernel/parked/doors/` holds 8 drafts for `00.00.00`, `10.00.00`, `10.11.00` and `10.11.21` page 0000.
- Their 05.01 lines check out against R1, R10, `kernel-trial.md` findings 10, 13 and 20, CONFLICTS K17, O14 and O34.
- Findings 16 and 17 apply.
- No verdict: they can't be built or seated while R10 stands.

## Method
- **Repo state:** the shared working tree was read only. My only writes are this file and Q51-Q52 in `kernel/QUESTIONS.md`.
- **Scratch copies:** all builds, tests and hostile edits ran in `/tmp/k4c` (a clone at `7b08cbf`) and copies of it, `/tmp/k4n` (archive, no git) and `/tmp/k4` (archive), plus the grinder in `/tmp/k4g`. The cargo target was `target/k4-trial` (gitignored).
- **Blobs:** each blob is `git rev-parse HEAD:<path>` at `7b08cbf`, written in full. Renaming `05.NN.draft.md` to `05.NN.md` to seat it does not change the blob.
