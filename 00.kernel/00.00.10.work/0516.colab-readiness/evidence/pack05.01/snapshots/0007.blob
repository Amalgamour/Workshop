# CONTRACT — prime_cycle.py, 05.02 correction (delta over build05.01/CONTRACT.md)

Written before the code change. Everything in `build05.01/CONTRACT.md` stays in force except where this page replaces it. The registration schema (`prime-cycle-registration/1`) is unchanged.

## 1. Commands and exits

| command | 0 | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|---|
| read | no attention | attention | refused | — | journal start failed; nothing ran | ran, journal end failed | unexpected error |
| record | recorded, or already-recorded | recorded with prime_review attention/hold | refused | partial write | as read | as read; the review result stands | as read |
| inspect | all committed | any partial or invalid | refused | — | as read | as read | as read |
| packet | assembled | — | refused | — | as read | as read | as read |
| day | the day is clean | incomplete, unreadable or attention | refused | — | — | — | — |

The new options on read, record, inspect and packet:
- `--journal-root ABS`;
- `--caller TEXT` (supplied);
- `--note TEXT` (supplied).

The new command is `day --journal-root ABS [--date YYYY-MM-DD] [--registration ABS] [--json]`.

## 2. Decision template `prime-cycle-decision/2`

`binding` is the 05.01 binding plus:

```json
"direction": {"schema": "prime-cycle-direction/1", "agreement_sha256": "<sha256 of canonical(work.agreement)>",
              "fields": {"goal": "<sha>", "scope": "<sha>", "prime_discretion": "<sha>", "director_required": "<sha>",
                         "finish_criteria": "<sha>", "recorded_decisions": "<sha>"},
              "review_location": "<work.review_location>", "book": "<registration.book>"}
```

**How each field is hashed:**
- each field's sha is the sha256 of `canonical(value)`, and an absent key hashes as `null`;
- extra agreement keys are covered by `agreement_sha256`;
- the fingerprint covers the whole binding, direction included.

**Excluded, on purpose:**
- output_root, bounds and other works, which do not change this work's judgment;
- the registration's file bytes, which change with unrelated edits;
- the reader's stdout hash and `live_observed_at`, which depend on the clock.

**Record refuses:**
- a decision schema other than `/2` ("template from an older read; read again");
- any change to `direction`, naming the field: "direction changed since read: agreement.scope". There is no silent refresh.

An identical replay of a `/2` decision under an unchanged direction is still a no-op; a successor still needs a new id plus `supersedes`.

## 3. Record `prime-cycle-review/2`

Same as `/1`, with the `/2` decision inside it; `observed_binding` includes `direction`. Read still accepts `/1` records, keeps them in the lineage, and shows them only as historical (§4).

## 4. Read view `prime-cycle-view/2`: current versus historical

**Head current.** The head review is *current* only when all three hold:
- its decision binding equals the current binding on `source.page_sha256`, `member`, `member_role`, `receipt_sha256`, `submission_id`, `origin`, `retrospective` and `direction`;
- its record schema is `/2`;
- no `hash-mismatch` directory in the location is left unrecovered. A review recovers it by naming it in `recovers`.

**When the head is not current:**
- `disposition`, `pass_terminal` and `goal_terminal` read `unknown`;
- `next_action` is null;
- `historical = {review_id, record_sha256, reason, disposition, pass_terminal, goal_terminal, goal_id, next_action}` holds the old declarations;
- `pass_state` is `review-stale` when the binding changed, or `review-unusable` (`legacy-binding` or `altered-review`);
- the text output prints `unknown (historical <value> in <review_id>, <reason>)`.

**Holds** of a non-current head stay listed and keep blocking. They are marked `from a non-current review`.

**Goal changes** keep the 05.01 behaviour, which is separate from staleness: the pass stays reviewed, and the goal reads open with a prior-completion note.

**`summary`** counts current values only: works, awaiting_review, reviewed_current, stale_or_unusable, finished_passes, completed_goals, open_holds.

**Marker kinds.** A `partial-marker-mismatch` row gains `marker`: `torn`, when the marker does not parse, or `hash-mismatch`.

## 5. Journal `prime-cycle-journal/1`

**Layout.** `<journal_root>/<YYYY-MM-DD local start date>/<op_id>/`. The op_id is `<UTC yyyymmddThhmmss.ffffffZ>-<12 hex random>`. Inside it:
- `start.json`: written before the operation;
- `registration.json` and `decision.json`: exact input snapshots, where the inputs were readable and within MAX_DOC;
- `stdout.txt`: exact, up to max 2 MiB, with a `truncated` flag;
- `end.json`: written after the operation.

Every file is exclusive-create, and nothing is ever rewritten or deleted.

**start.json:**
```
{schema: prime-cycle-journal-start/1, op_id, operation,
 machine: {started_at_local (ISO 8601 with offset), started_at_utc, clock_basis, pid, python, tool_path, tool_sha256, pins,
           argv, cwd, inputs: {registration: {path, sha256, bytes, snapshot} | {path, error}, decision: …}},
 supplied: {caller_label, note}}
```

**end.json:**
```
{schema: prime-cycle-journal-end/1, op_id,
 machine: {ended_at_local, ended_at_utc, duration_seconds (monotonic), exit, status,
           stdout: {sha256, bytes, snapshot, truncated}, result}}
```

**Status, per command:**
- read: `ok`, `ok-attention` or `refused`;
- record: `recorded`, `recorded-attention`, `replay`, `refused` or `partial`;
- inspect: `ok`, `ok-attention` or `refused`;
- packet: `ok` or `refused`;
- any command: `error`.

**Result, per command:**
- read: the view sha, the summary, and the templates written (path and sha);
- record: `review` = {work_id, review_id, dir, record_sha256, marker_sha256, schema}, re-read from disk. A partial gives the directory and the present files with their hashes;
- inspect: the phases;
- packet: the output dir, and the sha of assembly-status.json.

**Safety:**
- the root is absolute, local, with no link in the path;
- it is not inside the repository or the members book;
- the date and op directories are plain, created with mkdir, and their names never collide;
- `--templates` and `--out` may not lie inside the journal root.

**Failure:**
- **start fails:** exit 4 with `refused: journal start failed …; nothing was run`;
- **end fails:** the operation's stdout is unchanged; stderr says `journal: end event FAILED …` and, for record, names the committed or partial review path; the exit is 5; the operation stays incomplete in the journal;
- **an unexpected Exception:** the end status is `error`, and the exit is 6;
- **KeyboardInterrupt or a kill:** no end event is written, so the operation stays incomplete.

There is no retry, no transaction across files, and no same-user race safety.

**Visibility.** Text outputs end with one `journal:` line, showing `<root> op <op_id>` or `disabled (no --journal-root; this operation is not logged)`. JSON outputs (read --json, inspect) carry a `journal` field.

## 6. day

day is read-only and is not logged. It lists the date directory's operations in op_id order, with their status: `incomplete` when there is no end.json, `unreadable` when start.json is invalid.

It counts:
- attempts by operation and status;
- refusals, with the first stdout line;
- partials;
- unique reviews, keyed by (dir, record_sha256) from the record end events, then re-verified now (marker present and hashes equal), with their invocations and replays;
- declared finished passes, completed goals and holds, from unique verified records only.

With `--registration`, a fresh read lists the current finished passes, completed goals and open holds, by work. Without it, these read `current: not checked`.

Durations are given per operation: unknown for incomplete operations, with no totals. Productivity is not derived. A day that does not exist is refused. A day bigger than 5000 operations is refused.
