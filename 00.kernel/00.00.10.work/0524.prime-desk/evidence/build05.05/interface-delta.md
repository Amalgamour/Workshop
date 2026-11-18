# Interface delta — prime-desk-pass03 to prime-desk-pass04

Schema: prime-desk-interface-delta/0505
Date: 2026-11-01
Executor: Grok-1

Written before the pass04 code. The commands and the request schema do not change.

| Surface | pass03 | pass04 |
| --- | --- | --- |
| View command | `view --request ABS [--json]` | same |
| Packet command | `packet --request ABS --work-id ID [--json]` | same |
| Request schema | `prime-desk-request/2` | same |
| View schema | `prime-desk-view/3` | `prime-desk-view/4` |
| Packet schema | `prime-desk-packet/3` | `prime-desk-packet/4` |
| `record.supplied_without_worker` | JSON only | JSON, and a `Supplied context` block in the markdown |
| `## Brief` | absent | present on every non-refusal markdown view |
| Synthetic `review-loop` operation | always appended | appended only when no declared operation is named `review-loop` |
| Selection rule | assignment-record/v1 | same |
| N5NN and N7NN routes | as in the 05.03 contract | same |
| Escalation string | names `0524.prime-desk/05.03` | names `0524.prime-desk/05.04` |

`executed` on every operation row remains false. A declared review-loop limitation is the request's text. The synthetic limitation remains `Pending. Successor modules were not imported.` when the row is still synthesized.

Pass03 files are not edited. A pass03 request still renders with pass03. A pass04 request is a new file under `labs/prime-desk-use-pass02`. The use-pass01 request is left as its own cut.
