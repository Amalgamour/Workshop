# CONTRACT - 0512.prime-review/05.06 file-count identity

date: 2026-11-03
executor: Grok-1
reviewer: Codex Prime
state: locked before code
accepted: false

This contract is the counter API for review-report/3. It is not revised after tests. A failing test is repaired in the lab or recorded as a limit. labs/review-report-pass02 stays byte-for-byte, including the known identical-file failure. This pack does not reopen the digest repair.

## Command

```
python -B labs/review-report-pass03/report.py --code-root ABS --book ABS --source PAGE --pass 05.NN
```

The process working directory may be the code root. The four flags are required. There is no force flag, no publish flag, and no record flag. Unknown flags, missing flags, a relative book, a relative code root, a linked book, a linked code root, or a source or pass that starts with `-` exit 2.

Stdout is one JSON object, schema review-report/3, indent 2, sort_keys, trailing newline, UTF-8, LF. The object contains the structured observation and the ordinary `projection` string of that same observation. Stderr is empty on exit 0 and exit 1. Exit 2 prints `refused: ...` on stderr and still prints the JSON object.

Exit 0: state `readable`. The bound cut stayed stable, the selected record was checked, and the core stale flag is false. Exit 0 is not approval, publication, custody, or release.

Exit 1: state `stale`, `held`, `not-recorded`, or `identity-mismatch`. The JSON report is still complete.

Exit 2: bad invocation, pin mismatch, linked pin, core stdout that is not one workbook-review-result/1 object, or a core process exit that disagrees with the JSON `exit` field.

The report process calls only inspect, read, and recover. It does not call prepare, form, record, publish, or approve. It does not write under the book, the code root, or the review store. The file counters do not stat, list, open, or hash the intake paths.

## Pins

Before any core call, every path pinned by labs/review-report-pass01/report.py is a regular file under `--code-root`, not a reparse point, at that module's exact size and sha256. A mismatch exits 2 and does not call the core. This contract does not add pass03 to the pin table and does not change pass01 or pass02.

The core call is `python -B app/librarian.py review-loop {inspect|read|recover} --book ABS --source PAGE --pass 05.NN` with `PYTHONDONTWRITEBYTECODE=1`. `core_call` stays a module global on the pass03 module. `observe` and `main` copy that global onto the loaded pass02 module before the pass02 observation runs.

Neighbor, not a pin and not edited: app/README.md. The live pair hashes it before and after and requires those two reads to match. labs/return-lines-pass04 is not imported.

## Observation

Pass02 owns the selected-digest guard and the observation binding. Pass03 loads that module and does not replace `checked_record`, `read_cut`, `finish`, or the observation limit.

`checked_record` returns `digest-mismatch` before reading `record.json` when the reviews row has no `record_sha256`, when that value is not a string, or when that string differs from the expected digest.

A change to journal current during the core calls leaves state `held`, `observation.stable` false, `observation.status` `unstable`, and attention `not-exposed`. `review_id` stays the bound id. The later current is not selected.

`finish` rechecks the bound cut immediately before the projection is attached. A change found there withholds the judgment and the attention lines.

The limit text stays:

This observation binds journal current, record digest, and publication identity, then runs inspect, read, and recover, then rechecks that binding before reading record metadata and again before the projection is attached. The reporter has no lock, no concurrency control, and no power-loss guarantee. A change that lands after the final recheck is outside this observation. A coherent change that is already stable at the start of a later observation is a new measured cut. A change during this observation stays out of the emitted judgment, attention, and custody.

J/P/C/W/R stay separate. `authority` stays the core envelope. `claims.state` stays `not-recorded`. `tests_passed` null stays unknown. A boolean stays `supplied` with label `supplied bounded assessment`, and both proof flags stay false. The historical render note stays. The proposed core exposure stays the pass02 sentence. This pack does not add a physical-identity field to the core.

## Row totals

Artifact rows still come only from inspect `form.bindings.rows` after the pass02 row projection. `measured_by` is `accepted-intake`. The kept row keys stay path, role, root, sha256, bytes, declared_sha256, and declared_bytes. `declared_path` is not an identity.

Totals below are unknown unless `measurement` is the string `complete` and `rows` is a list. A null byte is not counted as zero. A boolean is not an int. A partial sum is not a total.

When the measurement is complete:

- `artifacts.count` and `artifacts.bytes` are manifest-declared artifact entries. Scope `manifest-declared-artifact-entries`, provenance `declared`. An entry is a row whose role is exactly `artifact` and whose `declared_sha256` is a string and whose `declared_bytes` is an int. The byte total is the sum of `declared_bytes`. The count is known only when every artifact-role row has that declaration and no finding has code `artifact-missing` or `declared-file-missing`. Zero such rows and no payload-missing finding is count 0, bytes 0.
- `artifacts.measured_artifact_rows` counts rows whose role is exactly `artifact`. Scope `current-measured-artifact-role-rows`, provenance `current-measured`. A missing measured byte makes the byte total unknown.
- `artifacts.intake_roles` counts every role row. Scope `full-intake-role-rows`, provenance `current-measured`. Its label is `intake role rows; not a declared artifact total`. Its bytes are the sum of role-row sizes.

`hash_match`, `hash_mismatch`, and `not_verified` on `artifacts` refer to artifact-role rows from the same intake. The same three figures for every role row live under `intake_roles`. A missing submission or other non-payload finding is not a missing payload.

`artifacts.missing` lists findings whose code is `artifact-missing` or `declared-file-missing`.

`artifacts.unique_files` is absent. Scope `unique-physical-files` is not emitted.

## File identities

Three counters replace `unique_files`. They read the kept rows only.

`artifacts.addressed_sources` counts exact `(root, path)` pairs. Scope `addressed-source-paths`, provenance `current-measured`. Both values must be strings. The pair is the exact root string plus the exact path string. There is no slash folding, no case folding, and no dot-segment resolution. Repeated roles on one pair are one addressed source. The same path string under two root strings is two addressed sources. The byte total adds that address's measured byte size once when every row of the address has the same int `bytes`. The assumption string is `exact root string plus exact path string; no slash folding, no case folding, and no dot-segment resolution`.

The addressed total is unknown, count and bytes both null, when measurement is not the string `complete`, when `rows` is not a list, or when any row lacks a string root or a string path. The reasons are:

- `measurement is not complete, so addressed-source identity is not established`
- `intake rows are absent, so addressed-source identity is not established`
- `a row lacks a root string or a path string, so the addressed-source total is not completed from the other rows`

Identified rows are not summed when another row lacks a path identity. When the count is measured and the sizes of one address disagree, or a byte is not an int, the count stays measured and the bytes are unknown. The reason is `rows of one addressed source do not agree on one int byte size`. A complete empty row list is count 0, bytes 0, and the reason key is absent.

`artifacts.content_blobs` counts 64-character lowercase sha256 values. Scope `content-sha256`, provenance `current-measured`. A hash proves content equality only. It does not union addressed sources and it is not a physical-file identity. The byte total adds that hash's measured byte size once when every row with that hash has the same int `bytes`. The assumption string is `a 64-character lowercase sha256 proves content equality only`.

The content total is unknown, count and bytes both null, when measurement is not complete, when `rows` is not a list, or when any row lacks a 64-character lowercase sha256. Uppercase hex is not folded. The reasons are:

- `measurement is not complete, so content-blob identity is not established`
- `intake rows are absent, so content-blob identity is not established`
- `a row lacks a 64-character lowercase sha256, so the content-blob total is not completed from the other rows`

Rows that do have a hash are not reported as a partial content total. When the count is measured and the sizes of one hash disagree, the count stays measured and the bytes are unknown. The reason is `rows of one content hash do not agree on one int byte size`. A complete empty row list is count 0, bytes 0, and the reason key is absent.

`artifacts.physical_files` is unknown on every report, including a complete empty row list. Scope `verified-physical-files`, provenance `not-established`, count null, bytes null, both states `unknown`. The reason is `accepted intake metadata has no physical-file identity; a path and a content hash do not establish one`. There is no assumption key. The counter does not claim a hard link and does not probe the filesystem.

On the disclosed two-file fixture, measurement complete, pass03 reports addressed count 2 and bytes 8, content count 1 and bytes 4, and physical unknown. Declared count is 0 because neither row has role `artifact`. Intake role rows are count 2 and bytes 8. Preserved pass02 still reports unique_files count 1 and bytes 4 on that fixture. That pass02 result remains the known failure.

On the four-role fixture in evidence/prime-review05.04/independent-artifact-count.json, the rows have four distinct paths and four distinct hashes. Pass03 reports declared count 1 and bytes 4, measured artifact rows count 1 and bytes 4, intake role rows count 4 and bytes 64, addressed count 4 and bytes 64, content count 4 and bytes 64, and physical unknown. Those equal addressed and content counts are four paths and four hashes. They are not a verified physical-file total.

## Ordinary projection

The pass02 projection stays, with the `unique_files` line replaced by three lines in this order: `addressed_sources`, `content_blobs`, `physical_files`. Each line uses `count`, `bytes`, `provenance`, and `scope`. A reason is appended only when the counter carries a reason string. Declared, measured, and intake lines stay in their pass02 wording. The detail line and the observation limit stay. The projection does not contain `unique_files:` or `unique-physical-files`.

## Tests

The suite is labs/review-report-pass03/tests/test_report.py. It is author work. It is not an independent run and it is not a rerun of Prime's suite or of the pass02 suite. Retained books go to D:/librarian/temp/0512-0506-report. The known-failure file written before this lab stays in place.

The known-failure case reloads pass02 and checks count 1 and bytes 4 against the retained file. The author cases cover two distinct equal-content paths, repeated roles on one root and path, the same relative path in different roots, a missing path identity, identical hashes without paths, distinct contents, null measurements, unnormalized path strings, a size disagreement, digest mismatch before a missing record read, a journal-current change during read, a finish recheck, the four-role row totals, a refusal that does not call the core, and counters that do not stat. One live pair reads 0522.review-construction/05.13 only. It requires the six attention lines, the bounded tests_note, custody missing, authority none, work_complete false, and action_released false. It requires the physical counter to stay unknown. It does not require a numeric physical-file total. A stale core result is reported as stale. The pair must match. The live review bytes and app/README.md must match before and after. The reader does not record, publish, or approve.
