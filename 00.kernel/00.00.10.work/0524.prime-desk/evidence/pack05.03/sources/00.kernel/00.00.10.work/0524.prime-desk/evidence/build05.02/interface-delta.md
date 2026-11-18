# Interface delta — pass01 to pass02

The view and packet commands keep the same connector names:

```text
python -B labs/prime-desk-pass02/prime_desk.py view --request ABS [--json]
python -B labs/prime-desk-pass02/prime_desk.py packet --request ABS --work-id ID [--json]
```

`request_index.py` is an added helper. It is not a third desk command and it does not call `view`.

Schema versions:

| record | pass01 | pass02 |
| --- | --- | --- |
| request | `prime-desk-request/1` | `prime-desk-request/2` |
| view | `prime-desk-view/1` | `prime-desk-view/2` |
| packet | `prime-desk-packet/1` | `prime-desk-packet/2` |
| catalog | `prime-desk-catalog/1` | `prime-desk-catalog/2` |
| worker evidence | `prime-desk-worker-evidence/1` | unchanged |
| selector file | `prime-desk-selector/1` | same file shape, authority removed |

Request v2 replaces top-level `selector` with `workspace`, `assignment`, `legacy_selector`, `coverage`, and `attribution`. `coverage` must be the string `declared-paths`. Each reference and each attribution span has a `binding` of `{"scope":"desk"}` or `{"scope":"work","work_id":"..."}`.

Roles removed: `director`, `model`, `review-home`. Role added: `checkpoint`. A task role bound to the desk is visible and is not the selected packet's task section. A work binding for another id stays out of that packet.

Catalog items add required `provenance`. Provenance is an index note. `catalog.used_for_selection` is false. A v1 catalog is a shape gap and is not a fallback selection.

`selected.rule` is `assignment-record/v1` when a page is current. The object adds `current_work`, `record_path`, `review_home`, and `legacy_selector`. The legacy object shows the old id, whether it agrees, and the hint limit. Its checkpoint, verified result, and next route are not applied.

Review home is derived. `N5NN/05.NN` maps to `N1NN` with the same subject and face. `N7NN/06.NN.review` is its own review home. `0412` reporting policy is a dependency.

Director and model text are attribution spans: `author`, `start`, `end`, source sha256, and the copied bytes. Overlap stays visible and the exit is not 0. A role named director is not a reason to quote a whole file.

Top-level result keys are unchanged. `packet` is null on `view`. The fingerprint still excludes observation time.

## Adapter boundary

Claude's 0705 checker pins the frozen pass01 baseline. This note is the version map for a later adapter. It is not an instruction to change that oracle, `expected.json`, or the pass01 candidate so that today's baseline matches pass02. A pass02 request is a different contract. Baseline failures against pass01 remain evidence about pass01.
