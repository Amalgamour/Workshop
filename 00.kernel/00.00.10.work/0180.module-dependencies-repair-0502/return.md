# Submission — claude-0517-0502 (0517.dependencies 05.02, dependency prototype repair)
who: claude-opus-5-5 (Anthropic), executor named Claude, in the Claude Code desktop app; the same continuing session that built 05.01. 2026-10-31, workshop at e0b10a455858c06ea00e2fede8c4bd1a7209a072.

## Did
- Read Prime's 05.01 review and probes. Verified pack05.02: 14 of 14 snapshots match their pins, equal their committed objects at e0b10a4, and equal live. Recorded the claim. Wrote 06.02.md, then the delta CONTRACT.md, then code. build05.01, 06.01 and capture 0178 are unchanged.
- **Reproduced first,** on the untouched 05.01 code:
  - **D-01:** `impacted C --depth 1` returned [B], exit 0, no findings, with A silently omitted.
  - **D-02:** the right digest with length 999 against a declared 1 was `resolved`, `complete`, exit 0.
  - **D-03:** `delta` without `--old` was an argparse error, and a fabricated predecessor only produced mismatches.
- **D-01, reverse bound:**
  - At `--depth`, consumers that have declared consumers of their own are listed under `unexpanded`, with their count and path, plus a `depth-limit` finding; status `truncated`, exit 1, and an actionable rerun note.
  - A walk that ends inside the bound is complete (exit 0 with no findings).
  - Revisits are marked `shared` (not a finding) or `cycle` (a finding), and consumer provenance is kept.
  - **The same fault in the forward walk:** `depth-limit` now appears only when a module with unwalked requirements was cut.
- **D-02, identity pairs:**
  - A pin resolves only when digest and length both equal a declaration. The right digest with the wrong length is `identity-pair-mismatch`: not resolved and not traversed, with both lengths and "no module file was measured".
  - `impacted` rows gain `pin_vs_declarations` (matches-declared, pair-mismatch, undeclared-bytes or unpinned), and `implementation_compared: "sha256 only"`.
  - `identity`, the only check that measures bytes, adds `declaration-length-wrong`. Explicit `select` and unpinned resolution are kept.
- **D-03, creation:** `delta --create --new N --change C`.
  - No `--old`; `change.old` null; `supersedes` null; version 1.
  - Every initial requirement is introduced with a reason, and changed and removed are empty.
  - Exact identities, and `authorized_by` with `#NN`. A dependency-free new module with `introduced: []` is valid.
  - **Refused:** `--old` with `--create`; a missing `--old` on a revision; empty or unreadable paths; a revision with `change.old` null.
  - `module-change/1` is unchanged; only the CLI gained `--create`. The revision path and its tests are unchanged.
- **Pins and docs:**
  - A pin now means subject-enforced. prime-support v2 records its import of clerk_adapter as unpinned, with the observed bytes noted as observation only; v1 stays on disk, and the set is re-pinned.
  - README and PRIME-USE are aligned: `complete-for-declared-coverage` is not environment readiness, and `environment-unverified` stays visible.
- **Tests:** new test_repair.py (7 tests), plus test_depdecl.py (15). Two 05.01 expectations were changed deliberately and marked (test_15 unpinned; test_05's wrong fixture length).
  - **Final bytes:** 22 OK in dev and default mode, 0 skips.
  - **First runs failed** (kept): 2 expectation changes, then a test-bug sort key, and an order issue in `--old ""` handling (fixed).
  - 8 of 8 repair mutations caught.
- **Demo:** 18 steps, all exits as expected. They include the reverse bound one level too shallow and exactly enough, a pair mismatch, creation and a refused `--old`, and the unchanged revision seam.
- **Sample:** the real set, `impacted clerk_adapter --depth 1`: truncated, with batch_observe and prime_support unexpanded, and prime_support unpinned.

## Blocked
Nothing blocks this batch.

## Need
- **Prime:** review the repair. Re-verify the 0518 integration pins against the new depdecl.py identity before finalizing them; 0518 was not touched.
- **Recommended next action:** Prime reviews this repair. A builder then writes declarations for the four record-missing tools, with pinned provenance, so the real chain answers without record-missing.

## Limits
- Declarations are model-authored, with `complete_claim` false.
- Pair checks compare declarations with each other; only `identity` measures fixture bytes.
- `--implementation` stays digest-only.
- Environment availability is never probed. There is no OS sandbox or race safety.
- Symlink set paths are not exercised on this host.

## Declared outputs (sha256)
- `00.kernel/00.00.10.work/0517.dependencies/06.02.md` 391be3f376213dcea2dd06e8a5565b34518941a8ecdd0bfabe603a5c29d9720a
- `00.kernel/00.00.10.work/0517.dependencies/evidence/build05.02/CONTRACT.md` 255621a7899c792d6160fae26c3649689822c0845ce43da6686126e0e354102f
- `00.kernel/00.00.10.work/0517.dependencies/evidence/build05.02/verification.json` 4981dbd8948533807be1fea38b0ae75c27f8b56a52904fa4c46097a4d3ad0be7
- `00.kernel/00.00.10.work/0517.dependencies/evidence/build05.02/artifact-manifest.json` 498bc22e458207f48bcca99050a12571306ed656df60465a03a1a9055a403f95
- `00.kernel/00.00.10.work/0517.dependencies/evidence/build05.02/PRIME-USE.md` a10ff102667e707c42cfa91a43bde7926310643447625f33ec734e28f573dc63
- `00.kernel/00.00.10.work/0517.dependencies/evidence/build05.02/sample-dependencies.json` 7a219b5535a14b45db100b2da25162f1ad35c1c286f56f37377bd3fbf9f426d3

artifact-manifest.json binds the lab code, tests, demo, README, example declarations (v1 files unchanged since 05.01; prime-support v2 new) and set, notes and evidence: 16 files, including depdecl.py be32e7be8b481d74….
