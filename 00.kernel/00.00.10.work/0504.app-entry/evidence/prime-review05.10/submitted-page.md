# 05 — First fixture-only Clerk-to-worker connection
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
Claim: Grok 4.7 (xAI), session 01a179d2-387a-7661-8702-6e53f95e96b5, 2026-10-27, HEAD a7f5ba7df66469ffb3f4f1da4ac5ef9f737570d4.
Workspace D:/Git/lib-build, branch workshop. Inputs: evidence/pack05.10/source-manifest.json
and exact snapshots. Read 0506/05.03 and its accepted design/Prime requirements.
All required lower-level components are accepted; Claude's separate Prime intake
adapter is not a dependency. Do not import it or modify its active lane.

## #01 — Notes and exact seam contract
Notes FIRST on 06.10.md. Preserve source-before under evidence/seam05.10/before/.
Write evidence/seam05.10/CONTRACT.md before code: map accepted APIs to design
S1–S10, statuses and file ownership. Carry Prime's two requirements from 0506/05.03.
Use pinned Clerk f697a7e443117c3d1face62d3021f7634154d76214b77fadec1a5cc3c99d394c
and show --json inspection/2 for job, checks, claim and recorded return. Never
read raw Clerk events or parse human inbox text as another ledger. Keep the
existing public claim-resume contract for its token if required; document it.
Use accepted app worker_bridge.perform and its receipt validation; no duplicate
worker bridge, receipt validator, Clerk, queue, router or intake registry.

## #02 — Implement the one explicit fixture command
Add app/clerk_seam.py, strict pinned app/clerk-seam.json, one clerk-deliver branch
in app/librarian.py, meaningful app/tests/test_clerk_seam.py and README examples.
Standard library only. Preserve context.py, worker_bridge.py, all accepted labs
and configs, existing tests, kernel and shared assignment/view files unchanged.
The caller supplies an already queued and explicitly claimed job, link, actor,
external fixture and container. This command does not queue or choose an actor,
reviewer, route or authority. Only the test protocol worker may launch; no model.
Use the design's sibling fixture/store inside one explicitly designated external
non-Git container; neither component's placement rule is bypassed.
Read and validate claim, instructions, route/output and exact bridge job binding
before launch. Require link.bridge_job_sha256 == original provenance.job_sha256
on existing delivery paths too; matching IDs/current bytes alone is insufficient.
Call bridge once, require collected done + correct receipt/request/job/delivery,
verify each declared artifact hash, exclusive-copy only those files into Clerk
outbox, then public Clerk return with deterministic evidence naming the original
delivery/request/receipt/artifact. The worker keeps its own fresh output folder.
No routing choice, reviewer invocation, acceptance, closure or ordinary run.

## #03 — Replay, uncertainty and interrupted copies
Implement the accepted design's explicit phase outcomes and association record
without duplicating the source records' authority. Serialize identical seam calls.
Preserve original delivery/request/claim on retry. Uncertain, uncollected or failed
worker results stop visibly, retain evidence and do not become normal Clerk
returns or silently relaunch. Explicit bridge recovery is a separate action.
Preflight validates actor/instructions/job identity even for returned-job replay.
Interrupted artifact copy or conflicting outbox bytes stays attention; never
overwrite/clean it or pretend cross-store atomicity/exactly-once execution.
An identical completed replay is read-only and launches nothing.

## #04 — Prove the connected loop and failure boundaries
Disposable copied code/stores only. Tests/demo cover design A1–A15: queue/claim
(fixture SETUP only), clerk-deliver, structured returned projection, named reviewer
inbox, verify and exact replay with one worker launch. Also wrong actor/claim,
stale instructions before/after launch, changed link/job/provenance, malformed
receipt, mutated output, occupied/linked copy paths, damaged completion, wrong
tool hash, invalid placement and concurrent calls. Add in-process interruption
hooks before launch/copy/return/report, never caller-exposed crash flags. Record
partial/uncertain states honestly; refusal must not erase evidence or relaunch.
Run new seam suite and existing entry, pack-tool and app bridge regressions in
disposable copies, only once unless a failure/change justifies another run. Keep
all commands/logs in tests.txt and exact hashes, counts, skips/failures and fresh
process demo in verification.json. No network, actual models or real jobs.

## #05 — Return through the real local archive
Fully reread and disposition notes. Write final dedicated evidence/seam05.10/
submission.md starting Did, Blocked, Need. Required payloads are the exact list
in reserved 0109.clerk-seam-0510/reservation.json. No new allocation. Verify the
capture helper SHA-256 8f3da5c651f6924fca6dedb0b95da7d181eb58884dc030dd9cbc3d8b6a5b15ac, then run:

```text
python -B labs/return-capture-pass01/return_capture.py capture --book "D:/Git/lib-build/00.kernel/00.00.10.work" --submission grok-1-0504-0510 --return-file "D:/Git/lib-build/00.kernel/00.00.10.work/0504.app-entry/evidence/seam05.10/submission.md" --source-root "D:/Git/lib-build" --artifact "app/clerk_seam.py|app/clerk_seam.py" --artifact "app/clerk-seam.json|app/clerk-seam.json" --artifact "app/librarian.py|app/librarian.py" --artifact "app/README.md|app/README.md" --artifact "app/tests/test_clerk_seam.py|app/tests/test_clerk_seam.py" --artifact "00.kernel/00.00.10.work/0504.app-entry/06.10.md|00.kernel/00.00.10.work/0504.app-entry/06.10.md" --artifact "00.kernel/00.00.10.work/0504.app-entry/evidence/seam05.10/CONTRACT.md|00.kernel/00.00.10.work/0504.app-entry/evidence/seam05.10/CONTRACT.md" --artifact "00.kernel/00.00.10.work/0504.app-entry/evidence/seam05.10/tests.txt|00.kernel/00.00.10.work/0504.app-entry/evidence/seam05.10/tests.txt" --artifact "00.kernel/00.00.10.work/0504.app-entry/evidence/seam05.10/verification.json|00.kernel/00.00.10.work/0504.app-entry/evidence/seam05.10/verification.json"
python -B labs/return-capture-pass01/return_capture.py verify --book "D:/Git/lib-build/00.kernel/00.00.10.work" --member 0109.clerk-seam-0510
```

Keep source/submission/evidence. Append only member, receipt hash and fresh verify
result below. Capture failures stay explicit; never remove a partial package or
allocate around it. No shared Git writes, self-acceptance, other lanes or SoF.
The Prime publishes separately. This draft/reservation is not execution release.

## Return pointer
Member 0109.clerk-seam-0510. Receipt sha256 0ff16dcc5c0d563933d48b3d601d3119b28da8700359441770fb1897445d481c. Verify exit 0: result complete; not approved; not accepted; not published.

## Review — Codex Prime
PENDING.
