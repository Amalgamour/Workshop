# Working path: QD24, QD25, QD44, QD45, and QD46

**WORKING PATH.** Tester's recommended options, written 2026-11-12
at about 2:15 AM EST (America/Toronto) for Prima to record and for
the Director to review. They are **not rulings** and **not settled
law**. No kernel, core, seated faces, or Designer drafts were
changed.

These are five questions from QUESTIONS-FOR-DIRECTOR.md that still
had no working path. QD38 was not answered (already covered).
QD41, QD43, QD12, QD50, QD61, QD66, and QD67 were not answered or
marked. Q41, Q43, and Q34 were not marked. Kernel Q45 and kernel
Q40 were not given a QD home and were not answered. F8 and F10
were not answered. F.2 was not seated. The D310/R21 shadow case
was not decided.

Checked against R18 (sets are matched by CC and title; the
IDE-design example), R22 (every design choice recorded), R23,
R24 (climb the 05 counter; lineage matters; the past is not
rewritten), R25 (face 00 is the registry root; a 00.counter is
its own face; this path does not answer QD66 or QD67), and the
axioms, especially 1, 2, 6, 7, and 8. Also checked against R4,
R6, R10, R12, and R19; OPEN.md O26, O27, and O30; kernel
CONFLICTS.md K09, K12, D11, and D16; kernel QUESTIONS Q37 and
Q48; format.md 3.4; Axioms.md; decisions.md (A2.2, A2.3, A2.5,
A2.6, A2.8, E9, F.1, F.2); the workflow-loop drafts; seqAddr.md;
the core, seqpage, the compute, the app, the kernel faces, and
the books.

---

## QD24. Same CC, different title: do you want to be told?

R18 matches pages by CC and title (the last two digits of the
page number, and the title). An older rule raised a title
mismatch to you, in case it is a typo. Option A: not a set,
nothing raised. Option B: not a set, but you are told. Now: `7`.
Nothing is raised.

**Best option:** Option A, sharpened: a page with the same CC and
a different title is not a set, and nothing is raised just
because the numbers match. If two such pages are joined by a
written link and their titles differ, that is raised.

R18 makes the set from both the CC and the title. The older
elevation rule (A2.6) was written when the number alone made the
set, and the title was a typo check inside a set. Under R18,
raising every same-CC pair with different titles would raise
pages that are not related. Matching is not a connection
(axiom 8), so not matching is not a defect either. An elevation
is not a halt: axiom 1 is for two live claims, which this is not.

If two pages are joined by a written connection (a face 08
link, a continuation pointer, or a pack's explicit predecessor
or set reference) and their titles differ, that is a real
disagreement between connected pieces. Axiom 8: "two that are
connected must agree." That is raised. It does not need F.2 to
be seated, and it does not make them a set.

Today nothing is raised because nothing looks: the core's
set-matching is built and has no callers outside tests. A
one-letter typo silently splits a set, and a proposal check
returns no finding. That is the Now, and it matches A for
unconnected pages.

**Offers, not the path:** a non-blocking finding at write time,
when a proposal writes or retitles a page whose CC already holds
a page in another band of the same thousand with a different
title. The finding would say they are not a set (R18). It is a
report, not an act (axiom 5). It is not a background search
(axiom 7), and it never makes them a set or repairs a lookalike
(axiom 8). A second offer: show "same CC, other title" only as
a derived, read-only listing in the app's page view, never
stored, never membership (S05: digits help a reader find related
pages).

**Findings, not implemented:** the seqpage derived `set` key is
CC and title with no thousands digit, so pages 0403 and 1503
get the same key, while the core requires the same thousands
digit. The core also lets bands outside N3-N7 form a set (for
example 0103 and 0903). Band scope belongs to F.2; this path
does not decide it. A2.6 still carries the old elevation clause
in a section marked settled; R18 governs over the older wording.

This does not seat F.2. It does not answer the other half of
O13 (membership by number vs face 08 links). It does not answer
QD12 or kernel Q43. It does not edit A2.6 or seqAddr.md.

Working path, not a ruling.

---

## QD25. May titles have capital letters?

Your R18 example is IDE-design. The title rule allows only
lowercase letters, digits and hyphens. Now: `7`. Capitals are
refused.

**Best option:** Option A. Titles stay lowercase (A2.3, settled).
Matthew's "IDE-design" is quoted as he said it, and is used as
`ide-design`. This path covers page titles only (the stamp
`title:` and the title in an address), not the free-text
`title:` field on work cards.

The point of R18 is that the CC and the title make the set, not
the case of the example. A2.3 is settled law. The kernel
grammar, the address parser, and the proposal check are all
lowercase. Where his words are quoted, keep the quote exactly
(axiom 7: do not invent a meaning for the capitals; axiom 8: a
copy does not become what it points to). Where the example is
used as a working example, write `ide-design` and say it is the
A2.3 form of his example. face00.md already writes it in
lowercase, without saying so.

No page has the title `IDE-design` or `ide-design`. Every page
stamp checked is already lowercase, so nothing is rewritten
(axiom 6).

If capitals were allowed and compared exactly, `IDE-design` and
`ide-design` would silently not be a set. Folding case to make
them one set would match by a lookalike, which axiom 8 forbids.

Kernel Q48 asks the same question. It is not in QD25's Raised
line. This path answers the substance; Q48 is not marked.

**Offer, not the path:** if capitals are wanted for reading, a
page could carry a display heading in any case, with the stored
title in title form, the way card keys already work (`Retry
Policy` becomes `retry-policy`). Matching and addresses would
use the stored form. This adds a field, and the display text
must never be used to match (axiom 8). Not recommended now
(R4: a simple storage design, limited characters is fine).

**Findings, not implemented:** A2.3 is enforced only when a
proposal is checked by the core. The kernel builder, a core
replay of a stored log, the compute loading a book, and a
`.seq` export and check all accept a stored capital title (the
builder's only title rule is that pages 1000 and up need a
title). A stored capital title then cannot be used in any
address, because the address parser refuses it, so the A2.8
address-vs-stamp check can never reach it. The word "title" is
also used for a free-text field on work cards, which A2.3 does
not cover and nothing checks.

This does not change A2.3, the grammar, or the core. It does
not edit the quotes. It does not rule on work-card `title:`
fields. R4 does not decide this (capitals are ASCII); A2.3
does.

Working path, not a ruling.

---

## QD44. Does a return live on its own task number?

Raised from O26 and K12. There is no Now line. O26's Option A
says "Yes, on the same counter as the pack." The question's
wording ("on its own task number") can be read two ways. This
path says "the same counter as its pack" in plain words: not a
new number.

**Best option:** Option A. A return lives on the same counter as
the pack it answers. The counter's tail moves from open to
return, and the return body is written in that same log entry,
so pack and return keep one identity and the pack text stays as
the earlier entry (axiom 6). This is what the core already does.

A new counter is used only for (a) rework after a failed review
and (b) replacement after an abandoned claim, each with a
written link to the earlier one. A new pass on a page (R24's
climb, a new 05 counter) is a new pack, not a return.

This matches the approved .002 text ("This settles where a
return lives"), the .003 draft, F.1 S02, S03 and S11, kernel
0057, and the core. The one-entry form already makes the return
and the tail move durable together, which is the durability
half of workflow-loop.003.md:181 for a single return. No
counter in any book has reached `return` yet.

Reject giving a return its own new counter: that would split
one attempt across two identities, need a link kind that is
still only proposed (`continues-from`, C4/E9), and break "the
counter keeps the same identity throughout."

**Offer, not the path:** seat E9's placement sentence ("on its
counter") separately from its second half ("its findings are
booked as 06 notes and 05 tasks on the pages they concern").
The second half creates new counters on other pages and needs
the C4 link kinds and questions about who may confirm (QD61).
Seating them together would tie a rule the core already follows
to one that is still open.

**Findings, not implemented:** the core accepts a return with no
body; there is no return-shape check yet (S02 is approved, not
built). workflow-loop.003-notes.md is still missing (7.8).
QD44 and QD45 have no Now line.

This does not change what face 05 means. It does not mark
kernel Q41 or answer QD01, QD61, or QD22. It does not seat
F.2 or the `continues-from` link. It does not reopen QD40 or
D407 (band 5 is jobs). It does not decide what happens if a
return is written on a seated 05 counter (QD01 / Q41).

Working path, not a ruling.

---

## QD45. What are the axioms' faces called?

Raised from O27 and K09. There is no Now line. This is not
kernel Q45 (that question is about what authorizes packs, and
is not answered here).

**Best option:** combine A and B. The axioms' faces use the face
names every page inherits: 00 registry, 01 law, 02 schema, 03
operate (worked out, never written), 04 user, 05 tasks, 06
notes. The five phrases in Axioms.md:3 ("01 agent form, 02 cite
card, 03 menu, 04 full explanation, 06 notes") match those
faces one-to-one and describe what they hold on this page. They
are not names, because faces carry no titles (A2.2), and a page
does not rename inherited faces (axiom 2: write only the
difference).

What is actually there today: face 00 (registry, draft), 01
(the axiom cards, law), 02 (one Cite card, schema), 04 (the
full explanations, user), 05.01 and 05.02 (seated, R22), and
06.01 (notes). There is no face 03: a written menu was removed,
because menus are derived and never drafted (C8.9,
drafting.md:40). Face 05 exists because of R22; Axioms.md:3 and
decisions.md:531 predate that.

The core and the app already use one global set of face names.
0052.01 (seated) uses the same names, with 00 as "registry"
(R10, R12, R19), not "identity."

The `axioms/` folder that Axioms.md:3 points to is not in the
repo (7.8). Do not invent its content (axiom 7). If Matthew has
it, the faces should be checked against it (the seated 05.02
work card already says this). That is his to send. Without it,
this path stands on the inherited names and on the reading of
Axioms.md:3 as descriptions. He can overturn it if the folder
says otherwise.

**Offer, not the path:** put the five phrases on the axioms page
as a short "holds:" description per face in the registry
(derived from the cards, never a title), so a reader sees both.
Not adopted; it adds a field.

**Findings, not implemented:** K09's heading says "SETTLED", but
its body says the face list is still open. O27 still blocks on
"kernel page 0050's face names"; R6 moved the axioms off 0050.
MAP.md lists a face 03 on the axioms page (it was removed) and
leaves out 05. Face 04 is called "user" in the spec and the
core, "Why" in the app, and "full explanation" in C3.
DESIGN.md section 10 still lists O10 and O1 as open; R6 and
R20 already answered them.

This does not decide the exact axioms address (R6 is still `7`,
QD09). It does not re-add a written face 03. It does not answer
QD43 (written permission) or define levels 02, 03, 05-09.

Working path, not a ruling.

---

## QD46. How far is a snapshot trusted, and when is one taken?

Now: `7`. Every snapshot is checked against the log. Raised
from O30.

**Best option:** Option A, made exact, and only for snapshots
inside a book's log. A snapshot is never trusted over the log.
It is checked on every open. A snapshot whose earlier entries
are not in the file is a connection that cannot be opened
(7.8): it is reported, and is not used as the start of the
line. Only the compute takes one, never a person or a model
and never through a proposal. None is needed now. No entries
are moved to an archive until an archive is defined that can
still be opened and is checked with the book.

"Snapshot" means three things in the repo. This path covers
only the first:

1. A snapshot entry in a book's log (format.md 3.4). This is
   what O30 asks.
2. R25's fingerprint taken before a change. That is QD66 and
   QD67, and is not answered here.
3. A git tree as a snapshot, in the builder. Not a Director
   question.

A snapshot is a saved copy of what the log already says, not a
record of a new step. The log is the line (axiom 6). A copy
never becomes what it points to (axiom 8). On every open, the
compute already checks every snapshot against the entries
before it; a mismatch is refused. The fast path that trusts the
latest snapshot has no callers, and the comment on it already
says to use it only on a book whose snapshots were checked on
this open.

When taken: not now. No book holds a snapshot. The core refuses
a snapshot in any proposal, including one by the compute, and
the compute has no other way to write one, so none are taken.
If one is needed later, the trigger is a compute policy written
down with its why (axiom 4), not a hidden habit.

Archive: format.md 3.4 allows older entries to move to an
archive. The built reader refuses any log not numbered from 1,
so that archive is unreadable today. Until an archive can be
opened and checked with the book, moving entries out would
leave every later replay starting from an unchecked snapshot,
which is trust over the log.

**Offers, not the path:** keep snapshots out of the book
entirely. A snapshot is worked-out state, and format.md:102
already says derived things are never written as entries. The
compute can keep a cache beside the book, throw it away when in
doubt, and rebuild from the log. Then "how far trusted" is
answered by design: never, because it is not part of the
record. That would change format.md 3.4, which is Matthew's.
A second offer: each snapshot carries a fingerprint of the log
before it (the same idea as the git-blob fingerprints of D323
and R25), so a reader can check quickly and start late without
trust. The core trial suggested this; it was not built.

**Findings, not implemented:** because every snapshot is checked
by replaying the whole log, a snapshot does not speed anything
up today. In memory, a log that starts with a forged snapshot,
or that starts at an entry after 1, can be accepted with no
check of what came before; text parsing blocks those cases
today. D84 cites format.md:87; the snapshot row is at 88.
D230 says "settled-by-spec format 3.4", but 3.4 says readers
start from the latest snapshot, which is not the rule that every
snapshot is checked. DESIGN.md still reports the forged-snapshot
finding as if it were open; it was fixed.

This does not answer QD66 or QD67, and it does not write a
00.counter. It does not change format.md, the core, or the
compute. It does not decide fork reconciliation or the
builder's git-tree "snapshot."

Working path, not a ruling.
