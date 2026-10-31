# CONTRACT delta — colab readiness checker, repair 05.02

This delta is the evaluation rule for the repaired checker. It does not edit or replace `evidence/build05.01/CONTRACT.md`. That file remains the contract of the captured 05.01 submission. Schema names stay `colab-readiness-request/1` and `colab-readiness/1`. No request key was added.

Requests that already accounted for every entry, recorded final-reread exits of 0, and pinned a nonempty transported evidence root keep the same ready result. The three false-positive shapes below now finish as a complete report that is not ready.

## R-01 — Accounted entry points

Every `entry_points` path must equal at least one `dependencies` path. That row is the root record.

A dependency-free root is a supplied row for that path with empty `invokes` and empty `needed_by`. An entry with no such row is unaccounted. `runtime_dependencies_resolved` is false. An empty `dependencies` list does not resolve.

The report lists `facets.runtime.entries` as `{id, path, accounted}`. Unknown, withheld, conditional, and closure results stay as they were. The other facets stay independent.

## R-02 — Successful final reread

For `return-review`, `child_exit` and `wrapper_exit` are the exits of the final stage named `reviewed-reread`. The successful exit for that stage is 0.

A `passed` claim whose two exits are equal and are not 0 becomes `failed`. The report keeps those exits on `facets.smoke` as `child_exit` and `wrapper_exit`, with `final_stage` and `success_exit`. Failure text names the stage and the actual exits.

Differing integers stay `partial`, and `exit_layers_differ` stays true. The distinct-layer result is unchanged.

The initial awaiting-review read is not this pair of fields. A first read exit of 1 can stand beside a final reread exit of 0. This rule does not require every exit in a route log to be 0.

A passed claim needs command text that is not empty. `no-return` and `observation-failed` still cannot be passed.

The checker validates the supplied smoke object. It does not run the command and does not authenticate the record. No command runner is added.

## R-03 — Evidence root identity and nonempty coverage

Each known reference path must be a transport row, and the delivered bytes must equal that row's sha256 and length. A file that is merely present, or a transport row whose hash differs, does not resolve.

A required category is satisfied only when each of its refs resolves and those refs yield at least one verified member. Members are the matched rows of `artifact-manifest/1`, `prime-pack-sources/1`, `review-packet-manifest/1`, and `colab-readiness-references/1`. A nested known manifest contributes its child members. An empty `artifacts`, `sources`, `files`, or `items` list yields none.

`evidence_references_resolved` answers whether the root and its declared rows match. `minimum_evidence_satisfied` answers whether required categories received material. An empty transported manifest can resolve as a manifest and still leave minimum coverage false.

Not-applicable, with a reason and no refs, stays satisfied. The checker does not judge whether prose is relevant or true.

The report adds `members` on each evidence reference and each minimum category.

## Preinstalled requirements

`preinstalled-verified` stays `unknown`. This checker does not measure bytes outside the delivery, and it does not gain an environment resolver. Supplying the bytes, or declaring the feature not-applicable with a reason, is a different act from deleting a requirement to make the report ready.

## Later module records

`00.00.10.work/0316.dependencies` is the Director's direction for maintained module requirements and construction provenance. A later record can feed this checker by becoming the declared dependency rows, evidence refs, and conditions of one delivery. This checker remains that consumer. It does not become the registry, the index, or the resolver.

## What a passing report still does not establish

Truth, acceptance, approval, publication, import-graph completeness, independent proof of a shared component, or values for tokens, cost, and clocks. Surface authorization stays not-established. Ready is support for the declared method under these rules.
