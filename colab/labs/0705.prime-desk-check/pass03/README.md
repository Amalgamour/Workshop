# 0705.prime-desk-check / pass03 — pinned baseline connected to the independent checker (lab)

Contract: `00.kernel/00.00.10.work/0705.prime-desk-check/evidence/return05.03/CONTRACT.md`. How to use: `.../return05.03/PRIME-USE.md`.

| File | What |
|---|---|
| `run_baseline.py` | pins the candidate, its reader and pass02 from pack05.03 snapshots; builds fixtures; prepares requests; runs the candidate; keeps raw output; adapts; checks |
| `adapter.py` | `prepare_request` (SYNTHETIC request artifacts; shadow selector rule R1) and `normalize` (raw JSON → `desk-observation/1`; verifies the raw, candidate and request hashes) |
| `mapping.json` | the exact field mapping and declared transformations; the unmapped fields with their reasons |
| `probe_c05.py` | SUPPLEMENTARY probe: C05 on a fixture-completed copy (pass02 FX-01); not part of the oracle run |
| `tests/test_adapter.py` | 9 adapter self-tests with synthetic raw outputs |

**Result** (evidence in `return05.03`): the candidate is `not-passed`.
- PD-01 (shadow selection) is exposed.
- PD-03 (whole-file Director quote) is exposed by the probe.
- PD-04 (crash on a malformed canonical record) is new.

pass01 and pass02 are unchanged. No successor was read or run.
