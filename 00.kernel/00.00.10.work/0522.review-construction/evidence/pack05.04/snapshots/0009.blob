# Contract — return placement safeguards (0521.return-placement 05.02)

Written before the repair code. This pass repairs the 05.01 candidate in labs/return-placement-pass01. It does not migrate the work book, does not call `return_capture.py reserve`, does not edit sealed `return-capture/1` bytes, and does not replace evidence/build05.01.

## 1. Route

Input is an origin object `{book, page, batch}` read from `reservation.json`. The folder name is not an origin.

`page` must be `NNNN.subject`. The subject is the text after the first dot. The first digit of `NNNN` is the workflow-space `N`. The band is the second digit. `NN` is the last two digits.

- Band 5: target page is `N1NN.subject`. The leading digit is the same `N` as the origin page. Route name `matched-workflow-return-line`. `0504.app-entry` passes `05.06` is `0104.app-entry/05.06.return.md`. `1504.app-entry` is `1104.app-entry`. `9504.x` is `9104.x`. A second pass of the same page is another tail on that same page.
- Band 7: target page is the same `N7NN.subject` at any supported prefix. `0701.bench-method` stays on that page. `1702.design` stays on `1702.design`. Route name `page-local-colab`. The names `05.NN.pack.md`, `05.NN.return.md`, and `06.NN.review.md` stay on that page. This candidate does not invent pack or review bytes.
- Any other band, including a page whose second digit is not 5 or 7, or a page or batch that is not these shapes: refusal `undeclared origin`. Nothing is placed. `1701.other` is band 0 and stays refused.

`batch` must match `05.NN`. The pass identity is that batch. It is not a new member number.

The route record is `return-placement-route/1`. It includes the origin, the workflow space, both numbers, the subject, the target page, the return path, and the custody directory `target-page/05.NN.custody`. `sequential_allocation` is false. Every generated identity uses that same `N`.

## 2. Occupied lines

A target number is occupied when any directory directly under the book or fixture root is named `NUMBER.something` and that name is not exactly the target page. The source directory counts when it is one of those directories. A missing return tail does not make the number available. The exact target page, when it is the only directory on that number, is the line itself and is not a different-name occupant.

The plan enumerates those occupants for every computed return line. Each occupied line is a collision of kind `occupied-line`, with the target page, the number, the occupant names, the source members, `staging_required` true, `retirement` `not performed`, `line_adoption` false, and `overwrite` false. The same rows are collected as `occupancy_conflicts`. `filing_0121` stays a separate blocker. `0121.return-placement` is not one of the occupied migration targets.

The fixture applier does not create the final page beside a different-name occupant and does not overwrite that occupant. It copies bytes under `staging/{old-member}/05.NN.return.md` and `staging/{old-member}/05.NN.custody/`. That staging directory is not a `01NN` member. Status is `staged` only when custody is valid. `complete` stays false. Retirement is not performed. A later accepted run would still have to retire the occupant before the final line can be adopted.

When the number is free, a destination file that already exists with different bytes is an occupied-target conflict. Nothing is overwritten. An N7 tail that already matches is `verified-equal` and is not rewritten. An N7 tail that differs, on a free line, is a conflict and nothing is written.

## 3. Custody, copy progress, and acceptance

Before a source is treated as ready, this lab loads the pinned `labs/return-capture-pass01/return_capture.py` by path and calls `verify_member`. The load refuses when those bytes are not the pinned reader. The reader is not edited. `reserve` is not called.

`verify_member` must accept the sealed reservation, manifest, receipt, return, and payload relationships. A simplified receipt is not custody. Missing or malformed receipt, manifest, or payload, and any wrong hash, set `custody_valid` false.

Three facts stay separate on every item and in the apply result:

- Copy progress is `none`, `copied`, `staged`, or `verified-equal`.
- `custody_valid` is the pinned reader's result. `custody_reason` is the reader's first refusal line when it refuses.
- `acceptance` is null. `approved`, `accepted`, and `published` are false. A validated receipt is not approval, acceptance, seating, publication, or finish.

`complete` is true only when every source is `placed` or `verified-equal`, custody is valid, the line was adopted, and the run was not interrupted. Status `placed` is an adopted copy of a package the reader accepted. Status `verified-equal` is an adopted N7 tail that already matched, with valid custody. Status `staged` is a valid package parked because the line is occupied. Status `copied-incomplete` is a copy of a package the reader refused. Status `incomplete` is a source with no `return.md`, including 0154. No return tail is invented. The incomplete source stays visible through lookup.

Existing incomplete bytes may be copied so the journal can show them. That copy does not set `complete` and does not set `line_adoption`. Historical packages are read only. Their reservation bytes are copied, not reserialized, and not patched. The relocation record still states that the sealed reservation destination was not rewritten.

## 4. Identity, conflicts, lookup

Identity is origin book, page, and batch, plus submission id.

- The same source bytes applied again are `already-placed` when the earlier status was `placed` or `verified-equal`, and `already-recorded` otherwise. No file is rewritten.
- The same identity with any different source byte is refused. The destination is left as it was.
- Two source folders in one apply with the same origin pass are a duplicate conflict. Neither is copied.
- A missing `reservation.json`, or a reservation without a usable origin, is unresolved. The slug is not consulted.

Lookup reads the journal. It answers by old member, by origin page plus batch, and by the final return path or the staged return path. An incomplete item remains visible as incomplete.

## 5. Fixture migration and rollback

`apply` and `resume` require a fixture root that does not contain `0100.band.returns`. Every source and destination is resolved with `os.path.abspath` and must stay inside that root. A path that escapes, or a reparse point on the path, is a refusal before the copy. Symlinks and hard links are not created. `os.walk` uses `followlinks` false.

The journal is `return-placement-journal/1` at `placement-journal.json`. Items run in ascending old-member order. The journal is flushed after each copied file.

`--interrupt-after N` stops after N newly created files, exits 3, and leaves the journal resumable. Resume checks hashes already recorded, then continues. A destination whose hash is not the recorded hash is a mismatch refusal. Resume does not delete that file.

Rollback deletes only destination files this journal created, and only when each still has the recorded hash. Source folders stay. Pre-existing N7 tails were not created by the journal and stay. Rollback does not use a shell delete of the fixture root.

Exit 0 is a complete journal. Exit 1 is recorded and not complete. Exit 2 is a refusal. Exit 3 is interrupted.

`filing-check` is read-only. A new filing onto `0121.return-placement` is blocked while any other directory named `0121.*` remains. This pass does not create that page and does not allocate 0184.

## 6. Live plan

`plan` reads the work book and the pinned `audit-corrected.json`. It writes only the requested `--out` file. It does not create member directories and it does not call `apply`. The new plan is evidence/build05.02/migration-plan.json. The 05.01 plan file stays as it was.

The plan schema remains `return-placement-plan/1`. `live_moves` is false. Items follow ascending old member, starting at the lowest capture. Each item has the computed route, the proposed final return path, the proposed custody directory, the live sha256 and length of every audited file, the occupancy record, and the custody result.

The pinned reader is re-executed read-only on each present member. `verify_reexecuted` is true. A matching audit hash is not custody. Changes since the audit are listed and do not alter the audit file. 0154 stays incomplete. An occupied line stays blocked. The precondition for this batch is that `0121.return-placement` is unused until `0121.archive-resolution-0508` has been migrated and, after Prime acceptance, retired. 0184 is not a destination.

## 7. Out of scope

No edit to pinned labs other than return-placement-pass01, no edit to app doors, kernel law, or existing captures. No Git write. Sequential reserve remains available for historical `/1` reads and is not claimed retired. This lab does not reserve, capture, or look up new live work. Enforcement of live callers is INTEGRATION.md, a proposal, not a patch applied here.
