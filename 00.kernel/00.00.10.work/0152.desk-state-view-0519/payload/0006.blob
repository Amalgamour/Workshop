# Migration proposal — legacy current_work to a desk record

Status: proposal. Nothing in this file is selected, adopted, or run.

## Selected source, later

The source that would become selected is one `desk-state/1` record. The example is `00.kernel/00.00.10.work/0508.return-capture/evidence/deskstate05.19/desk.json`. It is a proposed working configuration. It is not a second assignment. `00.kernel/00.00.10.work/0401.goal/06.01.md` remains the legacy assignment record.

## Readers that would need a later change

`labs/bootstrap-establish-pass01/render_live.py` reads `0401.goal/06.01.md` and `0410.imports/manifests/step03-selection-register.tsv`. It writes `00.kernel/00.live.md`. It does not read this view. A later adoption would change that reader, or replace it, so the generated live page comes from the desk record. Any other reader that treats `current_work` as the sole current task would need the same explicit change. This pass does not change those readers.

## Checks before adoption

- Codex Prime reviews `labs/desk-state-pass01` and this captured return.
- The Director decides whether the desk record becomes the selected source.
- Pins change only after that review. No boot pin changes in this pass.
- The adopted reader is run at the adoption commit, and its output is checked against the record hash and the source cuts.
- `00.kernel/00.live.md` is regenerated only by that adopted reader.

## Review and adoption

Adoption is a Prime review followed by a Director decision. This pass does not migrate, does not rewrite `00.kernel/00.live.md`, and does not rewrite `0401.goal/06.01.md`. The live page remains the observed stale legacy gap: it mirrors the 2026-10-27 assignment and says it is not an input.
