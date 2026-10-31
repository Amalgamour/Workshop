# PRIME-USE — colab readiness repair, 05.02

The command is unchanged:

```text
python -B colab_readiness.py check --request ABS
```

Exit 0 is a complete report. `ready=true` is only `ready_for_declared_method`. Exit 2 is a refusal or a kept partial. The request schema is still `colab-readiness-request/1`. The 05.02 delta in CONTRACT.md is the evaluation rule. The 05.01 contract remains the record of the captured original.

The checker validates a supplied smoke record. It does not run the command and does not authenticate that record.

## What changed

An entry point is accounted only when a dependency row names its path. A supplied row with no edges is a dependency-free root. An entry with no row leaves runtime unresolved. Empty dependencies do not resolve.

For a return-review, `child_exit` and `wrapper_exit` are the reviewed reread. The successful exit is 0. Equal exits of 2 are a failed final reread, and the report keeps those numbers. Differing exits stay partial. A first read exit of 1 is not this pair. Blank command text cannot be passed.

A known evidence root must be the transported file, with the same sha256 and length. A required category needs at least one verified member from its refs. An empty manifest resolves no material. Not-applicable with a reason stays valid. The checker does not judge prose.

## Facets

Each facet stays its own field.

| facet | meaning |
|---|---|
| `transport_valid` | Every transport row is a regular file inside the delivery, and the bytes match. |
| `runtime_dependencies_resolved` | Every entry has a dependency record, and the declared closure matches the transported bytes. `unknown` means a preinstalled dependency was not measured. |
| `evidence_references_resolved` | Known roots are the transported files, and their declared rows match. `unsupported` is not success. |
| `minimum_evidence_satisfied` | Required categories resolve at least one verified member. |
| `smoke_result` | The supplied record passed the final-stage rule, or a read-only method is `not-applicable`. |
| `ready_for_declared_method` | The required checks passed, the failure policy is complete, network and install are `denied`, and the exit layers do not conflict. |

`semantic_sufficiency`, `independent_proof`, and `surface_authorization` stay `not-established`.

## Preinstalled requirements

A `preinstalled-verified` dependency stays `unknown`. This checker has no environment resolver. Supply the bytes in the delivery, or declare that feature not-applicable with a reason. Deleting a real requirement is not a way to make the report ready.

## Later module records

`00.00.10.work/0316.dependencies` is where maintained module requirements and workflow provenance are being recorded. A later module record can feed this checker: its runtime relationships become dependency rows, its evidence and task relationships become the nine categories and their refs, and its conditions become `condition` objects. Compute then checks that declared set. This lab does not build the registry, the index, or a second resolver.

## What stays unestablished

Truth, acceptance, approval, publication, a complete import graph, independent proof of a shared component, and any value for tokens, cost, or clocks. The repaired ready result is still only support for the declared method.
