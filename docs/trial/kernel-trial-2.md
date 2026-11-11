# Kernel trial 2 (TRIAL-K2): the second axiom 9 hostile pass

Lane TRIAL-K2, 2026-11-11, about 3:25 PM EST. I'm a fresh session that did not build these faces. Under R20 (`DIRECTOR-RULINGS.md:78-80`) that counts as a different view, so a PASS here can qualify a face for an R2 seat (`DIRECTOR-RULINGS.md:7-9`).
I only report findings. Nothing in `kernel/` or `books/` was changed, and nothing was seated. Spec conflicts are not resolved here. They are added to `kernel/QUESTIONS.md` as Q31-Q36, tagged `[TRIAL-K2]`.

**Target:** `kernel/` and `books/` at HEAD `050c7bd`. Kernel and books have not changed since kernel pass 3 (`8c8f780`). Every one of the 55 faces changed after TRIAL-K (`34d5c00`), so every face is in scope.
**Judged against:** `DIRECTOR-RULINGS.md` R1-R20 (the Director's quoted words govern), `docs/spec/`, `docs/CONTRACT.md`, `kernel/QUESTIONS.md`, `kernel/CONFLICTS.md`, and `docs/trial/kernel-trial.md`.

## Summary

| Verdict | Faces |
|---|---|
| PASS (eligible for an R2 seat) | 2 |
| FAIL | 14 |
| HELD-7 (depends on an open question) | 39 |
| **total** | **55** |

| Severity | Findings |
|---|---|
| blocker | 2 |
| major | 7 |
| minor | 11 |

**PASS, eligible for an R2 seat:**
- `00.00.00.0056.01` (blob `112c169c`)
- `10.11.21.1001.01` (blob `5415cef2`)

A seat must name this trial and exactly these blobs. If either file changes, it needs a new trial. R14 lets each one be seated while its page's face 00 stays a draft.

## What held up (checks run)

- **`node kernel/build.mjs --check`:** exit 0. Result: 59 findings, 0 errors, and books identical to `books/` (5 files, 55 entries). All 59 findings are `why missing (4.7)` holes.
- **Hostile builder tests:** run in a scratch copy under `/tmp`, never in the repo.
  - Each of these is rejected with a clear error:
    - counter `06.00` (R9);
    - counter `06.99` (R9);
    - an accented letter in a face (R4, on the face and on the rendered book);
    - a face missing from its registry (R10);
    - a seated face with no `approved-by` (R2);
    - the card key `open`, a tail word (seqAddr.md:280);
    - a content face on page `0000` (R10);
    - an override card missing `achieve:` (R7).
  - See findings 8, 18 and 19 for what got through.
- **R4:** every face source and every book line is plain ASCII 0x20-0x7E plus newline. A byte scan of all `kernel/**/*.md` and `books/*` found nothing else.
- **R9:** no `FF.00` or `FF.99` in any address, file name or book entry. Counters run `01` only. The grammar comment says `01-98` (`0051.02:17`).
- **R10:** every page's registry lists exactly the faces present, across all 16 pages. Page `0000` holds only face 00 in all 4 books.
- **R5 and the follow-up:** every draft entry in every book has a non-empty `reason`. The lookup report prints the reason (`10.11.21.0056.04 -> 00.00.00.0056.04.draft (found draft; draft because ...)`).
- **R8:** every face is `FF.draft`. Book `addr` ends in `.draft` and agrees with `tail`.
- **R13:** no band head is called a door anywhere in `0051` or `0057`.
- **R15:** brand cards on `10.11.21.1001.01` have no 04 card, and the builder skips C3.2 for `type: brand`.
- **Copy check:** I reran `docs/trial/kernel-trial-copycheck.mjs`, extended to `00.00.axioms` and the R4 dash/quote mapping (a scratch copy, not committed). Every "not found" sentence falls into one of these groups:
  - an R1, R9 or R10 merge logged in the page's 06.01 note;
  - an appended ruling quote;
  - a `7` hole;
  - session-note or sample text.
  - The exception is finding 17 (chat text). No invented sentence was found in a 01/02 body.
- **Ruling line citations:** all `DIRECTOR-RULINGS.md:NN` references in kernel/ and books/ point at the right ruling (`:15` R4, `:19` R5, `:25` R6, `:31` R7, `:37` R9, `:40` R10, `:44` R11, `:53` R12, `:56` R13, `:59` R14, `:62` R15, `:65` R16, `:68` R17, `:71` R18).
- **`cargo test --workspace`:**
  - **Working tree:** does not compile (`compute`: missing `identity`, `ask`, `load_queue`). That comes from other lanes' uncommitted edits to `crates/compute` and `crates/seqpage`, not from kernel/.
  - **Clean export of HEAD `050c7bd`:** 387 passed and 3 failed:
    - `compute/tests/http.rs` `brands_and_cards_on_real_books` (finding 20);
    - `trial-compute` `held_r2_gate_basics...` (422 vs expected);
    - `trial-compute` `held_default_listen_is_loopback` (binary not found).
  - The two trial-compute failures are compute-lane items, not kernel.
  - `seqaddr-core` `repo_books` replays all real books cleanly.

## Findings

### 1. blocker: kernel law says a registry-only page is invalid, which contradicts R10
- **Evidence:**
  - `kernel/00.00.00/00.00.00.0052.01.draft.md:35`: "A page is valid when it has face 00 and at least one of faces 01-06 or 08. ... A page with only a registry has no reason to exist."
  - `0052.04.draft.md:34,36` says the same.
- **Breaks:** R10 (`DIRECTOR-RULINGS.md:40-41`): "Page 0000.00 is the only location that exists ... a door page needs no content face."
- **Why it's a blocker:** seated, this would make every door page invalid, including the kernel's own `0000`. That is two live claims (axiom 1). CONFLICTS K10 is marked SETTLED, but the face was never changed. The R10 merge (`0052.06.01:14-15`) rewrote "identity" to "registry", which makes the clash explicit.

### 2. blocker: kernel law says a draft is not active, which contradicts R5
- **Evidence:** `0053.01.draft.md:31`: "| `draft` | being written; not active |".
- **Breaks:** R5 (`DIRECTOR-RULINGS.md:19-20`): "Draft faces count and lookups find them."
- **Why it's a blocker:** every kernel face is a draft. Seated, this card tells readers the whole kernel is inactive, while the builder and core find drafts. CONFLICTS K18 is SETTLED, but the face was not changed.

### 3. major: the book layout still says all of 0001-0099 is overrides
- **Evidence:**
  - `0051.01.draft.md:191`: "`0001-0099` | reserved; a page here is a local override".
  - `0051.04.draft.md:241`: "A page in `0001-0099` that exists in a book is a local override".
- **Breaks:**
  - R7 (`:31-32`): overrides are pages in 0001-0009; 0020-0049 is behavior and 0050-0099 is structure.
  - R17 (`:68-69`): 0020-0099 are working pages.
- **Note:** the R17 quote was appended at `0051.01:198`, but the contradicting rule stays. CONFLICTS D4 lists it, and the face is unchanged.

### 4. major: R18 was appended, but the old matching rules stay in the law
- **Evidence:**
  - `0051.01.draft.md:178`: "Sets across bands are linked by number ... Titles should match; a mismatch is elevated".
  - `0051.04.draft.md:222` says the same.
  - `0057.01.draft.md:35-36`: "Under proposed F.2, membership requires reciprocal Face 08 links ... This amends A2.6".
- **Breaks:** R18 (`:71-72`): "They are matched by the CC and the title." The title is part of the match, not a check after it. R18 answered Q14 against option B, the reciprocal links.
- **Effect:** a reader of the seated card gets three membership rules.

### 5. major: "00 at any level means the door" includes faces
- **Evidence:** `0051.04.draft.md:140`: `00 at any level means "the door".` The same table at `:148` then says `PPPP.00` is "the page's own registry face".
- **Breaks:**
  - R9 (`:37-38`): faces have no sentinels; sentinels apply to desk, shelf, book and page only.
  - R10 (`:40-41`): face 00 is the registry, not a sentinel.

### 6. major: an R9 merge deleted non-sentinel rules from The Loop
- **Evidence:** the merge at `0057.06.01.draft.md:25` struck the whole paragraph at `workflow-loop.003.md:160` from `0057.01` The Loop (`:82-88`). That paragraph includes "The counter keeps the same identity throughout" and "Compute records each handoff in its history before showing the card in the next column."
- **Breaks:**
  - R9 removes only the `05.00` board.
  - R8 and `drafting.md` require one merge per change, and "A rewrite from memory silently drops what the model did not remember" (`drafting.md:7`). The lifecycle-history rule was lost.

### 7. major: the Registry Face law card leaves out what R10, R12 and R19 put in face 00
- **Evidence:**
  - `0052.01.draft.md:3`: "`PPPP.00` holds the page's stamp: address, title, state."
  - The same wording is at `0052.02.draft.md:5` and `0052.04.draft.md:5`.
- **Breaks:**
  - R10 (`:41`): face 00 "lists the page's faces".
  - R12 Read (`:54`): "address, title, type, state".
  - R19 (`:75-76`): stamp, type, and a per-type registry.
- **Effect:** the kernel's own 00 faces do list their faces, so the law and the practice disagree.

### 8. major: the builder misses in-place overrides and C3.2 across the lookup
- **Evidence:**
  - `kernel/build.mjs:196-225` (`resolve`, `lookupReport`) checks only cards on 0001-0009 pages.
  - **Hostile test:** I added `10.11.21.0056.00/.04.draft.md` (a book face at the kernel's spot). The build ran with 0 errors and the same 59 findings. The book face silently replaced kernel `0056.04` and hid the kernel 04 cards `new-face`, `exceptions` and `drafting-ops` for book 10.11.21.
- **Breaks:**
  - R7 (`:32`): "An override does not silently replace a face in place."
  - C3.2 (`seqAddr.md:184`).
- **Note:** the TRIAL-K fix pass (finding 21) says a C3.2 check across the lookup was added. It isn't in the current builder.

### 9. major: R19 is not applied to any face 00
- **Evidence:**
  - `build.mjs:4`: "Rulings applied: ... R1-R10". Kernel pass 3 lists R11-R18.
  - All 16 stamps carry `address`, `title`, `state` and `type` only.
  - Every registry says `format: 7` and lists faces as bullets.
  - The SEQPAGE draft `docs/spec/face00.md` (commit `050c7bd`, DRAFT) proposes `why-draft`, `axioms` and `lineage` stamp fields and a `faces:` registry line.
- **Breaks:** R19 (`:75-76`): "the stamp portion (address, title, state, axioms, lineage), (b) the page's type, and (c) a registry whose fields depend on the page type."
- **Effect:** R19 asks for the detail only as a draft for the Director, so every face 00 is HELD-7 until that draft is ruled on (Q33).

### 10. minor: R1 wording leftovers
- `0051.01.draft.md:85` "has an door page": the mechanical merge broke the article.
- `0051.01.draft.md:87` and `0051.04.draft.md:124` keep the table header "Identity page".
- `0052.04.draft.md:5`: "A page is identified by its face 00".
- **Breaks:** R1 (`:5`): "use the word 'door'".

### 11. minor: merge-log lines are cut off at the colon
- `0051.06.01:56,57,59`, `0052.06.01:134,140,142,145`, `0055.06.01:10,11` and `0057.06.01:22,23` end at "R13 (DIRECTOR-RULINGS.md".
- **Effect:** the line number and text of each appended ruling are lost from the lineage note (axiom 6).

### 12. minor: R14 is quoted as "door face"
- **Evidence:** `0052.01.draft.md:41`: "Q10: can a seated face sit on a page whose door face is still a draft?"
- **Breaks:** under R9 and R10, face 00 is the registry, not a door. Which meaning R14 has is raised as Q32.

### 13. minor: the stamp example is incomplete, and Card Shape is written twice
- **Evidence:**
  - `0052.02.draft.md:106`: `form: ---\ntitle: tools\n---` has no address, state or type (R12).
  - `0052.02.draft.md:121-122` and `:124-128` state the field-line rule twice.

### 14. minor: two 04 bodies are a copied face-01 row
- **Evidence:** `0052.04.draft.md:106` (`lineage-on-the-page`) and `:112` (`links-face`) are both the Face Jobs table row for `08`.
- **Breaks:** C3.2 finding "the 04 body copies the 01 body" (`0052.01:74`). The body doesn't explain lineage.

### 15. minor: the axioms carry a written menu card
- **Evidence:** `kernel/00.00.axioms/00.00.axioms.03.draft.md:1-4` writes a `type: menu` card.
- **Breaks:**
  - "menu | entries derived by the compute" (`0054.02:8`, `decisions.md:512-522`).
  - "Derived content ... is calculated and never drafted" (`drafting.md:40`).
- **Note:** this is TRIAL-K finding 16 again, after the R6 move.

### 16. minor: the axioms note still lists questions that are answered
- `00.00.axioms.06.01.draft.md:7` asks "does a fresh sitting of the same model count?" R20 (`:78-80`) answered it.
- `:12` lists "The axioms' own page number". R6 (`:25-26`) answered it.

### 17. minor: the override sample's body is chat, not spec
- **Evidence:** `10.11.21.0001.04.draft.md:9` is Prima chat t42u. It is not in docs/spec or DIRECTOR-RULINGS.
- **Effect:** the copy check can't verify it. This is TRIAL-K finding 18, still open.

### 18. minor: the builder's R5 message is misleading, and its ruling header is stale
- **Evidence:**
  - A registry line with no "draft because" text fails only as "registry lists ... but the page has ..." (hostile test T11), not as "a draft must say why (R5)".
  - The `build.mjs:4` header still says R1-R10.

### 19. minor: the builder accepts override cards outside 0001-0009
- **Evidence:** moving the 0001 override page to `0020` (behavior) gave 0 errors and 0 findings. The lookup simply stopped reporting the override (hostile test T12).
- **Breaks:** R7 (`:31-32`).

### 20. minor (cross-lane, not a kernel fault): a compute test still expects the removed bob 04 card
- **Evidence:** `crates/compute/tests/http.rs:261` expects a 04 card for `bob` on the real books. R15 removed it (`10.11.21.1001.00:16`), and the kernel is right.
- **Effect:** the test fails at HEAD `050c7bd`. Route this to the COMPUTE lane.

## Per-face verdicts

Kernel book `00.00.00`:

| Face | Verdict | Findings / open question |
|---|---|---|
| `00.00.00.0000.00` | HELD-7 | R19 registry fields (9, Q33); door title K17 |
| `0051.00` | HELD-7 | R19 (9, Q33) |
| `0051.01` | FAIL | 3 major, 4 major, 10 minor; also R17 split Q30 |
| `0051.02` | HELD-7 | the grammar can't parse `00.00.axioms.FF` (Q28); no finding of its own |
| `0051.04` | FAIL | 3, 4, 5 major; 10 minor |
| `0051.06.01` | FAIL | 11 minor |
| `0052.00` | HELD-7 | R19 (9, Q33) |
| `0052.01` | FAIL | 1 blocker; 7 major; 12 minor |
| `0052.02` | FAIL | 7 major; 13 minor |
| `0052.04` | FAIL | 1 blocker; 7 major; 10, 14 minor |
| `0052.06.01` | FAIL | 11 minor |
| `0053.00` | HELD-7 | R19 (9, Q33) |
| `0053.01` | FAIL | 2 blocker; also page state stamp vs tail (Q31) |
| `0053.02` | HELD-7 | copies `workflow-loop.003.md` (state: draft, "Director review required"); Q21 |
| `0053.04` | HELD-7 | `4.7` holes; `:16` container state via page tail (Q31) |
| `0053.06.01` | HELD-7 | counted face, never seated (Q35); session note open |
| `0054.00` | HELD-7 | R19 (9, Q33) |
| `0054.01` | HELD-7 | the type list lacks override/question/door types (Q33) |
| `0054.02` | HELD-7 | the table lacks `question` (CONFLICTS D14), which the samples use |
| `0054.04` | HELD-7 | `4.7` holes |
| `0054.06.01` | HELD-7 | counted (Q35); open note |
| `0055.00` | HELD-7 | R19 (9, Q33) |
| `0055.01` | HELD-7 | `03.00` menu or door (Q29) |
| `0055.02` | HELD-7 | `03.00` row (Q29) |
| `0055.04` | HELD-7 | `03.00` row `:83` (Q29); `4.7` holes |
| `0055.06.01` | FAIL | 11 minor |
| `0056.00` | HELD-7 | R19 (9, Q33) |
| `0056.01` | **PASS** | none. The principle is settled (`decisions.md:307`, `drafting.md:3`) and R8 agrees. The R9 merge at `:21` is logged. |
| `0056.02` | HELD-7 | "Proposed:" mechanism (`decisions.md:320`) awaits the Director; R2 can't answer it |
| `0056.04` | HELD-7 | `4.7` holes; drafting-ops is proposed |
| `0056.06.01` | HELD-7 | counted (Q35); open note |
| `0057.00` | HELD-7 | R19 (9, Q33) |
| `0057.01` | FAIL | 4, 6 major; also `.003` is a draft source |
| `0057.02` | HELD-7 | `.003` is a draft source |
| `0057.04` | HELD-7 | `.003`; `4.7` holes |
| `0057.06.01` | FAIL | 11 minor |

Axioms `00.00.axioms` (R6; exact address `7`, Q28):

| Face | Verdict | Findings / open question |
|---|---|---|
| `00.00.axioms.00` | HELD-7 | Q28; R19 (9, Q33) |
| `00.00.axioms.01` | HELD-7 | Q28 |
| `00.00.axioms.02` | HELD-7 | Q28 |
| `00.00.axioms.03` | FAIL | 15 minor; also Q28 |
| `00.00.axioms.04` | HELD-7 | Q28 |
| `00.00.axioms.06.01` | FAIL | 16 minor |

Samples (`kernel/samples`):

| Face | Verdict | Findings / open question |
|---|---|---|
| `10.00.00.0000.00` | HELD-7 | R19 (Q33); K17 |
| `10.11.00.0000.00` | HELD-7 | R19 (Q33); K17 |
| `10.11.21.0000.00` | HELD-7 | R19 (Q33); K17 |
| `10.11.21.0001.00` | HELD-7 | R19 (Q33); no override page type (Q33) |
| `10.11.21.0001.04` | FAIL | 17 minor; also the override form Q24, the approver (D4), and whether the lookup applies it (Q36) |
| `10.11.21.0012.00` | HELD-7 | R19 (Q33) |
| `10.11.21.0012.03.14` | HELD-7 | counted dictionary section (Q22, Q35); Q29 |
| `10.11.21.0012.03.16` | HELD-7 | counted dictionary section (Q22, Q35); Q29 |
| `10.11.21.0013.00` | HELD-7 | page number `7` (R11 placement); R19 (Q33) |
| `10.11.21.0013.01` | HELD-7 | `question` card fields are not given by the Director (D14) |
| `10.11.21.0013.04` | HELD-7 | follows 0013.01 |
| `10.11.21.1001.00` | HELD-7 | R19 (Q33) |
| `10.11.21.1001.01` | **PASS** | none. The brand cards match the `brands.md:34-41` form, R15 means no 04 card, the forms are case-exact, and the dictionary index (`0012.03.14`, `.16`) points to them in the right sections (`decisions.md:458-459`). |

## Method
- `node kernel/build.mjs --check` was run in the repo. The hostile builder tests T1-T13 ran only in a scratch copy at `/tmp/k2-hb`.
- A byte scan covered R4, plus a registry-vs-files diff per page and a book scan for draft reasons, `addr` and `tail` agreement, face sentinels and duplicate `addr` values.
- The copy check is `docs/trial/kernel-trial-copycheck.mjs`, adapted in `/tmp`: it skips the `docs/spec/examples/` directory, covers `00.00.axioms`, and maps R4 dashes and quotes. Without that change, the committed script crashes with EISDIR on `docs/spec/examples/`.
- `cargo test --workspace` was run on a clean `git archive` of HEAD (`CARGO_TARGET_DIR=target/k2-trial`), because the shared working tree holds other lanes' uncommitted changes that don't compile.

## Fix pass (KERNEL pass 4, 2026-11-11 EST)

Seats first: both PASS faces were seated at the trialed blobs (`112c169c`, `5415cef2`) before anything else was touched (commit `42ffbc9`); they were not edited after.

| # | Result | How |
|---|---|---|
| 1 | fixed | 0052.01/04 Which Faces: "except a door page 0000, which holds only face 00 (R10)" merged into the rule and the 04 why (builder merge list updated). |
| 2 | fixed | 0053.01 Tail Meanings: `draft` "being written; draft faces count and lookups find them (R5)". |
| 3 | fixed | 0051.01 A2.7 row becomes `0001-0009` override (R7, none while the app is built, R21) plus the seqAddr.md 0010-0099 rows; 0051.04 "A page in `0001-0009`..." (R7, R21). Exact four-way split still `7` (Q30). |
| 4 | fixed | 0051.01/04 Bands: matched by number and title (R18); 0057.01 Bound Bands: the F.2 line struck. Elevation of a same-CC, different-title pair raised as Q37. |
| 5 | fixed | 0051.04 Door Rule: "00 on the desk, shelf, book or page axis means the door (R1, R9); face 00 is the registry, not a sentinel (R10)". |
| 6 | fixed | 0057.01 The Loop: `workflow-loop.003.md:160` restored (matches the first-pass copy in `07b9bc0`) with only the `05.00` board sentences struck. |
| 7 | fixed | 0052.01/02/04: face 00 holds stamp (address, title, type, state) and the registry that lists the faces, fields by page type (R10, R12, R19). |
| 8 | fixed | build.mjs `crossChecks`: in-place replacement refused; C3.2 checked across the lookup. Tests in `kernel/build.test.mjs`. |
| 9 | partly, held | Every face 00 moved to the face00.md layout as a DRAFT (no meaning changed). Per-type fields and the R19 field set wait on the Director (Q33, Q38). |
| 10 | fixed | "a door page", "Door page" headers; 0052.04 A4.2 line (with 7). |
| 11 | fixed | merge-log lines now carry the full appended ruling text. |
| 12 | fixed | R14 quote's question now says "face 00"; which door R14 means stays Q32. |
| 13 | fixed | Stamp `form:` uses the face00.md 4.5 door shape (with `form-source:`); duplicate Card Shape line struck. The format.md:74 JSON example is left as copied. |
| 14 | fixed | 04 Lineage On The Page and Links Face are hole bodies (`7`) instead of a copied 01 row. |
| 15 | fixed | axioms face 03 (written menu) removed. |
| 16 | fixed | axioms note marks R20 and R6 answers. |
| 17 | moot | override sample parked (R21). |
| 18 | fixed | R5 message names the missing `why-NN:`; header lists R1-R21. |
| 19 | fixed | override fields outside 0001-0009 refused (R7); any 0001-0009 page refused (R21). |
| 20 | routed | COMPUTE lane (`crates/compute/tests/http.rs:261`); not a kernel change. |

Every face changed in this pass needs a new trial before an R2 seat (axiom 9).
