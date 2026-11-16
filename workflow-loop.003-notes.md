# Workflow loop .003 drafting notes

State: drafting and read-back record. `9` hostile trial pending.

axioms: 1.4.6.7.8.9

The Director's instruction on 2026-11-11, “Ok approved, write workflow-loop.003 now”, authorizes recording the prior S01–S12 decisions and drafting `.003` from the reviewed correction queue. The predecessor is [the root `.002` draft](workflow-loop.md). Its [drafting notes](workflow-loop.002-notes.md) record the original S01–S12 approval. The [Codex review](codex/workflow-loop-review.md) indexes Fable's review and the supplied follow-up consultation, including F10.

## Change notes

| Item | Change and why |
|---|---|
| F01 | ~~Record S01–S12, approval and rationale.~~ Applied in `decisions.md` F.1. The approval is for design directions. Each N4 runtime grant needs its own authority record. |
| F02–F03 | ~~Scope the map and draft the A2.6 amendment.~~ Applied in `.003` §§2–3 and proposed decision F.2, including A6.1 alignment and explicit user adoption. Candidate discovery and lawful membership have different effects. |
| F04 | ~~Give every terminal outcome a reviewed return path.~~ Applied in §6. Preserve the return after authorized fencing and record violations so review can act on them. |
| F05 | ~~Define pass 5, the pass-6 halt and resumption.~~ Applied in §9. The authority can respond on the named frame. A one-release default for “carry on” is proposed. |
| F06–F07 | ~~Set a Compute risk floor and define governing changes.~~ Applied in §5.3 through registered targets and declared behavioral impact. Keep classification data and calibration open. |
| F08 | ~~Distinguish controlled writes from external verification.~~ Applied in §§3.1 and 8. Preserve evidence and block acceptance while violations are unresolved. |
| F09 | ~~Record reviewer identity, context and trial scope.~~ Applied in §6.3. E7's general identity question remains open. |
| F10 | ~~Bind promotion to exact reviewed source and SeqAddr revisions.~~ Applied in §7.1. The promotion manifest pins publication. The handoff manifest supplies builder inputs. |
| Related fixes | ~~Repair the lifecycle fence, work-card example and section references.~~ Applied. E8/E9 and the default lead dependencies are marked where used. Review initiation and outcome evidence appear in §6. |

## Director clarification

The Director described `05.NN` as one Kanban card moving through `draft → pack → open → return → review → closed`, with each stage completing its work on the same card. ~~Make the board, card identity, and handoffs explicit in §6.~~ Applied. This clarifies S03 using the counted-face board in A4.4.

## Additional issues for Director review

1. **Recording a failed return must remain possible.** The `.002` lint table could leave a violating or incomplete return stuck `open`. `.003` distinguishes receipt of an adverse record from acceptance of its work. If the log publishes the return and its state transition independently, a crash can still strand the counter. `7` requires a single logical durable transition or an explicit restart protocol before production use.
2. **A Git diff cannot establish who changed a shared file.** A baseline can expose differences, including previously dirty files, while concurrent writers can still produce ambiguous attribution. Use an isolated worktree or exclusive workspace as an implementation option. With a shared baseline and unclear attribution, record the uncertainty and hold acceptance.
3. **Pass counting needs a transaction boundary.** A retry, parallel release, or renamed blocker must not let a frame evade its halt. `.003` proposes counting a successful release to `pack` once under the frame and tracking blocker history separately. `7` covers the release transaction and blocker continuity across revisions.
4. **An exact manifest can become stale during promotion.** The check and publication need revision guards, including across Git and book logs. `7` covers partial publication and reconciliation before enabling promotion that spans those stores.

## Read-back

Read back against `.002`, the numbered decisions and the SeqAddr rules. A1/A2 address shape, A2.5 tail spelling, A4.4 counter boards and A5/A6.1 continuation geometry carry forward. F.2 identifies the A2.6/A6.1 amendment for review. E8 and E9 remain open where the draft depends on them. The original `.002` draft and the Director's predecessors are preserved. The review cases below describe expected behavior. `9` marks the outstanding hostile trial.

## Review cases

| Attempt | Expected behavior |
|---|---|
| Follow a single job from draft through closure. | The `05.00` board shows one card with the same `05.NN` identity in its current column. Each move leaves a record of the work completed for that handoff. Closed displays the bare counter and its recorded outcome. |
| A user band exists at `1000`, and two standard band pages match by subject digits. | The user band keeps its own definition. Under proposed F.2, the matching digits identify candidates and reciprocal Face 08 links establish membership. |
| Two builders claim a pack, and the first accepted claim later goes stale. | Exactly one wins. Authorized recovery records a system return. The revoked claim's late return is rejected. Replacement uses a new counter. |
| The builder returns a valid record containing an out-of-grant edit, or Compute stops midway through recording a return. | Review can inspect the adverse evidence and withhold acceptance. Interruption must recover to a consistent return and tail before production use. |
| Two releases compete for the last authorized pass, or the same release is retried. | The frame consumes at most one allowance for that release. No release bypasses the recorded halt. |
| A repo diff includes a pre-existing dirty file, a rename outside the grant, or an edit by a concurrent writer. | Preserve the baseline and evidence. Check both rename paths. Raise uncertain attribution before accepting the return. |
| A small code change alters authority behavior while the lead rates it low. | Registered behavior and Compute's floor govern the check. Governing promotion requires the recorded N7 trial. |
| A promoted artifact or its expected live predecessor changes between review and publication. | The revision guard stops publication under that manifest. Mixed-store interruption needs reconciliation before this form of promotion can run. |
