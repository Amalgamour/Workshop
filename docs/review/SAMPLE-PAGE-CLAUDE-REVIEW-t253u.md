# Claude review of SAMPLE-PAGE, relayed by Matthew (t253u)

Recorded: 2026-11-17 12:16 PM EST. Matthew's words: "I have the response from claude now for you to review as well."
Verbatim review follows.

Prima,

This is a second review of SAMPLE-PAGE.md, written after reading Codex's review. Where I agree with Codex I say so and do not repeat its reasons. Where I add something, I give the line in the sample that shows it. I reviewed the sample as a design; I had no access to the code or the files it cites.

I agree with the one-page direction, and that 05.02 -> 05.03 (blocked, frame widened inside the grant, no trip to the Director) is the strongest part. I agree with using this sample as the first workflow fixture.

How to revise
- Change the lines that need changing. Do not rewrite the page from memory. Add a dated note at the top saying what changed and why.
- Keep every value marked EXAMPLE.
- Where a point needs the Director's decision, write it as a four-part question (question, proposed answer, why, axioms checked) and add it to ONE-PAGE-WORK.md. Do not decide it in the sample.
- If a point below is wrong, say so and show the line that proves it.

A. Points Codex raised that I agree with
1. Partial work (Codex 1). 05.02's w01 passed review but the counter closes `blocked`, so the board loses it. Show the outcome per work card, and say whether w01's commit was accepted, held as a candidate, or discarded.
2. Sign-off bound to exact versions (Codex 2): pack hash, return hash, source commit, review evidence, and what was left unresolved.
3. The worker prompt built from the released pack (Codex 3, and Codex's S4 answer). The prompt box for 05.03 leaves out `may touch`, `must not`, the checks and the grant. A worker given only that box cannot know it may edit src/input.rs, which is the reason 05.03 exists. Every field the commit check enforces must be in the box. Pin the face 01 version the pack used.
4. Separate trial findings (Codex 4). In 07.01, give "never past 30 degrees" and "taps twitch 2 degrees" each their own result, and say what `held` means when one finding is carried forward.
5. What is happening now, at the top (Codex 5): live version, active pass, who holds it, any blocker, the next expected action. It must be a view the compute builds, not a stored copy (W11).
6. A face 09 example (Codex 6): one recorded transition with its references, and how the board and tail feed are derived from it.

B. Points Codex did not raise
7. Face 01 changed with no approval on record. The card is at version 3 and says "rate 3" and "dead zone 50 ms", which came from your decisions D-a and D-b. Its "Done when" line is the acceptance criteria. Nothing shows who approved v2 or v3, and face 06 never mentions the change. Either show an approval line for each version, or ask the Director whether lead decisions inside the grant may update 01, and whether a changed "Done when" always needs his approval.
8. Scope is set in four places: the pack's `may touch`, `must not` and `grant`, and face 01's "Do not touch". Two already differ: 05.01's grant includes src/input.rs but its `may touch` does not. Propose one rule. Mine: the grant is the ceiling (set by the Director); `may touch` is the pack's frame (set by you, checked by the compute to sit inside the grant); `must not` is derived or dropped; face 01 does not hold scope.
9. Who "Prime" is. The Director wrote "Prime signs off"; the sample reads that as Prima and labels it as a reading. In his older Librarian kernel, "prime" was the name of a role. Because this decides who signs off, put it in S1 as an explicit question.
10. Cost is self-reported. 05.01's `cost` line (minutes, tries, tokens, dollars) is tagged [worker]. Under R37, 3 the compute fills every number. Time is already in the tail run; tokens and cost should come from the API record. The worker may add a note about cost, but not the figures.
11. Created or changed. 05.01's `pull` lists src/steer.rs, so the file existed, but the return says "Created: src/steer.rs". Make the return say create or modify, and have the commit check compare that with the pack.
12. Face 02 runs ahead of the code. It says "05.03 adds smoothing" while 05.03 is still open. Say whether face 02 is the design (ahead of the code) or a description of it (behind the code). The drift check means opposite things in each case.
13. Face 08 links by line range. `src/steer.rs:14-18` is wrong after the next edit, and only the first link carries a commit. Give every link its commit, and prefer a function or test name to line numbers.
14. Workers commit to `main`. 05.03 starts from 05.02's commit, so 05.02's work is live before anyone decided its fate (this is point 1 from the other side). Propose one branch per pass, merged when the pass closes with an accepted outcome.
15. The lead reads before the checker. In every tail run you read the return before checker C reviews. Workshop's S10 asks the reviewer to start from the criteria and the artifact, not the builder's summary. Move your read after review, or say why it comes first.
16. The face 00 axioms line. `1, 2, 3, 6, 8, 9` uses commas, which split a chain into separate pieces (E3). If it is a list, say so or use another form.
17. One page replaces the bands. The Workshop workflow draft put design, jobs, labs and build in separate bands (N4, N5, N7, N3). This page holds all of it, with labs on face 07, which seqAddr reserves. Record that O1 supersedes the band map, and say what page type a page holding all of it is (W8).

C. Passes the next sample should show
The Director asked for three passes "to make sure that is configured correctly". This sample shows passed, blocked and in progress. Those are the easy paths. Add, or show in a second sample:
- a review that fails, closed `failed`, with the rework as a new counter that continues from it;
- a return that touched a file outside `may touch`, refused by the commit check, showing what the worker and you are told;
- a blocker outside the grant, raised to the Director, showing what he sees and what waits while he decides.

What to return
- The revised SAMPLE-PAGE.md with its dated change note.
- A table: each point A1-A6 and B7-B17, whether you accept it (yes, no, partly), and what you changed or why not.
- The new questions for the Director, added to ONE-PAGE-WORK.md, top three first.
