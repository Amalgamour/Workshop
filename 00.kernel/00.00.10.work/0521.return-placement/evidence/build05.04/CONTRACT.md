# Contract — return-lines pass02

Schema of this file: `return-line-contract/0504`. Written before `labs/return-lines-pass02`. The tool follows this file. A later verification command does not revise it.

## Pins

| Input | sha256 | bytes |
|---|---|---|
| pass01 `labs/return-lines-pass01/return_lines.py` | `863968c59974d85910626ba5e80cf49f14a3186c8d33b855efe00bf6ccec378a` | 100897 |
| placement `labs/return-placement-pass01/return_placement.py` | `db96f7023c73dcececba0e7d42b821da8193af7534a4bdf8cd2e5d6cd53d0754` | 66097 |
| reader `labs/return-capture-pass01/return_capture.py` | `8f3da5c651f6924fca6dedb0b95da7d181eb58884dc030dd9cbc3d8b6a5b15ac` | 45767 |
| audit `0417.../audit-corrected.json` | `c3bf8c1e25bfd1a59ce40230d87f650897f3105691db732eadfe5abf4e275606` | 391778 |
| door `0100.band.returns/01.md` | `c9ff0949c09268451a8e2a2113c1612047b374b3ecc0b3c177b6c5fd22b6842d` | 10206 |
| pack05.04 source-manifest | `e9e2d7af52c12b0643444704b4183e18ea9e0fee15812962ddad7d2b86d2fe21` | 12387 |
| seam `colab/labs/0709.return-migration-check/pass01/seam.py` | `dccd66af39dc8ca688610ca67a7b8903e6631191df2f232c3cd21574e8f08a4f` | 5625 |
| review loop pass03 | `47f47d16426e4d69987398a8244877de58b6089326874f3279003f696814450b` | 55474 |

The successor loads pass01 by that pin and then calls pass01's loader for placement and the reader. A mismatch writes nothing. Pass01 on disk is not patched.

## Sequence

1. `plan` is read-only. It may run before init. Its exit 0 only means the plan file was written. `live_moves` and `live_apply` stay false. The plan hash is bound. It is not required to equal the earlier live-book plan `52951e1dbc0f37fa7f8c76be390a9510999a6944d7dc9f4e20c00c365f326f66`.
2. The operator writes a synthetic `return-line-authorization/1` file outside the book. See `AUTHORIZATION.md`.
3. `init` writes the line-pass layout on the copy only.
4. `stage` copies every audited member into `{backup}/sources/{old_member}` and every page-local tail into `{backup}/tails/{return_path}`. The stage marker is pass01's `return-line-stage-complete/1`. Staging does not retire.
5. `reconstruct` builds `{staging}/pages/` as the corrected logical tree: raw custody bytes, raw return bodies, and a new `relocation.json`. The marker `return-line-reconstruction-complete/1` is written only after staged sources and logical links re-read equal.
6. `publish` re-checks that tree, displaces staged occupants into `{retired}/occupants/{name}`, then installs the logical pages. The marker is `return-line-publish-complete/1`. Pass01 `adopt-complete` is not this marker.
7. `retire` moves every remaining audited old member to `{retired}/originals/{name}` after the logical links still match. Members already displaced are recorded and not moved twice. The marker `return-line-retire-complete/1` requires zero audited old-member directories left in the book.
8. `lookup` and `descriptor` delegate the byte check to pass01. The descriptor key set stays `return-line-descriptor/1`. Lookup detail adds `new_home` and `retained_original`. Descriptor stdout is the descriptor alone.
9. `rollback-retire` then `rollback-publish` reverse those journals when hashes match and the book slot is empty. `rollback-stage` remains the pass01 backup rollback and refuses once publish has created or displaced anything.

`adopt` is refused. It is the predecessor path that leaves non-occupant directories in the active namespace.

## Logical page versus archived identity

Each reconstruction record has `archived_identity` (the old member name) and `logical_return_path` (the route's return path). Those strings are different. Custody bytes are copied, not canonicalized. `reservation.json` destinations are not rewritten. `relocation.json` uses pass01's `return-line-relocation/1` keys, `custody_format` `legacy-relocated/1`, and `reservation_destination_rewritten` false. `source_backup` is `sources/{old_member}` under the backup root.

A record with no `return.md` is `incomplete`. Its return hash and length are null. The logical return path is not created. Page-local routes keep the existing tail; publication does not overwrite a matching tail. A different tail blocks the marker.

The migration pointer `return-line-migration.json` keeps pass01's keys so pass01 lookup can find the backup. After retire, `{backup}/retirement-pointer.json` (`return-line-retirement-pointer/1`) names the retired root. Lookup uses it to report `retired_rel` as `originals/{name}` or `occupants/{name}`.

## Counts

`record_count`, `page_local_count`, and `incomplete_count` are `len` of the prepared records, the page-local routes, and the records with no return. The tool does not compare them to the literals 83 or 18. Readiness is every prepared record's link plus the next successful filing on a freed line, not a count of moves.

## New-work filings

After retire, reserve and capture use pass01's `return-line-capture/1` bytes. Two batches on one origin page are two passes on one line. A band-7 page stays on that page. Synthetic submission ids start with `synthetic-`. They are not task association and not real custody. The capture receipt stays `accepted` false. This build does not write a Prime receipt and does not call `return_capture.py`.

## Journals

| File | Schema |
|---|---|
| `{staging}/reconstruction-journal.json` | `return-line-reconstruction-journal/1` |
| `{staging}/reconstruction-manifest.json` | `return-line-reconstruction-manifest/1` |
| `{staging}/reconstruction-complete.json` | `return-line-reconstruction-complete/1` |
| `{backup}/publish-journal.json` | `return-line-publish-journal/1` |
| `{backup}/publish-complete.json` | `return-line-publish-complete/1` |
| `{retired}/retire-journal.json` | `return-line-retire-journal/1` |
| `{retired}/retire-complete.json` | `return-line-retire-complete/1` |
| `{backup}/retirement-pointer.json` | `return-line-retirement-pointer/1` |

Journals are evidence. They are not a second status ledger. The pass01 index remains a derived view. Pass01 stage and adopt journal schemas are unchanged and stay inside pass01.

Displaced and retired directories record a file list of relative path, sha256, and length. Rollback checks that list before any rename back. Created book files are removed on rollback-publish only when the current hash still matches. The marker is removed after that check and before the deletes. A mismatch or an occupied slot stops and leaves the remaining evidence.

## CLI delta (not applied to callers)

Tool: `labs/return-lines-pass02/return_lines.py`.

Forwarded, pass01 behavior, authorization required when the book has `0100.band.returns` or the command is listed below as always authorized:

- `init --book --name --authorization --audit --plan --backup --staging --retired`
- `reserve` and `capture` gain `--authorization --audit --plan --backup --staging --retired` beside the pass01 arguments
- `stage` and `stage-resume` gain those arguments beside `--book --backup --audit` and optional `--interrupt-after`
- `rollback-stage` gains the same authorization arguments

Always require authorization, including on a book that has no door:

- `reconstruct`, `reconstruct-resume`
- `publish`, `publish-resume`
- `retire`, `retire-resume`
- `rollback-publish`, `rollback-retire`

No authorization, because they do not call `assert_mutable`:

- `plan --book --audit --out`
- `verify --book --page --batch`
- `lookup` and `descriptor` with one of `--member`, `--submission`, or `--page` plus `--batch`

Refused: `adopt`, `adopt-resume`, `rollback-adopt`.

`--interrupt-after N` stops before the next write once N writes have happened in that call. N of 0 stops before the first write. The test seam `arm_fault(phase, skip, "partial")` is not a CLI flag. It writes a short file, closes it, then raises. Resume must not delete that file.

Envelopes stay `return-line-result/1`. Detail `acceptance` is null and `approved`, `accepted`, and `published` are false, including after the publish command. The publish command installs bytes on a copy. It does not set custody accepted.

## In-process guard

Pass01 `assert_mutable` stays in the pass01 file and still refuses the live book and any book that contains the door. The successor, after `require_authorization` succeeds, points the loaded module's `assert_mutable` at a wrapper. The wrapper always refuses `live_book_path()`. It allows a door-marked book only when the bound authorization's `book_path` is that book and `synthetic` is true. A book with no door is handed back to the original function. Other processes, including the seam's subprocess, load pass01 themselves and do not see the wrapper.

## Copies

Disposable books live under `D:\librarian\temp\0521-0504\`, on the same volume as their retired roots so `os.rename` can move a directory. Each run has its own directory. The tool and the rehearsal do not delete a run. A copy includes the band door, the audited member directories named by the audit in use, and the page-local tail files for page-local records in that audit. It does not include the rest of the repository or nested snapshot trees. The live fingerprint is the audit-listed source files plus the door. It is measured before and after. Live bytes are not a mutation target.

## Limits

Caller enforcement, `app/return_line_tools_v2.py`, a helper-reserve refusal, a live init, a band-door edit, and the 0525 dependency records are outside this contract. The seam is run read-only against frozen review-loop pass03 to show descriptor compatibility. `prime_cycle.py` is the consumer behind that seam's `prepare` call. This build does not edit it. No N3NN registration, no Git write, no network, no model call, no bot, no AR-01.
