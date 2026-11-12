# Lessons from the parked door packs (Q42)

**DRAFT.** This is a draft for the Director to read. It is not settled law.
Anything marked PROPOSED is a builder's proposal. Anything marked `7` is open.

Lane: DESIGN (Designer). This fills in the Q42 working path
([WORKING-PATH-Q42.md](WORKING-PATH-Q42.md), D338): useful lessons in
the four parked door packs should be folded into 0051 and 0052's own
packs or notes. That path is not a ruling. This file is not a second
law.

The parked files stay as history (axiom 6). They were not moved,
deleted, or built. Kernel files, including 0051, 0052, and
`kernel/parked/`, were not edited. WORKING-PATH files were not
rewritten.

This draft does not decide Q26 or Q33. QD67 stays for Matthew.

Related: R10, R22, R25; Q26, Q31, Q33, Q42, Q44, Q45, Q51 (answered
by R25); O14, O34 (held); D44, D49, D50; kernel-trial.md findings 10
and 20; kernel-trial-4.md findings 3 and 17.

---

## 0. What is in the parked packs

Four door pages each have a parked 05.01 (what was learned) and a
parked 05.02 (the work pack), under `kernel/parked/doors/`:

- `00.00.00.0000` - kernel door (`level: kernel`)
- `10.00.00.0000` - desk door, personal (`level: desk`)
- `10.11.00.0000` - shelf door, me (`level: shelf`)
- `10.11.21.0000` - book door, about-me (`level: book`)

The four packs are almost the same, as the working path said. Every
05.02 already links to 0051 (sentinels and the door rule) and 0052
(face 00 registry). Shared steps are:

- rule the door registry fields and write them on that door's 00
  (blocked by Q33, Q42)
- decide where container state and back-links live (blocked by Q26,
  Q31; D44 says containers take state from their door; R10 leaves
  0000 no face 08)
- trial and seat that door's face 00 (blocked by Q34 and Q51)

The desk and shelf packs each have one extra step: exercise that
level's step of the lookup (kernel-trial.md finding 20 was left
open). The kernel and book packs do not.

Level-specific notes on 05.01: the kernel door is the root of the
lookup chain; the desk and shelf samples use the nested page and
leave O14 open; a book must have a door to be legal (D49).

---

## 1. PROPOSED: fold once, as a new step, not by rewriting seated packs

0051 and 0052 already have seated 05.01 and 05.02 (R2 seats; see
those pages' face 00 `seat-05.01` and `seat-05.02` lines). A trial
already refused appending a line to seated `0051.05.02` and keeping
the seat (kernel-trial-4.md, H1). Axiom 6: a change is a new step;
the past is not rewritten.

So the fold should be new 05 counters on 0051 and 0052, drafted and
later trialed, citing the parked files as the source. Do not edit
the seated 05.01 or 05.02. Do not unseat them. Do not copy the same
steps four times -- write them once, and name the level-specific
bits.

Recommended shape, following the existing 05.01 (lessons) and 05.02
(pack) split. Q44 (whether "what we learned" lives on 05 or 06)
stays open; this draft stays with R22 and uses 05:

- `0051.05.03` -- lessons from the parked packs that belong with the
  door rule and the lookup
- `0051.05.04` -- remaining door-related work on 0051
- `0052.05.03` -- lessons from the parked packs that belong with the
  face 00 registry
- `0052.05.04` -- remaining door-related work on 0052

Those files are not written here. KERNEL or PACKS would write them,
still as `7`, after this note. This draft only says what should go
into them.

---

## 2. Already on 0051 or 0052 -- do not copy again

These parked lines are already taught. A new 05.03 may point at them.
It should not repeat them as new law.

- A door holds only face 00 (R10). A 05 on 0000 would break R10.
  That is the Q42 path itself (D338), the parked README, and the
  0051 door rule.
- Before R10, a page with only a registry failed format.md:119
  (kernel-trial.md finding 10). The law card that called a
  registry-only page invalid was fixed in fae009a. Already on
  0052.05.01 (kernel-trial-2.md finding 1).
- Face 00 is held on R19 registry fields (Q33). Already on
  0052.05.01, and on 0052.05.02 w03 (write the ruled field set,
  blocked by Q33, Q34, Q38).
- A book is not legal without a door (D49). Already on 0051.
- The stamp on page 0000 holds the container title. Title placement
  is held and must not be re-asked (O34). Already on 0051.05.02's
  open line. The parked notes also name CONFLICTS K17; that is the
  same held clash.
- The sample desk and shelf doors are the nested pages
  (`10.00.00.0000`, `10.11.00.0000`). Already in the 0051 Door Page
  table. O14 (is the door also `DD.00` / `DD.SS.00`?) stays open
  (D50). Do not decide it here.
- The lookup walks book, then shelf, then desk, then kernel.
  Already in the 0051 Door Rule consequences (A1.8).

---

## 3. PROPOSED: what to fold into 0051

**On `0051.05.03` (lessons):**

- The desk step and the shelf step of the lookup were never
  exercised when those containers have only a door
  (kernel-trial.md finding 20, left open). That is the lived gap.
  The lookup rule itself is already on 0051; this is what building
  the desk and shelf doors taught us about testing it.
- The sample uses the nested page; O14 stays open. A short pointer
  is enough. Do not re-ask O14 as if it were new, and do not pick
  A or B.

**On `0051.05.04` (pack), two work cards, taken from the desk and
shelf parked w03:**

- Exercise the desk step of the lookup. The parked pack already
  names a path: R21 and the cross-checks refuse only a desk face at
  a spot the kernel already fills; a desk page the kernel does not
  have is found by a book lookup. A passing pattern already exists:
  "C3.2 across the lookup: 04 found on the desk passes", with
  `10.00.00.1500` (kernel-trial-4.md finding 17). Done when a
  builder or core test shows a desk page found by a book lookup
  before the kernel.
- Exercise the shelf step the same way, for a shelf page found
  before the desk and the kernel.

These two cards are not blocked by Q26 or Q33. They are tests of
the lookup already stated on 0051.

---

## 4. PROPOSED: what to fold into 0052

**On `0052.05.03` (lessons):**

- The parked packs planned a step "trial and seat this door's face
  00", and blocked it with Q34 and Q51 (face 00 holds its own seat
  record, so its blob changes when it is seated and cannot match a
  trial; kernel-trial-4.md finding 3). Q51 was answered by R25:
  face 00 is the registry root and is not seated the same way. The
  Q42 path already says face 00 is handled under R25, not by a 05
  pack (D338). The useful lesson is: do not revive that seating
  step. Record the line of face 00 on the 00.counter, as R25 says.
- Each of the four doors already carries a `level:` field (kernel,
  desk, shelf, or book), which the parked notes call "the build's
  own." That is practice, not a ruling. Q33 stays open. When Q33
  is ruled, this practice is evidence. This draft does not choose
  the door field set.

**On `0052.05.04` (pack), two work cards:**

- When Q33 is ruled, write the ruled door-type registry fields onto
  the four door pages (`00.00.00.0000.00`, `10.00.00.0000.00`,
  `10.11.00.0000.00`, `10.11.21.0000.00`) and show that the builder
  check passes. This is the parked w01, written once, for all four
  doors. It is the door half of 0052.05.02 w03 (that seated card is
  not edited). Blocked by Q33. This draft does not decide Q33.
- Decide where container state and back-links live, and have the
  core read them. Reason: containers take state from their door
  (D44), and R10 leaves page 0000 no face 08. This is the parked
  w02, written once. Blocked by Q26 and Q31. This draft does not
  decide Q26 (or Q31).

---

## 5. What this is not

- Not a move, a delete, or a build of `kernel/parked/doors/`. Those
  files stay as history. The builder still does not read them.
- Not a decision on Q26, Q31, or Q33. Those stay open. Work cards
  that wait on them stay blocked.
- Not a decision on O14, O34, Q44, or Q45. O34 stays held. QD67
  stays for Matthew and is not touched here.
- Not a rewrite of 0051 or 0052 law faces, seated packs, or
  WORKING-PATH-Q42.md.
- Not an answer to Q42 for the Director. It only proposes how the
  working path's "fold the lessons" line would be done. Prima takes
  Q42 to the Director.

---

## 6. Status

Still a draft, still `7`, not law. Aligns with D338. The parked
files were left in place. The working path file was not rewritten.
