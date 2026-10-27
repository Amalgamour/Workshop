# 05 — Read-only Prime status through the app entry
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
Claim: Grok 4.7 (xAI), session 01a179d2-387a-7661-8702-6e53f95e96b5, 2026-10-27, HEAD aaeb8dc4cd5a3e42342a7e79427f481c9f05896e.
Workspace D:/Git/lib-build, branch workshop. Verify evidence/pack05.14/source-manifest.json.

## #01 — Notes and contract
Notes FIRST in06.14.md; preserve source-before under evidence/intake05.14/before/.
Write CONTRACT.md before code. Add only prime-status --registry ABS --json through
app/librarian.py. It exposes accepted prime_support status, not a new queue or
planner. Registry is explicitly supplied data, never installed/discovered by this
wrapper. No role/assignment edits, acknowledgment, claim, dispatch or model call.

## #02 — Fixed read-only binding
Create app/prime_intake.py and app/prime-intake.json, following the fixed-binding
pattern of the app pack tools. Resolve code paths from this app's code root, not
from registry content/caller cwd. Pin prime_support.py700d60d2e49c186d49e56a9a38058e21a722b4a5dd79d461453a305e8d904f70,
its sibling clerk_adapter.py2f30ba751f78ec9f7d2995739bebde0e3b6509eeab35ae29a9078385ff33f8d4
and Clerk core f697a7e443117c3d1face62d3021f7634154d76214b77fadec1a5cc3c99d394c.
Check required code bytes before invoking the accepted tool. No shell, arbitrary
command/path override, guessed pins or new validator. Use the current Python
executable and an argument array. Preserve the accepted tool's JSON projection,
status/attention meaning and exit distinctions. UTF-8 output must remain lossless.
No selected attention entry grants authority. Read-only calls may not create app
scratch, registry, store, acknowledgment, bytecode or book files. A changed pin
refuses before backend execution. State remaining check/use gaps honestly.

## #03 — Meaningful fixture verification
Allowed product: app/librarian.py, new prime_intake.py, prime-intake.json,
new tests/test_prime_intake.py, additive app README only. No accepted lab/core,
existing tests, kernel, boot lab or other builder edits. Disposable fixtures:
compare wrapper JSON/status exits with direct pinned status on the same registry;
cover normal attention, malformed/missing registry, unsupported/malformed args,
wrong tool/adapter/core pin before execution, non-ASCII data and caller cwd.
Assert source/Git/store/registry bytes unchanged; no hidden ack/queue/launch.
Run new tests and existing entry/pack-wrapper tests sequentially; no full bridge
suite absent a demonstrated reason. Normal run stays refused. Reread/disposition
notes and record commands, first failures, counts/skips and hashes in tests.txt
and verification.json. No live registry install or actual model boot.

## #04 — Local capture
Dedicated evidence/intake05.14/submission.md starts Did, Blocked, Need.
Use reserved 0127.prime-intake-0514 and9 outputs, then freshly verify:
```text
python -B labs/return-capture-pass01/return_capture.py capture --book "D:/Git/lib-build/00.kernel/00.00.10.work" --submission grok-1-0504-0514 --return-file "D:/Git/lib-build/00.kernel/00.00.10.work/0504.app-entry/evidence/intake05.14/submission.md" --source-root "D:/Git/lib-build" --artifact "app/librarian.py|app/librarian.py" --artifact "app/prime_intake.py|app/prime_intake.py" --artifact "app/prime-intake.json|app/prime-intake.json" --artifact "app/tests/test_prime_intake.py|app/tests/test_prime_intake.py" --artifact "app/README.md|app/README.md" --artifact "00.kernel/00.00.10.work/0504.app-entry/06.14.md|00.kernel/00.00.10.work/0504.app-entry/06.14.md" --artifact "00.kernel/00.00.10.work/0504.app-entry/evidence/intake05.14/CONTRACT.md|00.kernel/00.00.10.work/0504.app-entry/evidence/intake05.14/CONTRACT.md" --artifact "00.kernel/00.00.10.work/0504.app-entry/evidence/intake05.14/tests.txt|00.kernel/00.00.10.work/0504.app-entry/evidence/intake05.14/tests.txt" --artifact "00.kernel/00.00.10.work/0504.app-entry/evidence/intake05.14/verification.json|00.kernel/00.00.10.work/0504.app-entry/evidence/intake05.14/verification.json"
python -B labs/return-capture-pass01/return_capture.py verify --book "D:/Git/lib-build/00.kernel/00.00.10.work" --member 0127.prime-intake-0514
```
Append pointer/receipt/fresh verify. Partial captures remain explicit, no overwrite
or allocating around failure. No shared Git stage/commit/push. Prime publishes.

## Return pointer
Member 0127.prime-intake-0514. Receipt sha256 44a362555e099d5362b46dd4b63514698893c9d00e14a4255f2977854389a8f0. Verify exit 0: result complete; not approved; not accepted; not published.

## Review — Codex Prime
PENDING.
