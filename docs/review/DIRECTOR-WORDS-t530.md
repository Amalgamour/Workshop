# Director words: t530u and t531u (2026-11-23, midday EST)

Matthew's answers to lab 90.50.10.0705 DESIGN.md section 4.1, relayed via Claude, then a clarification on the report-system work order. Verbatim below. Readings follow each answer.

## t530u  -  Q1: where setup reports chain

> A workers page

Then:

> N6 is where worker pages should live.

Asked whether one page per worker or one shared page:

> One page per worker

Then:

> The title should be the worker's name.

Reading: each worker has its own page at 90.50.10.06NN (the first open slot after 0600), titled with the worker's name. Setup reports chain there. Titles must be lowercase (seqAddr.md:112), so "Grok-Check" is titled grok-check; the exact name is kept in the stamp and the worker config. Exact-case titles would need a ruling. No 06NN page exists on packs or returns today. 0600 is the band door (seqAddr.md section 10 rule 4); the first open slot after 0600 is therefore 0601. This band ruling is recorded in docs/review/PENDING-RULES.md, not yet in seqAddr.md: 0705.05.01 is still open and cites seqAddr.md section 11 (t381u: rule files do not change mid pass).

## t530u  -  Q3: should wf check push?

> Always (Recommended)

Reading: every real `wf check` writes and pushes its report. `--dry-run` still writes nothing.

## t530u  -  Q2, first answer (worker-page numbering, not queue order)

Asked twice; the answer given was:

> First open slot after N600.

Claude read that as the numbering of worker pages, not the queue order. That reading stands for N6 (see Q1): first open slot after 0600.

## t530u  -  Q2, later answer (queue / N4 numbers)

> Next open N4 slot that isn't being used.

Reading: the wf report-system build gets the next open, unused 04NN page number, and it goes next in the queue. Used numbers include pages on packs and returns, and numbers already reserved in the queue, including suggested 0420 (dead lock) and 0421 (wf seat). 0422 was a queue placeholder for this work and is not on packs or returns; it is the next open unused 04NN. See t531u for the shape of that work.

## t531u  -  the report-system work is one page

> N4 is our dev band so the work for building the report system goes that is a work order page.  The work order is building our report-system :)

Reading: N4 (0400-0499) is the dev / work-order band. The report-system build is one work-order page, titled report-system (lowercase, seqAddr.md:112), at the next open unused 04NN, which is 90.50.10.0422. Its passes carry the build work. Claude's BUILD-PAGES.md should split that work into passes and grants under that one page, not into many pages. Sub-pages only if wf requires it, and then say why. This page goes next in the queue once lab 0705 closes. 0420 stays the dead-lock page; 0421 stays the wf seat page.

## Effect

Lab 0705 needs pass 05.02 to fold these answers into SPEC.md (setup and section 4), WORKER-SETUP.md, BUILD-PAGES.md, and DESIGN.md 4.1. Band N6 for worker pages is a ruling; it waits in docs/review/PENDING-RULES.md until 0705.05.01 is closed, then it should be added to seqAddr.md as a versioned note. The queue lists 90.50.10.0422 as the report-system work order. Packing 05.02 waits until 05.01 is checked (Grok-Check), signed off, and closed; the 05.02 pack text is drafted now.
