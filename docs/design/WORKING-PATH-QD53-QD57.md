# Working path: QD53, QD55, QD56, and QD57

**WORKING PATH.** Tester's recommended options, written 2026-11-12
at about 4:10 AM EST (America/Toronto) for Prima to record and for
the Director to review. They are **not rulings** and **not settled
law**. No kernel, core, seated faces, or Designer drafts were
changed.

These are four questions from QUESTIONS-FOR-DIRECTOR.md that still
had no working path. QD54 already has a path (D375) and was not
reopened. QD58, QD60, and QD63-QD65 were left for a later pass,
as Prima asked. QD50, QD38, QD41, QD43, QD12, QD61, QD66, and
QD67 were not answered or marked. Q41, Q43, and Q34 were not
marked. Kernel Q45 and kernel Q40 were not given a QD home and
were not answered. F8 and F10 were not answered. F.2 was not
seated. The D310/R21 shadow case was not decided. QD40/D407 and
QD52's path (D421) were not reopened. QD64 was not reopened.

Checked against R2 (a face may be seated after a trial; this does
not answer an open Director question), R3 (the book is the real
stored copy; import goes through the proposal queue), R5 (drafts
are found), R8 (drafting exists so seated work is not replaced
from memory), R11, R15 (a brand card on face 01 needs no 04
card), R21, and the axioms, especially 1, 2, 4, 6, 7, 8, and 9.
Also checked against C1.4, C2, C8.4, C8.5, C8.8, C8.10, D0,
D319, D414, format.md, drafting.md, brands.md, OPEN.md O39, O41,
O42, and O43, the core, the compute, the kernel, and the sample
books.

QD53, QD55, and QD57 have no "Now" line. QD55 also has no Log
line and no D-row. QD56 already says "Web calls only" at 7; this
path confirms that and sharpens it.

---

## QD53. Where does a new word meaning (brand card) go?

Raised from O39. Log: D74. No "Now" line.

**Best option:** a new meaning goes on face 01 of the page that
explains it (C8.4, C8.10). If that page is not known, the
computer asks the person which page, and never picks one itself
(decisions.md:525, first option; axiom 1; axiom 7). The person
may name a page that already exists, or a new page; the number
and title are theirs, as with the sample page 10.11.21.1001.
The card stays in the book, not the kernel (C8.5,
decisions.md:443; QD64 is not reopened). It starts as a draft.
The person confirming the meaning is its review
(decisions.md:503; drafting.md:41). A draft is found and shows
as a draft (R5). Whether that confirmation also seats the card
is left open (R2, QD21, QD61). A card may move later without
losing its name: the brand number stays the same; only the
dictionary line changes, and the old spot stays in the log
(decisions.md:432; axiom 6; axiom 8).

Why: this is what C8.10 already says, made exact. The person
holds authority over where meaning lives; the computer enforces,
and does not choose a home. No page is invented. A default
terms page is not the path: it needs a page number Matthew has
not given, and one terms page can hold only one meaning of each
word, because a card is titled with the word (decisions.md:435)
and two cards on one face cannot share a name (decisions.md:300;
cards.rs:105). The ham example already uses three pages
(brands.md:27-29). Writes to a card address stay refused (D406).

**Offers, not the path:** a default terms page per book, for a
word's first meaning only, with the page number Matthew's to
choose. A "new meaning" route that adds the card and the
dictionary entry together, all or nothing (format.md:100).

**Findings, not implemented:** one terms page can hold only one
meaning of each word, so C8.10's second option is incomplete
for a second meaning. Words that start with a digit or a symbol
have dictionary sections (03.01-03.09) but cannot be card keys
(cards.rs:54-69; BUILD-LOG:42), so they cannot have a brand
card titled with the word. A card cannot be written alone
(state.rs:410-411); adding one to a page whose face 01 is
seated reopens the whole face and needs a new R2 seat. /ask
finds brand cards anywhere by `type: brand` (askq.rs:64-79),
not through the dictionary. No route yet creates a brand card
or a dictionary entry (lib.rs:242-260). 0055.05.02 w04 bundles
QD52 and QD53; both paths are still 7. The sample page 1001
holds `cats` on a page titled `bob`.

This does not answer QD52 (D421 stands), who may confirm a
meaning or whether that seats the card (QD61, QD21, R2), the
terms page number, meters and failure counting, QD64, QD39 /
D406, QD27, or QD10.

Working path, not a ruling.

---

## QD55. May a page type turn drafting off, for scratch pages?

Raised from O41. No "Now" line, no Log line, and no D-row.

**Best option:** yes, but only for a new `scratch` page type,
and nothing on a scratch page is ever seated. Drafting protects
agreed work from being rewritten from memory (drafting.md:7;
R8). A scratch page has none. Every write is still a new line
in the book; nothing is edited in place (format.md:61, :63;
axiom 6). A scratch page is not found through inheritance, and
nothing may cite it as a reason or an authority (axiom 1;
axiom 8). To make scratch work real, it is copied into a
normal page through drafting and review, like any other change
(D0; R2; axiom 9). This is a new page type, not a `kind`,
because its laws are different (D319). C1.4 already lets a
type say whether drafting is required (decisions.md:288;
drafting.md:46). Existing types keep drafting on.

Why: the question is whether a type may turn drafting off, and
C1.4 already allows a type to carry that rule. Turning it off
on a page that can be seated would let a rewrite from memory
become law, which is what drafting exists to stop. A
never-seated scratch page has no agreed work to lose, and
cannot outrank a live record. The log still keeps every
version. Promotion to real work still needs a trial.

**Offers, not the path:** keep scratch outside the book
entirely, the way the trials already use scratch clones; only
what is kept is proposed into a book as a new face. A
per-type drafting switch in the core, instead of one
book-wide switch, if Matthew takes this path. An optional
`reason` on each scratch write.

**Findings, not implemented:** QD55 has no Now line, no Log
line, and no D-row (R22 asks every choice be recorded). The
core's drafting switch is book-wide (state.rs:22-23, :52),
not per page type, and no page type carries any rule yet
(face.rs:131-136). R5 says drafts are found, so a scratch
page in a desk or shelf book would today be found by child
books; the "not found through inheritance" rule is not
built. The word "scratch" is not defined in the spec, only
named at drafting.md:46. QD55 sits on QD42 (drafting is
built and on by default, still 7).

This does not answer QD42, QD02, whether R2 can ever apply
to a scratch page (under this path it cannot; making it real
is a copy), QD54 / D375, D365, or D400.

Working path, not a ruling.

---

## QD56. Should clients talk to the computer by web calls
(HTTP), MCP, or both?

Now: `7`. Web calls only. Raised from O42. Log: D93, D264.

**Best option:** the Now line is right for today. HTTP is the
one way in. If MCP is wanted, it is a thin adapter outside
the computer that makes the same HTTP calls, so it is not a
second door. The adapter passes on the caller's own token
and never holds one that can approve or seat (axiom 1;
CONTRACT.md:40, :42). "Web calls only" is a build choice,
not Matthew's words: it comes from Prima's lane contract
(CONTRACT.md:10), the compute build (BUILD-LOG:53), and
D264. MCP is not built anywhere in the repo. This stays 7
until Matthew rules.

Why: one computer owns the books, and writes go through one
queue (format.md:15-18, :41-42). A second door would have
to agree with the first (axiom 8); an adapter that only
makes the same calls cannot disagree. The R2 gate and the
tokens live in one place. MCP stays unbuilt (axiom 7) until
it is wanted.

**Offers, not the path:** an MCP adapter as above, only when
it is wanted. A single list of HTTP routes, so an adapter
can be generated from them, not hand-copied.

**Findings, not implemented:** "Web calls only" has no
Matthew source and is not a prior working path. OPEN.md O42
cites BUILD-LOG:58, which is the HTTP status-code line.
D264 cites BUILD-LOG:53, which describes the HTTP build.
Neither line says "only"; "only" comes from nothing else
being built. D93 bundles QD56, QD57, and QD60 in one row.
format.md:142 says agent clients are "any"; the build has
exactly one transport.

This does not answer QD60, remote access and identity
(D257), whether an MCP adapter is wanted, or anything about
the app.

Working path, not a ruling.

---

## QD57. How are two copies of a book that changed apart
merged?

Raised from O43. Log: D93. No "Now" line.

**Best option:** two copies are never merged by mixing their
lines. The computer keeps the shared start and re-plays the
other copy's later writes as new proposals, one at a time,
through the normal checks, on top of the live copy
(format.md:65, :117-125). The copy the computer holds is
the live one. Nothing in it is rewritten (axiom 6). Each
replayed write keeps who made it and when, and says which
copy it came from (axiom 4; axiom 6). If a write is refused,
or two live claims meet, the computer stops and asks the
person; it does not choose (axiom 1; format.md:42). The
other file is kept as it was, as history, and its snapshots
after the shared start are not used (D414). Until this is
built, a copy that changed apart is held as its own book,
not merged (format.md:15-18). "Keep both sides" was already
set aside, because two agents could both win a claim
(format.md:53). A plain git merge of two book files would
break the in-order numbering the reader requires
(log.rs:292-294).

Who may approve bringing a fork back in, and whether a fork
of the kernel may be merged at all, are for Matthew. Until
he rules, and until a merge is built, the path above is the
rule for how a merge works, and a copy that changed apart
stays its own book.

Why: the book is an append-only log (format.md:60-61). Mixing
lines would rewrite the past and break the reader. Re-playing
the other copy's later writes as new proposals inherits the
shared start and writes only the difference (axiom 2), through
the same checks every write already faces (axiom 9: being in
the other copy is not proof). Two live claims halt (axiom 1).
D414 already says a snapshot is never trusted over the log.
R3 is respected: the book is the real copy, and .seq import
already goes through the queue (BUILD-LOG:70).

**Offers, not the path:** treat a copy that changed apart as
a new book linked back, as a named step before any merge;
every container is already a book (format.md:21), and
exporting is copying the file (format.md:30). Merge page by
page through .seq files, which already works for new blocks
(BUILD-LOG:70). Mark the shared start (the entry number, plus
a fingerprint of the log up to that entry) when a copy is
made, so the start can be found later without guessing.

**Findings, not implemented:** if the book file is longer than
the compute wrote it, the compute cuts it back
(store.rs:940-941). The comment talks about a partial last
line (format.md:67; BUILD-LOG:143), but the code cuts any
extra bytes, including whole valid lines added outside the
compute. Those entries would be lost with no record. A
shorter file is refused (store.rs:937-939). This clashes
with axiom 6. A git line-merge of two book files breaks the
reader's numbering (log.rs:292-294); format.md:44 calls
appends "clean additions" and the result a fork, but a git
merge of two forks is not clean. Kernel and sample books are
rebuilt from Markdown (build.mjs); today a "merge" of kernel
content is a git merge of `.md` files, which is not the R3
shape. D93 bundles QD56, QD57, and QD60 in one row.

This does not answer the D310/R21 shadow case,
first-folder-wins (BUILD-LOG:56), QD46 / D414 (only used;
D414 already says it does not decide fork reconciliation),
QD66, QD67, who authorizes a merge, kernel forks, QD61
(writes across books), or archive policy (format.md:157).

Working path, not a ruling.
