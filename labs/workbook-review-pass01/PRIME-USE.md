# PRIME-USE - workbook review

Source: 0522.review-construction/05.11. This pack built the entry. The next review starts from a returned assignment. It starts from that returned page, after this pack has been returned.

Run these from `D:\Git\lib-build` with `python -B`. The book is an absolute directory. The source is a page id. The pass is `05.NN`.

```text
python -B app/librarian.py review-loop prepare --book ABSOLUTE-BOOK --source PAGE --pass 05.NN
python -B app/librarian.py review-loop form --book ABSOLUTE-BOOK --source PAGE --pass 05.NN
```

Copy `intake_id` from the form result. Write a judgment JSON file that contains only the declaration fields, in this order: finding, reasons, operation, disposition, pass_terminal, goal_terminal, next_action, semantic_conflict, design_fork, findings, sections, holds, answers, review_passes, gaps.

Leave out intake_id, review_id, hashes, registration, receipt, descriptor, and agreement. `semantic_conflict` is present as true, false, or null. Null is the legal unknown. An omitted field is a missing field. `tests_passed` null stays null. A required string is non-empty. The declaration is `labs/workbook-review-pass01/forms/workbook-review-v1.json`. This file is its correction route.

The pinned prime_review check still applies to the substantive shape. `continue` carries sections `return_result`, `prime_finding`, `within_direction`, and `next_bounded_action`, plus `next_action`. `director-input` carries sections `issue`, `consequences`, `options`, `recommendation`, and `question`, plus `affected` and a matching hold. `question` carries `id`, `revision`, `content_sha256`, and `text`. Director text measured from the page stays verbatim. A successor stores the supplied reply. That reply leaves the pack unreleased.

```text
python -B app/librarian.py review-loop record --book ABSOLUTE-BOOK --source PAGE --pass 05.NN --intake INTAKE --judgment ABS-JSON
python -B app/librarian.py review-loop inspect --book ABSOLUTE-BOOK --source PAGE --pass 05.NN
python -B app/librarian.py review-loop publish --book ABSOLUTE-BOOK --source PAGE --pass 05.NN --review REVIEW
python -B app/librarian.py review-loop read --book ABSOLUTE-BOOK --source PAGE --pass 05.NN
python -B app/librarian.py review-loop recover --book ABSOLUTE-BOOK --source PAGE --pass 05.NN
```

Copy `review_id` from the record result. It is `w` plus 16 hex characters. Pass that id to publish. On a filed book the cycle directory name is `{pass}-wb`. That directory name is a cycle id. The id Prime publishes with is the `w` id.

A successor passes `--successor CURRENT` when the judgment bytes differ. The old record stays.

Preliminary custody stays missing. `operation` complete is refused there. The correction names the refusal. The original bytes stay under `workbook-review/{page}/{pass}/failed/`.

Exit 0 is a completed command. It is not approval, filing, or release. Exit 1 means the judgment is kept and publication or recovery is blocked. Exit 2 is a refusal before a record, or a bad call.

A workbook command and `--fixture-root` together are refused. Record, publish, read, and recover refuse a book inside `D:\Git\lib-build`. Prepare, form, and inspect may read that checkout and write nothing.

This builder did not record or publish a judgment on 0522.review-construction/05.11. While the return pointer said PENDING, prepare, form, and inspect used book `D:\Git\lib-build\00.kernel\00.00.10.work`, source `0522.review-construction`, pass `05.11`. Each exited 0. Custody was missing. The findings were return-pending, custody-missing, and return-missing. The return path was null. Inspect judgment was null. The page stayed sha256 `22c7cdde7e847b6e15e7c31e621e4e49fc0466539496abaa80814d6e6cb10ed6`, 10286 bytes. Those outputs are `00.kernel/00.00.10.work/0522.review-construction/evidence/build05.11/current-book`. Matching line `0122.review-construction` stays pending. 0184 was not allocated.
