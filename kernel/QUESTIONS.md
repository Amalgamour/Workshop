# Questions for the Director

Each item needs a ruling. The kernel does not answer any of them: each stays `7` until you rule (axiom 1, axiom 7; R2 "does not let anyone answer an open Director question"). Options are only the ones the spec already allows. Paths are under `docs/spec/`.

**Q1. What page number does the axioms page get?**
The spec lists this as open (`decisions.md:598`). The kernel uses 0050 for now.
- Option A: keep 0050, the first structural page (`seqAddr.md:223`).
- Option B: another number in 0050-0099.
- **ANSWERED 2026-11-11 3:03 PM EST: R6: axioms live outside the book as 00.axioms on the desk.**

**Q2. When a book looks up a face and the only copy is a draft, is it found?**
- Option A: no. A draft is "being written; not active" (`seqAddr.md:133`). This is how the builder reads it now, so today almost every lookup comes back missing.
- Option B: yes. "Draft faces count" (`seqAddr.md:164`), and books follow the kernel live (`decisions.md:128`).
- **ANSWERED 2026-11-11 2:55 PM EST: Option B (ruling R5).**

**Q3. When a book overrides a face, does it replace the whole face or only the cards it writes?**
- Option A: the whole face. "The first match wins" (`seqAddr.md:104`). Then the sample's local 04 face hides the kernel's other 04 cards, and C3.2 breaks on that page.
- Option B: card by card. "The same key on two faces is the same card" (`seqAddr.md:168`).
- Linked: how is a named override written? Axiom 2 needs one. C5.4 (`decisions.md:397-398`) and the owner-class proposal (`decisions.md:610`) are still proposals.
- **ANSWERED 2026-11-11 3:03 PM EST: R7: overrides are pages in 0001-0009 stating what/why/need/goal; may target face, behavior 0020-0049 or structure 0050-0099.**

**Q4. In a book file, how is a draft face written?**
- Option A: `"addr":"...PPPP.01","tail":"draft"`. This is what the builder does now. `format.md:75-76` shows `tail` as a field, but only on a counter.
- Option B: `"addr":"...PPPP.01.draft"`. "`FF.draft` is its unseated draft" (`seqAddr.md:201`), and the draft exists beside the seated face (`drafting.md:11`).
- **ANSWERED 2026-11-11 3:03 PM EST: R8: FF.draft exists only while drafting (drafting.md).**

**Q5. Is the door of a counted face (`FF.00`) written in the book, or worked out from it?**
- Option A: worked out, never written (`format.md:102`).
- Option B: written before its counters (`format.md:123`). "A face is counted if and only if `FF.00` exists" (`decisions.md:196`).
- Linked: R1 renames this location "door". Does it still list every counter and its tail (`decisions.md:187`)?
- **ANSWERED 2026-11-11 3:03 PM EST: R9: faces have no sentinels; no FF.00.**

**Q6. What content face does a door page 0000 need?**
- Option A: door pages don't need one. Every container has one (`decisions.md:143`).
- Option B: they need one, because "A page with only an identity has no reason to exist" (`decisions.md:274`). The spec doesn't say which face.
- **ANSWERED 2026-11-11 3:03 PM EST: R10: page 0000 has only face 00; face 00 is the page registry.**

**Q7. Bob test, session 2: how should "what is my name" reach the `bob` card?**
- Option A: no route. Resolving works on a word the user types (C8.8, `decisions.md:496-503`), and the question never types `bob`. This stays `7`.
- Option B: a concordance, word to page (`decisions.md:606`). This is a proposal awaiting you.
- Option C: the read path (`claude/readpath.md`, named in `Design.md:14`, proposed). It is not in docs/spec.

**Q8. Where does a page keep its state: in the stamp, in the file name, or both?**
The stamp holds "address, title, state" (`decisions.md:176`), and a face may carry `draft` or `retired` (`seqAddr.md:127`). The kernel writes both: a `.draft` door file with `state: draft` inside.
- Option A: `state:` holds the page tail (`draft`, `retired`, or none). The door face's file tail shows only whether the stamp itself is approved.
- Option B: the file tail alone carries it, and `state:` is dropped.

**Q9. In `.002`, "door" means a band head (`N?00`). R1 says the door is the all-zero sequence. Which word do band heads use?**
- Option A: "band head" (`decisions.md:110`, `workflow-loop.003.md:51`).
- Option B: R1 also covers band heads.

**Q10. Can a seated face sit on a page whose door face is still a draft?**
"A draft face ... may exist on any page, live or draft" (`decisions.md:277`). The spec says nothing about a seated face on a draft page. Under R2 this decides whether any content face can be seated before its door.
- Option A: yes.
- Option B: no. The door is seated first.

**Q11. Does a brand card on face 01 need a 04 card?**
- Option A: yes. "Every 01/02 card key has a 04 card" (`decisions.md:353`).
- Option B: no. In the card-type table, the `brand` row says "Needs a 04 card": no (`decisions.md:521`).

**Q12. Is the dictionary's `03.00` a menu or a door?**
- Option A: a menu (`decisions.md:432`, `:450`).
- Option B: the door of a counted face, listing counters (`decisions.md:187`, R1).
- **ANSWERED 2026-11-11 3:03 PM EST: follows from R9: 03.00 is not a door (faces have no sentinels).**

**Q13. How is the book split below page 0100?**
- Option A: one reserved range, `0001-0099` (`decisions.md:120`).
- Option B: four ranges (`seqAddr.md:220-223`).

**Q14. Are pages in different bands one set because their numbers match, or only when they link both ways?**
- Option A: by number (`decisions.md:112`, `:250`).
- Option B: by reciprocal face 08 links (axiom 8; `decisions.md:644`, F.2 proposed).

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
