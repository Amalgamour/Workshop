# Morning review: working paths for the Director

**WORKING PATH.** A morning review sheet for Matthew, written by
Tester on 2026-11-12 at about 6:15 AM EST (America/Toronto). These
are recommended options for you to review. They are **not rulings**
and **not settled law**. No other file was changed.

Files are in `docs/design/WORKING-PATH-` plus the short name, so
`QD02.md` means `docs/design/WORKING-PATH-QD02.md`.

## If you rule first on these, the most work can move

1. Whether the workflow write-up is the law for this build
   (QD12). That unblocks the work loop and kernel page 0057.
2. How the fingerprint list (00.counter) is seated, and how it
   climbs (QD66, QD67). You already asked for this list (R25).
   Until a hole between the builder and the core is agreed, that
   list should not be written.
3. Which page types there are (QD02), and whether notes and
   dictionary sections are seated (the leftover in QD01). Many
   later page questions use these.
4. Who may change the kernel book (QD07).
5. Whether the page-file layout is OK as already built (QD34).

## Pages and faces

- QD01 (D320, LINEAGE.md; D337, Q35.md). A later pack is a new
  counter (05.07), not a silent replace. Do not seat notes. Do
  seat dictionary sections after a trial.
- QD02 (D319, QD02.md). Add a new type only when a page lives
  under different laws; otherwise use a kind field. Add door,
  override, and axioms.
- QD11 (D365, OPEN-QUESTIONS.md). Which faces are counted is
  law (05, 06, and dictionary face 03), not a switch a page
  type can flip.
- QD13 (D327, Q30.md). Four sections below 0100, each with its
  own laws: door 0000, overrides 0001-0009, required static
  0010-0019, working 0020-0099.
- QD14 (D382, QD04-QD15.md). In R14, "door" means the page's
  own face 00. Today's behaviour stays.
- QD16 (D363, OPEN-QUESTIONS.md). After 98, do not reuse a
  number and do not invent 99. Counter 98 points to a new page
  that starts a new 01-98 series.
- QD17 (D389, QD17-QD21.md). A book's tasks and notes are its
  own. The kernel's are found at the kernel address.
- QD20 (D392, QD17-QD21.md). The "every 01 or 02 card needs a
  04 card" rule does not apply to task lists.
- QD24 (D410, QD24-QD46.md). Same number and a different title
  is not a set. Raise it only if two such pages are joined by
  a written link.
- QD25 (D411, QD24-QD46.md). Titles stay lowercase. This
  covers page titles only.
- QD26 (D366, OPEN-QUESTIONS.md). Yes, add a "question" card
  type with the fields already in use.
- QD27 (D353, DRAFT-EVAL.md). Page 0013 is a sample, not a
  rule that every book must have one.
- QD32 (D399, QD29-QD33.md). Owner class lives on law cards,
  not on the system page's face 00.
- QD33 (D400, QD29-QD33.md). "Code" means the code laws you
  already decided. Workflow build pages stay type workflow.
- QD40 (D407, QD35-QD40.md). Band 3 (0300-0399) is build.
  Band 5 (0500-0599) is jobs.
- QD45 (D413, QD24-QD46.md). The axioms' faces use the same
  names as other pages: 00 registry, 01 law, 02 schema, 03
  operate, 04 user, 05 tasks, 06 notes.
- QD48 (D418, QD47-QD52.md). Reserved 01-09 is for axes, not
  counters. Tasks, notes, and dictionary sections count from
  01. The dictionary sets 03.01-03.09 aside for digit and
  symbol words.
- QD49 (D419, QD47-QD52.md). There is no page 0117 in
  Workshop. That name is from the old system. Do not create
  one.
- QD51 (D420, QD47-QD52.md). A note carries by, date, refs,
  why, and unresolved. It drops state.
- QD53 (D424, QD53-QD57.md). A new meaning goes on face 01 of
  the explaining page. If that page is not known, the computer
  asks and never picks. The card stays in the book.
- QD55 (D425, QD53-QD57.md). Yes, only for a new scratch page
  type, and nothing on it is ever seated. To make scratch work
  real, it is copied into a normal page.
- QD58 (D430, QD58-QD64.md). No. Keep one climbing 05 line,
  01-98. Do not split by number.
- QD59 (D369, OPEN-QUESTIONS.md). No. A fix is a new draft and
  a new seat, or a new 05 counter, not a patch on the seated
  body.

## Face 00

- QD03 (D326, QD03.md). Nobody writes a faces list into face
  00. The computer works the list out from the faces that
  exist, and still checks it.
- QD04 (D379, QD04-QD15.md). Face 00 is the list, so it is
  not in it.
- QD08 (D364, OPEN-QUESTIONS.md). The stamp is the only source
  of truth for a page's state.
- QD23 (D368, OPEN-QUESTIONS.md). A door's return link is a
  line on the door's face 00. Do not add face 08 to a door.
- QD28 (D367, OPEN-QUESTIONS.md). Halt a write when the book
  would be unreadable, when two live claims disagree, when a
  fingerprint mismatches, or when a seat names a blob that is
  not a real past seat.
- QD29 (D396, QD29-QD33.md). Face 00 is a stamp, then exactly
  one Registry card. Derived values are shown, not stored.
- QD30 (D397, QD29-QD33.md). The lineage line is the chain up
  only, and it is derived, never stored.
- QD35 (D403, QD35-QD40.md). Yes, as a derived inherits line
  only, never stored. It lists content faces only, not tasks,
  notes, or face 00.

## Workflow

- QD15 (D383, QD04-QD15.md). No. A task starts at draft, and
  only the computer moves it to pack, after a check.
- QD21 (D393, QD17-QD21.md). Yes. Every seat carries who
  approved it, including the computer's. Steps that are not
  seats stay exempt.
- QD22 (D374, WORKFLOW.md). A written "abandoned" decision
  with an approval. Silence alone does not take the task back.
- QD31 (D398, QD29-QD33.md). A write-once approval note on
  the approval page's notes face, under the approver's name.
- QD44 (D412, QD24-QD46.md). A return lives on the same
  counter as its pack, not on a new number.
- QD54 (D375, WORKFLOW.md). A rejection is the reviewer's
  notes on the draft, then a fresh review from a different
  view; or a logged withdraw if it should not be seated.
- QD62 (D376, WORKFLOW.md). Default order, every reason
  recorded: needs-authority, then failed, then abandoned only
  through recovery. "Carry on" may grant a further allowance,
  and may not reset the weight, widen the scope, or promote.

## Kernel and addresses (seqaddr)

- QD06 (D380, QD04-QD15.md). Keep the token sign-in as built
  for this stage: it knows who you are, not what you may do.
- QD07 (D381, QD04-QD15.md). Only level 00 may change what is
  live in the kernel. Anyone may propose a draft. Retiring
  needs the same approval as seating.
- QD09 (D332, QD09.md). The exact address of the axioms is
  00.axioms (desk 00, titled axioms). Keep the old name
  findable during the move.
- QD10 (D333, D351, QD10.md). There is no 03.00 file. The
  menu is worked out from the sections that exist. An
  explanation belongs on face 01 or 04, not at 03.
- QD18 (D390, QD17-QD21.md). Retiring an override means "I no
  longer have my own copy"; lookup walks on to the parent. A
  door must never fall through to the shelf's door.
- QD19 (D391, QD17-QD21.md). A draft may hold a return link
  while the pointer is also a draft. A seated pointer needs a
  seated return link, and they go live together.
- QD36 (D404, QD35-QD40.md). Keep the bytes exactly, and
  report body lines that end in spaces as findings. Do not
  change the format.
- QD37 (D405, QD35-QD40.md). Yes, a hand-written file is a
  proposal like any other, for a page that is not already
  found.
- QD39 (D406, QD35-QD40.md). Yes, a card's name may go in a
  read address, never as a write target and never as a title.
- QD46 (D414, QD24-QD46.md). A snapshot is never trusted over
  the book log, and is checked on every open. Only the
  compute takes one.
- QD47 (D417, QD47-QD52.md). Making the start-up law needs
  you; until then, follow what is already built, as
  provisional. The kernel holds the agreements; the compute
  runs the work.
- QD56 (D426, QD53-QD57.md). Web calls (HTTP) are the one way
  in. If MCP is wanted, it is a thin adapter that makes the
  same calls, not a second door.
- QD57 (D427, QD53-QD57.md). Two copies are never merged by
  mixing their lines. Re-play the other copy's later writes
  as new proposals, one at a time. Until that is built, a
  diverged copy is held as its own book.
- QD60 (D431, QD58-QD64.md). Hardware is a build choice
  already made: one ordinary computer, local plain-text
  books, loopback only, no special device. One point is left
  for you, in the list below.
- QD63 (D432, QD58-QD64.md). Your ruling on plain characters
  stands (R4). Accented letters do not come back now.
  Widening is your call later, only when a real need appears,
  and only after trials. Addresses, titles, and other grammar
  stay plain characters always.

## Ask

- QD52 (D421, QD47-QD52.md). Yes. Record every outcome. Count
  a failure only against a word meaning that was assumed and
  stated back.
- QD64 (D433, QD58-QD64.md). Empty until you give the words:
  empty for now, not "there is no base dictionary." When
  given, only Workshop-special words, each pointing to the
  page that explains it. Lookup must check the book first.

## Only Matthew can decide

These have no recommended path, or the choice itself stays
yours. One point from QD60 is included here.

- QD12. Is the workflow write-up (.003) the law for this
  build, or does it stay a draft? It cites decisions F02-F10
  that are not in the repo. Do you have those notes?
- QD34. Is the page-file layout (.seq) OK as already built,
  including that worked-out lines can change, and others only
  grow?
- QD38. Is the right place for "why it is a draft" a reason
  field on the write, with a why-NN line in face 00 too? That
  is how it is built.
- QD42. Should the drafting steps (copy, note, merge,
  promote) and all-or-nothing proposals become law, or stay
  proposed? They are built and on by default.
- QD61. The later workflow details: the risk list, claim
  time-outs, who confirms abandonment, writes across books,
  and more. Already in use: a proposal writes one book only.
- QD65. Do you want to check the Ask word lists and scoring?
  Key 2, linking 1, question 1, pass mark 0.5; all of it can
  be changed in one place.
- QD66 (D357, D360, 00-COUNTER-EVAL.md). Are these faces
  seated the normal way, or write-once evidence? Until a
  builder-and-core hole is agreed, do not write a 00.counter,
  and do not make face 00 a counted face.
- QD67 (D360, 00-COUNTER-EVAL.md). When a new fingerprint is
  added, is each snapshot a new counter (00.01, then 00.02),
  or does one face hold the whole list? The climb is yours.
- QD41. Is a desk's door written as DD.00, or as a full page
  DD.00.00.0000? The same question for a shelf.
- QD43. What is "written permission": a recorded grant, or a
  direct instruction?
- QD50. How are face 08 links stored and traced? Proposed
  kinds include member-of, continues-from, and references.
- F8. For an override page, do four statements sit in face 00
  or in a face 01 card, and what type is that page? Override
  pages are parked for this build (R21).
- F10. What types should page 0000, continuation pages, and
  the common questions list have? A recommendation is in
  QD02.
- QD60 (one point). Whether Workshop must be reached from
  more than one machine. That needs secure connections (TLS)
  first.

Nothing on this sheet is a ruling. No other file was changed.
