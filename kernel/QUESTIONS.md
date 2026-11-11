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

**Q39. [TRIAL-K3] How does face 00's `faces:` line list a counted face: by counter, or as one counted face?**
The kernel writes each counter with its tail, so each draft counter can carry its R5 reason: `faces: 01 draft, 02 draft, 04 draft, 06.01 draft` (`0051.00:10`), `03.14 draft, 03.16 draft` (`10.11.21.0012.00:10`). `docs/spec/face00.md` section 3.1 (DRAFT) and its examples write the counted face once: `05 counted`. `crates/seqpage` derives that form, so it flags every kernel face 00 with an axiom 8 finding (TRIAL-K3 finding 13).
- Option A: list counted faces once (`06 counted`). Each counter's draft reason stays on its own entry (`reason`), not in `faces:`.
- Option B: list every counter with its tail (`06.01 draft`), with `why-06.01:`. face00.md and seqpage would change.
- Option C: both. `06 counted` in `faces:`, and the counters in a separate field. Linked: face00.md F2 (written vs derived). `7`.

**Q40. [TRIAL-K3] What is the page state of a page whose face 00 is a draft but which has no other draft, or has a seated face?**
The kernel writes stamp `state: draft` on the four door pages (only face 00, a draft) and on `0056` and `10.11.21.1001` (face 01 seated, face 00 draft). `crates/seqpage` derives `live` for all six and reports "stamp state `draft` disagrees with the page's entries (`live`)" (TRIAL-K3 finding 14). R12: "A page's state is kept in the stamp in face 00." R14: a face may be seated while face 00 is a draft.
- Option A: the stamp `state:` is the page's state. A draft face 00 means the page is a draft, and seqpage's derivation changes.
- Option B: the page state is derived from its faces. A draft face 00 alone doesn't make the page a draft, and the kernel stamps say `live`.
- Linked: Q31 (stamp vs page tail), Q38 (face 00's own state). `7`.

**Q41. [TRIAL-K3] R22 asks for a seated face 05 on each page; the kernel law says a counted face is never seated. Which holds?**
R22 (`DIRECTOR-RULINGS.md:86-88`): "the seated 05 for each page should explain what you learned and become the seated pack of work". `0052.01:87` (`decisions.md:198-199`, `seqAddr.md:199-201`): "A counted face is never seated." `0052.01:88`: "Faces 05 (tasks) and 06 (notes) are always counted." Counter tails `draft -> pack -> open -> return -> review -> closed` (`0057.01:86`) move a pack by tails, not by seating.
- Option A: R22's "seated" means a reviewed, closed (bare) counter `05.NN` that holds the MVP pack. Face 05 stays counted.
- Option B: face 05 is uncounted on these pages (one seated face per page, R2 trial). R22 then overrides `decisions.md:198-199` for this use.
- Option C: the learning goes on a seated card (01/04), and the work pack goes on counters `05.NN`. Linked: Q35. `7`.
- **Applied R22 (kernel pass 5), awaiting Director confirmation.** R22 is the newer Director ruling, so `0052.01` and `0052.04` Counted Faces now say a counter of a counted face may be seated under R2 after a hostile trial, as each page's face 05 is (R22), and the builder requires and verifies a seat record for a seated counter (`seat-05.NN:`). Which option R22 means (A, B or C) is not chosen here. Still open: `7`.

**Q42. [PACKS] R22 asks for a face 05 on "each page", but R10 says a door page 0000 holds only face 00. Where do a door page's lessons and pack go?**
R22 (`DIRECTOR-RULINGS.md:86-88`): "the seated 05 for each page". R10 (`:40-41`): "Page 0000.00 is the only location that exists"; the builder refuses any other face on 0000 (`kernel/build.mjs` validate). Held: the four door packs are written but parked, not built (`kernel/parked/doors/`, `kernel/parked/README.md`).
- Option A: door pages get no 05; their packs live on the container's first working page (for example 0010).
- Option B: R22 lets a door page 0000 hold face 05 as well as face 00 (an exception to R10).
- Option C: the door pack lives in the parent container's pack (the desk's for a shelf door, and so on). `7`.

**Q43. [PACKS] Where does a page's MVP pack live: on its own face 05 (R22), or on an N5 page as the workflow loop says?**
`workflow-loop.003.md:99`: "A pack is a face 05 counter on the N5 page: `0501.05.NN`." `:92` (S12): "N4 Face 05 holds design questions; N5 Face 05 holds execution packs." R22: each page's 05 is "the seated pack of work to achieve the MVP for each page". Kernel pages 0051-0057 are not in a workflow band. Held: the packs are on each page's own 05 (05.02), as R22 says.
- Option A: R22 governs for kernel and sample pages; the N5 rule is for workflow sets (N3-N7) only.
- Option B: each page's 05.02 points to an N5 pack page by a face 08 link, once workflow bands exist. `7`.

**Q44. [PACKS] Face 05 is "tasks" and face 06 is "notes" (`seqAddr.md:154-155`). Is "what we learned" a 05 task, or a 06 note that 05 points to?**
R22 puts "explain what you learned" on the seated 05. Held: written as `05.01` with one `type: note` card (a kernel card type; note is the 06 default, so it is named on the card). Linked: Q41 option C, O44 (task and ticket split of 05).
- Option A: keep it on `05.01` as R22 says.
- Option B: write it on `06.NN` and keep 05 for the work pack only. `7`.

**Q45. [PACKS] What authorizes these packs?**
Pack lint (`workflow-loop.003.md:238-239`) hard-fails a pack whose `authorized` does not resolve to an approved N4 revision, and no N4 approval exists for any kernel or sample page. Held: every `05.02` writes `authorized: 7` and `frame: 7`, and stays `draft`, so lint is never asked to pass it.
- Option A: R22 itself is the authorization for these build-stage packs (record "authorized: R22").
- Option B: each pack waits for its own approval record before it can move `draft -> pack`. `7`.

**Q46. [PACKS] The packs name related pages (axiom 8, "links back to the overall design"). Face 08 holds links, but how it holds them is open (O36), and this lane may only write face 05. Is a `links:` field on the pack header enough for now?**
Held: each `05.02` has `design:` (docs/design section and DECISIONS ids) and `links:` (related pages by seqaddr) fields. No face 08 was written.
- Option A: yes, until O36 is ruled.
- Option B: write face 08 links now, and the 05 fields only name them. `7`.

**Q47. [PACKS] Adding a 05 counter changes face 00 (its `faces:` line and `why-05.NN:` lines), because the builder checks the registry against the files (R10). Does that registry edit need a new trial of face 00?**
Every face 00 is a draft and HELD-7 (TRIAL-K3), so no seat broke. But TRIAL-K3 recorded face 00 blobs at d37e532 that no longer match. Linked: Q27 (written vs derived), Q39 (counter form), face00.md F2.
- Option A: no; registry lines that the files force are bookkeeping, not content.
- Option B: yes; any byte change to face 00 needs a new trial (axiom 9), as for any face. `7`.

**Q48. [PACKS] R18's example "N403.IDE-design" has capital letters, but titles are lowercase letters, digits and hyphens (A2.3, D19). Is the example's case meaningful?**
The core compares titles exactly (`docs/BUILD-LOG.md` [CORE] R18 line, `7`).
- Option A: titles stay lowercase; the example means `ide-design`.
- Option B: title case is allowed and compared as written. `7`.

**Q49. [PACKS] The common-questions page number `0013` and the question card fields (`type: question`, `forms`, `answer`) are the build's, not yours (MAP hole 15, CONFLICTS D14). Are they right?**
Copied from crates/ask QuestionCard; the app also reads READER_BOOK.0013 (`docs/BUILD-LOG.md` [APP] round 3).
- Option A: keep 0013 and these fields; add `question` to the kernel card types (0054.02) and the core.
- Option B: give a different page number or field set. `7`.

**Q50. [PACKS] Which words are in the kernel base dictionary?**
decisions.md C8.5: "The kernel supplies a small base dictionary that books inherit." No words are listed, so no kernel dictionary page exists (`0055.06.01`; MAP hole 5). The `00.00.00.0055` pack step for it is blocked here.
- Option A: an empty base for now (books build their own).
- Option B: you give a starting word list. `7`.

**Q51. [TRIAL-K4] A face 00 keeps its own seat record (`seat-00:`) and every other seat record on its page (`seat-NN:`). Writing any of them changes face 00's blob. So face 00 can never match the blob a trial passed, and a seated face 00 would break at the next seat on its page. Where should seat records live?**
Evidence: `docs/trial/kernel-trial-4.md` finding 3 (hostile test HL: "blob 57d0389c is not 70cc70a8"). `kernel/build.mjs:128-129`, `:227-230`. The parked door packs plan "trial and seat 00.00.00.0000.00 ... its seat-00 stamp line" (`kernel/parked/doors/*.0000.05.02.draft.md`). R14 (`DIRECTOR-RULINGS.md:59-60`) and R22 (`:86-88`) assume face 00 can be seated some day. Linked: Q34 (where a seat is recorded), Q47 (does a registry edit need a new trial of face 00).
- Option A: seat records leave face 00 and go to a seat ledger: a book entry field written by the compute at promote, or one file such as `kernel/SEATS.md`.
- Option B: face 00's blob for trial and seat is computed without its `seat-` and `unseat-` lines, so those lines are bookkeeping (like Q47 option A).
- Option C: face 00 is never seated during the build stage; only content faces and face 05 counters are. `7`.

**Q52. [TRIAL-K4] (builder lane, not a Director question) How strong must the seat guard be?**
Evidence: `docs/trial/kernel-trial-4.md` findings 1, 2, 4, 5, 6.
- An 8-hex blob prefix was forged in about 20 seconds, and a changed seated law built clean (HM).
- A ruling appended to the working-tree `DIRECTOR-RULINGS.md` made `approved-by: director` build clean (HG).
- A forged trial committed anywhere is accepted (HA).
- With no git, a forged trial only raises a finding (HC).
- Deleting or editing `books/` hides a past seat (HI, HJ).
Proposed, for the KERNEL lane to choose and the next trial to check:
- (a) full 40-hex blobs in `seat-NN:` and in trial PASS lists, compared for equality, and the two existing seats re-pinned in full;
- (b) rulings and past seats read from git at HEAD, not from the working tree;
- (c) the cited trial commit must be an ancestor of HEAD;
- (d) no git means the seat is an error, not a finding.
`7` until a lane takes it.
Taken by KERNEL pass 6 (step 1): (a)-(d) built in `kernel/build.mjs` (`verifySeat`, `priorSeats`), with tests in `kernel/build.test.mjs`; the two seats re-pinned with full blobs. An older trial whose PASS list has a short prefix (kernel-trial-2.md) still seats only if the full seat blob is this face's file in that trial's commit. Left for the next trial to check. Not taken: a ruling must name the face in a seat line (a simple check is built; the exact wording is the Director's).

**Q53. [TRIAL-K5] (builder lane, not a Director question) How should a seat cite its trial so the seat still checks out in the published copy?**
Evidence: `docs/trial/kernel-trial-5.md` finding 1. Seats cite `docs/trial/<file>.md@<local commit>` (for example `@4b369fa`, `@ed82086`). The publish copy is filter-branched to drop `target/`, so every commit id changes. A clone of `publish`, and a clone of GitHub `prima/build`, both fail `node kernel/build.mjs --check` with 17 errors ("not an ancestor of HEAD" / "git cannot find"). The trial file's blob is the same in both (`a5d253d5e12722956afea38e79cb7fc1cf492c7b`).
- Option A: cite the trial file by its blob (`docs/trial/kernel-trial-4.md#<40-hex blob>`), and check that an ancestor of HEAD has that path at that blob. Re-pin the 17 seats (face 00 is a draft, so no seat breaks).
- Option B: keep `@commit`, and fall back to a content match (an ancestor whose copy of the trial file has the same PASS line) when the commit is missing.
- Option C: the publish flow rewrites seat lines with a commit map. That changes face 00 blobs per copy, so it is not recommended. `7` until a lane takes it.
Taken by KERNEL pass 7 (step 1): option A. A seat reads `trial: docs/trial/<file>.md blob <40-hex trial blob>; blob: <40-hex face blob>`. The guard finds the oldest commit on HEAD's history that adds that path and requires its blob to be the cited one (so a later edit of a trial cannot be cited), reads the trial with `git cat-file blob` and checks the read-back hash, and checks the PASS list names the face at its full blob (a pre-K4 short prefix also needs the face's full blob in the adding commit's tree). The old `@<commit>` form is refused with a re-pin message. All 17 seats re-pinned (kernel-trial-4 at `a5d253d5e12722956afea38e79cb7fc1cf492c7b`, kernel-trial-2 as added at `da5d51424fee3bea1d8443c619fcba3c534a1ace`; kernel-trial-2 was later edited in `fae009a`, so the added blob is the citable one). Test: a filter-branch rewrite of a scratch clone. Left for the next trial to check.

**Q54. [TRIAL-K5] (builder lane, not a Director question) What should the seat guard trust from git?**
Evidence: `docs/trial/kernel-trial-5.md` findings 2-5.
- `git replace` of a trial blob made a changed seated face build clean while citing the real `kernel-trial-4.md@4b369fa`, with no commit (HR).
- `GIT_DIR` pointed at another repo did the same (H15).
- A books/ edit that is committed hides an un-seat (H11).
- A trial file edited in a later commit, a new forged trial, or a committed forged ruling is accepted (H4, H5, H7).
- `unseat-NN: <8 hex>` with no reason is accepted (H13).
Proposed, for the KERNEL lane to choose and the next trial to check:
- (a) run git with `--no-replace-objects` and a cleaned environment (no `GIT_DIR`, `GIT_WORK_TREE`, `GIT_INDEX_FILE`, `GIT_OBJECT_DIRECTORY`, `GIT_ALTERNATE_OBJECT_DIRECTORIES`, `GIT_NAMESPACE`, `GIT_CONFIG_*`); refuse when `git replace -l` lists anything or `.git/info/grafts` exists;
- (b) past seats from history: every `seat-` line ever added on an ancestor that is gone now needs an `unseat-` record;
- (c) trial files are write-once: the cited commit is the one that added the file, and no later commit modifies it;
- (d) an un-seat record names the full old blob and gives a reason. `7` until a lane takes it.
Taken by KERNEL pass 7 (step 1):
- (a) built: git runs with `--no-replace-objects`, `GIT_NO_REPLACE_OBJECTS=1` and every `GIT_*` variable removed; any ref under `refs/replace/`, a grafts file, or a shallow clone is an error (no seat verifies).
- (b) built: past seats are every `seat-NN:` line ever added to a face 00 under `kernel/` on HEAD's history (`git log -p -G seat-`), plus `HEAD:books/`; a face seated there and not seated now needs an un-seat record naming its newest seated blob.
- (c) partly: a seat must cite the trial blob as first added (H5 refused), and the adding commit must touch only `docs/trial/` and `kernel/QUESTIONS.md` (every real trial commit does: ed82086, 4b369fa, 6a1fee5). Not built: proof of who wrote a trial, or of a committed forged ruling (H4, H7 residue); git cannot prove authorship, so that stays findable-in-git only (R2 `:9`).
- (d) built: the un-seat record must hold the full old blob and some reason text besides it.
Tests in `kernel/build.test.mjs` (HR, H15, H11, H5, H13, a mixed trial commit, a shallow clone). Left for the next trial to check.

**Q55. [TRIAL-K5] Must a pack's `grant:` cover every path its own work cards name, including the trial and seat steps?**
Evidence: `docs/trial/kernel-trial-5.md` finding 9.
- `0054.05.02:9` grants only `0054.*.draft.md` faces 01/02/04 and books, but its cards write `crates/seqaddr-core/src/face.rs`, `kernel/build.mjs`, `docs/spec/face00.md` and `0054.00`.
- `0012.05.02:9` says "not face 00 or 05", but w05 writes `0012.00`.
- The seated `0053.05.02` and `0055.05.02` have the same pattern.
- `workflow-loop.003.md:237` (a draft, O7) makes "intended targets ... inside the grant" a hard lint.
- Option A: widen each grant to the paths its cards name (code paths too), and mark trial and seat cards as done by other lanes.
- Option B: a pack grant covers only the builder's own cards; trial and seat cards name their lane (`by: trial lane`, `by: seat lane`) and sit outside the grant by design, and code paths get their own pack.
- Option C: leave grants as they are until `.003` is approved (O7). `7`.
Noted by KERNEL pass 7: this one is the Director's (it sets what a pack may write), so it is not decided here. No `grant:` line was changed; the 0054 and 0013 pack edits in pass 7 add paths to work cards only.

**Q56. [TRIAL-K6] (builder lane, not a Director question) How should the seat guard read history so attributes and merges can't hide a seat or a trial edit?**
Evidence: `docs/trial/kernel-trial-6.md` findings 1 and 2.
- K21: one committed `.gitattributes` line, `kernel/** -diff`, makes `git log -p -G seat-` (`build.mjs:265`) see no seat lines. A committed un-seat with no record then builds clean, also in a fresh clone. K22 does the same with `.git/info/attributes` alone.
- K26: a merge that takes `kernel/` from a side branch cut before a seat commit drops that commit from `git log` (history simplification). The un-seat builds clean, also in a fresh clone.
- K25: a merge that takes a side branch's copy of a real trial file makes the side commit the "oldest add" (`trialOrigin`, `:189-190`), so a PASS line added that way can be cited. That gets around Q54 (c).
Proposed, for the KERNEL lane to choose and the next trial to check:
- (a) read history with `-a --no-textconv` (or parse face 00 files per commit with `git cat-file blob`), so attributes cannot blind it;
- (b) add `--full-history` to the `trialOrigin` and `historySeats` walks;
- (c) optionally refuse merge commits that touch `kernel/` or `docs/trial/`, and attributes lines that touch `kernel/`, `books/` or `docs/trial/` (this branch is linear today);
- (d) add tests like K21, K25 and K26. `7` until a lane takes it.

Decided by KERNEL pass 8 (step 1), builder lane: (a), (b) and (d) are taken; (c) is not.
- (a) Every history walk in `kernel/build.mjs` uses `-a --no-textconv --no-ext-diff --full-history -m --no-abbrev` (`HIST`). Past seats are no longer read from a `git log -p -G seat-` diff: the walk lists every face 00 blob ever committed under `kernel/` (`--raw`) and reads each with `git cat-file --batch`, which applies no attributes or textconv, then parses the `seat-NN:` lines. `gitShow` uses `git cat-file blob`.
- (b) `--full-history` (plus `-m`) on both walks, so a merge cannot drop the side that added a seat (K26) or a trial (K25).
- (b, extra) A trial path added more than once on HEAD's full history with different blobs is refused, whatever the commit dates; a trial added only by a merge commit is refused.
- (c) not taken: a merge or an attributes line is not refused by itself. With (a) and (b) neither can hide a seat or a trial edit, and the branch is linear today.
- (d) 4 tests: committed `.gitattributes` (K21), `.git/info/attributes` (K22), a merge hiding an un-seat (K26), a merge citing an edited trial copy (K25). Each failed (built clean) before the fix and passes after. Left for the next trial to check.

**Q57. [TRIAL-K6] (builder lane, not a Director question) Should the publish copy keep refs that hold the old `target/` history?**
Evidence: `docs/trial/kernel-trial-6.md` part C3.
- `/workspace/workshop-build/publish` keeps `refs/heads/incoming` (`18dd576`), `refs/original/refs/heads/build` (`af8cee9`) and a stale `refs/remotes/origin/build` (`af8cee9`). Each reaches 2 commits that touch `target/`.
- `branch.build.merge` is `refs/heads/build` on `origin` (GitHub), so a bare `git push` would create an unapproved `build` branch on GitHub. A `--all` or `--mirror` push would publish the `target/` history.
- Option A: after each cherry-pick, delete `incoming` and the stale tracking ref, and run `git update-ref -d` on `refs/original/...` once.
- Option B: keep them, and set `branch.build.merge` to `refs/heads/prima/build` (or `push.default=nothing`), so only the explicit `build:refs/heads/prima/build` push works.
- Option C: leave it as is and rely on the explicit push command. `7` until a lane takes it. Report only: nothing was deleted.

Noted by KERNEL pass 8: Prima already handled this in the publish copy (this lane did not touch it). The push is limited to `prima/build` (`git push origin build:refs/heads/prima/build` only), the leftover refs that held the original `target/` history were removed, and `branch.build.merge` was retargeted to `refs/heads/prima/build`. Left for the next trial to confirm.

**Q58. [TRIAL-K7] (builder lane, not a Director question) Should the builder refuse symlinks under its sources, and check each seated face against the committed blob?**
Evidence: `docs/trial/kernel-trial-7.md` finding 1 (T18, T18b, T18c).
- The builder follows symlinks (`build.mjs:93`, `:101`), but `historySeats` reads only face 00 blobs committed under `kernel/` and skips `/parked/` (`:305`, `:310`). A symlinked face 00 is committed as link text, so a seat added and later removed through the link leaves no trace the guard reads. The un-seat with no record builds clean, also in a fresh clone.
- A symlinked book folder into `kernel/parked/` does the same for a whole book. A seated face can be a link to an untracked file, so its bytes are not in git.
- Option A: refuse any symlink (`lstatSync`) among book folders and face files, with a test like T18.
- Option B: also require, for every seated face, `git ls-tree HEAD <path>` mode `100644` with blob equal to the seat blob.
- Option C: both. `7` until a lane takes it.

Decided by KERNEL pass 9 (step 1), builder lane: option C (A and B), plus a history fallback.
- (A) The builder follows no symlink. Book folders, `kernel/samples`, every entry in a book folder, `books/` and each book file, cited trial files and cited `docs/spec` files are checked from the repo root down with `lstat`; a link at any step, or a path outside the repo, is an error. A symlink committed or staged under `kernel/`, `books/`, `docs/trial/` or `docs/spec/` is an error too.
- (B) Every seated face must be a regular file in git (mode 100644) whose blob is the seat blob: at HEAD under `--check`, and in the index (else HEAD) when writing, so a seat can be built before its commit. A symlink, an untracked path or a different blob is an error. This is checked after the trial or ruling, so those errors still come first.
- History fallback: a symlink ever committed under `kernel/` is followed in history (its link text names a path, and that path's history is walked too, `/parked/` included under a linked folder), so a seat added and removed through a link (T18, T18b) is still found.
- 7 tests: T18 live and in history, T18b live and in history, T18c live and committed as a link, and an untracked seated face. Each fails on the pass 8 builder and passes now. Left for the next trial to check.

**Q59. [TRIAL-K7] (builder lane, not a Director question) How should `trialOrigin` read a root commit?**
Evidence: `docs/trial/kernel-trial-7.md` finding 2 (T11).
- `--format=C %H %P` (`build.mjs:200`) gives `C <sha> ` with a trailing space for a root commit, which the regex at `:205` does not match. An add in a root commit is filed under the wrong commit or `null`; T11 (an orphan branch merged in) crashes at `:211` with a TypeError. It fails closed.
- Proposed: allow trailing space or `trim()` the line, give a clear error, and add a test like T11. `7` until a lane takes it.

Decided by KERNEL pass 9 (step 1), builder lane: taken.
- The header regex allows the trailing space, so a root commit is parsed like any other. An add listed under a header the builder cannot read blocks the seat with a message, not a crash. `HIST` adds `--root`, so `log.showRoot=false` cannot hide a root commit's adds.
- A root commit that adds only the trial file (and `kernel/QUESTIONS.md`) is an origin like any other first add; the touch rule now uses `git diff-tree --root`, which lists a root commit's files against the empty tree.
- With `-m`, a merge of an unrelated history lists every file as added against the orphan side. A merge add whose blob a parent already holds at that path is the parent's add (and `--full-history` walks it), so it is not counted twice. A merge that brings a blob no parent has is still counted. Without this, merging any orphan history blocked every seat whose trial had a later appendix.
- 2 tests: T11 (an orphan's edited trial copy, merged in) is now the "added more than once" refusal, not a TypeError; a trial added by an orphan root commit and merged in seats a face. Both fail on the pass 8 builder and pass now.

**Q60. [TRIAL-K7] (builder lane, not a Director question) Should `incoming` stay in the publish copy between rounds?**
Evidence: `docs/trial/kernel-trial-7.md` part C3, finding 4.
- After the Q57 cleanup, a bare `git push` goes only to `prima/build`, and `refs/original` and the stale `origin/build` are gone. `refs/heads/incoming` (`2db15dd`) still reaches commits that touch `target/`, so `git push --all`, `--mirror` or `git push origin incoming` would publish them. The Q57 note says the leftover refs were removed.
- Option A: delete `incoming` after each cherry-pick (it is re-fetched each round).
- Option B: keep it, and set `remote.origin.mirror=false` plus a pre-push hook that refuses any ref but `build`.
- Option C: keep it as is and correct the Q57 note. Report only: nothing was changed. `7` until a lane takes it.

Noted by KERNEL pass 9: Prima handles this in the publish copy (this lane did not touch it). Option A: the `incoming` branch is deleted after each publish, and later fetches use `FETCH_HEAD` (`git fetch ../repo build`, then cherry-pick from `FETCH_HEAD`), so no leftover ref holds the local `target/` history. This lane's own proof used a scratch clone of the publish copy with `FETCH_HEAD`, never an `incoming` branch. Left for the next trial to confirm.

Checked by TRIAL-K8 (`docs/trial/kernel-trial-8.md` part C3): option A landed. The publish copy has no `incoming` ref, a bare push goes only to `prima/build`, and no ref reaches a `target/` commit. Report only: `.git/FETCH_HEAD` and the reflogs still reach 2 `target/` commits; they are not refs, so `--all` and `--mirror` do not push them.

**Q61. [TRIAL-K8] (builder lane, not a Director question) Should the history fallback behind the symlink refusal cover every link shape, or be called best-effort?**
Evidence: `docs/trial/kernel-trial-8.md` finding 1 (H1, H2, H5).
- `historySeats` misses three shapes: a link at `kernel` itself (the walk is `-- kernel/`), an absolute link that points inside the repo (skipped at `build.mjs:391`), and a two-hop chain (the second hop's target is filed as a folder, `:394-395`). A seat line added and removed through any of them leaves no trace the guard reads.
- None of these states can build: the live refusal stops every commit where the link exists, so no seat was ever valid there. The pass 9 note says "a symlink ever committed under `kernel/` is followed in history", which holds only for one-hop relative links under `kernel/`.
- Option A: also walk `-- kernel` (no slash), resolve absolute targets that land inside the repo, and carry the page through chains, with tests like H1, H2, H5.
- Option B: keep the code, and say in the code comment, Q58 note and BUILD-LOG that the fallback is best-effort and the live refusal is the guard.
- `7` until a lane takes it.

**Q62. [TRIAL-K8] (builder lane, not a Director question) Should `--check` require face 00 (and every file it reads under `kernel/`) to be the committed bytes, or read past seats from the history of `books/`?**
Evidence: `docs/trial/kernel-trial-8.md` finding 2 (H3).
- `gitEntry` checks only the seated face. Face 00, which holds the seat line, is read from disk. With face 00 untracked and excluded, a seat was built and `books/` committed; local `--check` passed with `seats 27`. Later face 00 was put back without the seat and the books line dropped: exit 0, `seats 26`, also in a fresh clone. The seat is recorded only in `books/` history, and `priorSeats` reads `HEAD:books/` only.
- Local only: a fresh clone at the seat commit refuses it ("no face 00"). Same class as the gitfile swap.
- Option A: under `--check`, every file read under `kernel/` must be tracked and equal its HEAD blob (or at least each face 00).
- Option B: also read past seats from every `books/` blob on HEAD's history, as face 00 history is read now.
- Option C: both. `7` until a lane takes it.
