# colab-workflow-pass01

Standard-library workflow adapter for one caller-selected N7NN investigation. It opens a page in the declared 0700 band, attaches a verified package, records supplied statements and dispositions, and points at an existing 0100 capture. It does not prepare Claude's package, call a model, reserve a return, or write the live work book.

The fact store is `investigation.json`. Markdown faces are projections. `show` does not write `00.live`.

## First Prime invocation

Use a disposable book directory, not `D:\Git\lib-build\00.kernel\00.00.10.work`.

```text
python -B labs/colab-workflow-pass01/colab_workflow.py propose --book ABS-BOOK
python -B labs/colab-workflow-pass01/colab_workflow.py open --book ABS-BOOK --request ABS-REQUEST --sources ABS-SOURCES
python -B labs/colab-workflow-pass01/colab_workflow.py attach --book ABS-BOOK --page 0701.name --pass 05.01 --package ABS-PACKAGE --expect-digest HEX
python -B labs/colab-workflow-pass01/colab_workflow.py show --book ABS-BOOK
```

`propose` prints the lowest free number in 0701–0799 and creates nothing. The caller still has to pass the page to `open`.

## Limits

Space 0 only. Pages 0701–0799. The door 0700 is not a member. No face 07 and no `.colab` filename. The live kernel book is refused. Package digest algorithm `colab-package-digest/1` is local until Prime aligns it with the reviewed 0510 output. Section ids match the whole line `section-id: VALUE`. Return checks launch the pinned `return_inspect.py` and `return_capture.py verify` only. A receipt is custody. A recorded release line is not authority. This tool does not seat an app command.

`build_synthetic_package` writes a fixture directory for tests. It is not the 0510 preparer and it has no command-line entry.
