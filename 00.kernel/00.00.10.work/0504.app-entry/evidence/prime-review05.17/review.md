# Prime review — 0504/05.17
Date: 2026-10-28. Reviewer: Codex Prime.

HELD for CH-03/CH-04 failure reporting before app integration. Independent submitted
suite and demo exit0. Suite reports1 pass,25 expected refusals,1 file-symlink privilege
skip,0 failures. Fresh0139 capture verify is complete, not acceptance.
CH-01 final-report returned-artifact binding and CH-02 durable handoff identity are
implemented and exercised. Clean retry is read-only; partial evidence is retained.

CH-03: a real disposable stop immediately after successful capture leaves return.md,
manifest, receipt and payloads in the member, but stdout lists only intent/failure-log
writes and no retained member. failure.log still carries the earlier reserved
inspection and its writes omit the capture. The report must distinguish actual
capture outcome and observed retained files from earlier state, including when a
subprocess times out or cannot be re-inspected. Unobserved must stay unknown.

CH-04: injected OSError while writing failure_log after an after-intent stop escapes
execute() as an uncaught exception. Failure reporting must not destroy the controlled
refusal/attention result. Keep original reason, any reporting error and existing
partial bytes, return exit2 and never finish or overwrite the handoff.

Attached verification.json retains exact stdout and failure log from the first
countercase, plus the uncaught error from the second. Source return and0139 are
unchanged. Next bounded work is these failure-reporting repairs only; no app wiring,
live jobs, authority, queues or new recovery process.
