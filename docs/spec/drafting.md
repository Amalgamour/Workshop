# Drafting

Aligned from `director/drafting.md` with decision D0. The principle is settled; the enforcement is proposed.

## Why

A model must never rewrite a face from memory. A rewrite from memory silently drops what the model did not remember. Every change starts from a copy of the real text and arrives one note at a time, so nothing is lost and every change can be traced.

## Process

1. Copy the existing face to `FF.draft`.
2. Add notes from memory to the draft. Notes, not edits.
3. Check for additional sources. Add notes from them.
4. Merge the notes one at a time, striking each as it is merged.
5. Record overflow and unprompted ideas as new notes. Once all notes are merged, go on.
6. Read the whole face again and write notes again. A full view is needed to write well.
7. Merge and strike those notes.
8. Read again. If there are no more notes, hand back for review.

A brand-new face has nothing to copy. It starts as an empty draft and still goes through notes and merges.

## Enforcement by the compute (proposed)

The compute only accepts changes to an existing face through these operations, so a face cannot be replaced from memory:

| Op | Step | Effect |
|---|---|---|
| `copy` | 1 | the compute copies the seated face to `FF.draft`; the writer sends no body |
| `note` | 2, 3, 5, 6 | add one note to the draft |
| `merge` | 4, 7 | apply one change to the draft, citing its note; the note is struck |
| `promote` | after review | the draft replaces the seated face |

- `put` (a full body) is allowed only to create a new face, never to replace one.
- Every change traces to a note. Review checks that every note is struck before `promote`.
- The log keeps every note and merge, so the full history of a face can be read back.

## Exceptions

- **Meters** on brand cards are written only by the compute and are not drafted (`brands.md`).
- **Derived content** (boards, contents lists, menus, ancestor paths) is calculated and never drafted.
- **A new brand card** is drafted by the compute from the user's stated meaning; the user confirming the meaning is its review.

## Open

- How review is recorded, and what happens when review rejects a draft (section D).
- Whether a page type may turn drafting off, for example for scratch pages (C1.4 allows it as a type rule).
