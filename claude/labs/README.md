# Labs

why: test whether the axioms change what a model does, by giving the same work to cold models with and without them.

A lab is one piece of work, written as a pack, run under different conditions, and scored against a rubric written before the runs.

## Folders

| Folder | Holds | Rule |
|---|---|---|
| `packs/` | the packs, one file per condition (`01.a.md`, `01.b.md`), and the shared body they are built from | a pack is self-contained: hand it to any model as it stands |
| `returns/` | each run's return, as returned (`01.a.1.md`) | never edited after it is saved (axiom 6) |
| `notes/` | rubric, expected answers, predictions, results, and what each result means for the axioms | the rubric is written before the runs and not changed after |

## Conditions

- **a**: the pack alone.
- **b**: the pack with `Axioms.md` loaded and `axioms:` cites on the job items.
- **c** (from lab 02): the pack with the cites only, no `Axioms.md`. Tests whether the small package carries the concept on its own.

## Handing a lab to another model

1. Give the model one pack file, and nothing else from this folder. The rubric and expected answers must not travel with it.
2. Tell it: work from the pack only, and reply with the return the pack asks for.
3. Save the reply in `returns/` as `NN.<condition>.<model>.<run>.md`.
4. Score it against `notes/NN.rubric.md`, and add a line to the results table in `notes/NN.md`.

## Limits

- Scoring is by a model that wrote the packs, so it is not blind. The rubric is fixed first to limit that.
- The first runs use one model family. Other families are the real test.
