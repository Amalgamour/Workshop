# Kernel trial WHYS (TRIAL-WHYS): hostile pass on the 15 grade A why fills in five draft 04 faces

Lane TRIAL-WHYS, 2026-11-11, about 5:30 PM CST. I'm a fresh session that did not write these fills, WHY-GAPS.md or the builder. Under R20 (`DIRECTOR-RULINGS.md:78-80`) that counts as a different view (R2, axiom 9).
I only report. Nothing in `kernel/`, `books/`, `crates/`, `app/` or `kernel/QUESTIONS.md` was changed. Nothing was seated, pushed, merged or deleted. New questions are in this file, tagged `[TRIAL-WHYS]`.

**Target:** the five draft 04 faces changed in `a718c91` (WHY-GAPS). HEAD is `a09b043`; no later commit touched them, so the blobs at HEAD are the blobs at `a718c91`:

| Face | Blob (`git rev-parse a718c91:` = `HEAD:`) |
|---|---|
| `00.00.00.0051.04.draft` | `cbe32fdf3479f16c9106e7a41a1f59dd2e4dc374` |
| `00.00.00.0054.04.draft` | `8007a41c2225135e45bac704df07c5a3b54ac59d` |
| `00.00.00.0055.04.draft` | `eb1e0f6e2a0aec4ea3937ecd5ffc8da5ac64ff91` |
| `00.00.00.0056.04.draft` | `4d837c0646c21d4755e22a592aca70e27b3d04e2` |
| `00.00.00.0057.04.draft` | `be6b931b5b4147454790693d319fa0c4110453cd` |

**Judged against:** `docs/design/WHY-GAPS.md` (the table and the "Status: grade A filled" section), `DIRECTOR-RULINGS.md` R1-R22, Axioms 4, 7, 9, the cited spec lines, `kernel/build.mjs` `checkWhy`, `kernel/QUESTIONS.md` (Q30 read only), format from `docs/trial/kernel-trial-8.md`.
**Rules used:** a PASS means the new `why:` and `source:` lines are right. A face can PASS as a draft and still hold other `4.7` gaps (grade B, C or skipped). No face is recommended for a seat while it still holds leftover gaps or an open Director question.

## Summary

| Verdict | Faces |
|---|---|
| PASS (as a draft, not recommended for a seat) | 3: 0054.04, 0055.04, 0056.04 |
| FAIL | 2: 0051.04 (finding 1), 0057.04 (finding 2) |
| HELD-7 | 0 (0051.04 would be HELD-7 on Q30 after finding 1 is fixed) |
| **total** | **5** |

| Severity | Findings |
|---|---|
| blocker | 0 |
| major | 2 (finding 1: `which-pages-need-a-title` why covers one rule of three with no scope mark; finding 2: `roles` why covers one role of five with no scope mark) |
| minor | 5 (findings 3-7) |

**PASS list, eligible for an R2 seat:** none this pass.

Faces whose new why lines pass, kept as drafts (each still holds leftover `4.7` gaps, so no seat is recommended; blobs for the record only):
`00.00.00.0054.04.draft` blob `8007a41c2225135e45bac704df07c5a3b54ac59d` (1 grade B gap left: #40);
`00.00.00.0055.04.draft` blob `eb1e0f6e2a0aec4ea3937ecd5ffc8da5ac64ff91` (7 gaps left: 5 B, 2 C);
`00.00.00.0056.04.draft` blob `4d837c0646c21d4755e22a592aca70e27b3d04e2` (1 grade C gap left: `exceptions`, a Director question).

**Plain words:** all 15 new why lines are copied word for word from WHY-GAPS.md, every one of them really is on the spec line it cites, and nothing else on the cards was changed. Two of the fills say more than they should. On page 0051, the why for "which pages need a title" only explains why low pages may skip a title, but it now reads as the reason for the whole card, and the builder stopped reporting the missing part. On page 0057, the why for "roles" only explains why the reviewer is a separate person, but it now stands as the reason for all five roles. Those two faces fail until the gap is marked or the fill is taken back. The other three faces pass as drafts.

## Checks run (real output)

`/tmp/tw` is a fresh `git clone` of the shared repo, branch `build`, HEAD `a09b043`.

**`node kernel/build.mjs --check`**: exit 0.
```
... (44 findings, all "why missing (4.7)")
checked  books/00.00.00.book  50 entries
checked  books/00.00.axioms.jsonl  7 entries
checked  books/10.00.00.book  1 entries
checked  books/10.11.00.book  1 entries
checked  books/10.11.21.book  15 entries
seats 26
44 findings, 0 errors
```

**Seated faces untouched.** `git diff --name-only 6d3a0e6 HEAD` lists only `books/00.00.00.book`, `docs/BUILD-LOG.md`, `docs/design/WHY-GAPS.md`, `docs/trial/kernel-trial-9.md`, `kernel/QUESTIONS.md` and the five draft 04 files. No seated face file changed. All 26 `seat-` lines (17 in `kernel/00.00.00`, 2 in `kernel/00.00.axioms`, 7 in `kernel/samples/10.11.21`) were checked by a script that compared each `blob:` to `git rev-parse HEAD:<face>`: 26 match, 0 differ. Seated `00.00.00.0052.04` is still blob `e9ca59a1d708acfd57b9e5f7e6b758e41e4fde6f`, not touched.

**Only why and source lines changed.** `git diff -U0 a718c91^ a718c91 -- kernel/` has 15 hunks; every removed or added line starts with `source:` or `why:` (a filter for any other `+`/`-` line printed nothing). Each `source:` line only gains `; why: docs/spec/FILE:LINE` at the end. In `books/00.00.00.book` exactly 5 entries changed (lines 6, 27, 34, 41, 48: the five 04 drafts), only in `body`.

**Words and lines.** A script read every `; why: docs/spec/FILE:LINE` card in the five faces (39 cards), took the `why:` text, and tested it as a substring of the cited line at `a718c91` after the `checkWhy` normalizing (em dash, section sign, curly quotes). All 15 new fills: OK. (One older, pre-existing card is not a literal match: 0051.04 `overflow`, decisions.md:250, the R18 merge "matched by number and title" that the builder maps on purpose; see 0051.06.01:57. Not part of this commit.)

## The 15 fills, one by one

"Words" = the `why:` text equals the WHY-GAPS.md table cell. "On line" = the words are on the cited line. "Fits" = the line is a reason for this card (the hostile part).

| # | Face / card | Cited line | Words | On line | Fits | Note |
|---|---|---|---|---|---|---|
| 8 | 0051 `faces-carry-no-title` | decisions.md:72 | yes | yes | yes | Same paragraph as the rule. |
| 10 | 0051 `which-pages-need-a-title` | decisions.md:132 | yes | yes | **part, not scoped** | Finding 1. |
| 15 | 0051 `many-targets` | decisions.md:227 | yes | yes | yes | A5.2's own reason. |
| 16 | 0051 `back-links` | Axioms.md:27 | yes | yes | yes | Axiom 8 names "linked both ways (a link and its back-link)". Also covers the second bullet (hierarchy only through links). |
| 18 | 0051 `kernel-and-branches` | decisions.md:380 | yes | yes | part, self-scoped | Finding 3. |
| 39 | 0054 `card-types` | decisions.md:287 | yes | yes | yes, by analogy | Line 287 is in C1.4 (page types). C8.9 (decisions.md:501) says "A card type is to a card what a page type is to a page (C1.4)", and :509 repeats "defined in the kernel ... `owner: kernel-only`". Finding 6. |
| 41 | 0055 `card-key-address` | decisions.md:421 | yes | yes | yes | Same sentence as the rule (C8.2). |
| 43 | 0055 `brand-cards` | decisions.md:418 | yes | yes | yes | C8.1: a meaning is recorded as a brand, so it needs a card that holds it. Why meters are on the card is not covered (that is #44 `meters`, grade C, still open). |
| 46 | 0055 `resolving-a-word` | brands.md:7 | yes | yes | yes | Explains why the dictionary is looked up first. Why this exact fallback order is not written; acceptable, the card's point is "look it up, then state the assumption". |
| 51 | 0056 `new-face` | drafting.md:7 | yes | yes | yes | drafting.md "## Why" section; R8 (DIRECTOR-RULINGS.md:34) agrees. |
| 53 | 0057 `roles` | Axioms.md:29 | yes | yes | **part, not scoped** | Finding 2. |
| 54 | 0057 `packs` | workflow-loop.003.md:8 | yes | yes | yes, as a reading | Finding 5. I accept it as the fresh reviewer: a pack is the "agents.md-style build list for a builder" (:99), the device that lets a model run a pass without history. |
| 55 | 0057 `risk-and-governing-targets` | workflow-loop.003.md:150 | yes | yes | part, self-scoped | Finding 4. |
| 57 | 0057 `return-placement` | workflow-loop.003.md:183 | yes | yes | yes | Why a failed return is still recorded on its counter. |
| 59 | 0057 `why-questions` | workflow-loop.003.md:258 | yes | yes | yes | Same section 9; the questions are the pass-4 move-on point. |

**Fills that check out fully:** #8, #15, #16, #39, #41, #43, #46, #51, #54, #57, #59 (11). **Self-scoped partials, acceptable with a note:** #18, #55. **Over-claims:** #10, #53.

## Verdicts

| Face | Verdict | Why |
|---|---|---|
| `00.00.00.0051.04.draft` | **FAIL** | #10 over-claims (finding 1). Even when fixed, the face is not seatable: the `book-layout` card is on this face and its table depends on Q30 (the four sections below 0100, open), and it still holds 15 `4.7` gaps (10 grade B, 3 grade C, and the 2 skipped grade A cards `finding` and `book-layout`). After finding 1 is fixed this face would be HELD-7 on Q30. #8, #15, #16 pass; #18 passes with finding 3. |
| `00.00.00.0054.04.draft` | **PASS** (draft) | #39 correct (finding 6 is wording only). 1 grade B gap left (#40). |
| `00.00.00.0055.04.draft` | **PASS** (draft) | #41, #43, #46 correct. 7 gaps left (5 B, 2 C). |
| `00.00.00.0056.04.draft` | **PASS** (draft) | #51 correct. 1 grade C gap left (`exceptions`), a Director question, so no seat. |
| `00.00.00.0057.04.draft` | **FAIL** | #53 over-claims (finding 2). #54, #57, #59 pass; #55 passes with finding 4. 2 grade B gaps left (`the-loop`, `pack-header`). |

## Findings

**1. major: `which-pages-need-a-title` (0051.04) now reads as fully explained, but only one of its three rules has a reason.** The card says: pages 1000+ must have a title, 0001-0999 may, 0000 has none (plus the stamp-is-truth check). The new why "their number is already their name" (decisions.md:132) explains only the "may" part. WHY-GAPS.md row 10 says so ("Why pages 1000+ must have a title is not written (part stays 4.7)"), but nothing on the face says it: no scope mark, no `7` for the rest. The builder no longer reports this card, so the hole for the 1000+ rule has disappeared from the findings (axiom 7: a hole is kept, not closed; axiom 4: do not let a partial reason feel finished). Fix options: mark the scope on the card (for example a `7` line naming the unexplained part), or put `why: 4.7` back until the whole rule has a source. How a partial why should be marked is not decided anywhere: question W1.

**2. major: `roles` (0057.04) gets a reviewer reason for a card about five roles.** workflow-loop.003.md:24-32 defines Person, Lead, Builder, Reviewer and Compute. "its maker is the easiest one to convince" (Axioms.md:29) explains why the reviewer must be another view, and nothing else. On its own the fragment also has no subject on the card ("its" points at nothing). The spec section's own chain is `axioms: 1.3` (workflow-loop.003.md:22), not 9. WHY-GAPS.md row 53 knows it "Covers the reviewer role" and points to :32 "A lead is not authority (axiom 3)" for the lead, but the face shows neither the scope nor the second source. Same fix options as finding 1 (W1).

**3. minor: `kernel-and-branches` (0051.04) borrows from the user-levels table.** decisions.md:380 is in C5.2 (user levels): level `00`, "internal authorised admin", reaches the kernel; "The kernel is small and nearly untouchable, which is why it is `00`." Read plainly, "it" is the kernel, so the line does state why the kernel is desk `00`. The sentence names its own scope ("why it is `00`"), so it does not claim to explain 01-09 (branches), 10-98 (user desks) or 99. But those three rows are now unreported by the builder too. Accepted; mark the scope when W1 is decided.

**4. minor: `risk-and-governing-targets` (0057.04) explains the recording, not the floor or governing changes.** "Record the inputs and reason so a reviewer can reproduce the decision." (workflow-loop.003.md:150) is self-describing, so it does not pretend to explain why a floor exists or why governing changes need N7. WHY-GAPS.md row 55 says "why the floor exists is not written". Accepted; mark the scope when W1 is decided.

**5. minor: WHY-GAPS graded the same source line A for `packs` (#54) and B for `pack-header` (#58).** Both use workflow-loop.003.md:8, the page-level why. Grade B means "a fresh reviewer should accept or reject it before it is filled". As the fresh reviewer I accept it for `packs` (see the table); `pack-header` stays B and unfilled, which is fine.

**6. minor: `card-types` (0054.04) why "so no book can redefine it" has no "it" on the card.** The card says "Card types are defined in the kernel", so "it" should be "them". The words must be a substring of decisions.md:287, so the copy cannot change; the line is right, the English is slightly off. No action needed for a PASS.

**7. minor, report only: the "body fix first" reason for the two skipped cards is out of date on the face.** Both skipped cards, `finding` (#6) and `book-layout` (#19), sit on 0051.04. But the face text no longer says "reserved" for 0001-0099 or 0020-0049: 0051.04 `book-layout` (lines 224-240) already splits the range per R7/R17, and 0051.01:53 `finding` was fixed in kernel pass 6 (0051.06.01:59). The old "reserved" wording is only in the cited spec lines, decisions.md:55 and decisions.md:120 (Director source files; not ours to edit). So the real hold on `book-layout` is Q30 (which sections below 0100), not a body fix. `finding` has no body blocker left; its two proposed lines (decisions.md:128, Axioms.md:25) were not filled and not trialed here. WHY-GAPS.md "Two cards need a body fix" should be corrected by its owning lane.

**Info, not a finding:** the five fill cards in 0056/0057 that still carry the stock line "`7` - no person-facing explanation of this card is written in the spec" now also have a `why:`. That is not a contradiction: the `7` line is about the card's 04 explanation body, not its why line. It was already there before this commit.

## Questions [TRIAL-WHYS] (saved for the Director; not added to kernel/QUESTIONS.md, another lane owns it this round)

**W1. [TRIAL-WHYS] When a spec line explains only part of a card, how should the card show it?**
Four fills (#10, #18, #53, #55) explain one part of their card. The builder stops reporting a card once it has any why, so the unexplained part vanishes.
- Option A: keep `why: 4.7` until the whole card has a source; partial reasons stay in WHY-GAPS.md only.
- Option B: fill the why, and add a `7` line on the card naming the part that still has no reason (the builder could count it as a finding).
- Option C: split the card so each part carries its own why or `4.7`. `7`.

**W2. [TRIAL-WHYS] Can a why be borrowed from a sibling rule?**
#39 takes "so no book can redefine it" from page types (C1.4) for card types, because C8.9 says a card type is to a card what a page type is to a page. #18 takes the kernel's reason from the user-levels table (C5.2) for the desks table (A6.3).
- Option A: yes, when the spec itself ties the two rules together (as C8.9 does).
- Option B: only a line in the card's own section counts; anything else is grade B. `7`.
