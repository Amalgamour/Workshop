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
