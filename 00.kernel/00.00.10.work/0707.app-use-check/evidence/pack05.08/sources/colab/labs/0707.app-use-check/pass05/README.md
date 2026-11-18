# 0707.app-use-check / pass05 — acceptance harness successor (NONPRODUCTION)

**Successor of `../pass04/harness.py`.** pass04 is unchanged and its results stand. **Real candidate acceptance has NOT run:** `candidate.config.json` keeps the candidate sha256 and bytes null, so every real run is UNREADY.

| File | What |
|---|---|
| `harness5.py` | config validation (H03), preflight, launch with output preservation and Job containment (H01), canonical boundaries (H02), run record |
| `guards.py` | link-free, resolved path checks: protected roots, the output root, the authorized evidence root, fresh exclusive directories |
| `winjob.py` | Windows Job Object containment of each launched child's tree; `taskkill /T` fallback; POSIX process group |
| `stubs/STUB5.py`, `stub_cases5.py` | **STUB** CLI and matrix; never loop evidence |
| `selftest5.py` | 20 self-tests: H01, H02 (junctions in new scratch only), H03 fuzz and bytes, preservation |
| `candidate.config.json` | the real config with a null candidate |

**The real matrix is pass04's `cases.py` with pass04's `fixtures.py`,** loaded unchanged after their pack05.05 hashes match. Only `fixtures.build_book` is wrapped in memory, by the boundary guard.

## Commands
```text
python -I -B colab/labs/0707.app-use-check/pass05/harness5.py preflight --config ABS-CONFIG
python -I -B colab/labs/0707.app-use-check/pass05/harness5.py run --config ABS-CONFIG --matrix real|stub --evidence ABS-EVIDENCE
python -I -B colab/labs/0707.app-use-check/pass05/selftest5.py
```

**`--evidence` is required.** It must resolve, with no link anywhere on its path, under `00.kernel/00.00.10.work/0707.app-use-check/evidence/lab05.NN/` with NN ≥ 05. Each run creates `<evidence>/<UTC>-<hex>/` exclusively. Fixture books go under `<output_root>/<run>/` exclusively.

**Exits:**
- **0** PASS;
- **1** FAIL or INCOMPLETE;
- **2** UNREADY or REFUSED (including any config, boundary or provenance refusal).

## Per-call record
`argv`, `parent_exit`, `exit` (null if timed out), `timed_out`, `timeout_reason`, `termination`, `containment{method,note}`, `leftover_descendants`, `output_status`, stdout and stderr bytes and sha256, plus the raw `.stdout` and `.stderr` files.

**`output_status`** is one of: `complete`, `complete-after-termination`, `partial-cleanup-incomplete`.

**A case is ERROR** when any call timed out, left descendants, or did not end with `output_status: complete`.
