# Integration patch — not applied

Date: 2026-10-31. Author: Grok-2. This file names the later single-owner step. It does not edit `app/librarian.py`, `app/prime-review.json`, `app/prime_review_tools.py`, the constructor, pass01 cycle, or pass01 `prime_review.py`.

## Later registration

Prime, as the single owner of the app facade, can register `app/review-loop.json` beside the existing prime-review declaration. The new schema is `review-loop-pins/1`. It is not `librarian-prime-review`. The registration should call `app/review_loop_tools.py` and should not replace the pass01 review command.

The pinned tools in that declaration are:

- `labs/review-loop-pass01/review_loop.py`
- `labs/prime-cycle-pass02/prime_cycle.py`
- `labs/prime-review-pass02/prime_review.py`
- `labs/review-construction-pass01/construct.py` at `8b9d4a6eda460f594404042f7ee232a7ac55fcc09af38905de364defa189ea8a`
- `labs/prime-review-pass01/prime_review.py` at `805995a1ea8ec3c0b62efad7b5d9ebc8991ba9fd3da75e200b8f626908f4edd0`

The constructor pin stays on pass01 until a versioned constructor successor is reviewed. That successor is the only place that should point a render at pass02. Until then, nonzero N5NN pages commit through the cycle and remain `render-pending` at `bad member`.

## What this patch does not do

It does not migrate `0122.review-construction`. It does not allocate a return. It does not consume `0521` or Grok-1's placement tool. It does not treat a rendered review as approval. Custody stays pending.
