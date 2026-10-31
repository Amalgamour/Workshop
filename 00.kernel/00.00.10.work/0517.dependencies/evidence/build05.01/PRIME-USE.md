# PRIME-USE — module dependency declarations prototype (0517 05.01)

For Codex Prime.

**Reading order:**
1. This page.
2. `CONTRACT.md`: §2 the record, §5 resolution, §6 queries and findings, §8 the completion seam.
3. One example declaration: `labs/module-dependencies-pass01/examples/prime-cycle-chain/declarations/batch-observe.v1.json`.
4. `sample-dependencies.json`: one real observed answer.

Nothing here is accepted, seated or a gate.

## The shortest lookups

```text
set S = D:/Git/lib-build/labs/module-dependencies-pass01/examples/prime-cycle-chain/set.json
python -B labs/module-dependencies-pass01/depdecl.py requires --set S --module lib-build:labs/prime-cycle-pass01/prime_cycle.py
python -B labs/module-dependencies-pass01/depdecl.py requires --set S --module lib-build:labs/prime-cycle-pass01/prime_cycle.py --transitive --condition members-book=applicable
python -B labs/module-dependencies-pass01/depdecl.py explain  --set S --module lib-build:labs/prime-cycle-pass01/prime_cycle.py --to lib-build:labs/prime-support-pass01/clerk_adapter.py
python -B labs/module-dependencies-pass01/depdecl.py impacted --set S --module lib-build:labs/prime-support-pass01/clerk_adapter.py --implementation <new sha256>
```

- **Direct** lists the requirements prime_cycle declares.
- **Transitive** walks the declared edges with bounds.
- **`--condition`** states applicability for this query only. It is recorded as `stated_by: caller`.
- **`explain`** shows both declared paths into clerk_adapter: the shared, or diamond, dependency.
- **`impacted`** lists who declared they need clerk_adapter: batch_observe (hash-check), prime_support (import), and then, transitively, prime_cycle. For each it gives whether its pin equals the bytes you name, and its provenance links, or the stated unknown.

## Interpreting an incomplete answer

Each finding asks for a different decision.

| finding | it means | Prime decides |
|---|---|---|
| `record-missing` | The target has no declaration in this set: unknown, not "no dependencies". | Whether a declaration is needed before reuse. |
| root `undeclared` (requirements null) | There is no record for the module asked about. | The same; never read as dependency-free. |
| root `declared-dependency-free` | The author declared none, explicitly, for the covered entry points. | Whether the coverage is enough. |
| `pin-differs` | The consumer pins bytes the set's declarations do not have. | Rebuild, re-pin or retest; nothing changes automatically. |
| `ambiguous-version` | Several versions, and no pin or `select`. | Which version: write a `select`, never "highest". |
| `identity-conflict` / `duplicate` | Records disagree about one id, or one set of bytes. | Which record is right. |
| `cycle` / `shared` / `depth-limit` | Graph shape. A cycle is not expanded again. | Whether the cycle is real. |
| `condition-unknown` / `condition-inapplicable` | The condition, as stated by the record or by you. | Applicability for the method at hand. |
| `environment-unverified` / `environment-unavailable` / `external-unverified` | Declared; nothing on this machine was probed. | Target-environment verification, later. |
| `provenance-unknown` / `provenance-unpinned` | No workflow link, or a link without bytes, such as a docstring citation. | Whether to find and pin the construction pages. |
| `address-unresolved` | An evidence or task address is listed and not opened. | Whether it is the right evidence. |

The real chain answers `incomplete` today, and that is correct:
- four tools have no records;
- batch_observe's construction provenance is unknown;
- prime_support's and clerk_adapter's links are docstring citations only.

## Adding or changing a module: the proposed completion seam

1. The builder writes the new declaration version, with `supersedes` naming the old one. The old file is kept.
2. The builder returns a `module-change/1` record, CONTRACT §8: introduced, changed and removed relationships with reasons; `authorized_by` naming the page/pass `#NN`; the implementation and evidence identities.
3. Compute runs `delta --old --new --change`. It checks identities, supersession, and the declared delta against the computed one.
4. Prime reviews the meaning: are the relationships true and sufficient, are the conditions right, is it ready for reuse.
5. Prime writes `select` entries for the accepted versions. A later delivery checker reads that selected set by hash. It adds no authority and no second copy of the schema.

The demo's worked example (a SYNTHETIC batch_observe v2 re-pinned to a SYNTHETIC changed adapter) shows a consistent record (exit 0) and one that omits the changed pin (exit 1, `change-mismatch relationships.changed`).

## Limits

- Declarations are model-authored, from reading source. They are not a complete discovery of runtime closure.
- This prototype claims no complete coverage (`complete_claim` is always false).
- String content is never interpreted.
- There is no OS sandbox or race safety.
