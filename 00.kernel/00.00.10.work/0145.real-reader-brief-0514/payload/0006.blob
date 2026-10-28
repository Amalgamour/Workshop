# CONTRACT — PB-08, PB-09 and PB-10 repair; real reader to brief rehearsal (0507.prime-support 05.14)

Author: claude-opus-5-5. Date: 2026-10-28. Fixture lab plus one read-only rehearsal. `brief05.13/CONTRACT.md` stands unless this file amends it. The projection is pinned and unchanged (b349da5c…).

## A. Consumer repair in prime_brief.py

**A1. PB-08: required keys and types, before use.** Every consumed key must be present, and must be either the stated type or explicit null where that is allowed. All of this is checked before any lookup, hash, set membership, projection load or subprocess.

| object | required keys (type) |
|---|---|
| observation entry | `label` (str, one of the labels), `note` (str), `observation` (object) |
| observation | `schema` == `batch-observation/1`, `authority` == `none`, plus `source`, `page`, `document`, `assignment`, `legacy`, `pointers`, `assignment_mentions`, `custody`, `review`, `ambiguities` and `attention` |
| `source` | `kind` (str), `repository` (str or null), `path` (str), `commit` (hex40 or null), `sha256` (hex64), `bytes` (int), `label` (str or null), `time_basis` (str or null), `live_observed_at`, `observation_started_at` and `observation_finished_at` (str or null) |
| `page` | null, or exactly {`book`, `page`, `batch`} (str) |
| `document` | `header_state_raw` (str or null) |
| `assignment` | `executor_raw`, `release_raw` and `claim_raw` (str or null) |
| `legacy` | `status`, `reason` and `revision_id` (str or null) |
| `pointers[]` | `members` (list of {`name`: str}) |
| `assignment_mentions[]` | `member` (str) |
| `custody` | `basis` (str or null), `primary` (str or null), `observations` (list of {`member`: str, `role`: str or null}) |
| `review` | `sections` (list of {`text_raw`: str or null}), `text_raw` (str or null), `binding` (present), `typed_declaration` (present) |
| `ambiguities`, `attention` | lists of str |

Extra producer keys are kept as data and never read. A failure exits 2 with `refused: …`, and no traceback, projection or launch.

**A2. PB-09: source kinds.**

| source.kind | maps to | notes |
|---|---|---|
| `git-blob` | `supplied-commit`, with commit and page_sha256 | supplied; the adapter did not read Git |
| `live-file` | `supplied-live`, with page_sha256 | `live_observed_at` and the observation start and finish times are kept in the mapping evidence |
| `supplied-text` | **unprojected**: "schema gap: supplied text has no commit or live basis" | never recast as live |
| any other value, including the old synthetic `live` | **unprojected**: "schema gap: no commit/live basis for source kind X" | the old fixtures are updated to `live-file` |

**A3. PB-10: pointer ambiguity, from named reader codes only.** `return.pointer` is `ambiguous` when the reader's `ambiguities` contain `unknown-return-heading`, or its `attention` contains `conflicting-stated-receipts`, `unparsed-member-line` or `unpaired-receipt`. These codes come from batch_observe.py 8bea1817…. No other substring rule applies. `assignment-mention-not-pointer` does not make a pointer ambiguous.

**A4. Member form.** A pointer member that doesn't match the projection's `01NN.name` form makes the batch unprojected ("member name outside the projection's member form"). The input is not refused.

**A5. Reader codes on brief items.** Each projected brief item shows the reader's ambiguity and attention codes for that batch.

## B. Rehearsal harness `evidence/realbrief05.14/rehearse.py`

- **Inputs.** source-spec.json, coordination.json and coordination-provenance.json, read as given. There is no HEAD or latest-commit discovery.
- **Pins, before launch.** batch_observe 8bea1817…, prime_support 700d60d2…, clerk_adapter 2f30ba75…, inspector 947915fe…, helper 8f3da5c6…, brief (its final hash, recorded) and projection b349da5c…. Each is checked against the hash the code embeds, and the pack lists every pin except the brief's final hash.
- **Reader calls.** One per page: `[sys.executable, -B, labs/batch-observation-pass01/batch_observe.py, observe, --json, --repo, D:/Git/lib-build, --commit, <spec commit>, --path, <page>, --members-book, D:/Git/lib-build/00.kernel/00.00.10.work]`, with no shell. Exact stdout, stderr, exit and the start and end times are kept.
- **Adapter input.** Built from the unchanged parsed reports (the hash of the stdout bytes is recorded), labelled SUPPLIED, plus coordination.json byte-for-byte as its records. The record that the harness ran the pinned reader is separate.
- **Brief.** Run once with `--inspect --json` and once as text, using fresh live custody through the projection's pinned inspector.
- **Outputs.** `results.json` holds the raw reports (exact text), the inputs, the adapter input, the full brief JSON, outcomes, provenance, errors and timing. `brief.txt` is the readable brief. No other file is written.
- **Not done.** No queue, capture, model call or dispatch. Members are only inspected, never changed.

## C. Expected results for the real rehearsal, written before the run

| page | expected |
|---|---|
| 0504.app-entry/05.17 | `correction_or_held` (`open-held`), follow-up 0504.app-entry/05.18, provided the reader names 0139 in a pointer and the live receipt matches. Otherwise unprojected or other_open, with the reason shown. |
| 0508.return-capture/05.15 | `other_open` (`open-accepted-not-terminal`): accepted, terminal null, not completed |
| 0507.prime-support/05.12 | `correction_or_held` (`open-held`), follow-up 0507.prime-support/05.13 |
| 0504.app-entry/05.18 | `unprojected`: release and claim unknown |
| 0508.return-capture/05.16 | `unprojected`: release and claim unknown |
| all | nothing in `completed_fixtures`; publication shown and never closing; authority none; the source and book unchanged |

Any difference from this table is reported, not tuned away.

## D. Integration tests: real producer, disposable Git and book

| # | case | expected |
|---|---|---|
| R01 | live-file report on a titled page, a complete original capture, supplied coordination with no review | mapped unchanged (same canonical sha as the reader stdout); `supplied-live`; `awaiting_review` |
| R02 | git-blob report of the same committed page, accepted terminal | `supplied-commit`; `other_open` `open-commit-custody-unverified` |
| R03 | supplied-text report | `unprojected` (schema gap) |
| R04 | the pointer names a same-origin retrospective and a current member, in both orders | primary current; the retrospective one is secondary |
| R05 | coordination receipt stale | `open-re-review-required` |
| R06 | coordination source sha stale (the page changed after the decision) | `unprojected` |
| R07 | conflicting stated receipts for one member | pointer `ambiguous`, and the reader code shown |
| R08 | real `PENDING.` review section, no decision | review `pending`; `awaiting_review` |
| R09 | accepted without terminal | `open-accepted-not-terminal` |
| R10 | a page with an assignment mention only | pointer not ambiguous (PB-10) |
| V01-V10 | list or dict labels; a missing document, assignment, source or custody key; wrong nested types; unknown schemas; NaN and duplicate keys | exit 2; projection not loaded; no subprocess |
| M01 | the fixture repository, book and Git refs around the reader and brief runs | unchanged |
