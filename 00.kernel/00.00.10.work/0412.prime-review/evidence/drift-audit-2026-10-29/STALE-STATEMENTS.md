# Stale and misleading statements found
Audit cut:168daf9,2026-10-29. Original quotations/captures remain untouched.

| Source | Statement/problem | Current fact/disposition |
|---|---|---|
| 0157.prime-review-0501/return.md | "This file is the return. It has no receipt." | False as an unqualified current statement: committed0157/receipt.json exists. It describes a pre-capture moment, not current custody. Exact captured return remains immutable; this audit is the correction. |
| 0412.prime-review/01.md | Colab implementation outputs "are unreviewed" | Initial design snapshot.0155/0156 and later0158/0159 have bounded reviews. Corrected version labels initial state; STATUS separates remaining holds. |
| 0510.colab-tools/01.md | "Use05.02 for the next release" and workflow "remains held" | Superseded checkpoint: later05.03 producer reviewed, standalone checker held; no new release now. New text version points to current status. |
| 0511.workflow-colab/01.md |05.01 held and next05.02 | Historical checkpoint:05.02 repair accepted,05.03 v2 implementation not yet reviewed. Current work stopped. |
| 0700.band.colabs/01.md | Initial unsuffixed05.NN/06 description and initial build routes | Exchange was subsequently changed to pack/return/notes/review tails. New text version flags the later contract; no retrospective rename. |
| labs/colab-support-pass02/README.md | Experimental "until Prime reviews it" | Producer reviewed and bounded acceptance recorded; standalone checker held. README is now locally modified by Builder, so no conflicting edit here; current status recorded separately. |
| labs/prime-review-pass01/README.md and ADOPTION.md | "before Prime reviews"/"later caller" statements | Lab was reviewed and actually used by Prime. App entry remains unreviewed local work, not accepted wiring. Historical handoff language retained. |
| 0510/05.03 return and ADOPTION | Grok1/Grok2 "still" building/unreviewed | Explicitly the return-time boundary. Later reviews are now committed. Do not rewrite the original historical claim; current status is separate. |
| 0155–0159 returns | "Need Prime review" and claim HEAD values | Accurate submission-time statements, not current queue state. Reviews now exist and are indexed by backfilled reports. HEAD values identify claim cuts, not current HEAD. |
| 0156/0158 return | "No blocked check" | Builder's scoped test report, not proof of complete integration.0156 was held;0158 accepted only v1;v2 still requires review. |
| 0512 page | "05.02 exposes" app commands | Assignment describes intended result, not accepted integration. Local code exists but is not reviewed/published by this audit. |
| root README.md | "Latest" app/Clerk checkpoints from10/27 | Stale navigation beyond today's return set. Do not treat them as current acceptance state; current audit status supersedes for this review only. A future bounded navigation update is not silently performed here. |
| 0510/05.04 and0511/05.03 live files | Builder claim/execution records despite Director's awaiting-release description | Authority conflict: preserved unchanged, no new work or acceptance. Need reconciliation before any affected restart. |

Spacing failures are not evidence of changed code behavior. Shape/hash tests did not
verify human readability. No historical verification result is retroactively improved.
