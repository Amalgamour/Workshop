# 02

version: 001
Authorization: draft — 2026-11-02
who: claude-opus-5-5
state: draft. **ILLUSTRATIVE**, 0710/05.02 evidence. It shows four named forms in one face-02 section under candidate law 0002 v004. **Not installable:** the home and the governing source are unresolved (see `home`).
Face: 02
PPPP: 0423
book: 00.00.10.work
keyword: dev-authoring
why: Named forms for the development pack subject: read, create, revise, check.

## Pack

home: proposed `00.00.10.work/0423.dev-authoring/02.md`. **Unresolved:** 0423/01.md is a draft development contract and has no seated face-01 section `Pack`. Its meaning grounds below cite that draft's §4. Generic work-item law is 0005 (Task, Ticket). Pack-specific requirements need their own owner (R05).
machine form set: `pack.forms.json` (a proposed format, not kernel language)

form: pack-card
kind: card
purpose: Remind a reader what a development pack holds.
source: 0423/01 §4 (draft)
revision: 001
> A pack names its source and work pass, a goal, a scope, finish criteria, an executor and a reviewer, then one #NN per work item with its acceptance. Compute numbers and stamps it. Release is separate.

form: pack-create
kind: template
purpose: Build a new pack draft on the linked N5NN pass from its N4NN source.
source: 0423/01 §4 (draft); the 0423→0526 relation is the registered source→work relation
revision: 001
fields: see `pack.forms.json` → `pack-create`. Intent, note dispositions and repeating `item` (#NN by compute).

form: pack-revise
kind: template
purpose: Change one existing item of an unfrozen pack draft, keeping its #NN and the earlier revision.
source: 0423/01 §3 revise (draft)
revision: 001
fields: the item to revise (a semantic reference chosen by intelligence; compute resolves it), the changed fields, and the reason.

form: pack-check
kind: schema
purpose: Check a built pack draft before review.
source: 0423/01 §4 (draft)
revision: 001
checks: every required field is answered in an accepted way; #NN is contiguous; every declared note has a disposition; the dependency states are present.
