# Face 00's counter (00.CC)

**DRAFT.** This is a draft for the Director to read. It is not settled law.
It fills in what R25 leaves open. Anything marked PROPOSED is a builder's
proposal. Anything marked `7` is open.

Lane: DESIGN (Designer). Source ruling: R25 in `docs/spec/DIRECTOR-RULINGS.md`.
Related: axiom 6 (`Axioms.md:23`), R24 (how 05 climbs), kernel Q51, QD05,
QD66, QD67, QD03, QD16.

This file was first written as a proposal for how 00.counter climbs and
whether those faces are seated (QD67, QD66). Tester's hostile pass found
a listing cascade (F7) and two related holes (F8, F12) in
[R23-R25-lineage.md](R23-R25-lineage.md). Sections 7-9 address those.
They are still proposals, not law.

The QD03 working path ([WORKING-PATH-QD03.md](WORKING-PATH-QD03.md), D326)
is the working answer to F7: the face list is derived, not written into
face 00, so adding a 00.counter no longer forces a registry edit. That
path is not a ruling. The kernel builder has not been changed to match
it yet.

QD67 stays for Matthew, with both climb options. This draft recommends
one of them. That is not an answer. [F13] [WORKING-PATH-LINEAGE.md]

---

## 0. What R25 already decides

Face 00 is special. It is the registry root for the page. It is not seated
the same way as other faces. [R25]

Changes are still recorded onto face 00. [R25]

A second face, a 00 counter (`00.CC`), holds a list of face 00's
fingerprint as it was just before each change. [R25]

The steps are: snapshot that fingerprint first, then make the change,
then count and compare: the old fingerprint, the change, and what 00 is
now. [R25]

This keeps the line (axiom 6) without needing face 00's own fingerprint
to stay frozen. [R25] [Axioms.md:23]

The list must be its own face, not lines inside 00. Writing the list
inside 00 would change 00's fingerprint again, which is the problem we
are solving. [R25]

Seat records may still be written onto 00. The line of 00 itself is kept
on the 00.counter face. This answers Q51 and QD05. [R25]

Two things stay `7` (R25's held questions):

1. Whether 00.counter faces are themselves seated in the normal way. (QD66)
2. How the list climbs (`00.01`, `00.02`, ...) when a new fingerprint is
   added. (QD67)

---

## 1. Why this is needed

A face 00 holds seat records for the other faces on its page (`seat-NN:`).
Writing any of those records changes face 00's bytes (its fingerprint).
So a seated face 00 could never keep matching the fingerprint a trial
passed. That is Q51. [kernel/QUESTIONS.md Q51; `docs/trial/kernel-trial-4.md`
finding 3]

R25 solves this without moving the seat records off face 00, and without
pretending those lines are not part of 00's bytes. Face 00 may change.
The 00.counter keeps the earlier fingerprints, so the line is visible.

The fingerprint is the git blob of face 00's file. [D323] If a 00.counter
and git history disagree about face 00's past, neither silently wins:
halt and raise it. [D324] [axiom 1]

---

## 2. PROPOSED: how the list climbs (QD67)

**Option A (recommended).** Each snapshot is a new counter: `00.01`, then
`00.02`, and so on, up to `00.98`. Once a 00.CC face is written, it is
not edited. The "list" is the series of these faces, in order.

This matches how face 05 climbs (R24) and axiom 6: a change is a new
step in the line; the past is not rewritten. [R24] [Axioms.md:23]

**Option B (not recommended).** One 00.counter face holds the whole list,
and a new line is added to it each time. That would change that face's
fingerprint each time: the same kind of problem face 00 has.

Tester noted that the Director's words lean toward one list (F13). That
is a lean, not an answer. QD67 stays for Matthew, with both options
shown. This draft still recommends Option A, and does not treat that as
settled. [WORKING-PATH-LINEAGE.md]

**After 98.** Counters run 01-98 only. [R9] [seqAddr.md:24]. What happens
after 98 is already asked as QD16. The same question applies here. `7`.
Face 00 changes more often than a pack, so the cap may arrive sooner
for 00.CC than for 05. [F11] Under the QD03 path, F7's extra listing
snapshot is no longer needed, which helps, but the cap is still urgent
for face 00.

### What each 00.CC face holds (PROPOSED)

Plain ASCII only. [R4]

A 00.CC face is write-once. The fields below are card fields on that
face, not a page stamp. Only face 00 carries a stamp. [R12] [F14]

It names:

- `address:` the full address, ending in `00.CC` (for example
  `00.00.00.0051.00.01`). On a door page, the same shape is
  `0000.00.CC`, as an exception to R10 so the line can live next to
  the face 00 it measures. [D325]
- `prior:` the previous counter (`00.01` has none; it starts the line)
- `fingerprint-before:` the git blob of face 00's file (the full
  40-hex), taken just before the change. [D323]
- `change:` what is about to be written onto face 00, and why (for
  example a new `seat-05:` line). A void (section 9) says the named
  change was not made.
- `axioms:` 6 (lineage), and 9 if this snapshot has not yet been checked

It does not need to store the fingerprint after the change. The next
00.CC's `fingerprint-before` is what 00 became. The computer compares:

- the old fingerprint, stored on this 00.CC
- the change, stored on this 00.CC and also visible in the book
- what 00 is now (or what the next 00.CC recorded as `fingerprint-before`)

Writing the "after" fingerprint back onto this 00.CC would edit it,
which option A does not allow.

### The steps, in order

1. Read face 00's current fingerprint (the git blob of its file).
2. Write a new 00.CC face that stores that fingerprint and the coming
   change. Under the QD03 working path (D326), this write does not
   change face 00, because the face list is not stored as bytes in 00.
   See section 7.
3. Then make the change to face 00.
4. Then count and compare: old fingerprint, the change, and what 00
   is now.

If the change is refused before it is made, do not rewrite the 00.CC.
Write a void, as in section 9.

If the change was made and the compare fails, that is a defect. Do not
rewrite the 00.CC to make it fit, and do not void a change that
happened. Raise it. [Axioms.md:23] [Axioms.md:25]

---

## 3. PROPOSED: whether 00.counter faces are seated (QD66)

**Option A (recommended).** No. A 00.counter is write-once evidence. It
is not seated the same way as other faces. Face 00 itself already has
this kind of exception. [R25]

Why: if we seat `00.01` the normal way, that seat record is written
onto face 00. [R25: "seat records may still be written onto 00"]. That
write is itself a change to 00, so we would need a new snapshot
(`00.02`). If we then seat `00.02`, the same thing happens again. That
is a cascade.

A 00.CC face is final because it is never rewritten, not because a
seat line is added to face 00. A trial can still check that the
fingerprint it names really was face 00's bytes just before the named
change. [axiom 9]

**Option B.** Yes, a 00.counter is seated after a trial, like any other
face. Then we need a rule that stops the cascade. That rule is not
written. `7`.

---

## 4. What this is not

This draft does not seat, un-seat, or change any face. It does not
change the kernel builder or the core. Those wait until the Director
rules on QD66 and QD67, or until Prima says to build from this proposal
under R2 as a provisional `7`. The QD03 working path also has not yet
been built into the kernel builder.

This draft does not answer QD66 or QD67. It only proposes. Prima takes
those questions to the Director. QD67 stays neutral for Matthew.

Kernel Q51 itself lives in `kernel/QUESTIONS.md` (KERNEL lane). This
draft does not edit that file.

Face 00's stamp and registry fields stay as in `docs/spec/face00.md`.
A later pass can add 00.CC there once this is settled.

This file does not rewrite Tester's research note or any WORKING-PATH
file.

---

## 5. What builders can do now

Follow R25 as already written:

- Do not seat face 00 the same way as other faces.
- Seat records may still be written onto face 00.
- Before changing face 00, snapshot its fingerprint; after, compare.

Until QD66 and QD67 are ruled, treat the climb and the seating of
00.CC as `7`. The proposal above is the recommended shape, not law.

Until the kernel builder matches D326, adding a 00.CC file will still
trip the written `faces:` check in the builder. That is a known gap,
not a reason to write `faces:` back into 00. The working path is:
derive the list, and treat a leftover `faces:` line as a finding if it
disagrees. [D326] [WORKING-PATH-QD03.md]

The address, standing, and void rules in sections 7-9 are also `7`.

---

## 6. Open questions

- QD66. Are 00.counter faces seated the normal way?
- QD67. How does the 00.counter list climb when a new fingerprint is
  added? Both options stay; this draft recommends Option A.
- QD16. What happens after counter 98? The same question applies to
  00.CC, and is urgent for face 00. [F11]
- QD03 is a working path (D326), not a ruling. The F7 alignment in
  section 7 depends on it.

---

## 7. F7: writing a 00.counter must not change face 00

Tester found: writing a 00.counter is itself a change to face 00,
because face 00 must list every face on the page. The builder requires
the written `faces:` line to equal the files. So step 2 of this draft
(write a 00.CC) would already change 00 through its registry. The
snapshot would never be "just before the change" (R25). Either it
misses the registry edit, or that edit needs its own snapshot, and so
on. This listing cascade happens even if a 00.CC is never seated. [F7]

**PROPOSED, aligned with D326.** The working answer is the QD03 path:
nobody writes a `faces:` list into face 00. The computer works the
list out from the faces that exist (the files, and the book), and
still checks that derived list against seat lines, `why-NN` reasons,
and book entries. A leftover written `faces:` line is a finding if it
disagrees, not the source of truth. [WORKING-PATH-QD03.md] [D326]

Under that path, adding a 00.counter does not edit face 00. The
snapshot in step 1 stays "just before the change" that step 3 will
make (a seat record, or another real registry write). The listing
cascade is broken.

This is a working path, not a ruling. The kernel builder has not been
changed: it still requires a written `faces:` line. Until that changes,
the cascade is still real in the code. This draft does not edit the
builder (Pass 12 owns that lane).

QD04 (is face 00 itself in the list) is, on this path, a display
question. It is not reopened here. [WORKING-PATH-QD03.md]

---

## 8. F8: address and standing for a write-once 00.counter

Tester found: no address or state today can hold a "write-once, not
seated" 00.counter. A bare `00.NN` is treated as seated and needs a
seat record, then is refused, because only face 05 counters may be
seated. The only tails are workflow tails (`draft`, `pack`, `open`,
`return`, `review`). So QD66 Option A would end up as permanent
drafts, which axiom 9 reads as untrusted. The core also refuses
counters on face 00: counters live on counted faces only (05 and 06).
Face 00 as a counted face is a new case, and `00.00` is already the
registry, not a board. [F8]

**PROPOSED address.** The address is `PPPP.00.CC` (for example
`00.00.00.0051.00.01`). On a door page it is `0000.00.CC`, as the
working-path exception to R10. [D325] Face 00 is not a counted face
in the 05/06 sense: there is no separate board at `00.00`, because
`00.00` is the registry itself. The 00.CC counters are a special
case, allowed so the line lives next to the face 00 it measures. The
series is just the 00.CC files that exist, derived the same way as
the face list. [D326]

The core's "no counter on face 00" and the builder's "bare means
seated" would need this exception. That change is KERNEL and CORE
work, not this lane, and it waits for a ruling or for Prima to say
to build this as a provisional `7`.

**PROPOSED standing.** A 00.CC face has no workflow tail. It is bare.
For 00.CC only, bare means write-once evidence: not a draft, not a
seat, and it does not need a `seat-00.NN:` line on face 00. A trial
can still check it (axiom 9) without promoting it to a seat (QD66
Option A). This is the same kind of "neither draft nor trial-seated"
standing the lineage working path already proposes for face 00
itself. [D322]

A new tail word (`record`, or similar) is an alternative, if a
visible tail is wanted. It would need a grammar change. This draft
does not recommend inventing one unless the Director wants it. `7`.

---

## 9. F12: voiding a snapshot when the change is refused

Tester found: this draft writes the snapshot before the change, and
says not to rewrite the 00.CC face. If the change is then refused, a
write-once record of a change that never happened stays forever.
Axiom 6 says "A change that is not recorded did not happen." The
reverse case -- recorded but not made -- had no rule. [F12]

**PROPOSED.** Do not rewrite or delete the snapshot. Write the next
00.CC as a void. That void is a new step in the line. [axiom 6]

The void face is also write-once. It names:

- `prior:` the snapshot it voids
- `void:` the change that was not made, and why it was refused
- `fingerprint-before:` the same git blob as the voided snapshot's
  `fingerprint-before`, because face 00 did not change

The voided snapshot stays visible. The next real change starts after
the void: its `prior` is the void, and its `fingerprint-before` is
again that same blob (00 is still unchanged), unless a later lawful
change has happened.

A void uses a counter, so it counts toward the 98 cap (QD16 / F11).
That is accepted, so the refusal stays in the line.

If the change was already made and the compare fails, that is not a
void. It is a defect: halt and raise it. [axiom 1] [section 2]

---

## 10. Status

Still a draft, still `7`, not law. Sections 2 and 3 (QD67, QD66) are
unchanged in their recommendations. Sections 7-9 align F7 with the
QD03 working path, and propose standing (F8) and void (F12). Tester's
note and the WORKING-PATH files were not rewritten.
