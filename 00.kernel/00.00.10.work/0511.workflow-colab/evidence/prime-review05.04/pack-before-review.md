# 05.04 — Page-local Colab custody and subsequent passes
date: 2026-11-01
who: Codex Prime
state: Director-approved pack; execute only on named invocation
executor: Grok-2
reviewer: Codex Prime

## Purpose, source of truth and role
Build the missing workflow substrate identified in Claude's corrected 0510/05.06
design and Prime review. This is an ordinary bounded build/self-test, not a fresh
independent review or a live-workflow activation. Read those documents completely,
the N7NN routing record on 0510/06.08, and relevant current workflow source.
The review conditions govern where the prototype disagrees with its contract.
Do not copy prototype readiness results into an authority mechanism.

Selected route: ordinary and reserved N7NN work keeps 05.NN.pack.md,
05.NN.return.md and 06.NN.review.md on the same investigation page. N5NN uses its
matching N1NN line. This build does not reserve any N1NN member for N7NN, migrate
legacy captures or ask the Director to choose the route again.

NEW labs/colab-workflow-pass03 only. Preserve workflow pass02 and prior evidence.
Write a delta contract and failure/recovery plan before code. Verify frozen inputs
with compute; unexpected changes are findings, not permission to repin another
lane. Record the exact named invocation/claim here and notes in NEW 06.04.md.

## #01 — K1, exact page-local return sealing
Provide seal-return-local --book ABS --page NNNN.name --pass 05.NN
--return-file ABS --declared-transport TEXT (or a documented equally explicit
interface). Require an existing attached package/pass. Store the exact supplied
bytes as the page-local 05.NN.return.md and associate raw length/hash, package
digest, pass and declared transport with that return. Transport is a supplied
label, not authenticated provenance. Preserve an internal immutable copy if the
existing projection model requires it; choose one canonical byte identity.

Identical replay with the same declared identity is a no-op. Different occupied
content refuses without changing the previous record or return. A changed
transport label must not silently rewrite the original provenance. Reject links,
unsafe paths, nonregular inputs and declared limit violations. Read-back and
later operations must detect disagreement among the stored bytes, slot and seal.
Return-byte integrity is not semantic acceptance or release.

## #02 — K2, explicitly requested next pass
Provide open-pass --book ABS --page NNNN.name --pass 05.MM. Require exactly one
recorded request-next review naming that later pass on the same page, with its
prerequisite package and sealed return intact. No arbitrary pass allocation from
chat, return prose or an unrecorded proposal. Use the existing 05.NN grammar and
names. Refuse self/earlier pass, conflicting requests, occupied different state
and missing prerequisites. Define safe identical replay; do not erase a slot.
Create only the new slot and its appropriate projections; no fabricated pack,
return or review content and no model launch. Keep earlier passes byte-identical
except explicitly derived index/pointer projections with preserved inputs.

## #03 — K3, retained transition evidence
Keep the transition history inside the existing investigation fact-store, not a
second queue/status authority. Version the changed record/return shape explicitly.
Record the exact pass/package/return/review associations and sequence needed to
inspect open -> attach -> seal-return -> review -> open-pass. A replay appends no
duplicate transition. Each write preserves the prior transition prefix; reads
check sequence, links, hashes and consistency with slots. Document precisely
what is checked against a retained prior seal/checkpoint. A full external rewrite
with all hashes recomputed is not prevented by an internal hash chain: do not
claim authentication, external chronology or tamper-proofing.

Use supplied review judgments; compute does not decide their meaning. Keep
record-review protections and conflicting-return/review refusals. Expose history
through read-only show or a documented read view. Preserve explicit_finish,
review_recorded and return placement distinctions; review_pending=false alone
must not be described as complete. Do not add reserved exposure gates in this
slice. The later checker owns V01–V03 from the 0510 review.

## #04 — consistent writes, interruption and compatibility
Reuse existing path/link/live-book protections and pinned full producer verify
on attach. No weaker verifier or pin bypass. Preserve ordinary command behavior
where compatible with the new page-local route. Keep pass02 available for legacy
records; do not silently migrate existing books or claim byte-identical schemas
after adding fields. State the compatibility boundary explicitly.

Specify the write sequence for return bytes, projections, record, seal and
transition history. An interrupted operation must remain visibly partial/refused,
never falsely complete. Preserve the old authoritative data and diagnostic facts;
define a bounded recovery or clear stop-for-Prime result instead of ad hoc cleanup.
Do not remove stale/lock/partial protections to make tests pass. No hard-link race
probes or race-freedom/power-loss guarantee is requested; AR-01 remains held.

## #05 — focused acceptance and one ordinary two-pass path
Run in NEW disposable books outside the checkout; keep live-book refusal. Show
ordinary open/attach -> local return -> supplied request-next review -> open-pass
-> second attach/local return/review, with correct N7NN tails and no N1NN member.
Use actual pinned producer verification for the attach path; sources may be
existing committed Git blobs. Read-only Git-object queries are allowed. If a
legitimate source/package is missing, preserve the block rather than fabricate a
receipt or commit. No Git writes or descriptor-packaging H2 experiment here.

Cover LF and CRLF return preservation, identical replay/no extra event, conflicting
return, wrong pass/package, request-next prerequisite failures, transition/slot
tamper, page-local raw-byte tamper, read-only inspection, and injected interrupted
writes at meaningful boundaries. Assert the entire earlier sealed pass survives
later work. Separate real-tool evidence from mocked/synthetic fixture evidence.
Retain relevant existing protective cases by adapting tests to NEW fixtures; no
automatic broad producer/capture/app suites. Record skips as skips. Test runners
must return failure if required child steps fail (0510 V04), while preserving all
partial output. Every execution gets a unique run directory, never clearing one.

## Scope, outputs and stop
Allowed NEW labs/colab-workflow-pass03; NEW 0511/06.04.md;
NEW evidence/build05.04; this pack's invocation/claim/return pointer. External
disposable fixtures allowed. Prime owns this pack's review section. No edits to
the active app/README/door/loop/cycle/constructor, old workflow/producer/checker,
kernel/law/00.live, other worker lanes or old captures. No network/Git writes,
installs, models, paid APIs, scheduled jobs or live custody/migration work.

Return Did, Blocked, Need; CONTRACT and API/schema delta, PRIME-USE with exact
commands, failure/recovery contract, compatibility limits, test commands/exits,
fixtures and source before/after. Include Factfind/Hostile/Overflow/Unprompted,
verification.json, submission.md and artifact-manifest.json binding final notes,
new lab and evidence by bytes/hash, excluding itself. Put submission/manifest
hashes on this pack. Reread the return and integrate notes. Matching 0111 custody
stays pending; no fabricated receipt or new capture slot. Stop for Codex Prime
review. Passing tests do not select live tooling, approve findings or release
another pack. If a policy/authority fork appears, stop and elevate it under 0412.

## Return pointer
Release: the Director, this session, 2026-11-01: "Work in D:\Git\lib-build on workshop. Run: D:\Git\lib-build\00.kernel\00.00.10.work\0511.workflow-colab\05.04.md Read the complete pack, Claude’s corrected design and Prime’s review conditions. Verify frozen inputs and record this invocation and your claim. Build only the isolated workflow successor: exact page-local N7NN return sealing; opening the next pass from a recorded request; retained transitions and consistent interrupted-write handling. Preserve previous work and existing protections. Test in new disposable books. No active app integration, legacy migration or Git writes. Follow the pack’s return instructions. Stop for Codex Prime review."
Claim: Grok-2, this session, 2026-11-01. Scope 0511.workflow-colab/05.04 only. This builder adds labs/colab-workflow-pass03. The successor seals an exact page-local N7NN return, opens a later pass only from one recorded request-next review, and keeps transition history in the investigation record. Workflow pass02, its evidence, the producer, the checker, the app, the constructor lane, and prior captures stay unmodified. This builder does not commit. HEAD when the claim was recorded: 960d20c5290656095df8457b1740d2d5e586b111, branch workshop. Frozen inputs 40, bad count 0. Python 3.14.0. accepted is false. committed_by_this_builder is false.
Submission: 00.kernel/00.00.10.work/0511.workflow-colab/evidence/build05.04/submission.md sha256 f65a56bdfe4d15a0e2a5a54129c07d4cbf6c92a29797a5f09f41e7c375af74fa, 11277 bytes.
Artifact manifest: 00.kernel/00.00.10.work/0511.workflow-colab/evidence/build05.04/artifact-manifest.json sha256 90b9c2bf69131a13e3100466571cb484fdc18fb99b02ff7fd72a806aeed568c1, 4067 bytes. The manifest lists 16 files and excludes itself.

## Review - Codex Prime
PENDING.
