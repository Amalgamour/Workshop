# Prime use — 05.03 review loop

Date: 2026-10-31. Author: Grok-2. This note is for Prime's review. It is not acceptance, seating, adoption, or custody.

## What is ready to inspect

The 0-space demonstration is in `transcript.json`. A disposable book outside `D:\Git\lib-build` is required. The loop does not write the live work book.

From `D:\Git\lib-build`:

```text
python -B labs/review-loop-pass01/review_loop.py prepare --fixture-root ABS --request REL
python -B labs/review-loop-pass01/review_loop.py record --fixture-root ABS --request REL --decision REL
python -B labs/review-loop-pass01/review_loop.py render --fixture-root ABS --request REL
python -B labs/review-loop-pass01/review_loop.py read --fixture-root ABS --request REL
python -B labs/review-loop-pass01/review_loop.py recover --fixture-root ABS --request REL
```

`prepare` returns a `prime-cycle-decision/3` template. Prime fills `attribution`, `judgment`, and `supplied_record`. Compute does not invent those words. `record` commits on a pass02 report exit 0 or 1. Exit 1 is a recorded report, not approval. `render` calls the unchanged constructor. `read` in a new process returns the supplied next action and questions. `recover` retries a pending render or reports `already-rendered` without a second apply.

`full_success` means the mechanical step finished. It does not accept the work. Every result sets `custody` to `not-established`, `allocated` to false, and `closes_work`, `releases_action`, and `authenticates_actor` to false.

## What Prime should not treat as integrated

`app/review-loop.json` and `app/review_loop_tools.py` pin the adapter. `librarian.py` does not load them. The constructor still calls pass01 `prime_review.py`. A nonzero N1NN member can be committed through pass02 and still stops at `bad member` on the page. The judgment is kept as `render-pending`. A constructor successor has to pin `labs/prime-review-pass02/prime_review.py` before that page can render. This pack does not retarget the constructor.

The synthetic descriptor in `synthetic-descriptor.json` conforms to `return-line-descriptor/1`. It is not a live capture and not Grok-1's output. `verification.result` is an observed label, not authority.

## Historical records

A `/3` review stays current when the `review-task-binding/2` digest, origin, member, direction, and goal still match. Rendering changes the write token and does not stale that review. A changed task, evidence file, agreement, or receipt does. A `/1` record stays legacy. A `/2` record keeps the old whole-page rule and is not rewritten as `/3`.
