# REAL-USE — read-only preview on published sources (0515.prime-cycle 05.01)

**What was run.** The Builder ran `prime_cycle.py read` read-only against published commit `4d8bc1c7d6f0f960179deb87f1ebc81d18ab366a`, for one work:
- page `0508.return-capture/05.20.md` (git blob, sha256 `306dcd15…`);
- member `0169.desk-state-preservation-0520`.
The registration, the templates and the outputs were written to a new external temp directory, `pcy-preview-*`, which is recorded in sample-cycle.json. **Nothing was written to the repository.** `git status` for 0508.return-capture and 0169 was empty before and after, and no `prime-cycle-reviews` directory exists. **No review was recorded as Builder.**

## Result

| item | value |
|---|---|
| exits | `read --json` 1, `read` 1, `read --templates` 1 (attention present) |
| pass state | `awaiting-review` |
| custody | 0169, `primary-current-candidate`, inspection `complete`, receipt `94a5fe21286c95187c456c28ebd45a95f7ed2faaa06da6779d9ce220197424bc`. Custody is not acceptance. |
| disposition, pass terminal, goal terminal | `unknown`, `unknown`, `unknown` |
| attention | `legacy-review-unmapped` and `awaiting-review` |
| reader codes | `legacy-ambiguous-heading`, `legacy-revision-withheld`, `quoted-accepted-unbound`, `duplicate-release`, copied |
| elected | null |

## Facts that still need Prime's input

1. **The page goal statement.** The preview used the page title, marked "PREVIEW, Prime must confirm or replace". The goal id and statement are yours.
2. **The agreement.** goal, scope, prime_discretion, director_required, finish_criteria and recorded_decisions are all null (unknown) in the preview.
3. **The judgment.** outcome, disposition, pass terminal, goal terminal and evidence, finding, reasons, source refs, next action, unresolved, and the needed sections.

## Legacy mapping limit

Prime's existing review exists as page prose ("Accepted as a bounded derived-view lab helper…") and as `evidence/prime-review05.20/REVIEW.md` (sha256 recorded in sample-cycle.json). It is **not** a `prime-cycle-review/1` record. The cycle shows it as `legacy-review-unmapped`, and does not type it. Adoption is one explicit attributed review recorded by Prime (PRIME-USE §3). An old "Accepted" sentence never becomes a typed completion.

## Manually supplied judgment fields

Counted from the real template:

| case | fields |
|---|---|
| continue (accepted, pass finished, goal open) | 14 |
| complete (goal completed) | 18 |
| director-input (hold) | 15 |

That is 13 top-level judgment fields null in the template, plus the outcome-specific sections out of 24 available. All binding, hash, member and lineage fields are pre-filled. No time, token or productivity saving is claimed, and nothing here claims a fresh Prime.
