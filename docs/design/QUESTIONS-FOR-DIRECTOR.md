# Questions for the Director

state: draft. made: 2026-11-11, lane DECISIONS (Prima build), under ruling R22 ("keep moving forward, save questions").
what: every open question from the build, saved in one place. Each one appears once. Repeats are folded together.

## How to read this

- One question per section. One idea per line.
- Hard words are in brackets, for the builders. You can skip them.
- **Order:** the question that holds up the most work comes first.
- **Now:** what the builders are doing until you answer. It is marked `7` (not settled).
- **Raised:** where the question was first asked. Links are to files in this repo.
- **Log:** the matching rows in [DECISIONS-LOG.md](DECISIONS-LOG.md).
- Prima asks you one at a time. Nothing here needs an answer today.
- Questions you already answered are listed at the end, so nothing is asked twice.

Counts: 66 open, 1 held (do not re-ask), 40 answered or closed. (CONFLICTS D11, D12, D13, D14 and D16 are still open, as QD25, QD10, QD13, QD26 and QD24.) Updated 2026-11-11 evening (Designer): R23-R25 recorded; QD05 answered by R25; QD66 and QD67 saved. Updated 2026-11-11 7:15 PM EST (Prima): QD02 has a Tester working path (D319), still open, pending Director review. Updated 2026-11-11 7:20 PM EST (Prima): QD01 has a Tester working path on reseating (D320–D325), still open; see WORKING-PATH-LINEAGE.md.

---

## Open, most work blocked first

### QD01. Is face 05 a seated face now, or does it stay a task list?
- You said (R22): each page gets a seated face 05, its MVP work pack.
- The spec says face 05 is a task list, and a task list is never seated (seqAddr.md:199, decisions.md:198).
- Option A: face 05 becomes a normal face. It is seated. Its tasks are cards on it.
- Option B: face 05 stays a task list. One summary card is seated, and the tasks stay numbered (05.01 to 05.98).
- Also: may notes (06) and dictionary sections be seated? (part of kernel Q35)
- Blocks: the work pack on every page, plus 5 held faces.
- Now: `7`. R23 and R24 go further: we climb 05.01 through 05.06, then seat 05 as the best pack. If the page's work grows, we start 05.07 from that seated pack, and later reseat an update. The older seated 05 stays in the line. This is close to option B's numbered counters, with face 05 itself seated (option A). Working path (Tester, 2026-11-11 evening), not a ruling: the update is a new counter (05.07 beside 05.02); the builder should not silently replace the same address. See [WORKING-PATH-LINEAGE.md](WORKING-PATH-LINEAGE.md). Leftover: whether notes (06) and dictionary sections may be seated.
- Raised: [kernel Q35](../../kernel/QUESTIONS.md) line 181; [R22](../spec/DIRECTOR-RULINGS.md) line 86; [R23](../spec/DIRECTOR-RULINGS.md) line 90; [R24](../spec/DIRECTOR-RULINGS.md) line 94; [OPEN O44](OPEN.md) line 250 (tasks and tickets).
- Log: D53, D183, D225, D320.

### QD02. Which page types are there?
- You said (R19): each page type can have its own registry fields.
- The kernel lists six types: system, general, code, workflow, band, pointer.
- None of them fits: the door page 0000, an override page, the common questions page, or the axioms.
- Option A: add new types, like door, override, questions.
- Option B: keep six types, and put the role in a registry field.
- Also: do continuation pages (99, 9999, PP99) count as pointer, or get their own type?
- Blocks: 17 held faces (every face 00), and the face 00 checker.
- Now: `7`. Working path (Tester, 2026-11-11 evening), not a ruling: add a new type only when the page lives under different laws; when pages share the same laws and only differ in details, use a registry field (`kind`). Add `door` (page 0000), `override` (0001-0009), and `axioms` (desk-level, R6). Do not add a type for the common questions page yet (`system` plus `kind: questions`). Continuation pages use `pointer` with `kind: continuation`. Full write-up: [WORKING-PATH-QD02.md](WORKING-PATH-QD02.md). Pending Director review.
- Raised: [kernel Q33](../../kernel/QUESTIONS.md) line 169; [face00.md F10](../spec/face00.md) line 474; face00.md gaps line 150; [OPEN O35](OPEN.md) line 241.
- Log: D37, D152, D156, D319.

### QD03. Is the face list in face 00 written by hand, or worked out by the computer?
- You said (R10): face 00 lists the page's faces.
- An older rule says such lists are never written by hand (decisions.md:301, format.md:102).
- Option A: the computer writes the list and checks it. A mismatch is flagged.
- Option B: nobody writes it. It is always worked out from the faces that exist.
- Blocks: every face 00, the kernel builder, the .seq checker and the core.
- Now: `7`. The kernel writes it and checks it. The .seq file flags a mismatch. The core does not check.
- Raised: [kernel Q27](../../kernel/QUESTIONS.md) line 136; [face00.md F2](../spec/face00.md) line 466; [CONFLICTS D5](../../kernel/CONFLICTS.md) line 152; [seqpage S8](../spec/seqpage-QUESTIONS.md) line 34.
- Log: D83, D158, D159, D160.

### QD04. Is face 00 itself in its own face list?
- The face list leaves out face 00 itself.
- Face 00 can be a draft while another face is seated (R14).
- Option A: the stamp `state:` is the page's state. Face 00's own state comes from its file.
- Option B: face 00 is listed like any other face.
- Blocks: every face 00.
- Now: `7`. Option A is used.
- Raised: [kernel Q38](../../kernel/QUESTIONS.md) line 196.
- Log: D158.

### QD66. Are 00.counter faces seated the normal way?
- You said (R25): face 00 is not seated the same way. A 00.counter lists 00's fingerprint before each change.
- If we seat a 00.counter the normal way, that seat is written onto face 00 (R25: seat records may still go there). That is another change to 00, so we would need another 00.counter snapshot, and if we seat that one too, the same thing happens again.
- Option A: no. A 00.counter is write-once evidence. It is not seated the same way as other faces. (The design draft recommends this.)
- Option B: yes. A 00.counter is seated after a trial, like any other face. Then we need a rule that stops the cascade.
- Blocks: building the 00.counter, and any future seat of face 00.
- Now: `7`. Draft proposal in [00-counter.md](00-counter.md).
- Raised: [R25](../spec/DIRECTOR-RULINGS.md) line 99 (held 7); [kernel Q51](../../kernel/QUESTIONS.md) line 266.
- Log: D318.

### QD67. How does the 00.counter list climb when a new fingerprint is added?
- You said (R25): the list lives on its own face, not inside 00.
- Option A: each snapshot is a new counter, 00.01 then 00.02 and so on. Once written, that face is not edited. The list is the series of faces. This matches how 05 climbs (R24) and axiom 6 (the past is not rewritten). (The design draft recommends this.)
- Option B: one 00.counter face holds the whole list, and a new line is added to it each time. That would change that face's fingerprint each time.
- Also: after counter 98, what happens is the same open question as QD16.
- Blocks: building the 00.counter.
- Now: `7`. Draft proposal in [00-counter.md](00-counter.md) (option A).
- Raised: [R25](../spec/DIRECTOR-RULINGS.md) line 99 (held 7).
- Log: D317.

### QD06. Is the sign-in design right?
- Today every write needs a personal token (a secret key).
- The token says who you are. Only your token can approve as Director.
- The name "compute" can't be used from outside.
- Tokens sit in one file on the computer (books/.identities), never in git.
- Also open: the user levels 02, 03 and 05-09 (who may do what).
- Blocks: every write path, the app's sign-in, and the kernel write rule (QD07).
- Now: `7`. Built and tested this way.
- Raised: [compute trial finding 1](../trial/compute-trial.md) line 22; [CONTRACT addendum](../CONTRACT.md) line 38; [BUILD-LOG](../BUILD-LOG.md) line 140; [OPEN O15](OPEN.md) line 113.
- Log: D97, D255, D256, D286.

### QD07. Who may change the kernel book?
- Option A: only an admin at level 00.
- Option B: anyone, through a proposal you or R2 approve (today).
- Blocks: the kernel's safety; links to QD06.
- Now: `7`. Option B. Only "kernel-only" cards are locked.
- Raised: [kernel Q17](../../kernel/QUESTIONS.md) line 96; [core trial finding 8](../trial/core-trial.md) line 58.
- Log: D171, D266.

### QD08. Where does a page keep its state?
- You said (R12): in the stamp in face 00.
- An older rule also puts it in the page's name ending (like 1001.draft).
- Option A: the stamp only. Drop the name ending.
- Option B: both, and they must agree.
- Option C: the name ending decides; the stamp copies it.
- Also: when the written state and the real state differ, which wins?
- Blocks: kernel page 0053, every face 00, the core and the .seq file.
- Now: `7`. Both are written. A mismatch is flagged, never refused.
- Raised: [kernel Q31](../../kernel/QUESTIONS.md) line 157; [OPEN O5](OPEN.md) line 48; [BUILD-LOG](../BUILD-LOG.md) line 121.
- Log: D44, D154.

### QD09. What is the exact address of the axioms?
- You said (R6): the axioms sit on the desk as 00.axioms.
- The working address is 00.00.axioms.
- The address rules can't read that form yet.
- Option A: a new form, two numbers plus a title.
- Option B: a short name for a fixed page in the kernel book.
- Blocks: 7 held axiom faces.
- Now: `7`. Stored as 00.00.axioms; the core doesn't model it.
- Raised: [kernel Q28](../../kernel/QUESTIONS.md) line 140; [CONFLICTS D3](../../kernel/CONFLICTS.md) line 150.
- Log: D124, D144.

### QD10. Is the dictionary's 03.00 a door?
- You said "door" (R16).
- You also said faces have no doors (R9).
- Option A: the dictionary is the one exception.
- Option B: no 03.00. The dictionary menu becomes a card on face 03.
- Blocks: 5 held faces (kernel 0055 and the dictionary).
- Now: `7`. The old text stays. Nothing is built on 03.00.
- Raised: [kernel Q29](../../kernel/QUESTIONS.md) line 144; [face00.md F4](../spec/face00.md) line 468; [CONFLICTS K03](../../kernel/CONFLICTS.md) line 28, D12 line 159.
- Log: D64, D181, D182.

### QD11. Which faces are task lists, on which page types?
- Option A: each page type says which of its faces are task lists.
- Option B: keep a fixed list: 05, 06 and the dictionary 0012.03.
- Blocks: 2 held faces, and the core rule.
- Now: `7`. Option B.
- Raised: [kernel Q22](../../kernel/QUESTIONS.md) line 116; [OPEN O29](OPEN.md) line 199.
- Log: D52, D172.

### QD12. Is workflow loop .003 the law for this build? Where are F02-F10?
- .003 cites decisions F02 to F10. They are not in the repo.
- Also waiting from you: the `axioms/` folder and `.003-notes`.
- Blocks: kernel page 0057 and the work loop.
- Now: `7`. .003 is copied as a draft.
- Raised: [OPEN O7](OPEN.md) line 62; [CONFLICTS K15](../../kernel/CONFLICTS.md) line 98.
- Log: D98, D112, D113.

### QD13. What are the four sections below page 0100?
- You said (R17): four sections. 0000-0019 static, 0020-0099 working.
- The spec lists five rows.
- Option A: 0000-0009, 0010-0019, 0020-0049, 0050-0099.
- Option B: another split.
- Blocks: kernel 0051.
- Now: `7`.
- Raised: [kernel Q30](../../kernel/QUESTIONS.md) line 151; [CONFLICTS D13](../../kernel/CONFLICTS.md) line 160.
- Log: D60, D132.

### QD14. In R14, which "door" did you mean?
- R14: a face may be seated while its page's door is a draft.
- Option A: the page's own face 00.
- Option B: the book's door page 0000.
- Option C: both.
- Now: `7`. Both are allowed.
- Raised: [kernel Q32](../../kernel/QUESTIONS.md) line 163.
- Log: D187.

### QD15. May a task start straight at "pack"?
- One spec line says only the computer moves a task to pack.
- An example in another file starts a task at pack.
- Now: `7`. Allowed.
- Raised: [kernel Q21](../../kernel/QUESTIONS.md) line 112; [OPEN O19](OPEN.md) line 138.
- Log: D211.

### QD16. What happens after task 98?
- Faces have no slot 99 now (R9).
- Option A: the face is full; new work goes on a next page.
- Option B: closed tasks are archived.
- Now: `7`. Task 99 is refused.
- Raised: [kernel Q25](../../kernel/QUESTIONS.md) line 128.
- Log: D58, D174.

### QD17. Does a book see the kernel's tasks and notes?
- Option A: yes, like any face (today).
- Option B: no. Tasks belong to their own book.
- Now: `7`. Option A.
- Raised: [kernel Q15](../../kernel/QUESTIONS.md) line 88; [core trial finding 6](../trial/core-trial.md) line 48.
- Log: D224.

### QD18. When a book retires its own copy of a page, does lookup go on to the parent?
- Option A: yes, the parent's copy is found (today).
- Option B: no. Retired means "not here", so it comes back missing.
- Now: `7`. Option A.
- Raised: [kernel Q16](../../kernel/QUESTIONS.md) line 92; [OPEN O21](OPEN.md) line 151.
- Log: D94, D141.

### QD19. Can a draft be the return link for a pointer?
- Option A: yes, drafts count (R5).
- Option B: no, the return link must be seated.
- Now: `7`. Option A.
- Raised: [kernel Q19](../../kernel/QUESTIONS.md) line 104.
- Log: D143.

### QD20. Does the "every 01/02 card needs a 04 card" rule apply to task lists?
- Now: `7`. Skipped for task lists.
- Raised: [kernel Q20](../../kernel/QUESTIONS.md) line 108; [OPEN O28](OPEN.md) line 193.
- Log: D169.

### QD21. Does the computer's own write need a seat approval?
- It writes doors and worked-out pages.
- Now: `7`. Exempt, except when it promotes a draft.
- Raised: [kernel Q23](../../kernel/QUESTIONS.md) line 120.
- Log: D201.

### QD22. What record lets the computer take back someone's abandoned task?
- Option A: a written "abandoned" decision with an approval.
- Option B: a time-out rule.
- Now: `7`. Refused until you decide.
- Raised: [kernel Q18](../../kernel/QUESTIONS.md) line 100.
- Log: D109, D219.

### QD23. Where does a door page keep its return link?
- A door page holds only face 00 (R10), so it has no face 08.
- Option A: a line in face 00.
- Option B: pointers never aim at a door page.
- Now: `7`. Option A.
- Raised: [kernel Q26](../../kernel/QUESTIONS.md) line 132.
- Log: D142.

### QD24. Same CC, different title: do you want to be told?
- R18 matches pages by CC and title.
- An older rule raised a title mismatch to you, in case it is a typo.
- Option A: not a set, nothing raised.
- Option B: not a set, but you are told.
- Now: `7`. Nothing is raised.
- Raised: [kernel Q37](../../kernel/QUESTIONS.md) line 191; [CONFLICTS D16](../../kernel/CONFLICTS.md) line 163.
- Log: D63, D135.

### QD25. May titles have capital letters?
- Your R18 example is IDE-design.
- The title rule allows only lowercase letters, digits and hyphens.
- Now: `7`. Capitals are refused.
- Raised: [CONFLICTS D11](../../kernel/CONFLICTS.md) line 158; [BUILD-LOG](../BUILD-LOG.md) line 124.
- Log: D134.

### QD26. Add a "question" card type to the kernel?
- The common questions cards use type "question".
- The kernel's card type table has no such type.
- Now: `7`. Accepted anyway.
- Raised: [CONFLICTS D14](../../kernel/CONFLICTS.md) line 161.
- Log: D36, D180.

### QD27. Is page 0013 the right home for the common questions list?
- It sits next to the dictionary on 0012.
- Now: `7`. 0013 is used.
- Raised: [BUILD-LOG](../BUILD-LOG.md) lines 128, 139; [kernel trial 2](../trial/kernel-trial-2.md) line 255.
- Log: D147, D290.

### QD28. Which face 00 problems should stop a write, not just be flagged?
- Now: `7`. All are flagged only.
- Raised: [face00.md F3](../spec/face00.md) line 467.
- Log: D161.

### QD29. What is the exact layout of face 00?
- Now: `7`. A stamp at the top, then a Registry card.
- Raised: [face00.md F9](../spec/face00.md) line 473.
- Log: D160, D289.

### QD30. What should the lineage line show?
- Option A: the chain up (page, book, shelf, desk, kernel).
- Option B: the trail of who allowed it.
- Option C: both. Should face 08 links be in it?
- Now: `7`. The chain up only.
- Raised: [face00.md F5](../spec/face00.md) line 469; [seqpage S3](../spec/seqpage-QUESTIONS.md) line 14.
- Log: D155, D241.

### QD31. What does a workflow page's approval record look like?
- Now: `7`. Not built.
- Raised: [face00.md F6](../spec/face00.md) line 470.
- Log: D156.

### QD32. What owner kinds can a system page have?
- Proposed: kernel-only, desk-local, book-local.
- Now: `7`.
- Raised: [face00.md F7](../spec/face00.md) line 471.
- Log: D156.

### QD33. What does the "code" page type mean?
- Now: `7`. "A page whose faces describe code."
- Raised: [face00.md F11](../spec/face00.md) line 475.
- Log: D156.

### QD34. Is the .seq file layout OK, including lines that change?
- Lines with `:=` (worked-out lines) can change. All other lines only grow.
- Now: `7`. Built this way. See [SEQ-GUIDE.md](../spec/SEQ-GUIDE.md).
- Raised: [seqpage S1](../spec/seqpage-QUESTIONS.md) line 5; [OPEN O22](OPEN.md) line 157.
- Log: D03, D238.

### QD35. Should a .seq file list where borrowed faces come from?
- Borrowed faces (from shelf, desk or kernel) are not in the file.
- Now: `7`. Not listed.
- Raised: [seqpage S2](../spec/seqpage-QUESTIONS.md) line 10.
- Log: D241.

### QD36. Should spaces at the end of a line be made visible in a .seq file?
- Now: `7`. Kept as they are, not shown.
- Raised: [seqpage S4](../spec/seqpage-QUESTIONS.md) line 18.
- Log: D245.

### QD37. Can you write a .seq file by hand to ask for a new page?
- Now: `7`. Yes, it becomes a proposal.
- Raised: [seqpage S5](../spec/seqpage-QUESTIONS.md) line 22.
- Log: D246.

### QD38. Is the right place for "why it is a draft" a reason field on the write?
- Now: `7`. Yes, with a why-NN line in face 00 too.
- Raised: [seqpage S7](../spec/seqpage-QUESTIONS.md) line 30.
- Log: D157, D206, D207.

### QD39. Can a card's name go in an address, like ...1014.01.ham?
- Raised: [OPEN O12](OPEN.md) line 94.
- Log: D66.

### QD40. Which band number is "build"?
- One file says 05, the proposed band map says 03.
- Raised: [OPEN O13](OPEN.md) line 100; [CONFLICTS K08](../../kernel/CONFLICTS.md) line 60.
- Log: D114.

### QD41. Is a desk's door written DD.00, or as a page DD.00.00.0000? Same for a shelf.
- Raised: [OPEN O14](OPEN.md) line 107.
- Log: D50.

### QD42. Should the drafting steps (copy, note, merge, promote) become law?
- Also: all-or-nothing proposals.
- Now: `7`. Built and on by default.
- Raised: [OPEN O20](OPEN.md) line 145.
- Log: D77, D88, D196.

### QD43. What is "written permission"?
- Raised: [OPEN O25](OPEN.md) line 175; [CONFLICTS K14](../../kernel/CONFLICTS.md) line 93.
- Log: D116.

### QD44. Does a return live on its own task number?
- Raised: [OPEN O26](OPEN.md) line 181; [CONFLICTS K12](../../kernel/CONFLICTS.md) line 84.
- Log: D115.

### QD45. What are the axioms' faces called?
- Raised: [OPEN O27](OPEN.md) line 187; [CONFLICTS K09](../../kernel/CONFLICTS.md) line 65.
- Log: D124.

### QD46. How far is a snapshot trusted, and when is one taken?
- Now: `7`. Every snapshot is checked against the log.
- Raised: [OPEN O30](OPEN.md) line 205.
- Log: D84, D230.

### QD47. Is the computer's fixed start-up (bootstrap) law? Does the kernel also steer task routing?
- Raised: [OPEN O31](OPEN.md) line 211.
- Log: D91, D129, D250.

### QD48. Do the reserved numbers 01-09 apply to tasks and dictionary sections?
- Raised: [OPEN O32](OPEN.md) line 217; [CONFLICTS K05](../../kernel/CONFLICTS.md) line 38.
- Log: D15.

### QD49. Page 0117 (pack-lint) sits in a band the workflow doesn't use. Keep it there?
- Raised: [OPEN O33](OPEN.md) line 223; [CONFLICTS K13](../../kernel/CONFLICTS.md) line 89.

### QD50. How are face 08 links stored and traced?
- Raised: [OPEN O36](OPEN.md) line 242.
- Log: D40, D261.

### QD51. What fields does a note carry?
- Raised: [OPEN O37](OPEN.md) line 243.
- Log: D39.

### QD52. Does a failure count only against a word meaning (brand) that was guessed?
- Raised: [OPEN O38](OPEN.md) line 244.
- Log: D73.

### QD53. Where does a new word meaning (brand card) go?
- Raised: [OPEN O39](OPEN.md) line 245.
- Log: D74.

### QD54. What happens when review rejects a draft?
- Raised: [OPEN O40](OPEN.md) line 246.
- Log: D79.

### QD55. May a page type turn drafting off, for scratch pages?
- Raised: [OPEN O41](OPEN.md) line 247.

### QD56. Should clients talk to the computer by web calls (HTTP), MCP, or both?
- Now: `7`. Web calls only.
- Raised: [OPEN O42](OPEN.md) line 248.
- Log: D93, D264.

### QD57. How are two copies of a book that changed apart merged?
- Raised: [OPEN O43](OPEN.md) line 249.
- Log: D93.

### QD58. Should face 05 split into tasks (01-49) and tickets (50-99)?
- Linked to QD01.
- Raised: [OPEN O44](OPEN.md) line 250.
- Log: D127.

### QD59. Should small "patch and strike" edits be allowed on a seated face?
- Raised: [OPEN O45](OPEN.md) line 251.
- Log: D127.

### QD60. What hardware?
- Raised: [OPEN O46](OPEN.md) line 252.
- Log: D93.

### QD61. The later workflow details.
- Risk list, claim time-outs, who confirms abandonment, writes across books, and more.
- Now: `7`. A proposal writes one book only.
- Raised: [OPEN O47](OPEN.md) line 253.
- Log: D109, D233.

### QD62. When results are mixed, which outcome wins? What may "carry on" do after a halt?
- Raised: [OPEN O48](OPEN.md) line 254.
- Log: D113.

### QD63. Should accented letters come back later?
- R4 is plain characters "for now".
- Raised: [OPEN O49](OPEN.md) line 255.
- Log: D04.

### QD64. Which words go in the kernel's base dictionary?
- Now: `7`. None, so page 0012 is not in the kernel.
- Raised: [BUILD-LOG](../BUILD-LOG.md) line 20.
- Log: D179.

### QD65. Do you want to check the Ask word lists and scoring?
- The computer picks the key words and weights (key 2, linking 1, question 1, pass mark 0.5).
- Now: `7`. All of it can be changed in one place.
- Raised: [BUILD-LOG](../BUILD-LOG.md) lines 137-138.
- Log: D268, D269.

---

## Held: do not re-ask

### H1. Where a title lives (v2 clash 1), and whether page 0000 has a title.
- You dismissed this card. Wait for you to raise it.
- Folds in: [face00.md F1](../spec/face00.md) line 465; [CONFLICTS K17](../../kernel/CONFLICTS.md) line 108 and D6 line 153; [OPEN O34](OPEN.md) line 229.
- Now: `7`. Page 0000's stamp holds the container title. The address has none.
- Log: D18, D21, D22, D137, D163.

---

## Answered or closed (kept so they are never asked again)

| Question | Answer | Where |
|---|---|---|
| Kernel Q51, QD05 (where is a seat written down?) | R25: seat records may still be written onto 00; the line of 00 itself is kept on a 00.counter face. How that counter climbs, and whether it is seated, are QD66 and QD67. | DIRECTOR-RULINGS.md:99 |
| R22 leftover on how 05 is seated (part of QD01) | R23: the seated 05 is the best pack. R24: climb 05.CC, then seat 05; later climb from the seat and reseat an update. The older 05 stays in the line. QD01 leftover is notes (06) and dictionary sections. | DIRECTOR-RULINGS.md:90, 94 |
| Kernel Q1 (axioms page number) | R6: on the desk as 00.axioms. Exact address is QD09. | DIRECTOR-RULINGS.md:25 |
| Kernel Q2, OPEN O3 (are drafts found?) | R5: yes, and show why. | DIRECTOR-RULINGS.md:18, 28 |
| Kernel Q3, OPEN O8 (override form) | R7: its own page in 0001-0009. Then R21: no override pages for now. | DIRECTOR-RULINGS.md:31, 82 |
| Kernel Q4, OPEN O11, seqpage S6 (draft address) | R8: ...PPPP.FF.draft, only while drafting. | DIRECTOR-RULINGS.md:34 |
| Kernel Q5, OPEN O6 (face door FF.00) | R9: faces have no doors. | DIRECTOR-RULINGS.md:37 |
| Kernel Q6, OPEN O9 (door page content) | R10: page 0000 holds only face 00. | DIRECTOR-RULINGS.md:40 |
| Kernel Q7, OPEN O18 (Bob test, "what is my name") | R11: a common questions list. | DIRECTOR-RULINGS.md:43 |
| Kernel Q8, seqpage S9 (where state and title live) | R12: in face 00. Page tail part is QD08. | DIRECTOR-RULINGS.md:53 |
| Kernel Q9, OPEN O23 (band head word) | R13: "band". | DIRECTOR-RULINGS.md:56 |
| Kernel Q10, OPEN O4 (seat under a draft door) | R14: yes. Which door is QD14. | DIRECTOR-RULINGS.md:59 |
| Kernel Q11, OPEN O17, CONFLICTS D9 (brand needs 04?) | R15: no. | DIRECTOR-RULINGS.md:62 |
| Kernel Q12, OPEN O16 (03.00) | R16: "door", but it clashes with R9. Still open as QD10. | DIRECTOR-RULINGS.md:65 |
| Kernel Q13, OPEN O24 (below 0100) | R17: four sections. Exact split is QD13. | DIRECTOR-RULINGS.md:68 |
| Kernel Q14, OPEN O13 (band sets) | R18: CC plus title. "Build" band is QD40. | DIRECTOR-RULINGS.md:71 |
| Seqpage S8 (what face 00 holds) | R19: stamp, type, registry by type. | DIRECTOR-RULINGS.md:74 |
| OPEN O1 (same model counts as a different view?) | R20: yes, a fresh session counts. | DIRECTOR-RULINGS.md:78 |
| OPEN O2, CONFLICTS D8 (stamp on every face?) | R12: only face 00 has the stamp. | DIRECTOR-RULINGS.md:53 |
| OPEN O5 (where state lives) | R12 in part. The rest is QD08. | DIRECTOR-RULINGS.md:53 |
| OPEN O10 (axioms page number) | R6. | DIRECTOR-RULINGS.md:25 |
| OPEN O22 (what a .seq file looks like) | R3 in part, layout built. Approval is QD34. | DIRECTOR-RULINGS.md:11 |
| Kernel Q24, seqpage S10, face00.md F8 (override page shape) | Parked by R21 (no override pages for now). | DIRECTOR-RULINGS.md:82 |
| Kernel Q36 (does an override change lookup?) | Moot under R21. | DIRECTOR-RULINGS.md:82 |
| CONFLICTS D4 (who approves an override?) | Deferred by R21 until child desks. | DIRECTOR-RULINGS.md:82 |
| CONFLICTS D15 (R21 vs R7) | R21 governs while the app is built. | DIRECTOR-RULINGS.md:82 |
| CONFLICTS D10 (R18 vs axiom 8, F.2 links) | R18 governs; shown for checking only. | DIRECTOR-RULINGS.md:71 |
| Kernel Q35 (seat a task list?) | R22, R23, R24: face 05 is seated as the best pack, after climbing 05.CC. QD01 leftover is notes (06) and dictionary sections. | DIRECTOR-RULINGS.md:86, 90, 94 |
| face00.md F12 (no reason field) | Closed: the core request now has a `reason` field. | BUILD-LOG:118 |
| Workshop clash 1 | Dismissed by you. Held as H1. | OPEN.md:229 |
| CONFLICTS K01 (door word) | R1. | DIRECTOR-RULINGS.md:3 |
| CONFLICTS K02 (boards written?) | R9. | DIRECTOR-RULINGS.md:37 |
| CONFLICTS K04 | R15. | DIRECTOR-RULINGS.md:62 |
| CONFLICTS K06 | R17. | DIRECTOR-RULINGS.md:68 |
| CONFLICTS K07 | R18. | DIRECTOR-RULINGS.md:71 |
| CONFLICTS K10 | R10. | DIRECTOR-RULINGS.md:40 |
| CONFLICTS K16 | R13. | DIRECTOR-RULINGS.md:56 |
| CONFLICTS K18 | R5. | DIRECTOR-RULINGS.md:18 |
| CONFLICTS D1, D2, D3, D5, D6, D7 (ruling vs older text) | Rulings govern; open parts are QD03, QD09, H1. | CONFLICTS.md:148-154 |
| OPEN O19 part (draft task rewrite) | Closed in the core: a draft task is never rewritten. Pack part is QD15. | core-trial.md:177 |
| OPEN O28 part (9999 title) | Closed by the spec: 9999 needs a title (A2.8). 04 part is QD20. | core-trial.md:172 |
