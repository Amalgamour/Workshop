# Contract — desk-state pass 01

Schema `desk-state/1` in, schema `desk-view/1` out. Standard library only. Experimental until Prime reviews it. Not a seat, not a route, and not an assignment.

## Command

```text
python -B labs/desk-state-pass01/desk_state.py view --input ABS [--json] [--out DIR] [--candidate ABS]
python -B labs/desk-state-pass01/desk_state.py revise --record ABS --expected SHA256 --submission ABS --out ABS
```

`view --input ABS [--json]` is the morning-brief command. `--out` and `--candidate` are optional writes. `revise` is the guarded record edit. It does not launch a backend and it is not a worker command. The pinned projection stamps `projected_at` inside the raw brief. A repeated view can differ in that clock. Lane decisions, citations, and source bytes do not.

Exits:

- 0: a view with no attention item and no unknown.
- 1: a view that shows attention or an unknown.
- 2: refused. Stderr starts with `refused:`. No view is printed.

Reader legacy codes are copied onto the lane and do not by themselves change the exit. A repeat of `view` without `--out` or `--candidate` writes nothing.

## Record

`desk-state/1` objects have exactly these keys: `schema`, `desk`, `book`, `goal`, `milestone`, `lanes`, `blockers`, `handoff`, `pages`, `members`, `coordination`, `uninspected`, `legacy`, `tools`, `bounds`, `roots`, `revision`, `custody`.

Duplicate JSON keys and unknown keys refuse. There is at least one page and one lane.

- `desk` and `book` match `^[A-Za-z0-9][A-Za-z0-9._-]{0,63}$`.
- `goal` and `milestone` are `{statement, evidence}`. `statement` is a non-empty string up to 2000 characters. `evidence` is a list of citations.
- A citation is `{repository, path, commit, sha256, note}`. `repository` is the record's repository root. `path` is a relative forward-slash path with no `..`. `commit` is 40 lowercase hex. `sha256` is 64 lowercase hex. `note` is a string up to 400 characters.
- A page is `{id, repository, path, commit, observation}`. `observation` is `git-blob` or `live-file`. `git-blob` requires a 40-hex commit. `live-file` requires `commit: null`. The repository is the record root. Page ids are unique.
- A lane is `{id, page_id, worker, task}`. `worker` is null or a string up to 80 characters. Null means unrecorded, not available. `task` is a string up to 500 characters. The `page_id` names a page. Lane ids are unique.
- A blocker is `{id, statement, status, evidence}`. `status` is `unresolved` or `recorded`.
- `handoff` is `{statement, author, evidence}`. The view labels it `recorded-prime-intent`.
- A member is `{name, role}`. `name` matches `^01\d\d\.[a-z0-9][a-z0-9.-]*$`. `role` is `declared` or `pointer`. Names are unique.
- `coordination` items are prime-brief coordination objects: exactly `{label, batch_id, source_sha256, release, claim, claim_actor, candidate, review, publication}`. `label` is `SUPPLIED`. Release and claim are `recorded`, `pending`, `absent`, or `unknown`. A review is null or exactly `{member, receipt_sha256, disposition, terminal, reviewer, followup}` with disposition `accepted`, `held`, or `correction-required`, terminal `completed` or null, and a reviewer label. Publication is `{status, ref, commit}` with status `unknown` or `at-ref`. Batch ids are unique.
- `uninspected` items are `{label, reason}`. They are copied and not opened.
- `legacy` is one citation plus the key set `{repository, path, commit, sha256, note}`. It is the observed `00.live` gap, not a second story.
- `tools` has exactly `batch_observe`, `return_inspect`, `return_capture`, `state_projection`, and `prime_brief`. Each is `{path, sha256}`. The path must be the pinned relative path under `roots.tools`. The file hash must equal both the record and the built-in pin. A mismatch refuses before any backend launch.
- `bounds` is `{max_sources, max_source_bytes, max_total_bytes, max_output_bytes}`. Each is an integer from 1 through the hard cap. Caps are 32 sources, 262144 bytes for one source, 1048576 bytes total, and 1048576 bytes of output. A record cannot raise a cap.
- `roots` is `{repository, tools, members_book, output}`. All four are absolute. `output` is the only write root.
- `revision` is `{reason, authorizing, predecessor}`. `predecessor` is null or 64 hex. `reason` and `authorizing` are non-empty strings up to 2000 characters.
- `custody` is `inspect-named-members` or `commit-facts-only`.

Pins, checked before launch:

- `labs/batch-observation-pass01/batch_observe.py` `8bea18171b723650e8c0b07f5de334d2c5fd004c5d65c4fa8c4b85cf0bc830d4`
- `labs/return-capture-pass01/return_inspect.py` `947915febaa5918f56b6be03c81840c030d081fcab9a3bead2cd660973a9999b`
- `labs/return-capture-pass01/return_capture.py` `8f3da5c651f6924fca6dedb0b95da7d181eb58884dc030dd9cbc3d8b6a5b15ac`
- `labs/state-projection-pass01/state_projection.py` `b349da5cef5178296a069c354002a600ba4e168c2710aa5d87789724d4951ecb`
- `labs/prime-brief-pass01/prime_brief.py` `302ed832d2fa955a591420f13d3b22ce91e4a7669c69a778d443fc82627580d7`

## Paths and writes

Relative paths reject a backslash, a drive, an empty segment, and `..`. Absolute paths reject a UNC prefix. A symlink or a Windows reparse point on the path or an existing parent refuses. Source paths stay under `roots.repository`. The module never writes a source, the input record, `00.kernel/00.live.md`, or `00.kernel/00.00.10.work/0401.goal/06.01.md`.

`--out` and `--candidate` must resolve under `roots.output`. Files are created with exclusive create. If `view.json`, `PARTIAL.txt`, or the candidate already exists, the command refuses and does not replace them. If a later file in the same command fails, `PARTIAL.txt` is left beside the file that was created. A retry refuses. A refused command does not present that directory as a current complete view.

`revise` checks that `--expected` is the SHA-256 of `--record`, validates the submission without launching a backend, and requires `revision.predecessor` to equal that hash. It writes `--out` exclusively and leaves `--record` unchanged. A stale expected hash refuses. A `desk-view/1` document, a candidate markdown file, or any other schema is not a record.

## What the view computes

Hash and path checks come first. Citations are then read with `git cat-file` at the declared commit. A missing or different blob is an unknown. It is not replaced with the live file.

Each page is read by the pinned reader: `observe --json --repo --commit --path`, or `--live --repo --path` when the page asks for a live file. Exit 0 or 1 keeps the stdout unchanged. Exit 2, a timeout, or unreadable JSON records `observation-failed` and does not invent a page. The raw stdout stays in the view.

Declared members, and members named by a successful reader's pointer, are inspected only when `custody` is `inspect-named-members`. The command is `inspect --book ABS --member NAME --json`. A missing, reserved, incomplete, retrospective, or refused report stays visible. `commit-facts-only` does not launch the inspector. Declared members then stay `not-observed`.

The brief input is `prime-brief-input/1`. Observations are labelled `SUPPLIED` and passed through. Scope book is the record book. Scope lanes are the identified page names. `members_book` is set only for `inspect-named-members`, and only then is `--inspect` passed. Coordination whose batch was not successfully identified is omitted and reported as not applied, so a failed read cannot refuse the whole brief. A coordination whose `source_sha256` differs from the reader hash is passed through. The brief leaves that batch unprojected. This module does not rewrite the hash.

The view's `elected` field is null. Lane order is the record order. Lifecycle, follow-up, and projection attention come from the brief when it projected the batch. An unidentified page, a missing coordination record, an unknown release or claim, a stale source hash, and a failed observation stay unknown. A captured member with no bound review stays awaiting review when the projection says so. A held review keeps its follow-up. Accepted with `terminal: null` stays distinct from `terminal: completed`. A commit-basis source is not treated as live completion. Retrospective same-origin custody stays historical.

`handoff.kind` is `recorded-prime-intent`. The statement is copied from the record. Compute does not replace it.

Overflow of the source count, one source, the total, or the serialized view refuses the view. Required facts are not dropped. No Git fetch or push, no model call, and no queue write occurs.

## Readable view and candidate

Without `--json`, stdout is the readable view. With `--json`, stdout is the JSON view. Both come from the same object. Headings are Desk goal, Milestone, Lanes, Returns, Unresolved decisions, and Recorded next step.

`--candidate` writes markdown that starts with `DERIVED VIEW`, names the record hash, lists source cuts and live observation times, copies unresolved decisions, and lists known gaps. It is not an input. The next render reads the record again.

## Migration

No step in this contract edits `0401.goal/06.01.md`, `00.kernel/00.live.md`, a backend, a boot pin, or a queue. `MIGRATION.md` is a proposal for a later review.
