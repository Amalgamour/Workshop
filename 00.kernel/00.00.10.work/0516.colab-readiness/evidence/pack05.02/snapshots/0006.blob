# PRIME-USE — colab readiness checker, pass 01

Check one declared delivery. The exact request object is CONTRACT.md section 2.

```text
python -B colab_readiness.py check --request ABS
```

Run that from `labs/colab-readiness-pass01`, or pass the script path. The request names an existing delivery directory and a new output directory. A complete run writes `readiness.json` and `READINESS.md` there. Stdout is one line:

```text
colab-readiness assembly=… ready=… transport=… runtime=… evidence=… minimum=… smoke=…
```

Exit 0 means the report is complete. `ready=true` on that line is only `ready_for_declared_method`. Exit 2 means the request was refused, or a bound was crossed and a partial report was kept. There is no exit 1.

The smallest request is `colab-readiness-request/1` with one transport row, one entry point on that path, one subject-runtime dependency for that path, all nine evidence categories, one known reference, an empty withhold list, a declared failure policy, empty independent checks, and bounds. For `read-only`, smoke is `not-applicable`, label `none`, exits and hashes null, and both operation lists empty. For `return-review`, paste the recorded smoke object. The checker does not run its `command` string.

## Facets

Each facet is its own field. A true neighbor does not fill a false one.

| facet | true meaning |
|---|---|
| `transport_valid` | Every declared path is a regular file inside the delivery, and the bytes match. |
| `runtime_dependencies_resolved` | The declared closure is present, supplied bytes match transport, and required conditions were exercised. `unknown` means a preinstalled dependency was not measured. |
| `evidence_references_resolved` | Known manifests and their followed rows resolve to delivered bytes. `unsupported` means the format is outside the four known schemas. |
| `minimum_evidence_satisfied` | All nine categories are present once, and each required category's refs resolve. |
| `smoke_result` | The recorded smoke object passed the contract rules, or a read-only method is `not-applicable` with a reason. |
| `ready_for_declared_method` | Assembly is complete and the required checks above passed, with the failure policy complete, network and install `denied`, and the two exit fields not in conflict. |

`semantic_sufficiency` stays `not-established`. `independent_proof` stays `not-established`. `surface_authorization` stays `not-established`. `facets.smoke.command_executed` stays false.

## Actionable failures

Read stderr on exit 2. If the output directory was not created, the request was refused and nothing was written. `output exists` means the directory was already there and was left unchanged.

| what you see | what to do |
|---|---|
| transport false | The delivered file is missing, linked, outside the root, or its hash differs. Correct the delivery or the declared hash. A file in the source repo is not the delivery. |
| runtime false | A required dependency is outside the entry closure, has a null hash, does not match transport, is withheld or unavailable, or its required condition was not exercised. An `invokes` cycle fails the same way. |
| runtime unknown | `preinstalled-verified` was declared. This checker did not measure bytes outside the delivery. Supply the bytes or drop the dependency from the required closure. |
| evidence false | A known manifest row does not match, or a nested file named by that manifest is missing. A matching parent row does not cover the missing nested file. |
| evidence unsupported | The format is not one of `artifact-manifest/1`, `prime-pack-sources/1`, `review-packet-manifest/1`, `colab-readiness-references/1`. Name a known format or accept the unsupported result. It is not success. |
| minimum false | A required category's ref did not resolve. Shape alone is not coverage. |
| exit 2, missing category | One of the nine categories is absent or duplicated. That is a request refusal, not a finished report. |
| smoke `not-run` | On `return-review`, ready stays false. Record the route, then check again. |
| smoke failed on `no-return` or `observation-failed` | The route did not reach a usable state. Matching `expected_state` to that state does not make it a pass. |
| smoke `partial` and `exit_layers_differ` true | `child_exit` and `wrapper_exit` are different integers. Report both. Do not collapse them. |
| ready false while the five checks are true | The failure policy is incomplete, network or install is not `denied`, or the exit layers differ. |
| partial report, exit 2 | A file count or byte bound was crossed after the directory existed. Keep the partial. |
| manual fallback | A labelled manual fallback cannot be `passed`. |

Preserve the first failure. One read-only diagnostic and one named dependency check are the default. Do not repair the delivery inside the checker, and do not switch tools after a refusal.

## Declared coverage

The checker covers the request in CONTRACT.md: transport bytes, declared dependency closure, four manifest formats, nine evidence categories, a recorded smoke object, and the ready rule. Nested manifests open only when their schema is one of those four, and only four manifests deep. Other JSON is hashed content.

The suite of record is `labs/colab-readiness-pass01/tests/test_colab_readiness.py`: 28 tests, 1 skipped, 0 failed. The skip is `test_linked_path_is_refused`, because this host cannot create a file symlink (WinError 1314). Negative cases cover a missing adapter, a missing support file, changed pinned bytes, a missing nested snapshot whose parent row still matches, a null binding, an observation failure, a no-return, a missing category, an unsupported format, an unsafe path, duplicate and malformed JSON, an occupied output, a retained partial, a required withhold, an unknown preinstall, allowed network, manual fallback, distinct exit layers, a missing failure policy, a cycle, an unexercised condition, and a shared component.

One positive fixture copied snapshots 0009–0015 and the committed parser blob into a disposable tree and ran read, a SYNTHETIC judgment, record, and a reviewed re-read. The official result is `sample-readiness.json`. Judgment text is labelled SYNTHETIC. The checker validated that recorded object. It did not launch the tools. The route log beside the sample keeps the member, the receipt, both pass states, and the separate exits.

`inventories/replay-revision-sources.json` is the source list for a future replay revision. The checker does not treat that file as a delivery, and this slice does not build the revision.

## What this verifier leaves unestablished

Truth of the work. Prime's acceptance. Approval. Publication. A Director release beyond the named slice. Completeness of an import graph. Independent proof of a shared component. Values for tokens, cost, or clocks. Permission to use the network or to install software. Semantic sufficiency of a file that is merely present.

A shared component may still be mechanically ready. Its own output is not proof. An empty independent-check list is a limit. A non-empty list also leaves proof unestablished.

The sample's ready result is the frozen accepted interface in a disposable tree. It is not a correction of the live prime-cycle files, and those files were not read.
