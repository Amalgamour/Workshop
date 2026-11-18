# CONTRACT delta — execution proof v2, restored combined fixtures, reporter v2 (0707/05.25)
Over 05.24's SCHEMA.md. Labs: `labs/freshness-boundary-tests-pass03`, `labs/loop-convergence-harness-pass04`. Earlier labs stay frozen.

## Execution proof v2 (`identity3.execution_proof`)
- **Three runs of a fixed probe at ONE absolute path:** control, control, and a copy with a tamper line prepended to the target.
- **Every run is traced by the LAB AUDIT TRACER** (`tracer/sitecustomize.py`, prepended to `PYTHONPATH`). It records `cpython.run_file`, `exec` (code `co_filename`), `compile`, `open` and `subprocess.Popen` events under the disposable root, with pid and argv.
- **The doors copy `os.environ`** and run `sys.executable -B script`, so the tracer follows workbook and report subprocesses.

| Class | Evidence | Gate |
|---|---|---|
| `executed` | both controls' audit logs show the declared target run (`run_file`) or exec'd under the disposable root, during the probe command; the tamper run differs (corroboration: nonce, compile failure, target-named refusal or output change). Bound to the executing pid and argv. | **passes** |
| `verified-pin-check` | the target was opened or read, never run or exec'd; the tamper run changes (e.g. a digest refusal) | refuses |
| `decoy` | no audit access; the tamper run is identical | refuses |
| `nondeterministic` | the two untampered controls disagree | refuses |
| `unattributed-change` | the tamper run differs, but the audit shows no access to the target | refuses |
| `contradictory` | the audit shows execution, but the tamper run is identical | refuses |
| `no-audit-evidence` | an audit log is absent or unreadable | refuses |

- **An output delta or a target-named refusal alone can never set `executed`.** The open entry must also exit 0 on a new root.
- **Disclosed limits:**
  - the tracer shadows an installed `sitecustomize`;
  - a candidate that launches Python with `-I`, `-S` or a scrubbed env would give `no-audit-evidence`, which fails closed.

## Identity (`candidate-identity/1`, optional additions)
- **`loop_door`, `report_door`:** declared files used by the proposed DD-1..4.
  - **Legacy baselines:** `loop_door` is derived (proto-l `app/review_loop_tools_v8.py`, staged-g `app/review_loop_tools_v9.py`), labelled.
- **`builder`:** `{path, sha256, bytes, args}`. It is run as `BUILDER args… --root ABS` (0420/06.59) into an unoccupied root.

## Combined fixtures (harness pass04)

| Case | Contract |
|---|---|
| N5-1..3 | **Install the frozen v7 baseline closure** (v7.json + 17 tools, verified against the v7 pins and pack05.25) into the room where absent. A different file at a closure path is a recorded collision and is never overwritten. **The baseline must succeed** (exit 0, measurement and intake id present) before any comparison; otherwise `fail` naming the baseline refusal and the closure state. **Differences are reported per field** (codes: only_candidate / only_baseline). |
| PR-7 | **A successful control prepare first,** then a FRESH copy with the declared workbook altered (an appended comment, so the code stays valid) and the real dispatcher. **Required:** a clean refusal (integer nonzero, no traceback). |
| CTX-1 | **Fresh N5, N7, N5 prepares must succeed with intake ids.** Explicit identity: the workbook's `build_intake(book, page, pass_id)` hook, which must exist. Legacy: the reviewed adapter, labelled. **A load or call failure is a `fail` with its reason.** In-process ids must equal the fresh ids. |
| RC-1 | **Explicit identity:** the declared builder runs `--root ABS`. **Required:** exit 0, no created/changed/removed file under the builder's own directory, every declared file and CANDIDATE.json byte-equal, and the same N7 rows and cuts. **No builder declared is a `fail`**, with the 0522/05.18 blocker stated (its CLI writes under the delivered lab; never executed here). **Legacy:** the frozen pass01 builder (unchanged). |
| DD-1..4 | **PROPOSED, NOT REQUIRED:** altered or missing loop/report door → a clean refusal with no audit execution of the altered door. `blocked` when the door is not declared. |

**Required case sets unchanged:**
- **convergence:** 37 (ids, groups, needs and requirement text identical to pass02); 44 records in total, with KF-* and DD-* non-required;
- **freshness:** 34 / 32 (pinned pass01).

## Reporter v2 (`reporter_judges2.guard_v2`; proposed RP-3; not in the 37)
- **The pass03 rules are unchanged.** Added:
  - an inspect exit that is not the integer 0;
  - an inspect `current` that is missing or differs from the read review id;
  - an inspect `stale` that is not `false`;
  - a non-integer prepare exit, or a nonzero one with `measurement: complete`;
  - a prepare measurement that is not `complete`.
- **Any anomaly means the report must not be `readable`.**
