# Review of v3 AGENTS.md, relayed by Matthew (t386u, 2026-11-19, 11:27 AM EST)

Matthew's words: "Here is the review of the agents.md". The proposed rewrite is kept verbatim below (including its typos). It reviews the v3 template on agents-hash (adcadad / 4e64e47, templates/v3/agents.txt). Prima's comparison is in docs/design/AGENTS-V3-REVIEW-compare.md.

---

# AGENTS.md for page {{addr}}

Printed by WF. Do not edit. The page log records the SHA-256 of the issued
file. A copy that differs from that record is invalid.

Here you stop working from your own habits and start working in the
Workshop’s frame (t380u). Your assignment is in your pass’s `PROMPT.md`.
The prompt names this file and its SHA-256. WF records which revisions of
both files belong to the pass.

## The nine axioms

1. **Authority.** A person grants it, compute enforces it, and you work
   within it. Never claim it.
2. **Fractal.** The same shape at every scale. Inherit what is agreed.
   Write only the difference.
3. **Leads.** Person, model, and compute each lead the part they do best.
   A lead is not authority.
4. **Why.** Record the why when a choice is made. Never invent a reason.
5. **Frame.** Know the goal, the why, and where to stop before you start.
   Report findings outside the frame. Acting on them requires authority.
6. **Lineage.** The past is not rewritten. A change is a new, recorded step.
7. **Missing.** Report a gap that matters to the work. Leave unknowns
   visible and fill a gap only with authority.
8. **Connection.** Connections are recorded through address inheritance,
   a written link with its backlink, or a named override. A pointer
   points. The source governs.
9. **Trial.** Check your own work before handoff. Another view must check
   it before promotion.

The full axiom text is connection 2.

## The frame

- A page is one piece of work. Its stable address is `{{addr}}`.
- Faces are views of the page: 00 stamp, 01 agents card (goal and
  done-when), 02 pseudo code, 03 menu, 04 dev space, 05 work (one `05.NN`
  per pass), 06 Prime notes, 07 labs, and 08 connections.
- The page log `log.jsonl`) records the grant. Face 00 shows it.
  `PROMPT.md` describes your assignment within that grant. If the prompt
  and grant disagree, stop the affected action and tell Prime.
- Never edit files under `pages/` by hand. WF writes the page records
  and prints their views.

## If you’re the builder

1. Claim the pass using the WF claim line in `PROMPT.md`.
2. Work on the named pass branch. Touch only the paths the prompt assigns
   within the recorded grant.
3. Copy `RETURN-TEMPLATE.md` to the return path named in `PROMPT.md` and
   fill every line. A job you cannot finish ends `need` or `blocked`,
   with its why.
4. Before returning, reread any saved Unprompted notes. Keep findings with
   a concrete use. State what you noticed, why it matters, and its source.
   Report an urgent finding when you notice it.
5. Commit your work, then run the WF return line in `PROMPT.md`.
   Another view checks the return.

If you’re a checker or observer, follow your role in connection 4 and
the assignment issued for your pass.

## Connections

Each pointer identifies the exact revision issued for this pass. WF checks
the pinned source against its expected SHA-256.

| # | Source | Pinned location or record | Expected SHA-256 |
|---|---|---|---|
| 1 | Face 01, goal and done-when | Page log entry `{{face01_entry}}` | `{{face01_sha256}}` |
| 2 | `AXIOMS.md`, the full nine axioms | `{{axioms_ref}}` | `{{axioms_sha256}}` |
| 3 | `DESIGN.md`, pages, faces, passes, and roles | `{{design_ref}}` | `{{design_sha256}}` |
| 4 | Kit `AGENTS.md`, roles and commands | `{{kit_agents_ref}}` | `{{kit_agents_sha256}}` |

For face 01, the digest covers the exact source bytes WF pinned from
the recorded revision. A regenerated display is a view of that source.

If a pinned source cannot be opened or its bytes differ, stop the
affected action and tell Prime what WF could not verify. If a newer
revision has been published, the original pin still records what was
issued. When the change affects your assignment, ask Prime whether to
continue under the existing pack or wait for a revised one.
