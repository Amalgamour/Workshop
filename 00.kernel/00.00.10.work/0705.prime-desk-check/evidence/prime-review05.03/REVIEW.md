# Prime review - 0705/05.03 real-output adapter
date: 2026-11-01
who: Codex Prime
state: bounded Colab result accepted; pinned pass01 desk NOT accepted

## Alignment and evidence
Claude delivered actual pinned candidate execution and a traceable adapter rather
than another synthetic-only result. It preserved original oracle/expectations and
separated product defects, representation gaps, unsupported coverage and a fixture
error. Contextual session disclosed; not a cold-model test or real Prime activation.
All 78 frozen inputs and 417 artifact rows match, plus return/manifest pointer
hashes. Live app/librarian.py and README differ due the separately released lane;
these were not used in the experiment. Prime did not inspect or alter that lane.

## Independent reproduction
Prime ran nine adapter self-tests on Windows Python 3.12.14: all passed. Prime
also reran the baseline on fresh disposable copies using only the pinned pass01
candidate/context and pass02 fixture/checker snapshots. The runner completed, but
the actual desk verdict is not-passed. Per-assertion statuses exactly match Claude:
12 pass, 9 wrong, 29 unsupported, 4 not-run; all 24 manual items pending. The
runner's exit 0 is lab execution completion, not a desk pass. C18's actual traceback
was independently reproduced. No missing candidate result was filled in.
Prime reran the supplementary C05 probe separately: both attribution assertions
wrong. This probe adds the fixture's missing selected-task source and is not folded
into the original oracle result. Raw evidence, mapping traces, conflicts, reports,
source identities and exact commands are preserved under prime-review05.03.

## Confirmed product findings
PD-01: the parsed canonical assignment differs from selected work; the independent
shadow selector still wins. No actual selection-conflict attention is emitted.
PD-03: packet wraps the entire mixed-author file as Director text; exact words are
preserved but the Prime interpretation isn't separately attributed. The completed
C05 probe provides the valid evidence; main C05 cannot establish this defect.
PD-04: malformed canonical record with duplicate current_work raises the pinned
reader's Stop exception, which assignment_fields doesn't catch. Result is traceback,
empty stdout, exit 1 rather than a structured partial/refusal. This is not a runtime
pin mismatch. Add a regression when reviewing Grok-1's successor; its active pack
already requires malformed-selector handling. No mid-pass pack change needed.
PD-02 task-bound packet gap remains from the prior Prime review; this baseline
cannot exercise arbitrary work packets without the shadow-selection workaround.

## Prime technical dispositions requested by Claude
Holds boundary: first slice uses explicitly registered, attributed hold/finding
references, with exact source span/hash where the source is prose. A catalog can
index a supplied semantic finding; it cannot silently authorize execution or
replace the underlying rule. Compute needn't invent a prose interpretation engine.
For a page without a supported typed hold reader or declared hold references,
coverage is unknown/not inspected, never no holds. All relevant declared critical
holds must remain visible despite budget/overflow. Missing source or changed span
stays a gap. Current pass01 lacks sufficient output for these fixtures; do not
relabel that as proof no hold exists. Larger typed hold extraction can be later.
C03 boundary: the candidate explicitly reports foreign read=false/same_instance=false.
That is safe non-ingestion, not a demonstrated cross-instance leak. A separate
refusal status or fabricated filename isn't necessary to establish that boundary.
The adapter's null path is honest; retain it as a vocabulary/coverage limitation
until a versioned oracle/adapter correction expresses this valid behavior. No
reason to request a Director choice or weaken path isolation here.

## Fixture and coverage qualifications
FX-01: main C05 omits its own catalog's selected work file. The missing-packet
result cannot prove bad attribution. Preserve pass02 and document a successor
fixture/delta, not silently add the file to historical evidence. The supplementary
probe is correctly labelled. C10 counts include incidental gaps, so >=40 is not
proof that 40 intended attention items survived. Empty-list consistency checks
can pass vacuously. Distinguish assertion passes from actual requirement coverage.
The 29 unsupported assertions are not 29 demonstrated defects: some are absent
mapping, some missing product fields and some current read boundaries. Each needs
a declared reason; unsupported required facts still prevent desk acceptance.
Manual readability/forbidden-inference assessment is not supplied automatically.
No reason to fill all 24 yes boxes on a failed baseline merely to finish a form.

## Disposition and next
This Colab performed its job: expose failures without manufacturing observations.
Its adapter is a useful pinned baseline, not a product API or authenticated runner.
Keep this evidence stable. Wait for the already-running Grok-1 successor, verify
its canonical selector, per-work packet and structured malformed-input behavior,
then commission a precisely pinned adapter revision and rerun. Drop the synthetic
shadow selector for the canonical successor. Keep actual expectations independent;
correct FX-01 in a versioned fixture only with explicit before/after traceability.
No new Claude pass released here, no product/source edits, no N1NN allocation or
Director authority expansion. The app remains unaccepted until actual focused
Prime use is demonstrated; these results test the historical baseline only.
