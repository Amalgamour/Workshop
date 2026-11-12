# R23–R25 lineage — working path

**WORKING PATH.** These are Tester's recommended options, recorded by
Prima on 2026-11-11 at about 7:20 PM EST for the Director to review.
They are **not rulings** and **not settled law**. Prima will use them
as the working path until Matthew rules.

Source: Tester's research note [R23-R25-lineage.md](R23-R25-lineage.md)
(draft, not a trial verdict). Related: axiom 6, R23, R24, R25, QD01,
QD03, QD66, QD67, Q42, Q67.

Prima checked three claims from the note, and they held:

- No `05.03` file exists under `kernel/` (F2). The R24 climb has not
  been used yet.
- Seated packs cite `predecessor: fae009a`. In the local repo that
  commit is an ancestor. In the publish copy and on GitHub, the same
  work is commit `013db63f`, and `fae009a` is not an ancestor of
  `prima/build` (F3). The line back cannot be opened there.
- The builder's `unseatChecks` skips any address that is still seated
  (`kernel/build.mjs`, `if (now) continue`). A silent in-place replace
  of a seated face is not caught there (F1).

Other findings in the note were not re-run in this recording.

---

## The six working picks

1. **When a page's 05 is reseated as an update, the new pack goes on a
   new counter** (05.07 beside 05.02). Nothing at the old address is
   replaced. That is what R24's "start 05.07" and axiom 6 already say.
   The builder should not allow a silent in-place replace. (Sharpens
   QD01, from F1.)

2. **When two seated packs sit on one page, the newer pack carries a
   write-once `supersedes:` (or `prior:`) field pointing at the older
   one.** The old pack is not rewritten and is not marked `retired`
   until counters are allowed that state. A reader walks those links
   to the pack that nothing later supersedes. (From F4.)

3. **Face 00 is the live registry.** It is neither a draft that "needs
   a trial" nor a trial-seated face. The stamp `state:` stays the
   page's state (QD04's current path), and is separate from face 00's
   own standing. The `why-draft:` line that says "needs a new trial"
   should not be used for this. (From F6.)

4. **Face 00's fingerprint is the git blob of its file.** That is
   already what every seat record uses. Name it so. Do not pretend the
   book holds this today; it does not. (From F9.)

5. **If the 00.counter and git history disagree about face 00's past,
   neither silently wins.** They must agree. A mismatch is a defect:
   halt and raise it (axiom 1). (From F9.)

6. **A door page's 00.counter may live at `0000.00.CC`**, as an
   exception to R10, the way R25 already makes face 00 special. The
   line has to live next to the face 00 it measures. This does **not**
   also let a door hold a 05 pack (Q42 stays open). This pick is the
   most law-like of the six; it stays a working path until Matthew
   rules. (From F10.)

---

## What this does not settle

- QD67 (how the 00.counter list climbs) is left as it is. Tester
  noted that Matthew's words lean toward one list, and Designer's
  draft recommends many write-once faces. That question stays
  neutral for the Director (F13).
- F7 (writing a 00.counter changes face 00's face list, so the
  snapshot is itself a change) is tied to QD03, which Tester is doing
  next. F8, F12, and F3 are builder or design-lane problems first.
- Q67 (Pass 12) still applies to faces without counters (01, 04).
  Under pick 1, counters would not re-seat in place, so that attack
  goes away for 05 (F15).
- The six recommended tests in the research note were not run in this
  recording. They are assigned as scratch-clone tests, with no seats.

---

## Status

Working path, pending Director review. Not a ruling. Recorded in
[DECISIONS-LOG.md](DECISIONS-LOG.md) as D320–D325, and on QD01 in
[QUESTIONS-FOR-DIRECTOR.md](QUESTIONS-FOR-DIRECTOR.md). The full
findings stay in [R23-R25-lineage.md](R23-R25-lineage.md).
