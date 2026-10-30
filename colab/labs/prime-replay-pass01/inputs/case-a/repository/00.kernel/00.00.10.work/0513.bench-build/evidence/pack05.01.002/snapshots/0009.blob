# colab-workflow-pass02

Standard-library workflow for one caller-selected N7NN exchange. It opens a page in the declared 0700 band, attaches an accepted v2 producer package after the pinned full verifier runs, places exact captured return bytes, and renders a review from a supplied record. It does not prepare the package, call a model, reserve a return, capture a return, or write the live work book.

The fact store is `investigation.json`. Markdown files are projections. `show` does not write `00.live`.

Accepted `labs/colab-workflow-pass01` stays the v1 workflow. This lab does not import it. The v2 producer is `labs/colab-support-pass02/colab_support.py`. Attach calls that file's `verify`. This lab does not call `handoff_check.py`.

## Names

One pass uses `05.NN.pack.md`, `05.NN.return.md`, `06.NN.notes.md`, and `06.NN.review.md`. The binding pass stays `05.NN`. `06.NN.notes.md` is a projection: a header, the immutable launch snapshot, then working appends. `05.NN.return.md` is only the captured `return.md` bytes. Member, receipt, and return sha256 are in `08.md`.

## First Prime invocation

Use a disposable book directory, not `D:\Git\lib-build\00.kernel\00.00.10.work`. Point `--output` and `--closure` at a producer directory that the pinned verifier already accepts. Pass the digest Prime bound at launch. The local `--config` is `colab-config/2` and is not stored.

```text
python -B labs/colab-workflow-pass02/colab_workflow.py propose --book ABS-BOOK
python -B labs/colab-workflow-pass02/colab_workflow.py open --book ABS-BOOK --request ABS-REQUEST --closure ABS-OUTPUT
python -B labs/colab-workflow-pass02/colab_workflow.py attach --book ABS-BOOK --page 0701.colab-exchange-layout --pass 05.01 --output ABS-OUTPUT --config ABS-CONFIG --expect-digest 42734b859dca535dfe88b6c145fb03912d57a43636a2d7e67d5d3c7b75914184
python -B labs/colab-workflow-pass02/colab_workflow.py show --book ABS-BOOK
```

`propose` prints the lowest free number in 0701–0799 and creates nothing. The caller still names the page in `open`. `--sources` reads an explicit tree. `--closure` reads `package/binding.json`, `package/source-manifest.json`, and `package/<snapshot>`.

The digest above is the supplied envelope `00.kernel/00.00.10.work/0511.workflow-colab/evidence/real-producer-v2-05.03`. The tool does not allocate the page, call a model, or write `00.live`.

## Limits

Pages 0701–0799. The door 0700 is not an investigation. Source paths may name `0411.colab` or a file `07.md`. The tool still does not create face 07 or a filename ending in `.colab`. The live kernel book is refused as the book. The accepted envelope may be read.

`place-return` launches the pinned inspector and `return_capture.py verify` for the caller-named member. A receipt is custody. A route is not approval. `request-next` records the caller-named next pass and does not create that pack. This tool does not seat an app command.
