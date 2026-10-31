# PRIME-USE — dependency prototype after the 05.02 repair

For Codex Prime. This replaces `build05.01/PRIME-USE.md`; the 05.01 guide is kept.

**Reading order:**
1. This page.
2. `build05.02/CONTRACT.md`, the delta: pin meaning, identity pairs, the reverse and forward bounds, creation, status meaning.
3. `build05.01/CONTRACT.md` §2, §5, §6 and §8.
4. `sample-dependencies.json`.

Nothing here is accepted, seated, or a gate.

## The shortest lookups (unchanged commands)

```text
set S = D:/Git/lib-build/labs/module-dependencies-pass01/examples/prime-cycle-chain/set.json
python -B labs/module-dependencies-pass01/depdecl.py requires --set S --module lib-build:labs/prime-cycle-pass01/prime_cycle.py --transitive --condition members-book=applicable
python -B labs/module-dependencies-pass01/depdecl.py impacted --set S --module lib-build:labs/prime-support-pass01/clerk_adapter.py --depth 4
```

## What changed in the answers

- **Reverse impact is bounded honestly.**
  - If `--depth` stops the walk while a consumer still has consumers, the answer is `status: truncated`, with `depth-limit` and `unexpanded: [{module, direct_declared_consumers, path}]`, and exit 1. Rerun with a larger `--depth`.
  - A walk that ends inside the bound is `candidates-for-review`, exit 0 if there are no other findings.
  - Revisits are marked `shared` (listed, not a finding) or `cycle` (a finding).
- **Pins are pairs.**
  - A pin with the right digest and the wrong length is `identity-pair-mismatch`: not resolved and not traversed, with both lengths shown.
  - In `impacted`, `pin_vs_declarations: pair-mismatch` is a finding.
  - Only `identity` measures a real file. It reports `declaration-length-wrong` when the measured length contradicts a declaration.
- **Forward depth:** `depth-limit` appears only when a module with unwalked requirements was cut. A dependency-free leaf at the bound ends the walk naturally.
- **Pins mean subject enforcement.** prime-support v2 records its import of clerk_adapter as `pin: null` (prime_support does not hash-check it), with the observed bytes noted in the reason. So `impacted clerk_adapter` now shows prime_support as `unpinned`, and batch_observe (which hash-checks it) as the enforcing consumer. v1 stays on disk as history.
- **`complete-for-declared-coverage`** means the declared graph was answered without blocking findings. `environment-unverified` can still be listed in it. It is not environment readiness, closure or acceptance.

## Completing a module build

**A new module:**
```text
python -B labs/module-dependencies-pass01/depdecl.py delta --create --new NEW.json --change CHANGE.json
```
- `change.old` null; the new declaration has version 1 and `supersedes` null;
- every initial requirement is listed under `introduced`, with a reason; `changed` and `removed` are empty;
- exact new declaration and implementation identities; `authorized_by` a full page/pass address plus `#NN`;
- a dependency-free module (`no_requirements: true`) uses `introduced: []`.

**These are refused (exit 2):** `--old` together with `--create`; omitting `--old` without `--create`; an empty or unreadable path; a revision whose `change.old` is null.

**A revision** is unchanged: `delta --old OLD --new NEW --change CHANGE`.

**Either way,** Prime then reviews whether the relationships are true and sufficient, and selects accepted versions.

## Unchanged

- Missing records stay `record-missing`.
- The real prime-cycle chain still answers `incomplete`: four tools have no records, and provenance gaps remain. No declarations were added to clear it.
- Module-local records with a derived index remain the prototype layout. No migration, acceptance selection or delivery adapter was built here.
