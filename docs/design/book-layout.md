# How the four-section cut would appear on Book Layout (Q30 / D327)

**DRAFT.** This is a draft for the Director to read. It is not settled law.
Anything marked PROPOSED is a builder's proposal. Anything marked `7` is open.

Lane: DESIGN (Designer). This shows how the Q30 working path
([WORKING-PATH-Q30.md](WORKING-PATH-Q30.md), D327) would appear on the
0051 Book Layout card. That path is not a ruling. This file is not a
second law. Q30 stays open.

Kernel files were not edited, including `0051.01` and `0051.04` (both
are still drafts; the Q30 hold stays). The seqAddr table was not
edited. WORKING-PATH-Q30.md was not rewritten. QD67 was not touched.

Related: R17, R7, R10, R21, R25; QD13; CONFLICTS D13; seqAddr.md
section 6; decisions.md A2.7; 0051.05.02 w03 (write the four sections
into Book Layout, blocked by Q30).

---

## 0. What the card shows today

The 0051 Book Layout card (01 and 04) and the seqAddr table list
**five** rows below 0100:

- `0000` -- door
- `0001-0009` -- overrides (R7; none while the app is built, R21)
- `0010-0019` -- required pages
- `0020-0049` -- behavior
- `0050-0099` -- structure

Then three rows above 0100, which are not part of this cut:
`0100-0999` bands, `1000-9998` user space, `9999` continuation.

The 01 card already quotes R17 and says the exact four-way split is
`7`. The 04 card has `why: 4.7` and no R17 line. The Finding card on
the same page already says "0020-0099 are working pages (R17)"; that
card does not need a change for this cut.

---

## 1. PROPOSED: four section rows, kinds inside the fourth

On this path the five rows below 0100 become four sections, each
with its own laws. "0000-0019 are static" is a property of the first
three sections together, not a fifth way to cut the table. Behavior
and structure are two kinds inside the working-pages section, not
two extra sections. [D327]

The rows above 0100 stay as they are.

The 01 card (for builders) and the 04 card (for a person) must agree
on the four sections and the two kinds (C3.2). The 04 card may say
more, in plain words.

Until Matthew rules, the kernel cards stay as they are (the Q30 hold
stays). The proposed text below is for 0051.05.02 w03, after a
ruling, written through drafting (copy, note, merge). It is not
written into the kernel here.

---

## 2. PROPOSED: the 01 Book Layout card

Plain law. Four section rows, then the unchanged rows above 0100.

```
## Book Layout

The kernel is the template for `0000-0999` in every book, including
what each band digit means there.

Four sections below 0100, each with its own laws. The first three
together are static. Working pages are not just locations (R17).

| Section | Range | What it is |
|---|---|---|
| 1 | `0000` | the door (the book's identity; only face 00, R10 and R25) |
| 2 | `0001-0009` | overrides (R7); none while the Workshop app is built (R21) |
| 3 | `0010-0019` | required static pages (contents, dictionary, concordance, and the common questions sample at 0013) |
| 4 | `0020-0099` | working pages, not just locations. Two kinds, not two extra sections: `0020-0049` behavior (localized; exists locally or is inherited); `0050-0099` structure (mostly in the kernel or templates). R7 still uses those two ranges as override targets. |

Rows above 0100 are not part of this cut:

| Range | What it is |
|---|---|
| `0100-0999` | standard bands modelled by the kernel (`0100` ... `0900`) |
| `1000-9998` | user space; users design their own bands (`1000` ... `9800`) |
| `9999` | continuation (sentinel) |

`1000` is the head of the first user band, which is why the first
open page is `1001`.

R17 (DIRECTOR-RULINGS.md:68): "Its broken into 4 sections. Each one
has it's own important. 0000-0019 are static 0020-0099 aren't just
locations."
```

The last line of today's 01 card ("The exact four-way split is `7`")
drops once this is ruled. Until then, if this text is used only as a
proposed merge, that `7` line may stay.

---

## 3. PROPOSED: the 04 Book Layout card

The same four sections, said for a person. The `why:` would cite R17
instead of `4.7`.

```
## Book Layout
source: [01 / Book Layout] decisions.md:115-125; 04 text: seqAddr.md
  section 6; DIRECTOR-RULINGS.md R17 (:68), R7 (:31), R21 (:82-84)
why: R17 (DIRECTOR-RULINGS.md:68) splits the book below 0100 into
  four sections; 0000-0019 are static, and 0020-0099 are working
  pages, not just locations.

The kernel is the template for `0000-0999` in every book.

Below page 0100 there are four sections, each with its own laws.

The first three together are static (R17 "0000-0019 are static"):

- `0000` is the door: the book's identity. It holds only face 00
  (R10, R25).
- `0001-0009` are overrides. An override is its own page. It must
  state what it changes, why it is there, why it is needed, and
  what it should achieve (R7). A door and an override have opposite
  laws, so they are not one section. None of these pages are used
  while the Workshop app is built; changes are built into the pages
  (R21).
- `0010-0019` are required static pages: contents, dictionary,
  concordance, and the common questions sample at 0013.

The fourth section is working pages, "not just locations" (R17):

- The section is one range, `0020-0099`.
- Inside it are two kinds, not two extra sections: `0020-0049`
  behavior (localized; exists locally or is inherited), and
  `0050-0099` structure (mostly in the kernel or templates).
- R7 still uses those two ranges as the targets an override may
  point at.

The table on the 01 card is the same cut. Rows above 0100 (bands,
user space, continuation) are not part of this cut and stay as they
are.

A page in `0001-0009` that exists in a book is a local override of
the inherited environment (R7). None are used while the Workshop
app is built; changes are built into the pages (R21).
```

---

## 4. Note only: a matching change to the seqAddr table

This section is a note. `docs/spec/seqAddr.md` was not edited.

Section 6 ("Book page layout") should match the same four-section
cut: four rows below 0100, with behavior and structure named as
kinds inside `0020-0099`, and the three rows above 0100 unchanged.
The dictionary sentence (`0012`, face 03) can stay under the table.

One leftover in that same section should be corrected at the same
time, because it disagrees with R7 and with the 0051 cards already:
seqAddr.md today says "A page in `0001-0099` that exists in a book
is a local override of the inherited environment." Only `0001-0009`
are override pages (R7). The 04 card already uses `0001-0009`. The
matching seqAddr sentence should too.

`decisions.md` A2.7 is older still: one row `0001-0099`. That is
already CONFLICTS D13. This draft does not rewrite `decisions.md`.

---

## 5. What this is not

- Not a rewrite of 0051.01, 0051.04, seqAddr.md, or
  WORKING-PATH-Q30.md. The Q30 hold on 0051 stays.
- Not a decision on Q30 for the Director. It only shows how the
  working path would appear. Prima takes Q30 / QD13 to the Director.
- Not a change to R21 or to R7's two target ranges.
- Not a change to the Finding card (already aligned) or to rows
  above 0100. QD67 stays for Matthew and is not touched here.

---

## 6. Status

Still a draft, still `7`, not law. Aligns with D327. Q30 stays open.
