# Open questions for the Director

state: draft. Prima brings these to the Director one at a time, in this order.
made: 2026-11-11, lane DESIGN.
sources: `kernel/QUESTIONS.md` (Q1-Q14), `kernel/CONFLICTS.md` (K01-K18, W01-W15), `docs/trial/kernel-trial.md`, `docs/trial/core-trial.md`, `docs/BUILD-LOG.md`, and Prima's review of the Workshop branch (`/workspace/prima/workshop-claude/review.md`, five clashes with the v2 seqaddr page).

## How this list works

- Each question appears once. Where two files ask the same thing, they are folded together, and the "Folds" line names them.
- Nothing here is answered. Each option is quoted from his own files where it can be.
- **Ranking:** by how many built things a question holds up. A built thing is held up if it can't be seated, finished, or pass its checks until he answers.
- The built things are: 54 booked faces (43 kernel and 11 sample), and the components core, compute, app, kernel builder and seqpage. Counts are rough, and the "Blocks" line shows what was counted.
- Citation keys are the same as in `DESIGN.md`. `[v2:N]` is the Director's page `seqaddr.director.2026-11-09.v2.md`.
- **Don't re-ask:** v2 clash 1 (title in the address versus the stamp) was dismissed. It is listed last as held (O34).

---

## Ranked

### O1. For a build-stage seat (R2), does a fresh session of the same model count as "a different view"?
Every builder and every trial in this build is the same model, each in its own session. If a fresh session doesn't count, nothing can be seated under R2.
- A: Yes. A fresh sitting counts, as long as it isn't the maker's own session.
- B: No. "must the pass come from a different intelligence (a person, another model, compute)" [decisions.md:591].
- Linked: the compute "cannot check that the trial came 'from a different view than its maker'" [BUILD-LOG:59]. How review is recorded is still open [drafting.md:45].
- Blocks (~56): seating any of the 54 faces under R2, the compute's R2 gate, and the core's promote gate [core-trial:33-36].
- Folds: decisions E7 open part, core-trial 2 and 3, the R2 gate's `7`.

### O2. Does every face carry its own stamp at its top, or only the door face 00?
- A: Every face. "Must have a stamp the as the header explaining the context and what face" [v2:58].
- B: Only face 00. "Faces carry no stamp of their own; the page stamp is stored once" [decisions.md:176].
- Blocks (~56): the shape of all 54 faces, the core's stamp reader [BUILD-LOG:42], and the .seq layout.
- Folds: v2 clash 2 [prima-review:132], BUILD-LOG:22. R1 already makes 00 the door [R1], so this asks only where the stamp lives.

### O3. When a book looks up a face and the only copy is a draft, is it found?
- **ANSWERED 2026-11-11 2:55 PM EST: yes, drafts are found (ruling R5).**
- A: No. A draft is "being written; not active" [seqAddr.md:133]. Today every inherited lookup comes back missing [BUILD-LOG:57].
- B: Yes. "Draft faces count" [seqAddr.md:164], and "Books follow the kernel live" [seqAddr.md:104].
- Also: should a draft or open counter (a task) be inherited from the kernel at all? The core does it now, against its own promise [core-trial:48-51].
- Blocks (~48): all 43 kernel faces reaching any book, the sample override page 0056, and the lookup in the core, compute, app and builder.
- Folds: Q2, K18, kernel-trial 5 and 14, core-trial 6, BUILD-LOG:51.

### O4. Can a seated face sit on a page whose door face is still a draft?
- A: Yes. "A draft face ... may exist on any page, live or draft" [decisions.md:277].
- B: No, the door is seated first. The compute already wants "identity page first" [format.md:123].
- Blocks (~40): seating any of the 39 content faces before their doors, plus the builder's seat check [kernel/MAP.md:22].
- Folds: Q10.

### O5. Where does a page keep its state: in the stamp, in the file tail, or both?
- A: In the stamp. The stamp holds "address, title, state" [decisions.md:176], and the door face's file tail says only whether the stamp itself is approved [QUESTIONS.md:39].
- B: In the tail alone, such as `PPPP.draft` or `PPPP.retired` [seqAddr.md:126], and `state:` is dropped [QUESTIONS.md:40].
- Blocks (~18): seating the 15 door faces, the core and seqpage stamp readers, and the builder.
- Folds: Q8, BUILD-LOG:19.

### O6. Is the door of a counted face (`FF.00`, the task list) written into the book, or worked out from it?
- A: Worked out. "Boards (`FF.00`) ... are derived from the log and never written as entries" [format.md:102].
- B: Written before its counters, as "board before counters" [format.md:123]. "A face is counted if and only if `FF.00` exists" [decisions.md:196].
- Linked 1: under R1 it is the door. Does it still list "every counter and its current tail" [decisions.md:187]?
- Linked 2: does plain `FF` on a counted face mean `FF.00` [seqAddr.md:199], or is a seated face always bare FF [v2:38]? This is v2 clash 3.
- Blocks (~15): 10 counters with no written door (8 kernel `06.01` and the 2 dictionary sections), plus the core, compute, app, seqpage and builder.
- Folds: Q5, K02, kernel-trial 10 and 15, v2 clash 3 [prima-review:134], BUILD-LOG:31.

### O7. Is workflow loop `.003` approved as law for this build, and where are its decisions F02-F10?
- A: Keep it a draft. ".003 ... state: draft — Director review required; not live" [workflow-loop.003.md:3].
- B: Seat it after a hostile trial under R2. "Review and trial of `.003` remain due" [workflow-loop.003.md:6].
- Also: `.003` cites F02-F10, but `decisions.md` has only F.1 and F.2 [CONFLICTS.md:93-94]. Do you have the `.003` notes?
- Blocks (~12): kernel pages 0053 and 0057 (10 faces), and the core's claim and tail rules, which are provisional [BUILD-LOG:37].
- Folds: K15, W01-W15, kernel MAP 0053 and 0057.

### O8. When a book overrides a face, does it replace the whole face or only the cards it writes? And how is an override written?
- A: The whole face. "The first match wins" [seqAddr.md:104].
- B: Card by card. "The same key on two faces is the same card" [seqAddr.md:168].
- Linked: axiom 2 needs "a named override, approved by the authority above it" [Axioms.md:15]. The proposal is an "owner class ... on each law section" [decisions.md:610].
- Blocks (~8): sample `10.11.21.0056.04` and the 3 kernel 04 cards it hides, the core's C3.2 check [core-trial:117-120], `owner: kernel-only` [core-trial:58-61], the app's card matching [BUILD-LOG:15], and the builder.
- Folds: Q3, kernel-trial 6, core-trial 8 and 20, C5.4.

### O9. What content face does a door page 0000 need?
- A: None. "Page 0000 must exist for a book to be a legal space" [v2:102]. It is a special spot, not a normal page [v2:100].
- B: One, because "A page with only an identity has no reason to exist" [decisions.md:274]. The spec doesn't say which face [QUESTIONS.md:30].
- Blocks (~6): the 4 door pages (kernel, desk 10, shelf 10.11, book 10.11.21), the core's `c1_on_door_pages` rule [BUILD-LOG:39], and the builder.
- Folds: Q6, K10, kernel-trial 10.

### O10. What page number does the axioms page get?
- A: Keep 0050, the first structural page (`0050-0099 | structural pages`) [seqAddr.md:223].
- B: Another number in 0050-0099. It's listed as open: "The axioms' own page number" [decisions.md:598].
- Blocks (~6): the 6 faces of kernel page 0050.
- Folds: Q1, BUILD-LOG:18.

### O11. In a book file, how is a draft face written?
- A: As a field: `"addr":"...PPPP.01","tail":"draft"`. This is what is built [BUILD-LOG:50].
- B: In the address: `"addr":"...PPPP.01.draft"`. "`FF.draft` is its unseated draft" [seqAddr.md:201].
- Blocks (~5): the book format, the core log, the compute and app face keys [BUILD-LOG:10], the seqpage round trip, and the drafting copy step [drafting.md:11].
- Folds: Q4, kernel-trial 8.

### O12. Can a card's name sit in the address after the face, like `...1014.01.ham`?
- A: Yes. "A word after a face is a **card key**, not a title" [seqAddr.md:111].
- B: No. Cards live inside faces. "Faces exist without titles as they are a face and not a whole" [v2:32].
- Blocks (~5): the compute's `/face` card route [BUILD-LOG:62], the 2 brand addresses in the sample dictionary, the core grammar, and the app.
- Folds: v2 clash 5 [prima-review:137], C8.2.

### O13. Are pages in different bands one set because their numbers match, or only when they link both ways? And which band is "build"?
- A: By number. "Sets across bands are linked by number" [decisions.md:112].
- B: By links both ways. "Membership requires explicit reciprocal Face 08 links" [decisions.md:644], and "Agreement is not connection" [Axioms.md:27].
- Also: build is `0523` [decisions.md:112], or build is `0300` and jobs is `0500` [workflow-loop.003.md:44] [workflow-loop.003.md:46]?
- Blocks (~5): kernel page 0057's band cards.
- Folds: Q14, K07, K08, F.2, W03.

### O14. Is a desk's door `DD.00`, or a nested page `DD.00.00.0000`? The same question goes for a shelf.
- A: `DD.00` and `DD.SS.00`. "A desk must also have it's sentinal as DD.00" [v2:105]. "A shelf must also have a .00 as DD.SS.00" [v2:108].
- B: Nested pages. "Shelf `10.11` | `10.11.00.0000`" and "Desk `10` | `10.00.00.0000`" [seqAddr.md:61-62].
- Blocks (~4): the 2 sample door pages (`10.00.00.0000`, `10.11.00.0000`), and the shelf and desk steps of the lookup in the core and compute.
- Folds: v2 clash 4 [prima-review:135].

### O15. Who may do what? How does the compute know who is the Director, an admin, or a model?
- A: Use the user levels: "`00` | internal authorised admin | the kernel" ... "`04` | basic user" [decisions.md:380-384].
- B: Leave it open for now: "what exactly `02`, `03` and `05-09` grant" [decisions.md:392].
- Blocks (~4): `owner: kernel-only` enforcement and writes to the kernel [core-trial:58-61], the compute's author names [BUILD-LOG:59], and lint and close being compute-only [core-trial:38-41].
- Folds: C5.2, C5.2a, E8 levels, core-trial 4 and 8.

### O16. Is the dictionary's `03.00` a menu or a door?
- A: A menu. "`0012.03.00` is the menu of sections" [decisions.md:432].
- B: The door of a counted face, listing counters [decisions.md:187] [R1].
- Blocks (~4): the 2 sample dictionary sections, the core's counted-face list [BUILD-LOG:31], and the compute's `/brands` [BUILD-LOG:60].
- Folds: Q12, K03, BUILD-LOG:44.

### O17. Does a brand card on face 01 need a 04 card?
- A: Yes. "Every 01/02 card key has a 04 card" [decisions.md:353].
- B: No. The `brand` row says "Needs a 04 card": no [decisions.md:521].
- Blocks (~3): the 2 sample brand cards (`bob`, `cats`) and the core's card-type rule.
- Folds: Q11, K04.

### O18. Bob test, session 2: how should "what is my name" reach the `bob` card?
- A: No route. Resolving works only on a word the user types [decisions.md:496-503], so this stays `7`.
- B: A concordance, word to page [decisions.md:606]. This is a proposal waiting for you.
- C: The read path, where "a model is handed a pack built by the compute from the prompt" [Design.md:84] (proposed).
- Blocks (~3): the Bob test end to end, the `1001.04` hole, and the compute's `/brands` [BUILD-LOG:64].
- Folds: Q7, kernel-trial 4.

### O19. Can a task counter be made straight at `pack`, and can a pack still in `draft` be rewritten?
- A: Only compute's lint moves `draft -> pack` [workflow-loop.003.md:171].
- B: The book example writes a counter straight at `pack` [format.md:75].
- Also: "A full-body `put` is allowed only to create ... never to replace" [decisions.md:329].
- Blocks (~3): the core's counter rules [BUILD-LOG:33], the compute, and kernel pack lint.
- Folds: core-trial 18.

### O20. Should the drafting steps (copy, note, merge, promote) and all-or-nothing proposals become law, or stay proposed?
- A: Seat them. "the compute enforces this through its operations, so a face cannot be replaced from memory" [decisions.md:320].
- B: Keep them proposed [format.md:158].
- Blocks (~2): the core's drafting rules [BUILD-LOG:36] [BUILD-LOG:38] and the compute.
- Folds: D0 mechanism, format.md:100.

### O21. What does a retired page answer? And if a book retires its override, does the kernel's face show again?
- A: Nothing. A retired page is not live, since "location, state, and a lawful connection decide what is live" [Axioms.md:13].
- B: Its face stays readable as history only, because it is "previously seated, retired before removal" [seqAddr.md:138].
- Blocks (~2): the core resolver and the compute [core-trial:53-56] [core-trial:146].
- Folds: core-trial 7 and 10.

### O22. What does a .seq page file look like inside?
- A: Prima's proposal: the door first, then faces 01-08 as sections, cards as named blocks, and an add-only history at the end (chat, 2026-11-11 2:47 PM EST, not his words).
- B: Something else he picks. R3 sets only that it is a view and that the round trip loses nothing [R3].
- Blocks (~2): the seqpage crate and opening a .seq file in the app.
- Folds: R3.

### O23. In `.002`, "door" meant a band head like `0400`. Which word do band heads use now?
- A: "band head" [decisions.md:110] [workflow-loop.003.md:51].
- B: R1's door also covers band heads.
- Blocks (~1): the wording on page 0057.
- Folds: Q9, K16, kernel-trial 12.

### O24. How is the book split below page 0100?
- A: One reserved range, `0001-0099` [decisions.md:120].
- B: Four ranges: `0001-0009`, `0010-0019`, `0020-0049` and `0050-0099` [seqAddr.md:220-223].
- Blocks (~1): the reason given for kernel page numbers in `kernel/MAP.md`.
- Folds: Q13, K06.

### O25. What is "written permission"?
- A: A recorded grant. "This revision-bound approval is written permission to act within the agreed frame" [workflow-loop.md:88].
- B: A direct instruction [decisions.md:594].
- Blocks (~1): the pack grant in page 0057.
- Folds: E8, K14, W05.

### O26. Does a return live on its own task counter?
- A: Yes, on the same counter as the pack [decisions.md:612]. The core already does this [BUILD-LOG:37].
- B: Keep it a proposal: "`7`: seat the E9 placement" [workflow-loop.003.md:181].
- Blocks (~1): the core's return rule.
- Folds: K12, W10.

### O27. What are the axioms page's faces called?
- A: "01 agent form, 02 cite card, 03 menu, 04 full explanation, 06 notes" [Axioms.md:3].
- B: The general face jobs: "law", "schema", "operate" [seqAddr.md:150-152].
- Blocks (~1): kernel page 0050's face names.
- Folds: K09.

### O28. Does page 9999 need a title? And does the 04 rule apply to a counted 01 or 02 face?
- A: Yes to both. Pages 1000 and up "must have a title" [seqAddr.md:115], and every 01 or 02 card needs a 04 card [seqAddr.md:175].
- B: The core's choice for now: 9999 is exempt, and counted 01 and 02 faces are skipped [core-trial:84-85].
- Blocks (~1): the core's checks.
- Folds: core-trial 13.

### O29. Which faces beyond 05 and 06 may be counted?
- A: Set by page type: "Others may be counted on certain page types" [seqAddr.md:200].
- B: A fixed list for now: 05, 06 and `0012.03` [BUILD-LOG:31].
- Blocks (~1): the core's counted-face list [core-trial:113-115].
- Folds: core-trial 19.

### O30. How far is a snapshot trusted, and when is one taken?
- A: Never trusted over the log. Check it against a replay, because "The past is not rewritten" [Axioms.md:23].
- B: Leave the policy open: "when to snapshot, and when to move old entries out" [format.md:157].
- Blocks (~1): the core's replay [core-trial:43-46].
- Folds: core-trial 5.

### O31. Is the compute's small fixed start (bootstrap) law, and does the kernel also steer task routing?
- A: Seat the bootstrap. "a minimal contract fixed in compute" [decisions.md:613]. The compute already follows it [BUILD-LOG:54].
- B: Keep it proposed [kernel-design.md:4]. Routing is either "Structural/reasoning kernel" or "Kernel-directed coordination" [kernel-design.md:159-160].
- Blocks (~1): the compute's boot.
- Folds: E9 bootstrap, kernel-design 10.

### O32. Do the reserved values 01-09 apply to counters and dictionary sections?
- A: Not to counters: "the reserved 01-09 range does not apply to them" [decisions.md:36].
- B: The dictionary keeps its own: "This layout reserves `03.01-03.09` by its own definition" [decisions.md:481].
- Blocks (0): nothing built depends on this today.
- Folds: K05.

### O33. The pack-lint page `0117` sits in a band the workflow doesn't use. Is it kept there?
- A: Keep it, as "Consult the predecessor `0117.pack-lint`" says [workflow-loop.003.md:232].
- B: Move it, since `0100-0299` is "unassigned by this workflow" [workflow-loop.003.md:43].
- Blocks (0).
- Folds: K13.

### O34. HELD, DO NOT RE-ASK: where a title lives (v2 clash 1).
- v2: "DD.SS.BB.title = Book title" [v2:26]. "DD.SS.BB.0000 No title allowed" [v2:104].
- Spec: "A title stored in a stamp is the truth" [seqAddr.md:116].
- Folded in: the address shape [CONFLICTS.md:73-76], whether page 0000 has a title [CONFLICTS.md:101-104], and the core's rule that `10.tools.21.4442` is invalid [BUILD-LOG:43].
- He dismissed this clash's question card. Wait for him to raise it.

---

## Open in the spec, but nothing built waits on them yet

Each is one plain question with its source, kept so nothing is lost. None is ranked.

- O35. Do continuation pages (`99`, `9999`, `PP99`) share the `pointer` type, or get their own? [decisions.md:292]
- O36. How does the compute store and trace face 08 links? The proposed link kinds are `member-of`, `continues-from`, `references`, owner, exception and custody. [decisions.md:368] [decisions.md:609]
- O37. What fields does a note carry? The proposal is `by`, `date`, `refs`, `why`, `state` and `unresolved`. [decisions.md:409] [decisions.md:611]
- O38. Does a failure count only against a brand that was assumed? "Proposed: yes" [decisions.md:493]
- O39. Where does a new brand card go? "the model asks the user which page, or each book has a default terms page" [decisions.md:525]
- O40. What happens when review rejects a draft? [drafting.md:45]
- O41. May a page type turn drafting off, for example for scratch pages? [drafting.md:46]
- O42. Do clients talk to the compute by HTTP, MCP or both? HTTP is built for now. [format.md:155] [BUILD-LOG:58]
- O43. How are two copies of a book that were edited apart merged? [format.md:156]
- O44. Should face 05 counters split into tasks (`05.01-05.49`) and tickets (`05.50-05.99`)? [decisions.md:604]
- O45. Should "patch and strike" be allowed as small changes to a seated face? [decisions.md:605]
- O46. What hardware? [Design.md:96]
- O47. The later workflow details: risk registry, claim timeout and fencing, who confirms abandonment, approval compatibility, promotion mechanics, continuation allocation, evidence policy, cross-book writes, and workspace attribution. [workflow-loop.003.md:286-294]
- O48. When results are mixed, which outcome wins, and what does "carry on" allow after a halt? [workflow-loop.003.md:191] [workflow-loop.003.md:269]
- O49. Is accented text allowed again later? R4 is "a simplicity choice for now and may widen later" [R4].
