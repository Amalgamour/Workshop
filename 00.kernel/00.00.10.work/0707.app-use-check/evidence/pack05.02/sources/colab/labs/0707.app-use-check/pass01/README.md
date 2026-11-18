# 0707.app-use-check / pass01 — walking the review-loop operator path (lab)

Contract: `00.kernel/00.00.10.work/0707.app-use-check/evidence/build05.01/CONTRACT.md`. Return: `../../../../00.kernel/00.00.10.work/0707.app-use-check/05.01.return.md`.

| File | What |
|---|---|
| `harness.py` | records one `app/librarian.py review-loop` subprocess per call, with a byte guard on the 3 app files and 8 pinned tools before and after; copies 0182 from pack snapshot bytes |
| `walk.py` | operator stages: `start`, `a1`…`f1`, `end`; one stage per invocation |
| `decide.py` | fills the prepare template with the SUPPLIED sample; `PROVENANCE` says where each shape was learned |
| `supplied-judgment.json` | the SUPPLIED sample: Claude, test data, self-review conflict disclosed |
| `compare.py` | new-process recovery: read → `latest_review.directory/record.json` (hash-checked) → field and canonical-byte comparison |
| `verify.py` | aggregates the per-case criteria into `verification.json` |

Rerun (a new run name; existing names are refused), from `D:\Git\lib-build`:

```text
python -I -B colab/labs/0707.app-use-check/pass01/walk.py <run> start
python -I -B colab/labs/0707.app-use-check/pass01/walk.py <run> a1   (then a2 a3 b1 b2 c1 d1 e1 f1 end)
python -I -B colab/labs/0707.app-use-check/pass01/compare.py <run>
python -I -B colab/labs/0707.app-use-check/pass01/verify.py <run>
```

Disposable books go under the session scratchpad (`0707-books/<run>`), outside the checkout. This lab does not run `pilot.py`, a test `__main__`, `reproduce` or `run`.
