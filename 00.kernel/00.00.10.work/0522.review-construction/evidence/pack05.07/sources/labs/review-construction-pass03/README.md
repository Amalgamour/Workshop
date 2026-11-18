# review-construction-pass03

Isolated successor of `labs/review-construction-pass02/construct.py`. The pass02 file stays in place. The contract is `00.kernel/00.00.10.work/0522.review-construction/evidence/build05.06/CONTRACT.md`.

`review-construction/1` keeps the pass02 section text and the same task-binding inputs. `review-construction/2` adds `supplied_review_state` and the supplied-state section. `inspect` classifies a target and writes nothing.

```text
python -B labs/review-construction-pass03/construct.py preview --fixture-root ABS --input REL
python -B labs/review-construction-pass03/construct.py apply --fixture-root ABS --input REL
python -B labs/review-construction-pass03/construct.py bind --fixture-root ABS --input REL
python -B labs/review-construction-pass03/construct.py show --fixture-root ABS --target REL
python -B labs/review-construction-pass03/construct.py inspect --fixture-root ABS --target REL [--binding HEX64]
```

The fixture root must be an absolute directory outside `D:\Git\lib-build`. Exit 0 is a constructor answer. It is not Prime review and it is not app activation.
