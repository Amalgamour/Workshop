# Kernel trial 3 (TRIAL-K3): hostile pass on the faces kernel pass 4 changed

Lane TRIAL-K3, 2026-11-11, about 3:55 PM EST. I'm a fresh session that did not build these faces. Under R20 (`DIRECTOR-RULINGS.md:78-80`) that counts as a different view, so a PASS here could qualify a face for an R2 seat (`DIRECTOR-RULINGS.md:7-9`).
I only report. Nothing in `kernel/` or `books/` was changed, and nothing was seated. New conflicts go to `kernel/QUESTIONS.md` as Q39-Q41, tagged `[TRIAL-K3]`.

**Target:** the faces changed by kernel pass 4 (`42ffbc9` seats, `fae009a` fixes). Kernel and books are unchanged from `fae009a` to HEAD `8b2e909` (later commits touch only `app/`, `docs/spec/SEQ-GUIDE.md` and `DIRECTOR-RULINGS.md` R22).
**Judged against:** `DIRECTOR-RULINGS.md` R1-R21 (quoted words govern), `docs/spec/face00.md` (DRAFT), `kernel/QUESTIONS.md`, `kernel/CONFLICTS.md`, `docs/trial/kernel-trial-2.md`. R22 (3:50 PM EST, after this trial was set) is not used to judge any face; its one new conflict is raised as Q41.
**Rule for face 00s:** a face 00 whose only open part is a face00.md PROPOSED or `7` field is HELD-7, not FAIL.

## Summary

| Verdict | Faces |
|---|---|
| PASS (eligible for an R2 seat) | 0 |
| FAIL | 6 |
| HELD-7 (depends on an open question) | 23 |
| **total** | **29** |

| Severity | Findings |
|---|---|
| blocker | 0 |
| major | 4 |
| minor | 12 |

**PASS list:** none. No face in this trial may be seated.

**The two seated faces** are intact: `00.00.00.0056.01.md` is blob `112c169ccd06d54c6d9ab607fee6c2d16004cc62` and `10.11.21.1001.01.md` is blob `5415cef2dd0a37f3c2ba4c9b6d2652262f0ef82d`. These are the exact blobs TRIAL-K2 passed (`ed82086`); `42ffbc9` only renamed the files. Both book entries carry `approved-by: build-stage (R2)` and the trial reference. Editing either file is refused by the builder (test "R2: a seated face changed after its trial is refused"). But the seat guard has holes around them: findings 1, 2 and 11.

## TRIAL-K2 fixes: did they land?

| K2 # | Landed? | Evidence |
|---|---|---|
| 1 blocker | yes | `0052.01:35`, `0052.04:34,36`: door page 0000 excepted (R10). |
| 2 blocker | yes | `0053.01:31`: `draft` "draft faces count and lookups find them (R5)". |
| 3 major | yes, with residue | `0051.01:191-194`, `0051.04:233,241` now say 0001-0009. Residue: finding 7 (`0052.01:82`, `0052.04:86`). |
| 4 major | partly | `0051.01:178`, `0051.04:222`, `0057.01` F.2 line struck. Not landed: `0057.04:11` still states the F.2 rule (finding 4); "linked by number" remains (finding 5). |
| 5 major | yes, with residue | `0051.04:140`. Residue: "99 at any level" (finding 6). |
| 6 major | yes | `0057.01:83` equals `workflow-loop.003.md:160` minus the two `05.00` board sentences; both strikes logged at `0057.06.01:27-28`. |
| 7 major | yes, with residue | `0052.01:3`, `0052.02:6`, `0052.04:5`. Residue: `0052.01:20` (finding 8). |
| 8 major | yes for books, regressed for the axioms | In-place replacement is refused (builder test, and my H6 at shelf level). C3.2 across the lookup works for books, but the axioms lost C3.2 entirely (finding 3). |
| 9 | held, as reported | Every face 00 uses the face00.md layout; per-type fields not written (Q33). |
| 10 minor | yes, with residue | `0051.01:85,87`, `0051.04:124`, `0052.04:5`. Residue: `0051.04:122` (finding 9). |
| 11 minor | yes | No merge-log line ends at "(DIRECTOR-RULINGS.md" any more. |
| 12 minor | yes | `0052.01:41`, Q32. |
| 13 minor | partly | The duplicate Card Shape line is gone and its content is kept at `0052.02:19`. The new `form:` example is a mix of two sources, and the JSON example still disagrees (finding 10). |
| 14 minor | yes | `0052.04:106,112` are `7` hole bodies. |
| 15 minor | yes | Face 03 removed. "Cold set before a write: `1.7.8`" is kept at `00.00.axioms.02:9`, so no content was lost. |
| 16 minor | yes | `00.00.axioms.06.01:7,12`. |
| 17 minor | moot | Sample parked (R21). |
| 18 minor | yes | Builder test "R5: a draft with no why-NN says so"; header says R1-R21 (`build.mjs:4`). |
| 19 minor | partly | Refused for the builder's own field names only (finding 12). |
| 20 (COMPUTE) | yes | `crates/compute/tests/http.rs` `brands_and_cards_on_real_books` passes (14/14). |

## Checks run

- **`node kernel/build.mjs --check`** on a clean `git archive` of HEAD: exit 0, 59 findings, 0 errors. All 59 are `why missing (4.7)`. Books match `books/` (00.00.00: 36 entries; 00.00.axioms: 5; 10.00.00: 1; 10.11.00: 1; 10.11.21: 9).
- **`node kernel/build.test.mjs`**: 8/8 ok.
- **`cargo test --workspace --no-fail-fast`** on a clean archive (`CARGO_TARGET_DIR=target/k3-trial`): 407 passed, 2 failed. Both failures are in `trial-compute` `tests/binary.rs`. When I reran with the archive's `target/` linked to that build directory and no `CARGO_TARGET_DIR`, both passed (2/2). So there is no kernel failure and no core failure. This is a COMPUTE test-harness finding (15).
- **R4:** a byte scan of `kernel/00.00.00`, `kernel/00.00.axioms`, `kernel/samples` and `books/` found nothing outside 0x20-0x7E plus newline.
- **Registries:** every in-scope registry lists exactly the files present (the builder checks this, and it reports 0 errors).
- **Copy check:** `docs/trial/kernel-trial-copycheck.mjs`, adapted in a scratch copy. It skips non-`.md` entries (the committed script still crashes with EISDIR on `docs/spec/examples/`), maps R4 dashes and quotes, and covers `00.00.axioms`. Every "not found" sentence in an in-scope face is one of these:
  - a ruling merge logged in its 06.01 note;
  - an appended ruling quote;
  - a `7` hole;
  - note text.
  - No invented sentence was found in a 01/02/04 body, apart from finding 10 (an example line).
- **Hostile builder tests H1-H8:** run in scratch copies only.

| # | Hostile change | Result |
|---|---|---|
| H1 | rename `10.11.21.1001.00.draft.md` to `.md` (seat face 00, no record) | accepted, 0 errors (finding 1) |
| H1b | the same on kernel `0056.00` | accepted (finding 1) |
| H2 | seat `10.11.21.0013.01` with `seat-01: approved-by: director; trial: docs/trial/does-not-exist.md@0000000; blob: <its blob>` | accepted (finding 2) |
| H3 | add a 01 card with no 04 card to `00.00.axioms.01` | accepted at HEAD; rejected at `ed82086` "has no 04 card (C3.2)" (finding 3) |
| H3b | the same on kernel `0054.01` | rejected (C3.2 across the lookup works for books) |
| H4 | a 0020 page card with face00.md's override fields `changes:`, `why-here:`, `why-needed:`, `achieves:` | accepted (finding 12) |
| H5 | stamp `type: banana` | accepted. face00.md section 5 makes this a finding; the builder doesn't check it (no finding raised: face00.md F3 is `7`) |
| H6 | shelf `10.11.00.0056.01.draft` at the kernel's spot | rejected "replaces 00.00.00.0056.01 in place" |
| H7 | rename seated `0056.01.md` to `0056.01.retired.md`, with the registry set to `01 retired` | accepted; the rebuilt book loses the seated entry with no record (finding 11) |
| H8 | drop `title:` from `10.11.21.0000.00` | accepted. face00.md asks for a container title on 0000, but that is F1 `7` (no finding) |

- **seqpage check** (`crates/seqpage`, built from the archive): every kernel and sample page was exported to `.seq` and checked against its book. `ok: true` for all, with these face00 findings:
  - `faces:` disagrees with what the compute derives on 0051-0057 and `10.11.21.0012` (finding 13);
  - stamp `state: draft` vs derived `live` on the four door pages, `0056` and `1001` (finding 14);
  - `seat-01:` is "not a registry field" on `0056` and `1001` (Q34, held).

## Findings

### 1. major: a face 00 can be seated with no seat record
- **Evidence:** `kernel/build.mjs:179` only checks seat records for `x.ff !== '00'`, and `registry()` (`:146`) accepts a bare face 00 as `seated; ` with an empty record. In H1 and H1b, renaming `10.11.21.1001.00.draft.md` or `00.00.00.0056.00.draft.md` to `.md` builds with 0 errors and writes a seated face 00 entry.
- **Breaks:** R2 (`DIRECTOR-RULINGS.md:8`): a face is seated only after a hostile trial, "recorded as `approved-by: build-stage (R2)` with the trial reference". Every face 00 in scope is HELD-7 and has never passed a trial.

### 2. major: the seat record is self-asserted; neither the trial reference nor `director` is checked
- **Evidence:** `kernel/build.mjs:126` (`SEAT_LINE`) accepts `approved-by: director` or `build-stage (R2)`, with any `trial:` text. `:180-182` checks only that the blob prefix matches. In H2, a builder-written `seat-01: approved-by: director; trial: docs/trial/does-not-exist.md@0000000; blob: <blob>` built clean, and the book entry was written with `approved-by: director`.
- **Breaks:**
  - R2 (`:7-9`): the trial reference must let "every such seat be found and re-reviewed". A reference to a file that doesn't exist, or to a trial that never passed that face and blob, defeats that.
  - Only the Director approves as Director (`:8` "without the Director's review" is the only exception). A source file can claim `director`.
- **Note:** the 2 real seats are correct: they cite `docs/trial/kernel-trial-2.md@ed82086`, and that trial passes exactly those blobs (`kernel-trial-2.md:25-26`).

### 3. major: C3.2 is no longer checked on the axioms (regression from the finding 8 fix)
- **Evidence:** the local check was replaced by `if (!w) { /* looked up */ }` (`kernel/build.mjs:196-197`). `crossChecks` then drops the axioms (`:275` `books.filter((b) => !b.isAx)`). In H3, a 01 card with no 04 card on `00.00.axioms.01` builds with 0 errors. At `ed82086` it was rejected: "card ghost-rule has no 04 card (C3.2)".
- **Breaks:** C3.2 (`0052.01:72`, `decisions.md:350-357`): "Every 01/02 card key has a 04 card | hard: the compute rejects the write".
- **Effect:** no in-scope face is wrong today, but the axioms' 01/02 faces have lost their guard.

### 4. major: the old F.2 membership rule is still in the 04 explanation of 0057's set rules
- **Evidence:** `kernel/00.00.00/00.00.00.0057.04.draft.md:11` (Band Design, copied from `decisions.md:644-645`): "matching `N` and `NN` identify candidates for a set. Membership requires explicit reciprocal Face 08 links." Pass 4 struck the same rule from `0057.01` Bound Bands (`0057.06.01:27`), but not from its 04.
- **Breaks:**
  - R18 (`:71-72`): "They are matched by the CC and the title." R18 answered Q14 against option B, the reciprocal links.
  - C3.2 (`0052.01:76`): "A 01 card and its 04 card disagree | elevated to the user for correction; neither governs".
- **Effect:**
  - TRIAL-K2 finding 4 has not fully landed.
  - `0057.01` FAILs here because its card can't govern while its 04 disagrees.
  - `0057.04` was not changed in pass 4, so it is outside this trial's face list. It needs the R18 merge and a trial.

### 5. minor: "sets linked by number" remains
- **Evidence:**
  - `0051.01:148`: "This keeps A2.6 intact: ... and sets linked by number."
  - `0051.04:184` (`why:`) says the same.
- **Breaks:** R18 (`:71-72`): matched by CC **and** title. This is the leftover half of TRIAL-K2 finding 4.

### 6. minor: "99 at any level" still covers faces, and "00 ... on the page axis" is loose
- **Evidence:**
  - `0051.01:119`: "At every level, 99 is a pointer, never content."
  - `0051.04:160`: "99 at any level is a pointer to the next location."
  - `0051.04:140`: "00 on the desk, shelf, book or page axis means the door". The page-axis door is `0000`.
- **Breaks:**
  - R9 (`:37-38`): no `FF.99`; sentinels apply only to desk, shelf, book and page.
  - R1 (`:5`): "`00` for a 2-digit axis, `0000` for the page axis".
  - This is the same class as TRIAL-K2 finding 5.

### 7. minor: 0001-0099 is still called "reserved pages"
- **Evidence:**
  - `0052.01:82`: "Face 03 is allowed in normal books on their reserved pages (0001-0099)" (copied from `decisions.md:404`).
  - `0052.04:86` says the same (from `seqAddr.md:189`).
- **Breaks:**
  - R17 (`:68-69`): "0020-0099 aren't just locations".
  - R7 (`:31-32`): only 0001-0009 is the reserved override range.
  - This is the leftover of TRIAL-K2 finding 3.

### 8. minor: the Face Jobs row for 00 still says only "the page stamp"
- **Evidence:** `0052.01:20`: "| `00` | registry | the page stamp |". The same face at `:3` now says face 00 also lists the faces and holds type-dependent registry fields.
- **Breaks:** R10 (`:41`), R19 (`:75-76`). This is the leftover of TRIAL-K2 finding 7.

### 9. minor: R1 wording leftover
- **Evidence:** `0051.04:122`: "Every container is identified by a page 0000".
- **Breaks:** R1 (`:5`): use the word "door". This is the leftover of TRIAL-K2 finding 10.

### 10. minor: the Stamp example is a mix of sources, and the card's two examples disagree
- **Evidence:**
  - `0052.02:3` `form: ---\naddress: 10.11.21.0000\ntitle: tools\nstate: live\n---` joins face00.md 4.5's shape (address `10.11.40.0000`, title `workshop`) to format.md:74's title. The result is an example in neither source, and its title contradicts the real stamp of `10.11.21.0000` (`title: about-me`, `kernel/samples/10.11.21/10.11.21.0000.00.draft.md:3`).
  - It has no `type:`, though `:6` and `:8` of the same card put type in the stamp. Door type is F10 `7`.
  - `0052.02:12` still shows a title-only stamp.
- **Breaks:**
  - copy, don't compose (`drafting.md:7`; axiom 7);
  - R12 (`:53-54`);
  - A3.2 (a stamp title that doesn't match the container is elevated).

### 11. minor: retiring or un-seating a seated face leaves no record
- **Evidence:** H7. `0056.01.md` renamed to `.retired.md`, with the registry set to `01 retired`, builds clean. The rebuilt book has no seated `0056.01` entry and nothing records that the R2 seat was undone. Only `--check` against the committed `books/` shows the difference.
- **Breaks:** R2 (`:8`: every seat can be "found and re-reviewed later"); axiom 1 (the live record is where authority is kept).

### 12. minor: the override field guard uses names that differ from face00.md
- **Evidence:** `kernel/build.mjs:36` `OVERRIDE_FIELDS = ['changing', 'there', 'needed', 'achieve']`. face00.md section 3.3 proposes `changes`, `why-here`, `why-needed`, `achieves`. In H4, a 0020 card with the face00.md names built clean.
- **Breaks:** R7 (`:31-32`), the TRIAL-K2 finding 19 fix. Both name sets are PROPOSED/`7`, so this is minor (R21: no overrides now).

### 13. minor (cross-lane, held): kernel `faces:` lists counters; face00.md and seqpage list counted faces
- **Evidence:**
  - Kernel registries write `faces: 01 draft, 02 draft, 04 draft, 06.01 draft` (for example `0051.00:10`) and `03.14 draft, 03.16 draft` (`10.11.21.0012.00:10`).
  - face00.md section 3.1 and examples 4.1-4.4 write `05 counted`.
  - `seqpage check` flags every such page: "`faces: ...` disagrees with what the compute derives (`... 06 counted`); compute-only fields are never hand-edited".
- **Breaks:** axiom 8 (two lanes, one field, two forms). Raised as Q39. Held, because `faces:` is F2 `7`.

### 14. minor (cross-lane, held): a stamp `state: draft` that seqpage derives as `live`
- **Evidence:** `seqpage check` reports "stamp state `draft` disagrees with the page's entries (`live`)" on:
  - `00.00.00.0000`, `10.00.00.0000`, `10.11.00.0000`, `10.11.21.0000` (door pages whose only face, 00, is a draft);
  - `0056` and `10.11.21.1001` (pages with a seated face and a draft face 00).
- **Breaks:** axiom 8. This is linked to Q31 and Q38 and raised as Q40. Held.

### 15. minor (COMPUTE lane): two trial-compute tests ignore `CARGO_TARGET_DIR`
- **Evidence:** `crates/trial-compute/tests/binary.rs:8-11` builds `compute`, then runs `repo().join("target/debug/compute")`.
- **Effect:**
  - With `CARGO_TARGET_DIR` set, both `held_default_listen_is_loopback` and `f14_non_loopback_listen_accepted` panic at `:21` with NotFound.
  - With the default target dir, both pass.
  - This is the same failure TRIAL-K2 saw ("binary not found"). Route it to the COMPUTE lane: use `env!("CARGO_BIN_EXE_compute")` or honor `CARGO_TARGET_DIR`.

### 16. minor: MAP status text is stale after the seats
- **Evidence:**
  - `kernel/MAP.md:40`: "Every face is `FF.draft`."
  - `:82` (samples): "all draft".
  - The heading at `:39` says two faces are seated.
- **Breaks:** axiom 8. MAP is not a face, so no verdict is affected.

## Per-face verdicts

Kernel book `00.00.00`:

| Face | Blob (HEAD) | Verdict | Findings / open question |
|---|---|---|---|
| `00.00.00.0000.00` | `5333b295` | HELD-7 | door title F1; door type `system` F10/Q33; `faces:` F2; state Q31/Q38/Q40 |
| `0051.00` | `9a6610ca` | HELD-7 | Q33; F2; Q39 |
| `0051.01` | `72c559d3` | FAIL | 5, 6 minor; also Q30 (four-way split) |
| `0051.04` | `48927f71` | FAIL | 5, 6, 9 minor |
| `0051.06.01` | `1d26a7a8` | HELD-7 | counted (Q35); log checked: every pass-4 edit in 0051.01/04 has a merge line |
| `0052.00` | `4f7a661b` | HELD-7 | Q33; F2; Q39 |
| `0052.01` | `433e5a27` | FAIL | 7, 8 minor; also Q32 |
| `0052.02` | `6eb42451` | FAIL | 10 minor |
| `0052.04` | `cefb7928` | FAIL | 7 minor |
| `0052.06.01` | `79552f57` | HELD-7 | counted (Q35) |
| `0053.00` | `28f9207b` | HELD-7 | Q33; F2; Q39 |
| `0053.01` | `5872ea1d` | HELD-7 | the R5 fix landed; `:25` container state via page tail (Q31) |
| `0053.06.01` | `ac9b057f` | HELD-7 | counted (Q35) |
| `0054.00` | `fbef265a` | HELD-7 | Q33; F2; Q39 |
| `0055.00` | `5706f71a` | HELD-7 | Q33; F2; Q39; `03.00` Q29 |
| `0055.06.01` | `81144597` | HELD-7 | counted (Q35) |
| `0056.00` | `40a2e09a` | HELD-7 | `seat-01` placement Q34; Q33; Q38/Q40; seat guard findings 1, 2 are builder-side |
| `0056.06.01` | `c45e724f` | HELD-7 | counted (Q35) |
| `0057.00` | `f2e64407` | HELD-7 | Q33; F2; Q39 |
| `0057.01` | `60e9b9d7` | FAIL | 4 major (its 04 disagrees, C3.2); also `.003` is a draft source |
| `0057.06.01` | `1f36649a` | HELD-7 | counted (Q35); open note |

Axioms `00.00.axioms` (R6; exact address `7`, Q28):

| Face | Blob (HEAD) | Verdict | Findings / open question |
|---|---|---|---|
| `00.00.axioms.00` | `2c545c98` | HELD-7 | Q28; Q33; F2 |
| `00.00.axioms.06.01` | `36e06652` | HELD-7 | counted (Q35); Q28 |

Samples (`kernel/samples`):

| Face | Blob (HEAD) | Verdict | Findings / open question |
|---|---|---|---|
| `10.00.00.0000.00` | `72f07c58` | HELD-7 | F1; F10; Q40 |
| `10.11.00.0000.00` | `8063cb8d` | HELD-7 | F1; F10; Q40 |
| `10.11.21.0000.00` | `c103fd01` | HELD-7 | F1; F10; Q40 |
| `10.11.21.0012.00` | `f8fbd488` | HELD-7 | pointer fields not written (Q33); Q39; Q22 |
| `10.11.21.0013.00` | `7a869059` | HELD-7 | page number `0013` is `7` (R11); type for common questions F10/Q33 |
| `10.11.21.1001.00` | `fd65bf33` | HELD-7 | `seat-01` placement Q34; Q38/Q40 |

## Method
- **Repo state:** the repo was read only. `node kernel/build.mjs --check`, `node kernel/build.test.mjs` and `cargo test --workspace --no-fail-fast` ran on a clean `git archive HEAD` in `/workspace/k3-trial`, because the shared working tree holds other lanes' uncommitted `app/` edits.
- **Scratch copies:** hostile tests H1-H8 and the adapted copy check ran in scratch copies. The seqpage export/check ran against the archive's books.
- **Blobs:** blob prefixes are `git hash-object` of each file at HEAD. A seat must name the trial and the exact blob, and any edit needs a new trial (axiom 9).
