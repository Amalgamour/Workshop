# Failure cases (0707/05.13) — specified behavior, NOT RUN against any target

| # | Situation | Compute (specified) | Intelligence | Continues | Waits |
|---|---|---|---|---|---|
| F1 | **block absent** (old pack, like 0522/05.13; example c1) | report `absent`; all six fields unknown; **no inference from Goal/Scope headings** | may write a gloss in the review; it cannot create authority | preliminary record, publish, recover | complete, finished, release |
| F2 | **cited heading missing, or not exactly once** | refuse the binding for that field with the count and the path; other fields bind | names a correct cut, or leaves the field unknown | the other fields | the dependent acts |
| F3 | **a bound cut changed after intake** (example c2) | `stale`; keep the old binding and sha; reconciliation request; **no rebinding** | proposes the cut to rebind (task) or flags a conflict (Director record) | unrelated acts | acts depending on that field |
| F4 | **scope and a decision disagree** (example c3) | `conflict`; both cuts kept | explains the conflict; **does not choose a side** | work inside both cuts | the Director's judgment; the conflicting act |
| F5 | **verbatim and interpretation are the same cut** | refuse that decision binding | supplies distinct cuts | — | answers from that decision |
| F6 | **the answers cut does not resolve** | refuse that decision binding | names the question or proposal | — | that hold |
| F7 | **"yes" or "Ok" with no bound proposal** | no binding is possible, so recorded_decisions is unknown | finds the record and proposal, or leaves it unknown | — | anything needing that decision |
| F8 | **a gloss claims authority** ("Director approves X") | stored as interpretation; **never read as authority** | — | — | — |
| F9 | **a newer pack revision exists** | the old binding stays; a new intake needs a new binding | selects explicitly | the old work as bound | — |
| F10 | **wrong shape** (the block is not valid JSON, or an unknown field) | mechanical refusal with field and help; **the idea is not rejected** | corrects the block | — | binding |
