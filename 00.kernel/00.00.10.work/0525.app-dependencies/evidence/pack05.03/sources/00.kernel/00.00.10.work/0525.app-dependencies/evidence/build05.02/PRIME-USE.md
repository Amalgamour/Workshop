# PRIME-USE — 0525.app-dependencies/05.02

Reader: labs/module-dependencies-pass02/depdecl.py, sha256 a517b0ec3906589e16e2df9bcfb6b3e21a5dd0bd3ef1099d59bf95c0f15ff4e7, 53693 bytes. Python 3.14.0. cwd D:\Git\lib-build. The predecessor labs/module-dependencies-pass01/depdecl.py was not edited.

Corrected set: labs/app-dependencies-pass02/set.json, set_id review-loop-entry-2, sha256 444dba1589c0d6a0204e7a3d6be334b3135d524e4b376e7e92eb8fb434e6f706, 7054 bytes. Schema module-declaration-set/2. The /1 set labs/app-dependencies-pass01/set.json stays in place.

Scope: app/librarian.py command review-loop, the v2 door, app/review-loop-v2.json, and the reviewed modules that command reaches, including return_capture.py. Not every app namespace. Not run. Not reproduce.

## Commands

```
python -B labs/module-dependencies-pass02/depdecl.py validate --set D:\Git\lib-build\labs\app-dependencies-pass02\set.json
python -B labs/module-dependencies-pass02/depdecl.py requires --set D:\Git\lib-build\labs\app-dependencies-pass02\set.json --module lib-build:app/librarian.py --transitive
python -B labs/module-dependencies-pass02/depdecl.py requires --set D:\Git\lib-build\labs\app-dependencies-pass02\set.json --module lib-build:app/librarian.py --transitive --depth 2
python -B labs/module-dependencies-pass02/depdecl.py identity --set D:\Git\lib-build\labs\app-dependencies-pass02\set.json
python -B labs/module-dependencies-pass02/depdecl.py explain --set D:\Git\lib-build\labs\app-dependencies-pass02\set.json --module lib-build:app/librarian.py --to lib-build:labs/return-capture-pass01/return_capture.py
python -B labs/module-dependencies-pass02/depdecl.py impacted --set D:\Git\lib-build\labs\app-dependencies-pass02\set.json --module lib-build:labs/return-capture-pass01/return_capture.py --depth 1
python -B labs/module-dependencies-pass02/depdecl.py impacted --set D:\Git\lib-build\labs\app-dependencies-pass02\set.json --module lib-build:labs/return-capture-pass01/return_capture.py --depth 8
python -B labs/module-dependencies-pass02/depdecl.py impacted --set D:\Git\lib-build\labs\app-dependencies-pass02\set.json --module lib-build:labs/return-capture-pass01/return_capture.py --implementation 8f3da5c651f6924fca6dedb0b95da7d181eb58884dc030dd9cbc3d8b6a5b15ac --depth 8
python -B labs/module-dependencies-pass02/depdecl.py requires --set D:\Git\lib-build\00.kernel\00.00.10.work\0525.app-dependencies\evidence\build05.02\negative-missing\set.json --module lib-build:app/librarian.py --transitive
```

Saved exits: 0, 0, 1, 0, 0, 1, 0, 0, 1. Stderr empty. Raw stdout is in evidence/build05.02/commands.

## What a change forces

A change to return_capture.py changes its implementation sha256 and byte length. Repin the pair edges that enforce both, and repin the digest-only edge from return_inspect.py with the new sha and bytes null. Then rerun requires, identity, and impacted --depth 8. A digest mismatch stays pin-differs and digest-differs. Do not fill pin.bytes unless the caller compares length.

A change to a pair-pinned tool repins that pair. A change to librarian.py or to review-loop-v2.json changes an unpinned edge: the record's implementation identity changes, and the pin stays null. Stored hashes in the JSON are not executable checks.

The three git-blob records are supplied references. This reader will not confirm them. If the working tree stops matching HEAD, the next record uses observed-file rather than a false git-blob.

## Open limits

Environment rows are unverified. Depth 1 truncates the three direct consumers. Depth 2 leaves nine door edges unwalked. Explain keeps the first path, so the three paths go through the door. The loop's subprocess of return_inspect.py is a shared edge in requires-full.json. Extra-segment addresses and the nonloaded contract path stay outside the grammar. Matching line 0125.app-dependencies stays pending. No receipt. 0184 was not allocated. Exit 0 is not approval.
