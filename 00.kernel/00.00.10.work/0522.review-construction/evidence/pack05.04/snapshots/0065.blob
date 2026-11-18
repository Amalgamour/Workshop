# review-construction-pass01

Disposable constructor for a full Prime assessment on an N5NN `05.NN.md` review section. N7NN renders only the existing `06.NN.review.md` tail. Other source kinds are refused.

From `D:\Git\lib-build`:

```text
python -B labs/review-construction-pass01/construct.py preview --fixture-root ABS --input REL
python -B labs/review-construction-pass01/construct.py apply --fixture-root ABS --input REL
python -B labs/review-construction-pass01/construct.py bind --fixture-root ABS --input REL
python -B labs/review-construction-pass01/construct.py show --fixture-root ABS --target REL
python -B labs/review-construction-pass01/test_construct.py
```

`preview` writes nothing. `apply` writes only inside the fixture root, which must sit outside this checkout. The tool calls pinned `labs/prime-review-pass01/prime_review.py report` and does not edit it. It does not call return capture, return inspection, prime cycle, or the placement lab.

The target must be the derived fixture path for that source page and pass. An N5NN member is `{N}1{NN}.{subject}` from the source page id, and the typed origin book, page, and batch must name that same source. The task binding is `review-task-binding/2`: source book, page, and pass, the assignment logical path, assignment bytes, evidence identities, the supplied receipt files, and the agreement. It does not cover the rendered review or the target file hash. `review-task-binding/1` is not upgraded. A rendered review, a green check, and a byte match are not acceptance, release, closure, or custody. Compare-then-rename is not proof of race freedom.

`python -B labs/review-construction-pass01/test_construct.py` writes its transcript and sample under `00.kernel/00.00.10.work/0522.review-construction/evidence/build05.02/`. The pinned `prime_review.py` capture member pattern accepts `01NN` only. A nonzero N5NN address can be bound here and is refused by that pin at render time.
