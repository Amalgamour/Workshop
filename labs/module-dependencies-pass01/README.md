# module-dependencies-pass01

A prototype reader of module-local dependency declarations (0517.dependencies 05.01; module home 0316.dependencies). Standard library only.

- **Not:** a readiness checker, dispatcher, workflow engine, installer or loader.
- **Never:** imports, executes or follows anything a declaration names.

**Contract:** `00.kernel/00.00.10.work/0517.dependencies/evidence/build05.01/CONTRACT.md`, with the 05.02 delta in `build05.02/CONTRACT.md`. **Guide:** `evidence/build05.02/PRIME-USE.md` (it replaces the 05.01 guide).

```text
python -B labs/module-dependencies-pass01/depdecl.py validate --set ABS
python -B labs/module-dependencies-pass01/depdecl.py requires --set ABS --module REPO:PATH [--transitive] [--depth N] [--condition ID=STATE ...]
python -B labs/module-dependencies-pass01/depdecl.py explain  --set ABS --module REPO:PATH --to REPO:PATH
python -B labs/module-dependencies-pass01/depdecl.py impacted --set ABS --module REPO:PATH [--implementation SHA]
python -B labs/module-dependencies-pass01/depdecl.py identity --set ABS
python -B labs/module-dependencies-pass01/depdecl.py index    --set ABS --out ABS
python -B labs/module-dependencies-pass01/depdecl.py delta    --old ABS --new ABS --change ABS     (revision)
python -B labs/module-dependencies-pass01/depdecl.py delta    --create --new ABS --change ABS      (new module, no predecessor)
python -B -X dev labs/module-dependencies-pass01/tests/test_depdecl.py -v
python -B -X dev labs/module-dependencies-pass01/tests/test_repair.py -v
python -B labs/module-dependencies-pass01/demo.py --snapshots ABS_PACK_SNAPSHOTS --out ABS_NEW_DIR
```

**Layout:**
- `depdecl.py`: the prototype.
- `examples/prime-cycle-chain/`: four PROTOTYPE declarations (prime_cycle, batch_observe, prime_support, clerk_adapter at f0ccb90), and their pinned set. 05.02 replaced prime-support v1 in the set with v2, which records its unenforced import of clerk_adapter as unpinned; v1 stays on disk. The records for prime_review, review_packet, return_inspect, return_capture and the Clerk tool are deliberately absent, so they answer `record-missing`.
- `demo.py`: the bounded demonstration, with labelled SYNTHETIC negative versions.
- `tests/`.

**Reading an answer:**
- **`status`:**
  - `complete-for-declared-coverage` means the declared graph was answered with no blocking findings. The non-blocking `shared`, `environment-unverified` and `condition-inapplicable` findings may remain, and stay listed. It is **not** target-environment readiness, runtime closure or acceptance.
  - `incomplete` otherwise.
  - `truncated` (impacted) means the depth bound stopped the reverse walk with consumers left unexpanded; rerun with a larger `--depth`.
- **`root.state`:**
  - `declared`;
  - `declared-dependency-free` (an explicit `no_requirements`);
  - `undeclared` (no record; `requirements` is null, not empty);
  - `ambiguous-version`.
- **Each requirement** has a `resolution` (resolved, record-missing, pin-differs, identity-pair-mismatch, ambiguous-version, identity-conflict, selected, single-unpinned, not-a-module) and its own findings.
- **`impacted`** lists candidates for Prime review. It changes nothing. Each row's `pin_vs_declarations` compares the consumer pin with the target's declarations as a {sha256, bytes} pair. `--implementation` compares the digest only.

**Pins.** A requirement `pin` is the identity the requiring module itself enforces (a hash check, or a pinned launch). An import it does not hash-check is `pin: null`; any bytes observed at the cut are noted in the reason as observation only. Bytes chosen for a reproducible delivery belong to a later delivery selection.

**What is measured.** Only `identity` measures bytes, and only of the fixture copies listed in the set. Every other answer compares declarations with each other.

Declarations are model-authored and cover only the edges found for their named entry points. A digest proves bytes, not compatibility. There is no OS sandbox or race safety.
