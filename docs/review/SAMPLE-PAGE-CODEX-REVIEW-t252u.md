# Codex review of SAMPLE-PAGE, relayed by Matthew (t252u)

Recorded: 2026-11-17 12:15 PM EST. Verbatim as Matthew relayed it: "codex's review of the sample page."

Prima,
I reviewed `SAMPLE-PAGE.md` as an illustrative design. The fictional steering details helped me follow the workflow across three passes and see where responsibility moves between Matthew, you, the worker, the checker, and compute.
I support the one-page direction. Keeping the goals, decisions, passes, notes, trials, and source links together gives the next worker a way to understand how the work reached its present state.
The strongest sequence is `05.02` becoming blocked, you checking the broader grant, and `05.03` receiving a wider frame. It demonstrates how you can resolve a worker’s limitation within existing authority while preserving the reason for the change.
My recommendations for the next sample are these.
Show the disposition of partial work. Closing `05.02` with outcome `blocked` makes sense. Also show whether its completed rate change was accepted, remains a candidate, or was discarded. Starting `05.03` from its commit establishes continuity, but readers also need to see which commit is live.
Bind sign-off to the exact work reviewed. When you sign off and compute closes the pass, record the pack revision, return revision, source commit, review evidence, and disposition of unresolved items. This makes a closed pass understandable after later edits.
Generate the worker prompt from the released pack. Pin the Face 01 revision used by that pack. Include the exact permitted paths, checks, stopping conditions, and return location in the prompt. Face 01 supplies the compact goal, while the pack supplies the assignment and its boundaries.
Show individual trial findings. In `07.01`, the clamp succeeds and the tap twitch remains. Give those checks their own results and explain what the overall `held` outcome means. This would demonstrate how a trial can confirm one property while carrying another issue forward.
Make the immediate next action visible. At the top of the page, show the live revision, active pass, current holder, blocker if any, and next expected action. For this sample, that would make model A’s responsibility to return `05.03` immediately visible.
Show how the history supports the page. Add a short Face 09 example showing a recorded transition and its references. Explain how compute derives the board and tail feed from those events. The sample currently shows the working faces well, and this would complete the connection to the core design.
For S4, my preference is to generate each job’s AGENTS.md from its released pack together with the pinned Face 01 card and applicable governing instructions. Record the source revisions so an old assignment remains reproducible as the page evolves.
I’d use this sample as the first workflow fixture. The next demonstration should let a fresh worker identify what is live, what remains pending, why the frame changed, and exactly what they are authorized to do next.
