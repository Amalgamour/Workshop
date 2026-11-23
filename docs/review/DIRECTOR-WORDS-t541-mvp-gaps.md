# Director words: t541u MVP gaps G1-G8 (2026-11-23, about 12:51 PM EST)

Matthew's answers to the eight gaps in docs/plan/MVP-GOAL-PROPOSAL.md section 5, verbatim. Readings follow each answer. The proposal, the 0423 draft, and the builder queue were updated from these answers in the same turn. Nothing was packed.

## G1. What does the checking for the MVP?

> wf, plus one seqaddr validate step

Reading: for the MVP, the compute is wf as it is today, plus one step that runs `seqaddr validate` on the page and records the result. Moving wf into the core stays at roadmap stage 6.

## G2. Should page 0498 be the MVP test?

> Its part of our goals for MVP it's what we are aimign for.

Reading: 0498 is the MVP target. Its done-when is the acceptance criteria in the proposal. The stage is not done until that walkthrough is packed and run on Matthew's PC.

## G3. Does one worker hold the page for every step, including pack, check and signoff?

> A worker only holds the page when they are activelly working on it. If it's being updated as 01 or more work on 05 or just the human readable version of the page's scope and design as 04. One model should be working on it at a time.

Reading: a page is held only while one worker is actively working on a face. That face is 01 (agents and scope), 04 (the planned work, in human-readable form), or 05 (the work orders). That face is locked while it is being worked on. One model works on the page at a time. Between steps, when no one is actively working, the page is not held. This rejects the idea that the page always has a named holder, even between steps. It also widens the t533 reading, which treated only a 05 claim-to-return as being in the page.

## G4. Is a second-field trial part of the MVP?

> yes, small, after 0498

Reading: a small second-field trial is part of the MVP, and it comes after the 0498 run. Its own page in the 04NN band, so 0498 does not grow. Matthew still picks the field. The page number is chosen when the field is picked.

## G5. Which board do we use?

> wf board with holder, step and next

Reading: the MVP board is `wf board`. Each book-board line must show the page's holder, step and next move. That change is a pending wf page (0424, title book-board), not packed in this turn. WF-BOARD Q1 (column names) was not answered here and stays open.

## G6. What counts as searchable for now?

> GitHub is enough for now, we want it build into code for a gui I can sit at and use with models being able to see and use the Workshop manager. With pages as the cars and 05 as the workorders on them.

Reading: for the MVP, a plain search over the records pushed to GitHub is enough. The long-term direction is a GUI Workshop manager, built into the code, that Matthew can sit at and that models can also see and use. In that manager, pages are the cars and 05 passes are the work orders. The GUI is not part of the MVP scope.

## G7. What is a work order?

> It's the 05 face, 01 is the agents and scope, 04 is the planned out work we are doing on it. So the face must be locked while it's being worked on.

Reading: a work order is a 05 pass, not the whole page. Face 01 is the agents and scope. Face 04 is the planned work. The face being worked on is locked for that time. The page is the car; the 05 passes are the work orders. Queue wording that called 0422 itself "a work-order page" is wrong and is corrected. 0422 is the report-system page; its 05 passes are the work orders.

## G8. Must wf send reports itself before the MVP run?

> no, the current report file is enough

Reading: 0422 does not have to land before the MVP run. The stopgap report file (docs/plan/REPORTS.md) counts for the MVP. 0422 lands when it lands.
