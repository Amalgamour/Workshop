# Work book: eight questions for you

For Matthew. By Designer, Mon 16 Nov 2026, 4:55 PM EST. Nothing here is decided. Only you approve.
Marks come from Tester's check (AX = docs/review/WORK-BOOK-AXIOM-CHECK.md, c5cbf0d), or the spec where Tester is silent (SPEC = docs/design/WORK-BOOK-SPEC.md, 6bcc1c0).
Axioms: 1 who decides, 2 no copies, 3 leads, 4 why, 6 history, 7 missing, 8 links, 9 test it.

Change note (2026-11-16, 9:10 PM EST, Designer): W8 gets Tester's `workflow` page-type option, from WORK-BOOK-CONCEPT.md W8 (54b737d). Nothing else changed.

**Two things to know first.**
- W8 must be ruled before the first work page exists. Page type is locked once set (R36; AX:33-34).
- W7 asks you to name your local space: the folder. We will not guess it.

## W8. Is a work page a system page? (ANSWERED, t239u)
- Answered by Matthew, t239u (docs/review/DIRECTOR-WORDS-t239u.md:9): "1. I agree". Reading (7): yes to "not a system page"; the `workflow` type is not in his words (WORK-BOOK-CONCEPT.md F3).
- Answer (both, mine and Tester's): no. You read work pages; system pages are not for users (R34).
- Tester's option (added 2026-11-16, Designer, from WORK-BOOK-CONCEPT.md W8): use the page type `workflow` (seqAddr.md:192). It is not system, but no ruling says if it locks (7).
- Why: a wrong brief can then be fixed in place. Who gets hurt otherwise: you.
- Check: 1 pass, 2 pass, 7 pass, 9 tension (untried); R32 item 2 pass (AX:31-32). The spec also marks 6 pass (SPEC:394).

## W1. Is the work book a real book, written only by the compute?
- Answer (both): yes. Its state goes through the compute from day one. Tester adds: one work book per build, put on the shelf when done.
- Why: one log is the only truth (R37 item 1). Who gets hurt otherwise: you, if notes and book differ.
- Check: 1 tension (the door is not locked yet), 2 pass, 6 pass, 7 pass; R33 item 1 pass; R31 item 6 pass (AX:12-14).

## W2. Is the builder's sheet (AGENTS.md) kept in the page, or made fresh for each job?
- Answer (mine): both. The page keeps it; the compute makes a copy for each job, stamped with the page version. Tester gives no answer, because one side is Tester's own research; it needs a different view (AX:17-18).
- Why: you can open the page and see what the builder was told. Who gets hurt otherwise: a builder reading an old copy.
- Check: 2 tension (a copy); R33 item 2 tension (face 01 is usually key words); R32 pass; R37 items 3-4 pass; R34 depends on W8 (AX:19-25).

## W3. Who may hand a work page to a builder?
- Answer (both): you, for the first few. Then Prima, inside a written grant with a scope and a spending cap.
- Why: a release spends money. Who gets hurt otherwise: you, by a surprise bill.
- Check: 1 pass, 6 pass; 3 pass only with the written grant (AX:40-42). The spec marks 3 as tension (SPEC:401).

## W4. Cursor or Grok Builder: who gets a page?
- Answer (mine, Tester agrees): if a test can check the job, the cheaper builder tries first. Two fails: stop and hand back.
- Why: a test lets a cheap try fail safely. Who gets hurt otherwise: you, paying twice for one miss.
- Check: 3 pass, 4 pass, 9 tension (cheaper is untried); R37 item 8 pass (AX:49-50). The builder strengths come from Tester's research and need a different view (AX:51-52).

## W5. Do we write down what each job cost?
- Answer (both): yes: time, tries, tokens, dollars. "Not reported" is not "zero".
- Why: R37 item 6. Who gets hurt otherwise: you, reading a blank as free.
- Check: 7 pass, 9 pass (AX:58).

## W6. Who checks a builder's work?
- Answer (both): a different view, as R20 says; a fresh session counts. Never the builder, never the page's writer.
- Why: R2 needs a test from another view. Who gets hurt otherwise: every job.
- Check: 9 pass, 1 pass; R20 pass; R2 pass (AX:64).

## W7. Where is "my local space", and does it stay in step with ours?
- Answer (both): you name the folder. It holds a pinned copy of our code; work comes back only through our compute.
- Why: books change only through the compute (R33 item 1). Who gets hurt otherwise: you, with two books drifting apart.
- Check: 1 pass, 6 pass, 7 pass; 2 tension (a full copy); 8 tension (AX:70-74).
- Tester's option: make it a child desk with a written link. That needs your yes first, because child desks are on hold (R21; AX:75-77).

**Conflicts Tester found.** W7: axiom 2 was wrongly marked pass. The spec is now fixed (6bcc1c0). W2: a full sheet in face 01 is a new use of face 01 (R33 item 2). Every other ruling Tester checked passed.
