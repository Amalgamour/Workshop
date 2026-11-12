# How the dictionary menu appears on face 03 (QD10)

**DRAFT.** This is a draft for the Director to read. It is not settled law.
Anything marked PROPOSED is a builder's proposal. Anything marked `7` is open.

Lane: DESIGN (Designer). This fills in how a derived dictionary menu would
appear, given the QD10 working path ([WORKING-PATH-QD10.md](WORKING-PATH-QD10.md),
D333). That path is not a ruling. This file is not a second law.

Related: R9, R16, QD03 (D326), Q35 (D337), C8.6 (decisions.md:445-454),
the kernel card type `menu` (0054.02: entries derived by the compute),
format.md:102, face00.md F4, D339, D340, D351, A4.4
(`crates/seqaddr-core/src/resolve.rs:182`, `state.rs:296`, `state.rs:460`).

The WORKING-PATH files, the kernel, and the core were not edited. No
`0012.03` file and no 00.counter were written.

---

## 0. What is already on the working path

There is no `03.00` file. The dictionary still has a way in: a menu of
its sections. That menu is worked out from the sections that exist
(`03.10`, `03.14`, and so on), not written as a face-00 counter. Faces
still have no sentinels. [D333] [R9] [D339]

The original QD10 path said a card on face 03 may explain this to a
person. D351 changes that address: the explanation does not live at
`PPPP.03`. The list of sections itself is still derived. A
hand-written menu would go stale when a section is added.
[WORKING-PATH-QD10.md] [D351]

This is the same shape as the face list (QD03 / D326) and as boards
(format.md:102): derived, then checked, not stored as a special 00.

The kernel already has a card type `menu` for face 03, whose entries
are "derived by the compute" and are not drafted. [kernel 0054.02]
Derived menus are calculated and never drafted. [kernel 0056.01]
This draft uses that, and does not invent a new card type.

The C8.6 letter ranges stay (`03.01-03.09` reserved, `03.10-03.61`
letters, `03.62-03.98` reserved). The `03.00` and `03.99` rows in
C8.6 and `brands.md` should be dropped on this path. That change has
not been made, and is not made here. [WORKING-PATH-QD10.md]

---

## 1. PROPOSED: face 03 is only the derived menu; an explanation sits nearby

When a person opens the dictionary's face 03, they see one thing: the
derived menu. That menu is not a written file.

**1. The derived menu (required, never written as a file).** This is
a view the computer works out when someone looks. It is not a
`03.00` file, and it is not a hand-written list. It is the `menu`
card type's derived entries. [kernel 0054.02] A person opens
`0012.03` and sees this menu; choosing a row opens that section
(`03.14`). That is the entrance R16 asked for. [D333] [D339] [D351]

The core already uses plain `0012.03` as that derived listing (R9).
A bare put of `0012.03` is refused (A4.4): face 03 is counted, so it
holds counters only, and has no door of its own. That is the same
family as the A4.4 hole on face 00, in the other direction: here 03
is counted, so a bare face file is what the core rejects. If an
explanation were written at `0012.03`, resolve would still return
the derived list, not the card, and a propose of that put would be
rejected. Do not write a `0012.03` file. [D351]

Today the sample dictionary has no `0012.03` file, only `0012.03.14`
and `0012.03.16`. That is fine, and that is the shape the core can
read.

**2. An explanation card (allowed, not required), on face 01 or
face 04.** This is a person-facing card on another content face of
the dictionary page, not on face 03. Its address is `PPPP.01` or
`PPPP.04` (for the sample, `10.11.21.0012.01` or
`10.11.21.0012.04`). Face 01 is a natural home for "what the
dictionary is"; face 04 is also fine. This draft does not require
one over the other. The explanation, if written, is nearby, not at
the same address as the menu. [D351, which sharpens D340]

The card may say what the dictionary is, and may show the fixed C8.6
layout (which letter sits in which section). That layout is a scheme.
It does not go stale when a section is added or seated.

The card must not be the source of truth for which sections exist. If
it copies a live list, and that list disagrees with the files and the
book, that is a finding, not the list to trust. [D326]

The card is ordinary lasting content. It is drafted, and it may be
seated after a trial. It is optional. The menu still appears if no
such card has been written.

The rest of D340 stands: optional, not the source of truth, and the
derived menu still appears without it. Only the address changed.

---

## 2. PROPOSED: what the derived menu shows

The computer works the list out from the section files that exist
and from the book. It lists only sections that exist, in counter
order. Empty letter ranges from C8.6 are not listed (the explanation
card, if written on face 01 or 04, may still show the full scheme).

For each section it shows:

- the counter (`03.14`)
- the C8.6 letter range (`bi-bq`)
- a title, if the section has one (the sample `03.14` is "bob")
- the section's state (draft or seated)

State follows the Q35 working path: a dictionary section may be
seated after a trial. [D337] This draft does not seat anything. The
sample sections stay drafts until that path is ruled or built.

The computer still checks the derived list against the book and
against any `why-03.NN` or `seat-03.NN` lines on face 00. A
mismatch is a finding. [D326]

On today's sample `10.11.21.0012`, the derived menu would show two
rows: `03.14` (bi-bq, bob, draft) and `03.16` (ca-cg, cats, draft).
If a later section `03.49` (sa-sc) were added, it would appear on
the next look, with no edit to a menu file.

---

## 3. How a person gets there

The dictionary page (`0012`, type `pointer`, `kind: dictionary`) is
the book's dictionary. [page-types.md] Opening face 03, a person
sees the derived menu. Choosing a row opens that section (`03.14`,
and so on), whose cards are the word index for that letter range
(`type: index`). [kernel 0054.02] The explanation, if written, is
on face 01 or face 04, nearby. [D351]

There is no door at `03.00` to walk through, and there is no file
at `PPPP.03`. Face 03 is only the list the computer works out. That
is the entrance R16 asked for, without a face sentinel, and it
already works in the core. [D333] [R9] [D351]

---

## 4. What this is not

This draft does not add, remove, or seat any face. It does not write
a `0012.03` file, or a 00.counter. It does not edit the kernel, the
core, `decisions.md` C8.6, or `brands.md`. Those tables still name
`03.00` and `03.99`; dropping those rows is later spec work, already
noted on the working path.

It does not answer QD11 (whether `0012.03` is a task list). This
draft treats dictionary 03 sections as section counters (lasting
content, D337), not as a task list. A bare `0012.03` file is
refused by the core (D351), but QD11 itself stays open. If QD11
later says otherwise, the menu would need another look. QD16
(after 98, now that `03.99` is gone) stays open.

It does not answer QD10 for the Director. It only proposes how the
working path would appear. Prima takes QD10 to the Director.

---

## 5. What builders can do now

Until the Director rules, treat this as `7`. Recommended, so work
can move:

- Do not write a `03.00` file.
- Do not write a `PPPP.03` file (for the sample, do not write
  `0012.03`). Face 03 is only the derived menu. [D351]
- Do not write the live section list by hand.
- A derived menu may be shown from the sections that exist, when
  someone opens face 03.
- An explanation card may be drafted at `PPPP.01` or `PPPP.04`,
  not at `PPPP.03`. It should explain, not list the live sections
  as law. [D351]
- Do not seat dictionary sections until Q35 / D337 is ruled, or
  Prima says to follow that path as a provisional `7`. The builder
  still refuses those seats today.

---

## 6. Status

Still a draft, still `7`, not law. Aligns with D333 and D351 (D339
stands; D340 stands except the address). The WORKING-PATH files were
not rewritten. The kernel and the core were not edited. No `0012.03`
file and no 00.counter were written.
