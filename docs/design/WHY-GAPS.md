# Why gaps in the kernel (FOLLOWUPS, 2026-11-11)

DRAFT list. Nothing here edits a kernel face; the kernel lane owns `kernel/` and decides what to fill.

## What this is

`node kernel/build.mjs --check` at commit 1cd06de (books unchanged since 18b9cfa) reports 59 findings, all `04 KEY: why missing (4.7)`. Each one is a 04 card whose `why:` line is the bare chain `4.7` (axiom 7 marks a hole, axiom 4 says it is a why). The finding is printed against the 01 or 02 face that holds the card; the `why:` line itself is in the page's 04 face. All seven 04 faces are drafts (`kernel/00.00.00/00.00.00.005N.04.draft.md`), so filling a why touches no seated face. (0056.01 is seated, but its 04 face is a draft.)

How a why is filled, from `kernel/build.mjs` `checkWhy` (lines 335-346): the card's `source:` line gains `why: docs/spec/FILE:LINE`, and the card's `why:` text must appear on that one line (em-dash, section sign and curly quotes are normalized first). So each proposal below is one spec line plus the exact words to copy from it. Every quoted phrase was checked by script to be on the cited line at this commit.

## Grades

- **A**: the cited line states the reason for this rule (or for the named part of it). Ready for the kernel lane to fill, then a fresh-session trial (R2, R20).
- **B**: a real line supports it, but tying it to this card is a reading. A fresh reviewer should accept or reject it before it is filled. Axiom 4: "Never invent a reason so the work feels finished."
- **C**: no source found in docs/spec, DIRECTOR-RULINGS or the commits. It stays `4.7`; the hole is kept (axiom 7) and raised as a question for the Director.

Commit messages were searched (`git log --all -i --grep`) for the 13 C card keys and for `why missing` / `4.7`. The only hits are a81f1b4 and 71d11d0 (for `grammar`), code commits that give no reason. So every proposal points at a spec line.

## Totals

59 gaps: 22 A, 24 B, 13 C.

| Page | Gaps | A | B | C |
|---|---|---|---|---|
| 00.00.00.0051 (seqaddr) | 20 | 7 | 10 | 3 |
| 00.00.00.0052 (faces) | 13 | 5 | 4 | 4 |
| 00.00.00.0053 (tails) | 5 | 0 | 2 | 3 |
| 00.00.00.0054 (card types) | 2 | 1 | 1 | 0 |
| 00.00.00.0055 (brands) | 10 | 3 | 5 | 2 |
| 00.00.00.0056 (drafting) | 2 | 1 | 0 | 1 |
| 00.00.00.0057 (workflow) | 7 | 5 | 2 | 0 |

## Status: grade A filled (WHY-GAPS lane, 2026-11-11 CST)

15 of the 22 A gaps are filled; 7 are skipped. `--check` now reports 44 findings (was 59), 0 errors, 26 seats unchanged. Each fill adds `; why: docs/spec/FILE:LINE` to the card's `source:` line and replaces `why: 4.7` with the words in the table below; no other card text changed. Every phrase was rechecked against its line at 6d3a0e6 before the edit. These 04 faces are drafts and need a fresh-session trial (R2, R20) before any seat.

Filled (15): #8 `faces-carry-no-title`, #10 `which-pages-need-a-title` (pages 0001-0999 part only), #15 `many-targets`, #16 `back-links`, #18 `kernel-and-branches` (desk 00 part only) on 0051.04; #39 `card-types` on 0054.04; #41 `card-key-address`, #43 `brand-cards`, #46 `resolving-a-word` on 0055.04; #51 `new-face` on 0056.04; #53 `roles` (reviewer part), #54 `packs`, #55 `risk-and-governing-targets` (recording part), #57 `return-placement`, #59 `why-questions` on 0057.04.

Skipped (7):
- On a seated face: `00.00.00.0052.04` was seated after this list was made (blob e9ca59a1d708acfd57b9e5f7e6b758e41e4fde6f), so #21 `registry-face`, #26 `full-explanation`, #27 `hard-rules-and-findings`, #31 `links-face`, #33 `card-shape` stay `4.7`. Filling them means a new draft of 0052.04 (copy the seated face, add the five whys) and a fresh trial, or an un-seat; that is a choice for Prima or the Director, not this lane.
- ~~Body fix first~~ (out of date, corrected by WHY-FIX below): #19 `book-layout` and #6 `finding`. Both stay `4.7`.

Partial fills keep their note: the parts the table says are "not written" are still unexplained. (Since WHY-FIX they are also marked on the faces; see below.)

## Status: partial fills scoped (WHY-FIX lane, 2026-11-11 CST)

TRIAL-WHYS (`docs/trial/kernel-trial-whys.md`) failed 0051.04 and 0057.04: once a card had any `why:`, the builder stopped reporting the parts its cited line does not explain (findings 1 and 2, major; findings 3 and 4, minor). This lane fixed that conservatively. It does not decide Director question W1 (how part-reasons should work long-term).

How each of the four partial fills is now written, on the draft 04 faces only:
- The card that matches the 01 key goes back to `why: 4.7`, and loses its `; why:` cite, so `--check` reports it again. A `7` line on that card names the part with no written reason.
- The checked part-reason moves, word for word with the same cited line, to a second 04 card named "<card>: <part> Part". `checkWhy` still tests its words against the cited line. A "Scope:" line says what it covers and what it does not.

| # | Card (finding on) | Reported again for | Part-reason card, unchanged words and line |
|---|---|---|---|
| 10 | `which-pages-need-a-title` (0051.01) | why pages 1000 and up must have a title | `which-pages-need-a-title-pages-0001-0999-part`, decisions.md:132 |
| 18 | `kernel-and-branches` (0051.01) | why desks `01-09`, `10-98` and `99` are set as they are | `kernel-and-branches-desk-00-part`, decisions.md:380 |
| 53 | `roles` (0057.01) | the Person, Lead, Builder and Compute roles | `roles-reviewer-part`, Axioms.md:29 |
| 55 | `risk-and-governing-targets` (0057.01) | why the risk floor exists; why governing changes need N7 | `risk-and-governing-targets-recording-part`, workflow-loop.003.md:150 |

`--check` (builder at 299b308, in a scratch clone): 48 findings (was 44; the 4 above are back), 0 errors, 26 seats. The other 11 grade A fills are unchanged. Books rebuilt with the committed builder.

Left as is, noted:
- `roles`: the spec section's own chain is `axioms: 1.3` (workflow-loop.003.md:22), and the reviewer reason comes from axiom 9. No ruling decides this, so nothing was changed; it is noted on the card. workflow-loop.003.md:32 "A lead is not authority (axiom 3)." may explain the Lead; not filled, needs a trial.
- #18 borrows from the user-levels table (C5.2): question W2.
- Both faces still need a fresh-session trial (R2, R20) of this fix before anything else.

## Cards held before a why

- `counted-faces` (0052): its 01 source decisions.md:198 says "A counted face is never seated", but R22 (DIRECTOR-RULINGS.md:88) seats each page's face 05. Open as QUESTIONS Q41.
- `book-layout` (0051): no longer a body fix. The cards no longer call 0001-0099 "reserved"; they split the range per R7 and R17 (0051.04 says only 0001-0009 are reserved, for override pages). The real hold is QUESTIONS Q30 (the four sections below 0100). Its row 19 line also covers only 1000/1001, so a fill would be partial.
- `finding` (0051): no longer a body fix. 0051.01:53 was fixed in kernel pass 6 (0051.06.01:59) and nothing in its wording blocks a why. Not filled by WHY-FIX: row 6 proposes two lines for two parts (lookup order; elevate, never guess), and one `why:` can cite one line, so a fill would be partial. That waits on W1, or on a fill plus a part card as above, then a trial.
- The old "reserved" wording is still in the cited spec lines decisions.md:55 and decisions.md:120. Those are Director source files, not edited (TRIAL-WHYS finding 7).

## The list

Columns: page; the face the builder names; card key; the 01/02 source the card already cites; grade; proposed why source (`docs/spec/FILE:LINE` "words to copy"); note.

| # | Page | Finding on | Card | 01/02 source | Grade | Proposed why source | Note |
|---|---|---|---|---|---|---|---|
| 1 | 0051 | `00.00.00.0051.01.draft.md` | `full-address` | decisions.md:12 | B | `docs/spec/Axioms.md:23` "The address is the line written down, ranked so it is stable to store: each part comes from the one before it." | Axiom 6 explains why an address is a ranked line; it does not say why every address is always full. |
| 2 | 0051 | `00.00.00.0051.01.draft.md` | `container-address` | decisions.md:33 | B | `docs/spec/decisions.md:15` "Any address with a 4-digit group can be read by position alone" | Reading: with no 4-digit group there is no page anchor, so it is read from the desk. That step is inferred, not written. |
| 3 | 0051 | `00.00.00.0051.01.draft.md` | `counters` | decisions.md:36 | B | `docs/spec/decisions.md:36` "Counters are not an axis, so the reserved 01-09 range does not apply to them." | Gives a consequence of the rule, not why counters attach only to faces. |
| 4 | 0051 | `00.00.00.0051.01.draft.md` | `exact-widths` | decisions.md:39 | B | `docs/spec/decisions.md:15` "Any address with a 4-digit group can be read by position alone" | Reading by position needs exact widths; the link is inferred. |
| 5 | 0051 | `00.00.00.0051.01.draft.md` | `short-form` | decisions.md:51 | C | none found (stays `4.7`) | decisions.md:51 and seqAddr.md:95 say what models do (echo the full address), not why. Raise to the Director. |
| 6 | 0051 | `00.00.00.0051.01.draft.md` | `finding` | decisions.md:54-56 | A | `docs/spec/decisions.md:128` "so a kernel change reaches every book that has not overridden it"; `docs/spec/Axioms.md:25` "Never invent it; unknown stays unknown." | First line is the why of the lookup order; the second is the why of "elevate, never guess". Card text cites 0020-0049 as "reserved": R17 says they are working pages. |
| 7 | 0051 | `00.00.00.0051.01.draft.md` | `title-position` | decisions.md:69 | B | `docs/spec/seqAddr.md:71` "so any address containing it reads by position alone" | Position rule for the anchor; applying it to titles is a reading. |
| 8 | 0051 | `00.00.00.0051.01.draft.md` | `faces-carry-no-title` | decisions.md:72 | A | `docs/spec/decisions.md:72` ""Go to 2423.05.01 and run it" is unambiguous." |  |
| 9 | 0051 | `00.00.00.0051.01.draft.md` | `title-characters` | decisions.md:75 | B | `docs/spec/DIRECTOR-RULINGS.md:15` "We want a simple storage design for now." | R4 covers plain characters only; why no dots (the dot is the axis separator, seqAddr.md:14) is not written as a reason. |
| 10 | 0051 | `00.00.00.0051.01.draft.md` | `which-pages-need-a-title` | decisions.md:131-134 | A | `docs/spec/decisions.md:132` "their number is already their name" | Covers pages 0001-0999 only. Why pages 1000+ must have a title is not written (part stays 4.7). |
| 11 | 0051 | `00.00.00.0051.01.draft.md` | `door-page` | decisions.md:143-149 | B | `docs/spec/Design.md:80` "Every container is a book, so the kernel, a desk and a shelf are stored exactly like a book." | Why a container has a page at all; why it is page 0000 is R1 (a ruling, not a reason). |
| 12 | 0051 | `00.00.00.0051.01.draft.md` | `checked-labels` | decisions.md:152 | B | `docs/spec/Axioms.md:25` "Never invent it; unknown stays unknown." | Why a mismatch is elevated, not why titles are checked. |
| 13 | 0051 | `00.00.00.0051.01.draft.md` | `door-rule` | decisions.md:161-173 | B | `docs/spec/Axioms.md:15` "The same shape at every scale." | Axiom 2 (fractal) fits "one rule for every container axis"; the link is a reading. |
| 14 | 0051 | `00.00.00.0051.01.draft.md` | `pointer` | decisions.md:214-224 | B | `docs/spec/decisions.md:250` "This keeps A2.6 intact: fixed 100-page bands, every `xx00` a head, and sets linked by number." | Covers band continuations (PP99) only. |
| 15 | 0051 | `00.00.00.0051.01.draft.md` | `many-targets` | decisions.md:227 | A | `docs/spec/decisions.md:227` "One desk can have several child desks, and one book can continue in several places." |  |
| 16 | 0051 | `00.00.00.0051.01.draft.md` | `back-links` | decisions.md:230-232 | A | `docs/spec/Axioms.md:27` "A connection is lawful only when it is written: inherited through the address, linked both ways (a link and its back-link), or a named override." |  |
| 17 | 0051 | `00.00.00.0051.01.draft.md` | `namespace` | decisions.md:253, decisions.md:265 | C | none found (stays `4.7`) | decisions.md:253 and :265 state the rule only. Raise to the Director. |
| 18 | 0051 | `00.00.00.0051.01.draft.md` | `kernel-and-branches` | decisions.md:256-262 | A | `docs/spec/decisions.md:380` "The kernel is small and nearly untouchable, which is why it is `00`." | Covers desk 00 only; why 01-09 are branches and 10-98 user desks is not written. |
| 19 | 0051 | `00.00.00.0051.01.draft.md` | `book-layout` | decisions.md:115-125 | A | `docs/spec/decisions.md:125` "`1000` is the head of the first user band, which is why the first open page is `1001`." | Covers 1000/1001 only. The card calls 0001-0099 reserved; R17 (DIRECTOR-RULINGS.md:67-69) splits that range, so the body needs a fix before a why is added. |
| 20 | 0051 | `00.00.00.0051.02.draft.md` | `grammar` | seqAddr.md:264-284 | C | none found (stays `4.7`) | The grammar is the rule; no line says why this grammar. Raise to the Director. |
| 21 | 0052 | `00.00.00.0052.01.draft.md` | `registry-face` | decisions.md:176 | A | `docs/spec/DIRECTOR-RULINGS.md:40` "00 is a registry location on a page, because it's multi faceted." | Also decisions.md:176 "the page stamp is stored once" (what, not why). |
| 22 | 0052 | `00.00.00.0052.01.draft.md` | `face-ranges` | decisions.md:179-184 | C | none found (stays `4.7`) | decisions.md:179-184 give the table only. R9 forbids FF.00/FF.99 as face sentinels but gives no reason. Raise to the Director. |
| 23 | 0052 | `00.00.00.0052.01.draft.md` | `draft-faces` | decisions.md:277 | B | `docs/spec/drafting.md:7` "Every change starts from a copy of the real text and arrives one note at a time, so nothing is lost and every change can be traced." | R5 (DIRECTOR-RULINGS.md:19) is the authority that drafts count; drafting.md:7 is the reason drafts exist. Whether it is the why for "drafts count toward C1.1" is a reading. |
| 24 | 0052 | `00.00.00.0052.01.draft.md` | `retiring` | decisions.md:280 | C | none found (stays `4.7`) | decisions.md:280 says what the compute does, not why the page retires with its last face. Raise to the Director. |
| 25 | 0052 | `00.00.00.0052.01.draft.md` | `cards` | decisions.md:298-301 | C | none found (stays `4.7`) | decisions.md:298-301 state the card rules only. Raise to the Director. |
| 26 | 0052 | `00.00.00.0052.01.draft.md` | `full-explanation` | decisions.md:339-348 | A | `docs/spec/Axioms.md:19` "A law without its why is incomplete: its reasoning cannot be understood." |  |
| 27 | 0052 | `00.00.00.0052.01.draft.md` | `hard-rules-and-findings` | decisions.md:350-357 | A | `docs/spec/Axioms.md:19` "A law without its why is incomplete: its reasoning cannot be understood." | For the "disagree" row, decisions.md:357 already gives "neither governs (axiom 1)". |
| 28 | 0052 | `00.00.00.0052.01.draft.md` | `face-03` | decisions.md:404-405 | C | none found (stays `4.7`) | decisions.md:404-405 state where face 03 is allowed, not why. Raise to the Director. |
| 29 | 0052 | `00.00.00.0052.01.draft.md` | `counted-faces` | decisions.md:198-199 | B | `docs/spec/workflow-loop.003.md:160` "The counter keeps the same identity throughout." | CLASH: decisions.md:198 "A counted face is never seated" vs R22 (DIRECTOR-RULINGS.md:88) seating each face 05; QUESTIONS Q41. Fix the body first. |
| 30 | 0052 | `00.00.00.0052.01.draft.md` | `packed-face` | decisions.md:575 | B | `docs/spec/decisions.md:575` "A model that needs more requests the why from the compute by card key." | seqAddr.md:180 "Routing should reduce reading without replacing the source." fits better but it is the example why of a sample `Job` card, not a rule line. |
| 31 | 0052 | `00.00.00.0052.01.draft.md` | `links-face` | decisions.md:368 | A | `docs/spec/Axioms.md:27` "Nothing stands alone: each piece connects to what it came from and what depends on it" |  |
| 32 | 0052 | `00.00.00.0052.02.draft.md` | `stamp` | decisions.md:176, decisions.md:285, seqAddr.md:172, format.md:74 | B | `docs/spec/Axioms.md:15` "Inherit what is agreed; write only the difference." | decisions.md:176 "the page stamp is stored once" is the what; R12 (DIRECTOR-RULINGS.md:53) is the authority for where. Why it is stored once is a reading of axiom 2. |
| 33 | 0052 | `00.00.00.0052.02.draft.md` | `card-shape` | decisions.md:508-509, seqAddr.md:168-172 | A | `docs/spec/decisions.md:509` "Each face has a default type, so most cards need no `type:` line." | Covers the type default only. |
| 34 | 0053 | `00.00.00.0053.01.draft.md` | `where-tails-attach` | decisions.md:81-88 | C | none found (stays `4.7`) | decisions.md:81-88 state the rule; :88 "Tail words are reserved" has no reason. Raise to the Director. |
| 35 | 0053 | `00.00.00.0053.01.draft.md` | `allowed-tails` | decisions.md:90-97 | C | none found (stays `4.7`) | decisions.md:90-97 list the tails only. Raise to the Director. |
| 36 | 0053 | `00.00.00.0053.01.draft.md` | `workflow-state` | decisions.md:99 | B | `docs/spec/workflow-loop.003.md:160` "Its current tail determines its column." | Why workflow state is on counters (the board) is a reading of the loop. |
| 37 | 0053 | `00.00.00.0053.01.draft.md` | `tail-meanings` | seqAddr.md:131-138 | C | none found (stays `4.7`) | seqAddr.md:131-138 define meanings only. Raise to the Director. |
| 38 | 0053 | `00.00.00.0053.02.draft.md` | `tail-moves` | workflow-loop.003.md:162-164, format.md:124 | B | `docs/spec/format.md:42` "proposals are approved one at a time, so the first claim on a `pack` wins and the second is rejected." | Covers the claim step only. |
| 39 | 0054 | `00.00.00.0054.01.draft.md` | `card-types` | decisions.md:506-510 | A | `docs/spec/decisions.md:287` "so no book can redefine it" | Why types live in the kernel. decisions.md:509 gives why each face has a default. |
| 40 | 0054 | `00.00.00.0054.02.draft.md` | `card-type-table` | decisions.md:512-522 | B | `docs/spec/decisions.md:509` "Each face has a default type, so most cards need no `type:` line." | Why the table has a default column; why these exact types is not written. |
| 41 | 0055 | `00.00.00.0055.01.draft.md` | `card-key-address` | decisions.md:421 | A | `docs/spec/decisions.md:421` "Tail words stay reserved, so they never collide with card keys." |  |
| 42 | 0055 | `00.00.00.0055.01.draft.md` | `dictionary-is-an-index` | decisions.md:424-432 | B | `docs/spec/Axioms.md:23` "The past is not rewritten: rewriting a step breaks the line, and the way back is lost" | Fits "brand numbers are never reused or renumbered" (decisions.md:432); why the dictionary is only an index is not written. |
| 43 | 0055 | `00.00.00.0055.01.draft.md` | `brand-cards` | decisions.md:435-440 | A | `docs/spec/decisions.md:418` "A user's explained meaning of a word is recorded as a brand, so models never fall back on an average meaning." |  |
| 44 | 0055 | `00.00.00.0055.01.draft.md` | `local-first` | decisions.md:443 | B | `docs/spec/Axioms.md:15` "Inherit what is agreed; write only the difference." | Fits the inherited base dictionary; why each book keeps its own is a reading. |
| 45 | 0055 | `00.00.00.0055.01.draft.md` | `meters` | decisions.md:484-493 | C | none found (stays `4.7`) | decisions.md:484 says meters are compute-only and exempt from drafting, not why. Raise to the Director. |
| 46 | 0055 | `00.00.00.0055.01.draft.md` | `resolving-a-word` | decisions.md:496-503 | A | `docs/spec/brands.md:7` "When a user explains their meaning of a word, it is recorded, so models look it up instead of guessing." |  |
| 47 | 0055 | `00.00.00.0055.01.draft.md` | `keywords-are-brands` | decisions.md:360 | B | `docs/spec/Axioms.md:15` "do not reinvent what already exists: both create drift." | Fits "if a matching meaning already exists, it is reused" (decisions.md:360). |
| 48 | 0055 | `00.00.00.0055.02.draft.md` | `dictionary-layout` | decisions.md:446-481 | B | `docs/spec/decisions.md:446` "One layout, the same from the kernel out." | States the choice; the 2.1% split is how, not why. |
| 49 | 0055 | `00.00.00.0055.02.draft.md` | `index-card` | brands.md:23-30 | C | none found (stays `4.7`) | brands.md:23-30 is an example only. Raise to the Director. |
| 50 | 0055 | `00.00.00.0055.02.draft.md` | `brand-card-form` | brands.md:34-41 | B | `docs/spec/brands.md:7` "When a user explains their meaning of a word, it is recorded, so models look it up instead of guessing." | Why brand cards exist; why this field form is not written. |
| 51 | 0056 | `00.00.00.0056.01.md` | `new-face` | drafting.md:20 | A | `docs/spec/drafting.md:7` "A rewrite from memory silently drops what the model did not remember." | R8 (DIRECTOR-RULINGS.md:34) says the same: "so we don't replace an existing work from memory". |
| 52 | 0056 | `00.00.00.0056.01.md` | `exceptions` | drafting.md:39-41 | C | none found (stays `4.7`) | drafting.md:39-41 list the exceptions (derived content, meters) without a reason. Raise to the Director. |
| 53 | 0057 | `00.00.00.0057.01.draft.md` | `roles` | workflow-loop.003.md:24-32 | A | `docs/spec/Axioms.md:29` "its maker is the easiest one to convince" | Covers the reviewer role. workflow-loop.003.md:32 "A lead is not authority (axiom 3)." covers the lead. |
| 54 | 0057 | `00.00.00.0057.01.draft.md` | `packs` | workflow-loop.003.md:99 | A | `docs/spec/workflow-loop.003.md:8` "so a model can run passes without history and a person can check every step." | This is the page-level why of workflow-loop.003 applied to packs. |
| 55 | 0057 | `00.00.00.0057.01.draft.md` | `risk-and-governing-targets` | workflow-loop.003.md:150-154 | A | `docs/spec/workflow-loop.003.md:150` "Record the inputs and reason so a reviewer can reproduce the decision." | Covers recording; why the floor exists is not written. |
| 56 | 0057 | `00.00.00.0057.01.draft.md` | `the-loop` | workflow-loop.003.md:160-177 | B | `docs/spec/workflow-loop.003.md:160` "The counter keeps the same identity throughout." |  |
| 57 | 0057 | `00.00.00.0057.01.draft.md` | `return-placement` | workflow-loop.003.md:181-183 | A | `docs/spec/workflow-loop.003.md:183` "Review uses those findings to decide the outcome." | Why a failed return is still recorded. |
| 58 | 0057 | `00.00.00.0057.02.draft.md` | `pack-header` | workflow-loop.003.md:103-116 | B | `docs/spec/workflow-loop.003.md:8` "so a model can run passes without history and a person can check every step." | Page-level why; the header fields carry their own axiom column. |
| 59 | 0057 | `00.00.00.0057.02.draft.md` | `why-questions` | workflow-loop.003.md:273-278 | A | `docs/spec/workflow-loop.003.md:258` "Models left alone loop on one detail, so there are hard move-on points." |  |

## C list for the Director (13, kept as `4.7`)

0051: `short-form`, `namespace`, `grammar`. 0052: `face-ranges`, `retiring`, `cards`, `face-03`. 0053: `where-tails-attach`, `allowed-tails`, `tail-meanings`. 0055: `meters`, `index-card`. 0056: `exceptions`.

One question covers them: "These 13 kernel rules say what to do but not why. Do you want to give the why for each, or leave them marked missing for now?" Saved here, not asked (R22: save questions).

## How this list was made

1. `node kernel/build.mjs --check` (read-only; exit 0, 59 findings, 0 errors).
2. Each 04 card with `why: 4.7` was read from `kernel/00.00.00/*.04.draft.md` with its `source:` line.
3. The cited decisions.md / seqAddr.md / brands.md / drafting.md / workflow-loop.003.md lines, their sections, Axioms.md and DIRECTOR-RULINGS.md were read for a stated reason.
4. Each proposed phrase was checked to be a substring of its cited line, the same test `checkWhy` uses.
