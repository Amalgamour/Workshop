# Codex draft: "Workshop Manager and the First Desk Trial" (Draft 01), verbatim

Pasted by Matthew in Prima's chat, message t304u, Wed Nov 18 2026, 1:56 PM EST.
Recorded by Prima, unchanged below the line. Matthew's own lead-in line comes first.
Prima's review: PRIMA-REVIEW-MANAGER-DRAFT-t304u.md (commit 99d2030).

Matthew's lead-in (verbatim): "I want you to read over what I have been doing with Codex."

---

# Workshop Manager and the First Desk Trial
Draft 01 · For Prima’s review

Matthew and I have been working through what it should feel like to sit at a Workshop desk and oversee work across a project. This draft brings together his direction, my proposed design, and the reasons behind the choices. The axiom numbers refer to the nine-axiom Workshop text I reviewed earlier. The proposed portal behavior and trial are open for review.

## Matthew’s direction

> Think bodyshop manger software.

> The workshop I should be able to see the kanban styled view of pages. Pull up the pages faces and the work that was done, being done. a workorder is the 05.NN Where the car represents the full details of the car and the owner.

> Yes, it has the responsible model the responsible person. So think the person is the show manager, the lead model is like the floor manager.

> So a project is a book, it contains all the details, the car is a page that is the details of that task. Like the steering wheel is a small part of building a driving game.

> The shelf is so we can repeat similar projects in the same environment over and over. So a driving game shelf might exist on a Game dev desk. The desk is the specialized workshop. The shelf is the like a department.

> The workorder never disappears

> We keep them so we can extract and condense the lessons for quick access in a repo. With xlinks back to the original if needed.

## The shape of the Workshop

| Level | Example | What belongs there and why |
|---|---|---|
| Desk | Game Dev | The specialized workshop where people and models sit together. It holds the tools and practices useful across game development. |
| Shelf | Driving Games | The department where similar projects repeat. Shared templates, checks, and lessons can improve here as more projects go through the same environment. |
| Book | Dirt Circuit | The full project. It holds the game’s goals, common constraints, and the pages for steering, braking, tracks, and other parts. |
| Page | Steering | The equivalent of the car and its full file. It holds the part’s purpose, current design, faces, responsible person, responsible model, dependencies, and work history. |
| Work order | `05.01` · Limit steering angle | One scoped piece of work on the page. It keeps the assignment, what was handed back, review evidence, and the outcome. |

**Why this shape.** Put each decision at the level where it applies. Test both steering limits may be useful throughout the Driving Games shelf. Choosing ±30° may make sense for Dirt Circuit because of how that particular game should feel. Preserve the number and its why on the project page. If a second game needs the reasoning, give it an xlink to the original. This lets the department inherit useful practice while each project keeps its own judgment.

Axioms 2 (Fractal), 4 (Why), 5 (Frame), 6 (Lineage), 8 (Connection).

## What the manager sees

The portal opens into a specialized desk, then a shelf, then a project book. The book shows a **Kanban board of pages**. Each card gives the page’s name and address, its responsible person and lead model, a short account of the work in flight, and the next decision if there is one. Open a card to see every page face, plus work being done and work already completed. Keep the page and both responsible roles visible while switching faces.

- **Shop Manager · responsible person.** Owns the page’s intended outcome and makes decisions that exceed delegated authority.
- **Floor Manager · responsible lead model.** Coordinates the page’s work, prepares assignments, tracks handoffs, and brings the person decisions with a recommendation and its why.
- **Work order assignee.** Owns the next action on a specific `05.NN`. That can change as work moves through `draft → pack → open → return → review → closed`.

**Why these roles stay visible.** A person opening the board needs to know who can decide. A model opening a page needs to know who is coordinating and who owes the next move. When a floor manager changes, the page shows the current lead and the work history keeps the attribution of earlier decisions.

**Why the board shows pages.** A single Steering card can contain `05.01` closed, `05.02` waiting on Matthew, and `05.03` moving with a builder. The page remains visible with an indicator that points to the exact decision. Each order keeps its own WF state. I’d derive the board’s summary from those records so it stays consistent with the underlying work. When the page has no active work, it can drop out of the active board while remaining in its book.

Axioms 1 (Authority), 3 (Leads), 5 (Frame), 6 (Lineage), 8 (Connection).

## What survives the work

A closed order stays in the page’s history. If it later moves into archive storage, keep its original identity and a resolvable xlink. The body shop’s seven-year example illustrates the difference between active records and archived records. Workshop’s actual retention policy is still open.

A person and model can sit at the desk, open a completed order, and extract a short lesson for the repo. My proposed minimum is **the lesson, its why, where it applies, and an xlink to the source**. A single order can produce a draft lesson immediately. Before it becomes shared shelf guidance, have someone test whether it applies to another project and identify where it stops applying.

**Why keep both.** The short lesson gives the next worker quick access. The original order lets them inspect the evidence, recover a detail the summary left out, or reconsider the lesson later. If the evidence is thin, preserve that uncertainty with the lesson.

Axioms 4 (Why), 6 (Lineage), 7 (Missing), 8 (Connection), 9 (Trial).

## First desk trial

Prove one sitting before building the full portal. Use the driving-game example and identify which records are real and which are fixtures.

1. **Oversee the book.** From the page board, Matthew can tell what needs his decision, what work is still moving, and what has passed review. Opening Steering gives him the face or work order behind each answer.
2. **Think together at the desk.** Matthew and the model open one completed order and work out what it actually taught them. Preserve the observation or correction that changed the lesson, then produce a short draft with the why and source xlink.
3. **Try it on another book on the same shelf.** Give a fresh model the new game’s goal and the condensed lesson. Ask what it would carry forward, what it would decide anew, and what evidence it would open if unsure. A useful result would be carrying forward the steering checks while treating ±30° as evidence from Dirt Circuit, then making a fresh choice for the new game.

**Why this trial.** It exercises the whole idea in miniature. The person can oversee the work, the desk can help a person and model turn experience into a lesson, and a fresh model can use that lesson in a different project without Matthew retelling the original story.

Please review which pieces can already be shown using the existing page faces, WF records, and repo links. Flag any place where the proposed portal would duplicate a governing record or where an authority decision is still needed. The first question for us to settle is what a new book on a shelf inherits automatically and what it sees as reference material.
