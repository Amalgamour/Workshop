# colab-workflow-pass01

Standard-library workflow adapter for one caller-selected N7NN investigation. It opens a page in the declared 0700 band, attaches an accepted producer package after the pinned verifier runs, records supplied statements and dispositions, and points at an existing 0100 capture. It does not prepare Claude's package, call a model, reserve a return, or write the live work book.

The fact store is `investigation.json`. Markdown faces are projections. `show` does not write `00.live`.

## First Prime invocation

Use a disposable book directory, not `D:\Git\lib-build\00.kernel\00.00.10.work`. Point `--output` at a producer directory that `colab_support.py verify` already accepts. Pass the digest Prime bound at launch. The local `--config` is `colab-config/1` and is not stored.

```text
python -B labs/colab-workflow-pass01/colab_workflow.py propose --book ABS-BOOK
python -B labs/colab-workflow-pass01/colab_workflow.py open --book ABS-BOOK --request ABS-REQUEST --closure ABS-OUTPUT
python -B labs/colab-workflow-pass01/colab_workflow.py attach --book ABS-BOOK --page 0701.name --pass 05.01 --output ABS-OUTPUT --config ABS-CONFIG --expect-digest HEX
python -B labs/colab-workflow-pass01/colab_workflow.py show --book ABS-BOOK
```

`propose` prints the lowest free number in 0701–0799 and creates nothing. The caller still has to pass the page to `open`. `--sources` remains for an explicit tree. `--closure` reads `package/source-manifest.json` and the snapshot blobs.

`legacy-diagnose --package ABS` reports the 05.01 synthetic directory and writes nothing. `attach` refuses that directory.

## Limits

Space 0 only. Pages 0701–0799. The door 0700 is not a member. Source paths may name `0411.colab` or a file `07.md`. The tool still does not create face 07 or a filename ending in `.colab`. The live kernel book is refused as the book. The accepted envelope may be read.

`colab-package-digest/1` means the producer length-prefixed preimage. This tool does not recompute it. The old line-oriented preimage is `legacy-line-preimage`. Section kind `id` is unsupported. Headings are exact lines outside fences. Return checks launch the pinned inspector and `return_capture.py verify` only. A receipt is custody. A recorded release line is not authority. This tool does not seat an app command.

`build_synthetic_package` still writes the legacy fixture for the refusal test. It is not the 0510 preparer and it has no command-line entry.
