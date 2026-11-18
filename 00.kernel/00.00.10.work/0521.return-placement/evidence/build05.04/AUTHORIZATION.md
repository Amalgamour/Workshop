# Authorization — return-line-authorization/1

This file is the authorization contract for the 05.04 tooling build. It is not a live-book authorization. The fixture used in tests is explicitly synthetic. It cannot authorize `D:\Git\lib-build\00.kernel\00.00.10.work`.

## Release text

The `release` field must equal `evidence/build05.04/release.txt` byte for byte. Those bytes are the Director invocation recorded in `06.07.md`: the user text, LF newlines, final LF. Codex Prime is the recorded executor under that release. The label alone is not permission. `synthetic` must be JSON `true`. `synthetic: false` is refused because this build does not release live execution.

## Schema

Exact keys, JSON object, UTF-8, no BOM:

| Key | Rule |
|---|---|
| schema | `return-line-authorization/1` |
| synthetic | JSON boolean `true` |
| executor | `Codex Prime` |
| release | exact release.txt bytes decoded as UTF-8 |
| book | `00.00.10.work` (the book name, not a path) |
| book_path | absolute path of the disposable book |
| layout_sha256 | sha256 of the pass01 layout body for that book name |
| plan_sha256 | sha256 of the read-only plan file named by the run |
| audit_sha256 | sha256 of the audit file |
| audit_bytes | length of the audit file |
| backup_root | absolute backup directory outside the book |
| staging_root | absolute reconstruction directory outside the book |
| retired_root | absolute caller-supplied retirement directory outside the book |
| operations | JSON list of command names this file allows |

`operations` must include each command the run will execute. Resume names are separate (`stage-resume`, `reconstruct-resume`, `publish-resume`, `retire-resume`). There is no `--force` and no operation that means "all".

## What a match requires

The command name is in `operations`. `book_path` is the book argument. The book name is the layout name. The audit file's sha256 and length match. The plan file's sha256 matches. The layout hash matches `layout_body("00.00.10.work")` from pinned pass01, which is 216 bytes, sha256 `2c414ac4e11cd874d28b8c477b7eed30ee477e216ed1653552d802f03c4d7804`. If the layout file already exists, its bytes must be that body. The three roots match the command arguments, are outside the book, are outside the live work book, do not contain `0100.band.returns`, and do not contain each other.

The live path is refused before any write even when `book_path` is that path and every other field matches.

## Scope

This authorization gates the successor tool in one process. It does not edit pass01, app modules, callers, or the band door. It does not select an approved live archive path. A retired root on a disposable copy is a test destination, not a Director-selected live archive.
