# Contract — prime desk view 05.01

Schema: prime-desk-contract/0501
Batch: 0524.prime-desk/05.01
Date: 2026-11-01
Executor: Grok-1

This contract was written before labs/prime-desk-pass01. The tool is a development read view. It is not seated 00.live, not a second lifecycle engine, and not authority.

## What the tool is

A standard-library CLI reads one explicit request and writes a Markdown or JSON view to stdout. `packet` expands the one work item named by the canonical selector. The process exit is the only status channel besides that stdout document.

```text
python -B labs/prime-desk-pass01/prime_desk.py view --request ABS [--json]
python -B labs/prime-desk-pass01/prime_desk.py packet --request ABS --work-id ID [--json]
```

Run from the repository root. `PYTHONDONTWRITEBYTECODE=1` and `sys.dont_write_bytecode` are set. The tool creates no file, including under the instance root, a tools root, or 00.live.

## Exit

| exit | meaning |
| --- | --- |
| 0 | The document was emitted and this request shows no open attention, no observed gap, no stale or changed source, and no unknown verification field. |
| 1 | The document was emitted, and at least one open attention item, observed gap, stale source, changed source, or unknown verification field is visible. A packet whose `--work-id` is not the selector's id is exit 1 and is not expanded as the selected packet. |
| 2 | The request, the instance root, or the selector identity is mechanically unusable. A partial JSON or Markdown refusal is still emitted. No source facts are invented to fill the hole. |

Exit 0 is not acceptance, release, or a clean bill of health for unregistered sources. Coverage is the declared request only. Unregistered does not mean none.

When exit is not 0, the correction names the check and the route. The escalation line is: `Escalation: Codex Prime on 0524.prime-desk/05.01. This tool does not decide meaning, acceptance, or live authority.`

## Request

Schema `prime-desk-request/1`. Exact keys:

`schema`, `instance`, `selector`, `references`, `work`, `workers`, `supplied`, `attention`, `history`, `catalog`, `operations`, `legacy`, `foreign`.

`instance` exact keys: `root`, `book`, `role`, `tools_root`.
`root` is an absolute directory, the only book instance whose relative paths may be read. `book` and `role` are labels. `tools_root` is null or an absolute directory. Operation files and predecessor modules are read only under `tools_root` when it is set. A null tools root means those modules are not loaded.

`selector` exact keys: `path`, `sha256`, `bytes`. The path is relative to `instance.root`. The file must be schema `prime-desk-selector/1` with exact keys `schema`, `selected_work_id`, `checkpoint`, `verified_result`, `next_route`.

`checkpoint` and `verified_result` are null or `{path, sha256, bytes}`. `next_route` is null or `{path, sha256, bytes, speaker}`. Paths are relative to the instance root. A null `verified_result` is unknown verification, not a pass.

`references`, `work`, `workers`, `supplied`, `attention`, `history`, `operations`, `legacy`, and `foreign` are lists.

Reference exact keys: `id`, `role`, `path`, `sha256`, `bytes`, `label`.
Roles: `goal`, `scope`, `authority`, `criteria`, `assignment`, `director`, `model`, `return`, `receipt`, `deliverable`, `verification`, `finding`, `dependency`, `review-home`, `next`, `talk`, `other`.
`label` is an index phrase of at most 200 characters. It is not a second copy of the file and it is not selected task text.

Work exact keys: `id`, `address`, `path`, `sha256`, `bytes`.
`address` is the declared location label. The tool does not infer it from a directory listing or from which file is newest.

Worker exact keys: `id`, `work_id`, `evidence`.
`evidence` is null or `{path, sha256, bytes}`. The evidence file is schema `prime-desk-worker-evidence/1` with exact keys `schema`, `state`, `note`. `state` is `released`, `claimed`, `returned`, or `awaiting-review`. That state is a recorded file. It is not proof a process is running.

Supplied exact keys: `id`, `speaker`, `about`, `text`, `limit`.
`text` is at most 500 characters. `about` is a worker id or an empty string. This is attributed supplied evidence. The limit sentence must say what the label does not prove.

Attention exact keys: `id`, `kind`, `path`, `sha256`, `bytes`, `open`, `label`.
Kinds: `director-question`, `return-awaiting-review`, `observer-finding`, `conflict`, `missing-evidence`, `interrupted`, `hold`.
Every open item is listed. History is not an attention item.

History exact keys: `id`, `path`, `sha256`, `bytes`.
History bodies stay at the path. The overview and the packet list the id, path, hash, and byte length. They do not copy the body.

Catalog file schema `prime-desk-catalog/1`. Exact keys: `schema`, `items`.
Item exact keys: `work_id`, `address`, `label`.
The request names the catalog with exact keys `path`, `sha256`, `bytes`. The catalog is an index. If its bytes match, a `work_id` that differs from the selector is shown and is not chosen. If its bytes differ or the file is missing, the current bytes are not parsed and the selector still decides.

Operation exact keys: `id`, `name`, `path`, `sha256`, `bytes`, `limitation`, `past_tests`, `activation`.
`path` is relative to `tools_root`, or to the instance root when `tools_root` is null.
`past_tests` and `activation` are `unknown` or `supplied-not-verified`. Any other token is kept visible as an unrecognized supplied token and is not treated as a passed test or a live activation. The tool does not execute the operation.

Legacy exact keys: `id`, `reader`, `path`, `sha256`, `bytes`.
`path` is an input document relative to the instance root.
`reader` is `desk-state`, `prime-brief`, `state-projection`, `prime-support`, or `app-context`.

Foreign exact keys: `id`, `root`, `address`, `note`.
`root` is absolute and is not read. A same address in that other root is reported as another instance. Its bytes are not mixed into the selected record.

## Bytes before facts

A declared file is used only when it is a regular file inside the allowed root, not a reparse point, and its sha256 and length equal the request. The tool reads the bytes twice. When the two reads differ, the source is `changed`, the body is not used, and the correction is to rerun after the file is stable. The tool does not refresh itself onto the new bytes.

A hash mismatch is `stale`. A missing file is `missing`. A path with a drive, a leading slash, an empty segment, `.`, or `..` is `outside` and is not opened. A foreign root is not opened.

An unchanged hash proves those bytes. It does not prove meaning, acceptance, freshness of a process, or that unregistered sources are quiet.

## Selection

`selected_work_id` is looked up in `work`. The matching item is current only when its file matched. Other work items are declared and not selected, including a newer page. Duplicate work ids are a mechanical refusal. Two work items with the same address and different ids are both shown; only the selector's id can be current, and the other is an observed conflict.

`packet --work-id` expands a packet only when that id is the current selection. Any other id is named and refused as the packet selection.

Talk files are not parsed and are not executed. A quoted command inside talk does not become an operation.

## Overview and packet

Markdown overview sections, in order:

1. Context and purpose.
2. Current work, checkpoint, verified result, supplied next route, and work that was not selected.
3. Attention: every declared item, then every observed gap, with counts.
4. Workers: recorded evidence and supplied labels kept apart. Activity stays unknown unless a recorded evidence file matched. A supplied word such as running is not that evidence.
5. Operations: path, hash, limitation, and the separate past-test and activation labels. Review-loop integration is the pending line. Successor modules are not called.
6. Record: Director and model sources as separate links. History count and paths. Discussion is not a released command.
7. Inspectability: request hash, observation time, fingerprint, basis, and the correction route.

The overview does not copy work-page bodies, history bodies, or talk bodies. A normal fixture stays readable in well under a minute. An open hold is still listed when the list is long.

The packet adds the selected assignment bytes when they matched and fit in 12000 bytes. A longer matched assignment is not cut: the packet gives path, hash, and length and says the file is the record. Director wording and model explanation are separate sections, quoted from their own matched files under the same rule. Returns, receipts, verification, findings, dependencies, review home, and next routes use the matching reference roles. A missing return or receipt stays absent. Missing verification stays unknown.

JSON schemas are `prime-desk-view/1` and `prime-desk-packet/1`. Exact top-level keys: `schema`, `command`, `state`, `exit`, `check`, `correction`, `observed_at`, `coverage`, `instance`, `selected`, `not_selected`, `catalog`, `attention`, `gaps`, `workers`, `operations`, `record`, `inspectability`, `legacy`, `foreign`, `packet`.

`packet` is null on `view`. On a refused packet selection it is null. On an expanded packet it carries the quoted sections and the same source identities.

`state` is `ready`, `attention`, `partial`, or `refused`.
Basis on each fact is `observed`, `supplied`, `unknown`, `stale`, or `changed`.
`coverage.statement` is fixed: `Declared request paths only. Unregistered sources were not searched.`

`inspectability.fingerprint` is the sha256 of the sorted lines `relative-or-tool-path`, sha256, and length for each file whose bytes were accepted. Observation time is outside that fingerprint, so a second process can recover the same fingerprint and the same selected id.

## Readers

Pins, checked before a reader module is loaded, and only when `tools_root` is set:

| reader | path under tools_root | sha256 | bytes |
| --- | --- | --- | --- |
| desk-state | labs/desk-state-pass01/desk_state.py | 4d924bf6549fe37b229962d4f3a81924109a879a8206ea95066f4bfde11701b4 | 55144 |
| prime-brief | labs/prime-brief-pass01/prime_brief.py | 302ed832d2fa955a591420f13d3b22ce91e4a7669c69a778d443fc82627580d7 | 22747 |
| state-projection | labs/state-projection-pass01/state_projection.py | b349da5cef5178296a069c354002a600ba4e168c2710aa5d87789724d4951ecb | 20338 |
| prime-support | labs/prime-support-pass01/prime_support.py | 700d60d2e49c186d49e56a9a38058e21a722b4a5dd79d461453a305e8d904f70 | 59791 |
| app-context | app/context.py | 5b1a31d47bb9f9b465a8492541467abbd9bd3a99ae524be7aa0dbffe2380eb9f | 22063 |

Loaded modules use a file-location import. They are not imported by package name.

- `prime-brief`: `validate` only. `build` is not called, so fixture lifecycle labels are not copied onto the desk.
- `state-projection`: `validate` only. `project` and `inspect` are not called.
- `desk-state`: the schema token is read. `validate`, `build_view`, and `revise` are not called. `build_view` launches pinned subprocesses and can write a candidate.
- `prime-support`: the module is not called. `status` and `collect` use Git. This request forbids that.
- `app-context`: `parse_assignment` runs on a matched reference whose role is `assignment`. `validate_context` is not called. It lists a runtime band and checks a runner. A record field `assignment_state` is a record field. The value `running` is not a live process check.
- An assignment record that the reader refuses stays visible as a reader refusal. The rest of the view remains.
- Review-loop successors under labs/prime-cycle-pass03, labs/review-loop-pass02, and labs/review-construction-pass02 are not imported.

A legacy input whose bytes do not match is stale and is not passed to the reader.

## Refusals

Mechanical contract failure: wrong schema, wrong keys, bad path, duplicate work id, root missing. Exit 2.
Incomplete evidence: missing file, null verification, absent return or receipt. Exit 1 when the request itself is usable.
Unknown capability: a reader or operation this tool does not execute. The row stays visible.
This tool does not rule on meaning. A catalog that names a different work item is not a semantic judgment. The selector remains the declared rule.
Lack of authority: the tool does not select, release, accept, dispatch, or write. Supplied labels do not gain authority here.

## Out of scope

No Git, network, model call, install, or kernel edit. No edit to predecessor modules, app facades, 0522 successor files, live captures, or 00.live. No return allocation and no 0124 filing. No durable view stored as an authority record. Demo and test transcripts may be saved under evidence/build05.01 by the demo or by the executor after stdout is captured. The tool itself does not write them.
