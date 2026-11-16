# The work book: a concept to read before we go ahead

For Matthew. By Designer, Mon 16 Nov 2026, 4:58 PM EST. A concept, not a ruling. Nothing here is decided. Only you approve.

**How to read the cites.**
- "You, item N" is your answer t223u, recorded word for word at docs/review/DIRECTOR-WORDS-t223u.md (2461a19). Line numbers are that file's.
- OWB means "old work book (zip from Matthew)", with a path inside 10.10.13.brand-clerk. It stays outside the repo.
- AX is Tester's axiom check, docs/review/WORK-BOOK-AXIOM-CHECK.md (c5cbf0d). SPEC is docs/design/WORK-BOOK-SPEC.md (6bcc1c0).
- `7` means open. `9` means untried.

---

## What you asked for

"I want the concept I can read before we go ahead." (You, item 5, t223u:14)

"Does this make a solid base for running our work? What changes would you make?" (You, item 6, t223u:16)

Short answer: yes, the old work book is a solid base. It already has packs, returns, a refusal with a handback, and an exact starting commit. Six changes would make it safer. They are under "Six changes Prima proposes".

## Where the work lives

Your words: "you'll host it on github then when you give the instruction prompt for me to que up the model. It can go pull down the files it needs locally. Because you don't have access to my local files." (You, item 1, t223u:6)

In plain words:
- The code and the books live on GitHub.
- Prima writes a short prompt. You paste it to start the model.
- The model pulls what it needs onto your machine.

## A pack is the job

Your words: "You write a pack. It goes into the page 05.NN next open counter. Then in the pack is the jobs list, the model then returns what it did on each." (You, item 2, t223u:8)

In plain words:
- Prima writes the pack.
- It goes in the next free slot on the page: 05.01, then 05.02, and so on. (Side label: face 05 counter.)
- The pack lists the jobs.
- The model answers each job in its return.

The old book did this. Pack 05.02 lists three jobs, each with an ask and a status (OWB, 0501.brand-clerk/05.02.md:23-36).

## Who frames it, who records it

Your words: "This is packs are how we use 6 framing the work, with 8 returning the record of work, with the scope and authority coming from you." (You, item 2, t223u:8)

In plain words:
- The pack frames the work.
- The return is the record of the work.
- Prima gives the scope and the authority.

One thing to confirm. You wrote "6" and "8". In Axioms.md, frame is axiom 5 [Axioms.md:21], lineage is axiom 6 [Axioms.md:23], and connection is axiom 8 [Axioms.md:27]. Did you mean the axioms, or something else? `7`

## Commit, push, check, assemble

Your words: "commit and push it for you to check the work on Github. YOu can pull the work and have cursor do the finally assembly on my computer." (You, item 3, t223u:10)

Your words: "you check the work, or assign a review bot to do the checks for you." (You, item 4, t223u:12)

In plain words:
1. The model commits its work and pushes it to GitHub.
2. Prima checks it there, or gives the check to a review bot.
3. Prima pulls the work. Cursor puts it together on your computer.

## Where AGENTS.md fits next to the pack (W2)

- The pack is the job list. It is the source. (You, item 2, t223u:8)
- AGENTS.md is the sheet the model reads first (SPEC B2).
- Proposal (7): the compute makes AGENTS.md from the pack, plus the page's standing rules. The model reads it. It never edits it. If the pack changes, the sheet is made again.
- The old book had the same idea. A fresh worker opened STATUS.md first, then BOOT.md, then the active pack (OWB, 0701.brand-clerk/STATUS.md:3).
- Where the sheet is kept is still W2 (below, under questions to confirm).

## How it ties to the core spec

- **Books change only through the compute.** "Yes, books change through compute not by models." (R33 item 1, DIRECTOR-RULINGS.md:159). See the open question W10.
- **The open door.** Today a program on the box can still write the books directly. K8 step 1 narrows that door (CORE-AND-TOOLS-SPEC.md:873, B1). Until then, every check must look for book changes.
- **Handbacks and packets.** "Refuse with a handback, and stop rather than invent a meaning." "Every packet says what it gathered and what it didn't." (R37 items 8 and 10, DIRECTOR-RULINGS.md:202, :204). Each return says what it did, what blocked it, and what it left out.

## What the old book teaches

- It had seven matched pages per piece of work: returns, code, modules, plan, packs, notes, inspect (OWB, 00.md:26-36, :43-44).
- A pack lived on one page and its return on another: pack 0501/05.02, return 0101/05.02.return, linked by "matched-pack" (OWB, 0101.brand-clerk/05.02.return.md:8).
- But its inspect page already kept pack and return side by side: 05.02.pack next to 05.02.return (OWB, 0701.brand-clerk/05.02.pack:7, 05.02.return:6).
- STATUS.md let a fresh worker recover the book from one file (OWB, 0701.brand-clerk/STATUS.md:1-3).
- It is rough, as you said: "it's not complete just a rough working design." (You, item 6, t223u:16)

## Six changes Prima proposes (each a proposal, 7)

Each was checked against the samples.

**1. Pack and return side by side on one page.** Use 05.NN and 05.NN.return, not seven matched pages.
- Backed. The seven bands are at OWB, 00.md:26-36. The inspect page already pairs 05.NN.pack with 05.NN.return (OWB, 0701.brand-clerk/, file list).

**2. The compute fills the state fields.**
- Backed. Pack 05.16 says "state: ready" (OWB, 0501.brand-clerk/05.16.md:6). Its return says "state: complete" (OWB, 0101.brand-clerk/05.16.return.md:3). The pack's job status lines are still blank (OWB, 0501.brand-clerk/05.16.md:34-35, :45-46). The same split shows on the inspect page: "ready" (0701.brand-clerk/05.02.pack:6) and "complete" (05.02.return:4).

**3. A return carries proof:** the commit it made, the test output, and what it did not do.
- Backed as a gap. Return 05.02 shows check output, but no commit and no test run (OWB, 0101.brand-clerk/05.02.return.md:23-39). Pack 05.16 asks for a test (05.16.md:37-43). Its return has no commit and no test output (0101.brand-clerk/05.16.return.md:1-11). The commits sit only in STATUS.md (0701.brand-clerk/STATUS.md:29, :35).

**4. Each pack names its exact starting commit on GitHub. Your local path appears only in the queue-up prompt.**
- Backed. The book itself holds your local path (OWB, 00.md:49-50; 0701.brand-clerk/STATUS.md:13). The exact commit is in STATUS.md (:10-11), not in the pack (0501.brand-clerk/05.02.md:1-21).

**5. The receipt files become lines in the one log.**
- Backed. Receipts are loose files (OWB, 0701.brand-clerk/receipts/, e.g. 2026-11-05-05.02-code__clerk.py.receipt; named in 0101.brand-clerk/05.02.return.md:29). R37 item 1: "One append-only log is the only source of truth" (DIRECTOR-RULINGS.md:195).

**6. A real gate.**
- Backed. The old 05.02 return asks for "clerk-mediated write so a model cannot bypass `check` by editing files directly in-agent" (OWB, 0101.brand-clerk/05.02.return.md:21). STATUS.md says the same, "Proposed only - not released" (0701.brand-clerk/STATUS.md:84; its dash made ASCII). One nuance: the return lists it under "Need", as the next hardening. It does not report a bypass that happened.

---

## Open questions, top three first

Proposed answers only. W8 must be ruled before the first work page exists, because page type is locked once set (R36, DIRECTOR-RULINGS.md:190; AX:33-34).

### W8 (TOP). Is a work page a system page?
1. **Question.** System pages freeze once linked (R34, DIRECTOR-RULINGS.md:170). Is a work page one?
2. **Proposed answer (Designer and Tester).** No. You read work pages. System pages are not for users (DIRECTOR-RULINGS.md:169).
3. **Why.** A wrong pack can then be fixed in place. Who gets hurt otherwise: you.
4. **Axioms checked (AX:31-32).** 1 [Axioms.md:13] pass. 2 [Axioms.md:15] pass. 7 [Axioms.md:25] pass. 9 [Axioms.md:29] tension. R32 item 2 pass. The spec also marks 6 [Axioms.md:23] pass (SPEC:394).

### W10 (TOP, new). Does a pushed return count as a book change?
1. **Question.** You said the model will "commit and push" (t223u:10). R33 says "books change through compute not by models" (DIRECTOR-RULINGS.md:159). Does a push count as a book change?
2. **Proposed answer (Designer, 7).** No, as long as the push holds only code, exports and the return text. A push never touches books/. The compute reads the pushed return. It then writes the book line itself, with the commit named. The push is a proposal. The compute decides.
3. **Why.** It keeps your push-and-check flow and R33 both. Who gets hurt otherwise: you, if a model's push quietly changes a book.
4. **Axioms checked (Designer's marks; Tester has not checked this, 9).** 1 [Axioms.md:13] pass: the compute books it. 6 [Axioms.md:23] pass: the book line names the commit. 8 [Axioms.md:27] pass: the return links to its commit. 2 [Axioms.md:15] tension: the return text sits in git and in the book.

### W9 (TOP, new). Should a return sit beside its pack?
1. **Question.** Should 05.NN.return sit on the same page as 05.NN?
2. **Proposed answer (Designer, 7).** Yes. One page per piece of work, not seven matched pages.
3. **Why.** "A return and its next step are saved together" (R37 item 2, DIRECTOR-RULINGS.md:196). The old inspect page already does it. Who gets hurt otherwise: a reviewer hunting across seven pages.
4. **Axioms checked (Designer's marks; Tester has not checked this, 9).** 2 [Axioms.md:15] pass: one page, no matched copies. 6 [Axioms.md:23] pass. 8 [Axioms.md:27] pass. 9 [Axioms.md:29] tension: untried here.

## Questions your answers touch: open for you to confirm

- **W1, a real book?** You: "It goes into the page 05.NN next open counter." (t223u:8). That reads as real pages in a real book. Tester's marks: 1 tension, 2, 6 and 7 pass (AX:12-14). Confirm.
- **W2, where AGENTS.md lives.** You: "in the pack is the jobs list" (t223u:8). Your earlier words put "an agents.md in it" (DIRECTOR-WORDS-t212u.md:10). "Where AGENTS.md fits" proposes: the pack is the source and AGENTS.md is made from it. Tester: axiom 2 tension, R33 item 2 tension (AX:19-25). Confirm.
- **W3, who releases.** You: "the scope and authority coming from you" (t223u:8), that is, from Prima. Still open: the spending cap. Tester: 1 and 6 pass; 3 pass only with a written grant (AX:40-42). Confirm.
- **W6, who checks.** You: "you check the work, or assign a review bot" (t223u:12). Fits R20: a different view (DIRECTOR-RULINGS.md:79). Tester: 9, 1, R20 and R2 pass (AX:64). Confirm.
- **W7, your local space.** You: "pull down the files it needs locally" (t223u:6) and "cursor do the finally assembly on my computer" (t223u:10). Still open: please name the folder. Tester: 1, 6 and 7 pass; 2 and 8 tension (AX:70-74).

## Questions your answers do not settle

### W4. Cursor or Grok Builder for a page?
1. **Question.** You queue up the model (t223u:6). Who picks which one?
2. **Proposed answer.** If a test can check the job, the cheaper builder goes first. Two fails: stop and hand back (SPEC B4).
3. **Why.** A test lets a cheap try fail safely. Who gets hurt otherwise: you, paying twice for one miss.
4. **Axioms checked (AX:49-50).** 3 [Axioms.md:17] pass. 4 [Axioms.md:19] pass. 9 [Axioms.md:29] tension: cheaper is untried. R37 item 8 pass.

### W5. Do we record what each job cost?
1. **Question.** Should each return record time, tries, tokens and dollars?
2. **Proposed answer.** Yes, when reported. "Not reported" is not "zero".
3. **Why.** R37 item 6 (DIRECTOR-RULINGS.md:200). Who gets hurt otherwise: you, reading a blank as free.
4. **Axioms checked (AX:58).** 7 [Axioms.md:25] pass. 9 [Axioms.md:29] pass.

---

## What Prima's summary said, and what your words say

- **Who checks on GitHub.** The summary says you check on GitHub. Your words: "for you to check the work on Github" (t223u:10). "You" is Prima.
- **Who reviews.** The summary says you check, or assign a review bot. Your words: "you check the work, or assign a review bot to do the checks for you" (t223u:12). Again, "you" is Prima.
- **Who pulls and assembles.** Your words: "YOu can pull the work and have cursor do the finally assembly on my computer" (t223u:10). Prima pulls; Cursor assembles on your computer. The summary leaves out the pull.
- **"6" and "8".** The summary reads them as axiom 6 (framing) and axiom 8 (record). In Axioms.md, frame is axiom 5. Your words do not say "axiom" (see "Who frames it, who records it").
- **Left out of the summary.** "it pushes it like our workflow concept" (t223u:8). Your item 6 questions: "Does this make a solid base for running our work? What changes would you make?" (t223u:16). "What you asked for" answers them.
