# 05 — Concurrent creation of shared bridge parents
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
Claim: Grok 4.7 (xAI), session 01a179d2-387a-7661-8702-6e53f95e96b5, 2026-10-27, HEAD 81f690a71af373cefed79d58bcf5d70360585c28.
Workspace D:/Git/lib-build, branch workshop. Verify evidence/pack05.12/source-manifest.json
and exact snapshots. CS-02 only; shared Git writes and other active lanes excluded.

## #01 — Reproduce and preserve
Notes FIRST on06.12.md. Preserve worker_bridge.py under evidence/concurrency05.12/
before/. Reproduce the reported race deterministically in a disposable copy:
caller checks absent shared parent, another caller creates it, first mkdir sees
FileExistsError. Preserve before-code result and the original failed concurrent
run. Do not rely on repeated timing runs until one happens to pass.

## #02 — Shared parent creation is different from exclusive delivery creation
Allow the first caller to revalidate an ordinary shared parent created by another
caller. Recheck path type/link/containment expectations before proceeding. A file,
junction, symlink or otherwise invalid raced target must refuse clearly without
traceback or unauthorized writes. Do not merely use exist_ok=True or swallow
FileExistsError unconditionally. Keep _exclusive_dir and every per-delivery
input/output/store/provenance identity exclusive: an occupied delivery is not an
ordinary shared parent and never authorizes another launch or overwrite.
Product edits: app/worker_bridge.py, new app/tests/test_bridge_dirs.py and additive
app/README clarification only. No lab backend, Clerk, seam, context, configs,
existing tests, loader, kernel or role edits. If another file is genuinely needed,
report concrete evidence before expanding scope. No new global lock/queue or
exactly-once guarantee. Preserve CS-01 phase-aware attention and retry boundaries.

## #03 — Verify the interleavings and complete connection
New tests must control the shared-parent interleaving, not sleep and hope. Cover
plain-directory success and raced file/link refusal with retained bytes, and
explicit proof _exclusive_dir still rejects an occupied delivery. Use disposable
containers only. Also run the existing seam suite (including concurrent same-job
case and partial-I/O cases) and existing app worker-bridge suite sequentially.
Record every failure/skip, not only a passing rerun. Demonstrate overlapping
same-delivery calls yield at most one worker launch and one Clerk return, with
later identical replay read-only. State any unproved different-delivery or race
boundary honestly. No live model, arbitrary command, network or real store.
Write commands/logs to tests.txt; exact hashes/controlled outcomes/limits in
verification.json. No unrelated whole-core suites absent a failure/new change.
Fully reread and account for notes.

## #04 — Capture locally before publication
Verify unchanged capture helper 8f3da5c651f6924fca6dedb0b95da7d181eb58884dc030dd9cbc3d8b6a5b15ac. Write final dedicated
evidence/concurrency05.12/submission.md starting Did, Blocked, Need. Complete
the reserved 0117.bridge-parent-0512's seven outputs, then run:

```text
python -B labs/return-capture-pass01/return_capture.py capture --book "D:/Git/lib-build/00.kernel/00.00.10.work" --submission grok-1-0504-0512 --return-file "D:/Git/lib-build/00.kernel/00.00.10.work/0504.app-entry/evidence/concurrency05.12/submission.md" --source-root "D:/Git/lib-build" --artifact "app/worker_bridge.py|app/worker_bridge.py" --artifact "app/tests/test_bridge_dirs.py|app/tests/test_bridge_dirs.py" --artifact "app/README.md|app/README.md" --artifact "00.kernel/00.00.10.work/0504.app-entry/06.12.md|00.kernel/00.00.10.work/0504.app-entry/06.12.md" --artifact "00.kernel/00.00.10.work/0504.app-entry/evidence/concurrency05.12/before/worker_bridge.py|00.kernel/00.00.10.work/0504.app-entry/evidence/concurrency05.12/before/worker_bridge.py" --artifact "00.kernel/00.00.10.work/0504.app-entry/evidence/concurrency05.12/tests.txt|00.kernel/00.00.10.work/0504.app-entry/evidence/concurrency05.12/tests.txt" --artifact "00.kernel/00.00.10.work/0504.app-entry/evidence/concurrency05.12/verification.json|00.kernel/00.00.10.work/0504.app-entry/evidence/concurrency05.12/verification.json"
python -B labs/return-capture-pass01/return_capture.py verify --book "D:/Git/lib-build/00.kernel/00.00.10.work" --member 0117.bridge-parent-0512
```

Keep submitted source and failed evidence. Append only member/receipt/fresh verify
below. Partial/refused capture stays explicit; no overwrite/removal or allocating
around failure. Prime reviews and publishes separately. No shared Git commit/push,
other builder work or SoF. This draft/reservation is not release or acceptance.

## Return pointer
Member 0117.bridge-parent-0512. Receipt sha256 408e3cdfe4f9c95558513718c00f464498207ce568265e40f3650e384a3d677e. Verify exit 0: result complete; not approved; not accepted; not published.

## Review — Codex Prime
PENDING.
