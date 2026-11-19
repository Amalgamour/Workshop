# v3 AGENTS.md review (t386u): Prima's keep or drop choices

Matthew (t387u): "You are my engineering lead. You ask why for each change you want to make. Is is better? Is is stronger? Does it align? Then you tell me what you think should stay or not." He reviews and overrides. Rulings can change when new information conflicts (t388u), so each conflict below weighs the new idea against the ruling instead of just citing the ruling.

Three checks for each change: **Better** (clearer for a fresh worker), **Stronger** (harder to misuse or drift), **Aligns** (with Axioms.md and the design).

| # | Change in the review | Better | Stronger | Aligns | Choice |
|---|---|---|---|---|---|
| 1 | "WF records which revisions of both files belong to the pass" | yes, it says what the hash is for | same | yes, it's what wf does (agents_hash, prompt_hash) | **Adopt** |
| 2 | Axiom 5: "Report findings outside the frame. Acting on them requires authority." | yes | yes, it keeps the raise path | yes, Axioms.md 5 "permission to report, not to act ... raise it to authority" | **Adopt** |
| 3 | Axiom 7: "Report a gap that matters ... fill a gap only with authority" | yes | yes | yes, Axioms.md 7 "written permission to solve it". Ours lost the permission path | **Adopt** |
| 4 | Axiom 8: three lawful connections (address, link and back-link, named override) | yes | yes | yes, word for word with Axioms.md 8. Ours ("only a written link") was wrong | **Adopt** |
| 5 | Axiom 9: "Check your own work before handoff. Another view must check it before promotion." | half | no: the first sentence invites trusting your own check | partly. Axioms.md 9 says "its maker is the easiest one to convince". Ours ("never by you") also overstated it | **Change both** to: "Your own check is not proof. Another view must try to break it before promotion." |
| 6 | Faces called "views of the page" | no | no | mixes two words: in the kit a "view" is a file wf prints | **Keep ours** ("a face is one side of a page") |
| 7 | Grant line: "If the prompt and grant disagree, stop the affected action and tell Prime." | yes | yes, a new guard | yes, axiom 1 at the pass | **Adopt** |
| 8 | Drops ours: "authority never from you, and never from a copy" | no | weaker | ours carries axiom 8 "a copy never becomes what it points to" | **Keep ours**, and add item 7 after it |
| 9 | Builder steps as a numbered list | yes | same | yes | **Adopt** the list form |
| 10 | Step 4, "reread any saved Unprompted notes ... findings" | no | no | **conflicts**: in the kit, `unprompted:` means work done that was not asked (kit AGENTS.md:71, DESIGN.md:75, return template line 9), not a findings notebook | **Drop.** Return findings stay in the return file's own lines |
| 11 | Checker or observer pointer to connection 4 | yes | same | yes | **Adopt** |
| 12 | Connections as a table | yes, easier to scan | same | yes | **Adopt** the table, filled from wf's link data |
| 13 | "If a pinned source cannot be opened or its bytes differ, stop ... tell Prime what WF could not verify" | yes | yes | yes, axiom 8: unopenable = 7.8, don't repair from memory | **Adopt** |
| 14 | "If a newer revision has been published ... ask Prime whether to continue under the existing pack or wait" | no | **weaker**: it makes mid-pass drift a judgment call | conflicts with t381u, t382u and the t382s1446 answer | **Drop.** Weighed again under t388u: the new idea's only gain is avoiding a stopped pass, and t382u's reason (each pass builds exactly what was imagined) is stronger. The lock stays |
| 15 | Pins by revision (`{{axioms_ref}}`, `{{face01_entry}}` bytes) instead of path | yes for history | **yes**: closed passes could still be checked byte for byte, while today they are history only | yes, axiom 6 (the past stays readable) | **Park as later work.** It's a new mechanism (wf must read old bytes from git or a store). It is worth doing, and it doesn't fight the lock: the lock still compares the pin with the current file while a pass is open |
| 16 | Overall length about twice ours | partly | same | t379u "very narrow" | **Merge** keeps ours as the base and adds items 1-5, 7, 9, 11-13 only |

## Next step
The builder writes the merged template on agents-hash (the v3 template has not been issued to any real page, so changing it breaks no released file, t378u). Then Tester checks it. Item 15 goes on the later-work list.

## Tester's check of 4e64e47 (11:32 AM EST): Prima's choices
- **status gets a lock line, and observe runs on a locked pass.** Better: yes, a person can see why a page is stuck. Stronger: same, because both are read-only. Aligns: yes, axiom 7 (leave it visible). **Adopt**, the builder is doing it now.
- **Outside anchor for the full-rewrite hole.** Tester's proof: drop the templates label, strip the hashes, re-chain the log, then run --fix, and the page reads as pre-t373u and swaps in the v1 files without a warning. Nothing inside a page that agrees with itself can catch a whole rewrite. Fix: after each pack, write the log head and agents_hash to a place outside the page (for example a committed file in the build repo), and have verify compare against it. Better: yes. Stronger: yes, it is the only fix. Aligns: yes, axiom 6 (the past is not rewritten) and axiom 8 (a written connection both ways). **Park as later design work, together with item 15 (revision pins).** Both need the same thing: a record outside the page that wf can read. Doing them together avoids building two stores.

## Builder round a786566 / c224329 (11:34 AM EST): Prima's choice
- **Observe runs on any unclean page, not only a locked one.** A hand-edited view shows as a "page not clean" finding instead of a refusal. Better: yes, a person can see what's wrong. Stronger: same, because it writes nothing and --record is still refused. Aligns: yes, axiom 7 (leave the gap visible) and axiom 5 (report, don't act). **Keep as built.**
