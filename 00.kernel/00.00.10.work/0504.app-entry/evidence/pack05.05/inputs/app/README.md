# app

Development entry for the Workshop desk. No screen. Nothing here is seated or activated.

The commands, from any current directory:

```text
python <workspace>/app/librarian.py where --root <workspace>
python <workspace>/app/librarian.py validate --root <workspace>
python <workspace>/app/librarian.py test-run --root <fixture> --candidate <fixture-relative-path> --sha256 <payload-hash> [--container <external-container>]
```

`where` and `validate` read `app/development-workspace.json` under `--root`, then the assignment record that file names. They report the desk, work book, workflow space, current work, assignment state, runtime book, runtime space, N3NN band, and the pinned runner path and SHA-256. They do not import the runner. `validate` adds `validate: pass` when the references resolve.

`test-run` reads the configuration and the runner from the workspace that contains this entry. It reads the assignment, the books, and `fixture.json` under `--root`. The selected runner is `00.kernel/00.00.01.law/0302.run/02.run.003.py`, matched by the path and SHA-256 in `development-workspace.json` before it is imported. `02.run.002.py` stays in place and is not selected by version number. 003 is required because the page fixtures directory sits inside the work book, and 002 refuses every payload there before the inventory can run. The payload must sit in the fixture's declared compute page, match the hash, and carry the card and stamp checks. The operation writes one JSON inventory.

The writable container is chosen before `fixture.json` is read. `allowed_root` is not a fixture field and cannot grant a directory. Inside this workspace the only containers are `app/scratch` and `00.kernel/00.00.10.work/0504.app-entry/fixtures`, named by `fixture_containers` in the configuration. A fixture root anywhere else in the workspace is refused. A fixture root outside the workspace requires `--container` naming that external directory. The named directory must contain the fixture root, must not be a filesystem root, and must not overlap this workspace. Paths are resolved, including directory junctions, before those checks. A resolved output or payload that leaves the container, or that lands in the workspace outside the two containers, is refused before the payload runs. Before the payload is imported, the output name and its sibling temporary name (the output file's name plus `.tmp`) go through those same containment checks. If either name is already present, including a hard link, a symlink, a junction, or a dangling link, the run stops and does not remove or replace that name.

`run` refuses. `--test` does not authorize the live workspace, the live work book, or a source directory. An accepted or otherwise unreleased assignment can be inspected and cannot be executed. `00.kernel/00.live.md` is never an input.

Context checks and path checks are not an operating-system sandbox. Same-user Python is not confined by them. The caller supplies the payload hash and the fixture records that same hash. The entry checks the hash, the stamp, the card, and the path. That is integrity and context. It is not an approval allowlist of one payload, and it does not make an arbitrary program safe. A name check made before the payload runs is not a claim of resistance to a later change.

Configuration, refusal, and the later owner of the space declaration are on `00.kernel/00.00.10.work/0014.design/01.002.md`. Tests are `app/tests/test_entry.py`. Scratch under `app/scratch/` is gitignored.

The next proposed work, not released: integrate one existing compute module against fixtures and review activation, then connect the independently reviewed worker bridge.
