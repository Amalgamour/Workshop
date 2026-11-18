# PRIME-USE - workbook review pass03

Source: 0522.review-construction/05.13. This pack repairs actual return intake and duplicate source identities. It is not acceptance and not a release.

Run these from `D:\Git\lib-build` with `python -B`. The book is an absolute directory. The source is a page id. The pass is `05.NN`.

The owned book is `D:\Git\lib-build\00.kernel\00.00.10.work`, or a directory outside `D:\Git\lib-build`. The repo root and any other directory inside the checkout are refused. A junction into the checkout is refused and is not followed.

```text
python -B app/librarian.py review-loop prepare --book ABSOLUTE-BOOK --source PAGE --pass 05.NN
python -B app/librarian.py review-loop form --book ABSOLUTE-BOOK --source PAGE --pass 05.NN
```

Copy `intake_id` from the form result. Write a judgment JSON file that contains only the declaration fields. Leave out intake_id, review_id, hashes, registration, receipt, descriptor, and agreement. `semantic_conflict` is present as true, false, or null. `tests_passed` null stays null. The declaration is `labs/workbook-review-pass03/forms/workbook-review-v1.json`. This file is its correction route.

`continue` carries sections `return_result`, `prime_finding`, `within_direction`, and `next_bounded_action`, plus `next_action`. A page-relative `evidence/...` pointer is resolved from the source page. An artifact line may end in `bytes, N files.` with the two known exclude sentences. A submission may declare verification on four separate lines. That declaration is not a successful verification run. The same physical file keeps one validator id and every intake role.

```text
python -B app/librarian.py review-loop record --book ABSOLUTE-BOOK --source PAGE --pass 05.NN --intake INTAKE --judgment ABS-JSON
python -B app/librarian.py review-loop inspect --book ABSOLUTE-BOOK --source PAGE --pass 05.NN
python -B app/librarian.py review-loop publish --book ABSOLUTE-BOOK --source PAGE --pass 05.NN --review REVIEW
python -B app/librarian.py review-loop read --book ABSOLUTE-BOOK --source PAGE --pass 05.NN
python -B app/librarian.py review-loop recover --book ABSOLUTE-BOOK --source PAGE --pass 05.NN
```

Copy `review_id` from the record result. It is `w` plus 16 hex characters. Pass that id to publish. On a filed book the cycle id is `{pass}-{review_id}` under `workbook-review/{page}/{pass}/cycle-records/`. A second source uses its own cycle directory. A successor passes `--successor CURRENT`.

Exit 0 is a completed command. It is not approval, filing, or release. Exit 1 means the judgment is kept and publication or recovery is blocked. Exit 2 is a refusal before a record, or a bad call.

Prepare, form, and inspect of the current book are read-only. The current book is `D:\Git\lib-build\00.kernel\00.00.10.work`, source `0521.return-placement`, pass `05.10`. This builder does not record or publish there. Matching line `0122.review-construction` stays pending.


The read-only current-book run used book `D:\Git\lib-build\00.kernel\00.00.10.work`, source `0521.return-placement`, pass `05.10`. prepare, form, and inspect each exited 0. Stderr was empty. Custody is missing. Measurement is complete. The submission row is root book, path `0521.return-placement/evidence/build05.10/submission.md`, sha256 `ddccb9110a02d82df300adffc25870c8ebf24d0815dab2651c67ececfaf36de8`, 874 bytes. The artifact-manifest row is the historical 05.10 manifest, sha256 `bbd4e5a33279105f0177491c7eff2ecfa70e172cd0fd6a266d70c2c3b93e809d`, 3867 bytes. Sixteen artifact rows are bound. Twelve are book files and four are code-root files under `labs/return-readiness-pass01/`. Displayed artifact cuts stop at 12. Every bound artifact hash matches its declaration. The page stayed sha256 `af56727c4a29007d9a78b0a746af4c949774daf01632bf7c1b7258ce471963c5`, 8076 bytes. The verification declaration is measured. `successful_run` is false. Its sources are `submission-lines` and `artifact-index`. This builder did not record or publish there. Outputs are `00.kernel/00.00.10.work/0522.review-construction/evidence/build05.13/current-book`. Successful copied runs are not Prime's independent acceptance or the real-use gate.
