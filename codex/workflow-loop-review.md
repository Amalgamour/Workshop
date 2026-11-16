# Workflow loop .002 review and decision queue

State: historical review of `.002`, 2026-11-11. The [`.003` draft](../workflow-loop.003.md), [drafting notes](../workflow-loop.003-notes.md) and [decision record F](../decisions.md#f-workflow-decisions) now carry the disposition.

axioms: 1.4.6.7.8.9

## Evidence in this checkout

- [Root workflow draft](../workflow-loop.md) identifies itself as `.002` and attributes S01–S12 and four choices to the Director. Its predecessor is available at [director/workflow-loop.001.md](../director/workflow-loop.001.md), alongside the [original workflow](../director/workflow-loop.md).
- The [`.002` drafting notes](../workflow-loop.002-notes.md) are now available in this checkout. They list all twelve accepted directions and attribute approval to the Director on 2026-11-11. They also list the four choices: delegated promotion within approved N4 scope, risk-proportional evidence, risk-based N7 with mandatory trial for governing changes, and lowercase `w01` keys. The notes identify the full `.002` draft as awaiting Director review.
- [Fable's repository review](../claude/workflow-loop-review.md) identifies nine findings and flags dependencies on open decisions. The [supplied consultation](https://chatgpt.com/library?file_id=libfile_a058db50203c8191bd04aba411b30c14&account_id=personal) adds proposed resolutions and F10. The addition of the notes resolved F01's missing-file finding. Decision F.1 now records the S01–S12 entries and references.
- The table below indexes the directions against the draft. Use the notes and draft to prepare the decision entries with their why, scope and revision. Where the source does not establish a why or approval reference, mark the gap `7` for the Director.

| ID | Direction described in the draft | Draft section |
|---|---|---|
| S01 | Identify the approved N4 revision, frame, grant and approval. | §4 |
| S02 | Require inspectable evidence proportionate to risk. | §§3.1, 6.2 |
| S03 | Close at the bare counter and store the outcome separately. | §§6, 6.3 |
| S04 | Distinguish a passed pack, a completed MVP and authorized promotion. Bound delegation to the approved frame. | §§4, 7 |
| S05 | Specialize the workflow band map and distinguish band counterparts from continuation. | §§2–3 |
| S06 | Derive a read-only handoff from pinned records, sources and acceptance criteria. | §7 |
| S07 | Use lowercase `w01`, `w02`, and so on as card keys. | §5.2 |
| S08 | Distinguish dependency, modify and create targets. | §8 |
| S09 | Count passes against the approved frame and repeated blocker. | §9 |
| S10 | Require evidence review by another view and an N7 trial for governing changes. | §§6.3, 8 |
| S11 | Claim atomically and record recovery terms. | §§6, 6.4 |
| S12 | Use separate N4 question and N5 execution boards with explicit references. | §4 |

## Proposed changes and how to check them

| ID | Proposed change and why | Check before seating |
|---|---|---|
| F01 | Use the available drafting notes to record S01–S12 in `decisions.md` with individual whys and approval references. The workflow's future grant record should link the approval, N4 revision and frame explicitly. | A reader can trace each entry to its approving authority and exact revision. A missing reference produces `7.8`. |
| F02 | Limit the default N3 build / N4 dev / N5 jobs / N7 colab map to `0100–0999`. A user band adopts the mapping by name. This preserves the user space allocated by A2.7. | `1000` remains the first user band head. A user band's rules apply until the band explicitly adopts the workflow template. |
| F03 | Draft an explicit A2.6 amendment. Use matching `N` and `NN` for discovery and reciprocal Face 08 links for membership. Reconcile the build-band example and affected A6.1 wording. | Matching `0423` and `0523` can be found as candidates. Only a lawful record establishes membership under the amendment. Continuation still follows `PP99` and its explicit links. |
| F04 | Give blocked and needs-authority cases a builder return. On authorized recovery, Compute fences the old claim and records a system return using verified facts and missing evidence. All outcomes go through review before closing. | Replay shows `open → return → review → bare` for each outcome. A revoked claim's late return cannot overwrite the recovery record. |
| F05 | Preserve pass-4 gravity checks at pass 5. At the pass-6 halt, record the Director's decision on that frame as continue, revise, delegate or stop. A continuation carries a bounded allowance and keeps the prior counts. | An explicit reply to the recorded halt can resume the named frame. Unrelated conversation and a stop decision leave the halt in force. |
| F06 | Compute derives a minimum risk from target class, operation, grant and governing metadata. The lead can raise it based on impact and uncertainty. | A low lead rating cannot lower the floor. An unknown target raises a classification finding. The scoring rubric and thresholds remain `7`. |
| F07 | Define governing changes through registered records and affected behavior, including address grammar, kernel contracts, type definitions, authority, inheritance and lifecycle. This gives mandatory N7 and promotion scope a testable trigger. | A registered target or declared governing behavior triggers stricter review. Unclassified or disputed effects go to review. The target registry and routine eligibility remain `7`. |
| F08 | For Compute-owned writes, authorize before execution and record the result. For Git or filesystem work, check the intended grant before work and verify actual changes against the recorded baseline afterward. Preserve evidence of deviations and block acceptance pending remediation. | An out-of-grant change is caught even if absent from the return. Include additions, removals, renames and untracked files. Existing unrelated changes can be distinguished from work under the pack. |
| F09 | Use proportional review. Proposed R1 is a separate reviewer for routine work, R2 starts from approved criteria and artifacts in fresh context, and R3 records a hostile N7 trial for governing work. Capture builder/reviewer identity, context and evidence. | The review record shows what the reviewer saw and tried to break. E7 still needs a decision on whether a fresh session of the same model satisfies the trial rule. |
| F10 | Bind promotion to exact reviewed artifacts, the approval and frame, the evidence and any required N7 trial. Include exclusions and unresolved issues. This prevents promotion from picking up unrelated workspace changes. | An artifact changed after review or absent from the manifest cannot pass verification under that review. The handoff manifest continues to serve the builder's input needs. |

## Dependencies and editing order

1. **Authority and geometry (F01–F03).** Prepare the decision entries from the available notes and flag any missing approval details. Draft any A2.6 change as an explicit amendment and carry its effect into SeqAddr only through the authorized change path.
2. **Execution (F04–F07).** Before specifying a state machine, settle recovery authority and fencing, the gravity event and allowance, the risk rubric, and governing target classification. Define how `blocked` and `need` work-card results inform counter outcomes, who initiates review, and how a reviewer claim is recorded.
3. **Verification (F08–F10).** Define the repo baseline and scope of diff inspection, review identity under E7, and the exact artifact and authority requirements for promotion. Trial cases should include an unrelated dirty file, a stale claim, a changed artifact after review, and a governing code change with no governing document edit.

`7` The draft still relies on E8 written permission, E9 return placement and `continues-from`, and an unrecorded `3MC` band default. Resolve these explicitly. The claim may be the E4 raise point for a builder who differs from the lead, pending agreement. Clarify the handoff terminology in the proposed read path, define or remove the example's `placed` field, use a resolvable `reason` example, correct the §6 code fence and use the §6.1 and §7.1 SeqAddr references. Keep E9's task/ticket counter split separate from S12's separate boards.

When authorized to draft `.003`, start from the exact `.002` source, record the change notes, apply and strike them, reread the whole draft and send it for Director review. Record each dependency still missing as `7` and each required trial still outstanding as `9`.
