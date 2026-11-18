# Integration — review construction after this lab

Date: 2026-10-31. Author: Grok-2. This page names the next seam. It does not change `app/`, `prime_cycle.py`, or the placement lab.

## What this lab already does

`labs/review-construction-pass01/construct.py` renders a full assessment into an N5NN `05.NN.md` section headed `Review — Codex Prime` or `Review - Codex Prime`. N7NN is only the existing `06.NN.review.md` tail. The task binding is `review-task-binding/1`. The safe-write hash is the target file hash and is not part of that binding. Receipt files are hashed. Custody stays `not-established`. No member is allocated.

## Future cycle change

`labs/prime-cycle-pass01/prime_cycle.py` `record` compares the decision template with `current_binding`. The compared `source` is the observed page sha256 (`source.page_sha256` around the binding built in `current_binding`). A review written onto that same page changes the page hash, so a later `record` refuses with `source changed since read: source`. This lab does not patch that function.

The smallest cycle change is one new accepted binding input, `review-task-binding/1`, beside the existing page hash. Staleness for the judgment uses the task binding. The page hash remains the compare-and-swap token for the write. A rendered review that leaves task, assignment bytes, evidence, receipt, and agreement unchanged must not be reported as source-stale. A change to any of those must. Old templates that bind only `page_sha256` stay readable and keep today's refusal. `closes_work`, `releases_action`, and `authenticates_actor` stay false.

Do not add a second status engine. The cycle already calls pinned `prime_review.py`. The constructor also calls that report command. One integration worker should own the shared facade change. No parallel edit to `app/librarian.py`.

## Future app entry

`app/prime_review_tools.py` already launches pinned `prime_review.py` for `prime-review`, `prime-guard`, and `prime-check-next`. A later pack can add one command, `prime-review-construct`, with declaration `app/prime-review.json` pointing at `labs/review-construction-pass01/construct.py`. The command passes through stdout, stderr, and the integer exit. It refuses a fixture root inside the checkout, a drifted pin, and a linked path. It does not gain `draft`, reserve, or capture.

## Adapter after reviewed placement

This constructor's receipt object is the seam. A later adapter, written only after Prime reviews the 0521 migration, fills that object from the placed bytes. For this source the matching line is `0122.review-construction`. The adapter reads the placed `receipt.json`, return bytes, and manifest, and sets `placement` to `n5nn-matching-line`. It does not scan the old `01NN` table and it does not allocate. N7NN keeps `page_local` `05.NN.return.md` and `member` null. `labs/return-placement-pass01` was not imported here. Until that adapter exists, a caller passes the three files explicitly. A boolean does not authenticate them.

## Minimal next test

One disposable N5NN page with a `PENDING.` review section. Apply this constructor. In a second process, run the updated cycle read and record using `review-task-binding/1` computed before the render. The record must succeed, and the stored binding must equal the pre-render binding. Then change one evidence byte and show the new record refused. Do not point that test at the live work book, and do not run inventory, bridge fixtures, or race probes. AR-01 stays held.

## Not in this pack

No universal face builder. No worker launch. No claim that the live cycle is already fixed. No Git publication.
