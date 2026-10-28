Did
The Director released 0504.app-entry/05.18 on 2026-10-28. Claim: Grok 4.7 (xAI), session 01a179d2-387a-7661-8702-6e53f95e96b5, 2026-10-28, HEAD befac9fe0dacdae15522187a14a887dadad571bc. Pack manifest cdc02fe6afa125b77c96b58bfe3e90b2ab73e9a874f5b170cac1d311d94fbbda matched its eleven snapshots before that release line was recorded.

The repair is in labs/capture-handoff-pass01. CH-01 and CH-02 guards stay. After a capture attempt, a failure report separates that attempt from the adapter's record writes. A later return_inspect observation is the current member state. The reserved inspection stays an earlier phase. If pins, a timeout, inspection, or a safe read fail, the report says unknown or unverified and does not claim that the child wrote nothing. An OSError or controlled refusal while writing the failure log keeps the original reason, reports the secondary error, keeps any partial log bytes, and returns exit 2. The adapter does not queue, claim, return, reserve, recover, or wire app/librarian.py.

Before: Prime's disposable stop after a successful capture exited 2 with stdout "attention: stopped after-capture", one intent write, one failure-log write, and "result attention". The member already held return.md, manifest.json, receipt.json, and payload blobs. failure.log still stored the pre-capture reserved inspection. An injected OSError, message "injected failure-log write error", then escaped execute() uncaught.

After: the passing stop-after-capture case still starts "attention: stopped after-capture" and ends "result attention". It also reports member-written observed, custody complete, observed-record intent.json, record-absent completed.json, handoff-complete no, and the retained return.md path. The current inspect.status is complete. The before-capture phase is reserved. tool_stdout still contains "result captured". completed.json is absent, and the retry does not recapture. The failure-log OSError cases return exit 2 with no traceback. Stdout keeps the original pin reason first and adds "reporting-error failure log: OSError: injected failure-log write error". No file is created when the error is raised before any bytes. A partial log stays the bytes partial\n and is not overwritten.

The suite exited 0. evidence/failure05.18/tests.txt is sha256 2608af93343feea462c9954fef2caa52609155dbd6616cd2d68070e932d41aae, 2851 bytes. Summary: pass 1, expected-refusal 31, skip 1, fail 0. The demo exited 0 and printed result complete, not approved, not accepted, and not published. The retry printed writes none. The success path printed demo failure-log absent.

evidence/failure05.18/verification.json is sha256 325345592e8b379bb1e7c6979a05c45a2ef76fba0e9126e0304bce3badba5aaa, 4303 bytes. It hashes the captured sources and does not hash itself.

Blocked
Nothing in this fixture slice stopped the repair. File-symlink creation returned WinError 1314, and that single case was skipped.

Need
Codex Prime review. No acceptance, acknowledgement, closure, or publication is claimed. A verified receipt is custody, not acceptance. The same-user gap between a hash read and a later write remains open. This module is not an operating-system sandbox. An observation that cannot be read stays unknown. The app stays unwired. There is no automatic recovery.
