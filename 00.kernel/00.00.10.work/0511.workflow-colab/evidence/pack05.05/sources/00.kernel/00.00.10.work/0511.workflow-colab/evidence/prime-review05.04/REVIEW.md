# Prime review — 0511.workflow-colab / 05.04
Date: 2026-11-01. Reviewer: Codex Prime.
Disposition: useful isolated implementation; correction required before routine use or selection.

## Verified progress
All 40 frozen source rows match snapshots and live bytes; all 16 artifact rows match. Inspected the new transition/load/seal/open-pass/commit paths against pass02 and the return, contract and failure plan. Independently ran the unchanged focused runner on Python 3.12.14 into NEW Prime evidence: 10 synthetic tests passed, one file-symlink privilege skip, plus the real producer-backed two-pass path passed. No full old/app suites or live book were run.

The successful path now does open -> attach -> local seal -> request-next review -> open-pass -> second attach/seal/review on one N7NN page. Return bytes, transport provenance, replays, prerequisite checks and transition/slot projections are inspectable. No N1NN allocation is required for the selected path. Schema /1 history remains with pass02; no migration is implied. The 64-transition cap is an explicit bounded limit, not unlimited workflow history.

## WF01 — mid-write failure can destroy the prior record
The pack requires preserving old authoritative data. write_bytes uses O_TRUNC on existing files. The submitted injection hook runs before open/truncation, so its successful preservation cases do not establish behavior after writing begins. FAILURE.md explicitly excludes that point; this leaves an important requirement unmet.

Independent controlled fixture: after opening a new disposable page, inject a partial os.write followed by OSError while committing investigation.json. The module returns interrupted write and leaves partial.json, correctly refusing later use. But the previous 768-byte record becomes 384 bytes; the old seal remains. No retained prior-record checkpoint is established by the implementation. This is an injected I/O failure, not a real crash or power-loss experiment, and only the NEW fixture was affected.

Required repair: preserve a verifiable prior record/seal pair before mutating authoritative files and avoid in-place truncation of those records. Stage/exclusively create candidate bytes and publish with a defined replacement protocol, retaining prior bytes and clear partial evidence. An interrupted operation need not auto-recover, but Prime must be able to inspect/recover the prior sealed state from preserved files, not reconstruct it from memory or incomplete projections. Test mid-write failure as well as before-write hooks. No race-freedom or power-loss guarantee is requested.

## Remaining boundary
K1/K2/K3 are useful substrate, not the reserved exposure checker or app wiring. Hash chains prove internal consistency with a recorded prefix, not resistance to wholesale external rewriting. Stop-on-partial is honest but insufficient if it also loses the only authoritative prior bytes. Keep the existing source, return and tests; repair in a new successor. Also provide the explicitly requested PRIME-USE artifact with exact fixture/command prerequisites; do not make the operator reconstruct them from test source alone.

Next pack prepared for Grok-2: 0511/05.05, isolated workflow pass04 preservation repair. No app/live selection, receipt, capture allocation, kernel change or new authority is granted by this review.
