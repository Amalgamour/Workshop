# AGENTS-HASH: the release hash on a pass's AGENTS.md and PROMPT.md

Status: **build stage.** Rules from t373u, t378u, t379u, t380u, t381u, t382u and t386u-t388u. Built on branch agents-hash (from harden-dev 2b5a7ef). Not merged, not pushed.
The rule comes from the Director (t373u). The details below (field names, messages, what counts as
"old") are the builder's reading, not his words.

## His words (t373u, Nov 19 2026, 10:57 AM EST, verbatim)

"We need to run that bit check thing.  I can't remember the name so it's recorded once a released agents file is done.  So we can confirm it's correct otherwise it's invalid."

Our reading (not his words): the "bit check thing" is a hash (sha256). When wf releases a pass's
AGENTS.md (and PROMPT.md, which is released at the same moment), it records the hash in the page log.
Any copy whose hash does not match is invalid. This answers question C5 of the Codex ideas design
pass (docs/design/CODEX-IDEAS-design-pass.md on prima/build, lines 149-151 and 227-231).

## Why

- Before this, the pack entry pinned the templates only by a label, `templates: "2"` (cmd.rs pack;
  render.rs `packed_templates`). If someone edited templates/agents.txt without a new label,
  `wf verify --fix` would reprint every past AGENTS.md with the new words and call it "matches the log".
  The past would have been rewritten, and no one could say what a worker was really given.
- Axiom 1 (authority): the live record is the log. A copy does not outrank it. The hash lets the log
  say exactly which text was released, byte for byte.
- Axiom 6/8: a view is a pointer to the record; the hash is how anyone checks the pointer.

## What wf does now

1. **At pack.** wf prints AGENTS.md and PROMPT.md from the new pack entry itself, then stores
   `agents_hash` and `prompt_hash` (full sha256 hex of the exact bytes written) in that entry.
   The templates have no slot for these two fields, so storing them does not change the text.
2. **Every read that loads the page** (every command except `board`, which compares the same way
   without writing) recomputes:
   - the copy on disk against the recorded hash. A hand edit gives
     `AGENTS.md for pass 05.NN is invalid: hash mismatch (the copy on disk hashes to X, the log recorded Y)`.
   - the text this wf would print against the recorded hash. A template change after release gives
     `AGENTS.md for pass 05.NN is invalid: hash mismatch (pack entry N recorded Y, this wf would print X; the released text is not reprinted)`.
   The same for PROMPT.md. `verify` exits 1; write commands are refused and write nothing.
   Recorded values are escaped (a forged field may hold control characters) and a non-string field
   matches nothing.
3. **verify --fix.** A hand-edited copy is reprinted, because the reprint hashes to the recorded value
   (the released bytes come back). If the reprint would hash differently, `--fix` refuses with
   `refused to reprint: ...; nothing was changed` and writes no view at all, not even a missing one.
   wf never rewrites what a worker was given.
4. **Old pack entries** (no hash field, packed before t373u) are not failed. `verify` adds one line per
   pass, `05.NN: AGENTS.md no hash recorded (before t373u); PROMPT.md no hash recorded (before t373u)`,
   and the board card has a `released:` line saying the same. The real pages 90.10, 90.20 and 90.30
   verify ok this way.
5. `wf verify` on a page with hashes prints `05.NN: AGENTS.md hash <12 chars> holds; PROMPT.md hash <12 chars> holds`.

## Reuse: one released AGENTS.md for many passes (Director t378u)

His words (t378u, Nov 19 2026, 11:07 AM EST, verbatim): "So once a agents.md is released it can't be changed correct?  Well that is a good thing.  If a new agents.md is required a new one is printed then hashed.  agents.md should be replacable on each pass of the WF loop if it's needed.  Although if no change is required the existing should stay."

Our reading (not his words): a released AGENTS.md is locked by its hash. A pass gets a new one only
when its text would change; otherwise the pass keeps the one already released.

**Why a new template version (v3) was needed.** The v1/v2 AGENTS.md names its own pass and pack hash
and lists the jobs, may-touch, checks and return file. Two passes could never print the same bytes,
so "if no change is required the existing should stay" could never happen. v3
(templates/v3/agents.txt) keeps only what belongs to the page and the kit: face 01 goal and
done-when, the pinned face 01 / AXIOMS / DESIGN sources, the rules and the checker notes. Everything
pass-specific was already in PROMPT.md and stays there. New packs write `templates: "3"`; v1/v2 entries
print exactly as before (the real pages are unchanged). Moving the job lines out of AGENTS.md is the
builder's reading; see "Needs Matthew" in the journal.

**What wf does.**
1. At pack, wf prints this pass's AGENTS.md text in memory and compares its sha256 with the latest
   released AGENTS.md on the page (the latest pack entry that recorded an `agents_hash`).
   - Same hash: no 05.NN/AGENTS.md is printed. The pack entry records `agents_from: "05.MM"` (the
     pass that printed the file; a chain of reuses always points at the printer) and `agents_hash`.
   - Different hash (or no earlier hashed one): a new 05.NN/AGENTS.md is printed and hashed, as before.
2. v3 PROMPT.md says which file is yours: `Read first: pages/<page>/05.MM/AGENTS.md (sha256 <12>, reused from 05.MM)`.
   `wf claim` names the same path. The board card lists that path with "(reused, t378u)".
3. verify and every page load treat the reused file as this pass's file:
   - a hand edit of 05.MM/AGENTS.md is invalid for 05.MM and for every pass that reuses it
     (`AGENTS.md for pass 05.NN is invalid: hash mismatch (it reuses 05.MM/AGENTS.md, ...)`);
   - the text this wf would print for the reusing pass must still match the recorded hash;
   - the pointer must name an earlier-packed pass that printed its own AGENTS.md with the same hash.
     Anything else is `AGENTS.md for pass 05.NN is invalid: bad reuse of <name> (<why>)` (escaped).
   - `verify --fix` restores the source file and never prints a copy for the reusing pass.
   - verify prints `05.NN: AGENTS.md reused from 05.MM (hash <12> holds)`.

## Narrow, hashed links, and the switch to our frame (Director t379u, t380u)

His words (t379u, Nov 19 2026, 11:14 AM EST, verbatim): "1. We want a very narrow agents.md, it should give the connections it needs to explore. It can point to other work.  But we need to make sure it's linking to valid hashed work.  so splitting is fine with me for now. 2. I think it's good enough for now, we might need a log of past max 5 agents.md"

His words (t380u, Nov 19 2026, 11:15 AM EST, verbatim): "I mean agents is where we switch from using the LLm's frame work to teaching it ours."

Our reading (not his words): AGENTS.md is the point where a model stops working from its own habits
and starts working in the Workshop's frame. So it is narrow but not bare: a few plain lines teach the
core, and everything deeper is reached through pointers, each pinned by sha256. Reuse against the latest
AGENTS.md only is enough for now; the "past max 5" log is a "might need" and is not built.

**What v3 AGENTS.md holds now** (templates/v3/agents.txt):
- the nine axioms in one plain line each, with the full text as link 2;
- the frame: what a page, an address and a face are; authority comes from the log and the grant on
  face 00, never from the model or a copy; only wf writes under pages/;
- how to return work, in five sentences;
- Connections: numbered pointers, each a place plus the sha256 of what must be found there.
Moved out: the goal and done-when (link 1, and printed in PROMPT.md as "Goal (face 01)"); the build,
commit and checker notes (in the kit rules, link 4).

**The links** (recorded at pack in the pack entry as `links`, printed into AGENTS.md, so the AGENTS.md
hash covers them):
1. `pages/<page>/log.jsonl entry N: face 01 vV text (view: pages/<page>/01.md)`: the face 01 text as
   written at entry N. The 01.md view header shows the same hash (12 chars) while that version is current.
2. `kit docs/AXIOMS.md`, 3. `kit docs/DESIGN.md`, 4. `kit AGENTS.md` (kit rules): the copies built
   into this wf.

**The check** (same model as the file hash): on verify and every page load, wf re-hashes each link's
target: face 01 is rebuilt from the log up to entry N; a kit document is the copy in this wf. A target
that is missing, unknown, or hashes differently makes that AGENTS.md
`invalid: link N (<path>) points to changed or missing work` (escaped), exit 1, writes refused, and
`--fix` refuses to reprint. A good page prints `links 4 hold` per pass.

**Rule files are frozen while a pass is open (Director t381u, t382u).**

His words (t381u, Nov 19 2026, 11:20 AM EST, verbatim): "It never changes mid pass only after review and before a new draft starts"

His words (t382u, Nov 19 2026, 11:21 AM EST, verbatim): "Design never is updated during work.  We break into passes so each on refines it's exactly how AI made imagines."

Our reading (not his words): the design and rule files a pass links to (kit AXIOMS.md, DESIGN.md,
AGENTS.md) are frozen while the pass is open. Refinement happens only between passes: after review,
before the next draft. So the lock is strict.
- A pass that is packed and not closed (tails pack, open, return, review) whose kit link target now
  hashes differently: `AGENTS.md for pass 05.NN is invalid: rule file link N (<path>) changed mid pass:
  rule files change only after review, before a new draft (t381u)`. Exit 1; every write on the page
  is refused (the same as any invalid released file), and `--fix` will not reprint.
- The next pass is packed under the new rule files and records their new hashes (a new AGENTS.md is
  printed, since its link lines change).
- A missing or unknown target, or a changed face 01 entry, keeps the general message
  `link N (<path>) points to changed or missing work`.

- Reading a locked page (Tester, CHECK-4e64e47): `wf status` adds `locked:  05.NN locked: rule file
  link N (<path>) changed mid pass (t381u). It stays locked until the original kit returns (the wf
  built with the pinned rule files).` Read-only `wf observe` runs on a locked or unclean page and lists
  the lock and `page not clean: <reason>` as findings; `observe --record` writes, so it is still refused.
  Why: a lock must be visible and explainable; reading never changes the record. On a clean page,
  status and observe print exactly what they printed before.

**Closed passes are history.** A closed pass's AGENTS.md was valid when it was used. If a kit
document changes after the close, verify notes `link N changed after the pass closed (history, not
failed)` and does not lock the page. Why: t381u allows the change exactly then (after review, before
the next draft); failing closed passes would lock every page that ever packed a v3 pass.

## Every v2/v3 pack must carry its hashes (Tester downgrade hole)

Tester (scratch/tester-ahash/CHECK-RESULTS.md, section 2e) found that stripping the hash fields and
re-sealing the log chain made a v2/v3 pack read as "no hash recorded (before t373u)"; `--fix` then
reprinted, and a later label switch laundered the text. Now:
- A pack whose `templates` is "2" or "3" must carry `agents_hash` and `prompt_hash`; a "3" pack must
  also carry `links` (or `agents_from`). Otherwise: `05.NN: pack entry N (templates X) has no hash
  recorded: invalid` (or `... has no links recorded: invalid`). Exit 1, writes and `--fix` refused.
  The board card says `NO HASH (invalid ...)`.
- Only a pack with templates "1" or no label may say "no hash recorded (before t373u)". The real pages
  90.10, 90.20, 90.30 have no label on any pack (checked: 10, 5 and 4 packs), so they still verify.
- Residual (not closed by this rule): someone who can rewrite the whole log can strip the hashes and
  also remove the label, so the pack reads as v1. Only an anchor outside the log (for example the log
  head pinned in git or held by a person) can catch a full rewrite. Packs written by a wf from
  before t373u with label "2" (2b5a7ef and older v2 builds; only in Tester scratch pages) are now
  invalid on this wf.

## A stray AGENTS.md beside a reused one

If a file 05.NN/AGENTS.md sits in the folder of a pass that reuses another pass's AGENTS.md, wf did
not print it and does not check it. verify (and `--fix`) prints `warning: 05.NN/AGENTS.md is on disk,
but 05.NN reuses 05.MM/AGENTS.md. wf did not print it, does not check it, and will not delete it;
remove it by hand if nobody needs it.` It does not fail verify. wf never deletes it: deleting is a
person's call. The pass's PROMPT.md still names the released file and its hash.

**PROMPT.md is not reused.** It names its own pass, pack hash, log entry, time, branch and return file,
so no two passes can share it, and making it shareable would mean moving the job itself out of the job
box. It is always printed and hashed per pass. It is also where the pass points at its AGENTS.md.

## Consequence for builders

A template text change is now a new template version (a new label and a new file, like templates/v1 or templates/v3),
never an edit of the current one. Editing templates/agents.txt or prompt.txt in place would make every
hashed pass on every page invalid and lock those pages until the old text is back.

## Not covered (open)

- RETURN-TEMPLATE.md and PACK.md are not hashed by this rule. PACK.md already has `pack_hash`.
- The hash proves what wf printed. It does not prove what reached the worker (Codex idea 1 / C2: a
  delivery entry). It does not prove who claimed (the name is still `--as`).
- Whether an "invalid" file should also be raised to Prime or the person automatically is not decided.

## v3 AGENTS.md after the review (t386u-t388u)

Matthew relayed a review of the v3 template (t386u, docs/review/AGENTS-V3-REVIEW-t386u.md on prima/build).
He asked Prima to weigh each change: better, stronger, aligned (t387u: "You ask why for each change you
want to make. Is is better? Is is stronger? Does it align?"), and rulings can change when new information
conflicts (t388u: "my rulings can change, if current information conflicts with past choices we need to
check it and figure out which is best"). Prima's calls: docs/design/AGENTS-V3-REVIEW-decisions.md (cecd40a).
v3 had not been issued to any real page, so the template was edited in place (no released file changes).

What changed in templates/v3/agents.txt, with the why:
- Item 1: "wf records which revisions of both files belong to the pass." Says what the hash is for.
- Item 2, axiom 5: findings outside the frame are reported; acting on them requires authority (keeps the raise path, Axioms.md 5).
- Item 3, axiom 7: report a gap that matters; fill it only with authority (ours had lost the permission path, Axioms.md 7).
- Item 4, axiom 8: the three lawful connections (address inheritance, link with back-link, named override). Ours said "only a written link", which was wrong against Axioms.md 8.
- Axiom 9 rewritten for both versions: "Your own check is not proof. Another view must try to break it before promotion." (Axioms.md 9: the maker is the easiest one to convince.)
- Item 7: "If the prompt and the grant disagree, stop the affected action and tell Prime." Placed after our kept line "never from you, and never from a copy" (item 8 kept ours).
- Item 9: builder steps as a numbered list. Item 11: checkers and observers follow connection 4.
- Item 12: the connections are a table (#, source, pinned location, expected sha256), printed from wf's
  link data in the pack entry (`source`, `path`, `sha`). Cells are escaped and a `|` is written `\|`, so a field cannot add a column.
- Item 13: if a source cannot be opened or its bytes differ, stop the affected action and tell Prime; do not repair from memory (axiom 8, `7.8`).
- Kept ours: "a face is one side of a page" (item 6; in the kit a "view" is a printed file).
- Dropped item 10 ("Unprompted notes"): in the kit `unprompted:` means work done that was not asked, not a findings notebook.
- Dropped item 14 ("ask Prime whether to continue under the existing pack"): it would make mid-pass drift a judgment call; t381u/t382u keep the lock.
- Stays narrow (t379u): about the same length as before.

**Later work (parked, item 15): pins by revision.** Pin each source by revision (a git object or a stored copy) instead of by path, so wf could re-check a closed pass byte for byte instead of treating it as history. It needs wf to read old bytes from git or a store. Not built.
