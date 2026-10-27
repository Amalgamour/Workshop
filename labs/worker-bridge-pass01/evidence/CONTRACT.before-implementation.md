# Worker bridge contract, lab pass 01

**state:** design written before implementation (batch `0503.worker-bridge/05.01` #01). Lab contract, not kernel law, not an app commitment.
**who:** claude-opus-5-5, Colab, 2026-10-26

## Boundary

```text
Clerk (not in this lab) ── validated, released request ──> Adapter ──> worker process
                                                              │            │ reads named inputs
                                                              │            │ writes artifacts in its output root
Clerk <── receipt (transport evidence) <── Verifier <── result ┘ <─────────┘ prints one result
```

**The Clerk** decides the route and supplies a released request. In this lab, a fixture producer stands in for it.

**The adapter** carries exactly one request to exactly one configured backend, and brings back a correlated result. It never invents a job, picks a recipient, retries on its own judgment, approves work, or changes book state.

**The verifier** checks the result against the request and against the bytes on disk. It reports, separately:
- whether transport succeeded;
- what the worker claims about the job;
- whether the artifacts were collected.

Review is a different seat's act, and the receipt always says `review: not performed`.

## Request envelope (`request.json`, UTF-8 JSON)

| Field | Meaning |
|---|---|
| `schema` | `worker-bridge/request` version 1 |
| `delivery_id` | identity of this delivery; unique per attempt-at-work |
| `job_id` | the job the delivery belongs to |
| `role` | the intended role (`builder`, `colab`, …), as data only |
| `work_ref` | reference to the work item, for example `00.kernel/00.00.10.work/0503.worker-bridge/05.01.md#02` |
| `inputs` | list of `{name, path, sha256, bytes}`. Paths are relative to the declared input root. |
| `input_root` | the folder the worker may read |
| `output_root` | the folder the worker may write; artifacts must land inside it |
| `limits` | `{timeout_s, max_stdout_bytes, max_stderr_bytes}` |
| `release` | `{by, ref}`, recorded as evidence of who released it. **Not proof of authorization:** authority comes from the supplying system's validated release, and the adapter does not trust a field that says `approved`. |
| `backend` | the name of a configured backend profile, never a command line |

`request_sha256` is the SHA-256 of the canonical JSON of the envelope (sorted keys, no spaces, UTF-8). It is the request's revision identity.

## Adapter interface

`deliver(envelope) -> receipt`, `status(delivery_id) -> receipt or state`.

**Inputs:** the envelope, and a backend profile from the adapter's own allowlist. A profile has a name, an exact executable and an exact argv, plus a working directory policy. Nothing from the request or the result is ever executed or appended to argv.

**Errors** are always recorded, never raised past the receipt store unless the store itself fails:

| Kind | When |
|---|---|
| `refused` | before launch: envelope invalid, input hash wrong, identity reused with a different request, unknown backend, ambiguous earlier attempt |
| `launch-failed` | the process could not start |
| `crashed` | non-zero exit |
| `timeout` | ran past the limit and was killed; **outcome uncertain** |
| `output-limit` | stdout or stderr went over its cap; killed; **outcome uncertain** |
| `malformed` | the result is not valid JSON or has the wrong shape |
| `uncollected` | the result is valid but its artifacts are missing, wrong, or outside the root |
| `collected` | the result is valid and every artifact verified |

## Local-process implementation

- Launch with an argv list (no shell), the request on stdin as JSON, stdout as the single result JSON, and stderr as diagnostics.
- Both streams are read concurrently and capped. Time is limited, and the child is killed on overrun.
- **Persistence, one folder per delivery:**

  ```text
  store/<delivery_id>/
    request.json      the envelope as given (bytes kept)
    launch.json       written with exclusive create BEFORE the process starts: request hash, profile, argv, time
    attempt/stdout.bin, attempt/stderr.bin, attempt/exit.json
    receipt.json      written last, atomically (temp file, then replace)
  ```

- **Idempotency:**
  - a receipt for the same delivery and the same request hash is returned as it is, and nothing is relaunched;
  - a different request under the same `delivery_id` is refused;
  - `launch.json` without a receipt means an earlier attempt's outcome is unknown. The adapter refuses to relaunch it automatically, and reports `uncertain` with the evidence. Recovery takes a new `delivery_id`, chosen by the supplier.

## Result (`stdout` of the worker, UTF-8 JSON)

| Field | Meaning |
|---|---|
| `schema` | `worker-bridge/result` version 1 |
| `delivery_id`, `job_id`, `request_sha256` | must equal the request's |
| `outcome` | the worker's claim: `done` or `failed` |
| `artifacts` | list of `{path, sha256, bytes}`, relative to `output_root` |
| `diagnostics` | free text, kept but never executed |

## Result verifier

Checks the shape and the identities. For each artifact, the path must stay inside `output_root` (no `..`, no drive, no reparse point on the way), the file must exist, and its length and SHA-256 must match. The verdict is `collected` or `uncollected`, with reasons. The worker's `outcome` is reported beside it, never instead of it.

## Receipt (`receipt.json`)

Holds:
- the identities: `delivery_id`, `job_id`, `request_sha256`;
- the backend profile name, and whether it is a **protocol test worker** or a **real model worker**;
- the transport status (the kinds above);
- the worker's claimed outcome;
- the collection verdict and its reasons;
- the verified artifacts;
- diagnostics paths with their hashes, exit code and duration;
- `review: not performed`.

It is lab transport evidence. It is not a production ledger, and not a second authority for the work's state.

## Confinement limits (stated, not solved)

The worker is a same-user subprocess. Path checks on the result prove where the artifacts **are**, not what the process could touch. It can read and write anything the user can. There is no OS sandbox, no network control, and no process-tree kill on Windows: only the direct child is killed. Real model workers must bring their own confinement (for example `claude --restricted`, or `grok --sandbox`), and that is outside this lab.

## Not in this pass

Clerk routing and state, entry and context validation, scheduling or waking workers, concurrency beyond exclusive launch creation, authentication, and any real model invocation.
