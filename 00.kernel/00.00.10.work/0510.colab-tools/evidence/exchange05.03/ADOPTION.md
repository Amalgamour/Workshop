# ADOPTION — exchange layout v2 preparer (0510/05.03)

State: an adoption note from the producer side. It changes no other lane's work and claims no integration.

## Timing and boundary at this return
- **Grok-1, 0511/05.02** is repairing v1 workflow integration against frozen v1 33bbe41c…. v1 is byte-identical before and after this batch, and is pinned by test. I did not read or change any 0511 page, claim, evidence or `labs/colab-workflow-pass01` file.
- **Grok-2, 0512/05.01** is building Prime reporting and holds. I did not read or change any 0512 page or `labs/prime-review-pass01` file.
- Both are unfinished and unreviewed. Neither is a dependency of this lab, and this lab is not a dependency of theirs.

## What a later workflow update would adopt (names only; not changing their work)
1. **Grok-1's upcoming workflow layout update** (a future reviewed and released pass, not 0511/05.02):
   - Consume `handoff.json` (`colab-handoff/2`) at the launch-carried digest. Validate with `colab_support.py verify` or the standalone `handoff_check.py check`.
   - Attach `package/05.NN.pack.md` and `package/06.NN.notes.md` to the investigation pass unchanged.
   - Place the return later from the verified N1NN capture, as exact bytes at `05.NN.return.md`, using the `colab-placement-proposal/2` record from intake.
   - Treat `support/` as transport support only.
2. **Grok-2's review output integration**:
   - Map supplied Prime reports to `06.NN.review.md`, using the sections of `templates/06.NN.review.TEMPLATE.md`: return provenance, Prime assessment, Director reply, unresolved questions, dispositions and reasons, route.
   - Keep `06.NN.notes.md` separate.
   - Never infer a Director reply or approval from an empty field.

## Explicit adoption, no bulk rename
- v2 applies only to new packages prepared with `colab-request/2`.
- Prior v1 captures (0155), v1 packages (digest a4b91dd6…) and every receipt stay intact. Nothing is relabelled or renamed.
- Existing N5NN implementation batch names (`05.NN.md`, `06.NN.md`) stay canonical. The tails are for actual N7NN exchanges only.

## Supported now
- **Origin:** N7NN pages 0701–0799 in a declared book.
- **Targets:** one repository and commit, exact headings or whole files.
- **Scoring:** unscored, open scored, or blind scored with evaluator isolation.
- **Recipients:** zip-only or local-tools.
- **Intake:** exact capture with origin enforcement, and a placement proposal.

## Not supported or not done
- Live placement, review writing, next-pack creation, closure and model dispatch.
- Section ids and multi-commit packages.
- End-to-end v2 workflow: no claim until a reviewed consumer integrates it.
