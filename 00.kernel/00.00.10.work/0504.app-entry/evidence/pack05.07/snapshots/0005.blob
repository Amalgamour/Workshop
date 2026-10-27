# SEAM — Clerk claim to one worker delivery to Clerk return

Batch: `0506.clerk-handoff/05.03`, design only.
Author: claude-opus-5-5, Colab, technical lead.
Date: 2026-10-27.
Inputs: pack05.03 (15 files at 54274e6). Line references below are to those snapshots.
Nothing here is built, run, or released.

## 1. The connection in one line

```text
router writes jobs -> clerk queue -> clerk claim (explicit)
  -> librarian clerk-deliver: resume-read claim -> one bridge delivery -> verify receipt artifact
     -> exclusive copy into the Clerk outbox -> clerk return -> reviewer inbox (a projection; nobody is invoked)
```

**One new app command, `clerk-deliver`, in a new `app/clerk_seam.py`.**
- It reuses `worker_bridge.perform` for the delivery.
- It reaches Clerk only through Clerk's public CLI, as a subprocess of a hash-pinned `clerk.py`.
- It never queues, claims, chooses a recipient, reviews, accepts, retries, or relaunches.
- Routing, assignee, reviewer and release come from records that the router (intelligence) wrote.

## 2. Placement: two rules, one container, no override

- **App rule:** the app writes only inside a designated container: `app/scratch`, the 0504 fixtures, or an external `--container` that is disjoint from the workspace (`context.select_container`).
- **Clerk rule:** a Clerk store must resolve outside every Git working tree, and there is no bypass (`clerk.py:240-245`).

`app/scratch` therefore cannot hold a Clerk store. The seam uses **one external container that holds both**, as siblings. The verified-artifact copy then lands inside the app's own designated container, and the Clerk store is outside Git. Neither boundary is bent.

```text
<T>/router/instructions/task.md            router   Clerk instructions base (read only to the seam)
<T>/router/clerk-job.json                  router   Clerk job file
<T>/container/                             --container (external, not in Git, not a filesystem root)
  clerk-store/jobs/clerk-0001/             Clerk    0001.queued, 0002.claimed, outbox/, 0003.returned (+ 05.02 witness)
    outbox/result.json                     seam     the only seam write outside the fixture root
  fixture/                                 --root   synthetic released record, current_work = work_ref, runtime band (as 0504 fixtures)
    bridge/job.json                        router   bridge job
    bridge/declared/task.md                router   byte copy of the instruction file
    clerk-link/bridge-0001.json            router   link between this delivery and the Clerk job
    bridge/delivery/bridge-0001/input/     bridge   fresh, exclusive (worker_bridge.py:538-541)
    bridge/delivery/bridge-0001/output/    bridge   fresh worker output: result.json AND launches.log
    bridge/provenance/bridge-0001.json     bridge   exclusive
    bridge/store/bridge-0001/              adapter  request, launch, attempt/, receipt
```

**Why the worker never writes into the Clerk outbox:**
- fixture-ok appends `launches.log` beside `result.json`. Clerk refuses any extra outbox file (`clerk.py:823-831`).
- Clerk creates the outbox at claim time (`:797-800`), so it exists before the bridge's "fresh output" rule could apply.

So the seam copies only the receipt's verified artifacts. A fixture placed in `app/scratch` is refused through Clerk's own rule (Clerk store inside Git), and the seam adds no flag to get around it.

## 3. Example records (files beside this one, in `examples/`)

- **`router/clerk-job.json`:** job `clerk-0001`; assignee `fixture-worker`; reviewer `codex-prime`; instructions `task.md` with sha256 `6c913091…` (175 bytes); expected_outputs `["result.json"]`.
- **`fixture/bridge/job.json`:** `librarian-bridge-job` v1; delivery `bridge-0001`; job_id `clerk-0001` (equal to the Clerk id); backend `fixture-ok`; inputs[0] is the same `task.md` hash; limits.
- **`fixture/clerk-link/bridge-0001.json`:** proposed `librarian-clerk-link` v1. Exact keys, all of which the router writes once (exclusive):

  ```json
  {"schema":"librarian-clerk-link","version":1,"delivery_id":"bridge-0001",
   "clerk_store":"<abs path inside the container>","clerk_job_id":"clerk-0001",
   "bridge_job":"bridge/job.json","bridge_job_sha256":"4d57cdb9…"}
  ```

  It holds no assignee, reviewer, state, token or authority. It only pins which Clerk job this delivery serves.
- **`app/clerk-seam.json`:** proposed pin config, `librarian-clerk-seam` v1, `{clerk_path, clerk_sha256}`. The hash is the 0506/05.02 clerk.py that Prime accepts.

The expected artifact is `result.json` = `{"count":3}`, sha256 `0c07187e…`, 11 bytes. That is the same bytes and hash as the 0504/05.05 demonstration.

## 4. The command

```text
python <ws>/app/librarian.py clerk-deliver --root <T>/container/fixture --container <T>/container
       --link clerk-link/bridge-0001.json --as fixture-worker --instructions-base <T>/router/instructions
```

Steps. Each one stops at the first failure.

| # | Step | Reads | May write | Stop outcome |
|---|---|---|---|---|
| S0 | app prepare | config, container rules, `validate_context(execute=False)` | nothing | 2 |
| S1 | pin check | `app/clerk-seam.json`, then hash `clerk.py` | nothing | 2, before any subprocess |
| S2 | link | link file: strict, exact keys, plain file with one link; delivery = file name = bridge job; job sha equal; `clerk_store` absolute, inside the container, outside `--root` | nothing | 2 |
| S3 | bridge job | `worker_bridge._load_job`; `job_id == clerk_job_id` | nothing | 2 |
| S4 | Clerk state | `clerk.py show` → queued: stop "claim first"; bad/incomplete: stop; claimed: continue at S5. Returned: if the recorded delivery is not the link's, stop "conflicting delivery". If it is, replay: the token comes from show's `claim` line (clerk.py:960), S5 and S6 are skipped, S7 is status only, and S11 must report `already-recorded` | nothing | 2 |
| S5 | claim | `clerk.py claim --resume --as A`: token and `instructions-usable sha256=X`. Clerk checks assignee and instruction hash; writes nothing | nothing | 2 |
| S6 | instruction identity | X == bridge job inputs[0].sha256 == sha of `bridge/declared/task.md` | nothing | 2 |
| S7 | one delivery | no provenance/store for d: `perform("bridge-test")` (execute=True; the one launch). Otherwise `perform("bridge-status")` (no launch) | bridge writes only | bridge code 2/3/4 passed through |
| S8 | receipt | receipt via the accepted 0504/05.06 validator: delivery, job_id, request_sha = provenance; transport `delivered`, collection `collected`, outcome `done`; every artifact name a simple filename | nothing | 3 or 4 |
| S9 | source artifact | `bridge/delivery/d/output/<name>`: plain, one link, sha and bytes = receipt | nothing | 2 if nothing was written on this call, otherwise 4 |
| S10 | copy | outbox/<name> absent: exclusive create, fsync, re-read and compare. Present and identical: skip. Present and different: stop | outbox/<name> | 4 (human) |
| S11 | Clerk return | `clerk.py return --delivery d --evidence E` → `returned` or `already-recorded` | Clerk's own events | 4 if refused after a copy |
| S12 | report | print the lines below | nothing | 0 |

Evidence E is deterministic, so a repeat gives an identical return:

```text
bridge delivery bridge-0001 request <request_sha256> receipt <receipt.json sha256> artifact result.json <sha256> source bridge/delivery/bridge-0001/output/result.json
```

Report on success:

```text
clerk_job: clerk-0001
delivery_id: bridge-0001
transport: delivered
collection: collected
artifact: result.json sha256 0c07187e… copied to clerk outbox
clerk: returned            (or: already-recorded)
reviewer: codex-prime (inbox projection; not invoked)
review: not performed
acceptance: not performed
```

**Exit codes:**
- 0: returned, or already recorded.
- 2: refused; this call wrote nothing.
- 3: delivered but not collected, or outcome `failed`. Nothing is copied and Clerk is unchanged.
- 4: uncertain. Either the bridge result is uncertain, or the stores are left in a mixed state, with the diagnostic naming what this call wrote.

## 5. Sequence: who writes each file, and what permits it

| # | Actor and process | File | Permitted by |
|---|---|---|---|
| 1 | router fixture (intelligence's stand-in) | `router/*`, `fixture/bridge/job.json`, `bridge/declared/task.md`, `clerk-link/bridge-0001.json`, fixture record | the Director's release of the slice; the fixture record is synthetic |
| 2 | `clerk.py queue` | `clerk-store/jobs/clerk-0001/0001.queued.json` | the router's job file (Clerk checks schema and instruction hash) |
| 3 | `clerk.py claim --as fixture-worker` (explicit, separate) | `0002.claimed.json`, `outbox/` | recorded assignee only (Clerk) |
| 4 | `librarian clerk-deliver` → bridge | provenance, delivery dirs, store/request, launch, attempt, receipt | `released` fixture record, `work_ref == current_work`, allowlisted backend, pinned lab |
| 5 | worker process (fixture-ok) | `output/result.json`, `output/launches.log` | its own `output_root` only |
| 6 | `clerk-deliver` | `outbox/result.json` | a valid claim (resume), a collected receipt, an artifact equal to the receipt |
| 7 | `clerk.py return` (run by the seam as the assignee label) | `0003.returned.json` (+ 05.02 witness) | the claim token and the outbox matching expected_outputs (Clerk) |
| 8 | `clerk.py inbox --as codex-prime` | nothing | the projection; the reviewer is not invoked |

## 6. One owner per fact

| Fact | Owner (single editable source) | Copies, and how they are checked |
|---|---|---|
| route, assignee, reviewer, expected outputs, release text | Clerk `0001` (router's job) | none. The link deliberately repeats none of them |
| claim, token | Clerk `0002` | the seam reads them via resume and never stores them |
| instruction identity | Clerk `0001` instructions.sha256 | bridge job inputs[0] and `bridge/declared/task.md`: checked equal at S6 |
| job ↔ delivery association | link file (router, immutable) | the bridge job's `job_id` must equal `clerk_job_id` |
| work_ref, role, backend, limits, delivery_id | bridge job (router) | provenance and request (bridge-owned, hash-correlated) |
| request identity | bridge provenance/request | the receipt repeats it; checked at S8 |
| verified artifact | bridge receipt | the outbox copy. Clerk hashes it at return; it must equal the receipt; E names both |
| returned / review-available | Clerk `0003` (+ witness) | the inbox is a projection |

There is no seam ledger, no seam state file, and no second job record. The seam's only durable write is the outbox copy, and Clerk itself turns that into a record.

## 7. Interruption and replay across the two stores

There is no cross-store transaction. Every state below is visible from its owner, and a repeat reads before it writes.

| Boundary reached, then interrupted | What a repeat reads | What a repeat may write | Outcome |
|---|---|---|---|
| B1. claim recorded, seam never ran (or died before S7) | Clerk claimed; no provenance or store | the one new delivery | proceeds; the first launch |
| B1a. claim event without outbox (Clerk incomplete) | Clerk `bad state: incomplete` | nothing | 2; human. Clerk has no repair; a new job id in a new store |
| B2. `launch.json`, no receipt (uncertain) | bridge status `uncertain` | nothing | 4; no relaunch. A human chooses `bridge-recover` (no launch, needs a fully recorded attempt) or a new delivery (a new bridge job and a new link, `bridge-0002`). The old evidence stays |
| B3. receipt complete, copy not made | Clerk claimed; receipt collected | outbox copy, then return | completes with no launch (status path) |
| B4. copy made, Clerk return not made | outbox file equal to the receipt | Clerk return | completes; copy skipped |
| B4a. outbox file present but different | outbox ≠ receipt | nothing | 4; human. Never overwritten or deleted |
| B5. Clerk return complete, caller saw no success | Clerk returned with delivery = link | nothing (Clerk `already-recorded`) | 0; no new event, no new time |
| B5a. partial Clerk return or witness mismatch (05.02) | Clerk incomplete or corrupt | nothing | 4; human. The reviewer never sees success |

**Named failures:**

| Case | Where it is caught | Outcome |
|---|---|---|
| artifact bytes changed in the bridge output after the receipt | S9 | 2 or 4; no copy |
| outbox copy changed before return | S10 (re-read) and S11 (Clerk hashes it) | 4; no return |
| outbox copy changed after return | Clerk inbox/verify: `artifact changed`, `not-returned-clean` | Clerk's finding, exit 1 |
| missing completion marker: no receipt | S7 status `uncertain` | 4 |
| missing completion marker: no Clerk witness (05.02) | S4 | 4 |
| bad receipt correlation (BRI-01 shape: ids swapped, request hash missing) | S8, via the 0504/05.06 validator | 2/4; no copy, no launch |
| wrong claim: `--as` is not the assignee; job queued, not claimed; link names another job | S4, S5 (Clerk refuses), S3 | 2; nothing written |
| stale instruction hash before delivery | S5 (Clerk resume) or S6 | 2; nothing written |
| stale instruction hash after delivery, at return time | S5 on the repeat | 4; delivered and not returned. Human: a new Clerk job, or restore the instruction bytes |
| conflicting delivery: Clerk returned under another delivery | S4 | 2; before any launch |
| conflicting delivery: bridge id reused with a different job | S7 (bridge refusal) | 2 |
| two seam calls at once | bridge `launch.json` exclusive; outbox exclusive create; Clerk exclusive events | one completes; the other stops 2 or 4 and can be repeated |

**Human boundaries:**
- an uncertain launch;
- a differing outbox copy;
- an incomplete Clerk record;
- instructions changed after delivery;
- an uncollected or failed result.

At each one the seam stops, keeps every byte, and names the boundary. It never finishes, resets or relaunches anything.

## 8. Built, proposed, blocked

| Item | Status |
|---|---|
| Clerk CLI: queue, claim, resume, return, inbox, show, verify | built (pass02); correction 0506/05.02 pending |
| bridge `perform`: bridge-test, status, recover; provenance; per-delivery dirs; receipt | built (0504/05.05); BRI-01 correction 0504/05.06 pending |
| container rules, `validate_context`, `resolve_under`, `guard_workspace_path` | built (accepted APP-01) |
| `clerk-deliver`, `app/clerk_seam.py`, `app/clerk-seam.json`, `librarian-clerk-link` v1, evidence format E, seam exit codes | proposed here |
| optional Clerk `--json` output, to replace line parsing | named proposal only, not required: the seam parses Clerk's `token`, `state`, `claim`, `instructions-usable sha256=` and `result` lines. Whether `show` still prints `claim <token>` after 05.02 must be checked against the accepted clerk.py; if it does not, the replay path needs that line or this proposal |
| trust in stored receipts | **blocked** on 0504/05.06 acceptance and its validator's interface |
| pinned clerk.py hash; no clean re-return after tail loss; Clerk OSError → exit 2; nonblank evidence | **blocked** on 0506/05.02 acceptance |

## 9. Recommended next slice (ONE)

**Name:** "clerk-deliver, fixture only". Start it only after Prime accepts both 0504/05.06 and 0506/05.02.

**Owner:** the app's builder. All new code is in `app/`. Clerk and the bridge lab are not edited.

**Files:**
- `app/clerk_seam.py`, new;
- `app/clerk-seam.json`, new; pins the accepted clerk.py;
- `app/librarian.py`, one more dispatch branch;
- `app/tests/test_clerk_seam.py`, new;
- `app/README.md`, a section.

No change to `context.py`, `worker_bridge.py` (it is called, not edited), `clerk.py`, the bridge lab, kernel pages, or shared records.

**Contracts:**
- Python standard library only.
- `clerk.py` is run as `sys.executable -B <pinned path>` after the hash matches. The same-user gap between that check and the launch is stated.
- The bridge pins in `app/worker-bridge.json` stay unchanged.
- The receipt validator is the 05.06 helper, called and not re-implemented.
- Clerk store format: the version that 05.02 stamps.

**Demonstration** (separate processes, in an external `%TEMP%` container):
1. The router fixture writes the files in §3.
2. `clerk queue`.
3. `clerk claim`.
4. `clerk-deliver`, exit 0.
5. `clerk inbox --as codex-prime` lists `clerk-0001` with result.json `0c07187e…`. The assignee and another label do not get it to review.
6. A fresh `clerk verify` exits 0.
7. `bridge-status` gives the same receipt hash.
8. A second `clerk-deliver`: exit 0, `already-recorded`. `launches.log` still has one line, and the Clerk event set and all bytes are unchanged.

**Acceptance tests.** Each also asserts no traceback, no write outside the container, no relaunch (a `launches.log` line count), and an unchanged Clerk event set wherever the outcome is a refusal:
- **A1:** success path and demonstration.
- **A2 to A6:** B1 to B5 above, using in-process crash points like the bridge's `crash_before_receipt` (no CLI flags):
  - B1: a first run after the claim;
  - B2: uncertain, then `bridge-recover`, then a repeat that completes without a launch;
  - B3: a crash before the copy;
  - B4: a crash before the Clerk return;
  - B5: a crash before the report.
- **A7:** a different outbox copy, and a changed bridge output.
- **A8:** the BRI-01 receipt mutation is refused.
- **A9:** a wrong `--as`, an unclaimed job, a link job mismatch, a link Clerk store outside the container, a missing link.
- **A10:** a stale instruction before and after delivery.
- **A11:** conflicting deliveries in both stores.
- **A12:** placement. A fixture in `app/scratch` with its store beside it is refused through Clerk's Git rule. An unknown flag is refused. There is no override.
- **A13:** uncollected, failed, timeout and crash map to 3/4, with nothing copied and nothing in the reviewer's inbox.
- **A14:** a clerk.py pin mismatch stops before any subprocess.
- **A15:** two concurrent `clerk-deliver` runs: one launch, one return.

**Not in the slice:** a real model, a scheduler, invoking the reviewer, acceptance or closure, routing choices, a cross-store transaction or exactly-once claim, activation, or Clerk or bridge edits.

## 10. Decision with scope effect (one)

Q01. Should a delivered-but-uncollected or `failed` worker result become a Clerk return for the reviewer to see?
- This design says no: the seam stops (exit 3), keeps the evidence, and a human decides.
- A yes would mean the reviewer's inbox holds non-success returns under the same three states. That needs a Clerk evidence convention and a Prime/Director decision.
- Everything else here is a routine choice, carried as a recommendation.
