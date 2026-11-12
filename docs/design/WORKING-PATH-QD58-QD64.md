# Working path: QD58, QD60, QD63, and QD64

**WORKING PATH.** Tester's recommended options, written 2026-11-12
at about 5:10 AM EST (America/Toronto) for Prima to record and for
the Director to review. They are **not rulings** and **not settled
law**. No kernel, core, seated faces, or Designer drafts were
changed.

These are four questions from QUESTIONS-FOR-DIRECTOR.md. QD65
(whether Matthew wants to check the Ask word lists and scoring)
stays with him; no path is given. QD59, QD61, and QD62 already
have paths and were not reopened. QD53-QD57 (D424-D427), QD54
(D375), QD52 (D421), and QD40/D407 were not reopened. QD01's
leftover on notes (06) and dictionary seating was not answered.
QD50, QD38, QD41, QD43, QD12, QD66, and QD67 were not answered
or marked. Q41, Q43, and Q34 were not marked. Kernel Q44 and
kernel Q45 were not marked. Kernel Q40 was not given a QD home.
F8 and F10 were not answered. F.2 was not seated. The D310/R21
shadow case was not decided. No 00.counter was written.
Kernel-design.md was not promoted. R4 was not reopened. D418
was not reopened.

Checked against R22, R23, R24 (Matthew's words "05.01-06"),
R25, R2, R4, R5, R9, R11, R21, and the axioms, especially 1,
2, 4, 6, 7, 8, and 9. Also checked against A1.4, C8.5, C8.8,
D179, D93, D127, D04, D407, OPEN.md O44, O46, and O49, the
brief (AGENTS.md), format.md, workflow-loop.003.md, the core,
the compute, the kernel, and the sample books.

QD58, QD60, and QD63 have no "Now" line. QD64 already says
`7`: none, so page 0012 is not in the kernel; this path
confirms D179 and sharpens it.

---

## QD58. Should face 05 split into tasks (01-49) and tickets (50-99)?

Linked to QD01. Raised from O44. Log: D127. No "Now" line.

**Best option:** no. Do not split face 05 by number. Keep one
climbing 05 line, 01-98, as R24 describes (05.01 onward, then
seat 05, then 05.07 from the seat, then reseat). What a
counter is (a lessons note, a pack, a rework, a replacement)
is said by its card type and its written links, not by its
number. Single jobs that "tickets" would hold are already
work cards (`w01`, `w02`, ...) inside the pack (S07,
workflow-loop.003.md:122-126). Findings from a return that
concern another page are booked on that page as 05 work in
its next pass (decisions.md:612), not on a reserved number
range.

Why: the proposed ticket range ends at 05.99, and R9 already
rules that out (counters run 01-98 only; addr.rs:835-837 and
state.rs:417 refuse 00 and 99). E9 itself marks the split
"Against A1.4" (decisions.md:604): counters are not an axis,
so a number range should not carry a meaning. R24 and axiom
6 want one climbing line; two ranges on one face would make
time order and number order stop agreeing. S07 already moved
single tasks into cards. "Ticket" is never defined in the
Workshop spec. The seated 05.01 and 05.02 counters would not
need renumbering (they already sit in 01-49), but the
clashes with R9, A1.4, and R24 are enough. Keeping one line
needs no code change and touches no seated counter.

**Offers, not the path:** a derived view that groups a page's
05 counters by kind (using a card type or `kind:`), so the
split becomes a filter and no number ranges are reserved.
Boards are derived and never written (R9). If a real ticket
queue is wanted, put it on its own page in the jobs band N5
(D407), where each ticket is its own 05 counter: separate
pages, not separate ranges on one face (axiom 2).

**Findings, not implemented:** OPEN.md:250, decisions.md:604,
and the QD58 heading still say 99; under R9 the top counter
is 98. "Ticket" has no definition in the Workshop documents.

This does not answer QD01 or its leftover on notes (06) and
dictionary sections, QD59 (D369), QD44/D412, or what face 05
means beyond R22-R24. Kernel Q41, Q43, and Q44 were not
marked.

Working path, not a ruling.

---

## QD60. What hardware?

Raised from O46. Log: D93 (a bundle with QD56 and QD57, which
already have paths and are not reopened). No "Now" line. D93
says nothing about hardware beyond the one word.

**Best option:** treat hardware as a build choice the brief
already hands to the builders (AGENTS.md:5), recorded with
its why (AGENTS.md:45; R22), not as a ruling to wait for.
The choice to record is what is already built: one ordinary
computer runs the compute and the reader; books are plain
text files on that computer's local disk, which must honour
fsync; the compute listens on loopback only; models run
elsewhere as clients over HTTP (D426); no special device is
needed. This stays `7` until Matthew rules. One point is
left for him: whether Workshop must be reached from more
than one machine. That needs TLS first (main.rs:39: the
compute has no TLS, and tokens would cross the network in
the clear).

Why: the brief asks the builders to make the hardware
choice and record the why. A Director question should be
kept for what only Matthew can say (where it must run, who
must reach it). What is already built is the honest
description, and nothing in the BUILD-LOG yet records it as
a hardware choice.

**Offers, not the path:** state the disk need as a test, not
a named machine: any disk that passes the crash-cut test
(core-trial:12) is fine (AGENTS.md:45, portability). Do not
keep live book files in a cloud-sync folder or on a network
share: two machines editing a synced book is two copies that
changed apart (QD57/D427), and claims only work on one disk
(format.md:50). If more than one machine is ever wanted,
keep one compute on one machine and let others reach it,
rather than running a compute on each machine against shared
files (format.md:15-18).

**Findings, not implemented:** nothing records which
operating systems were tried; only this Linux computer is
evidenced.

This does not answer QD56 (D426), QD57 (D427), or snapshot
policy (D414).

Working path, not a ruling.

---

## QD63. Should accented letters come back later?

R4 is plain characters "for now". Raised from O49. Log: D04.
No "Now" line.

**Best option:** R4 stands as written. Accented letters do
not come back now. Whether and when storage widens is
Matthew's call alone (R4 is his ruling; axiom 1). "For now"
is his own phrase ("a simple storage design for now"). "May
widen later" is from the Read of R4, not from his words
(DIRECTOR-RULINGS.md:15-16; O49 quotes the Read). Ask him
only when a real need appears, for example a person's name
or a word that must be kept as typed, and ask it then as a
narrow choice, not by reopening R4. Before a widening could
even be offered as ready, five things must be trialled
(axiom 9): a hostile test that a crash cutting inside an
accented letter is repaired safely (core-trial finding 1 was
fixed by R4, not by repair code, and there is today no such
test); a new book format version, so old readers refuse new
books cleanly (log.rs:282); one normalisation rule on write,
so two spellings of the same letter do not become two brand
forms; dictionary and Ask rules for accented words (C8.6
has sections for a-z only); and the widening reaches
content only. Addresses, titles, card keys, tail words,
identities, and tokens stay plain ASCII in every case,
because they are grammar, not content.

Why: Matthew asked for a simple storage design for now. The
one storage failure seen so far (core-trial finding 1) was
exactly an accented letter cut in half. Keeping grammar
ASCII is what lets the address parser stay one exact parser
everywhere (format.md:145). Old books stay ASCII, which any
later widened reader can still read (axiom 6).

**Offers, not the path:** allow accented letters in card
bodies and face text only, never in addresses, titles, or
card keys. Or store accents as ASCII escapes (`\u00e9`) so
every byte stays ASCII and a crash cannot split a character;
the Read of R4 refuses those escapes today (log.rs:297-298),
so this too would be Matthew's to allow.

**Findings, not implemented:** O49 quotes the Read of R4 as
if "may widen later" were Matthew's words; only "for now"
is. There is no live test of UTF-8 crash repair, only of
refusal.

This does not reopen or narrow R4. It does not touch
trailing spaces (QD36/D404) or the .seq format approval
(QD34).

Working path, not a ruling.

---

## QD64. Which words go in the kernel's base dictionary?

Now: `7`. None, so page 0012 is not in the kernel. Raised
from BUILD-LOG:20. Log: D179.

**Best option:** D179 holds, sharpened. Keep the kernel base
dictionary empty, and page 0012 out of the kernel, until
Matthew gives or approves a word list. This is "empty for
now because no words are ruled" (axiom 7), not "there is no
base dictionary": C8.5 is settled and stays
(decisions.md:443). Which words go in is Matthew's (axiom
1; C8.1). When he does give words, the base should hold
only words that mean something special in Workshop, not
ordinary English, which C8.8 step 4 already covers. Each
such word points to a kernel brand card on face 01 of the
kernel page that explains it (C8.4). Before the first base
word is written, the word lookup must check the book before
the kernel: today /brands returns every book in the chain
together (store.rs:622-667), which is not C8.5's "Local
first".

Why: nothing in any source lists a word (BUILD-LOG:20,
kernel Q50, MAP hole 5). Inventing words would break axiom
7. D179 is a provisional hole, not a claim that C8.5 should
be dropped. The seated kernel pack 0055.05.02, work card
w02, already waits for "ruled words". A kernel 0012 written
today would be found from other books, as a draft if not
seated (R5); inheritance of kernel faces is now live, so a
careless base entry would reach every book at once.

**Offers, not the path:** a tick-list drawn only from words
Matthew has already defined in rulings, for him to tick or
strike: `door` (R1), `band` (R13), `registry` (R10, R19),
`draft` (R8), `pack` (R23, R24). Each would point to the
kernel law page that explains it. Or the kernel's own law
terms (face, page, counter, tail, seat, brand, card) as the
base. Or leave the shared words on each desk book rather
than the kernel, which would need him to read C8.5's
"kernel" as "the nearest container that has one".

**Findings, not implemented:** BUILD-LOG:57's "books inherit
nothing from the kernel yet" is out of date: that was the
effect when kernel faces were all drafts; R5 was later
applied (BUILD-LOG:92), /page includes inherited drafts
(BUILD-LOG:142), and some kernel faces are now seated.
/brands is a union over the chain, not local first
(store.rs:637-667). Two cards on one face cannot share a
name (decisions.md:300), so a kernel brand card must not
collide with a law card already on that face. Kernel Q50 is
the kernel twin of this question; it was not marked.

This does not reopen QD53/D424. It does not reopen D418,
A1.4, or the dictionary's 03.01-03.09 layout. It does not
answer the QD01 leftover on seating dictionary sections, or
the R16/R9 tension on 03.00. It does not add a kernel page
0012, and it does not invent a word list.

Working path, not a ruling.
