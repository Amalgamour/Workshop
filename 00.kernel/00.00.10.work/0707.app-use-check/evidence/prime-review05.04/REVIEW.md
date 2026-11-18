# Prime review — 0707.app-use-check / 05.04
Date: 2026-11-01. Reviewer: Codex Prime.
Disposition: useful acceptance-lab preparation; hold real-candidate activation pending harness repairs.

## Independently checked
All 60 frozen source rows match snapshots and live bytes; all 336 listed artifacts match. Read the return, harness, fixture builder, case matrix and source, self-test/activation contracts and limits. Independently ran the 14 harness self-tests on Python 3.12.14 with OUT/SCRATCH and the interpreter configuration redirected to NEW Prime fixtures; all passed. Only labelled stubs/fixture recipes ran, not a real candidate, cycle, constructor or app. Candidate pins remain null and the real matrix unready. The model is an informed contract/harness author, not a fresh reviewer.

Positive boundaries: unknown candidates launch nothing; real/stub results are distinguished; every named case has evidence/status; MANUAL A24 prevents a false all-pass aggregate; the self-test's earlier failure was retained. Case wording heuristics and field_map remain explicit limitations. A24 may be completed later through a declared independent/manual check, not silently skipped or set PASS from a pin declaration alone.

## H01 — timeout discards partial child output
Run.call catches TimeoutExpired, calls kill_tree (which consumes communicate output), then writes out=err=empty bytes. In an independent labelled stub that flushes stdout and stderr before sleeping, the timeout occurred and both saved files were zero bytes. Required diagnostic output is lost precisely on the failure path. Preserve actual partial stdout/stderr after timeout/termination, without duplicating bytes or representing unavailable output as empty success. Retain argv/exit/timeout and bounded cleanup of the launched tree only.

## H02 — lexical output guard accepts a checkout junction
preflight uses abspath/normcase instead of resolving/rejecting reparse ancestors. A NEW external junction whose resolved target is D:/Git/lib-build passed preflight READY with a pinned STUB. Only preflight/interpreter probe ran: no matrix or project-file write occurred. If used for a run, the fixture writer can write into the protected checkout through that alias.

Required repair: canonicalize and check output roots/parents, reject unsafe link/reparse traversal and enforce the boundary at the actual fixture write entry too. Apply equivalent checks to evidence destinations so a caller cannot silently place them in protected/occupied locations. Keep an explicit authorized fresh evidence root. This is a static path boundary, not an OS sandbox or same-user race guarantee. The test junction stays only in Prime scratch and is NOT copied into review evidence.

## H03 — malformed dependency container escapes refusal
With otherwise valid STUB configuration and dependencies=null, preflight raises uncaught TypeError ('NoneType object is not iterable') rather than REFUSED. Validate all config/container/pin/interpreter/release/field-map types and malformed JSON/input errors before launch or fixture creation; return bounded, preserved refusal evidence, no traceback. Do not turn an invalid configuration into UNREADY for a missing real candidate while silently disregarding malformed fields that should have been checked.

## Next
Prepare a NEW pass05 harness successor addressing H01–H03; preserve pass04 and its evidence. Reuse unchanged acceptance cases and label any changed assertion. No in-progress Grok-1 candidate is to be opened or run by the repair assignment. After its separate review, fill an explicit new candidate configuration and run the external acceptance under a named invocation. Never adjust assertions merely to make a candidate pass. No new Director policy choice is needed for these mechanical repairs.

Evidence: evidence/prime-review05.04 with native self-test result, timeout-check.json, junction-preflight.json and shape-preflight.json. Real candidate acceptance remains NOT RUN. No approval, release, app selection, N1NN receipt or authority is inferred.
