# Contract delta — colab review report preservation (0518.colab-review 05.02)

Written before the code, for the PR-01, PR-02, and PR-03 repair. The 05.01 contract remains the original and is not rewritten. This delta states only what the repair changes. The adapter still validates declared plans, links, and results. It does not launch a model or a reviewer, does not authenticate isolation, and does not judge meaning.

## 1. What stays

- Commands stay `stage`, `bind`, `intake`, and `synthesize`. Exits stay 0 clean, 1 answered with findings or mismatch, 2 refused, 3 partial.
- `colab-review-plan/1`, `colab-review-binding/1`, `colab-review-result/1`, and `colab-review-synthesis/1` keep their keys.
- `incomplete` on intake and on synthesis stays the required reviewer/stage list. A required pair that is absent, failed, partial, or not-run is in that list. It is never counted as zero findings.
- Intake `status` is `complete` only when `findings` is empty and `incomplete` is empty. Otherwise it is `incomplete`.
- Synthesis mapping checks are unchanged: plan id, intake sha256, each original finding id once, known disagreement ids, `incomplete` equal to the intake list, and `acceptance` null. Report `status` is `consistent` only when those mapping findings are empty. That status is mapping consistency. It does not clear intake diagnostics, and it is not acceptance.
- `report_digest` is still the sha256 of the canonical report object before that field is inserted. Stored `/1` reports are not rewritten, and their digests are not recomputed.
- Pinned producer, helper, and inspector bytes stay the 05.01 pins. Capture and inspect tools stay byte-exact.
- A member with no `review-result.json` still reads as `legacy-no-result`. A package with no plan still binds as `legacy-no-review-plan`.

## 2. Intake `colab-review-intake/2`

New intake files use this schema. Every 05.01 field remains, with the same meaning. One field is added.

`stage_status` is one row per declared reviewer/stage, in plan stage order and then that stage's reviewer order:

```
{"reviewer", "stage", "required": bool, "status": "completed"|"partial"|"failed"|"not-run"|"absent",
 "member": str|null, "receipt_sha256": str|null}
```

`absent` means no accepted result for that pair. `member` and `receipt_sha256` are null in that case. A present result keeps its own status, member name, and receipt.

Optional pairs are in `stage_status` and are not added to `incomplete`. An optional failed, partial, not-run, or absent pair does not by itself make intake `status` incomplete.

## 3. Report `colab-review-report/2`

`synthesize` writes this schema. The 05.01 report fields remain. These fields are added:

- `intake_findings`: the intake `findings` list, object for object, including a context-mismatch and its declared plan and result context.
- `stage_status` and `stage_status_note`: copied from a `/2` intake. On a `/2` intake the note is null.
- `distinctions`: `{"mapping": "consistent"|"inconsistent", "required_review": "complete"|"incomplete", "acceptance": null}`. `mapping` equals report `status`. `required_review` equals `intake_status`. `acceptance` is null.

`findings` on the report remains the synthesis mapping findings only. Intake diagnostics are not moved into that list and are not dropped when the mapping list is empty.

`REPORT.md` keeps the 05.01 header line (`Status`, `Intake`, and the digest domain). The domain is `colab-review-report/2`. The next line states mapping consistency, required review, and acceptance separately. Sections, in order:

- Comprehension, verbatim, as before.
- Consolidated items. Each original prints its text, target, location, member, and receipt. The text is the supplied wording.
- Retained. The id, disposition, duplicate target, and reason stay on the first line. The following lines print `text`, `target`, `location`, and `custody` (member and receipt). The text is the supplied wording. A retained id with no original on the intake says `not on this intake` and does not invent a sentence.
- Disagreements, as before.
- Incomplete reviewers. This section is the required list only. It says so. An empty required list prints `none`.
- Reviewer stages. Every `stage_status` row prints reviewer, stage, required or optional, status, and member plus receipt, or `absent` when no member was captured. A line states that optional status does not by itself change required review completion.
- Intake diagnostics. When required review is incomplete, the section says the investigation is incomplete and that a consistent mapping does not resolve these diagnostics. Each intake finding is printed as one JSON object. An empty list prints `none`.
- Residual uncertainty, as before.
- Mechanical findings, only when the synthesis mapping list is non-empty.

Reporting an incomplete intake is allowed. Synthesize still exits 0 when the mapping list is empty, and the intake status and intake findings remain in the report.

## 4. Old intake files

`synthesize` accepts `colab-review-intake/1` and `colab-review-intake/2`.

- A `/1` intake has no `stage_status`. The report sets `stage_status` to null and `stage_status_note` to `not recorded: intake is colab-review-intake/1 and has no reviewer/stage inventory`. The reviewer-stage section prints that sentence. No optional or required row is invented.
- A `/1` intake's `findings` list is still copied to `intake_findings`.
- A `/2` intake must include `stage_status` as a list of rows with the keys in section 2. A missing list, a bad row, or a status outside the five values is a refusal. The file is not repaired.
- Both schemas must carry `findings` as a list. The list may be empty.

Synthesis input stays `colab-review-synthesis/1`. The author does not supply `stage_status` or `intake_findings`. Those are derived. `incomplete` must still equal the required intake list exactly.

## 5. Out of scope

No new plan mode, no multi-return workflow, no semantic scorer, and no change to producer or custody schemas. Original 05.01 evidence and capture 0179 are not rewritten. Prime review evidence is not rewritten.
