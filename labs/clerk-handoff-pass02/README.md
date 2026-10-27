# Clerk handoff lab — pass 02

Lab ID: `clerk-handoff-pass02`  
Schema: `clerk-handoff-pass02/2`  
Status: development lab, not a seated Clerk

One job moves from queued to claimed to returned, and the named reviewer can see it. Clerk copies the assignee and the reviewer from the job record. It does not choose a recipient, accept, close, retry, infer authority, launch a worker, or call a model.

Pass01 is a different experiment and is not imported. Patterns cited from `labs/clerk-handoff-pass01/clerk_lab.py`, not copied as this program:

- canonical JSON and sha256, lines 21-30
- hash-linked events and a reducer that refuses a broken chain, lines 29-84
- identical delivery already recorded, changed body under that id refused, lines 183-188
- claim token and return must match the claim, lines 166-169 and 191-193
- artifact path and hash checked again on read, lines 135-141
- path containment, lines 126-133
- explicit resume, lines 154-160
- a view is a projection, lines 224-232

Not carried forward: hard-coded recipients, closure when a review says accepted, `next(role)`, and SQLite.

## Commands

Python 3.10+ standard library. From this folder:

```text
python -B clerk.py queue --store S --job JOB.json --instructions-base BASE
python -B clerk.py claim --store S --job ID --as NAME --instructions-base BASE
python -B clerk.py claim --store S --job ID --as NAME --instructions-base BASE --resume
python -B clerk.py return --store S --job ID --as NAME --claim TOKEN --delivery DID --evidence TEXT
python -B clerk.py inbox --store S --as NAME [--instructions-base BASE]
python -B clerk.py show --store S --job ID [--instructions-base BASE]
python -B clerk.py show --store S --job ID --json [--instructions-base BASE]
python -B clerk.py verify --store S [--instructions-base BASE]
```

`--store`, `--job`, and `--instructions-base` are absolute paths. Clerk does not resolve them from the process working directory. There is no `--allow-repo-store` flag. A store whose path resolves into a Git working tree is refused, including a working tree whose `.git` entry is a file. `--json` is only on `show`.

Exit codes: `0` ok, `1` findings, `2` refused. Human stdout ends with `result ok`, `result findings`, or `result refused`. `show --json` prints the inspection document and does not add that line.

## Job record

The router writes the job file. Clerk checks it and does not fill in missing fields. The object has exactly these keys:

- `job_id`, `assignee`, `reviewer` — windows-safe ids, assignee and reviewer different even by case
- `instructions` — exactly `path` and `sha256`; `path` is relative to the named base, forward slashes, no `..`
- `release`, `routed_by` — non-empty text, recorded and not treated as proof
- `expected_outputs` — a non-empty list of distinct simple filenames

Ids are ASCII, at most 64 characters, and are not Windows device names (`CON`, `NUL`, `COM1`, and the rest of that set). Case-colliding ids and output names are refused. JSON must be finite, without duplicate keys.

`--as` is a label. The claim token ties a return to a claim. Neither one proves who a person or a model is. `release` and `routed_by` are recorded text, not a check that the Director authorized the job. Return `--evidence` must be one line of non-blank printable text. Whitespace-only evidence is refused as `evidence is blank`. Nonblank evidence containing any control character (below U+0020: tab, CR, LF and the rest) is refused as `evidence contains a control character; it must be one line of printable text`. Neither refusal writes anything. There is no multi-line convention. Evidence is a note from the caller, not a credential.

## Store

```text
<store>/jobs/<job-id>/
  0001.queued.json
  0002.claimed.json
  outbox/
  0003.witness.json
  0003.returned.json
```

Event files are canonical UTF-8 JSON, one trailing LF, keys sorted. `prev` on the first event is null. Each later `prev` is the SHA-256 of the previous event file's exact bytes. New events are stamped `clerk-handoff-pass02/2`.

`0003.witness.json` is the completion witness. Clerk writes it with exclusive create before `0003.returned.json`. It records the SHA-256 of the exact returned-event bytes that are about to be written. A returned job is clean only when both files exist and that digest matches the event file. A witness without the event, an event without the witness, a partial witness, a digest mismatch, or any other completion file is incomplete or corrupt. It is not a clean claim, and a later return does not repair it or write a replacement event.

A store stamped `clerk-handoff-pass02/1` is an earlier format. Readers name that format and refuse it. Clerk does not rewrite it into the new shape.

Every new file is created with exclusive create (`open(..., "xb")`). The outbox directory is an exclusive `mkdir`. Clerk does not truncate, replace, or delete an existing record.

Expected outputs are ordinary files in `outbox` with link count one. A symlink, junction, other reparse point, hard link, directory, missing name, or extra name refuses the return. These checks do not defeat a malicious program running as the same user.

## Resume and resend

A complete claim (valid `0002` and a plain `outbox`, no return yet) stays visible to its assignee. `claim --resume` prints the same token, checks the instruction hash, and does not write an event, a token, or another outbox.

A second `claim` without `--resume` is refused.

After a complete return, the resend identity is the caller's `--as`, `--claim`, `--delivery`, `--evidence`, and the verified artifact bytes. Timestamps and `prev` are not part of that identity. The same delivery id and the same identity print `already-recorded` and do not write a new witness or a new event. The same delivery id with different evidence or different artifact bytes is a delivery conflict and does not write. This is per job. The same delivery id on another job is a different record. It is not a global exactly-once guarantee. An identical return does not finish a missing event when the witness was left behind. That partial pair stays incomplete.

## Instructions

The instruction base is named on every queue and claim, including resume. Clerk hashes the file under that base before queue, before a new claim, before resume returns the token, and before inbox or show describes the instructions as usable. A mismatch refuses the mutation and does not write. Inbox and show without a base say `instructions-not-checked` and do not call the instructions usable. Verify does not treat an unchecked instruction file as verified.

## Inspection

`show --json` reuses the validated view. It does not read the event files a second time, and it does not write. Stdout is one canonical JSON object and a trailing LF. Stderr is empty. The schema identifier is `clerk-handoff-inspection/2`. Its predecessor `clerk-handoff-inspection/1` had the same document without `returned.event_sha256`. The keys are exactly `schema`, `job_id`, `state`, `job`, `claim`, `returned`, `checks`, and `problems`. A CLI syntax error stays argparse's exit 2 on stderr, and that stdout is not this document. `--json` on another command is that syntax error and writes nothing.

`state` is `queued`, `claimed`, or `returned` only when the reducer accepts that phase. `incomplete` and `corrupt` are damaged records. `unknown` means the job was not found, the path was refused, or a filesystem error escaped the reader. `job`, `claim`, and `returned` are null unless the phase is clean. A clean non-returned phase has null `returned`. The projection does not invent outputs, and an invalid structure is never a clean returned object.

`job` is the validated seven-key queued object, including its `job_id`. Assignee, reviewer, instructions, expected outputs, release, and routed_by stay on that object. Top-level `job_id` is the requested id, including when `job` is null. `claim` is `by` and `token` from the validated claim. `returned` is `by`, `delivery`, `evidence`, `artifacts`, and `event_sha256` from the validated return. Those artifact hashes are the hashes recorded on the event. A later byte change does not rewrite them.

`event_sha256` is the SHA-256 of the exact `0003.returned.json` bytes that the reducer read once and matched against the completion witness before it accepted the pair. It is the returned event's identity. It is present only when `returned` is not null, so an incomplete, corrupt or unknown record never supplies one. A later change to an artifact leaves it as the recorded event's identity, while `checks.artifacts` reports `changed`. Names and the claim token are labels, not authentication.

`checks.events` is `ok`, `unreadable`, `broken`, or `not-applicable`. `checks.completion` is `ok`, `partial`, `missing-event`, `missing-witness`, `mismatch`, or `not-applicable`. `checks.artifacts` is `ok`, `changed`, or `not-applicable`. `checks.instructions` is `usable`, `unusable`, `not-checked`, or `not-applicable`. `not-checked` means a clean job and no instruction base. `not-applicable` means the check was not run against a usable record. Neither one means the check passed. `unusable` means the file at the named base does not match the recorded instruction hash.

`problems` is a list of objects with `kind` and `detail`. An `artifact-changed` problem also has `path`, and its detail is the same artifact line human `show` prints. Kinds are `unknown`, `incomplete`, `corrupt`, `artifact-changed`, `instructions-unusable`, and `filesystem`. The list is empty only on exit 0. Exit 0 is a structurally valid queued, claimed, or returned projection with no problems. It can still carry `instructions: not-checked` (see the consumer contract below). Exit 1 means that projection is intact and the only problems are a changed artifact, unusable instructions, or both. Exit 2 is unknown, incomplete, corrupt, a refusal, or a filesystem error. Structural detail is the reducer's diagnosis, without the human `bad state:` wrapper. Refusal detail drops one `refused: ` prefix. Filesystem detail is the exception class and its message.

**Consumer contract.**
- **Exit 0 means a structurally valid projection.** It does not mean every check ran.
- **`instructions: not-checked` does not mean verified, and it does not mean ready.**
- **A consumer that needs usable instructions** must pass `--instructions-base` and require `checks.instructions` to be `usable`.
- **A clean returned handoff requires all of these:** `state` is `returned`; `checks.events`, `checks.completion` and `checks.artifacts` are all `ok`; and `problems` is empty. Reading `state` alone is not enough.
- **A consumer that records or acknowledges a troubled record** keeps its `checks` and `problems` with it, rather than hiding them.
- **Nothing here grants approval.** A good document is not an accepted job.

The document is a projection for a later reader. It is not an acceptance, a closure, or a second copy of the job. The witness limit below is unchanged.

## Interrupted writes

An interrupted queue, claim, or return is not a success and is not repaired.

- A partial event file stays where it was. Inbox, show, and verify report `bad state: incomplete:` and do not present a clean empty queue or a successful return.
- A claim event that exists without an outbox stays incomplete. Resume does not create the outbox or a new token. Return does not succeed. The reviewer is not told the job was returned.
- Clerk does not delete the partial record, roll it back, or finish it. There is no repair command. The partial store is evidence. Doing the work again means a new job id in a new store, outside this program.

A filesystem error at a command boundary exits `2` and says `incomplete: filesystem error:`. The partial files stay. If the claim event is already on disk, the diagnostic says `claim event exists` and prints that existing token as `existing token`. It does not write a second token. An OS error is not findings and not success. A programming error is not caught and reported as success.

The hash chain shows that an earlier event file changed after the next event recorded its bytes. It is not a signature. The completion witness detects one isolated break in the returned pair: deleting or changing only the returned event, or only the witness, no longer looks like a clean claim or a clean return. It does not authenticate history. Someone who rewrites the whole store, or who rewrites the witness and the returned event so they still agree, or who deletes both and leaves the claimed prefix, is not caught. `verify` exits `2` for a broken or incomplete record and `1` when the record is intact but an artifact's bytes changed. A changed artifact is `artifact changed` and `not-returned-clean`, never a clean return.

Corrupt and incomplete jobs are listed for every inbox caller. Omitting them would make a damaged store look like an empty queue. A person who is not the assignee or the reviewer still sees no clean job.

## What this lab does not do

No accept, close, route, scheduler, model call, worker launch, app import, or SQLite. Tests and `demo.py` keep their stores in a temporary directory outside the Git working tree. `python -B demo.py --out <new absolute temp dir>` runs the seven-step demonstration in separate processes. `python -B tests/test_clerk.py` runs the refusal and resume tests. A link type this Windows account cannot create is reported as a skip, not as a pass.
