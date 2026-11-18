# Contract — prime desk view 05.02

Schema: prime-desk-contract/0502
Batch: 0524.prime-desk/05.02
Date: 2026-11-01
Executor: Grok-1

This contract was written before labs/prime-desk-pass02. The tool is a development read view. It is not seated 00.live, not a second lifecycle engine, and not authority. labs/prime-desk-pass01 remains the prior implementation and is not edited.

## What the tool is

A standard-library CLI reads one explicit request and writes Markdown or JSON to stdout. `packet` expands only the work named by the canonical assignment record. The process exit is the status channel besides that stdout document.

```text
python -B labs/prime-desk-pass02/prime_desk.py view --request ABS [--json]
python -B labs/prime-desk-pass02/prime_desk.py packet --request ABS --work-id ID [--json]
python -B labs/prime-desk-pass02/request_index.py --list ABS --out ABS [--accept REL]
```

Run from the repository root. `PYTHONDONTWRITEBYTECODE=1` and `sys.dont_write_bytecode` are set. The view tool creates no file. The index helper writes only the new `--out` request, and only when every declared hash matches or a path was passed to `--accept`.

## Exit

| exit | meaning |
| --- | --- |
| 0 | The document was emitted. This request shows no open attention, no observed gap, no stale or changed source, no unknown verification, no legacy disagreement, and no pending derived custody. |
| 1 | The document was emitted, and at least one open attention item, gap, stale source, changed source, unknown verification, legacy disagreement, or pending custody line is visible. A packet whose `--work-id` is not the canonical id is exit 1 and is not expanded. |
| 2 | The request, the instance, the coverage token, or the canonical identity is mechanically unusable. A partial refusal is still emitted. No newer page and no catalog entry is chosen to fill the hole. |

Exit 0 is not acceptance. Coverage is declared paths only.

When exit is not 0, the correction includes: `Escalation: Codex Prime on 0524.prime-desk/05.02. This tool does not decide meaning, acceptance, or live authority.`

## Canonical selection

The workspace file is the pinned `app/development-workspace.json` named by the request, read under `tools_root`. Its `assignment_record`, `desk`, and `work_book` name the record. `instance.book` must equal `work_book`. The request's assignment path must be that record with the `{desk}/{work_book}/` prefix removed. Any other assignment path is a refusal. The tool does not generate a selector file.

The record is schema `00.kernel/00.00.10.work/0410.imports/01.md#assignment-record version 1`. It is parsed with the pinned `app/context.py` `parse_assignment` only. `validate_context` is not called. `assignment_state` stays a record field.

`current_work` must use the same prefix. The remainder is the page inside this instance. A path outside that prefix is a foreign identity and a refusal. The page must match one of these shapes, and the declared work address must equal it exactly:

- `N5NN.subject/05.NN.md` with N5NN in 0500–0599 and NN from 01 through 99. Review home is `N1NN.subject/05.NN.md` in this same instance. The matching custody file is linked only when the request already names that path. Absence is pending custody, not a fabricated receipt and not a substitute policy page.
- `N7NN.subject/06.NN.review.md` with N7NN in 0700–0799. Review home is that same page. Reporting policy stays a dependency.

Any other page identity is an unsupported selection and a refusal. The catalog, file order, and a legacy selector cannot replace it. If the identity is valid and no declared work row has that exact path, the result is partial: selected is null, and nothing else is chosen.

## Legacy selector

`legacy_selector` is null or a hashed file. The readable shape is still `prime-desk-selector/1`, and it is a hint. `selected_work_id` is shown. Checkpoint, verified result, and next route inside that file are not applied. Disagreement with the canonical work id stays visible. A missing or malformed hint does not block a valid canonical selection and does not create a replacement selector.

## Request

Schema `prime-desk-request/2`. Exact keys:

`schema`, `instance`, `workspace`, `assignment`, `legacy_selector`, `coverage`, `references`, `work`, `workers`, `supplied`, `attention`, `history`, `catalog`, `operations`, `legacy`, `foreign`, `attribution`.

`coverage` must be `declared-paths`. Any other token is an unsupported-coverage refusal.

`instance` exact keys: `root`, `book`, `role`, `tools_root`. `root` and `tools_root` are absolute directories. `tools_root` is required.

`workspace` and `assignment` exact keys: `path`, `sha256`, `bytes`. Workspace paths are relative to `tools_root`. Assignment and other book paths are relative to `instance.root`.

Reference exact keys: `id`, `role`, `path`, `sha256`, `bytes`, `label`, `binding`.
Desk-wide roles: `goal`, `scope`, `authority`, `dependency`, `talk`, `assignment`, `other`.
Work-bound roles: `criteria`, `checkpoint`, `return`, `receipt`, `deliverable`, `verification`, `finding`, `next`.
There is no `director`, `model`, or `review-home` role. A task role with desk scope is visible as unbound task material and is not the selected packet's task section. A work binding whose id is not the canonical id stays out of that packet.

Work exact keys: `id`, `address`, `path`, `sha256`, `bytes`.

Worker exact keys: `id`, `work_id`, `evidence`. Evidence is null or `{path, sha256, bytes}` with schema `prime-desk-worker-evidence/1`. The state is a recorded file. Process activity stays unknown. A worker's `work_id` is a supplied association, not proof.

Supplied exact keys: `id`, `speaker`, `about`, `text`, `limit`. `text` is at most 500 characters. `about` is a worker id or empty.

Attention exact keys: `id`, `kind`, `path`, `sha256`, `bytes`, `open`, `label`.
Kinds: `director-question`, `return-awaiting-review`, `observer-finding`, `conflict`, `missing-evidence`, `interrupted`, `hold`.
Every open item is listed. History is not attention.

History exact keys: `id`, `path`, `sha256`, `bytes`. Bodies are not copied into the overview.

Catalog file schema `prime-desk-catalog/2`. Exact keys: `schema`, `items`.
Item exact keys: `work_id`, `address`, `label`, `provenance`.
Provenance is an index note of at most 200 characters. The catalog does not select.

Operation exact keys: `id`, `name`, `path`, `sha256`, `bytes`, `limitation`, `past_tests`, `activation`.
`path` is relative to `tools_root`. `past_tests` and `activation` are `unknown` or `supplied-not-verified`. Any other token stays visible and is not a passed test or a live activation. The tool does not execute the operation.

Legacy reader exact keys: `id`, `reader`, `path`, `sha256`, `bytes`.
Readers: `desk-state`, `prime-brief`, `state-projection`, `prime-support`, `app-context`.
`build`, `project`, `inspect`, `build_view`, Git, and `validate_context` are not called. Review-loop successor modules are not imported. One operation row says that integration is pending.

Foreign exact keys: `id`, `root`, `address`, `note`. An absolute foreign root is not read.

Attribution exact keys: `id`, `author`, `path`, `sha256`, `bytes`, `start`, `end`, `binding`.
`author` is `director` or `model`. `start` is inclusive and `end` is exclusive, both byte offsets into the hashed file. The tool copies that slice and does not read headings to decide the author. Overlapping spans on one file are ambiguity: both stay visible, neither becomes the sole wording, and the exit is not 0. A slice is withheld when the file hash does not match. Spans bound to another work stay out of this packet.

`label` is at most 200 characters. An unchanged hash proves bytes, not meaning, acceptance, or process freshness. A changed or stale file is withheld. The tool does not refresh onto the new bytes.

## Output

View schema `prime-desk-view/2`. Packet schema `prime-desk-packet/2`. The same top-level keys are present. `packet` is null on `view`. `selected.rule` is `assignment-record/v1` when a page is current. Markdown keeps the seven overview sections and puts task text in the packet. Open holds are not truncated. Missing verification is unknown. Talk is not executable.

The fingerprint is the sha256 of the sorted accepted `path/sha/length` lines. It excludes observation time, so a second process can recover the same fingerprint and selected id.

## Index helper

`request_index.py` hashes only the paths named in a source list. It does not walk the repository and does not invent task text or a running status. When a declared hash differs, it writes no request and reports a revision. That report is not a corruption finding. `--accept REL` may pin that one path's current bytes into a new request. A builder updating a returned page is that kind of revision.

## Preserved limits

Pass01 CLI verbs stay. Pass01 files and evidence are not rewritten. No source write, no 00.live rewrite, no Git, no worker launch, and no live-book run in this pass.
