# 0708.colab-capability pass02

Evidence-preserving successor for one probe run. It allocates a new evidence slot and a new scratch slot under roots the operator names. It does not delete a directory, and it has no default evidence path and no default scratch path.

Method and claim: `00.kernel/00.00.10.work/0708.colab-capability/06.02.notes.md`.

Create both roots first. Then, from `D:\Git\lib-build`:

```text
python -B colab/labs/0708.colab-capability/pass02/probe.py run --evidence-root ABS --scratch-root ABS --run-id ID --mode ok
```

Modes are `ok`, `fail`, `hold`, and `preview`. `preview` also requires absolute `--request`, `--config`, and `--producer` paths. The producer must match the pinned sha256 and length recorded in the probe. A mismatch is stored in the new evidence slot and the producer is not started.

Exit 0 means `status.json` says `complete`. Exit 1 means this process wrote `failed` in a new slot. Exit 2 means the probe refused before creating an evidence slot. An existing run id is exit 2, and the existing bytes stay.

A `status` of `running` with interruption null, after the process is gone, is an actual termination marker. A caught child failure is `failed` with interruption `caught-failure`, and its partial files stay. Do not point a later run at an earlier slot to finish it. This probe has no resume command.

`ok` and `fail` are synthetic children. `hold` sleeps so a caller can terminate the process. `preview` is the only existing-tool path. Harness tests use temporary roots and are not package acceptance.

```text
python -B colab/labs/0708.colab-capability/pass02/tests/test_probe.py
```
