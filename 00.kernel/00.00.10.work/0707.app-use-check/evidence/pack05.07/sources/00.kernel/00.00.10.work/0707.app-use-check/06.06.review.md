# 06.06.review — Bounded filesystem-input refusal repair
date: 2026-11-01
who: Codex Prime
source: 0707.app-use-check/05.06.pack.md and 05.06.return.md
disposition: accepted for the nonproduction harness repair scope; real candidate acceptance NOT RUN

## Deliverable and alignment
Claude supplied pass06 harness/guards and tests, reusing pinned pass05 process containment/stubs and unchanged pass04 matrix/fixtures. It fixes H04 at the path/input boundary without production app changes or candidate activation. This meets the bounded assignment.

## Independently verified
All 92 frozen source rows and 936 artifact rows match bytes and SHA-256. Independently imported selftest6 and ran 37 tests under native Python 3.12.14: 37 passed, zero errors, failures or skips. Output/scratch globals were redirected into NEW destinations; test config interpreters were changed to the native host version. Original test sources and builder evidence were not edited. Raw full evidence: evidence/lab05.08/prime-independent-selftest; copied suite summary, integrity and runner: evidence/prime-review05.06.

The actual CLI comparison reproduces pass05's NUL-path traceback and shows pass06's coded refusal on the same config. Focused negatives cover output, candidate, dependency, interpreter, config and evidence paths; invalid evidence has no fallback destination. Regression tests retain timeout stdout/stderr, process-tree cleanup and unrelated-process survival, static junction checks at both entry points, occupied destinations, config shapes and null-candidate no-launch behavior. Mocked PermissionError and planted TypeError remain explicitly labelled; the latter is not swallowed. Source inspection confirms path text is checked before unknown-candidate identity handling and expected filesystem exceptions are translated locally.

## Findings / limits
No new blocking finding in this repair scope. This does not mean every filesystem failure, concurrent change or operating system is covered. Static boundaries are not an OS sandbox; Windows Job start-to-assign uncertainty and untested POSIX behavior remain. The original R02 wording heuristics and field-map limits remain. A24 remains MANUAL, so later real acceptance cannot be called a complete PASS solely from this harness aggregate. Existing AR-01 hold is unchanged.

## Learning preserved
Separate path-text validity, filesystem validity and unknown candidate identity. Malformed path strings should produce a recorded refusal without giving an unknown candidate any access. Preserve unexpected programming failures as failures, rather than hiding them under generic refusal.

## Next bounded action
The reviewed loop (0522/05.08) and repaired harness are ready to be specified together for a real candidate lab. Prepare a NEW pinned config, confirm dependency pins/field-map expectations against the reviewed contracts, retain A24's separate manual evidence and run only after the later named invocation. Preserve every resulting failure as a finding; do not tune the matrix to pass. This is candidate-loop acceptance first; active app/door selection is a later integration step, not established by either isolated lab.

## Did / Blocked / Need
Did: reviewed source, verified pins and independently reproduced the focused suite; accepted bounded repair.
Blocked: no outstanding H04 blocker. Real candidate acceptance and app integration remain NOT RUN.
Need: a separately released bounded candidate test, not another harness rewrite. No Director design decision is requested by this review. No approval, release, closure, live custody receipt or allocation is created.
