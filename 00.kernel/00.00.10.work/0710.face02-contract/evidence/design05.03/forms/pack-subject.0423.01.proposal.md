# PROPOSAL — local subject section `Pack` for `00.00.10.work/0423.dev-authoring/01`
date: 2026-11-02 · who: claude-opus-5-5 · state: **draft proposal, not seated, not written to the page.** Evidence for 0710/05.03 only.

**Owner class:** book-local, the work book `00.00.10.work`.
**Ground, the recorded task authority:** the Director's request recorded in 0423/06.01 ("draft the dev cycle and template, then pack for coding"), carried out under 0526/05.01.
**Generic law above it:** 0005 Task and Ticket (face-05 work items). **This section adds pack semantics only for this book's development cycle.** Kernel law 0002 stays general.

```text
## Pack

owner: book-local

A development pack is a face-05 work item of its work page, prepared from its N4NN source page.
It states its source, goal, scope (included, excluded, allowed writes), finish criteria, executor and reviewer,
and one numbered work item per change, each with its acceptance.
Each declared source note has a disposition: integrated into an item, deferred with a reason, or rejected with a reason.
A pack is prepared, not released. Release is the Director's separate act. A pack grants no permission beyond 0005 Boundary.
```

**What this would ground** (the meaning grounds for `pack.forms.json`):
- goal, scope, finish, executor, reviewer, items and acceptance;
- note dispositions.

**What stays representation** (the form's own ground):
- `#NN` numbering;
- field order;
- UTF-8;
- the answer encodings.

**Not decided here:**
- seating this section, which needs its own draft, sign and approval;
- whether 0423/01's other sections move to face 04.
