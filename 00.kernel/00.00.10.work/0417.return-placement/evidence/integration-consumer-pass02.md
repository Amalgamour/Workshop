# Integration consumer profile - scoped successor
date: 2026-11-01
who: Codex Prime
state: technical contract for 0522/05.04 only; not new law

## Basis
Frozen integration-seam-v1.md remains unchanged. 0704/05.02 is advisory; Prime's
06.02.review.md selects this bounded subset. Source producer is reviewed 0521/05.03.
No new custody writer or permission. No N1NN allocation or live book mutation.

## Exact meanings
origin is book/page/batch, derived from verified reservation, not directory name.
route is the declared N5NN -> same-N N1NN.subject relation or N7NN page-local.
target_page is the actual return page DIRECTORY (e.g. 0199.synth-lab); it is not
0599.synth-lab/05.01.md. That latter review destination is independently derived
from origin. For N7NN, target_page is its source directory and the review tail is
06.NN.review.md. return_path names the returned text FILE. custody_path names the
custody DIRECTORY. receipt_path and manifest_path name files verified inside the
specified custody format; no arbitrary regular-file substitute for custody.
All descriptor paths are normalized root-relative within the fixture book.
verification.tool_path is repository-relative to the pinned installed tool bundle,
not a caller executable selected by its path. evidence_path is book-relative.
A result label or evidence file's existence is never proof; reexecute a pinned
validator and validate the actual current records. Consumers never execute a
caller-supplied arbitrary verification.tool_path.

## Supported descriptors
Read exact return-line-descriptor/1 from the real 0521 producer, with
return-line-capture/1 or legacy-relocated/1. Preserve old /1 bytes and semantics.
Also read exact return-line-descriptor/2: the /1 keys plus placement with exact
keys status, intended_target_page, intended_return_path, relocation_record_path,
occupancy. Supported /2 variant in this slice: legacy-in-place/1 with pending
placement, actual target_page/custody_path = original member directory, origin
from the historical reservation, intended fields = derived correct line/tail.
No staged-seal/1 writer or consumer, no relocation equivalence. Explicitly refuse
unsupported variants with preserved reasons. Do not claim every v2 feature works.
If /2 final variants are implemented, apply the same verified /1 final rules.
Unknown/missing hashes are null, never invented empty digests.

## Validators and identity
New placed captures: invoke pinned 0521 read-only verify/lookup against actual
records; match returned descriptor fields and independently derived origin/route
and expected submission. Validate reservation -> manifest -> receipt -> return,
required payloads and hashes; compare the page tail with custody text.
Legacy-in-place: pinned return_inspect.py with its pinned helper validates the old
member without writing or allocating. Extract true origin/submission from records.
legacy-relocated: the pinned placed reader validates actual relocation provenance
and old-format custody, not rewritten legacy metadata under a new name.
Missing/incomplete/reserved/conflict remain distinct. Never promote a synthetic
schema or a descriptor's self-selected bytes to verified custody. Labels do not
authenticate actors or approve work. Reject mismatched origin, subject, prefix,
pass, submission, reservation hash, payload or manifest chain.
Historical captures do not universally contain an authoritative semantic task
binding. Distinguish verified custody, material reviewed now, and proof that the
return answers today's task. Preserve known task changes as stale; where task
association is unprovable, expose unknown/not-established rather than invent it.
Do not make task freshness claims solely from receipt presence.

## Ownership and limits
0521 bytes stay frozen. Add only read adapters in the review lane. Real producer
fixtures can write disposable copies, never live captures. No migration, staged
seal, semantic judgment generation, Director approval or app facade registration.
Reviewers supply judgment; compute verifies identity, preserves, records, renders
and recovers. Unknown capability is not authorization. Keep predecessor schemas
and existing records readable under their historical interpretation.
