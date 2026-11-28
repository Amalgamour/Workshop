# Draft-page questions, in plain words

Builder: Claude. 2026-11-28. Pack C3.
The full questions are in QUESTIONS.md. Nothing here is decided.
"QN" cites are lines of labs/draft-page/QUESTIONS.md. "WP" cites are lines of docs/plan/WORK-PAGE-2026-11-30.md on prima/build 5d26b448.

## Q1. What is a draft?
- The new kernel is built on a side branch of the same work page.
- Default: a draft branch on the work page (QUESTIONS:14; WP:152).
- The other choices need new wf code (QUESTIONS:17-23).

## Q2. Where do we write which wf build is live?
- Today nothing records it. Prompts just say "a823" (QUESTIONS:31).
- Default: one line on face 08 of the band door, 90.50.10.0400 (QUESTIONS:33; WP:146).

## Q3. Who says yes to the switch?
- The switch changes what is live for every page.
- Default: the Prime signs off, then you approve the merge and the pin move (QUESTIONS:50; WP:153).

## Q4. Does an open draft lock its files on returns?
- If it does, everyone waits again.
- Default: no. It holds them only on its own branch, until the switch (QUESTIONS:65; WP:154).

## Q5. Where does the draft's page log go?
- Default: on the draft branch, read in with `wf intake --branch` (QUESTIONS:77).
- The work page marks B ★ instead: a later wf change so the log always goes to returns. The default is still A (WP:155).

## Q6. Do we keep a failed draft's branch?
- Default: keep it, and mark it dropped on face 08 (QUESTIONS:93; WP:156).
- Nothing is lost that way (QUESTIONS:94).

## Q7. Should wf check that two pages don't edit the same file?
- Today wf checks this only inside one page (QUESTIONS:104).
- Default: not now. The lead checks it by hand (QUESTIONS:106; WP:157).

## Q8. Should wf refuse a pack that started before the last switch?
- Today wf does not check this (QUESTIONS:115).
- Default: not now. The lead lists stale packs by hand after each switch (QUESTIONS:117; WP:158).
