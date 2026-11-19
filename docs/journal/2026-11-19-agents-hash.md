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

## For Matthew

- Builders can no longer edit a template in place; a new wording must be a new template version.
- Should an invalid file also raise an elevation to Prime or the person by itself? Not built; proposed only.
