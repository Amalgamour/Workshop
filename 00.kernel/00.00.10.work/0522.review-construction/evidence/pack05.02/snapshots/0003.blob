# Contract — review-construction/1

Date: 2026-10-31. Author: Grok-2. This contract is written before `labs/review-construction-pass01`. It is the interface that lab implements. A rendered review is not approval, acceptance, release, closure, or custody.

## Roles

Intelligence supplies the `prime-review-record/1`: outcome, finding, reasons, dissent (`design_fork`), findings, limits, questions, Director replies (`answers`), and next action. Compute checks shape by calling pinned `labs/prime-review-pass01/prime_review.py report --json`, then supplies headings, order, required lines, and source hashes. Missing judgment stays missing. Unknown keys are refused. `closes_work`, `releases_action`, and `authenticates_actor` stay false.

The lab does not import `desk_lab.py`, `prime_cycle.py`, `return_capture.py`, `return_inspect.py`, or `labs/return-placement-pass01`. It does not edit them.

## Command

From `D:\Git\lib-build`:

```text
python -B labs/review-construction-pass01/construct.py preview --fixture-root ABS --input REL
python -B labs/review-construction-pass01/construct.py apply --fixture-root ABS --input REL
python -B labs/review-construction-pass01/construct.py bind --fixture-root ABS --input REL
python -B labs/review-construction-pass01/construct.py show --fixture-root ABS --target REL
```

`--input` and `--target` are relative to the fixture root, or absolute paths that resolve inside it. The fixture root must be an absolute directory outside `D:\Git\lib-build`. Preview is the default write behavior: `preview` and `bind` and `show` create no files. `apply` is the only writer, and only inside that root.

Exit 0 means the command completed. Exit 2 means refused, with `refused:` on stderr. A held or incomplete judgment can still render; `prime_review_exit` in the result carries the report exit. That exit is not acceptance.

## Envelope

Schema `review-construction/1`. Exact keys:

`schema`, `source_kind`, `page`, `pass`, `target`, `expect_sha256`, `permit_create`, `review_identity`, `task`, `evidence`, `agreement`, `receipt`, `record`.

- `source_kind` is `N5NN` or `N7NN`. Any other kind, including `N1NN`, `N2NN`, `N3NN`, `N4NN`, and `N6NN`, is refused.
- N5NN `page` matches `00.kernel/00.00.10.work/05NN.subject/05.NN.md`. `pass` equals that `05.NN`. `target` basename equals `05.NN.md`.
- N7NN `page` matches `00.kernel/00.00.10.work/07NN.subject/05.NN.pack.md`. The review file is the existing tail `06.NN.review.md`. `target` basename must be that name. No N1NN path is written or allocated.
- `expect_sha256` is 64 lowercase hex, or `absent` when the target file is absent.
- `permit_create` is true only to create that absent file. The created file is the review heading plus the assessment. It does not invent assignment text.
- `task` keys: `task_id`, `assignment_path`. The assignment file is the immutable task text.
- `evidence` is a list of `{logical_path, label}`. `label` is `synthetic` or `supplied`.
- `agreement` has exactly `goal`, `scope`, `prime_discretion`, `director_required`, `finish_criteria`, `recorded_decisions`.
- `receipt` keys: `placement`, `member`, `page_local`, `submission_id`, `receipt_path`, `return_path`, `manifest_path`, `status`, `label`.
- N5NN placement is `n5nn-matching-line`. `member` matches `01NN.subject`. `page_local` is null. The member string is a declared descriptor. This lab does not create it.
- N7NN placement is `n7nn-page-local`. `member` is null. `page_local` is `05.NN.return.md`.
- `status` is `complete`, `reserved`, `incomplete`, or `refused`. It is rendered as declared status. It does not prove custody.
- `label` is `synthetic` or `supplied`.
- `record` is a `prime-review-record/1` object. Its agreement equals the envelope agreement. Its sources cover the assignment, each evidence path, and the return bytes. An N5NN record has one `return-capture/1` identity whose member, submission id, and `receipt_sha256` equal the hashed receipt file. A null receipt hash is a mismatch.

There is no `verified` or `custody_ok` field. An extra key is refused.

## Readable review

On an existing target, exactly one heading is accepted, as bytes:

- `## Review — Codex Prime` (U+2014)
- `## Review - Codex Prime` (hyphen-minus)

Zero headings, or more than one, is a refusal. The heading line stays. Bytes before it and bytes from the next `## ` heading onward stay. The section body is replaced only when it is the placeholder `PENDING` or `PENDING.`, or when it already equals the new render.

The body states authority none, the three false flags, `task_binding`, `record_sha256`, `agreement_sha256`, receipt hashes, `custody: not-established`, and `allocated: false`. It quotes finding, reasons, dissent, Director reply text, next action, agreement, findings, and check notes. It then includes the `prime_review` report markdown. Null judgment is written as none supplied. The typed record is stored on apply at `support/<review_identity>/record.json` inside the fixture. That file is the record's bytes. The review cites its sha256.

Compute's own blocks use level-3 headings, and each heading line in the pinned report is nested two levels down. A level-2 heading inside the new body would be the next page section, so a rendered body that contains one is refused and nothing is written. The report wording is unchanged.

UTF-8 is required. A BOM, a NUL, invalid UTF-8, or mixed CR/LF is refused with no write. A file that is entirely LF, or entirely CRLF, keeps that newline. Only the new section body uses the file's newline. Created files use LF and the U+2014 heading.

## Writes

`expect_sha256` must equal the target bytes immediately before a change. A stale hash is refused and the target stays. Identical render with the current hash is idempotent: exit 0, `written` false, target bytes unchanged. A different substantive section is a conflict: the target stays, history is not overwritten, and apply saves the unused render under `partial/` inside the fixture. The refusal asks for an explicit successor process.

Apply writes a temporary sibling, fsyncs, rereads the target hash, then renames. If the target changed after the first read, the temporary file stays and the target stays. This compare-then-rename narrows a stale write. It is not proof of race freedom. Same-user processes can still rewrite files. No OS sandbox is claimed.

## Task binding

Schema `review-task-binding/1`. Canonical JSON, UTF-8, sorted keys, compact separators. The sha256 covers `task_id`, assignment sha256 and length, evidence path/sha256/length/label sorted by path, agreement sha256, and the receipt identities (placement, member, page-local name, submission id, status, label, and receipt, return, and manifest hashes and lengths).

It does not cover the review text, the record bytes, or the target file hash. Rendering a review must leave this digest unchanged. Changing assignment bytes, an evidence file, the agreement, or the receipt bytes must change it. `bind` does not read the target.

## Adapter after 0521

This constructor consumes an explicit return descriptor and the three byte files it names. It does not reserve, capture, migrate, discover, or scan members. After Prime reviews the 0521 placement migration, a later adapter may fill this descriptor from matching line `0122.review-construction` for source `0522.review-construction`, using the placed receipt bytes. N7NN stays page-local. That adapter is not this lab. Until that migration is reviewed, custody of this assignment's own handback remains pending. The old sequential allocator is not used.

## Result

Success stdout is one JSON object. `preview`, `apply`, and the idempotent replay use schema `review-construction-result/1` with keys `schema`, `result`, `written`, `source_kind`, `page`, `pass`, `binding_sha256`, `agreement_sha256`, `record_sha256`, `review_sha256`, `target_sha256_before`, `target_sha256_after`, `prime_review_exit`, `effective`, `supplied_outcome`, `receipt_check`, `custody`, `placement`, `member`, `allocated`, `race_limitation`, and `review`. `result` is `preview`, `applied`, or `idempotent`. `bind` returns schema `review-task-binding/1` with `binding_sha256`, `binding`, and `target_read` false. `show` returns schema `review-construction-show/1` with `binding_sha256`, `section_sha256`, and `section`.
