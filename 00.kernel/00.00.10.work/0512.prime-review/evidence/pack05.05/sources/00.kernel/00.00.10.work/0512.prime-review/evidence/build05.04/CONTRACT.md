# CONTRACT - 0512.prime-review/05.04 review projection

date: 2026-11-03
executor: Grok-1
reviewer: Codex Prime
state: locked before code
accepted: false

This contract is the API, the ownership, the pins, and the delta. It is not revised after tests. A failing test is repaired in the lab or recorded as a limit. The schema names below stay.

## Command

```
python -B labs/review-report-pass01/report.py --code-root ABS --book ABS --source PAGE --pass 05.NN
```

The process working directory may be the code root. The four flags are required. There is no force flag, no publish flag, and no record flag. Unknown flags, missing flags, a relative book, a relative code root, a linked book, a linked code root, or a source or pass that starts with `-` exit 2.

Stdout is one JSON object, schema review-report/1, indent 2, sort_keys, trailing newline, UTF-8, LF. The object contains the structured observation and the `projection` string of that same observation. Stderr is empty on exit 0 and exit 1. Exit 2 prints `refused: ...` on stderr and still prints the JSON object.

Exit 0: state `readable`. The selected record is recoverable and the core stale flag is false. Exit 0 is not approval, publication, custody, or release.

Exit 1: state `stale`, `held`, `not-recorded`, or `identity-mismatch`. The JSON report is still complete.

Exit 2: bad invocation, pin mismatch, linked pin, core stdout that is not one workbook-review-result/1 object, or a core process exit that disagrees with the JSON `exit` field.

The report process does not write under the book, the code root, or the review store. It does not call prepare, form, record, or publish.

## Pins

Before any core call, every path below is a regular file under `--code-root`, not a reparse point, at the exact size and sha256. A mismatch exits 2 and does not call the core.

| Path | bytes | sha256 |
|---|---:|---|
| app/librarian.py | 12204 | c3a5be3b612c021d95effaa5da4a151bf89026422b94f4cad98331014c7f0cd9 |
| app/review_loop_tools_v7.py | 10291 | 93a89939b6e6143eaffbb75c3b7cb60c38c60ad91902bd15d0b48c5bb35c382d |
| app/review-loop-v7.json | 3515 | bf12aa7cdf67cc6f8e6ae9d674aa39929933293495c6857dc423dab4c1cab8f8 |
| app/review_loop_tools_v6.py | 9175 | e2a5df36efe29f9dad8abd8fa0f842fd98941d58ca1eb3cd4be5227e20420a94 |
| app/review-loop-v6.json | 2743 | c7f95d16f91644c6465fd3483e3db4d6fb9b9115aa6e20fc09a194fc5bb1f0aa |
| app/review_loop_tools_v5.py | 7875 | b1192daf5d265c66f10adfe2125ff0c92a08ccd3c797d229698ecc20e2fdeed9 |
| app/review-loop-v5.json | 1964 | eaa9120bba2c7274f2218c875ec3ecfc84d291188557049240c30a1c2a430de3 |
| app/review_loop_tools_v4.py | 13381 | 0769179366a6c1659f38cb2c79c51981d5cb76fa8d48ee7325f9eaf00d14c296 |
| app/review-loop-v4.json | 2519 | 769f81321e19a9f3296020e3b0b4a4905ec1b3a66c1629bf53d9548b7182d723 |
| labs/workbook-review-pass03/workbook.py | 19533 | 9e66d7e4413e8f0aedcc4ff416080c549ce435b10103149ef73de493b245ff8c |
| labs/workbook-review-pass03/forms/workbook-review-v1.json | 4532 | 4b8cf0e8c81cc421fd0212ae169ba1557998bf526c5f6d87ee170c9d038cbb0b |
| labs/workbook-review-pass02/workbook.py | 52574 | 6ce4a5ff2e7505a8b56a13c05af3f5f2e9d8648112a6bf67c0e6392ab043a49a |
| labs/workbook-review-pass02/forms/workbook-review-v1.json | 4532 | 66b3f8f70f8e5d2f940296918767ff0e712e7e144378ad8653259e83d3284645 |
| labs/workbook-review-pass01/workbook.py | 79131 | 60e040fa30f61348adac76a4f3bdfbfdb9aba859f25bacadf317937c167e9b0a |
| labs/workbook-review-pass01/forms/workbook-review-v1.json | 4532 | 152b436bda8e19d15f252bb5208791c8eefd9a658789e2ab6e9789ffa362b49f |
| labs/return-access-pass01/return_access.py | 26561 | 501d40d7c7b08720d3ae061441284ac26d544e7b80100059b2ddce25f67358f5 |
| labs/review-loop-pass03/review_loop.py | 55474 | 47f47d16426e4d69987398a8244877de58b6089326874f3279003f696814450b |
| labs/review-construction-pass04/construct.py | 42582 | 6d541d4225ed0f9ccdb6263b475a79f55e4312be80a7e9a810a3622e5bd8df20 |
| labs/prime-cycle-pass03/prime_cycle.py | 76045 | 496b4d721cfb136fa847d998d421209616c60508beb5cda5620af73041eed17c |
| labs/prime-review-pass02/prime_review.py | 58560 | 80836a13278365de863ed8231cb8118ad14ddbad672dd02ec2ebf69beff3b44e |

Neighbor, not a pin and not edited: app/README.md sha256 3c2125aa0cebd7ddc1604de2a823c1250edf40a8e97bd7dbd2eb09ca91155920, 39687 bytes. The suite asserts that neighbor is unchanged. labs/return-lines-pass04 is not imported.

The core call is `python -B app/librarian.py review-loop {inspect|read|recover} --book ABS --source PAGE --pass 05.NN` with `PYTHONDONTWRITEBYTECODE=1`.

## Identity

The selected id is the journal current id, never the newest directory name.

1. Run inspect, then read, then recover.
2. Require each stdout to be one object, schema workbook-review-result/1, whose `command` matches and whose `exit` equals the process code.
3. Require the same `page`, `pass`, and `instance_id` on all three. `page` must equal `--source` and `pass` must equal `--pass`.
4. Command envelopes `accepted`, `approved`, `authority`, `closes_work`, `releases_action`, and `task_association` are copied from inspect. They are core statements. If read or recover disagrees on those keys, state is `identity-mismatch` and no judgment is displayed.
5. If read and recover both exit 2 with correction `No recorded judgment.` and omit `review_id`:
   - inspect.current null: state `not-recorded`. Judgment fields stay unknown.
   - inspect.current a string: state `held`. The id is reported. Judgment, holds, attention, and custody stay unknown. Inspect's empty holds list is not "none supplied".
6. Otherwise inspect.current, read.review_id, and recover.review_id must be the same string. Any other disagreement is `identity-mismatch`.
7. Read `workbook-review/{page}/{pass}/journal.json` only as a measured check. It must be a regular file, schema workbook-review-journal/1, and `current` must equal the agreed id. The reviews row supplies `record_sha256`.
8. Read `reviews/{id}/record.json` only when its raw sha256 equals that `record_sha256` and its `judgment` object equals recover.judgment and inspect.judgment. Only then are attention, prime_review_effective, custody, successor_of, eligible_for_custody_completion, and the stored render taken from that file. Custody must also equal recover.custody.
9. If the hash differs, or the judgment objects differ, do not display the file and do not display inspect.judgment. State `held` when the hash differs. State `identity-mismatch` when the ids disagreed or the judgment objects disagree. Attention state is `not-exposed`. The withheld text is not quoted.

A newer reviews directory is not opened for selection.

## Meaning

Null and a missing recoverable judgment are `unknown`. A stored empty list is `none-supplied`. The report does not invent findings, holds, or attention lines.

`tests_passed` null is unknown, not passed, and not the render line `tests_passed: none supplied`. A boolean is `supplied` with label `supplied bounded assessment`. `proof_of_all_tests` and `proof_of_requirements` stay false. `tests_note` null is unknown. A string is copied verbatim.

`limits` null is unknown. Any other JSON value is supplied verbatim.

Director text null on a checked record is `none-measured`. A string is verbatim Director words. Answer replies are verbatim selected replies. The supplied finding is the supplied judgment. Those three stay labeled apart from each other. `successor_of` is copied from the checked record.

`goal_terminal` and `pass_terminal` come from the checked judgment. `work_complete` is the checked record's `eligible_for_custody_completion`. It is unknown when the record is not checked. `action_released` is the core envelope `releases_action`. Disposition accepted does not set either flag.

`custody` comes from the checked record. It is unknown when the record is not checked. The word missing stays missing.

Publication class, from inspect.publication and recover.target_state when recover ran:

- no selected id and state not-recorded: `not-recorded`
- status `pointer-pending` or target_state `pointer-pending`: `blocked`
- status `recorded` or status absent while an id exists: `recorded`
- status `published` and target_state `verified` or `section-verified`: `complete`
- status `published` and target_state `missing`, `bytes-changed`, `marker-missing`, or `heading-unreadable`: `partial`
- otherwise: `unknown`

Stale stays true when the core reports stale, including source drift after a complete publication. The judgment stays. Stale is not cleared. State `stale` exits 1 and still shows the recoverable judgment. A held or hash-mismatch record is stale true. A not-recorded report has stale null.

Intake findings stay intake findings. Judgment findings stay judgment findings.

## Evidence

Artifact rows come only from inspect `form.bindings.rows`. `measured_by` is `accepted-intake`. This report does not re-hash the files.

- count: number of rows
- bytes: sum of integer row byte counts
- hash_match: rows whose declared sha256 and declared bytes are both present and equal the measured values
- hash_mismatch: rows whose declared sha256 or declared bytes are present and differ
- not_verified: rows with no declared sha256
- missing: intake findings whose code is `artifact-missing` or `declared-file-missing`

`measurement` is the inspect measurement string. Incomplete stays incomplete.

`claims.state` is `not-recorded`. `claims.rows` is an empty list. The limit is: the selected record has no structured claim, case, run, or result rows. Prose in tests_note is not parsed into a pass.

`evidence_index.state` is `missing-referenced` when a missing finding exists, and the finding code and path are listed. Otherwise it is `not-recorded`. The report does not create the missing file.

`render_coverage` cites `workbook-review/{page}/{pass}/reviews/{id}/rendered.md` when an id is selected. A value is shown by the render only when its exact text occurs in the stored render of a hash-matched record. The historical render line for tests_passed is recorded separately and is not a second judgment. Omitted names include a supplied tests_note, any attention line, a supplied limits value, and any gap string that is absent. The projection is a reader view. It does not replace rendered.md.

Ordinary projection text includes state, review id, publication class, stale, custody, operation, disposition, terminals, work_complete, action_released, authority, task_association, the tests_passed value and label, the tests_note verbatim, limits, every attention line, next action, Director words, holds, claims, evidence index, and the compact artifact counts. Detailed projection in the same string includes reasons, both finding lists, gaps, non-null sections, replies, successor_of, artifact rows, render omissions, and the interface gap. No silent cut and no padding word count.

## Interface gap and proposed integration

Inspect, read, and recover do not return `attention` or `prime_review_effective`. This lab's hash-checked record read is the staged bridge. The proposed later core change, for Prime to select, is to add those two fields to inspect, read, and recover from the same journal-checked record revalidate already hashes.

A later formatter may call this same projection to supply inspect and publish display. journal.current stays the selected id. publication.review_id stays the published id. Publish still requires rendered.md, record.rendered, and render_body(record) to match. before_sha256 and after_sha256 stay the own-pointer attestation. Historical renders stay valid under their recorded rendered_sha256. A reader selects the renderer whose output matches that hash. A formatter revision does not rewrite an old rendered.md and does not make an old review look corrupt. New publishes may record projection schema review-report/1 beside the render. This pack does not edit the core, the dispatcher, the README, the live review, or any journal, and it does not migrate old records.

## Tests

The suite is labs/review-report-pass01/tests/test_report.py. It is author work. It is not an independent run and it is not a known-failure reproduction. Retained books go to D:/librarian/temp/0512-0504-report. Failed trees stay.

Cases:

- coverage: tests_passed true, tests_note, and limits supplied; the note appears in the projection; the stored render omits the note
- attention: disposition accepted, custody missing, prime_review_effective attention, and the six agreement lines
- unknown-coverage: tests_passed, tests_note, and limits null stay unknown
- hold-reply-successor: Director verbatim, a supplied hold, a supplied reply, and successor_of on the selected id
- blocked-publication: pointer-pending publication, class blocked, judgment preserved, exit 0
- source-drift: published record, later artifact byte change, stale true, class complete, finding preserved, exit 1
- changed-record: altered record.json is not displayed; attention not-exposed; exit 1
- missing-record: deleted record.json is held; findings unknown; exit 1
- another-book: a second book with the same page id is a different instance_id and not-recorded
- missing-evidence: a declared missing path is missing-referenced and is not created
- hostile-newer-folder: an extra reviews directory is not the selected id and its finding text is absent
- hostile-prose-pass: tests_note that says independent and all tests passed leaves claims.rows empty and both proof flags false

The live observation is a separate pair of processes on book D:/Git/lib-build/00.kernel/00.00.10.work, source 0522.review-construction, pass 05.13. It must report w4c5ae945c250d823, the six attention lines, the bounded tests_note, disposition accepted, and custody missing. The two projections match. Journal, record.json, rendered.md, judgment.json, intake.json, and 05.13.md are hashed before and after and must be unchanged. The live page is observation, not approval.

Raw hostile stdout is saved under the KEEP tree on the author run. A first-run product failure stays in that tree.

## Return schemas

verification.json schema is review-report-verification/1. It records accepted false, allocated not used, committed_by_this_builder false, custody pending, matching line 0112.prime-review unfiled, receipt null, and seated false. It may record the submission sha256. It does not record the artifact-manifest sha256.

artifact-manifest.json schema is review-report-artifact-manifest/1. It lists files with path, bytes, and sha256. It excludes itself. It omits 05.04.md. file_count is not a second authority. There are no directory rows.

submission.md does not carry the artifact-manifest hash. That hash is written only on the 05.04 Return pointer.

## Ownership

This builder writes only labs/review-report-pass01/, 06.05.md, evidence/build05.04/, retained books under D:/librarian/temp/0512-0504-report, and the 05.04 Return pointer after submission and the manifest exist. The pointer replace is the first `## Return pointer\nPENDING.\n` only. The Review line stays PENDING. The state line stays `state: PREPARED; execute on named Director invocation; staged outputs only`.
