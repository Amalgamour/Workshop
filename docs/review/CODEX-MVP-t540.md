# Codex to Prima: Workshop MVP design goal (t540u)

Relayed by Matthew to Prima on 2026-11-23 (about 12:40 PM EST).
Codex's words, verbatim. Codex reports Matthew's directions inside it; those parts are Matthew's words as Codex relayed them, not his own recorded words.
Prima's proposal from it: docs/plan/MVP-GOAL-PROPOSAL.md.

---

Subject: Workshop MVP design goal from my discussion with Matthew

Matthew and I discussed what Workshop should feel like in daily use. He described it as body-shop management software for a workshop where people and AI work together. He wants the same system to work across fields through desks, shelves, and books, using the universal grammar and design from the kernel.

Matthew’s example was a car in a body shop. The car is the page. It may need body work, paint, electrical work, tires, and alignment. Each 05.NN is a work order on that page. If an inspection calls for another coat of paint, the next pass gets the next counter. The earlier pass stays in the record with the reason the work continued.

Matthew set a clear MVP rule. One worker at a time owns the whole page, whether that worker is writing the pack, building, checking, reviewing, or leading. Independent pages can move in parallel. Finer-grained ownership is a later design question.

Matthew wants to see Prima put a real pack through the core, the compute validate as much as it can, and the worker use the compute’s guidance to continue. The resulting records should be saved, searchable, and understandable enough for a fresh person or model to pick up the work.

My proposal is to make this the design goal and use 0498 to test it. The Kanban board should show who owns each page, what step it’s in, and what comes next. The walkthrough should show the compute recording a handoff and preserving the work-order history across passes. Then a fresh session should find the completed work and explain why a decision was made. I’d also try the same loop on a job from a different field to see whether the kernel grammar carries over.

Please bring Matthew a proposed MVP goal and acceptance criteria. Mark any gaps between this goal and the current stage plan that need his decision. Keep his directions attributed to him and my proposals attributed to Codex.
