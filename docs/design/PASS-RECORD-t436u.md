# Pass record: 05.NN read as one work order (t436u, t438u)

state: v1 design for Prima's review. Not a ruling. Nothing built; wf not run; nothing
written under wf-run-gh/pages.
made: 2026-11-19, 2:27 PM EST, by Designer.
base: wf returns c09fa60c (code d9110934); build repo d0827d9; packs b57cfdd2.
axioms: 1.7.8,6.2.8

## 1. Matthew's words, quoted exactly

t435u (docs/review/DIRECTOR-WORDS-t436u.md:4, :6, at 9047205): "I looked over
D:\Git\wf-run\pages\90.50.10.0403\05.01" and "i didn't see a return in there.  Was on
created and pushed from cursor-1 for the return?  I didn't see one."

t436u (DIRECTOR-WORDS-t436u.md:9): "So I feel the completed pack > becomes a return >
reviewed > closed with the notes along the way.  IT's one evolving document that starts
with my words, your lead formatting into a framed piece of work to the worker building
it.  It being reviewed then sitting as a 05.NN So if we have 10 passes on that page over
a year, we can see what we did and learned each time we work on this page of work."

t438u (DIRECTOR-WORDS-t437-t438u.md:7, at d0827d9): "So lets define this as a workorder
is what we pack/return/review/close.  A work order can be broken into sections with
fields, some once created can't be changed, others filled in by different parties in
the chain of work."

Where Prima's relay differs:
- t436u: the relay drops "So I feel" at the start and ends at "each time"; the file goes
  on "we work on this page of work." Meaning unchanged.
- t438u: the relay matches, except double spaces.
- t435u: Matthew looked in his own clone, D:\Git\wf-run, not wf-run-gh.
- Relay (steering): "Cursor-1 has 0701". At packs b57cfdd2, 0701.05.01 is at tail pack,
  claim "-" (pages/90.50.10.0701/05.md), and origin/returns has no 0701 log yet. A claim
  may exist in Cursor-1's own run folder; I could not see it.
- Relay (brief): "The review notes live only in log.jsonl, rendered into 05.md." True,
  and more than that is already there; see 2.

## 2. How wf does it today (checked at c09fa60c, and in 0403's log)

- The pass folder pages/<page>/05.NN/ holds only what is printed at pack: PACK.md,
  PROMPT.md, AGENTS.md, BUILDER-PROMPT.md, RETURN-TEMPLATE.md (src/render.rs:387-399).
  Nothing is added there later. That is why Matthew found no return in 05.01/.
- The return is NOT missing. wf took the whole return text into the log at return:
  0403 entry 8 holds "text" (2702 bytes) and "hash" 3e707246e39f
  (src/cmd.rs:504, :519-521). The file itself is on returns at
  .workshop/returns/90.50.10.0403.05.01.md in commit d9110934.
- The whole story is already printed, but in the page-wide 05.md, not in 05.01/:
  pack hash, return text, check report, signoff, close record (src/render.rs:315-347;
  pages/90.50.10.0403/05.md shows all of it).
- Every entry is chained: each log line holds prev, the sha256 of the line before
  (src/log.rs:2, :81-89). So any field in an entry is locked once the next entry exists.
- Finding: the return "hash" is the sha256 of the text after git's output is trimmed
  (src/git.rs:11, trim_end), not of the file's bytes. For 0403 the file at d9110934
  hashes to e49c5fbf97f2, the log says 3e707246e39f (the file ends in CR LF). The copy
  is still provable from the chain and from commit plus path, but not with a plain
  "git show | sha256sum".

## 3. Name: work order, and the existing words

"Work order" does not clash; it already names the same thing.
- Matthew, quoted in docs/review/CODEX-MANAGER-DRAFT-t304u.md:20: "a workorder is the
  05.NN"; and :28 "The workorder never disappears". (Quoted inside a Codex draft; there
  is no DIRECTOR-WORDS file for it.)
- docs/design/WF-BOARD.md:5 and :12 ("one card per 05.NN work order"); wf src/board.rs:1.
- seqAddr.md calls 05.NN a counter (:128) on face 05 "passes, as counters" (:154). wf
  code calls it a pass (src/cmd.rs, p.pass). "Pack" is one tail of it (seqAddr.md:128),
  and "job" is a work card w01-wNN (src/render.rs:69-71) or a job page (seqAddr.md:322).
Use: the address is 05.NN; the reader's name is "work order"; wf code keeps "pass". Do
not call the whole thing a pack or a job.

## 4. The work order: sections, fields, who fills, when it locks

Lock proof is always the same: the field is in a log entry, and the chain hash of that
entry is held by the next entry (src/log.rs:2). Where an entry also carries its own
hash, it is named. Today's home: where the field lives at c09fa60c.

### 4.1 Authority (his words)

| Field | Filled by | Locks at | Proof | Today's home |
|---|---|---|---|---|
| person, title, prime | person (init) | init | init entry | log init; 00.md (render.rs:352-361) |
| grant paths | person | init or grant | init / grant entry | log; 00.md; PACK.md "grant:" (templates/pack.txt:11) |
| grant ref (tNNNu) | person | same | same | log grant_ref; PACK.md grant line |
| words quote with file:line | Prime | at draft, fixed at pack | draft entry fields | GAP: nowhere. Only the ref text (cmd.rs:198). 0701 face 06 quotes t437 as a note |
| who typed (runner) | Prime | at the note | face 06 entry | face 06 note only, until 0411/0412 (cmd.rs:190) |

### 4.2 Frame (Prime's pack)

| Field | Filled by | Locks at | Proof | Today's home |
|---|---|---|---|---|
| outcome, overview, axioms, w01-wNN, may touch, checks, stop if, repo, start, predecessor | Prime | pack (draft may be redrafted until then) | pack entry pack_hash (cmd.rs:403) | draft entry fields (cmd.rs:304); PACK.md (render.rs:390) |
| must not | wf (fixed text) | pack | pack_hash | templates/pack.txt:18; a draft field "must not" is stored but not printed |
| done when | Prime, on face 01 | pack | pack entry done_when; face 01 entry hash in sources | PACK.md; face 01 |
| pins 04, 06, last closed 05 | wf | draft; checked again at pack | draft entry pins (cmd.rs:303, :375-377) | PACK.md pins |
| start commit, branch, return file | wf | pack | pack entry (cmd.rs:380, :403) | PACK.md; PROMPT.md |
| sources: face 01, kit AXIOMS, DESIGN hashes | wf | pack | pack entry sources | PACK.md |
| AGENTS.md, PROMPT.md | wf | pack | agents_hash, prompt_hash (render.rs:405) | 05.NN/AGENTS.md, PROMPT.md |
| BUILDER-PROMPT.md, RETURN-TEMPLATE.md | wf | pack (printed from the pack entry) | pack_hash, templates | 05.NN/ (render.rs:396, :398) |

### 4.3 Claim

| Field | Filled by | Locks at | Proof | Today's home |
|---|---|---|---|---|
| builder name | builder via wf | claim (first wins) | claim entry (cmd.rs:435-443) | log; 05.md heading |

### 4.4 Return (the builder)

| Field | Filled by | Locks at | Proof | Today's home |
|---|---|---|---|---|
| done, changed, noticed, w01-wNN results, proof, not done, unprompted, overflow | builder | return | return entry text and hash (cmd.rs:519-521) | .workshop/returns/<page>.05.NN.md on returns; log; 05.md (render.rs:330-337) |
| design review line (t416u.md:7) | builder | return | same | GAP: not in templates/return.txt at c09fa60c; added by Prima by hand; 0404 adds it |
| commit, branch, file | wf | return | return entry | log; 05.md |
| git changed list | wf | return | return entry | log; 05.md; close record |
| refusals | wf | each refusal | return-refused entry (cmd.rs:515) | log; 05.md |
| jobs not done | wf | return | elevate entries (cmd.rs:522-527) | log |

### 4.5 Check (the checker, never the builder)

| Field | Filled by | Locks at | Proof | Today's home |
|---|---|---|---|---|
| commit checked, each check command and result, verdict, report | checker via wf | check | check entry (cmd.rs:782) | log; 05.md (render.rs:338-340) |

### 4.6 Signoff and close

| Field | Filled by | Locks at | Proof | Today's home |
|---|---|---|---|---|
| outcome, cards accepted, note | Prime | signoff | signoff entry (cmd.rs:833) | log; 05.md one line (render.rs:341-343); the note shows only in the close record |
| close record | wf | close | close entry record_hash (cmd.rs:862) | log; 05.md (render.rs:344-346) |

### 4.7 Notes along the way (never locked as a section; each note is locked)

| Field | Filled by | Locks at | Proof | Today's home |
|---|---|---|---|---|
| Prime notes | Prime | each note | face 06 entry | 06.md, page-wide; not tied to a pass |
| elevations and answers | wf, Prime, person | each | elevate / answer entries | log |
| observer findings | observer | each | finding entry | log only |
| halt, resume | Prime or person | each | entries | log |
| a correction to a locked field | whoever owns it | as a new note | new entry | GAP: no way to tie a note to a closed 05.NN |

Gaps, all in one place: the words quote; one per-work-order view in 05.NN/; notes tied
to a work order; corrections to a closed work order; the t416u design review line (0404);
the return file byte hash (2, finding); the signoff note shown only in the close record.

## 5. The design

1. A new view, pages/<page>/05.NN/WORK-ORDER.md, printed by wf from the log, like 05.md.
   It is a render, never a source (DIRECTOR-RULINGS.md:195; Axioms.md:15). Sections in
   order: 1 authority (words, grant, ref), 2 frame (outcome, jobs, may touch, checks,
   done when, stop if, links to PACK.md and PROMPT.md with their hashes), 3 claim,
   4 return (the text as recorded, its entry and hash, commit and file), 5 check,
   6 signoff, 7 close record, 8 notes. A section not reached yet says "not yet".
2. Each field shows who filled it, the entry number and, once locked, "locked at entry
   N". Rebuilt from the log the same way every time, so it can be checked by reprinting.
3. Packed files never change: PACK.md, PROMPT.md, AGENTS.md, BUILDER-PROMPT.md,
   RETURN-TEMPLATE.md stay byte for byte (their hashes are in the pack entry).
4. Words: Prime adds a "words:" field to the draft (his quote, file:line, commit). draft
   already stores any field (cmd.rs:265, :304), so no CLI change; the pack template is
   unchanged. With no words field, section 1 prints "words: not quoted; grant ref only".
5. Notes: section 8 lists entries for this pass (data.pass = NN) and page entries
   (face 06, findings, halts) after the previous close and up to this close, the same
   window draft already uses (cmd.rs:296-298). A later face 06 note that starts
   "on 05.NN:" is listed under "later notes" of 05.NN. That is how a closed work order is
   corrected: a new note, never an edit (Axioms.md:23).
6. No RETURN.md copy. Prima's option copied the returned form into 05.NN/RETURN.md. The
   return text and its hash are already in the return entry (cmd.rs:519-521), so a copy
   is a second home for the same text (Axioms.md:15; workflow-loop.md:170, "In the book
   format nothing is copied"). WORK-ORDER.md prints it from the log instead.
7. No new hash needed for the copy to be provable: the return entry holds text and hash,
   and the chain holds the entry. The byte-hash finding (2) stays a tension: section 4
   prints the commit and path, and says the hash is of the trimmed text (git.rs:11).
8. Branch: WORK-ORDER.md is under pages/<page>/, so it lives on packs and goes out with
   publish-pack, which commits pages/<page> by path (cmd.rs:579-596). The returns
   branch is unchanged: work and the log copy (push_log, cmd.rs:554-575).
9. Closed passes (0403.05.01): nothing to back-fill. Entries 1-12 hold every section.
   With the new wf, WORK-ORDER.md prints from the log; no entry is added or rewritten.
   Only the words field is empty (its draft had none); a face 06 note "on 05.01:" with
   the t413u quote adds it as a later note.
10. Old pages: today a missing view makes every command refuse until wf verify --fix
    (src/lib.rs:202-206; src/render.rs:639). So the new view must not lock up pages made
    by the old wf: a missing WORK-ORDER.md is printed by the next write and reported by
    verify, not refused. A changed one is refused like any view.
11. Code: src/render.rs only: views() adds the file (:378-401), a work_order() printer
    beside face05() (:315), and the missing-file rule in edited() (:608-639). No change
    to cmd.rs, lib.rs or the log. If Prima wants the byte hash too, that is a later,
    separate cmd.rs job; not here.

## 6. Checks against the files (RELEASE-CHECK.md @ c0e5b22)

compared: Axioms.md @ 3291593, seqAddr.md @ 34eff12, DIRECTOR-RULINGS.md @ 26a17be,
workflow-loop.md @ 3291593, workflow-loop.003.md @ 420fc98, face00.md @ 1cd06de,
wf src at c09fa60c.

| Item | Source file:line | Seen in this design | Result |
|---|---|---|---|
| 6 Lineage: locked fields never change | Axioms.md:23 | 5.3 packed files unchanged; 5.5 corrections are new notes; 5.9 no rewrite | PASS |
| 2 Fractal: one source | Axioms.md:15; DIRECTOR-RULINGS.md:195 | WORK-ORDER.md is a render; no RETURN.md copy (5.6) | PASS |
| 8 Connection | Axioms.md:27 | notes tied by pass number or "on 05.NN:", never by matching text; links with hashes | PASS |
| 7 Missing | Axioms.md:25 | gaps listed in 4, words "not quoted" printed, not filled | PASS |
| 9 Trial | Axioms.md:29 | trials in lab 0701 (7.3); no hostile pass on this design yet | TENSION |
| Counter and tails | seqAddr.md:128, :140 | state stays on the counter; no new tail | PASS |
| Face 05 counted, 05.00 board | seqAddr.md:197, :200 | 05.md stays the board; WORK-ORDER.md is one counter's view | PASS |
| 05.NN/ files | seqAddr.md has no files inside a counter | the folder is wf v0's layout, not seqAddr grammar | TENSION (as today) |
| Card keeps its history | workflow-loop.003.md:176; workflow-loop.md:165 | all sections kept after close | PASS (drafts) |
| Return on the same counter, nothing copied | workflow-loop.md:170; .003:181 | 5.6 | PASS (drafts) |
| Compute may add to 05 after a lock | DIRECTOR-RULINGS.md:132 | a new view and later notes are additions by wf | PASS |
| Review tied to the version it read | DIRECTOR-RULINGS.md:198 | check section shows the commit checked | PASS |
| Return and next step together | DIRECTOR-RULINGS.md:196 | return section and its elevations | PASS |
| Approval record | face00.md:202, :375 (PROPOSED, 7) | words section is where it would show; not settled | TENSION |
| Hash chain | src/log.rs:2, :81-89 | every lock proof is an entry in the chain | PASS |
| t416u line | DIRECTOR-WORDS-t416u.md:7 | listed as a gap; 0404 adds it | PASS (gap named) |
| H1 habits | t415u.md:5 | "copy the form to RETURN.md" traced and refused (5.6); file name traced to WF-BOARD.md:12 and t304u :20; page slot traced in 7.1 | PASS |
| A1-A9 on 90.50.10.0413 | t413u.md:7, :9; seqAddr.md:240-242 | desk 90, shelf 50, book 10, page 0413 in band 0400, not 00 or 99 | PASS |
| ASCII, plain words, no R-numbers | DIRECTOR-RULINGS.md:16 | file | PASS |

Verdict: no FAIL. Tensions: no hostile pass yet; the byte hash of the return file; the
05.NN/ folder is a wf layout; the approval record is open in face00.md; the term
"work order" for 05.NN is quoted from a Codex draft, not a words file.

## 7. The wf page

### 7.1 Address: 90.50.10.0413

- Not 0405 or 0410: planned, never made, and kept unused so older plan lines still point
  at the right work (STAGE-PLAN-90.50.10.md 11.4, 12.5; Axioms.md:23, :27). Not 0497
  (13.4, same reason). An address once titled is never reused (DIRECTOR-RULINGS.md:
  129-130).
- 0413 is the next slot after 0412 and was never planned or made in book 90.50.10
  (wf-run-gh pages/ has no 0413; the stage plan never names it). The only 0413 in docs/
  is LIB:W 0413.assistants, an old library page in another book
  (docs/reference/LIB-BUILD-SURVEY.md:104), so no title is reused. It is on PP01-PP98
  (seqAddr.md:240-242).
- Title: "work order view: 05.NN reads as one record (t436u, t438u)".

### 7.2 Files, size, place

- May touch: src/render.rs. Grant: src/render.rs (t436u, t438u).
- Size (best/likely/worst passes): 1/2/3. Its trial in lab 0701: 1/1/2.
- Not in the src/cmd.rs queue. It shares src/render.rs with 0404, 0406 and 0407. Under
  the strict reading (t432.md:11) it runs in wave 6 beside 0409 (cmd.rs, lib.rs,
  page.rs), and its trial in wave 7 beside trial 0409. No wave is added: still 15.
- Prima's two options: "before 0404" puts it in wave 2 with 0404, which shares
  render.rs, so it would add two waves (17). "Next after 0701" is the same as before 0404.
  Wave 6 is the first slot where render.rs is free.
- Needs: 0701 pass 1 (harness) and its own trial. Needed by: 0498. 0701 lists it under
  "serves" only after 0701.05.01 closes: changing 0701 face 01 earlier would stop its
  close as passed (cmd.rs:848-849).

### 7.3 Lab trial cases (tests/lab_0413.rs in lab 0701, per t425u, t432u)

Each must fail on 0413's start commit and pass on its return.
1. A closed pass prints 05.NN/WORK-ORDER.md with the eight sections in order.
2. Two prints from the same log are byte equal; a hand edit is reported as changed.
3. PACK.md, PROMPT.md, AGENTS.md, BUILDER-PROMPT.md, RETURN-TEMPLATE.md are unchanged
   and agents_hash and prompt_hash still hold.
4. A page made by the old wf, with no WORK-ORDER.md, still takes commands; the next
   write prints it; no log entry is added by printing.
5. The return section shows the recorded text, its entry number and hash, commit and
   file.
6. A draft with "words:" prints it first; without one, "words: not quoted; grant ref
   only".
7. Notes: a face 06 note between the previous close and this close is listed; one from
   another window is not; a later "on 05.01:" note is listed under later notes.
8. A packed, unclaimed pass shows sections 3-7 as "not yet".
9. A refused return is listed under notes.

## 8. Question for Matthew (one)

Q14. How does a work order start with your words?
- Proposed: (default) Prime quotes your exact words in the work order, with the file,
  line and commit they come from, once, when the pass is drafted. Other options: a link
  only (file, line and hash, no quote), which needs the build repo to read; or wf copies
  the whole words file into the log.
- Why: t436u says it "starts with my words". Today only a ref like "t413u" is stored, and
  your words files are in the build repo, not in wf-run, so 05.01 cannot show them.
- Axioms: 2 Fractal (Axioms.md:15) PASS for the default: a short quote with its cite, as
  every design file already does (RELEASE-CHECK.md:31-32); the whole-file copy fails it.
  8 Connection (:27) PASS: the cite is the written link. 6 (:23) PASS: once packed, the
  quote is locked.

## v2 (2026-11-19, 2:30 PM EST, Designer): the builder field (t439u)

Additions only; sections 1-8 stand as written (Axioms.md:23). 54b77af was reviewed and
pushed by Prima. 0413's face 01 changes stay on hold until 0701.05.01 closes. Q14 is
with Matthew.

### v2.1 Matthew's words (docs/review/DIRECTOR-WORDS-t439u.md:5-14, at 79400f9), quoted exactly

"For your next builder prompt, I need you to include which builder we are using.
Currently we have
Cursor-1: Localized on my pc in the wf-run/
Cursor-C: Our cloud cursor you run
Codex: Codex on my computer no setup down
Claude: Claude on my computer no setup
Grok-1: Grok builder not setup
Grok-2: 2nd grok builder not setup."

Where the relay differs: the six names match the file. The file's own line :16
("Effect: every builder prompt starts with a "Builder: <name>" line") is Prima's
reading, not his words. "Filled by Prime at pack, locks at pack" is Prima's proposal;
his words ask only that the builder prompt names the builder. Only Cursor-1 and
Cursor-C are set up; Codex reads "no setup down", Claude "no setup", Grok-1 and Grok-2
"not setup" (:11-14).

### v2.2 The field (frame section, 4.2)

| Field | Filled by | Locks at | Proof | Today's home |
|---|---|---|---|---|
| builder: one of Cursor-1, Cursor-C, Codex, Claude, Grok-1, Grok-2 (t439u.md:9-14) | Prime | pack | until wf prints it: the draft entry, which cannot be redrafted once packed (cmd.rs:276, tail must be draft); after the wf change: inside pack_text, so pack_hash (cmd.rs:403) | GAP: nowhere |

Where it lives today (c09fa60c): nowhere.
- PROMPT.md: "wf claim {{addr}} {{nn}} --as <your-name>" (templates/prompt.txt:4,
  templates/v3/prompt.txt:4), a blank for the builder to fill.
- BUILDER-PROMPT.md: '$env:WF_AS = "<your builder name>"' (templates/v3/builder.txt:21),
  also a blank.
- Draft fields: there is no builder key. draft stores any key (fields(), cmd.rs:147-160;
  stored at :304), so "builder: Cursor-1" in a draft file is kept in the log, but pack
  does not print it: the pack fill list has no builder (cmd.rs:393-399).
- The claim entry records the claimant only as the entry's actor (cmd.rs:443).
Until wf prints it, Prima meets t439u by hand: a "builder:" line in the draft file and
"Builder: <name>" as the first line of the prompt she pastes. 0413's view can show the
draft field (render only).

### v2.3 Claimant differs from the named builder: raise, not refuse

The files settle it:
- decisions.md:570 (E4, settled): "Every piece of work has a lead: named on it, or the
  default set by its band or pack. Another may do the work, but raises it before moving
  forward."
- workflow-loop.003.md:172 (draft): "atomic first valid claim wins. ... Record the E4
  raise before work if the builder differs from the lead."
- wf today: first claim wins (cmd.rs:439-440); only the claim holder may return
  (cmd.rs:488); the builder may not check its own work (cmd.rs:730, :778).
So: a claim by a name other than builder: is taken, and wf records the raise in the same
step, as an elevate entry to Prime ("claimed by X; the pack names Y"), the same shape as
the elevate for a job not done (cmd.rs:522-527). Prime sees it before signoff. A claim
by the named builder adds nothing. No new question: E4 is settled, and the raise is the
fractal answer (the same rule at the lead level and the builder level, Axioms.md:15).
Honest limit: --as and WF_AS are self-stated, so the check catches mistakes, not
pretenders (door open, not proof; t434.md:28).

### v2.4 Which page carries the wf change

Not 0413: it is render-only (section 7.2), and this needs pack and claim in src/cmd.rs
and the prompt templates. Not 0404 either: one page, one job (t249u.md:9), and 0404 is
the design review line. A new page:
- 90.50.10.0414 "the work order names its builder; claim raises a different one". 0414
  is the next slot after 0413, never planned in this book (0405, 0410, 0497 stay unused;
  DIRECTOR-RULINGS.md:129-130).
- May touch: src/cmd.rs (pack prints builder, claim adds the raise), src/render.rs and
  templates for PROMPT.md and BUILDER-PROMPT.md ("Builder: <name>" first, and the --as
  value filled in). Template version: after 0404 it is v4, so 0414 edits v4 rather than
  adding a version (render.rs:29).
- Size 1/2/3; trial in lab 0701 (tests/lab_0414.rs) 1/1/2.
- Place: in the src/cmd.rs queue, after 0412 and before 0498 (waves 14-15), so 0498 moves
  to 16-17: 17 waves. Not added to the stage plan in this note; it goes in as section 15
  when Prima agrees.
- Trial cases: a pack with builder: prints it first in PROMPT.md and BUILDER-PROMPT.md and
  in pack_text; a pack with a name not in the list is refused; a claim by the named
  builder adds no elevate; a claim by another name is taken and adds one elevate naming
  both; a pack with no builder: still packs (old drafts) and prints "builder: not named".

### v2.5 Axioms and mini release check (RELEASE-CHECK.md @ c0e5b22)

| Item | Source file:line | Seen in v2 | Result |
|---|---|---|---|
| 1 Authority | Axioms.md:13 | Prime names the builder in the frame; the claim does not overrule it, it raises | PASS |
| 3 Leads | Axioms.md:17; decisions.md:570 | builder named on the work; another raises before moving | PASS |
| 5 Frame | Axioms.md:21 | the frame now says who builds | PASS |
| 6 Lineage | Axioms.md:23 | locked at pack; a change is a new pass, not an edit | PASS |
| 2 Fractal | Axioms.md:15 | same raise rule as E4 | PASS |
| 7 Missing | Axioms.md:25 | "builder: not named" printed, not guessed | PASS |
| 9 Trial | Axioms.md:29 | trials in lab 0701; no hostile pass yet | TENSION |
| Quote exact | t439u.md:5-14 | v2.1 | PASS |
| A1-A9 on 90.50.10.0414 | t413u.md:7, :9; seqAddr.md:240-242 | page 0414 on PP01-PP98 | PASS |
| H1 habit: "refuse a wrong claimant" | decisions.md:570 | traced; the files say raise | PASS |
| ASCII, plain words | DIRECTOR-RULINGS.md:16 | file | PASS |

Verdict: no FAIL. Tensions: self-stated names; four of the six builders are not set up
(t439u.md:11-14); 0414 adds two waves; no hostile pass yet.

v-note (2026-11-19, 2:30 PM EST, Designer): Q14 is answered, not with Matthew: docs/review/DIRECTOR-WORDS-t440.md:7 "Quote my exact words once, with file, line and commit" (227933e). The default stands: Prime quotes his words once in the draft words: field, with file, line and commit. The "Q14 is with Matthew" line in v2 above was written before I saw 227933e.
