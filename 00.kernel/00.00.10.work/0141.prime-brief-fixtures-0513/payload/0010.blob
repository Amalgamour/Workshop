# CONTRACT — SP-05 repair and prime-brief-pass01 (0507.prime-support 05.13)

Author: claude-opus-5-5. Date: 2026-10-28. Fixture only. Standard library only.
`projection05.12/CONTRACT.md` stands unless this file amends it. This is not a seated schema, registry, law or lane change.

## A. SP-05 amendment to state-projection-pass01

1. **Retrospective flag.** A `complete` inspector report must carry `capture.retrospective` as a JSON boolean. A missing or non-boolean value is `observation: failed`.
2. **Retrospective captures are never candidates.** A complete member whose origin book, page and batch match is a candidate only when `retrospective` is `false`. A same-origin capture with `retrospective: true` is listed under `secondary`, with `"historical": "same-origin retrospective"`. It never counts toward ambiguity.
3. **Explicit historical candidate.** If the explicit `candidate` is a same-origin retrospective capture, custody is `candidate-historical`, and the lifecycle is `conflict-candidate` with the attention item "declared candidate is a retrospective (historical) capture". It is never primary, and never completes.
4. **No other change.** Lifecycle, exits and the input schema are unchanged. The 17 existing tests are unchanged.

## B. prime-brief-pass01

```text
python -B prime_brief.py brief --input IN.json [--inspect] [--json]
```

| exit | meaning |
|---|---|
| 0 | brief produced, with no attention items and nothing unprojected |
| 1 | brief produced, with attention items or unprojected batches |
| 2 | refused: invalid input or a pin mismatch; no brief |

- Output goes to stdout only. The tool writes no file.
- **The projection.** It is loaded from `../state-projection-pass01/state_projection.py`, only after its sha256 equals the constant `PROJECTION_SHA256` in the code. The projection then applies its own inspector and helper pins.
- **No overrides.** There are no caller tool paths and no reader launch or import.

### B1. Input `prime-brief-input/1` (strict: exact keys, no duplicate keys, no NaN)

```text
{schema: "prime-brief-input/1",
 scope: {book, lanes[]},
 members_book: ABS | null,
 observations: [{label: "SYNTHETIC" | "SUPPLIED" | "DERIVED-FROM-RETAINED-SUMMARY", note: STR,
                 observation: <batch-observation/1 object, the subset in B2>}],
 coordination: [{label: "SUPPLIED", batch_id, source_sha256: HEX64,
                 release: recorded | pending | absent | unknown,
                 claim: recorded | pending | absent | unknown, claim_actor: STR | null,
                 candidate: MEMBER | null,
                 review: null | {member, receipt_sha256, disposition: accepted | held | correction-required,
                                 terminal: completed | null, reviewer, followup},
                 publication: {status: unknown | at-ref, ref, commit}}]}
```

### B2. Reader fields the adapter reads, from Grok-2's reader05.13 contract

The adapter reads only these fields, and checks each one's type before use:
- `schema` (`batch-observation/1`), `authority`;
- `source` {kind, repository, path, commit, sha256, bytes, label};
- `page` (null, or {book, page, batch});
- `document.header_state_raw`;
- `assignment` {executor_raw, release_raw, claim_raw};
- `legacy` {status, reason, revision_id};
- `pointers` [{line, form, members [{name}]}];
- `assignment_mentions` [{member}];
- `custody` {basis, primary, observations [{member, role}]};
- `review` {sections [{text_raw}], text_raw, binding, typed_declaration};
- `ambiguities` [str] and `attention` [str].

Other keys are kept as raw data but not read. A wrong type in a read field refuses the whole input.

### B3. Mapping to state-observations/1, one batch at a time

| target | rule |
|---|---|
| `id`, `lane`, `batch` | from `page`; `page.book` must equal `scope.book` and `page.page` must be in `scope.lanes`, or the input is refused |
| `provenance` | source.kind `git-blob` maps to `supplied-commit`, with `commit` = source.commit and `page_sha256` = source.sha256, labelled SUPPLIED (not verified). `live` maps to `supplied-live`. Any other kind goes to **unprojected**, with reason "schema gap: no commit/live basis for source kind …". |
| `document.header_state` | `header_state_raw`, verbatim |
| `release`, `claim` | **only** from the coordination record bound to `batch_id` and `source_sha256`. A missing record, `unknown`, or a sha mismatch goes to **unprojected**. The raw `release_raw` and `claim_raw` are kept as evidence and never used. |
| `return.pointer` | no pointer gives `absent`; a pointer with members gives `present`; a pointer with no members gives `pending`. A reader ambiguity code containing `pointer` gives `ambiguous`. |
| `return.members` | the member names from pointers, in first-seen order, unique. Assignment mentions are excluded. |
| `return.candidate` | coordination `candidate` only. The reader's `custody.primary` is never used. |
| `review` | a coordination `review` gives `bound`, with that binding. Otherwise: reader `text_raw` that is exactly `PENDING.` after trimming gives `pending`; any other non-empty text gives `text`; no section gives `absent`. `typed_declaration` never binds. |
| `publication` | from coordination; otherwise `unknown` |

**Refused** (exit 2): duplicate coordination for one batch; coordination for a batch with no observation; duplicate observation ids.

### B4. Output `prime-brief/1`

- `inputs`: each observation's label, note, source reference and `observation_sha256` (canonical JSON hash).
- `mapping`: per batch, the field decisions and the raw evidence kept.
- `projection`: the full `state-projection/1`, or null when nothing was projectable.
- `reader_custody_snapshots`: the reader's earlier custody roles, labelled `earlier reader observation`.
- `brief`: these lists, each item `{id, source_ref, lifecycle, reason, followup}`:
  - `awaiting_review`: `returned-awaiting-review`;
  - `correction_or_held`: `open-held` and `open-correction-required`;
  - `completed_fixtures`: `completed`, labelled "derived fixture label; not approval or release";
  - `conflicts`: `conflict-*`;
  - `other_open`: every remaining open lifecycle (`open-re-review-required`, `open-review-unresolved`, `open-candidate-ambiguous`, `open-accepted-not-terminal`, `open-commit-custody-unverified`, `claimed`, `released`);
  - `unprojected`: with its reason;
  - `unreleased`: `unreleased`.
- `authority`: `none; a brief selects, releases, accepts and dispatches nothing`.

## C. Expected results, written before the harness

| # | case | expected |
|---|---|---|
| E01 | returned fixture, live, a real complete current member, no review | `awaiting_review` |
| E02 | bound held with a follow-up | `correction_or_held`, with the follow-up kept |
| E03 | bound accepted terminal on a real current member, live | `completed_fixtures` |
| E04 | text-only "Accepted within scope" | `other_open` (`open-review-unresolved`) |
| E05 | a reader `release_raw` from a fenced example, with no coordination | `unprojected` (release unknown); the raw line kept as evidence; never `released` |
| E06 | coordination `release: unknown` | `unprojected` |
| E07 | bound review with a stale receipt | `other_open` (`open-re-review-required`) |
| E08 | two current complete members, no candidate | `other_open` (`open-candidate-ambiguous`) |
| E09 | current plus same-origin retrospective, in both pointer orders | primary is current; the retrospective one is secondary; accepted terminal gives `completed_fixtures` |
| E10 | the sole same-origin retrospective member, with an accepted terminal | not completed: custody `none`, lifecycle `open-review-unresolved` |
| E11 | the explicit candidate is retrospective | `conflicts` (`conflict-candidate`) |
| E12 | decision bound to a different `source_sha256` (changed source) | `unprojected` |
| E13 | a git-blob source with accepted terminal and live custody complete | `other_open` (`open-commit-custody-unverified`); live inspections kept separately |
| E14 | published held | `correction_or_held`; publication shown, not closing |
| E15 | multiple lanes with open items | all listed; nothing selected |
| E16 | a DERIVED-FROM-RETAINED-SUMMARY fixture (0508/05.10, legacy unsupported, revision null) | revision stays null in mapping evidence; it projects from coordination only |
| E17 | malformed input, unknown versions, duplicate keys, NaN, bad nested types, out-of-scope lane | exit 2, no brief |
| E18 | projection hash drift, or inspector or helper drift | exit 2 before any launch |
| E19 | stdout is UTF-8 with non-ASCII; the inputs, member book, labs and Git are unchanged | yes |
