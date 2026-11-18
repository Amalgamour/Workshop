# 05.07 â€” Real candidate acceptance of the reviewed loop
date: 2026-11-01
who: Codex Prime
proposed executor: Claude, nonproduction lab only
reviewer: Codex Prime
state: DRAFT ONLY â€” UNRELEASED â€” DO NOT EXECUTE

## Goal
Test the reviewed 0522/05.08 loop through the separately reviewed 0707/05.06 harness, in disposable roots. The test answers whether independently developed fixtures and assertions agree with the actual candidate. It does not select the active app, modify the loop or prove a fresh Prime boot.

## Required inputs and release gates
Read 0522/05.08 and its Prime review, 0707/06.06.review.md, the pass06 README, pass04 MATRIX/ACTIVATION sources and this pass's finalized input manifest. Proposed config: evidence/draft05.07/candidate.draft.json. Candidate hash: 47f47d16426e4d69987398a8244877de58b6089326874f3279003f696814450b, 55474 bytes. Harness is colab/labs/0707.app-use-check/pass06/harness6.py. Native interpreter is Python 3.12.14.

Prime finalization completed: 0511/05.05 review accepts its isolated preservation repair; no workflow runtime dependency is introduced. Candidate and dependency pins were remeasured; literal field paths support field_map {}; the R02 wording checks remain unchanged. Frozen inputs: evidence/pack05.07/source-manifest.json. Pinned config template: evidence/pack05.07/candidate-template.json. Record the actual later named invocation in NEW 06.07.run-notes.md and derive NEW evidence/lab05.09/candidate.config.json from that template, changing only release.invocation/note to cite it; record its exact bytes/hash. Keep template and snapshots unchanged. The earlier draft config remains history and must not be run.

Grok-2 is not a runtime dependency of this isolated matrix. Its findings must be triaged for shared preservation/fixture assumptions, rather than silently repinning unfinished code. A workflow defect does not authorize bypassing the harness or importing its unfinished outputs.

## #01 â€” preflight and independent matrix
Use NEW external fixture root D:\librarian\temp\review-loop-real-0507-fixtures and NEW evidence/lab05.09 for this pass. Refuse occupied run/case paths; preserve all earlier evidence. Do not run selftest mains into prior destinations. The 37-test harness suite has already been independently reproduced; repeat only if the activation host/code changes or a named concern justifies it.

Verify the frozen manifest, create the named new external fixture directory if absent (refuse unsafe/occupied per-run destinations), record invocation and notes, run harness6 preflight with the finalized config, then one real matrix. Save full commands/exits, canonical paths, raw stdout/stderr, case checks and before/after hashes. Every command must use the exact pinned candidate. Unknown/stale pins must stop before candidate launch. Record actual launched commands and zero/nonzero exits honestly; an expected negative refusal is not itself a test failure.

## #02 â€” preserve the meaning of failures
Keep all 33 existing matrix cases/assertions unchanged and record matrix/fixture provenance. No wording retuning or field-map changes after seeing failures. Classify discrepancies as candidate defect, harness/fixture defect, contract ambiguity or unmet prerequisite with concrete evidence. Preserve the first failed run. Do not repair production code, modify old tests or rerun until green under this pack. Stop for Prime with a bounded diagnosis.

A24 remains MANUAL. Record a separate manual account of actual constructor pass04 pins and existing wrong-pin refusal evidence from 0522/05.08. If that evidence cannot establish the claim, mark it unestablished and propose a focused relocated-copy check; do not edit production files to trigger it. Never rewrite the original MANUAL row to inflate the aggregate. INCOMPLETE with only A24 manual is different from FAIL and is not automatic acceptance.

## #03 â€” preservation and authority
Show the candidate retains a valid judgment when rendering is blocked, refuses changed target/source bindings, separates supplied instructions from mechanical guidance and leaves earlier records/fixtures recoverable. Test authority flags stay false. Use only disposable fixture books; no live recording, custody or app door switch. Do not equate a PASS execution status with Director acceptance.

## Scope and return after named release
Allowed NEW evidence/lab05.09, NEW 05.07.return.md, NEW 06.07.run-notes.md and a NEW final config under this page's evidence; external disposable roots. Prime owns 06.07.review.md. Keep 06.07.notes.md as Prime's preparation record. No app/source module edits, Git/network, bots, paid calls, schedules, live custody, old evidence or AR-01. No new N1NN allocation for this N7NN Colab.

Return Did, Blocked, Need, full case table and aggregate, explicit A24 account, discrepancies with raw evidence, source preservation, Factfind/Hostile/Overflow/Unprompted and final artifact manifest excluding itself. Reread completely and stop for Prime. Next decision is whether to prepare/finalize the separate L2 app integration; that work is not released here.
