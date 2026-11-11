# Kernel trial WHYS-2 (TRIAL-WHYS-2): hostile pass on the WHY-FIX scoping of four partial why fills

Lane TRIAL-WHYS-2, 2026-11-11, about 6:45 PM EST (box git stamps -0600). I'm a fresh session that did not write WHY-FIX, the first TRIAL-WHYS, WHY-GAPS.md or the builder. Under R20 (`DIRECTOR-RULINGS.md:78-80`) that counts as a different view (R2, axiom 9).
I only report. Nothing in `kernel/`, `books/`, `crates/`, `app/` or `kernel/QUESTIONS.md` was changed. Nothing was seated, pushed, merged or deleted. New questions are in this file only, tagged `[TRIAL-WHYS-2]`.

**Target:** `8cb7cd5` (WHY-FIX). Later commits on `build`: `bbdc1a9` (KERNEL pass 11, only `kernel/build.mjs` and `kernel/build.test.mjs`) and `5f2f43d` (R23, only `DIRECTOR-RULINGS.md`). Neither touches the two faces, so the blobs at HEAD are the blobs at `8cb7cd5`:

| Face | Blob (`git rev-parse 8cb7cd5:` = `HEAD:`) |
|---|---|
| `kernel/00.00.00/00.00.00.0051.04.draft.md` | `4fcba4a15786d20b9a7321793cb1a1d7229aa1bc` |
| `kernel/00.00.00/00.00.00.0057.04.draft.md` | `855019c344daa6f01a3b2518f5bc6d5aff11b56b` |

**Judged against:** `docs/trial/kernel-trial-whys.md` (findings 1-4, W1, W2), `docs/design/WHY-GAPS.md` "Status: partial fills scoped (WHY-FIX lane)", `DIRECTOR-RULINGS.md` R1-R23, Axioms 4, 7, 9, the cited spec lines, `kernel/build.mjs` `checkWhy` and the 01/04 match in the face loop.
**Rules used:** a PASS means the fix is right: each original card is back at `why: 4.7` and reported, each part card holds the exact checked words and cite, its Scope line and `source:` are accurate, nothing is invented. W1 and W2 stay open and are not held against a face. Q30 on 0051.04 `book-layout` is not held against this fix.

## Summary

| Verdict | Faces |
|---|---|
| PASS on this fix, then HELD-7 | 1: 0051.04 (fix correct; face held on Q30 for `book-layout`, and still holds other `4.7` gaps) |
| FAIL | 1: 0057.04 (finding 1: the Reviewer part card cites the Compute row) |
| **total** | **2** |

| Severity | Findings |
|---|---|
| blocker | 0 |
| major | 1 (finding 1) |
| minor | 2 (findings 2, 3) |
| info | 2 (findings 4, 5) |

**PASS list, eligible for an R2 seat:** none. Neither face is seat-ready: 0051.04 still has `4.7` gaps and Q30; 0057.04 fails finding 1 and still has 2 grade B gaps (`the-loop`, `pack-header`) plus the 4 now reported again.

**Plain words:** the fix works. All four cards that were only partly explained are back on the builder's missing list, so the holes show again. Each part reason moved to its own card, word for word, with the same cited line, and the builder still checks those words. Three of the four part cards are right. The fourth, on page 0057, points to the wrong row of the roles table: it names line 30, which is the Compute row, but the Reviewer row is line 29. The builder can't catch that, because it only checks the line the why words come from. That is a one-line fix. Page 0051 passes this fix but stays held on Q30.

## Checks run (real output)

`/tmp/tw2` is a fresh `git clone` of the shared repo, branch `build`, HEAD `bbdc1a9` at clone time (HEAD later `5f2f43d`, rulings only).

**`node kernel/build.mjs --check`** at HEAD (builder of pass 11), exit 0:
```
... (48 findings, all "why missing (4.7)")
checked  books/00.00.00.book  50 entries
checked  books/00.00.axioms.jsonl  7 entries
checked  books/10.00.00.book  1 entries
checked  books/10.11.00.book  1 entries
checked  books/10.11.21.book  15 entries
seats 26
48 findings, 0 errors
```
Same at `8cb7cd5` (builder of `299b308`): `seats 26`, `48 findings, 0 errors`.

**The four gaps show again.** Findings at `299b308` vs HEAD, sorted diff: exactly 4 added, 0 removed:
```
> finding  00.00.00.0051.01.draft.md: 04 kernel-and-branches: why missing (4.7)
> finding  00.00.00.0051.01.draft.md: 04 which-pages-need-a-title: why missing (4.7)
> finding  00.00.00.0057.01.draft.md: 04 risk-and-governing-targets: why missing (4.7)
> finding  00.00.00.0057.01.draft.md: 04 roles: why missing (4.7)
```

**Part cards hold the exact checked words and cite.** A script read each original card at `299b308` and each part card at HEAD:

| Part card | words same | cite same | original card now |
|---|---|---|---|
| Which Pages Need A Title: Pages 0001-0999 Part | yes | yes, decisions.md:132 | `why: 4.7` |
| Kernel And Branches: Desk 00 Part | yes | yes, decisions.md:380 | `why: 4.7` |
| Roles: Reviewer Part | yes | yes, Axioms.md:29 | `why: 4.7` |
| Risk And Governing Targets: Recording Part | yes | yes, workflow-loop.003.md:150 | `why: 4.7` |

**checkWhy still tests the part cards** (`build.mjs:680`: every 04 card with a why other than `4.7` goes to `checkWhy`). Mutations in a scratch clone `/tmp/tw2m`, each restored after:
- 0051 part why "name" -> "title": `ERROR ... 04 card which-pages-need-a-title-pages-0001-0999-part: why is not on decisions.md:132`, `1 errors; nothing written`.
- 0057 recording part cite :150 -> :152: 1 error.
- 0057 reviewer part "easiest" -> "hardest": 1 error.
- 0051 desk 00 part why cut to "The kernel is small.": 1 error.

**Only the four scoped cards changed.** `git show 8cb7cd5 -- kernel/` has exactly the 4 hunks above; the other 11 grade A fills are untouched. In `books/00.00.00.book` the last `put` for `00.00.00.0051.04.draft` and `00.00.00.0057.04.draft` has a `body` equal to the file on disk.

**Seats intact.** A script compared every `seat-NN: ... blob:` in every face 00 to `git rev-parse HEAD:<face>`: 26 seats, 0 differ (17 in `kernel/00.00.00`, 2 in `kernel/00.00.axioms`, 7 in `kernel/samples/10.11.21`). Seated `00.00.00.0052.04` is still blob `e9ca59a1d708acfd57b9e5f7e6b758e41e4fde6f` (same at `299b308`). `git diff --name-only 299b308 HEAD` lists no seated face.

**Builder tests:** `node --test kernel/build.test.mjs`: pass 1, fail 0 (the file runs as one top-level test).

## The four scoped fills, one by one

| # | Card | Back at 4.7 + reported | Part card words/cite | Scope line | `source:` on part card | Invented words |
|---|---|---|---|---|---|---|
| 10 | 0051 `which-pages-need-a-title` | yes | yes | accurate, but the `7` line names one leftover part of three (finding 2) | decisions.md:132, right | none: bullet "Pages 0001-0999 may have a title; their number is already their name." is decisions.md:132 word for word |
| 18 | 0051 `kernel-and-branches` | yes | yes | accurate: `7` names 01-09, 10-98, 99; Scope names desk 00 only and the C5.2 borrow (W2) | decisions.md:256-262, right (258 is desk 00) | none: "Desk `00` is the kernel. Its own book is `00.00.00`." restates seqAddr.md:36 / decisions.md:258 |
| 53 | 0057 `roles` | yes | yes | accurate: Reviewer row only, other four stay 4.7 | **workflow-loop.003.md:30 is the Compute row; the Reviewer row is :29 (finding 1)** | none in the why; bullet paraphrases :29 and Axioms.md:29 |
| 55 | 0057 `risk-and-governing-targets` | yes | yes | accurate; `7` line omits a little (finding 2) | workflow-loop.003.md:150, right | "Compute records the inputs..." is a reading of :150 (finding 3) |

## Verdicts

| Face | Blob | Verdict | Why |
|---|---|---|---|
| `00.00.00.0051.04.draft` | `4fcba4a15786d20b9a7321793cb1a1d7229aa1bc` | **PASS on this fix; face HELD-7 (Q30)** | #10 and #18 scoped correctly; finding 2 (minor) only. The face stays a draft: `book-layout` depends on Q30, and it still holds `4.7` gaps (now including #10, #18). Not recommended for a seat. |
| `00.00.00.0057.04.draft` | `855019c344daa6f01a3b2518f5bc6d5aff11b56b` | **FAIL** | Finding 1 (major): the Reviewer part card's `source:` and bullet cite workflow-loop.003.md:30, the Compute row. #55 is correct (findings 2, 3 minor). Even after the fix the face is not seat-ready (grade B gaps `the-loop`, `pack-header`; #53, #55 reported again). |

## Findings

**1. major: `Roles: Reviewer Part` (0057.04) cites the wrong row.** Its `source:` is `[01 / Roles] workflow-loop.003.md:30` and its bullet ends `[workflow-loop.003.md:30, Axioms.md:29]`. At HEAD (and since `420fc98`, the only commit to that file) line 30 is `| Compute | the compute | ...`; the Reviewer row, "a view other than the builder **(approved S10)**", is line 29. The words in the bullet ("a view other than the builder") come from :29. The why itself (Axioms.md:29) is right and checked. The builder does not catch this: `checkWhy` reads only the `why: docs/spec/FILE:LINE` cite, not the 01 source line. Axiom 4: a citation that points at the wrong row is an unchecked claim that looks checked. Fix: `:30` -> `:29` in both places, then a trial.

**2. minor: two `7` lines name less than is unexplained.** On `which-pages-need-a-title` (0051.04) the `7` line names only "why pages 1000 and up must have a title". The card also says page 0000 has none, and that a stamp title is the truth and a mismatch is elevated (A2.8, A3.2); TRIAL-WHYS finding 1 counted three rules. decisions.md:132 does give a reason in brackets for 0000 ("it holds the book's title in its stamp"), but the stamp-is-truth and mismatch rule has no reason named anywhere on the face. On `risk-and-governing-targets` (0057.04) the `7` line skips "the effective risk is the higher of that floor and the lead's proposal" (:150) and the classify-before-delegation rule (:152). Not a FAIL: the cards are back at `4.7`, so the builder reports them whole and no hole is hidden. Make the `7` lines complete when W1 is decided.

**3. minor: the recording part bullet adds a subject.** "Compute records the inputs and the reason for the effective risk." workflow-loop.003.md:150 says "Record the inputs and reason so a reviewer can reproduce the decision." with no subject; the sentence before has Compute deriving the floor, and the roles table (:30) has Compute "records claims". A fair reading, not invented, but it is a reading. Report only.

**4. info: nothing ties a part card to its parent.** The builder matches 01 keys to 04 keys; a 04 card with no 01 key (like `roles-reviewer-part`) is accepted and checked by `checkWhy`, but nothing checks that its parent exists or that its Scope line is true. Today the link is only the title "<card>: <part> Part". Part of W1 (question X1 below).

**5. info: `checkWhy` accepts any substring of the cited line.** A why cut to a fragment that changes meaning would pass if the fragment is on the line (my "The kernel is small." test failed only because of the added full stop). Pre-existing design, not part of this fix. Question X2.

## Questions [TRIAL-WHYS-2] (saved for the Director; in this file only)

**X1. [TRIAL-WHYS-2] If part cards stay (W1 option C or this WHY-FIX form), should the builder check that a part card's parent exists and is still at `4.7` or `7`?**
- Option A: yes, a `<card>: <part> Part` 04 card needs a matching parent card on the same face.
- Option B: no, a part card is a normal 04 card; trials check the link. `7`.

**X2. [TRIAL-WHYS-2] Should a why be a whole sentence or clause of its cited line, not any substring?**
- Option A: whole sentence or clause only.
- Option B: any substring, as now; trials judge meaning. `7`.

W1 and W2 (`kernel-trial-whys.md`) stay open; not decided here.
