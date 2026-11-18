# First-use rehearsal package: 0521.return-placement/05.03

- `catalog.json`: 12 explicitly pinned sources from pack05.02, each with its role. This is an index, not an authority.
- `expected-facts.json`: what the overview and packet must recover, with the source of each fact, and what is forbidden.

Selecting this packet does not change the primary work. The copied selector still names 0522.review-construction/05.04.

| Step | What | Runs now? |
|---|---|---|
| 1 | Build a disposable copy: copy the 12 catalogued snapshot bytes from pack05.02 into a new external directory, the same way `build_fixture.py` does. Check every sha256. | **Yes** (lab operation). No live file is touched. |
| 2 | Collect candidate outputs: run the reviewed desk tool's overview, then its packet for `0521.return-placement/05.03`, against that copy. Save the raw outputs. | **No: pending.** It needs the reviewed 0524 tool and an exact invocation, which is not frozen. |
| 3 | Map the raw outputs to `desk-observation/1` with a declared adapter, recording its id, sha256 and unmapped paths. | **No: pending.** The adapter is NOT CONNECTED. |
| 4 | Check: compare against `expected-facts.json`. This is a manual comparison for now. The lab `check.py` covers the C-cases, not this packet. | Partially: the manual reading only, after step 2. |
| 5 | Manual review: Prime answers M-01…M-06 in `manual-checklist.json` for this packet, with `by` and `date`. | **No: pending** until step 2. |
| 6 | Retain everything: raw outputs, the mapped observation, check reports and manual answers, in a new evidence folder. Nothing is overwritten. | After steps 2–5. |
| 7 | Repeat steps 2–4 in a new process and compare the identity fields. | **No: pending.** This would be desk restart. The lab's own `harness.py` only shows harness restart. |

**Manual assembly still needed:**
- the exact candidate request or invocation for this catalog;
- the adapter;
- placing the rehearsal evidence folder (Prime decides where).

**Not implied:**
- No live review or approval.
- No source edit.
- No status store.
- No completion of 0420.
