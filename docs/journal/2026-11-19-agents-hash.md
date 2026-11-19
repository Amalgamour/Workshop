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

## Narrow AGENTS.md with hashed links (t379u, t380u)

Matthew, t379u (11:14 AM EST, verbatim): "1. We want a very narrow agents.md, it should give the connections it needs to explore. It can point to other work.  But we need to make sure it's linking to valid hashed work.  so splitting is fine with me for now. 2. I think it's good enough for now, we might need a log of past max 5 agents.md"

Matthew, t380u (11:15 AM EST, verbatim): "I mean agents is where we switch from using the LLm's frame work to teaching it ours."

1. v3 AGENTS.md was cut down to the core: the nine axioms in one line each, page / address / face,
   where authority comes from (the log and the grant, never the model), and how to return work.
   Why: t380u, AGENTS.md is where the model is taught our frame, so the core must be in it, in plain words.
2. Everything else became a numbered pointer with a sha256: face 01 at its entry, kit AXIOMS.md, kit
   DESIGN.md, kit AGENTS.md (the kit rules). The goal moved to PROMPT.md ("Goal (face 01)").
   Why: t379u, "a very narrow agents.md ... the connections it needs to explore".
3. wf records each link's target hash at pack and re-hashes every target on verify and load. A missing
   or changed target makes the AGENTS.md invalid, exit 1, writes refused, --fix refused.
   Why: t379u, "make sure it's linking to valid hashed work"; same model as the file hash (t373u).
4. Closed passes are history: a changed kit doc after close is noted, not failed. Why: otherwise one
   kit doc edit in a new wf locks every page that ever packed a v3 pass.
5. The "past max 5 AGENTS.md" log was not built (t379u: "might need").

Tests added: valid links pass (each link hash equals the real target, the 01.md view shows the same
hash, verify says "links 4 hold"); an edited face 01 entry is invalid and --fix writes nothing; a
missing target (entry 99, an unknown kit doc) is invalid; a forged link is escaped and the claim is
refused. Four older tests now look for the goal and done-when in PROMPT.md and for the links in AGENTS.md.

## Tester's downgrade hole, the stray file, and the mid-pass lock (t381u, t382u)

1. Tester showed that stripping the hashes from a v2/v3 pack and re-sealing the log made it look like
   an old page. Now a "2" or "3" pack with no hash (or a "3" pack with no links) is invalid, and --fix
   cannot clear it. Why: only wf at t373u or later writes those labels, so a missing hash there is a
   removed hash. The real pages have no label on any pack and still verify. A full rewrite that also
   removes the label is still possible; only an anchor outside the log would catch it.
2. A stray 05.NN/AGENTS.md beside a reused file gets a warning in verify and --fix, and is left alone.
   Why: wf never deletes; a person decides.
3. Matthew, t381u (11:20 AM EST, verbatim): "It never changes mid pass only after review and before a new draft starts"
   Matthew, t382u (11:21 AM EST, verbatim): "Design never is updated during work.  We break into passes so each on refines it's exactly how AI made imagines."
   So a kit rule file that changed under an open pass locks it: "rule file link N (...) changed mid
   pass: rule files change only after review, before a new draft (t381u)". The next pass records the
   new hash. Closed passes stay history. Why: design and rules are frozen during work; refinement
   happens only between passes.

Tests added: stripped hashes plus a re-sealed log stay invalid after --fix (labels 3 and 2, and a v3
with no links); a planted stray AGENTS.md is warned about and kept; a rule file changed under an open
pass locks it and refuses the return; after a close the change is history and the next pass records
the new hash. Older tests whose seeded packs had no hash now label them "1" (pre-t373u), which is the
only lawful way for a pack to have no hash.

## The review merge (t386u-t388u)

Matthew relayed a review of v3 AGENTS.md (t386u). Prima weighed each change (t387u: better, stronger,
aligned; t388u: rulings can change when new information conflicts) and wrote the calls in
docs/design/AGENTS-V3-REVIEW-decisions.md (cecd40a). The builder applied them to templates/v3/agents.txt:
items 1, 2, 3, 4, 7, 9, 11, 12, 13 adopted; axiom 9 rewritten ("Your own check is not proof. Another view
must try to break it before promotion."); "a face is one side of a page" and "never from you, never from
a copy" kept; items 10 and 14 dropped (14 would undo the t381u/t382u lock); item 15 (pins by revision)
parked in the spec. The connections became a table printed from the pack's link data, which now also
records a `source` for each link. Why in place: v3 was never issued to a real page, so no released file
changes. Tests that matched the old link lines and paths were updated; a unit test checks a `|` in a link
field cannot add a table column.

## Seeing the lock (Tester, CHECK-4e64e47)

Tester passed 4e64e47 and noted that status said nothing about a t381u lock and that read-only observe
was refused on a locked page. Now status prints a `locked:` line (which link changed, and that the pass
stays locked until the original kit returns), and observe without --record runs and lists the lock.
Why: a stopped pass has to say why it stopped (axiom 4), and reading never writes. On the real pages,
status and observe output is byte-identical to the pinned wf. The outside-anchor hole (label strip plus
a full log rewrite) is parked by Prima as a design item.

## For Matthew

- t378u reading: the job lines (jobs, may touch, checks, stop if, return file) now live only in
  PROMPT.md, not in AGENTS.md, so AGENTS.md can stay the same across passes. Is that the split he wants?
- Reuse compares with the latest released AGENTS.md only. If a pass goes back to an older text, a new
  file is printed (same words, new file). Proposed as fine; say if it should look further back.

- Builders can no longer edit a template in place; a new wording must be a new template version.
- Should an invalid file also raise an elevation to Prime or the person by itself? Not built; proposed only.
- Answered by t381u/t382u: a rule file change under an open pass locks it (strict). Note: the lock refuses
  every write on that page, including halt, signoff and close, so the old wf must be used to finish the
  pass. Does "after review" mean after close, or may a pass at review (checked, not yet signed off)
  already take a changed rule file? Built as: only closed passes are exempt.
