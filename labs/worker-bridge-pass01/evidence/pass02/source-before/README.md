# Worker bridge, lab pass 01

**batch:** `00.kernel/00.00.10.work/0503.worker-bridge/05.01.md` (released by the Director, 2026-10-26)
**who:** claude-opus-5-5, Colab · **state:** lab experiment. Not runtime, not Clerk, no real model.

## What it is

A small transport boundary. One recorded request goes to one allowlisted worker process, and the adapter collects a correlated, hash-verified result plus a durable receipt. The only backend is a local process, and every configured profile is a **protocol test worker** (`fixtures/worker_fixture.py`), not a model.

| File | Holds |
|---|---|
| `docs/CONTRACT.md` | envelope, adapter, local-process backend, verifier, receipt; and the read-back of what changed |
| `docs/INVENTORY.md` | the model connections on this machine, and the next real exchange |
| `bridge/` | `envelope.py`, `adapter.py` (interface and `LocalProcessAdapter`, with `recover`), `verify.py`, `canon.py`, `cli.py` |
| `profiles.json` | the allowlist: exact argv per profile, all test workers |
| `fixtures/worker_fixture.py` | the protocol test worker; behaviour chosen only by its profile's `--mode` |
| `tests/test_bridge.py` | 18 tests |
| `run_demo.py` | the demonstration |
| `evidence/` | test runs, the demonstration, the inventory, the contract before implementation, hashes |
| `scratch/` | test runs; ignored by the lab's `.gitignore` |

## Run

From this folder, with the machine's Python 3.14, standard library only:

```text
python -B tests/test_bridge.py -v
python -B -X dev tests/test_bridge.py
python -B run_demo.py evidence/demo-<new-name>
python -B -m bridge.cli status --store evidence/demo-run-01/store --delivery demo-0001
```

## Limits

- **No sandbox.** The worker is a same-user subprocess. Path checks prove where the artifacts are, not what the process could touch.
- **Process cleanup:** only the direct child is killed on a timeout. Grandchildren are not (there are no Windows job objects).
- **Concurrency:** one launcher per delivery, through an exclusive-create `launch.json`. Nothing more is supported.
- **Authentication:** none. The `release` field is evidence, not authority.
- **The receipts are lab transport evidence,** not a ledger.
- **The demo's request names absolute folders** under this lab.
