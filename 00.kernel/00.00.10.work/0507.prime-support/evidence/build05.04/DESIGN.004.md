# DESIGN.004 — registered Clerk returns (0507.prime-support 05.04)

Author: claude-opus-5-5. Date: 2026-10-27.
Additive to DESIGN.002 and DESIGN.003, which stay as they are. Every field is a provisional fixture contract, not kernel law. The scope is **registered jobs only**: there is no inbox discovery.

## 1. Registry version 2

Version 1 is unchanged and still accepted. Version 2 adds two things.

**Top level, required when any lane has `clerk_jobs`:**

```json
"clerk_tool": {"path": "<absolute path to clerk.py>", "sha256": "f697a7e443117c3d1face62d3021f7634154d76214b77fadec1a5cc3c99d394c"}
```

**Per lane, optional:**

```json
"clerk_jobs": [{"store": "<absolute>", "job_id": "<id>", "instructions_base": "<absolute>", "reviewer": "<label>"}]
```

The rules:
- Exact keys apply.
- Paths must be absolute.
- `job_id` and `reviewer` follow Clerk's id rule.
- A (store, job_id) pair may be registered at most once.
- A version-1 registry using `clerk_tool` or `clerk_jobs` is refused.

## 2. One accepted reader

The adapter's constant `ACCEPTED_CLERK_SHA256` is the accepted inspection/2 code.
- The registry's `clerk_tool.sha256` must equal it.
- The file at `clerk_tool.path` must be a regular file, not a link, that hashes to it at the moment of use. Otherwise nothing is executed, and the job reports `unsupported: tool identity`.

The only command run is:

```text
<sys.executable> -I -B <clerk_tool.path> show --store <store> --job <job_id> --instructions-base <instructions_base> --json
```

It runs with no shell, cwd set to the system temp directory, and a 60-second timeout.

The adapter never opens a store file, never lists a store directory, and never parses human output.

## 3. Strict projection parse (inspection/2)

The adapter requires:
- stdout is one strict JSON object (no duplicate keys, no NaN), and stderr is empty;
- the keys are exactly `schema, job_id, state, job, claim, returned, checks, problems`, with `schema` equal to `clerk-handoff-inspection/2`;
- `job_id` is the registered one;
- `state` ∈ {queued, claimed, returned, incomplete, corrupt, unknown};
- `checks` has exactly its four keys, each with an enum value from the Clerk README;
- `problems` is a list of objects, each with string `kind` and `detail`;
- `job`, `claim` and `returned` are non-null exactly as the state requires;
- `returned`, when present, has exactly `by, delivery, evidence, artifacts, event_sha256`, and `event_sha256` is 64 hex;
- the exit code agrees with `problems`: 0 has none, 1 has only artifact-changed or instructions-unusable, 2 is a nonclean state.

Any violation is `unsupported: <reason>`, kept with the raw exit code. It is never a success.

## 4. Identity, binding, cleanliness

- **Binding:** `job.job_id == job_id` and `job.reviewer == reviewer` (registered). A mismatch is a `conflict`, and the return is unusable.
- **Identity:** `(store normcase-realpath, job_id, returned.event_sha256)`. It exists only for state `returned` with `checks.events` and `checks.completion` both `ok` and the binding valid. Queued, claimed, incomplete, corrupt and unknown never have one.
- **Clean** additionally requires `artifacts ok`, `instructions usable`, empty problems and exit 0.
- **Review:** `not-machine-readable`. Nothing is inferred.
- **Context packet:** `clerk:<store>#<job_id>@<event_sha256>` plus the tool sha, `show --json`, the exit code, and the full `checks` and `problems`.

## 5. Intake records (`prime-intake/2`)

- **Subject:** `{"kind": "clerk-return", "store", "job_id", "event_sha256"}`.
- **Observed:** `{"tool_sha256", "exit", "state", "checks", "problems"}`, exactly as projected at the acknowledgement.
- **Other keys** are as in `/1`: schema, subject_id, supersedes (null), by, at, note.
- **Path:** `subjects/<id12>/0001.seen.json`. `/1` records are read as before.

**`intake ack-clerk --registry R --intake S --lane L --store STORE --job J --event-sha256 H --as LABEL`:**
- refuses an abbreviated `H`;
- inspects freshly;
- requires an identity equal to `H`, refusing a stale one;
- writes one exclusive record;
- is idempotent for the same label, and refuses a different label.

The intake store must be absolute, outside Git, and outside every registered Clerk store.

## 6. Attention

- `unseen`: an identity with no acknowledgement.
- `review-needed`: seen; review is not machine-readable.
- `clerk-not-clean`: an identity that is not clean. This stays after the acknowledgement.
- `conflict`: a binding mismatch.
- `unsupported`: the tool or the projection.
- `missing`: state unknown.

A queued or claimed job is listed as information, and is not an attention item.
