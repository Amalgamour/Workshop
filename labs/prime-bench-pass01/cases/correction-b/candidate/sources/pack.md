# 05.04 — confine export paths to the export root
Executor: worker. Reviewer: Prime.

## Finish criteria
- F1. Every written path stays inside the export root; a path outside it refuses with exit 2.
- F2. Tests cover traversal and sibling paths; the suite passes with 0 skips.
- F3. The return reports exact test counts.
