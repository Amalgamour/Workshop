# Prime review - 0524.prime-desk
date: 2026-11-01
who: Codex Prime

Disposition: repair required before real desk use.

All 39 frozen inputs match; 41 artifact rows and both pointer hashes match. The
live 0522/05.04 page differs from the frozen input because its builder returned;
that is an expected recorded revision, not automatic corruption. Prime reran 17
unit tests on Windows Python 3.12.14: 17 passed in 5.848s. The independent demo
wrapper exited 0, while the generated view/packet report attention (exit 1), as
expected for missing verification and supplied facts. No live view was attempted.
The output is useful scaffolding: source hashes, read-only stdout, visible missing
information and separate supplied activity. It is not ready as the canonical desk.

PD-01: the tool introduces prime-desk-selector/1 with selected_work_id as the
selector, while the canonical 0401/06.01 assignment-record is only a reference
parsed separately. Prime changed only the canonical assignment in a disposable
copy, updated that reference's expected hash and left custom selector unchanged.
The view still selected 0522/05.04, despite the canonical record naming 0521/05.03.
This contradicts 0420 and the pack: current work must come from the existing
canonical selector. An index/cache may point but may not independently choose.
Repair in a versioned successor, preserving this implementation and counterexample.

PD-02: packet references are collected globally by role rather than bound to the
selected work. The demo gives every packet the desk deliverable as criteria and
0412 reporting policy as review-home. General policy can be linked, but the actual
review destination must be derived from the chosen page/pass, and task-specific
criteria/returns/findings must not silently become another work's packet. Bind
references to work identity; distinguish desk-wide policy from task material.

PD-03: the Director-role quote currently includes the whole mixed-author source
file, including the separately headed Prime interpretation. The headings survive,
so no literal words were lost, but a single role=director wrapper is insufficient
attribution. Preserve exact Director blocks with source spans/hash and keep model
blocks separately attributed; don't assume separate files mean separate authors.

Manual live-request assembly and frozen-to-current source selection remain Prime
work. A changed source is not repaired by blind rehash: review the actual change,
select the version explicitly and retain provenance. No product reader/activation
or custody guarantee follows from these unit tests. Draft next pass is 05.02,
held for Director review. No live migration or matching 0124 custody claimed.
