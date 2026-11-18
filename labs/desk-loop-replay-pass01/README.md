# desk-loop-replay-pass01

Lab glue for `0520.desk-loop-lab/05.01`. It is not seated, not an app change, and not a Prime.

`replay.py` starts a new process for each existing CLI:

- `labs/clerk-handoff-pass02/clerk.py`
- `labs/capture-handoff-pass01/handoff.py`
- `labs/return-capture-pass01/return_capture.py`
- `labs/prime-cycle-pass01/prime_cycle.py`

The cycle calls the pinned reader, inspector, and `prime_review.py`. This lab does not edit those files and does not call a model. Judgment text is supplied by `supply()`.

Disposable repositories and clerk stores are created under the process temp directory, outside `D:\Git\lib-build`.

```text
python -B labs/desk-loop-replay-pass01/test_replay.py
python -B labs/desk-loop-replay-pass01/replay.py --transcript OUT.json
```

Run both from `D:\Git\lib-build`. The contract is `00.kernel/00.00.10.work/0520.desk-loop-lab/evidence/build05.01/CONTRACT.md`.

A verified receipt, a recorded review, and a passing check are custody and observation. They do not accept, release, or publish the work.
