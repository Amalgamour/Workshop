# CONTRACT — prime-cycle-pass01 (0515.prime-cycle 05.01)

Author: claude-opus-5-5. Date: 2026-10-30. Standard library only. This is an experimental lab adapter: no seat, no route, no app wiring, no canonical-state migration. The design is 0415.prime-cycle/01.md.

## 1. Commands and exits

```text
python -B labs/prime-cycle-pass01/prime_cycle.py read     --registration ABS [--json] [--templates DIR]
python -B labs/prime-cycle-pass01/prime_cycle.py record   --registration ABS --decision ABS
python -B labs/prime-cycle-pass01/prime_cycle.py inspect  --registration ABS --work ID
python -B labs/prime-cycle-pass01/prime_cycle.py packet   --registration ABS --work ID --out DIR
```

| command | 0 | 1 | 2 | 3 |
|---|---|---|---|---|
| read | view, no attention | view, with attention | refused | — |
| record | review committed, or an identical replay (no-op) | committed, and prime_review reports a hold or attention | refused; nothing written | a write failed after the review directory was created (partial left as it is) |
| inspect | every review directory committed | partials or stale bindings present | refused | — |
| packet | review_packet assembled | — | refused, or review_packet exit 2 | — |

**Outputs.** Output is UTF-8. `read` writes nothing unless `--templates` is given. `--templates` writes one template file per work, `template-<work_id>.json`, with an exclusive create, under `output_root` only. `record` writes only inside the work's declared review location.

## 2. Registration `prime-cycle-registration/1` (strict JSON; exact keys; no duplicate keys or NaN)

```text
{schema, repository: ABS, book: "00.kernel/00.00.10.work" (relative), book_label: LABEL,
 source: {kind: "git-blob", commit: HEX40} | {kind: "live-file", commit: null},
 members_book: ABS | null, output_root: ABS,
 bounds: {max_works 1..16, max_page_bytes 1..262144, max_output_bytes 1..2097152},
 works: [{work_id: LABEL, page: REL, pass: "05.NN", member: MEMBER | null,
          goal: {goal_id: LABEL, statement: STR},
          agreement: <prime-review-record/1 agreement object>,
          review_location: REL}]}
```

- `page` must be `<book>/<lane>/<pass>.md`.
- `review_location` must lie under `<book>/<lane>/evidence/`, so it is work-local. It must not be a face file or a page, and it must not be in another lane.
- Relative paths: forward slashes; no `..`, empty segment, drive or colon.
- Absolute paths: no UNC. Links and reparse points on an existing path refuse.
- `output_root` must be outside every `review_location`.
- Work ids are unique.
- `goal_sha256` is the sha256 of the UTF-8 goal statement. Changing the statement or the id is a new goal.

## 3. Pinned dependencies (each checked before use; a mismatch refuses and launches nothing)

| file | sha256 | how used |
|---|---|---|
| `labs/batch-observation-pass01/batch_observe.py` | `8bea18171b723650e8c0b07f5de334d2c5fd004c5d65c4fa8c4b85cf0bc830d4` | `observe --json --repo R (--commit C | --live) --path P [--members-book B]` |
| `labs/return-capture-pass01/return_inspect.py` | `947915febaa5918f56b6be03c81840c030d081fcab9a3bead2cd660973a9999b` | through the reader, which checks it again |
| `labs/return-capture-pass01/return_capture.py` | `8f3da5c651f6924fca6dedb0b95da7d181eb58884dc030dd9cbc3d8b6a5b15ac` | the inspector's helper, used through the inspector |
| `labs/prime-review-pass01/prime_review.py` | `805995a1…` (full value in code) | `report --input F --json`, `check-next --input F --json` |
| `labs/review-packet-pass01/review_packet.py` | `f658cbe4…` (full value in code) | `assemble --request F`, only on `packet` |

Every launch is `[sys.executable, "-B", tool, …]`, with no shell and a timeout. No other subprocess. **Not invoked:** prime_brief, state_projection and desk_state. The unsupported mappings are in §9.

## 4. read

For each work, in registration order:
1. Run the reader at the source basis, with `--members-book` when it is set. Keep exit, stdout sha256 and stderr. Exit 2, an unparsable report, or a page over the bound gives `observation-failed`; nothing is invented.
2. Custody comes from the reader: `custody.primary`, plus each named member's role, inspection status, origin, retrospective flag and receipt. A primary is accepted only when the reader's role is `primary-current-candidate`.
3. Read the work's review location. Directories are review ids. For each:
   - **committed:** `COMMITTED.json` is present, and its record and REVIEW hashes equal the files;
   - **partial:** COMMITTED is missing, or the hashes mismatch;
   - **invalid:** record.json is unreadable or not in the schema.
   The lineage follows `supersedes`. The latest committed review is the one no other committed review supersedes. More than one such head gives `lineage-fork`, which is attention. Nothing is chosen by time or name.
4. **Derived state:**
   - `pass_state`:
     - `no-return`: no member, or no primary;
     - `awaiting-review`: a primary and no committed review;
     - `reviewed`: the latest review binds the current page sha, member and receipt;
     - `review-stale`: the latest review binds a different page sha or receipt. Re-review is required, and the old review stays visible.
   - `disposition`, `pass_terminal` and `outcome`: copied from the latest review (`unknown` if none).
   - `goal_terminal`: `completed` only if the latest review declares it for the current goal_id and goal_sha256. If it declared completion for another goal, `open (prior completion bound to goal X)`. Otherwise `open`, or `unknown`.
   - `holds`: from the latest review's prime_review report, with status and dependent scope.
   - `next_action`: from the latest review, with its author label, review id and record sha. For each recorded next action that has an `action_id`, prime_review `check-next` runs against every other committed latest review that has holds. The result is `blocked`, `not-released` or `independent-of-holds`, with the holding review named.
   - **Legacy:** if the page's reader review text is non-empty and there is no committed cycle review, the work is `legacy-review-unmapped`, which is attention. The text is shown, never typed. Adoption is an explicitly attributed new review.
5. **Template** (`prime-cycle-decision/1`):
   - `binding`: pre-filled. It holds work_id, page, pass, source {kind, commit, page_sha256, page_bytes}, member, receipt_sha256, origin, retrospective, goal {goal_id, goal_sha256}, expected_prior {review_id, record_sha256} or null, and fingerprint, which is the sha256 of the canonical binding without the fingerprint.
   - `judgment`: null fields for Prime.
   - `review_id`: a suggested `<pass>-r<n>`.
   - `supersedes` and `recovers`: null.
6. **Output** `prime-cycle-view/1` (JSON) or a readable text view. Bounded by `max_output_bytes`; overflow refuses. `authority: none`. No elected item.

## 5. record

The decision is `prime-cycle-decision/1`, with exact keys: `schema, review_id, supersedes, recovers, binding, attribution, judgment`.
- `attribution` is `{actor_label, role, evidence}`, in the prime_review shape. It is a label and nothing more.
- `judgment` has exact keys: `outcome, disposition, pass_terminal, goal, finding, reasons, source_refs, next_action, unresolved, semantic_conflict, design_fork, holds, answers, sections`.
  - `outcome`: continue, director-input, develop or complete.
  - `disposition`: accepted, held or correction-required.
  - `pass_terminal`: finished or open.
  - `goal`: `{terminal: open|completed, goal_id, goal_sha256, evidence: [str]}`.
  - `next_action`: `{action_id: LABEL, text: str, authorized_in_grant: bool|null}` or null.
  - `unresolved`: [str].
  - `holds`, `answers`, `sections`, `semantic_conflict` and `design_fork`: the prime_review shapes.

**Steps:**
1. Validate the decision and the registration work. Re-observe with the reader. The fresh binding must equal `binding` field for field, fingerprint included. Any difference refuses: "source changed since read: <fields>". Nothing is refreshed silently.
2. `expected_prior` must equal the current latest committed review, or null when there is none. If `supersedes` is given, it must equal `expected_prior`. A record over an existing review without `supersedes` refuses.
3. Apply the terminal rules (§6).
4. Build a `prime-review-record/1`:
   - attribution;
   - sources: the page (kind page, with content and transport sha equal to the page sha; bind true for live-file under `--root`, false for git-blob) and the capture (kind capture, identity return-capture/1, content equal to the receipt sha and bytes);
   - the registration agreement;
   - the judgment fields;
   - holds and answers;
   - `review_passes []`, and `gaps` equal to `unresolved`.
   Run `report --json`. Exit 2 refuses the record. Keep the report's `effective`, holds, attention and markdown_sha256.
5. Write, in this order, each file exclusive-create inside `<review_location>/<review_id>/`:
   - `record.json`: canonical `prime-cycle-review/1` {decision, observed binding, prime_review input sha256, report summary, tool shas, lineage};
   - `REVIEW.md`: a header binding record.json's sha and the noncanonical-projection note, the terminal summary, then the prime_review markdown verbatim;
   - `COMMITTED.json`: {record_sha256, review_md_sha256}. **This is the completion marker.**
6. **Replay and recovery.**
   - The directory exists and is committed, with identical record bytes: exit 0, `already-recorded`, no write.
   - Committed, with different bytes: refuse, conflict.
   - The directory exists without a valid COMMITTED: refuse, `partial review present`. Recovery: `inspect`, then record under a new `review_id` with `recovers: <partial id>`. The partial stays, and read keeps showing it as attention.
   - A failure after the directory was created: exit 3, the files so far left as they are.

## 6. Terminal rules (refused, never coerced)

- `outcome complete` if and only if `goal.terminal completed`.
- `goal.terminal completed` requires:
  - disposition `accepted` and `pass_terminal finished`;
  - `goal.goal_id` and `goal.goal_sha256` equal to the registration's current goal;
  - non-empty evidence;
  - prime_review `effective == complete-as-supplied`.
- Disposition `held` or `correction-required` requires pass `open` and goal `open`.
- `outcome director-input` requires disposition `held`. prime_review requires the hold.
- `goal.goal_id` and `goal_sha256` must name the registration's current goal even when the goal is open.
- Accepted with pass finished and goal open is valid: a finished pass, an open goal.
- No rule infers a terminal state from tests, a receipt, publication or the word accepted.

## 7. Paths, bounds and writes

- **Write roots.** `record` writes only under `repository/<review_location>`. The parent chain must exist and contain no links; the review location directory may be created, but only under `<lane>/evidence/`. `--templates` and `packet` write only under `output_root`.
- **Never written:** a source page, a face, a capture member, `00.kernel/00.live.md` or `0401.goal/06.01.md`.
- **Bounds.** Reads are bounded: each page by `max_page_bytes`, decisions and records by 262144 bytes. Output is bounded by `max_output_bytes`.
- **Limits.** A label is not authentication. The trusted caller is the local user. Same-user races between a check and a write are not prevented, and no OS sandbox is claimed. There is no transaction across files: COMMITTED.json is the only usable-state marker.

## 8. inspect

`inspect --work ID` lists each review directory with its files, sizes and hashes, and gives its phase: `committed`, `partial-no-marker`, `partial-marker-mismatch` or `invalid`. It also states the next safe step: a new review_id with `recovers`. It is read-only.

## 9. Unsupported mappings (documented, not bridged)

- **prime_brief and state_projection.** Their `completed` is batch closure: a bound review with `terminal: completed` and live custody. Mapping a page goal onto it would relabel batch semantics as whole-page closure, which 0415 forbids. The cycle keeps its own pass and goal fields.
- **desk_state.** It renders a hand-maintained desk-state/1 record, with coordination arrays. The cycle derives its view from work-local review records instead. The two are not merged, and neither feeds the other.
- **Legacy manual reviews.** Prose in a page's Review section is not mapped to a typed decision. It shows as `legacy-review-unmapped` until Prime records an attributed review.
