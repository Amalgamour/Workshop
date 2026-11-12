# Six-test results, Q67, and R24 — working path

**WORKING PATH.** These are Tester's recommended options, recorded by
Prima on 2026-11-11 at about 7:30 PM EST for the Director to review.
They are **not rulings** and **not settled law**. Prima will use them
as the working path until Matthew rules. The builder, the core, and
the seated packs were not changed in this recording.

Source: Tester, 2026-11-11 evening. Full results:
[R23-R25-six-tests.md](R23-R25-six-tests.md) (a copy of the file
Tester left outside the repo). Related: R23–R25, axiom 6, axiom 8,
D320–D326, D323–D324, Q67 (Pass 12), Q53.

Prima checked these claims from the report, and they held (read-only,
no attack re-run):

- `unseatChecks` still skips a still-seated address
  (`if (now) continue` at `kernel/build.mjs:578`). Pass 12 did not
  change that.
- The builder still refuses a seated counter other than 05
  (`SEATABLE_COUNTERS` and the check at `build.mjs:651`).
- The word "fingerprint" does not appear in the builder, the core,
  the app, or the scripts. It is only in the docs.
- The core's A4.4 refusal sits at `crates/seqaddr-core/src/state.rs:420`.
- There is still no `05.03` file under `kernel/` (parked files aside).
- `0052.05.02` still points at `0052.04.draft.md`, and that file does
  not exist. `0052.04` is seated.
- In the publish copy, `fae009a` is not an ancestor of `HEAD` (exit 1).
  The same work is `013db63f`, which is an ancestor.

The six hostile scratch-clone runs themselves were not re-run here.
They lived only in `/tmp` clones.

---

## The six tests, in short

All six original findings held. Tests 3, 5 and 6 found more. Tests 1–3
were first run before Pass 12 and re-run at `37d5e18`; Tester says the
results were the same.

1. **In-place re-seat (F1): confirmed, also after Pass 12.** A seated
   pack can still be replaced at the same address. `--check` exits 0.
   The old blob leaves the live registry and the book. Only git history
   and the old trial file still name it. Cause: the still-seated skip
   at `build.mjs:578`.
2. **Two seated packs (F4): confirmed.** A new seated `05.03` builds
   clean. Replay and resolve show `05.01`, `05.02` and `05.03` all
   "closed". Nothing marks which is current. `predecessor:` is free
   text; no code reads it.
3. **00.counter dry run (F7, F8): confirmed, plus a new hole.** A bare
   `00.01` is refused ("a 00 counter may not be seated"). A
   `00.01.draft` builds clean once face 00 lists it and gives a
   `why-00.01`. Then the core rejects the whole `00.00.00` book (A4.4:
   face 00 is not a counted face). Every resolve fails, even an address
   in another book, because `load_world` loads every book. The core's
   `repo_books` test catches this; `--check` does not. F7 in numbers:
   the snapshot named face 00 blob `0430347c...`, but the face 00
   committed with it was `14ce04b8...`. That cascade is today's
   builder (it still writes `faces:`). The QD03 working path is meant
   to break the cascade; the builder has not been changed to match.
   The new hole is separate, and it blocks any 00.counter
   implementation until the address and state are agreed with the core.
4. **Fingerprint drift (F9): confirmed.** A `00.01.draft` naming a real
   but wrong prior blob, and then an all-zero blob, both pass
   `--check`. The compare R25 asks for has no implementation.
5. **Lineage cites (F3): confirmed and wider.** 50 commit cites in 19
   of 22 seated 05 files. All 50 fail in a fresh publish clone and on
   GitHub `prima/build` ("Not a valid object name"). All pass locally.
   It is not only `fae009a`. Five distinct commits are involved. Blob
   cites resolve in all three copies. Today's matching publish ids
   (which may change at the next filter-branch): `fae009a` →
   `013db63f`, `8c8f780` → `7a9795c9`, `d37e532` → `d5a19b75`,
   `42ffbc9` → `6322281b`, `ef28051` → `076d783e`.
6. **Stale packs (F2): confirmed and worse.** The packs were already
   stale when seated. Several TRIAL-K3 fix cards (w01) were finished in
   `7b08cbf`, an ancestor of the seat commit `679d49e`. Broken counts
   include 0051 w02 (card says 20 holes / 28 cards; now 17 and 30),
   also 0054, 0055, 0056, 0057. 0052 w02 points at a draft file that
   does not exist; following that card would mean editing a seated
   face. R25 narrows Q34 but does not close it. Q41 and Q43 look
   answered in substance by R23/R24 but are not marked; that is for
   Matthew to confirm, **not for us to mark**.

---

## Working-path picks from the tests (not law)

These sharpen picks already recorded in
[WORKING-PATH-LINEAGE.md](WORKING-PATH-LINEAGE.md) (D320–D325). They
do not replace those picks.

1. **The builder should refuse a pack re-seated in place** (D344). Use
   the every-blob walk Pass 12 already has: if a still-seated address
   has a distinct earlier seat blob, that is an error unless a new
   counter is used. This is D320 as a check, not only a path. The
   builder was not changed in this recording.
2. **`supersedes:` only helps if the builder and the core read it**
   (D345), and the core exposes "current" on resolve of `...05`. Keep
   05.01 notes out of that rule. This sharpens D321.
3. **`--check` should replay written books with the core's rules, or
   refuse counters on faces the core does not count** (D346). The
   `repo_books` test should be in the pre-commit set. The F7 listing
   cascade is for today's builder; on the QD03 path the list is
   derived, so that part is already the working answer. The new A4.4
   hole is separate, and it must be solved before any 00.counter is
   written in the shared repo.
4. **Define fingerprint as face 00's git blob at the parent of the
   commit that adds the 00.CC**, and make the builder check it (D347).
   A mismatch halts (D324). This sharpens D323.
5. **Use the 05.03 climb (R24) to re-cite lineage by address plus
   blob, never by commit id** (D348), as Q53 already did for trials;
   to close the already-done w01 cards; to fix the broken counts; and
   to re-point 0052 w02 at a `0052.04.draft` re-trial. A trial of a
   pack should run those mechanical done-tests before the seat. The
   new counters were not written in this recording.

---

## Q67 (Option C) — confirm, with one improvement

Tester confirms Option C. Pass 12 (`84d6bd9`) implements it as the
brief stated: an un-seat record names every distinct past seat blob
from face 00 history and from `books/` history (re-seats included);
each must be a blob reachable from HEAD (`git rev-list --objects
HEAD`). That closes K10 DO, F1, and F1b. Fail closed is right. Tester
would not change the naming rule or the HEAD-reachable rule.

The improvement is **beside** Option C, not instead of it, and is the
same as D344 above. Option C only runs when the face is no longer
seated. Test 1 showed the still-seated skip is still there after Pass
12, so a same-address re-seat still builds clean and the old blob is
not required to be recorded until a later un-seat. Use the same
every-blob walk on still-seated faces: if history holds a distinct
earlier seat blob at this address, refuse, and require a new counter
(D320). Option C stays as the un-seat naming rule, and is still
needed for history even if same-address re-seats are later refused.

A framing note, not a change to C: Pass 12 comments treat same-address
re-seats as "R24, normal." R24 says we climb to a new counter, we do
not rewrite the seated pack, and the older one stays in the line. The
tests for C can still use a same-address re-seat as an attack, because
that is what K10 found. The comments should not read it as what R24
wants. Those comments were not edited here.

---

## R24, design versus actual

What R24 asks: climb 05.CC (05.01 through 05.06, then seat the best
pack); if the page's work later grows, start a new counter from that
seat plus the changes (05.07 in the example); reseat an update; do not
rewrite the past; the older seated 05 stays in the line. That aligns
with axiom 6.

What the code and the files actually do:

- The climb has never been used. There is no `05.03` in the shared
  repo. The seated packs are still 05.02, and they were already stale
  when seated (test 6).
- The builder still allows a seated pack to be replaced at the same
  address, with the live registry and the book losing the old blob
  (test 1). That is a direct clash with R24 and axiom 6. Pass 12 did
  not change it.
- If the climb were used today, the core would still not mark the
  current pack: two seated packs both show as "closed", and
  `predecessor:` is unread (test 2). So R24 cannot work at resolve
  time until `supersedes:` (or an equivalent) is actually read.
- Lineage cites in the seated packs name local commit ids that do not
  exist in the published copies (test 5). That is axiom 8: the written
  connection cannot be opened there.
- Following 0052 w02 as written would mean editing a seated face
  (test 6).

The design of R24 holds. The builder and the core do not yet do it.
The working path is the one already recorded (D320: a new counter,
never a silent in-place replace), sharpened by D344–D348 above.

The new counters, the builder check, and the core reader were not
built in this recording. They are a later deliberate pass, still as
working path, not law.

---

## What this does not settle

- Q41 and Q43 look answered in substance by R23/R24, but they are not
  marked. Q34 is narrowed by R25, not closed. These are for Matthew
  to confirm. They were not marked here.
- QD67 stays for Matthew, untouched.
- The builder and the core were not changed.

---

## Status

Working path, pending Director review. Not a ruling. Recorded in
[DECISIONS-LOG.md](DECISIONS-LOG.md) as D344–D348. The full results
stay in [R23-R25-six-tests.md](R23-R25-six-tests.md).
