# .seq page file: open questions (`7`)

None of these is answered. Each records the provisional choice made so the build could go on, and why. Only the Director answers them.

## S1. Derived lines change in place
The brief asks that a git diff show only added lines, and also that the face header show its state. State changes over time, so a state line must change.
Provisional: state, board, source, title and the other summaries are derived lines (`key := value`). They may change in place; every other line only grows. Derived lines are never imported.
Why: a person needs the current state at a glance; the history below stays append-only. A test checks that a later export only adds non-derived lines.

## S2. Inherited faces
A `.seq` file holds only the page's own entries in its own book. Faces found by lookup in the shelf, desk or kernel (A1.8; R5 now finds drafts too) are not in the file.
Provisional: not included. Why: the file is a lossless view of one book's page; inherited text belongs to another book, and copying it in would be a copy pretending to be the source (axiom 8). A later option: a derived `inherits :=` line listing where each missing face resolves.

## S3. Face 08 in lineage
seqAddr 5.1 and E6 put a page's lineage on face 00 with face 08, kept by the compute. Face 08 links (C4) are not designed yet.
Provisional: `lineage :=` shows only the address chain (page < book < shelf < desk < kernel).

## S4. Trailing spaces
A body line ending in spaces keeps them (`|  ` is a body line of one space). Some editors strip trailing spaces on save, which would change the body; import against the book then refuses it as an edited past entry (axiom 6), so nothing is lost silently.
Provisional: kept as is. Option: mark trailing spaces visibly.

## S5. New pages from a file
Import proposes only `new` blocks for the page the door names. A file for a page that is not yet in the book can be written by hand (door section with `new` blocks only) and imports as a proposal to create it.
Provisional: allowed; the compute's validation decides (door first, C1.1).

## S6. Draft address form
The kernel books drafts as address `PPPP.FF` with field `tail: draft` (kernel QUESTIONS Q4). The file keeps whatever form the book uses; both land in the same face section.
