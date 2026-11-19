# Trial: work order view and the builder name (0413, 0414)

Who: Cursor-C (Test), for Prima. This is a hostile pass. It is not a ruling.
Matthew approves rulings. An agent's approval does not.
Date: 2026-11-19.
Read: docs/design/PASS-RECORD-t436u.md (v1, v2, v-note) and docs/design/STAGE-PLAN-90.50.10.md sections 14 and 15.
wf source: branch returns, commit 3646e344. src/ is the same bytes as c09fa60c (the commit the design cites). Only tests/ changed after c09fa60c.
Plan base: prima/build 8e96151d.

## Result

| Page | Result |
|---|---|
| 90.50.10.0413 work order view | FAIL |
| 90.50.10.0414 wf prints the builder | FAIL |

Counts: 9 major, 8 minor, 5 note.

The pass totals in section 15 are right: 23 / 34 / 57, plus 0403. The wave count 17 is right. The reason given for 17 is not. See minor 1 and note 2.

His words in the words files are quoted accurately. The failures are what the design adds after the quote, and locks that do not hold in wf.

## What I ran

Scratch clone only. Nothing from it was pushed.

`cargo test --test hostile_work_order` on returns 3646e344. 5 passed, 0 failed.

- quote_is_split_and_a_redraft_drops_it
- pack_does_not_print_builder_or_words_and_prime_can_claim
- prime_and_grant_do_not_lock_at_init
- first_claim_locks_out_the_named_builder_and_the_name_is_the_only_check
- chain_accepts_a_rewritten_quote_and_an_edited_last_line

The 0403 return file was checked with git cat-file on commit d9110934. That check is note 1.

## Major

### 1. A paste of his words is cut up, and a redraft deletes it

Page: 0413. Grade: major.

The design stores the quote in a draft field named words: (PASS-RECORD section 5.4 and the v-note on t440). wf's draft reader keeps a line only when it has a colon, or when it starts with a space (src/cmd.rs:147-160 at 3646e344).

I drafted this:

```
words: Quote my exact words once
with file, line and commit
file: docs/review/DIRECTOR-WORDS-t440.md
line: 7
commit: 227933e
```

The stored words value was only "Quote my exact words once". The second line was dropped. file, line, and commit became three other fields. A second draft of the same pass, with those lines left out, replaced the whole field map (src/page.rs:316-321). The quote was gone. Pack still succeeded.

Matthew, t440 (docs/review/DIRECTOR-WORDS-t440.md:7): "Quote my exact words once, with file, line and commit."

Fix: read the quote from its own file, whole, not through the key: value reader. Refuse the draft when the file name, the line number, or the commit is missing. A redraft that omits the quote keeps the quote already stored.

### 2. The quote is not in the prompt, and the pack hash does not cover it

Page: 0413. Grade: major.

After a draft that contained words: and builder:, PACK.md, PROMPT.md, and BUILDER-PROMPT.md did not contain the quote or the builder name. PROMPT.md still says `--as <your-name>` (templates/v3/prompt.txt:4). The pack fill list has no words key and no builder key (src/cmd.rs:395-401).

I then changed the quote inside the log and recomputed the later chain hashes. wf loaded the page. The pack hash was the same string as before. The quote is not inside pack_text, so pack_hash (src/cmd.rs:403) does not seal it.

Matthew, t436u (docs/review/DIRECTOR-WORDS-t436u.md:9): the document "starts with my words, your lead formatting into a framed piece of work to the worker building it." The framed piece the worker is told to read is PROMPT.md (templates/v3/builder.txt:23). The quote is not there.

Fix: copy the quote into the pack text, so the pack hash covers it, and print it as the first lines of PROMPT.md and BUILDER-PROMPT.md.

### 3. Prime and the grant do not lock at init

Page: 0413. Grade: major.

Section 4.1 says person, title, and prime lock at init. Person and title have no later command. I found none in src/cmd.rs. Prime does. set-prime lets the person or the current prime name a new prime (src/cmd.rs:213-217). I ran it. Face 00 then showed the new prime. Grant paths grow when the person runs grant (src/cmd.rs:220-226). I added tests/ and face 00 listed it.

The table can say: each log entry stays as written. It cannot say the live prime and the live grant freeze at init.

Fix: split the row. Person and title lock at init. Prime keeps a history (face 00 already prints previous primes, src/render.rs:354-356). Grant paths can grow. The work order shows the prime and the grant as they were at pack time, from the pack entry, and shows later changes as later entries.

### 4. The chain does not seal the last line, and a rebuilt chain still loads

Pages: 0413 and 0414. Grade: major.

Section 4 says the lock proof is always the next entry's prev hash (src/log.rs:2, src/log.rs:81-89). Two holes:

- I edited the actor on the last line and left its prev value alone. The page loaded. The claim name changed from bob to Cursor-C. Nothing seals the last entry. A field is not locked at the moment it is written. It is unsealed until a later entry exists.
- I changed an earlier draft field and rewrote each later prev hash. The page loaded. verify's chain check accepts that file. wf's own commands only append (src/log.rs:96-111). A hand edit of log.jsonl is a different path, and the chain does not stop it.

The outside seal is a second copy. intake refuses a returned log that is not the local log plus new lines at the end (src/cmd.rs:625-626). The design does not name that seal.

Fix: the view prints "sealed by the next entry" only when a next entry exists. The last entry prints "last entry, not sealed". Name the git copy of the log as the outside seal.

### 5. The folder he opened does not update when the return is pushed

Page: 0413. Grade: major.

He looked in D:\Git\wf-run\pages\90.50.10.0403\05.01 and saw no return (docs/review/DIRECTOR-WORDS-t436u.md:4). The builder prompt checks that pages folder out from the packs branch and throws away local page writes (templates/v3/builder.txt:15-18).

return --push copies the log to the returns branch (src/cmd.rs:554-575). It does not run publish-pack. publish-pack is a separate command, and it commits pages/<page> on the packs checkout (src/cmd.rs:579-596). Section 5.8 says the new view "goes out with publish-pack" and the returns branch is unchanged. It never says to publish again after the return, the check, or the close.

So a WORK-ORDER.md published at pack time still says the return is not yet, in the folder he opens, after the return has been pushed.

Fix: name the second publish. After return, check, signoff, and close, publish the page again, or write the view to the branch his wf-run pages folder pulls. Ask him which folder that is (question 5).

### 6. The notes rule cites a check that does not list notes

Page: 0413. Grade: major.

Section 5.5 says section 8 lists notes in "the same window draft already uses (cmd.rs:296-298)". Those lines only ask whether the newest face 06 entry is newer than the last close. They do not collect a window. They use the page's last close, not this pass's close.

A later note is tied to a closed pass when the text starts with "on 05.NN:". That is a match on the wording. Axiom 8 says a connection is written, and a match is not a connection (docs/spec/Axioms.md:27). The design's own check marks Connection PASS and says the notes are "never by matching text" (PASS-RECORD section 6). The rule it just wrote is a text match.

A note that corrects the pass and does not use that prefix stays off the work order. A note that happens to start with the prefix is pulled in.

Fix: give the note a pass field, written by the command, for example pass: 05.01. List notes by that field and by entry numbers stored when the pass is drafted. Do not match a prefix.

### 7. A lied --as takes the claim, and filling in the name hides the raise

Page: 0414. Grade: major.

Today claim records whatever --as says. It does not check the name against a list or a role (src/cmd.rs:435-443). The entry data is only the pass number. The name is the actor. --as wins over WF_AS (src/lib.rs:128).

I claimed as pri while WF_AS was Cursor-C. The claim stuck. Prime can take the builder slot. A second claim as Cursor-C was refused: first claim wins (src/cmd.rs:439-440).

I claimed as Grok-1. Cursor-C was then refused. The named builder cannot claim after a lie. Only the claim holder can return (src/cmd.rs:488).

The same person can check their own work under a second name. Check refuses only when the check name equals the claim name (src/cmd.rs:730 and src/cmd.rs:778). Grok-1 was refused. Cursor-C was accepted, on Grok-1's return.

v2.4 says the prompt prints the builder first and the --as value is filled in. BUILDER-PROMPT.md claims with WF_AS and no --as (templates/v3/builder.txt:21 and :25). If that blank is filled with the name on the pack, a person who follows the prompt claims under the official name. The raise in v2.3 never runs. The raise runs only when they disobey the prompt and type their own name.

Fix: print "Builder: <name>" as a label. Leave the claim name blank, and tell the person to type their own name. Compare the typed name to the label. Do not fill --as or WF_AS with the pack's name.

### 8. Editing template version 4 in place breaks packs already made

Page: 0414. Grade: major.

There is no templates/v4 at 3646e344. The live version constant is "3" (src/render.rs:29). v2.4 says 0404 will make v4, and 0414 will edit v4 rather than add a version.

PROMPT.md and AGENTS.md are hashed at pack (src/render.rs:405, written at src/cmd.rs:423-429). If a later wf reprints different bytes, the page is invalid and wf will not reprint those files (src/render.rs:456-458 and src/render.rs:484-494). Packs made with v4 between wave 3 and wave 14 would fail that check once 0414 changes the v4 prompt text.

BUILDER-PROMPT.md is not hashed (src/render.rs:26). An in-place edit rewrites it on the next verify --fix for every pass that uses that version.

Fix: 0414 writes the next template version. Old pack entries keep the version they recorded, and the old text.

### 9. The raise is more than he approved, and the work does not wait

Page: 0414. Grade: major.

t439u asks for the builder's name on the next prompt (docs/review/DIRECTOR-WORDS-t439u.md:5-14). t441 says yes to adding page 0414, and the question was only "Should WF print the builder's name itself" (docs/review/DIRECTOR-WORDS-t441.md:3 and :7).

The page's done-when also refuses unknown names, and it takes a claim under another name and writes an elevate (STAGE-PLAN section 15.1). Section 15.5 already says the raise is not in his answer. v2.3 then says "No new question" because decisions.md:570 (E4) is settled.

E4 says another person may do the work, but raises it before moving forward. The design records the raise and lets the return happen with no answer. "Before moving forward" is not settled by that. workflow-loop.003.md:172 is a draft, and it compares the builder to the lead. The design compares the claim name to the builder field. Those are different pairs.

The first-claim rule makes this sharper. The other name is taken. The named builder is locked out (major 7). Prime sees a note at signoff, which is after the work.

Fix: 0414, as approved, only prints the name. Ask him whether a different builder must wait for an answer before the return (question 1). Do not mark that wait as already settled.

## Minor

### 1. The wave count is 17, and the render.rs reason is wrong

Pages: 0413 and 0414. Grade: minor.

Section 15.4 lists waves 1 through 17. I count 17. 0414 needs src/cmd.rs, and cmd.rs stays busy from wave 2 through wave 13 (0404, 0408, 0409, 0406, 0411, 0412). 0498 needs 0414 (section 15.2), so 0498 stays at waves 16 and 17.

The same paragraph says every render.rs slot before wave 14 is taken. render.rs is free in waves 10 through 13. 0411 and 0412 change src/cmd.rs and src/lib.rs only (section 13.5). They do not change src/render.rs. 0414 still cannot start there, because of cmd.rs, not because render.rs is busy.

Fix: delete the render.rs sentence. Say 0414 waits on cmd.rs.

### 2. The older text still says 15 waves

Pages: 0413 and 0414. Grade: minor.

PASS-RECORD section 7.2 says no wave is added, still 15. v2.4 says 17 waves and "not added to the stage plan in this note". Section 15 is now in the stage plan, because t441 said yes. The pass record has no later line that says the plan caught up.

Section 14.3 still says still 15, and stage 21/31/52. Section 15 says 17, and stage 23/34/57. Adding those two stage totals would double count.

Fix: add a short v3 note on the pass record: section 15 is in the plan, the live count is 17 and 23/34/57, and section 7.2's "still 15" is the older sentence. Leave the old sentence in place.

### 3. Two of the five packed files are not hashed

Page: 0413. Grade: minor.

Section 5.3 says PACK.md, PROMPT.md, AGENTS.md, BUILDER-PROMPT.md, and RETURN-TEMPLATE.md stay byte for byte because their hashes are in the pack entry. The pack entry hashes the pack text, AGENTS.md, and PROMPT.md (src/render.rs:405). BUILDER-PROMPT.md is marked "a view, not hashed" (src/render.rs:26). RETURN-TEMPLATE.md is not in that hash list. A later template change rewrites them.

AGENTS.md is also omitted when the pass reuses an older copy (src/render.rs:392-394). BUILDER-PROMPT.md is printed only for template version 3 (src/render.rs:395-397).

Fix: say which three are pinned. Say the other two are reprinted from the template version stored on the pack, and that version's text must not change (see major 8).

### 4. The door-open cite does not point at a line, and it is about a different subject

Page: 0414. Grade: minor.

v2.3 cites t434.md:28 for "door open, not proof". docs/review/DIRECTOR-WORDS-t434.md has 12 lines. The words are at line 10, and they are about stages 3 and 5: "Yes, stages 3 and 5 go ahead, marked door open not proof." They do not say that --as catches mistakes and not pretenders.

The limit itself is real. I showed it in major 7. The cite gives it his authority for the wrong subject.

Fix: drop the t434 cite. State the --as limit as the design's own limit, next to question 2.

### 5. A face 01 edit before signoff does not block the close

Pages: 0413 and 0414. Grade: minor.

Section 15.2 says changing 0701 face 01 before 0701.05.01 closes would stop that pass closing as passed, and cites src/cmd.rs:848-849. Those lines refuse the close when face 01's entry is newer than the signoff entry. An edit made before signoff is older than the signoff. Signoff of passed can still succeed if the note covers the drift (src/cmd.rs:681 and src/cmd.rs:809-810).

Fix: cite the signoff note rule. Keep the hold if you want the lab page quiet, and say it is a choice, not a hard stop in cmd.rs:848-849.

### 6. Refusing a seventh builder name is more than he said

Page: 0414. Grade: minor.

t439u lists six builders and says "Currently we have" (docs/review/DIRECTOR-WORDS-t439u.md:7-14). The done-when refuses any other name at pack. He did not say the list is closed. Four of the six are "not setup" or "no setup". The design still lets a pack name them. That tension is already written. The closed list is not.

Fix: ask him (question 3). Until he answers, an unknown name prints "builder: not in the list" and still packs, the same way a missing name prints "builder: not named".

### 7. The work order's eight sections do not include the builder

Pages: 0413 and 0414. Grade: minor.

Section 5.1 lists the frame as outcome, jobs, may touch, checks, done when, stop if, and the pack links. v2 adds builder: to the field table and says the view can show the draft field. The eight sections are not updated. 0414's done-when does not require the name on WORK-ORDER.md.

Fix: add the builder line to section 2 of the view, taken from the pack text after major 2 and major 8, so the one document and the prompt show the same name.

### 8. A pack with no builder name does not say what claim does

Page: 0414. Grade: minor.

Old drafts have no builder field. The design says they still pack and print "builder: not named". It does not say whether claim then writes an elevate. v2.3 says a claim by a name other than builder: writes one. With no builder, every name is other.

Fix: when the pack says "builder: not named", claim records the name and writes no elevate. Say that in the trial list for lab_0414.

## Note

### 1. The 0403 hash finding is true

Page: 0413. Grade: note.

Section 2 says the return hash is the trimmed git text, not the file bytes (src/git.rs:11). On commit d9110934, file .workshop/returns/90.50.10.0403.05.01.md is 2704 bytes, ends in CR LF, and hashes to e49c5fbf97f2. Log entry 8 stores 2702 bytes of text and hash 3e707246e39f. The scratch return test showed the same split on a new CR LF file.

No fix inside 0413. The view should say the hash is of the trimmed text, as section 5.7 already says. A byte hash is a later cmd.rs job, as the design says.

### 2. The stage totals add up

Pages: 0413 and 0414. Grade: note.

From the section 15.3 table, best / likely / worst:

- Work pages: 11 / 21 / 32 (ten pages; 0406 is the 2/3/4; 0498 worst is 4; the other eight are 1/2/3).
- Lab 0701: 12 / 13 / 25 (pass 1 is 2/3/5, plus 10 trials at 1/1/2). The ten trials are 0404, 0406, 0407, 0408, 0409, 0411, 0412, 0413, 0414, 0498.
- Stage: 23 / 34 / 57. 0403 is extra, not inside the 23.

Waves 1 through 17 are seventeen waves. Section 14's 21/31/52 and "still 15" are the previous note. Read section 15 for the live count. Do not add the two totals together.

### 3. His words are quoted accurately

Pages: 0413 and 0414. Grade: note.

I compared the quotes in the pass record and in sections 14 and 15 to docs/review/DIRECTOR-WORDS-t436u.md, DIRECTOR-WORDS-t437-t438u.md, DIRECTOR-WORDS-t439u.md, DIRECTOR-WORDS-t440.md, and DIRECTOR-WORDS-t441.md. The quoted lines match. v2.1 correctly says the "Effect" line in the t439u file is Prima's reading, not his words. The failures above are additions after the quote.

### 4. The main story in section 2 matches the source

Page: 0413. Grade: note.

At 3646e344 the pass folder is filled only at pack, from src/render.rs:387-399. The return text and its hash are stored at return (src/cmd.rs:504 and src/cmd.rs:519-521). Face 05 prints the story (src/render.rs:315-347). A missing view file is recorded at src/render.rs:639 and blocks writes at src/lib.rs:202-206. Those cites match. The design is right that a new required file would lock old pages unless a missing WORK-ORDER.md is exempt. Keep that exemption.

### 5. 0414 also exists as an old library page, in another book

Page: 0414. Grade: note.

docs/reference/LIB-BUILD-SURVEY.md:104 lists "0414 bench" next to "0413 assistants". The pass record mentions the library 0413 and does not mention the library 0414. The address in this book, 90.50.10.0414, is still free. Titles may be reused across books (docs/spec/DIRECTOR-RULINGS.md, R34). No fix required. Name the library page in the 0414 note so the next reader does not think the slot was checked only for 0413.

## Page verdicts

0413 FAIL. Majors 1 through 6. The view can still be built after those fixes. The exemption for a missing WORK-ORDER.md on old pages should stay (note 4).

0414 FAIL. Majors 7 through 9. Printing the name is what he approved. The raise, the closed name list, and the in-place template edit are not ready to build.

## Questions for Matthew

1. If the person who does the work is not the builder named on the pack, must they wait for an answer before they return, or is a note enough?
2. Should that person type their own name on the claim, or the name printed on the pack?
3. Is the list of six builders closed? Should a new name be refused, or printed as "not in the list" and still packed?
4. Should your words be the first lines of the prompt the builder reads, with the file, the line, and the commit checked by wf?
5. When you look in pages/<page>/05.NN on your machine, should that folder update as soon as the return is pushed?
