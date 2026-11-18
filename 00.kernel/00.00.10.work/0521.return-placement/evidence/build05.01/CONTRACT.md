# Contract — return placement candidate (0521.return-placement 05.01)

Written before the code. This lab computes a return line and can rehearse a move inside a disposable fixture. It does not migrate the work book, does not call `return_capture.py reserve`, and does not edit sealed `return-capture/1` bytes.

## 1. Route

Input is an origin object `{book, page, batch}` read from `reservation.json`. The folder name is not an origin.

`page` must be `NNNN.subject`. The subject is the text after the first dot. The band is the second digit of `NNNN`. `NN` is the last two digits.

- Band 5: target page is `01NN.subject`. Route name `matched-workflow-return-line`. Pass `05.NN` from `batch` is the tail `05.NN.return.md` on that one page. A second pass of the same page is another tail on the same page.
- Band 7: target page is the same `07NN.subject`. Route name `page-local-colab`. The tails `05.NN.pack.md`, `05.NN.return.md`, and `06.NN.review.md` stay on that page. No N1NN page is computed. This candidate does not invent pack or review bytes. It records those names and leaves existing files untouched.
- Any other band, or a page or batch that is not these shapes: refusal `undeclared origin`. Nothing is placed.

`batch` must match `05.NN`. The pass identity is that batch. It is not a new member number.

The route record is `return-placement-route/1`. It includes the origin, both numbers, the subject, the target page, the return path, and the custody directory `target-page/05.NN.custody`. `sequential_allocation` is false.

## 2. Custody copy

A fixture apply copies these regular files when they exist: `01.md`, `reservation.json`, `manifest.json`, `receipt.json`, `return.md`, and the files under `payload/`. Bytes are unchanged. Reparse points, junctions, and hard links are refused and are not created.

The only new file inside the custody directory is `relocation.json`, schema `return-placement-relocation/1`. It names the old member path, the origin, the submission id, the route, and each copied file's relative path, sha256, and length. It states that the sealed reservation destination was not rewritten.

If `return.md` exists, the return tail is a byte copy of it. If `return.md` is absent, no tail is written and the item is `incomplete`. That item is never reported complete. 0154 is this case.

N7: if the return tail already exists and its bytes equal `return.md`, the tail is kept and reported `verified-equal`. It is not rewritten. The custody copy is still required. If the tail exists and differs, the item is a conflict and nothing is overwritten.

## 3. Identity, conflicts, lookup

Identity is origin book, page, and batch, plus submission id.

- The same source bytes applied again to the same destination are `already-placed`. No file is rewritten.
- The same identity with any different source byte is refused. The destination is left as it was.
- Two source folders in one apply with the same origin pass are a duplicate conflict. Neither is copied.
- A destination file that already exists with different bytes is an occupied-target conflict. It is not overwritten.
- A missing `reservation.json`, or a reservation without a usable origin, is unresolved. The slug is not consulted.

Lookup reads the journal. It answers by old member, by origin page plus batch, and by the return path. An incomplete item remains visible as incomplete.

## 4. Fixture migration and rollback

`apply` and `resume` require a fixture root that does not contain `0100.band.returns`. Every source and destination is resolved to an absolute path and must stay inside that root. A path that escapes, or a reparse point on the path, is a refusal before the recursive copy.

The journal is `return-placement-journal/1`, inside the fixture root. Items run in ascending old-member order. The journal is flushed after each copied file. `complete` is true only when every item is `placed` or `verified-equal`. Incomplete, conflict, refusal, and interruption keep `complete` false.

`--interrupt-after N` stops after N successful file copies, exits 3, and leaves the journal resumable. Resume checks hashes already recorded, then continues. A destination whose hash is not the recorded hash is a mismatch refusal. Resume does not mark that run complete.

Rollback deletes only destination files this journal created, and only when each still has the recorded hash, and only after the containment check. Source folders stay. Rollback does not use a shell delete of the fixture root.

`filing-check` is read-only. A new filing onto `0121.return-placement` is blocked while any other directory named `0121.*` remains. This pass does not create that page.

## 5. Live plan

`plan` reads the work book and the pinned `audit-corrected.json`. It writes only the requested `--out` file. It does not create member directories.

The plan schema is `return-placement-plan/1`. `live_moves` is false. Items follow ascending old member, starting at the lowest capture. Each item has the computed route, the proposed return path, the proposed custody directory, and the live sha256 and length of every audited file under that member, compared with the audit. N7 tails are hashed again and compared with the captured `return.md`.

Changes since the audit are listed and do not alter the audit file. Unresolved items, collisions, and preconditions are fields on the plan. 0154 stays incomplete. The precondition for this batch is that `0121.return-placement` is unused until `0121.archive-resolution-0508` has been migrated and, after Prime acceptance, retired. 0184 is not a destination.

## 6. Out of scope

No edit to pinned labs, app doors, kernel law, or existing captures. No Git write. Sequential reserve remains available for historical `/1` reads and is not claimed retired. Enforcement of live callers is `INTEGRATION.md`, a proposal, not a patch applied here.
