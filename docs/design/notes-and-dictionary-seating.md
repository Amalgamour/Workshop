# Notes and dictionary sections: may they be seated? (QD01 leftover)

**DRAFT.** This is a draft for the Director to read. It is not settled law.
Anything marked PROPOSED is a builder's proposal. Anything marked `7` is open.

Lane: DESIGN (Designer). This sketches only the leftover part of QD01, after
R23 and R24. Related: kernel Q35, R22-R24, seqAddr.md:199 ("a counted face
is never seated"), D53, D183, D225.

The page-types proposal is a separate file: `docs/design/page-types.md`.

---

## 0. What is already decided

Face 05 is seated. It is the best version of that page's work pack. [R22] [R23]

We climb 05.CC as work proceeds (05.01 through 05.06, then seat 05). If the page's work later grows, we start 05.07 from that seated pack, and later reseat an update. The older seated 05 stays in the line. The past is not rewritten. [R24] [Axioms.md:23]

That settles the 05 part of QD01. How a later 05 update is stored (a new counter beside the old pack, a write-once supersedes link) is in Tester's working path [WORKING-PATH-LINEAGE.md](WORKING-PATH-LINEAGE.md) (D320-D325). That path is not a ruling, and this file does not revisit it.

The leftover question this file sketches is: may notes (06) and dictionary sections be seated? [QD01] [kernel Q35]

Q35 asked this for counted faces: `06.01` notes, and dictionary sections such as `03.14`. The older rule says "A counted face is never seated." [seqAddr.md:199] That rule is already in tension with seated 05. [D53] [D225]

---

## 1. PROPOSED: notes (06) are not seated

Notes are "one notes per session." [v2:83] [seqAddr.md:155] A note records what one session did, which model wrote it, and why the note exists.

That is a session record, not a work pack. Seating a "best note" would mix two jobs.

**Recommended.** Do not seat face 06, and do not seat a 06.CC note, the way we seat 05.

Notes still climb 06.CC, one counter per session. When a session is finished, that note can close (bare). It is not promoted to seated law.

If something in a note should last, it is merged into a content face (01, 02 or 04) and seated there, through the normal drafting steps. [drafting.md]

This matches what the kernel builder already does: notes that passed a trial as drafts were left unseated, because Q35 is open. [BUILD-LOG, KERNEL pass 8]

---

## 2. PROPOSED: dictionary sections may be seated

A dictionary section is a word meaning (a brand). It is lasting content, not a session record and not a task.

**Recommended.** Yes: a dictionary section (for example `0012.03.14`) may be seated after a hostile trial, the same way other lasting content is seated. [R2] [R20] [axiom 9]

This is the dictionary half of Q35 option B: "dictionary sections are seated like faces, and only 05/06 counters use workflow tails."

The older "counted face is never seated" rule then has two known exceptions, both for lasting content: the 05 pack (already ruled), and dictionary sections (proposed here). Notes stay unseated.

---

## 3. What this is not

This draft does not seat, un-seat, or change any face. It does not change the kernel builder. KERNEL Pass 12 owns that code.

It does not answer QD10 (whether the dictionary's 03.00 is a door). It does not answer QD11 (which faces are task lists) beyond what is already used.

It does not answer QD01 for the Director. It only proposes. Prima takes the leftover question to the Director.

---

## 4. What builders can do now

Until the Director rules, treat this as `7`.

Recommended, so work can move:

- Keep seating 05 as R22-R24 already require.
- Do not seat 06 notes. If a note holds lasting content, merge that content into a content face.
- A dictionary section may be prepared for a seat (trial first), but is not seated until this leftover is ruled, or Prima says to follow this proposal as a provisional 7.
