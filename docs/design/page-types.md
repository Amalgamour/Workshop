# Page types (QD02)

**DRAFT.** This is a draft for the Director to read. It is not settled law.
Anything marked PROPOSED is a builder's proposal. Anything marked `7` is open.

Lane: DESIGN (Designer). Related: R19, R1, R6, R7, R10, R11, R21, R25;
kernel Q33; face00.md (F10 and the field sets); OPEN O35; D37, D152, D156;
C1.4 (decisions.md:282-292).

This file sits next to Tester's working path,
[WORKING-PATH-QD02.md](WORKING-PATH-QD02.md) (D319). That path is already the
working path Prima will use until Matthew rules. It is not a ruling, and this
file is not a second law. Designer agrees with it, and adds how the field
sets attach, how existing stamps change, and one small correction about the
common questions page.

A shorter related sketch, for the leftover part of QD01, is in
[notes-and-dictionary-seating.md](notes-and-dictionary-seating.md).

---

## 0. What is already decided

A page type is a property that rules attach to. It lives in the stamp on
face 00. [C1.4] [R19] [D37] [D152]

Page number alone is not enough to say what a page is for. [C1.4]

The starting types are six: `system`, `general`, `code`, `workflow`, `band`,
`pointer`. [C1.4] [seqAddr.md:192] [kernel 0054.01]

They are defined in the kernel, as kernel-only cards. [C1.4]

The default is: the stamp's type, else the band head's default, else
`general`. [C1.4] [seqAddr.md:194]

Changing a type goes through drafting and review, like any other change.
[C1.4]

Each page type can have its own registry fields. [R19]

`face00.md` already drafts those field sets. That file is itself a draft,
not law. [face00.md:191-254] [D156]

A type not in the six is a finding, not an error. The page is still read.
[face00.md:146]

---

## 1. The working path this draft agrees with

Tester's recommended rule: a type names the laws a page lives under. Add a
new type only when those laws are different. When pages share the same laws
and only differ in details, use a registry field (`kind`) -- the way
`pointer` already does. [WORKING-PATH-QD02.md] [D319]

The recommended list, which this draft also recommends:

- **Add `door`** for page 0000. A door may hold only face 00 [R10], is not
  seated the same way [R25], and is the container's identity. Today every
  door is stamped `type: system`, and that stamp has no given meaning
  (MAP hole 4; the door's own why-draft says so).
- **Add `override`** for pages 0001-0009. An override must state what it
  changes, why it is there, why it is needed, and what it should achieve
  [R7], and it must not silently replace a face. Those are different laws,
  and opposite face laws from a door (content faces, versus only face 00).
  This picks a type only. It does not decide where the four statements sit
  (Q24 / face00 F8). These pages are not built during this build [R21].
- **Add `axioms`** for the axioms. They sit outside the book, at desk level
  [R6], not as a book page. A type lets the computer attach the right
  rules. This does not decide the exact address -- that is QD09. Tester
  called this the softer of the three adds: axioms could stay `system`
  until QD09 is settled. Designer agrees a type is cleaner, and records
  that softer option as well.
- **Do not add a type** for the common questions page yet [R11]. We do not
  yet have unique face or range laws for it. See section 5 for a small
  correction: the sample is already `general`, not `system`.
- **Continuation pages** (`99`, `9999`, `PP99`) use the existing `pointer`
  type with `kind: continuation` (already proposed in face00.md). A
  continuation is a pointer: it says where to look next. No new type.
  This is also the recommended answer to O35.

Why not pure A (a new type for every missing name): the list would keep
growing, and we would invent types where `kind` already works. [axiom 2]

Why not pure B (keep only the six, and put every role in a field): then
`system` has to mean door, axioms, questions, and ordinary kernel pages,
and the special rules would attach to page numbers -- which is what
`face00.md` section 3.3 does now. That is what C1.4 said is not enough. A
field on `system` cannot forbid content faces on a door without
special-casing 0000 by number.

Designer first considered that "address is enough" path (section 3.3 of
face00.md), because the kernel already writes `system` on those pages.
C1.4, and the different laws above, are why that path is set aside. The
field sets in face00.md stay useful. They attach to the new types, instead
of to a page number. If the Director later prefers pure B, those same
field sets can sit on `system` by address. That would be a new step.
[axiom 6]

---

## 2. PROPOSED: how the field sets attach

This draft does not invent new fields. It points at the sets already
drafted in `docs/spec/face00.md` sections 3.2 and 3.3, and treats them as
PROPOSED, as that file does. [D156]

The change of attachment, proposed here:

- Type `door` carries the door fields already drafted: `level` (kernel,
  desk, shelf, or book), `parent` (back-link), `continues` (the book's
  `9999`, if any). [face00.md:232-240]
- Type `override` carries the R7 fields already drafted: `changes`,
  `why-here`, `why-needed`, `achieves`, and `authorized-by`.
  [face00.md:242-254] Whether those four statements sit in face 00 or on
  a face 01 card remains `7` (face00.md F8).
- Type `axioms` can use the `system` field set (`owner`) until QD09 is
  settled, or a shorter axioms-only set if SEQPAGE later drafts one. This
  file does not invent that set.
- Type `pointer` already has `kind`. Add `continuation` to the kind list,
  as face00.md already proposes. [face00.md:208] [decisions.md:292]
- The other six-type field sets stay as in face00.md section 3.2:
  `general` has only the common fields; `system` has `owner` (the exact
  owner list is QD32); `code` has `repo` (what "code" means is QD33);
  `workflow` has `role`, `set`, `approval` (the shape of `approval` is
  QD31); `band` has `role`, `default-type`, `lead`, `contents`,
  `continues`.

The face 00 checker can then validate field sets by type, and can drop
"special fields by page number." Door and override rules (R10, R7, R25)
have a type to attach to. [WORKING-PATH-QD02.md]

---

## 3. PROPOSED: how existing stamps change

Today, doors, the axioms, kernel structural pages 0051-0057, and the
parked sample override, all say `type: system`. The door's own why-draft
says that value has no given meaning (MAP hole 4).

Changing a type goes through drafting and review, like any other change.
[C1.4] That is a new step in the line. The past stamp is not rewritten
in place as if it had always said `door`. [axiom 6]

Until those drafts are reviewed:

- A page 0000 still stamped `system` is a finding (address and type
  disagree), not a hard error. The page is still read. [face00.md:146]
- The parked override at `10.11.21.0001` stays parked. [R21] If it returns
  later, its type would be `override`, through the same drafting step.
- The axioms at `00.00.axioms` stay `system` until the type is drafted,
  and until QD09 (the address) is settled.
- Ordinary kernel law pages (0051-0057) stay `system`. They are kernel
  structural pages, and that is what `system` already means. [C1.4]

Adding `door`, `override`, and `axioms` to the kernel's type list (page
0054) is a kernel card change. It waits for a ruling, and it belongs to
the KERNEL lane, not this one. This draft does not edit that page, the
builder, or any face.

---

## 4. PROPOSED: one small correction -- the common questions page

Tester's working path said: keep the common questions page as `system`
with `kind: questions`, until unique laws are known. [D319]

The sample at `10.11.21.0013` is already stamped `type: general`.
[kernel/samples/10.11.21/10.11.21.0013.00.draft.md]

**Recommended.** Do not add a new type (agreed). Until unique face or
range laws exist, keep the type already written: `general`. Use
`kind: questions` if a registry field is needed to mark the role. The
special behavior is already the card type `question` (forms, answer),
not a page type. [R11] [QD26]

Whether 0013 is the right page number stays QD27.

This is a small correction to D319's "keep as `system`." It does not
change the rest of the working path.

---

## 5. What builders can do now

Until the Director rules on QD02, treat this as `7`. Prima is already
using D319 as the working path. The recommended shape, so work can move:

- The face 00 checker may allow the six starting types, plus `door`,
  `override`, and `axioms`. It may validate the field sets in section 2
  by type. A `pointer` may have `kind: continuation`.
- A page 0000 still stamped `system` is a finding, not a hard error,
  until its type is drafted to `door`.
- The common questions sample stays `general`. A type not in the allowed
  list stays a finding, not a hard error. [face00.md:146]
- Do not build override pages during this build. [R21]
- Do not rename existing face 00s in this lane, and do not edit the
  kernel type list, until a ruling says to.

This is meant to let the 17 held face 00s and the checker move, without
pretending QD02 is settled.

This draft does not edit `docs/spec/face00.md`, the kernel, or any face.
KERNEL Pass 12 owns the builder. SEQPAGE can update `face00.md` later if
this proposal is taken (field sets move from "by page number" onto the
new types).

---

## 6. Open questions left for Prima

- QD02 itself: this file only proposes. D319 is the working path, not a
  ruling.
- QD27: is page 0013 the right home for the common questions list?
- QD09: what is the exact address of the axioms?
- QD31, QD32, QD33: approval shape, system owner values, and what `code`
  means.
- face00.md F8 / Q24: where the R7 statements sit, when override pages
  return.
- QD13 / Q30: the four sections below 0100 have a Tester working path
  in [WORKING-PATH-Q30.md](WORKING-PATH-Q30.md) (D327). This file does
  not reopen that.
