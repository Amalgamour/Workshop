# CONTRACT — colab readiness checker, pass 01

Written before the checker. Schema names below are the contract. The checker verifies a declared delivery. It does not decide truth, execute a Colab, authorize work, or repair inputs.

## 1. Program

`python -B colab_readiness.py check --request ABS`

The request names a new output directory. The checker writes `readiness.json` and `READINESS.md` there.

| exit | meaning |
|---|---|
| 0 | The report is complete. `ready_for_declared_method` may still be false. |
| 2 | The request was refused, or a bound was crossed and a partial report was kept. |

Refusal before the output directory is created leaves that path absent. An existing output path is occupied: exit 2, and the checker does not modify it. There is no exit 1. The checker does not import or launch the delivery.

`READINESS.md` sections, in order: Transport, Runtime dependencies, Evidence references, Minimum evidence, Smoke, Ready for declared method, Limits.

## 2. Request `colab-readiness-request/1`

Exact keys: `schema`, `purpose`, `surface`, `delivery_root`, `output`, `transport`, `entry_points`, `dependencies`, `evidence`, `references`, `withholds`, `smoke`, `failure_policy`, `independent_checks`, `bounds`.

JSON is UTF-8. Duplicate keys are refused. Non-finite numbers are refused.

`purpose` exact keys: `statement`, `mode`, `question`, `role`, `method`, `finish_boundary`. `mode` is `return-review` or `read-only`.

`surface` exact keys: `kind`, `os`, `interpreter`, `network`, `install`, `secrets`, `read_roots`, `write_roots`. `network` and `install` are `denied`, `allowed`, or `unknown`. Roots are absolute local paths.

`delivery_root` and `output` are absolute local paths. The delivery root must be an existing plain directory. The output directory must not exist, and its parent must.

`transport` is a list of exact objects `{path, sha256, bytes}`. `path` is relative to `delivery_root`, uses `/`, and has no empty, `.`, or `..` segment, backslash, or drive prefix. `sha256` is 64 lowercase hex. `bytes` is a non-negative integer. Paths are unique.

`entry_points` is a non-empty list of exact objects `{id, path}`. Each path is one transport path. Ids are unique labels (`^[A-Za-z0-9][A-Za-z0-9._-]{0,63}$`).

`dependencies` is a list of exact objects:

`id`, `path`, `sha256`, `bytes`, `role`, `required`, `needed_by`, `invokes`, `supply`, `condition`, `withhold_reason`.

- `role`: `subject-runtime`, `reviewer-assistance`, `shared-subject-and-assistance`, `source-under-review`, `fixture`, `evaluator-only`.
- `required` is boolean.
- `needed_by` and `invokes` are lists of dependency ids.
- `supply`: `supplied`, `withheld`, `unavailable`, `preinstalled-verified`.
- `condition` is null or exact `{text, exercised}` with non-empty text and boolean `exercised`.
- `sha256` is 64 lowercase hex or null. `bytes` is a non-negative integer or null.
- `withhold_reason` is a string or null.

`evidence` has each of these categories once: `task-criteria`, `director-constraints`, `return-work-custody`, `contract-code`, `tests-evidence`, `source-index`, `capabilities`, `fallback`, `return-route`. Each item is exact `{category, applicability, reason, refs}`. `applicability` is `required` or `not-applicable`. `refs` is a list of reference ids. A required category has a non-empty reason and at least one ref. A not-applicable category has a non-empty reason and no refs.

`references` is a list of exact `{id, format, path, follow_nested}`. Ids are unique. `follow_nested` is boolean. `format` is one of `artifact-manifest/1`, `prime-pack-sources/1`, `review-packet-manifest/1`, `colab-readiness-references/1`. Any other format is unsupported. It is not success.

`withholds` is a list of exact `{path, reason}` with a non-empty reason.

`smoke` exact keys: `status`, `reason`, `command`, `child_exit`, `wrapper_exit`, `expected_state`, `observed_state`, `cutoff`, `in_flight`, `manual_fallback`, `label`, `page_sha256`, `receipt_sha256`, `pass_state_before`, `pass_state_after`, `custody`, `judgment_label`, `journal_operations`.

- `status`: `passed`, `failed`, `not-applicable`, `not-run`, `partial`.
- `label`: `synthetic`, `historical`, `none`.
- `command` is a string or null. The checker never executes it.
- `child_exit` and `wrapper_exit` are integers or null. They stay separate fields.
- `in_flight` and `journal_operations` are lists of strings.
- `manual_fallback` is boolean.
- `cutoff` is a string.
- Hash fields are 64 lowercase hex or null. State and custody fields are strings or null.

`failure_policy` exact keys: `declared`, `retain_first_failure`, `diagnostic`, `dependency_check`, `manual_fallback`. The first two are boolean. The last three are strings.

`independent_checks` is a list of exact `{id, text, status}`. `status` is `present`, `absent`, or `not-established`.

`bounds` exact keys: `max_files`, `max_file_bytes`, `max_total_bytes`. Each is an integer from 1 through 100000, 20000000, and 50000000 respectively.

## 3. Closure

Prime or the model declares entry points, dependency edges, and which dependencies are required. The checker does not scan imports.

The closure starts at dependencies whose path equals an entry-point path. It then follows `invokes`, and it includes a dependency whose `needed_by` names an id already in the closure. A cycle in `invokes` fails runtime resolution. A `required` dependency outside the closure fails runtime resolution.

For a dependency in the closure, or any dependency with `supply` `supplied`:

- `supplied` must name a transport path whose file matches `sha256` and `bytes`. Null hash or length is a null source binding and fails.
- `withheld` on a required dependency fails. The path must also appear in `withholds`. Optional withheld assistance does not fail.
- `unavailable` on a required dependency fails.
- `preinstalled-verified` is unknown. This checker does not measure bytes outside the delivery. Unknown blocks ready.
- A required condition with `exercised` false fails. A null condition is not an unexercised condition.

`shared-subject-and-assistance` is reported as a shared component. The report may still be mechanically ready. `independent_proof` remains `not-established`.

## 4. Evidence bytes

The checker hashes delivered files. It does not open a source repository and it does not regenerate a packet.

- `artifact-manifest/1`: `{schema, artifacts: [{path, sha256, bytes, ...}]}`. Paths are relative to the delivery root. Extra keys are not interpreted.
- `prime-pack-sources/1`: `{schema, sources: [{path, snapshot, sha256, bytes, ...}]}`. `snapshot` is relative to the manifest's directory. The source `path` is not opened.
- `review-packet-manifest/1`: `{schema, files: [{path, sha256, bytes}]}`. Paths are relative to the manifest's directory.
- `colab-readiness-references/1`: `{schema, items: [{path, sha256, bytes}]}`. Paths are relative to the delivery root.

The file's `schema` must equal the reference `format`. A known manifest that does not parse, or whose rows are incomplete, fails the reference. An unknown schema is `unsupported`, not success.

`follow_nested` opens a referenced file that is itself one of the four manifests, up to four manifest opens. A deeper manifest fails closed. A missing nested file fails `evidence_references_resolved` even when the parent row's own hash matches. Content that is not one of those manifests is hashed only.

## 5. Facets

`transport_valid` is true only when every transport row is a regular file, not a link, inside the delivery root, and equal to the declared hash and length, within bounds.

`runtime_dependencies_resolved` is `true`, `false`, or `unknown`.

`evidence_references_resolved` is `true`, `false`, or `unsupported`.

`minimum_evidence_satisfied` is true only when all nine categories are present once and each required category's refs resolve. That is coverage of the declared set. `semantic_sufficiency` is always `not-established`.

`smoke_result` is the checked status, not a new execution.

For `read-only`, smoke must be `not-applicable` with a non-empty reason, null exits, null hashes, empty `in_flight`, empty `journal_operations`, `manual_fallback` false, and `label` `none`. The checker then reports `not-applicable`.

For `return-review`, `not-run` stays `not-run`. `not-applicable` is a failed smoke. `failed` and `partial` stay themselves.

A request status of `passed` is accepted only when all of these hold:

- `label` is `synthetic` or `historical`, and `judgment_label` equals that label;
- `page_sha256` and `receipt_sha256` are 64 hex;
- `pass_state_before` is `awaiting-review`;
- `pass_state_after` is `reviewed`;
- `custody` is `complete`;
- `expected_state` equals `observed_state`;
- `observed_state` is not `no-return` and not `observation-failed`;
- `in_flight` is empty;
- `manual_fallback` is false;
- `child_exit` is an integer;
- `wrapper_exit` is an integer;
- `cutoff` is non-empty;
- `journal_operations` contains `read`, then later `record`, then later `read`;
- `reason` is non-empty;
- `command` is a string. It is not run.

If `manual_fallback` is true, the smoke cannot be `passed`. If the observed state is `no-return` or `observation-failed`, a passed claim is `failed` even when `expected_state` was set to the same unusable state. If the two exits differ, `exit_layers_differ` is true and the smoke result is `partial`. If either exit is null on a passed claim, the smoke result is `failed`.

`ready_for_declared_method` is true only when the assembly is complete and all of these hold:

- `transport_valid` is true;
- `runtime_dependencies_resolved` is true;
- `evidence_references_resolved` is true;
- `minimum_evidence_satisfied` is true;
- smoke is `passed`, or the mode is `read-only` and smoke is `not-applicable`;
- `failure_policy.declared` and `retain_first_failure` are true, and `diagnostic`, `dependency_check`, and `manual_fallback` are non-empty;
- `network` and `install` are `denied`;
- `exit_layers_differ` is false.

`surface_authorization` is always `not-established`. Denied network and install do not become permission. `allowed` or `unknown` blocks ready. Ready is not semantic correctness, acceptance, or approval.

## 6. Report `colab-readiness/1`

Exact top-level keys: `schema`, `assembly`, `mode`, `transport_valid`, `runtime_dependencies_resolved`, `evidence_references_resolved`, `minimum_evidence_satisfied`, `smoke_result`, `ready_for_declared_method`, `semantic_sufficiency`, `independent_proof`, `exit_layers_differ`, `surface_authorization`, `shared_component`, `facets`, `limits`, `problems`.

`assembly` is `complete` or `partial`. `independent_proof` is `not-established`. `semantic_sufficiency` is `not-established`. `facets` records the rows and problems for the six sections. `facets.smoke.command_executed` is false.

An empty `independent_checks` list adds a limit. A non-empty list also leaves proof not established. A shared component adds a limit that its own output is not proof.

Crossing `max_files`, `max_file_bytes`, or `max_total_bytes` after the output directory exists writes a partial report and returns 2. The partial is kept.

## 7. Inventory `colab-readiness-inventory/1`

The lab inventory is a source list for a future replay revision. The checker does not treat it as a delivery and does not create that revision. It separates `subject-runtime` from `reviewer-assistance`, records the shared review-packet component, and copies nested specimen provenance from the frozen nested-manifest check. Unsupported or missing references stay stated.

## 8. What a passing report does not establish

It does not establish that the work is true, that Prime accepts it, that the Director released anything beyond the named slice, that an import graph is complete, that a shared component was independently proved, or that unknown tokens, costs, or clocks have values.
