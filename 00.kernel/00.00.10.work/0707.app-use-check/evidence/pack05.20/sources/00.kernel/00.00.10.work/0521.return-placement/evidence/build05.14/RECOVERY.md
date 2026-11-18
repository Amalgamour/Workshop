# Recovery limits — N7 first review

Date: 2026-11-03. Executor: Grok-2. Reviewer: Codex Prime.

## What the proof measured

Before publish, `09-n7-cycle-read` reported mechanical state `create-pending`, route `recover`, and the sentence that recover creates the declared review file while that file is still absent. The page was absent. The token was `absent-create`.

`review_loop` recover calls `render_committed`. That is the exclusive-create path: the pinned constructor writes `name.review-construct.tmp` with `O_EXCL` and renames it onto the derived target. The happy path created the file through workbook publish, which calls that render. The later new-process render returned `already-rendered` and left the page hash `66b30232469c651229e8db1e8818769ed9a562441896dd02155ddbd5c4510234`. Workbook recover, run after that publish, left those bytes in place.

The planted temporary `06.01.review.md.review-construct.tmp` was still 18 bytes after the refused publish. No `rendered.json` on that copy marks it complete. The driver did not delete it.

A file planted after prepare stayed in place under rule `target appeared after read`. A directory at the destination stayed in place. A return edited after record blocked publication, and that copy's review file stayed absent.

## What this exclusive create covers

One declared N7 path. Absence rechecked at commit and again at render. Creation only through the constructor's exclusive temporary plus rename. An existing review, Director sentence, link, or directory is left untouched. An incomplete temporary is kept and stays unmarked.

## What remains outside this proof

Power loss beyond the retained temporary. A crash after a successful rename and before `rendered.json` is a later read of the page bytes against the committed record. Multiwriter races. AR-01. A second review on the same N7 page. Live migration. Shared route selection. The mechanical route was observed. The proof's creating call was publish. A separate pre-create call to `review_loop recover`, with no publish, was not the happy-path command.
