# Verification — 2026-10-11

Prototype only. No live batch, kernel face, existing Director reply, or routing policy was changed.

Twelve focused unittest cases passed: preview makes no writes; existing decisions survive allocation; eight concurrent writers get distinct files; missing and ambiguous routes stop; missing/reserved pages are not created; path escape, unknown verbs, missing parameters, absent exact source headings, and cyclic dependencies stop; dependencies precede dependent work; multiline content cannot create new top-level request/reply markers; exhausted numbering does not reuse gaps; even an approval request only produces a draft batch.

The first test attempt encountered sandbox denial in Windows temporary directories. The approved rerun completed all twelve tests. Tests use isolated disposable copies, not the live book.

The complete CLI-format example was previewed and saved as `example-output.md`. The incomplete JSON example was rejected with `Missing text: #01 point.relationship`. No example command was executed.

Kernel linter: 0 reworked errors before and after. Kernel git diff was empty. These counts describe the unchanged kernel, not approval of the proposed contracts. The prototype has its own tests because the current kernel checker does not validate this proposed batch format.

Source grounding: repository AGENTS; syntax design/rules/axioms/gravity/triangulate; law ticket/grammar/compose/page/behavior/write/approve/clean/strike; signed point test; workshop `00.live`; current 05.08 and 05.09. This is selective grounding, not a claim to have reviewed all law or established a complete coldboot. Missing `00.live` without the `.md` suffix was resolved by inspecting the actual furniture. No missing law or page class was fabricated.

Remaining limits are documented in README and design.md: semantic truth and authority need model/Director review; live routing and page allocation await a settled contract; command chains/replies/execution/receipts are not implemented; source-heading checks do not prove a source is approved or governing.
