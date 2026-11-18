# 0708.colab-capability pass01

Audit driver for 0708.colab-capability/05.01. It builds one synthetic request and calls the existing producer, handoff checker, and workflow. It does not prepare packages itself, does not define a Colab extension schema, and does not edit those tools.

Method and claim: `00.kernel/00.00.10.work/0708.colab-capability/06.01.notes.md`.

Raw command output is written to `00.kernel/00.00.10.work/0708.colab-capability/evidence/build05.01`. Disposable output and books stay under `%TEMP%\0708-colab-capability`, outside the live book.

```text
python -B colab/labs/0708.colab-capability/pass01/probe.py
```

Run from `D:\Git\lib-build`. The probe uses read-only `git cat-file` against HEAD. It does not run intake, capture, place-return, or the existing test suites.
