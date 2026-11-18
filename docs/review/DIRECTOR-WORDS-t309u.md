# Director's words: t309u

Date: Wed Nov 18, 2026, about 2:20 PM EST
Source: Matthew, in chat.

## Verbatim

"I realize we are going to have to build anti hacker into the compute.  To protect us against hackers attacking agents.md files for creating malicious attacks."

## Prima's notes (not his words)

Threat: instruction files models read and obey (AGENTS.md, templates, job boxes) get altered to carry hidden commands
(prompt injection), so every model that reads them acts for the attacker. Existing partial guards: grant/may-touch
refusals, the hash-chained log (axiom 6), pinned packs. Missing: a guard on the instruction files themselves.
Design to follow as a roadmap item (to be proposed to the Director, not yet ruled).
