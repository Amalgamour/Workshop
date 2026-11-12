# Test 3 hole: --check and the core disagree - working path

**WORKING PATH.** Tester's recommended options, written 2026-11-11
at about 8:00 PM EST (America/Toronto) for Prima to record and for
the Director to review. They are **not rulings** and **not settled
law**. The builder and the core were not changed here. No 00.counter
was written.

Source: Tester, from six-test 3 and D346, D349, D357. Related:
[WORKING-PATH-SIX-TESTS.md](WORKING-PATH-SIX-TESTS.md),
[R23-R25-six-tests.md](R23-R25-six-tests.md) test 3,
[00-counter.md](00-counter.md) section 10,
[WORKING-PATH-00-COUNTER-EVAL.md](WORKING-PATH-00-COUNTER-EVAL.md).

This sharpens D346: it picks one fix, and names options that were
considered, including ones Matthew might not have thought of.

---

## The hole, in short

A `00.CC.draft` that the builder's `--check` accepts makes the
`00.00.00` book unreadable to the core (A4.4,
`crates/seqaddr-core/src/state.rs:420`: face 00 is not a counted
face; counters live on counted faces only). Every resolve then
fails, even an address in another book, because `load_world`
loads every book (`crates/seqaddr-core/src/bin/seqaddr.rs:36-47`).
The core's `repo_books` test catches this. `--check` does not: it
rebuilds the books in memory and compares them to `books/`, and
it never runs the core's replay. A `--check` exit of 0 is not
proof the books are readable. A bare `00.01` is already refused
by the builder. Neither form can live in the shared repo today.

This is a disagreement between two judges. It is not only about
00.counter. Any book entry the builder writes and the core
refuses would have the same shape.

Do not write a 00.counter in the shared repo until this hole is
solved (D346, D349). When the later agreement allows 00.CC, do
not make face 00 a counted face (D357).

---

## Best option

**The core is the only judge of whether a book is readable.** The
builder's `--check`, and the path that writes a book, must use
the core's replay. Concretely:

1. After the builder has built each book (the step it already
   does), it runs the core's replay on that book: `seqaddr replay`
   on the file, or the same `BookState::replay` that the
   `repo_books` test uses (`crates/seqaddr-core/tests/repo_books.rs`).
2. If the core refuses, `--check` fails, and the write is not
   accepted. The error is the core's error, so the two sides
   cannot tell different stories.
3. Do not copy A4.4, or any other core rule, into the JavaScript
   builder. A second copy is how this hole appeared: the builder
   already allows a `00.CC.draft`, and the core does not. Two
   lists will drift again (the dictionary's `0012.03` is already
   a special counted face only in the core's
   `Policy.extra_counted`).
4. If the core tool is not built or cannot be run, `--check`
   fails closed. It does not skip the gate and exit 0.
5. The same replay is in the pre-commit set (the `repo_books`
   test, which exists and is not a hook today). That is a second
   gate, not a substitute for (1).

This closes the hole for test 3, and for any later disagreement
of the same kind.

When 00.CC is later allowed (F8 standing in 00-counter.md; D357):
the special case is added in the core first. The builder does
not grow its own exception. It asks the core, by calling replay.
The special case must allow `00.CC` without `is_counted(page, 0)`
being true, so plain face 00 stays the registry. Do not add face
00 to `always_counted`, and do not put `(page, 0)` into
`Policy.extra_counted`.

KERNEL would implement this. This file does not edit the builder
or the core.

---

## Options considered

**A. (best)** The core is the judge, as above. One set of rules.
`--check` invokes replay. Pre-commit runs `repo_books`. Fail
closed if the core cannot be run.

**B.** The builder reimplements "refuse counters on faces the
core does not count" in JavaScript. This would catch a
`00.CC.draft` today, and it is the second half of D346's "or".
It is not enough on its own: the counted-face list already
differs (builder vs `Policy.extra_counted`), and the next hole
may not be about counters at all. A JS hint is fine only if it
asks the core, or reads the same policy the core uses, and
replay remains the judge.

**C.** Loosen the core so it accepts what `--check` accepts
today. Rejected. The core is right that face 00 is not a counted
face. Loosening A4.4 without the F8 special case would let a
00.counter into the books for the wrong reason. And the wrong
special case -- making face 00 counted -- would hide the
registry (D357).

**D. (Matthew may not have thought of this; it is not a
substitute for A.)** `load_world` today stops on the first book
that fails replay, so a bad `00.00.00` book makes
`10.11.21.1001.01` fail too. A later improvement: load each
book on its own; mark a failed book unreadable; let other books
still resolve; and name the bad book in the error. That is
defense in depth. It does not make a bad book safe to commit.
Recommend A first, and D as a second, later step.

---

## For Matthew

The builder and the core should not disagree about whether a
book can be read. If the core says no, the builder's check
should fail too.

The way to do that is to let the core be the judge: the builder
asks it, and does not copy its rules. Copied rules drift, and
that is how this hole appeared.

Do not treat face 00 as a counted face to get past this. That
would hide the registry behind a list of counters.

Do not write a 00.counter until this check is in place.

---

## Status

Still `7`, not law. This is a working path, pending Director
review. The builder, the core, and the seated packs were not
changed. No 00.counter was written. QD67 stays for Matthew.
Q41, Q43, and Q34 were not marked.
