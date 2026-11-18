# PRIME-USE — review-loop entry declarations

For Codex Prime. Nothing here is accepted, seated, or a gate. The reader is the existing prototype. It was not modified.

Reader: `labs/module-dependencies-pass01/depdecl.py`
sha256 `be32e7be8b481d7439f9f884f3cc709841964c807c8274f68bed7a3ce12567f0`, 48898 bytes.

Set: `D:\Git\lib-build\labs\app-dependencies-pass01\set.json`
set id `review-loop-entry-1`
sha256 `0a2ae9b028e974a20c15c3c5904ff654f7fa91f01a0380fbd6b5e9dfcf6e6af6`, 7039 bytes.

Scope: `app/librarian.py` command `review-loop` only. The v2 door, `app/review-loop-v2.json`, the reviewed loop, the pass03 cycle, the pass02 constructor, both prime_review files, return_lines, return_placement, return_inspect, and return_capture. Not every app namespace. Not `run`. Not `reproduce`. Not the old facade.

`complete-for-declared-coverage` means this declared graph answered without blocking findings. Environment rows stay unverified inside that status. It is not target readiness, runtime closure, or approval.

## Commands

Run from `D:\Git\lib-build`.

```text
set S = D:\Git\lib-build\labs\app-dependencies-pass01\set.json
python -B labs/module-dependencies-pass01/depdecl.py validate --set S
python -B labs/module-dependencies-pass01/depdecl.py requires --set S --module lib-build:app/librarian.py --transitive
python -B labs/module-dependencies-pass01/depdecl.py identity --set S
python -B labs/module-dependencies-pass01/depdecl.py explain --set S --module lib-build:app/librarian.py --to lib-build:labs/return-capture-pass01/return_capture.py
python -B labs/module-dependencies-pass01/depdecl.py impacted --set S --module lib-build:labs/return-capture-pass01/return_capture.py --depth 8
```

This pass ran those, plus the bounds and the negative copy below. Raw stdout, stderr, and exit files are in `evidence/build05.01/commands/`. Stderr was empty. Exit 0 on validate, the full requires, identity, explain, and impacted depth 8.

## What a change forces

Repin means edit the enforcing source and every declaration whose `requirement.pin` names the old pair, then retest the app command that reaches that edge. A green `identity` result only says the fixture copy matches the declaration. It does not retarget the app.

- `return_capture.py` changes: `return_lines.py` and `return_placement.py` enforce sha256 and length (`load_module`, `_reader`). `return_inspect.py` enforces the digest only and will still load a same-digest file of any length it can read. The door's `TOOLS` map does not name this sibling. Retest describe-legacy and a cycle read that verifies a descriptor. Update the three reader declarations. `impacted` depth 8 lists the door, the JSON declaration, the loop, the cycle, and librarian as well as the three readers. Depth 1 does not.
- A file named in `review_loop_tools_v2.py` `TOOLS` changes: the door hash-checks all eight before it launches `review_loop.py`, and it compares the parsed JSON to those same pairs. The loop's `pin_set` checks seven of them again. Change the door, the JSON, and the loop constants together. Librarian does not hash the door. A door-only edit is still a change to the entry. Retest the six app commands on a disposable fixture. `describe-legacy` may read a book and must write nothing.
- `app/librarian.py` loads the door with `load_module` and no hash (lines 98-101). The declaration leaves that edge unpinned on purpose. Delivery having selected the current door bytes is not a pin.
- `review-loop-v2.json` stores hashes and does not open the files. Treat a JSON-only edit as data until the door's field compare is updated. The door refuses when the parsed fields differ from `TOOLS`.
- prime_review pass01 is hash-checked by the door, the loop, and the cycle. These six commands do not launch it. A byte change still refuses the entry at `pin_set` / `pin_tools`.
- Environment rows (`python`, `checkout-root`, `fixture-root`, `caller-book`) were not probed. Python 3.14.0 on this machine is an observation. The sources bind `D:\Git\lib-build`. Another machine, another interpreter, or a linked path is unverified. Do not infer portability from a matching digest.

## Bounds

```text
python -B labs/module-dependencies-pass01/depdecl.py impacted --set S --module lib-build:labs/return-capture-pass01/return_capture.py --depth 1
python -B labs/module-dependencies-pass01/depdecl.py requires --set S --module lib-build:app/librarian.py --transitive --depth 2
```

Depth 1 exits 1, status `truncated`. The three direct consumers stay unexpanded: lines 5, placement 7, inspect 6. Depth 2 exits 1, status `incomplete`, nine `depth-limit` findings on the door's targets. Rerun with a larger `--depth`. The set cap is 16. Depth 8 of the capture impact exited 0 and reached librarian.

## Negative copy

`evidence/build05.01/negative-missing/set.json` is a disposable copy with the `return-capture-pass01` record and its select entry removed. Fixtures are empty. Sources were not edited.

```text
python -B labs/module-dependencies-pass01/depdecl.py requires --set D:\Git\lib-build\00.kernel\00.00.10.work\0525.app-dependencies\evidence\build05.01\negative-missing\set.json --module lib-build:app/librarian.py --transitive
```

Exit 1. Status `incomplete`. Finding `record-missing` 3, from return_inspect, return_lines, and return_placement, each targeting `labs/return-capture-pass01/return_capture.py`. The selected set was not changed to hide this, and the reader was not changed to invent the record.

## Open limits

See `coverage.md` for the digest-only pin, the git-blob field on working-tree bytes, the unlinked `05.01.002` page, the contract string kept as provenance, and the route command's inapplicable custody load. Matching line `0125.app-dependencies` stays pending. This pass did not allocate `0184` and did not write a receipt.
