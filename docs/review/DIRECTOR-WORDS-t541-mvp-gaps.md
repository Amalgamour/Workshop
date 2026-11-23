# Director words: t541u MVP gaps G1-G8 (2026-11-23, about 12:51 PM EST)

Matthew's answers to the eight gaps in docs/plan/MVP-GOAL-PROPOSAL.md section 5, verbatim, plus later answers the same day on how the face lock works, who may break an abandoned lock, and where the book's Prime sits. Readings follow each answer. Nothing was packed.

## G1. What does the checking for the MVP?

> wf, plus one seqaddr validate step

Reading: for the MVP, the compute is wf as it is today, plus one step that runs `seqaddr validate` on the page and records the result. Moving wf into the core stays at roadmap stage 6.

## G2. Should page 0498 be the MVP test?

> Its part of our goals for MVP it's what we are aimign for.

Reading: 0498 is the MVP target. Its done-when is the acceptance criteria in the proposal. The stage is not done until that walkthrough is packed and run on Matthew's PC.

## G3. Does one worker hold the page for every step, including pack, check and signoff?

> A worker only holds the page when they are activelly working on it. If it's being updated as 01 or more work on 05 or just the human readable version of the page's scope and design as 04. One model should be working on it at a time.

Reading: a page is held only while one worker is actively working on a face. That face is 01 (agents and scope), 04 (the planned work, in human-readable form), or 05 (the work orders). That face is locked while it is being worked on. One model works on the page at a time. Between steps, when no one is actively working, the page is not held. This rejects the idea that the page always has a named holder, even between steps. It also widens the t533 reading, which treated only a 05 claim-to-return as being in the page. How long the lock lasts, and the lockout template, are in the two answers after G8.

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

Reading: a work order is a 05 pass, not the whole page. Face 01 is the agents and scope. Face 04 is the planned work. The face being worked on is locked for that time. The page is the car; the 05 passes are the work orders. Queue wording that called 0422 itself "a work-order page" is wrong and is corrected. 0422 is the report-system page; its 05 passes are the work orders. The lock lasts the whole work session; see the answers after G8.

## G8. Must wf send reports itself before the MVP run?

> no, the current report file is enough

Reading: 0422 does not have to land before the MVP run. The stopgap report file (docs/plan/REPORTS.md) counts for the MVP. 0422 lands when it lands.

## Session-long face lock (12:57 PM EST)

Asked how long a face lock lasts, after the 0423 draft flagged that wf had no session-long hold for 01 or 04 (`face-write` and `draft` are single commands).

> Lock the face for the whole work session, released when the worker is done

Reading: a worker takes a lock on the face they will work on (01, 04 or 05). The lock lasts the whole work session, not just one command. It is released when that worker is done. While it is held, every other worker is refused. Between sessions the page is not held.

## Lockout template (12:58 PM EST)

> It's a lock out. Look at lockouts as your template from industrial construction and maintaince safety practices.

Reading: the face lock follows lockout/tagout (LOTO) practice from industrial construction and maintenance safety. In Workshop terms: each worker applies their own named lock and tag, giving the face, the worker, the reason and the start time. Only the worker who applied a lock removes it, and that removal is a release entry in the log. Before work starts, the lock is checked (try-out: verify it holds). Group lockout, where several locks sit on one face, is not allowed, because only one worker may work a face, and only one worker may work a page at a time. Removing an abandoned lock takes a recorded supervisor override: it needs a reason, and the log keeps it. Who may do it is in the 1:08 PM EST answers below. The 0423 draft uses this template. The kit DESIGN.md is not edited while open packs pin it (t381u); the rule sits in docs/review/PENDING-RULES.md until then.

## Abandoned-lock override (1:08 PM EST)

Asked who may break an abandoned lock, after the 0423 draft read that as `--as Prima` or the page's person, and asked whether a prime who is not Prima may override.

> Only Prima or Matthew may break an abandoned lock, with a reason

Then, the same minute, a refinement:

> Project lead of the book can break or higher authority.

Reading: the first answer names the people who hold those roles on this work today. The refinement states it as roles, so it stays true if the lead changes. The book's project lead, or a higher authority, may break an abandoned lock, with a recorded reason. The kit already records the team-lead role as Prime (t254u), on the page stamp, face 00 (t255u): current Prime and previous Primes. wf stores that as the page's current Prime, set at init and changed with `wf set-prime`. The 1:08 reading used the work page's Prime, because no book-level field had been found yet. The 2:17 PM EST answer below settles that the Prime is the book's lead, one position below the Director (the person).

## Book Prime (2:17 PM EST)

Asked whether "project lead of the book" is the work page's Prime, or a book-level lead, after the 0423 draft flagged that wf records Prime only per page.

> The book has a prime or lead, that is the position below the director/person.

Reading: the book itself has a Prime, also called the lead. That role sits one position below the Director, who is the person. The abandoned-lock override is done by the book's Prime, or by a higher authority (the Director / the person), always with a recorded reason. A work page's own Prime is not enough, unless that person is also the book's Prime.

Where it is recorded today: seqAddr.md already names the book's identity page as `DD.SS.BB.0000` (section 1.4 and 1.5; section 6, `0000` is book identity). Face 00 of a page is the stamp. The wf kit DESIGN.md already lists person, current Prime and previous Primes on face 00 (t254u, t255u). `wf set-prime` and `wf init-page` already write those fields, but only on the page you name. There is no book-scoped command, and no `DD.SS.BB.0000` page is in use in wf today, so the book's Prime is not actually recorded yet. The smallest way to record it is to put it on that identity page's face 00 stamp, using the same fields, and to let `wf set-prime` work on `DD.SS.BB.0000`. That recording is a pending wf page (0425, title book-prime), not part of 0423. 0423 only reads the book's Prime when that page exists; it does not create it.
