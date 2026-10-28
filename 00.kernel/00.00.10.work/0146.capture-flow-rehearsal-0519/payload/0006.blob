# Contract — disposable capture-flow rehearsal
Date: 2026-10-28
Schema: flow05.19-contract
State: expected outcomes, written after 06.19.md and before code.

This contract is the fixture proof for `labs/capture-flow-rehearsal-pass01`. It does not wire the app, seat a workflow, or accept a return. A verified receipt is custody. It is not review, acceptance, acknowledgement, closure, or publication.

## Closure before execution
The harness hash-checks `evidence/pack05.19/source-manifest.json` (`5c492c54e15a47a5bdf6f9231d619de428335ba470899e09e1b077d098613ef0`, 7167 bytes) and `source-provenance.json` (`b6b255dcafd42696525dd2600b2049c1fbfea6eb943fcdd27389bfc07d1c7909`, 5499 bytes). Every snapshot must match. The path sets must match. Bad count 0.

It then writes the declared tool closure into a disposable source-view and hashes that view before import. The closure is `app/context.py`, `app/clerk_seam.py`, `app/clerk-seam.json`, `app/worker_bridge.py`, `app/worker-bridge.json`, `app/development-workspace.json`, the pinned Clerk, the pinned return-capture pair, `labs/capture-handoff-pass01/handoff.py`, and the eight bridge files named by `worker-bridge.json`.

`app/librarian.py` is not copied. Its accepted snapshot stays `a320f270dd87508d4fa9d3d5e78904108605fa308abb3ebd86513ae9c3c01fab`. The live file may differ and must be left untouched.

The runner `00.kernel/00.00.01.law/0302.run/02.run.003.py` is copied only when its bytes are sha256 `bbca135691ba4e873e27b9322b1ad6d79deeb59107eb7d377f7d20014067d50c` (10143 bytes). The result records it as a declared config pin, not a pack snapshot. A mismatch is a gap. The harness stops. It does not scan the checkout for another runner.

A tampered closure file is a refusal before import and before any protocol-worker subprocess. A relative binding path is a refusal before a tool launch. A fixture root that is the source-view is a refusal before launch (`fixture root is the live workspace`). An artifact source that is not a simple filename is a refusal before Clerk show, capture, or the worker.

## Complete flow
Fixture setup is explicit and disposable. The root, the Clerk store, and the book are absolute directories outside the checkout and outside Git. The store does not overlap the fixture root and sits inside the named container. Setup writes the design task, the design bridge job, and the design Clerk job from snapshot bytes. It also writes a synthetic assignment record inside the fixture only, with state released, so the accepted context check can resolve that disposable root. That record is not the live kernel page and it is not a release. Setup queues and claims job `clerk-0001` for `fixture-worker`. Those two calls are setup, not a new lifecycle.

`clerk_seam.perform` then runs one `fixture-ok` protocol test worker. The worker is not a model. Success means exit 0, transport delivered, collection collected, and the Clerk line returned or already-recorded. Review is not performed. Acceptance is not performed. The stdout does not say approval.

Exactly one launch line is written: `bridge-0001 ok`. Exactly one `0003.returned.json` exists. `result.json` is the SYNTHETIC final-report payload. Its bytes are preserved from the worker output into the report source, the Clerk outbox, `return.md`, and the payload blob. Those four copies compare equal. The known digest for the design task's count of three is `0c07187ea6d064441225b3cba26a7b1e8bc702fcf332b457dae8e26892ba68a6`. Transport evidence is recorded separately and is not that file.

The rehearsal then pre-reserves a disposable member and calls the accepted handoff. The binding schema is `clerk-capture-handoff/1`. `work_ref` is the supplied label `00.kernel/00.00.10.work/0504.app-entry/05.01.md`, recorded as a declared label. Origin is book `00.00.10.work`, page `0504.app-entry`, batch `05.19`, and that origin matches the fixture reservation. The reservation release string says it is a fixture reservation, not a Director release.

Handoff exit 0. Stdout contains `result ok`, `result complete`, `not approved`, `not accepted`, and `not published`. The member holds `return.md`, `manifest.json`, `receipt.json`, and the payload. The handoff record holds `intent.json` and `completed.json`.

## Read-only repetition
The same seam delivery and the same handoff run again on that fixture. The launch log stays one `bridge-0001 ok` line. The returned event file stays one and its bytes stay the same. Source `result.json`, the Clerk job files, the member files, and the handoff record files are unchanged. The second handoff prints `writes none` and exits 0. This is one fixture observation. It is not a general exactly-once guarantee.

## Changed binding and changed payload
A second binding whose returned-event hash differs is refused with `returned event does not match the binding`. Exit 2. No additional worker launch. The member bytes stay as they were.

Changing the report source bytes, leaving the outbox and the original binding in place, is refused because the source bytes are not the outbox bytes. Exit 2. No additional worker launch. The member bytes stay as they were. The rehearsal does not repair, delete, or recapture.

## Failed delivery
A separate fixture uses backend `fixture-crash`, the same allowlisted protocol test worker in its crash mode. The seam does not return success. No `0003.returned.json` is written. No outbox `result.json` is written. The rehearsal does not reserve a member and does not call handoff. The launch line is `bridge-0001 crash`. No capture files exist.

## Stop after capture
A separate success delivery is handed off with the private hook returning `stop` at `after-capture`. Exit 2. Stdout begins `attention: stopped after-capture` and ends `result attention`. It also reports `member-written observed`, `custody complete`, `observed-record intent.json`, `record-absent completed.json`, and `handoff-complete no`. The failure record keeps `result captured` and a before-capture phase of `reserved`. The member still holds `return.md`, `manifest.json`, `receipt.json`, and the payload, and `return.md` still equals the synthetic report. `completed.json` is absent.

The next handoff call, with no stop hook, is attention: `complete capture has no completed handoff record`. It does not write `completed.json`, does not replace the member, and does not launch another worker. The receipt bytes stay the same. The rehearsal does not resume or allocate another member.

## Evidence
`results.json` embeds the source-view manifest, the fixture request identities, the raw seam and handoff outputs, the byte comparisons, the launch and event counts, and the before and after tree indexes. It does not point at deleted temporary files as the only record. Fixture acts are labeled fixture. Unknowns stay labeled unknown.

The suite covers the cases above. It does not run the unchanged Clerk, bridge, or handoff suites. It records the hashes of the live app, the pinned tools, the runner, and `0146` before and after, and those hashes must match. Cleanup removes only the owned temporary roots.

## Out of scope
No edit to app files, handoff, Clerk, bridge, or kernel law. No live queue, job, role, registry, canonical assignment, or batch-pointer mutation inside the fixture product. No model. No second receipt validator. No recovery.
