# Implementation brief — attaching task agreements to the workbook review intake (0707/05.13)
who: claude-opus-5-5 · state: proposal for a later bounded build. **The names are illustrative. No code was written or run, and the live core is unchanged.**

## Seam
The existing intake already resolves `book_instance + page + pass` into an intake id, and it already emits `attention: agreement.* is unknown`. **Replace only the agreement lookup:**
- today: "the selected source-heading format";
- proposed: read the `task-agreement` block from the pack cut.

**Reuse the same instance, intake and review identities.** No new queue, current-assignment store or approval system.

## Responsibilities
| Step | Input | Output | Invariants |
|---|---|---|---|
| prepare | book instance, page, pass | `agreement: present / absent` plus the parsed block, or a parse refusal | read-only; absent ≠ error |
| bind (at intake) | the parsed block | per field: cuts measured (path, kind, heading, count, sha256, bytes) and state; decision pairings checked | stored inside the intake record; **immutable** |
| read | intake id | the agreement view (states, cuts, holds), with the current re-measurement giving `stale` where it applies | **no writes;** no rebinding |
| reconcile-request | intake id, field, proposed cut, reason | an append-only request record under the same intake | **never applies itself;** Prime or the Director decides |

**The holds table** (declaration `holds`) feeds the existing `releases_action`, `closes_work` and `goal_terminal` checks. **An unknown or stale field blocks only the acts that depend on it.**

## Compatibility
- **Old packs (no block):** `agreement: absent`, all six fields unknown, the same as today's behavior, but **with a precise reason** instead of a generic attention list. No migration. No retroactive authority.
- **Optional retrospective citation:** Prime may record cuts for an old pack in the review's evidence, labelled `retrospective`. It is a citation, not a grant; it never edits the old pack.
- **Code payloads,** if ever cited, keep the Director's `02.filename.VVV.filetype` convention. None is needed here.

## Acceptance for a later build (each NOT RUN here)
- examples a, b, c1–c3 bind or report exactly as `examples/views` specify;
- the real-batch application measures the same hashes;
- **F1–F10 behave as in `FAILURE-CASES.md`;**
- intake and review identities are unchanged;
- **no write on read.**
