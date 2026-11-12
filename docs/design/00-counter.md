# Face 00's counter (00.CC)

**DRAFT.** This is a draft for the Director to read. It is not settled law.
It fills in what R25 leaves open. Anything marked PROPOSED is a builder's
proposal. Anything marked `7` is open.

Lane: DESIGN (Designer). Source ruling: R25 in `docs/spec/DIRECTOR-RULINGS.md`.
Related: axiom 6 (`Axioms.md:23`), R24 (how 05 climbs), kernel Q51, QD05, QD66, QD67.

---

## 0. What R25 already decides

Face 00 is special. It is the registry root for the page. It is not seated the same way as other faces. [R25]

Changes are still recorded onto face 00. [R25]

A second face, a 00 counter (`00.CC`), holds a list of face 00's fingerprint as it was just before each change. [R25]

The steps are: snapshot that fingerprint first, then make the change, then count and compare: the old fingerprint, the change, and what 00 is now. [R25]

This keeps the line (axiom 6) without needing face 00's own fingerprint to stay frozen. [R25] [Axioms.md:23]

The list must be its own face, not lines inside 00. Writing the list inside 00 would change 00's fingerprint again, which is the problem we are solving. [R25]

Seat records may still be written onto 00. The line of 00 itself is kept on the 00.counter face. This answers Q51 and QD05. [R25]

Two things stay `7` (R25's held questions):

1. Whether 00.counter faces are themselves seated in the normal way. (QD66)
2. How the list climbs (`00.01`, `00.02`, ...) when a new fingerprint is added. (QD67)

---

## 1. Why this is needed

A face 00 holds seat records for the other faces on its page (`seat-NN:`). Writing any of those records changes face 00's bytes (its fingerprint). So a seated face 00 could never keep matching the fingerprint a trial passed. That is Q51. [kernel/QUESTIONS.md Q51; `docs/trial/kernel-trial-4.md` finding 3]

R25 solves this without moving the seat records off face 00, and without pretending those lines are not part of 00's bytes. Face 00 may change. The 00.counter keeps the earlier fingerprints, so the line is visible.

---

## 2. PROPOSED: how the list climbs (QD67)

**Option A (recommended).** Each snapshot is a new counter: `00.01`, then `00.02`, and so on, up to `00.98`. Once a 00.CC face is written, it is not edited. The "list" is the series of these faces, in order.

This matches how face 05 climbs (R24) and axiom 6: a change is a new step in the line; the past is not rewritten. [R24] [Axioms.md:23]

**Option B (not recommended).** One 00.counter face holds the whole list, and a new line is added to it each time. That would change that face's fingerprint each time: the same kind of problem face 00 has.

**After 98.** Counters run 01-98 only. [R9] [seqAddr.md:24]. What happens after 98 is already asked as QD16. The same question applies here. `7`.

### What each 00.CC face holds (PROPOSED)

Plain ASCII only. [R4]

A 00.CC face is write-once. It names:

- `address:` the full address, ending in `00.CC` (for example `00.00.00.0051.00.01`)
- `prior:` the previous counter (`00.01` has none; it starts the line)
- `fingerprint-before:` the full 40-hex fingerprint of face 00, taken just before the change
- `change:` what is about to be written onto face 00, and why (for example a new `seat-05:` line)
- `axioms:` 6 (lineage), and 9 if this snapshot has not yet been checked

It does not need to store the fingerprint after the change. The next 00.CC's `fingerprint-before` is what 00 became. The computer compares:

- the old fingerprint, stored on this 00.CC
- the change, stored on this 00.CC and also visible in the book
- what 00 is now (or what the next 00.CC recorded as `fingerprint-before`)

Writing the "after" fingerprint back onto this 00.CC would edit it, which option A does not allow.

### The steps, in order

1. Read face 00's current fingerprint.
2. Write a new 00.CC face that stores that fingerprint and the coming change.
3. Then make the change to face 00.
4. Then count and compare: old fingerprint, the change, and what 00 is now.

If the compare fails, that is a defect. Do not rewrite the 00.CC face to make it fit. Raise it. [Axioms.md:23] [Axioms.md:25]

---

## 3. PROPOSED: whether 00.counter faces are seated (QD66)

**Option A (recommended).** No. A 00.counter is write-once evidence. It is not seated the same way as other faces. Face 00 itself already has this kind of exception. [R25]

Why: if we seat `00.01` the normal way, that seat record is written onto face 00. [R25: "seat records may still be written onto 00"]. That write is itself a change to 00, so we would need a new snapshot (`00.02`). If we then seat `00.02`, the same thing happens again. That is a cascade.

A 00.CC face is final because it is never rewritten, not because a seat line is added to face 00. A trial can still check that the fingerprint it names really was face 00's bytes just before the named change. [axiom 9]

**Option B.** Yes, a 00.counter is seated after a trial, like any other face. Then we need a rule that stops the cascade. That rule is not written. `7`.

---

## 4. What this is not

This draft does not seat, un-seat, or change any face. It does not change the kernel builder or the core. Those wait until the Director rules on QD66 and QD67, or until Prima says to build from this proposal under R2 as a provisional `7`.

This draft does not answer QD66 or QD67. It only proposes. Prima takes those questions to the Director.

Kernel Q51 itself lives in `kernel/QUESTIONS.md` (KERNEL lane). This draft does not edit that file.

Face 00's stamp and registry fields stay as in `docs/spec/face00.md`. A later pass can add 00.CC there once this is settled.

---

## 5. What builders can do now

Follow R25 as already written:

- Do not seat face 00 the same way as other faces.
- Seat records may still be written onto face 00.
- Before changing face 00, snapshot its fingerprint; after, compare.

Until QD66 and QD67 are ruled, treat the climb and the seating of 00.CC as `7`. The proposal above is the recommended shape, not law.

---

## 6. Open questions

- QD66. Are 00.counter faces seated the normal way?
- QD67. How does the 00.counter list climb when a new fingerprint is added?
- QD16. What happens after counter 98? The same question applies to 00.CC.
