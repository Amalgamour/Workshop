# CONTRACT — prime-status, read-only

Batch: `0504.app-entry/05.14`. This file is the implementation contract written before `app/prime_intake.py`. It binds one app command to the accepted Prime status tool. It is not kernel law. A status result is not authority and is not release readiness.

## Command

```text
python <workspace>/app/librarian.py prime-status --registry <absolute-registry> --json
```

`--registry` and `--json` may appear in either order. Each is required once. The registry value is passed through unchanged when `Path.is_absolute` is true. A relative path, a missing value, a repeated flag, an unknown flag, a positional argument, or `--intake` is a wrapper refusal. Those refusals happen before any pin subprocess.

The registry is caller-supplied data. This command does not install a registry, discover one, or choose a default path. It does not read the caller cwd to find code or the registry.

## Pins

`app/prime-intake.json`, schema `librarian-prime-intake`, version 1. The same three identities are fixed in `app/prime_intake.py`.

| Label | Path, relative to the code root | SHA-256 |
|---|---|---|
| prime_support | `labs/prime-support-pass01/prime_support.py` | `700d60d2e49c186d49e56a9a38058e21a722b4a5dd79d461453a305e8d904f70` |
| clerk_adapter | `labs/prime-support-pass01/clerk_adapter.py` | `2f30ba751f78ec9f7d2995739bebde0e3b6509eeab35ae29a9078385ff33f8d4` |
| clerk | `labs/clerk-handoff-pass02/clerk.py` | `f697a7e443117c3d1face62d3021f7634154d76214b77fadec1a5cc3c99d394c` |

The code root is the parent of the `app` directory that contains the entry. Each path is a relative forward-slash path. An empty segment, a backslash, a drive, an absolute path, `.`, or `..` is an escape. A symlink or junction on the declaration or on any path segment is refused and is not followed. All three files are hashed before the subprocess. A mismatch, a missing file, or a declaration that is not the pinned identity refuses with `stop:` and exit 2. The accepted tool is not started.

## Subprocess

Argument array, with no shell:

```text
<current Python> -B <pinned prime_support.py> status --registry <absolute-registry> --json
```

No `--intake`. No scan, ack, ack-clerk, or show. No checker override and no alternate tool path. The child environment is the caller environment plus `PYTHONDONTWRITEBYTECODE=1`. The wrapper does not create a scratch directory, a registry, a store, an acknowledgment, bytecode, or a book file.

Stdout and stderr are copied as bytes. The child exit is preserved. Exit 0 means the tool reported no attention. Exit 1 means the tool reported attention and is not rewritten as `stop:`. Exit 2 from the tool stays the tool's own text, including `refused:` on stdout. A non-integer exit, a failed start, or a timeout is a wrapper refusal. The same-user gap between the hash read and the subprocess is not closed.

## Meaning

The JSON projection, the attention kinds, and the exit distinctions belong to the pinned tool. This wrapper does not reimplement `collect`. An attention item is a recommendation. Selecting one does not authorize a role change, a claim, an acknowledgment, a dispatch, or a model call.

An absolute registry that is missing or malformed is forwarded, so the wrapper result matches the tool. A relative registry is not forwarded.

## Not exposed

Queue, dispatch, acknowledgment, intake scan, intake show, live registry installation, role edits, and model calls are outside this command. `run` stays refused. Normal invocation with no known command stays refused.

## Gaps

This wrapper does not prove every read the lab may make when a registry names a path. A registry can name a Clerk job, and the unchanged lab can then inspect that job. This command cannot point `--intake` at a store because the flag is refused. A clean status is not release readiness, not acceptance, and not an exactly-once or dispatch guarantee. File-symlink creation may be unavailable (WinError 1314). The entry resolves its own file path before this wrapper sees the code root; links under the tool paths are still refused.
