# App-to-worker integration design (batch 05.04)

**who:** claude-opus-5-5, Colab · **date:** 2026-10-26 · **state:** design proposal for Codex Prime review. Nothing here is implemented, run or approved.
**inputs:** `evidence/pack05.04/` (13 snapshots, all matching their pins), plus the Prime-accepted pass 03 lab manifest for the three bridge files the pack does not pin (`canon.py`, `ids.py`, `fixtures/worker_fixture.py`; see 06.04 T04).

## 1. Shape in one line

`app/librarian.py bridge-test` turns one fixture job into one envelope and hands it to the accepted lab adapter, which is loaded by pinned hashes. It prints the receipt. Nothing dispatches, loops, retries or accepts.

## 2. Module plan

| Piece | Owner | Change in the next slice | Responsibility |
|---|---|---|---|
| `app/librarian.py` | app | three thin subcommands: `bridge-test`, `bridge-status`, `bridge-recover` | parse arguments, call `worker_bridge`, print, set the exit code |
| `app/context.py` | app (APP-01 repair: Grok) | **none by this slice** | resolve and validate the fixture container's context (`validate_context(execute=True)`) and the designated-container rules from APP-01 |
| `app/worker_bridge.py` | app, **new** | glue only | load `app/worker-bridge.json`; hash-check every pinned bridge file **before** import; import the bridge as an isolated package; build the envelope from the job and the container; enforce `allowed_kinds`; call `deliver`, `status` or `recover`; return the receipt and its hash |
| `app/worker-bridge.json` | app, **new** | the pins (example: `example/worker-bridge.json`) | the lab path, eight file hashes, allowed kinds, the container subfolder |
| `labs/worker-bridge-pass01/bridge/*`, `profiles.json`, `fixtures/worker_fixture.py` | lab | **unchanged** | transport, validation, verification, receipts; used only at the pinned bytes |
| Clerk, observer, scheduler, real-model profile | — | not in this slice | — |

**Why glue in `app/`, not a page:** the bridge is a development dependency, pinned exactly the way the app pins the runner candidate. No page is allocated and no N3NN band is used, so runtime lookup is unchanged. Moving the bridge into law (a `03NN` candidate) or into the app package is a later Director decision (section 8).

**Import rule:**
1. Read each file's bytes and compare SHA-256 against the pin; any mismatch refuses before import.
2. Build a package spec with `importlib.util.spec_from_file_location("worker_bridge_pinned", <dir>/bridge/__init__.py, submodule_search_locations=[<dir>/bridge])` and register it under that private name for the call.
3. Remove `sys.path` changes afterwards; write no bytecode (`sys.dont_write_bytecode`, as `librarian.py` already sets).

Stated limit: a same-user change between the hash check and the import is not prevented (06.04 N08).

## 3. Authority: what exists and what is proposed

| Check | Status | Where |
|---|---|---|
| The fixture root is not the live workspace or work book | **exists** | `context.overlaps_live` |
| The record's `assignment_state` is `released` | **exists** (in fixture mode this is the fixture's synthetic record: it proves the check path, not real authority) | `context.validate_context(execute=True)` |
| The record is never the derived `00.live.md` | **exists** | `context.validate_context` |
| The container is designated by app config or invocation, not by fixture metadata; no source tree inside it; no alias escape | **proposed by APP-01, owned by Grok, not accepted** | `context.py` after 0504/05.02 |
| The job's `work_ref` equals the record's `current_work` | **proposed here** | `worker_bridge.py` |
| The profile's `kind` is in `allowed_kinds` (`protocol test worker` only) | **proposed here** | `worker_bridge.py` |
| Every bridge file matches its pin before import | **proposed here** (same pattern as the runner pin, which exists) | `worker_bridge.py` |
| Envelope shape, id rules, limits, input hashes, the allowlisted argv, artifact containment and bytes | **exists** (lab, accepted) | `envelope.py`, `ids.py`, `adapter.py`, `verify.py` |

Never authority:
- the envelope's `release` field (filled as evidence: `{by: "fixture record", ref: "<record path> sha256 <hash>"}`);
- a fixture label;
- `transport: delivered`;
- `collection: collected`.

Every output says `review: not performed` and `acceptance: not performed`.

## 4. The end-to-end fixture job (concrete)

**The container** (the path comes from APP-01's interface, for example `app/scratch/bridge-0001/` or an explicit external folder):

```text
<container>/
  00.kernel/00.00.10.work/0401.goal/06.01.md          synthetic record: assignment_state released,
                                                      current_work 00.kernel/00.00.10.work/0501.fixture/05.01.md
  00.kernel/00.00.10.work/0501.fixture/05.01.md       synthetic work item
  00.kernel/00.00.01.law/...                           the minimal runtime band that validate_context needs (as 0504 fixtures)
  <APP-01 container metadata>                         whatever the repaired interface defines
  bridge/job.json                                     example/job.json
  bridge/input/input.txt                              example/input.txt: 22 bytes, sha256 f1f6c82d215ccf38a9d5eafce281febb2c971dc71ae7a15bbe0c1c81458d69c8
  bridge/output/                                      empty; the worker's only write root
  bridge/store/                                       the adapter's receipt store
```

**Invocation** (development only, run by hand):

```text
python <workspace>/app/librarian.py bridge-test   --root <container> --job bridge/job.json
python <workspace>/app/librarian.py bridge-status --root <container> --delivery bridge-0001
```

**Sequence, and who does what:**

1. `librarian.py` loads `context.py` and `worker_bridge.py` from its own folder.
2. `context` checks that the container is designated and not the live workspace (APP-01), and resolves the synthetic record: `released`, `current_work`.
3. `worker_bridge` reads `bridge/job.json` with the bridge's strict loader, and checks that `work_ref == current_work`.
4. `worker_bridge` hash-checks the eight pinned files, imports the bridge, reads `profiles.json`, and checks that `fixture-ok` has kind `protocol test worker`.
5. `worker_bridge` builds the envelope:
   - **from the job:** `schema worker-bridge/request@1`, `delivery_id bridge-0001`, `job_id job-count-lines`, `role builder`, `work_ref`, `inputs`, `backend fixture-ok`, `limits`;
   - **paths:** `input_root <container>/bridge/input`, `output_root <container>/bridge/output`;
   - **release:** `{by: "fixture record", ref: "00.kernel/00.00.10.work/0401.goal/06.01.md sha256 <record hash>"}`.
6. The adapter (lab) validates the envelope, writes `store/bridge-0001/request.json` and `launch.json`, then starts `{python} -B -I fixtures/worker_fixture.py --mode ok` with no shell, cwd the output root, and the request on stdin.
7. The fixture worker reads `input.txt`, writes `output/result.json` = `{"count":3}` (11 bytes, sha256 `0c07187ea6d064441225b3cba26a7b1e8bc702fcf332b457dae8e26892ba68a6`), and prints a `worker-bridge/result@1` object.
8. The adapter correlates the ids and `request_sha256`, verifies the artifact's path and bytes, and writes `store/bridge-0001/receipt.json` (shape as `reference-receipt.json`).
9. `librarian.py` prints, then exits 0:

   ```text
   delivery_id: bridge-0001
   worker_kind: protocol test worker
   transport: delivered
   claimed_outcome: done
   collection: collected
   artifact: bridge/output/result.json sha256 0c07187e…
   receipt: bridge/store/bridge-0001/receipt.json sha256 <hash>
   review: not performed
   acceptance: not performed
   ```

10. A fresh process runs `bridge-status`, reads the same receipt through `adapter.status`, and prints the same lines and the same receipt hash.

`request_sha256` covers the absolute container paths, so it is fixed only per run. The input and artifact hashes above are fixed.

## 5. Failure and recovery contract (observable outcomes)

Exit codes for the bridge subcommands:
- **0:** collected.
- **2:** refused before launch.
- **3:** delivered, but not collected, or the worker claims failure.
- **4:** the outcome is uncertain.

| Case | How it is produced (fixture profile or setup) | Receipt or result | App exit | Relaunch |
|---|---|---|---|---|
| success | `fixture-ok` | delivered, collected, claimed done | 0 | — |
| malformed result | `fixture-garbage`, `-partial`, `-bad-shape`, `-dup-keys` | malformed, uncertain, not attempted | 4 | never automatic |
| wrong artifact hash | `fixture-bad-hash` | delivered, uncollected ("bytes differ") | 3 | — |
| missing or escaping artifact | `fixture-missing-artifact`, `-escape` | delivered, uncollected | 3 | — |
| timeout | `fixture-sleep`, `limits.timeout_s` 1.5 | timeout, uncertain (work may have started) | 4 | never automatic; a repeat replays |
| incomplete output / retained pipes | `fixture-inherit-pipes` | incomplete-output, uncertain, `cleanup.retained` named; returns within about timeout + 2 s + start-up | 4 | never automatic. The CLI process exits, so the retained readers end with it and the descendant may see a broken pipe (06.04 N07) |
| repeat identical delivery | the same job twice | the stored receipt, `replayed: true`; `launches.log` still 1 line | as the original | none |
| conflicting delivery identity | the same `delivery_id`, a changed job or input | refused ("reused with a different request") | 2 | none |
| interrupted receipt persistence | a crash after the attempt, before `receipt.json` (test hook) | `bridge-status`: uncertain (launch recorded, no receipt); `bridge-recover`: the receipt rebuilt from the recorded attempt, `recovered: true` | 4, then the recovered receipt's code | `recover` never launches |
| a launch record with no attempt | — | `bridge-recover` refuses; uncertain | 4 | none; only a new `delivery_id` moves on |
| invalid fixture scope | a live root, an undesignated container, a source tree as container, a job path escape, `../` in a delivery id, an unknown profile, a kind not allowed, `work_ref` ≠ `current_work`, a record not released, bad limits, a pinned-file hash mismatch | refused before launch, with the reason; no store write where the check precedes the store | 2 | none |

Kept separate in every row: transport, artifact validity (collection), review, and acceptance. Not promised: process-tree termination, authentication, a sandbox, general concurrency (one launcher per delivery through `launch.json` only).

## 6. The next implementation slice (one batch)

**Title:** app-to-worker fixture exchange, protocol workers only.
**Prerequisites:** APP-01 repaired and accepted by Prime (the container interface); pass 03 lab accepted (done).
**Executor:** the Director's choice. The files touched are app files, so it follows the app's single owner: Grok, after 0504/05.02, or Claude if the Director moves app ownership.

**Files**
- **New:**
  - `app/worker_bridge.py`;
  - `app/worker-bridge.json` (the example above, with hashes re-verified at packing);
  - `app/tests/test_worker_bridge.py`;
  - a fixture container builder inside the tests.
- **Changed:** `app/librarian.py` (three subcommands) and `app/README.md` (one section).
- **Unchanged and pinned:** the lab, `context.py` (beyond the APP-01 repair), law and the books.
- **Dependencies:** the Python standard library only. No install.

**Demonstration**, exact, in a container under `app/scratch/`:
1. `bridge-test --root <c> --job bridge/job.json` → exit 0, the printed lines from section 4.
2. A fresh process runs `bridge-status --root <c> --delivery bridge-0001` → the same receipt hash.
3. `bridge-test` again → `replayed: true`, and `bridge/output/launches.log` has exactly one line.

**Acceptance checks**
1. The demonstration above, with the artifact bytes equal to `example/expected-result.json`.
2. Every failure row of section 5 produces its stated receipt and exit code. The timeout and inherited-pipe rows return within their documented bounds, under an outer watchdog.
3. Each refusal row refuses before any launch (no `launch.json`) and before any write outside `bridge/`.
4. Protected bytes are unchanged before and after the suite: `app/README.md`, `app/context.py`, every pinned lab file, the live work book and the assignment record.
5. A tampered copy of a pinned bridge file in a scratch copy refuses at import.
6. No bytecode in source or books. The existing app suite and the lab's 30 tests still pass.
7. Nothing in the slice calls a real model, dispatches, loops, uses SQLite or adds UI.

## 7. Differences between the pinned snapshots and the live files

At the start and the end of this pass, all 13 pinned paths were byte-identical to the live files (checked by SHA-256). The pack does not pin `canon.py`, `ids.py` or `worker_fixture.py`. Their live hashes equal the accepted pass 03 manifest, and section 6 pins them.

## 8. Director decisions (actual ones, with effects)

- **D-1, deferred, not needed for the slice: the long-term home of the bridge code.**
  - Options: a law `03NN` runtime candidate under seating, or an app package.
  - Effect: where custody, versioning and lookup apply.
  - Recommendation: keep it in the lab, pinned by hash, until one real-model exchange is accepted; then propose a law candidate.
- **D-2, already pending separately:** the release of a named real-model connection (backend, cost cap, confinement). Not part of this slice.

Everything else in this design is a routine implementation choice, with a recommendation above.
