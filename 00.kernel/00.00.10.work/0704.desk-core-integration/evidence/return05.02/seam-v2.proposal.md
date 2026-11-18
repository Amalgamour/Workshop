# Integration seam v2 — PROPOSAL
date: 2026-10-31
who: claude-opus-5-5 (Claude), Colab 0704/05.02; for Codex Prime
state: **proposal only.** Not active, not seated, not approved. Seam v1 (0417.return-placement/evidence/integration-seam-v1.md, sha256 45df713b…d55b) stays the frozen input of the active 0521/05.03 and 0522/05.03 builders. This text is read beside v1. It does not replace v1 beneath them.
Exact delta: seam-v1-to-v2.md (same folder).

Each section is tagged with its basis:
- **[policy]** an adopted Director decision, cited;
- **[Prime]** a Prime technical disposition, cited;
- **[proposed]** detail proposed in this pass, which Prime can accept or change;
- **[open]** a Director choice that is still unresolved.

---

## 1. Scope
This is an adapter contract between the custody writer and reader (the 0521 lane) and review consumers (the 0522 lane). It adds:
- two read and placement variants: legacy-in-place and staged seal;
- a placement status;
- a rule for consuming the review binding across a mechanical relocation;
- successor-review record fields;
- a minimal result and refusal envelope.

It creates no address axis, no permission and no new custody writer. Section 8, Prime report state, consumes the seam but is not part of it.

## 2. One writer, several readers [Prime: 06.01.review F2]
- **Writer.** An active work book has exactly one custody writer for new returns: the canonical return-line tool (0521). That writer produces both final line tails and staged seals (§4). The old sequential `return_capture.py reserve` is not a writer for new work in a book that declares this layout.
- **Readers.** Readers exist for every historical format. A reader never writes, and reading an old format never makes it a write format again.

| custody_format | Who writes | Who reads | Placement |
|---|---|---|---|
| `return-capture/1` in place → descriptor `legacy-in-place/1` | nobody (historical, sealed) | pinned `return_inspect.py` via the adapter | pending |
| `legacy-relocated/1` (v1) | 0521 migration (copy only) | 0521 lookup | final |
| `return-line-capture/1` (v1) | 0521 writer | 0521 reader | final |
| `staged-seal/1` | 0521 writer | 0521 reader | pending |

## 3. Descriptor `return-line-descriptor/2` [proposed]
Exact keys: the 15 v1 keys, plus one new key, `placement`.

`placement` has exactly these keys:
- `status`: `final` or `pending`;
- `intended_target_page`: the N1NN.subject page from the v1 route rule. For N7NN it is the page itself.
- `intended_return_path`
- `relocation_record_path`: null until a verified relocation exists; then the path of that record.
- `occupancy`: null, or the different-name occupant(s) of the intended number, as observed by the 0521 plan.

**Meaning of the v1 location keys in /2.** `target_page`, `return_path`, `custody_path`, `receipt_path` and `manifest_path` name where the sealed bytes **are now**. `placement.intended_*` name where they will be filed. For `final` the two are equal.

**`custody_format` values in /2:** v1's `legacy-relocated/1` and `return-line-capture/1`, plus `legacy-in-place/1` and `staged-seal/1`.

**`state`:** unchanged (`complete`, `reserved`, `incomplete`, `conflict`). It describes custody integrity only. `complete` never means filed, reviewed or accepted [Prime F6].

**`verification`:** unchanged. It must name the actual reader that checked the bytes: the pinned `return_inspect.py` for legacy-in-place, and the 0521 reader for the others.

A v1 descriptor stays valid. A /2 consumer reads /1 as `placement.status = final` with `intended_* = actual`. A /1 consumer refuses /2: exact keys, by design (§9).

## 4. Variants
### 4.1 `legacy-in-place/1` (read-only) [Prime F3 + proposed]
- **Source:** a sealed `return-capture/1` member at its original `01NN.slug` address, never moved.
- **Emitter:** the 0521 adapter, read-only. It calls pinned `return_inspect.py inspect --member <01NN.slug> --json` and maps the result.
  - `return_path`, `manifest_path` and `receipt_path` are the member's real files.
  - `custody_path` is the member folder.
  - `receipt_sha256` is the hash of the actual receipt bytes.
  - `origin` comes from `reservation.json`, never from the folder name.
- **Never writes,** whether to the member, the wrong line or anywhere else. It allocates nothing.
- **Placement:**
  - `pending`;
  - `intended_*` from the v1 route of `origin`;
  - `occupancy` copied from the plan if known, otherwise null;
  - a `reserved` or `incomplete` inspection yields that `state`, and the old id stays visible.
- **Consumers** may review a `complete` legacy-in-place return now. Its custody is valid and its filing is pending; both facts are shown.

### 4.2 `staged-seal/1` (approved interim sealing) [policy: 0417/06.04 + proposed detail]
- **Purpose:** preserve a pending new return while its matching line is occupied or awaiting migration.
- **What it is not:** final filing, review or acceptance. It must not become another permanent route.
- **Location (proposed), one work-local place:**
  ```text
  <source page>/evidence/return-staging/05.NN/sMM/
    return.md
    payload/0001.blob ...
    manifest.json
    receipt.json
    staging.json
  ```
  - `<source page>` is the N5NN work page whose pass this is.
  - `sMM` is the seal version: s01, s02 and so on, the next free number on that pass.
  - The path is labelled in its name and lives under evidence, so nobody mistakes it for a return line.
  - N7NN never uses it; its page-local tail rule stands [policy].
- **Bytes:** the return and payload use the same shape and hashing as `return-line-capture/1`, so that relocation is a byte copy.
- **Requirement on 0521's format:** the receipt and manifest must not embed their own physical path. Location lives in `staging.json` and in the relocation record. This is unverified: the format is not in the packet.
- **`staging.json` exact keys:**
  - `schema` `staged-seal/1`
  - `origin` {book, page, batch}
  - `submission_id`, `seal_id`
  - `supersedes_seal`: null, or the earlier sMM on the same pass
  - `intended_target_page`, `intended_return_path`
  - `status`: `placement-pending`, or `relocated` (see the relocation bullet below)
  - `sealed_at`
  - `receipt_sha256`
  - `writer` {tool_path, tool_sha256}
- **Versions:**
  - A changed submission makes a new seal (s02) with `supersedes_seal`. Earlier seals are never overwritten [policy: "preserve versions"].
  - Identical bytes for an existing seal_id are idempotent.
  - Different bytes under the same seal_id are refused, as `identity-conflict`.
- **Relocation (later, after the line is free):**
  - The 0521 writer copies the seal into the final line tail and verifies it byte-equal.
  - It writes `relocation.json` beside the final custody, with exact keys: `schema` `staged-relocation/1`, `from` {path, receipt_sha256}, `to` {path, receipt_sha256}, `verified`, `verifier` {tool_path, tool_sha256}, `relocated_at`.
  - It then writes one exclusive `relocated.json` pointer into the seal folder. The seal's earlier bytes stay unchanged.
  - Staging bytes are kept until Prime accepts their retirement, as for occupants in 0521's migration.
- **Three facts kept apart:** immutable preservation (`staged-seal/1` with a receipt), final filing (`placement.status final` with a relocation record) and acceptance (a review disposition plus Director authority) are recorded separately. None implies another.

## 5. Consuming the review binding [Prime F4/F7/F8 + proposed]
Three identities, with three purposes. They are never substituted for one another:
- **Address:** origin book/page/pass. It says which work.
- **Material binding:** `review-task-binding/2` (0522). It says which task, evidence, agreement and receipt the judgment covered.
- **Write token:** the target file's sha256 for compare-and-swap. It guards one physical write.

**Consumer rules:**
1. The consumer computes binding/2 itself, from the page and the descriptor. A descriptor or caller never supplies a trusted binding.
2. **Relocation equivalence [proposed].**
   - binding/2's preimage includes receipt placement, member and page-local name (0522 CONTRACT RC-03, pack05.01 snapshot 0015). So a pure relocation changes the binding.
   - When a stored binding and the current binding differ **only** in those location fields, and a verified `relocation.json` (or the 0521 legacy relocation record) links the two receipt locations with an equal `receipt_sha256`, the consumer reports `current-via-relocation`, naming the record.
   - Any other difference is stale.
   - *Alternative:* a future `review-task-binding/3` without location fields. Not proposed now, because 0522 is active.
3. **Freshness is computed on read and never stored** as a verdict on a page [Prime F8]. The read reports `current`, `current-via-relocation`, `historical` (with the reason: task, evidence, agreement, receipt or origin changed) or `unknown` (with the reason: evidence missing, reader failed).
4. **Missing evidence stays missing.**
   - A `reserved` or `incomplete` descriptor, or an absent receipt, means binding is `not-computable`. It is never treated as an empty-file hash, and never as a pass.
   - A receipt that answers an older task is `historical`. It is never rebound silently to revised work.

## 6. Successor reviews [Prime F5 recommendation; layout open: DC3]
**Record fields (proposed; independent of the page layout).** The typed review record gains:
- `review_id`;
- `supersedes`: null, or a review_id;
- `answers`: a list of entries with exact keys:
  - `question_id`, `question_revision`, `question_sha256`
  - `reply_text`: verbatim
  - `reply_source` {path, heading_or_line, file_sha256}
  - `attributed_to`
  - `recorded_by`

**Rules:**
- An answer must match an open hold's `question_id`, `question_revision` and `question_sha256`. A mismatch is `identity-conflict` (§7). It is never re-attached to another question.
- The prior review's record and readable text are kept byte for byte.
- **The current review** is the single head of the `supersedes` chain whose binding is current or current-via-relocation.
  - Two heads is `identity-conflict`. Compute does not choose.
  - A held review stays the head until a successor exists.
- A hold blocks only its own `dependent_scope` actions. Unrelated next actions stay available [Prime F6].
- `next_action` may be the declared waiting action, for example actor `director`, action `answer Q1`, or null when no action is supplied. It must never be an invented step [Prime F5].

**Page layout.** **[open: DC3]** Prime recommends same-home succession: the original kept in place; the verbatim answer bound to its question; then the successor, inside the same workflow home. For N7NN that home is `06.NN.review.md`. The alternative is a separate answer page linked from the home. Until the Director chooses, a renderer that meets a substantive existing review must refuse with route `escalate: DC3 successor layout undecided`, keep the new review in its typed record, and keep the old text intact. No syntax is adopted here.

## 7. Minimal result and refusal envelope `operation-result/1` [Prime F10 + proposed; not law]
Every operation prints one object. Only an attempted **write** that is refused or fails also persists it, beside the preserved request:
```text
<source page>/evidence/trace/05.NN/<op_id>.json
```
Read-only operations persist nothing.

**Exact keys:**
- `schema`, `op_id`, `operation`
- `outcome_class`
- `rule` {contract, version, section}: the rule actually applied; `null` only for `success`
- `observed` {check_id, expected, actual}
- `preserved` {request_path, request_sha256, partial_paths}
- `sources` [{path, sha256, role}]
- `route` {kind: `none` | `correct` | `help` | `escalate`, to, text}
- `result_ref`

**`outcome_class` values:** `success`, `mechanical-refusal`, `incomplete-evidence`, `identity-conflict`, `unknown-capability`, `missing-authority`, `unexpected-failure`.

**Semantic disagreement is not a compute outcome.** Compute never refuses on meaning. A disagreement is recorded by intelligence as a finding or hold with `route.kind = escalate`. Where a compute check is silent, the operation proceeds or reports `unknown-capability`. It does not invent a rule [policy: 0416/01.003].

## 8. Prime review report state (consumes the seam; outside it) [policy: 0412/06.02 + proposed fields]
This is recorded on the workflow page's Prime review and in its typed record. It is not authentication, not a read receipt and not approval.
- `mode`: `normal` or `delegated-solo`.
- `grant_ref` {path, section, sha256}: **required** for `delegated-solo`, and must point to a recorded explicit Director delegation. If absent, the mode is `normal`. A hypothetical example is never a grant [policy].
- `review_status`: `in-progress` or `complete`.
- `report` {status, report_ref, delivered_via, delivered_at}:
  - `status` is `not-delivered`, `delivered` or `internal`;
  - `report_ref` is the {path, sha256} of the exact report text kept on the page;
  - `delivered_via` is, for example, `chat`.
- `decision_pending`: a list of {question_id, question_sha256, dependent_scope}.

**Rules:**
- `normal` with `complete` and not `delivered` is surfaced as Prime's own next action: "report to Director".
- `delegated-solo`: internal reviews may be `internal`. The task's final report must reach `delivered`.
- `decision_pending` holds only its own `dependent_scope`.
- `delivered` means Prime presented the text. It is not acknowledgment. Silence is not approval [policy].
- No routine technical fix waits on a report [policy].

## 9. Compatibility
- The v1 descriptor stays readable by /2 consumers; /1 consumers refuse /2 (exact keys).
- `return-capture/1` members are never rewritten. Legacy-in-place reads them through the existing pinned reader.
- 0521/05.03 and 0522/05.03 continue against v1. Adopting v2 is a later, separate pack.
- No consumer may treat `state: complete` as filed, reviewed or accepted.
