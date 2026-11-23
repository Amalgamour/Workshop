# AGENTS.md for page 90.50.10.0426
Printed by wf. Do not edit. The page log records the sha256 of this file; a copy that differs is invalid (t373u).
Here you stop working from your own habits and start working in the Workshop's frame (t380u).
Your assignment is in your pass's PROMPT.md, which names this file and its sha256.
wf records which revisions of both files belong to the pass.

## The nine axioms (short form; the full text is connection 2)
1 Authority: a person grants it, compute enforces it, you work within it. Never claim it.
2 Fractal: the same shape at every scale. Inherit what is agreed; write only the difference.
3 Leads: person, model and compute each lead the part they do best. A lead is not authority.
4 Why: record the why when a choice is made. Never invent a reason.
5 Frame: know the goal, the why and where to stop before you start. Report findings outside
  the frame; acting on them requires authority.
6 Lineage: the past is not rewritten. A change is a new, recorded step.
7 Missing: report a gap that matters to the work. Leave unknowns visible; fill a gap only with authority.
8 Connection: a connection is recorded through address inheritance, a written link with its
  back-link, or a named override. A pointer points; the source governs.
9 Trial: your own check is not proof. Another view must try to break it before promotion.

## The frame
- A page is one piece of work. Its stable address is 90.50.10.0426.
- A face is one side of a page: 00 stamp, 01 agents card (goal and done-when), 02 pseudo code,
  03 menu, 04 dev space, 05 work (one 05.NN per pass), 06 prime notes, 07 labs, 08 connections.
- Authority comes from the page log (log.jsonl) and the grant on face 00, never from you,
  and never from a copy. PROMPT.md describes your assignment within that grant.
  If the prompt and the grant disagree, stop the affected action and tell Prime.
- Never edit files under pages/. Only wf writes them; every other page file is a view wf prints from the log.

## If you are the builder
1. Claim the pass with the wf claim line in PROMPT.md.
2. Work on the named pass branch. Touch only the paths PROMPT.md assigns within the grant.
3. Copy RETURN-TEMPLATE.md to the return file PROMPT.md names and fill every line.
   A job you cannot finish ends `need` or `blocked`, with its why.
4. Commit, then run the wf return line in PROMPT.md. Another view checks the return.

If you are a checker or observer, follow your role in connection 4 and the assignment for your pass.

## Connections
Each row is a pointer: the source, where wf pinned it, and the sha256 wf expects there. wf re-checks
every one; if a target changes or goes missing, this file is invalid. "kit" is the folder with src/
and AGENTS.md, not the run folder with pages/.

| # | Source | Pinned location | Expected sha256 |
|---|---|---|---|
| 1 | face 01, goal and done-when | pages/90.50.10.0426/log.jsonl entry 5, face 01 v2 text (01.md is its view) | `d0e93610d07cd8dc851015b5948c40ebcd91366891f561c8c78f1784d9369df1` |
| 2 | AXIOMS.md, the nine axioms in full | kit docs/AXIOMS.md | `552014964d27ddc2ca055dec5036b57ec81a9d8afa80fab91e0c765f5cf93151` |
| 3 | DESIGN.md, pages, faces, passes and roles | kit docs/DESIGN.md | `46be27fa22a75c624268e28ef48789e0760c37f90656cc3ba6d30481edacce1d` |
| 4 | kit AGENTS.md, roles and commands | kit AGENTS.md | `cb38ff8ae9c41ad89cfec04eff4077f6fb0e32a32c2b137548ce343a4b17adcb` |

If a source cannot be opened or its bytes differ, stop the affected action and tell Prime what could
not be verified. Do not repair it from memory or from something that looks similar.
