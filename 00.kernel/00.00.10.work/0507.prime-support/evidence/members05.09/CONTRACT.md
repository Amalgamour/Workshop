# CONTRACT — members05.09 (0507.prime-support 05.09), additive to build05.07 and repair05.08

Author: claude-opus-5-5. Date: 2026-10-27.
The earlier contracts stand unless this file changes them. The request schema `prime-boot-request/1`, the exit semantics, the replay rules, the caps and `authority: none` are unchanged.

## 1. Pins and launch

| Tool | sha256 | Located |
|---|---|---|
| return_inspect.py | 947915febaa5918f56b6be03c81840c030d081fcab9a3bead2cd660973a9999b | the sibling of `tools.return_capture` |
| return_capture.py | 8f3da5c651f6924fca6dedb0b95da7d181eb58884dc030dd9cbc3d8b6a5b15ac | `tools.return_capture`, which the inspector executes |

The other pins are unchanged.
- Stage 03 checks all five pinned files. Before each inspector launch, both the inspector and its sibling helper are re-checked. A mismatch fails the stage and never launches.
- The launch is `[sys.executable, "-I", "-B", <return_inspect.py>, "inspect", "--book", <members_book>, "--member", <name>, "--json"]`.
- No other command, no version discovery, and no inspector or helper code is copied.

## 2. Member observation (`08.members.json` → `members[]`, `prime-boot-member-observation/1`)

| key | value |
|---|---|
| `schema` | `prime-boot-member-observation/1` |
| `member` | the requested name |
| `members_book` | absolute |
| `source_kind` | `live-inspection` (the member directory now, through the pinned inspector; not a commit blob) |
| `observed_at` | UTC time just before the launch |
| `tool` | `{path, sha256}` of return_inspect.py |
| `argv`, `exit`, `stderr` | as run |
| `raw_file` | `08.member-NN.inspect.raw` (the exact stdout bytes; `10.` for re-observation) |
| `stdout_sha256`, `stdout_bytes` | of those bytes |
| `observation` | `ok`, or `failed` with `reason` (§3) |
| `status` | the inspector's status when `ok`, otherwise null |
| `problems`, `reservation`, `capture` | the inspector's projection, as returned, when `ok` |
| `identity` | `{status, reservation_sha256, submission_id, manifest_sha256, receipt_sha256, return_sha256, return_bytes}`; fields stay null unless the inspector returned them (capture fields only for `complete`) |
| `readiness` | `ready` (ok and complete) or `not-ready` |
| `remediation` | null, or one line naming what is required |
| `scope` | `capture custody only; review, acceptance and publication are not inferred either way` |

## 3. Interface checks (not a validator)

The observation is `failed`, not a stage failure, when any of these hold:
- stderr is not empty;
- stdout is not strict JSON, or is not an object;
- `schema` is not `return-capture-inspection/1`;
- `status` is not one of the five, or `exit` does not equal the documented exit for that status (complete 0, reserved 1, missing 1, incomplete 2, refused 2);
- `member` is not the requested name;
- `problems` is not a list of strings, or is empty and the status is not complete, or is non-empty and the status is complete;
- `reservation` is not an object or null;
- `capture` is not an object exactly when the status is complete;
- for complete, an identity field read here has the wrong type: `submission_id` is not a string, or a hash is not 64 hex, or `return.bytes` is not an integer.

Package integrity is never re-derived here.

## 4. Readiness

- Every requested member must be `ready`. Otherwise prepare is `partial`, with a reason per member in `19.prepare-outcome.json` `reasons` and the line in `remediation[]`.
- Since `oriented` needs a `prepared` prepare, a not-ready member can never be oriented.
- An empty `members` list is valid.

## 5. Packet

Refs come in this order:
1. the four required commit refs;
2. one `live-inspection` ref per member observation;
3. `packet[]`.

A member ref is `{id R.., kind: live-inspection, path: "member:<name>", member, members_book, observed_at, observation, status, sha256, bytes, text, raw_file, note}`. `text` is the exact UTF-8 stdout. It has no `commit` and no `live` field.
- A member ref counts one ref and its bytes against `max_refs` and `max_bytes`.
- An observation that doesn't fit, or whose stdout is empty or not UTF-8, gets an `omitted` record `{kind: live-inspection, member, sha256, bytes, raw_file, reason}`.
- The O1 scope is the status scope plus the `commit-blob` ref paths. Member refs are citable in O2 to O6, but are never a work target.

## 6. Stability

Stage 10 records `before` and `after` identities, including the tool hashes, as before.
- If every `after` tool hash still equals its pin, each member is inspected again into `10.member-NN.inspect.raw`. `members_after` records the identities, and any difference from stage 08 adds `members` to `changed`.
- If a tool hash changed, `members_reobserved` is false, and it says why.
- Two reads are two observations. No atomic snapshot, and no protection against a same-user swap between the reads, is claimed.
