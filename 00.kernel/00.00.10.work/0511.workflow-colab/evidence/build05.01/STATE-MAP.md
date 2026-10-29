# State map

schema: colab-workflow-state-map/1
The map is derived. investigation.json does not store these labels.

## Facts that move a flag

| Fact in the record | Flag that becomes true | Flag that stays false |
|---|---|---|
| Pass opened, package absent or present, closure null | draft | explicit_completion |
| Statement kind release or claim | draft, and the statement is visible | explicit_completion. The statement is not authority |
| return_pointer from a complete verify, no review statement or review text PENDING | custody_complete, review_pending, draft | accepted_without_terminal, explicit_completion |
| includes_prime_review true on the captured return | the boolean is visible | review_pending does not clear |
| Disposition action held, with followup_ref or park | held_followup, draft | explicit_completion |
| Disposition action accepted, closure null | accepted_without_terminal, draft | explicit_completion |
| Disposition action rejected, still in dispositions | draft until a later closure | the finding is not removed |
| Closure object after every finding is disposed | explicit_completion | draft |
| Reconciliation flag blocked for a target | attention reconciliation | a new disposition for that target is refused |
| retain-historical recorded | the historical sha256 is unchanged | retarget is not a state |

## Refusals that write no new fact

| Condition | Result |
|---|---|
| Page outside 0701–0799, including the door 0700 | refused, outside declared band |
| Same page, different identity | refused, occupied different content |
| Same title on another page | refused, duplicate title |
| Same package bytes and digest | repeat, no write |
| Same pass, different package bytes | refused, conflicting bytes |
| expect-digest differs | refused, stale expected hash |
| Statement kind outside release, claim, review | refused, claim/release unknown |
| Inspect status reserved, missing, incomplete, or refused | refused, partial custody |
| Origin page or batch is not the investigation pass | refused, wrong origin |
| Two primary captures | refused, ambiguous custody |
| Retrospective capture without an explicit secondary selection | refused, retrospective capture is secondary |
| Seal missing, lock present, or partial.json present | refused, resume refused. Retained files stay |
| Link, junction, or escaping path | refused before a write |

## Read-only views
`show` and `propose` and `check-subject` do not create a page, do not update seal.json, and do not write 00.live. `show` of a partial page reports the partial and leaves the files.
