# Fire sale: question sweep, Thu Nov 26 2026

state: review, not a ruling. By Prima's fire-sale worker, 12:23-12:26 AM EST (log times).
For: Prima, to mark the lists. Nothing in the lists was edited.

## What this is

The old question lists still show many questions as open. Several were answered by later rulings.
This sweep checks each one against the later rulings and gives the source.

Sources checked:
- docs/spec/DIRECTOR-RULINGS.md (R1-R37, last ruling R37, Nov 16).
- docs/review/DIRECTOR-WORDS-*.md (t212u-t558, up to Nov 23).
- docs/review/PENDING-RULES.md (t530u-t558s2225, approved process rules).
- Rulings t572u-t593u have no DIRECTOR-WORDS file yet (see STALE-DOCS S8). Where one is used here it is marked "(no file yet)" and cited from Prima's record of it, not quoted.

Status words:
- **Answered**: a later ruling settles it. Mark it answered.
- **Partly**: a ruling settles part. The open part is named.
- **Moot**: the design it asks about was replaced (by the built wf, by R21 "no override pages during this build", or by R26 "small files are stored"). Close it, or park it until the design returns.
- **Open**: no later ruling found.
- **Reading**: my reading of the ruling, not its exact words. Prima should check these before marking. Firm cites have no mark.

## Counts

Counted by table row. Some rows group several items (for example W1-W7, or #14-17).

| List | Last change | Rows | Answered | Partly | Moot | Open |
|---|---|---|---|---|---|---|
| docs/design/QUESTIONS-FOR-DIRECTOR.md (QD01-QD67 open section, less QD05) | f867b08, Nov 12 | 66 | 4 | 24 | 10 | 28 |
| docs/design/OPEN.md (O1-O33; O34 held) | 59f344f, Nov 11 | 33 | 5 | 10 | 7 | 11 |
| docs/design/DECISIONS-WAITING.md (open items) | Nov 17 | 49 | 9 | 12 | 12 | 16 |
| docs/review/QUESTIONS-2026-11-19.md (19 items) | Nov 19 | 12 | 1 | 2 | 0 | 9 |
| docs/spec/seqpage-QUESTIONS.md (open ones) | 050c7bd, Nov 11 | 7 | 0 | 1 | 4 | 2 |
| **All** | | **167** | **19** | **49** | **33** | **66** |

Not swept, with the reason:
- kernel/QUESTIONS.md (8f8e810, Nov 11): kernel Q1-Q14 are answered by R5-R18 (the ruling headings say so). Q15 and up were not checked.
- docs/design/WORKING-PATH-OPEN-QUESTIONS.md: working paths by Tester, not questions to Matthew. It points at the same QD numbers.
- docs/review/PENDING-RULES.md: every section is marked "approved by Matthew". These are rules, not questions.
- docs/spec/decisions.md, DECISIONS-LOG.md, DECISIONS-INDEX.md: records, not question lists. DECISIONS-LOG's "open - QDnn" rows follow the QD status below.

## Top findings

1. **QD01 / O6 (seated 05)**: answered by t512 ("Yes, approve the seated-05 rule change", DIRECTOR-WORDS-t512-seated05-approval.md:7). Still shown open in two lists (also STALE-DOCS S13).
2. **QD22 (taking back an abandoned task)**: answered by t541u (book Prime or higher, with a recorded reason; DIRECTOR-WORDS-t541-mvp-gaps.md:67-79; PENDING-RULES.md t541u, t547u). Also STALE-DOCS S15.
3. **T1 (branch per pass, who merges)**: answered by t401u. One shared `packs` branch and one `returns` branch replace one branch per pass (DIRECTOR-WORDS-t401u.md:3,10).
4. **QUESTIONS-2026-11-19 #10 (several models on one page at once)**: answered by t533u (one worker per page; PENDING-RULES.md:22) and t541u ("One model should be working on it", DIRECTOR-WORDS-t541-mvp-gaps.md:19).
5. **Top item 1 of DECISIONS-WAITING (check the sample page before building)**: answered by t267u ("I'm good with the design we have come up with ... So lets get this build quickly", DIRECTOR-WORDS-t267u.md:7). The list still shows it as the top blocker.
6. **QD06 / O15 (sign-in)**: put off by t585u (no file yet). Not blocking now.
7. **About 23 workflow-shape questions** (QD12, QD31, QD42, QD44, QD61, W9-W13, P1-P8, K8, S6, T3) are moot or answered by the built wf (t267u authority to build; t401u branches; t526u-t528u reports; t541u board). They should be closed as "replaced by wf", not left as open questions for Matthew.
8. **QUESTIONS-2026-11-19 has 9 rows (16 items) with no later ruling found**, including the AGENTS.md manager questions (1-3), the joining-characters rule (7), the Q14 drafts (18-19) and a disk cleanup (12). This is now the oldest list that is likely still live. It should be re-checked against Prima's own chat record, which this sweep can't see.

## 1. QUESTIONS-FOR-DIRECTOR.md (QD, open section)

| QD | Question (short) | Status | Ruling that answers it |
|---|---|---|---|
| QD01 | Face 05 seated or task list? | Answered (for 05) | t512 (DIRECTOR-WORDS-t512-seated05-approval.md:7); before that R22-R24. Notes/dictionary leftover (DECISIONS-LOG D183) stays open. |
| QD02 | Which page types? | Partly | R31 item 3 (office kinds: sheet, word document), R34 item 1 (system pages), R36 (page type is a locked face 00 field). The full type list is open. |
| QD03 | Face list in 00: by hand or computed? | Partly (reading) | R31 item 7 and R32 item 3: face 00 holds the page type and its face list. Face positions sit in the page index. Who writes the list is not ruled. |
| QD04 | Is face 00 in its own face list? | Open | none found |
| QD66 | 00.counter faces seated the normal way? | Open | R25 sets up 00.counter. Seating not ruled. |
| QD67 | How does the 00.counter list climb? | Open | R25 only |
| QD06 | Is the sign-in design right? | Partly (deferred) | t585u (no file yet): proper sign-in comes at a later dev stage. Typed-for notes stand in for now. Not blocking now. |
| QD07 | Who may change the kernel book? | Partly | R33 item 1 (books change through the compute, not models); R31 item 4 (promote is dev only); t328u (the compute is the fortress). Who exactly is not named. |
| QD08 | Where does a page keep its state? | Partly | R32 item 3 (face places in the page index); R36 (face 00 open fields); R31 item 9 ("last change" note in the page index, held). |
| QD09 | Exact address of the axioms? | Open | none found (WORKING-PATH-QD09.md is a working path) |
| QD10 | Is the dictionary's 03.00 a door? | Answered (reading) | R9 (faces have no door, as DECISIONS-LOG D01 notes) and R35 item 2 (face 03 is a menu). So 03.00 is not a door. |
| QD11 | Which faces are task lists? | Partly | t512 (seated 05, 05.NN passes); t541u (05 passes are the work orders; 01 is agents and scope; 04 the planned work, DIRECTOR-WORDS-t541-mvp-gaps.md:43-45). Other page types open. |
| QD12 | Is loop .003 law? Where are F02-F10? | Moot | Replaced by the built wf: t267u (authority to build the workflow branch), t268u (Rust wf tool). |
| QD13 | Four sections below page 0100? | Open | none found |
| QD14 | In R14, which "door"? | Open | none found |
| QD15 | May a task start at "pack"? | Open | wf has init-page then pack (t460 Q17 names init-page). No ruling on skipping steps. |
| QD16 | What after task 98? | Partly | t275 card Q-SA: pass numbers 01-98 are enforced now. What comes after 98 is open. |
| QD17 | Does a book see the kernel's tasks and notes? | Open | none found |
| QD18 | Retired copy: does lookup go on to the parent? | Moot (for now) | R21: no override pages during this build. |
| QD19 | Can a draft be a pointer's return link? | Open | none found |
| QD20 | "01/02 card needs 04 card" for task lists? | Partly | R33 item 2: on normal pages, 01 and 02 usually hold only key words. Task lists not ruled. |
| QD21 | Does the compute's own write need seat approval? | Partly | R33 item 1 (books change only through the compute's gate). Approval not ruled. |
| QD22 | Record to take back an abandoned task? | Answered | t541u (DIRECTOR-WORDS-t541-mvp-gaps.md:67-79); PENDING-RULES.md t541u and t547u: the book's Prime or higher, with a recorded reason. |
| QD23 | Where does a door page keep its return link? | Open | none found |
| QD24 | Same CC, different title: tell you? | Partly | R34 item 3 (titles may be reused); R31 item 1 (address-title pairing fixed). Whether to be told is open. |
| QD25 | May titles have capitals? | Open | R31 item 8 (titles are plain text) does not settle case. |
| QD26 | Add a "question" card type? | Open | none found |
| QD27 | Is 0013 the home for common questions? | Partly | R11 (common questions solved by key words). The home page is not ruled. |
| QD28 | Which face 00 problems stop a write? | Partly | R36 (locked fields never change), so a write to a locked field must stop. The rest is open. |
| QD29 | Exact layout of face 00? | Partly | R36 (locked and open fields: address, title, page type locked). The rest is open (R36 says so). |
| QD30 | What does the lineage line show? | Open | none found |
| QD31 | A workflow page's approval record? | Moot | Replaced by wf signoff and close (built; PENDING-RULES.md t557u item 5 on review before close). |
| QD32 | Owner kinds for a system page? | Partly | R34 item 1 (system pages are back end, for control, not for users). Owner kinds open. |
| QD33 | What does the "code" page type mean? | Partly (reading) | R31 item 3 (pages may hold office kinds). Not named. |
| QD34 | Is the .seq file layout OK? | Moot | R26 (small files are stored; a whole-book .seq is an export); R31 item 7 (one folder per page, one file per face); R27 (only face 04 must be readable). |
| QD35 | Should a .seq list where borrowed faces come from? | Moot (for now) | R21 (no override pages), R26 |
| QD36 | Make trailing spaces visible in .seq? | Partly | R27 narrows it to face 04 only. Open for 04. |
| QD37 | Write a .seq by hand to ask for a new page? | Partly (reading) | R33 item 1: books change only through the compute. A hand file could only be a request. |
| QD38 | Draft reason as a field on the write? | Open | none found |
| QD39 | Card name in an address (...1014.01.ham)? | Answered (reading) | R30: a link is 2.2.2.4.title, "we don't include the face". So no card names in addresses. |
| QD40 | Which band is "build"? | Partly | t424 (stage 1 = band 0400-0499). A band named "build" is not ruled. |
| QD41 | Desk door DD.00 or DD.00.00.0000? | Open | t541u notes seqAddr.md names the book page DD.SS.BB.0000. The desk form is not ruled. |
| QD42 | Drafting steps become law? | Moot | Replaced by the wf pack, return, check, close flow (t267u). |
| QD43 | What is "written permission"? | Partly | t335s1296 (three safety rules); t523 grant-ref; t267u and t330s1270 grants. No one definition. |
| QD44 | Does a return live on its own task number? | Moot | t401u (one returns branch); wf returns go with their pass. |
| QD45 | Names of the axioms' faces? | Open | none found |
| QD46 | How far is a snapshot trusted? | Partly | R29 (full snapshots now and then for 04). Trust and timing open. |
| QD47 | Is bootstrap law? Kernel steers routing? | Open | none found |
| QD48 | Reserved 01-09 for tasks and dictionary? | Open | t275 Q-SA (01-98) does not settle 01-09. |
| QD49 | Keep 0117 (pack-lint) in its band? | Moot (reading) | t416u: old WF pages retired. Check 0117 is among them. |
| QD50 | How are face 08 links stored and traced? | Partly | R30, R32 item 1 (a link is address plus title, to the page, not a version). Storage open. |
| QD51 | What fields does a note carry? | Open | none found |
| QD52 | Failure counts only on a guessed brand? | Open | none found |
| QD53 | Where does a new brand card go? | Open | none found |
| QD54 | What when review rejects a draft? | Partly | wf close FAILED exists (built); R35 item 1 (elevate: compute, model, person). Draft rejection not ruled. |
| QD55 | May a page type turn drafting off? | Open | none found |
| QD56 | HTTP, MCP, or both? | Open | none found |
| QD57 | Merging two copies of a book? | Partly | R31 items 4-5 (rework is a new copy at a new address, links both ways). Merge open. |
| QD58 | Split 05 into tasks (01-49) and tickets (50-99)? | Moot (reading) | t512 (seated 05 plus 05.NN passes) and t541u (05 passes are work orders). |
| QD59 | "Patch and strike" edits on a seated face? | Partly | R29 (04 edited the Google Docs way). Seated faces open. |
| QD60 | What hardware? | Open | none found |
| QD61 | Later workflow details | Moot | Replaced by the built wf (t267u, t268u). |
| QD62 | Mixed results: which wins? "Carry on" after a halt? | Open | t381u (out of rule means locked, strict). QUESTIONS-2026-11-19 #18-19 still open. |
| QD63 | Accented letters later? | Open | R4, R27 (only 04 must be readable). QUESTIONS-2026-11-19 #7 asks the same kind of thing. |
| QD64 | Base dictionary words? | Open | none found |
| QD65 | Check the Ask word lists and scoring? | Open | none found |

QD05 is not in the open list (it is settled by R25, DECISIONS-LOG D315).

## 2. OPEN.md (O1-O33)

Most O items were carried into QD (Nov 12). Where an O has a QD twin, the status follows the QD row.

| O | Short | Status | Ruling |
|---|---|---|---|
| O1 | Fresh session = different view? | Answered | R20 |
| O2 | Stamp on every face, or only 00? | Partly | R19, R36 (face 00 is the stamp, locked and open fields) |
| O3 | Drafts found? | Answered | R5 (already marked in the file, :35) |
| O4 | Seated face on a page with a draft door? | Open | none found |
| O5 | Where page state lives | Partly | = QD08 |
| O6 | Door of a counted face written or worked out? | Answered (reading) | R9 (faces have no door) |
| O7 | Loop .003 law? | Moot | = QD12 |
| O8 | Override: whole face or cards? | Moot (for now) | R21 |
| O9 | Content face of door page 0000? | Partly | t541u reading (0000 is the book identity page, DIRECTOR-WORDS-t541-mvp-gaps.md:87) |
| O10 | Axioms page number | Open | = QD09 |
| O11 | Draft face in a book file | Moot | R26 (small files stored; book file is an export) |
| O12 | Card name in an address | Answered (reading) | = QD39, R30 |
| O13 | Band sets; which band is build | Partly | = QD40; R32 (links connect pages) |
| O14 | Desk door form | Open | = QD41 |
| O15 | Who may do what; who is Director | Partly (deferred) | t585u (no file yet); t580u Claude fence (no file yet); t335s1296 |
| O16 | Dictionary 03.00 menu or door | Answered (reading) | = QD10, R35 |
| O17 | Brand card on 01 needs a 04 card? | Partly | = QD20 |
| O18 | Bob test: "what is my name" | Open | R11 (key words) is the likely path. Not ruled. |
| O19 | Start at pack; rewrite a draft pack | Open | = QD15 |
| O20 | Drafting steps law | Moot | = QD42 |
| O21 | What a retired page answers | Partly | R32 item 2 (retired stays on record, leaves active searches). Override part moot (R21). |
| O22 | Inside a .seq file | Moot | = QD34 |
| O23 | Word for band heads | Open | = QD14 |
| O24 | Split below 0100 | Open | = QD13 |
| O25 | Written permission | Partly | = QD43 |
| O26 | Return on its own counter | Moot | = QD44 |
| O27 | Axioms page faces | Open | = QD45 |
| O28 | Page 9999 title; 04 rule on counted 01/02 | Open | none found |
| O29 | Faces beyond 05 and 06 counted | Partly | = QD11 |
| O30 | Snapshot trust | Partly | = QD46 |
| O31 | Bootstrap law | Open | = QD47 |
| O32 | Reserved 01-09 | Open | = QD48 |
| O33 | 0117 band | Moot (reading) | = QD49 |

O34 is held (do not re-ask). Unchanged.

## 3. DECISIONS-WAITING.md (open items)

| Item | Short | Status | Ruling |
|---|---|---|---|
| Top 1 | Check sample page v2 before building | Answered | t267u:7 ("I'm good with the design ... lets get this build quickly") |
| Top 2 / S9 | One rule for scope | Moot (reading) | Built as wf grants (t267u; t401u); grant is the ceiling in practice. Not ruled in words. |
| Top 3 / T4 | Pre-draft pins | Open | none found |
| S6 | What the close record holds | Moot (reading) | Built in wf close. Not ruled. |
| T1 | Branch name and who merges | Answered | t401u:3,10 (one packs branch, one returns branch) |
| T2 | "06 allow" = "06 along"? | Open | none found |
| T5 | Face pairing (lead 01, observer 06, builder 05, person 04) | Partly | t541u:43 (01 agents and scope, 04 planned work, 05 work orders) |
| T7 | What the checker hands the lead | Partly | t533u (checker enters only after the return; DIRECTOR-WORDS-t533.md:11). Short-report rule not ruled. |
| T8 | Where the observer reports | Partly | t263 T6 (observer is the lead's assistant, DIRECTOR-WORDS-t263-T6.md:17) |
| T3 | How the finish ping reaches the compute | Answered (in direction) | t526u-t528u (builders push reports to GitHub; wf will push them; DIRECTOR-WORDS-t526-t528u.md:17); t399u-t400u |
| E1 | Which signals send work up | Partly | R35 item 1 (elevate: compute, model, person). Trigger list not ruled. |
| S4 | AGENTS.md sources | Partly | t326u, t327u (templates with exact approved wording per section) |
| S5 | Face 09 stored or a view | Answered (reading) | R28 (09 is the page's log) and R37 item 1 (one append-only log is the only source of truth) |
| S7 | Words for each card's fate | Partly | R37 item 5 (selected, pending, accepted separate). Final words open. |
| S8 | May Prime change face 01? | Open | none found |
| S10 | Cost figures | Open | none found (t575u-t576u weekly metrics sheet is related; no file yet) |
| S11 | Face 02: design or description | Open | none found |
| S14 | Who may change the Prime | Partly | t547u handover (PENDING-RULES.md:59) |
| S15 | A pass open across a change of Prime | Partly | t547u handover; t557u (builder keeps page during manual return) |
| S2 | Face 00 role and set | Open | none found |
| S3 | Where 02 drift goes in the return | Open | none found |
| E3 | How you review as it goes | Answered (in direction) | t541u G5 (`wf board` with holder, step, next, :31); t526u-t528u (reports on GitHub) |
| E4 | Prima's occasional checks | Open | none found |
| E5 | "Flex" for 07 outside dev | Open | none found |
| O3 | Who runs a face 07 trial | Partly | t460 (labs live in band 0700, DIRECTOR-WORDS-t460.md:14) |
| O9 | Each return notes mismatches | Open | none found |
| O6 | Best pass seated on plain 05 | Answered | t512 |
| O7 | Decisions on 04, notes on 06 | Partly | t541u (04 is the planned work); t460 (runner noted on face 06). Not ruled as a rule. |
| O8 | The completing page | Open | none found (t424 makes 0498 the tie-it-together MVP page; reading only) |
| W9 | Return on the same slot as its pack | Moot | t401u; wf returns go with their pass |
| W11 | Board only a view | Answered (in direction) | t541u G5 (`wf board`) |
| W12 | Read-only board first | Moot | Build order passed (wf board built) |
| W13 | Seat templates before the check step | Moot | wf kit templates built (t267u) |
| P1 | Return order | Moot | wf return template built |
| P8 | How pack 1 is made | Moot | wf pack built |
| P7 / D2 | Linked by number or by link | Answered (reading) | R32 item 1 (a link points to the page by address plus title) |
| P2 | Who fills "authorized" | Moot | wf pack fields built |
| P3 | Start commit source | Moot | wf pack start commit built; t523 grant-ref (core run from prima/build) |
| P4 | What is hashed, and when | Partly | R37 item 3 (the compute fills hashes). Method in wf. |
| P5 | When the code copy of the sheet ends | Open | none found |
| D1 | What the lab page is for | Answered | t460 (labs in band 0700, findings in labs/07NN) |
| D3 | Who makes pages and links | Partly | R33 item 1 (through the compute); t460 Q17 (Prima types init-page) |
| D4 | 05NN jobs or build | Moot | t424 stage bands replace it |
| D5 | Prima's note before the next pack | Open | none found |
| W1-W7 | Work book SPEC items | Open | not checked one by one; no later ruling names them |
| "6" and "8" | "6 framing the work, with 8 returning" | Open | none found |
| K8 | Build order | Moot | t267u (build now); t424 stage plan |
| R37 item 5 | Where selected, pending, accepted show | Open | none found |
| Next 1-3 | Sample as fixture; tools in order; workflow branch | Moot | t267u (workflow branch built); t401u |

## 4. QUESTIONS-2026-11-19.md

| # | Short | Status | Ruling |
|---|---|---|---|
| 1-3 | AGENTS.md manager M1-M3 | Open | none found after Nov 19 |
| 4-5 | Version numbers; typed-up words as source | Open | none found |
| 6 | Locked rules (C9); 0000-0009 layout (C10) | Open | none found |
| 7 | Joining characters (ZWJ/ZWNJ) | Open | none found |
| 8 | Board columns, STALE after 24h, log-only first | Partly | t541u G5 (`wf board` with holder, step, next). Column names not ruled (t541u says so, :33). |
| 9 | Handoff trial | Open | none found |
| 10 | Several models on one page at once | Answered | t533u (one worker per page, PENDING-RULES.md:22); t541u:19 |
| 11 | Roadmap C1-C12, G1-G7 | Partly | t326u answers G4 (per Prima's record). Others open. |
| 12 | Delete Tester's old scratch folders | Open | none found |
| 13 | `wf board` merge | Open | none found (board later used, t541u; merge itself not ruled in a file) |
| 14-17 | Log order check; old wf rename; merge harden-dev | Open | t381u (out of rule is strict) covers the idea, not these asks |
| 18-19 | Q14: clear "out of rule"; skip or count | Open | none found |

## 5. seqpage-QUESTIONS.md (open ones)

| S | Short | Status | Ruling |
|---|---|---|---|
| S1 | Derived lines change in place | Moot | R26, R31 item 7 (one file per face) |
| S2 | Inherited faces | Moot (for now) | R21 |
| S3 | Face 08 in lineage | Open | none found |
| S4 | Trailing spaces | Partly | = QD36, R27 |
| S5 | New pages from a file | Moot (reading) | = QD37, R33 item 1 |
| S7 | Where a draft's reason lives | Open | = QD38 |
| S10 | Shape of an override page | Moot (for now) | R21 |

S6, S8 and S9 are already marked settled in the file.

## What Prima could do

- Mark the Answered rows in each list with the ruling (one line each). The lists say "only you approve", so marking an answer is a records fix, not a ruling.
- Close the Moot rows as "replaced by wf" or "parked under R21", with the cite.
- Check every "(reading)" row before marking it.
- File DIRECTOR-WORDS for t572u-t593u first (STALE-DOCS S8). Three rows here lean on t580u and t585u with no file.
- Re-check QUESTIONS-2026-11-19 against the chat record. It is the most likely to hold live questions.
