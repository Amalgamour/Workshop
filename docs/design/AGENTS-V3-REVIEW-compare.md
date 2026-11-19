# v3 AGENTS.md: the t386u review compared with what we built

Sources: docs/review/AGENTS-V3-REVIEW-t386u.md (the review), templates/v3/agents.txt on agents-hash 4e64e47 (ours), docs/spec/Axioms.md (the full axioms), and Director words t378u-t384u.

## Where the review is closer to the full axioms than ours (adopt)
- **5 Frame:** "Report findings outside the frame. Acting on them requires authority." This matches Axioms.md 5 ("permission to report, not to act ... raise it to authority"). Ours said "do not act", which is flatter.
- **7 Missing:** "fill a gap only with authority." This matches Axioms.md 7 ("whether you have written permission to solve it"). Ours said "never ... quietly filled", which loses the permission path.
- **8 Connection:** it names all three lawful connection types (address inheritance, link with back-link, named override), which matches Axioms.md 8 exactly. Ours ("only a written link connects") is too narrow and drops two of them.
- **Prompt vs grant:** "If the prompt and grant disagree, stop the affected action and tell Prime." This is new and good: it is axiom 1 applied at the pass.
- **Builder steps as a numbered list, with a pointer for checkers and observers:** clearer, with the same content.

## Where it conflicts with rulings (do not adopt as written)
- **The last paragraph** ("If a newer revision has been published ... ask Prime whether to continue under the existing pack or wait for a revised one") goes against t381u, t382u and the t382s1446 answer: rule files and design never change mid pass, only once the pass is closed. A choice to "continue under the existing pack" opens the drift those rulings shut. Default (follows the rulings): drop that sentence and keep "a changed or missing source invalidates this file; stop and tell Prime". The pass stays locked until it is closed.
- **9 Trial, "Check your own work before handoff":** Axioms.md 9 does not say this ("its maker is the easiest one to convince"). A self-check is harmless, but writing it into the axiom's short form adds a rule the axiom doesn't have (axiom 2: write only the difference, and don't invent). Default: keep the full-axiom meaning, "Another view must check it before promotion", and put any self-check in the return template, not in the axiom line.

## A design change it implies (park for later)
- **Pins by revision** ({{axioms_ref}}, {{face01_entry}}) rather than by path. Today wf checks the current bytes at a path, which is what makes the strict lock work. Revision pins would let old bytes stay readable after a file changes. That's useful for history, but it is a new mechanism. Default: keep path plus sha256 as built (it enforces t381u) and park revision pins as later work.
- **Link 3 DESIGN.md** is a new link. Today link 3 is different in the build. To check: which file holds pages, faces, passes and roles in the kit.
- **Unprompted notes (step 4)** already exist in the kit specs (drafting.md, workflow-loop.md), so pointing to them is fine.

## Length
The review is about twice as long as ours. t379u asked for "very narrow". The extra length is mostly clearer wording and the builder list, not new links.
