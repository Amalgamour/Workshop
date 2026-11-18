# Future cutover proposal — 0521.return-placement

Date: 2026-11-02. Executor: Grok-2. Reviewer: Codex Prime.

This document is a proposal for a later cutover. It is not a Director release, not a recorded release, and not authority to move the live book. The candidate exercised here has `active` false. Preflight refused it. The three paths below were not created. No `return-line-recorded-release/1` file was written for the live book.

## Measured inputs

Audit `00.kernel/00.00.10.work/0417.return-placement/evidence/audit-corrected.json`, schema `return-placement-audit/2`, sha256 `c3bf8c1e25bfd1a59ce40230d87f650897f3105691db732eadfe5abf4e275606`, 391778 bytes.

Read-only live plan, written outside the book at `D:\librarian\temp\0521-0506\20261102T192444618088Z-suite\live-plan.json`, sha256 `52951e1dbc0f37fa7f8c76be390a9510999a6944d7dc9f4e20c00c365f326f66`, 789717 bytes. `live_moves` false. `live_apply` false. Enforcement pending. The disposable copy produced the same hash and length. The contract does not require that match. `evidence/build05.06/live-plan-identity.json` records the path and the hash. The plan body was not copied into the work book.

Layout body for book name `00.00.10.work`: sha256 `2c414ac4e11cd874d28b8c477b7eed30ee477e216ed1653552d802f03c4d7804`, 216 bytes.

Live fingerprint, audit-listed files plus `0100.band.returns/01.md`: `75061b0c183e299c36623e809be8518a0d6efd4482ff13ed3bb3d4865c5e2e6d`. It was the same after the rehearsal.

Successor `labs/return-lines-pass04/return_lines.py`, sha256 `708443c5b3af457f930e8751be4224234d1494f2a2b4e18e3cf08bd7a7af1df6`, 12124 bytes. It loads pass03 by pin `78cc4d8679bb6e54b3f2456ce777643da7a9a650ef5c79c216abd38a4c209c63`, 33349 bytes.

Derived counts from the audit: 83 records, 5 page-local tails, 1 incomplete record. Candidate preflight checked 1204 audit-listed files and found 0 mismatches.

## Unresolved locations

These three paths are candidates carried forward from the 05.05 proposal. The Director has not approved them. This pack did not create them, did not move files into them, and did not commit them.

| Role | Path |
| --- | --- |
| Staging | `D:\librarian\return-placement\0521-staging` |
| Separately verified backup | `D:\librarian\return-placement\0521-backup` |
| Git-trackable retirement | `D:\Git\lib-build\00.archive\0521.return-lines` |

All three are on `D:`, outside the work book `D:\Git\lib-build\00.kernel\00.00.10.work`, and outside each other. They were absent before the rehearsal and absent after it. `00.archive` is absent.

A future execution has to keep the three roots on the book volume. The tool stops a cross-device rename. It does not copy and then delete. The parent of each root has to exist already. The readiness check does not create it.

## Occupants and originals

Publish asks `lines.occupants(book, route target_number, route target_page)`. A staged directory moves to `{retired}/occupants/{name}` when its name starts with that target number and is not the target page. The target number is the line the directory currently occupies. It comes from the origin page through `compute_route`. It is not the record's own destination line.

`0102.prime-support-0501` has logical home `0107.prime-support`. Its directory name starts with `0102`. The route for `0118.workflow-start-0501` has target number `0102` and target page `0102.workflow-start`, so publish moves `0102.prime-support-0501` to occupants. Retire then moves every remaining audited old member to `{retired}/originals/{name}`.

On the ordinary CLI copy the measurement was 18 occupant directories and 65 original directories. Together they are the 83 audited members. Zero old members remained in the book. The tool does not encode 18 or 65.

Lookup keeps the pass01 descriptor and adds `detail.new_home` plus `detail.retained_original`. `retired_rel` is `originals/{name}` or `occupants/{name}` under the caller-supplied retired root. On this rehearsal that root is the disposable copy. It is not an approved live archive.

## Old-reader routing

`labs/return-capture-pass01/return_capture.py` `verify --book --member` expects a capture envelope as a direct child of `--book`. The member argument cannot contain a slash. The reader was not patched.

Measured on the official copy:

- `--book` the retired root, member `0101.app-entry-0506` or `0104.app-entry-0508`: exit 2, `member is missing`.
- `--book` `originals/`, member `0101.app-entry-0506`: exit 0, not approved, not accepted, not published.
- `--book` `originals/`, member `0104.app-entry-0508`: exit 2, `member is missing`.
- `--book` `occupants/`, member `0104.app-entry-0508`: exit 0, not approved, not accepted, not published.
- `--book` `occupants/`, member `0101.app-entry-0506`: exit 2, `member is missing`.

No one of those books verifies both members. The logical page `0121.synthetic-filing` exits 2 with `unexpected 05.01.custody`. An adapter was not added. Historical readers and old sequential-writer closure remain separate gates.

## Incomplete 0154 and pending captures

`0154.colab-support-first-0501` stays incomplete. Lookup exit 1. Return hash and return length stay null. No `0110.colab-tools/05.01.return.md` was invented.

Current-work captures `0121` through `0126` have no receipt and no task association in this pack. They are separate from the historical members `0121.archive-resolution-0508`, `0122.bridge-overlap-0513`, `0123.boot-validation-0508`, `0124.clerk-seam-design-0503`, `0125.mapping-capture-0509`, and `0126.boot-members-0509`. This proposal does not invent those receipts.

## Release candidate

The candidate file is `D:\librarian\temp\0521-0506\20261102T192444618088Z-suite\live-candidate.json`, schema `return-line-release-candidate/1`, sha256 `b2cc40741208bc19c961a0e66844da02e9c082f5d459037eebab7196fbc2cdc6`, 1681 bytes. `active` is false. That hash equals the 05.05 candidate because the audit, plan, layout, roots, and unresolved sentences are the same bindings. Equality is a measurement. It does not promote the candidate. `executor` records the name Codex Prime. That label is not a release.

`evidence/build05.06/preflight-candidate.json` is the live preflight of that candidate. Exit 2. Check `return-line-release-candidate/1`. `evidence/build05.06/preflight-absent.json` is the live preflight with no authorization file. Exit 2. Check `authorization`. Reason `authorization is absent`. Neither probe wrote a layout, a marker, or a proposed directory.

Unresolved choices, each of which blocks a live cutover:

- The Director has not approved the staging, backup, or retirement paths.
- This invocation is not an execution release, and Prime has not recorded one.
- The executing identity is not recorded for a live cutover.
- `0154.colab-support-first-0501` stays incomplete. No return is invented.
- Pending captures `0121` through `0126` have no receipt and no task association.
- Retained bytes are split across occupants and originals. The historical reader has no adapter.
- Old sequential reserve closure is not built. The allocation-lock sentinel is not adopted.

A later live pair would be a new `return-line-director-release/1` file and a new `return-line-recorded-release/1` file that pins those bytes. The production validator would then evaluate that pair for the canonical book with the same checks it uses for a copy. Editing the plan, the release file, or the pin alone drops the old approval. This pack does not write that pair.

## Later declaration-only pin

After Prime reviews this return, a later pack can change the app declaration from `labs/return-lines-pass03/return_lines.py` at `78cc4d8679bb6e54b3f2456ce777643da7a9a650ef5c79c216abd38a4c209c63` to `labs/return-lines-pass04/return_lines.py` at `708443c5b3af457f930e8751be4224234d1494f2a2b4e18e3cf08bd7a7af1df6`. That change is declaration-only. This pack does not make it. Grok-1's concurrent pass03 copy integration is not edited here.

## What stays held

A future live cutover stays held until a reviewed Director release binds the book, the plan, the audit, the layout, the operation list, the three roots, and the executing identity; until the archive locations are chosen; until caller closure is reviewed; and until recovery is reviewed. The capability to evaluate that release is what this pack built. Running it on the live book is not what this pack did. Old sequential reserve closure and Claude's lock sentinel remain proposals. This pack did not install a sentinel, patch an allocator, or edit `app/` or callers.

The disposable test recording says it is a test recording. It does not authorize the live book.
