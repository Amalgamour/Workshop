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

## R6 to R10 — 2026-11-11 3:03 PM EST — answers to kernel Q1-Q6
Director's words (t64u), quoted then read:

**R6 (Q1)** "Axioms exist outside of the book as a 00.axioms on the desk."
Read: the axioms are not a page inside a book (so not page 0050). They sit at desk level in the desk's 00 spot, titled axioms. Working address: `00.00.axioms` on the kernel desk (7 until the Director confirms the exact address).

**R5 follow-up (Q2)** "Yes it can be looked up but also why is it a draft?"
Read: a draft is found (R5), and the lookup should show why it is a draft (its reason/notes), not just that it is one.

**R7 (Q3)** "When a local override happens it exists in the reserved face pages of 0001-0009. Then it states what its changing, why it's there, why it's needed, what it should achieve. It might not change any faces but some structure or behavior. Those are 0020-0049 for behavior and 0050-0099 for structural."
Read: an override is written as its own page in the book's reserved range 0001-0009. It states: what it changes, why it is there, why it is needed, what it should achieve. Its target may be a face, a behavior (0020-0049) or a structure (0050-0099). An override does not silently replace a face in place.

**R8 (Q4)** "Only if its a draft. See the drafting.md to understand why we have the draft so we don't replace an existing work from memory."
Read: `FF.draft` exists only while a face is being drafted. It is the copy drafting.md step 1 makes so seated work is never replaced from memory. A draft is addressed as `...PPPP.FF.draft`.

**R9 (Q5)** "Faces do not have sentinels. Only pages, books, shelves and desks."
Read: no `FF.00` and no `FF.99`. Counted faces have no door; counters run 01-98 only. Sentinels (00/99 and 0000/9999) apply only to the desk, shelf, book and page axes. Narrows R1 to those axes.

**R10 (Q6)** "Page 0000.00 is the only location that exists. 00 is a registry location on a page, because it's multi faceted."
Read: on a book's door page 0000, face 00 is the only face. On any page, face 00 is the registry: the place that lists the page's faces (it is not a sentinel, per R9). So a door page needs no content face.

## R11 — 2026-11-11 3:07 PM EST — common questions, solved by key words (answers kernel Q7)
Director's words (t65u): "The what is my name will become part of a common questions people ask list. When we see a version of this, it becomes linked as a sentence; it works like brands do. This is how we let the compute solve. So when it sees prepositions, paired with key words like 'what' + 'name' + 'my' we can use those to solve and give the best guess. Most people only have a few important words when they write or say something. We use this as how we solve. Then compute should be complex enough to parse the words and find what it should hand to the model. It should list 1-3 pieces from that the model can use its intelligence to solve, or ask the model about another option. Otherwise it should ask the person what they are saying, probing them for more detail until the compute and model can solve and resolve their prompt."
Read:
- There is a **common questions list**. Each entry is a sentence pattern that works like a brand card: a set of key words (e.g. what + my + name) linked to what answers it (e.g. the user's name -> the `bob` card).
- The compute pulls the few important words out of a prompt (key words plus the small linking words), matches them to the list and to brand cards, and ranks the best guesses.
- It hands the model **1 to 3 pieces**. The model uses its own judgment to solve from them, or asks the compute for another option.
- If nothing fits well enough, the compute asks the person what they mean, probing for more detail until it can be resolved.
- New phrasings of a known question get linked to that question, the way new forms are added to a brand.
