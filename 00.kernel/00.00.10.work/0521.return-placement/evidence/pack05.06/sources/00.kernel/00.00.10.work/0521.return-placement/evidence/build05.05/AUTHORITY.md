# Authority — plan-bound recorded release

This file is the authority delta for the 05.05 tooling build. It does not authorize `D:\Git\lib-build\00.kernel\00.00.10.work`. It does not install a sentinel. The fixture schema from 05.04 remains the rule for an ordinary disposable copy and is not extended to a real book.

## Records

JSON, UTF-8, no BOM, exact keys. Hashes are 64 lowercase hex characters. Lengths are non-negative integers and not booleans. Paths are absolute. `operations` is a non-empty list of unique command names. There is no operation named `all` or `force`.

### `return-line-director-release/1`

The external release file. Keys: `schema`, `book`, `book_path`, `executor`, `release_text`, `layout_sha256`, `plan_sha256`, `plan_bytes`, `audit_sha256`, `audit_bytes`, `backup_root`, `staging_root`, `retired_root`, `operations`.

`book` is `00.00.10.work`. `executor` and `release_text` are non-empty, at most 4096 characters. `release_text` may contain LF and tab. Other control characters are refused. `executor` has no control characters. The text is not compared to `invocation.txt` or to `evidence/build05.04/release.txt`.

### `return-line-recorded-release/1`

The `--authorization` file for a designated copy. Keys: `schema`, `synthetic`, `release_path`, `release_sha256`, `release_bytes`, `executor`, `book`, `book_path`, `layout_sha256`, `plan_sha256`, `plan_bytes`, `audit_sha256`, `audit_bytes`, `backup_root`, `staging_root`, `retired_root`, `operations`.

`synthetic` must be false. On every check the tool re-reads `release_path` and requires those exact bytes. These fields must then be equal, paths compared with the tool's path normalization: `book`, `book_path`, `executor`, `layout_sha256`, `plan_sha256`, `plan_bytes`, `audit_sha256`, `audit_bytes`, `backup_root`, `staging_root`, `retired_root`, `operations`. A disagreement refuses. The tool does not choose one side.

The release file and the authorization file must each sit outside the target book and outside the live work book, and they must not be the same path. The plan file is re-read. Its hash and length must match. `live_moves` and `live_apply` must be false. The audit file is re-read at the start of every authorized command. Audit-listed member files are compared to the book before preflight, init, stage, reconstruct, and publish, including resumes. A difference refuses before a root is created. Retire, rollback, reserve, and capture do not demand that a member already moved out of the book still sit there. Those commands keep the pass02 backup and journal byte checks.

The three roots must match the command, stay outside the book, stay outside each other, not contain `0100.band.returns`, and share the book's volume.

A matching record authorizes the named operations on a copy only after `designate_live` has marked that copy in this process. It does not authorize the canonical live book in this pack.

### `return-line-release-candidate/1`

Keys: `schema`, `active`, `book`, `book_path`, `executor`, `release_text`, `layout_sha256`, `plan_sha256`, `plan_bytes`, `audit_sha256`, `audit_bytes`, `backup_root`, `staging_root`, `retired_root`, `operations`, `unresolved`.

`unresolved` is a non-empty list of strings. `active` false yields reason `candidate is not authority`. `active` true yields reason `candidate claims active authority` and is still not executed. Preflight returns that refusal and writes nothing.

### `return-line-authorization/1`

Unchanged pass02 fixture. `synthetic` true, executor `Codex Prime`, release text equal to `evidence/build05.04/release.txt`. It authorizes an ordinary door-marked disposable copy. On a designated-live copy it refuses even when every fixture field matches. On the canonical book it refuses with `live execution`.

## Correction route

To change a checked plan, write a new director-release file and a new recorded-release file that pins the new file bytes, then review that pair. The previous pin does not follow the edited plan. This builder does not write that pair for the live book. Tests may write a pair whose `release_text` says it is a disposable test recording. That pair is not a Director release.

## Proposal bindings that stay unresolved

The candidate that the run writes uses the paths in `CONTRACT.md`. Unresolved choices, all of which block execution:

- The Director has not approved the staging, backup, or retirement paths.
- This invocation is not an execution release, and Prime has not recorded one.
- The executing identity is not recorded for a live cutover.
- `0154.colab-support-first-0501` stays incomplete. No return is invented.
- Pending captures `0121` through `0126` have no receipt and no task association in this pack. They are not the historical members `0121.archive-resolution-0508` through `0126.boot-members-0509`.
- Retained bytes are split across `occupants/` and `originals/`. The historical reader has no adapter. No single book-shaped archive is claimed.
- Old sequential reserve closure is not built. Claude's allocation-lock sentinel is not adopted and is not installed.

## Interface facts for a later app integration

These are observations for a later pack. They are not installed into `app/` or into callers.

C1. The line tool under test is `labs/return-lines-pass03/return_lines.py`. Its sha256 and length are the bytes on disk after this build, cited by verification. The predecessor remains pass02 at the pin in `CONTRACT.md`. No production path is guessed.

C2. A book with `0100.band.returns` passes `--authorization`, `--audit`, `--plan`, `--backup`, `--staging`, and `--retired` in addition to the command's own arguments. Refusal checks include `live execution`, `return-line-authorization/1`, `return-line-recorded-release/1`, `return-line-director-release/1`, `return-line-release-candidate/1`, `return-line-plan/1`, `audit identity`, `stale source`, and `filesystem`. There is no live-path override argument. `designate_live` is not a CLI flag.

C3. `lookup --member` keeps the pass01 descriptor and adds `detail.new_home` plus `detail.retained_original`. The archive field is `retained_original.retired_rel`, either `originals/{name}` or `occupants/{name}`, under the caller-supplied retired root. That root is not a Director-approved live path.

C4. This tool does not write a sentinel and does not verify one. A sentinel phase is not part of this schema.
