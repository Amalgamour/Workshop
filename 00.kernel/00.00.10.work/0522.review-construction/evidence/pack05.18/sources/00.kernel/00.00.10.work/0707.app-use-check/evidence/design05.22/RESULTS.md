# RESULTS — harness successor (0707/05.22)
All runs are mine (Claude). Rooms are under `D:/librarian/temp/lch2-0522` (external). Raw stdout, JSON and exits are beside this file.

## A. Reproduction of 06.21 H1–H4 against the preserved pass01 (`reproduce-h-run01`, exit 0)
| | Kind | Result |
|---|---|---|
| H1 | helper probe (direct call) | CAP-4, RP-1, RP-2 and IN-2 return `not-run` with no context at all. **Reproduced.** |
| H2 | helper probe | `aggregate` with dependencies None, {} or `"not-a-list"` → `ready: true`. **Reproduced.** |
| H3 | **full CLI** (pass01 `harness.py --suite strict-n7`, rebuilt proto-l) | ST-2 `pass` with codes lacking `malformed-n7-declaration`. **Reproduced.** pass01 still exited 1, only because K, I, R and W are pending. |
| H4 | helper probe | A 3-case `n5-same-cut` subset with all six dependencies accepted → `ready: true` (pass01 had 35 required). **Reproduced.** |

- **No CLI readiness was ever released by H2 or H4.** The pass01 CLI is still held by today's pending rows, which is exactly why the bug needed a test that does not depend on them.
- **pass01 was hash-checked before and after: unchanged.**

## B. Harness-unit evidence. No app is run. NOT app acceptance.
| Suite | Result | What it shows |
|---|---|---|
| `test_verdict.py` | **40/40**, exit 0 | The 16 inherited cases, reconciled to the new signature. Malformed dependency collections (None, {}, a string, [], a non-object row, a non-boolean or missing `required`, a duplicate, an unknown status, an empty id) are never ready. With every dependency **synthetically accepted**, a passing subset is still NOT READY. The real driver (`select`/`run_cases`/`decide`) over a fake registry gives exits 0, 4 and 1 correctly. The real registry's baseline is 37 required; a capacity-only all-pass gives exit 4 with 32 missing. No callback source contains `"not-run"`. |
| `test_shapes.py` | **24/24**, exit 0 (run01: 2 failures in **my test helper**, kept) | Every malformed `harness-inputs/2` shape is refused before execution. That includes a status string flipped to `accepted` without pins, and a wrong frozen review reference. The unmutated inputs validate. |
| `test_callbacks.py` | **29/29**, exit 0 | **LABELLED SCRIPTED COMMAND RESPONSES:** CAP-4, RP-1, RP-2 and IN-2 drive the right commands, and pass only good responses. Each fails these explicitly: 9 CAP-4 variants, 7 RP-1, 4 RP-2 and 6 IN-2 bad variants, including an unimplemented route, missing fields, a crash, an always-refusing reporter, and a copy that reads current. The strict and N7-3 judges pass and fail as required. Wrong types (`exit: true`, `stale: "true"`, a list body) never pass. |

## C. Real-candidate evidence: the actual baseline commands
### Full suites (37 required cases; scope full)
| Candidate | Exit | Ready | Counts | Not-ready reasons (summary) |
|---|---|---|---|---|
| proto-l (the 05.20 prototype) | **1** | false | 26 pass · 4 fail · 7 blocked · 3 known failures reproduced | ST-1, ST-2, ST-3 (no `malformed-n7-declaration`); N7-3; K, I, R and W pending |
| staged-g (the accepted pass05/v9) | **1** | false | 19 pass · 11 fail · 7 blocked · 3 known failures | N7-1/2, LR-1..7, PR-6 (no local exchange; as in 05.21); N7-3; K, I, R and W pending |
| combined (PENDING) | **1** | false | 40 blocked | candidate PENDING; K, I, R and W pending |

- **Reconciliation against the 05.21 results** (`reconcile-*.json`): 40 rows per candidate, 30 unchanged, **0 UNEXPECTED.** Every change is the one declared before the run:
  - **proto-l ST-2: pass → fail** (H3);
  - **ST-4 and N7-3:** new;
  - **CAP-4, RP-1, RP-2 and IN-2:** now real callbacks, still blocked in the suite;
  - **LR-6:** a destination check was added; the verdict is unchanged on both.
- **New real findings:**
  1. **N7-3 fails on BOTH baselines.** Both store and render N7 custody as `missing`; staged-g also lacks the exchange. This is a real integration requirement, not a harness defect. The combined W must record `not-applicable`.
  2. **On proto-l, ST-2 binds the rejected alternative `06.15.notes.md` as the submission.** The prototype was refused for the pair rule, but its grammar accepted the second `Returned:` line.

### Callback probes (`probe.py`: the dependency gate is bypassed, `mode: probe`, always exit 1, **never readiness**)
| Case | proto-l and staged-g, identical | Real baseline behaviour |
|---|---|---|
| CAP-4 | fail | 64 refused `limit sources` (old 24 bound). 65 refused. **The unrelated limits already hold:** 25 reasons refused `limit reasons`; a 265605-byte judgment refused `input exceeds 262144 bytes`. K must keep both. |
| RP-1 | fail | `review-report` gives no JSON body (`stop: normal run is not activated`): an unimplemented route. |
| RP-2 | fail | The positive control fails for the same reason, so no refusal is credited. |
| IN-2 | fail | The copy reads current, its recover returns the judgment, and **its publish succeeds and writes a destination.** The original stays current and unchanged. |

### Hostile (`demo_hostile.py`, 14/14, exit 0)
- **HX-1..HX-6** are the 05.21 cases, reconciled: HX-5 now runs the three unit suites, and HX-6 reports scope subset with 32 missing.
- **HX-7/8/9:** dependencies None, {} or a string **through the CLI** → exit 2, with no rooms.
- **HX-10:** a status-only promotion → exit 2.
- **HX-11:** a wrong review reference → exit 2.
- **HX-12:** an unknown suite group → exit 2.
- **HX-13:** on staged-g, every strict-n7 subset case passes, `subset.all_selected_required_pass: true`, yet NOT READY (exit 1, pending dependencies).
- **HX-14:** on proto-l, ST-1/2/3 fail, naming the absent malformed reason; the ST-4 control passes.

### Reconstruction (`reconstruct-run02`, exit 0)
- **Fresh root:** both candidates rebuilt by the frozen pass01 builder (hash-checked); the three input manifests are **byte-identical** to `inputs/`; the three unit suites pass; strict-n7 on the rebuilt staged-g is 4/4 pass (exit 1, pending dependencies).
- **No production writes:**
  - 183 frozen `app/` and `labs/` rows show zero drift;
  - none of the 220 `app/` files changed after the pack05.22 manifest was written.
- **run01 (kept)** flagged 200 untouched pre-existing `app/` files. My check compared against pack rows, which freeze only 20 `app/` files. Fixed in my checker, not in any input.

## D. First failures kept
1. **`test-shapes-run01-FIRST-FAILURE.txt`:** the helper `doc = mutate(doc) or doc` replaced the document with `pop()`'s return value. S08 and S12 failed for the wrong reason.
2. **`reconstruct-run01-FIRST-FAILURE.*`:** the wrong production-write rule (above).
3. **No harness crash, and no `error` record,** in any suite run.

## E. Freeze
- **pack05.22:** 689 rows. 689/689 snapshots are equal, at the start and at the end.
- **687/689 live files are equal.** The two drifts are the Grok-1 and Grok-2 assignment pages (0512/05.11 → cd37fa13…, 0522/05.16 → 2db73a62…), the same values at the start and at the end.
  - **I did not read their live bytes.**
  - The frozen snapshots are the requirement text. No repin.
- **The pass01 harness is unchanged.** `app/librarian.py` is still c3a5be3b….
