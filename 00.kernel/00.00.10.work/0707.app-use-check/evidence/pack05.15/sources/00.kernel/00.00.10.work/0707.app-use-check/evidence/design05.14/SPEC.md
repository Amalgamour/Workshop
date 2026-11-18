# Task-agreement reference contract — specification v2 (0707/05.14)
who: claude-opus-5-5 (Claude), Colab design/labs · state: **PROPOSAL for a future builder.** It supersedes `design05.13` (preserved byte-identical). It applies Prime's 06.13 review R1–R5 as technical directions. **No kernel law, no release rule, no approval ledger.** Reference lab: `labs/task-agreement-reference-pass01`.

## 1. What it is
- **A passive reference resolver.** A pack names *where* its goal, scope, finish criteria, Prime discretion, Director-required boundaries and recorded decisions are written. Compute resolves and measures those places and reports **field states with evidence.**
- **It applies no release, terminal or hold rule of its own** (R1). A host such as the review core may apply its own **declared** policy (for example the existing 0412 source-bound holds) to the states.
- **A resolved Director-text and proposal pair is inspectable evidence, not authenticated approval** (R2).

## 2. Inputs and outputs
| Step | Input | Output | Writes |
|---|---|---|---|
| construct | explicit choices JSON (intelligence), book root, page, pass | block text plus provenance | **only** a NEW output file (occupied → refuse) |
| assemble (authoring tool's job; the lab demonstrates it) | pack text, block text | the pack with `## Task agreement` + fence inserted before `## Return pointer` | a NEW output file |
| bind | book root, page, pass, optional `--profile` | a binding record (§5) | a NEW output file |
| inspect | a binding file | a readable view | **none** |
| compare | a binding file, book root | a per-reference status (§6) | **none** |
| reconcile-request | binding, proposed change, reason, attribution | a request record; **never applied** | a NEW output file |

## 3. The block (inside the pack; references only)
````text
## Task agreement
```task-agreement
{"schema": "task-agreement/2",
 "for": {"page": "0599.fixture-task", "pass": "05.02"},
 "fields": {
  "goal":              {"state": "cited", "refs": [{"source": "self", "heading": "Goal"}]},
  "scope":             {"state": "cited", "refs": [{"source": "self", "heading": "Scope"}]},
  "finish_criteria":   {"state": "not-applicable", "reason": "…"},
  "prime_discretion":  {"state": "cited", "refs": [{"source": "0412.prime-review/01.md", "heading": "Local work agreement", "applicability": "standing"}]},
  "director_required": {"state": "cited", "refs": [{"source": "0412.prime-review/evidence/director-agreement.md", "whole": true, "applicability": "standing"}]},
  "recorded_decisions":{"state": "cited", "decisions": [{"record": "…/06.08.md", "verbatim": "Director - verbatim",
                          "interpretation": "Prime - exact proposal this reply approves",
                          "answers": {"source": "same", "heading": "Prime - exact proposal this reply approves"}}]}},
 "semantic_findings": [{"between": ["scope", "recorded_decisions[0]"], "finding": "…", "by": "Codex Prime"}],
 "gloss": {"text": "…", "by": "…"}}
```
````

- **The block holds NO hashes** (D1). A `sha256` key anywhere in the block is refused, so no pack hash can contain itself.
- **Source namespace:** book-relative paths `PPPP.title/…` under the selected work-book root, or `self` (the pack). No absolute paths, `..`, links or junctions. A different book instance is a different namespace.
- **Cut syntax:** `heading` (the exact text after `## `, which must occur exactly once **outside code fences**; the cut runs to before the next real `## ` line) or `whole: true`. Raw bytes are kept as stored, CRLF or LF. The pack must decode as strict UTF-8.
- **Supplied states** (distinct; each with its limits):
  - `cited` needs refs or decisions;
  - `unknown` means the source is not known;
  - `none-recorded` (recorded_decisions only; needs a reason) means **Prime declares that none applies. It is not proof that none exists anywhere;**
  - `not-applicable` needs a reason.
- **A decision** has a verbatim cut ≠ an interpretation cut, and an answers cut. **The answers scope is the cited question or proposal only.**
- **`semantic_findings`** are intelligence findings, stored attributed. Compute never computes or clears them (R2).

## 4. Block generation and self-reference
The authoring tool constructs the block from the choices, inserts it, and only **then** is the pack frozen. `bind` measures the **pack cut** (bytes before `## Return pointer`) and the sources. Because the block has no hashes, and the Return pointer and Review lie outside the cut, the tool's later writes never change the bound pack cut. **This is observed in lab case T01.**

## 5. Binding record (`task-agreement-binding/1`)
It records:
- the book instance (the lab uses the sha256 of the resolved root path; production reuses the core's `instance_id`), page and pass;
- the pack file sha256, the pack cut sha256 and its bytes;
- the block present or absent, with the block sha256;
- the profile, if one is used;
- per field: the declared state plus, per ref, `{source, cut kind, heading, record_sha256, record_bytes, cut_sha256, cut_bytes, count, status, raw_cut_b64}`;
- per decision: the verbatim, interpretation and answers cuts, plus a pairing status;
- `structural_findings` (compute) and `semantic_findings` (attributed, as supplied);
- `policy: "passive"`;
- the tool sha256 and the input provenance.

**A `self` reference's record identity is the pack cut** (`record_basis: pack-cut`), not the whole pack file, so the tool's own Return-pointer and Review writes never look like context drift (found by lab case T01, run02).

**Immutable once written** (R3). A new binding is a new file and a new revision, and the earlier one stays. In production, the intake record links the binding; **a review that adds agreement evidence gets new identities, and old hashes are not preserved by pretending nothing changed.**

## 6. Compare (read-only) statuses per reference
| Status | Meaning |
|---|---|
| `current` | the record and the cut are byte-identical |
| `cut-changed` | the cut bytes differ |
| `context-changed` | the cut is identical but the **whole record** differs. Applicability is unconfirmed until reconciled (a revocation may sit outside the cut; R5) |
| `missing` | the record or heading is gone, or the count ≠ 1 |
| `instance-mismatch` | a different book instance; **refused, never treated as the same** |

The pack cut is compared the same way. **Compare never rebinds and writes nothing.**

## 7. Failure and correction
- **Exit codes:** 0 ok; 1 completed with findings (compare drift; unresolved refs); 2 refusal (bad shape or encoding, escape or link, occupied output, a hash in the block, instance mismatch).
- **Every refusal names the field or ref, the reason, and a correction hint.** A refusal is mechanical; **it is not a rejection of the idea.**

## 8. Compatibility (R4)
- **A pack without a block** is reported `block-absent`, and every field `unknown` **unless** a compatibility profile is explicitly selected.
- **A profile** (for example `profiles/legacy-headings-v0.json`) maps **exact** headings to fields and is labelled `provenance: profile`. It never fuzzy-matches and never creates decisions.
- **Its match to the core's currently recognized format is unconfirmed** (D5): a builder item.
- **Existing valid bindings are never erased or rewritten.**

## 9. Host policy seam (R1)
- The resolver output feeds the host's **existing declared policy.** For the review core, that is its current agreement-attention list and the 0412 source-bound holds.
- **The resolver does not decide** what an `unknown` blocks. If Prime later wants a new policy (for example "a release needs a cited scope"), it is a separate, named host policy with its own record. **Possibly a Director decision; not introduced here.**
