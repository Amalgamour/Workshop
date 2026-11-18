# PRIME-USE — pass06 acceptance harness
date: 2026-11-01 · who: claude-opus-5-5 (Claude)

## Check this pass
1. **Verify the artifact manifest** in this directory: `artifact-manifest.json` (it excludes itself).
2. **Rerun the self-tests** into a NEW location. `selftest6.py`'s output paths are module constants (`OUT`, `SCRATCH`). To redirect them, import the module, rebind those constants, then call `main()`, as Prime did for pass05. A plain run writes a new stamped directory under `lab05.07/selftest/`:
   ```text
   python -I -B colab/labs/0707.app-use-check/pass06/selftest6.py
   ```
   The expected result is 37 tests: 17 H04 and 20 rebound pass05.
3. **Reproduce H04 by hand:**
   - make a config like `pass06/candidate.config.json` with `output_root` set to `"C:\\x\u0000y"`;
   - `pass05/harness5.py preflight --config <it>` gives a ValueError traceback, exit 1;
   - `pass06/harness6.py preflight --config <it>` gives `refused: config-path: …`, exit 2, with no traceback.

## Refusal codes added or reached by H04
| Code | Where | Meaning |
|---|---|---|
| `config-path` | shape (`validate_config`, `read_config`) | the path text is empty, longer than 32767 characters, or contains NUL or another C0 control character. **String check only; no filesystem access** (so an unknown candidate path is never opened) |
| `config-read` | `read_config` | ValueError or OSError while reading the CLI config file |
| `path-os` | guards (`lstat`, `abspath`, `lexists`, `realpath`, `isdir`, `isjunction`, `mkdir`) | ValueError or OSError from a filesystem call on output, evidence, run, case or fixture paths |
| `pin` | `check_file_pin` | a dependency or known candidate is missing or unreadable (now including OSError/ValueError) |
| `interpreter` | preflight | the interpreter is missing, cannot be launched (OSError, for example WinError 193), or its probe timed out |
| `occupied` | `fresh_dir` | the directory exists already, or appeared before `mkdir` (FileExistsError) |

**Not translated:** any other exception. Test `test_programming_error_is_not_swallowed` shows a planted TypeError propagating out of `run_matrix`.

## Activation (unchanged in meaning)
Follow `lab05.04/ACTIVATION.md` items 1–8, using `harness6.py`, a NEW config file with Prime's reviewed candidate pins, and a NEW `lab05.NN` (NN ≥ 08) evidence directory. Run `selftest6.py` on the activation host first. A24 stays MANUAL, so INCOMPLETE is the best real aggregate; a PASS here is not acceptance.
