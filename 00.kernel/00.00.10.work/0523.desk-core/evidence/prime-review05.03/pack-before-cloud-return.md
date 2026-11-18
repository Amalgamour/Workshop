# 05 - Prototype portability and interrupted-revision reliability
version: 001
date: 2026-11-01
who: Codex Prime
state: prepared for named Director invocation
book: 00.00.10.work
PPPP: 0523
Face: 05

## Purpose and assignment
Executor grok.com builder. Reviewer Codex Prime. This is the Director's exploratory
test build, developed differently from the normal app, for insight. It is not a
replacement app, production integration or a reason to hold other builders.
Base returned build eeefbeced8587991e4b4a80ce6620ea78a90c1e3. Read the full Prime
review on 05.02 and verify evidence/pack05.03/source-manifest.json. Record named
Director invocation/claim here and 06.05.md; notes and CONTRACT.md before code.
Use builder/grok-core-pass01 only after fast-forwarding the exact published Prime
review/pack commit supplied in the Director prompt. No reset/force or merging to
workshop/main. Do not incorporate unrelated branches. One bounded pass, then return.

## Engineering requirements, not a prescribed algorithm
Keep the documented prototype CLI connector names and existing request/result
contracts compatible. If correctness requires a new field/schema, document exact
version/compatibility and refuse unsupported input rather than silently rebind it.
Builder chooses internal transaction/recovery mechanism. Reference implementation
is not mandated. Tests assert externally observable preservation and recovery,
not that one particular helper is called. State every tested and untested limit.

## #01 - finish native portability, CC-05 and CC-06
Lock contention test must use a real platform-appropriate independent child probe:
Windows msvcrt and POSIX fcntl as appropriate. Parent-held lock must actually
exclude a competing nonblocking child. Do not replace runtime lock with a no-op.
Assignment-tamper tests must mutate intended bytes without incidental newline
conversion. Separately cover LF and CRLF face headings, UTF-8/non-ASCII content,
exact byte reads/writes and section updates preserving outside-section bytes.
Prefer supporting both newline styles; never silently normalize existing captured
or hashed material. A format refusal must report the actual unsupported format,
not falsely claim a present heading is absent. Preserve occupied temporary files.
Rerun the original loop/demo, history, stale-return and identity regressions.

## #02 - revision preservation invariants
For a selected task A/face A and proposed B, preserve exact A and B material,
authorizing reference, reason, before/after hashes and request identity. Before
any replacement can destroy the sole old copy, history must be recoverable.
A selected state must identify a consistent task/face pair and verified revision.
Do not report B complete merely because one selected file was replaced. Old
selected metadata with new task bytes is a conflict/partial, not an authoritative
current state. Preserve partial requests and diagnose every interrupted transition.
Recovery must either retain/restore a coherent previous state, or complete an
explicit recorded proposal with verified bytes and authority. Never silently choose
an arbitrary highest version, discard partial evidence or invent authorization.
Idempotent replay of the same request must not duplicate semantic revisions or
history, hide unresolved partial work or overwrite an unrelated proposal. Conflict
between another request and an unfinished revision is explicit. Existing sealed
receipts/history remain unchanged; stale returns remain historical.

## #03 - failure-injection matrix inside the write sequence
Exercise failure boundaries in a separate process, not only the current interrupt
flag before selection. At minimum before/after preserving prior task/face; before/
after staging proposed material; before/after revision metadata or journal; after
selected-task replacement but before face replacement; after face replacement but
before selection commit; after selection commit but before cleanup/marker removal.
Map the actual implementation's boundaries and explain any non-applicable point.
Use deterministic test-only injection which cannot be activated by ordinary model
requests. Include abrupt process exit at relevant boundaries, followed by a NEW
process inspecting and recovering the same disposable book. Exception injection
may supplement but is not a substitute for every crash case. Never imply this
simulates sudden power loss, all filesystem behaviors or arbitrary concurrency.
At each point check previous wording and exact bytes retrievable, proposed work
preserved or absent with an honest reason, selected state coherent or explicitly
partial/conflict, receipts unchanged, repeated recovery idempotent, and stale A
return cannot become a fresh B review. Where a crash occurred before durable intent
or any mutation, unchanged A is valid; do not invent preservation of never-written
B bytes. No cleanup step may erase the only evidence needed for safe recovery.
Add corrupt/missing staged artifact and conflicting retry cases; refusal preserves
material and gives a correction route. Do not blanket-retry until checks pass.

## #04 - inspectable results and platform evidence
Keep a bounded linked trace: operation/request identity, governing contract,
observed hashes and actual failure boundary, resulting selected/partial state,
recovery performed and next route. Separate supplied semantic judgment from compute
checks and labels. No general telemetry service or scheduler. Fault-injection
matrix records commands, injected boundary, exit, before/after evidence/hashes,
restart observations, exact expected outcome and actual assertion result.
Windows Python 3.12+ is Prime's native verification target. Linux Python 3.11 is
permitted supplementary cloud runtime, as before; 3.10 optional. Do not install a
runtime or start paid CI. If Windows unavailable, say pending for Prime; don't
claim native pass or stop useful cloud checks solely for that known limitation.
Expected test refusals and injected crashes are not unexpected build failures.
Unexpected missing authority/dependency/contract -> preserve STOP-NNN evidence,
commit/push the checkpoint and report the smallest proposal; stop affected work.
Diagnosed implementation bugs within this pack may be repaired with first failures
preserved. No expanding scope to a new architecture or live tool integration.

## #05 - return and provenance
Before code write 06.05.md and evidence/build05.03/CONTRACT.md. Deliver submission.md
starting Did, Blocked, Need; PRIME-USE.md, verification.json, artifact-manifest.json,
regression and demo transcripts, fault-matrix.json plus readable summary, and raw
failure/recovery evidence. Include original failing runs, exact runtime/platform,
predecessor hashes/delta, manual limits, and one fresh-process reproduction command.
Record what the experiment teaches the normal app without copying code into it.
Reread fully, integrate notes, pin final code and evidence. Manifest self row null
or excluded; submission and manifest hashes go in this batch pointer. Checkpoint
commits use Model: trailer, stage explicit paths, push builder/grok-core-pass01 only.

## Allowed writes and finish
Only app/desk_core/, 0523/06.05.md, evidence/build05.03/, and this pack's claim/return
pointer. Preserve old code in Git history and old captures, packs, notes and Prime
evidence on disk. No app facade, other modules, kernel/law, runtime activation,
live custody/migration, 0184 allocation, OS permission changes, paid calls or models.
Do not overwrite any existing return capture or evidence transcript. Synthetic
books stay separate. Receipt is not review; review is not Director approval.
No completed matching 0123 custody is invented while migration remains pending.
Stop after return. Prime records the full review on this batch. A green Linux suite
is not Windows acceptance, concurrency proof or permission to adopt the prototype.

## Return pointer
PENDING. Record invocation/claim, exact commits and completed output hashes here.

## Review - Codex Prime
PENDING.
