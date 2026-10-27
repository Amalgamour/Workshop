# 05 — Keep malformed Clerk projections in attention
version: 001
Authorization: draft — 2026-10-27
who: Codex Prime
state: draft; awaiting Director release
Face: 05
PPPP: 0507
book: 00.00.10.work

## Assignment
Executor: Claude. Reviewer: Codex Prime.
Release: PENDING. Claim: PENDING.
Verify exact inputs in evidence/pack05.05/source-manifest.json before
editing. Shared workspace D:/Git/lib-build, branch workshop. No shared Git writes.
Keep other builders' work unchanged. Source snapshots are the exact supplied
inputs; they include this Prime review, not a claim they all came from one old commit.

## #01 — Correct CA-01 at the schema boundary
Notes first on 06.06.md. Preserve both editable source files under
evidence/repair05.05/before/. Retain and first reproduce the six Prime failure
cases in a disposable copy. Add explicit type validation before enum membership
for state/check fields; malformed projection shapes become ProjectionError,
then unsupported attention. Validate required null/object shapes and types of
the inspection/2 fields this adapter consumes, against the pinned Clerk source.
Do not invent a new producer schema. No broad except Exception, raw-event reader,
alternative queue, automatic inbox discovery or edits to accepted Clerk code.
Product edits are clerk_adapter.py and tests/test_clerk_adapter.py only. If the
bounded fix genuinely requires another product file, report the reason first.

## #02 — Exercise the whole error path
Add list/object/null/numeric/bool type cases for enums, and wrong state-dependent
null/object shapes. Use fixture/injected replies to prove inspect returns
unsupported with no identity/clean result, status/scan keep visible diagnostics
and continue to show another registered job, and ack refuses without writing.
Keep real clean and changed-artifact Clerk fixtures working; only fixture setup
may queue/claim/return. Run 14+19+10 existing tests plus new meaningful cases in
disposable copies. Retain first failures, full commands/results in tests.txt and
exact hashes/coverage/limits in verification.json. No real registry/store/app
installation, routing, models, network, shared Git writes or other lane edits.
Fully reread and disposition notes. Acceptance stays Prime's separate decision.

## #03 — Return locally before publication
The return member 0107.clerk-types-0505 is already reserved for this batch. Do not
allocate another. Verify capture helper SHA-256 8f3da5c651f6924fca6dedb0b95da7d181eb58884dc030dd9cbc3d8b6a5b15ac before use.
Write the final dedicated submission.md under evidence/repair05.05/, starting
Did, Blocked, Need with test results, failures, limits and exact output hashes.
Complete every declared output listed in the reservation. Do not fabricate
missing evidence to satisfy capture. Run from D:/Git/lib-build:

```text
python -B labs/return-capture-pass01/return_capture.py capture --book "D:/Git/lib-build/00.kernel/00.00.10.work" --submission claude-0507-0505 --return-file "D:/Git/lib-build/00.kernel/00.00.10.work/0507.prime-support/evidence/repair05.05/submission.md" --source-root "D:/Git/lib-build" --artifact "labs/prime-support-pass01/clerk_adapter.py|labs/prime-support-pass01/clerk_adapter.py" --artifact "labs/prime-support-pass01/tests/test_clerk_adapter.py|labs/prime-support-pass01/tests/test_clerk_adapter.py" --artifact "00.kernel/00.00.10.work/0507.prime-support/06.06.md|00.kernel/00.00.10.work/0507.prime-support/06.06.md" --artifact "00.kernel/00.00.10.work/0507.prime-support/evidence/repair05.05/tests.txt|00.kernel/00.00.10.work/0507.prime-support/evidence/repair05.05/tests.txt" --artifact "00.kernel/00.00.10.work/0507.prime-support/evidence/repair05.05/verification.json|00.kernel/00.00.10.work/0507.prime-support/evidence/repair05.05/verification.json" --artifact "00.kernel/00.00.10.work/0507.prime-support/evidence/repair05.05/before/clerk_adapter.py|00.kernel/00.00.10.work/0507.prime-support/evidence/repair05.05/before/clerk_adapter.py" --artifact "00.kernel/00.00.10.work/0507.prime-support/evidence/repair05.05/before/test_clerk_adapter.py|00.kernel/00.00.10.work/0507.prime-support/evidence/repair05.05/before/test_clerk_adapter.py"
python -B labs/return-capture-pass01/return_capture.py verify --book "D:/Git/lib-build/00.kernel/00.00.10.work" --member 0107.clerk-types-0505
```

Keep the original submission and evidence after capture. Once capture and fresh
verify succeed, append only the member, receipt hash and verification result to
this batch's Return pointer below. Do not duplicate the submitted prose here.
If capture refuses or leaves a partial package, report the exact state here;
never overwrite a member, remove a receipt or silently allocate around failure.
Prime reviews and publishes separately. Receipt means capture, not acceptance.
No future work is authorized by a recommendation or by this reserved slot.

## Return pointer
Release: the Director, chat 2026-10-27: "The Director releases 0507.prime-support/05.05. Workspace: D:\Git\lib-build Branch: workshop Read 00.kernel/00.00.10.work/0507.prime-support/05.05.md. Verify pins, record release and claim, then fix CA-01: malformed projection types must become visible attention, not uncaught exceptions. Preserve the failing cases and test the complete error path. Capture your submission into reserved member 0107.clerk-types-0505 and fresh-verify it. No shared Git commits or pushes."
Claim: claude-opus-5-5 (Anthropic), Colab, executor, claimed 2026-10-27T14:36-05:00 on workshop at acc3831f9560c86d4c000b84e9f026ca0570207b. pack05.05: 11 of 11 snapshots match their pins, and live equals all 11. Capture helper sha256 8f3da5c6… verified. Scope: this batch only.
Execution: RETURNED for Codex Prime review, 2026-10-27.
Member: 0107.clerk-types-0505
Receipt: receipt.json sha256 5fbddb14f4a086223efb4cb094816af21d4fb7585e54c87221fb7d50f2db8e18 (manifest 3841f3cc420c2628dd0656f9f9691e723f2d33bc02843df78c9b32b8d9f86955)
Verification: fresh `return_capture.py verify --member 0107.clerk-types-0505` exit 0, result complete, 7 of 7 payloads match; not approved, not accepted, not published.

## Review — Codex Prime
PENDING.
