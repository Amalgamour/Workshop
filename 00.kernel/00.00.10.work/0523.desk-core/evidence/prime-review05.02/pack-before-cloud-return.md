# 05 - Portable, preserving desk-core repair
version: 001
date: 2026-10-31
who: Codex Prime
state: prepared for named Director invocation
Face: 05
PPPP: 0523
book: 00.00.10.work

## Assignment
Executor grok.com builder. Reviewer Codex Prime. Work builder/grok-core-pass01 only.
Read full Prime review on 05.01. Verify evidence/pack05.02/source-manifest.json.
Record invocation/claim. No merge to main/workshop or production acceptance.

## #01 - contract and runtime
Write 06.03.md and evidence/build05.02/CONTRACT.md before code. Preserve build05.01,
old checkpoints and Prime review. Target Windows Python 3.12+ and Linux; cloud
Python 3.11 is permitted for supplementary checks. Report exact tested platforms.
Do not install runtimes or start paid CI. If the target cannot be tested in your
host, label that validation pending for Prime rather than claim it passed.

## #02 - CC-01 portable durable byte I/O
Replace Unix-only locking with a documented portable standard-library approach
that does not silently disable locking on Windows. Byte writes must remain exact
across Windows/Linux, including LF/CRLF, UTF-8 and non-ASCII content. Preserve/refuse
occupied temporary files rather than truncate prior partial work. Write complete
buffers and keep interrupted writes observable. Do not claim race freedom.
Run available platform tests; Prime will rerun unmodified source natively on Windows.

## #03 - CC-02 revision preservation
Before replacing a task or face assignment, durably preserve immutable original
record and face bytes with reason, authorizing task/request reference, hashes and
explicit selected revision. Do not invent an authorizing Director decision; supply
the declared revision request in synthetic tests. Idempotent retry must not create
duplicate history. Interrupted revision must remain partial or retain the prior
selected version; it must not silently lose old wording or show false completion.

## #04 - CC-03/04 exact identity and stale-return protection
Bind normalized source page, subject, pass and kind as well as task content and
declared source/evidence identities. Preserve leading N in N5NN -> N1NN; N7NN is
page-local at supported prefixes. Version changed schemas/preimages explicitly.
Check a receipt's captured task identity against the reviewed/current task. Old
returns remain available as historical/stale; do not label them fresh for revised
work. Preserve the old receipt's bytes. Conflicting/stale release, claim or source
identity must not yield an authoritative fresh next action just because a review
hash can be recomputed. Do not create an implicit semantic approval or discard
work. Preserve the finding and report the affected transition's precise refusal.

## #05 - focused inspectability and tests
For each core transition/refusal expose task/operation identity, applicable contract
version, input/source hashes, actual check/failure, recorded outcome and next route.
Preserve received request and partial evidence where a write was attempted. Do not
log credentials or invent model judgment. Use a small linked record/trace, not a
new event service. Tests must let a fresh reader trace a refusal and successful
transition from their output back to the relevant durable work-book records.
Add regressions for native portable writes/locking; exact prior wording retrievable
after revision; interrupted revision; task A return then task B review refused or
explicitly stale; stale claims; equal text at different source addresses; nonzero
workflow prefix; existing partial temp file preserved; and original loop/idempotence.
Expected negative refusals are successes, not unexpected blocks. Real platform
test failures are evidence to retain and report, not grounds for fabricated passes.

## #06 - stop protocol and return
At coherent checkpoints save notes and scoped commits. Unexpected issue:
STOP, save build05.02/stops/STOP-NNN.json and .md with category, exact command/error,
source/check identity, what worked, recommended smallest fix, required input,
current commit and resume point. Commit/push checkpoint; wait for Prime response.
Do not repeat the earlier runtime override without authorization. Tests expected
to refuse do not trigger STOP. If Git is blocked, retain files and report it.
Finish with submission.md (Did, Blocked, Need), CONTRACT.md, PRIME-USE.md,
verification.json, artifact-manifest.json and raw test/demo evidence under
evidence/build05.02. Full reread and integrate notes. Document old-record handling
and remaining integration boundaries. No live custody claim: matching 0123 awaits
reviewed migration. Update this batch pointer, never allocate 0184.

## Allowed writes
Only app/desk_core/, 0523/06.03.md, evidence/build05.02 and this batch's pointer.
No other modules/pages, capture migration, kernel/law, OS permission changes,
new models, paid calls or installs. Existing app/librarian.py stays unchanged.
Stage explicit paths, Model trailer, push only builder/grok-core-pass01. No force
push, reset/clean, main/workshop writes or self-merge. Prime reviews.

## Return pointer
PENDING. Full submission and checkpoint evidence stay on this page. Correct
matching-line custody remains pending; no completed receipt is fabricated.

## Review - Codex Prime
PENDING.
