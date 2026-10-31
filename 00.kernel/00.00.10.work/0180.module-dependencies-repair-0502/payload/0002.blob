# CONTRACT — dependency prototype, 05.02 repair (delta over build05.01/CONTRACT.md)

Written before the code change. Everything in `build05.01/CONTRACT.md` stays in force except where this page replaces it. These schemas are unchanged:
- `module-declaration/1`;
- `module-declaration-set/1`;
- `module-change/1`.

The result schema stays `module-dependency-result/1`, with the added fields listed below.

## 1. Pin meaning (clarifies §2)

`requirement.pin` is the `{sha256, bytes}` identity that the **requiring module itself enforces** before use (a hash check, or a pinned launch).
- A dependency the module uses without checking it (an import by path, a reference) has `pin: null` and `pin_required: false`. Its `reason` may name the bytes observed at the declared cut, as an observation.
- Bytes selected for a reproducible delivery are a later delivery selection. They are never written as a subject pin.

## 2. Identity pairs (replaces §5 step 2)

For a module target with a pin:
1. Take the declarations whose `implementation.sha256` equals `pin.sha256`.
2. **One, with `implementation.bytes == pin.bytes`:** `resolved`.
3. **One or more, with no equal length:** resolution `identity-pair-mismatch`. The finding gives `pinned: {sha256, bytes}` and `declared: [{declaration, bytes}]`. Not traversed.
4. **None:** `pin-differs`, as before. More than one equal pair: `identity-conflict`, as before.

**These compare declarations with each other. No module file is measured.** Only `identity` measures bytes:
- for each fixture, the measured `{sha256, bytes}`;
- `identical` when a declaration has the same pair;
- `declaration-length-wrong` when a declaration has the digest but another length, because measured bytes contradict the declared length;
- `changed` when no declaration has the digest.

## 3. Reverse impact bound (replaces the §6 `impacted` row)

`impacted --module M [--implementation SHA] [--depth N]` walks derived consumers breadth-first, up to `N` levels (the default and cap is `max_depth`).

**Each row gains:**
- `pin_vs_declarations`: `matches-declared`, `pair-mismatch`, `undeclared-bytes` or `unpinned`, which compares the consumer pin with the target's declarations as a pair;
- `revisit`: null, `shared` or `cycle`.

A revisited consumer is listed and not expanded again.

**`unexpanded`** lists the consumers at the last level that have declared consumers of their own. Each entry gives the module and the count of its direct declared consumers. When it is non-empty:
- the finding is `depth-limit`, with `{max_depth, unexpanded}`;
- `status` is `truncated`.

A walk that ends naturally inside the bound has no `depth-limit`, and `status` is `candidates-for-review`.

**Exit:** 0 only when there are no findings; 1 otherwise.

`--implementation` stays digest-only. The result says `implementation_compared: "sha256 only"`.

## 4. Forward bound (corrects §6 traversal)

`depth-limit` in `requires` is reported only when the next module would be expanded and has at least one requirement. A dependency-free module at the bound ends the walk naturally.

## 5. Creation (adds to §8)

**Revision, unchanged:** `delta --old OLD --new NEW --change CHANGE`. Here `change.old` null is refused: "a revision needs change.old".

**Creation, new:** `delta --create --new NEW --change CHANGE`.
- `--old` together with `--create` is refused.
- `--old` without `--create` is required; omitting it is refused with "for a new module use --create".
- No path, empty string or null-like value stands in for a predecessor.

**Creation checks (each failure is a `change-mismatch` finding; malformed input is refused):**
- `change.old` is null;
- `new.supersedes` is null, and `new.version` is 1;
- `change.module` equals the new module;
- `change.new` equals the new file's id, version and sha;
- `change.implementation` equals the new `implementation` {sha256, bytes};
- `relationships.introduced` ids equal every new requirement id, each with a non-empty reason;
- `changed` and `removed` are empty;
- `authorized_by` is a full address with `#NN`.

A `no_requirements: true` declaration with `introduced: []` is valid.

**Output:** `mode: "create"` or `"revise"`, plus the computed relationships, as before.

## 6. Status meaning (clarifies §6)

`complete-for-declared-coverage` means the declared graph was answered without blocking findings. Non-blocking findings may remain, and stay listed:
- `shared`;
- `environment-unverified`;
- `condition-inapplicable`.

It is not target-environment readiness, runtime closure or acceptance.

## 7. Amendment written during implementation (2026-10-31, before any capture)

These were decided while coding §3 and §5, and are recorded here rather than silently.
- **In `impacted`, two revisits count as findings** (exit 1): a `cycle` revisit, and a `pin_vs_declarations: pair-mismatch` row. A `shared` revisit is not a finding.
- **In revision mode, `delta` validates the `--old` path before checking `change.old`,** so an empty or unreadable predecessor path is refused for what it is.
