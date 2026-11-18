# Prime desk

Book `00.00.10.work` role `prime`.
Root: `D:\librarian\temp\two-prime-returns-review-nov01\desk-demo\book-0522`.
Observed: 2026-11-01T17:49:57Z.
Coverage: Declared request paths only. Unregistered sources were not searched. Matched 21, missing 0, stale 0, changed 0.

## 1. Context and purpose

goal: goal page (`0401.goal/01.md` matched 20f23f4cfed6 5914 basis observed). Label basis supplied.
scope: seats page (`0408.seats/01.md` matched dbf2399d5285 2031 basis observed). Label basis supplied.
authority: desk-app direction (`0416.desk-app/01.003.md` matched d432c796404f 4617 basis observed). Label basis supplied.
This view does not grant authority.

## 2. Current work

Selected: work-0522-0504 `0522.review-construction/05.04`.
Rule: assignment-record/v1.
Source: `0522.review-construction/05.04.md` matched efe9ae39305f 10802 basis observed.
Record current_work: `00.kernel/00.00.10.work/0522.review-construction/05.04.md`.
Legacy selector: work-0521-0503. Agrees: False. Hint only.
Review home: `0122.review-construction/05.04` basis unknown. Pending custody. The derived review file is not a matched declared source. No receipt is fabricated.
Verified result: `verified.md` matched 8f5a1374b3eb 9 basis observed. Basis observed. a matching hash proves these bytes, not acceptance or process freshness
Checkpoint: `checkpoint.md` matched a252f87b9c2c 11 basis observed. Basis observed.
Next route: none. Basis unknown.
Declared and not selected:
- work-0521-0503 `0521.return-placement/05.03` not the canonical assignment record.
- work-0522-0503 `0522.review-construction/05.03` not the canonical assignment record.
Catalog index names: work-0522-0504. Used for selection: false.

## 3. Attention

Open declared attention: 1. Listed in full.
- open hold hold-live: live desk activation is not approved (`0420.prime-desk/01.md` matched 557226b48a27 4153 basis observed).
Observed gaps: 3. Listed in full.
- selector-disagreement prime-desk-selector/1: legacy selector names work-0521-0503; canonical assignment names work-0522-0504. The canonical assignment is kept.
- custody-pending 0122.review-construction/05.04: Pending custody. The derived review file is not a matched declared source. No receipt is fabricated.
- worker-unknown workers:grok-2: no recorded evidence file; process activity is unknown
Unregistered sources were not searched. That is not a report that none exist.

## 4. Workers

- grok-2 on work-0522-0504: recorded none (`none` absent none none basis unknown). Association basis supplied. Process activity: unknown.
  supplied codex-prime: Director says the worker is running Limit: supplied label, not a live process check

## 5. Operations

- desk-state `labs/desk-state-pass01/desk_state.py` matched 4d924bf6549f 55144 basis observed. Limitation (supplied): view launches subprocesses; this desk does not call it Past tests unknown (unknown). Activation unknown (unknown). Executed: false.
- prime-brief `labs/prime-brief-pass01/prime_brief.py` matched 302ed832d2fa 22747 basis observed. Limitation (supplied): build was not called Past tests unknown (unknown). Activation unknown (unknown). Executed: false.
- state-projection `labs/state-projection-pass01/state_projection.py` matched b349da5cef51 20338 basis observed. Limitation (supplied): project and inspect were not called Past tests unknown (unknown). Activation unknown (unknown). Executed: false.
- prime-support `labs/prime-support-pass01/prime_support.py` matched 700d60d2e49c 59791 basis observed. Limitation (supplied): status uses Git; this desk does not call it Past tests unknown (unknown). Activation unknown (unknown). Executed: false.
- review-loop no file. Limitation (tool): Pending. Successor modules were not imported. Past tests unknown (unknown). Activation unknown (unknown). Executed: false.

## 6. Record

Director and model wording are attribution spans, not request roles.
- director dir bytes 111:403 ambiguous False (`0420.prime-desk/06.01.md` matched 2e5fe132ea0b 834 basis observed).
- model mod bytes 430:834 ambiguous False (`0420.prime-desk/06.01.md` matched 2e5fe132ea0b 834 basis observed).
talk: quoted command (`talk.md` matched 0185bd225351 26 basis observed). Not parsed. Not executable.
assignment_state `returned` basis observed. assignment_state is a record field, not a live process check. validate_context was not called.
History records: 1. Bodies are not copied.
- hist-0419 `0419.work-history/01.md` matched 51a55a7ad8f4 4405 basis observed.

## 7. Inspectability

Request sha256: 509d049064a2fac5cab41ca9dab6027b0666f8cbe2f618de834a89089fd94905.
Fingerprint: a2dbc9ecbf9e3d12db072066ea30b67b10227f630b748df5094a8f49f38832d7.
observed = declared bytes matched; supplied = caller label; unknown = not present; stale = different bytes withheld; changed = bytes moved during the read and were withheld
Read the gaps and open attention. Keep the canonical assignment. Do not treat a supplied label or a legacy selector as the current work. Escalation: Codex Prime on 0524.prime-desk/05.02. This tool does not decide meaning, acceptance, or live authority.

## Packet

### Assignment
```
# 05 - Real custody into the Prime review loop
version: 001
date: 2026-11-01
who: Codex Prime
state: prepared for named Director invocation
book: 00.00.10.work
PPPP: 0522
Face: 05

## Assignment
Executor Grok-2. Reviewer Codex Prime. Work D:/Git/lib-build on workshop.
Director requested this repair after Prime reviewed both returned lanes. Record
invocation/claim and verify evidence/pack05.04/source-manifest.json before edits.
Read full 05.03 Prime review, 0704/06.02.review and the scoped consumer profile.
This is one bounded build/test pass. No new authority or live adoption.

## #01 - notes, contract and exact successor ownership
Write 06.07.md notes and evidence/build05.04/CONTRACT.md before implementation.
Use versioned successors labs/prime-cycle-pass03, labs/review-loop-pass02 and
labs/review-construction-pass02. Name predecessor hashes and precise deltas.
Reuse pinned labs/prime-review-pass02 and reviewed 0521 tool/legacy readers.
Preserve all predecessors and shared seam-v1. No edits to 0521, any existing app
facade, old module or pin file. If a new app door helps, only NEW
app/review_loop_tools_v2.py and app/review-loop-v2.json are allowed; do not register
it in librarian.py. Prefer repairing integration over inventing a status engine.

## #02 - real custody verification, RL-01 and RL-02
Implement 0417/evidence/integration-consumer-pass02.md exactly for this slice.
Consume descriptors produced by the real pinned 0521 tool, not fixtures that merely
look similar. Derive review target from origin; target_page is return-page directory,
custody_path is custody directory. Verify the full actual custody chain using
pinned read-only validators; do not execute arbitrary tool paths from inputs.
Compare regenerated descriptor identity/hashes with caller input. Reject arbitrary
receipt schemas, wrong origin/pass/submission, changed payload/manifest, custody
placeholder files and unsupported formats. Presence and a matching caller-provided
hash are not custody proof. Show incomplete/unknown/conflict precisely; retain
request and partial work. A prepare exit 0 alone does not mean full_success.

## #03 - read-only legacy adapter for first real Prime use
Add describe-legacy --book ABS --member EXACT to the new review-loop lab (or a
small named adapter there). The named book may be read only, including the live
book; no queue/layout/capture/review/trace writes under that book. Print descriptor
/2, pinned validation result and material hashes to stdout. The caller may save
stdout elsewhere. Use pinned return_inspect.py and helper; no sequential reserve.
Origin comes from reservation; correct intended placement comes from the source
route. Placement remains pending. Never turn valid legacy custody into claimed
final filing. Unknown unsupported prefix/route must be explicit. /1 final captures
still work. Staged seals and relocation equivalence are not part of this pass.
Do not rewrite legacy bytes. Demonstrate on disposable historical-format fixtures;
Prime will choose an actual live return for read-only use after review.

## #04 - nonzero rendering and stable reviewed material
The constructor successor must pin the already reviewed prime-review-pass02 and
support declared N5NN/N1NN prefixes and N7NN local tails. Preserve stable
review-task-binding/2 behavior and independent file write tokens. Rendering must
not stale the judgment; changed material/known changed task does. Do not silently
rebind task A return to task B. Where historical custody lacks proof of task
association, report the limit explicitly rather than inventing freshness.
Keep commit-before-render, render-pending, idempotent recovery, full in-page review,
outside-section bytes, Director replies and original wording. An existing substantive
review remains a conflict; no successor renderer in this pass. Director chose
same-home succession with separately attributed Director/model blocks (0704/06.03),
but detailed implementation is deferred. Preserve typed judgment if render refuses.

## #05 - required executable tests
First create a real disposable book through 0521 init/reserve/capture. Feed its
UNCHANGED emitted descriptor into prepare -> supplied typed judgment -> record ->
render -> fresh-process read. Assert exact full review in N5NN/05.NN, current
binding after render and correct supplied next action/questions. Repeat with a
nonzero prefix and a real N7NN local capture. Test duplicate and interrupted render.
Test wrong page/pass/subject/submission, unrelated receipt with updated descriptor
hash, invalid receipt schema, manifest/reservation mismatch, changed/missing payload,
missing receipt, reserved/incomplete, custody-file substitute, arbitrary verifier
path and changed task/evidence/agreement. Negative tests must refuse or report the
specific non-complete state, never claim success by default. Retain diagnostics.
Build valid historical-format fixtures with the existing helper and read them with
the pinned legacy reader. Test legacy-in-place /2 pending review and real
legacy-relocated /1 (stage/adopt in a DISPOSABLE copy only) through consumption.
Verify historical /1 and /2 cycle records keep their meaning. Rerun relevant new
and predecessor tests without overwriting prior evidence. Do not rerun a __main__
writer aimed at old transcripts; use imported tests or disposable exported tree.
No AR-01 inventory/bridge or concurrent hard-link race tests; that hold remains.
No broad app suite, network, paid services, installs, other models or Git writes.

## #06 - finish and inspectability
Provide a runnable PRIME-USE with exact commands, full dependencies/pins and a
realistic first-use request/decision example. One short reproduction command must
run the integrated real-capture loop on disposable records and write evidence to
an explicit NEW destination. Keep operation/request/check/version, verified facts,
supplied judgment, refusal/partial state and correction route inspectable. State
what is verified custody versus unproved task association. Compute supplies no
semantic judgment. No general telemetry/reporting platform or staging writer.
If a required dependency/contract blocks progress, save a checkpoint with the exact
issue and smallest proposal; stop the affected work rather than inventing a route.

## Return and scope
Allowed writes only the three NEW lab directories in #01; the two optional NEW app
files there; 0522/06.07.md; evidence/build05.04; this pack's claim/return pointer.
Use evidence/build05.04 for submission.md (Did, Blocked, Need), CONTRACT.md,
PRIME-USE.md, integration-patch.md, verification.json, artifact-manifest.json and
raw commands/exits/tests/demo/negative cases. Keep all failures and limitations.
Report Python/platform, hashes, skips and exact predecessor delta. Reread fully,
integrate notes, append submission/manifest hashes to pointer. Manifest self row
must be explicitly excluded or null; do not claim an impossible self hash.
No live book mutation except these assignment records, no capture migration or
allocation, no 0184, no seating or approval. Correct matching 0122 custody remains
pending migration; page-local evidence preserves the handback without fabricating
completion. Full Prime review will land here on 05.04. Stop after this pass.

## Return pointer
Release: the Director, this session, 2026-11-01: "Work in D:\Git\lib-build on workshop. Run: 00.kernel/00.00.10.work/0522.review-construction/05.04.md"
Claim: Grok-2, this session, 2026-11-01. pack05.04: 69 of 69 live bytes, snapshots, and declared hashes matched at this pointer. Bad count 0. HEAD at the note and at this pointer: 960d20c5290656095df8457b1740d2d5e586b111. This builder did not commit. Scope: this page only.
Submission: 00.kernel/00.00.10.work/0522.review-construction/evidence/build05.04/submission.md sha256 1cf6a36f07d1e2e1219d23a535608c385077deea22ad29133e3d74fd124e0a48
Artifact manifest: 00.kernel/00.00.10.work/0522.review-construction/evidence/build05.04/artifact-manifest.json sha256 9f87d70d90e75d890d2106c6f36bb5a0e06d2ed8204b72537cdd814da7e040f1
Custody: PENDING. Matching line 0122.review-construction awaits reviewed placement migration. This pass did not use the old allocator and did not allocate 0184.

## Review - Codex Prime

# Prime review - 0522.review-construction
date: 2026-11-01
who: Codex Prime

Disposition: bounded real-custody review-loop repair verified; app entry pending.

All 69 input snapshots/current bytes, 48 artifact rows and pointer hashes match.
Prime imported the test module, set only its PY harness variable to available
Windows Python 3.12.14, and ran the suite without its __main__ evidence writer.
13 tests passed in 142.726s. Raw logs preserve the actual run and commands. This
includes unchanged real producer descriptors, prepare/record/render/new-process
read, nonzero N5NN, N7NN local tails, stale material and negative custody inputs,
legacy-in-place, legacy-relocated, duplicate/partial rendering and historical
record behavior. The original 32 cycle tests were builder-reported; not separately
rerun here. Sealed predecessor evidence remains covered by the suite's hash check.

The important previous integration defects are addressed: real custody is checked
through pinned validators, correct return-page/custody directory meanings are
consumed, and the constructor successor handles nonzero destinations. Task
association remains honestly not-established where capture metadata lacks it.
Full_success represents the mechanical cycle, not task acceptance or filing.

Prime additionally ran describe-legacy read-only on actual member
0182.desk-app-integration-design-0501. It returned state complete, descriptor /2,
legacy-in-place, origin 0519/05.01 and intended 0119.desk-app; placement pending,
acceptance false and task association not-established. Fingerprints of the member's
files before/after matched. No live review was recorded or rendered. This is an
actual read-only use, not a fresh-Prime or end-to-end live workflow completion.

Known gaps remain explicit: existing app door isn't wired to this successor;
reproduce fixes a synthetic identity; source task association may be unknown;
existing substantive review still conflicts; staged seals, relocation equivalence
and successor rendering are deferred. The runtime contract omits the reproduce
decision schema later documented in PRIME-USE: record this contract/doc delta in
the next interface pack, without pretending it was fixed before the original tests.

No further core rewrite is justified by these checks. Proposed next pass adds one
pinned controlled app entry and targeted adapter tests, with a user-supplied request
and judgment. Draft 05.05 is held for Director review. No live mutation/migration,
seating, automatic judgment, role change or matching 0122 custody claimed.
```
### Finish criteria
```
# 05 - Real custody into the Prime review loop
version: 001
date: 2026-11-01
who: Codex Prime
state: prepared for named Director invocation
book: 00.00.10.work
PPPP: 0522
Face: 05

## Assignment
Executor Grok-2. Reviewer Codex Prime. Work D:/Git/lib-build on workshop.
Director requested this repair after Prime reviewed both returned lanes. Record
invocation/claim and verify evidence/pack05.04/source-manifest.json before edits.
Read full 05.03 Prime review, 0704/06.02.review and the scoped consumer profile.
This is one bounded build/test pass. No new authority or live adoption.

## #01 - notes, contract and exact successor ownership
Write 06.07.md notes and evidence/build05.04/CONTRACT.md before implementation.
Use versioned successors labs/prime-cycle-pass03, labs/review-loop-pass02 and
labs/review-construction-pass02. Name predecessor hashes and precise deltas.
Reuse pinned labs/prime-review-pass02 and reviewed 0521 tool/legacy readers.
Preserve all predecessors and shared seam-v1. No edits to 0521, any existing app
facade, old module or pin file. If a new app door helps, only NEW
app/review_loop_tools_v2.py and app/review-loop-v2.json are allowed; do not register
it in librarian.py. Prefer repairing integration over inventing a status engine.

## #02 - real custody verification, RL-01 and RL-02
Implement 0417/evidence/integration-consumer-pass02.md exactly for this slice.
Consume descriptors produced by the real pinned 0521 tool, not fixtures that merely
look similar. Derive review target from origin; target_page is return-page directory,
custody_path is custody directory. Verify the full actual custody chain using
pinned read-only validators; do not execute arbitrary tool paths from inputs.
Compare regenerated descriptor identity/hashes with caller input. Reject arbitrary
receipt schemas, wrong origin/pass/submission, changed payload/manifest, custody
placeholder files and unsupported formats. Presence and a matching caller-provided
hash are not custody proof. Show incomplete/unknown/conflict precisely; retain
request and partial work. A prepare exit 0 alone does not mean full_success.

## #03 - read-only legacy adapter for first real Prime use
Add describe-legacy --book ABS --member EXACT to the new review-loop lab (or a
small named adapter there). The named book may be read only, including the live
book; no queue/layout/capture/review/trace writes under that book. Print descriptor
/2, pinned validation result and material hashes to stdout. The caller may save
stdout elsewhere. Use pinned return_inspect.py and helper; no sequential reserve.
Origin comes from reservation; correct intended placement comes from the source
route. Placement remains pending. Never turn valid legacy custody into claimed
final filing. Unknown unsupported prefix/route must be explicit. /1 final captures
still work. Staged seals and relocation equivalence are not part of this pass.
Do not rewrite legacy bytes. Demonstrate on disposable historical-format fixtures;
Prime will choose an actual live return for read-only use after review.

## #04 - nonzero rendering and stable reviewed material
The constructor successor must pin the already reviewed prime-review-pass02 and
support declared N5NN/N1NN prefixes and N7NN local tails. Preserve stable
review-task-binding/2 behavior and independent file write tokens. Rendering must
not stale the judgment; changed material/known changed task does. Do not silently
rebind task A return to task B. Where historical custody lacks proof of task
association, report the limit explicitly rather than inventing freshness.
Keep commit-before-render, render-pending, idempotent recovery, full in-page review,
outside-section bytes, Director replies and original wording. An existing substantive
review remains a conflict; no successor renderer in this pass. Director chose
same-home succession with separately attributed Director/model blocks (0704/06.03),
but detailed implementation is deferred. Preserve typed judgment if render refuses.

## #05 - required executable tests
First create a real disposable book through 0521 init/reserve/capture. Feed its
UNCHANGED emitted descriptor into prepare -> supplied typed judgment -> record ->
render -> fresh-process read. Assert exact full review in N5NN/05.NN, current
binding after render and correct supplied next action/questions. Repeat with a
nonzero prefix and a real N7NN local capture. Test duplicate and interrupted render.
Test wrong page/pass/subject/submission, unrelated receipt with updated descriptor
hash, invalid receipt schema, manifest/reservation mismatch, changed/missing payload,
missing receipt, reserved/incomplete, custody-file substitute, arbitrary verifier
path and changed task/evidence/agreement. Negative tests must refuse or report the
specific non-complete state, never claim success by default. Retain diagnostics.
Build valid historical-format fixtures with the existing helper and read them with
the pinned legacy reader. Test legacy-in-place /2 pending review and real
legacy-relocated /1 (stage/adopt in a DISPOSABLE copy only) through consumption.
Verify historical /1 and /2 cycle records keep their meaning. Rerun relevant new
and predecessor tests without overwriting prior evidence. Do not rerun a __main__
writer aimed at old transcripts; use imported tests or disposable exported tree.
No AR-01 inventory/bridge or concurrent hard-link race tests; that hold remains.
No broad app suite, network, paid services, installs, other models or Git writes.

## #06 - finish and inspectability
Provide a runnable PRIME-USE with exact commands, full dependencies/pins and a
realistic first-use request/decision example. One short reproduction command must
run the integrated real-capture loop on disposable records and write evidence to
an explicit NEW destination. Keep operation/request/check/version, verified facts,
supplied judgment, refusal/partial state and correction route inspectable. State
what is verified custody versus unproved task association. Compute supplies no
semantic judgment. No general telemetry/reporting platform or staging writer.
If a required dependency/contract blocks progress, save a checkpoint with the exact
issue and smallest proposal; stop the affected work rather than inventing a route.

## Return and scope
Allowed writes only the three NEW lab directories in #01; the two optional NEW app
files there; 0522/06.07.md; evidence/build05.04; this pack's claim/return pointer.
Use evidence/build05.04 for submission.md (Did, Blocked, Need), CONTRACT.md,
PRIME-USE.md, integration-patch.md, verification.json, artifact-manifest.json and
raw commands/exits/tests/demo/negative cases. Keep all failures and limitations.
Report Python/platform, hashes, skips and exact predecessor delta. Reread fully,
integrate notes, append submission/manifest hashes to pointer. Manifest self row
must be explicitly excluded or null; do not claim an impossible self hash.
No live book mutation except these assignment records, no capture migration or
allocation, no 0184, no seating or approval. Correct matching 0122 custody remains
pending migration; page-local evidence preserves the handback without fabricating
completion. Full Prime review will land here on 05.04. Stop after this pass.

## Return pointer
Release: the Director, this session, 2026-11-01: "Work in D:\Git\lib-build on workshop. Run: 00.kernel/00.00.10.work/0522.review-construction/05.04.md"
Claim: Grok-2, this session, 2026-11-01. pack05.04: 69 of 69 live bytes, snapshots, and declared hashes matched at this pointer. Bad count 0. HEAD at the note and at this pointer: 960d20c5290656095df8457b1740d2d5e586b111. This builder did not commit. Scope: this page only.
Submission: 00.kernel/00.00.10.work/0522.review-construction/evidence/build05.04/submission.md sha256 1cf6a36f07d1e2e1219d23a535608c385077deea22ad29133e3d74fd124e0a48
Artifact manifest: 00.kernel/00.00.10.work/0522.review-construction/evidence/build05.04/artifact-manifest.json sha256 9f87d70d90e75d890d2106c6f36bb5a0e06d2ed8204b72537cdd814da7e040f1
Custody: PENDING. Matching line 0122.review-construction awaits reviewed placement migration. This pass did not use the old allocator and did not allocate 0184.

## Review - Codex Prime

# Prime review - 0522.review-construction
date: 2026-11-01
who: Codex Prime

Disposition: bounded real-custody review-loop repair verified; app entry pending.

All 69 input snapshots/current bytes, 48 artifact rows and pointer hashes match.
Prime imported the test module, set only its PY harness variable to available
Windows Python 3.12.14, and ran the suite without its __main__ evidence writer.
13 tests passed in 142.726s. Raw logs preserve the actual run and commands. This
includes unchanged real producer descriptors, prepare/record/render/new-process
read, nonzero N5NN, N7NN local tails, stale material and negative custody inputs,
legacy-in-place, legacy-relocated, duplicate/partial rendering and historical
record behavior. The original 32 cycle tests were builder-reported; not separately
rerun here. Sealed predecessor evidence remains covered by the suite's hash check.

The important previous integration defects are addressed: real custody is checked
through pinned validators, correct return-page/custody directory meanings are
consumed, and the constructor successor handles nonzero destinations. Task
association remains honestly not-established where capture metadata lacks it.
Full_success represents the mechanical cycle, not task acceptance or filing.

Prime additionally ran describe-legacy read-only on actual member
0182.desk-app-integration-design-0501. It returned state complete, descriptor /2,
legacy-in-place, origin 0519/05.01 and intended 0119.desk-app; placement pending,
acceptance false and task association not-established. Fingerprints of the member's
files before/after matched. No live review was recorded or rendered. This is an
actual read-only use, not a fresh-Prime or end-to-end live workflow completion.

Known gaps remain explicit: existing app door isn't wired to this successor;
reproduce fixes a synthetic identity; source task association may be unknown;
existing substantive review still conflicts; staged seals, relocation equivalence
and successor rendering are deferred. The runtime contract omits the reproduce
decision schema later documented in PRIME-USE: record this contract/doc delta in
the next interface pack, without pretending it was fixed before the original tests.

No further core rewrite is justified by these checks. Proposed next pass adds one
pinned controlled app entry and targeted adapter tests, with a user-supplied request
and judgment. Draft 05.05 is held for Director review. No live mutation/migration,
seating, automatic judgment, role change or matching 0122 custody claimed.
```
### Director wording
Declared director spans only. A file role is not an author.
director dir bytes 111:403 sha256 2e5fe132ea0b4e943daa078dd1c1cf20c63bd4d7a882b64079e738512d39e342 ambiguous False
```
> I like it.  I can't think of anything to change so lets go with it.  Add to our deliverables so we are moving this forward I think we can start to get the core working for you today.
>
> Then if you are good pack it for work to be done.
>
> We have claude and grok-1 sitting at the moment.
```
### Model explanation
This section is separate from Director wording.
model mod bytes 430:834 sha256 2e5fe132ea0b4e943daa078dd1c1cf20c63bd4d7a882b64079e738512d39e342 ambiguous False
```
The proposed Prime desk overview and selected-task working packet are approved
as deliverables. Prepare Grok-1 implementation and Claude independent Colab. This
is not permission to migrate live returns, seat kernel, activate workers, replace
an authority record, or claim today's finish before measured use. Director/model
wording stays separate. Scope below is the first read-only text implementation.
```
### Returns and deliverables
- ret-0522: 0522 return (`0522.review-construction/05.04.md` matched efe9ae39305f 10802 basis observed).
### Receipts
None bound to this work.
### Verification
a matching hash proves these bytes, not acceptance or process freshness
- ver: verification (`verified.md` matched 8f5a1374b3eb 9 basis observed).
### Findings
None bound to this work.
### Dependencies
- policy: reporting policy (`0412.prime-review/06.02.md` matched 28e9afeb6263 2044 basis observed).
### Review home
`0122.review-construction/05.04` `0122.review-construction/05.04.md` basis unknown. Pending custody. The derived review file is not a matched declared source. No receipt is fabricated.
### Next routes
None bound to this work.
### Desk policy
Desk-wide references are policy links. They are not another task's criteria or review destination.
- goal: goal page (`0401.goal/01.md` matched 20f23f4cfed6 5914 basis observed).
- scope: seats page (`0408.seats/01.md` matched dbf2399d5285 2031 basis observed).
- authority: desk-app direction (`0416.desk-app/01.003.md` matched d432c796404f 4617 basis observed).
- policy: reporting policy (`0412.prime-review/06.02.md` matched 28e9afeb6263 2044 basis observed).
- talk: quoted command (`talk.md` matched 0185bd225351 26 basis observed).
