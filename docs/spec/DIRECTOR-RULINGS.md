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

## R12 to R18 — 2026-11-11 3:11 PM EST — answers to kernel Q8-Q14 (t66u, numbered 1-7 = Q8-Q14)
**R12 (Q8, also seqpage S9)** "The stamp should go in the .00 as the reg location."
Read: the stamp (address, title, type, state) lives in face 00, the page's registry location. A page's state is kept in the stamp in face 00.

**R13 (Q9)** "I like bands, it's a band because it binding together a set of pages into a work space."
Read: a band head (N?00) keeps the word "band". A band binds a set of pages into a work space. "Door" is only the all-zero sentinel (R1, narrowed by R9).

**R14 (Q10)** "Yes."
Read: a face may be seated while its page's door is still a draft.

**R15 (Q11)** "No."
Read: a brand card on face 01 does not need a 04 card (decisions.md:521 card-type table wins over :353 for brands).

**R16 (Q12)** "door"
Read: the dictionary's 03.00 is a door. TENSION with R9 ("Faces do not have sentinels"): held as 7 and asked back to the Director. Builders do not resolve it.

**R17 (Q13)** "Its broken into 4 sections. Each one has it's own important. 0000-0019 are static 0020-0099 aren't just locations."
Read: below 0100 the book is split into four sections, not one reserved range (Q13 option B). 0000-0019 are static; 0020-0099 are working pages, not just locations (0020-0049 behavior, 0050-0099 structure). The exact four-way split is 7: seqAddr.md lists 0000, 0001-0009, 0010-0019, 0020-0049, 0050-0099 (five rows); asked back to the Director.

**R18 (Q14)** "The matching would be in the hundreds range as in workflow. So N4CC, CC is a counter space, so if you have a workflow from N3-N7 then N403.IDE-design would match N503.IDE-design. They are matched by the CC and the title."
Read: pages in different bands belong together when their last two digits (CC, the counter space inside the band) AND their title match. Example: N403.IDE-design and N503.IDE-design are one set across bands N3-N7.

## R19 — 2026-11-11 3:12 PM EST — what face 00 holds (answers seqpage S8/S9)
Director's words (t67u): "It's a registry location, it can hold a stamp, a registry, it's type. Each page type can have a different set of registry fields to use. But we have the stamp portion, a types field, that sort of thing. Fill out what is missing but that is what I am thinking."
Read: face 00 is the registry location. It holds (a) the stamp portion (address, title, state, axioms, lineage), (b) the page's type, and (c) a registry whose fields depend on the page type: each type defines its own set of registry fields. Builders are to draft the missing detail (the common fields and the per-type field sets) as a draft for the Director to see, never as settled law.

## R20 — 2026-11-11 3:14 PM EST — what counts as a "different view" for an R2 trial (answers design O1)
Director's answer (widget on t68s322): "Yes, a fresh session of the same model counts as a different view."
Read: a hostile trial run by a fresh session (a new subagent that did not build the face) satisfies R2's "different view", even on the same model. The builder's own session never trials its own work.

## R21 — 2026-11-11 3:25 PM EST — no override pages during this build
Director's answer (widget t68s326, "Who approves an override page?"): "No overrides for now. we build them in. But because we are working children desks can have override we are working on the app it's self right now."
Read: while we build the Workshop app itself, nothing is changed by an override page. Changes are built straight into the pages, the kernel or the app. Override pages (R7, 0001-0009) stay in the design for child desks later. The approver question is deferred until then. The sample override page 10.11.21.0001 is parked (not used), and R7 code stays but is not exercised.

## R22 — 2026-11-11 3:50 PM EST — every design choice recorded; seated 05 per page is its MVP work pack
Director's words (t77u): "I want you to make every design choice recorded. As the seated 05 for each page should explain what you learned and become the seated pack of work to achieve the MVP for each page that links back to the overall design. Keep moving forward save questions."
Read: (1) every design choice made in the build is written down with its source. (2) Each page gets a face 05 that says what was learned building that page and holds the work pack to reach that page's MVP, linking back to the overall design (docs/design). That 05 is seated (under R2 after a fresh-session trial, R20). (3) Builders keep moving and save questions instead of stopping.

## R23 — 2026-11-11 6:41 PM EST — the seated 05 is the best version of the pack (t79u)
Director's words (t79u): "So the seated 05 is for the best version of the pack. So a pass might need 3-5 fixes, the 05.02 might solve those issues. But when a page is done, we build the best version of the pack so it solves the issues models run into before they run it. Does that make sense?"
Read: This confirms R22: face 05 is seated. What is seated is the best version of that page's pack. During a pass, the pack (05.02) may change to cover the 3-5 fixes that come up. When the page is finished, we build and seat the best pack, so it already solves issues models run into, before the next model runs it. Earlier seated packs stay as the best so far; a better version is seated (after a fresh trial, R2 and R20) when the page is done. Held 7: whether an older seated 05 is un-seated when the new best version is seated, or both remain and the newer one wins.
