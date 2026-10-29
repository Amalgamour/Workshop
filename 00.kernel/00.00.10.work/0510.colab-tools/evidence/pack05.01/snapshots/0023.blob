# Pack assembler, pass 01

**batch:** `00.kernel/00.00.10.work/0509.pack-assembly/05.01.md`
**state:** fixture tool. It writes a draft pack. It does not release, approve, or allocate a live return slot.

`pack_assembly.py` turns one explicit `pack-assembly-request/1` document and the blobs of one named local commit into a draft pack. Preview writes nothing. Assemble writes only when the recomputed digest matches and the target is an absent or empty directory outside the source repository and outside any directory that contains `00.kernel`.

The custody checker is `labs/pack-custody-pass01/pack_check.py`, pinned at sha256 `9bbd9d57f3b7da43234ac2e6ae4ce40a0ab6af2f53c8135ecfb2ee0c8a6e322d`, 21563 bytes. Pass that file, or a byte-identical copy, as `--checker`. A different hash is not run. The assembler does not reimplement the manifest parser. Path rules are the checker's `declared_path` and `reject_aliases`. Git reads use its `git_run` and `resolve_commit`: one local revision, `GIT_OPTIONAL_LOCKS=0`, `GIT_TERMINAL_PROMPT=0`, no fetch, no checkout, no config write. Blob bytes come from tree objects through `git cat-file --batch`. A symlink or submodule is not followed. The worktree is not a fallback.

The jobs formatter `02.jobs.010.py` was read as reference and is not called. Its `01NN` / `04NN` / `05NN` routing, open/ready/replied/ran/closed renames, `hashed:` stamps, `Authorization: signed`, and clock fields are not copied. The draft header is a new `Authorization: draft` / `state: draft` stamp. One instruction is one `#NN`.

## Request

`pack-assembly-request/1` is strict JSON. Unknown keys, duplicate keys, a BOM, and trailing data are invalid. The template field must be `pack-assembly-draft/1`. Prime supplies the title, date, author, origin, draft identity (`book`, `pppp`, `keyword`, `05.NN`), executor, reviewer, goal, scope, revision, relative paths, instructions numbered `01` through `N` in order, evidence, dependencies, and a return destination. Dependencies and the destination are `supplied` or `unresolved`. An omitted value is invalid and is not invented.

Instruction text is data. A structural heading outside a fence is rejected. A fenced block and a `>` line are kept, including example headings and `>` commands. Nothing in the request is executed. `05.NN` is the requested batch name. The tool does not scan a book for the next number.

## Digest

Preview returns a sha256 over length-prefixed parts, 8-byte big-endian length then UTF-8 bytes:

1. `pack-assembly-digest/1`
2. `pack-assembly-draft/1`
3. the exact request bytes
4. the resolved commit
5. each selected path, sha256, and decimal length, in request order
6. each planned output path, sha256, and decimal length

Planned order is `05.NN.md`, `request.snapshot`, `source-manifest.json`, then `snapshots/0001.blob` upward. The completion receipt is not an input. Assemble recomputes the digest and writes nothing when the supplied value differs.

## Pack

```text
05.NN.md
request.snapshot
source-manifest.json
snapshots/0001.blob
completion-receipt.json
```

`source-manifest.json` is `prime-pack-sources/1`. Snapshot paths are flat. `commit` and `repository` in that file are labels, not a fetch. The draft says that live return-slot allocation and Clerk readiness are not checked. Release, Claim, Return, and Review stay `PENDING`.

The checker runs on the manifest before the receipt. A finding leaves the partial draft, writes no receipt, and a later assemble does not overwrite it. `verify` recomputes the receipt identities, runs the checker, and does not rewrite the receipt. The receipt records the request, batch, source, and manifest hashes, plus the checker hash and result. It does not hash itself.

## Run

```text
python -B pack_assembly.py preview --request ABS --repo ABS --checker ABS --json
python -B pack_assembly.py assemble --request ABS --repo ABS --checker ABS --output ABS --digest HEX --json
python -B pack_assembly.py verify --pack ABS --checker ABS --json
python -B tests\test_pack_assembly.py
```

Paths on the command line are absolute. Paths inside the pack are relative. Exit 0 is a preview, a completed assemble, or an intact verify. Exit 1 is a checker finding, a partial pack, or a detected mismatch. Exit 2 is invalid input or a tool failure. Expected failures print no traceback. A missing subcommand is argparse's own stderr.

## Limits

A receipt is not acceptance. The tool does not install dependencies, call a model, publish Git, or choose a return slot. Later worktree drift does not change a pack that was built from the pinned commit. A file symlink could not be created on the machine used for the first run (`WinError 1314`); directory junctions are refused. Global Git config is not changed, and `core.longpaths` is not set. A long source path is read as a Git object and is not checked out.
