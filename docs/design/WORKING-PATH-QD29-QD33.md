# Working path: QD29, QD30, QD31, QD32, and QD33

**WORKING PATH.** Tester's recommended options, written 2026-11-12
at about 12:15 AM EST (America/Toronto) for Prima to record and for
the Director to review. They are **not rulings** and **not settled
law**. No kernel, core, seated faces, or Designer drafts were
changed.

These are the face00.md F5-F11 questions that still had no working
path. F8 (override pages) and F10 (types for page 0000, continuation
pages, and the common questions list) were not answered. QD34,
QD41, QD43, QD12, QD61, QD66, and QD67 were not answered or marked.
Q41, Q43, and Q34 were not marked. Kernel Q45 has no QD home and
was not given one, and was not answered.

Checked against R24 (climb the 05 counter; lineage matters; the past
is not rewritten), R25 (face 00 is the registry root; a 00.counter
is its own face, listing 00's fingerprint before each change), and
WORKING-PATH-LINEAGE.md. Also checked against the axioms, face00.md,
the settled decisions, the core and seqpage parsers, the kernel
builder, and the app.

---

## QD29. What is the exact layout of face 00? (face00.md F9)

Now: a stamp at the top, then a Registry card.

**Best option:** Option A, made exact. Face 00 is a stamp at the
top (lines between two `---` lines), then exactly one `## Registry`
card. That is already what R12, R19, the kernel, seqpage, and the
app all use. The path is to make the layout exact, not to change
the form.

Stored stamp fields are only the ones a person or a proposal
decides: `address`, `title`, `type`, `state`, `why-draft`, and
`axioms`. Values the computer can work out (`faces`, `lineage`,
workflow `role` and `set`, door `level` and `continues`, band
`contents` and `continues`) are shown as `:=`, not stored. A
leftover written one is a finding if it disagrees (the same reason
as D326 and R25: every stored byte in face 00 is a change recorded
onto 00, and writing a derived list would change 00's fingerprint).
The 00.counter list does not go in face 00 (R25, D357) and is not
written yet (D346).

The registry card's field lines run to the first blank line. After
that, free prose is allowed as a person-facing note, but is never
read as a field. No other `##` cards belong in face 00; if one
appears, it is a finding.

One field grammar for every reader: core, builder, seqpage, and
app. Today they disagree. The builder and the app accept dotted
keys such as `seat-05.01` and `why-06.01`; the core and seqpage do
not (`cards.rs`: a field key may not contain a dot, and a
non-field line ends the field block). I checked page 0054: the
registry has seven field lines (`faces`, two `seat-05.NN` lines,
and four `why-` lines). Because `seat-05.01` comes second and has
a dot, the core reads only `faces:` and treats the rest, including
later `why-01` lines that have no dot, as body text. Two readings
of the live record (axiom 1). The path is one grammar, and it must
accept face-spot keys that include a counter (`why-01` and
`why-06.01`), because those are the proposed stored why-lines
(D157, QD38) and counted faces already use a dot. A related
finding, not a requested rewrite: seqpage matches `why-NN` only
when the key is six characters, so `why-06.01` would still not
match even after the parser accepted the dot. Do not decide
whether `seat-NN` belongs in face 00 (kernel Q34 stays for
Matthew).

The door return link is one stored line (D368). D391 already calls
it `target:`; face00.md and seqpage call it `parent`. The path
uses `target:`, as already recorded, and treats `parent` as the
same D368 line under a second name. One name, not two.

Reject folding the stamp into the Registry card: R12 and R19 name
the stamp as its own portion, and every reader would have to
change for no gain.

An option Matthew may not have thought of (offer it, do not adopt
it): the stored part of face 00 is only the stamp, and `why-NN`
moves off 00 onto the entry's `reason`. That would give 00 the
shortest line (R25). It touches QD38 and kernel Q34, so it stays
an offer.

A smaller finding, not a requested rewrite: DESIGN.md still calls
face 00 "the door", and still says no kernel face is seated.

This depends on D322, D326, D357, and D368. It does not need
QD34, QD66, QD67, F8, or F10 answered.

Working path, not a ruling.

---

## QD30. What should the lineage line show? (face00.md F5)

Option A: the chain up (page, book, shelf, desk, kernel).
Option B: the trail of who allowed it. Option C: both. Should
face 08 links be in it? Now: the chain up only.

**Best option:** a new option D. The face 00 line is the chain up
only (Option A as the line), and it is derived, never stored. Face
08 links are not in it. The trail of who allowed it is walked from
records that already exist, not copied into face 00.

Axiom 6 says "the address is the line written down." Axiom 8
gives three lawful connections: inheritance through the address,
links both ways, and a named override. E6 says lineage appears on
face 00 and face 08, is kept by the compute, and is travelled
through structure and through time. Those are three kinds of
lineage, not one line.

The face 00 line is the first kind: the address chain, worked out
from the address (page, then book, shelf, desk, kernel).
`format.md` and A5.4 already say ancestor path lists are derived
and never written as entries. Seqpage already works this out
from the address. If a leftover `lineage:` is written and
disagrees, that is a finding (D367 shape; seqpage already flags
it).

Face 08 links are the second kind. They stay on face 08 and are
walked by the compute, once C4 is designed (QD50 is not assigned
and is not answered here). They must not be copied into the face
00 line: a link is a different kind of connection from inheritance
(axiom 8: a pointer never becomes what it points to), and putting
changing links into 00 would rewrite 00 (R25). A door has no face
08 at all (R10, D368); its return link is a face 00 line, and that
line is a connection, not part of the chain up. This answers the
sub-question without reopening QD66 or QD67.

The "who allowed it" trail is the third kind. It is walked from
the written records: book entries (`by`, `approved-by`, `trial`),
seat lines, pack `authorized` (QD31), `supersedes:` (D321), the
00.counter when it is built, and later an override's
`authorized-by` (R21 parks overrides for now). It must not be
stored as a line in face 00: every new seat or approval would
rewrite 00 to record itself, which is the loop R25 removed for
fingerprints. Copying those records into 00 would also make a
copy pretend to be the source (axiom 8).

Reject plain Option B or C as a face 00 line, for those R25 and
axiom 8 reasons. The chain up is enough while R21 holds (no
override pages); once overrides return, what governs a face can
differ from what is found, and the trail matters then. Do not
answer F8.

An option Matthew may not have thought of (offer it, do not adopt
it): the compute may show the trail as a derived view (for
example a `trail :=` line in the .seq, or an app panel), never as
stored text in 00. A second offer is to drop `lineage` from the
stamp field list entirely and keep only the derived `:=` line.

A finding, not a requested rewrite: the app never shows the
derived chain; it shows the stored stamp field, which no real
page writes, so every real page shows the line as not written.
Compute itself has no lineage value; only seqpage derives it.

This does not depend on a skipped question for the face 00 line.
The face 08 half waits on C4. Exact chain text at a desk or shelf
door waits on QD41, which is not answered here. QD09's axioms
address still cannot be parsed, so its chain cannot be derived
today; that is a note only.

Working path, not a ruling.

---

## QD31. What does a workflow page's approval record look like? (face00.md F6)

Now: not built.

**Best option:** a new option B. The approval is a write-once
note on the N4 page's face 06, written under the approver's own
identity, and closed bare (D337: notes are not seated). Its
address is the stable identifier S01 asks for (for example
`10.11.40.0403.06.03`). Face 00 shows only a derived
`approval :=` pointer. The pack's `authorized:` cites that
address, plus the blob of the approved N4 faces.

S01 says: "Approval is a lineage record with a stable identifier,
not a mutable flag on the page." Face00.md's proposed
compute-written `approval:` field on face 00 pulls against that:
it would change 00 at every new approval (R25), it cannot hold
S01's six parts, and a computer-written field for a person's
grant inverts axiom 1 (Compute enforces authority; it does not
grant it).

The record carries the S01 parts, and no new law: what it
approves (the N4 page address, plus the blob of each approved
face at approval time, never a commit id: D348), criteria,
scope, frame, delegation, and authority. It also carries `why:`
(axiom 4) and, when it replaces an earlier approval, a write-once
`supersedes:` (D321). "Who may approve" stays QD61, and what
"written permission" is stays QD43; those are not answered here.
The shape does not need them, but no real approval can be written
until they are.

The derived `approval :=` is the newest approval note that
nothing supersedes and whose approved blob still matches the live
N4 face. If the N4 face has changed since, the pointer is shown
as stale, and the old grant is never carried forward (S01: a
later N4 edit must not inherit authority by reusing the same page
address). This belongs on N4 (dev) pages only. On N3, N5, and N7
pages the approval is reached through the set (the pack's
`authorized:`), not repeated (workflow-loop.003.md: lineage runs
from the design back to its approval).

This follows D374 (a written decision under the authority's
identity, preferably a separate note the return can cite, so the
core can check who wrote it), D321, D326, R25, and D365 (do not
invent a new counted face). N4 face 05 stays for design questions
(S12).

N4 face 06 is also where the lead's session notes live
(workflow-loop.003.md). An approval is a formal grant, not a
session note. They may share the face, distinguished by a kind
(for example `kind: approval`), and they do not share the
meaning. The note is written by the approver, not by the lead.

This is a different record from an R2 seat `approved-by`. F.1
already says a design approval is not an N4 runtime grant. Keep
the two apart in name, place, and checks.

Reject a card on N4 face 04 or 01: approving would change the
very blob being approved. Reject a face 08 link as the grant: a
link is a connection, not a grant, and C4 is not designed.

An option Matthew may not have thought of (offer it, do not adopt
it): a new book operation `approve`, carrying the fields on the
entry, like seat `approved-by`. The core could check who wrote it
at the operation level, but an entry is not addressable as a
seqaddr, so a pack could not cite it by address, and it would mix
S01 grants with R2 seats. A second offer: if Matthew wants formal
grants fully apart from session notes, a dedicated page in the
set, still not a new counted face.

Kernel Q45 (every pack today says `authorized: 7`) becomes
answerable once this shape exists. It has no QD home and is not
answered here.

Working path, not a ruling.

---

## QD32. What owner kinds can a system page have? (face00.md F7)

Proposed: kernel-only, desk-local, book-local. Now: `7`.

**Best option:** a new option B. Owner class is a field on each
law card (`rule` cards, C8.9; and the type-definition cards,
C1.4), as the settled spec and the core already do. The system
page's face 00 does not store `owner:`. E9's three names stay:
`kernel-only`, `desk-local`, `book-local`. Their meaning is one
rule: the owner class names the lowest level that may hold its
own version of that law. `kernel-only` means no desk, shelf, or
book may differ (this is what the core already enforces,
`validate.rs`). `desk-local` means a desk may differ, nothing
below it. `book-local` means a book may differ. Any difference
below the kernel still needs a named, approved override (C5.4),
which is off under R21. During this build, only `kernel-only`
has an effect, and only when a kernel card actually carries the
field.

Face00.md puts `owner` on the system page's registry. C1.4, C8.9,
and the core put it on cards. Two places that can disagree about
who may change the same law would be two live claims (axiom 1).
The path keeps the settled place (the card) and drops the page
field. If a summary is useful, the computer may show a derived
`owner :=` (for example the strictest class among the page's
cards); that is an offer, not stored in 00 (same R25 reason).

Reject putting owner on both the page and the card, with the page
as a default: a card silent on owner would silently inherit a
page claim. Reject owner by user level number (00, 01, ...):
levels 02, 03, and 05-09 are undefined (QD06, not reopened), and
that mixes "who" with "where".

An option Matthew may not have thought of (offer it, do not adopt
it): add `shelf-local`, so the classes follow every level of the
lookup chain (kernel, desk, shelf, book; C5.2a). That would make
the "lowest level" rule read cleanly at every step. It is not in
E9, and C5.2 has no separate authority level for a shelf, so it
stays an offer.

A finding, not the path: no kernel card carries `owner:` today
(D381 already noted this; the C1.4 type-definition cards on 0054
say "owner: kernel-only" only as prose). The lock protects
nothing until a card carries the field. E9's source,
`claude/kernel-notes.md`, is not in the repo, so the three names
cannot be opened at their origin (`7.8`).

This depends on D381 and on R21. It does not answer F8 or how an
override names its target. It does not need Matthew for the
three-name path; the shelf class is only an offer.

Working path, not a ruling.

---

## QD33. What does the "code" page type mean? (face00.md F11)

Now: "A page whose faces describe code."

**Best option:** a new option B, with a pick for the overlap with
workflow pages. `code` means a page that describes code which
lives in a repo, under the section 3.1 laws Matthew already
decided: the book keeps the why and the description; code bodies
are not stored in the book; face 01 says what the module is, and
face 02 its files and interface; face 08 links each file by repo
path, with the revision it was last checked at; the computer
checks that each linked path exists, and a path that cannot be
opened is `7.8`, never repointed to a similar file; the registry
stores `repo:`, the repository those links point into. Those are
different laws, so `code` stays a type (D319: add a type only
when the page lives under different laws).

A page has one `type`. An N3 build page describes code (3.1) and
also sits in a workflow set (it needs `role`, `set`, and the
set's approval lineage). The path is: N3 build pages stay
`workflow` and follow the 3.1 laws because of their band role;
`code` is for code pages outside the workflow map (for example a
desk documenting a library). The other reading -- N3 pages are
`code`, and set and role come from the band and the address
(R18) -- would need workflow's `role` and `set` fields on the
`code` type, mixing two law-sets. That reading is not adopted.

Reject the present one-line meaning on its own: "a page whose
faces describe code" says nothing a page must or must not do, so
it is not a type under D319. Reject dropping `code` and using
only `workflow`: C1.4 lists `code` as a settled starting type,
and code can be described outside a workflow band. Reject making
`code` a `kind` of `general`: 3.1 gives distinct laws, so D319
says type, not kind.

An option Matthew may not have thought of (offer it, do not adopt
it): pin each face 08 file link by blob as well as commit (the
D348 lesson), so the link can be opened in the published history.
A second offer is a derived "links checked at" view, not stored
in face 00.

A finding, not the path: no page anywhere uses `type: code`, and
nothing tests it. Face 08 storage is still open (C4, QD50), so
the path check cannot be built yet. Face00.md and seqpage give
two different one-line meanings; the path above replaces both.

This depends on D319. It waits on C4 for the face 08 links. It
does not answer QD12; the "code lives in the repo" line is
already a Director decision (workflow-loop.003.md:70). The N3
type pick is a working path Matthew can overturn; it is not
blocked on him.

Working path, not a ruling.
