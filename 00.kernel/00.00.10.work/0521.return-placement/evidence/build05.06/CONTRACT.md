# Contract — return-lines pass04

Schema of this file: `return-line-contract/0506`. Written before `labs/return-lines-pass04`. The tool follows this file. A later verification command does not revise it.

## Pins

| Input | sha256 | bytes |
|---|---|---|
| pass03 `labs/return-lines-pass03/return_lines.py` | `78cc4d8679bb6e54b3f2456ce777643da7a9a650ef5c79c216abd38a4c209c63` | 33349 |
| pass02 `labs/return-lines-pass02/return_lines.py` | `6691d0587ab97ba24a1709c9950b506961152939e2d112ee608f9dbd23e92908` | 82908 |
| pass01 `labs/return-lines-pass01/return_lines.py` | `863968c59974d85910626ba5e80cf49f14a3186c8d33b855efe00bf6ccec378a` | 100897 |
| placement `labs/return-placement-pass01/return_placement.py` | `db96f7023c73dcececba0e7d42b821da8193af7534a4bdf8cd2e5d6cd53d0754` | 66097 |
| reader `labs/return-capture-pass01/return_capture.py` | `8f3da5c651f6924fca6dedb0b95da7d181eb58884dc030dd9cbc3d8b6a5b15ac` | 45767 |
| audit `0417.../audit-corrected.json` | `c3bf8c1e25bfd1a59ce40230d87f650897f3105691db732eadfe5abf4e275606` | 391778 |
| door `0100.band.returns/01.md` | `c9ff0949c09268451a8e2a2113c1612047b374b3ecc0b3c177b6c5fd22b6842d` | 10206 |
| pack05.06 source-manifest | `07924f4d2fbcf9b68c500e46d4c2cbbdf54b922f32902be04f3c52083db4d22c` | 7062 |
| seam `colab/labs/0709.return-migration-check/pass01/seam.py` | `dccd66af39dc8ca688610ca67a7b8903e6631191df2f232c3cd21574e8f08a4f` | 5625 |
| review loop pass03 | `47f47d16426e4d69987398a8244877de58b6089326874f3279003f696814450b` | 55474 |
| prime cycle pass03 | `496b4d721cfb136fa847d998d421209616c60508beb5cda5620af73041eed17c` | 76045 |

The successor loads pass03 by that pin. Pass03 loads pass02 by its pin. Pass02 loads pass01, placement, and the reader by the pins it already checks. A mismatch writes nothing. Pass01, pass02, and pass03 on disk are not patched. The layout body for book name `00.00.10.work` stays 216 bytes, sha256 `2c414ac4e11cd874d28b8c477b7eed30ee477e216ed1653552d802f03c4d7804`.

`06.10.md` records that pass03 still refuses the canonical book before it evaluates a recorded release, and that `designate_live` is the only way pass03 accepts that schema. Pass04 is the repair. It does not edit pass03.

## What this pack releases

Permission to implement the normal recorded-authorization path and to prove it on disposable copies. Permission to implement that path is not permission to migrate `D:\Git\lib-build\00.kernel\00.00.10.work`. This build writes no `return-line-director-release/1` file and no `return-line-recorded-release/1` file whose `book_path` is that workbook. It does not call init, stage, reconstruct, publish, retire, rollback, reserve, or capture on that workbook.

`evidence/build05.06/invocation.txt`, `evidence/build05.05/invocation.txt`, and `evidence/build05.04/release.txt` are not a migration release. The tool has no hard-coded release string that authorizes a book.

## One validator

`inspect` is the production decision. `require_authorization` and `patched_assert` use that same decision. `live_refusal` does not refuse. There is no earlier branch that refuses because the path is the real workbook or because a record names that workbook.

A path is the canonical identity when it is the real workbook, or when the in-process test seam `classify_canonical` has reported that absolute path. The seam is not a CLI flag. It does not skip a binding check, a source check, or the recorded-schema rule. The production CLI has no `designate_live`, `--designate`, `--force`, or `--allow-live`.

The same recorded-release function runs for a disposable copy and for a canonical identity. These preconditions are the whole gate:

1. `--authorization` exists and is `return-line-recorded-release/1`.
2. `synthetic` is JSON false.
3. `release_path` is a different file, outside the target book and outside the real workbook. Each check re-reads it. `release_sha256` and `release_bytes` match those bytes. Its schema is `return-line-director-release/1`.
4. These fields are equal, with paths compared by the tool's normalization: `book`, `book_path`, `executor`, `layout_sha256`, `plan_sha256`, `plan_bytes`, `audit_sha256`, `audit_bytes`, `backup_root`, `staging_root`, `retired_root`, `operations`. A disagreement refuses. The tool does not choose a side.
5. `book` is `00.00.10.work`. `book_path` is the command's book. `executor` and `release_text` are plain text. `release_text` may contain LF and tab. The text is not compared to an invocation file.
6. The command is in `operations`. There is no operation named `all` or `force`. Preflight may omit `--operation`, in which case the list is not required to contain a particular command.
7. `layout_sha256` is the pass01 layout body for `00.00.10.work`. An existing `return-line-layout.json` in the book must already equal that body.
8. The plan file is re-read. Its hash and length match. `live_moves` and `live_apply` are false.
9. The audit file is re-read. Its hash and length match.
10. The three roots match the command, sit outside the target book, outside each other, and outside the real workbook, do not contain `0100.band.returns`, share the book's volume, and already have parent directories. The check does not create a parent. A cross-device rename stops. The tool does not copy and then delete.
11. For preflight, init, stage, reconstruct, and publish, including resumes, every audit-listed member file still in scope matches the audit bytes. A difference refuses before a root is created. Retire, rollback, reserve, and capture do not demand that a member already moved out of the book still sit there. Those commands keep the pass02 backup and journal byte checks.
12. A mutation command binds that record in the same process before `assert_mutable` runs. A later process does not inherit the binding. Preflight does not bind a later command.

A synthetic `return-line-authorization/1` record still authorizes an ordinary door-marked copy under pass02's fixture rules, including `synthetic` true and the 05.04 fixture release text. The same record refuses when the command book is the canonical identity or when the record's `book_path` is that identity. Reason: `fixture authorization cannot authorize the canonical book`.

`return-line-release-candidate/1` never authorizes. `active` false yields `candidate is not authority`. `active` true yields `candidate claims active authority` and is still not executed.

No conflict between these records is resolved by picking the more permissive one. The file passed in `--authorization` is the only record consulted. A Prime label, a boolean, a build invocation, or the word force is not a record.

The correction route for a changed plan is a new director-release file and a new recorded-release file that pins the new bytes. Editing the plan, the release file, or the recorded pin alone refuses before the next phase. This is a byte record. It is not a cryptographic identity guarantee.

## Sequence

The pass02 order is unchanged: plan, authorization, init, stage, reconstruct, verify logical pages, publish with occupant displacement, retire every remaining audited old member, lookup, rollback-retire then rollback-publish. `adopt` stays refused. `0154` stays incomplete. Page-local tails stay on their pages. Raw custody bytes and N7NN tails are not normalized.

`preflight` is read-only and separate from materialization. It uses the same checks and writes no layout, archive, marker, or root. Exit 0, check `readiness`, means the record matched. `detail.mutated`, `detail.executed`, and `detail.live_execution` are false. That exit does not mean the migration ran.

Directories for backup, staging, and retired are created only after a mutation command's checks succeed.

## Retirement layout

Publication moves colliding occupants to `{retired}/occupants/{name}`. The occupant set comes from `lines.occupants(book, route target_number, route target_page)`. The target number is the line the directory currently occupies, from `compute_route` on the origin page. It is not the record's own `target_line`. Retirement moves every remaining audited old member to `{retired}/originals/{name}`. Both sets are retired. The pass04 README says that. The pass02 README is not edited. The tool does not encode the counts 18 or 65.

Lookup still delegates the descriptor to pass01 and adds `detail.new_home` and `detail.retained_original`. `retired_rel` is `originals/{name}` or `occupants/{name}`. There is no single book-shaped archive. The historical reader is `return_capture.py` `verify --book --member`. Its member argument cannot contain a slash, and it expects a capture envelope as a direct child of `--book`. The rehearsal points that reader at the retired root, at `originals/`, and at `occupants/`, and records the exits. An adapter is not added. Historical readers and old sequential-writer closure stay separate gates.

## CLI

Tool: `labs/return-lines-pass04/return_lines.py`. Verification records its sha256 and length after the file exists. The predecessor pin remains pass03 in the table above.

Read-only preflight:

`preflight --book --authorization --audit --plan --backup --staging --retired [--operation NAME]`

Plan, init, stage, reconstruct, publish, retire, rollback, reserve, and capture keep the pass02 arguments. A book with `0100.band.returns` passes `--authorization`, `--audit`, `--plan`, `--backup`, `--staging`, and `--retired` on those commands. Exit 0 envelopes do not receive an escalation sentence. Refusals raised by pass04 name `0521.return-placement/05.06`. Fixture refusals that pass02 itself produces keep the 05.04 sentence.

## Unresolved candidate roots

These paths are candidates from the 05.05 proposal. The Director has not approved them. This pack does not create them, does not move files into them, and does not commit them.

| Role | Path |
|---|---|
| Staging | `D:\librarian\return-placement\0521-staging` |
| Separately verified backup | `D:\librarian\return-placement\0521-backup` |
| Git-trackable retirement | `D:\Git\lib-build\00.archive\0521.return-lines` |

All three are on `D:`, outside the work book, and outside each other. They were absent when this contract was written.

## Later declaration-only pin

Grok-1's concurrent pack 05.07 integrates reviewed pass03 access on copies. This pack does not edit that app code, that adapter, or unfinished 05.07 outputs. After Prime reviews this return, a later pack can change the app declaration from `labs/return-lines-pass03/return_lines.py` at `78cc4d8679bb6e54b3f2456ce777643da7a9a650ef5c79c216abd38a4c209c63` to `labs/return-lines-pass04/return_lines.py` and the hash verification records. That change is declaration-only. This pack does not make it. It does not write a sentinel and does not verify one.

## Interface facts for that later change

C1. The line tool under test is `labs/return-lines-pass04/return_lines.py`. Its sha256 and length are the bytes on disk after this build, cited by verification. The loaded predecessor remains pass03 at the pin above.

C2. Refusal checks include `authorization`, `return-line-authorization/1`, `return-line-recorded-release/1`, `return-line-director-release/1`, `return-line-release-candidate/1`, `return-line-plan/1`, `audit identity`, `stale source`, and `filesystem`. The production path has no check whose reason is `this pack does not execute the canonical live book`. There is no live-path override argument.

C3. `lookup --member` keeps the pass01 descriptor and adds `detail.new_home` plus `detail.retained_original`. The archive field is `retained_original.retired_rel`, either `originals/{name}` or `occupants/{name}`, under the caller-supplied retired root. That root is not a Director-approved live path.

C4. This tool does not write a sentinel and does not verify one. A sentinel phase is not part of this schema.
