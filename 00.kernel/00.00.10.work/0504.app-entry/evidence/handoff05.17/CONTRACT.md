# CONTRACT — fixture handoff from a returned Clerk job

Batch `0504.app-entry/05.17`. This contract is the fixture boundary for `labs/capture-handoff-pass01/handoff.py`. It is not kernel law, not app wiring, and not a seated workflow. A Director release of this batch is not acceptance of a captured member. A verified receipt remains custody.

The accepted 05.16 design is the base. Prime review CH-01 and CH-02 tighten it.

## CH-01 — the report is a returned artifact

`returned.delivery` is the transport id. `returned.evidence` is one transport line. Neither is the final report. The report is one returned artifact, named by path and checked by sha256 and byte count against `show --json` and against the outbox file. Each captured artifact is checked the same way. A caller-supplied hash alone is not that check.

`artifact_base` is an absolute path and must be the job outbox `clerk_store/jobs/<job_id>/outbox`. The adapter does not search another directory for a byte-identical file. `report.source` and every artifact `source` equal the Clerk path, one simple filename. A different relative name is an ambiguous mapping and is refused before launch. `source_root` may be that outbox or another plain directory. When it is another directory, the adapter still reads the outbox file and the source file and requires both byte sequences to match the returned record.

The return file passed to capture is the source file under `source_root`. The adapter does not pass a return file outside that root.

## CH-02 — the handoff record

`record` is an absolute directory outside the capture member, outside the Clerk job directory, and outside `source_root`. `failure_log` is an absolute file outside that record directory and outside those same places. Neither path may contain a `.git` segment. The book may sit in an ordinary Git working tree. The Clerk store may not; the pinned Clerk tool refuses that, and this adapter does not launch capture after that refusal.

`intent.json` is exclusive-created before capture. It stores schema `clerk-capture-handoff-record/1`, kind `intent`, the canonical binding sha256, the returned event sha256, the job, submission, member, `work_ref`, the transport pair, and the report and artifact identities.

`completed.json` is exclusive-created only after `verify`, `return_inspect --json`, and a comparison of `return.md` and each payload to the source bytes already checked. It stores kind `completed` and the binding sha256, event sha256, reservation sha256, manifest sha256, and receipt sha256 taken from the tool interfaces. This module does not reimplement receipt validation and does not parse `0003.returned.json`.

An identical completed retry re-reads the inspection, the source bytes, verify, and inspect. When they still match the completed record, the retry writes nothing and exits 0. A changed event, report, artifact, origin, or binding conflicts, including when the member is already complete. The completed file is not overwritten.

A complete member with no matching completed record is attention. The adapter does not adopt it and does not write `completed.json`. An `intent.json` without `completed.json`, an incomplete member, and a capture that finished without the final record stay retained. There is no delete, overwrite, automatic resume, or second member. Failure text lists the writes that happened. A second failure does not overwrite an existing failure log.

`work_ref` is stored as a declared label. Clerk has no field that confirms it. `instructions_base` is required. `checks.instructions` must be `usable`. `not-checked` is refused.

## Binding

Schema `clerk-capture-handoff/1`. One JSON object, UTF-8, no BOM, no duplicate keys, no trailing value. Unknown fields and missing fields are refused. Required fields:

| Field | Rule |
|---|---|
| `clerk_store` | absolute store path |
| `job_id` | must equal the inspection |
| `instructions_base` | absolute base passed to `show --json` |
| `returned_event_sha256` | 64 lowercase hex; must equal `returned.event_sha256` |
| `assignee` | must equal `returned.by` |
| `work_ref` | non-empty label; not a Clerk identity |
| `origin.book`, `origin.page`, `origin.batch` | must equal the reservation origin; batch matches `05.NN` |
| `book` | absolute book directory |
| `submission_id` | must equal the reservation |
| `member` | must equal `reservation.destination.path` |
| `source_root` | absolute plain directory |
| `artifact_base` | absolute path of the job outbox |
| `report` | `clerk_path`, `source`, `sha256`, `bytes`; source equals clerk path |
| `artifacts` | non-empty ordered list of `clerk_path`, `source`, `logical`, `sha256`, `bytes` |
| `record` | absolute handoff directory |
| `failure_log` | absolute failure file outside `record` |

`logical` equals `clerk_path` and `source`. The logical list must equal `expected_outputs` in order. Hashes are 64 lowercase hex. Byte counts are non-negative integers. A JSON boolean is not an integer. Paths use forward slashes, one filename segment, and no `..`.

The canonical binding sha256 is the sha256 of the canonical JSON object of those fields after absolute paths are normalized with `os.path.abspath`. Canonical JSON sorts keys, uses separators `(",", ":")`, and ends with one LF.

## Before capture

Refuse, and do not create `intent.json`, unless all of these hold:

- The three pinned tool files match their sha256 values, are regular files, and are not links.
- The inspection schema is `clerk-handoff-inspection/2`, `state` is `returned`, the event hash and assignee match, `checks.events`, `checks.completion`, and `checks.artifacts` are `ok`, `checks.instructions` is `usable`, and `problems` is empty.
- The report and every artifact match a returned artifact's path, sha256, and byte count, and the outbox file and the source file both contain those bytes.
- Those files are regular, link count one, and not reparse points. A junction is not followed.
- Inspect schema is `return-capture-inspection/1`. Status `reserved` has exit 1. The reservation submission, origin, member, and ordered outputs match.
- Status `complete` without a matching completed record stops. Status `incomplete` stops. The planted bytes stay.
- No `intent.json` or `completed.json` is already present for this reserved member.

Pins are checked again immediately before the capture subprocess. Source bytes are read again. A difference does not start capture.

The capture command is the pinned `return_capture.py` with `--book`, `--submission`, `--return-file`, `--source-root`, and one `--artifact source|logical` per binding artifact, in order. It does not set retrospective, source commit, or the prime-review flag.

## After capture

Verify must exit 0 and include `result complete`, `not approved`, `not accepted`, and `not published`. Inspect must be status `complete` with exit 0. `return.md` must equal the report bytes. Each `payload/NNNN.blob` must equal the matching source bytes and the inspect payload hash. Pins and source bytes are checked again. Only then is `completed.json` exclusive-created.

A stop after intent, after capture, or before the final record leaves the files already written and does not write `completed.json`. A later `perform` of the same binding sees that retained state and exits 2. It does not finish the record.

A pin or source change found after capture and before the final record does not write `completed.json`. The conflict is described on stdout and, when the log can be created, in the failure log. The same-user interval between the last read and the write is not closed. This module claims no operating-system sandbox.

## Interface

`perform(binding_path: str, *, hook=None, pins=None) -> int`

The CLI is `handoff.py perform --binding ABS`. It does not accept a fault switch. `hook(point)` and `pins` are private in-process seams. A hook return of `stop` at `before-intent`, `after-intent`, `after-capture`, or `before-final-record` stops at that point. `pins` cannot retarget the script path.

Exit 0 is `result ok`: the first completed handoff, or an identical retry that wrote nothing. Exit 2 is `result refused` or `result attention`. Clerk show exit 1 becomes exit 2. The adapter does not call queue, claim, return, or reserve.

Competing callers exclusive-create `intent.json`. One writer proceeds. The other does not overwrite and does not report success while the intent is unfinished.
