# Working path: QD04, QD06, QD07, QD14, and QD15

**WORKING PATH.** Tester's recommended options, written 2026-11-11
at about 10:15 PM EST (America/Toronto) for Prima to record and for
the Director to review. They are **not rulings** and **not settled
law**. No kernel, core, seated faces, or Designer drafts were
changed.

These are the next open Director questions that still had no working
path, from the top of the list. QD12, QD61, QD66, QD67, Q41, Q43,
and Q34 were not answered or marked.

---

## QD04. Is face 00 itself in its own face list? (kernel Q38)

The face list leaves out face 00. Option A (used today): the stamp
`state:` is the page's state, and face 00's own state comes from its
file. Option B: face 00 is listed like any other face.

**Best option:** Option A, sharpened. No: face 00 is the list, so it
is not in it. The stamp `state:` is the page's state, worked out from
the content faces and checked (R12, D364). Face 00's own standing is
shown separately as `registry`, never in `state:` (D322). This is
what seqpage already does, and it matches kernel Q38's Option A
(`registry :=` as a separate value). This does not reopen QD03
(written vs derived); it only says what the derived list contains.

Option B would put face 00 back among the seatable faces, which R25
and D322 moved away from. Under D326 a derived entry would not change
face 00's fingerprint, so it is harmless as bytes, but it is
self-referential and clashes with the builder's special `00.<tail>`
key.

A kernel stamp that says `draft` on a page with a seated face (for
example page 0052) is a finding to clean up, not a reason to refuse
the book (same shape as D367). This also bears on kernel Q40 (page
state when face 00 is a draft but a face is seated), which has no QD
home. Under this path, a draft face 00 does not by itself make the
page a draft. Q40 stays open; Prima should decide whether it needs a
QD home.

Another option, not the working path: face 00 could have no
draft/seated standing at all, with its history only on 00.CC and git
blobs (the logical end of D322). That depends on 00.CC existing,
which D357 says not to write yet, and it touches QD66 and QD67, which
stay for Matthew. Offer it to him; do not adopt it here.

This does not depend on QD12 or F02-F10.

---

## QD06. Is the sign-in design right?

Today every write needs a personal token; the token says who you are;
only your token approves as Director; the name "compute" cannot be
used from outside; tokens sit in `books/.identities`, never in git.
Also open: what user levels 02, 03 and 05-09 may do. No options are
listed; it is a "please confirm" question.

**Best option:** Keep the token sign-in as built for the build stage.
It already stops forged Director approvals and outside writes. It
knows who you are, not what you may do. Levels are not in the
identity file, and C5.2's 01-vs-04 desk scope is not enforced.

An option Matthew may not have thought of (offer it, do not build it
now): split the secret from the grant. The token file keeps only
secrets (who you are). Who holds which level where (Director, level
00, level 01 in a given book) becomes a granted record written in the
live record, with lineage, approved by the Director. That follows
axiom 1 (the live record is where authority is kept) and axiom 6 (a
change that is not recorded did not happen), and it gives revocation
and history. Today's Director is only a name in a gitignored file,
with no grant history.

**Needs Matthew (one line):** what levels 02, 03 and 05-09 grant
(C5.2, `docs/spec/decisions.md`, the open line under C5.2a). Nothing
in the repo defines them, so they cannot be worked out here.

Smaller gaps, not a ruling: the R2 trial author is a self-asserted
line in a file, not tied to a token (same shape as `approved_by`);
tie it to a committed file or to the writer's token. D286 is out of
date: it says there is no `/whoami` route, but one exists now.
`scripts/dev.sh` prints the director token to the terminal.

This does not depend on QD12 or F02-F10. QD07 depends on this:
level 00 cannot be enforced until identities carry levels, or until
a "who holds 00" record exists.

---

## QD07. Who may change the kernel book? (kernel Q17)

Option A: only an admin at level 00. Option B (used today): anyone,
through a proposal the Director or R2 approves. Only "kernel-only"
cards are locked. C5.2 is already settled that level 00 reaches the
kernel, so today's B is a departure from that settled spec.

**Best option:** a new option C: open proposals, gated go-live, one
door. Only level 00 may change what is live in the kernel (the spec
already says so). During this build stage, level 00 is the Director,
or an R2 build-stage seat with a hostile trial. Anyone with a token
may propose a kernel draft: a draft is untrusted (axiom 9) and not
law. Anything that changes what is live in 00.00.00 (seat, promote,
retire, a page or door tail move) needs that same level-00 grant.
The kernel book should have one way in (the builder, from reviewed
kernel files). A `/propose` aimed at 00.00.00 is flagged, or turned
into a kernel draft, rather than appended.

Reject plain B, because it leaves retiring open and has two writers.
Retiring a seated face or a page currently needs no approval
(approval runs only on seating; a `tail` to `retired` is not a
seat). Plain A matches C5.2 but cannot be enforced until QD06
carries levels.

Gaps for the builders, not a ruling:

- `owner: kernel-only` is enforced for other books, but no kernel
  card carries that field, so the lock protects nothing today.
- The compute can append to a book the builder regenerates: two
  writers with no lawful connection (axiom 1), and a possible
  silent rewrite (axiom 6). This was read from the code, not run
  as a test.
- Retiring a kernel face or the kernel door, by any token holder,
  is also untested, and is worth a test.

This does not depend on QD12 or F02-F10. Enforcing it needs QD06
levels, or at least a "who holds 00" record. It unblocks core-trial
finding 8 in part.

---

## QD14. In R14, which "door" did you mean? (kernel Q32)

R14: a face may be seated while its page's door is a draft. Option
A: the page's own face 00. Option B: the book's door page 0000.
Option C: both. Today both are allowed.

**Best option:** Option A as the meaning of R14, with today's
behaviour unchanged (both remain allowed). When Q10 was asked,
"door face" was the name for face 00 (R1 wording, before R9 and
R10 named the door as page 0000 only). R14 answered Q10 as written,
so it meant the page's own face 00. The kernel already reads it
that way (0052.01). Nothing forbids seating under a draft book door
either, and the kernel does that today, so keep allowing it.

Reject B, because it misreads the question. C is fine as behaviour
but loses the historical meaning.

An option Matthew may not have thought of: after R25, face 00 is
the live registry rather than a draft (D322, still 7). Under that
path, "a seated face under a draft face 00" stops being a real
state, and R14 is met automatically. The book door 0000 holds only
face 00 (R10), so the same reasoning covers it, and B needs no
separate rule.

The wording fix on 0052.01 (work card w04 on 0052.05.02) must go
through a new draft and a new seat (D344, D369), not a patch:
0052.01 is already seated, and the card still points at
`0052.01.draft.md`.

This is consistent with the QD04 recommendation and D322. It does
not depend on QD12 or F02-F10. It unblocks 0052.05.02 w04.

---

## QD15. May a task start straight at "pack"? (kernel Q21)

One spec line says only the computer moves a task to pack. An
example in another file starts a task at pack. Today, starting at
pack is allowed.

**Best option:** No. A task starts at draft, and only the computer
moves it to pack, after the pack lint. That is the same line in
the .002 and .003 loops, and the approved gravity rule (S09)
counts on packs leaving draft through the computer. Today anyone
can create a counter straight at pack (`check_counter_create`
allows it; `apply_put` does not check who) and skip the lint, the
S01 authority check, and the S09 gravity gate. A client cannot
move a draft to pack, but can skip that step by creating at pack.
The `format.md` example that starts a task at pack is a finding,
not law.

The way to enforce this (a new option C, not a different rule): a
put at `pack` is accepted only when the writer is the computer,
the same gate as `draft -> pack`. The computer records it as two
steps in one proposal: put at draft, then a lint move to pack, so
every step is visible in the line (axiom 6).

Reject "yes" (today), because of that bypass and the clash with
axiom 1 (Compute enforces it) and approved S01 and S09.

**Interim note for Prima:** no pack lint is built yet. If this
gate is switched on before a minimal computer lint exists (the
hard header checks in .003 section 8), no pack can be created
through the HTTP path at all. Sequence it: build a minimal lint,
then switch the gate. Section 8 templates stay 7.

This does not need F02-F10: the lint row cites no F number, and
the same row is in .002. It leans lightly on QD12 (is .003 law),
but the pick holds on .002 plus approved S09 alone. It does not
touch Q41 or QD61.

---

## What this does not do

It does not edit the kernel, the core, seated faces, or Designer
drafts. It does not answer QD12, QD61, QD66, or QD67. It does not
mark Q41, Q43, or Q34. It does not write a 00.counter or a new 05.
It does not define levels 02, 03 and 05-09. It does not implement
the lint gate, the kernel-write gate, or the grant record.

---

## For Matthew

Face 00 is the list, so it is not in the list. The page's state
and face 00's own standing are two different things.

The sign-in we have is fine for this build stage: it knows who
you are. Who may do what should, later, be a granted record in
the live book, not only a secret file. What levels 02, 03 and
05-09 may do is still yours to say.

Only level 00 should change what is live in the kernel. Anyone
may propose a draft. Retiring a kernel page needs the same
approval as seating one. During this build, level 00 is you, or
an R2 seat after a hostile trial.

When you said a face may be seated while its "door" is a draft,
you meant the page's own face 00. Seating under a draft book
door stays allowed too.

A task starts as a draft. Only the computer may move it to pack,
after it checks the pack. Starting straight at pack would skip
that check.

---

## Status

Still `7`, not law. Pending Director review. No files in the
kernel, the core, or the seated packs were changed. QD67 stays
for Matthew. Q41, Q43, and Q34 were not marked.
