# Prime review - 0521/05.01

date: 2026-10-31
who: Codex Prime
disposition: repair required before migration or enforcement adoption

### Verified
All nine declared artifact rows match. Independent supplied suite ran 19 tests:
18 passed, 1 skipped for symlink privilege, zero failures. Hard-link refusal was
exercised by the supplied suite. Prime reran the live read-only plan independently.
It describes the same 83 audited records; no original captures were moved or edited.
The candidate correctly keeps source bytes, adds relocation provenance, exercises
fixture interruption/resume and explicitly says live enforcement is not implemented.

### RP-01 - workflow-space digit lost
compute_route maps 1504.app-entry to 0104.app-entry, not 1104.app-entry. It rejects
1702.design as undeclared rather than keeping that N7NN page local. The implementation
hardcodes 01 and 07 instead of preserving the leading workflow-space digit N.
Current 0-space examples pass, but the declared general N5NN/N1NN and N7NN contract
does not. Repair route construction and cover multiple prefixes in fixtures.

### RP-02 - migration plan omits occupied line-number conflicts
The independent plan reports zero collisions. Prime checked the computed return
pages against current sibling directories: all 18 target line numbers already have
different historical occupants. The plan lists only a special filing_0121 blocker;
it does not account for the other 17 number/name collisions. File-tail absence does
not make a line address available. Repair planning to enumerate every occupant,
retained source and retirement/staging dependency, without treating an occupied
line as safe. Fixture application must also respect one number/one name or use an
explicit journaled staging phase, not simply create conflicting sibling pages.
No live migration can rely on the current zero-collision summary.

### RP-03 - incomplete custody can become a complete placement
An independent fixture with a usable reservation and return.md but no receipt,
manifest or payload was copied and returned exit 0, complete true, status placed.
The candidate tests use simplified fake custody packages, so they do not establish
preservation of a valid sealed capture. Check required custody structure and its
hash relationships before calling the source ready; a copy ledger alone is not
capture verification. Preserve incomplete sources as incomplete and visible.
The real 0154 has no return and must stay incomplete, even after relocation.

### RP-04 - enforcement scope remains unfinished
The pack requested a line/pass-aware writer/reader candidate. This build supplies
a relocation copier and lookup plus an integration proposal. It has no actual new
reserve/capture route for future work. That is an honestly reported limitation,
not permission to mark workflow enforcement finished. After the migration safeguards
are repaired, a bounded integration slice must retire sequential allocation for new
work in this book and wire all active callers/readers together with their pins.
Frozen fixtures/snapshots need not be globally rewritten to change active routing.

### Disposition and next
Keep this candidate and its evidence; do not perform live moves. 05.02 is the
bounded repair for RP-01 to RP-03 and a precise inventory of remaining RP-04 work.
No Director judgment is needed for these corrections to the stated contract.
No extra Claude work. Existing Grok-2 constructor and cloud core lanes continue.
Full review lives on this batch. Raw probes, test logs and independent plan are
under evidence/prime-review05.01/. No Git publication or custody filing is claimed.
