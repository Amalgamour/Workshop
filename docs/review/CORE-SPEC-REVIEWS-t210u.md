# Reviews of CORE-AND-TOOLS-SPEC.md, relayed verbatim by Matthew (t210u, Mon 16 Nov 2026, 1:36 PM EST)

## Review 1: Codex (second reviewer)

prima,
I’m Codex, the OpenAI coding agent Matthew works with in his local Workshop checkout. I’m a second reviewer on this pass. I read your full `CORE-AND-TOOLS-SPEC.md` and checked it against the SeqAddr grammar, book format, and kernel design in Matthew’s checkout. That checkout didn’t contain your `26a17be` commit, so my review covers the architecture and the draft’s stated implementation status. The runtime claims still need verification against your build.
My opinion is that this is a coherent architecture and a good basis for the first prototype. You took Matthew’s split between person, model, and compute and made it concrete in the write gate, the tools, and the records each produces. I’d build from it and keep the storage protocol in draft while testing interrupted writes.
My favorite decision is that links follow the live page and reviews bind to the version they read. A link about Jim can keep working as the record grows. A reviewer’s judgment remains tied to the evidence they saw. Showing pending work alongside the live version also lets the next model pick up an unfinished change without mistaking it for an accepted one.
I agree with K1. Keep the operational journal outside the books and link its entries to Face 09 where relevant. Face 09 should answer what changed on the page, who changed it, and why. The journal should trace what compute attempted, refused, or elevated.
I’d focus the next pass on two things.
Specify recovery at each step in B6. If the new Face 04 view reaches disk before the book line commits and compute stops, every reader should see the previous committed page after restart. Spell out which records prove the commit, how compute rebuilds the view, and how it distinguishes an interrupted write from damage. Test an interruption after each write step. Also test the case where the commit succeeds and the reply is lost. Retrying the same delivery ID and content must return the original committed result without adding a second change. That means the delivery ID and receipt must be recoverable from the commit.
Define the scope of delegated model judgment in B9. R35 came from the copy-check discussion. I’d start with explicitly delegated copy-check cases. Record the proposal, the comparison text, the governing rule, and the model’s reason. Before booking the decision, have compute verify that the proposal and the evidence still match what was reviewed and that the delegation covers the case. A second model’s agreement strengthens the judgment. The delegation gives it authority to affect live state.
I’d keep Part F’s one edit, one review, one restart as the first build. Add the interrupted-write and lost-reply cases. At the end, have someone use the records alone to reconstruct what was proposed, why it changed, exactly what the reviewer saw, and what survived the restart. That’s the proof I’d want Matthew to be able to inspect for himself.

## Review 2: revision brief (reviewer had no access to crates/ or docs/)

You are revising CORE-AND-TOOLS-SPEC.md (draft of Mon 16 Nov 2026). An outside reviewer read the whole spec but had no access to crates/ or docs/, so every point below is a design concern, not a verified defect. Your first job on each point is to check it against the code and the source files and say whether it holds.

Rules for this revision
- Keep the spec's own conventions: EXISTS TODAY / PLANNED / NEW (proposal), file:line citations, `7` for open, `9` for untried.
- Change the lines that need changing. Do not rewrite the spec from memory. Add a dated change note at the top saying what changed and why.
- You propose; the Director decides. Do not close an open question or number a ruling. Where a point needs his decision, write it as a question in the four-part form used in Part E.
- If a point is wrong, say so and cite the line that shows it. Do not accept a point just because it was raised.
- Keep Part A readable by a person. New detail goes in Part B onward.

Points to address, most important first

1. Crash recovery for the multi-file write (B3, B4, B6).
Today one write is one append and one fsync. The plan is four or five writes across face file, face 09, page index, band line and book line, with the book line as the commit point. The spec does not say:
- what happens at boot to a face piece or a face 09 line whose book line never landed, given that face 09 is append-only and "nothing old is ever rewritten";
- how the compute tells an incomplete last write from a real disagreement. B4 says any disagreement between face 09, the index and the "last change" note halts the compute. A crash between steps 2 and 4 produces that disagreement, so as written every crash halts;
- whether directory entries are fsynced when a new face file or page folder is created.
Write the recovery rule step by step: for a crash after each of steps 0 to 4, what is on disk, what boot does, and what the caller was told. Mark power loss as `9` until it is tested, and say what test would remove the mark.

2. A model can allow a write (B9, T7, the A2 picture).
A "highly sure" model answer books the change. "Highly sure" is the model reporting on itself, and R33, 1 records that models can be wrong. Address:
- whether the model rung should be limited to refuse and hand back, with allow permitted only for named, low-stakes case types. List the case types and say which rung may settle each;
- that the judging model must not be the proposing model, and how the compute checks this from tokens;
- that a model's decision makes the gate non-deterministic. The decision must be logged as an input, so a replay reproduces the result without asking a model again;
- what "a second hostile pass agrees" means in Q7 if both passes are the same model.

3. A waiting draft has no base version (B9, B15, K6).
K6 lets an elevated draft wait with no time limit. If the page changes while it waits, a later approval books a change made against old text. Propose that every proposal carries the fingerprint it was based on, and that a waiting draft whose base has moved goes stale and is handed back, the same way a review goes stale (R37, 4). Also state plainly that a waiting draft never blocks the single write queue.

4. Until the OS account and file lock exist, the gate is optional (B1).
Any process with a shell on the box can write the stored files directly. That is the fault the spec holds against Brand Clerk ("the gate only works if the model calls it"). Say so in B1 and in Part D, and say what detects a direct write today and what will prevent it. Since the chain hash has no secret, say what stops a process that can write files from also rewriting the chain. Propose where this sits in the build order and why.

5. The read side is thin (B10, T3, T4, Q9).
How a key word finds its pages is still open, and it is the centre of the read path. Add a section that follows one model query from start to finish, the way A2 follows one write: the query arrives, words are resolved, pages are found, menus are served, sections are requested, coverage is reported. Mark each step EXISTS, PLANNED or NEW. If holding a model on task and checking its return for drift is out of scope for this spec, say so in the "does not" line and name where it will be designed.

6. The spec grades itself.
Every section ends with "Axioms: pass" and "Better than", written by the designer about its own design. By axiom 9 that is not a trial. Relabel the axiom lines as claims awaiting a hostile pass, and name who will make that pass. Remove the "Better" lines, or keep only those that cite a measured result. Keep a "tension" line wherever one exists.

Smaller points

7. Clock check (B2 item 6, B11). A line dated earlier than the line above makes the book refused at boot. One backwards correction of the system clock could lock a book. Say what the compute does when its own clock steps back, and whether that should halt and raise instead of producing a line that later fails.

8. ASCII only (B2 item 7, T4, T10). Face 04 is the face people read and edit. Accented names and curly quotes are refused. Cite the ruling this rests on. If there is none, ask it as a question.

9. Menu stored on face 03 (B10). A derived menu rebuilt after every write means each write causes a second write, and a stored copy that can disagree with its source. Say whether that second write gets a face 09 line and enters the chain. Compare with keeping the menu in the page index, which is already derived and rebuildable.

10. Journal floor (B14, K2). "Every refusal" at the minimum level lets a faulty or hostile client fill the disk with 421 and 415 refusals. Propose how refusals made before identity is known are counted or summarised without losing the floor.

11. The `build-stage (R2)` seat path (B2 item 4). It seats a face without the Director's token if a hostile trial exists. Say who checks that the trial happened, what record proves it, and whether the trial may come from the same model that made the change.

12. Delivery id (K4). Say how long ids are kept, whether an id is scoped to one token, and what a retry gets after the record of the first answer is gone.

13. Names and records. The spec calls the Director "Matthew". Check this against the rulings file and the repository's commit author, and correct it wherever it is wrong. Difference 1 shows the request for this spec was never recorded in his own words. Propose how a relayed instruction is recorded verbatim before it is passed on.

14. Divergence from the Workshop design files. This build makes face 09 the page log, allows face 03 menus on any page, and stores a book as small files. The Workshop seqAddr.md and format.md say otherwise (face 09 unassigned, face 03 restricted, one append-only file per book). List each divergence with the ruling that authorises it, so the older files can be updated or marked superseded.

Build order to assess (a proposal, not a decision)
The reviewer suggests running the Part F proof on today's one-file log, with face 09 produced as a derived view, and treating the storage migration as a separate step that starts only after point 1 is written and a power-cut test exists. Give your reasons for or against, with what each order risks.

What to return
- The revised spec, changed in place, with the dated change note.
- A short table: each point above, whether it held when checked against the code (yes, no, partly), the citation, and what you changed.
- The new questions for the Director, top three first.
