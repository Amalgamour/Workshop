# colab-review-pass01

The Colab review adapter (0518.colab-review 05.01). Standard library only. It adds four bounded features to the existing Colab tools:
- declared review modes and context;
- a retained comprehension paraphrase;
- post-fix simplicity review;
- traceable synthesis.

It is a lab adapter, not seated and not a review engine. It never launches a model, a reviewer or a session, never authenticates isolation, and never judges meaning.

**Contract:** `00.kernel/00.00.10.work/0518.colab-review/evidence/build05.01/CONTRACT.md`. **Guide:** `evidence/build05.01/PRIME-USE.md`.

The 05.02 repair keeps that route. It carries intake diagnostics, every declared reviewer/stage status, and the original retained wording into the derived report. Delta contract: `evidence/build05.02/CONTRACT.md`. Guide: `evidence/build05.02/PRIME-USE.md`. New intake is `colab-review-intake/2`. New reports are `colab-review-report/2`. A stored `/1` intake still synthesizes; its missing stage inventory is stated and is not invented.

```text
python -B labs/colab-review-pass01/colab_review.py stage      --plan ABS --request ABS --repo ABS --out-request ABS
python -B labs/colab-review-pass01/colab_review.py bind       --output ABS --config ABS --producer ABS --expect-digest HEX --out ABS [--plan ABS]
python -B labs/colab-review-pass01/colab_review.py intake     --binding ABS --plan ABS --book ABS --member NAME [...] --config ABS --out ABS
python -B labs/colab-review-pass01/colab_review.py synthesize --intake ABS --synthesis ABS --out ABS
python -B -X dev labs/colab-review-pass01/tests/test_colab_review.py -v
python -B labs/colab-review-pass01/demo.py --out ABS_NEW_DIR
```

## How it fits the existing tools

None of them is changed.

| step | tool |
|---|---|
| stage the plan, prompts and template as `required_sources`, in one commit with the target | this adapter (`stage`) |
| preview, prepare and verify the package | producer v2, unchanged |
| prove the review files are inside the verified package | this adapter (`bind`) |
| open, attach and place-return the investigation | workflow v2, unchanged |
| reserve, capture and verify each reviewer's return, with `review-result.json` as an artifact | helper, and producer intake, unchanged |
| check what came back | this adapter (`intake`) |
| derive a traceable report from a supplied synthesis | this adapter (`synthesize`) |
| record Prime's review and its projection | workflow v2 `record-review`, unchanged |

## Boundaries

- **One return per pass.** The workflow places one return per pass (`05.NN.return.md`). With several reviewers, one member is placed and the rest stay verified in N1 custody; `intake` reads all of them. The smallest follow-up would be a reviewed workflow pass for multi-member placement. It is not built here.
- **Producer `mode` is unchanged.** It still has its four values. The review mode lives in the plan.
- **Compute checks shape and links only:** identities, required fields, order and mapping. Comprehension, findings and synthesis are supplied text. Isolation is shown as declared, and is never verified.
