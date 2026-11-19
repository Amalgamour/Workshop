# Dev journal: the release hash (AGENTS.md and PROMPT.md)

date: Thu 19 Nov 2026. All times are EST.
written by: Prima builder-b21, for Prima.
the spec (what the code does now): docs/spec/AGENTS-HASH.md. Status: build stage.

## Why this was built

Matthew, t373u (10:57 AM EST, verbatim): "We need to run that bit check thing.  I can't remember the name so it's recorded once a released agents file is done.  So we can confirm it's correct otherwise it's invalid."

Prima's reading: a hash. Designer's Codex pass had found the gap the same morning (C5): the pack pinned
the template only by the label "templates: 2", so `wf verify --fix` could reprint an old AGENTS.md with
new text and not notice.

## What was done, in order

1. Pack now prints AGENTS.md and PROMPT.md from the entry it is about to write and stores their sha256
   as `agents_hash` and `prompt_hash`. Why: the record of what was released has to be written at the
   moment of release, in the log, which is the only truth (axiom 1).
2. Every page load compares the files on disk, and the text this wf would print, with those hashes.
   A mismatch says "AGENTS.md for pass 05.NN is invalid: hash mismatch" and exits 1. Why: his words,
   "otherwise it's invalid".
3. `verify --fix` restores a hand-edited copy (the reprint matches the hash) but refuses, and writes
   nothing, when the reprint would differ. Why: fixing by reprint would rewrite the past.
4. Old pack entries without a hash say "no hash recorded (before t373u)" and still verify. Why: the
   real pages 90.10/90.20/90.30 were released before the rule; failing them would be inventing a fault
   (axiom 7).
5. One older test forged the pack's branch field; that now (rightly) breaks the PROMPT.md hash, so the
   test drops the hash fields to stay a test of escaping in close.

## Tests

Three new e2e tests: a hand-edited AGENTS.md is invalid (and --fix restores the released bytes); a
changed template plus --fix is refused with every page file byte-identical; an old page without a hash
still verifies, and a forged hash field is escaped. The "changed template" case is made by switching the
entry's template label from 2 to 1 after release, so this wf prints different text for it.

## Follow-up: reuse when nothing changed (t378u)

Matthew, t378u (11:07 AM EST, verbatim): "So once a agents.md is released it can't be changed correct?  Well that is a good thing.  If a new agents.md is required a new one is printed then hashed.  agents.md should be replacable on each pass of the WF loop if it's needed.  Although if no change is required the existing should stay."

1. Found first: the v2 AGENTS.md names its own pass and pack hash and lists the jobs, so two passes
   never print the same bytes. Reuse would never happen. Why that matters: his "the existing should
   stay" would be a rule that never fires.
2. So a v3 template: AGENTS.md holds only the page and kit parts (goal, done-when, pinned sources,
   rules, checker notes). The job stays in PROMPT.md, which already had all of it. Old v1/v2 entries
   print exactly as before, so no released file changes (t373u still holds).
3. At pack, if the new AGENTS.md text hashes the same as the latest released one, no copy is printed;
   the entry records `agents_from` and the hash. If it differs, a new file is printed and hashed.
   Why: his words, "a new one is printed then hashed" only "if it's needed".
4. v3 PROMPT.md names the AGENTS.md path and hash, so a worker reads the right file. A hand edit of the
   shared file is invalid for every pass that uses it; a forged pointer is refused.
5. PROMPT.md is always printed per pass: it is the pass's own job box (pass, pack hash, branch,
   return file), so it can never be the same twice.

Tests added: unchanged text is reused (no 05.02/AGENTS.md, pointer "05.01" and the same hash in the
log, PROMPT.md and claim name 05.01's file); a changed face 01 prints a new hashed 05.02/AGENTS.md; a
hand edit of the reused file is invalid for both passes, --fix restores it, and a forged pointer is
refused and escaped. One unit test checks v3 AGENTS.md has no pass-specific slot.

## For Matthew

- t378u reading: the job lines (jobs, may touch, checks, stop if, return file) now live only in
  PROMPT.md, not in AGENTS.md, so AGENTS.md can stay the same across passes. Is that the split he wants?
- Reuse compares with the latest released AGENTS.md only. If a pass goes back to an older text, a new
  file is printed (same words, new file). Proposed as fine; say if it should look further back.

- Builders can no longer edit a template in place; a new wording must be a new template version.
- Should an invalid file also raise an elevation to Prime or the person by itself? Not built; proposed only.
