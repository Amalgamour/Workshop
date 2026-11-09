# seqAddr Design Review

Reviewed: `seqAddr.md` (2026-11-09). `seqAddr.001.md` is treated as the earlier draft.

## Verdict

The **address layer** is close to ready. The hierarchy (desk, shelf, book, page, face), fixed widths, sentinels and the counter/tail lifecycle form a coherent model. About six ambiguities need decisions, and then a grammar and validator can be built.

The **file format** is not ready. The spec says what each face is *for*. It does not yet say what a page file *looks like on disk*. That has to be designed before anything can read or write pages.

Suggested build order:

1. Address grammar + parser/validator (after the decisions in section A)
2. On-disk page format (section B)
3. Face rules and cross-face card linking (section C)
4. Task lifecycle / workflow state machine (section D)

---

## A. Address layer: decisions needed

### A1. Short forms are ambiguous without a context rule
`05.03` could be desk 05 / shelf 03, or face 05 / counter 03. `05.draft` could be a desk titled "draft" or face 05 in draft. Only the 4-digit page axis is unambiguous by width.

Proposal: an address is **absolute** if it starts at DD, and **page-relative** if it starts at PPPP. Anything shorter than that (`FF`, `FF.NN`, `BB.PPPP...`) is only legal *inside* a page or book and resolves against it, like a relative path. Canonical (stored) form is always the full address.

### A2. Titles and tails collide
The title rule says the first non-digit segment ends the address. Tails (`draft`, `pack`, `open`, `return`, `review`, `retired`) are also non-digit segments.

Proposal: position decides. A non-digit after DD/SS/BB/PPPP is a title. A non-digit after FF or NN is a tail. Faces never have titles, so this is unambiguous for full addresses. Also define:
- Allowed title characters (suggest `[a-z0-9-]`, must start with a letter, no dots)
- Whether titles are case-sensitive
- Whether a title is part of identity or only a label. Recommend label only, so `10.11.21` and `10.11.21.anything` resolve to the same book.

### A3. Where is a title stored?
`DD.SS.BB.title` names a book, but page `0000` (the book's sentinel) allows no title. Say where the book's title lives. The likely answer is in page 0000's stamp.

### A4. The 00 sentinel has two meanings
`DD.00` is the desk sentinel. `DD.00.BB` is a "desk book", meaning a book directly under the desk. Both work if 00 is defined once as **"the owner of the previous axis itself"**:
- `DD.00` is the desk's own space
- `DD.00.BB` is a book owned by the desk
- `DD.SS.00` is the shelf's own space
- `DD.SS.BB.0000` is the book's own page

State this as one rule rather than case by case. Also define 00/99 for the **face** and **counter** axes. Counters are 01-98, so are `FF.00` and `FF.99` reserved?

### A5. The 99 sentinel means different things per axis
- Page 9999: continuation into another book
- `DD.99`: child desk
- Shelf `.99`: child (a child of what kind?)

How is a child desk addressed? If it gets its own global DD, the whole system has only 98 desks, so the nesting isn't really in the address. Decide whether 99 is always "link to continuation/child" with the target recorded on that sentinel's face 08.

### A6. Capacity and exhaustion
Counters climb 01-98 and face 06 uses one counter per session. So a page gets 98 sessions of notes and 98 tasks, ever. Define what happens at 98. One option mirrors page 9999: `FF.99` points to a continuation.

Also: is the namespace global, or one per repository/root? Where does the **kernel** sit? It is referenced but has no address yet (`00`?).

---

## B. On-disk format: not yet specified

These need answers before any code can store a page:

- **File vs faces.** Is a page one file with faces as sections, or a directory with one file per face? Tails and counters change over time (`05.03.pack` becomes `05.03.open`), which suggests faces need to be individually addressable and maybe separate files.
- **File naming and layout.** For example, are desks, shelves and books directories, with pages named `0001.title.<ext>`? Which extension?
- **Body syntax.** Markdown with frontmatter is the obvious fit for both people and models. Confirm it.
- **Stamp.** List its fields: full address, face number, title, created/updated, model/author, authority source. The spec says it is required but doesn't define it.
- **Contents list.** Generated from cards, or written by hand? Generated avoids drift.
- **Cards.** Give the syntax (for example a `##` heading = card title), the uniqueness scope (per face? per page?) and the matching rule across faces (exact string or normalized slug).

---

## C. Faces: gaps

- **Required faces.** Which faces must a page have? The spec implies a user page may have only 04, and page 0000 has which?
- **Faces 09-98.** Unassigned. Reserved? Free for custom use?
- **Face 03 "reserved fields".** Not defined.
- **Face 04 mirroring 01/02.** Every 01/02 card must appear on 04. Who keeps them in sync? Is drift a validation error? (Typo: "a while piece" probably means "a why piece".)
- **Face 08 map.** Is it written by hand, or derived from the addresses referenced in other faces? If it is written by hand it will drift. Are links bidirectional, and is the back-link required?
- **Authority.** Desk is "highest controlling", face 03 "states where authority comes from", and child desks sit "under authority". There is no precedence rule yet. When desk law (face 01) and book law conflict, which wins? Can a lower level override, or only narrow?

---

## D. Task lifecycle (face 05): the workflow core

The lifecycle is `draft -> pack -> open -> return -> review -> closed (bare)`.

- **Identity vs state.** If the tail is part of the address, the address changes every time the task changes state, and links to it break. Recommend: `FF.NN` is the identity, and the tail is state. References use `FF.NN` and resolve to whichever tail currently exists. Only one tail per `FF.NN` may exist at a time.
- **Failure paths.** What happens if review rejects the work? Does it go back to `open`, or is a new counter created? What about a worker that dies while `open`?
- **Claiming.** Two agents should not both take the same `pack`. Is the `pack -> open` rename the lock? On a filesystem, an atomic rename works as a claim.
- **Seated faces.** For `FF.draft` and `FF.retired`: can a seated `FF` and an `FF.draft` coexist? What makes a draft seated, and what happens to the old seated face? Spell out the promotion step.
- Notation: the spec uses both `NN` and `MM` for the counter. Pick one.

---

## E. Project-level notes

- `AGENTS.md` says the app has **no persistence**, but seqAddr is a storage format. Is the Next.js app meant to read and write these files (local folder, browser File System Access API, git)? Or does it only edit in memory and export? This decides the app's architecture.
- `Axioms.md` is empty. It would be a good place for the invariants this review keeps asking for: one rule per line, each one testable by the validator.
- Typo: `10.11.21.tile` should be `.title`.

---

## Draft grammar (pending section A decisions)

```
address    = absolute | page_rel
absolute   = desk [ "." shelf [ "." book [ "." page [ "." face_part ] ] ] ] [ "." title ]
page_rel   = page [ "." face_part ] [ "." title ]
face_part  = face [ "." counter ] [ "." tail ]

desk       = 2DIGIT          ; 00 kernel?, 99 sentinel
shelf      = 2DIGIT          ; 00 = desk's own space
book       = 2DIGIT          ; 00 = shelf's own space
page       = 4DIGIT          ; 0000 book sentinel, 9999 continuation
face       = 2DIGIT          ; 01-08 defined, 07 reserved
counter    = 2DIGIT          ; 01-98
tail       = "draft" | "pack" | "open" | "return" | "review" | "retired"
title      = ALPHA *( ALPHA / DIGIT / "-" )   ; never after face_part
```

Validation rules this grammar does not capture yet:
- `title` is not allowed together with `face_part`, or on page 0000
- `retired` is valid only without a counter; `pack|open|return|review` only with one; `draft` with or without
- Each container must have its `00` sentinel to be legal
