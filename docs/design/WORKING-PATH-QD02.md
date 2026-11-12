# Page types (QD02) — working path

**WORKING PATH.** This is Tester's recommended option, recorded by Prima
on 2026-11-11 at about 7:15 PM EST for the Director to review. It is
**not a ruling** and **not settled law**. Prima will use it as the
working path until Matthew rules.

Question: [QD02](QUESTIONS-FOR-DIRECTOR.md) — Which page types are there?
Source: Tester, 2026-11-11 evening. Related: R19, R1, R6, R7, R10, R11, R25;
kernel Q33; face00.md F10; OPEN O35.

---

## The idea, in one line

A type names the laws a page lives under. Add a new type only when those
laws are different. When pages share the same laws and only differ in
details, use a registry field (`kind`) — the way `pointer` already does.

---

## The recommended list

The kernel already has six types: `system`, `general`, `code`,
`workflow`, `band`, and `pointer`. Tester's recommendation is a hybrid:
not "add a type for every missing name" (pure A), and not "keep only
those six and put every role in a field" (pure B).

- **Add `door`** for page 0000. A door may hold only face 00 (R10), is
  not seated the same way (R25), and is the container's identity. Today
  every door is stamped `type: system`, and that value has no given
  meaning (MAP hole 4; the door's own why-draft says so). `system`
  cannot carry "only face 00" without special-casing the page number.
- **Add `override`** for pages 0001-0009. An override must state what it
  changes, why it is there, why it is needed, and what it should achieve
  (R7), and it must not silently replace a face. Those are different
  laws and different registry fields. This picks a type only. It does
  not decide Q24 / face00 F8: whether those four statements sit in face
  00 or on a content card.
- **Add `axioms`** for the axioms. Matthew said they sit outside the
  book, at desk level (R6), not as a book page. `system` means a kernel
  or structural page inside a book. A type lets the computer attach the
  right rules. This does not decide the exact address — that is QD09.
  Tester called this the softer of the three adds: if we want the
  shortest list, axioms could stay `system` until QD09 is settled.
  Tester still prefers a type, because the address is already unusual
  and `system` is what left the stamp meaningless.
- **Do not add a type** for the common questions page yet (R11; there
  is a sample at `10.11.21.0013`). We do not yet have unique face or
  range laws for it. Keep it as `system` with a registry field such as
  `kind: questions` until those rules are known.
- **Continuation pages** (`99`, `9999`, `PP99`) should use the existing
  `pointer` type with `kind: continuation` (already proposed in
  face00.md). A continuation is a pointer: it says where to look next.
  No new type. This is also Tester's working answer to the leftover in
  C1.4 / O35.

---

## Why not the pure options

Why not pure A (add a type for every missing name): the list would keep
growing, and we would invent types where `kind` already works. Axiom 2:
do not reinvent what already exists; write only the difference.

Why not pure B (keep the six and put the role in a field): then
`system` has to mean door, axioms, questions, and ordinary kernel
pages, and the special rules would attach to page numbers — which is
what face00.md section 3.3 does now. But C1.4 said page number alone is
not enough to say what a page is for. A type is "a property that rules
attach to" (required faces, ranges, who may write). A field on
`system` cannot forbid content faces on a door without special-casing
0000 by number.

---

## Other options Tester considered

1. The hybrid above (recommended).
2. One new type `reserved` with `kind: door` or `override`. Tester
   considered this and does not recommend it. Door and override have
   opposite face laws (door: only face 00; override: content faces and
   four statements). Bundling them repeats "system means everything."
3. Derive the type from the address for reserved pages (0000 is always
   a door; 0001-0009 are always overrides) and only stamp a type on
   working pages. The computer should check that address and type
   agree — a mismatch is a finding. But the type should still be
   written in the stamp: R19 puts it there, and a reader should see it.

---

## A naming caution

"Door" here is the page-0000 type, which matches Matthew's word (R1,
R10). It is not face 00 on an ordinary page. That face 00 is the
registry, on every page.

---

## What this unblocks, and what it does not

This unblocks a meaningful `type:` on the held face 00s (QD02 said 17),
and the per-type registry fields R19 asked for. The face 00 checker can
validate field sets by type and can drop "special fields by page
number." Door and override rules (R10, R7, R25) have a place to attach.

It does not answer QD09, Q42, or QD66/QD67. It does not decide Q24 /
face00 F8.

---

## Status

Working path, pending Director review. Not a ruling. Recorded in
[DECISIONS-LOG.md](DECISIONS-LOG.md) as D319, and on QD02 in
[QUESTIONS-FOR-DIRECTOR.md](QUESTIONS-FOR-DIRECTOR.md).
