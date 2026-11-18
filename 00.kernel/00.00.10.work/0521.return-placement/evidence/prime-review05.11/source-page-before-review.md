# 05.11 - Robust malformed input and coherent readiness observation
date: 2026-11-02
who: Codex Prime
executor: Grok-2
reviewer: Codex Prime
state: PREPARED; execute on named Director invocation only

## Goal and method
Repair T1/T2 in 06.21 without expanding the readiness tool. Verify evidence/pack05.11/source-manifest.json; claim/notes in NEW 06.22.md. Reproduce the frozen invalid-encoding and late-dispatcher-change failures first; preserve outcomes as known-failure reproductions. Write the narrow delta before implementation. NEW labs/return-readiness-pass02 only, reusing the exact reviewed route contracts. Preserve pass01 and all selected app files byte-for-byte.

## #01 - Truthful malformed/unreadable observations
Handle non-UTF8 dispatcher bytes without traceback. Keep measured byte identity, classify malformed/unsupported, show which route selection is unknown, retain authority not-assessed and non-authority warnings. Similar expected decoding/read/disappearance faults in dispatcher, declarations, dependencies, layout and door must return a bounded explicit observation or a documented CLI refusal, not a false selected-valid result. Never execute inspected code, guess replacements or substitute empty inputs as valid defaults. Do not hide programmer exceptions with a catch-all that reports success.

## #02 - Validate the observation boundary
Adjacent double reads of each file are insufficient: a previously measured dispatcher can change while later dependencies are being read. Establish a bounded read set, then revalidate measured dispatcher, selected facade/declaration/dependencies and observed book declaration/door before returning route validity. Changed bytes, disappearance, linked/wrong-type replacement or missing->present declaration transitions produce unstable/unknown for affected claims, not a mixture of cuts. Conservative whole-observation unknown is acceptable if clearly explained. No locking daemon, persistent registry, auto-repin or unbounded retry. State that a completed bounded observation is not a guarantee against changes after the final check.

Use only a test-injected read seam on copies to reproduce: dispatcher changes AFTER its initial pair of reads during later facade read; an earlier dependency changes during later measurement; the absent layout appears before final validation. Public CLI has no injection/bypass. Also prove stable old and stable selected-successor routes still report correctly, unrelated other-branch whole-file changes between separate inspections do not create a permanent pin requirement, valid/missing/malformed declaration behavior remains explicit, and the tool creates no output files.

## #03 - Deliver a small usable successor
JSON/text remain projections of the same observation. Preserve static AST recognizer limits, selected vs staged vs valid-declaration distinctions, explicit authority-not-assessed and direct historical writer warning. No review-loop classification, model calls, inspected imports/subprocesses or app selection. One real code/book READ-ONLY demo through the successor, with read set and before/after preservation evidence. PRIME-USE gives that standalone command and limits. Prime independently probes before adoption.

## Outputs / return
NEW labs/return-readiness-pass02, NEW 06.22.md/evidence/build05.11, this pack Return pointer, retained small external fixtures only. No current app/README/facade/declaration/backends edits, other-builder source/return reads, kernel/00.live/N3NN/current assignment changes, migration/layout/release/root creation, custody/closure, Git/network/install/models/bots/AR-01 or cleanup.

Return Did/Blocked/Need, T1/T2 disposition, exact API/contract/pins/ownership, per-case commands/results/limits, known-failure reproduction vs new author tests, first failures, no-write proof, Factfind/Hostile/Overflow/Unprompted, reread corrections, artifact manifest excluding itself. Matching 0121 custody pending. Stop for Prime review; no activation or Director release claim.

## Return pointer
Invocation/claim: 06.22.md records the Director invocation and the readiness-successor claim. Live migration is not released. App selection is not applied.
Submission: evidence/build05.11/submission.md sha256 65b9a76b3d317a13be057986870aca9eea90a838ee633b651968f847063900d2, 874 bytes.
Artifact manifest: evidence/build05.11/artifact-manifest.json sha256 45958641dd7c067b140062a19c2b1f9d22b965912571f35f3096828e032115d1, 4374 bytes, 19 files. Excludes itself and this page.

## Review - Codex Prime
PENDING.
