# Tester evaluation of Designer's six-tests answer (D361) — working path

**WORKING PATH.** This is Tester's recommended fill-in of Designer's
`docs/design/six-tests-answer.md` (commit `1be71e9`, D361), recorded
by Prima on 2026-11-11 at about 8:05 PM EST for the Director to
review. It is **not a ruling** and **not settled law**. Prima will
use it as the working path until Matthew rules.

The Designer draft was not rewritten here. The kernel and the core
were not edited. No 00.counter and no new 05 counter were written.
QD67 stays for Matthew. Q41, Q43, and Q34 were not marked. Still `7`.

Source: Tester, 2026-11-11 about 8:00 PM EST. Tester evaluated the
draft against axiom 6 and the live core, read-only, and did not
re-run the six hostile clones (the kernel and the core were not
changed, so those results would be the same).

---

## The idea, in one line

Adopt D361 as a faithful assembly of D320, D321, D344-D348, D352,
and D357-D360, still `7`, still not law. The one real improvement:
when you open plain face 05, keep the derived listing of every
counter, and mark which seated pack is current. Do not replace
that listing with only the current pack's body. That would hide
the line.

---

## D370 — do not hide the 05 line

Tester agrees with the assembly: a 05 climb is a new counter,
never a same-address re-seat; `supersedes:` on the new pack,
address plus blob; cites by address or path plus blob, never a
commit id, and already-seated packs are not edited; 00.counter
waits on the A4.4 agreement and is never made by counting face
00. That holds axiom 6 (a change is a new step; the past is not
rewritten) and axiom 8 (a connection that cannot be opened is
7.8).

**The improvement.** The draft says that when you open face 05
(resolve of `...05`), the core shows the current pack. That
should not mean that plain 05 returns only the current pack's
body. Face 05 is counted. The core already uses plain 05 as a
derived listing of every counter (`resolve.rs:182-183`,
`state.rs:296-297` `board()`, R9: a counted face has no door).
Replacing that listing with one pack body is the same family as
D351 and D357, in a third direction: it would hide the line.

Recommended: keep plain 05 as the derived listing, and mark
which seated pack is current (the one nothing later supersedes).
Opening that counter shows the pack body.

The word `supersedes` still does not appear in the builder or
the core (test 2 still holds).

**Smaller notes, not disagreements:**

- If two seated packs would both count as current, or the
  `supersedes:` chain cycles, halt (axiom 1). There must be
  exactly one current pack.
- The computer tells packs from lessons because packs carry
  `supersedes:` (the first new pack starts the chain). Until a
  page has climbed once, "current" is not yet machine-readable;
  do not edit old packs to add the field.
- Section 3 still uses D346's "replay, or refuse counters." The
  sharpened path is in
  [WORKING-PATH-CHECK-CORE.md](WORKING-PATH-CHECK-CORE.md)
  (D362: the core is the only judge; do not reimplement in
  JavaScript). A pointer is enough. The Designer draft was not
  rewritten here.

Prima confirmed, read-only:

- `resolve.rs:182-183`: plain FF on a counted face is a derived
  listing.
- `state.rs:296-297`: `board()` lists every counter (except 99)
  and has no current marker.
- The words `supersedes` and `predecessor` do not appear in
  `kernel/build.mjs` or in the core's code (they appear as free
  text in some kernel documents).
- There is still no 00.counter file and no new 05.03 or 05.04.
- The D361 commit touches only BUILD-LOG, DECISIONS-LOG, and
  `six-tests-answer.md`.

---

## What this does not do

D370 did not rewrite `six-tests-answer.md`, the kernel, or the
core. It does not answer QD67 or QD66. Those stay for Matthew.
It does not mark Q41, Q43, or Q34.

---

## D372 — Tester agrees D371 is a faithful fill-in; no further improvements

Designer updated [six-tests-answer.md](six-tests-answer.md) for
D370 in commit `2b3efd7`, recorded as D371 (provisional 7, still
not law). Tester evaluated that update against D370, read-only,
on 2026-11-11 at about 8:07 PM EST, and did not re-run the six
clones (the kernel and the core were not changed).

**Adopt D371 as a faithful fill-in of D370. No further
improvements.**

Section 1 applies the improvement in full: keep plain face 05 as
the derived listing of every counter (already what the core does:
`resolve.rs:182-183`, `board()` at `state.rs:296-297`, R9); mark
which seated pack is current (the one nothing later supersedes);
opening that counter shows the pack body; do not replace the
listing with only the current pack's body (that would hide the
line; same family as D351 and D357, in a third direction). The
old wording ("the core shows the current pack") is gone.

The smaller notes are all there: halt if two packs would both be
current or the `supersedes:` chain cycles (axiom 1; there must
be exactly one current pack); packs are told from lessons
because packs carry `supersedes:` (the first new pack starts the
chain); until a page has climbed once, current is not yet
machine-readable; do not edit old packs to add the field.

Section 3 is faithful: D346's "or" is gone. It now says the
core is the only judge, `--check` must run the core's replay,
do not reimplement A4.4 in JavaScript, and points at
[WORKING-PATH-CHECK-CORE.md](WORKING-PATH-CHECK-CORE.md)
(D362). `repo_books` is a second gate, not a substitute.
"Fail closed" and option D stay in that file; a pointer is
enough, as D370 said.

The rest of the assembly is unchanged: a new counter, not a
same-address re-seat; `supersedes:` by address plus blob; cites
the same way; 00.counter waits on agreement and is never made
by counting face 00. The D371 commit touches only BUILD-LOG,
DECISIONS-LOG, and six-tests-answer.md. No 00.counter and no
new 05 were written.

This is still a working path, not a ruling. The Designer draft
was not rewritten again here. The kernel and the core were not
edited.

---

## Status

Working path, pending Director review. Not a ruling. Recorded in
[DECISIONS-LOG.md](DECISIONS-LOG.md) as D370 (the improvement)
and D372 (Tester agrees Designer's D371 is a faithful fill-in;
no further improvements). The Designer draft itself was updated
in D371 and was not rewritten after that.
