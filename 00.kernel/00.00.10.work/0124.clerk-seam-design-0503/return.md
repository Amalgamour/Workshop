# 05 — Design the Clerk-to-worker seam
version: 001
Authorization: draft — 2026-10-27
who: Codex Prime
state: draft; awaiting Director release
Face: 05
PPPP: 0506
book: 00.00.10.work
keyword: clerk-handoff

## Assignment
Executor: Claude, technical lead/Colab. Reviewer: Codex Prime.
Release: PENDING. Claim: PENDING.
Design the smallest manually invoked connection between the file-backed Clerk
and fixture-only app worker exchange. No code changes, execution or dispatch.
Inputs are exact Git objects at 54274e698dde1c6cbd5e25177395c62c2a2c645a, bundled under
evidence/pack05.03/inputs; source-manifest.tsv pins all 15 files.

## Independence
Grok 1 owns app receipt correction 0504/05.06. Grok 2 owns Clerk correction
0506/05.02. Both are pending acceptance; do not assume their future implementation.
Use the frozen inputs, not their changing files. State the precise dependency
on those fixes. This design can proceed now; integrated execution must wait.
SoF is a separate project and outside this task. No new numeric page allocation.

## #01 — Trace and ownership
Use NEW 06.06.md notes first; leave 06.04 for correction review and 06.05 for the
Builder's repair notes. Trace what each existing component actually records.
Propose one small glue boundary and command in the app; do not build another
Clerk, worker adapter, loader, global registry, source of approval or shared ledger.
Map Clerk job ID, claimant/token, instruction identity, app work_ref, worker role,
delivery ID, request hash, artifact and named reviewer explicitly. A caller label
or token is correlation, not identity authentication or execution authorization.
Any required schema change is a named proposal with a reason, never assumed real.

## #02 — One concrete end-to-end exchange
Design a router fixture job with a named assignee/reviewer and expected output
result.json (compatible with fixture-ok), then: queue -> explicit claim -> one
worker delivery -> verify artifact -> exclusive copy into Clerk outbox -> Clerk
return -> reviewer inbox. Show actual example JSON, proposed command arguments,
locations and a sequence table with who writes each file and what permits it.
The worker must keep its fresh per-delivery output directory; do not point it at
the existing Clerk outbox. Copy only verified declared artifacts, preserving their
hash/source relationship. State the owning record for each fact and the distinct
copies, so there is no independently editable duplicate job/state authority.
Intelligence supplies assignee/reviewer and route; compute neither chooses nor
approves them. Do not automatically invoke the reviewer. No real model or scheduler.

## #03 — Interruption and replay across two stores
Work through these boundaries concretely: claim recorded before launch; launch
recorded with uncertain result; complete receipt before artifact copy; copy before
Clerk return; Clerk return complete before the caller sees success. Explain what
a repeated invocation reads and whether it may write at each point. Reuse original
delivery/request identity; never silently relaunch an uncertain attempt or replace
a claim token. A minimal association/intent record may own the cross-component
relationship, but it must not become a duplicate ledger or grant authority.
Do not claim a cross-store transaction/exactly-once guarantee that does not exist.
Changing artifact bytes, missing completion marker, bad receipt correlation, wrong
claim, stale instruction hash and a conflicting delivery need explicit outcomes.
If a case needs a human decision, preserve evidence and name that boundary rather
than inventing automatic recovery. Carry 0504/05.06 and 0506/05.02 requirements.

## #04 — Bounded implementation recommendation
Write evidence/design05.03/SEAM.md plus the minimal example files required to
understand it. Recommend ONE next implementation slice, with exact proposed files,
dependency versions/contracts, a runnable fixture demonstration and meaningful
acceptance tests for the success path and interruptions above. Distinguish built
interfaces, proposed interfaces and current blockers in a short table. Address the
fact that app fixtures and Clerk stores currently have different placement rules;
do not quietly bypass either component's boundary or add an override flag.
Routine choices should carry your recommendation, not become a long Director
questionnaire. Report only decisions with material scope/authority effects.

## #05 — Reread and return
Reread the complete proposal against the snapshots; account for notes, hash the
outputs and return on this page with Did, Blocked, Need, then recommendation,
verified readings versus unexecuted design claims, decisions and next slice.
May edit only this 05.03 and create 06.06 plus evidence/design05.03/ under this page.
No other page, code, app/lab/store, shared assignment/view/queue or Git writes.
No worker execution, network/model calls, dependencies, real jobs, approval,
activation or automatic messages. Do not implement either Builder's correction.

## Return — Claude
Release: the Director, chat 2026-10-27: "Read and execute: D:\Git\lib-build\00.kernel\00.00.10.work\0506.clerk-handoff\05.03.md I release this batch for design work only. Design the smallest explicit connection: Clerk claim -> one worker delivery -> verified artifact -> Clerk return -> named reviewer inbox. Work through interruption and replay between those steps. Recommend one bounded implementation slice. Use the pinned snapshots. Do not implement or alter either builder's corrections, shared records, Git state or SoF. Return on that page for Codex Prime review."
Claim: claude-opus-5-5 (Anthropic), Colab, technical lead, claimed 2026-10-27T11:48-05:00. Scope: this batch only; not the global current assignment.
Execution: RETURNED for Codex Prime review, 2026-10-27. Design only: no code, no worker, Clerk store or fixture created, no model call, no dispatch, no Git write. Neither Builder's correction was touched. SoF was not touched.

Did:
- Verified pack05.03: 15 of 15 match their pins, the blobs at 54274e698dde1c6cbd5e25177395c62c2a2c645a (now HEAD of workshop) and the live bytes.
- Wrote the notes first: 06.06.md (sha256 be428b40…), with I01-I02, trace T01-T05, mapping M01-M09, decisions D01-D06, dependencies P01-P02, Q01 and reread R01-R04.
- Wrote evidence/design05.03/SEAM.md (sha256 ef0c7507…, 18616 bytes) and five example files. Manifest evidence/design05.03/SHA256SUMS.txt, LF, sha256 b3f9dcf780081d4e016ea69ef9de4cb903de0a9ceeb041668452bb65f19da0b7. It does not list itself.
Blocked: nothing for the design. Integrated execution waits on both pending corrections (below).
Need: Prime's review. One decision with scope effect, Q01, below.

Recommendation, in short:
- One app command, `librarian.py clerk-deliver`, in a new app/clerk_seam.py.
  - It requires an existing, explicit Clerk claim and reads it with `claim --resume`, which writes nothing.
  - It runs exactly one bridge delivery through the existing worker_bridge.perform.
  - It checks the stored receipt (collected, done, ids and request correlated) and the source artifact bytes against it.
  - It copies only the verified declared artifacts into the Clerk outbox, by exclusive create.
  - It then calls `clerk.py return` with deterministic evidence (delivery, request, receipt and artifact hashes, source path).
- The named reviewer sees the job through Clerk's inbox projection. Nothing invokes the reviewer.
- Clerk is reached only through its public CLI, as a subprocess of a hash-pinned clerk.py (proposed app/clerk-seam.json). There is no second Clerk, loader, ledger or registry.
- The worker keeps its fresh per-delivery output directory. It must not write into the Clerk outbox: fixture-ok also writes launches.log there, and Clerk refuses extra outbox files.

Placement: the app allows only designated containers, and Clerk refuses any store inside Git, so app/scratch cannot hold a Clerk store. The design puts one external `--container` around both the fixture root and the Clerk store, as siblings. The seam's single write outside the fixture root then stays inside the app's designated container, and the Clerk store stays outside Git. No override flag. app/scratch is refused through Clerk's own rule.

Correlation:
- by equality: bridge job_id = Clerk job_id; Clerk return delivery = bridge delivery_id; the Clerk instruction sha = bridge inputs[0] sha = the declared input bytes.
- by one router-written, immutable link file, proposed `librarian-clerk-link` v1: delivery, Clerk store, Clerk job, and the bridge job path and hash.
- The link holds no assignee, reviewer, state, token or authority. --as and the token stay correlation labels.
- SEAM §6 gives one owner per fact.

Interruption and replay (SEAM §7). Each boundary has what a repeat reads, what it may write, and the outcome:
- a claim before launch proceeds to the one launch;
- an uncertain launch gives exit 4 with no relaunch, and a human chooses bridge-recover or a new delivery and link;
- receipt complete before the copy, and copy complete before the Clerk return, both complete without a launch;
- a Clerk return already complete gives `already-recorded`, with no event and no new time.
The table also covers: changed artifact bytes, a missing receipt or witness, the BRI-01 receipt shape, wrong claim, stale instructions before and after delivery, conflicting deliveries in both stores, and concurrent calls. There is no cross-store transaction and no exactly-once claim. Human boundaries are named, and every byte is kept.

Next slice (ONE, SEAM §9): "clerk-deliver, fixture only".
- Files: app/clerk_seam.py, app/clerk-seam.json, one dispatch in app/librarian.py, app/tests/test_clerk_seam.py, an app/README.md section.
- No edits to context.py, worker_bridge.py, clerk.py, the bridge lab, kernel pages or shared records.
- Demonstration: queue, claim, clerk-deliver, reviewer inbox, fresh verify, the same receipt hash, and a second clerk-deliver giving already-recorded with launches.log still one line.
- Acceptance tests A1 to A15: success, B1 to B5 by in-process crash points, mutations, placement and concurrency. Each asserts no relaunch, no traceback, no write outside the container, and unchanged Clerk events on refusal.

Dependencies, precise:
- 0504/05.06 accepted. The seam calls its single stored-receipt validator, by its accepted interface. Until then a BRI-01 receipt can read as collected.
- 0506/05.02 accepted. The seam pins that clerk.py. It needs the completion witness (no clean re-return after tail loss), OSError → exit 2, nonblank evidence and nonempty outputs. Whether `show` still prints the `claim` line that the returned-job replay path reads must be confirmed against the accepted clerk.py.

Verified readings (from the snapshots):
- every file, line and field cited in SEAM and 06.06, rechecked after writing (R01);
- the example instruction sha 6c913091…, 175 bytes;
- the expected artifact {"count":3} sha 0c07187e…, identical to the 0504/05.05 demo artifact;
- the example bridge job sha 4d57cdb9….
Unexecuted design claims: the whole command, its exit codes, the link schema, the evidence format, every interruption outcome and every test. None of it has run. One unpinned read: fixture-ok's behaviour, from labs/worker-bridge-pass01/fixtures/worker_fixture.py (sha 0d519c8b…, equal to its pin in the pinned worker-bridge.json).

Decision with material scope effect: Q01. Should an uncollected or `failed` delivery become a Clerk return the reviewer sees? Recommended no: stop with exit 3 and the evidence kept; a human decides. Everything else carries a routine recommendation.
Overflow: an optional Clerk `--json` output would replace line parsing. It is named, not required. One thing I would do differently: ask for worker_fixture.py in the pack, since the outbox-placement argument rests on its launches.log behaviour.

## Review — Codex Prime
Date: 2026-10-27. Reviewed return SHA-256: `936023d145ff6fd84423eee25779fa27a14cd7c586c74f04ca3cc8658088c562`.
Disposition: ACCEPTED AS DESIGN INPUT with two implementation requirements.
Read the complete SEAM.md and 06.06 notes. Verified 15 input blobs at 54274e6,
all 6 design-manifest files, example instruction/job/link hashes and IDs, and the
example's three nonblank lines. No seam command exists or was executed by this
review. The app correction is now Prime-accepted; Clerk correction independently
passes Prime's checks and still awaits its scheduled lead review.

1. A structured Clerk inspection result is REQUIRED, not optional. Current schema-2
show prints state/token, hashes and diagnostics but does not expose job routing,
expected_outputs or recorded return delivery. S4's returned-delivery comparison
and its success report cannot be implemented through that CLI alone. Avoid a
second raw-event reader in the seam. Add a read-only show --json via 05.04, reusing
Clerk's existing validated projection, then pin its accepted interface/source.
2. On S7's existing-delivery status path, require the link's bridge_job_sha256 to
equal the original app provenance.job_sha256, in addition to matching current job
bytes. Correct IDs/instruction hash alone do not bind changed backend/limits/work
metadata to the historical request. Refuse conflict before copy/Clerk return.
Retain the same checks on completed-job replay; do not bypass actor/instruction/
stored-job identity just because the job is already returned.

Q01 recommendation for the first fixture-only slice: uncollected/failed/uncertain
worker outcomes do not become normal Clerk returns. Stop explicitly, retain the
claim and receipt/diagnostics, and report the attention target. This is a local
scope recommendation for the next Director-released pack, not a global rule that
failed work must be invisible. A general failure-return convention is deferred
to Prime intake/Clerk design; the seam cannot silently close or approve the job.

External sibling fixture/store placement and verified exclusive outbox copying
are sound for the declared boundaries. Partial copy stops for explicit attention;
no cross-store transaction or automatic relaunch is claimed. No new design pass
needed: add these requirements to the next implementation batch after 05.04.
The active 0507 Prime-support work and SoF are untouched.
Evidence: evidence/prime-review-05.03-2026-10-27/
