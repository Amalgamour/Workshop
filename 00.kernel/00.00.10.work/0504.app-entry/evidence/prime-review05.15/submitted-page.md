# 05 — Recorded boot through the app entry
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
Claim: Grok 4.7 (xAI), session 01a179d2-387a-7661-8702-6e53f95e96b5, 2026-10-27, HEAD fab74ab2c73d274775ce0971105bb735878f2c50.
Workspace D:/Git/lib-build, branch workshop. Verify evidence/pack05.15/source-manifest.json.

## #01 — Notes and explicit app interface
Notes FIRST in06.15.md; preserve source-before in evidence/boot-entry05.15/before/.
Write CONTRACT.md before code. Add only boot-prepare, boot-check, boot-judge and
boot-show at app/librarian.py, forwarding explicit arguments to the accepted boot
lab. Keep its prepare/check/judge/show semantics and exit0/1/2/3 distinctions.
These commands do not invoke a model or grant a role. Prepare/check/judge write
only the explicitly designated external attempt records as the accepted backend
permits. show is read-only. There is no default records root or live registration.

## #02 — Fixed pins, no second boot implementation
Create app/boot_tools.py and app/prime-boot.json following existing fixed app
bindings. Backend prime_boot.py SHA-25654b23484f9e0812db92a623a8588175702682ebe14f8b0b915111daf51a91534.
Pin all7 dependencies listed in this pack's source manifest/code-pins.json; check
their required code bytes before invoking the backend. Resolve from this app code
root, never a caller command/path override or packet content. Use the current
Python executable and argument arrays, no shell. Forward exact backend UTF-8 output
and exit meanings. Enforce the command's explicit allowed flags; no auto-answer,
auto-judge, ack, claim, queue, dispatch, normal run or hidden workspace writes.
Do not import/recreate validators, packet logic, grading or retry behavior. An
orientation result is not authorization, and supplied reviewer labels are not auth.
Keep same-user check/use limitations honest; no OS-sandbox claim.

## #03 — Meaningful disposable tests
Allowed product: app/librarian.py, new boot_tools.py, prime-boot.json,
new tests/test_boot_tools.py and additive app README. No boot lab, accepted core,
existing tests, kernel, role/assignment or other-lane changes. Use the accepted
boot fixture factory in tests if useful; production must not depend on tests.
Compare direct versus wrapper prepare/check/judge/show on independent equivalent
fixtures (ignore only explicitly nondeterministic paths/times). Cover valid flow,
malformed answers, failed judgement, incomplete-stage replay, read-only show,
unknown/repeated/missing args, wrong pin before launch, explicit record root and
Unicode output. Prove no writes outside declared records apart from test fixtures.
Run new tests plus existing entry/intake tests, sequentially. Do not rerun the full
boot suite for unchanged backend unless a demonstrated failure requires it.
Keep first failures/skips, commands, hashes and limits in tests.txt/verification.json.
Reread fully and disposition notes. No actual model boot, network or live install.

## Local capture
Dedicated submission starts Did, Blocked, Need. Use reserved 0130.boot-entry-0515:
```text
python -B labs/return-capture-pass01/return_capture.py capture --book "D:/Git/lib-build/00.kernel/00.00.10.work" --submission grok-1-0504-0515 --return-file "D:/Git/lib-build/00.kernel/00.00.10.work/0504.app-entry/evidence/boot-entry05.15/submission.md" --source-root "D:/Git/lib-build" --artifact "app/librarian.py|app/librarian.py" --artifact "app/boot_tools.py|app/boot_tools.py" --artifact "app/prime-boot.json|app/prime-boot.json" --artifact "app/tests/test_boot_tools.py|app/tests/test_boot_tools.py" --artifact "app/README.md|app/README.md" --artifact "00.kernel/00.00.10.work/0504.app-entry/06.15.md|00.kernel/00.00.10.work/0504.app-entry/06.15.md" --artifact "00.kernel/00.00.10.work/0504.app-entry/evidence/boot-entry05.15/CONTRACT.md|00.kernel/00.00.10.work/0504.app-entry/evidence/boot-entry05.15/CONTRACT.md" --artifact "00.kernel/00.00.10.work/0504.app-entry/evidence/boot-entry05.15/tests.txt|00.kernel/00.00.10.work/0504.app-entry/evidence/boot-entry05.15/tests.txt" --artifact "00.kernel/00.00.10.work/0504.app-entry/evidence/boot-entry05.15/verification.json|00.kernel/00.00.10.work/0504.app-entry/evidence/boot-entry05.15/verification.json"
python -B labs/return-capture-pass01/return_capture.py verify --book "D:/Git/lib-build/00.kernel/00.00.10.work" --member 0130.boot-entry-0515
```
Keep submitted sources and partial evidence. Never overwrite/remove captures or
allocate around failure. Append pointers/receipt/fresh verify below. No shared Git
stage/commit/push, other-lane changes or new authority. Prime reviews/publishes.
Draft/reservation is not Director release.

## Return pointer
Member 0130.boot-entry-0515. Receipt sha256 bbae480098b46980e8d48cc707e763de016f7a7cd57d3243b5834aa22c2491c4. Verify exit 0: result complete; not approved; not accepted; not published.

## Review — Codex Prime
PENDING.
