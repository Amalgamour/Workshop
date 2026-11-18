# PRIME-USE - workbook review pass02

Source: 0522.review-construction/05.12. This pack repairs intake, freshness, and publication. It is not acceptance and not a release.

Run these from `D:\Git\lib-build` with `python -B`. The book is an absolute directory. The source is a page id. The pass is `05.NN`.

The owned book is `D:\Git\lib-build\00.kernel\00.00.10.work`, or a directory outside `D:\Git\lib-build`. The repo root and any other directory inside the checkout are refused. A junction into the checkout is refused and is not followed.

```text
python -B app/librarian.py review-loop prepare --book ABSOLUTE-BOOK --source PAGE --pass 05.NN
python -B app/librarian.py review-loop form --book ABSOLUTE-BOOK --source PAGE --pass 05.NN
```

Copy `intake_id` from the form result. Write a judgment JSON file that contains only the declaration fields. Leave out intake_id, review_id, hashes, registration, receipt, descriptor, and agreement. `semantic_conflict` is present as true, false, or null. An omitted field is a missing field. `tests_passed` null stays null. The declaration is `labs/workbook-review-pass02/forms/workbook-review-v1.json`. This file is its correction route.

`continue` carries sections `return_result`, `prime_finding`, `within_direction`, and `next_bounded_action`, plus `next_action`. `director-input` carries sections `issue`, `consequences`, `options`, `recommendation`, and `question`, plus `affected` and a matching hold. Director text measured from the page stays verbatim. A successor stores the supplied reply. That reply leaves the pack unreleased.

```text
python -B app/librarian.py review-loop record --book ABSOLUTE-BOOK --source PAGE --pass 05.NN --intake INTAKE --judgment ABS-JSON
python -B app/librarian.py review-loop inspect --book ABSOLUTE-BOOK --source PAGE --pass 05.NN
python -B app/librarian.py review-loop publish --book ABSOLUTE-BOOK --source PAGE --pass 05.NN --review REVIEW
python -B app/librarian.py review-loop read --book ABSOLUTE-BOOK --source PAGE --pass 05.NN
python -B app/librarian.py review-loop recover --book ABSOLUTE-BOOK --source PAGE --pass 05.NN
```

Copy `review_id` from the record result. It is `w` plus 16 hex characters. Pass that id to publish. On a filed book the cycle id is `{pass}-{review_id}` under `workbook-review/{page}/{pass}/cycle-records/`. The id Prime publishes with is the `w` id. A second source uses its own cycle directory. A successor passes `--successor CURRENT`.

Writes this module performs stay under `workbook-review/` or the one derived target, `{page}/{pass}.md` for N5NN or `{page}/06.{tail}.review.md` for N7NN. A filed call also lets the pinned loop write `scratch/`, `trace/`, `partial/`, and `support/{review_id}/` under the book. The pinned constructor does not replace a review section that is already filled. That publish exits 1 and the existing section stays.

Exit 0 is a completed command. It is not approval, filing, or release. Exit 1 means the judgment is kept and publication or recovery is blocked. Exit 2 is a refusal before a record, or a bad call.

Prepare, form, and inspect of the current book are read-only. The current book is `D:\Git\lib-build\00.kernel\00.00.10.work`, source `0522.review-construction`, pass `05.11`. This builder does not record or publish there. Matching line `0122.review-construction` stays pending.

The read-only current-book run used book `D:\Git\lib-build\00.kernel\00.00.10.work`, source `0522.review-construction`, pass `05.11`. prepare, form, and inspect each exited 0. Stderr was empty. Custody is missing. The submission row is root book, path `0522.review-construction/evidence/build05.11/submission.md`, sha256 `409b983fd58f6432b356ebecb716f250cec4e2406c0c443d5a0fa3e91fe6c96c`, 16825 bytes. The artifact-manifest row is the returned 05.11 manifest, sha256 `ec7ff7fbc7cf1e2939439ff85c82e7a0f3ab46f0b2d4cf4649c870e5faa4ed3e`, 4637 bytes. Twenty artifact rows are bound. Displayed artifact cuts stop at 12. Measurement is incomplete because `app/librarian.py` and `app/README.md` no longer match that historical manifest. Those mismatches are findings. The page stayed sha256 `531482b4b7a0c14cc2a6aba7014089972636a54e013cbc75ed3cedd786f32ef2`, 11646 bytes. This builder did not record or publish there. Outputs are `00.kernel/00.00.10.work/0522.review-construction/evidence/build05.12/current-book`. Successful copied runs are not Prime's independent acceptance or the real-use gate.
