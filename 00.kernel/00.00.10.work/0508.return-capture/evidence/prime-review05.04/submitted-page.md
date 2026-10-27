# 05 — Read-only structured inspection of one return member
version: 001
Authorization: draft — 2026-10-27
who: Codex Prime
state: released by the Director 2026-10-27; claimed by Grok Builder 2
Face: 05
PPPP: 0508
book: 00.00.10.work

## Assignment
Executor: Grok Builder 2. Reviewer: Codex Prime.
Release: Director, this session, 2026-10-27. Claim: Grok Builder 2, this page only.
Workspace D:/Git/lib-build, branch workshop. Verify exact supplied snapshots in
evidence/pack05.04/source-manifest.json before editing. No shared Git writes.
Source snapshots pin supplied bytes, not an invented single historical commit.

## #01 — Contract and immutable dependency
Notes FIRST on 06.05.md. Preserve before bytes and write CONTRACT.md under
evidence/inspection05.04/ before code. Build one read-only inspection command for
an explicitly named book/member; no enumeration, queue or allocation. Product
files: new labs/return-capture-pass01/return_inspect.py, new tests/test_return_inspect.py,
and an additive README section. The accepted return_capture.py is IMMUTABLE:
Grok-1's active pack pins it. Do not edit it, its tests or CLI to add inspection.
The new module verifies that fixed sibling's full SHA-256 before importing it,
then reuses its reader guards, strict parsing and reservation/verify_member
validation. No copied hash/receipt validator or parsing the human verify text.
No data file is code, no caller-selected helper, no highest-version fallback.

## #02 — A small provisional projection
Expose `return_inspect.py inspect --book ABS --member NAME --json`.
Define return-capture-inspection/1 in CONTRACT.md, with exact keys/types and
concrete examples. Include canonical book path, requested member, observation
status (complete/reserved/missing/incomplete/refused), verified capture identity
and hashes for a complete package, validated origin/submission metadata where
available, and explicit problems for noncomplete results. Use the accepted
validator as the source of integrity truth. Preserve both return hash/length and
receipt hash; the latter binds this precise capture. Do not manufacture identity
from missing/damaged receipt or merely trusting stored hash strings.
A complete observation reports capture integrity only. Review/acceptance/seating/
publication are OUTSIDE SCOPE, not false claims that those decisions never occurred.
An empty slot, valid reservation, partial payload, bad hashes, duplicate/malformed
metadata and unreadable member must be distinguishable without claiming success.
For a well-formed --json invocation emit one strict JSON object even on refusal;
document exact exit codes. Invalid CLI syntax may use ordinary argparse errors.
Reserved/missing are informational, not complete. No writes, temp markers,
automatic repair, Git/network commands or source/member changes.

## #03 — Verify useful reads and honest failure states
Use disposable copied code and members created by the copied accepted helper.
Test complete, reserved-only, missing, partial before receipt, mutated return,
payload/manifest/receipt/reservation mutation, malformed/duplicate-key metadata,
wrong helper hash, path escape, linked/hard-linked inputs and Git-backed books.
Assert observation status, exit, hashes/identity rules, no traceback and every
source/member/Git index/ref byte unchanged around inspection. A repeated read
creates nothing. Retain initial failures and privilege skips in tests.txt and
verification.json. Demonstrate a fresh-process complete read and a noncomplete
read. Pin-check the unchanged core; use its public verify on fixtures to confirm
agreement. Do not rerun unrelated app/Clerk/Prime suites or mutate live members.
Fully reread and disposition notes. No historical backfill, other lane code,
kernel changes, app installation, shared Git writes or model execution.

## #05 — Capture the submission locally
Verify unchanged capture helper SHA-256 8f3da5c651f6924fca6dedb0b95da7d181eb58884dc030dd9cbc3d8b6a5b15ac. The member
0110.return-inspection-0504 is already reserved. Complete every declared output or report the
missing item; do not fabricate evidence. Write dedicated evidence/inspection05.04/
submission.md beginning Did, Blocked, Need with hashes, results and limits.
Run from D:/Git/lib-build:

```text
python -B labs/return-capture-pass01/return_capture.py capture --book "D:/Git/lib-build/00.kernel/00.00.10.work" --submission grok-2-0508-0504 --return-file "D:/Git/lib-build/00.kernel/00.00.10.work/0508.return-capture/evidence/inspection05.04/submission.md" --source-root "D:/Git/lib-build" --artifact "labs/return-capture-pass01/return_inspect.py|labs/return-capture-pass01/return_inspect.py" --artifact "labs/return-capture-pass01/tests/test_return_inspect.py|labs/return-capture-pass01/tests/test_return_inspect.py" --artifact "labs/return-capture-pass01/README.md|labs/return-capture-pass01/README.md" --artifact "00.kernel/00.00.10.work/0508.return-capture/06.05.md|00.kernel/00.00.10.work/0508.return-capture/06.05.md" --artifact "00.kernel/00.00.10.work/0508.return-capture/evidence/inspection05.04/CONTRACT.md|00.kernel/00.00.10.work/0508.return-capture/evidence/inspection05.04/CONTRACT.md" --artifact "00.kernel/00.00.10.work/0508.return-capture/evidence/inspection05.04/tests.txt|00.kernel/00.00.10.work/0508.return-capture/evidence/inspection05.04/tests.txt" --artifact "00.kernel/00.00.10.work/0508.return-capture/evidence/inspection05.04/verification.json|00.kernel/00.00.10.work/0508.return-capture/evidence/inspection05.04/verification.json"
python -B labs/return-capture-pass01/return_capture.py verify --book "D:/Git/lib-build/00.kernel/00.00.10.work" --member 0110.return-inspection-0504
```

Preserve source/submission. Append only member, receipt hash and fresh verification
result below. A partial/refused capture stays explicit; no overwrite, receipt
removal or silent allocation around failure. Prime reviews/publishes separately.
This draft and reservation grant no execution authority or future scope.

## Return pointer
Member: 0110.return-inspection-0504
Receipt: 06173d2dc254efc0046a143cbfab12e1d3e4ded036c8448a0d0b813539020d81
Verification: result complete. Not approved. Not accepted. Not published. Exit 0.

## Review — Codex Prime
PENDING.
