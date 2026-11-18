# Prime review — 0511.workflow-colab/05.05
date: 2026-11-01
who: Codex Prime
disposition: accepted for the isolated staged-publication preservation repair; not active app selection or live adoption

## Deliverable and alignment
Grok-2 supplies workflow pass04 with staged exclusive writes and retained prior sealed pairs, preserving page-local Colab routes and existing schema. This addresses WF01, where pass03 truncated the authoritative investigation in place. App, door, loop, cycle, producer and earlier captures remain unchanged.

## Independently verified
All 52 frozen input rows and 21 artifact rows match bytes/SHA-256. Ran focused test_pass04.py under native Python 3.12.14: 9 passed, 1 symlink-privilege skip (WinError 1314), no failures. The separate real producer-backed two-pass smoke passed: open, attach, seal-return, review, open-pass, attach, seal-return, review. LF/CRLF returns and the original producer envelope remain preserved. No original evidence runner main was executed.

Source inspection confirms the prior pair is retained and checked before candidate publication, authority files are staged and replaced rather than truncated, collisions are refused and the read path blocks partial/attempt/lock states. It does not select the highest checkpoint or silently repair an interrupted page.

Added a separate retained failure fixture: after investigation replacement, deliberately fail before seal replacement during the second pass. The command returns exit 2, interrupted write, wrote true. The root pair is mixed and blocked; the retained checkpoint equals the saved prior investigation/seal byte-for-byte. Earlier pass artifact, pack, review and return projection remain unchanged. This fixture is preserved under D:\librarian\temp\workflow-pass04-review-nov01\retained-fixture and copied with this review. Producer verification is stubbed for this fault probe; the separate ordinary smoke uses the real pinned producer. No power-loss or process-kill trial is claimed.

## Limits / findings
No new blocking finding in the bounded WF01 repair. Retention and staging do not make multi-file publication atomic. Projections may be newer than the authority pair during an interrupted publication, and explicit partial state must therefore remain visible. Current/previous selection must use the attempt/checkpoint identity and verify bytes, not filenames or highest versions. If checkpoint construction itself was interrupted before attempt.json exists, stop: preserve the intact root pair and incomplete evidence for inspection; do not follow the normal completed-checkpoint recipe blindly or delete blockers. Automatic restore remains outside scope.

The documented inherited post-commit record-review refusal when the requested next-pack file already exists remains a separate integration concern: wrote true is not a complete transition. Review_pending=false and a result named complete do not independently mean acceptance. Existing V01–V03/checker and H2 descriptor work is not solved here. File-symlink refusal remains untested on this host, while static junction refusal was exercised. No race, hard-link or power-loss guarantee; AR-01 remains held.

## Learning preserved
An interrupted command needs a recoverable, verifiable previous authority state, not merely a marker saying it failed. Separately inspect current authority, previous evidence, projections and the completion flag. A return can be retained even when its publication did not finish.

## Next bounded action / effect on waiting drafts
Update the queued candidate-loop test and conditional app plan with this accepted pin and preservation limits. The independent loop/harness matrix has no workflow runtime dependency, so keep it unchanged rather than adding this module to the test. No third workflow build is justified merely by the green repair. Before later workflow adoption, explicitly test occupied next-pack behavior and interrupted-checkpoint inspection in a disposable adoption scope; do not bundle that into the loop-door selection.

## Did / Blocked / Need
Did: independent integrity, focused regressions, real two-pass smoke and preserved fault probe; accepted this isolated repair.
Blocked: no WF01 blocker remains in tested scope. Live adoption, automatic recovery and app integration remain unperformed.
Need: separately released candidate-loop acceptance next. No Director design question for this disposition. Matching 0111 custody remains pending; no receipt or new allocation was invented.
