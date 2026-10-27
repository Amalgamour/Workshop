# Prime review — recorded Prime boot design
Date: 2026-10-27. Reviewer: Codex Prime.
Disposition: ACCEPTED AS DESIGN INPUT with implementation requirements below.
No runtime boot, model-readiness trial or real installation was performed.

Read all of BOOT.md, examples.json, verification.json, notes and submission.
Independent checks: 12 supplied snapshots; six real source citations across five
examples, including the extra dated source in the earlier TSV pack; current 0107
receipt identity; fresh verification of builder-local 0111 and all four declared
source outputs. No code changed and no runtime suite needed for this design.
The initial Prime harness expected an old JSON manifest; pack05.01 is TSV. The
harness was corrected to read its exact recorded format; no product change.

What is strong: a bounded explicit boot, recorded inputs, source references,
separate seen/readiness/authority, remediation without invented answers, and no
claim that the draft return inspector or absent role seating is already built.

PB-01: allocate attempt identity and preserve request/intent before fallible
preparation. Failed and interrupted boots must leave honest stage/failure evidence,
not vanish because B10 was reached only after successful B0-B9. Exclusive per-stage
files are compatible with an append-only attempt; no multi-file atomicity claim.
If the designated record store itself is invalid/unwritable, report that failure
explicitly rather than claiming an attempt was recorded.
PB-02: attention order is advisory. Check that the model's target belongs to the
declared scope and cited observations; do not require attention[0] or make sorting
choose a route/authorize work. Judge the explanation separately.
PB-03: a clean bounded packet may honestly say no unknown was found. Missing
sources need explicit absence evidence; do not demand an existing-blob citation
to a nonexistent file, or make the model invent a dependency to pass O5.
PB-04: distinguish exact Git-commit blobs from dirty/live/store observations.
The latter cannot inherit a stale commit citation. Record observed identities;
an unstable required source prevents a falsely coherent prepared packet.
PB-05: carry actual bounded, retrievable source material and omission records,
not just filenames/hashes. Receipt integrity is scoped; it does not assert that
review/publication elsewhere never happened. Reading orientation is not authority.

Fixture-only working choices for U01-U05 (not live policy): external explicit
records directory; explicitly supplied judge report recorded by the prototype;
explicit bounded registry/target selection, no canonical-record schema rewrite;
default 12 references and 128 KiB raw source material with honest overflow;
draft Prime role may support a fixture exercise, no seated-role claim. Real
installation, authority delegation and replacement Prime remain Director decisions.

Next bounded implementation: 0507/05.07. The new return inspector remains unaccepted
and is not a runtime dependency of the first prototype. Its later pin-gated
integration is separate. Grok-2 is still active and is not reviewed in this pass.
