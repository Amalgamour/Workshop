# app

Development entry for the Workshop desk. No screen. Nothing here is seated or activated.

The commands, from any current directory:

```text
python <workspace>/app/librarian.py where --root <workspace>
python <workspace>/app/librarian.py validate --root <workspace>
python <workspace>/app/librarian.py test-run --root <fixture> --candidate <fixture-relative-path> --sha256 <payload-hash>
```

`where` and `validate` read `app/development-workspace.json` under `--root`, then the assignment record that file names. They report the desk, work book, workflow space, current work, assignment state, runtime book, runtime space, N3NN band, and the pinned runner path and SHA-256. They do not import the runner. `validate` adds `validate: pass` when the references resolve.

`test-run` reads the configuration and the runner from the workspace that contains this entry. It reads the assignment, the books, and `fixture.json` under `--root`. The runner is `00.kernel/00.00.01.law/0302.run/02.run.002.py`, matched by SHA-256 before it is imported. The payload must sit in the fixture's declared compute page, match the hash, and carry the card and stamp checks. The operation writes one JSON inventory.

`run` refuses. `--test` does not authorize the live workspace or the live work book. An accepted or otherwise unreleased assignment can be inspected and cannot be executed. `00.kernel/00.live.md` is never an input.

Context checks and path checks are not an operating-system sandbox. Same-user Python is not confined by them. This slice runs the one reviewed fixture payload; it does not claim those checks make an arbitrary program safe.

Configuration, refusal, and the later owner of the space declaration are on `00.kernel/00.00.10.work/0014.design/01.002.md`. Tests are `app/tests/test_entry.py`. Scratch under `app/scratch/` is gitignored.

The next proposed work, not released: integrate one existing compute module against fixtures and review activation, then connect the independently reviewed worker bridge.
