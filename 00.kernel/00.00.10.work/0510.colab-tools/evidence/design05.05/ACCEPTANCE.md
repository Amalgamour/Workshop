# ACCEPTANCE (proposed) — reserved two-pass checker and stage order
date: 2026-11-01 · who: claude-opus-5-5 (Claude) · state: plan.

- **Group P** ran here on the rule prototype with synthetic data: 31 of 31 pass. Raw: `probes/P2-rule-tests.run2.*`; first run 30 of 30 before the authority check was added, `run1.*`.
- **Groups A–D** are for the builder, on disposable fixtures through the real tools.

## P — rule prototype (ran; `test_reserved_rules.py`)
| Case (pack wording) | Test | Expected and observed |
|---|---|---|
| absent trigger | `test_absent_trigger` | `no-trigger` |
| mismatched target cut | `test_mismatched_cut`, `test_changed_target_is_new_comparison` | `cut-mismatch` / `target-changed` |
| hashes not supplied → launch unready | `test_target_hash_not_supplied_is_unready` | `launch-unready` |
| missing first findings | `test_missing_first_findings` | `missing-reserved-findings` |
| attempted replacement (of the first return bytes) | `test_replaced_first_return_bytes` | `first-not-sealed` |
| context accidentally bundled into the first packet | `test_context_bundled_into_first_packet`, `test_context_bytes_under_another_name` | `context-in-first-packet` (path, and bytes under another name) |
| different environment | `test_different_environment_is_recorded` | recorded `["os"]`, not refused |
| unknown model | `test_unknown_model_is_kept_unknown` | stays `unknown`; "declared facts only" |
| same-model fresh session | `test_same_model_fresh_session_is_valid_and_disclosed` | valid; `same_family_declared: true` |
| familiar session claiming cold | `test_continuing_session_cannot_be_independent` | `not-fresh` |
| unknown freshness | `test_unknown_session_is_labelled_not_refused` | `independent-freshness-unknown` |
| requirements omitted to manufacture failures | `test_requirement_omitted_to_manufacture_failure` | `requirement-missing` |
| authority limits omitted | `test_authority_limits_must_travel` | `authority-missing` |
| a withhold not declared to the reviewer | `test_withhold_not_declared_to_reviewer` | `withhold-undeclared` |
| informed packet built before sealing | `test_informed_packet_lacks_sealed_first_return`, `test_first_return_not_captured` | `order` / `first-not-sealed` |
| stage order | `test_informed_before_independent` | `stage-order` |
| ordinary compatibility | `test_ordinary_has_no_descriptor` | `ordinary` |
| undispositioned / invented / reasonless / duplicate block / duplicate key | Reconcile tests | `incomplete` / `unknown-finding` / `reason` / `duplicate-…` / `json` |

## A — ordinary compatibility (builder; real tools)
1. The existing v2 real package (digest 42734b85…): the producer `verify`, `handoff_check check` and workflow `attach` results are byte-identical before and after slice 1 (no existing file changed).
2. `reserved_check launch` on that package → `ordinary`, exit 0, nothing written.
3. The v2 producer suite and the handoff_check suite are run once (unchanged files), not as a broad sweep.

## B — real two-pass on a disposable book and repository
These need a disposable Git repository for the descriptors. That needs Prime's permission, because it is a Git write outside the project.
1. Prepare the 05.01 package with a descriptor → `launch` ready → synthetic return with a block → capture → place → review `request-next`.
2. Prepare 05.02 with the first return and the builder context → `stage` ready → synthetic second return → capture → `reconcile --record` → `reconciled-as-declared`. The record file is created exclusively.
3. `reconcile --record` again with identical inputs → replay, no write. With a changed second return member → refused; the existing record is kept.

## C — existing protections re-tested in the two-pass flow (no new code)
1. `place-return` a different member for 05.01 → `occupied different content`.
2. Edit the placed `05.01.return.md` → capture verify / `hash conflict`.
3. `record-review` 06.01 with `finish` and an unresolved finding → `unresolved findings`.

## D — checker robustness
1. A tampered package (any HC01-style field) → handoff_check `mismatch` → the checker refuses `package-unverified`, with no trusted claims used.
2. The descriptor path is present twice, or with role `target` → `descriptor`.
3. A non-strict JSON descriptor or block (BOM, duplicate key, NaN) → `json`, no traceback.
4. The inspector reports `reserved` or the wrong origin → `first-not-sealed`.
5. A pinned tool hash mismatch → refusal before launch.

**Every case asserts the exact code and that nothing was written outside `--record`.**
