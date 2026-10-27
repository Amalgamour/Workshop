# 05 — Two distinct Clerk deliveries sharing bridge parents
version: 001
Authorization: draft — 2026-10-27
who: Codex Prime
state: returned
Face: 05
PPPP: 0504
book: 00.00.10.work

## Assignment
Executor: Grok Builder 1. Reviewer: Codex Prime.
Release: released by the Director, 2026-10-27.
Claim: Grok 4.7 (xAI), session 01a179d2-387a-7661-8702-6e53f95e96b5, 2026-10-27, HEAD 8538dc0a9932410cd830ea4e493d18fb0194ee74.
Workspace D:/Git/lib-build, branch workshop. Verify evidence/pack05.13/source-manifest.json.
Test-only slice. Product bridge/seam/Clerk changes are not authorized by this pack.

## #01 — Notes and controlled integration
Notes FIRST in06.13.md. Build new app/tests/test_bridge_overlap.py using existing
allowlisted fixture workers and disposable external containers. Two distinct queued
and claimed Clerk jobs must share a fixture root and bridge parent directories but
use distinct delivery ids and artifacts. Start overlapping calls with a bounded
barrier or observable process coordination, not repeated timing until a pass.
Verify the overlap actually happened. Do not add a runtime fault hook or loosen pins.
No model calls, network, arbitrary worker command, real store, or other lane edits.

## #02 — Required assertions
Each distinct job produces its own correctly linked collected artifact, exactly one
worker launch and one Clerk return within the test. Identities must not cross and
shared parents remain ordinary directories. Repeat each identical call; confirm
already-recorded, no new launch/event and no stored-byte changes. An occupied
per-delivery id still refuses and retains its bytes. Keep same-job overlap covered
by the existing seam suite. Do not claim a general exactly-once guarantee.
If real overlap exposes another product defect, preserve the first failure and
report it; do not edit product code to make the tests pass in this assignment.

## #03 — Verify and retain
Run the new test and existing app/tests/test_clerk_seam.py sequentially in a
disposable source copy. No unrelated suites absent a new failure. Record all
commands, first failures, skips, observed identities, counters, replay hashes and
limits in evidence/overlap05.13/tests.txt and verification.json. Preserve notes,
reread fully, and account for them. No edits to existing tests or README needed.

## #04 — Local capture
Write dedicated evidence/overlap05.13/submission.md starting Did, Blocked, Need.
Capture only this test/report in reserved 0122.bridge-overlap-0513, then freshly verify:
```text
python -B labs/return-capture-pass01/return_capture.py capture --book "D:/Git/lib-build/00.kernel/00.00.10.work" --submission grok-1-0504-0513 --return-file "D:/Git/lib-build/00.kernel/00.00.10.work/0504.app-entry/evidence/overlap05.13/submission.md" --source-root "D:/Git/lib-build" --artifact "app/tests/test_bridge_overlap.py|app/tests/test_bridge_overlap.py" --artifact "00.kernel/00.00.10.work/0504.app-entry/06.13.md|00.kernel/00.00.10.work/0504.app-entry/06.13.md" --artifact "00.kernel/00.00.10.work/0504.app-entry/evidence/overlap05.13/tests.txt|00.kernel/00.00.10.work/0504.app-entry/evidence/overlap05.13/tests.txt" --artifact "00.kernel/00.00.10.work/0504.app-entry/evidence/overlap05.13/verification.json|00.kernel/00.00.10.work/0504.app-entry/evidence/overlap05.13/verification.json"
python -B labs/return-capture-pass01/return_capture.py verify --book "D:/Git/lib-build/00.kernel/00.00.10.work" --member 0122.bridge-overlap-0513
```
Keep partial capture explicit; never overwrite/remove or allocate around it.
Append member, receipt and fresh verify only. No shared Git stage/commit/push.
Prime reviews/publishes. Reservation/draft is not Director release.

## Return pointer
Member 0122.bridge-overlap-0513. Receipt sha256 5183efeeadf3ed4293fa9563d430c6f0e45a7cfbbe1f1da3c38763cc8d7f77bf. Verify exit 0: result complete; not approved; not accepted; not published.

## Review — Codex Prime
PENDING.
