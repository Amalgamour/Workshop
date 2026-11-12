# The axioms' exact address (QD09) — working path

**WORKING PATH.** This is Tester's recommended option, recorded by Prima
on 2026-11-11 at about 7:35 PM EST for the Director to review. It is
**not a ruling** and **not settled law**. Prima will use it as the
working path until Matthew rules. Nothing has been renamed.

Question: [QD09](QUESTIONS-FOR-DIRECTOR.md) — What is the exact address
of the axioms?
Source: Tester, 2026-11-11 evening. Related: R6, CONFLICTS D3, kernel
Q28, axiom 6 and 8, the QD02 working path (`axioms` type).

---

## The idea, in one line

The exact address is `00.axioms`, as Matthew said: desk 00, titled
axioms. This is Option A (a form with numbers plus a title). Faces and
counters attach after the title, as they already do in spirit:
`00.axioms.05.02`.

---

## Why this form

A director's earlier draft already had this shape: "DD.title after a
dot that is not the next axis is a desk title," so `00.axioms` reads
as desk 00 titled axioms (CONFLICTS D3). That is "on the desk" and
"outside of the book" (R6), with no page number and no place inside
`00.00.00`.

The stored working address `00.00.axioms` was a guess in the R6 read
("the desk's 00 spot"). It parses as shelf `00.00` titled axioms, not
as a thing on the desk. Shelf 00 is "never an ordinary shelf"
(decisions.md:173), which is extra machinery we do not need if we
take his words straight.

**Recommended:** use `00.axioms`, and keep `00.00.axioms` as a
findable prior name during the move so the line is not broken (axiom
6 and 8). Do not silently rewrite the old address.

---

## Why not the other options

Why not Option B (a short name for a fixed page in the kernel book):
R6 says the axioms are not a page inside a book, and not page 0050.
An alias into `00.00.00` would put them back where they were taken
from (D145, superseded).

Keep `00.00.axioms` as the exact address, and treat `00.axioms` as
short form: that is what the R6 read already did. It still needs a
new grammar, it still does not match his words, and it still looks
like a titled shelf.

Give them a numeric desk-book id in the ordinary `DD.SS.BB` pattern:
he used a title, not a number.

---

## The grammar and storage (not yet changed)

After a desk (or a container with no page), a title may name
desk-level work that is not a page in a book. Axiom chains stay only
in the `axioms:` field; the title `axioms` is a word, not a one-digit
axiom mark. The core today rejects `00.00.axioms` as "not a face
address"; on this path it would accept `00.axioms` and its faces.

Storage is already its own file (`books/00.00.axioms.jsonl`, folder
`kernel/00.00.axioms/`); those names would follow the address. The
QD02 working path's `axioms` type still fits.

This unblocks the 7 held axiom faces, CONFLICTS D3, Q28, and the
core and builder special case (`build.mjs` `AXIOMS = '00.00.axioms'`,
still marked 7). None of those have been renamed or recoded.

For Matthew, one idea: the axioms live at `00.axioms` — desk 00,
titled axioms — just as you said. They are not a page inside the
kernel book. The current `00.00.axioms` was a working guess; we
should use your form, and keep a link from the old name so the line
is not broken.

---

## Status

Working path, pending Director review. Not a ruling. Recorded in
[DECISIONS-LOG.md](DECISIONS-LOG.md) as D332, and on QD09 in
[QUESTIONS-FOR-DIRECTOR.md](QUESTIONS-FOR-DIRECTOR.md). Kernel files
were not edited. Nothing was renamed.
