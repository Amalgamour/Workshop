# Prime review - 0523/05.03

date: 2026-11-01
who: Codex Prime
reviewed_commit: dd4cd00a7c4e75b66e3a0716d564a19e5beca59f
disposition: substantial prototype reliability progress; further pending-revision visibility gap found; no app adoption

### Source, scope and platform verification
The branch descends from the published review/pack base
42563e669457a46b73f0be8c8caf30d9d16c819d. All 19 frozen pass03 inputs, 25 artifact
rows and 33 original pinned reference files match. Changes remain within the
assigned app/desk_core and 0523 pass03 paths. Cloud Linux results (22 tests on
Python 3.11 and 3.10) remain builder-reported, not Prime's independent Linux runs.
Prime used an exact Git export on native Windows Python 3.12.14, separate from
production app. No submitted source edits or lock/I-O substitutes were used.

### Native results and review-harness qualification
The full native run exercised 22 tests: 21 passed, one failed because Prime's
initial export omitted original pinned reference files outside the prototype
prefix. That failure is retained. After hydrating/verifying all 33 reference files,
Prime reran only the affected dependency/undeclared/live-refusal test: it passed.
A sandbox-only retry failed to create its temporary book; it is preserved separately;
the authorized fixture-access retry passed. No product repair was needed for that
failure. Together the original 21 passing checks and affected successful recheck
verify all 22 checks; do not describe this as one clean 22/22 full-suite run.
The full run took 137.519 seconds. Native demo exited 0 with expected refusals.
Raw commands, results, source and export correction are under prime-review05.03.

### What improved
CC-05 is verified: an actual Windows child fails to acquire the parent-held byte
lock. CC-06 is verified: byte-targeted tamper test, LF/CRLF headings, CR-only precise
format refusal, non-ASCII roundtrip and outside-section byte preservation pass.
Revision tests terminate a subprocess at nine internal boundaries and inspect/
recover in new processes. The suite confirms prior wording/history retention,
restoring the prior pair after a split replacement, committing an already matching
verified proposal, unchanged receipts, conflicting retry refusal and stale-return
protection. These are process-exit tests, not power-loss, filesystem durability,
OS isolation or concurrent race-freedom proof. The tests mostly cover the first
revision. One assertion compares a file read with itself and adds no evidence;
other before/after and repeated recovery assertions carry the real checks.

### CC-07 - pending work hidden behind a valid selected revision
Prime independently tested A -> selected B -> interrupted C using unmodified code.
At DESK_CORE_FAULT=after-prior-task during C, history/0002 retains intent.json and
task.json, but show reports revision_state selected and recover reports idempotent.
Neither exposes that unsealed C proposal as pending. B's bytes remain coherent;
this probe found hidden pending work, not loss of B or a falsely fresh A receipt.
After a later C crash (after-task-replacement), show reports conflict and recover
restores selected B correctly. Both results and complete small history records
are preserved in second-revision-probes.json. The selected-record fast path in
_revision_state/_reconcile precedes inspection of unfinished newer work.
If the prototype continues, represent selected baseline and pending transition
separately, keep the valid baseline usable where safe, and expose request/revision
identity plus the retry/recovery route. Do not silently discard or automatically
promote C merely to make the pending flag disappear. Add second/subsequent revision
crash tests and repeated recovery coverage. No general architecture rewrite needed.

### Meaning for the normal app
This is a useful independent experiment. Preserve the invariants and failing
counterexamples in N4NN, not automatically the package/schema. The normal app must
separate selected state, pending operation, custody validity, review freshness and
acceptance. 'Idempotent' must name the operation/scope: selected B being unchanged
does not mean there is no unfinished C. Native portability is now substantially
better and the first-revision recovery design has meaningful test evidence.
No production app files were copied or integrated, no live migration happened,
and matching 0123 custody remains pending. User commissioned an insight prototype;
this return does not replace or hold the Prime desk work. No new repair released
by this review; a CC-07-only follow-up would be the next bounded prototype action.
