## Review — Codex Prime
Date: 2026-10-27.
Disposition: HELD FOR BOUNDED CORRECTION; NOT READY FOR LIVE PRIME INTAKE.
Prime verified all 21 manifest entries, reran all 19 tests successfully and the
14-process/18-check demo successfully in disposable copies. PS-01's fenced-heading
decoys and PS-02's explicit SoF file adapter now work in the declared lab.
PS-03's preservation direction is implemented but has two material binding/order
defects found by independent probes; the passing suite did not cover them.

PSI-01 — Unbound resolution closes a finding. Reproduce with one committed return
reviewed at its actual revision, PS-X=unresolved, then a later review naming an
unknown but well-formed hash aaaa... and PS-X=verified-fixed. status reports closed,
passes=2 and attention=[] although no observed return has that hash. Do not let
an unbound/invalid resolution change the last valid finding or increment passes.
Show the conflict and retain the unmatched review; never hide it by dropping it.

PSI-02 — Timestamp order can erase a later unresolved finding. In a normal ancestry
chain, commit A dated 2030 says verified-fixed; descendant B dated 2029 says
unresolved on the same return. With worktree off, status picks A and reports closed.
Commit timestamps do not establish ancestry or authority. Use causal ancestry for
same-source updates; incomparable branch/source resolutions must remain explicit
conflicts rather than silently picking by timestamp or registry order. Define the
status of uncommitted review edits separately from committed resolutions.

Independent fixtures and complete results are preserved in independent-probes.json.
No live store is installed and no shadow Prime was started. Provisional schema
fields remain local to the lab. Keep original runs/design before changing code.
Next: 05.03, a correction only for PSI-01 and PSI-02, then repeat original tests,
demo and both independent counterexamples. Clerk adapter and capture adapter wait.
Evidence: evidence/prime-review05.02/.
