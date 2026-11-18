# PRIME-USE — 0705 pass03 baseline check
date: 2026-11-01 · who: claude-opus-5-5 (Claude)

## Rerun exactly
From `D:\Git\lib-build`, with any standard-library Python (3.14.0 was used here):
```text
python -I -B colab/labs/0705.prime-desk-check/pass03/run_baseline.py --pack05-03 <abs>/0705.prime-desk-check/evidence/pack05.03/source-manifest.json --pack05-02 <abs>/0705.prime-desk-check/evidence/pack05.02/source-manifest.json --out <new abs dir outside the checkout>
python -I -B colab/labs/0705.prime-desk-check/pass03/probe_c05.py --baseline <that dir> --pack05-02 <abs>/.../pack05.02/source-manifest.json --out <new abs dir>
python -I -B colab/labs/0705.prime-desk-check/pass03/tests/test_adapter.py
```
- Everything executed comes from pack05.03 snapshot bytes under `<out>/pinned/`: the candidate b047a303…0b20, its pinned reader `app/context.py`, and the pass02 builder, checker, expected manifest and checklist.
- The baseline writes:
  - `runs/<case>/`: run-record, raw view/packet stdout and stderr, request artifacts;
  - `observations/`, `mapping-trace/`, `conflicts/`;
  - `check-report.json`, `baseline-summary.json`.

## How to read the result
- **The verdict** is `not-passed`: 12 pass, 9 wrong, 29 unsupported, 4 not-run, 24 manual items pending.
- **Do not read that as "29 defects".** Use `classification.json`, which sorts every row into:

  | Class | Count | What it means |
  |---|---|---|
  | product-defect | 2 | PD-01 |
  | candidate-crash | 4 | PD-04 (C18) |
  | boundary-needs-prime-decision | 3 | a hold written inside a page is not shown |
  | needs-prime-judgment | 1 | |
  | vocabulary-gap | 1 | |
  | fixture-defect | 2 | my pass02 C05 fixture (FX-01) |
  | unsupported-by-mapping | 29 | the candidate does not output those fields |
  | pass-dependent-on-R1 | 3 | passes only because the shadow selector agrees with the canonical record |
  | incidental-pass / vacuous-pass | 1 / 2 | the count is met by other items, or the list is empty |
  | genuine-pass | 6 | 2 of them qualified |

- **Manual items:** the 24 are yours. Suggested evidence per item (references only, no answers):

  | Item | Look at |
  |---|---|
  | M-01 | `runs/C01/view.stdout` `/selected` with `/record/assignment_reader` |
  | M-02 | `/gaps` and `/coverage` |
  | M-03 | `/selected/next_route`: `{basis: unknown, source: null, speaker: null}` in every run with a selection, because no route source was declared; absent where nothing was selected (C05 main run) |
  | M-04 | C07/C10 `view.stdout` `/attention` (empty) |
  | M-05 | `probe-C05-final/runs/C05/packet.stdout` `/packet/director` and C09 `/workers/*/supplied` |
  | M-06 | read `view.stdout` rendered without `--json` (not produced here) |
  | F-* | each case's raw view against its `forbidden` list in pass02 `cases.json` |

## Successor rerun (contract only; not executed)
- **Selection:** a later run selects a candidate only by `--candidate <repo-relative path> --candidate-sha256 <hex supplied by Prime> --dependencies <manifest of {path, sha256}>`.
- **Allowlist:** an existing view/packet CLI under `labs/prime-desk-pass*/prime_desk.py`.
- **Execution:** copied by those hashes into a disposable pinned tree, never run in place.
- **Schema change:** a changed output schema needs an adapter revision (a new `ADAPTER_ID` and its own self-tests). The pass02 expectations stay as they are; a fact that a new schema cannot carry stays unsupported.
- **R1 (the shadow selector) must then be dropped.** If the successor reads the canonical record, the request carries the canonical record only, and C01 tests canonical selection directly.

## Interface questions for the successor (0524/05.02)
1. **Selection.** Is the selection taken from 0401/06.01 directly? Which output field names the selection's source path and sha256 (so `selected.source` maps)?
2. **Conflict.** Is a disagreement between any index, cache or legacy selector and the canonical record emitted as a typed item that names the work refs?
3. **Per-work facts.** Will the packet expose return, custody, review, disposition and approval as fields with a basis, or only as references? If only references, the C04/C06 assertions stay unsupported, and that coverage gap needs your acceptance.
4. **Holds.** Are holds read from the work page, or must they be catalogued in the request? (C07/C10)
5. **Foreign.** Will a cross-instance reference carry the path and a refusal or stale state?
6. **Quotes.** Director blocks with exact span and hash; model blocks with an author (PD-03).
7. **Malformed canonical record.** Handle the reader's `Stop` and report a refusal naming the schema rule (PD-04).
8. **Workers and parallel work.** A state with a basis, without parsing the supplied text.

## 0521/05.03 rehearsal: request plan and manual steps
- **The candidate rule blocks it.** pass01 expands a packet only for its own selector's work. Rehearsing 0521/05.03 would need the shadow selector to name 0521/05.03, which is exactly the custom-selector workaround the pack forbids. So the rehearsal waits for one of these:
  - a successor that selects from the canonical record; or
  - you making an explicit, attributed selection of 0521/05.03 in a **disposable** copy of 0401/06.01.
- **Request plan:**
  - **work:** 0521/05.03 and 0522/05.04;
  - **references** (all pinned in `pass02/rehearsal/0521-05.03/catalog.json`):
    - `assignment`: 0401/06.01;
    - `criteria` and `review-home`: 0521/05.03.md;
    - `return`: submission.md;
    - `deliverable`: artifact-manifest.json;
    - `verification`: return-lines-tests.stderr, rehearsal-report.json, pin-and-pointer-checks.json;
    - `finding`: 0522/05.03.md (RL-01);
    - `model`: 06.05.md;
  - **attention:** none declared, unless you catalogue RL-01.
- **Manual steps:** make the selection decision above; build the request (it can reuse `adapter.prepare_request` once the work and references are added); check against `expected-facts.json` by hand; answer M-01…M-06.
