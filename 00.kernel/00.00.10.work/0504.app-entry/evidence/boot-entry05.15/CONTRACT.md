# CONTRACT — recorded boot through the app entry

Batch: `0504.app-entry/05.15`. This file is the implementation contract written before `app/boot_tools.py`. It binds four app commands to the accepted recorded-boot tool. It is not kernel law. An orientation result is not authorization. A reviewer label is not authentication.

## Commands

```text
python <workspace>/app/librarian.py boot-prepare --request <request.json> --records <absolute-directory> --attempt <id>
python <workspace>/app/librarian.py boot-check --attempt <attempt-directory> --answers <answers.json>
python <workspace>/app/librarian.py boot-judge --attempt <attempt-directory> --judgement <judgement.json>
python <workspace>/app/librarian.py boot-show --attempt <attempt-directory> [--json]
```

Each named flag is required once, except `--json` on show, which is optional and has no value. Flags may appear in either order. The values are forwarded unchanged. A missing flag, a repeated flag, an unknown flag, or a positional argument is a wrapper refusal before the subprocess. There is no default records root, no default attempt, and no flag that selects a tool path.

## Pins

`app/prime-boot.json`, schema `librarian-prime-boot`, version 1. The same seven identities are fixed in `app/boot_tools.py`.

| Label | Path, relative to the code root | SHA-256 |
|---|---|---|
| prime_boot | `labs/prime-boot-pass01/prime_boot.py` | `54b23484f9e0812db92a623a8588175702682ebe14f8b0b915111daf51a91534` |
| prime_support | `labs/prime-support-pass01/prime_support.py` | `700d60d2e49c186d49e56a9a38058e21a722b4a5dd79d461453a305e8d904f70` |
| clerk_adapter | `labs/prime-support-pass01/clerk_adapter.py` | `2f30ba751f78ec9f7d2995739bebde0e3b6509eeab35ae29a9078385ff33f8d4` |
| check_book | `labs/book-orientation-pass01/check_book.py` | `fc16d2f68a3645050b6766ce18ce55f8169a0e2bad52d3392b4d059c629073a4` |
| return_capture | `labs/return-capture-pass01/return_capture.py` | `8f3da5c651f6924fca6dedb0b95da7d181eb58884dc030dd9cbc3d8b6a5b15ac` |
| return_inspect | `labs/return-capture-pass01/return_inspect.py` | `947915febaa5918f56b6be03c81840c030d081fcab9a3bead2cd660973a9999b` |
| clerk | `labs/clerk-handoff-pass02/clerk.py` | `f697a7e443117c3d1face62d3021f7634154d76214b77fadec1a5cc3c99d394c` |

The code root is the parent of the `app` directory that contains the entry. Each path is a relative forward-slash path. An empty segment, a backslash, a drive, an absolute path, `.`, or `..` is an escape. A symlink or junction on the declaration or on any path segment is refused and is not followed. All seven files are hashed before the subprocess. A mismatch, a missing file, or a declaration that is not the pinned identity refuses with `stop:` and exit 2. The accepted tool is not started.

These paths are not taken from the request, from the caller cwd, or from an override flag. The request may still name tool paths. The backend checks those paths. This wrapper does not rewrite them and does not treat them as the pin source.

## Subprocess

Argument array, with no shell:

```text
<current Python> -B <pinned prime_boot.py> prepare|check|judge|show <forwarded flags>
```

No auto-answer, auto-judge, acknowledgement, claim, queue, or dispatch. The child environment is the caller environment plus `PYTHONDONTWRITEBYTECODE=1`. The wrapper does not create a records root, an attempt, a scratch directory, or a book file.

Stdout and stderr are copied as bytes. The child exit is preserved.

| exit | meaning, from the accepted tool |
|---|---|
| 0 | the stage completed with a positive result |
| 1 | the stage completed with a recorded negative result |
| 2 | refused, or prepare failed at a stage and recorded that failure |
| 3 | incomplete: raw input is present and the terminal record is not readable; replay does not finish the stage |

A non-integer exit, a failed start, or a timeout is a wrapper refusal. The same-user gap between the hash read and the subprocess is not closed. Path checks are not an operating-system sandbox.

## Meaning

Prepare, check, and judge write only where the backend writes, inside the records root the caller passed. Show is read-only. This wrapper does not reimplement grading, packet logic, or retry. An attention item, an orientation result, and a reviewer label grant no role and no new work. `authority` stays the backend's own value.

## Not exposed

Model calls, live registration, a default records root, role edits, and normal run are outside these commands. `run` stays refused.

## Gaps

The wrapper does not prove every read the lab may make from a request path. `clerk.py` is pinned here because the pack lists it. The backend's own pin map does not name that file, and a request with Clerk jobs is refused by the lab. A clean or oriented result is not release readiness, not acceptance, and not an exactly-once guarantee. File-symlink creation may be unavailable (WinError 1314). The entry resolves its own file path before this wrapper sees the code root; links under the tool paths are still refused.
