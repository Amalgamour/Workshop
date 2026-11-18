# 06.02.review - Enforcement design review
date: 2026-11-02
who: Codex Prime
disposition: useful reviewed design/findings; not a released production integration pack

## Verified and relayed evidence
Full return and proposed integration/cutover design read; helper allocation_lock source inspected. All 37 inputs and 44 artifacts independently match bytes/hash. Claude's preserved H1-H4 probes report that direct old reserve ignores the layout, while an occupied allocation lock stops reserve and leaves existing capture/verify/inspect usable. Those subprocess probes were not independently rerun by Prime in this review; the O_EXCL lock behavior is supported by the inspected helper source.

## What aligns
The active instruction path, not the newest helper's existence, determines real routing. The proposed phase gate and source-linked first-filings checks are useful. Reconstruction-before-retirement, incomplete 0154 and explicit Prime execution under Director release follow 0417/06.05. Keeping archive old names can support unchanged historical readers; actual reader behavior after retirement still needs the returned contract/tests. Live authorization and exact archive roots remain future bound-plan material.

## Changes/conditions before implementation release
Do not release the integration against invented Grok-2 C1-C4 values or stub tests as if joint operation passed. Wait for the real returned tool contract and reconcile ownership, authorization/phase gate, retirement and lookup outputs. A test double may support isolated unit development but is not a reason to freeze a guessed production interface now.

The persistent .allocation.lock sentinel is a proposal, not adopted law. It repurposes a crash/concurrency lock as routing policy; implications include five-second generic refusal, lost idempotent reserve, mistaken stale-lock cleanup, and old direct reserve becoming usable again if the sentinel is removed. A new door detects inconsistency only for calls through that door. Before adoption require exact lifecycle/ownership/removal rules, explicit operator text, missing/changed sentinel checks and resumed-cutover evidence. Do not claim this enforces arbitrary same-user writes. Prefer the smallest supported route consistent with the actual migration tool.

109 textual helper-pin matches are not automatically 109 runtime edits. Separate active pinners, frozen historical modules, docs and sealed capture evidence; never rewrite sealed bytes to update a pin. Compare the bounded successor/guard alternative on actual active dependencies rather than total grep count alone. No global repin is granted.

The app registration observations were made during another lane's work and are not a final current app selection statement. Any integration pack must remeasure after the authoring lane finishes, not silently repin an in-flight app file. Archive lcheck compatibility and post-retirement reader tests are still unperformed.

## Next and status
Grok-1 is idle, not claimed on 0526/05.01. Director reports Grok-2 still working on 0521/05.04; leave it running. Ready next assignment for Grok-1 is 0526.dev-authoring/05.01, per the Director's new dev-cycle request. That pack owns the authoring app branch; do not simultaneously launch the return-lines app integration against the same librarian.py. Keep this design as input for the later actual-contract integration, not another ready-to-run worker pack.

No additional Claude job is needed merely to keep it busy. No live move, sentinel, layout, authorization, production edit, approval or custody claim is made by this review. Director clarification already recorded; no new policy question is raised here.
