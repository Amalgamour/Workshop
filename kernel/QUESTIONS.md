# Questions for the Director

Q1-Q11, Q13 and Q14 are answered by R5-R18 and applied in kernel passes 2-3 (kept below as history). Q12 is answered by R16 ("door"), which is in tension with R9; it is held `7` and asked back (Q29). Still open: the exact four-way split below 0100 (R17, `7`), and Q15-Q29. The kernel does not answer any of them: each stays `7` until you rule (axiom 1, axiom 7; R2 "does not let anyone answer an open Director question"). Options are only the ones the spec already allows. Paths are under `docs/spec/`.

**Q1. [ANSWERED by R6, DIRECTOR-RULINGS.md]** "Axioms exist outside of the book as a 00.axioms on the desk." Applied: axioms moved to `00.00.axioms` (exact address still `7`).
Original question: **What page number does the axioms page get?**
The spec lists this as open (`decisions.md:598`). The kernel uses 0050 for now.
- Option A: keep 0050, the first structural page (`seqAddr.md:223`).
- Option B: another number in 0050-0099.
- **ANSWERED 2026-11-11 3:03 PM EST: R6: axioms live outside the book as 00.axioms on the desk.**

**Q2. [ANSWERED by R5, DIRECTOR-RULINGS.md]** "Yes. Draft faces count and lookups find them." and "Yes it can be looked up but also why is it a draft?" Applied: the lookup finds drafts; each registry line says why a face is a draft.
Original question: **When a book looks up a face and the only copy is a draft, is it found?**
- Option A: no. A draft is "being written; not active" (`seqAddr.md:133`). This is how the builder reads it now, so today almost every lookup comes back missing.
- Option B: yes. "Draft faces count" (`seqAddr.md:164`), and books follow the kernel live (`decisions.md:128`).
- **ANSWERED 2026-11-11 2:55 PM EST: Option B (ruling R5).**

**Q3. [ANSWERED by R7, DIRECTOR-RULINGS.md]** "When a local override happens it exists in the reserved face pages of 0001-0009..." Applied: the sample override is page 10.11.21.0001. Whether an override replaces a whole face or one card is still not ruled (`7`).
Original question: **When a book overrides a face, does it replace the whole face or only the cards it writes?**
- Option A: the whole face. "The first match wins" (`seqAddr.md:104`). Then the sample's local 04 face hides the kernel's other 04 cards, and C3.2 breaks on that page.
- Option B: card by card. "The same key on two faces is the same card" (`seqAddr.md:168`).
- Linked: how is a named override written? Axiom 2 needs one. C5.4 (`decisions.md:397-398`) and the owner-class proposal (`decisions.md:610`) are still proposals.
- **ANSWERED 2026-11-11 3:03 PM EST: R7: overrides are pages in 0001-0009 stating what/why/need/goal; may target face, behavior 0020-0049 or structure 0050-0099.**

**Q4. [ANSWERED by R8, DIRECTOR-RULINGS.md]** "Only if its a draft..." Applied: drafts are addressed `...PPPP.FF.draft` (the book entry keeps the same word in `tail` too).
Original question: **In a book file, how is a draft face written?**
- Option A: `"addr":"...PPPP.01","tail":"draft"`. This is what the builder does now. `format.md:75-76` shows `tail` as a field, but only on a counter.
- Option B: `"addr":"...PPPP.01.draft"`. "`FF.draft` is its unseated draft" (`seqAddr.md:201`), and the draft exists beside the seated face (`drafting.md:11`).
- **ANSWERED 2026-11-11 3:03 PM EST: R8: FF.draft exists only while drafting (drafting.md).**

**Q5. [ANSWERED by R9, DIRECTOR-RULINGS.md]** "Faces do not have sentinels. Only pages, books, shelves and desks." Applied: no `FF.00`, no `FF.99`; counters 01-98.
Original question: **Is the door of a counted face (`FF.00`) written in the book, or worked out from it?**
- Option A: worked out, never written (`format.md:102`).
- Option B: written before its counters (`format.md:123`). "A face is counted if and only if `FF.00` exists" (`decisions.md:196`).
- Linked: R1 renames this location "door". Does it still list every counter and its tail (`decisions.md:187`)?
- **ANSWERED 2026-11-11 3:03 PM EST: R9: faces have no sentinels; no FF.00.**

**Q6. [ANSWERED by R10, DIRECTOR-RULINGS.md]** "Page 0000.00 is the only location that exists. 00 is a registry location on a page, because it's multi faceted." Applied: page 0000 has only face 00; face 00 is the registry on every page.
Original question: **What content face does a door page 0000 need?**
- Option A: door pages don't need one. Every container has one (`decisions.md:143`).
- Option B: they need one, because "A page with only an identity has no reason to exist" (`decisions.md:274`). The spec doesn't say which face.
- **ANSWERED 2026-11-11 3:03 PM EST: R10: page 0000 has only face 00; face 00 is the page registry.**

**Q7. [ANSWERED by R11, DIRECTOR-RULINGS.md; applied in pass 3]** A common questions list: key words (what + my + name) linked like a brand to what answers it; the compute hands the model 1-3 pieces, or probes the person. Applied: sample page `10.11.21.0013` (number `7`) holds a `question` card `what-is-my-name` with `answer: 10.11.21.1001.01.bob`, in the crates/ask `QuestionCard` shape. The `question` card type is not in decisions.md C8.9 (`7`).
Original question: **Bob test, session 2: how should "what is my name" reach the `bob` card?**
- Option A: no route. Resolving works on a word the user types (C8.8, `decisions.md:496-503`), and the question never types `bob`. This stays `7`.
- Option B: a concordance, word to page (`decisions.md:606`). This is a proposal awaiting you.
- Option C: the read path (`claude/readpath.md`, named in `Design.md:14`, proposed). It is not in docs/spec.
- **ANSWERED 2026-11-11 3:07 PM EST: R11, a common-questions list matched by key words, handing the model 1-3 pieces or probing the person.**

**Q8. Where does a page keep its state: in the stamp, in the file name, or both?**
The stamp holds "address, title, state" (`decisions.md:176`), and a face may carry `draft` or `retired` (`seqAddr.md:127`). The kernel writes both: a `.draft` door file with `state: draft` inside.
- Option A: `state:` holds the page tail (`draft`, `retired`, or none). The door face's file tail shows only whether the stamp itself is approved.
- Option B: the file tail alone carries it, and `state:` is dropped.
- **ANSWERED 2026-11-11 3:11 PM EST: R12: the stamp (incl. state) lives in face 00, the registry.**

**Q9. In `.002`, "door" means a band head (`N?00`). R1 says the door is the all-zero sequence. Which word do band heads use?**
- Option A: "band head" (`decisions.md:110`, `workflow-loop.003.md:51`).
- Option B: R1 also covers band heads.
- **ANSWERED 2026-11-11 3:11 PM EST: R13: band heads keep the word band.**

**Q10. Can a seated face sit on a page whose door face is still a draft?**
"A draft face ... may exist on any page, live or draft" (`decisions.md:277`). The spec says nothing about a seated face on a draft page. Under R2 this decides whether any content face can be seated before its door.
- Option A: yes.
- Option B: no. The door is seated first.
- **ANSWERED 2026-11-11 3:11 PM EST: R14: yes.**

**Q11. Does a brand card on face 01 need a 04 card?**
- Option A: yes. "Every 01/02 card key has a 04 card" (`decisions.md:353`).
- Option B: no. In the card-type table, the `brand` row says "Needs a 04 card": no (`decisions.md:521`).
- **ANSWERED 2026-11-11 3:11 PM EST: R15: no 04 card needed for a brand card.**

Original question: **Is the dictionary's `03.00` a menu or a door?**
- Option A: a menu (`decisions.md:432`, `:450`).
- Option B: the door of a counted face, listing counters (`decisions.md:187`, R1).
- **ANSWERED 2026-11-11 3:11 PM EST: R16: Director said door; conflicts with R9 (faces have no sentinels), held 7 and asked back.**

**Q13. How is the book split below page 0100?**
- Option A: one reserved range, `0001-0099` (`decisions.md:120`).
- Option B: four ranges (`seqAddr.md:220-223`).
- **ANSWERED 2026-11-11 3:11 PM EST: R17: four ranges; 0000-0019 static, 0020-0099 working pages.**

**Q14. Are pages in different bands one set because their numbers match, or only when they link both ways?**
- Option A: by number (`decisions.md:112`, `:250`).
- Option B: by reciprocal face 08 links (axiom 8; `decisions.md:644`, F.2 proposed).
- **ANSWERED 2026-11-11 3:11 PM EST: R18: matched by CC (last two digits) plus title, e.g. N403.IDE-design = N503.IDE-design.**

**Q15. [CORE] Do counters and task boards of a counted face inherit down the chain (trial finding 6)?**
- Option A: yes, like any face; R5 says drafts are inherited too, and A2.9 lets a book read the kernel's 05/06 (current core).
- Option B: no; a board is per book (decisions.md:196 "derived"), so a book never shows the kernel's tasks or notes as its own.

**Q16. [CORE] When a book retires its own copy of a page, does the walk go on to the parent (trial finding 7)?**
- Option A: yes; the retired page is skipped and the shelf/desk/kernel copy is found (current core, notes "retired page").
- Option B: no; retiring is an explicit "not here", so the lookup stops and returns missing (axiom 7).

**Q17. [CORE] Who may write the kernel book 00.00.00 (trial finding 8)?**
- Option A: only an admin identity at access level 00 (C5.2); the core needs a named identity to check.
- Option B: anyone through a proposal with Director approval (R2), as today. The core enforces only `owner: kernel-only` cards.

**Q18. [CORE] What record authorizes the compute to return someone else's open claim (trial finding 11)?**
- Option A: a recorded abandonment decision on the counter (wl.003 S11), e.g. `outcome: abandoned` with `approved-by`.
- Option B: a timeout rule in the kernel. Until decided the core refuses (Policy `compute_recovery_return = false`).

**Q19. [CORE] Can a draft face 08 be the back-link that A5.3 asks for (trial finding 12)?**
- Option A: yes; R5 says drafts count (current core).
- Option B: no; a pointer's back-link must be seated, or the link is one-way until it is.

**Q20. [CORE] Does C3.2 (01/02 card needs a 04 card) apply to counted 01/02 faces (trial finding 13)?**
- Option A: no; counters are entries, not cards (current core skips it).
- Option B: yes; every 01/02 card needs its 04 card wherever it is.

**Q21. [CORE] May a counter be created directly as `pack` (trial finding 18)?**
- Option A: no; wl.003:171 says only the compute's lint moves `draft -> pack`, so a new counter starts as draft (or bare).
- Option B: yes, as the format.md:75 example does. The two texts conflict; the core still allows `put ... pack`.

**Q22. [CORE] Which faces are counted on which page types (trial finding 19)?**
- Option A: a kernel page-type card lists its counted faces (decisions.md:199 "03 or 04 on a contents or dictionary page"); the core reads it.
- Option B: keep a fixed list (05, 06, and 0012.03) in Policy, as today.

**Q23. [CORE] Does the compute's own bare `put` of a face need a seat approval (R2)?**
- Option A: no; the compute writes doors and derived pages (current core exempts `compute_name` on bare puts, never on `promote`).
- Option B: yes; every seat, whoever writes it, carries `approved-by`.

**Q24. [CORE] How does an R7 override page name its target and its four statements?**
- Option A: one card per override on a content face of the 0001-0009 page, with fields `target:` (full face, page, or range address), `changes:`, `why:`, `needed:`, `achieves:` (current core reads only `target:` lines and reports in-place overrides as an R7 finding).
- Option B: a fixed page type `override` whose stamp names the target; the core then rejects in-place overrides outright.

**Q25. [CORE] Under R9 a counted face holds counters 01-98 only. What happens after counter 98?**
- Option A: the face is full; new work goes on a continuation page (PP99 band continuation or a new page), named on face 08.
- Option B: closed counters are archived/renumbered (would need a rule; nothing in the spec today).

**Q26. [CORE] Under R10 the door page 0000 holds only face 00. Where does a door keep its back-link when a 9999 pointer targets a book's door (A5.3)?**
- Option A: a `target:` line in the door's registry face 00 (current core, provisional).
- Option B: pointers never target 0000; they target a page with a face 08 (e.g. 0010).

**Q27. [CORE] Under R10, what must the registry face 00 list, and must it match the faces present?**
- Option A: face 00 lists the page's faces and the core checks it against the faces present (needs a format).
- Option B: face 00 is the stamp; the "list" is derived from the faces present (current core, no check).

**Q28. [CORE] R6 puts the axioms at `00.00.axioms` on the kernel desk. Is that a new address form (two axes plus a title), or a page of book 00.00.00?**
- Option A: a container title form `DD.SS.title` (the grammar would need it; the core today parses titles only after full addresses).
- Option B: an alias for a fixed page in the kernel book.

**Q29. R16 and R9: is the dictionary's `03.00` a door?**
- R16 (`DIRECTOR-RULINGS.md:65`): "door".
- R9 (`DIRECTOR-RULINGS.md:37`): "Faces do not have sentinels. Only pages, books, shelves and desks."
- Option A: R16 wins for the dictionary only: `03.00` is a door (an exception to R9).
- Option B: R9 wins: no `03.00`; the dictionary menu becomes a card on face 03.
- Held: the kernel copies `decisions.md:432` and `:450` (`03.00` menu) unchanged and the builder still rejects a written counter `00`. `7`.

**Q30. R17: what are the four sections below 0100?**
seqAddr.md:219-223 lists five rows (`0000`, `0001-0009`, `0010-0019`, `0020-0049`, `0050-0099`). R17: "0000-0019 are static 0020-0099 aren't just locations."
- Option A: `0000`+`0001-0009` together, then `0010-0019`, `0020-0049`, `0050-0099`.
- Option B: `0000-0009`, `0010-0019`, `0020-0049`, `0050-0099` (same as A, named as ranges).
- Option C: another split. `7`.

**Q31. [TRIAL-K2] Where does a page keep its state: in the stamp `state:` (R12), or in the page tail?**
R12 (`DIRECTOR-RULINGS.md:53-54`): "A page's state is kept in the stamp in face 00." But `0053.01:25` (from `seqAddr.md` section 4) still puts container and page state in page tails: `10.11.21.0000.retired`, `PPPP.draft`. The kernel writes both: `0000.00.draft` with `state: draft` inside.
- Option A: the stamp only. Page tails (`PPPP.draft`, `PPPP.retired`) are dropped from the grammar.
- Option B: both. The page tail and the stamp `state:` must agree, and a mismatch is elevated.
- Option C: the page tail decides, and the stamp mirrors it. `7`.

**Q32. [TRIAL-K2] R14 says "a face may be seated while its page's door is still a draft". Which "door" is meant?**
Under R9 and R10, face 00 is the page's registry, not a door. The door is only the all-zero page `0000`. `0052.01:41` says "door face".
- Option A: the page's own face 00 (its registry and stamp) may stay a draft.
- Option B: the book's door page `0000` may stay a draft.
- Option C: both. `7`.

**Q33. [TRIAL-K2] Which page types exist for R19's per-type registry fields?**
R19: "Each page type can have a different set of registry fields." Kernel `0054.01:6` lists `system`, `general`, `code`, `workflow`, `band` and `pointer`. None of these names an R7 override page (0001-0009), an R11 common-questions page, a door page `0000`, or the R6 axioms. The SEQPAGE draft `docs/spec/face00.md` (DRAFT) proposes field sets.
- Option A: add types for these (for example `override`, `questions`, `door`), each with its own registry fields.
- Option B: keep the six types and carry the role in a registry field. `7`.

**Q34. [TRIAL-K2] Where is an R2 seat recorded on a face?**
R2: record `approved-by: build-stage (R2)` with the trial reference. Under R12 only face 00 has a stamp, and other faces carry no front matter (CONFLICTS D8).
- Option A: a field on the book entry or proposal that seats the face (as the core gate does now).
- Option B: a line in the page's face 00 registry, beside that face.
- Option C: both. `7`.
- Held (kernel pass 4): the kernel uses B and C together. The seat sits in the page's face 00 registry as `seat-01: approved-by: build-stage (R2); trial: docs/trial/kernel-trial-2.md@ed82086; blob: 112c169c`, so the seated file is unchanged, and the builder writes the same `approved-by` and `trial` onto the book entry. `7` until you rule.

**Q35. [TRIAL-K2] Can an R2 seat apply to a counted face (`06.01` notes, dictionary `03.14`)?**
`0052.01:87` (seqAddr.md:199-201): "A counted face is never seated." Counter tails are `draft`, `pack`, `open`, `return` and `review`; bare means closed.
- Option A: no. Counters move only by tails, so a note closes bare, and a dictionary section is bare once reviewed.
- Option B: dictionary sections are seated like faces, and only 05/06 counters use workflow tails. Linked: Q22. `7`.

**Q36. [TRIAL-K2] [MOOT under R21, DIRECTOR-RULINGS.md:82-84: no override pages while the app is built; the sample 10.11.21.0001 is parked in kernel/parked/]** Does an R7 override page change what the lookup returns?
The sample `10.11.21.0001.04` says `achieve: a reader of 10.11.21 who looks up never-from-memory sees the line below as its explanation`. The builder's lookup still returns the kernel's `00.00.00.0056.04.draft` and only reports that the override exists. R7: "An override does not silently replace a face in place."
- Option A: the lookup returns the kernel face with the override card applied on top (per card), and shows both.
- Option B: the lookup returns the kernel face, and the override is reported beside it. Linked: Q3 (per face or per card), Q24 (override form). `7`.

**Q37. [KERNEL pass 4] R18: when two pages in different bands have the same CC but different titles, is that elevated to the user?**
decisions.md:112 said "Titles should match; a mismatch is elevated to the user (A2.8)." R18: "They are matched by the CC and the title." Pass 4 changed the Bands law so the title is part of the match, and dropped the elevation clause.
- Option A: not a set, and nothing is raised.
- Option B: not a set, but the mismatch is still elevated to the user (A2.8), as it may be a typo. `7`.

**Q38. [KERNEL pass 4] face00.md lists the faces in `faces:` without face 00 itself (its example 4.1: `faces: 01 draft`). Is face 00's own state the stamp `state:`, or a separate value?**
The stamp `state:` is the page's state (R12). Face 00 can be a draft while a face is seated (R14). The kernel reads face 00's own state from its file tail and gives its reason in `why-draft:`.
- Option A: `state:` is the page state; face 00's own state comes from its entry tail (as face00.md's `registry :=` line shows).
- Option B: face 00 is listed in `faces:` like any other face. `7`.
