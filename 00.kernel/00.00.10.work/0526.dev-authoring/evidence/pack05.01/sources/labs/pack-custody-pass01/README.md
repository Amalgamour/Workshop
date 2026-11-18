# Pack custody checker, pass 01

**batch:** `00.kernel/00.00.10.work/0504.app-entry/05.07.md`
**state:** read-only development tool. Not an application entry, not a release, and not an instruction to run the sources it checks.

`pack_check.py` compares declared snapshot bytes with the bytes named by a pack manifest. A clean result means only that those bytes match. It does not judge meaning, instruction sufficiency, approval, release, dependencies, or whether executing a pinned source is safe or appropriate.

The pinned book checker `labs/book-orientation-pass01/check_book.py` is not part of this tool and is not modified. Git reads follow its discipline: one local revision, `GIT_OPTIONAL_LOCKS=0`, `GIT_TERMINAL_PROMPT=0`, no fetch, no checkout, no config write. Blob bytes are read with `git cat-file --batch` on stdin so a long path is not a worktree path and is not passed to `git show`.

## Formats

The format is always explicit. The tool does not guess.

`tsv` is a file whose first line is exactly `path`, a tab, `sha256`, a tab, `bytes`. Each later line is one source. The caller passes `--root`, the directory that contains those relative paths. The older clerk example uses `inputs/` as that root.

`prime-pack-sources/1` is a JSON object. `sources` is a non-empty list of objects with `path`, `sha256`, `bytes`, and `snapshot`. Snapshot paths resolve under the directory that contains the manifest. Optional top-level `commit` and `repository` are copied into the report as labels. They are not a commit to resolve and not a repository to fetch. Do not pass `--root` with this format.

SHA-256 must already be 64 lowercase hex characters. `bytes` must be a nonnegative integer. A JSON boolean is not an integer. Duplicate keys, duplicate paths, and paths that differ only by case are invalid. Comparison uses the raw bytes, so a CRLF file does not match an LF hash.

Paths must already be canonical and relative. Absolute paths, drive paths, UNC paths, backslashes, `.`, `..`, empty segments, trailing spaces or dots, and non-NFC spellings are rejected. The manifest is hashed and parsed before any snapshot is opened. A row that names another manifest is hashed as bytes and is not loaded or executed.

A symlink or junction on a snapshot path, or on a directory above it, is a finding. The checker does not follow it. The snapshot root itself must be a real directory.

## Git mode

`--git-repo` and `--rev` together read the manifest and the snapshots as blobs at one commit. `--rev` is resolved once with `git rev-parse --verify --end-of-options <rev>^{commit}`. The worktree, the index, and any remote are ignored. A missing blob stays missing even if a worktree file has the same name. `--manifest` and, for TSV, `--root` are repository-relative paths.

On Windows, `CreateProcess` runs `git.exe` and skips a `git.cmd` earlier on `PATH`. The tool resolves `git` with the process `PATH` and then starts that file. Global Git config is not changed.

## Report and exit codes

Without `--json`, the report is text on stdout. With `--json`, stdout is one `pack-custody-report/1` object. Expected failures do not print a traceback. A missing `--format` or other argparse error uses argparse's own stderr.

- **0:** every declared snapshot matched.
- **1:** the manifest was valid, and at least one snapshot was missing, mismatched, linked, unreadable, or not a file or blob.
- **2:** the manifest or the invocation was invalid or unsupported, or the tool failed.

`not_checked` is always present. It names meaning, instruction sufficiency, approval and release, dependencies, execution safety, and live-source drift. Drift does not rewrite a snapshot and does not, by itself, fail an intact historical blob. This slice has no live-source comparison and no fix mode.

## Run

```text
python -B pack_check.py --format tsv --manifest PACK\source-manifest.tsv --root PACK\inputs
python -B pack_check.py --format prime-pack-sources/1 --manifest PACK\source-manifest.json --json
python -B pack_check.py --format tsv --git-repo REPO --rev REV --manifest source-manifest.tsv --root inputs --json
python -B pack_check.py --format prime-pack-sources/1 --git-repo REPO --rev REV --manifest source-manifest.json
python -B tests\test_pack_check.py
```

The tests build disposable directories and repositories. They do not modify the shared pack fixtures. A file symlink needs a privilege this machine does not grant (`WinError 1314`); that one test is skipped and the junction case still runs. A path longer than 260 characters is stored with nested `git mktree` calls and is not checked out. `git mktree` accepts one path segment at a time.

## Limits

A pass is not pack acceptance. The tool does not install dependencies, call a model, or start the files it hashes. Filesystem reads use the extended `\\?\` path on Windows and still refuse reparse points. A snapshot whose absolute path exceeds the process path limit can be unreadable on disk even when the same blob is readable from Git. This slice does not change that limit and does not set `core.longpaths`.
