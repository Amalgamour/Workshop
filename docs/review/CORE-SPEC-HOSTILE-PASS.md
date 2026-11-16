# CORE-AND-TOOLS-SPEC: hostile pass

WORKING PATH. Hostile pass by Tester (Grok Bot). Not a ruling.
author: Tester
Tested: docs/design/CORE-AND-TOOLS-SPEC.md at bcd5aac.
Code read at HEAD bcd5aac (same code as 341a63f and 26a17be).
No code changed since: R33 fixes 5e63ad8, d85d4f8, a150d03 are
already in.
Live tests ran in scratch copies only (/tmp/ctrial, /tmp/live).
Every server I started was stopped.
Matthew decides. Picks here are my working path, not rulings.

## Verdict

Holds with fixes.
The plan is sound. Some "today" lines are too kind to the code.
Three claims about today's code are wrong (see Top findings).

## Top findings

1. The door is more open than B1 says.
   - A line I wrote straight into the book, signed "director",
     loaded at the next start with no warning. (store.rs:270-284)
   - The token file sits in the same folder as the books
     (store.rs:297, identity.rs:3). Anyone who can write books/
     can add a director token. B1 does not say this.
   - A line I appended while the compute ran was cut with no
     report at the next write. (store.rs:950-951)
   - A same-length edit to an old line ("Retry." to "HACKD.")
     was served as the seated face after a restart.
2. A lost reply can double a change today.
   - I sent the same `note` twice, as a retry would. Both were
     booked: entries 19 and 20, same body.
   - The write still books if the client has gone:
     the reply send is ignored (lib.rs:66).
   - A retried create is refused 422 ("put never replaces"),
     so the caller cannot tell "booked" from "refused".
   - B6 "EXISTS TODAY" does not say any of this.
3. The write gate does not check titles.
   - B9 says Elevate "is used for a title mismatch" and the gate
     maps it to 409 (store.rs:894).
   - On /propose I retired page 10.11.21.0501 with the address
     title "wrongtitle"; the stamp says "retry". It was booked
     (entry 25). No elevate.
   - The title check runs on reads only (store.rs:364,
     resolve.rs:293-305). validate.rs:297 checks only the
     title's shape.
4. A refused book reads as "missing", and the gate forgets it.
   - Damaged 10.11.21.book was refused at start. /face answered
     404 "not found in book, shelf, desk or kernel".
     R37 item 6 says "couldn't look" is not "isn't there"
     [DIRECTOR-RULINGS.md:200].
   - A director put to that book's door passed every check.
     Only the file-exists guard stopped it: 500
     "File exists" (log.rs:418, create_new).
5. Queue ids can repeat after a crash.
   - `.queue` is written after the book, with no fsync, and a
     failed write is ignored (store.rs:745-749).
   - Ids come back from `.queue` at start (store.rs:999-1015).
   - I deleted the last `.queue` line (what a power cut can
     do) and restarted: id q8 was used twice.
   - B1 says ids "never repeat after a restart". Not true.
6. Part A says more than the rulings do.
   - Line 60: "This order is your ruling (R35)" for every
     change. R35 was given for the copy check
     [DIRECTOR-RULINGS.md:177]. The spec's own Differences
     item 4 (line 171) says the wider use is NEW.
   - Line 80: menus for every read. K3 is still open.
   - B4 line 271: "Copy-check steps get lines (Q8)". Q8 is open
     [SECTIONS-AND-CARDS.md:246]. B9, T6 and T7 assume it too.

## 1. Cite check (point table and Parts B-D)

Code cites opened: 105.
- OK: 100.
- WRONG LINE: 1.
- WRONG CLAIM: 4.
Doc cites sampled: 112 (rulings, axioms, plans, reviews).
- OK: 111. WRONG CLAIM: 1.

WRONG LINE
- kernel/build.mjs:20-22 (B1, T13). Those are comments.
  The refusal to write into books/ is build.mjs:842.

WRONG CLAIM
- store.rs:735-753 (B1): "ids never repeat after a restart".
  See finding 5.
- store.rs:894 with resolve.rs:304-305 (B9, Part D):
  title mismatch is not elevated on writes. See finding 3.
- resolve.rs:292-305 (B8): "a mismatch is elevated". True on
  reads only. See finding 3.
- store.rs:270-284 (B1, B11): true as cited, but B11 leaves out
  that a refused book is treated as absent. See finding 4.
- OUR-CODE-VS-CURSOR-LESSONS.md:226-227 (T13): says the typed
  time "goes away with Tester's Q3". The source says Q1. Q1 has
  shipped (5e63ad8) and the typed time is still there
  (build.mjs:36). It now reaches export/ only.

Incomplete, not wrong
- log.rs:282-300 (B6, Part D) covers the torn last line.
  The all-or-nothing drop of a cut multi-op group is
  log.rs:324-333. Cite both.
- Point 10: "421, 415, 401 happen before any token check".
  The 401 is the token check (lib.rs:86-97).

Point table rows 1-14: all hold on the code except where
noted above. Test count claim holds: I got 418 passed,
0 failed, 2 ignored (cargo test --workspace --offline,
bcd5aac, scratch copy). Kernel builder tests: all passed.

## 2. B6 crash table

What I ran (scratch /tmp/live, compute built from bcd5aac):
- T1 torn tail: kill -9, add half a line, restart.
  Result: "partly written last line was dropped"; the next
  write cut it. Bytes are not kept anywhere.
- T2 direct append while running: cut at the next write,
  no report (store.rs:950-951).
- T3 same-length edit: served after restart.
- T4 direct append before start: loaded as real.
- T5 lost `.queue` line: queue id reused.
- T6 wrong title on /propose: booked.
- T7 damaged book: reads say "missing".
- T8 write into a refused book: passes the rules, 500 at
  file create.
- Retry: same `note` twice, booked twice.
- The suite's kill -9 test passed
  (held_kill9_mid_append_keeps_every_acknowledged_proposal_whole).

Power cut after each step
- Not tested. kill -9 is not a power cut, as the spec says.
- Today, by reading:
  - Book appends are safe: sync_data before OK (store.rs:972).
  - A new book file is synced, its folder is not
    (log.rs:422, store.rs:936-937). An acked first write can
    vanish with the file.
  - `.queue` is never synced (finding 5).
- Planned table, by reading. Rows 0-4b fit "book line is the
  commit". Gaps:
  - Folder fsync is proposed for create only (B3). Step 3
    (new view file) and boot's "move aside" are renames.
    They need a folder fsync too, or a second crash can bring
    the moved piece back.
  - All sections share one face 04 file
    [SECTIONS-AND-CARDS.md:111]. "Move the piece aside" is
    then a cut of a shared file. Say it is copy-then-cut, at
    start-up only [SEQ-FILE-PLAN.md:592].
  - A write across pages: "a tail out of write order" means
    damage, but files have no shared order. Say how boot finds
    order: the book line's chain heads per page
    [SEQ-FILE-PLAN.md:553] are enough. Use them, not order.
  - A direct writer that adds a piece and a 09 line, no book
    line, is "unfinished": set aside, no halt. That is fine,
    but it should raise, not only journal.

Lost reply (client never hears, retries)
- Today: fails. Measured doubling (finding 2).
- Planned (row 4b, K4): works only if the delivery-id check
  runs before the rules, and the id index is rebuilt at
  start from the face 09 lines. Say both.

Missing folder fsync
- Today: real gap on new book files and new folders. Read,
  not tested (needs a power cut).
- Planned: see the rename gap above.

## 3. B16 read path

- Steps 1-3 marked EXISTS: true (lib.rs:202-210, ask lib.rs:6-14,
  :83, :278).
- Nothing marked EXISTS is missing.
- Step 4 (pages for a key word) marked PLANNED only. Parts exist:
  /brands maps a word to card addresses (store.rs:624) and /cards
  finds cards by title in every book (store.rs:701). Name them.
- Step 8 marked NEW: right. Today it says "missing" (T7).
Errors: 0 false EXISTS, 1 under-credit (step 4).

## 4. Closed questions and assumed rulings

- Part A:60 and the A2 picture: R35 order for every change.
  Assumed. Ask it (it is K10's scope).
- Part A:80: menus for every read. K3 open.
- B4:271, B9, T6, T7: copy-check lines on face 09. Q8 open.
- T6 "Refuses": "a `source:` line naming another page's card".
  R35 item 3 is held 7 [DIRECTOR-RULINGS.md:182].
- B14: journal "stored as small files", "chained like face 09".
  Part of K1's answer, written as design. Mark it NEW.
- R33 fix 2: not built, not claimed. R35 item 1 later says
  "the proposal stands" [DIRECTOR-RULINGS.md:178], so B2's
  PLANNED copy refusal is backed.
- R28 and R29 holds: R29's hold is closed by R31 item 10
  [DIRECTOR-RULINGS.md:148]. R28's "no log in 00" is answered by
  R31 item 9 [DIRECTOR-RULINGS.md:146]; where the note goes is
  still held (C24). The spec handles both right.
- Not asked anywhere: R37 item 1, "One append-only log is the
  only source of truth" [DIRECTOR-RULINGS.md:195]. The spec has
  per-page 09 logs, band and book lines, a journal and a
  recovery folder. Which is the one log? See Q-A below.

## 5. Claim lines: axioms and Better

"Axioms (claim, 9)" lines: 33, with 89 pass marks.
I tested the 26 marks the code can check now.
- Backed: 10. A2 ax8 (gate order, lib.rs:184-192 then
  store.rs:851-913); B2 ax1 and ax8 (token names writer,
  lib.rs:85-97); B13 ax1, ax6, ax8 (seqpage lib.rs:1-7,
  build.mjs:842); T2 ax7 (resolve.rs:140); T4 ax7
  (askq.rs:84-98); T10 ax1 (seqpage.rs:1-3); T13 ax1
  (build.mjs:842).
- Knocked for today's code: 10.
  - A2 ax6 "nothing is rewritten": T3.
  - B1 ax1 "Compute enforces it": T4, token file.
  - B1 ax6 "cannot erase another's lines": T2.
  - B2 ax9 "seating needs a hostile trial": the check is a
    typed name in any docs/trial file (store.rs:818-825).
  - B6 ax1 "an outside change is refused and raised": T2, T4.
  - B8 ax1 "a mismatch is raised": T6.
  - B11 ax7 "a required absence is reported": T7.
  - B11 ax1 "no writes before the record is checked": T8.
  - B16 ax7 and T1 ax1: T7, T4.
  These may pass once B1's lock is built. Today they fail.
- Should be tension, not pass: 6.
  - B6 ax6 and K9 ax6: moving tail bytes out of append-only
    files is a cut, even if never booked.
  - B3 ax6: step 3 replaces the view file.
  - B4 ax1: the compute picks "unfinished" over "damage"
    without a halt; axiom 1 says "Do not choose" [Axioms.md:13].
  - B9 ax9: rests on Q7, which is open.
  - B10 ax2: a stored menu is a copy until K12 is answered.
- The other 63 are design claims. They stay `9`.

"Better (claim, 9)" lines: 33.
- Backed by code or a run: 9 (A2, B5, B11, B13, B14, T2, T4,
  T10, T13).
- Partly: 2. B2 (no CORS: lib.rs:9; receipt is planned).
  T1 (true through the gate, false through files: T4).
- Knocked: 3.
  - B1: "one writer" is not true today.
  - B6: "never less safe" than today. Untested, more states.
  - B9: "most end at the compute". No count exists.
- Comparisons with a cited source, no measure: 19.

## 6. K8-K15: my answers

Recommendations, not rulings. t189u form.

K8. Build order
1. Question: build the first proof on today's book file first?
2. Answer: yes, but widen step 1. Close the door fully first:
   move the token file out of books/, OS account, refuse not
   cut, fsync `.queue` and new folders. Add delivery ids in
   step 2, since retries double today.
3. Why: the proof is worthless if a file write can fake it (T4).
   Hurt: anyone trusting a proof log a shell could edit.
4. Axioms: 1 :13 pass; 9 :29 pass; 2 :15 tension (derived 09
   now, stored 09 later); 6 :23 pass.
Option not listed: run Part F twice, once now and once after
the storage move, with the same script, and diff the logs.

K9. After a crash: set aside or finish?
1. Question: an unfinished change at start-up: set aside?
2. Answer: set aside, as proposed. Copy to recovery, then cut,
   folder fsync, then raise once. A retry with the same id gets
   "not booked".
3. Why: the caller was never told "booked". Hurt: a reader who
   sees a change nobody confirmed.
4. Axioms: 6 :23 tension (a cut, though never booked); 1 :13
   pass; 7 :25 pass; 9 :29 tension (untried).
Option not listed: keep it as a waiting draft (R5) the person
can take in. Nothing is lost and nothing is decided.

K10. What may a model settle?
1. Question: listed case types only? May a model say yes?
2. Answer: listed types only. For now a model may refuse or
   hand back, not allow. Allow comes later, per type, after Q7
   is answered and a measured wrong-allow count exists.
3. Why: R33 item 1, "Models can be wrong" [DIRECTOR-RULINGS.md:159].
   A wrong no is a retry. A wrong yes changes a page. Hurt: the
   page owner.
4. Axioms: 1 :13 pass; 9 :29 pass; 3 :17 tension (more goes to
   the person).
Option not listed: a model "allow" seats, but a person sees a
daily list of model allows and can undo by a new step.

K11. Does every proposal name its base?
1. Question: carry the base version on every proposal?
2. Answer: yes. Start now with the page's last entry number,
   which exists today (log entry `n`). Add the fingerprint
   when B5 lands.
3. Why: today a waiting draft has no base
   (validate.rs:16-43). Hurt: whoever's newer edit is buried.
4. Axioms: 6 :23 pass; 8 :27 pass; 7 :25 pass.
Option not listed: allow "no base" only for pure appends, such
as a note, where order does not matter.

K12. Menu stored or worked out?
1. Question: store the face 03 menu, or derive it?
2. Answer: derive it from the page index, as proposed.
3. Why: no second copy to drift. Hurt: a model that trusts a
   stale menu.
4. Axioms: 8 :27 pass; 2 :15 pass; 1 :13 tension (R35's Read
   says "face 03 menu" [DIRECTOR-RULINGS.md:180]).
Option not listed: store it as a cache that is checked on
every open and never trusted over the log, like a snapshot.

K13. Who may write an R2 trial?
1. Question: may the same model, under another name, trial?
2. Answer: no. Different token and different model. Record the
   trial file's git blob in the seat line.
3. Why: today the author is a typed line in any docs/trial file
   (store.rs:818-825). Hurt: everyone downstream of a weak seat.
4. Axioms: 9 :29 pass; 1 :13 pass; 6 :23 pass.
Option not listed: the trial itself goes through the gate, so
its author comes from a token, not from typed text.

K14. Record relays word for word?
1. Question: record each relayed instruction before passing it?
2. Answer: yes, as 341a63f did. Add the turn id and time.
3. Why: a summary drifts. Hurt: you, when work rests on words
   you did not say.
4. Axioms: 6 :23 pass; 4 :19 pass; 1 :13 pass.
Option not listed: the relaying agent quotes the file and
line in every brief, so a missing record shows at once.

K15. Keep the Better lines?
1. Question: keep or drop them?
2. Answer: keep only those that cite code or a run (9 of 33,
   plus 2 partly). Turn the 19 comparisons into one short
   "Compared with" list. Drop the 3 knocked.
3. Why: a claim read as a result misleads. Hurt: a reader who
   takes an opinion as a test.
4. Axioms: 9 :29 pass; 4 :19 pass; 2 :15 pass (less repeat).
Option not listed: mark each Better line "measured" or
"compared", like EXISTS and PLANNED.

## Questions for Matthew

Q-A. Which log is the one source of truth?
1. Question: R37 item 1 says one log is the only truth. The plan
   has page logs, book lines and a journal. Which one is it?
2. Answer: the book's chained lines, with each page's 09 lines
   tied into that chain. The journal and index are views.
3. Why: a fresh start must rebuild from one place
   [DIRECTOR-RULINGS.md:195]. Hurt: a rebuild that picks the
   wrong record.
4. Axioms: 1 :13 pass; 2 :15 pass; 6 :23 pass; 8 :27 pass.

## Fixes to ask Designer for

- B1: add the token file in books/ and T4's loaded forgery.
- B1: fix "ids never repeat" (finding 5).
- B6: add today's lost-reply doubling; add rename fsync;
  replace "write order" with chain heads.
- B8, B9, Part D: title check is reads only (finding 3).
- B11: refused book reads "missing"; writes ignore it.
- B16: name /brands and /cards under step 4.
- Part A:60, :80, B4:271: mark as NEW or open (K10, K3, Q8).
- build.mjs:20-22 to :842; T13 "Q3" to "Q1".
- Retag the 10 knocked and 6 tension axiom marks.

## Not checked

- Power cuts (needs a VM that hard-resets).
- Writes across several books at once.
- app/ (not read this pass).
- Doc cites not in the 112 sampled.
- The planned layout itself: there is no code for it.
- Whether a retired page should need approval (seen in T6:
  any writer token retired it). Out of scope here.
