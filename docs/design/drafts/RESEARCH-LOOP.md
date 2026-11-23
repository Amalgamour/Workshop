# Research loop

state: draft for Matthew. Not a ruling. Nothing built.
made: 2026-11-23, 10:55 AM EST, by Cursor-C (Design).
Words files for t506u, t507u, and t508u are not in the repo (looked on origin/prima/build at 78101fe6). t508u below is the quote from this job. t506u and t507u are the job's summary of his rulings, not a file quote.

t506u, as this job states it: every lab ends with a final learning report by its builder, cross-checked by the other builder. Lessons are kept in docs/lessons/ in the Workshop repo.

t507u, as this job states it: docs/lessons/ is the primary source for researchers. The menu is docs/lessons/INDEX.md, with topic, read-when, size, and link, so a researcher chooses what to spend usage on.

t508u, his words, from this job:

"Any completed work should have that in the page and in the repo as well. So if the researcher needs to look at all the packs and returns it can. So it's first menu on the lessons, then the lessons reports, then the actually pages 3rd if needed request from lead for that deep should be authorized. Research should have packs as well. So you can link them to pages for finding later. Then we need loops for how to run a check how you authorize different kinds of research work."

## 1. Three levels

A researcher starts at the cheap end and stops there unless the work needs more.

| Level | What they may read | Authorization |
|---|---|---|
| 1 Menu | docs/lessons/INDEX.md only | none |
| 2 Reports | the lesson files the index links | the index row is the permission. Prime adds the row |
| 3 Deep | the page, its packs, and its returns | Prime says yes first, in a note on the research page |

Level 3 is the "if needed" step in t508u. The request goes to the lead. The lead here is Prime.

How the yes is recorded, for now: a face 06 note on the research page, before the draft. wf already refuses a draft until a new face 06 note exists (src/cmd.rs:298 on origin/returns). The note names the pages and says deep. The draft pins that note, so it stays with the pack. No new wf field yet. A future page can add an auth field and refuse a deep pack without it.

## 2. Where a research pack sits

Work for this stage is band 0400-0499, door 0400 (STAGE-PLAN-90.50.10.md:8; t423u). Labs are band 0700-0799, door 0700 (same plan, section 13; t432u). A lab tries to break a page. A research page reads lessons and, when authorized, packs and returns. Those are different jobs, so research does not go on a lab page.

Proposal: band 0800 on the same book. Door 90.50.10.0800. Research pages 0801-0898. 0899 is the continuation, not a page. 0800 is not the stage band and not the lab band. The plan's other stage-numbering idea skips 0700 and would use 0800 as a later stage (STAGE-PLAN section 13.2). That is why this band is a proposal, not a claim. See question 1.

The pack is the page's own 05.NN, the same shape wf already packs. Face 08 says serves: and lists the work or lab pages this research is about. The other page lists the research page back when it is next written. A research pack can link those pages for finding later (t508u). Linking is the face 08 line. It is not a copy of the pack.

No new wf command is needed to start one. init-page, face 01, face 08, a face 06 note, draft, pack.

## 3. Lessons at each close

Two homes, as t508u says: on the page, and in the repo.

On the page: face 06 (seqAddr.md:155, notes). The builder writes the lesson in the return, under noticed. Prime, at signoff, adds one face 06 note: the pass number, one short lesson, and the file name in docs/lessons/. The lab's last pass is the final learning report (t506u). The other builder cross-checks that report before the file is added to the index. See section 4. That cross-check is not the code check.

In the repo: one file, docs/lessons/<page>.<pass>.md, plus one row in docs/lessons/INDEX.md. The row is topic, read-when, size, link (t507u). Size is so the researcher can see the usage before opening it. wf does not write the Workshop repo. A person copies the file. That is convention until a later page.

## 4. The check loop, as the logs show it

Read on origin/packs at bac1d93f.

The code check and the lesson cross-check are two different checks.

Code check, what the logs already do:

1. Dry run. wf check --dry-run prints the verdict and writes nothing (src/cmd.rs:735 and :760). None of the four page logs below contain the word dry-run. The dry run is done, then the real check is the one that is kept.
2. Recorded check. The actor is prima-check, role checker. The builder may not check their own work (src/cmd.rs:734).
3. Signoff. Actor prima, role prime, outcome passed or failed.
4. Close. Actor prima, role tool (src/cmd.rs:866).

What the packs logs show:

- 90.50.10.0404 pass 1: Cursor-1 built it. prima-check failed. Prima signed off failed. Closed failed.
- 90.50.10.0415 pass 1: Cursor-1 built it. prima-check passed. No signoff in that log yet.
- 90.50.10.0701 pass 1: Cursor-1 built it. prima-check passed. Prima signed off passed. Closed passed.
- 90.50.10.0702 pass 1: Claude built it. prima-check passed. Prima signed off failed. Closed failed.
- 90.50.10.0703 pass 1: Codex built it. prima-check passed. Prima signed off failed. Closed failed.

A passed check is not a passed signoff. 0702 and 0703 show that.

Lesson cross-check, not in those logs yet. t506u: the builder writes the report, the other builder checks it. The pair already on the lab pages is Claude (0702) and Codex (0703). Each checks the other's lesson. For a page built by Cursor-1, the pack names the other builder. The cross-check is a face 06 line, "cross-check: <name>, pass" or "fail", written before the lesson is added to the index. It is not a wf check, because a wf check runs the pack's commands, not a reading of the lesson.

## 5. Authorization by kind

| Kind | What it is | Who says yes | Why the usage matters |
|---|---|---|---|
| Menu only | read the index | nobody | one small file |
| Reports | read the lesson files | Prime, by adding the index row | the size column is the cost |
| Deep | read pages, packs, and returns | Prime, face 06 note before the draft, naming the pages | a log is much larger than a lesson |
| Code runs and benchmarks | run commands, not only read | Prime names the commands in that same note. A new kind of benchmark waits for Matthew | a run costs more than a read, and a benchmark can be open-ended |

The researcher does not open a deep page, a pack, or a return until the note is on the research page. They do not run a command that the note does not name.

## What works now, and what needs a wf page

Works now, by convention:

- Level 1 and level 2, once INDEX.md and the lesson files exist.
- A research page in band 0800, packed with today's wf, face 08 serves links written by hand.
- Level 3 and code-run yes recorded as a face 06 note, which the draft already pins.
- The lesson in the return, Prime's short copy on face 06, and a person copying docs/lessons/ and the index row.
- The code check loop in section 4. It already runs.
- The lesson cross-check as a face 06 line by the other builder. Nothing in wf does this yet. People do it.

Needs a future wf page:

- An auth field that refuses a deep pack with no note. Not this draft.
- wf writing docs/lessons/ or INDEX.md. wf does not write the Workshop repo today.
- A lesson cross-check that is its own log entry, separate from prima-check.

## Questions for Matthew

1. Where do research pages live? (default) Band 0800, door 90.50.10.0800, so they are not lab pages. Other choice: a lab page in band 0700.
2. How is a deep read authorized? (default) Prime's face 06 note on the research page, before the draft. Other choice: a new wf field now.
3. When is the lesson written down? (default) At close. The return holds the builder's words. Face 06 gets Prime's short copy. The repo file is added after the other builder's cross-check.
4. Who is the other builder? (default) Claude and Codex check each other on the seq labs (0702 and 0703). Any other page names the pair in the pack.
5. Who may approve a benchmark? (default) Prime, for a command list written in the note. Matthew, only when the kind of run is new.
6. May this note stand until the words files exist? (default) Yes, as a draft. The t508u quote is from this job. t506u and t507u are summaries. A words file should replace them when it is recorded.
