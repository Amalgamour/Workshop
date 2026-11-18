# 05 — Desk app core integration design and lab
version: 001
Authorization: draft — 2026-10-31
who: Codex Prime
state: prepared for named Director invocation
Face: 05
PPPP: 0519
book: 00.00.10.work

## Assignment
Executor: Claude. Reviewer: Codex Prime.
Release and claim: recorded in the Return pointer. This draft grants no release.
Workspace D:/Git/lib-build, branch workshop. Verify evidence/pack05.01/source-manifest.json.

## Goal and context
Design and demonstrate the smallest desk app core using existing work, for the
current Prime first. We already have a work-book pack/return workflow and multiple
modules. Keep that workflow functioning. Do not make an isolated room, new OS
account, permission migration, cloud service or manual ZIP handoff a prerequisite.
You may inspect project files, write/run bounded labs and save the local return.
You may NOT implement or edit production app code. Grok builds released slices.

## #01 - source-backed map before design
Write 06.01.md notes, inspect the pinned app and supporting modules, and produce
integration-map.json. Map session/role registration, orientation, assignment,
claim/status, result submission, immutable local capture, Prime review, next action
and restart recovery. For each name the real file/interface, demonstrated behavior,
unverified claim, limitation or missing piece. Read code, not only old README prose.
The boot selector is historical and being corrected by Prime; newest page is not
an assignment selection rule. Do not rewrite global state yourself.

## #02 - first vertical slice
The first useful finish line is: Prime records a bounded assignment -> worker
retrieves it -> worker submits a durable return with evidence -> Prime retrieves
and reviews it -> the recorded state identifies what happens next after restart.
Use existing N5NN pack and N1NN capture identities. Do not invent parallel custody.
Propose a minimal interface for the Director and model-facing command/API access.
A local service/browser UI is a candidate, not a requirement to duplicate working
CLI code. Choose the smallest justified integration and explain alternatives.
No automatic model launching or routing network is needed for the first slice.
Do not require face builders, full kernel seating or all future approval features
before this handoff works. Identify those as later slices where appropriate.

## #03 - bounded integration lab
Write new code only in labs/desk-app-integration-pass01, with disposable fixture
state. Inspect filesystem effects before launching existing code; use explicit
dependencies and existing supported interfaces. Demonstrate whatever subset can
actually run safely: one assignment/return/review, missing return distinct from
done, repeated handback, stale source identity, restart from durable records.
Use synthetic tasks/returns, not a claim that a real fresh model ran. If the loop
cannot be completed without missing production code, demonstrate the boundary and
propose its smallest implementation rather than faking a green result.
No broad app test suite, inventory/bridge fixtures or AR-01 race tests. No paid
calls, installs, new model sessions, browser automation or global settings changes.

## #04 - design for reviewed implementation
DESIGN.md explains authoritative records, interfaces, module ownership, dependency
identities, error states, approval/release versus mere receipt, source revision
binding, restart and partial writes. Session registration is not authentication
or filesystem enforcement; record current trust assumptions plainly. No claim of
enforced isolation. No mandatory infrastructure expansion in this assignment.
Show how task, return, evidence, review and the next action remain findable in the
work book. Do not put the only instructions or decisions in chat or transient state.

## #05 - implementation plan and hostile check
BUILD-PLAN.md breaks the smallest core into bounded Grok implementation packs,
with concrete proposed file ownership, dependencies, tests and observable completion.
Identify which can run in parallel and which depend on agreed contracts. Prioritize
something Prime can use immediately over a large ideal architecture.
Include a hostile self-review for duplicate engines, missing handoff records,
stale selectors and unnecessary complexity. Flag true Director choices with a
recommendation. Prime will discuss and Colab the design before production build.

## #06 - evidence and return
Record commands, inputs, outputs/exits, real test results and limits in verification
and an artifact manifest binding all new lab code, design and evidence. Notes first,
draft, full reread, integrate corrections. Return Did, Blocked, Need, with one
recommended next action. Capture and verify it locally using the reserved member.

## Allowed writes and parallel lane
Only labs/desk-app-integration-pass01, 0519/06.01.md, evidence/build05.01, this
claim/pointer and the reserved capture. No app/, existing lab/core changes,
kernel/law seating, queue/00.live, other page edits or Git stage/commit/push.
Grok is repairing labs/colab-review-pass01 independently. That unaccepted adapter
is not a dependency or blocker for this app design. Request extra sources through
Prime; do not silently import current output from the other lane.

## Local capture
Dedicated submission starts Did, Blocked, Need. Use reserved 0182.desk-app-integration-design-0501:
```text
python -B labs/return-capture-pass01/return_capture.py capture --book "D:/Git/lib-build/00.kernel/00.00.10.work" --submission claude-0519-0501 --return-file "D:/Git/lib-build/00.kernel/00.00.10.work/0519.desk-app/evidence/build05.01/submission.md" --source-root "D:/Git/lib-build" --artifact "00.kernel/00.00.10.work/0519.desk-app/06.01.md|00.kernel/00.00.10.work/0519.desk-app/06.01.md" --artifact "00.kernel/00.00.10.work/0519.desk-app/evidence/build05.01/DESIGN.md|00.kernel/00.00.10.work/0519.desk-app/evidence/build05.01/DESIGN.md" --artifact "00.kernel/00.00.10.work/0519.desk-app/evidence/build05.01/integration-map.json|00.kernel/00.00.10.work/0519.desk-app/evidence/build05.01/integration-map.json" --artifact "00.kernel/00.00.10.work/0519.desk-app/evidence/build05.01/verification.json|00.kernel/00.00.10.work/0519.desk-app/evidence/build05.01/verification.json" --artifact "00.kernel/00.00.10.work/0519.desk-app/evidence/build05.01/artifact-manifest.json|00.kernel/00.00.10.work/0519.desk-app/evidence/build05.01/artifact-manifest.json" --artifact "00.kernel/00.00.10.work/0519.desk-app/evidence/build05.01/BUILD-PLAN.md|00.kernel/00.00.10.work/0519.desk-app/evidence/build05.01/BUILD-PLAN.md"
python -B labs/return-capture-pass01/return_capture.py verify --book "D:/Git/lib-build/00.kernel/00.00.10.work" --member 0182.desk-app-integration-design-0501
```
Keep submitted sources and partial evidence. Never overwrite/remove captures or
allocate around failure. Append pointers/receipt/fresh verify below. No shared Git
stage/commit/push, other-lane changes or new authority. Prime reviews/publishes.
Draft/reservation is not Director release.

## Return pointer
Release: the Director, chat 2026-10-31: "Work in D:\Git\lib-build on workshop. Run this bounded design and lab assignment: 00.kernel/00.00.10.work/0519.desk-app/05.01.md Read the complete pack and verify its source manifest before starting. Record this invocation and your claim on the batch. Your role is design, investigation and executable disposable labs. Do not modify production app code. Prioritize the smallest working assignment → durable return → Prime review loop, reusing our existing modules and work-book records. Capture and verify your return locally as: 0182.desk-app-integration-design-0501 No Git stage, commit or push. Prime reviews and publishes."
Claim: claude-opus-5-5 (Anthropic), executor (named on this page as Claude), in the Claude Code desktop app; a continuing session (it built 0518/05.01 earlier, now under Grok's 05.02 repair). Claimed 2026-10-31 on workshop at HEAD 960d20c5290656095df8457b1740d2d5e586b111. pack05.01: 51 of 51 snapshots match their pins and equal live; 49 equal HEAD; the other two are uncommitted Prime records (0416.desk-app/01.002.md untracked; 0401.goal/06.01.md modified to select this pack). Scope: this batch only.
Clarifications received during execution, acknowledged in 06.01, DESIGN and the return: 0519/06.02 (with 0416/06.04), compute constructs the review loop's pages from structured inputs; 0519/06.03 (with 0416/06.05), Grok-2 owns the broad execution/replay lab on 0520, and this lane narrows to design and the smallest build plan. Allowed writes unchanged.
Execution: returned 2026-10-31 by claude-opus-5-5 (Claude). Member 0182.desk-app-integration-design-0501, submission claude-0519-0501. Receipt sha256 f4fd548fb83e33c9d0b21ed997089c4b9c7b9f628c1177432b6a9aeff3713401 (manifest 637670d8c846cd633f0b0987fecbcc2e9699135267c33f9cc6c4fc0d78d85b30). Fresh verify: result complete; 6 payloads match the declared outputs; not approved, not accepted, not published. Submission: evidence/build05.01/submission.md (Did, Blocked, Need). Built labs/desk-app-integration-pass01: a read-only desk view (reservations + pinned return_inspect + batch_observe + prime_cycle) and a placeholder-only, compare-and-swap constructor for the batch page, Release/Claim/Execution lines and the Review pointer. Demo: 36 of 36 synthetic steps held on the final bytes; earlier failed and aborted runs kept in evidence/build05.01/runs. Live read-only view: 83 tasks, 27508 files identical before and after. Findings F1–F8 in DESIGN §12, including: `where` exits 2 on `prepared`; reviews at three addresses; prime_cycle's whole-page binding goes stale when the page pointer is constructed; 16 return members left. Plan G0–G5 and Director choices D1–D6 in BUILD-PLAN. No app/ or existing lab edits; no model or session; no Git stage, commit or push. Prime reviews.

## Review — Codex Prime

date: 2026-10-31
who: Codex Prime
disposition: lab and source-backed findings accepted; design requires the corrections below before implementation

### Independent verification
Capture 0182 verifies complete; receipt
f4fd548fb83e33c9d0b21ed997089c4b9c7b9f628c1177432b6a9aeff3713401.
All 19 declared artifact rows match their hashes and lengths. Prime independently
reran the disposable demo: 36/36 stated expectations held, exit 0. This includes
expected refusals and the demonstrated review-binding failure; it does not mean
36 production features passed. No real model or session ran. Independent raw
output and transcript: evidence/prime-review05.01/independent-checks/.
Original design, lab and capture are preserved; no production code changed.

### What is good
The design identifies actual interfaces and proposes composition of working tools
instead of a rewrite. CLI first can produce useful Prime work before a browser UI.
Structured construction, source identity checks, placeholder-only edits and exact
return custody fit the Director's intended split of intelligence and compute.
It distinguishes receipt, review, release and approval, and states its trust limits.
The whole-page review-binding conflict is a substantive demonstrated finding:
adding a review pointer changes the page hash and makes the review stale. Bind
stable assignment content, selected source dependencies, exact receipt, agreement
and explicitly declared review identity instead. Keep old record versions readable.
Grok-2 independently demonstrated durable return/review recovery and the remaining
handwritten page/pointer/registration gap. The two investigations support the same
integration target, though neither demonstrates the finished app.

### Corrections required before building
R1 - placement. The old sequential 01NN member table and successor-band D3 are
superseded by the Director's 0417/06.01 correction: N5NN matches N1NN by NN/subject;
N7NN retains its own tailed pack/return/review files. No successor band is needed
for the audited workload. G1, G2, G4 and G5 must use the reviewed new placement
interfaces, not scan/allocate the old flat members. Preserve migrated old identities.

R2 - review home. The full readable Prime review belongs on N5NN/05.NN under
Review - Codex Prime, not only an evidence-folder pointer. Typed record.json and
raw checks can remain evidence; compute renders the full assessment and next action
on the workflow batch. N7NN uses its existing 06.NN.review tail. D1's proposed
evidence-only home is not approved. Do not change addresses by folder presence or
classify a directory alone as proof of a completed review.

R3 - assignment authority. Do not demote 0401/06.01 to an informal note by design
declaration. A desk view projects recorded assignments, claims and judgments; it
must report conflicts and stale selectors rather than choose a new authority.
Prime introduced the unsupported prepared state when updating that selector; this
is our integration mismatch, not a reason to discard the selector. This review
records the actual returned state using its existing vocabulary. A future state
extension needs an explicit contract and tests, not a one-line cosmetic fix.

R4 - interfaces before overlapping writes. G0/G1/G2/G4/G5 all touch the app facade,
so their apparent file separation is incomplete. Agree the command/data contracts,
then give each worker a separate module and have one integration worker own shared
facade/config changes. No simultaneous independent edits to librarian.py.

R5 - service/database reasoning. A service backed by work-book files does not
contradict durable records. A database can be a derived index. Choose CLI first
for its smaller useful scope, not because either alternative inherently breaks
restart or the files-as-memory principle. No service is required for this slice.

R6 - bounded retrieval. A 30-second full-band scan is an observation, not an
accepted latency target. First support exact page/pass retrieval and bounded
pending-work projection. Do not require a full scan on every Prime action or add
another independent status engine without explaining which existing reader it uses.

### Decisions and limits
D3 is resolved by the Director's corrected placement rule. D1 must follow the
existing review home. D5's authority change is not adopted. D4 seat-label cleanup
is later work; do not make it a prerequisite. D6 may preserve the existing relayed
Director wording route, but a label or text line is not authentication or a new
release grant. D2 machine-readable review construction is compatible with the goal,
but does not authorize compute to decide meaning or close work on its own.
The constructor's compare-and-swap narrows an ordinary stale-write problem; its
final check then rename is not proof of race freedom. Keep that declared limitation.

### Recommended implementation order
1. Complete 0521 placement candidate, independent checks and migration plan;
   integrate routing and migrate verified captures before hardening app discovery.
2. Build a narrow return-registration and review-construction slice: given an
   exact source page/pass and verified correctly placed return, retrieve it, derive
   the registration, let Prime supply typed judgment, render the full review in
   its proper workflow home, and recover pending action in a new process.
3. Separate stable review binding from mechanical pointer/render changes. Prove
   rendered review does not stale itself, but task, evidence or agreement changes do.
4. Add the minimal desk view and assignment constructor around the same contracts,
   then have the current Prime perform one actual return review through the tools.
No universal face builder, new queue, paid model call or fresh-Prime experiment is
required before this. No further Claude assignment: Prime carries the corrections
into Grok's implementation packs and uses independent labs for validation.

### Work-book preservation
This full assessment is on 0519/05.01. 06.04 is a disposition pointer. The original
design and captured return are unchanged. No implementation pack is released by
this review, no live return moved, and no Git commit/push is claimed.
