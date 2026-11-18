# Contract — return-line writer, reader, and staged migration

Schema of this file: return-line-contract/0503.
Date: 2026-10-31. Executor: Grok-1. Batch: 0521.return-placement/05.03.
This file is written before labs/return-lines-pass01. The lab implements this contract.
It does not change the shared seam, the placement candidate, or the sealed reader.

## Authority

- Descriptor shape: 0417.return-placement/evidence/integration-seam-v1.md, schema return-line-descriptor/1.
- Route arithmetic: the pinned placement `compute_route`. Leading digit is the workflow space. The second digit is the band. Band 5 maps to the same space, digit 1, and the same NN and subject. Band 7 stays on that page. Every other band is undeclared.
- Historical custody: pinned `verify_member` on a directory whose name is still the original `01NN.slug`. A receipt is a byte check. Acceptance stays null.
- Director correction used as recorded: 0417.return-placement/06.01.md. This tool does not invent a route for an undeclared band.

## Pins loaded by path

| role | path | sha256 | bytes |
| --- | --- | --- | --- |
| placement | labs/return-placement-pass01/return_placement.py | db96f7023c73dcececba0e7d42b821da8193af7534a4bdf8cd2e5d6cd53d0754 | 66097 |
| reader | labs/return-capture-pass01/return_capture.py | 8f3da5c651f6924fca6dedb0b95da7d181eb58884dc030dd9cbc3d8b6a5b15ac | 45767 |

A mismatch raises check `pinned reader mismatch` or `pinned placement mismatch` and writes nothing. The reader is loaded as `return_capture_pinned`. The placement module is loaded as `return_placement_pinned`. This tool does not call the sequential allocator. Its source must not contain the substrings `import return_capture` or `reserve(`.

The inspector is not loaded. The app door records its pin: labs/return-capture-pass01/return_inspect.py, sha256 947915febaa5918f56b6be03c81840c030d081fcab9a3bead2cd660973a9999b, 11402 bytes.

## What this tool owns

Canonical program: labs/return-lines-pass01/return_lines.py.
Door: app/return_line_tools.py, a development pin and forwarder. It is not kernel law. It does not edit app/librarian.py or any existing facade.

Commands: `init`, `reserve`, `capture`, `verify`, `lookup`, `descriptor`, `stage`, `stage-resume`, `adopt`, `adopt-resume`, `rollback-stage`, `rollback-adopt`, `plan`.

JSON records this tool writes use UTF-8, indent 2, sorted keys, a trailing newline, and no BOM. Return bodies and payload bytes are stored raw. They are not canonicalized. Paths in records are posix paths relative to the declared book root unless this contract names a backup path.

## Layout declaration

File: `{book}/return-line-layout.json`. Schema `return-line-layout/1`.
Exact keys: `schema`, `book`, `allocation`, `sequential_allocation`, `bands`.
`allocation` is `line-pass`. `sequential_allocation` is false.
`bands` is exactly `{"5":"matched-workflow-return-line","7":"page-local-colab"}`.
`book` is the book name string, such as `00.00.10.work`, not a filesystem path.

`init --book PATH --name NAME` writes that file only when it is absent. The same bytes are idempotent. Different bytes are refused. `init` refuses when PATH is the live work book, when PATH contains a child `0100.band.returns`, or when PATH is not a directory. The live work book is `00.kernel/00.00.10.work` under the repository that contains this lab. `init` does not write that file into the live book.

`reserve`, `capture`, `verify`, `lookup`, `descriptor`, `stage`, and `adopt` require this file. `plan` does not, and `plan` does not create it.

## New-work bytes

Schema `return-line-capture/1`. This is not `return-capture/1`. Historical reservation, manifest, and receipt files are not rewritten into this schema.

One pass is one `05.NN` on one page. Identity is book + page + batch. One submission occupies that pass. A second pass on the same page adds another tail on the same `N1NN.subject` or the same N7 page. It does not take another page number.

Reservation exact keys: `schema`, `kind`, `submission_id`, `origin`, `expected_outputs`, `submitter`, `reviewer`, `release`, `supersedes`, `reserved_at`, `line`, `sequential_allocation`.
`kind` is `reservation`. `sequential_allocation` is false. `supersedes` is null or a string with no path separator.
`origin` exact keys: `book`, `page`, `batch`. `book` comes from the layout, not from a caller override.
`line` exact keys: `workflow_space`, `target_page`, `target_number`, `subject`, `route`, `pass`, `return_path`, `custody_dir`. Those values are the placement route. `pass` is the batch.

Manifest exact keys: `schema`, `kind`, `submission_id`, `reservation_sha256`, `return`, `source_commit`, `captured_at`, `sources`, `omitted`, `required`.
`kind` is `manifest`. `source_commit` is null. `omitted` is `[]`. `required` equals `expected_outputs` in order.
`return` exact keys: `sha256`, `bytes`. There is no `includes_prime_review` field in this schema. That flag remains inside relocated `/1` manifests.
`sources` items exact keys: `logical`, `payload`, `sha256`, `bytes`. Payloads are `0001.blob`, `0002.blob`, in listed order.

Receipt exact keys: `schema`, `kind`, `submission_id`, `reservation_sha256`, `manifest_sha256`, `return_sha256`, `captured_at`, `acceptance`, `approved`, `accepted`, `published`.
`kind` is `receipt`. `acceptance` is null. `approved`, `accepted`, and `published` are false. A receipt does not accept, seat, publish, or finish the work.

Files for a new pass:

- `{target_page}/{batch}.return.md` — the raw return bytes
- `{target_page}/{batch}.custody/reservation.json`
- `{target_page}/{batch}.custody/manifest.json`
- `{target_page}/{batch}.custody/receipt.json`
- `{target_page}/{batch}.custody/return.md` — the same raw return bytes
- `{target_page}/{batch}.custody/payload/000N.blob`

The receipt is written last. Without a receipt whose hashes match, the pass is not complete.

Same identity and the same bytes are idempotent and do not rewrite the file. The same page and batch with a different submission, a different expected-output list, or different return or payload bytes is a conflict. The sealed files stay. The conflicting bytes are written under `{target_page}/{batch}.refused/attempt-NNN/` with `refusal.json`. That directory is evidence. It is not custody.

A different-name directory on the target number blocks `reserve` and `capture`. Check `occupied-line`. Nothing is written. Correction: the migration adopt path retires a verified staged occupant. This command does not overwrite a subject.

Reserved is not done. `verify` after `reserve` and before `capture` exits 1, descriptor state `reserved`, and the return hash and length are null.

## Descriptor

Exact keys: `schema`, `origin`, `route`, `target_page`, `return_path`, `custody_path`, `receipt_path`, `manifest_path`, `submission_id`, `custody_format`, `receipt_sha256`, `return_sha256`, `return_bytes`, `state`, `verification`.
`schema` is `return-line-descriptor/1`.
`origin` exact keys: `book`, `page`, `batch`.
`verification` exact keys: `tool_path`, `tool_sha256`, `result`, `evidence_path`.
`tool_path` is `labs/return-lines-pass01/return_lines.py`. `tool_sha256` is the hash of that file at runtime. `result` is the observed state word, not a boolean and not authority.
`state` is `complete`, `reserved`, `incomplete`, or `conflict`.
Missing return or receipt bytes use null hashes and a null length. They do not use the empty-file hash.
Paths are relative to the book root. The descriptor has no absolute path and no `expected_outputs` field. Expected-output checks are in the result envelope.

`complete` means this tool re-read the files, the route still matches `compute_route`, the expected outputs match the payload list, and the hashes match. For `legacy-relocated/1`, `complete` also means `verify_member` passed on the backup copy of the original directory and every copied custody file except `relocation.json` matches that backup. A caller flag cannot set `complete`. Copying a directory cannot set `complete`.

`descriptor` prints the descriptor only. `verify` and `lookup` print the envelope, including the descriptor when one can be built.

## Envelope

Schema `return-line-result/1`.
Exact keys: `schema`, `command`, `check`, `state`, `exit`, `correction`, `evidence`, `descriptor`, `detail`.
`exit` 0 is a finished command of the kind named in the command section below. `exit` 1 means a recorded pass is reserved or incomplete. `exit` 2 is a refusal or a byte conflict. `exit` 3 is an interrupted phase. A crash that skips the completion marker is not success.

`detail.acceptance` is null on every command. `detail.approved`, `detail.accepted`, and `detail.published` are false.

Refusals name the check, keep the input or the partial files, and set `correction` to a concrete next action plus: `Escalation: Codex Prime on 0521.return-placement/05.03. This tool does not decide meaning, acceptance, or live authority.`

Classes, which the check name distinguishes:

- Mechanical contract failure: bad JSON, wrong keys, hash mismatch, unsafe path. State `conflict` when sealed bytes remain, otherwise `refused`.
- Incomplete evidence: missing return, missing receipt, or 0154. State `incomplete` or `reserved`. Exit 1.
- Unknown capability: band other than 5 or 7. Check `return-placement-route/1`. State `refused`. Correction says to stop and read 0417.return-placement/06.01.md. No route is invented.
- Semantic disagreement: the audit route or target return differs from `compute_route`. Check `audit identity`. Stop. Do not pick a winner.
- Lack of authority: a mutating command aimed at the live book, or a request to treat this plan as permission. Check `live book` or `return-line-plan/1`.

## Migration

Two phases. Neither is implied by the other. A missing marker means that phase is not complete.

Backup root requirements: a directory outside the book; the book does not contain the backup and the backup does not contain the book; the backup is not inside the live work book; the backup does not contain `0100.band.returns`. Book and backup must allow `os.rename` on the same volume. A cross-device error stops. This tool does not delete the source in order to fake a rename.

`stage` and `stage-resume` read an audit of schema `return-placement-audit/2`. They record its sha256 and length. Resume refuses a different audit hash.

Before any copy, every record origin book must equal the layout book, and every record route and `target_return` must equal `compute_route`. A disagreement writes the journal finding and exits 2 with no copies and no marker.

Copies then proceed from the lowest `old_member` upward. Each regular file under that member is copied to `backup/sources/{old_member}/...` by reading and writing bytes. Reparse points, non-regular files, and link count other than 1 are refused before that item is copied. Containment is checked before the walk. The copy is compared with the audit hash and length. An extra file, a missing file, or a hash mismatch blocks the marker. The observed bytes stay in the backup as evidence. The book source is not deleted and is not repaired.

When `verify_exit` is 0, `verify_member` must pass on the book member during stage and on the backup member before adopt. A failure blocks the marker. When `verify_exit` is not 0 and `return.md` is absent, the reader refusal is recorded, the existing files are copied, and the record stays incomplete. No `return.md` is invented. 0154 is that case. When `verify_exit` is not 0 and `return.md` is present and the reader still fails, the marker is blocked.

Page-local records copy the existing tail to `backup/tails/{return_path}` and compare it with the member `return.md`. Inequality or a missing tail on a page-local record that has `return.md` blocks the marker. The tail in the book is not overwritten during stage.

Journal: `backup/stage-journal.json`, schema `return-line-stage-journal/1`.
Marker: `backup/stage-complete.json`, schema `return-line-stage-complete/1`. The marker is written only after every source and required tail has been copied and the checks above passed. `--interrupt-after N` counts files written by this invocation, saves the journal, exits 3, and does not write the marker. N of 0 interrupts before the first write. Resume skips files whose backup hash already matches the audit.

`rollback-stage` deletes only journaled backup files whose current hash still matches the journal, then empty directories it created under the backup. It does not touch the book. A hash mismatch stops and leaves the remaining evidence. It refuses when an adopt journal has already retired or created anything.

`adopt` and `adopt-resume` require the stage marker and the same audit hash. They re-hash every journaled backup file first. A mismatch stops and writes nothing new.

For each record, in the same order, before writing that record's line:

- List direct child directories of the book whose names start with `{target_number}.` and are not the target page.
- Each such occupant must be one of the staged source names. Any other occupant stops the phase. Evidence already written stays.
- A verified occupant is `os.rename`d to `backup/retired/{name}/`. That is the only retirement. It happens only after the stage marker exists. The original directory name is preserved under `retired`.
- Line bytes are then read from `backup/sources`, not from a directory that has been renamed away.

Final files, from those backup bytes:

- Every original file is copied into `{target_page}/{batch}.custody/` without changing its bytes.
- `relocation.json` is added beside them. Schema `return-line-relocation/1`. Exact keys: `schema`, `custody_format`, `old_member`, `original_destination`, `reservation_destination_rewritten`, `source_backup`, `return_sha256`, `return_bytes`. `custody_format` is `legacy-relocated/1`. `reservation_destination_rewritten` is false. `original_destination` is the reservation destination object, or null when the source has no readable reservation. `source_backup` is `sources/{old_member}`.
- When `return.md` exists, `{target_page}/{batch}.return.md` is written from those bytes. An existing tail with the same bytes is left untouched and is not listed as a created file. An existing tail with different bytes is a conflict: it is not overwritten, the page is not retired, and the adopt marker is not written.
- A source with no `return.md` gets no return tail. Its custody directory still receives the files that exist, plus `relocation.json`. Lookup state is `incomplete`.

`reservation.json` inside the custody copy is the original file. It is not edited to point at the new folder. `verify_member` is not called on the custody folder, because that folder is not an `01NN.slug` member and it contains `relocation.json`. `verify_member` is called on `backup/sources/{old_member}`.

Non-occupant source directories stay in the book. They are a second copy, not a deletion. Lookup by the old member name still resolves through `relocation.json` and the index.

Journal: `backup/adopt-journal.json`, schema `return-line-adopt-journal/1`.
Marker: `backup/adopt-complete.json`, schema `return-line-adopt-complete/1`, only after every record is written or recorded incomplete on purpose, the index is written, and no block remains. Interrupt behavior matches stage. A partial line without the marker is not an adopted book.

Index: `{book}/return-line-index.json`, schema `return-line-index/1`. It is a derived view. Items carry `old_member`, `submission_id`, `origin`, `return_path`, `custody_path`, `state`, `custody_format`. Lookup may use it to find a path. Lookup then re-reads the files. A stale `state` value in the index cannot grant `complete`.

Migration pointer: `{book}/return-line-migration.json`, schema `return-line-migration/1`. It records the backup path used by adopt so lookup can find the rollback copy. The shared descriptor does not carry that absolute path. If the backup copy is missing, a legacy record is not `complete`.

`rollback-adopt` removes the adopt marker first, after recording its hash, so a crash cannot leave the phase looking complete. It then deletes journaled created files whose hashes still match, removes empty directories that deletion leaves, and renames retired directories back when the book slot is empty. A hash mismatch or a slot that is already occupied stops and keeps the evidence. It does not delete a book file that the journal does not list.

The 18 occupied lines on the audited book are an input to rehearsal and to the live plan. They are not hard-coded as the only possible occupants. The rule is the directory scan above.

## Live plan

`plan --book --audit --out` is read-only toward the book except for the `--out` file. `--out` must not lie inside a capture member and must not be `0100.band.returns`. On the live book this pack writes only `evidence/build05.03/migration-plan.json`.

The command calls pinned `build_plan` and writes schema `return-line-plan/1` with: `schema`, `live_moves` false, `live_apply` false, `enforcement` `pending`, `sequential_allocation` false, `placement_plan` (the full plan), `new_work_route`, `post_audit_changes`, `preconditions`. Exit 0 means the plan file was written. It does not mean migration is authorized. Envelope state stays `incomplete`.

No command in this pack performs live apply, live adopt, or live retirement. The placement candidate's live-book guard is not removed.

## Command results

| command | exit 0 means | custody state |
| --- | --- | --- |
| init | layout present and identical | not a return |
| reserve | reservation bytes stored or already identical | `reserved` |
| capture | receipt hashes match the written bytes | `complete` |
| verify, lookup, descriptor | descriptor state `complete` | the descriptor state; exit 1 when reserved or incomplete; exit 2 on conflict |
| stage, adopt | that phase marker is valid | not Director acceptance |
| rollback-stage, rollback-adopt | the journaled reversal finished | not a deletion of the only copy |
| plan | the read-only plan file was written | live migration remains incomplete |

## Integration patch

evidence/build05.03/integration-patch.md names the current caller files and their hashes. It is not applied. Those files stay as Grok-2 reviewed them. Old-format reads remain available. Live enforcement stays pending until Prime applies that pin change. This lab being present does not enforce the current book.

## Out of scope

No live move. No edit to labs/return-placement-pass01, labs/return-capture-pass01, existing app modules, 0522, or the seam. No Git write. No call to the sequential allocator. No creation of `0121.return-placement` on the live book. No allocation of 0184. No held AR-01 inventory, bridge, or race fixture. No new status engine. Compute does not decide meaning.
