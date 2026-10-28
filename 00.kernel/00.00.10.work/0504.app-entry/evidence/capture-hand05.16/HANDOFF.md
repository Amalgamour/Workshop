# HANDOFF — returned Clerk job to a pre-reserved capture

Batch: `0504.app-entry/05.16`. This contract is a design. It does not add a module, a command, or a route. It is not kernel law. An orientation result, a Clerk return, and a capture receipt are not authorization. This draft grants no release.

## One binding

The proposed document is schema `clerk-capture-handoff/1`. A later fixture adapter reads one such document and does not invent missing fields. There is no current-version lookup and no inferred Director release.

| Field | Owner | Must match |
|---|---|---|
| `clerk_store` | caller, absolute path | a plain directory outside every Git working tree, as `clerk.py` already requires |
| `job_id` | caller | `inspection.job_id` |
| `instructions_base` | caller, absolute path | the base passed to `show --json` when the binding requires usable instructions |
| `returned_event_sha256` | caller | `inspection.returned.event_sha256` |
| `assignee` | caller | `inspection.returned.by` |
| `work_ref` | caller | nothing in the job; the adapter does not read a work ref out of Clerk |
| `origin.book`, `origin.page`, `origin.batch` | caller | `reservation.origin` exactly |
| `book` | caller, absolute path | the book passed to capture and inspect |
| `submission_id` | caller | the one reservation with that id |
| `member` | caller | `reservation.destination.path` |
| `source_root` | caller, absolute path | the capture source root |
| `report` | caller, relative path under `source_root` | the builder final report |
| `report_sha256` | caller | the sha256 of that report file |
| `artifacts[]` | caller | `source`, `logical`, `sha256` for each expected output, in reservation order |

`inspection` means one `show --json` document, schema `clerk-handoff-inspection/2`, from the pinned `clerk.py`. The adapter does not parse `0001.queued.json`, `0002.claimed.json`, or `0003.returned.json` itself. `reservation` means the reservation the pinned capture tool already stored. The adapter does not allocate a member and does not rewrite `reservation.json`.

The stored `release` string on the job and on the reservation stays stored text. The adapter copies neither string into a new authority field.

## Two records that must not be merged

Clerk `returned.delivery` is a transport id. Clerk `returned.evidence` is one printable line. Together with `returned.by`, `returned.claim` on the event, and the artifact hashes, they are the worker transport record. A worker transport result may be that line, or a file the worker wrote in the outbox. Neither one is the builder final report unless the caller names that same file as `report` and its bytes are copied whole.

The builder final report is the file at `report`. Capture copies that file, unchanged, to `return.md`. The adapter does not summarize it, does not search it for a Review heading, and does not set `includes_prime_review` unless the binding says that flag explicitly. This first design does not set `retrospective` and does not set `source_commit`.

The Clerk returned event and the capture receipt are separate facts. Recording one does not record the other. The adapter must not call `queue`, `claim`, or `return`. The adapter must not call `reserve`. The job is already returned, and the member is already reserved, before the adapter runs.

## Before capture

The adapter refuses, and does not call capture, unless all of these hold:

- The inspection schema is `clerk-handoff-inspection/2`.
- `state` is `returned`.
- `returned` is an object and `returned.event_sha256` equals the binding.
- `checks.events`, `checks.completion`, and `checks.artifacts` are `ok`.
- `problems` is empty.
- If `instructions_base` is present, `checks.instructions` is `usable`. `not-checked` is not usable. A clean state with unchecked instructions is not enough.
- `job_id` and `returned.by` match the binding.
- `return_inspect --json` on the named member has `status` `reserved`, the same `submission_id`, the same origin, and `expected_outputs` equal to the binding's logical names in order.
- A `complete` member is not a new write. It is the idempotent case below.
- An `incomplete` member stops the adapter. It is not finished and not replaced.
- Each artifact's current bytes hash to the binding sha256 and to the matching `returned.artifacts` item (`path`, `sha256`, and `bytes`).
- The report's current bytes hash to `report_sha256`.
- The report path and every artifact source are relative, stay under `source_root`, and are plain files with link count one.

A claimed job, a queued job, a dirty outbox, a different event sha256, or a different origin is a refusal. The refusal is recorded outside the member. No capture files are added by the adapter in those cases.

## What the current tools already do

These rules belong to the pinned tools. The adapter calls them. It does not reimplement them.

- `clerk.py` refuses a store that resolves inside a Git working tree. `show --json` is read-only. On a clean return, `returned.event_sha256` is the sha256 of the exact `0003.returned.json` bytes matched to the completion witness. A later outbox change does not change that sha256. `checks.artifacts` becomes `changed`, a problem `artifact-changed` is added, and the exit is 1. Exit 1 is not a clean handoff.
- An identical Clerk return prints `already-recorded` and writes nothing. The same delivery id with different evidence or different artifact bytes is `delivery conflict` and writes nothing.
- `return_capture.py` requires an absolute book, an absolute return file, and an absolute source root. Relative artifact paths use forward slashes and may not contain `..`. A path that leaves the source root is refused. A symlink, junction, or other reparse point on a walked segment is refused and is not followed. A regular file with link count other than one is refused as `link-count`.
- Each selected input is read twice before a capture write. A difference refuses with `bytes changed before capture` and writes nothing. This fixture does not race that read. The rule is the tool's.
- The source root, the return file, and each artifact must not sit inside the destination member.
- Logical names must equal `expected_outputs` in order. A missing logical name writes nothing and leaves the reservation.
- An identical second capture prints `already-captured` and writes nothing. Changed return bytes, payload bytes, or capture flags conflict and write nothing.
- If `return.md`, `payload/`, `manifest.json`, or `receipt.json` is present and the member does not verify, capture writes nothing, lists the retained paths, and returns `result refused`. There is no cleanup flag and no second allocation for that submission.
- `interrupt` is not a command flag. A partial package cannot be finished by retrying capture.
- Verify of a complete member says `result complete`, `not approved`, `not accepted`, and `not published`. `return_inspect.py` uses schema `return-capture-inspection/1`. Reserved is exit 1. Complete is exit 0. Incomplete is exit 2. Inspect does not write.
- The tool allows a return file that sits outside the source root. The proposed adapter does not. A report outside `source_root` is an adapter refusal even when capture would copy it.

The capture tool does not read the Clerk store. The Clerk tool does not read the book. A person, or a harness, can still run capture for a job that is only claimed, for bytes that no longer match the returned event, or while a side file names a different origin. Those successes are not guards. The adapter's refusal is the guard. This design does not claim that a sequence of manual commands is that guard.

## After a complete capture

The adapter runs verify and keeps the stdout, including the custody lines. It records `returned_event_sha256`, `reservation_sha256`, `manifest_sha256`, and `receipt_sha256` in its own fixture log, outside the member. It compares `return.md` to the report bytes and each payload to the named source. A mismatch is a failure record, not a rewrite.

A missing pointer on the batch page is a later projection. This adapter does not edit `05.16.md` or any other batch page. `01.md` remains an index. It is not completion.

## Idempotency and failure

| Situation | Adapter result | Writes |
|---|---|---|
| Same binding, same bytes, member already complete, receipt still matches | exit 0, `already-captured` | none |
| Same submission, different report bytes, artifact bytes, event sha256, or origin | exit 2 | none |
| Member incomplete | exit 2, retained paths listed | none, and no new member |
| Tool exit 2 | exit 2, tool text kept | none beyond what the tool already retained |
| Clerk show exit 1 | exit 2, problems kept | none |

The adapter does not turn exit 1 into success. It does not delete retained capture files. It does not mint a new submission id after a conflict. A new submission is a separate caller act, with `supersedes` chosen by that caller, and it is outside this adapter.

## Next fixture slice

One module, `labs/capture-handoff-pass01/handoff.py`, fixture only. No `app/librarian.py` wiring. No import of Clerk or of the capture tool. The call is a subprocess argument array of the current Python executable, `-B`, and the pinned script path, with `shell` false.

Public function: `perform(binding_path: str) -> int`.

The module pins the three tool files above by sha256 before the first subprocess. A mismatch exits 2 and starts nothing. Paths come from the binding and from those pins, not from packet text and not from a caller tool override.

Failure log: one file the binding names, outside the member and outside the Clerk job directory. The log quotes tool stdout, the inspection object, and the inspect object. It does not replace them.

Acceptance for that later slice:

- A disposable returned job and a pre-reserved member produce a verify result of complete, with the three custody lines, and `return.md` equal to the named report.
- The recorded `event_sha256` equals the inspection.
- A second `perform` of the same binding writes nothing and exits 0.
- Claimed-not-returned, dirty artifacts, mismatched origin, and a changed event sha256 each exit 2 with no new capture files.
- A planted partial member stays partial, with the same retained bytes.
- A linked path and a hard link are refused by the tool and are not followed.
- No batch page changes. No Clerk return is written. No model is called.

This page authorizes none of that module. It only names the boundary.
