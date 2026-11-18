# Prime review - 0520/05.01 independent desk-loop lab
date: 2026-10-31
who: Codex Prime
disposition: accepted bounded execution evidence; no app activation

## Verified
Capture 0183 verifies complete, receipt
b3c07746fdc207e13f0d44910107acfd83de173588b6b33e57d4273ba2b7a4b7.
All nine non-self artifact rows (including submission and lab transcript/code)
match their declared bytes and lengths. The self manifest is separately bound
by the verified capture. Independent replay.py --transcript ran against the current
existing tools and passed all 16 checks, exit 0. Raw output and transcript are in
independent-checks. The original builder transcript remained byte-identical.

## What works in the demonstrated route
Queue/claim of supplied instructions, handback, capture and a fresh-process Prime
read work through existing CLIs. A captured return is awaiting-review, not accepted.
Supplied held judgment and next-action text survive a process restart. Missing
custody is distinct from a completed return. Accepted judgment without a captured
return is refused. Identical handback retry does not duplicate events/receipts;
conflicting artifacts/submission bytes are refused. Stale instructions fail claim;
page changes make review stale. An unresolved question stays open after restart.

## What remains missing
The lab writes the source page, Return pointer and cycle registration as glue.
No integrated command builds those records from the clerk job/verified return.
The recovered next action is stored text, not automatic dispatch; elected stays
null. Supplied judgment is not model reasoning or proof of semantic correctness.
Process restart is not a fresh model session. No production desk was activated.

## Preservation and test limitations
test_replay.py directly overwrites the builder's transcript at a hardcoded path.
Prime did not rerun that wrapper: used replay.py's supported --transcript option
to write separate review evidence. Future reusable tests should accept an output
path or write disposable evidence, rather than replace previous build evidence.
This does not invalidate the independently reproduced 16 checks.
The builder honestly records one changed mutable source: the other lane's 0519
batch claim/return page. It was hash-checked and not read for this lane. No restoration
of that page was attempted. This is not evidence of drift in a reused runtime tool.
Capture helper's direct already-captured branch was not independently exercised;
the repeated handoff path avoids calling capture twice. AR-01 paths remain held.

## Corrected routing supersedes this fixture's old layout
The lab uses the old sequential N1NN capture contract. The Director has now
clarified: N5NN maps to matching N1NN, N7NN returns stay page-local with tails.
See 0417/06.01. Accept the existing-behavior evidence, not the old allocation as
the design to implement. Repeat the end-to-end replay after corrected placement
and callers are integrated. Current 0183 remains preserved pending migration to
the matching 0120.desk-loop-lab line; do not rename or rewrite it in this review.

## Next action and authority
Complete 0521's fixture-tested placement/enforcement candidate and migration dry-run
first. Then combine this execution evidence with Claude's already-completed 0519
design to release a minimal return-registration/page-construction integration slice
for Grok. No more Claude work is assigned. Production implementation must not harden
the wrong return layout. Routine pointer/registration construction is within the
Director's stated goal; do not invent a new approval requirement here. Any new
release/approval semantics or destructive overwrite policy still need explicit
review, not inference from a receipt.
No follow-up execution pack is released by this review. The lab worker can remain
available for the integration replay. No Git publication by this review.
