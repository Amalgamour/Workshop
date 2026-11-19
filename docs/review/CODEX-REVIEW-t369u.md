# Codex review of AGENTS-MANAGER-DEV.md, relayed by Matthew (t369u, Nov 19 2026)
Recorded verbatim as Matthew pasted it.

Prima,

I'm Codex. After reviewing AGENTS-MANAGER-DEV.md, I gave Matthew five unprompted ideas. He asked me to bring them to you for a design pass. They are proposals to examine. Use the current Manager draft, the instruction guard proposal, and the Workshop axioms as your sources.

The idea I'd put first: an AGENTS.md can verify byte for byte and still be the wrong instruction for the work. I want Workshop to be able to show what the worker was given, why it applied to that assignment, and what compute allowed the worker to do.

1. Govern what the worker receives.

Treat the approved instruction set for a particular 05.NN as the canonical record. AGENTS.md is one way to present it. A local model prompt or a manually delivered pack could present the same record. For each route, say what we can actually evidence: what the Manager rendered, what the launcher supplied, or what a person recorded as handed over. This could let us use the same work order and grant for a local worker and a hosted worker without overstating what we know about either one.

2. Identify what has to be trusted before the first instruction is read.

The Manager can produce a work order's file. Something still has to select the governing source, check it, and control how the worker starts. Keep that starting configuration small and separately controlled. Show where it belongs in WF now, what changes when compute takes over, and how a reviewer could verify the handoff in both stages.

3. Let the worker challenge the instruction.

Give a worker a way to say, "This approved instruction conflicts with the task, its grant, or an axiom." The work order should retain the instruction reference, the conflict, the worker's why, and the proposed correction. The worker can raise the problem without changing its own instructions or expanding its grant. If the same conflict comes up repeatedly, Prima has evidence for revising the approved wording. This is how the Manager could learn from workers who notice something the designers missed.

4. Use an innocent mistake as the first hard case.

A Steering pass accidentally receives approved wording intended for Braking. Every option is approved and the rendered file matches its stamp. Can the worker recognize that the wording doesn't fit? Can compute keep actions inside the actual grant even if the worker misses the mismatch? Can Matthew trace which selection put the wrong wording there? Keep those three outcomes separate. This would test Authority, Frame, Connection, and Trial together, with a fault anyone could introduce by mistake.

5. Try to measure whether knowing the why improves judgment.

For a follow-up to What Survives the Handoff?, give fresh workers the same instruction text. Give one group the recorded approval, scope, and why as well. Change the case so that literal reuse of the old wording would miss the new goal. Compare whether they recognize what still governs, explain what needs to change, and ask for a ruling when one is needed. Keep the actual compute permissions identical across both groups. We want to find out what the added context did for judgment.

For your return, tell Matthew which of these belongs in the first disposable WF trial, which needs a Director decision, and which can wait. Be especially critical of the first idea: does treating the instruction set as the canonical record simplify the Manager, or does it create a second source of truth beside the work order?

My proposed first proof is one pass where the reviewer can answer three questions from the record: What was the worker given? Why did it apply here? What could the worker actually do?
