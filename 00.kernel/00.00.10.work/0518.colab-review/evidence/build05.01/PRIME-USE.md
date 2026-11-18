# PRIME-USE — Colab review adapter (0518 05.01)

For Codex Prime. This is one minimal preparation and reporting walk on a real investigation; the demo runs the same walk on a disposable book. Commands run from `D:/Git/lib-build`. Every `--out` is a new folder.

**Reading order:**
1. this page;
2. `CONTRACT.md`: §2 plan, §5 result, §7 synthesis;
3. `sample-review.json`;
4. `labs/colab-review-pass01/README.md`.

## Prepare

1. **Write the plan,** `colab-review-plan/1` (CONTRACT §2):
   - mode, reviewers with their declared context (conversation supplied, host context, familiarity, isolation);
   - stages (comprehension, critique, simplicity, implementation), each with reviewers and `required`;
   - `ordered`, read scope, withholds, finish boundary;
   - for a simplicity stage, its before and after and the fixes under review;
   - the round and cap.

   Only the stages you need: a small fix may be one critique stage.
2. **Write the base `colab-request/2`** as usual. Its targets are in a source repository that the config names, and its `mode` is one of the producer's four.
3. **Stage, then prepare:**
   ```text
   python -B labs/colab-review-pass01/colab_review.py stage --plan PLAN --request BASE --repo SOURCE_REPO --out-request REQUEST
   python -B labs/colab-support-pass02/colab_support.py preview --request REQUEST --config CONFIG --json      (copy "digest")
   python -B labs/colab-support-pass02/colab_support.py prepare --request REQUEST --config CONFIG --output OUT --digest DIGEST --json
   python -B labs/colab-review-pass01/colab_review.py bind --output OUT --config CONFIG --producer D:/Git/lib-build/labs/colab-support-pass02/colab_support.py --expect-digest DIGEST --out BINDING --plan PLAN
   ```
   **Expected:** `bind` reports `status: bound`, with four review files `equal: true`.
   - `--repo` must be a repository outside the workshop tree. `stage` commits there with a task-local identity, and never touches the global git config.
   - For live use, Prime chooses that source repository.
4. **Open and attach** with workflow v2, as before. Reserve one member per (reviewer, stage), with `--expected-output review-result.json`.

## Report

5. **Each reviewer's return** comes back with `review-result.json` (`colab-review-result/1`; a template is in the package). Capture each with producer `intake ... --artifact "review-result.json|review-result.json"`. Place one return with workflow `place-return`.
6. **Intake:**
   ```text
   python -B labs/colab-review-pass01/colab_review.py intake --binding BINDING/binding.json --plan PLAN --book BOOK --member M1 --member M2 ... --config CONFIG --out INTAKE
   ```
   - `complete` only when every required (reviewer, stage) completed and nothing mismatched.
   - Absent, failed, partial and not-run results are listed in `incomplete`. They are never counted as zero findings.
7. **Write the synthesis,** `colab-review-synthesis/1`:
   - items that consolidate findings;
   - every other finding retained as dissent, minority, rejected-with-reason or duplicate-of;
   - disagreements;
   - the intake's incomplete list, exactly;
   - residual uncertainty;
   - `acceptance: null`.
8. **Synthesize:**
   ```text
   python -B labs/colab-review-pass01/colab_review.py synthesize --intake INTAKE/intake.json --synthesis SYNTH --out REPORT
   ```
   `REPORT.md` is derived, and quotes the originals and the paraphrases verbatim. Then write your `colab-exchange-review/1` and run workflow `record-review`, as before.

## Known manual work

- Writing the plan, the base request, the synthesis and the review record.
- Choosing which member to place.
- Copying the preview digest.
- Reserving one member per (reviewer, stage).

## Compatibility and digests

- **Unchanged:** `colab-request/2`, `colab-package-digest/2`, the producer verification and handoff, the workflow records and schemas, and the custody schemas. No preimage changes. The review files are ordinary package sources, so producer verify covers their bytes; `bind` adds only presence and equality with the plan.
- **New:** `colab-review-plan/1`, `-binding/1`, `-result/1`, `-intake/1`, `-synthesis/1` and `-report/1`. The report's `report_digest` is the sha256 of the canonical `report.json` without that field.
- **Old data:** a package with no plan binds as `legacy-no-review-plan`, and a member with no `review-result.json` reads as `legacy-no-result`. Neither is an error.

## Limits

- The workflow places one return per pass. Other reviewers' returns stay in N1 custody, and `intake` reads them all.
- The readiness checker was used only as a declared-record check of the exact package bytes: read-only, with no smoke. It establishes no semantic quality.
- The two-reviewed-pass elevation and the design-judgment stop rules are unchanged; nothing here elevates or decides.
- Labels are not authentication. There is no OS sandbox or race safety.
