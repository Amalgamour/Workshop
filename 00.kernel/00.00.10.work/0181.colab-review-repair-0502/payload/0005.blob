# Prime use — colab review report preservation (05.02)

For Codex Prime. This is the reading guide for the repaired lab adapter. The 05.01 guide still describes stage, bind, intake, and the workflow route. This page says what the derived report now keeps. Commands run from `D:/Git/lib-build`. Every `--out` is a new folder.

## What changed

Three facts stay separate.

- Mapping consistency is report `status`: `consistent` or `inconsistent`. It only says whether the supplied synthesis maps the original finding ids and echoes the required incomplete list. An empty mapping list does not clear an intake error.
- Required review is the intake status: `complete` or `incomplete`. It is complete only when the intake findings are empty and every required reviewer/stage completed. A context mismatch keeps it incomplete even when no required reviewer is missing.
- Acceptance is never recorded here. The report says `Acceptance: none.` A synthesis that sets acceptance is refused.

Optional reviewer/stage status is visible and does not by itself change required review. Absent, failed, partial, and not-run optional pairs stay in `stage_status`. They are not added to `incomplete`.

## How to read the report

`synthesize` writes `report.json` (`colab-review-report/2`) and `REPORT.md`.

- `intake_findings` is the intake finding list, unchanged. `## Intake diagnostics` prints each object. When required review is incomplete, that section says a consistent mapping does not resolve the diagnostics.
- `incomplete` is still required pairs only. The Markdown says so.
- `## Reviewer stages` lists every declared pair: required or optional, status, member, and receipt, or `absent` when no result was captured.
- Consolidated items and retained findings quote the supplied text, target, location, and custody (member and receipt). The wording is not rewritten.
- `## Mechanical findings` appears only for synthesis mapping findings.

`report_digest` is the sha256 of the canonical report object before that field is added. The digest domain is `colab-review-report/2`. A stored `colab-review-report/1` file is not recomputed.

## Commands

The route is unchanged:

```text
python -B labs/colab-review-pass01/colab_review.py stage      --plan ABS --request ABS --repo ABS --out-request ABS
python -B labs/colab-review-pass01/colab_review.py bind       --output ABS --config ABS --producer ABS --expect-digest HEX --out ABS [--plan ABS]
python -B labs/colab-review-pass01/colab_review.py intake     --binding ABS --plan ABS --book ABS --member NAME [...] --config ABS --out ABS
python -B labs/colab-review-pass01/colab_review.py synthesize --intake ABS --synthesis ABS --out ABS
```

New intake files are `colab-review-intake/2` and include `stage_status`. The synthesis file stays `colab-review-synthesis/1`. Copy `incomplete` from the intake. Do not supply `stage_status` or `intake_findings`; the adapter derives them.

A stored `colab-review-intake/1` still synthesizes. The report sets `stage_status` to null and says the inventory was not recorded. It does not invent optional rows. It still copies that intake's findings.

## Checks

The lab suite is:

```text
python -B -X dev labs/colab-review-pass01/tests/test_colab_review.py -v
```

This repair's run is recorded in `verification.json`. The new tests reconstruct the three preserved probes (context mismatch, optional failed, retained original text), a normal successful report, required missing and required failed reviewers, and optional absent, partial, and not-run reviewers. They also synthesize a `/1` intake and refuse a `/2` intake that drops `stage_status`. Reviewer results in those tests are synthetic. No model is launched.

## Limits

- The adapter does not judge meaning, authenticate isolation, or decide acceptance.
- The workflow still places one return per pass. Other results stay in N1 custody, and intake reads the members it is given.
- Optional status is not a required-completion gate. A failed optional stage can sit beside a complete required review. The stage line is the record.
- `demo.py` and `tests/fixture.py` were not changed and were not re-run as a separate demo.
- Producer, helper, inspector, workflow, app code, kernel law, the 05.01 capture, and the Prime review evidence were not edited.
- This guide does not release the adapter for routine use. Prime reviews the repair. A verified receipt is custody.
