# Worker bridge contract, lab pass 01

**state:** design written before implementation (batch `0503.worker-bridge/05.01` #01), then read back against the code; see "Read-back" at the end. Lab contract, not kernel law, not an app commitment.
**before implementation:** `evidence/CONTRACT.before-implementation.md`, sha256 c3a6ee8b1a0615ee6b1057d28bbdd8f087c67ab743a3d7e81e01e1c715bf4e06
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
| `schema` | `worker-bridge/request@1` |
| `delivery_id` | identity of this delivery; unique per attempt-at-work. It becomes a folder name, so it follows the identifier rules in "Delivery identity" below (pass 02). |
| `job_id` | the job the delivery belongs to |
| `role` | the intended role (`builder`, `colab`, …), as data only |
| `work_ref` | reference to the work item, for example `00.kernel/00.00.10.work/0503.worker-bridge/05.01.md#02` |
| `inputs` | list of `{name, path, sha256, bytes}`. Paths are relative to the declared input root. |
| `input_root` | the folder the worker may read |
| `output_root` | the folder the worker may write; artifacts must land inside it |
| `limits` | `{timeout_s, max_stdout_bytes, max_stderr_bytes}`, the only keys. `timeout_s` is an int or float, not a bool, finite, with 0 < t ≤ 3600. Each byte cap is an int, not a bool, with 1 ≤ n ≤ 67108864 (64 MiB). Anything else is refused before launch (pass 02). |
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
| `incomplete-output` | the direct child exited, but its output streams were still open when the budget ended (a descendant may hold them). The captured bytes are a partial snapshot, kept as diagnostics and never parsed. **Outcome uncertain** (pass 03). |
| `malformed` | the result is not valid JSON or has the wrong shape |
| `uncollected` | the result is valid but its artifacts are missing, wrong, or outside the root |
| `collected` | the result is valid and every artifact verified |

## Local-process implementation

- Launch with an argv list (no shell), the request on stdin as JSON, stdout as the single result JSON, and stderr as diagnostics.
- **One deadline** (`t0 + timeout_s`) covers writing stdin, reading stdout and stderr to EOF, and the child's exit. Each stream has exactly one owner thread, which is the only code that reads, writes or closes it (pass 03). On overrun, or when a cap is exceeded, the direct child is killed. Then at most `CLEANUP_ALLOWANCE_S` (2.0 s) more is spent reaping it and letting the threads finish, and after that `deliver()` **returns**. The adapter never closes, joins or waits on a stream that a thread still owns. Pass 02 did, and a descendant holding the pipe blocked the return for 5.078 s (BR-01b). A thread still running is named in `cleanup.retained`. It keeps draining its pipe, and closes it itself when the other end closes, or when the interpreter exits (it is a daemon thread). The captured bytes are frozen at the return, and later bytes are dropped, never added to a result. Observed bound: about `timeout_s` + 2.0 s plus process start-up (2.219 s at a 0.2 s timeout with a descendant holding both pipes). This is a best effort for the adapter's return, not a real-time guarantee, and not a bound on the descendant's lifetime.
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
| `schema` | `worker-bridge/result@1` |
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

## Delivery identity and store containment (pass 02)

Every entry point (`deliver`, `status`, `recover`, and the CLI through them) gets its per-delivery folder from one function, `bridge/ids.py:store_dir`. It applies the identifier rules before any file is touched, then checks that the folder is not a link or reparse point and that it resolves directly inside the store. A refusal is a normal result with `transport: refused`, never an outside read or write, and never an uncaught path error.

**Identifier rules** (Windows-safe, because the id is a folder name):
- 1 to 64 characters: lowercase ASCII letters, digits, `.`, `_` and `-`;
- a letter or digit at both ends, so no leading dot and no trailing dot or space (Windows drops those);
- no `..`;
- the part before the first `.` is not a reserved device name (`con`, `prn`, `aux`, `nul`, `com1`–`com9`, `lpt1`–`lpt9`).

Lowercase only, so two ids can never name the same folder on a case-insensitive file system. This is containment, not authentication.

## Strict JSON (pass 02)

Messages (requests read by the CLI, worker results, and the adapter's own stored records) are parsed by `canon.strict_loads`. It refuses `NaN`, `Infinity`, `-Infinity` and duplicate keys, which Python's `json` module otherwise accepts silently: a duplicate key would keep the last value. `canonical()` refuses to encode NaN or Infinity.

## Confinement limits (stated, not solved)

The worker is a same-user subprocess. Path checks on the result prove where the artifacts **are**, not what the process could touch. It can read and write anything the user can. There is no OS sandbox, no network control, and no process-tree kill on Windows: only the direct child is killed. Real model workers must bring their own confinement (for example `claude --restricted`, or `grok --sandbox`), and that is outside this lab.

## Not in this pass

Clerk routing and state, entry and context validation, scheduling or waking workers, concurrency beyond exclusive launch creation, authentication, and any real model invocation.

## Read-back after implementation (what changed, and why)

| # | Change | Why |
|---|---|---|
| R1 | Schema values became `worker-bridge/request@1`, `worker-bridge/result@1` and `worker-bridge/receipt@1`. | A single exact string is simpler to check than a name plus a version. |
| R2 | Added `recover(delivery_id)`. If the attempt was fully recorded (`launch.json`, `attempt/exit.json`, stdout and stderr) but the receipt is missing, it rebuilds the receipt from those records, marks it `recovered`, and never relaunches. If the attempt wasn't fully recorded, the state stays `uncertain`, and only a new `delivery_id` from the supplier moves on. | The design said only "recovery takes a new delivery_id". That would throw away a finished, verifiable result whenever just the receipt write was interrupted. |
| R3 | A repeated identical request returns the stored receipt with `replayed: true`. | Makes "applied once" visible to the caller. |
| R4 | The worker's working directory is its `output_root`. | Relative writes land in the declared output root by default. That is still not confinement. |
| R5 | The adapter closes the parent's stdout and stderr pipe handles after the readers finish. | Test run 01 showed `ResourceWarning: unclosed file` on every launch (`evidence/tests/run-01.txt`). Runs 02 and 03 are clean. |
| R6 | The protocol test worker appends each launch to `launches.log` in its output root. | Lets the tests count real launches, which is how "not relaunched" and "applied once" are proved. This is a test aid, not part of the protocol. |
| R7 | An existing `launch.json` from someone else (exclusive create failed, or found before launch) is reported `uncertain`, not relaunched. | Basic protection against two launchers on one filesystem. It is not a lock manager. |

Unchanged from the design: the envelope fields, the result fields, the error kinds, the receipt's separate transport, outcome, collection and review statements, and the confinement limits.

## Pass 02 corrections (Prime review of 05.01: BR-01, BR-02, BR-03)

| # | Change | Why |
|---|---|---|
| R8 | The stdin write moved into its own thread under the single deadline, with a documented 2.0 s cleanup allowance and a `cleanup` record in `exit.json` and the receipt. | BR-01: the synchronous `proc.stdin.write` ran before the timeout loop; a child that never read stdin held the adapter about 3.05 s against a 0.2 s timeout. |
| R9 | `bridge/ids.py`: one identity and containment check for every entry; stricter delivery-id rules (lowercase, no trailing dot, no reserved names). | BR-02: `status` and `recover` joined an unchecked id to the store and read `../outside/receipt.json`. |
| R10 | `check_limits`: finite, typed, bounded limits; lab ceilings of 3600 s and 64 MiB. | BR-03: infinity, fractional byte caps and bools were accepted. |
| R11 | Strict JSON for messages; canonical encoding refuses NaN and Infinity. | Nonstandard numbers or duplicate keys could hide a bad limit, or change a result's meaning. |
| R12 | New protocol test workers: `no-stdin-reader` (self-terminates after 10 s), `flood-stderr`, `dup-keys`. | Regression fixtures for R8 and R11, and the stderr cap. |

Pass 01's statement "Time is limited, and the child is killed on overrun" was overbroad: it did not cover stdin. It is replaced above.

## Pass 03 correction (Prime review of 05.02: BR-01b)

| # | Change | Why |
|---|---|---|
| R13 | Stream ownership: unbuffered pipes (`bufsize=0`); one owner thread per stream that reads or writes and then closes it; a capture object frozen by `snapshot()` at the return; `cleanup.retained` names any thread still running; the adapter never closes a stream after the joins. | BR-01b: after the bounded joins, pass 02 called `close()` on buffered streams whose reader threads were blocked inside `read()` holding the stream lock. With a descendant holding both pipes, `deliver()` returned only when it exited (5.078 s at timeout 0.2 s plus allowance 2.0 s). |
| R14 | New transport kind `incomplete-output`: the child exited, but its output was not at EOF within the budget. It is never parsed, even if a complete result had already been written. | Late or partial output must not become a verified result after the deadline. |
| R15 | Normal completion now also waits, within the deadline, for both streams to reach EOF. | So "delivered" means the output was complete, not only that the child had exited. |

Pass 02's line "it can keep a reader thread alive past the allowance, and that is recorded" was true about the thread, but it hid that the adapter itself also waited. It is replaced above.
