# seqAddr Decisions

Working record of decisions on the open items in `claude/seqaddr-review.md`, each with its reason. The rules are applied in `seqAddr.md`, `format.md`, `brands.md` and `drafting.md`. Section E records the axioms (`Axioms.md`).

---

## A1. Short form

Status: settled.

### A1.1 Every address is full; short form only leaves parts unstated
A page or face always has a full address `DD.SS.BB.PPPP[.FF[.NN]]`. Short form is a way of *writing* it that leaves out ancestors. Those are inferred from the active book's book, shelf and desk.

### A1.2 The page is the anchor
The page is the only 4-digit axis. Any address with a 4-digit group can be read by position alone:

```
[DD.][SS.][BB.] PPPP [.FF][.NN] [.tail]
```

- Right of the page: 1 group = `FF`, 2 groups = `FF.NN`.
- Left of the page, reading right to left: `BB`, then `SS`, then `DD`.
- The number of groups on the left decides what is inferred:

| Written | Inferred from active book | Example in `10.11.21` |
|---|---|---|
| `PPPP...` | DD, SS, BB | `4442.01` -> `10.11.21.4442.01` |
| `BB.PPPP...` | DD, SS | `12.2523.04` -> `10.11.12.2523.04` |
| `SS.BB.PPPP...` | DD | `30.12.2523` -> `10.30.12.2523` |
| `DD.SS.BB.PPPP...` | nothing | already full |

### A1.3 No page means a container address from the desk
An address with no 4-digit group is always read from the desk: `21` is desk 21, `10.11` is a shelf, `10.11.21` is a book. To refer to a sibling book in short form, use its sentinel page: `21.0000` is book 21 on the active shelf.

### A1.4 Counters attach only to faces
`NN` exists only directly after `FF`. Counters are not an axis, so the reserved 01-09 range does not apply to them. The first counter is `01`.

### A1.5 Exact widths
Every group must have its exact width. `4442.1` is invalid, not padded to `4442.01`.

### A1.6 Active page
The session has one active book, and usually an active page, but sometimes several pages are in play. A bare `04` cannot mean "face 04 of the active page", because A1.3 already reads it as desk 04.

A **leading dot** means "relative to the active page".
- `.04` is face 04 of the active page.
- `.05.03` is task 03 on the active page.
- No other address starts with a dot, so this never collides with A1.3.
- If more than one page is active, `.04` is ambiguous and is elevated to the user (same as A1.8).

### A1.7 Short form is for users; models echo the full address
Users may write short form. Models always write the full address. When a user writes short form, the model states the expanded full address back. If the address was inherited (A1.8), the model also states where it was found.

### A1.8 Reading vs. finding
- **Reading** (is it well formed?) uses only A1.2-A1.5. It needs no context beyond the active book.
- **Finding** (where is it?) looks up in order: book -> shelf -> desk -> kernel. The first match wins. This matters for the inherited reserved pages (0020-0049).
- If nothing is found, the address is **elevated to the user** to resolve. It is never guessed.

### Carried forward
- Where a shelf or desk physically keeps its own pages (needed for the A1.8 lookup) belongs to **A4**.
- The kernel's address belongs to **A6**.

---

## A2. Titles and tails

Status: settled.

### A2.1 Position decides
A word after DD, SS, BB or PPPP is a title. A word after FF or NN is a tail if it is a tail word, otherwise a card key (amended by C8.2). Faces never have titles.

### A2.2 Faces carry no title
A face is written `PPPP.FF` or `PPPP.FF.NN`. `2423.05.01` is page 2423, face 05 (tasks), counter 01: one task. "Go to 2423.05.01 and run it" is unambiguous.

### A2.3 Title characters
Lowercase letters, digits and hyphens. Starts with a letter. No dots, no spaces.

### A2.4 Titles are labels and need not be unique
A title is not part of identity: `4442` and `4442.plan` are the same page. Several pages may share a title on purpose. This is how a band set works (A2.6).

### A2.5 Where tails attach
A tail follows a title or a face:
- Page: `PPPP.title.tail`
- Face: `PPPP.FF.tail`
- Counter: `PPPP.FF.NN.tail`

Only a tail may follow a title.

Tail words are reserved and can never be titles. `PPPP.draft` and `PPPP.plan.draft` both mean page PPPP in draft.

Allowed tails per level:

| Level | Tails |
|---|---|
| Page | `draft`, `retired` |
| Face | `draft`, `retired` |
| Counter | `draft`, `pack`, `open`, `return`, `review` (bare = closed) |
| Desk / shelf / book | none |

Workflow state lives only on counters. A container takes its state from its sentinel page: `10.11.21.0000.retired` retires the book, `10.11.21.0000.draft` is a book still being set up.

### A2.6 Bands
A page number reads as `NDNN`. `D` (the second digit) is the band.

```
0 4 23
N D NN     D = 4 = dev band, NN = 23 = item in the band
```

- **Fixed width.** Every band is exactly 100 pages, `PP00` to `PP99`.
- **Head by number.** Every page at or above 0100 ending in `00` is a band head. It holds the band's definition and contents. No marker or tail is needed: listing pages that end in `00` finds every band.
- **`PP99` is continuation.** A band that outgrows 100 pages points to its continuation from `PP99`, as page 9999 does for a book. This mirrors the axis sentinels: `00` start, `99` end.
- **Sets across bands are linked by number.** Pages with the same `N` and `NN` in different bands are one set: `0423.timer` (dev) and `0523.timer` (build). Titles should match; a mismatch is elevated to the user (A2.8).

### A2.7 Book page layout
The kernel is the template for `0000-0999` in every book, including what each band digit means there.

| Range | What it is |
|---|---|
| `0000` | book identity (sentinel) |
| `0001-0099` | reserved; a page here is a local override of the inherited environment |
| `0100-0999` | standard bands modelled by the kernel (`0100` ... `0900`) |
| `1000-9998` | user space; users design their own bands (`1000` ... `9800`) |
| `9999` | continuation (sentinel) |

`1000` is the head of the first user band, which is why the first open page is `1001`.

### A2.9 Live inheritance
Books follow the kernel template live; they do not copy it at creation. Anything a book does not override is found through the A1.8 lookup (book -> shelf -> desk -> kernel), so a kernel change reaches every book that has not overridden it.

### A2.8 Which pages need a title
1. Pages 1000 and up must have a title, stored in the stamp.
2. Pages 0001-0999 may have a title; their number is already their name. Page 0000 has none (it holds the book's title in its stamp).
3. A title in a written address is optional. If written, it is checked against the stamp. A mismatch (`4442.timer` when the stamp says `clock`) is elevated to the user.
4. Tail words can never be titles (A2.5).

---

## A3. Where container titles live

Status: settled.

### A3.1 Every container is identified by a page 0000
Each desk, shelf and book has an identity page. Its stamp holds the container's title.

| Container | Identity page |
|---|---|
| Book `10.11.21` | `10.11.21.0000` |
| Shelf `10.11` | `10.11.00.0000` |
| Desk `10` | `10.00.00.0000` |

### A3.2 Titles in addresses are checked labels
A title written in a container address (`10.11.21.tools`) is checked against the identity page's stamp. A mismatch is elevated to the user (A2.8).

---

## A4. Meaning of 00 and 99

Status: settled.

### A4.1 00 means "the owner of the level above, itself"
One rule for every container axis:

| Address | Meaning |
|---|---|
| `DD.00.00` | the desk's own book (identity, law, overrides) |
| `DD.00.BB` | a desk book: owned by the desk, no shelf |
| `DD.SS.00` | the shelf's own book |
| `DD.SS.BB.0000` | the book's own page |

Consequences:
- The A1.8 lookup uses real books: book `10.11.21`, then shelf `10.11.00`, then desk `10.00.00`, then kernel. An inherited page such as `0020` lives at `10.11.00.0020` or `10.00.00.0020`.
- A container's state uses page tails (A2.5): `10.00.00.0000.retired` retires the desk.
- Shelf 00 and book 00 are never ordinary shelves or books.

### A4.2 Face 00 is the page's identity
`PPPP.00` holds the page's stamp: address, title, state. Faces carry no stamp of their own; the page stamp is stored once.

### A4.3 Face ranges
| Faces | Use |
|---|---|
| `00` | page identity (A4.2) |
| `01-09` | system faces (01-08 defined, 07 reserved, 09 unassigned) |
| `10-98` | not used in this design; reserved for later customization |
| `99` | reserved |

### A4.4 `FF.00` is the board of a counted face
A counted face's `00` lists every counter and its current tail, like a kanban board:

```
1523.05.00   board for build tasks
  05.01  closed
  05.02  review
  05.03  open
```

- A face is counted **if and only if `FF.00` exists**. The board's presence is the check.
- A counter `FF.NN` without `FF.00` is invalid.
- A counted face is never seated. Plain `FF` on a counted face means `FF.00`. The seated address `DD.SS.BB.PPPP.FF` applies only to faces without counters.
- Faces 05 (tasks) and 06 (notes) are always counted. Other faces may be counted on certain page types, for example 03 or 04 on a contents or dictionary page.

### A4.5 `FF.99` is the counter continuation
`FF.99` is required only once `FF.98` exists. Its contents are defined in A6.

### A4.6 Missing is a valid state
Absence carries meaning and is not an error: no `FF.00` means the face is not counted, no `FF.99` means no continuation, no `9999` means the book does not continue.

---

## A5. Meaning of 99 and continuation

Status: settled.

### A5.1 99 means "look for the next location"
At every level, 99 is a pointer, never content. It lists all valid paths onward. Its face 08 (map) records each target and the kind of link (continuation or child).

| Where | Pointer to |
|---|---|
| `DD.99` (identity `DD.99.00.0000`) | child desks |
| `DD.SS.99` | shelf continuations or children |
| `....9999` | book continuations |
| `PP99` | band continuations |
| `FF.99` | counter continuations |

Missing means no continuation (A4.6).

### A5.2 One pointer, many targets
A 99 pointer may list several targets. One desk can have several child desks, and one book can continue in several places.

### A5.3 Back-links are required
Every target's identity page must link back to the pointer that names it. A link that only goes one way is a validation error.

Child desks take their own top-level desk number (10-98). Hierarchy beyond the fixed depth exists only through these links.

### A5.4 Ancestors are updated on every continuation
When a chain continues, every ancestor in the chain is updated with the new location.

Each pointer's **direct** links (A5.2, A5.3) are the source of truth. An ancestor's list of all locations further down the chain is **derived**: regenerated by walking the direct links whenever a continuation is added, never edited by hand. This meets the requirement while keeping one source of truth, so a missed or partial update can always be repaired by regenerating.

---

## A6. Capacity, namespace and kernel

Status: settled.

### A6.1 Overflow
**Counters.** When `FF.98` exists, `FF.99` points to the same face on the **next free page in the same band**. Counting restarts at `01` there, and that page's `FF.00` board links back (A5.3). Old counters never move.

**Bands.** When a band has no free page, it continues: `PP99` points to the next free hundred, which becomes the continuation band. Example: band `1000` is full and the first free hundred is `2100`, so `1099` points to `2100`.

Bands never grow in place; they always continue through `PP99`. This keeps A2.6 intact: fixed 100-page bands, every `xx00` a head, and sets linked by number. Items in a continuation band (for example `2123`) do not line up by number with their set in other bands, so they link to their set explicitly in face 08.

### A6.2 One namespace per repository
Each repository is its own address space. Desk `10` in one repository is unrelated to desk `10` in another.

### A6.3 Kernel and branches
| Desk | Use |
|---|---|
| `00` | kernel. `00.00.00` is its own book, `00.00.00.0000` its identity page. The A1.8 lookup ends here. |
| `01-09` | kernel branches |
| `10-98` | user environments. An instantiated workspace is a desk 10 or above. |

Example branch: SoF (Science of Fiction), a space for building a book using RPG elements to test paths and branches, rewind the story and fork it. Likely a shelf on desk 01. A fork maps naturally to a multi-target 99 pointer (A5.2).

### A6.4 The kernel lives in each repository
Every repository contains its own kernel (desk 00). Kernel branches (desks 01-09) are downloaded into the repository as needed.

---

## C1. Which faces a page needs

Status: settled, except the pointer/index split in C1.4.

### C1.1 Face 00 plus one content face
A page is valid when it has face 00 and at least one of faces 01-06 or 08. Face 07 is not active and does not count. A page with only an identity has no reason to exist.

### C1.2 Draft faces count and are allowed anywhere
A draft face (`04.draft`, `05.01.draft`) counts toward C1.1 and may exist on any page, live or draft. A brand-new page may start with only drafts.

### C1.3 Retiring the last face retires the page
If the last content face is retired, the page is retired with it. The compute then updates every derived path that referred to it: boards, contents lists, ancestor lists and incoming links (A5.4).

### C1.4 Page types
Page number alone is not enough to say what a page is for. A page type is a property that rules attach to.

- **`type` is a field in the page stamp** (face 00).
- **Starting types:** `system`, `general`, `code`, `workflow`, `band`, `pointer`.
- **Defined in the kernel.** Each type is a card on a kernel structural page (0050-0099), marked `owner: kernel-only`, so no book can redefine it. Live inheritance applies.
- **Rules a type can carry:** required or forbidden faces, page ranges it may live in, who may write it, whether drafting (D0) is required.
- **Default:** the page stamp's type, else the default set by the page's band head, else `general`.
- **Changing a type** goes through drafting and review like any other change.

Open: `pointer` covers contents, dictionary and concordance pages. Do continuation pages (`99`, `9999`, `PP99`) share that type, or get their own?

## C2. Cards

Status: settled.

- A card is a `##` heading in a face's Markdown.
- Its key is the heading in title form: `Retry Policy` -> `retry-policy`.
- Keys are unique within a face. Cards with the same key on different faces are the same card.
- A face's contents list is derived from its cards, never written by hand.

---

## D0. Drafting: never rewrite from memory

Status: principle settled (from `drafting.md`); mechanism proposed. Belongs to section D.

A model must not rewrite a face from memory. Every change goes through a draft that starts as a copy and is changed one note at a time:

1. Copy the existing face to `FF.draft`.
2. Add notes from memory to the draft. Notes, not edits.
3. Check for additional sources and add notes from them.
4. Merge the notes one at a time, striking each as it is merged.
5. Record overflow and unprompted ideas as new notes. Once all notes are merged, go on.
6. Read the whole face again and write notes again. A full view is needed to write well.
7. Merge and strike those notes.
8. Read again. If there are no more notes, hand back for review.

Proposed: the compute enforces this through its operations, so a face cannot be replaced from memory:

| Op | Effect |
|---|---|
| `copy` | the compute copies the current seated face to `FF.draft`. The writer supplies no body. |
| `note` | add one note to a draft |
| `merge` | apply one change to the draft body, citing the note it comes from; that note is struck |
| `promote` | after review, the draft replaces the seated face |

- A full-body `put` is allowed only to create a new face, never to replace an existing one.
- Every change to a draft traces back to a note, and review can check that every note is struck.

---

## C3. Face 04 is a full explanation, not a mirror

Status: settled.

### C3.1 Shape of a 04 card
Every card on face 01 or 02 has a matching 04 card with the same key:

```
## Job
source: [01 / Job], [02 / Job]
why: Routing should reduce reading without replacing the source.
<full explanation, written for a person>
```

A card title (its `##` heading) is also stored in the dictionary (C8).

### C3.2 Hard rules and findings
| Check | Kind |
|---|---|
| Every 01/02 card key has a 04 card | hard: the compute rejects the write |
| That 04 card has a `why:` line and a body | hard |
| The 04 body is not identical to the 01 body | finding: flagged for review |
| The 01 card's keywords appear in the 04 card | finding |
| A 01 card and its 04 card disagree | elevated to the user for correction; neither governs (axiom 1) |

### C3.3 Keywords are brands
The model proposes keywords for a card and hands them to the compute, which stores each one in the dictionary with what it states. If a matching meaning already exists, it is reused. See C8.

---

## C4. Face 08 links

Status: direction set; design open.

Face 08 is the links face: every connection to other pages that matters to this page. Most pages have none; some have many. The compute holds all connections in memory, so it can see and trace them. How the compute stores and traces them is still to be designed.

## C5. Authority

Status: order and levels settled; precedence between levels proposed. Source: axiom 1 (`axioms/`).

### C5.1 The order
A person holds authority and grants it on. Compute enforces it. A model works within it. The live record keeps it. Authority is granted, never claimed.

### C5.2 User levels
| Level | User type | Reaches |
|---|---|---|
| `00` | internal authorised admin | the kernel. The kernel is small and nearly untouchable, which is why it is `00`. |
| `01` | power user | can modify up to desk level |
| `02` | weaker form, to define | less than `01` |
| `03` | weaker than `02`, more than `04` | to define |
| `04` | basic user | sees face 04 only; compute and the model do the rest |
| `05-09` | specialist | to define |

Like user accounts in an operating system: a few basic types, linked to `00-09`.

### C5.2a Authority is scoped to the environment
A level is held within an environment, and the same holder can hold different levels in different places: a magic user may hold `01` in an isolated book and only `04` everywhere else. Authority runs desk > shelf > book. A grant reaches down from where it is attached, never up or sideways: `01` in a book cannot override its shelf, its desk, or another book.

Open: what exactly `02`, `03` and `05-09` grant.

### C5.3 Halts rise up the order
Two live claims with no lawful connection halt and go to whoever holds more authority. A magic user can resolve one, with compute and the model laying out the choice.

### C5.4 Precedence between levels (proposed)
From axiom 2: a lower level may differ from a higher one only through a named and approved override. The lookup (book, shelf, desk, kernel) finds things; axiom 2 decides whether a found difference is lawful.

## C6. Face 03 in normal books

Status: settled.

- Face 03 is allowed in normal books on their reserved pages (0001-0099). The kernel and desk books may use it anywhere.
- User pages are mostly face 04. A 04 section may have a 01 card: a brief of how a model should understand it. It has a 02 card only when the section describes a task process.

## C7. Notes metadata

Status: open, to discuss.

---

## C8. Dictionary and brands

Source: `brands.md`. Status: settled, except C8.7 (assumed-only failures) and C8.10.

### C8.1 Brands
A word can carry several meanings. Each meaning is a **brand**, `word.NNN`, backed by a **brand card**. A user's explained meaning of a word is recorded as a brand, so models never fall back on an average meaning.

### C8.2 Addressing: a word after a face is a card
A word after a container is a title (A2.1); a word after a face is a card key. `10.10.11.1014.01.ham` is card `ham` on face 01 of page 1014. Tail words stay reserved, so they never collide with card keys. A 3-digit group can only be a brand number: `ham.002`.

### C8.3 The dictionary is only an index
The dictionary (page 0012, face 03, counted) maps a word to its brand cards and nothing more:

```
ham.001 -> 10.10.11.1014.01.ham
ham.002 -> 10.10.11.1026.01.ham
ham.003 -> 10.10.11.1145.01.ham
```

`0012.03.00` is the menu of sections. Brand numbers are never reused or renumbered.

### C8.4 Brand cards carry the meaning and the meters
A brand card is titled with the word and lives on the face 01 of the page that explains it. It holds:
- the surface forms it covers (case-sensitive): `Ham, Hammie, hammie`
- what it means: "user's friend from work"
- **meters:** the top 5 words found with it, and how often each appears when this meaning is used. For `ham.001`: sandwich 100%, lunch 95%, hungry 75%, eat 50%, meal 43%.

To resolve a word, the compute finds it in the dictionary, reads each brand card, and compares the sentence against the meters.

### C8.5 Local first; brand number sentinels
Each book keeps its own dictionary. The kernel supplies a small base dictionary that books inherit. Linking dictionaries to other books (source books) is a later design issue. Brand numbers `000` and `999` are reserved and unused; brands run 001-998.

### C8.6 Fixed dictionary layout
One layout, the same from the kernel out. Sections are never re-split. Each letter gets 1-5 sections by its share of English words (PlainSpell, Wiktionary, 2026): S at 10.7% gets 5, so each section holds about 2.1%.

| Range | Use |
|---|---|
| `03.00` | menu |
| `03.01-03.09` | reserved: words starting with digits or symbols |
| `03.10-03.61` | letters, below |
| `03.62-03.98` | reserved |
| `03.99` | continuation |

| Letter | Sections |
|---|---|
| A | `10` a-ak, `11` al-ap, `12` aq-az |
| B | `13` ba-bh, `14` bi-bq, `15` br-bz |
| C | `16` ca-cg, `17` ch-cn, `18` co-con, `19` coo-cz |
| D | `20` da-de, `21` df-di, `22` dj-dz |
| E | `23` ea-em, `24` en-ez |
| F | `25` fa-fk, `26` fl-fz |
| G | `27` ga-gk, `28` gl-gz |
| H | `29` ha-hh, `30` hi-hz |
| I | `31` ia-im, `32` in-iz |
| J, K | `33`, `34` |
| L | `35` la-lh, `36` li-lz |
| M | `37` ma, `38` mb-mi, `39` mj-mz |
| N, O | `40`, `41` |
| P | `42` pa-pd, `43` pe-pk, `44` pl-pq, `45` pr-pz |
| Q | `46` |
| R | `47` ra-re, `48` rf-rz |
| S | `49` sa-sc, `50` sd-sh, `51` si-so, `52` sp-st, `53` su-sz |
| T | `54` ta-th, `55` ti-tz |
| U, V, W, X, Y, Z | `56`, `57`, `58`, `59`, `60`, `61` |

- A word is placed by its lowercase form; case still separates brands inside the entry.
- Missing sections are valid (A4.6): a small book creates only what it needs.
- Within-letter boundaries are estimates and are checked against a real word list before the layout is frozen.
- This layout reserves `03.01-03.09` by its own definition. A1.4 (the reserved range does not apply to climbing counters) still stands.

### C8.7 Meters are written only by the compute
The compute records each resolution of a word: the brand chosen, the sentence's words, and the outcome. Meters are calculated from these records. They are shown on the card, readable by a person, never written by hand, and exempt from drafting (D0).

| Outcome | Signal |
|---|---|
| success | the output runs and the user carries on |
| failure | negative words; the user stops the process; **restatement**: the user repeats and over-explains because the first attempt failed |

On a failure, the compute updates the brand cards linked to that resolution.

Open: does a failure count only against a brand that was assumed (recent or default) rather than matched by meters? Proposed: yes, and a repeated failure triggers the probe in C8.8.

### C8.8 Resolving a word
1. The sentence matches one brand's meters clearly: use it.
2. No clear match: use the brand last used in this session.
3. None used yet: use the default marked in the dictionary entry.
4. No default, or no brand at all: use the LLM's ordinary meaning.

Any assumption is stated back ("ham, taken as ham.001, the sandwich").

When the user shows a meaning the dictionary does not have, the compute pushes the model to ask for it. The model hands the answer to the compute, which creates the brand card and the dictionary entry. The new card goes through drafting (D0); the user confirming the meaning is its review.

### C8.9 Card types
A card type is to a card what a page type is to a page (C1.4).

- `type:` is a field line directly under the card heading. Field lines (`name: value`) come first, then a blank line, then the body.
- Each face has a default type, so most cards need no `type:` line.
- Types are defined in the kernel on a structural page, `owner: kernel-only`, inherited live. A definition states: faces allowed, required and optional fields, fields only the compute writes, whether a 04 card is required, hard checks and findings, whether drafting applies.

| Type | Default on | Fields | Needs a 04 card |
|---|---|---|---|
| `rule` | 01 | `owner` | yes |
| `schema` | 02 | `source`, `form` | yes |
| `menu` | 03 | entries derived by the compute | no |
| `why` | 04 | `source`, `why` | - |
| `task` | 05 | section D | no |
| `note` | 06 | C7 | no |
| `link` | 08 | `target`, `kind` | no |
| `brand` | 01 | `brand`, `forms`, `means`, `meters` (compute) | no |
| `index` | 0012.03 | `default`, brand list | no |

### C8.10 Where a new brand card goes (open)
A brand card lives on face 01 of a page that explains the meaning. When the page does not exist yet: the model asks the user which page, or each book has a default terms page.

---

## E. Axioms

Source: `Axioms.md` (context form) and `axioms/` (faces 00-04, notes 06.01). How each was reached is in `axioms/06.01.md`; the lab evidence is in `claude/labs/notes/`. The axioms are the shape; seqAddr is the geometry (AGENTS.md).

### E1 The nine
Status: settled. Numbers and order kept from the kernel original.

| # | Name | Was | Holds |
|---|---|---|---|
| 1 | Authority | | granted, never claimed; person, compute, model; the live record; halt on two live claims |
| 2 | Fractal | | same shape at every scale; inherit, write only the difference; named, approved overrides |
| 3 | Leads | Dance | three intelligences; the lead letters M, P, C; every piece of work has a lead |
| 4 | Why | | a law without its why is incomplete; record it; never invent one |
| 5 | Frame | Narrow | know the aim and why; full intelligence inside the frame; report, do not act, outside it |
| 6 | Lineage | | the line travelled back to authority and forward to what depends; the past is not rewritten |
| 7 | Missing | | a gap is normal; ask why, then whether written permission exists; never invent |
| 8 | Connection | Record | lawful connections only: inherited, linked both ways, named override; agreement is not connection |
| 9 | Trial | Hostile | work is not right because you made it; a hostile pass from another view before promotion |

Why: a model receives a large concept in a very small package. Lab 03 put each against a trap; none broke.

### E2 Cite and the `axioms:` field
Status: settled.
- To cite is to attach a chain of axioms. The field is `axioms:`.
- It is optional on every card and on the page stamp.
- A cite runs nothing and permits nothing.

Why: the field name says what it carries; "cite" is the act (Director).

### E3 Chain grammar
Status: settled.
- A dot orders axioms inside one piece (`1.7.8`). A comma splits pieces (`1,3`). A later axiom refines; it does not replace.
- A one-digit mark is an axiom, never an address part. A chain is never an address.
- Only axiom 3 takes a modifier: one to three distinct letters from M, P, C, with no dot (`3MPC`, `3C`).
- `7` follows the same order rule as every axiom: `7.8` is a connection that is missing; `8.7` is a connection that is incomplete.
- Cold set before a write: `1.7.8`.

Why: order is meaning, and a special case for `7` would break the same shape (axiom 2). Lab 02 cold readers split on `8.7`; with the `7` line, lab 03 readers agreed.

### E4 Default lead
Status: settled.
Every piece of work has a lead: named on it, or the default set by its band or pack. Another may do the work, but raises it before moving forward.

Why: in three labs, models handed work to compute only where `3C` was cited; the packed card alone never did it.

### E5 Packed face and its why
Status: settled. A face 01 card is the packed form of its 04 card. A model that needs more requests the why from the compute by card key. When the two disagree, it is elevated to the user (C3.2).

### E6 Lineage is kept with the page
Status: settled.
- Lineage lives with the page; its book, shelf and desk rule over it.
- It appears on face 00 and face 08. It is not user-facing: the compute keeps it.
- It is travelled in two directions, back and forward, through structure and through time.
- An override links back to who authorized it.

Why: authority without lineage is only hierarchy (Director). Related: C4.

### E7 Trial and the `9` mark
Status: settled, one part open.
- Nothing is promoted until it has faced a hostile pass from a view other than its maker's.
- Before replacing anything, its predecessor is opened read-only.
- `9` marks what has not yet faced its trial.
- Open: must the pass come from a different intelligence (a person, another model, compute), or does a fresh sitting of the same model count?

### E8 Open from the axioms
- "Written permission" (axiom 7): a recorded grant, or a direct instruction? `claude/readpath.md` assumes a pack's grant is the permission.
- Levels `02`, `03`, `05-09` (C5.2).
- Marks: draft, signed, approved, lock (carried; a proposal is in `claude/kernel-notes.md` 3.5).
- Hats as roles (section D).
- The axioms' own page number.

### E9 Proposals awaiting the Director
Status: proposed, not applied. From `claude/kernel-notes.md` (what the old kernel answers), `claude/readpath.md` (how a prompt becomes a pack, R1-R9) and `kernel-design.md`.

These would change a settled decision:
- Face 05 counters split into tasks (`05.01-05.49`) and tickets (`05.50-05.99`). Against A1.4.
- Patch and strike as small changes to a seated face. Against D0's copy, note, merge, promote.
- A concordance (word to page) beside the dictionary. Adds to C8.3.

These close open items:
- C4 link kinds: `member-of`, `continues-from`, `references`, owner, exception, custody.
- C5.4 precedence: owner class (kernel-only, desk-local, book-local) on each law section.
- C7 note fields: `by`, `date`, `refs`, `why`, `state`, `unresolved`.
- Where a return lives: on its counter; its findings are booked as 06 notes and 05 tasks on the pages they concern.
- A kernel bootstrap: a minimal contract fixed in compute, so it can read the kernel before the kernel loads.

---

## F. Workflow decisions

### F.1 Approval record for S01–S12

Approval reference: `F.1`, recording the Director's 2026-11-11 approval described in [Workflow Loop .002 drafting notes, Accepted decisions](workflow-loop.002-notes.md#accepted-decisions), read with [the `.002` draft](workflow-loop.md). The Director's 2026-11-11 instruction “Ok approved, write workflow-loop.003 now” authorizes entering these directions here and drafting the corrections. Scope: workflow design directions. Exact implementation mechanics and changes to existing governing decisions require their recorded disposition. This design approval does not serve as an N4 runtime grant.

The why column captures design rationale from the draft and review. It does not attribute new wording to the Director.

| Decision | Approved direction and scope | Why |
|---|---|---|
| S01 | Bind every workflow grant to an approval ID, exact N4 revision, frame, criteria, scope, and delegation. | A later N4 edit must not inherit authority by reusing the same page address. |
| S02 | Require inspectable evidence for returns in proportion to the risk of the work. | A reviewer must be able to test the claim, and the cost of verification should reflect the cost of error. |
| S03 | Close at the bare counter and record the outcome separately, including passed, failed, blocked, needs-authority, and abandoned. | The same lifecycle can preserve distinct reasons the work ended. |
| S04 | Record pack acceptance, MVP completion, and promotion separately. Allow routine promotion only within explicitly delegated N4 scope. | Evidence that a pack passed establishes neither the whole MVP nor authority to change what is live. |
| S05 | Distinguish corresponding workflow pages from continuation pointers and preserve SeqAddr overflow and identities. The workflow's proposed map and A2.6 amendment are addressed in F.2. | Matching subject digits can help a reader find related pages. Continuation must follow the actual pointer and backlinks. |
| S06 | Derive a read-only builder handoff from exact source references, approved criteria, dependencies, and current pack state. | A cold builder can reproduce its starting context, and stale copies can be regenerated from the governing records. |
| S07 | Use lowercase `w01`, `w02`, and onward as the work-card keys. | This follows the SeqAddr card-key grammar and keeps card keys distinct from counters. |
| S08 | Validate dependencies, modifications, and creations according to their target intent. | Dependencies and modification targets must resolve. A creation needs an available legal location. |
| S09 | Count passes per approved frame and track repeated blockers within it. | Gravity must follow the work across different agents and expose repetition without counting unrelated work. |
| S10 | Require independent evidence review, proportionate trials, and a recorded N7 trial before promoting governing changes. | Another view must test the artifacts against the criteria, with a deeper trial when inherited rules can change. E7 retains its open identity question. |
| S11 | Record one valid claim, its owner, recovery terms, and lineage to any replacement counter. | Competing claims and stale workers must not overwrite the record of an attempt. |
| S12 | Keep N4 design questions and N5 execution packs on separate counted boards, linked by explicit references. | Counter identity belongs to its own board, and equal numbers cannot prove a relationship. |

### F.2 A2.6 amendment for workflow sets

Status: proposed amendment for Director review with [workflow `.003`](workflow-loop.003.md#3-bound-bands). `9` trial pending. A2.6 and A6.1 retain their recorded status until the amendment is seated.

- In a workflow that adopts the map in `.003` section 2, matching `N` and `NN` identify candidates for a set. Membership requires explicit reciprocal Face 08 links. Matching titles help a person inspect the set.
- The workflow map defaults within `0100–0999`: `0300` build, `0400` dev, `0500` jobs, and `0700` colab. A user band adopts a workflow role by name in its band definition. A2.7's allocation stays in force.
- When seated, update the A2.6 example and A6.1 wording that treats sets as linked by number, then align `seqAddr.md` sections 6.1 and 7.1. Preserve fixed hundred-page bands, the `PP99` pointer and backlinks, and original identities when overflow occurs.

Why: Axiom 8 requires written connections for lawful traversal. Candidate discovery by number remains available, including during migration. Existing sets without reciprocal records need review before the amended rule governs them (`7`).
