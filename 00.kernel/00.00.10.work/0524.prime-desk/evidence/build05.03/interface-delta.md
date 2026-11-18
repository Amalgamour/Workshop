# Interface delta — pass02 to pass03

The view and packet commands keep the same connector names. The lab directory changes:

```text
python -B labs/prime-desk-pass03/prime_desk.py view --request ABS [--json]
python -B labs/prime-desk-pass03/prime_desk.py packet --request ABS --work-id ID [--json]
```

`request_index.py` stays a helper. It is not a third desk command and it does not call `view`.

Schema versions:

| record | pass02 | pass03 |
| --- | --- | --- |
| request | `prime-desk-request/2` | unchanged |
| view | `prime-desk-view/2` | `prime-desk-view/3` |
| packet | `prime-desk-packet/2` | `prime-desk-packet/3` |
| catalog | `prime-desk-catalog/2` | unchanged |
| worker evidence | `prime-desk-worker-evidence/1` | unchanged |
| selector file | `prime-desk-selector/1` | unchanged, still a hint |

Top-level result keys are unchanged. `packet` is null on `view`. The fingerprint still excludes observation time.

`selected.review_home` is removed. `selected.route` replaces it. Pass02's N1NN path without a `.return.md` tail is not a review destination in this output.

`route` carries `band`, `source_kind`, `source_path`, `review`, `return_line`, and `limit`. `review` and `return_line` each carry `path`, `file`, and `judgment` or `custody`. File state is one of `matched`, `missing`, `stale`, `changed`, or `undeclared`. Judgment stays `unknown`. A matched return has custody `unknown`. A declared missing return has custody `pending`. Undeclared means the derived path was not in the request. The tool does not search for it and does not create it.

Executable sources:

- N5NN `05.PP.md`. Review path is that source page. Return path is `{prefix}1{NN}.subject/05.PP.return.md`.
- N7NN `05.PP.pack.md`. Return path is `05.PP.return.md` and review path is `06.PP.review.md` on the same page. No N1NN path is allocated.

The band is the page's second digit. The first digit is kept. `1599` and `1705` are ordinary pages under that rule. A `06.PP.review.md` path, a `.return.md` path, and a band-1 `05.PP.md` path are not executable sources. The tool names the kind and does not infer another page.

`packet.review_home` is removed. A packet carries `relation`, `canonical_id`, `work_id`, and `route`. Relation `current` expands the canonical id. Relation `inspection` expands another registered executable source and leaves `selected` on the canonical assignment. That inspection adds a gap, so the exit is not 0. A return, a review, or an unknown kind is not expanded.

Pass02 files and the 14 pass02 tests stay as they were. Those tests still expect the old review-home field. This note is the version map. It is not an instruction to change Claude's 0705 checker, `expected.json`, or those historical results.
