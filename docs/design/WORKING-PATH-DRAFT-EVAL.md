# Tester evaluation of three Designer drafts — working path

**WORKING PATH.** This is Tester's recommended fill-in of three Designer
drafts, recorded by Prima on 2026-11-11 at about 7:40 PM EST for the
Director to review. It is **not a ruling** and **not settled law**.
Prima will use it as the working path until Matthew rules.

The three drafts stay as Designer wrote them. They were not rewritten
here. The kernel was not edited. All three still sit at `7`.

Source: Tester, 2026-11-11 evening. The drafts are
[dictionary-menu.md](dictionary-menu.md) (D339-D340),
[parked-door-lessons.md](parked-door-lessons.md) (D341-D342), and
[book-layout.md](book-layout.md) (D343). They fill in
[WORKING-PATH-QD10.md](WORKING-PATH-QD10.md) (D333),
[WORKING-PATH-Q42.md](WORKING-PATH-Q42.md) (D338), and
[WORKING-PATH-Q30.md](WORKING-PATH-Q30.md) (D327).

---

## The idea, in one line

Adopt all three drafts as working-path fill-ins, still `7`, still not
law. The one change to make before anyone writes files is this: the
dictionary's optional explanation card does not live at `PPPP.03`.

---

## 1. Dictionary menu (D339-D340) — the address change is D351

Adopt D339 as written. The menu on face 03 is a derived view, never a
`03.00` file, never a hand-written live list. It lists only sections
that exist, with their letter range and state, and is checked against
the book and the why-NN / seat-NN lines. It uses the kernel's existing
`menu` card type (0054.02, 0056.01). Empty ranges stay off the live
list. The C8.6 and brands.md rows for `03.00` and `03.99` stay for
later. QD11 and QD16 stay open.

Adopt D340's other points: an optional explanation is fine, and it
must not be the source of truth for which sections exist. The one
change is the address.

**D351.** The explanation card should not live at `PPPP.03` (for the
sample, not at `10.11.21.0012.03`). Put it on another content face of
the dictionary page: face 01 ("what the dictionary is") or face 04.
Face 03 is only the derived view. A person opens `0012.03` and sees
the menu; choosing a row opens that section (`03.14`). That is the
entrance R16 asked for, and it already works in the core. The
explanation, if written, is nearby, not at the same address as the
menu.

Why: the core already uses plain `0012.03` as the derived menu. On a
counted face, plain FF returns a derived listing of the counters,
never written as an entry. A bare `put` of `0012.03` is refused:
"face 03 is counted: it holds counters only, so write a counter FF.NN;
it has no door of its own (R9)" (A4.4). That is the same family as
the A4.4 hole in the six tests, in the other direction: here 03 is
counted, so a bare face file is what the core rejects. If an
explanation were written at `0012.03`, `resolve 0012.03` would still
return the board, not the card, and `propose` of that put would be
rejected. The sample today has no `0012.03` file, only `03.14` and
`03.16`, which the draft already calls fine — and that is the shape
the core can read.

Prima checked this read-only, and it holds:

- `crates/seqaddr-core/src/resolve.rs:182`: "R9: a counted face has no
  door/board slot; plain `FF` reads a derived listing (7)."
- `crates/seqaddr-core/src/state.rs:296`: "A derived listing of a
  counted face's counters (R9: there is no `FF.00`; never written as
  an entry)."
- `crates/seqaddr-core/src/state.rs:460`: the A4.4 refusal of a bare
  put on a counted face, as quoted above.
- The sample under `kernel/samples/10.11.21/` has
  `10.11.21.0012.03.14.draft.md` and `10.11.21.0012.03.16.draft.md`.
  There is no `10.11.21.0012.03` file (there is a `0012.00.draft` and
  seated `0012.05.01` / `0012.05.02`).

This sharpens D340. The rest of D340 stands. The Designer draft was
not rewritten here.

For Matthew, one idea: the dictionary's way in is already there —
when you open face 03 you see the list of sections the computer
worked out. An explanation can sit on another face, but not at that
same address, because face 03 is counted and has no door of its own.

---

## 2. Parked door lessons (D341-D342) — climb notes are D352

Adopt both drafts as written. Fold once, onto new 05 counters on
0051 and 0052, not by rewriting the seated 05.01 and 05.02 (axiom 6,
kernel-trial-4 H1, D344). Not four copies. Parked files stay as
history and are not built. Do not revive "trial and seat the door's
face 00" as a seating step (D342): that is R25 and D338, and it
belongs on 0052 as a lesson. Do not decide Q26, Q31, Q33, or O14.
The two lookup-exercise cards on 0051.05.04 are not blocked and can
move. This is a good fill-in of D338, and it is also the start of
the R24 climb on those two pages (D348).

**D352.** Smaller improvements, not disagreements:

- `0051.05.04` and `0052.05.04` are the next packs. They should name
  the seated 05.02 they follow (`supersedes:` or an equivalent), and
  the core should eventually read that (D345). 05.03 is lessons, like
  05.01: keep it out of the "which pack is current" rule. Q44 stays
  open; this is only so the climb has a reader.
- Cite the parked files by path plus blob (D348, as Q53 did for
  trials), not by commit id. New counters should not add more
  local-only commit cites (test 5).
- The 00.counter lesson on 0052.05.03 is right as a lesson. Do not
  write a 00.counter into the shared repo until the A4.4 hole is
  solved (D346).
- These counters are the door-lessons slice of the climb. D348's
  stale-card work (close the already-done w01 cards, fix broken
  counts, re-point 0052 w02) is a separate set of cards, on these
  new counters or a later one. This draft is right not to mix that
  in; it should not be forgotten.

The Designer draft was not rewritten here. The new counters were
not written.

---

## 3. Book Layout (D343) — how it is merged is D353

Adopt the draft as written. The proposed 01 and 04 text is the Q30
path (D327) in card form: four sections, behavior and structure as
kinds inside `0020-0099`, "0000-0019 are static" as a property of
the first three together, rows above 0100 unchanged, R21 and R7's
two target ranges unchanged, 01 and 04 agreeing (C3.2), the Q30
hold left on the kernel until Matthew rules. The leftover seqAddr
sentence that treats `0001-0099` as overrides should become
`0001-0009` (R7; the 04 card already says this). That is a real
correction. decisions.md A2.7 is rightly left as CONFLICTS D13.

**D353.** After a ruling, merge the text into the draft law cards
`0051.01` and `0051.04` (w03's own path already names those draft
files). Do not rewrite the seated `0051.05.02` to close the card.
If w03 needs a closed mark, that goes on the next 05 counter
(D348, and D341 already plans `0051.05.04`). Same lesson as test 6
and 0052 w02: a seated pack is not edited.

A light caution, not a disagreement: "the common questions sample
at 0013" is the wording already on WORKING-PATH-Q30.md. QD27 (is
0013 the right home) is still `7`. Keep 0013 as a sample, not as a
ruling that every book must have 0013. Q30 stays open.

The kernel cards and the seqAddr table were not edited. The Q30
hold stays.

---

## What this does not do

It does not rewrite the three Designer drafts, the kernel, or the
earlier working-path files' original recommendations (D333, D338,
D327). Those still stand, with the D351 address change on D340.
It does not mark Q41, Q43, or Q34. QD67 was not touched. Q26, Q31,
Q33, Q44, QD11, QD16, and QD27 stay open.

---

## Status

Working path, pending Director review. Not a ruling. Recorded in
[DECISIONS-LOG.md](DECISIONS-LOG.md) as D351-D353, and on QD10,
QD13, and QD27 in [QUESTIONS-FOR-DIRECTOR.md](QUESTIONS-FOR-DIRECTOR.md).
