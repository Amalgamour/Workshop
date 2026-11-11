# .seq page file: open questions (`7`)

Status after rulings R5-R10 (2026-11-11 3:03 PM EST): **S6 settled by R8.** S2 is touched by R5 but not settled. The others stay open. Each records the provisional choice made so the build could go on, and why. Only the Director answers them.

## S1. Derived lines change in place
The brief asks that a git diff show only added lines, and also that the face header show its state. State changes over time, so a state line must change.
Provisional: state, board, source, title and the other summaries are derived lines (`key := value`). They may change in place; every other line only grows. Derived lines are never imported.
Why: a person needs the current state at a glance; the history below stays append-only. A test checks that a later export only adds non-derived lines.

## S2. Inherited faces (touched by R5, still open)
A `.seq` file holds only the page's own entries in its own book. Faces found by lookup in the shelf, desk or kernel (A1.8; R5 now finds drafts too) are not in the file.
Provisional: not included. Why: the file is a lossless view of one book's page; inherited text belongs to another book, and copying it in would be a copy pretending to be the source (axiom 8). A later option: a derived `inherits :=` line listing where each missing face resolves.

## S3. Face 08 in lineage
seqAddr 5.1 and E6 put a page's lineage on face 00 with face 08, kept by the compute. Face 08 links (C4) are not designed yet.
Provisional: `lineage :=` shows only the address chain (page < book < shelf < desk < kernel).

## S4. Trailing spaces
A body line ending in spaces keeps them (`|  ` is a body line of one space). Some editors strip trailing spaces on save, which would change the body; import against the book then refuses it as an edited past entry (axiom 6), so nothing is lost silently.
Provisional: kept as is. Option: mark trailing spaces visibly.

## S5. New pages from a file (touched by R10, still open)
Import proposes only `new` blocks for the page the door names. A file for a page that is not yet in the book can be written by hand (door section with `new` blocks only) and imports as a proposal to create it.
Provisional: allowed; the compute's validation decides (book door registry first; C1.1). R10 says a door page needs no content face, so a new book's 0000 file has only face 00.

## S6. Draft address form - SETTLED by R8
The kernel books drafts as address `PPPP.FF` with field `tail: draft` (kernel QUESTIONS Q4). The file keeps whatever form the book uses; both land in the same face section.
Answer (R8): a draft is `...PPPP.FF.draft` and exists only while drafting. The file refuses a `tail: draft` field on the seated address (rule R8).

## S7. Where a draft's reason lives (R5)
R5: a lookup shows why a face is a draft. Spec gives no field.
Provisional: the `reason` field on the entry that opened the draft (`put` to `FF.draft` or `copy`), else the first line of the first `note` on it, else `7` and a finding. Note for CORE: `OpRequest` has no `reason` field yet, so a proposal cannot carry one; the compute would need to accept it (or name another place).

## S8. What face 00's body holds (R10) - ANSWERED by R19, detail in face00.md
R19: face 00 holds the stamp, the type and a registry whose fields depend on the type. Builders' draft of the fields: docs/spec/face00.md (DRAFT). The file now compares a written `faces:` to the derived list and reports a finding (written vs derived is face00.md F2).
Old text:
R10: face 00 is the registry that lists the page's faces. Spec does not say whether the list is written in face 00's body or derived.
Provisional: the file derives `faces :=` from the page's entries and shows face 00's body as written. It does not compare the two.

## S9. Where title, state and type live (R10) - SETTLED by R12/R19
R12: "The stamp should go in the .00 as the reg location." Title, state and type live in face 00's stamp. Page 0000 title: face00.md F1.
Old text:
Face 00 was the stamp (address, title, state, type, axioms). R10 makes it the registry and says it is not a sentinel; it does not say where the title goes.
Provisional: `title`, `type`, `axioms` are still read from fields in face 00's body when present.

## S10. The shape of an override page (R7)
R7: an override page in 0001-0009 states what it changes, why it is there, why it is needed, what it should achieve. No card names or fields are given.
Provisional: the file marks the page `kind := override (R7)` and checks nothing more.
