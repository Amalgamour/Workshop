# Prime review - 0704/05.02
date: 2026-11-01
who: Codex Prime
disposition: useful design accepted in bounded parts; full v2 not adopted wholesale

## Evidence and scope
Prime read the full return, notes, seam proposal and exact delta. All 15 frozen
source snapshots match their declared hashes. All five returned output hashes
match the pack pointer. Two live source pages now differ from their snapshots
because Prime completed the returned builder reviews; the old frozen inputs stay
valid historical inputs. This was a contextual design Colab, not a cold reader
or executed lab; Claude correctly disclosed prior involvement and no execution.
Supporting checks are in evidence/prime-review05.02/.

## What is useful
The proposal separates valid custody, final filing, review judgment and Director
reporting. It exposes a practical legacy-in-place route, so the first real review
need not wait for every historical return to move. Versioning the descriptor is
right: exact-key /1 readers must not silently accept /2. Staging remains approved
policy, and a work-local evidence location is a reasonable technical direction.
The result classes and report-versus-approval distinction fit the Director's goals.

## R1 - relocation equivalence: retain direction; defer implementation
A mechanically relocated return should not lose its historical review. However,
equal receipt hashes plus a claimed relocation are insufficient proof. Validate
the full relocation provenance and every material component, including task,
source identity, agreement, manifest/payload and judgment bindings. Store both
preimages/evidence if using an equivalence rule. Do not turn a changed origin,
assignment or evidence set into current-via-relocation. No equivalence capability
is adopted or implemented in the next repair; retain explicit historical states.

## R2 - staged bytes: requirement needs refinement
A portable receipt need not embed its own physical path, but the 0521 receipt
hashes a reservation, and that reservation includes line metadata. A staged format
cannot be obtained by casually relabelling those records. Specify immutable
material identities and separate placement provenance, then test the full chain.
Do not change the reviewed 0521 tool under this repair. Staged-seal/1 remains a
future explicit writer contract; absent staging does not mean a fake receipt.

## R3 and today's measured integration gap
Adopt a scoped /2 reader profile for legacy-in-place only, plus real /1 compatibility.
Do not adopt the entire v2 proposal. The measured 0521 -> 0522 probe exposed two
underspecified field meanings: target_page is the return page directory, not the
review-face destination; custody_path is a directory, not a placeholder file.
The review destination is independently derived from origin. Actual receipt,
reservation, manifest and payload relationships must be verified by pinned
readers, not inferred from matching arbitrary hashes. Prime's v1 contract did not
state the object types clearly enough. A new scoped supplement records these
meanings without rewriting the frozen v1 or adopting unrelated proposals.

## R4 - Director decision received
DC3 is now resolved by the Director on 2026-11-01. See 06.03.notes.md for the verbatim
reply. Keep original review, Director answer and successor assessment in the same
home but clearly separated and attributed. Preserve prior bytes/meaning and name
the selected successor explicitly. No detailed schema or implementation is implied.
Successor rendering is deferred; no gate on first-review repair is created.

## R5-R7 - bounded dispositions
Work-local staging under the source page is accepted as a design direction; the
exact staged schema, numbering and relocation writer are deferred. No solo grant
exists here: normal reporting applies. A delivered report records Prime's statement
and exact presented text, not proof of viewing or approval. A report reference to
its own changing whole-page hash would be circular; bind the exact report block
or immutable report artifact, not a self-containing page hash. No new report-state
engine is required for the next repair.

## Additional corrections
Where a gate lacks a required implementation or evidence, return unsupported or
unknown and preserve the request; do not interpret silence as permission for a
write. Semantic disagreement remains for intelligence, not an invented mechanical
refusal. Freshness is derived on read; a timestamped past observation may still be
stored as history if it is not represented as today's truth. No two status systems.
The draft staging.json status transition also needs clarity: an immutable seal
must not be rewritten from pending to relocated; use a separate verified event.

## Next bounded action
0522/05.04 repairs real producer/consumer verification, a read-only legacy adapter,
and nonzero constructor compatibility. It preserves reviewed predecessors and
runs a real generated capture through prepare/record/render/new-process read.
No staging writer, live migration, relocation equivalence, report-state expansion,
scheduler or successor rendering. Those remain separately scoped future work.
