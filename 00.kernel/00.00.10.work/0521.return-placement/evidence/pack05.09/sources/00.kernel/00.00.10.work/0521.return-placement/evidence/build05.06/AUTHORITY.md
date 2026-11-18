# Authority — one recorded-release validator

This file is the authority decision table for the 05.06 tooling build. It does not authorize `D:\Git\lib-build\00.kernel\00.00.10.work`. It does not install a sentinel. The fixture schema from 05.04 remains the rule for an ordinary disposable copy and is not extended to a canonical book.

## Decision

| Record on `--authorization` | Ordinary door-marked copy | Canonical identity |
|---|---|---|
| Absent path | Refuse `authorization is absent` before mutation | Same refusal. The missing file is not a special live veto. |
| `return-line-release-candidate/1` | Refuse. `active` true still does not execute | Same refusal. |
| `return-line-authorization/1` with `synthetic` true | Pass02 fixture rules, including the 05.04 release text | Refuse `fixture authorization cannot authorize the canonical book`. |
| `return-line-recorded-release/1` with `synthetic` false and matching release, book, operations, layout, plan, audit, roots, and current source | Authorize the named operations. No designation call | The same function and the same preconditions. No designation call. |
| Any other schema, or `synthetic` not false on a recorded schema | Refuse before mutation | Same refusal. |

Canonical identity means the real workbook path, or one absolute disposable path reported by `classify_canonical` in that process. The seam is how a test proves the canonical branch without mutating the real workbook. It is not a second validator and it is not a CLI permission.

A matching recorded release is a byte record of a Director release file. It is not a cryptographic identity guarantee. This build does not create that pair for the real workbook. A disposable pair whose `release_text` says it is a test recording is not a Director release.

## Records

JSON, UTF-8, no BOM, exact keys. Hashes are 64 lowercase hex characters. Lengths are non-negative integers and not booleans. Paths are absolute. `operations` is a non-empty list of unique command names. There is no operation named `all` or `force`.

### `return-line-director-release/1`

The external release file. Keys: `schema`, `book`, `book_path`, `executor`, `release_text`, `layout_sha256`, `plan_sha256`, `plan_bytes`, `audit_sha256`, `audit_bytes`, `backup_root`, `staging_root`, `retired_root`, `operations`.

`book` is `00.00.10.work`. `executor` and `release_text` are non-empty, at most 4096 characters. `release_text` may contain LF and tab. Other control characters are refused. `executor` has no control characters. The text is not compared to `invocation.txt` or to `evidence/build05.04/release.txt`.

### `return-line-recorded-release/1`

The `--authorization` file. Keys: `schema`, `synthetic`, `release_path`, `release_sha256`, `release_bytes`, plus the binding fields of the director release.

`synthetic` must be false. On every check the tool re-reads `release_path` and requires those exact bytes. The binding fields must then be equal. The release file and the authorization file must each sit outside the target book and outside the real workbook, and they must not be the same path.

The plan file is re-read. Its hash and length must match. `live_moves` and `live_apply` must be false. The audit file is re-read at the start of every authorized command. Audit-listed member files are compared to the book before preflight, init, stage, reconstruct, and publish, including resumes. A difference refuses before a root is created. Retire, rollback, reserve, and capture do not demand that a member already moved out of the book still sit there.

The three roots must match the command, stay outside the book, stay outside each other, not contain `0100.band.returns`, and share the book's volume. Their parents must already exist. Readiness does not create them. Materialization creates the root directories only after a mutation command passes the checks.

A matching record authorizes the named operations on the named book. The book may be a disposable copy or the canonical identity. `designate_live` is not part of the production path and is not a CLI flag.

### `return-line-release-candidate/1`

Keys: `schema`, `active`, `book`, `book_path`, `executor`, `release_text`, `layout_sha256`, `plan_sha256`, `plan_bytes`, `audit_sha256`, `audit_bytes`, `backup_root`, `staging_root`, `retired_root`, `operations`, `unresolved`.

`unresolved` is a non-empty list of strings. `active` false yields reason `candidate is not authority`. `active` true yields reason `candidate claims active authority` and is still not executed. Preflight returns that refusal and writes nothing. A candidate never authorizes the canonical book.

### `return-line-authorization/1`

Unchanged pass02 fixture. `synthetic` true, executor `Codex Prime`, release text equal to `evidence/build05.04/release.txt`. It authorizes an ordinary door-marked disposable copy. It does not authorize a canonical identity.

## Same-process binding

`patched_assert` reads the authorization bound for that command in that process. A recorded schema with `synthetic` false satisfies a door-marked copy and a canonical identity. A fixture schema with `synthetic` true satisfies only a book that is not the canonical identity. A missing binding refuses. The phase and byte checks in pass02 still run after the binding is accepted, including `arm_fault`, which is not a CLI flag.

## Correction route

To change a checked plan, write a new director-release file and a new recorded-release file that pins the new file bytes, then review that pair. The previous pin does not follow the edited plan. This builder does not write that pair for the live book. Tests may write a pair for a disposable copy. That pair is not a Director release.

## Proposal bindings that stay unresolved

Unresolved choices, all of which block a live cutover:

- The Director has not approved the staging, backup, or retirement paths named in `CONTRACT.md`.
- This invocation is not an execution release, and Prime has not recorded one for the live book.
- The executing identity is not recorded for a live cutover.
- `0154.colab-support-first-0501` stays incomplete. No return is invented.
- Pending captures `0121` through `0126` have no receipt and no task association in this pack. They are not the historical members `0121.archive-resolution-0508` through `0126.boot-members-0509`.
- Retained bytes are split across `occupants/` and `originals/`. The historical reader has no adapter. No single book-shaped archive is claimed.
- Old sequential reserve closure is not built. Claude's allocation-lock sentinel is not adopted and is not installed.

## Later pin

These are observations for a later pack. They are not installed into `app/` or into callers. After this return is reviewed, the app entry that now pins pass03 can be updated, declaration only, to `labs/return-lines-pass04/return_lines.py` and the hash in this return's verification. This pack does not make that edit. Grok-1's pass03 copy integration is a separate pack and is not edited here.
