# 06.05.review — Harness repair H01–H03
date: 2026-11-01
who: Codex Prime
source: 0707.app-use-check/05.05.pack.md and 05.05.return.md
disposition: timeout and static-boundary repairs verified in the lab; one bounded-input defect remains; candidate activation held

## Deliverable and alignment
Claude produced a nonproduction harness successor, not app code. It preserves the original 33-case matrix and fixture sources by pin, keeps null-candidate runs UNREADY and A24 MANUAL, and documents the Job Object and static-boundary limits. This aligns with the assignment. No active app selection or production-code change was made.

## Independently verified
All 76 frozen input rows and 1,729 artifact rows match bytes and SHA-256. Ran all 20 focused self-tests independently under Python 3.12.14: zero failures, errors or skips. Imported the suite and redirected its scratch/evidence destinations; replaced only the test config interpreter with the native host interpreter. Raw run evidence is evidence/lab05.06/prime-independent-selftest, with suite summary and additional probes copied to evidence/prime-review05.05.

The tests exercise actual stub processes, timeout output on both streams without duplicate markers, child cleanup and unrelated-process survival; static junction refusal at preflight and the fixture writer; malformed ordinary config shapes including dependencies=null; unknown-candidate no-launch behavior and preservation. No real loop, constructor, cycle or app was launched by this review. The original tests and builder evidence remain unchanged.

## Finding H04 — malformed filesystem paths escape the refusal boundary
Severity: bounded repair before activation. A shape-valid config with output_root containing an embedded NUL passes validate_config, then preflight raises ValueError from guards.is_link_like/os.lstat. The public CLI catches Refused only, so this path does not produce the promised controlled refusal. Reproduction is a preflight-level independent probe, not a candidate launch. Exact traceback is additional-negatives.json. The probe did not create a fixture or touch a candidate.

Repair expected path/input exceptions at their boundary, with coded REFUSED and no child or fixture write. Cover path-bearing config fields and CLI config/evidence paths; test the real entry boundary as well as direct helpers. Do not catch arbitrary internal bugs as ordinary refusal. Preserve raw config bytes when an authorized evidence destination is usable; an invalid evidence path must not cause fallback writes.

A separate 1,200-level JSON-array probe correctly raised the intended config-shape Refused on this host. It is not a new defect. The existing fuzz allow-list is consistent with documented shape-only validation; it is not evidence of correct file identities while the candidate is unknown.

## Limits
Windows Job assignment still has the documented start-to-assign window; fallback cleanup and untested POSIX behavior are not stronger guarantees. Static guards are not a sandbox or race protection. R02 wording heuristics and field-map limits remain. A24 stays MANUAL, so a later real aggregate may be INCOMPLETE; do not relabel it PASS. Earlier AR-01 hold is unaffected.

## Learning and next bounded action
The reported three failures are repaired on their tested paths, but checking JSON types alone does not guarantee valid filesystem input. Translate expected path failures into observable refusal before any candidate work. Prepared 05.06.pack.md for that small nonproduction repair. Once reviewed, a separately released real-candidate run can use the reviewed 0522/05.08 loop pins in a NEW config; this review does not release that run or switch the app.

## Director / disposition
No Director design decision required. Preserve this review, Claude's original return and the failing probe. No custody receipt or allocation is created.
