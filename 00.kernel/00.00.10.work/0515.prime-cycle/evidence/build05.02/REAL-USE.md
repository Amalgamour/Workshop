# REAL-USE — real sources, read-only (0515.prime-cycle 05.02)

The 05.01 read-only preview stays as recorded in `build05.01/REAL-USE.md`, at 4d8bc1c. For 05.02 the Builder repeated it read-only with the corrected tool and the journal on:
- the published commit `d19241074e8db09723ddf44e0900c839a62bc526`;
- one work: page `0508.return-capture/05.20.md` and member `0169.desk-state-preservation-0520`.

The registration, templates and journal went to a new external temp directory, `pcy-preview-*`, which is recorded in sample-cycle.json under `real_preview`.

**Nothing was written to the repository.** `git status` for 0508.return-capture and 0169 was empty before and after, and no `prime-cycle-reviews` directory exists. **No review was recorded, and the real 0169 review was not adopted.**

## Result

| item | value |
|---|---|
| exits | `read --json` 1, `read` 1, `read --templates` 1; `day` 0 |
| pass state | `awaiting-review` |
| summary | works 1, awaiting review 1, finished passes 0, completed goals 0 |
| custody | 0169, `primary-current-candidate`, receipt `94a5fe21286c95187c456c28ebd45a95f7ed2faaa06da6779d9ce220197424bc`. Custody is not acceptance. |
| attention | `legacy-review-unmapped` and `awaiting-review` |
| template | `prime-cycle-decision/2`, with `direction` bound. The preview's agreement fields are null (unknown). Each is bound as the sha256 of canonical `null`, so filling one in later changes the direction. |
| journal | 3 read operations, each with start, inputs, stdout and end; status `ok-attention`, caller "Claude Builder (read-only preview)" |
| day | 3 attempts, 0 unique reviews, current: nothing finished or completed |

## Facts that still need Prime's input

These are unchanged from 05.01:
1. **The page goal id and statement.** The preview used the page title, marked PREVIEW.
2. **The agreement:** goal, scope, prime_discretion, director_required, finish_criteria and recorded_decisions. These are now bound into the template, so they must be final before the read whose template you fill.
3. **The judgment.** Minimal supplied fields: 14 for continue, 18 for complete, 15 for a hold.

## Legacy mapping limit

- Prime's existing review is still page prose plus `evidence/prime-review05.20/REVIEW.md`. It is not a typed record; the view shows `legacy-review-unmapped`, and adoption is one explicit attributed review.
- A `prime-cycle-review/1` record from the 05.01 tool would be read, but shown only as historical (`review-unusable`, `legacy-binding`), because it has no direction binding. No such record exists on any real page.

No time, token or productivity saving is claimed.
