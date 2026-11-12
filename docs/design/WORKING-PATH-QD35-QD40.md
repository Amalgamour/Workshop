# Working path: QD35, QD36, QD37, QD39, and QD40

**WORKING PATH.** Tester's recommended options, written 2026-11-12
at about 1:30 AM EST (America/Toronto) for Prima to record and for
the Director to review. They are **not rulings** and **not settled
law**. No kernel, core, seated faces, or Designer drafts were
changed.

These are five questions from QUESTIONS-FOR-DIRECTOR.md that still
had no working path. QD38 was not answered (already covered).
QD41, QD43, QD12, QD50, QD61, QD66, and QD67 were not answered or
marked. Q41, Q43, and Q34 were not marked. Kernel Q45 and kernel
Q40 were not given a QD home and were not answered. F8 and F10
were not answered.

Checked against R22 (every design choice recorded), R23, R24
(climb the 05 counter; lineage matters; the past is not rewritten),
R25 (face 00 is the registry root; a 00.counter is its own face),
and the axioms, especially 1, 6, 7, and 8. Also checked against
R3, R4, R5, R7, R18, and R21; seqpage-QUESTIONS.md S2, S4, and S5;
OPEN.md O12 and O13; kernel CONFLICTS.md K08; format.md; SEQ-GUIDE.md;
seqAddr.md; decisions.md (A1.7, A2.6, C8, F.1 S05, F.2); the
workflow-loop drafts; WORKING-PATH-QD17-QD21.md (D389) and
WORKING-PATH-QD29-QD33.md (D396, D397, D400); the core, seqpage,
the compute, the app, and the books.

---

## QD35. Should a .seq file list where borrowed faces come from?

Borrowed faces (from shelf, desk or kernel) are not in the file.
Now: `7`. Not listed.

**Best option:** Option C, sharpened: yes, but only as a worked-out
`inherits :=` line, never stored and never imported.

The file's content stays this book's own entries for this page
(the Now claim, D241, and S2). Nothing from another book is copied
in. Copying it in would make a copy pretend to be the source
(axiom 8) and would make the R3 round trip write the inherited
text into this book as its own (axiom 2: do not copy the parent).
That is rejected.

When the exporter has the lookup chain (the compute always does;
the CLI only when it is given the other books), the registry may
show one derived line, for example:

`inherits := 01 kernel 00.00.00.0051.01 draft, 04 kernel 00.00.00.0051.04 draft`

For each content face the page lacks locally and the A1.8 lookup
finds above: the face, the level, the source address, and its
state (R5: an inherited draft must still show it is a draft).
A1.7 already requires that a model state where inherited content
was found; this is the same fact, shown in the file.

The line never lists counted faces 05 and 06 (D389: a book's
tasks and notes are its own; the kernel's are read at the kernel
address). It never lists face 00 (the registry is the page's own;
R10, R25). It is never imported, never stored in the book, and
never drafted (format.md:102, D396, D397).

On read, the line is checked only when the chain is given. A
disagreement is a finding ("the parent changed since this file
was exported"), not a refusal. This is the one place the path
differs from seqpage.md:178, and it should say so. Books follow
the kernel live (A2.9), so a parent change must not make the
child's own, unchanged entries unreadable. That is the D367
shape: flag leftover derived values; only the page's own entries
can refuse a file. The same rule should apply to any derived
line that depends on other books (for example a derived `role`
or the offered `trail :=`).

The compute's `/page` already lists inherited faces with their
sources; `/page.seq` lists local faces only, and for a page this
book has no entries for, `/page.seq` is a 404 while `/page` shows
the inherited faces. The app still labels the .seq "every face".
Those two views should agree on content faces and their sources.
For a page this book has no entries for, the file is not this
book's page (R3: the .seq is a view of a book's page), so export
need not invent entry blocks; the compute may still show the
derived `inherits :=` line, and that view is never imported as a
create.

Axiom 7 ("Absence does not start a search") does not forbid this.
A1.8 is a lawful written connection through the address (axiom 8),
not a search from a hole's shape.

Today no real page has both local entries and inherited content
faces (the only overlapping page number is 0000, and a door never
falls through: D390), so the line would be empty on every real
page until a book writes its own face beside an inherited one.

An option Matthew may not have thought of (offer it, do not adopt
it): put the list only in an export header, or leave the file
alone and only correct the app's "every face" wording to "this
book's own faces". Both are smaller. A second offer is to include
the inherited face's entry number (`@n`), and a CLI
`export --books`, so a reader can open the exact source entry.

Reject copying inherited faces into the file (axiom 8, R3, axiom
2). Reject listing 05 or 06 in the line (D389). Reject plain "not
listed" as the final answer: it leaves the two views disagreeing
and ignores A1.7. It is fine as the state until the line is built.

This does not answer QD50, F8, D389's offered kernel-owned list
on the app board, or D390. It does not reopen QD17.

A smaller finding, not a requested rewrite: DESIGN.md:175 still
says nothing in crates/seqpage is committed; it is committed and
tested. A comment in the compute (`store.rs`) still says drafts
are not inherited, which R5 superseded; the code below it does
inherit a lone draft.

This depends on D389, D396, D397, and D367. It does not need
Matthew for the path. The "stale is a finding" rule is new, and
he can overturn it.

Working path, not a ruling.

---

## QD36. Should spaces at the end of a line be made visible in a .seq file?

Now: `7`. Kept as they are, not shown.

**Best option:** a new option C. Keep the bytes exactly, as D245
and the Now claim already say (R3 requires a lossless round trip;
D323 makes every byte of face 00, spaces included, part of its
fingerprint). Make trailing spaces visible as findings, with no
change to the file format.

Export and check report a finding that names each body line
ending in a space (for example, "line N ends in 2 spaces; some
editors remove them"). When a book comparison fails and the only
difference is trailing spaces, the error says so, instead of only
"the past is not rewritten". The same finding runs on `new`
blocks, and in the app's .seq box (it already pre-checks R4
characters in the same place).

This is needed because S4's "nothing is lost silently" is not
true in two cases I checked: a `seqpage check` without the book
accepts a file whose trailing spaces have been stripped, with no
finding; and in a `new` block there is no book entry to compare
with, so a strip changes the proposed body with no signal at all.
A one-space line (`|  `) stripped becomes an empty line (`|`),
which is a different body. For face 00, a lost space is a
fingerprint change (D323), which D367 would halt on once a
00.counter exists (R25).

I counted 138 stored bodies across the eight book files, and zero
of them end a line with a space. None of the 50 kernel face files
has a trailing space either. So this path moves no data.

Option C does not recover a `new` block's body after an editor
has already stripped the spaces: once they are gone, the finding
has nothing to report. That is why the next offer exists.

An option Matthew may not have thought of (offer it, do not adopt
it): write a body line that ends in a space in the same
JSON-quoted form field values already use (seqpage.md:152), for
example `|"faces: 04 draft  "`. The line then ends in a quote, so
editors cannot strip it. Today any body line that does not start
`| ` is refused, so no existing file uses that form, and no data
would move. It is a format change and makes body text less plain,
so it stays an offer. It is the option that actually prevents
silent loss on `new` blocks, which option C can only flag before
a strip.

A second offer, not adopted: extend R4 so a stored body line may
not end in a space (refused on write, like a tab). Zero existing
bodies would be refused. It would forbid Markdown's two-space
hard break (a backslash break still works). This widens a ruling,
so only Matthew can choose it.

Reject stripping or normalising spaces on export or import: that
breaks R3 and would change face 00 fingerprints (D323). Reject
plain "kept, not shown" as the final answer: the silent-loss
cases above are real. Reject a marker character inside `| `
lines (a trailing `$` or a middle dot): it is ambiguous with
real text, and a middle dot breaks R4.

This does not answer QD34 (which lines in the file may change)
and does not touch QD38. It does not widen R4.

This depends on R3, D245, D323, and D367. It does not need
Matthew for option C. Offer E (refuse trailing spaces on write)
is his alone.

Working path, not a ruling.

---

## QD37. Can you write a .seq file by hand to ask for a new page?

Now: `7`. Yes, it becomes a proposal.

**Best option:** Option A, sharpened: yes, a hand-written .seq is
a proposal like any other, for a page the lookup does not already
find.

Import always goes through the normal proposal queue (R3). Writes
are proposals; only the compute writes to the book
(format.md:17 and :18). The file is one more way to send a
proposal; the compute's validation is the gate (axiom 1). The
gates that already hold, and that I checked: D0 (a seated face
is drafted with `copy`, and `put` does not replace it); E7 (a
new face starts as `FF.draft`); format 4.1 (the book door is
written first); and A2.8 (pages 1000 and up must have a title).

A "new page" is a page number that no book in the lookup chain
already holds. A page the lookup already finds is not a new page;
it is a local difference, and stays under R7, R21, and D310
(today the compute approves it with an R7 finding; that is not
decided here). QD37's "yes" is not a back door for overrides.

Each new draft block should carry `reason:` (R5 follow-up; the
field exists, F12). A missing reason is a finding at check time.
`check` and `/check.seq` should run the same face 00 and R5
checks on `new` blocks that they already run on booked blocks, as
findings, so the person writing by hand sees them before booking.
Today they do not: the hand-written example
`docs/spec/examples/proposals/10.11.21.1002.seq` checks with zero
findings (no `address:`, no `state:`, no Registry card, no
`reason:`), and once booked the same page carries five findings,
with `why-draft := 7`. The example teaches the gap.

A finding, not a .seq rule: drafting.md:20 says a brand-new face
starts as an empty draft; a hand-written new draft with a full
body is approved today. JSON `/propose` behaves the same, so this
is a core gap, not a file-format one.

A case to raise to Matthew, not decided here: a hand-written file
creating `10.11.21.0057` (a page the kernel already has) was
approved in a dry run with only an R7 finding, "replaces the face
inherited from 00.00.00.0057.01 in place". That is D310
(provisional, on hold by R21). Under axiom 2 a contradicting
difference needs a named override, and R21 says no override pages
for now. Both faces are drafts today, so this is not yet two live
claims (axiom 1), but it would be once either is seated. The
path's "yes" does not approve that case; it leaves it on D310 and
R21, for Matthew.

An option Matthew may not have thought of (offer it, do not adopt
it): a "template export": the compute exports an empty .seq for
an unused page number, with the stamp fields and `reason:` lines
already present, so hand-writing starts from a correct shape
instead of from memory (the point of drafting.md).

Reject closing this door and allowing new pages only through the
app or a JSON proposal: that would make the .seq a one-way view,
with no safety gain, because the same proposal can already be
sent as JSON. Reject deciding the shadow case as a refuse-or-
approve rule here: that would decide D310 and touch R7, R21, and
F8, which are not answered.

This does not answer D310, R7, F8, QD38, QD42, QD54, or QD21. D0
is used, not changed.

This depends on R3, R5, D0, and D246. It does not need Matthew
for the path. The shadowing case should be raised to him, because
R21 and D310 disagree in effect.

Working path, not a ruling.

---

## QD39. Can a card's name go in an address, like ...1014.01.ham?

Raised as OPEN O12. No "Now" line. Option A: yes, a word after a
face is a card key (seqAddr.md:111). Option B: no, citing v2's
"Faces exist without titles".

**Best option:** Option A, sharpened: yes, as a read address to a
card inside a face, never a write target and never a title.

This is already settled spec. decisions.md:415 calls C8 settled,
except C8.7 and C8.10, which are not this question. C8.2
(decisions.md:420-421) and seqAddr.md:111 say a word after a face
is a card key, not a title: `10.10.11.1014.01.ham` is card `ham`
on face 01. A 3-digit group after the card is a brand number
(`ham.002`). The dictionary (C8.3) maps `ham.001` to that same
form of address, so the dictionary depends on it. The Bob test
(the MVP check) expects card addresses such as
`10.11.21.1001.01.bob`. The core grammar already parses them, and
the tests pass.

A card address is not a title, so faces still have no titles
(A2.1, and O12's v2 quote). A word after the page is a title; a
word after the face is a card key. Option B reads "title" as
"card key"; the clash is weaker than O12 states.

A card address is a pointer for reading and linking (the
dictionary, questions, and ask). Every write still names a whole
face or counter. The core already refuses a `put`, a tail, or a
drafting operation aimed at a card (rule "format 3.3": "`put`
writes a whole face or counter, not a single card"). That keeps
the seated address as `DD.SS.BB.PPPP.FF`.

A brand number after a card must agree with the card it reaches.
A mismatch is `7.8` (or elevated), never served (axiom 8: two
that are connected must agree; a connection that cannot be opened
is missing; do not repair it from a lookalike). Today it is
served: I read the compute's `/face` handler, and it matches only
the card key and ignores the brand number, so
`...01.bob.002` and `...01.cats.007` return the live card
(`bob.001`, `cats.001`). That is a finding, not a requested
rewrite. On a dictionary 03 face, `ham.002` selects one brand
line in the index; on a 01 brand card, the same form is a claim
about that card's `brand:` field. One grammar, two uses, both
are reads; the path names both, and both must agree.

A card address that no longer opens (the heading was renamed, or
the card was removed) is `7.8`, never repointed to a similar card
(axiom 8). Nothing checks inbound card addresses today.

An option Matthew may not have thought of (offer it, do not adopt
it): a derived "who points here" list per card, worked out by the
compute, so a heading rename shows its broken pointers before
promotion (the same shape as D396 and D397: derived, not stored).

Reject option B: it would break settled C8.2, the dictionary, the
common-questions answers, the compute's card route, and the Bob
test, with no rule that needs it. Inventing a second address form
for cards would be axiom 7's "never invent". Reject letting a
card address be a write target: that would bypass drafting (D0)
and the whole-face fingerprint (D323).

This does not answer C8.7, C8.10, QD50, QD12, or brand meters.
Kernel Q34 is not touched. F8 is not answered.

This depends on C8.2, seqAddr.md:111, and D323. It does not need
Matthew for the path. He can overturn it if v2 was meant to
forbid any word after a face.

Working path, not a ruling.

---

## QD40. Which band number is "build"?

One file says 05, the proposed band map says 03. Raised as OPEN
O13 and CONFLICTS K08. No "Now" line. Band 05 (pages 0500-0599)
is not face 05 (tasks). Under the map, N5 jobs pages hold their
packs on face 05 counters, which is why the two 5s get mixed up.

**Best option:** band 3 (pages 0300-0399, N3) is build; band 5
(pages 0500-0599, N5) is jobs (packs and returns, as face 05
counters). The "0523.timer (build)" wording in the A2.6 example
is stale example text, and is relabelled through its own drafting
step, not by a silent edit.

This is the map in the Director's workflow-loop .002 and .003
drafts (.002:45-47 and :54; .003:44 and :46). The .002 text says
the A2.6 examples are "not authority to overwrite this map" and
asks that their documentation be updated "through its own
authorized drafting path; do not silently edit SeqAddr." R18 (the
newest Director words on bands) frames a workflow as N3-N7, which
is that map. Kernel page 0057, face00.md, D400 ("N3 build pages
stay workflow"), and the built seqpage checker all use it: I
checked `face00.rs`, which derives `role` as `build` for page
numbers 0300-0399 and `jobs` for 0500-0599, and a 0523 workflow
page with a stored `role: build` is already flagged as disagreeing
with the derived `jobs`.

The "05 is build" reading has no source except one A2.6 example
sentence (`0423.timer` (dev) and `0523.timer` (build)), copied
into seqAddr.md:243, decisions.md:112, kernel 0051 (a draft), and
a few example files. F.1 S05 approved distinguishing set
counterparts from continuation pointers; the map itself is still
proposed (F.2, decisions.md:642). This path only fixes which
digit the word "build" means. The F.2 map stays proposed until
Matthew seats it. When it is seated, the A2.6 example is
relabelled through drafting (for example to "(jobs)"), with a
note citing this path; the kernel 0051 drafts get the same change
as a new draft step (axiom 6, R24: a new step, not a rewrite).
Kernel 0051 and 0057 currently disagree about which band is
build, but both are drafts, so this is not yet two live claims
(axiom 1). It should be fixed before either is seated.

No page in any book sits in band 3 or band 5, so no data has to
move. The core itself has no band role names; it only knows the
band digit and matches sets by CC and title (R18).

A sub-question, not answered here: what role a user-band page
such as 1303 takes. The .002 draft and R18's N-notation treat
N3 as the hundreds digit in any thousands band; the .003 draft
says a user band adopts a role by name in its band definition;
the built code derives a role only for 0300-0799. That is
Matthew's, with the seating of F.2.

An option Matthew may not have thought of (offer it, do not adopt
it): make the A2.6 example role-free (for example "0423.timer and
0523.timer are one set"), so the address law never names a
workflow role and the map lives only on the workflow page. That
separates seqAddr geometry from the workflow map, which is what
F.2 says (A2.7 allocation stays in force).

A note, not law: a file outside the repo (Prima's collected
workflow sources) suggests "build" was an older title of the 0500
door, later renamed to packs. That would explain why the A2.6
example says "0523 (build)". The repo itself does not record this.

Reject "band 5 is build": it contradicts the Director's drafts,
0057, face00.md, and the built checker, and it would collide with
N5 holding the packs on face 05 counters. Reject "both, by
context": two meanings for one role word is the two-readers
problem axiom 1 forbids. The role rule for user thousands is not
adopted here.

This does not seat F.2. It does not answer the other half of O13
(whether set membership is by number or by face 08 links; that
stays on F.2). It does not answer QD12, QD24, or kernel Q43. It
does not touch face 05. A smaller finding, not a rewrite:
workflow-loop.003.md:16 links a notes file that is not in the
repo (`7.8`).

This depends on R18, D400, and the workflow-loop drafts. It does
not need Matthew for "N3 is build". Seating the F.2 map, and the
user-band role rule, are his.

Working path, not a ruling.
