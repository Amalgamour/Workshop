# Face 00: stamp, type and registry

**DRAFT.** This is a draft for the Director to read. It is not settled law.
It fills in what R19 asks for: "Fill out what is missing".
Anything marked PROPOSED is a builder's proposal. Anything marked `7` is open.

Lane: SEQPAGE. Code mirror: `crates/seqpage/src/face00.rs`.
A test checks that every type and field in the code is named in this file.

---

## 0. What face 00 is

Face 00 is the page's registry location. (R10, R19.)

The Director's words (R19): "It's a registry location, it can hold a stamp, a registry, it's type. Each page type can have a different set of registry fields to use."

The stamp lives in face 00. The page's state is kept there. (R12: "The stamp should go in the .00 as the reg location.")

So face 00 holds three things:

1. the stamp (who and what the page is),
2. the type (what kind of page it is),
3. the registry (fields that depend on the type).

### How it is written

Face 00 is one card body. It has two parts.

The stamp is front matter: lines between two `---` lines.

The registry is a card headed `## Registry` with `key: value` lines.

```
---
address: 10.11.40.0403
title: ide-design
type: workflow
state: live
---

## Registry
faces: 04 seated, 05 counted
role: dev
```

This is the form the kernel lane already uses on page 0054 (a front-matter stamp and a `## Registry` card). The exact layout is still `7` until KERNEL settles it (F9).

All text is plain ASCII (R4).

---

## 1. The stamp

These are the common fields. Every page may carry them.

| field | meaning | source | status |
|---|---|---|---|
| `address` | the page's full address `DD.SS.BB.PPPP` | decisions.md:176 (A4.2); R12 | sourced |
| `title` | the page's title; on page 0000, the container's title | decisions.md:131-132 (A2.8), :143 (A3.1); R12 | sourced |
| `type` | the page type (section 2) | decisions.md:285 (C1.4); R12; R19 | sourced |
| `state` | `live`, `draft` or `retired` | decisions.md:176 (A4.2); R12; seqAddr.md section 4 | sourced |
| `why-draft` | why the page is a draft | R5 | PROPOSED name |
| `axioms` | the axiom chain the page cites | decisions.md:553 (E2) | sourced |
| `lineage` | the line back to what governs the page | decisions.md:577-582 (E6); R19 | PROPOSED form |

### address

The stamp says the page's own address, without a title.

If the stamp address and the real address disagree, that is elevated to the user (A3.2).

### title

Pages 1000 and up must have a title (A2.8.1).

Pages 0001-0999 may have one. Their number is already their name (A2.8.2).

A title written in an address is checked against the stamp. A mismatch is elevated (A2.8.3).

### title on page 0000

v2 line 104 says: "DD.SS.BB.0000 No title allowed" (quoted in docs/design/OPEN.md:230).

decisions.md:132 says: "Page 0000 has none (it holds the book's title in its stamp)."

This draft reads both together. Page 0000 has no title **of its own**.

So `10.11.40.0000.workshop` is never a valid address, and the .seq file is named `10.11.40.0000.seq`.

But its stamp `title:` line holds the **container's** title: the book's, shelf's, desk's or kernel's name.

The checker asks for that title on page 0000, as A2.8 and A3.1 say. This reading is `7` until the Director confirms it (F1).

### type

`type:` names the page type. Section 2 lists the types.

If the stamp has no type, the band head's default applies, else `general` (C1.4, decisions.md:289).

### state

`state:` is `live`, `draft` or `retired`.

The compute also works the state out from the page's entries. If the two disagree, that is a finding (axiom 8).

### why-draft

R5 says drafts must be found, and must show why they are drafts.

So a draft page carries `why-draft:` with one plain sentence.

The name `why-draft` is PROPOSED.

The .seq view also shows `why-draft :=` for each draft face. It comes from the `reason` on the entry that opened the draft, else the first note line (seqpage.md).

### axioms

`axioms:` lists the axioms the page cites, like `1.4.5` (E2).

### lineage

`lineage:` is the line back to what governs the page (E6).

This draft proposes the inheritance chain form: `10.11.40.0403 < 10.11.40 < 10.11.00 < 10.00.00 < 00.00.00` (seqAddr.md line 102).

The compute keeps it. If it is written, it must match. The form is PROPOSED (F5).

---

## 2. The type field

The spec names six starting types (C1.4, decisions.md:285-286).

| type | what it is | source |
|---|---|---|
| `general` | an ordinary page; the default | decisions.md:286, :289 |
| `system` | a kernel or structural page | decisions.md:286-287 |
| `code` | a page whose faces describe code | decisions.md:286 |
| `workflow` | a page in a workflow band (build, dev, jobs, colab) | decisions.md:286; workflow-loop.003.md section 2 |
| `band` | a band head `N?00`: it binds pages into a work space (R13) | decisions.md:286; R13 |
| `pointer` | contents, dictionary and concordance pages | decisions.md:292 |

Types are defined in the kernel, as cards on structural pages 0050-0099, marked `owner: kernel-only` (decisions.md:287).

A type not in this list is a **finding**, not an error. The page is still read.

This draft invents no new types.

### Gaps (all `7`)

- Continuation pages (`99`, `9999`, `PP99`): `pointer` or their own type? Open in C1.4 (decisions.md:292). `7`
- Page 0000: no type is named for it. The kernel lane writes `system`. `7`
- Override pages 0001-0009 (R7): no type is named. `7`
- The common questions list (R11): no type is named. `7`
- A dictionary page sits under `pointer` (decisions.md:292). That is sourced, not a gap.

---

## 3. The registry

The registry is the `## Registry` card in face 00.

Some fields are common. The rest depend on the type.

### 3.1 Common registry fields

| field | meaning | source | status |
|---|---|---|---|
| `faces` | the page's faces and their state, like `01 seated, 04 draft, 05 counted` | R10; decisions.md:301 | sourced, see tension |
| `why-NN` | why face NN is a draft, like `why-04:` | R5 | PROPOSED name |

### The faces tension

R10 says face 00 is the registry, so it lists the faces.

decisions.md:301 says a contents list "is derived from its cards, never written by hand". A5.4 says the same for pointers.

This draft proposes: the compute writes `faces:`, nobody writes it by hand, and the checker compares it to what it derives.

A written `faces:` line that does not match is a finding. Which wins is `7` (F2).

### Compute-only fields

Some fields are marked compute-only. The compute fills them in.

If one is written and does not match what the compute derives, that is a finding.

The value `7` means "not known yet". It is never a mismatch.

### 3.2 Fields by type

`C` = compute-only.

| type | field | meaning | source | status |
|---|---|---|---|---|
| `general` | (none) | only the common fields | decisions.md:289 | sourced |
| `system` | `owner` | who may change it: `kernel-only`, `desk-local` or `book-local` | decisions.md:287; :610 (E9) | PROPOSED |
| `code` | `repo` | the repository its face 08 file links point into | workflow-loop.003.md:68-77 | PROPOSED |
| `workflow` | `role` C | the band's role: `build`, `dev`, `jobs` or `colab` | workflow-loop.003.md:38-50 | sourced |
| `workflow` | `set` C | the cross-band set key `CC.title` | R18 | sourced |
| `workflow` | `approval` C | the approval record of the current N4 revision | workflow-loop.003.md:86 (S01) | PROPOSED |
| `band` | `role` | the workflow role this band adopts by name | workflow-loop.003.md:38 | sourced |
| `band` | `default-type` | the type for band pages with none in the stamp | decisions.md:289 | sourced |
| `band` | `lead` | default lead letters for work in the band | Axioms.md:17 (axiom 3); workflow-loop.003.md:107 | sourced |
| `band` | `contents` C | the band's pages | seqAddr.md:241; decisions.md:301 | sourced |
| `band` | `continues` C | the band's continuation `PP99`, if any | seqAddr.md 7.1; decisions.md A5.1 | sourced |
| `pointer` | `kind` | `contents`, `dictionary`, `concordance` or `continuation` | decisions.md:292 (open) | PROPOSED |
| `pointer` | `index` | the face that holds the index (dictionary: `03`) | brands.md:15; decisions.md:424 (C8.3) | sourced |
| `pointer` | `layout` | the fixed layout it follows (dictionary: `kernel`) | brands.md:82 | sourced |

### Workflow `role`

The role comes from the band digit: `N3` build, `N4` dev, `N5` jobs, `N7` colab (workflow-loop.003.md section 2).

### Workflow `set`

R18: pages across bands are matched by `CC` plus title. `N403.ide-design` matches `N503.ide-design`.

So `set:` is `03.ide-design` for both. The compute derives it from the address.

### Workflow `approval`

S01 needs an approval record for the current N4 revision (workflow-loop.003.md:86).

Its shape is not settled. `7` (F6).

### 3.3 Fields on special pages

Page 0000 and pages 0001-0009 have no named type. They get their own fields here.

**Page 0000 (the door, face 00 only, R10):**

| field | meaning | source | status |
|---|---|---|---|
| `level` C | `kernel`, `desk`, `shelf` or `book`, from the address | seqAddr.md 1.4-1.5 | sourced |
| `parent` | back-link to the pointer that names this container | decisions.md:230 (A5.3); R10 | PROPOSED |
| `continues` C | the book's continuation `9999`, if any | decisions.md A4.6, A5.1 | sourced |

`parent` is needed because page 0000 may not have a face 08 (R10), so the back-link must sit in face 00.

**Pages 0001-0009 (overrides, R7):**

R7 says an override must state what it changes, why it is there, why it is needed, and what it should achieve.

| field | meaning | source | status |
|---|---|---|---|
| `changes` | what it changes: a face, a behavior (0020-0049) or a structure (0050-0099) | R7 | PROPOSED name |
| `why-here` | why it is there | R7 | PROPOSED name |
| `why-needed` | why it is needed | R7 | PROPOSED name |
| `achieves` | what it should achieve | R7 | PROPOSED name |
| `authorized-by` | who authorized it | decisions.md:582 (E6) | PROPOSED |

Whether these four sit in face 00 or in a face 01 card is `7` (F8).

---

## 4. Worked examples

All five are in `docs/spec/examples/face00/`. Their book is `docs/spec/examples/sources/10.11.40.book`. Each passes `seqpage check` with no findings.

A real-book example, exported by the CLI from `books/10.11.21.book` (page 10.11.21.1001 bob, with face 01 and 05.01/05.02 seated), is in `docs/spec/examples/real/`. It passes `seqpage check` with no errors but 3 findings (QUESTIONS Q31, Q34, Q38); see that folder's README. (FOLLOWUPS, 2026-11-11)

Below is only the face 00 section of each .seq file.

`:=` lines are worked out by the compute. `|` lines are the stored face 00 text.

### 4.1 A general page, still a draft

Page 1001 `cats`. The user has not confirmed the meaning yet, so it says why it is a draft (R5).

```
seqpage 1
= 00 registry 10.11.40.1001.00
title := cats
state := draft
registry := draft
why-draft := a new page starts as a draft (drafting.md)
faces := 01 draft
type := general
axioms := -
lineage := 10.11.40.1001 < 10.11.40 < 10.11.00 < 10.00.00 < 00.00.00
source := book 10.11.40 @9

--- @9 put 10.11.40.1001.00.draft
at: 2026-11-11T21:09:00Z
by: user
reason: a new page starts as a draft (drafting.md)
| ---
| address: 10.11.40.1001
| title: cats
| type: general
| state: draft
| why-draft: a new page starts as a draft; the user has not confirmed the meaning yet
| ---
|
| ## Registry
| faces: 01 draft
| why-01: the user has not confirmed this meaning yet
```

### 4.2 A dictionary page (pointer)

Page 0012. Its index is face 03 and it follows the kernel layout (brands.md:15, :82).

```
seqpage 1
= 00 registry 10.11.40.0012.00
title := dictionary
state := live
registry := seated
faces := 03 counted
type := pointer
axioms := -
lineage := 10.11.40.0012 < 10.11.40 < 10.11.00 < 10.00.00 < 00.00.00
source := book 10.11.40 @2

--- @2 put 10.11.40.0012.00
at: 2026-11-11T21:02:00Z
by: user
| ---
| address: 10.11.40.0012
| title: dictionary
| type: pointer
| state: live
| ---
|
| ## Registry
| faces: 03 counted
| kind: dictionary
| index: 03
| layout: kernel
```

Note: R16 calls the dictionary's `03.00` a "door". R9 removes face sentinels. That tension is `7` (F4).

### 4.3 A band head

Page 0400, the dev band (R13).

```
seqpage 1
= 00 registry 10.11.40.0400.00
title := dev
state := live
registry := seated
faces := 04 seated
type := band
axioms := 2.6
lineage := 10.11.40.0400 < 10.11.40 < 10.11.00 < 10.00.00 < 00.00.00
source := book 10.11.40 @4

--- @4 put 10.11.40.0400.00
at: 2026-11-11T21:04:00Z
by: user
| ---
| address: 10.11.40.0400
| title: dev
| type: band
| state: live
| axioms: 2.6
| ---
|
| ## Registry
| faces: 04 seated
| role: dev
| default-type: workflow
| lead: 3MP
```

### 4.4 A workflow page in band N4 (R18)

Page 0403 `ide-design`. Its set is `03.ide-design`. A jobs page `0503.ide-design` would share it.

The approval record is `7`: not settled yet.

```
seqpage 1
= 00 registry 10.11.40.0403.00
title := ide-design
state := live
registry := seated
faces := 04 seated, 05 counted
type := workflow
axioms := 1.4.5
lineage := 10.11.40.0403 < 10.11.40 < 10.11.00 < 10.00.00 < 00.00.00
source := book 10.11.40 @6

--- @6 put 10.11.40.0403.00
at: 2026-11-11T21:06:00Z
by: compute
| ---
| address: 10.11.40.0403
| title: ide-design
| type: workflow
| state: live
| axioms: 1.4.5
| lineage: 10.11.40.0403 < 10.11.40 < 10.11.00 < 10.00.00 < 00.00.00
| ---
|
| ## Registry
| faces: 04 seated, 05 counted
| role: dev
| set: 03.ide-design
| approval: 7
```

### 4.5 The door page 0000

Only face 00 (R10). The title is the book's title, not the page's (section 1).

```
seqpage 1
= 00 registry 10.11.40.0000.00
title := workshop
state := live
registry := seated
faces := -
type := -
axioms := -
lineage := 10.11.40.0000 < 10.11.40 < 10.11.00 < 10.00.00 < 00.00.00
kind := book door (R10: face 00 only)
source := book 10.11.40 @1

--- @1 put 10.11.40.0000.00
at: 2026-11-11T21:01:00Z
by: user
| ---
| address: 10.11.40.0000
| title: workshop
| state: live
| ---
|
| ## Registry
| faces: -
| level: book
```

---

## 5. What the checker does

`crates/seqpage` reads face 00 from the newest face 00 entry.

Every check is a **finding**. None refuses the file. So real books always open.

Findings:

- no stamp address, title (page 0000 and 1000+) or state;
- stamp address not the page's address (elevated, A3.2);
- a type not in section 2;
- a state that is not live, draft or retired;
- stamp state disagrees with the entries (axiom 8);
- a draft with no `why-draft` (R5);
- a stamp field not in section 1;
- `lineage` not matching the compute;
- no `## Registry` card (R19);
- a registry field not allowed for the type;
- a compute-only field not matching the compute.

Which findings should become hard errors is `7` (F3).

---

## 6. Open questions

- **F1** Page 0000 title: is the stamp `title:` the container's title (decisions.md:132), with no title in the address (v2:104)? This draft says yes.
- **F2** `faces:` written or derived? R10 vs decisions.md:301 and A5.4. This draft says the compute writes it and checks it.
- **F3** Which face 00 findings become hard errors, and when (after KERNEL migrates its books)?
- **F4** R16 dictionary `03.00` "door" vs R9 no face sentinels.
- **F5** Lineage form: the inheritance chain, or the E6 authorization trail, or both?
- **F6** The shape of the S01 approval record on workflow pages.
- **F7** `system` owner values: are E9's owner classes the right list?
- **F8** Override pages: do R7's four statements sit in face 00 or in a face 01 card? And what type is an override page?
- **F9** Exact layout of face 00 (front matter + `## Registry`), to match KERNEL's 0054.
- **F10** Types for page 0000, continuation pages, and the common questions list (R11).
- **F11** What `code` means beyond "a page whose faces describe code".
- **F12** The core OpRequest has no `reason` field, so a proposal cannot carry a why-draft reason yet (CORE).
