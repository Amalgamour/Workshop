# CONTRACT — review-loop entry declarations (0525.app-dependencies 05.01)

Written before the declaration files. This pass adds module-local records for one app command. It does not change module-declaration/1, module-declaration-set/1, module-change/1, or module-dependency-result/1. The reader remains labs/module-dependencies-pass01/depdecl.py. The 0517 build05.01 contract and the build05.02 delta stay in force. This page seats nothing and accepts nothing.

## 1. Scope

The selected set describes `app/librarian.py` command `review-loop` and the files that command reaches:

- the v2 door `app/review_loop_tools_v2.py`
- the declaration file `app/review-loop-v2.json`
- the reviewed loop, pass03 cycle, pass02 constructor, both prime_review modules, return_lines, return_placement, return_inspect, and the inspector's sibling return_capture.py

It does not describe every app namespace, the old review-loop facade, `run`, or `reproduce`. Those last two are refused or unwired at the app door. Coverage `complete_claim` stays false. A digest is byte identity, not compatibility, readiness, or approval.

Home on each record is 0316.dependencies `01.001.md`, the dependency module home. This pack is a construction slice. It is not another dependency runtime.

## 2. How an edge is recorded

Schemas and commands are the existing prototype. This pass uses `validate`, `requires --transitive`, `identity`, `explain`, and `impacted`.

- `requirement.pin` is the `{sha256, bytes}` pair the requiring file enforces before use.
- A load, import, or stored path that the file does not check is `pin: null` and `pin_required: false`. Observed bytes may be named in the reason. They are not a pin.
- `return_inspect.py` compares `HELPER_SHA256` and does not compare length. The schema's pin object cannot say "digest only", so that edge is unpinned. The observed digest and length stay in the reason. coverage.md records the gap.
- A hash check and a later subprocess of the same file are two requirements when both happen. One mechanism field cannot carry both.
- `review-loop-v2.json` stores paths and hashes. It does not open those files. Those edges are `runtime-resource` / `document` / unpinned. The door's `hash-check` edges are the enforcement.
- Environment rows use `availability: unverified`. Nothing in this pass probes the machine. `environment-unverified` remains non-blocking and is not readiness.
- Caller-chosen books and fixture roots are environment rows. They are not module pins.
- The loop names `0522.review-construction/evidence/build05.04/CONTRACT.md` in source. That page is a provenance link. It is not stored as an address requirement, because an address target is listed and never opened (`address-unresolved`). coverage.md states that choice and the proposed extension.
- Provenance links are real work pages read for this pass, with the live file's sha256. A missing construction page stays in `provenance.unknown`. No page is invented. A link is not acceptance.
- `basis.kind` must be `git-blob`. For files whose working-tree blob is not in HEAD and was not found by `git log --find-object`, `basis.commit` is the HEAD observed on 2026-11-01, and `provenance.unknown` says the measured bytes are not that blob. The implementation sha256 and byte length are the measured file.

## 3. What the answers mean here

`complete-for-declared-coverage` means the declared graph was answered without blocking findings. It is not closure of the app and not acceptance.

`impacted` lists declared consumers for Prime to review. It changes nothing. A shared reader is shown by walking `return_capture.py` far enough to list every declared consumer, and again with a depth bound that leaves consumers unexpanded. Truncation stays visible.

`identity` hashes fixture copies under this lab. It does not hash the live sources a second time and does not execute them. The live sources stay the bytes measured for the implementation rows.

One disposable copy of the set drops the return_capture record. That copy stays incomplete. The selected set is not edited to hide the gap, and depdecl.py is not edited to fill it.

## 4. Limits

No app edit, no reader edit, no migration, no live book write, no allocator, no receipt, no 0184. Matching line 0125.app-dependencies stays pending. Exit 0 from depdecl is an answer about declarations. It is not Prime review and not production classification.
