# Tester evaluation of two 00-counter updates — working path

**WORKING PATH.** This is Tester's recommended fill-in of Designer's
00-counter updates, recorded by Prima on 2026-11-11 at about 7:45 PM
EST for the Director to review. It is **not a ruling** and **not
settled law**. Prima will use it as the working path until Matthew
rules.

The Designer draft (`docs/design/00-counter.md`) was not rewritten
here. The kernel and the core were not edited. No 00.counter was
written. QD67 stays for Matthew. Q41, Q43, and Q34 were not marked.
Still `7`.

Source: Tester, 2026-11-11 evening. The updates are section 10
(D349, the A4.4 hole, filling in D346) and section 11 (D350, parent-
commit fingerprint timing, filling in D347). See
[00-counter.md](00-counter.md) and
[WORKING-PATH-SIX-TESTS.md](WORKING-PATH-SIX-TESTS.md).

---

## The idea, in one line

Adopt both updates as working-path fill-ins, still `7`, still not
law. The one thing to add before anyone implements the A4.4
agreement: do not make face 00 a counted face.

---

## 1. D349 / section 10 (A4.4) — the caution is D357

Adopt D349 as written. This is D346 in the draft: a `00.CC.draft`
that `--check` accepts makes the `00.00.00` book unreadable to the
core (A4.4), and every resolve then fails, even in another book,
because `load_world` loads every book. A bare `00.01` is already
refused by the builder. Neither form can live in the shared repo
today. Do not write a 00.counter until the address and the standing
are agreed with the core. `--check` should replay written books with
the core's rules, or refuse counters on faces the core does not
count, and `repo_books` should be in the pre-commit set. The F7
listing cascade is a separate point (D326). The F8 standing (bare
means write-once evidence; face 00 is not a 05/06 counted face; the
counters are a special case next to the registry) stays the
recommended shape and cannot be used until KERNEL and CORE implement
that agreement. The draft does not edit them, and it does not write
a 00.counter.

**D357.** One important caution, not a disagreement, for whoever
later implements the agreement: do not solve A4.4 by making face 00
a counted face. Do not add it to `always_counted`, and do not put
`(page, 0)` into `Policy.extra_counted`.

That would let `00.CC` through at `state.rs:420`, and would then
break the registry: a bare put of face 00 would be refused ("it
holds counters only; it has no door of its own", `state.rs:460`),
and resolve of plain face 00 would return a derived listing of
counters, not the registry (`resolve.rs:182`). That is the same
family as D351, in the other direction: there, plain `0012.03` is
already the derived menu, so an explanation card cannot live at that
address; here, plain face 00 is already the registry, and must stay
that way.

Designer's F8 already says face 00 is not a counted face in the
05/06 sense, and that `00.00` is the registry itself. The
implementation must match that: allow `00.CC` as a special case
without `is_counted(page, 0)` being true.

Prima checked this read-only, and the claims hold:

- `crates/seqaddr-core/src/state.rs:420`: A4.4, counters only on
  counted faces.
- `crates/seqaddr-core/src/state.rs:460`: a counted face holds
  counters only; a bare put is refused (R9).
- `crates/seqaddr-core/src/resolve.rs:182` and `state.rs:296`:
  resolve of plain FF on a counted face is a derived listing.
- `crates/seqaddr-core/src/face.rs:83-84`: `always_counted` is only
  faces 05 and 06 (`matches!(ff, 5 | 6)`).
- `crates/seqaddr-core/src/state.rs:54`: `Policy.extra_counted` is
  still only `(12, 3)` (the dictionary).
- `crates/seqaddr-core/src/bin/seqaddr.rs:36-47`: `load_world`
  loads every `.book` file in the directory into one World.
- There is still no 00.counter file in the repo (no `*.00.01` …
  `*.00.98` face-00 counter files).
- `crates/seqaddr-core/tests/repo_books.rs` exists as a test. It is
  not a pre-commit hook (the hooks directory has only `.sample`
  files).

Prima did not run a forged trial of "make face 00 counted." The
caution follows from those code paths: if `is_counted(page, 0)` were
true, the refusal at `:420` would not fire, and the refusal at `:460`
and the derived listing at `resolve.rs:182` would.

The Designer draft was not rewritten here. No 00.counter was written.

For Matthew, one idea: do not write a 00.counter until the builder
and the core agree; and when they do, do not treat face 00 as a
counted face, because that would hide the registry behind a list of
counters.

---

## 2. D350 / section 11 (fingerprint timing) — notes are D358

Adopt D350 as written. This is D347 in the draft, and it sharpens
D323 the way the six tests asked: the fingerprint is face 00's git
blob at the parent of the commit that adds the 00.CC; the builder
checks that `fingerprint-before` equals that blob; a mismatch
halts (D324). That is the draft's earlier "just before the change,"
said so a computer can check it after the fact. Section 2 is
updated only for that timing; the QD67 recommendation is otherwise
unchanged and is not treated as settled. Test 4 / F9 is reported
accurately: a real-but-wrong prior blob, and an all-zero blob, both
pass `--check` today, and there is still no implementation. The
draft does not edit the builder and does not write a 00.counter.

Prima also confirmed, read-only: the word "fingerprint" still does
not appear in the builder, the core, the app, or the scripts. It
appears in docs, and in prose in `kernel/QUESTIONS.md`.

**D358.** Two smaller notes, not disagreements:

- The stored value is the blob, never a commit id (test 5, D348).
  After a publish rewrite the commit SHA will change, as it did for
  `fae009a`. The check should walk to the commit that introduced
  the 00.CC file, then read face 00's blob at that commit's parent
  tree. Blob cites survive; commit cites do not.
- The before-field check is only half of R25. The after-compare
  (old fingerprint, the named change, and what 00 is now) is still
  unimplemented. The draft already says so in section 11 and in
  section 2 step 4. Worth keeping visible when KERNEL builds the
  check, so the before-timing is not taken as the whole of R25.

The Designer draft was not rewritten here. The builder was not
edited.

---

## What this does not do

It does not rewrite `00-counter.md`, the kernel, or the core. It
does not write a 00.counter. It does not answer QD67 (how the list
climbs) or QD66 (whether those faces are seated). Those stay for
Matthew. It does not mark Q41, Q43, or Q34.

---

## 3. D359 — the Designer draft is a faithful fill-in (D360)

Tester evaluated Designer's update of `00-counter.md` (commit
`dfe94d7`, D359) against D357 and D358. Tester agrees. Adopt D359
as a faithful fill-in. There are no further improvements. The
Designer draft was not rewritten.

Section 10 takes the D357 caution in full, in plain words first,
then with the code paths. The caution is also in section 8 (F8),
where an implementer would look, and in the earlier summary. The
F8 standing stays the recommended shape and still cannot be used
until KERNEL and CORE agree. The "do not write a 00.counter until
the hole is solved" bar from D346/D349 is unchanged.

Section 11 takes both D358 notes, and those notes also land in
section 2 (the field list and step 4), which is where the
procedure is written. The F9 correction ("fingerprint" is also in
prose in `kernel/QUESTIONS.md`, not only in docs) is accurate.

Sections 2 and 3 (QD67, QD66) are otherwise unchanged and are not
treated as settled. Still `7`, not law. The commit touches only
BUILD-LOG, `00-counter.md`, and DECISIONS-LOG.

Prima confirmed, read-only: the comment at
`crates/seqaddr-core/src/resolve.rs:182` says a counted face's
plain FF reads a derived listing, and the matching arm is at
line 183. There is still no 00.counter file in the repo. Kernel
and core were not edited.

## Status

Working path, pending Director review. Not a ruling. Recorded in
[DECISIONS-LOG.md](DECISIONS-LOG.md) as D357-D358 and D360, and
noted on QD66 and QD67 in
[QUESTIONS-FOR-DIRECTOR.md](QUESTIONS-FOR-DIRECTOR.md). The climb
question itself stays for Matthew. Designer's D359 draft is
adopted as a faithful fill-in; the draft itself was not rewritten.
