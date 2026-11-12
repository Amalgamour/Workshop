# Open Director questions that block the most work - working path

**WORKING PATH.** Tester's recommended options, written 2026-11-11
at about 8:00 PM EST (America/Toronto) for Prima to record and for
the Director to review. They are **not rulings** and **not settled
law**. No kernel or seated files were changed.

These are the open questions in [QUESTIONS-FOR-DIRECTOR.md](QUESTIONS-FOR-DIRECTOR.md)
that have no working path yet and that block the most work. Each
gets a best option, the other options considered, and why. Questions
already given a working path (QD02, QD03, QD09, QD10, QD13/Q30,
QD01/Q35, kernel Q42, and the 00-counter fill-ins) are not repeated.
QD66 and QD67 stay for Matthew. Kernel Q41, Q43, and Q34 were not
marked.

---

## QD16. What happens after counter 98?

Urgent for face 00's 00.counter line (F11), and it also applies
to every counted face. Counters run 01-98 only (R9). Today's
code refuses 99. Option A: the face is full; new work goes on a
next page. Option B: closed counters are archived.

**Best option:** After 98, do not reuse a number, and do not
invent a slot 99. Write a connection from counter 98 to a
continuation page (the `pointer` type already exists) that starts
a new 01-98 series for the same job. The old numbers stay as
history (axiom 6). The link is written (axiom 8), so a person
and the computer can travel to the next series. This is Option A,
with the connection made explicit.

Option B helps only if archived numbers are reused. Reuse would
give two lives to the same address, which axiom 6 does not allow.
If "archive" means freeze and keep the numbers, the face is still
full at 98, so B does not solve it. Raising the 98 cap would
change R9; that is not recommended.

This unblocks the 00.counter climb design (the cap may arrive
sooner there than on a pack, because face 00 changes more often)
and any 05 or 03 series that reaches 98.

---

## QD08. Where does a page keep its state? (kernel Q31)

Matthew already said the state lives in the stamp in face 00
(R12). Today both the stamp and the file-name ending are written,
and a mismatch is flagged, never refused. That is two live claims
(axiom 1). It blocks kernel page 0053, every face 00, and the
parked door cards that wait on Q31.

**Best option:** The stamp is the only source of truth (R12,
Option A). If a file-name ending is kept, the computer derives
it from the stamp; it is not a second authority. A leftover
ending that disagrees is a finding, not a reason to refuse the
whole book. This is the same shape as QD03 (D326): one derived
list, a leftover written line is a finding.

Option B (both must agree, and a mismatch refuses) still leaves
two authorities. Option C (the file ending decides) goes against
R12.

---

## QD11. Which faces are counted, on which page types? (kernel Q22)

Today a fixed list is used: faces 05 and 06 everywhere, and
dictionary 0012.03 (`always_counted` and `Policy.extra_counted`).
Option A would let each page type name its counted faces.
Option B keeps the fixed list.

**Best option:** Option B, sharpened. Counted-ness is law, not a
switch a page type can flip. Adding a counted face changes what
plain FF means (it becomes a derived listing, `resolve.rs:182`)
and refuses a bare put (`state.rs:460`). That is the D351 lesson:
an explanation card cannot live at `0012.03` because 03 is
already counted. A page type should not be able to hide a content
face that way. If a new counted face is needed, that is a
Director question, not a type field.

This keeps the A4.4 rule stable, and it is what the core already
does.

---

## QD26. Add a "question" card type to the kernel? (CONFLICTS D14)

The common-questions cards already use `type: question`. The
kernel's card type table has no such type. They are accepted
anyway. Page 0054 and the sample 0013 pack wait on this (kernel
Q49, CONFLICTS D14).

**Best option:** Yes, add `question` as a named card type, with
the fields those cards already use (`forms`, `answer`, and the
rest as already written). If a kind of card is in use and has
its own fields, it should be on the table (axiom 8: name what
is there). This is the same idea as QD02: add a type when the
laws or fields differ; do not keep accepting an unnamed type.

The other option -- leave it unofficial and keep accepting it --
leaves a conflict on the table and keeps 0054 blocked. QD27
(whether 0013 is the right home) stays `7` and is a separate
question; adding the type does not decide the page number.

---

## QD28. Which face 00 problems should stop a write, not just be flagged?

Today all face 00 problems are flagged only. That is too soft
for some, and it is part of why `--check` can pass a book the
core will refuse.

**Best option:** Halt (the write is refused, `--check` fails)
when:

- the book would be unreadable to the core (the test-3 hole;
  see [WORKING-PATH-CHECK-CORE.md](WORKING-PATH-CHECK-CORE.md));
- two live claims disagree and there is no lawful connection
  (axiom 1);
- a fingerprint does not match (D324, D347);
- a seat or un-seat names a blob git does not hold as a real
  past seat (already Pass 12).

Flag, and do not halt, leftover derived fields that are not the
source of truth: a written `faces:` line that disagrees with the
derived list (D326), or a file-name state ending that disagrees
with the stamp (QD08 above). Those are findings to clean up,
not a reason to make the book unreadable.

---

## QD23. Where does a door page keep its return link? (kernel Q26)

A door page holds only face 00 (R10), so it has no face 08.
Option A: a line in face 00. Option B: pointers never aim at a
door page. Today Option A is used. The parked door packs wait
on this (and on Q31, which is QD08 above).

**Best option:** Option A. The return link is a line on the
door's face 00. That honours R10 (the door has no other face to
put it on) and axiom 8 (the connection is written). Option B
would forbid a lawful pointer at a book's door (A5.3), which is
a real use. Do not add a face 08 to the door to hold the link;
that would break R10.

---

## QD59. Should small "patch and strike" edits be allowed on a seated face?

**Best option:** No. A seated face is not edited (axiom 6; the
in-place reseat hole, D344; kernel-trial-4 H1; test 6; D353).
A small fix is a new draft, written through the drafting steps
(copy, note, merge), and then a new seat; for a pack, it is a
new 05 counter (R24), not a patch on the seated pack. Struck
notes on a draft during writing (D0) are a different mechanism,
and they stay on the draft, not on the seated body.

Allowing a patch on a seated face would rewrite the past, which
axiom 6 forbids, and it would teach the builder the same habit
test 1 already caught.

---

## Not picked here, on purpose

- QD22 (what record lets the computer take back an abandoned
  task) is refused until Matthew decides, and it does block a
  compute path. A lean, not an answer: a written "abandoned"
  decision with an approval (Option A) is safer than a silent
  time-out. Left for a later pass if Prima wants it.
- QD12 (is workflow loop .003 the law, and where are F02-F10)
  blocks page 0057, but the missing decisions are Matthew's
  files. There is no best option without them.
- QD41 / O14 (is a desk's door `DD.00` or `DD.00.00.0000`)
  blocks some door work. It sits next to kernel Q41, which
  stays for Matthew, so it is not answered here.
- Kernel Q33 is page types, already a working path as QD02;
  those packs wait on a ruling, not on a new pick.

---

## For Matthew

Six open questions were picked because work is waiting on them.

After counter 98, start a new page that continues the line, and
do not reuse a number.

A page's state lives only in the stamp, as you already said.

Which faces hold counters is a fixed law (05, 06, and the
dictionary's 03), not something a page type can switch.

The "question" card type should be named, because those cards
already exist.

Some face 00 problems should stop a write (a book the core
cannot read, two disagreeing claims, a bad fingerprint). Others,
like a leftover list, are just findings.

A door's return link lives on face 00, because a door has no
other face.

A seated face is not patched. A fix is a new step in the line.

---

## Status

Still `7`, not law. Pending Director review. No files in the
kernel, the core, or the seated packs were changed. QD67 stays
for Matthew. Q41, Q43, and Q34 were not marked.
