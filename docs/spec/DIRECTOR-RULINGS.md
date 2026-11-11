# Director rulings (given in chat; these govern over older spec wording)

## R1 — 2026-11-11 2:38 PM EST — the zero sequence is the door
Director's words: "a 00seq is the door 00 and 0000 are the same as a full zero sequence."
Meaning: on any axis, the full-zero sentinel (`00` for a 2-digit axis, `0000` for the page axis) is the **door**. Older spec wording that calls it owner, identity, or board refers to this same location; use the word "door".

## R2 — 2026-11-11 2:44 PM EST — build-stage approval
Director's words: "Approval without my eyes is fine for this stage of the work."
Meaning: during this build stage, a face may be seated without the Director's review once it has passed a hostile trial (axiom 9) from a different view than its maker. Record it as `approved-by: build-stage (R2)` with the trial reference, so every such seat can be found and re-reviewed later. This does not let anyone answer an open Director question (those stay 7 in QUESTIONS.md).

## R3 — 2026-11-11 2:46 PM EST — the page file type (.seq)
Director asked for a new file type that holds one multifaceted page. Ruling: the **book is the real stored copy**; the `.seq` page file is a **view** you export from a book and import back (import goes through the normal proposal queue). Round trip book -> .seq -> book must be lossless.

## R4 — 2026-11-11 2:54 PM EST — plain characters only
Director's words: "Remove accented letters from being used. We want a simple storage design for now. So limited characters is fine."
Meaning: stored files (books, .seq pages, addresses, titles, card text) use plain ASCII only: printable characters 0x20-0x7E plus newline. Any other byte (accented letters, emoji, tabs, CR) is rejected on write with a clear error, and a book holding one is reported as damaged on read. This is a simplicity choice for now and may widen later.

## R5 — 2026-11-11 2:55 PM EST — drafts are found (answers kernel Q2)
Director's answer to Q2: "Yes. Draft faces count and lookups find them."
Meaning: when the only copy of a face is a draft, resolution finds it (seqAddr.md:164 "Draft faces count"; books follow the kernel live, decisions.md:128). The result must still show the face's state as draft so a reader can tell it is unseated. Where a seated face and a draft both exist at the same spot, the seated face wins.
