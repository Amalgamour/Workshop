# WORKING PATH, axiom check by Tester (Grok Bot), not a ruling;
checked 6fbba08.

Axioms.md lines checked: 1 :13, 2 :15, 3 :17, 4 :19, 6 :23, 7 :25,
8 :27, 9 :29. All match. RULINGS = docs/spec/DIRECTOR-RULINGS.md.
LIB: cites are not in this repo; not checked here.

## W1. Is the work book a real book, written by the compute?
- Answer: yes. One work book per build, written through today's
  gate, retired to the shelf when the build is done.
- Why: R37 item 1, one log is the only truth (RULINGS:195).
- Check: 1 :13 tension (gate is not a lock yet); 2 :15 pass;
  6 :23 pass; 7 :25 pass. R33 item 1 (:159-160) pass.
  R31 item 6, book is a journal (:139-140) pass.

## W2. Is AGENTS.md stored in the page or made fresh per job?
- Needs a different view (R20, RULINGS:79). One side is my own
  research. No answer from me. Spec's "both" checked on rulings:
- R33 item 2 (:162, held 7): face 01 is usually key words.
  Tension: a full brief in 01 is a new use of 01.
- R32 items 1-2 (:152, :154): faces past 00 may change. Pass.
- R34 (:170): freezes only if W8 says system page. Depends on W8.
- R37 item 3 (:197) pass: compute writes the copy.
- R37 item 4 (:198) pass: return bound to the version read.
- Axiom 2 :15 tension (a copy), as the spec says itself.

## W8. Is a work page a system page?
- Answer: no. Matthew reads work pages; system pages are not
  for users (R34, RULINGS:169-170).
- Why: so a wrong brief can be fixed in place. Hurt: Matthew.
- Check: 1 :13 pass; 2 :15 pass; 7 :25 pass; 9 :29 tension.
  R32 item 2 (:154) pass: faces past 00 may still change.
- Note: page type is a locked 00 field (R36, :190). So W8 must
  be ruled before the first work page is written.

## W3. Who may release a work page to a builder?
- Answer: Matthew releases the first few. Then Prima, inside a
  written grant naming the scope and a spending cap.
- Why: a release spends money. Hurt: Matthew, by a surprise bill.
- Check: 1 :13 pass; 3 :17 pass only with the written grant
  ("A lead is not authority"); 6 :23 pass.
  workflow-loop.003.md:89 ("only to the extent delegated") pass.
- Gap: the spec's answer drops the cap; it sits only in my note.

## W4. What decides Cursor or Grok Builder for a page?
- Answer: the B4 rule, written on each page with its reason.
- Why: a runnable check lets the cheap try fail safely.
  Hurt: Matthew, paying twice for the same miss.
- Check: 3 :17 pass; 4 :19 pass; 9 :29 tension: cheaper is 9.
  R37 item 8 (:202) pass: two fails stop with a handback.
- Needs a different view for the builder strengths in B4:
  they come from my research (WORK-BOOK-RESEARCH.md:169-171).

## W5. Do we record cost per job?
- Answer: yes: time, tries, tokens, dollars, when reported.
- Why: R37 item 6 keeps "not reported" apart from "zero" (:200).
  Hurt: Matthew, reading a blank as free.
- Check: 7 :25 pass; 9 :29 pass (lets "cheap" be tried).

## W6. Who reviews a return?
- Answer: a different view as R20 defines it (:79), never the
  builder and never the page's writer.
- Why: R2 needs a trial from another view (RULINGS:7-9).
- Check: 9 :29 pass; 1 :13 pass. R20 pass. R2 pass.

## W7. What is "my local space"; does it stay in step?
- Answer: ask Matthew to name it; nothing is guessed. Spec's
  shape (pinned copy, returns flow back via our compute) is fine.
- Why: R33 item 1, books change only through compute (:159).
- Check: 1 :13 pass; 6 :23 pass; 7 :25 pass.
  2 :15 tension, not pass: a full copy is what 2 warns against.
  The spec's cite seqAddr.md:104 says books follow the kernel
  "live"; a pinned copy does not. So that cite does not back it.
  8 :27 tension, as the spec says.
- Better option: make it a child desk with a written 99 link
  (decisions.md:218-232). That link is lawful (8). Child desks
  are deferred (R21, :84), so Matthew must say yes first.
