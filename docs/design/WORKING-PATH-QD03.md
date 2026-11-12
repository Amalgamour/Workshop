# The face list in face 00 (QD03) — working path

**WORKING PATH.** This is Tester's recommended option, recorded by Prima
on 2026-11-11 at about 7:25 PM EST for the Director to review. It is
**not a ruling** and **not settled law**. Prima will use it as the
working path until Matthew rules.

Question: [QD03](QUESTIONS-FOR-DIRECTOR.md) — Is the face list in face
00 written by hand, or worked out by the computer?
Source: Tester, 2026-11-11 evening. Related: R10, R25, axiom 6, F7 in
[R23-R25-lineage.md](R23-R25-lineage.md); kernel Q27; face00.md F2;
CONFLICTS D5; format.md:102.

---

## The idea, in one line

Nobody writes a `faces:` list into face 00. The computer always works
the list out from the faces that exist (the files, and the book). It
still checks that this derived list agrees with the other written
records — seat lines, `why-NN` reasons, and book entries. A mismatch
is flagged.

---

## What this is, and is not

This is Option B for where the list lives, plus the check from Option
A. It is not pure B (the core today derives and does not check). It is
not Option A (the kernel and the face00.md draft today: the computer
writes `faces:` into face 00 and checks it).

During a move-over, a leftover written `faces:` line is a finding if
it disagrees, and is not the source of truth.

---

## Why Option A is not enough

Who writes the list does not matter. If the list is stored as bytes in
face 00, every new face, and every tail change (a draft becoming
seated), changes face 00's fingerprint. That is the cascade Tester
reported as F7. R25 already used this exact reason for the fingerprint
list: the list must be its own face, not lines inside 00, or writing
the list would again change 00's fingerprint. The same reason applies
to `faces:`. Option A looks like it solves "never written by hand"
(decisions.md:301, format.md:102), but it still rewrites face 00,
which axiom 6 and R25 are trying to avoid.

---

## Why this still honours R10

Matthew said face 00 is "the place that lists the page's faces." That
is the registry's job — the list it presents when you look. It does
not have to be stored text inside 00. Contents lists and boards are
already derived, never written as entries (format.md:102, A5.4). The
face list should follow that same shape.

---

## Why not the other options Tester considered

Why not pure B with no check: a missing file, or a seat record that
names a face that is not there, would just vanish from the list with
no alarm. R2 wants every seat to be findable. The computer should
still compare the derived list to seat lines and to the book.

Write the list somewhere else (a side file, or onto a 00.counter):
that is a second copy to go out of date. Derive it instead.

Write `faces:` only for seated faces, and derive drafts: a new seat
would still change face 00. A partial cascade, not worth it.

---

## What this does not decide

- QD04 (is face 00 in the list): if the list is derived, that is only
  a display question; today's path, state from the file, still works.
- Q39 (how counted faces are shown: `06 counted` vs `06.01 draft`).
  Those are about the shape of the derived list, not whether it is
  written.
- It does not remove `why-NN` or `seat-NN` from face 00. Those are
  real records (R5, R25), and they are why 00.counter exists.

The builder's hard error at `kernel/build.mjs:615-617` would, on this
path, become a derive-and-check, and existing `faces:` lines would be
findings until they are dropped. That change has not been made.

---

## What this unblocks

Every face 00, the kernel builder, the .seq checker, and the core can
agree on one path (QD03's block). CONFLICTS D5 and face00 F2 get a
working path. The F7 cascade is broken: adding a 00.counter no longer
forces a registry edit on face 00.

For Matthew, one idea: the list of faces should be worked out from the
files that exist, not written into face 00, because writing it would
change face 00 every time a face is added — the same problem you
already solved for fingerprints.

---

## Status

Working path, pending Director review. Not a ruling. Recorded in
[DECISIONS-LOG.md](DECISIONS-LOG.md) as D326, and on QD03 in
[QUESTIONS-FOR-DIRECTOR.md](QUESTIONS-FOR-DIRECTOR.md).
