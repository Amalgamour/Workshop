# Working path: QD17, QD18, QD19, QD20, and QD21

**WORKING PATH.** Tester's recommended options, written 2026-11-11
at about 11:00 PM EST (America/Toronto) for Prima to record and for
the Director to review. They are **not rulings** and **not settled
law**. No kernel, core, seated faces, or Designer drafts were
changed.

These are the next open Director questions that still had no working
path, from the top of the list. QD34, QD41, QD43, QD12, QD61, QD66,
and QD67 were not answered or marked.

---

## QD17. Does a book see the kernel's tasks and notes? (kernel Q15)

Option A (used today): yes, like any face. Option B: no. Tasks
belong to their own book.

**Best option:** Option B, sharpened. A book's tasks and notes are
its own. The kernel's tasks and notes belong to the kernel. A book
may still read them at the kernel address (`00.00.00`). A2.9 still
holds: books follow the kernel live, so the kernel's work is found
there. The book's own face 05 and face 06 boards show only that
book's counters.

R22 and R24 already treat face 05 as one page's own work pack and
lineage: "Each page gets a face 05 that says what was learned
building that page." The kernel's work on a kernel page is not this
book's work. Axiom 8 says a copy or a link never becomes what it
points to, so inherited kernel work must not become the book's own
board. The trial's claim that this inheritance is "not a lawful
connection" is too strong: axiom 8 also says inheritance through
the address is a lawful way to connect. The problem is adoption,
not visibility.

Plain Option A, as it behaves today, has problems I checked
against the core. If a book has its own `0057.05.01`, the plain
board shows only the local counters, but `0057.05.02` still walks
on to the kernel's `05.02`: the board and the counter lookup
disagree. A matching number also hides the kernel's unrelated
counter at the same number. A book cannot act on those inherited
tasks; a write is rejected unless it uses the kernel address. That
is a confusing view, and it is not what R22 describes.

An option Matthew may not have thought of (offer it as a way to
show the kernel's work without adopting it): if a listing on the
book's page is useful, show a separate "inherited, kernel-owned"
list, labelled `origin: kernel`, never mixed into the book's own
board.

Do not write a "do not inherit counted faces" rule that would
catch a future `00.CC`. Face 00 is not a counted face (D357), and
a 00.counter is not to be written yet. That is only a flag.

A smaller finding, not a requested rewrite: `DESIGN.md` still says
drafts are not inherited. That is superseded by R5.

This does not depend on QD12, F02-F10, or a skipped question.

---

## QD18. When a book retires its own copy of a page, does lookup go on to the parent? (kernel Q16)

Option A (used today): yes, the parent's copy is found. Option B:
no. Retired means "not here", so it comes back missing.

**Best option:** Option A, sharpened. When a book retires its own
copy of a page, lookup goes on to the parent (shelf, then desk,
then kernel). Retiring an override means "I no longer have my own
copy," not "hide the parent." That fits axiom 2 (inherit what is
agreed; a difference that contradicts the parent needs a named
override) and R21 (no override pages during this build). The
retired body stays readable at `.retired`, as history (axiom 6).
This is what the core already does for pages, and it matches D141.

Reject Option B for this build. Using retirement as a mask on the
parent would be a contradicting difference, which axiom 2 says
needs a named override, and R21 parks overrides. After overrides
return, Matthew could add a second kind of retire that means
"remove, do not re-expose." That is an offer, not the path now.

The door is different, and this is part of the path. The door page
`0000` is the book's identity (R1). It must never fall through to
the shelf's door. A retired book answers "retired" for its own
door, and refuses further writes except un-retiring. A check
against the core showed that retiring the door makes
`10.11.21.0000.00` answer with the shelf's door, and that a
retired book still takes writes. Those are findings to fix. They
are not a reason to refuse Option A for ordinary pages.

A smaller finding, read from the code, not run as a test: compute
`/page` does not skip an explicitly retired page, so it can still
list the local faces and hide the parent, while core `resolve`
(`/face`) skips and walks on. The two disagree.

Approval on retiring is already a gap on D381 (QD07). A check
against the core confirmed it: a user can retire the kernel door
with no approval, and it is accepted. That does not reopen QD07
here.

This does not depend on F02-F10 or a skipped question. It touches
D381 only as confirmation.

---

## QD19. Can a draft be the return link for a pointer? (kernel Q19)

Option A (used today): yes, drafts count (R5). Option B: no, the
return link must be seated.

**Best option:** a new option C. They go live together, and the
seated body wins while a draft is being worked.

A draft may hold a return link while the pointer is also still a
draft. Staging is allowed: R5 says a draft is found, and R8 says a
draft exists only while the face is being drafted.

A seated (live) pointer needs a seated return link. The two sides
go live together. Axiom 8: a connection is lawful when it is
linked both ways. Axiom 9: a draft has not yet faced its trial; do
not trust it as it stands. R5 is about finding faces, not about a
draft standing as a live lawful connection.

When a seated return link already exists, check the seated body
(R5: the seated face wins). A working draft that drops the link
must not break the live connection. Today's `view()` prefers the
draft, so a working copy that drops the link is rejected even
while the seated face still has it. A check against the core
showed that. That should change.

For a door, "must be seated" has no clear meaning. Under D368 the
return link is a line on face 00, and under D322 face 00 is the
live registry, neither a draft nor trial-seated. A written
`target:` line on face 00 counts. This does not wait on QD66 or
QD67, and does not answer them.

Reject plain Option A for a live pointer: it is too loose given
axiom 9. Reject plain Option B for staging: it would block draft
work, and it is unclear for doors.

If a logged withdraw of a draft is later built (D375), withdrawing
a draft return link must recheck A5.3. Today a draft-only face
cannot be retired or withdrawn.

This does not depend on F02-F10. The door part stays consistent
with D322 and D368, which are already working paths.

---

## QD20. Does the "every 01/02 card needs a 04 card" rule apply to task lists? (kernel Q20)

Today this is skipped for task lists. The kernel's Q20 asks a
slightly different question: does the rule apply to counted 01 and
02 faces.

**Best option:** No. The rule does not apply to task lists, and it
should not. Task lists are faces 05 and 06. The rule (C3.2,
`seqAddr.md`) is only about faces 01 and 02. Task and note cards
already do not need a 04.

The kernel's Q20 is moot under D365 (QD11): counted-ness is a
fixed law (faces 05, 06, and dictionary `0012.03`), so 01 and 02
are never counted. The skip in the core is dead code under the
default Policy; it only runs if a special Policy marks face 01 or
02 as counted. Leave deleting that skip to the builder. Do not
adopt "counted 01/02 are skipped" (D169) as the path, because that
would clash with D365.

A finding, not the path: a `type: rule` or `type: schema` card
placed on a 05 or 06 counter escapes the 04 rule (a check against
the core accepted it). An option Matthew may not have thought of:
follow the card type, not the face. Either such a card needs a 04,
or that type is not allowed on a task list. Offer it; do not
adopt it here.

A smaller finding, not a requested rewrite: `DESIGN.md` still says
the core demands a local 04 card. That was already fixed (the 04
may be inherited).

This depends on D365 standing. It does not depend on F02-F10 or a
skipped question.

---

## QD21. Does the computer's own write need a seat approval? (kernel Q23)

Option A (used today): no; the computer writes doors and worked-out
pages, and is exempt on a bare put, never on a promote. Option B:
yes; every seat, whoever writes it, carries `approved-by`.

**Best option:** a new option C. Remove the exemption. Every seat
carries `approved-by`, whoever writes it, including the computer.
Promote stays gated, as it is today. The computer's writes that
stay exempt are only compute-only steps (the lint move from draft
to pack, the close from review to bare, a recovery return), which
do not seat a face (D383, D374). Derived listings (boards,
contents lists, ancestor lists) are never written as entries, so
they need no exemption (`format.md`).

Axiom 1: Compute enforces authority; it does not grant it. D201's
examples do not hold: derived pages are not entries, and a door is
a seat. The exemption is a match on the name `compute`. At the
core, a bare put by `compute` into the kernel, with no approval,
is accepted (a check against the core showed this). That clashes
with D381: the kernel book should have one way in, and anything
live in the kernel needs a level-00 grant. The HTTP layer has no
such exemption (read from the code), so the core and the HTTP path
disagree. In the real books, no entry is `by: compute`; the kernel
is seeded with `approved-by` on seats. The exemption covers
nothing in production and only opens a bypass at the core.

An option Matthew may not have thought of, for doors: when a
granted user approves a proposal that creates a book, the computer
may write the door as part of that same proposal. The approval is
carried, not exempted.

Reject plain Option A. Plain Option B is close; C is B with the
compute-only steps and the derived listings kept clear.

Two confirmations of earlier gaps, not new paths: retiring still
needs no approval, including the kernel door (now tested, D381).
A bare closed counter, which is how a seated pack is stored, also
needs no approval from anyone (it is outside `seats_a_face`). That
bears on D320 and D383, not on this question.

"Who may confirm" a recovery return stays 7 on QD61, which is not
answered here. Enforcing level 00 already has a working path
(D380, D381). This does not depend on F02-F10 or QD12.
