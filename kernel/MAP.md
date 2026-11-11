# Kernel map

What is seated in `kernel/`, at which page number, and why. Paths in sources are under `docs/spec/`. Generated card rows come from the seed script; the text is copied from the spec, never written from memory.

## Status: everything is draft

Every content face is written `FF.draft`. None is seated.
- Why: `drafting.md:20` — "A brand-new face has nothing to copy. It starts as an empty draft and still goes through notes and merges."
- Why: `Axioms.md:29` — "Before anything is promoted, it faces a hostile pass from another view". No face here has had that pass, and the Director has approved none of them.
- Why: `seqAddr.md:133` — "`draft` | being written; not active".
- Face 00 (the stamp) is written bare, with `state: draft` inside it. `7`: the spec does not say whether a stamp itself takes the `draft` tail, or what values `state:` holds. Chosen: the page's state lives in its stamp (`decisions.md:176` "`PPPP.00` holds the page's stamp: address, title, state"), so the stamp file has no tail.
- Promotion of any face needs the Director and a trial (axiom 9, E7). The builder writes the `draft` tail on every entry so the compute can tell.

## Page numbers chosen

`seqAddr.md:223` — "`0050-0099` | structural pages, mostly in the kernel or templates". `decisions.md:287` — "Each type is a card on a kernel structural page (0050-0099)". The kernel's own rule pages are structural, so they go in 0050-0099. The order inside that range is not in the spec (`7`); chosen: the order the brief and `review.md:150-159` list the pages, starting at the first number of the range.

| Page | Title | Faces | Source of the number |
|---|---|---|---|
| `0000` | kernel | 00, 04 | `decisions.md:258` — "`00.00.00` is its own book, `00.00.00.0000` its identity page." |
| `0050` | axioms | 00, 01, 02, 03, 04, 06.01 | `7`: `decisions.md:598` lists "The axioms' own page number." as open. Provisional: first structural page. |
| `0051` | seqaddr | 00, 01, 02, 04, 06.01 | `7` order; range from `seqAddr.md:223` |
| `0052` | faces | 00, 01, 02, 04, 06.01 | `7` order; range from `seqAddr.md:223` |
| `0053` | tails | 00, 01, 02, 04, 06.01 | `7` order; range from `seqAddr.md:223` |
| `0054` | types | 00, 01, 02, 04, 06.01 | `decisions.md:287` (page types) and `decisions.md:510` (card types "on a structural page") |
| `0055` | brands | 00, 01, 02, 04, 06.01 | `7` order; range from `seqAddr.md:223` |
| `0056` | drafting | 00, 01, 02, 04, 06.01 | `7` order; range from `seqAddr.md:223` |
| `0057` | workflow-loop | 00, 01, 02, 04, 06.01 | `7` order. `workflow-loop.003.md:232` puts the templates in the kernel "as card types under C8.9" (a structural page). Not a band head: the workflow bands `0300/0400/0500/0700` are proposed (F.2). |

Not seated, on purpose:
- `0012` dictionary. `decisions.md:443` — "The kernel supplies a small base dictionary that books inherit." No words are listed, so there is nothing to copy (`7`). A page with no content face is invalid (`decisions.md:274`).
- `0001-0009`, `0010-0019` (except 0012), `0020-0049`: the spec names no kernel content for them (`7`).
- `9999`, `PP99`, face 08: no continuation and no links yet. "Missing is a valid state" (`decisions.md:205`). Face 08 design is open (C4).
- Band heads `0100`-`0900`: their definitions are not in the spec (`7`).

## Face choices
- 01 cards copy the decision text (`decisions.md`) or, where no decision text exists, `seqAddr.md` / `workflow-loop.003.md`.
- 04 cards copy the person-facing text from `seqAddr.md`, `brands.md`, `drafting.md`, `kernel-design.md`, or the F.1 approval table. Each has `source:` and `why:`.
- `why:` copies a reason sentence from the spec when one is written. When none is written, it is `4.7` (a why that is missing; `Axioms.md:25` "A bare `7` warns, and a chain names what is missing: `4.7` a why"). It is never invented.
- Where no person-facing text exists, the 04 body is a `7` hole saying so. C3.2 requires the card, so each is a required absence: reported, not filled.
- Axioms page: 01 "agent form" = the Holds column of `decisions.md` E1 (`:538-546`); 02 "cite card" = E3 chain grammar; 03 "menu" = derived menu (hole) + cold set; 04 "full explanation" = each axiom's paragraph in `Axioms.md`, why = `Design.md` "Gives" column; 06.01 = notes.
- Only face 00 carries a stamp. `decisions.md:176` — "Faces carry no stamp of their own; the page stamp is stored once." The brief asked for a stamp header on each face; the spec wins (CONTRACT.md: "Where this contract and the spec disagree, the spec wins").
- 03 menu entries are "derived by the compute" (`decisions.md:516`); not written.
- 06 notes: one counter, `06.01`, this session (`seqAddr.md:155` "one counter per session"). Note fields are open (C7), so notes carry none. Boards `06.00` are not written (CONFLICTS K02).

## Workflow-loop page source
Page 0057 copies `workflow-loop.003.md` (state: draft, revision `.003`). `.002` (`workflow-loop.md`) is kept as lineage and not copied, except two 04 bodies that quote `workflow-loop.002-notes.md` (lines 40 and 48), because `.003`'s own notes file is not in docs/spec. Differences that matter are in CONFLICTS.md section B (W01-W15).

## Samples (`kernel/samples/`)
Test fixtures, not kernel content, also all draft.
- Desk `10` "personal" (`10.00.00`), shelf `10.11` "me" (`10.11.00`), book `10.11.21` "about-me". Identity pages are face 00 only (CONFLICTS K10).
- Inheritance: `10.11.21.0056` overrides kernel face `00.00.00.0056.04` with a local 04 card `Never From Memory` (the Director's own words: "Copy it then update don't create from memory."). Faces 01, 02 and 06 are missing locally, so the lookup `book -> shelf -> desk -> kernel` (`decisions.md:55`) finds them at `00.00.00.0056`. `seqAddr.md:228` — "A page in `0001-0099` that exists in a book is a local override of the inherited environment." `7`: the named override form (C5.4, proposed) is not designed, so the card carries none.
- Bob test: page `10.11.21.1001` "bob" holds brand cards `bob` (bob.001, "the user's name") and `cats` (cats.001, "animals the user likes") on face 01, each with a 04 card quoting session 1, "My name is Bob and I like cats". The dictionary `10.11.21.0012`, face 03, counted, has section counters `03.14` (bi-bq: `bob`) and `03.16` (ca-cg: `cats`) per `decisions.md:459-460`. `7`: there is no "fact" card type in C8.9, so the fact lives on brand cards. Meters are compute-only (C8.7) and none are recorded, so none are written.
- `7`: whether a draft face is found by the lookup is not in the spec. The compute decides; every entry carries its tail.

## Holes left as `7`
1. Axioms page number (E8 open).
2. Order of pages inside 0050-0099.
3. Stamp `state:` values, and whether a stamp takes a tail.
4. Page `type` for kernel pages: chosen `system` from the C1.4 list; the list gives no meaning per type.
5. Kernel base dictionary words (C8.5).
6. 03 menu entries (derived).
7. Missing whys: 04 cards with `why: 4.7` (count in the builder's findings).
8. Missing person-facing 04 bodies (hole text).
9. Note fields (C7). Face 08 links (C4). Lineage on 00/08, kept by the compute (E6).
10. Content face of an identity page (K10).
11. A "fact" card type.
12. Whether drafts resolve through inheritance.
13. Named override form (C5.4).
14. Seed timestamp: fixed `2026-11-11T19:30:00Z` for a deterministic build.
15. Whether band head `1000` must exist before page `1001` in the sample.
16. `7.8`: `axioms/` folder, `axioms/06.01.md`, `workflow-loop.003-notes.md`, decision codes F02-F10.

## Build
`node kernel/build.mjs` writes `books/00.00.00.book`, `books/10.00.00.book`, `books/10.11.00.book`, `books/10.11.21.book` (JSON Lines, `docs/CONTRACT.md`), `by: prima-kernel-seed`, one proposal id per page. `--check` rebuilds and fails if `books/` differs. Hard checks (grammar of names, tails, face 00, content face, C3.2 04 cards, card types) stop the build; findings print.

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
| 03 | `menu` | decisions.md:516 | hole: derived |
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
| 04 | `finding` | seqAddr.md:98-104 |  |
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
| 04 | `which-pages-need-a-title` | seqAddr.md:115-116 |  |
| 01 | `identity-page` | decisions.md:143-149 |  |
| 04 | `identity-page` | seqAddr.md:56-62 | why missing: 4.7 |
| 01 | `checked-labels` | decisions.md:152 |  |
| 04 | `checked-labels` | seqAddr.md:116 | why missing: 4.7 |
| 01 | `owner-rule` | decisions.md:161-173 |  |
| 04 | `owner-rule` | seqAddr.md:44-53 | why missing: 4.7 |
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
| 01 | `face-identity` | decisions.md:176 |  |
| 04 | `face-identity` | seqAddr.md:64 | why missing: 4.7 |
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
| 04 | `bound-bands` | workflow-loop.002-notes.md:40 |  |
| 01 | `code-in-the-repo` | workflow-loop.003.md:70-81 |  |
| 04 | `code-in-the-repo` |  |  |
| 01 | `n4-approval` | workflow-loop.003.md:87-93 |  |
| 04 | `n4-approval` |  |  |
| 01 | `packs` | workflow-loop.003.md:99 |  |
| 04 | `packs` |  | why missing: 4.7 |
| 01 | `risk-and-governing-targets` | workflow-loop.003.md:150-154 |  |
| 04 | `risk-and-governing-targets` |  |  |
| 01 | `the-loop` | workflow-loop.003.md:160-177 |  |
| 04 | `the-loop` | workflow-loop.002-notes.md:37-38 | why missing: 4.7 |
| 01 | `return-placement` | workflow-loop.003.md:181-183 |  |
| 04 | `return-placement` | decisions.md:611 | why missing: 4.7 |
| 01 | `review` | workflow-loop.003.md:199-202 |  |
| 04 | `review` |  |  |
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
