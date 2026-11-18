# CONTRACT - 0512.prime-review/05.05 coherent report reads

date: 2026-11-03
executor: Grok-1
reviewer: Codex Prime
state: locked before code
accepted: false

This contract is the API, the ownership, the pins, and the delta from review-report/1. It is not revised after tests. A failing test is repaired in the lab or recorded as a limit. The schema names below stay. labs/review-report-pass01 stays byte-for-byte, including its known failures.

## Command

```
python -B labs/review-report-pass02/report.py --code-root ABS --book ABS --source PAGE --pass 05.NN
```

The process working directory may be the code root. The four flags are required. There is no force flag, no publish flag, and no record flag. Unknown flags, missing flags, a relative book, a relative code root, a linked book, a linked code root, or a source or pass that starts with `-` exit 2.

Stdout is one JSON object, schema review-report/2, indent 2, sort_keys, trailing newline, UTF-8, LF. The object contains the structured observation and the ordinary `projection` string of that same observation. Stderr is empty on exit 0 and exit 1. Exit 2 prints `refused: ...` on stderr and still prints the JSON object.

Exit 0: state `readable`. The bound cut stayed stable, the selected record was checked, and the core stale flag is false. Exit 0 is not approval, publication, custody, or release.

Exit 1: state `stale`, `held`, `not-recorded`, or `identity-mismatch`. The JSON report is still complete.

Exit 2: bad invocation, pin mismatch, linked pin, core stdout that is not one workbook-review-result/1 object, or a core process exit that disagrees with the JSON `exit` field.

The report process calls only inspect, read, and recover. It does not call prepare, form, record, publish, or approve. It does not write under the book, the code root, or the review store.

## Pins

Before any core call, every path pinned by labs/review-report-pass01/report.py is a regular file under `--code-root`, not a reparse point, at that module's exact size and sha256. A mismatch exits 2 and does not call the core. This contract does not add pass02 to the pin table and does not change pass01.

The core call is `python -B app/librarian.py review-loop {inspect|read|recover} --book ABS --source PAGE --pass 05.NN` with `PYTHONDONTWRITEBYTECODE=1`.

Neighbor, not a pin and not edited: app/README.md. The suite hashes it before and after the live reads and requires those two reads to match. labs/return-lines-pass04 is not imported.

## Observation

The reporter binds one cut, then runs the core, then checks the cut again.

1. Read `workbook-review/{page}/{pass}/journal.json` as a regular file. Bind `current`, the `record_sha256` on that current's reviews row, the raw sha256 of `reviews/{current}/record.json` when the file is present, and the publication identity. Publication identity is `publication` and `published_target`. Each block contributes `after_sha256`, `before_sha256`, `rendered_sha256`, `review_id`, `status`, and `target` when the value is a string.
2. Run inspect, then read, then recover.
3. Recheck the same binding. Read record metadata only when the recheck matches and the bound digest is the expected string.
4. Recheck again after the metadata read, and once more in `finish` immediately before the projection string is attached.

`checked_record` receives that bound digest as `expected`. It returns `digest-mismatch` before reading `record.json` when the reviews row has no `record_sha256`, when that value is not a string, or when that string differs from `expected`. A later journal digest is not a substitute for `expected`. Judgment and custody equality does not excuse a different digest.

When the recheck differs, state is `held`, `observation.stable` is false, `observation.status` is `unstable`, and `observation.changed` names the moved fields. Judgment, attention, custody, director text, and the other checked-record fields stay unexposed. `review_id` and `observation.bound` keep the bound cut. The later current is not selected. There is no second bind, no retry, and no adoption of a journal and record that match each other after the bind. `publication.class` is `unknown`. `publication.status` remains the bound status.

When the files stay still and the digest or the record hash fails the check, state is `held`, `observation.stable` is true, and `observation.status` is `mismatch`. Attention is `not-exposed`.

When the files stay still and inspect, read, and recover disagree on identity, page, pass, instance, or the command envelope, state is `identity-mismatch`. A judgment object that differs from the core is `identity-mismatch`. The newest reviews directory is not opened for selection.

A cut that is already coherent at the start of a later observation is that observation's measured cut. Its digest is the digest read at that start.

The limit, stored on `observation.limit` and copied into the ordinary projection, is:

This observation binds journal current, record digest, and publication identity, then runs inspect, read, and recover, then rechecks that binding before reading record metadata and again before the projection is attached. The reporter has no lock, no concurrency control, and no power-loss guarantee. A change that lands after the final recheck is outside this observation. A coherent change that is already stable at the start of a later observation is a new measured cut. A change during this observation stays out of the emitted judgment, attention, and custody.

Inspect, read, and recover still omit attention, prime_review_effective, and this bound token. The file recheck is the reader-side measurement. It is the whole of the guarantee this lab can establish from the current core.

## Identity and meaning

Pass01's page, pass, instance, and envelope rules stay. The envelopes `accepted`, `approved`, `authority`, `closes_work`, `releases_action`, and `task_association` are copied from inspect when read and recover agree. They are core statements.

Separate fields stay separate:

- `judgment_recorded` is true only after a stable checked record is shown
- `publication.class` is the publication class
- `custody` is the checked record custody, or null when that record is unexposed
- `work_complete` is the checked record's `eligible_for_custody_completion`
- `action_released` is the envelope `releases_action`

Null and a missing recoverable judgment are `unknown`. A stored empty list is `none-supplied`. The report does not invent findings, holds, or attention lines.

`tests_passed` null is unknown. A boolean is `supplied` with label `supplied bounded assessment`. `proof_of_all_tests` and `proof_of_requirements` stay false. `tests_note` and `limits` sit in their own fields beside it. Prose in `tests_note` is not a claim row and is not a count.

`claims.state` is `not-recorded`. `claims.rows` is empty. The limit text is the pass01 claim limit.

Publication class, when the observation is stable, uses the pass01 rules from inspect.publication and recover.target_state. Stale stays true when the core reports stale. State `stale` exits 1 and still shows the checked judgment. The historical judgment and the current intake stay distinct. A held hash mismatch is stale true. A not-recorded report has stale null.

`render_coverage` cites `workbook-review/{page}/{pass}/reviews/{id}/rendered.md` when an id is bound. The stored render is compared only for a checked record. The historical note stays: the stored render is the historical published bytes; this projection is a separate reader view and does not replace rendered.md.

## Counters

Artifact rows still come only from inspect `form.bindings.rows`. `measured_by` is `accepted-intake`. This report does not re-hash the files and does not create a missing path.

`artifacts.rows` lists every intake role row. The row keys stay path, role, root, sha256, bytes, declared_sha256, and declared_bytes. Role accounting stays on those rows.

Totals are unknown unless `measurement` is the string `complete` and `rows` is a list. Unknown totals are null, with `count_state` or `bytes_state` `unknown`. A null byte is not counted as zero. A partial sum is not a total.

When the measurement is complete:

- `artifacts.count` and `artifacts.bytes` are manifest-declared artifact entries. Scope `manifest-declared-artifact-entries`, provenance `declared`. An entry is a row whose role is exactly `artifact` and whose `declared_sha256` is a string and whose `declared_bytes` is an int. The byte total is the sum of `declared_bytes`. The count is known only when every artifact-role row has that declaration and no finding has code `artifact-missing` or `declared-file-missing`. Zero such rows and no payload-missing finding is count 0, bytes 0. A payload-missing finding makes the declared total unknown. Other finding codes do not.
- `artifacts.measured_artifact_rows` counts rows whose role is exactly `artifact`. Scope `current-measured-artifact-role-rows`, provenance `current-measured`. Bytes are the measured `bytes` values. A missing measured byte makes the byte total unknown.
- `artifacts.unique_files` counts physical files once. Scope `unique-physical-files`, provenance `current-measured`. Rows that share a `root` plus `path`, or that share one 64-character lowercase sha256, are one file. The byte total adds that file's measured byte size once. Conflicting sizes make the byte total unknown. A row with neither a path identity nor a sha256 makes the unique total unknown.
- `artifacts.intake_roles` counts every role row. Scope `full-intake-role-rows`, provenance `current-measured`. Its label is `intake role rows; not a declared artifact total`. Its bytes are the sum of role-row sizes, so overlapping roles remain visible there and do not increase `unique_files`.

`hash_match`, `hash_mismatch`, and `not_verified` on `artifacts` refer to artifact-role rows from the same intake. A row with no declared sha256 is not verified. A declared pair that equals the measured sha256 and bytes is a match. Anything else with a declared sha256 is a mismatch. The same three figures for every role row live under `intake_roles`. A missing submission or other non-payload finding is not a missing payload, not a mismatch, and not a verified payload.

`artifacts.missing` lists findings whose code is `artifact-missing` or `declared-file-missing`. `evidence_index.state` is `missing-referenced` when that list is non-empty, and `not-recorded` otherwise.

## Ordinary projection

`projection` is the ordinary view. It carries state, review id, observation status and stability, the selected digest, the five J/P/C/W/R fields, publication, stale, operation, disposition, terminals, authority, task association, tests_passed, tests_note, limits, every attention line, next action, Director words, holds, claims, the evidence index, the four counter lines, artifact integrity, the observation limit, and one detail line. The detail line names `reasons`, `findings`, `gaps`, `answers`, `sections`, `intake_findings`, `artifacts.rows`, `render_coverage`, `identity`, `observation`, and `interface_gap`. Those values stay in this JSON object. The historical sentence closes the projection. The projection is not a second copy of every detailed field.

## Interface gap and proposed integration

The gap text is the pass01 gap plus the missing bound token. The proposed later core change, for Prime to select, is to add attention, prime_review_effective, journal current, record digest, and publication identity from the same journal-checked record to inspect, read, and recover.

journal.current stays the selected id. publication.review_id stays the published id. Publish still requires rendered.md, record.rendered, and render_body(record) to match. before_sha256 and after_sha256 stay the own-pointer attestation. Historical renders stay valid under their recorded rendered_sha256. A formatter revision does not rewrite an old rendered.md. This pack does not edit the core, the dispatcher, the README, pass01, the live review, or any journal, and it does not migrate old records. Pass02 is not activated.

## Tests

The suite is labs/review-report-pass02/tests/test_report.py. It is author work. It is not an independent run. Retained books go to D:/librarian/temp/0512-0505-report. Failed trees stay. The known-failure directory written before this lab is left in place.

Known reproductions, labeled as pass01 failures rather than new coverage:

- the saved P1 result is ok and exposes UNVERIFIED SECOND-CUT ATTENTION
- the saved P2 result is count 4 and bytes 64
- a direct pass02 call rejects that different string with digest-mismatch before a missing record file can matter
- the four-role fixture's declared total is 1 entry and 4 declared bytes

Required successor cases:

- expected-digest mismatch with the same judgment and custody
- journal current changed during the core read
- publication identity changed while the current id stays
- record metadata changed during the observation
- four-role one-artifact counters
- overlapping roles and aliases
- missing submission beside a missing artifact
- null and unknown counts, including null tests_passed
- a selected historical judgment with stale current intake
- a cut that is already coherent before the observation is reported as that new cut

Two new author hostile cases, not independent and not the known reproductions:

- a newer reviews directory is not selected and its text stays absent
- a journal and record that are rewritten into a new matching pair during the observation are not adopted

Also: usage and pin refusal, core commands limited to inspect/read/recover, a no-write hash of the fixture book, the final recheck inside finish, pass01 and the frozen live bytes unchanged, two live processes on 0522.review-construction/05.13, and one observation of 0512.prime-review/05.04 review weffe9a51780b52b3. The 05.04 observation is not a product pass. The 05.13 read keeps the bounded tests_note, the six agreement attention lines, disposition accepted, custody missing, and authority unresolved. If that source is stale, the report says so. This suite does not repin it. This suite does not rerun the broad core suites.

## Return schemas

verification.json schema is review-report-verification/2. It records accepted false, allocated not used, committed_by_this_builder false, custody pending, matching line 0112.prime-review unfiled, receipt null, and seated false. It may record the submission sha256. It does not record the artifact-manifest sha256.

artifact-manifest.json schema is review-report-artifact-manifest/2. It lists files with path, bytes, and sha256. It excludes itself. It omits 05.05.md. file_count is not a second authority. There are no directory rows.

submission.md does not carry the artifact-manifest hash. That hash is written only on the 05.05 Return pointer.

## Ownership

This builder writes only labs/review-report-pass02/, 06.07.md, evidence/build05.05/, retained books under D:/librarian/temp/0512-0505-report, and the 05.05 Return pointer after submission and the manifest exist. The pointer replace is the first `## Return pointer\nPENDING.\n` only. The Review line stays PENDING. The state line stays `state: PREPARED; execute on named Director invocation; staged successor only`.
