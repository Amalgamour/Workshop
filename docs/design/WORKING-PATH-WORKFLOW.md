# Working path: abandoned tasks, rejected drafts, and mixed outcomes

**WORKING PATH.** This is Tester's recommended options on QD22,
QD54, and QD62, recorded by Prima on 2026-11-11 at about 9:00 PM
EST for the Director to review. It is **not a ruling** and **not
settled law**. Prima will use it as the working path until
Matthew rules.

Still `7`. The kernel, the core, seated faces, and Designer's
drafts were not edited. Q41, Q43, Q34, QD41, QD12, and QD67 were
not marked. "Who may confirm" an abandonment stays `7` on QD61.
The carry-on default count stays `7` until F05 or QD12 lands.

Source: Tester, 2026-11-11 about 8:57 PM EST. Tester did not
write a file; Prima recorded the recommendations here. Tester
said QD22 and the mixed-results half of QD62 do not depend on
the missing F02-F10 files; the carry-on half recommends what
"carry on" may and may not do, and does not guess the missing
count.

---

## D374 — QD22: a written abandoned decision, not a time-out

**Question:** What record lets the computer take back someone's
abandoned task?

**Best option:** Option A — a written "abandoned" decision with
an approval. Reject Option B (a time-out that takes the task
back on its own).

Option B clashes with approved S11. The kernel's S11 text
(`0057.01`) says silence alone leaves the claim unresolved, and
that Compute fences the old claim only after the required
authority records an abandonment decision. A silent time-out
would also go against the silent-abandon rule that was already
struck.

**The record.** The authority writes a decision under their own
identity, naming the counter, the claim id, and the why. A
separate note (face 06 is a natural home; today's ops can
already create one) is stronger than a self-asserted string on
the compute's return, because the core can check who wrote it
(axiom 1) and the return can cite it both ways (axiom 8). The
compute refuses the system return unless it cites a decision for
that exact claim. Once that is written, the old owner's further
writes on that claim are refused (the fence). A counter the
compute returned may close only as abandoned. Replacement is a
new counter with an explicit predecessor (axiom 6, same family
as D344).

**Smaller notes, not substitutes:**

- A time-out or missed heartbeat may only raise the question
  (mark stale, elevate). Taking the task back still needs the
  written decision. The duration stays `7` under QD61.
- If the owner gives the task back themselves, they already can
  (open to return, with blocked or need). Recovery is only for
  when they are silent, so do not build a second path for that.
- "Who may confirm" stays `7`, for QD61. A placeholder is
  "whoever approved the frame," but that is not decided.

This does not depend on the missing F02-F10: S11 is approved,
and the `.002` text already requires an authorized decision.
The Policy switch (`compute_recovery_return`) is not itself the
record. Turning it on with no decision written brings trial
finding 11 back. Do not treat that switch as the answer.

Prima confirmed, read-only: S11 in `0057.01` requires a recorded
abandonment decision, and says silence alone leaves the claim
unresolved; replacement is a new counter with an explicit
predecessor. `Policy.compute_recovery_return` defaults to false
(`state.rs:60`). Trial finding 11 is the Q18 / QD22 question.

---

## D375 — QD54: what happens when review rejects a draft

**Question:** What happens when review rejects a draft?

This is about face drafts (`FF.draft`), not workflow counters,
and it does not depend on F02-F10.

**Best option:** a rejection is, by default, the reviewer's
notes on the draft (those already block promote until every
note is struck). The draft goes back to the drafter, then a
fresh review from a different view (R20, axiom 9, D0). When the
draft should not be seated at all, the reviewer or the authority
ends it with a logged withdraw (who, why, trial reference). The
body stays in the log; the seated face is untouched (axiom 6,
D344). The slot is free for a later fresh copy (R8). Both kinds
of review are recorded with reviewer identity (different from
the drafter) and the trial reference, so a rejection can be
found again (same spirit as R2).

Reject today's behaviour as the answer: a draft can only end by
promote, and there is only one draft per face, so a rejected
draft blocks every later copy, and under R5 a rejected
brand-new face is still served. Do not overwrite the draft with
`put` (D0 forbids it).

For workflow counters, the path already exists: a failed review
closes `failed`, and rework is a new counter with a predecessor
link. Do not invent a second rule there. This unblocks
`0056.05.02` w05 ("record how review is done and what a reject
does").

One core gap the recommendation needs: closing and draft review
currently store no why, no reviewer on the draft path as a
lasting reject record, and no outcome other than a successful
promote.

Prima confirmed, read-only: `promote` is refused while notes
are unstruck (`state.rs:670`); a full-body `put` never replaces
an existing face (D0, `state.rs:475`); a face may have only one
`FF.draft` (seqAddr 5.7, `state.rs:485`). `0056.05.02` w05 is
the card that asks for this.

---

## D376 — QD62: which outcome wins, and what "carry on" may do

**Question:** When results are mixed, which outcome wins? What
may "carry on" do after a halt?

Two halves.

**Mixed results.** This half does not depend on F02-F10. Best
option: a default order, with every reason always recorded, and
a reviewer override only with a why. For the mix the text
actually names (blockers and missing authority together):
needs-authority wins, because that is a raise to the person
(axioms 1 and 5). If failed also applies (unmet criteria,
rejected evidence or scope), failed is the headline — a
violation is not dressed as a request. Abandoned is exclusive
and only through recovery (D374). Passed only if nothing else
applies (S03). The core today stores only one outcome string
and no why; this recommendation needs both a why and a reasons
list on close.

Prima confirmed, read-only: the core stores a single `outcome`
string (`state.rs:118`, `log.rs:85`). Allowed values are
`passed`, `failed`, `blocked`, `needs-authority`, and
`abandoned` (`state.rs:593`, approved S03). S03 in `0057.01`
says `passed` requires satisfied criteria, `failed` records
unmet criteria or rejected evidence or scope, `needs-authority`
records a next step outside the grant, and `abandoned` requires
the recovery record.

**Carry on.** Recommend what it may and may not do, but do not
fix the default count or the counting unit — those are defined
only by missing F05 (QD12). A "carry on" from the frame's
authority, tied to the recorded halt, may grant a further
allowance inside the same approved frame, N4 revision, and
grant. Unrelated talk does not lift the halt. Counts and
reasons stay in lineage.

It may not: reset the gravity count (that needs an explicit
change or re-approval of the frame, already approved at
`.002`); widen scope, grant, or frame (that is a revise with
fresh approval); accept a pack, mark the MVP done, or promote
(S04); or lift a separate axiom-1 conflict halt. The allowance
is counted in whatever unit F05 defines. The `.003` default of
one more release, and the restart policy, stay `7` until F05 or
QD12 lands. Do not treat a bare "carry on" as unlimited.

QD12 and the missing F02-F10 files stay for Matthew. This path
does not guess them.

---

## What this does not do

It does not edit the kernel, the core, seated faces, or
Designer drafts. It does not answer QD61, QD12, QD66, or QD67.
It does not mark Q41, Q43, Q34, or QD41. It does not turn on
`compute_recovery_return`. It does not implement a withdraw
path or a reasons list. Those are later work, after a ruling
or a deliberate pass.

---

## Status

Working path, pending Director review. Not a ruling. Recorded
in [DECISIONS-LOG.md](DECISIONS-LOG.md) as D374 (QD22), D375
(QD54), and D376 (QD62). Those questions stay open and marked
`7`.
