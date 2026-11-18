# Seam v1 → v2: exact proposed delta
date: 2026-10-31
who: claude-opus-5-5 (Claude), 0704/05.02
state: **proposal.** Base: `0417.return-placement/evidence/integration-seam-v1.md`, sha256 45df713ba192dbe5f9a74c0e238b403a696020191225309d2cf38b2a2154d55b (frozen; unchanged by this pass). Full text: seam-v2.proposal.md.

## A. Descriptor schema
| v1 | v2 | Change | Compatibility |
|---|---|---|---|
| `schema: return-line-descriptor/1` | `return-line-descriptor/2` | new identifier | /2 consumers read /1; /1 consumers refuse /2 (exact keys) |
| exact keys: schema, origin, route, target_page, return_path, custody_path, receipt_path, manifest_path, submission_id, custody_format, receipt_sha256, return_sha256, return_bytes, state, verification | same 15 **+ `placement`** | ADD 1 key | a /1 descriptor is read as placement.status final, intended = actual |
| — | `placement` = {status, intended_target_page, intended_return_path, relocation_record_path, occupancy} | NEW object, exact keys | `status` ∈ {final, pending} |
| `origin` {book, page, batch} | unchanged | — | read from reservation/staging record, never from a folder name |
| `route` ∈ {matched-workflow-return-line, page-local-colab} | unchanged | — | describes the *intended* route for pending placements |
| `target_page`, `return_path`, `custody_path`, `receipt_path`, `manifest_path`: where the return is | unchanged meaning: **actual current location** | clarified | for final, equal to intended |
| `custody_format` ∈ {legacy-relocated/1, return-line-capture/1} | ∈ {legacy-relocated/1, return-line-capture/1, **legacy-in-place/1**, **staged-seal/1**} | ADD 2 values | other values refused as before |
| `state` ∈ {complete, reserved, incomplete, conflict} | unchanged | — | still custody integrity only |
| `verification` {tool_path, tool_sha256, result, evidence_path} | unchanged | — | must name the reader that actually ran (pinned return_inspect for legacy-in-place) |
| receipt_sha256 = actual receipt bytes; missing → null | unchanged | — | — |

## B. Rules added
| # | v1 text | v2 addition |
|---|---|---|
| B1 | "No arbitrary absolute path overrides, newest version selection or sequential slot." | Unchanged. Also: a legacy-in-place descriptor names the existing old `01NN.slug` member as its actual location; this is **reading**, not allocation. |
| B2 | — | **One custody writer per active book** (0521 tool) produces return-line-capture/1 and staged-seal/1. Readers exist for all formats; reading never re-enables writing an old format. |
| B3 | — | **staged-seal/1** at `<source page>/evidence/return-staging/05.NN/sMM/` with `staging.json` (exact keys in proposal §4.2); versions never overwritten; status placement-pending; N7NN never staged. |
| B4 | — | **Relocation record** `staged-relocation/1` (from, to, both receipt_sha256, verified, verifier, relocated_at) plus a `relocated.json` pointer in the seal; staging bytes kept until Prime accepts retirement. |
| B5 | "Consumers validate … task/evidence binding." | Consumers compute `review-task-binding/2` themselves. **Relocation equivalence:** a difference only in receipt location fields, linked by a verified relocation record with equal receipt_sha256, is `current-via-relocation`. Anything else is stale. |
| B6 | "Wrong/missing sources are refused or held with preserved reasons." | Freshness is read-time only: current / current-via-relocation / historical(reason) / unknown(reason); never stored as a page verdict. Missing evidence makes the binding `not-computable`, never empty-hash. |
| B7 | — | **Successor record fields**: review_id, supersedes, answers[{question_id, question_revision, question_sha256, reply_text verbatim, reply_source, attributed_to, recorded_by}]. A single chain head is current; two heads is identity-conflict. **Page layout: open (DC3).** Until it is decided, a renderer refuses to overwrite and escalates. |
| B8 | — | **operation-result/1** envelope (proposal §7); persisted only for refused or failed write attempts at `<source page>/evidence/trace/05.NN/<op_id>.json`; semantic disagreement is never a compute refusal. |

## C. Outside the seam (consumer side)
| # | Addition | Basis |
|---|---|---|
| C1 | Prime review report state: mode, grant_ref, review_status, report{status, report_ref, delivered_via, delivered_at}, decision_pending | policy 0412/06.02; fields proposed |

## D. Not changed
Routing rule (N5NN→N1NN keeping N/NN/subject; N7NN local); the refusal of undeclared kinds; the meaning of `receipt_sha256`; the instruction that a stated complete result never replaces checks; v1 itself (stays the active builders' input).
