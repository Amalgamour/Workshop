# 05.15 - Strict N7 declarations without changing N5 filenames
date: 2026-11-04
who: Codex Prime
executor: Grok-2
reviewer: Codex Prime
state: PREPARED; execute on Director handoff; staged successor only
source_design: 0420.prime-desk/06.42.md
matching_return_line: 0122.review-construction (custody pending)

## Goal and Director decision
Director selected: "Block malformed N7 declarations (Recommended)". Exact question/answer is on 0420/06.42. The accepted 05.14 canonical staging works but retains A-01/A-02: an N7 manifest with trailing text can fall through and select a different comma-suffixed filename; a rejected declaration may be ignored beside another valid one. Repair this explicitly. Preserve the accepted valid N7 forms and unchanged N5 grammar, including legitimate filename punctuation. Do not impose a new global filename ban.

## #01 - Freeze and precise contract
Verify evidence/pack05.15/source-manifest.json and snapshots. Read 06.31, the Director decision and frozen independent parser probes. Write NEW 06.32.md before code. Reproduce A-01/A-02 on staged pass04 read-only; retain raw known failures. Define recognized declaration labels and accepted forms. Malformed recognized N7 declarations must block the whole intake until corrected even beside a valid declaration; mere diagnostic findings with measurement complete are insufficient. Unsupported nondeclaration Notes/prose remains diagnostic, not an invented declaration or silent filename rewrite. Existing ambiguous duplicate protection remains. State parse-to-measurement-to-record behavior, including labels with no value and near-matches; escalate any unresolved design fork.

## #02 - Versioned canonical staging
NEW labs/workbook-review-pass05/workbook.py, app/review_loop_tools_v9.py and app/review-loop-v9.json; NEW labs/review-entry-staging-pass02 for tests/adapters. Confirm free paths before writes. Implement from accepted pass04 with explicit measured-kind gating/context reset. All N5 and no-context parser behavior delegates unchanged. N7 malformed recognized lines cannot fall back to another filename interpretation. Ensure the blocking state survives prepare/form and record refusal rather than only changing parser output. New door must validate actual dependencies and run at canonical root. Preserve all v4-v8/pass01-pass04/current app/README byte-identical. No source-capacity or first-review-cycle integration in this slice.

## #03 - Real read-only proof and disposable mutations
Only prepare/form are authorized on actual book. Invoke new door directly on 0522/05.13, 0512/05.06, 0707/05.15 and 0707/05.17. Two N5 results must match current v7 on actual form.bindings.rows, cuts, findings and intake_id on the same cut; N7 must remain complete with 26/33 artifacts. Record before/after source hashes. Notes lines remain explicit diagnostics.

ALL mutations/lifecycle tests use NEW external books. Test exact valid forms; manifest suffix and returned suffix; incomplete labels; malformed declaration before/after a valid line; misleading attribution; duplicate/conflicting lines; comma/semicolon/parenthesis N5 filenames; CRLF/LF; source-kind context reset after failure. Demonstrate malformed N7 prepare held/incomplete plus record refusal with no accepted-current judgment/publication, retaining raw source bytes. At least one positive N5 and N7 preliminary cycle: record -> full inspect/read -> separate publish -> read/recover. Preserve manual Director text and refuse a changed source. Do not precreate a fake first-review target or claim the separate absent-target fix is integrated.

## #04 - Regression, pins and honest limits
Rerun relevant accepted 12 cases, and reconcile historical 17 cases individually rather than calling revised expectations unchanged. Keep canonical-root ambiguity failures distinguishable from parser regressions. Add two new author hostile cases and wrong/missing tool/declaration/dependency tests. Preserve first failures and no-write checks. Report exact selection/rollback delta; both reporter and reader change dispatcher identity, so future combined pins need a new coherent version. Do not select app or repin historical 0522/05.13 evidence. No code from Grok-1's unfinished capacity lane.

## #05 - Return
NEW evidence/build05.15: Did/Blocked/Need; pre-code contract; decision trace; changed grammar/state transition; source/dependency/pin delta; per-case provenance/commands/results; raw known failures; canonical measurements; no-write proof; PRIME-USE; unapplied selection/rollback proposal; Factfind/Hostile/Overflow/Unprompted; artifact manifest excluding itself. Reread/integrate 06.32 and reverify source freeze. Fill this Return pointer with exact N5 Submission/Artifact manifest hash/length form. Matching line 0122: custody pending if native route unavailable; no legacy allocator/new sequential return/receipt invention. Stop for Prime review.

Allowed writes: named NEW staged files/lab/external copies, 06.32.md, evidence/build05.15 and this pointer. No active app/README/old modules/live reviews/custody/01NN/kernel/layout/migration/other-worker files/Git/network/install/models/bots/AR-01. No approval/activation/release. Normal reserve; no burn-down. Stay in this session.

## Return pointer
Invocation/claim: Grok-2 claims 0522.review-construction/05.15. Named Director assignment on 2026-11-04. Reviewer Codex Prime. Block malformed recognized N7 declarations and keep N5 filename rules. The shared dispatcher stays on the v7 door. This builder does not commit. Python 3.14.0. accepted false. approved false. published false. seated false. committed false. app_selected false.
Submission: 00.kernel/00.00.10.work/0522.review-construction/evidence/build05.15/submission.md sha256 0d26fb1d9d017aa4e4172c86800b64a12d3bb890dea5a1a2f68fdcba16c45286, 7802 bytes.
Artifact manifest: 00.kernel/00.00.10.work/0522.review-construction/evidence/build05.15/artifact-manifest.json sha256 40afbb4d273298b0d6a7d7c49a1ae2fba440280233a9bdfb0af12c979748a548, 4829 bytes. The manifest lists 20 files and excludes itself.
Custody: PENDING. Matching line 0122.review-construction is absent under the live work book. This pass did not use the old allocator, did not allocate 0184, and did not invent a receipt.

## Review - Codex Prime
PENDING.
