# 05.07 - App command for the accepted read-only review reporter
date: 2026-11-03
who: Codex Prime
executor: Grok-1
reviewer: Codex Prime
state: PREPARED; execute on named Director invocation; staged app connector

## Goal / scope
Expose the accepted review-report-pass03 through a normal app command, retaining the exact report meaning. Prime should call librarian.py review-report --book ABS --source PAGE --pass 05.NN. The connector is read-only; review mutation stays on review-loop. Shared app selection remains Prime-owned after review.

## #01 - Freeze and design before code
Verify evidence/pack05.07/source-manifest.json. Read 06.10.md and the accepted report's CONTRACT/PRIME-USE. Write 06.11.md notes before implementation. Define arguments, output/exit contract, pin chain and dependencies. Preserve pass01/pass02/pass03 and the existing core. No new report semantics or identity policy. Record dependencies on the workflow page so future builders can recover why they are present.

## #02 - Staged connector
Create NEW app/review_report_tools_v1.py and app/review-report-v1.json, plus NEW labs/review-report-app-pass01 for tests/proposed dispatcher. Existing app/librarian.py and README remain unchanged. The copied dispatcher may add only the new command and its handler, preserving all other routes. Supply the exact unapplied minimal dispatcher diff and proposed usage text. Do not replace the dispatcher with an old copy.

Use the existing accepted reporter, not a rewrite. Check hashes/lengths of the actual reporter/import chain before loading or executing it; report.py pass03 imports pass02, which imports pass01. Include the selected app/core dependency cut needed by their existing checks. Derive the normal code root from the installed app, disclose any copied-fixture roots and refuse ambiguity rather than silently mixing roots. No installation, network, polling, scheduling or model call.

The connector must preserve the existing JSON object, attention, bounded tests_note, declared/measured/addressed/content/unknown-physical counters, stale/coherence status and exit meanings. Exit 0 never means release. Bad arguments/pins must fail before reader execution. Do not use the new command to record/publish or manufacture custody. Do not edit old report renderings.

## #03 - Connected acceptance
Compare direct standalone output with the staged connector and copied app command on the SAME unchanged source cut. Actual 0512/05.06 and 0521/05.13 may be read only; both currently have published preliminary Prime reviews. Hash relevant source/review files before and after. Prove same report/exit and no writes. On disposable fixtures cover stale/missing review, wrong dependency hash, malformed/repeated arguments, and mid-observation hold by existing regression evidence. Add two new author hostile cases for the connector. Label author tests and Prime's future independent probes separately.

Test the copied dispatcher's existing review-loop/authoring/return-lines route selection without doing real mutations. Do not run unrelated broad suites. If source pins drift, stop and return the exact dependency conflict rather than update other workers' files.

## #04 - Return
NEW evidence/build05.07: submission, contract, command logs, test table, no-write proof, artifact manifest excluding itself, PRIME-USE and exact shared-app integration/rollback proposal. Fill this pack Return pointer. Allowed writes only new staged files above, 06.11.md, evidence/build05.07, disposable external fixtures and this pointer. No shared dispatcher/README/current modules/core reviews/custody/migration/kernel/00.live/other worker output/Git/network/install/models/bots/AR-01. Stop for Prime review; no selection or release.

## Return pointer
Submission: 00.kernel/00.00.10.work/0512.prime-review/evidence/build05.07/submission.md sha256 dfefe8754c4153d5a8228adfc0c80725d046bc3dd6df0744f49f2648ebee8a87, 8252 bytes.
Artifact manifest: 00.kernel/00.00.10.work/0512.prime-review/evidence/build05.07/artifact-manifest.json sha256 dfd5ea00aca3265dd049d04cb101507a18fa5f4db84664fa26ab1ad68f97bef4, 4977 bytes. The manifest lists 23 files and excludes itself.

## Review - Codex Prime
PENDING.
