# plan.5 stages

Authorization: draft — 2026-10-15
who: claude-opus-5-5
state: draft
page: 1008.app-plan
why: The order of the build. Each stage ends in something you can use and a project that still works.

## Units
A **batch** is one released round of work: your replies on a `05.NN`, the work, the report, your review. As a rough guide, a batch is 1 to 3 hours of model work and 15 to 45 minutes of your reading. The ranges below count batches, not days. They widen where a stage depends on an open decision or on something new to this project (the screen library, Windows file locking, packaging). No stage has a date.

## The common gate
Every stage passes these before the next starts:
- All app tests pass, and the run is shown in the report.
- `lcheck.py` on kernel.draft gives the same counts as before the stage.
- `git status` shows only the files the stage's batch lines name.
- You ran the demo yourself.
- The stage's work branch has one commit per closed line, and you merged it into `main`. The merge is the stage's restore point.

**Recovery, any stage:** the app lives in `app/` and `.librarian/`. To undo a stage before it is merged, do not merge its branch. After it is merged, revert the merge. App writes into the tree are batch lines, replies, status lines and new pages, each with a before-copy in the journal, and each is also in git.

## Stage 1 — See the work (read-only)
- **Outcome:** `librarian items` lists every batch line on the tree that needs you: stopped first, then waiting, then solo work to review, grouped by page and batch. `librarian item <page> <batch> <NN>` prints one line in full. `librarian show <page> <face>` prints a face with a clean header. Nothing is written.
- **Modules:** place, tree, face, batches (read), commands.
- **Prerequisites:** `05.01` #01, #04; `05.02` #01, #02 answered.
- **Batches:** 2 to 3. (1) setup, `place`, `tree`, test fixture. (2) `face`, batch reading, commands. (3, if needed) fixes from the real tree.
- **Tests:** name table; fixture tree with every batch name form, each command in the list plus one that is not, a `>stop` line, solo work under a grant, and a carry chain; a read-only run over the real tree that proves no file changed; counts against five batches counted by hand.
- **Your demo:** run `librarian items`. Find `2003.reference 05.01` with 3 waiting. Run `librarian item 2003.reference 05.01 02` and compare it with the file.
- **Gate:** the five hand counts match; no tree file changed.
- **Uncertainty:** low. The parsing rules exist in `jobs.py`. The unknown is how many odd files the real tree holds.

## Stage 2 — Answer (your side of the loop)
- **Outcome:** `librarian reply` takes your text, runs every check in plan.4, writes it, and shows the result. `librarian undo` reverses the last app write. You can do your real batch work without opening raw files.
- **Modules:** write, batches (reply), commands.
- **Prerequisites:** stage 1; `05.01` #05, #06, #12.
- **Batches:** 2 to 3. (1) `write` with journal and refusals. (2) reply and undo. (3, if needed) Windows lock handling.
- **Tests:** each refusal in plan.4 has a failing case; only the reply bytes change; CRLF and LF files keep their endings; a change between read and write is refused; undo restores the exact bytes; `reply` refuses when not at an interactive terminal.
- **Your demo:** `librarian sandbox` makes a practice copy of one batch. Reply there, look, `undo`, look again. Then reply to a real line you want to answer anyway.
- **Gate:** your real reply is in the file and `git diff` shows only that line.
- **Uncertainty:** medium-low. Windows can refuse a swap while an editor holds the file.

## Stage 3 — The work loop (the model side)
- **Outcome:** a model can do your timer example with commands: `page new` in an authorized band, `01` filled, `batch new`, `item add`, `status`, `stop`, and solo work under a grant. `jobs.py` keeps working beside it.
- **Modules:** pages, batches (model writes), write, commands.
- **Prerequisites:** stage 2; `05.02` #03, #05.
- **Batches:** 2 to 4. (1) `batch new`, `item add`, `status`, `stop`. (2) grants by shelf and book, and solo work. (3) `page new`. (4, if needed) agreement with `jobs.py carry` and `ran`.
- **Tests:** a scripted model run on the fixture builds a page, a batch with three jobs, a stop, and two solo statuses; every refusal in plan.4 for these writes; `jobs.py find` and `carry` read the result.
- **Your demo:** ask a model, in a real session, to start a small page in band `2000` the job names, with a batch of three jobs. Read it in `librarian items`. Reply. Watch it report status.
- **Gate:** the model's whole run is visible as batch lines; nothing it changed is outside a line.
- **Uncertainty:** medium. Models must actually use the commands; the first real run will show where the instructions need tightening.

## Stage 4 — The desk screen
- **Outcome:** `librarian` with no arguments opens the full-screen terminal app from plan.2.
- **Modules:** screen.
- **Prerequisites:** stages 1 to 3; `05.01` #03.
- **Batches:** 2 to 4. (1) home and tree. (2) line cards and face view. (3) reply editor and confirm. (4, if needed) keys, colors, your feedback.
- **Tests:** scripted screen runs on the fixture; a reply made in the screen equals the command result byte for byte.
- **Your demo:** the plan.2 session, steps 1 to 6, on real lines.
- **Gate:** you can do a normal day of review in the screen without opening a file by hand.
- **Uncertainty:** medium. It is the first screen in this project and taste matters.

## Stage 5 — Coming back
- **Outcome:** the home screen shows since your last visit, unseen work, uncommitted count, branches waiting to merge, the checker per page, and a warning if one of your replies was altered.
- **Modules:** changes, check.
- **Prerequisites:** stage 4; `05.01` #07; `05.02` #04.
- **Batches:** 2 to 3.
- **Tests:** a scripted worker change appears; a changed file with no batch line is flagged; a hand-edited reply raises the warning; checker counts equal a direct run.
- **Your demo:** reply, let a model work, close the app, reopen it next day.
- **Gate:** the change list matches `git status` and the model's report.
- **Uncertainty:** low to medium (git output on Windows paths).

**After stage 5 the first version is done:** the batch desk, both sides, end to end.

## Stage 6 — Drafts
- **Outcome:** make a draft of a face beside its seat as `FF.VVV.md`, drop or replace one section, see the difference against the seat. One face engine replaces `clerk.py` and solo `face.py`. Notes are carried in full for now.
- **Prerequisites:** `05.02` #06, #07; a decision on whether the app may write drafts in kernel.draft or only in books.
- **Batches:** 3 to 6. Two programs and their tests must be merged.
- **Gate:** the merged engine passes every ported test; retiring the two old programs is your reply.
- **Uncertainty:** medium-high.

## Stage 7 — Seat, and note sweep
- **Outcome:** sign and approve as your acts (rename onto the seat, retire the old seat into `00.retire.09`, law `0021`, `0022`). The note sweep proposes `applied:` marks as a batch, so drafts stop carrying stale notes.
- **Prerequisites:** stage 6; the `built` state (`2004.approve`) if derived faces are involved.
- **Batches:** 3 to 5.
- **Gate:** an approve on a test book matches law `0022` step by step, and undo restores it.
- **Uncertainty:** medium. The highest-risk write, and the law around it is still moving.

## Stage 8 — Windows window
- **Outcome:** the same desk in a Windows desktop window (Qt for Python), started from the Start menu.
- **Prerequisites:** stages 1 to 5 at least.
- **Batches:** 4 to 8, plus packaging (an installer or a single `.exe`), its own uncertainty.
- **Gate:** every screen test passes against the new shell; your demo matches stage 4.

## Later, not ordered
Index and search, batch rename of old files, dispatch to model workers, colab packs and returns, desks from a brief, drift check, promote. Each is listed in plan.3. Each gets its own `#NN` when you want it.
