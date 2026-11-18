# Failure table — return access and guarded handoff

Schema: `return-access-handoff-failure/0509`
Date: 2026-11-02. Written before the successors.

A guard refusal on a declared book prints `writer_started: false`, `sequential_allocation: not-used`, and `result refused`. Exit code 2. The book bytes stay as they were. A handoff over that refusal reports attention, writes `clerk-capture-handoff-failure/1` when the log is absent, and retains the intent. It does not print `result ok`.

A guard mismatch prints `launched: false`, `writer_started: false`, and `result refused` before any tool subprocess. Exit code 2.

| Case | Where it refuses | Writer or launch |
| --- | --- | --- |
| Pass04, pass03, pass02, pass01, placement, or reader pin fails | return-access, before load | not loaded |
| Guard, sealed handoff, clerk, capture, or inspect pin fails | new handoff or its facade, before launch | not launched |
| Selected guard bytes differ from the reviewed pin | new handoff, before launch | not launched |
| Layout absent on reserve or capture through the guard | guard delegates | historical writer, with the absent-protection sentence |
| Layout absent on reserve or capture through the return-lines facade | facade, before pass04 | not launched |
| Accepted line-pass layout, legacy reserve or capture | guard | not loaded |
| Malformed, linked, duplicate-key, or conflicting layout | facade and guard | not loaded |
| Missing authorization file on preflight | pass04 | no layout written |
| Fixture operations omit the command | pass04 | no layout written for a refused init |
| Fixture aimed at the live book | pass04 predecessor validator | live tree unchanged |
| Repeated or conflicting line submission | pass04 | existing return bytes stay |
| Changed return bytes presented to verify | return-access verify | the tool does not rewrite the file |
| Handoff artifact bytes differ from the binding | sealed handoff checks, through the new selector | capture does not complete |
| Publish interrupted, then resumed | pass04 on a disposable copy | partial state stays until resume |
| `adopt` and its resume or rollback names | pass04 | no layout written by that command |
| Second handoff perform after a retained failure log | sealed handoff | existing log bytes stay |

An undeclared doorless reserve is a scoped legacy success plus the missing-protection sentence. It is not a declared-book success. A reader `complete` state is not task association and is not approval. Exit 0 from a suite is not Prime review and is not app activation.
