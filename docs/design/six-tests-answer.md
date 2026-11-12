# Design answer to the six tests

**DRAFT.** This is a draft for the Director to read. It is not settled
law. Anything marked PROPOSED is a builder's proposal. Anything marked
`7` is open.

Lane: DESIGN (Designer). This is the design answer to Tester's six
tests ([R23-R25-six-tests.md](R23-R25-six-tests.md);
[WORKING-PATH-SIX-TESTS.md](WORKING-PATH-SIX-TESTS.md), D344-D348).
Those paths are not rulings. This file is not a second law.

It covers three things: how a 05 climb is recorded (R24, axiom 6);
how lineage cites still work in the published copy and on GitHub;
and how 00.counter (R25) can be its own face that the core can
read. The detailed 00.counter design stays in
[00-counter.md](00-counter.md) (D359, adopted as D360). The 0051
and 0052 door-lessons slice stays in
[parked-door-lessons.md](parked-door-lessons.md) (D355). This file
does not rewrite those drafts, or any WORKING-PATH file.

Related: R23, R24, R25, axiom 6, axiom 8, Q53, Q67, D320, D321,
D344, D345, D346, D347, D348, D352, D355, D357, D358, D359, D360,
D361, D362, D370. QD67 stays for Matthew. Q41, Q43, and Q34 stay
unmarked.

This draft does not edit the kernel or the core. It does not write
a new 05 counter, a 00.counter, or any seated face.

Tester's evaluation of this draft is now a working path (D370).
The one real improvement: when you open plain face 05, keep the
derived listing of every counter, and mark which seated pack is
current. Do not replace that listing with only the current pack's
body. Section 1 records this. Section 3 also points at
[WORKING-PATH-CHECK-CORE.md](WORKING-PATH-CHECK-CORE.md) (D362)
instead of restating D346's "or". These are working paths, not
rulings.

---

## 1. How a 05 climb is recorded (tests 1, 2, and 6)

When a seated pack needs to change, write a new counter. Do not
change the file that is already seated. The old pack stays in the
line. That is R24, and it aligns with axiom 6.

**A new counter, not a change at the same address.**

Today the builder still allows a seated pack to be replaced at the
same address (test 1). `--check` exits 0. The old blob leaves the
live registry and the book. Only git history and the old trial
file still name it. That clashes with R24.

**PROPOSED, aligned with D320 and D344.** Use a new counter for
the update (05.03 in the general case; R24's later-update example
is 05.07). The builder should refuse a same-address re-seat: if a
still-seated address has a distinct earlier seat blob, that is an
error unless a new counter is used. Pass 12's every-blob walk
already has the history; it should run on still-seated faces, not
only on un-seats. Q67 Option C stays as the un-seat naming rule,
and is still needed for history.

R24's "05.01 through 05.06" is the shape of the first stretch, not
a count every page must fill. Pages already seated at 05.02 climb
to the next free pack counter.

**How the current best pack is marked, among 05.01, 05.02, 05.03.**

Today, a new seated 05.03 builds clean, but resolve shows 05.01,
05.02, and 05.03 all "closed". Nothing marks which is current.
`predecessor:` is free text; no code reads it (test 2). So R24
cannot work at resolve time yet.

**PROPOSED, aligned with D321, D345, and D370.** The new seated
pack carries a write-once `supersedes:` field, naming the pack
it follows by address plus blob (the full 40-hex), never by
commit id. The builder and the core read that field. The older
pack stays in the line; it is not rewritten, and it is not
un-seated.

When you open plain face 05 (resolve of `...05`), keep the
derived listing of every counter. That is already what the core
does (`resolve.rs:182-183`, `state.rs:296-297` `board()`, R9:
a counted face has no door). Mark which seated pack is current:
the one nothing later supersedes. Opening that counter shows
the pack body.

Do not replace the listing with only the current pack's body.
Face 05 is counted. Replacing the listing would hide the line.
That is the same family as D351 and D357, in a third direction.
[D370] [WORKING-PATH-SIX-TESTS-ANSWER.md]

Use the word `supersedes:` for this, not `predecessor:` (unread)
and not `prior:` (`prior:` already means the previous 00.CC on
the 00.counter).

If two seated packs would both count as current, or the
`supersedes:` chain cycles, halt (axiom 1). There must be
exactly one current pack.

The computer tells packs from lessons because packs carry
`supersedes:` (the first new pack starts the chain). Notes and
lessons stay out of the "which pack is current" rule (D345):
they do not carry that field. Face 05.01 is notes, not a pack.
On 0051 and 0052, the planned 05.03 is also lessons, so the
next pack there is 05.04 and it names 05.02 (D352,
[parked-door-lessons.md](parked-door-lessons.md)). On a page
where 05.03 is the next work pack, 05.03 is the one that names
05.02. Until a page has climbed once, current is not yet
machine-readable. Do not edit old packs to add the field. The
new pack names the old one. [D370]

**Stale packs (test 6).** The same climb carries the stale-card
work already picked in D348: close the already-done w01 cards,
fix the broken counts, and re-point 0052 w02 at a `0052.04.draft`
re-trial. A trial of a pack should run those mechanical
done-tests before the seat, so a pack is not seated already
stale. Following 0052 w02 as written today would mean editing a
seated face; the climb avoids that. The new counters are not
written here. That is later KERNEL or PACKS work, still `7`.

---

## 2. Lineage cites that still work when published (test 5)

A cite in a seated pack must still open in the published copy and
on GitHub, not only on this computer.

Today, 50 commit cites in 19 of 22 seated 05 files fail in a
fresh publish clone and on GitHub `prima/build` ("Not a valid
object name"). All 50 pass locally. Five distinct commits are
involved, not only `fae009a`. That is axiom 8: the written
connection cannot be opened there. A publish rewrite changes
commit SHAs; it does not change blobs. Blob cites already
resolve in all three copies.

**PROPOSED, aligned with D348.** In the new counter, cite
lineage by address plus blob (the full 40-hex), never by commit
id. For a file that is not a seated face (for example a parked
pack, or a trial), cite by path plus blob. This is the same
rule Q53 already used for trials. Do not add more local-only
commit cites.

Do not edit the already-seated packs to fix the 50 cites. Write
the corrected cites on the new counter (section 1). The
temporary map of today's publish SHAs in the six-test results
may change at the next rewrite; do not treat it as the cite
form.

---

## 3. How 00.counter can be its own face the core can read (tests 3 and 4)

R25 says the 00.counter is its own face, not lines inside face
00. The core must be able to read the book after that face is
written.

Today that is not true (test 3). A bare `00.01` is refused by
the builder ("a 00 counter may not be seated"). A `00.01.draft`
builds clean once face 00 lists it, then the core refuses the
whole `00.00.00` book (A4.4: face 00 is not a counted face).
Every resolve fails, even an address in another book, because
`load_world` loads every book. The core's `repo_books` test
catches this; `--check` does not.

**PROPOSED, aligned with D346, D357, D359, and D362.** Do not
write a 00.counter in the shared repo until the builder and
the core agree on the address and the standing. The core is
the only judge; `--check` must run the core's replay; do not
reimplement A4.4 in JavaScript. See
[WORKING-PATH-CHECK-CORE.md](WORKING-PATH-CHECK-CORE.md)
(D362). The `repo_books` test should be in the pre-commit set
as a second gate, not a substitute.

When that agreement is implemented, do not solve A4.4 by making
face 00 a counted face. Do not add it to `always_counted`, and
do not put `(page, 0)` into `Policy.extra_counted`. Allow
`00.CC` as a special case without `is_counted(page, 0)` being
true, so plain face 00 stays the registry. The recommended
standing (F8: for 00.CC only, bare means write-once evidence)
stays as written in [00-counter.md](00-counter.md). Tester
adopted that update (D360), with no further improvements.

The fingerprint check (test 4) is also in that draft, section
11: the stored value is the blob at the parent of the commit
that adds the 00.CC, never a commit id; the before-field check
is only half of R25. This file does not restate that section.

QD67 (how the 00.counter list climbs) and QD66 (whether those
faces are seated the normal way) stay for Matthew. This draft
does not answer them, and it does not write a 00.counter.

---

## 4. Status

Still a draft, still `7`, not law. This file assembles the
working paths D320, D321, D344-D348, D352, and D357-D360 into
one design answer, adopted as a faithful assembly (D370) with
one improvement: keep plain face 05 as the derived listing of
every counter, and mark which seated pack is current; do not
replace the listing with one pack body. Section 3 points at
WORKING-PATH-CHECK-CORE.md (D362) instead of restating D346's
"or". It does not rewrite 00-counter.md,
parked-door-lessons.md, or any WORKING-PATH file. The kernel
and the core were not edited. Q41, Q43, and Q34 were not
marked. QD67 stays for Matthew. No new 05 counter and no
00.counter were written. No seated face was edited.
