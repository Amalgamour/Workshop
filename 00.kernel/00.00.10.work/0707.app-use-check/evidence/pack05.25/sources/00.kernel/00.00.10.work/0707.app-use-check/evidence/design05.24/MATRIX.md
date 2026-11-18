# MATRIX — requirement → equipment → evidence (0707/05.24)

## Identity contract (0420/06.57) → adapter control
| Requirement | Control | Result |
|---|---|---|
| Declared entry, workbook and open entry; no `review_loop_tools_vN.py` inference | identity.resolve v3; pass03 `selected_workbook`/CTX-1 (r03, r04) | pass |
| Untrusted paths: relative, containment, types, duplicates, presence, hash and length, supported schema | u06–u14, u16, u17, u20 | pass (26/26) |
| Wrong or absent entry | u06, u07 | refused |
| A workbook the dispatcher does not use | u02, u03 (dummy), r08 (CLI), old-combined C | DECOY → refused |
| False or duplicate identity | u09, u10, u13 | refused |
| External path | u11 (`..`, `/`, `C:`, `\`, `.`, `//`) | refused |
| A copied dependency that is not used | u05 | flagged (not executed) |
| An open entry that is not executable on a new root | u04; old-combined C (`not at its canonical root`, control exit 2) | recorded and refused |
| A pending candidate | u15, r06 | refused (fbt) / all-blocked (pass03) |
| Legacy, only for the two baselines | u21, u22, u24, r05 | labelled legacy-discovery; others refused |
| Prime's old combined v2 identity | u23, r09, demo A | refused: legacy limit, undeclared open entry, no workbook_entry |

## Preservation (#03)
| Item | Evidence |
|---|---|
| Freshness: 34 cases / 32 required; F1, F1b, E1, E2 and C4 still required | u25 (pinned pass01 run.py and judges.py, pack05.24 hashes) |
| Convergence: 40 cases / 37 required, same ids/requirements/needs | r01; only CTX-1 and RC-1 sources differ (r02) |
| Old harness, freshness labs and inputs byte-identical | u26; reconstruct: 53 rows, 0 drift |
| Old unit suites still pass | test_judges 30, test_verdict 40, test_shapes 24, test_callbacks 29 |
| Verdicts unchanged through the new adapters | reconcile24: 29 rows per baseline (10 freshness + 19 convergence), 0 differences |

## Reporter obligations (0522/06.38) → equipment judge (proposed RP-3; NOT in the required registry)
| Obligation | Scripted check |
|---|---|
| unsupported authority or accepted (in the core response, or in the report) | r11, r12 |
| absent or wrongly typed envelope fields | r13, r16, r20 |
| mismatched or missing read/recover ids | r14 |
| disagreeing stale and exit, or recover vs read | r15 |
| current vs historical judgment separation | r17 |
| N7 / N5 custody | r18 |
| refusing everything is not a current report | r19 |
