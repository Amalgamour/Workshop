# CONTRACT — clerk-deliver, fixture only

Batch: `0504.app-entry/05.10`. This file is the implementation contract written before `app/clerk_seam.py`. It maps the accepted SEAM to the pinned Clerk inspection and to Prime's two requirements. It is not kernel law.

## Components used, and only these

| Need | Accepted component | How this command uses it |
|---|---|---|
| Desk, container, path guards | `app/context.py` | `select_container`, `validate_context(execute=False)` at prepare, `resolve_under`, `guard_workspace_path`, `is_inside` |
| One worker delivery | `app/worker_bridge.py` `perform` | `bridge-test` only when no provenance and no store exist; otherwise `bridge-status` |
| Stored receipt identity | `worker_bridge._require_stored_receipt` via `_read_stored_receipt` | Called for a collected receipt. Not reimplemented |
| Clerk queue, claim, return, inbox, verify, show | `labs/clerk-handoff-pass02/clerk.py` sha256 `f697a7e443117c3d1face62d3021f7634154d76214b77fadec1a5cc3c99d394c` | Subprocess of `sys.executable -B` after the pin matches |
| Inspection | `show --json`, schema `clerk-handoff-inspection/2` | Job, checks, claim, recorded return, problems |
| Unfinished-claim token | public `claim --resume` | Only while inspection state is `claimed` |

No second Clerk, worker bridge, receipt validator, queue, router, intake registry, or seam ledger. The router link is the association record. The seam reads it and does not rewrite it.

## Prime requirements carried from 0506/05.03

1. Structured inspection is required. `show --json` supplies job, checks, claim, and recorded return. The seam does not read raw event files and does not parse human inbox text as a ledger.
2. On every existing-delivery path, including a returned-job replay, `link.bridge_job_sha256` must equal the original provenance `job_sha256`, and the current bridge-job bytes must equal that digest. The check happens before copy and before Clerk return. Actor, instruction usability, and stored job identity are checked on that replay too.

Uncollected, failed, and uncertain worker outcomes do not become a normal Clerk return. The seam stops, retains the claim and the bridge evidence, and names the attention target.

## Public claim-resume contract

`claim --resume` writes nothing. It succeeds only for a complete unfinished claim. Its stdout contract, before Clerk's trailing `result ok` label, is exactly:

```text
resume <job_id>
token <32 lowercase hex>
instructions-usable sha256=<64 lowercase hex>
```

The token must equal inspection `claim.token`. The hash must equal the Clerk job's instruction sha256. A returned job makes resume refuse (`resume requires a complete claim`). The returned replay therefore uses inspection `claim.token` and does not call resume. That limitation is Clerk's public contract, recorded here so the replay does not invent a second token store.

## Command

```text
python <workspace>/app/librarian.py clerk-deliver --root <fixture> --link <link-relative> --as <actor> --instructions-base <dir> [--container <external-container>]
```

There is no crash flag, no reviewer flag, no route flag, and no override flag. Hooks `before-launch`, `before-copy`, `before-return`, and `before-report` exist only as the `interrupt` argument of `clerk_seam.perform`.

## Pin

`app/clerk-seam.json`, schema `librarian-clerk-seam`, version 1, exact keys `schema`, `version`, `clerk_path`, `clerk_sha256`. The path is relative to the code root. The file is hashed before any Clerk subprocess. A mismatch stops with exit 2 and starts no subprocess. The same-user gap between that read and the subprocess is not closed.

## Link

Schema `librarian-clerk-link`, version 1, exact keys `schema`, `version`, `delivery_id`, `clerk_store`, `clerk_job_id`, `bridge_job`, `bridge_job_sha256`. The file name stem is the delivery id. The bridge job file's bytes hash to `bridge_job_sha256`. `clerk_store` is an absolute plain directory inside the designated container, neither inside the fixture root nor containing it. The link holds no assignee, reviewer, state, token, or authority.

## Steps

| Step | Reads | May write | Stop |
|---|---|---|---|
| S0 | config, container, `validate_context(execute=False)` | nothing | 2 |
| S1 | `clerk-seam.json` and the Clerk file hash | nothing | 2, before any Clerk subprocess |
| S2 | link file | nothing | 2 |
| S3 | bridge job through `worker_bridge._load_job`; `job_id` equals `clerk_job_id` | nothing | 2 |
| S4 | `show --json` | nothing | queued: 2 `claim first`. Incomplete claim: 2. Damaged completion: 4. Returned under another delivery: 2 `conflicting delivery` |
| S5 | actor equals inspection assignee and `claim.by`. Claimed jobs also call `claim --resume` | nothing | wrong actor: 2. Stale instructions before a delivery: 2. Stale instructions after a delivery: 4 |
| S6 | instruction sha256 equals bridge `inputs[0]` and `bridge/declared/<path>` | nothing | same as S5 |
| S7 | no provenance and no store: `perform("bridge-test")`, one launch. Otherwise bind the link hash to provenance, then `perform("bridge-status")`, no launch | bridge only | bridge 3 and 4 pass through. Binding failure: 2, before copy and before Clerk return |
| S8 | stored receipt through the accepted validator; transport `delivered`, collection `collected`, claimed outcome `done`; artifact names are single path segments | nothing | uncollected or `failed`: 3. Uncertain: 4. Validator refusal: 2, evidence kept |
| S9 | output bytes equal the receipt | nothing | 4 when a delivery exists and the bytes differ. No copy |
| S10 | outbox file absent: exclusive create, fsync, re-read. Identical: skip. Different, linked, or extra name: stop | `outbox/<name>` only | 4. Never overwrite or delete |
| S11 | `clerk.py return` with the deterministic evidence line | Clerk's own events | 4 if Clerk refuses after a copy. `returned` or `already-recorded` continues |
| S12 | print the success lines | nothing | 0 |

Evidence, one line, deterministic:

```text
bridge delivery <delivery_id> request <request_sha256> receipt <receipt.json sha256> artifact <name> <sha256> source bridge/delivery/<delivery_id>/output/<name>
```

Success report:

```text
clerk_job: <id>
delivery_id: <id>
transport: delivered
collection: collected
artifact: <name> sha256 <sha256> copied to clerk outbox
clerk: returned
reviewer: <reviewer> (inbox projection; not invoked)
review: not performed
acceptance: not performed
```

`copied to clerk outbox` becomes `already in clerk outbox` when this call did not write the file. `clerk: already-recorded` is the completed replay. Exit 0 is only those two Clerk results.

## File ownership

| Fact | Owner | What the seam does |
|---|---|---|
| Route, assignee, reviewer, expected outputs | Clerk queued job | Reads them from inspection. Does not choose them |
| Claim and token | Clerk claimed event | Reads inspection. Resume reads the token while the claim is unfinished. The seam does not store a token |
| Instruction bytes | Clerk instructions base, checked by Clerk | Compares that sha256 with the bridge input and the declared copy |
| Job-to-delivery association | Router link | Reads it. Requires its job hash to equal original provenance on existing deliveries |
| Request, provenance, worker output | Bridge | `perform` only. The worker's output directory stays `bridge/delivery/<id>/output` |
| Verified outbox bytes | Seam copy of receipt artifacts | Exclusive copy of those names only. `launches.log` is not an artifact and is not copied |
| Returned record | Clerk | `return` only. Inbox is a later projection. The seam does not invoke the reviewer |

## Interruption

| Hook | Leaves | Repeat |
|---|---|---|
| `before-launch` | claim, no delivery | the one launch |
| `before-copy` | receipt collected, outbox without the artifact | status, copy, return, no launch |
| `before-return` | outbox bytes equal the receipt, no Clerk return | return, copy skipped, no launch |
| `before-report` | Clerk return already recorded | `already-recorded`, no launch, no new event |

Each hook returns exit 4 and names the boundary. It does not raise a traceback, delete evidence, or launch. Two overlapping calls have no seam lock. Bridge exclusive create, outbox exclusive create, and Clerk exclusive events are the serialization. One can finish. The other stops at 2 or 4 and can be repeated. A repeat of a finished identical call launches nothing.

## Placement

One external `--container` holds `fixture/` and `clerk-store/` as siblings. The fixture root is `--root`. The worker never writes the Clerk outbox. A fixture placed in `app/scratch` with a store beside it is left for Clerk's own rule: the store resolves inside a Git working tree. This command adds no bypass.

## Exit codes

| Code | Meaning |
|---|---|
| 0 | `returned` or `already-recorded` |
| 2 | refused before this call's outbox copy and Clerk return. Stderr starts with `stop:`. Stdout is empty. Existing evidence stays |
| 3 | delivered but uncollected, or collected `failed`. Nothing copied. Clerk unchanged |
| 4 | uncertain, interrupted, stale instructions after a delivery, or a mixed outbox. Evidence stays. No relaunch and no automatic `bridge-recover` |

`run` is not activated. No model is called. A clean fixture result is not release readiness. These pins are development wiring, not kernel law.
