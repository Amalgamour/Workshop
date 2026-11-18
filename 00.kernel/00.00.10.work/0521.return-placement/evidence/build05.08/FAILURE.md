# Failure table — guarded legacy writer

Schema: `return-capture-guard-failure/0508`
Date: 2026-11-02. Written before the successor.

A refusal prints `writer_started: false`, `sequential_allocation: not-used`, and `result refused`. It does not print `result reserved`, `result captured`, or `result complete`. Exit code 2. The book bytes stay as they were.

| Case | Check | State | Writer |
| --- | --- | --- | --- |
| Capture helper hash, length, link, or link-count fails | `pin` | refused | not loaded |
| Layout-rules hash, length, link, or link-count fails | `pin` | refused | not loaded |
| Layout absent, reserve or capture | historical result, plus line-pass protection absent | historical | loaded |
| Accepted line-pass layout, new reserve | `return-line-layout/1` | refused | not loaded |
| Accepted layout, repeated reserve of an existing legacy member | `return-line-layout/1` | refused | not loaded |
| Accepted layout, capture of a pre-reserved unfinished member | `return-line-layout/1` | refused | not loaded |
| Malformed layout | `return-line-layout/1` | attention | not loaded |
| Linked layout | `return-line-layout/1` | attention | not loaded |
| Conflicting layout bytes | `return-line-layout/1` | attention | not loaded |
| Verify of a completed legacy member after a later declaration | historical verify text | historical | loaded for verify |
| Inspect of that member | `return-capture-inspection/1` through `return_inspect.py` | historical | inspector only |

The correction on a declared book tells the caller to use the line-pass route. The correction on a bad layout says sequential allocation was not used. Neither correction invents a receipt.

Retry evidence lives outside the book. A second refusal does not become a reservation. The handoff failure log, once written by the selected caller, stays in place for a later attempt.
