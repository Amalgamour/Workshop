# 0707.app-use-check / pass04 — external acceptance harness for the isolated loop (NONPRODUCTION)

**What this is.** A contract-derived acceptance lab for the loop successor (0522/05.08). Its author is the session that wrote the contract; it is not a fresh review. **Real candidate acceptance has NOT run:** the candidate identity is null, so every real run is UNREADY.

| File | What |
|---|---|
| `harness.py` | config loading, preflight, bounded subprocess runner (child-tree kill only), unique run directories, case table, aggregate |
| `cases.py` | the REAL matrix: 33 rows (A01–A26 with sub-cases; A24 MANUAL), from `evidence/lab05.04/MATRIX.md` |
| `fixtures.py` | copy-only, pin-checked book builders; pass01 `decide.py` recipe (hash-checked, read-only); mutations |
| `candidate.config.json` | the real config: candidate sha256 and bytes **null** |
| `stubs/STUB_loop.py`, `stub_cases.py` | **STUB** CLI and matrix for harness self-tests; never loop evidence |
| `selftest.py` | harness self-tests (stubs, fixture builders, real-case code smoke) |

## Commands (from any directory; paths absolute)
```text
python -I -B colab/labs/0707.app-use-check/pass04/harness.py preflight --config ABS-CONFIG
python -I -B colab/labs/0707.app-use-check/pass04/harness.py run --config ABS-CONFIG --matrix real [--evidence ABS-DIR]
python -I -B colab/labs/0707.app-use-check/pass04/selftest.py
```

**Exits:**
- **0** PASS;
- **1** FAIL or INCOMPLETE (any MANUAL or NOT RUN case blocks PASS);
- **2** UNREADY or REFUSED.

**Evidence:** each run writes `evidence/lab05.04/runs/<UTC>-<hex>/`:
- `config.json`, `preflight.json`, `summary.json` (config sha256, code sha256s, command, aggregate, `loop_evidence`), `CASES.md`;
- per case: `cases/<ID>/calls/NN-label.{json,stdout,stderr}`, `checks.json` and `fixture-*.json`.

**Fixture books** live under `output_root/<run>/<case>/`. Nothing is deleted.

## Config schema `acceptance-candidate/1` (exact keys)
| Key | Meaning |
|---|---|
| `kind` | `candidate` (the real matrix only) or `stub` (the stub matrix only) |
| `label` | text |
| `candidate` | {path, sha256, bytes}. **null sha256 or bytes means UNREADY**, and the path is never read |
| `dependencies` | [{path, sha256, bytes}], all must match before launch |
| `interpreter` | {path, version}; the version is checked with `-I -B -c platform.python_version()` |
| `output_root` | an existing absolute directory outside `D:\Git\lib-build` and the live book |
| `timeout_seconds` | per call, 1–600. On timeout the launched child and its descendants are killed (`taskkill /T /F /PID <child>`; POSIX `killpg`) and the call is ERROR |
| `field_map` | contract path → candidate path, recorded in `config.json`; default `{}` |
| `release` | {invocation, note}; informational |
