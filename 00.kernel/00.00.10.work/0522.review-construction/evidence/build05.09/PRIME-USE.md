# PRIME-USE — 0522.review-construction/05.09

date: 2026-11-01
who: Grok-1
reviewer: Codex Prime

This is development wiring. It is not a live review, not acceptance, and not the live-use pilot. The current-assignment record was not changed. No page under 00.kernel/00.00.10.work was written by these commands except the evidence this slice already names.

The selected entry is app/librarian.py. It loads app/review_loop_tools_v3.py and app/review-loop-v3.json. The launched module is labs/review-loop-pass03/review_loop.py. Direct construction is construct_pass04. The cycle bind remains construct_pass02. The door checks all nine declared pins before launch and does not accept a caller executable.

## Disposable path

Use Python 3.14.0 at C:\Users\misg\AppData\Local\Programs\Python\Python314\python.exe, with python -B and PYTHONDONTWRITEBYTECODE=1, from D:\Git\lib-build.

Create a fresh directory outside D:\Git\lib-build. The cited test used prefix rc0509-, page 0599.synth-lab/05.01.md, pinned return_lines for init, reserve, and capture, registration schema prime-cycle-registration/2, and request schema review-loop-request/1 at request.json. The decision file is decision.json. The judgment used for the round trip is outcome continue, disposition held, pass terminal open, goal terminal open. The supplied next sentence is:

Pack one bounded correction for the disposable capture.

Those fixture directories are deleted when the test ends. The preserved outputs are in the cited run below. A Prime repeats the path by making a new disposable root, not by reusing a deleted temp directory and not by writing the live work book.

## Commands

Prepare, then record, then render, then read. The read is a separate process.

```text
python -B app/librarian.py review-loop prepare --fixture-root <absolute-disposable-root> --request request.json
python -B app/librarian.py review-loop record --fixture-root <absolute-disposable-root> --request request.json --decision decision.json
python -B app/librarian.py review-loop render --fixture-root <absolute-disposable-root> --request request.json
python -B app/librarian.py review-loop read --fixture-root <absolute-disposable-root> --request request.json
```

Inspect the stored judgment at <absolute-disposable-root>/cycle/05.01-r1/record.json. In the cited round trip that judgment's disposition is held.

Recover the same next action in another fresh process:

```text
python -B app/librarian.py review-loop recover --fixture-root <absolute-disposable-root> --request request.json
```

Cited run evidence/build05.09/runs/20261101T225355Z-b3e958a5. round-read exited 0. again-recover exited 0 with render.result already-rendered and apply_called false. The following read returned the same two sentences below.

## Supplied next and mechanical next

From round-read in that run, schema review-loop-result/2:

- Supplied. current.next_action_label is supplied. supplied_next_action.text is "Pack one bounded correction for the disposable capture."
- Mechanical. mechanical.state is rendered. mechanical.route is read. mechanical.text and the top-level next are "Read the rendered review."

Top-level next is the mechanical sentence. It is not the supplied sentence. accepted is false. authority is none. custody is not-established.

After record and before render, the mechanical sentence in that run was "Run recover: it retries rendering the same committed review into the unchanged target." The supplied sentence was already the correction sentence. Those are different fields.

## Rollback

This slice did not perform rollback and did not delete the v3 files.

1. In app/librarian.py, load app/review_loop_tools_v2.py again under the module name librarian_review_loop_tools_v2. The before-edit copy is 00.kernel/00.00.10.work/0522.review-construction/evidence/build05.09/before/librarian.py, sha256 d07de8a7c6d0c2ecb03300c5a4aed1d2659122e4fdecd843431adafba715857b, 11037 bytes.
2. Restore the review-loop section of app/README.md from evidence/build05.09/before/README.md, sha256 f33cf04646fbc6841bea4a9e99a37841edbd3d9e04635f52297d0fca906b2b3c, 29833 bytes.
3. Leave app/review_loop_tools_v3.py and app/review-loop-v3.json on disk.
4. Do not edit the v2 door, the v2 declaration, or any lab module. Their bytes were unchanged by this slice.
