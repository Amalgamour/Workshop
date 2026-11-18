# Prime review - 0518/05.01
date: 2026-10-31
who: Codex Prime
disposition: repair required before routine use; capture preserved

## Deliverable and alignment
Claude built a lab-only review adapter, not production app code. It reuses the
pinned producer and custody tools, adds declared review plans, retains comprehension
in JSON and maps supplied synthesis to original findings. This aligns with the
released pack. It does not implement the desk application's handoff core, launch
models or establish context isolation. No reason was found to discard it because
of the model/provider used; the defects below are reproducible implementation gaps.

## Independent evidence
- Capture 0179 verified complete; receipt
  56506ac5d33fc062de5f052785ce8250847a0686dccb398904211d4d9f748c8c.
- All 10 artifact-manifest rows match current bytes and lengths.
- All 65 source pins match live files and their supplied snapshots.
- Supplied test suite: 11 passed, zero skips, 42.847 seconds in the authorized
  rerun. See independent-checks/tests.stderr and checks.json.
- Three additional end-to-end synthetic probes used actual stage/prepare/bind,
  captured review payloads and intake/synthesis commands. See independent-probes/
  results.json and its preserved scratch inputs/outputs. No actual reviewer ran.
- First default-temp attempt failed before behavior checks with WinError 5 when
  creating a fixture src directory. A writable-workspace temp attempt failed the
  same way; its raw log is retained in attempt02-sandbox. The authorized rerun
  passed. These are execution-environment failures, not product test failures.
  The first attempt's raw trace remains in chat tool output; it is not claimed
  to have been captured as a separate file here.

## PR-01 - intake errors lose their explanation in synthesis
Priority: high for normal use. Probe context-error supplied full conversation
against a plan declaring none. Intake correctly returned exit 1, status incomplete,
and context-mismatch. Synthesis returned exit 0 and consistent, retained only the
intake_status label, and omitted the mechanical intake finding from both its
report findings and Markdown. Markdown said no incomplete reviewers and no
residual uncertainty. Consistent mapping is not a complete investigation, but
the exact reason must remain visible through the report interface.
Fix: carry intake diagnostics into derived JSON and Markdown, and distinguish
mapping consistency from review completion. Reporting may still work on incomplete
input; do not drop its errors or imply that zero synthesis errors resolves them.
Location: colab_review.py cmd_synthesize and render_report.

## PR-02 - an optional reviewer's failure disappears from the report
Priority: medium. Probe optional-failed submitted an actual captured failed result
for optional simplicity stage S03. Intake retained the row but counted only
required stages in incomplete. The final report said complete and consistent,
with no incomplete reviewers and no mention of the failed optional stage.
Optional may remain nonblocking; it must not become invisible or look like a
successful zero-finding review. Fix: preserve a stage/reviewer status inventory,
including optional absent, failed, partial and not-run states, in JSON and Markdown.
Location: cmd_intake required-only incomplete loop; cmd_synthesize projection.

## PR-03 - retained original finding text omitted from Markdown
Priority: medium. Probe retained-text mapped a sole finding to minority. JSON
kept its original text, but REPORT.md printed only id, disposition and reason.
The concern itself ('SYNTHETIC ORIGINAL: return recording may lose its evidence.')
was absent. This contradicts the guide's promise that the report quotes originals.
Fix: render the original text, target/location and custody reference for retained
findings, as well as consolidated ones. Preserve the exact original wording.
Location: render_report Retained section.

## Boundaries and learning
The one-return-per-pass workflow limit was honestly declared. Multiple originals
remain in N1 custody; this review does not authorize a multi-return redesign.
The source tests check intake and synthesis mostly in isolation; the new probes
expose information lost between them. Add regression checks across that boundary.
Immutable originals surviving is necessary but insufficient if the ordinary Prime
report omits the facts needed to judge them. Preserve both custody and visibility.

## Disposition and next action
Do not use this adapter as the sole routine review interface until PR-01 to PR-03
are repaired and independently checked. Existing pack/return workflow continues.
No implementation file was edited in this review. No app rollback is needed.
Use Grok Build for a bounded follow-up implementation pack under the Director's
current role split; Claude may run labs or review the repaired behavior. Do not
rebuild all code or erase the original capture. The next pack should bind these
findings, original source and tests; regression checks must exercise all three
counterexamples and a normal successful report.
No new Director design decision is needed for these repairs; no execution pack
is released by this review. The app-core design/lab assignment remains a separate
next task through the existing work-book route.

## Preservation
This review and its evidence are on 0518. Original capture 0179, submission,
builder evidence and code remain unchanged. No Git commit or push was made by
this review. Published availability is therefore still pending.
