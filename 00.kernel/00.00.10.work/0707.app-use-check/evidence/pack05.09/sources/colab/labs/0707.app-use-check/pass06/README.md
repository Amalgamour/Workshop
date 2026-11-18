# 0707.app-use-check / pass06 — H04 path-input refusals (NONPRODUCTION)

**Successor of `../pass05`.** pass05 is unchanged. **Real candidate acceptance has NOT run:** `candidate.config.json` keeps the candidate sha256 and bytes null.

| File | What |
|---|---|
| `guards6.py` | pass05 `guards.py` plus `path_text()` and a narrow `fs()` translation of ValueError/OSError into `Boundary("path-os")` |
| `harness6.py` | pass05 `harness5.py` plus path-text validation of every path-bearing config field, narrow translation at `read_config`, the evidence directory, `check_file_pin` and the interpreter probe, and controlled refusal when run, case or fixture directories cannot be created |
| `selftest6.py` | H04 tests, plus pass05's 20 self-tests rebound to pass06 (pass05's `main` is never run) |
| `candidate.config.json` | the real config: null candidate, `output_root` in new scratch |

**Reused unchanged and hash-checked against pack05.06** (recorded as `reused_pass05` in every run): pass05 `winjob.py`, `stub_cases5.py` and `stubs/STUB5.py`. pass04 `cases.py` and `fixtures.py` are reused the same way (`matrix_provenance`).

## Commands
```text
python -I -B colab/labs/0707.app-use-check/pass06/harness6.py preflight --config ABS-CONFIG
python -I -B colab/labs/0707.app-use-check/pass06/harness6.py run --config ABS-CONFIG --matrix real|stub --evidence ABS-EVIDENCE
python -I -B colab/labs/0707.app-use-check/pass06/selftest6.py
```

The evidence rules and exits are as in pass05: `--evidence` is required, under `0707…/evidence/lab05.NN` with NN ≥ 05; exit 0 PASS, 1 FAIL or INCOMPLETE, 2 UNREADY or REFUSED.
