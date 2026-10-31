# Prime review — readiness checker 05.01
Date: 2026-10-31
Reviewer: Codex Prime
Disposition: correction required before operational readiness gating.

## Did and verified
All 10 artifact rows match current delivered bytes. All six captured payloads
match their declared identities and current source copies; fresh capture verify
succeeds. Prime independently ran 28 tests: 27 passed, one file-symlink test
skipped for WinError 1314, no failures. The suite includes the frozen copied-tool
read/record/read demonstration, which passed. These are local tests, not a fresh
model trial or the proposed second replay.

## What works
Separate readiness facets, bounded file hashing, nested evidence checks, explicit
unsupported formats, labelled synthetic judgment, and failure/withhold reporting
are useful. Runtime and evidence closure are treated separately. No command text
is executed by the checker. The historical inventories retain the first replay's
five support requirements and 19 omitted nested specimen references.

## Findings
R-01 — A transported entry point with an empty dependency declaration reports
runtime_dependencies_resolved=true and ready=true. There is no required root
declaration or explicit dependency-free assertion, so an undeclared entry is
indistinguishable from a verified dependency-free entry. Require accounted roots.

R-02 — A passed smoke object with final child_exit=2 and wrapper_exit=2 still
reports passed and ready=true. Equality preserves the exit layers but does not
establish a usable execution. Define the expected successful exit for the named
stage, bind it to the record, and reject a failed final reread. Do not erase the
first route read's legitimate awaiting-review exit 1 or demand all route exits 0.

R-03 — Required evidence can refer to an untransported, unpinned empty manifest
and still satisfy evidence_references_resolved, minimum_evidence_satisfied and
ready. Prime's disposable probe removed manifest.json from transport and replaced
it with an empty artifact list. Require evidence-root identity coverage and do
not let required categories be discharged by an empty evidence set. This is a
mechanical gap, not a request for compute to judge the prose's relevance.

The submitted tests pass because they do not exercise these cases. Raw requests
and outputs are retained in independent-probes.json. Submitted files and sealed
capture are unchanged. The contract itself permits some of these false positives;
repair the contract and tests together, preserving the original submission.

## Learning and next action
0316.dependencies records the Director's new N3NN direction: maintained module
requirements and construction provenance. This checker remains a bounded consumer
of a declared inventory, not that maintained registry. Avoid conflating the two.
Next bounded action: repair R-01 through R-03, preserve the six independent facets,
and review the corrected checker before creating a jointly verified Colab delivery.
No Director design choice is required to correct these false-positive paths.
No code, kernel, runtime activation, replay seal or accepted adapter was modified.
AR-01 remains held. File-symlink behavior remains unexecuted on this host.
