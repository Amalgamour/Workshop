# Dependency map (0707/05.19)
**Frozen bytes:** pack05.19 `source-manifest.json` (405 rows). PENDING = not frozen yet; never guessed.

## Executed modules (the combined candidate)
| Path | sha256 | Role | Canonical-root dependency |
|---|---|---|---|
| app/librarian.py | c3a5be3b… now; combined PENDING | the single selection point | `code_root` = its own parent |
| app/review_loop_tools_v8.py, review-loop-v8.json | 0335da32…, 92a718d3… (staged) | predecessor; becomes a pinned predecessor of vN | none (uses code_root) |
| app/review_loop_tools_vN.py + JSON | PENDING | the combined door | none |
| labs/workbook-review-pass06/workbook.py (W) | PENDING | overlay: G + K + F | REPO guard (as pass04) |
| labs/workbook-review-pass05/workbook.py (G) | PENDING (Grok-2) | strict N7 grammar | REPO hard-coded |
| labs/workbook-review-pass04/workbook.py | b7b8776c… | **superseded by G, kept; it is evidence of 0522/05.14** | REPO + guard |
| labs/workbook-review-pass03 / 02 / 01 | 9e66d7e4… / 6ce4a5ff… / 60e040fa… | the base chain; **02 and 01 are imported at import time from the hard-coded REPO** | yes |
| K: the prime_review successor | PENDING (Grok-1) | record validation | (pass02 has no REPO; check K) |
| labs/prime-review-pass02/prime_review.py | 80836a13… | current validator, `MAX_LIST = 24` | — |
| F: labs/n7-first-review-pass01/review_loop.py, prime_cycle.py | fb0e1e32…, b664c2c9… | to be re-staged under versioned shared names | ROOT hard-coded; their fixture-root guards refuse books inside it |
| labs/review-construction-pass04/construct.py, pass02 | 6d541d42…, b82413ff… | render and bind | ROOT |
| labs/return-access-pass01/return_access.py | 501d40d7… | custody lookup | ROOT |
| R′: app/review_report_tools_v4.py + JSON | PENDING | reporter connector, pinning the combined dispatcher | derives its root from its own path; fixed live helper root (06.13) |
| labs/review-report-hardening-pass01/report.py | 27e513f4… | the R runtime; observation to be re-cut on W | pass03 helper |

## Forms and schemas
- `workbook-review-form/1`: pass03's form (`labs/workbook-review-pass03/forms/…`, 4b8cf0e8…), unchanged.
- `review-loop-pins/6` (v8) → **/7 (vN, proposed)**.
- `review-report-command/2` (v2 and v3 both use /2, as measured) → **a new schema for v4 (proposed)**.
- `review-write-token/1`, including F's `absent-create` state.
- `prime-review-record/1` (K may version it; PENDING).
- `review-report/3`.

## Source evidence (replay inputs)
- **N5:** 0522/05.13 (29 rows; declares app files), 0512/05.06 (14), 0512/05.09 (36 rows, 29 sources), 0522/05.14 (28 rows, 20 sources; declares the staged v8 files).
- **N7:** 0707/05.15 (26 rows, about 20 sources), 0707/05.17 (33 rows, 26 sources).
- **Each must be built from pack snapshots, plus manifest rows verified by hash** (`labs/loop-convergence-design-pass01/lcd.py`).

## Author adapters (lab only; never production)
- **05.18 `adapter/workbook-pass04.lab.py`:** one line, REPO = own root.
  - **Collides with 0522/05.14 evidence** (inv1 C5): a root that needs the staged bytes as evidence cannot hold the adapter.
  - **The builder must run W at the canonical root,** or use a root whose adapter path is NOT a declared artifact path.
- **`n7compat2 --repo-root`** (the faithful pass03 baseline).
- **The 05.18 `cases/` adapter** (the 12 + 17 historical cases).

## Historical context only
- 0706/06.02.review (reporter B-findings);
- 0420/06.42 (the Director decision and the plan);
- 0416/01.003, 0420/01;
- design05.15–05.18.

## Where an isolated fixture diverges from production
1. **The hard-coded ROOT/REPO in every helper.** A copy root uses live helper code (hash-equal) and its guards treat books outside live as fixtures.
   - **The cycle path is not exercised without custody;** inv2 X4 shows `cycle.called` is false.
2. **The lab adapter at a path that is a declared artifact** (inv1 C5).
3. **intake_id includes the book path.** Rows and cuts do not.
4. **Custody:** copy books have no N1 descriptor, so they are always preliminary, as on the live Colab route.
