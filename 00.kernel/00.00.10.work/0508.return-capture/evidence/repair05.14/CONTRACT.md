# CONTRACT — batch-observation repair (0508.return-capture 05.14)

Recorder: Grok Builder 2. Date: 2026-10-28.
This contract is written before the repair code. It corrects BO-01 through BO-04. It does not replace the captured 05.13 bytes in `0138.batch-reader-0513`. The reader remains `batch-observation/1`. It still grants no release, acceptance, closure, or seat. `parse_source` stays the pinned file and its object is copied unchanged.

## 1. Eligible source fields (BO-01)

`document.header_state_raw`, `assignment.executor_raw`, `assignment.release_raw`, and `assignment.claim_raw` are filled only from lines that are outside fences, outside blockquotes, and inside an eligible section. The fence rule is the same rule `parse_source` uses, including a longer outer fence around a shorter inner fence. A blockquote is a line whose text after leading spaces or tabs starts with `>`.

| field | eligible sections | line starts with |
|---|---|---|
| header state | header, before the first heading | `state:` |
| executor | Assignment (`## Assignment` or a level-2 title that starts with `Assignment`) | `Executor:` |
| release | header, Assignment, or a return-family pointer section | `Release:` or `Release and claim:` |
| claim | header, Assignment, or a return-family pointer section | `Claim:` |

A fenced example, a blockquote, a line in any other section, and prose that merely contains the label do not populate the field. Each kept line is stored with its original 1-based line number.

Each field also stores its line list. When the list has one line, the raw value is that line. When the list is empty, the raw value is null. When the list has more than one line, the raw value is null, `ambiguous` is true, and the observation records `duplicate-header-state`, `duplicate-executor`, `duplicate-release`, or `duplicate-claim`. The first line is not selected.

## 2. Declarations (BO-02)

`--declaration` is optional. A well-formed `batch-review-declaration/1` object is copied with `authority: not authenticated`. `review.binding` stays `unbound`. No terminal or closure field is created.

Before any membership test or hash test, each of `reviewed_member`, `reviewed_receipt_sha256`, `reviewed_disposition`, and `reviewer` must be a string. A list, object, null, boolean, or number refuses. Duplicate keys, non-finite constants (`NaN`, `Infinity`), malformed JSON, a missing or extra key, and an unknown schema refuse. Refusal is exit 2, empty stdout, and a short stderr reason. It is not a traceback. No observation document is emitted.

## 3. Live time (BO-03)

UTC timestamps use a `Z` suffix.

- A `--live` read sets `source.time_basis` to `live-read` and sets `source.live_observed_at`, `source.observation_started_at`, and `source.observation_finished_at` to the read interval.
- A Git blob sets `source.time_basis` to `git-blob`. Those three time fields are null. The named commit stays the commit. The live time is not written back onto it.
- Supplied text sets `source.time_basis` to `supplied-text` and the same three fields null.
- Each inspector launch sets `observation_started_at` and `observation_finished_at` on the custody observation. The inspector JSON object and the exit code stay the inspector's own values. Those timestamp fields are not inserted into the inspector object.
- `custody.package_at_commit` remains `not-established`.

## 4. Reservation fixture (BO-04)

The suite must pass while `0138.batch-reader-0513` is still reservation-only and after that member is sealed. The reservation-only assertion uses a disposable book created by the pinned reserve command and left uncaptured. The test records that the live `0138` directory, whatever it contains, is unchanged. It does not delete a receipt or rewrite an old test record.

Existing behavioral cases stay: sixteen corpus pages, six controls, fenced headings, singular and plural pointers, archive pointers, primary after a foreign historical member, conflicting receipts, two same-origin candidates, cross-book origin, missing, partial, reserved, review text, and pin refusal before Git or inspect.

## 5. Demo and limits

The demo shows one page whose fenced release is ignored and whose actual claim is kept, then one malformed declaration that refuses. The reader is not imported by the state-projection lab. This repair writes the reader lab, `06.15.md`, `evidence/repair05.14/`, and the `05.14` return pointer only.
