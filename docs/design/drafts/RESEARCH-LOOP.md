# Research loop

state: draft, revised after t509. Not a ruling. Nothing built.
made: 2026-11-23, 11:15 AM EST, by Cursor-C (Design).
replaces: the band 0800 proposal and questions 1 to 5 in the previous draft of this file. That text stays in the git history.
words: docs/design/drafts/DIRECTOR-WORDS-t506-t509.md. The review copies of t506u through t509 are not in the repo (origin/prima/build at 78101fe6). t508u and t509 below are the quotes from this job. t506u and t507u were summaries, so they are not quoted as his words.

t508u:

"Any completed work should have that in the page and in the repo as well. So if the researcher needs to look at all the packs and returns it can. So it's first menu on the lessons, then the lessons reports, then the actually pages 3rd if needed request from lead for that deep should be authorized. Research should have packs as well. So you can link them to pages for finding later. Then we need loops for how to run a check how you authorize different kinds of research work."

t509, the answers that change this note:

- Q1: "I think 900 band it's also set aside for logs so it's a good match such things go there."
- Q2: "By writing a reseach pack with limites on how much it can use, example it can review 10 pages in research, check 4 packs and max 4 web searches."
- Q3: "When a page has achieved its goals and no more active work on it is needed to achieve the current phrase of the project. Like our steering wheel example. Once we have a working steering wheel we take the lessons learned and shape it into a report that can be found in the N9 band."
- Q4: the reviewer of the completed work builds the lessons. They are the seated 05. The page can be parked as complete for now. The reviewer builds that pack, updates face 01, then we extract a brief searchable part. His word is "ritted 05". That is read here as "seated 05".
- Q5: "Matthew approves only new kinds of runs; Prima approves named command lists."

## 1. Three levels

The order is his: menu, then lesson reports, then the pages only if needed.

| Level | What they may read | How far |
|---|---|---|
| 1 Menu | docs/lessons/INDEX.md | one small file. No pack |
| 2 Reports | the lesson reports the index links, in band 0900 | the report. Not the work pages |
| 3 Deep | the work pages, their packs, and their returns | only inside a research pack Prime has written, and only up to its limits |

A deep dig is not a note. Prime writes a research pack. The pack is the authorization. The example he gave: review 10 pages, check 4 packs, max 4 web searches. The researcher stops at the first limit they hit, and reports what was used. They do not take one more page, pack, or search.

The pack also has lines for returns and for runs, because t508u names packs and returns, and Q5 names runs. His example does not set those two numbers. See the last question.

## 2. The research pack, band 0900

Stage work is band 0400-0499, door 0400 (STAGE-PLAN-90.50.10.md:8). Labs are band 0700-0799, door 0700 (same plan, section 13). He put research on the 900 band, which is N9: pages 0900-0999. Door 90.50.10.0900. Research pages 0901-0998. 0999 is the continuation, not a research page.

What the files already say about N9:

- workflow-loop.md:50: N8NN and N9NN are "not in use" and "reserved".
- workflow-loop.003.md:49: 0800-0999 is "unassigned by this workflow".
- decisions.md:121 and seqAddr.md:225: 0100-0999 are the kernel's standard bands, and the list runs through 0900. They do not say what 0900 holds.
- No file in this repo says band 0900 is set aside for logs. He says it is. That clash is flagged, not fixed here. His answer is the later word for where research and lesson reports go.

The stage plan does not use 0900 as a stage band. Its default for later stages is one 0400-shaped band in each thousand (section 13.2). 0900 is not that.

The pack uses the pass wf already has, 05.NN on the research page. No new command to start it. Face 08 says serves: and lists the work pages it may look at. Those pages link back when they are next written.

Limits, written in the pack, in plain numbers:

- pages: 10
- packs: 4
- web searches: 4
- returns: a number, or blank
- runs: a number, or blank

stop if: any count would pass its number. The researcher stops and reports the counts. They do not continue.

wf today will not count this. The numbers sit in the pack text. The researcher keeps the count. A future page can refuse a dig past the number. Web searches are outside wf. Runs are too, unless the pack names commands Prime has approved (Q5).

## 3. When the lesson is written, and the seated 05

Not at every close. When the page has met its goals, and no more work is needed for this phase. His picture: a working steering wheel. Then the lessons become a report that can be found in the N9 band.

Who writes it: the reviewer of the completed work, not the builder. The steps he named:

1. The packs and returns are complete. The page can be parked as complete for now.
2. The reviewer builds a new pack. That pack is the seated 05. It holds the finished work and the lessons learned.
3. The reviewer updates face 01, so a later builder can be handed that 05 and run it again.
4. We extract the lessons and give a brief searchable part.

The brief part is one row in docs/lessons/INDEX.md: topic, read-when, size, link. The link points at the report in band 0900. The full report stays on that 0900 page. The index is the menu (level 1). Opening the report is level 2. Opening the work packs is level 3, and only inside a research pack.

What wf can do today:

- A new pass can be drafted, packed, and closed. The reviewer can put the best pack and the lessons in that pass. Face 01 can be rewritten with face-write. That much is convention, and it works now.
- wf has no seat command. Face 05 is a counted face, and seqAddr.md:199 says a counted face is never seated. So the new pass is not a seated 05 yet. It is the pass we will seat when a later page allows it. R22 and R23 already ask for a seated 05 (DIRECTOR-RULINGS.md:86-92). wf does not do that.
- wf has no "parked as complete". It has halt (src/lib.rs:36 on origin/returns). Halt stops a new draft while a note is on the page. Halt is not "complete". Retire is page 0409, and it is not built.

Until those pages exist: the reviewer closes the lesson pass, updates face 01, and Prime halts the work page with a note that says "complete for this phase". The note also says halt is the stand-in, not the real parked-complete state.

The copy into docs/lessons/INDEX.md is done by a person. wf does not write the Workshop repo.

## 4. The check loop, as the logs show it

This is the code check. It is not the lesson. Read on origin/packs at bac1d93f.

1. Dry run. wf check --dry-run prints a verdict and writes nothing (src/cmd.rs:735 and :760). The logs of 0404, 0415, 0701, and 0702 do not contain the word dry-run. The dry run happens first. The saved check is the one that stays.
2. Saved check. Actor prima-check, role checker. The builder may not check their own work (src/cmd.rs:734).
3. Signoff. Actor prima, role prime.
4. Close. Actor prima, role tool (src/cmd.rs:866).

0404 pass 1: Cursor-1 built it, prima-check failed, signoff failed, closed failed. 0702 and 0703: Claude and Codex built them, prima-check passed, and Prima still signed off failed. A passed check is not a passed signoff.

The lesson is not this loop. The reviewer builds it after the work is done (Q4).

## 5. Who approves which kind

| Kind | Who says yes | Usage reason |
|---|---|---|
| Menu only | nobody | one small file |
| Reports | the index row. Prime adds it | the size column shows the cost before the file is opened |
| Deep pages, packs, returns, web searches | Prime, by writing the research pack and its limits | each extra page, pack, or search costs more, so the pack sets a max |
| Named command list | Prime (Q5) | a run costs more than a read, and the commands are named in advance |
| A new kind of run | Matthew (Q5) | an open-ended run has no max until he allows that kind |

The researcher stops at the pack's limits and reports. They do not raise the numbers themselves.

## What works now, and what needs a page

Works now, by people using wf as it is:

- A research page at 90.50.10.0901 and up, with a normal 05.NN pack and the limit lines in the pack text.
- Face 08 links to the work pages.
- The reviewer drafts the lesson pass and updates face 01.
- A person adds the index row.
- The code check loop in section 4.

Needs a future wf page:

- Parked as complete. Halt is only the stand-in.
- Seating 05. seqAddr.md:199 forbids seating a counted face, and wf has no seat command.
- wf counting the limits and refusing past them.
- wf writing docs/lessons/INDEX.md.

## Questions still open

1. A blank returns line or runs line. (default) Blank means 0. The researcher may not open returns or run commands unless the pack writes a number. His example would be pages 10, packs 4, web searches 4, returns 0, runs 0.
2. Halt as the stand-in for parked complete. (default) Yes, with the note "complete for this phase", until a page adds a real complete state. Halt is not that state.
