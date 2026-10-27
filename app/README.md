# app

Development entry for the Workshop desk. No screen. Nothing here is seated or activated.

The commands, from any current directory:

```text
python <workspace>/app/librarian.py where --root <workspace>
python <workspace>/app/librarian.py validate --root <workspace>
python <workspace>/app/librarian.py test-run --root <fixture> --candidate <fixture-relative-path> --sha256 <payload-hash> [--container <external-container>]
python <workspace>/app/librarian.py bridge-test --root <fixture> --job bridge/job.json [--container <external-container>]
python <workspace>/app/librarian.py bridge-status --root <fixture> --delivery bridge-0001 [--container <external-container>]
python <workspace>/app/librarian.py bridge-recover --root <fixture> --delivery bridge-0001 --recovery-request bridge/recover.json [--container <external-container>]
```

`where` and `validate` read `app/development-workspace.json` under `--root`, then the assignment record that file names. They report the desk, work book, workflow space, current work, assignment state, runtime book, runtime space, N3NN band, and the pinned runner path and SHA-256. They do not import the runner. `validate` adds `validate: pass` when the references resolve.

`test-run` reads the configuration and the runner from the workspace that contains this entry. It reads the assignment, the books, and `fixture.json` under `--root`. The selected runner is `00.kernel/00.00.01.law/0302.run/02.run.003.py`, matched by the path and SHA-256 in `development-workspace.json` before it is imported. `02.run.002.py` stays in place and is not selected by version number. 003 is required because the page fixtures directory sits inside the work book, and 002 refuses every payload there before the inventory can run. The payload must sit in the fixture's declared compute page, match the hash, and carry the card and stamp checks. The operation writes one JSON inventory.

The writable container is chosen before `fixture.json` is read. `allowed_root` is not a fixture field and cannot grant a directory. Inside this workspace the only containers are `app/scratch` and `00.kernel/00.00.10.work/0504.app-entry/fixtures`, named by `fixture_containers` in the configuration. A fixture root anywhere else in the workspace is refused. A fixture root outside the workspace requires `--container` naming that external directory. The named directory must contain the fixture root, must not be a filesystem root, and must not overlap this workspace. Paths are resolved, including directory junctions, before those checks. A resolved output or payload that leaves the container, or that lands in the workspace outside the two containers, is refused before the payload runs. Before the payload is imported, the output name and its sibling temporary name (the output file's name plus `.tmp`) go through those same containment checks. If either name is already present, including a hard link, a symlink, a junction, or a dangling link, the run stops and does not remove or replace that name.

`run` refuses. `--test` does not authorize the live workspace, the live work book, or a source directory. An accepted or otherwise unreleased assignment can be inspected and cannot be executed. `00.kernel/00.live.md` is never an input.

Context checks and path checks are not an operating-system sandbox. Same-user Python is not confined by them. The caller supplies the payload hash and the fixture records that same hash. The entry checks the hash, the stamp, the card, and the path. That is integrity and context. It is not an approval allowlist of one payload, and it does not make an arbitrary program safe. A name check made before the payload runs is not a claim of resistance to a later change.

Configuration, refusal, and the later owner of the space declaration are on `00.kernel/00.00.10.work/0014.design/01.002.md`. Scratch under `app/scratch/` is gitignored.

`bridge-test` submits one exact-key job to the pinned local process adapter in `labs/worker-bridge-pass01`. The only allowed kind is `protocol test worker`. A new delivery copies declared inputs from `bridge/declared/` into a fresh `bridge/delivery/<id>/input` and launches only into `bridge/delivery/<id>/output`. A directory, file, hard link, junction, or temporary name that is already present at those paths is refused and is not removed. The adapter store stays `bridge/store/`. One provenance file, `bridge/provenance/<id>.json`, associates the stored request with the fixture, the work ref, and the declared job. It is not a second job ledger.

An identical `bridge-test` reuses the stored request bytes. It does not rebuild the envelope from a later assignment hash. `bridge-status` is read-only and remains available after the fixture record is returned or accepted. `bridge-recover` requires a local recovery request naming the delivery, the original request hash, a reason, and a requester. It can rebuild a receipt from a recorded attempt. It does not launch a worker. Collection, `review: not performed`, and `acceptance: not performed` stay separate. Collection is not approval.

Exit 0 is a collected `done`. Exit 2 is a refusal on this call (`stop:` on stderr, empty stdout). A reused delivery id is exit 2 and says this call did not launch; a prior launch record, when one exists, is still reported. Exit 3 is delivered but uncollected, or a collected claim of failure. Exit 4 is uncertain or not collected, including unknown, accepted-not-launched, launch-failed, timeout, output-limit, incomplete output, and malformed output. Unknown is never collected. Nothing relaunches after uncertainty.

The bridge hash-checks the eight pinned lab files before it imports them under the private name `worker_bridge_pinned`. The same-user gap between that read and the import is not closed. Path checks are not a sandbox. The adapter kills only the direct child. A descendant that still holds a pipe is named in `cleanup.retained` and is not tree-killed. There is no exactly-once promise. No model is called. `run` is still refused. Nothing here is seated or activated.

Tests are `app/tests/test_entry.py` and `app/tests/test_worker_bridge.py`.
