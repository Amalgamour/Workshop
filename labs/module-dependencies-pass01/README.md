# module-dependencies-pass01

A prototype reader of module-local dependency declarations (0517.dependencies 05.01; module home 0316.dependencies). Standard library only.

- **Not:** a readiness checker, dispatcher, workflow engine, installer or loader.
- **Never:** imports, executes or follows anything a declaration names.

**Contract:** `00.kernel/00.00.10.work/0517.dependencies/evidence/build05.01/CONTRACT.md`. **Guide:** `evidence/build05.01/PRIME-USE.md`.

```text
python -B labs/module-dependencies-pass01/depdecl.py validate --set ABS
python -B labs/module-dependencies-pass01/depdecl.py requires --set ABS --module REPO:PATH [--transitive] [--depth N] [--condition ID=STATE ...]
python -B labs/module-dependencies-pass01/depdecl.py explain  --set ABS --module REPO:PATH --to REPO:PATH
python -B labs/module-dependencies-pass01/depdecl.py impacted --set ABS --module REPO:PATH [--implementation SHA]
python -B labs/module-dependencies-pass01/depdecl.py identity --set ABS
python -B labs/module-dependencies-pass01/depdecl.py index    --set ABS --out ABS
python -B labs/module-dependencies-pass01/depdecl.py delta    --old ABS --new ABS --change ABS
python -B -X dev labs/module-dependencies-pass01/tests/test_depdecl.py -v
python -B labs/module-dependencies-pass01/demo.py --snapshots ABS_PACK_SNAPSHOTS --out ABS_NEW_DIR
```

**Layout:**
- `depdecl.py`: the prototype.
- `examples/prime-cycle-chain/`: four PROTOTYPE declarations (prime_cycle, batch_observe, prime_support, clerk_adapter at f0ccb90), and their pinned set. The records for prime_review, review_packet, return_inspect, return_capture and the Clerk tool are deliberately absent, so they answer `record-missing`.
- `demo.py`: the bounded demonstration, with labelled SYNTHETIC negative versions.
- `tests/`.

**Reading an answer:**
- **`status`:**
  - `complete-for-declared-coverage` only when nothing is missing, unknown or conflicting;
  - `incomplete` otherwise.
- **`root.state`:**
  - `declared`;
  - `declared-dependency-free` (an explicit `no_requirements`);
  - `undeclared` (no record; `requirements` is null, not empty);
  - `ambiguous-version`.
- **Each requirement** has a `resolution` (resolved, record-missing, pin-differs, ambiguous-version, identity-conflict, selected, single-unpinned, not-a-module) and its own findings.
- **`impacted`** lists candidates for Prime review. It changes nothing.

Declarations are model-authored and cover only the edges found for their named entry points. A digest proves bytes, not compatibility. There is no OS sandbox or race safety.
