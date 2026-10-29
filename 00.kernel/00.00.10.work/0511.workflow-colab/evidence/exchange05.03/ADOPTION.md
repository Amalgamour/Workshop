# Adoption for the N7NN exchange workflow

schema: colab-exchange-adoption/1
status: map only. No caller in this list was edited.

## What this pass keeps separate
N5NN remains the implementation-job band. 0510 and 0511 stay there. N7NN remains the investigation band, pages 0701–0799. The new tool is labs/colab-workflow-pass02. It consumes exchange layout v2: 05.NN.pack.md, 05.NN.return.md, 06.NN.notes.md, and 06.NN.review.md. labs/colab-workflow-pass01 remains the accepted v1 workflow.

## Future callers, not edited now
| caller | this pass | later bounded change |
|---|---|---|
| app/librarian.py | not edited | a reviewed app route, with app/tests/test_entry.py |
| app/prime_intake.py | not edited | a reviewed registry change, with app/tests/test_prime_intake.py |
| app/context.py | not edited | existing context tests if a caller starts reading this lab |
| 00.kernel/00.live.md | not edited | labs/bootstrap-establish-pass01/test_render_live.py if the derived view changes |
| 0700.band.colabs/03.md | not edited | do not write the menu in this integration |
| 0500.band.packs/01.md | not edited | do not move 0510 or 0511 |

## First useful invocation
Disposable book only. `propose`, then `open --closure` on the accepted v2 output, then `attach --output --config --expect-digest`, then `show`. The digest for the supplied envelope is 42734b859dca535dfe88b6c145fb03912d57a43636a2d7e67d5d3c7b75914184. The tool does not allocate the page, call a model, or write 00.live.

## Smallest post-review action
Prime independently runs that disposable invocation. Do not edit 00.live or app/librarian.py in that same step.
