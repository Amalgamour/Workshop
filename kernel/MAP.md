# Kernel map

What is in `kernel/`, at which page number, and why. Paths in sources are under `docs/spec/`. The card rows below come from the seed script. Text is copied from the spec, never written from memory. The only change to copied text is R1's word "door" (see Door wording).

## Status: everything is draft, door faces included

Every face, including every door face 00, is written `FF.draft`. None is seated.
- `drafting.md:20`: "A brand-new face has nothing to copy. It starts as an empty draft and still goes through notes and merges."
- `seqAddr.md:201`: "`FF.draft` is its unseated draft." This applies to face 00 too (grammar `seqAddr.md:283`). Trial finding 1 is fixed.
- The stamp also says `state: draft`. Whether state lives in the stamp, the file tail, or both is QUESTIONS Q8.

### Seated under R2: none
R2 (`DIRECTOR-RULINGS.md:7-9`) lets a face be seated during the build stage once it has passed a hostile trial, recorded as `approved-by: build-stage (R2)`. I checked every face against TRIAL-K (`docs/trial/kernel-trial.md`) and QUESTIONS.md. No face qualifies yet:
- Door faces 00: the stamp's `state` and `type` values are open (Q8, hole 4). Door pages 0000 also have Q6 open.
- 0050 (all faces): the page number is open (Q1, `decisions.md:598`).
- 0051.01/02, 0052.01/02, 0054.02, 0055.01: their cards are named in open conflicts and questions (Q5, Q11-Q14, K05, K11).
- 0053, 0057: copied from `workflow-loop.003.md`, which says "state: draft — Director review required; not live" (`:3`).
- 0054.01: C1.4 has an open question (`decisions.md:292`).
- 0056.01: 2 of its 3 cards (`new-face`, `exceptions`) still have a missing why (`4.7`) and a hole body on 04, which is an unresolved finding.
- 0056.02: the mechanism is proposed (`decisions.md:320`).
- Every 04 face: holds `why: 4.7` or `7` hole bodies, except 0050.04 (page number open, Q1).
- Q10 (seated face under a draft door) is open as well.

The builder rejects a seated (no-tail) face whose cards lack `approved-by: ... (R2)`, so a later seat has to be recorded.

## Door wording (R1)
`DIRECTOR-RULINGS.md:5`: "Older spec wording that calls it owner, identity, or board refers to this same location; use the word 'door'."
- Copied text was changed phrase by phrase. Each change is recorded as a merge line in that page's `06.01` note (drafting.md: notes, then merges).
- Only the zero-sequence sense was changed. Other senses stay as written: "part of identity" (a title), "reviewer identity", "Counter identity", "original identities", "owner, claim ID", `owner: kernel-only`, and "like a kanban board" (a comparison).
- Card headings that were my own choice were renamed: Identity Page -> Door Page, Owner Rule -> Door Rule, Face Identity -> Door Face.
- R1 renames the location only. Whether the counter list stays the door's job is Q5.

## Page numbers chosen

`seqAddr.md:223`: "`0050-0099` | structural pages, mostly in the kernel or templates". `decisions.md:287`: "Each type is a card on a kernel structural page (0050-0099)". The order inside that range is not in the spec (`7`). Chosen: the order the brief lists the pages, starting at 0050.

| Page | Title | Faces | Source of the number |
|---|---|---|---|
| `0000` | kernel | 00, 04 | `decisions.md:258`: "`00.00.00` is its own book, `00.00.00.0000` its identity page." (door page under R1) |
| `0050` | axioms | 00, 01, 02, 03, 04, 06.01 | `7`, Q1: `decisions.md:598` |
| `0051` | seqaddr | 00, 01, 02, 04, 06.01 | `7` order |
| `0052` | faces | 00, 01, 02, 04, 06.01 | `7` order |
| `0053` | tails | 00, 01, 02, 04, 06.01 | `7` order |
| `0054` | types | 00, 01, 02, 04, 06.01 | `decisions.md:287`, `:510` |
| `0055` | brands | 00, 01, 02, 04, 06.01 | `7` order |
| `0056` | drafting | 00, 01, 02, 04, 06.01 | `7` order |
| `0057` | workflow-loop | 00, 01, 02, 04, 06.01 | `7` order. Templates are kernel card types (`workflow-loop.003.md:232`). |

Not written, on purpose:
- `0012` dictionary: no base words are listed (`decisions.md:443`), so it stays `7`.
- `0001-0049` and band heads: no kernel content is named for them (`7`).
- Face 08 (C4 open) and `9999`/`PP99` ("Missing is a valid state", `decisions.md:205`).
- 03 menu entries, derived (`decisions.md:516`; `drafting.md:40` "calculated and never drafted"). The derived Menu card was removed (trial 16).

## Face choices
- **01 cards** copy the decision text, or `seqAddr.md` / `workflow-loop.003.md` where no decision text exists. Their lineage is kept in the book: each matching 04 card's `source:` names the 01 lines first (trial 9).
- **04 cards** copy person-facing text from `seqAddr.md`, `brands.md`, `drafting.md`, `kernel-design.md` or the F.1 table.
  - `source:` gives `[FF / Card] 01-lines; 04 text: lines; why: docs/spec/FILE:LINE`.
  - The builder checks that each `why:` sits on its cited line (trial 7, 21).
  - `why: 4.7` means no reason is written in the spec. I removed three borrowed whys: `which-pages-need-a-title`, `finding` and `risk-and-governing-targets`.
  - Axioms 04 whys now use their recorded why, `decisions.md:548` (trial 19).
  - Where no person-facing text exists, the body is a `7` hole: a required absence, reported. This includes `roles` and `bound-bands`, which no longer borrow `.002` notes (trial 17).
- **Card keys** follow `seqAddr.md:280` and are never a tail word. `## Review` became `## Review (filled)`, the `.003` section heading (`workflow-loop.003.md:195`), giving key `review-filled` (trial 2).
- **Stamps:** only face 00 carries one (`decisions.md:176`).
- **Notes:** 06 is counter `06.01`, this session. Note fields are open (C7).

## Workflow-loop page source
Page 0057 copies `workflow-loop.003.md`. `.002` is lineage only. The differences are in CONFLICTS section B. The 04 text for `return-placement` is `decisions.md:612`; the first build cited :611 by mistake, which the fix pass caught.

## Samples (`kernel/samples/`)
Test fixtures, not kernel content, and all draft.
- Desk `10` "personal", shelf `10.11` "me", book `10.11.21` "about-me". Their door pages are face 00 only (K10, Q6).
- **Lookup today:** every kernel face is a draft, and a draft is "not active" (`seqAddr.md:133`). So every lookup from the sample comes back missing. The builder prints each one as a `lookup: missing` finding. Whether drafts should be found is Q2 (trial 5).
- **Override:** `10.11.21.0056.04` holds a local `Never From Memory` 04 card, in the Director's words from Prima chat t42u ("Copy it then update don't create from memory."). Those words are not in docs/spec, and the card says so (trial 18). If lookup goes face by face, this hides the kernel's other 04 cards and breaks C3.2. The builder prints that as a finding (trial 6). Per face or per card, and how a named override is written, is Q3.
- **Bob test:** page `10.11.21.1001` holds brand cards `bob` and `cats`, and dictionary counters `03.14` / `03.16` (`decisions.md:458-460`).
  - Session 2 ("what is my name") has **no route** to `bob`, so it stays `7` (Q7). The invented route was removed (trial 4).
  - There is no "fact" card type, and no meters (they are compute-only).
- The shelf and desk steps of the lookup have no sample faces. Adding some would need content the spec doesn't give, and with drafts not found they would show nothing (trial 20, left).

## Holes left as `7`
1. Axioms page number (Q1).
2. Page order in 0050-0099.
3. Stamp state (Q8).
4. Page `type` values for kernel pages (C1.4 lists types without their meanings).
5. Base dictionary.
6. 03 menus (derived).
7. `why: 4.7` cards and hole bodies (counted in the builder's findings).
8. Note fields (C7), face 08 (C4), lineage on 00/08 (E6).
9. Door page content face (Q6).
10. "Fact" card type.
11. Draft lookup (Q2).
12. Override form (Q3).
13. Draft entry shape in books (Q4).
14. Door `FF.00` written or derived (Q5).
15. Seed timestamp, fixed for determinism.
16. Band head 1000 before 1001.
17. Bob session 2 (Q7).
18. `7.8`: the `axioms/` folder, `workflow-loop.003-notes.md`, decisions F02-F10.

## Build
`node kernel/build.mjs` writes `books/00.00.00.book`, `10.00.00.book`, `10.11.00.book` and `10.11.21.book`. `--check` fails if `books/` differs. The build is deterministic: sorted input, fixed time and author.
- **Hard checks:** name grammar, tails, door face, content face, C3.2, card types, card keys, `why:` on its cited line, and `approved-by` on any seated face.
- **Findings:** missing whys, doors not written, door pages without a content face, lookup results, and C3.2 across the lookup.

## Card sources


### `00.00.00.0000` kernel

| Face | Card | Copied from | Note |
|---|---|---|---|
| 04 | `kernel` | kernel-design.md:9, kernel-design.md:11, kernel-design.md:166 |  |

### `00.00.00.0050` axioms

| Face | Card | Copied from | Note |
|---|---|---|---|
| 01 | `authority` | decisions.md:538 | body = Holds column of decisions.md E1 row |
| 04 | `authority` | Axioms.md:13 |  |
| 01 | `fractal` | decisions.md:539 | body = Holds column of decisions.md E1 row |
| 04 | `fractal` | Axioms.md:15 |  |
| 01 | `leads` | decisions.md:540 | body = Holds column of decisions.md E1 row |
| 04 | `leads` | Axioms.md:17 |  |
| 01 | `why` | decisions.md:541 | body = Holds column of decisions.md E1 row |
| 04 | `why` | Axioms.md:19 |  |
| 01 | `frame` | decisions.md:542 | body = Holds column of decisions.md E1 row |
| 04 | `frame` | Axioms.md:21 |  |
| 01 | `lineage` | decisions.md:543 | body = Holds column of decisions.md E1 row |
| 04 | `lineage` | Axioms.md:23 |  |
| 01 | `missing` | decisions.md:544 | body = Holds column of decisions.md E1 row |
| 04 | `missing` | Axioms.md:25 |  |
| 01 | `connection` | decisions.md:545 | body = Holds column of decisions.md E1 row |
| 04 | `connection` | Axioms.md:27 |  |
| 01 | `trial` | decisions.md:546 | body = Holds column of decisions.md E1 row |
| 04 | `trial` | Axioms.md:29 |  |
| 01 | `cite` | decisions.md:552-554 |  |
| 02 | `cite` | decisions.md:560-564 |  |
| 04 | `cite` | Axioms.md:5, Axioms.md:7, decisions.md:566 |  |
| 03 | `cold-set` | Axioms.md:9 | 03 default type is menu; whether an operation card needs another type is 7 |
| 06.01 | `seed-session` | see body | session note |

### `00.00.00.0051` seqaddr

| Face | Card | Copied from | Note |
|---|---|---|---|
| 01 | `full-address` | decisions.md:12 |  |
| 04 | `full-address` | seqAddr.md:14-24 | why missing: 4.7 |
| 01 | `page-anchor` | decisions.md:15-30 |  |
| 04 | `page-anchor` | seqAddr.md:71-86 |  |
| 01 | `container-address` | decisions.md:33 |  |
| 04 | `container-address` | seqAddr.md:89 | why missing: 4.7 |
| 01 | `counters` | decisions.md:36 |  |
| 04 | `counters` | seqAddr.md:24 | why missing: 4.7 |
| 01 | `exact-widths` | decisions.md:39 |  |
| 04 | `exact-widths` | seqAddr.md:14 | why missing: 4.7 |
| 01 | `active-page` | decisions.md:42-48 |  |
| 04 | `active-page` | seqAddr.md:92 |  |
| 01 | `short-form` | decisions.md:51 |  |
| 04 | `short-form` | seqAddr.md:95 | why missing: 4.7 |
| 01 | `finding` | decisions.md:54-56 |  |
| 04 | `finding` | seqAddr.md:98-104 | why missing: 4.7 |
| 01 | `live-inheritance` | decisions.md:128 |  |
| 04 | `live-inheritance` | seqAddr.md:104 |  |
| 01 | `title-position` | decisions.md:69 |  |
| 04 | `title-position` | seqAddr.md:110-111 | why missing: 4.7 |
| 01 | `faces-carry-no-title` | decisions.md:72 |  |
| 04 | `faces-carry-no-title` | seqAddr.md:110 | why missing: 4.7 |
| 01 | `title-characters` | decisions.md:75 |  |
| 04 | `title-characters` | seqAddr.md:112 | why missing: 4.7 |
| 01 | `titles-are-labels` | decisions.md:78 |  |
| 04 | `titles-are-labels` | seqAddr.md:114 |  |
| 01 | `which-pages-need-a-title` | decisions.md:131-134 |  |
| 04 | `which-pages-need-a-title` | seqAddr.md:115-116 | why missing: 4.7 |
| 01 | `door-page` | decisions.md:143-149 |  |
| 04 | `door-page` | seqAddr.md:56-62 | why missing: 4.7 |
| 01 | `checked-labels` | decisions.md:152 |  |
| 04 | `checked-labels` | seqAddr.md:116 | why missing: 4.7 |
| 01 | `door-rule` | decisions.md:161-173 |  |
| 04 | `door-rule` | seqAddr.md:44-53 | why missing: 4.7 |
| 01 | `missing-is-valid` | decisions.md:205 |  |
| 04 | `missing-is-valid` | seqAddr.md:254 |  |
| 01 | `pointer` | decisions.md:214-224 |  |
| 04 | `pointer` | seqAddr.md:249 | why missing: 4.7 |
| 01 | `many-targets` | decisions.md:227 |  |
| 04 | `many-targets` | seqAddr.md:250 | why missing: 4.7 |
| 01 | `back-links` | decisions.md:230-232 |  |
| 04 | `back-links` | seqAddr.md:251, seqAddr.md:253 | why missing: 4.7 |
| 01 | `derived-ancestors` | decisions.md:237 |  |
| 04 | `derived-ancestors` | seqAddr.md:252 |  |
| 01 | `overflow` | decisions.md:246-250 |  |
| 04 | `overflow` | seqAddr.md:256-258 |  |
| 01 | `namespace` | decisions.md:253, decisions.md:265 |  |
| 04 | `namespace` | seqAddr.md:41 | why missing: 4.7 |
| 01 | `kernel-and-branches` | decisions.md:256-262 |  |
| 04 | `kernel-and-branches` | seqAddr.md:33-39 | why missing: 4.7 |
| 01 | `bands` | decisions.md:102-112 |  |
| 04 | `bands` | seqAddr.md:232-243 |  |
| 01 | `book-layout` | decisions.md:115-125 |  |
| 04 | `book-layout` | seqAddr.md:215-228 | why missing: 4.7 |
| 02 | `grammar` | seqAddr.md:264-284 |  |
| 04 | `grammar` | seqAddr.md:286-293 | why missing: 4.7 |
| 06.01 | `seed-session` | see body | session note |

### `00.00.00.0052` faces

| Face | Card | Copied from | Note |
|---|---|---|---|
| 01 | `door-face` | decisions.md:176 |  |
| 04 | `door-face` | seqAddr.md:64 | why missing: 4.7 |
| 01 | `face-ranges` | decisions.md:179-184 |  |
| 04 | `face-ranges` |  | why missing: 4.7 |
| 01 | `face-jobs` | seqAddr.md:147-160 |  |
| 04 | `face-jobs` | kernel-design.md:94, kernel-design.md:96-107 |  |
| 01 | `which-faces` | decisions.md:274 |  |
| 04 | `which-faces` | seqAddr.md:163 |  |
| 01 | `draft-faces` | decisions.md:277 |  |
| 04 | `draft-faces` | seqAddr.md:164 | why missing: 4.7 |
| 01 | `retiring` | decisions.md:280 |  |
| 04 | `retiring` | seqAddr.md:165 | why missing: 4.7 |
| 01 | `cards` | decisions.md:298-301 |  |
| 04 | `cards` | seqAddr.md:168-170 | why missing: 4.7 |
| 01 | `full-explanation` | decisions.md:339-348 |  |
| 04 | `full-explanation` | seqAddr.md:175-186 | why missing: 4.7 |
| 01 | `hard-rules-and-findings` | decisions.md:350-357 |  |
| 04 | `hard-rules-and-findings` | seqAddr.md:184-185 | why missing: 4.7 |
| 01 | `face-03` | decisions.md:404-405 |  |
| 04 | `face-03` | seqAddr.md:189 | why missing: 4.7 |
| 01 | `counted-faces` | decisions.md:187-199 |  |
| 04 | `counted-faces` | seqAddr.md:197-209 | why missing: 4.7 |
| 01 | `counter-continuation` | decisions.md:202 |  |
| 04 | `counter-continuation` | seqAddr.md:257 | why missing: 4.7 |
| 01 | `packed-face` | decisions.md:575 |  |
| 04 | `packed-face` |  | why missing: 4.7 |
| 01 | `lineage-on-the-page` | decisions.md:579-582 |  |
| 04 | `lineage-on-the-page` | seqAddr.md:157 |  |
| 01 | `links-face` | decisions.md:368 |  |
| 04 | `links-face` | seqAddr.md:157 | why missing: 4.7 |
| 02 | `stamp` | decisions.md:176, decisions.md:285, seqAddr.md:172, format.md:74 |  |
| 04 | `stamp` | kernel-design.md:96 | why missing: 4.7 |
| 02 | `card-shape` | decisions.md:508-509, seqAddr.md:168-172 |  |
| 04 | `card-shape` |  | why missing: 4.7 |
| 06.01 | `seed-session` | see body | session note |

### `00.00.00.0053` tails

| Face | Card | Copied from | Note |
|---|---|---|---|
| 01 | `where-tails-attach` | decisions.md:81-88 |  |
| 04 | `where-tails-attach` | seqAddr.md:122 | why missing: 4.7 |
| 01 | `allowed-tails` | decisions.md:90-97 |  |
| 04 | `allowed-tails` | seqAddr.md:124-129 | why missing: 4.7 |
| 01 | `workflow-state` | decisions.md:99 |  |
| 04 | `workflow-state` | seqAddr.md:140 | why missing: 4.7 |
| 01 | `tail-meanings` | seqAddr.md:131-138 |  |
| 04 | `tail-meanings` |  | why missing: 4.7 |
| 01 | `closed-is-bare` | workflow-loop.003.md:166 |  |
| 04 | `closed-is-bare` |  |  |
| 02 | `tail-moves` | workflow-loop.003.md:162-164, format.md:124 |  |
| 04 | `tail-moves` |  | why missing: 4.7 |
| 06.01 | `seed-session` | see body | session note |

### `00.00.00.0054` types

| Face | Card | Copied from | Note |
|---|---|---|---|
| 01 | `page-types` | decisions.md:283-290 |  |
| 04 | `page-types` | seqAddr.md:192-194 |  |
| 01 | `card-types` | decisions.md:506-510 |  |
| 04 | `card-types` | seqAddr.md:171 | why missing: 4.7 |
| 02 | `card-type-table` | decisions.md:512-522 |  |
| 04 | `card-type-table` |  | why missing: 4.7 |
| 06.01 | `seed-session` | see body | session note |

### `00.00.00.0055` brands

| Face | Card | Copied from | Note |
|---|---|---|---|
| 01 | `brands` | decisions.md:418 |  |
| 04 | `brands` | brands.md:7 |  |
| 01 | `card-key-address` | decisions.md:421 |  |
| 04 | `card-key-address` | brands.md:47 | why missing: 4.7 |
| 01 | `dictionary-is-an-index` | decisions.md:424-432 |  |
| 04 | `dictionary-is-an-index` | brands.md:11-15 | why missing: 4.7 |
| 01 | `brand-cards` | decisions.md:435-440 |  |
| 04 | `brand-cards` | brands.md:32-43 | why missing: 4.7 |
| 01 | `local-first` | decisions.md:443 |  |
| 04 | `local-first` | brands.md:78 | why missing: 4.7 |
| 01 | `meters` | decisions.md:484-493 |  |
| 04 | `meters` | brands.md:55-61 | why missing: 4.7 |
| 01 | `resolving-a-word` | decisions.md:496-503 |  |
| 04 | `resolving-a-word` | brands.md:65-70 | why missing: 4.7 |
| 01 | `keywords-are-brands` | decisions.md:360 |  |
| 04 | `keywords-are-brands` |  | why missing: 4.7 |
| 02 | `dictionary-layout` | decisions.md:446-481 |  |
| 04 | `dictionary-layout` | brands.md:82-92 | why missing: 4.7 |
| 02 | `index-card` | brands.md:23-30 |  |
| 04 | `index-card` |  | why missing: 4.7 |
| 02 | `brand-card-form` | brands.md:34-41 |  |
| 04 | `brand-card-form` |  | why missing: 4.7 |
| 06.01 | `seed-session` | see body | session note |

### `00.00.00.0056` drafting

| Face | Card | Copied from | Note |
|---|---|---|---|
| 01 | `never-from-memory` | decisions.md:309-318 |  |
| 04 | `never-from-memory` | drafting.md:7 |  |
| 01 | `new-face` | drafting.md:20 |  |
| 04 | `new-face` |  | why missing: 4.7 |
| 01 | `exceptions` | drafting.md:39-41 |  |
| 04 | `exceptions` |  | why missing: 4.7 |
| 02 | `drafting-ops` | decisions.md:320-330 |  |
| 04 | `drafting-ops` | drafting.md:24-35 |  |
| 06.01 | `seed-session` | see body | session note |

### `00.00.00.0057` workflow-loop

| Face | Card | Copied from | Note |
|---|---|---|---|
| 01 | `roles` | workflow-loop.003.md:24-32 |  |
| 04 | `roles` |  | why missing: 4.7 |
| 01 | `band-design` | workflow-loop.003.md:38-53 |  |
| 04 | `band-design` | decisions.md:644-645 |  |
| 01 | `bound-bands` | workflow-loop.003.md:59-64 |  |
| 04 | `bound-bands` |  |  |
| 01 | `code-in-the-repo` | workflow-loop.003.md:70-81 |  |
| 04 | `code-in-the-repo` |  |  |
| 01 | `n4-approval` | workflow-loop.003.md:87-93 |  |
| 04 | `n4-approval` |  |  |
| 01 | `packs` | workflow-loop.003.md:99 |  |
| 04 | `packs` |  | why missing: 4.7 |
| 01 | `risk-and-governing-targets` | workflow-loop.003.md:150-154 |  |
| 04 | `risk-and-governing-targets` |  | why missing: 4.7 |
| 01 | `the-loop` | workflow-loop.003.md:160-177 |  |
| 04 | `the-loop` | workflow-loop.002-notes.md:37-38 | why missing: 4.7 |
| 01 | `return-placement` | workflow-loop.003.md:181-183 |  |
| 04 | `return-placement` | decisions.md:612 | why missing: 4.7 |
| 01 | `review-filled` | workflow-loop.003.md:199-202 |  |
| 04 | `review-filled` |  |  |
| 01 | `open-while-gone` | workflow-loop.003.md:206-208 |  |
| 04 | `open-while-gone` |  |  |
| 01 | `lead-pass` | workflow-loop.003.md:214-220 |  |
| 04 | `lead-pass` |  |  |
| 01 | `promotion-manifest` | workflow-loop.003.md:224-226 |  |
| 04 | `promotion-manifest` |  |  |
| 01 | `gravity` | workflow-loop.003.md:258-269, workflow-loop.003.md:280 |  |
| 04 | `gravity` |  |  |
| 02 | `pack-header` | workflow-loop.003.md:103-116 |  |
| 04 | `pack-header` |  | why missing: 4.7 |
| 02 | `work-card` | workflow-loop.003.md:120-146 |  |
| 04 | `work-card` |  |  |
| 02 | `return-shape` | workflow-loop.003.md:189-193 |  |
| 04 | `return-shape` |  |  |
| 02 | `pack-lint` | workflow-loop.003.md:232-252 |  |
| 04 | `pack-lint` |  |  |
| 02 | `why-questions` | workflow-loop.003.md:273-278 |  |
| 04 | `why-questions` |  | why missing: 4.7 |
| 06.01 | `seed-session` | see body | session note |
