# Clerk handoff lab — pass 02

Lab ID: `clerk-handoff-pass02`  
Schema: `clerk-handoff-pass02/1`  
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
python -B clerk.py verify --store S [--instructions-base BASE]
```

`--store`, `--job`, and `--instructions-base` are absolute paths. Clerk does not resolve them from the process working directory. There is no `--allow-repo-store` flag. A store whose path resolves into a Git working tree is refused, including a working tree whose `.git` entry is a file.

Exit codes: `0` ok, `1` findings, `2` refused. Stdout ends with `result ok`, `result findings`, or `result refused`.

## Job record

The router writes the job file. Clerk checks it and does not fill in missing fields. The object has exactly these keys:

- `job_id`, `assignee`, `reviewer` — windows-safe ids, assignee and reviewer different even by case
- `instructions` — exactly `path` and `sha256`; `path` is relative to the named base, forward slashes, no `..`
- `release`, `routed_by` — non-empty text, recorded and not treated as proof
- `expected_outputs` — a list of distinct simple filenames

Ids are ASCII, at most 64 characters, and are not Windows device names (`CON`, `NUL`, `COM1`, and the rest of that set). Case-colliding ids and output names are refused. JSON must be finite, without duplicate keys.

`--as` is a label. The claim token ties a return to a claim. Neither one proves who a person or a model is. `release` and `routed_by` are evidence text, not a check that the Director authorized the job.

## Store

```text
<store>/jobs/<job-id>/
  0001.queued.json
  0002.claimed.json
  outbox/
  0003.returned.json
```

Event files are canonical UTF-8 JSON, one trailing LF, keys sorted. `prev` on the first event is null. Each later `prev` is the SHA-256 of the previous event file's exact bytes. The schema stamp is `clerk-handoff-pass02/1`.

Every new file is created with exclusive create (`open(..., "xb")`). The outbox directory is an exclusive `mkdir`. Clerk does not truncate, replace, or delete an existing record.

Expected outputs are ordinary files in `outbox` with link count one. A symlink, junction, other reparse point, hard link, directory, missing name, or extra name refuses the return. These checks do not defeat a malicious program running as the same user.

## Resume and resend

A complete claim (valid `0002` and a plain `outbox`, no return yet) stays visible to its assignee. `claim --resume` prints the same token, checks the instruction hash, and does not write an event, a token, or another outbox.

A second `claim` without `--resume` is refused.

After a complete return, the resend identity is the caller's `--as`, `--claim`, `--delivery`, `--evidence`, and the verified artifact bytes. Timestamps and `prev` are not part of that identity. The same delivery id and the same identity print `already-recorded` and do not write. The same delivery id with different evidence or different artifact bytes is a delivery conflict and does not write. This is per job. The same delivery id on another job is a different record. It is not a global exactly-once guarantee.

## Instructions

The instruction base is named on every queue and claim, including resume. Clerk hashes the file under that base before queue, before a new claim, before resume returns the token, and before inbox or show describes the instructions as usable. A mismatch refuses the mutation and does not write. Inbox and show without a base say `instructions-not-checked` and do not call the instructions usable. Verify does not treat an unchecked instruction file as verified.

## Interrupted writes

An interrupted queue, claim, or return is not a success and is not repaired.

- A partial event file stays where it was. Inbox, show, and verify report `bad state: incomplete:` and do not present a clean empty queue or a successful return.
- A claim event that exists without an outbox stays incomplete. Resume does not create the outbox or a new token. Return does not succeed. The reviewer is not told the job was returned.
- Clerk does not delete the partial record, roll it back, or finish it. There is no repair command. The partial store is evidence. Doing the work again means a new job id in a new store, outside this program.

The hash chain shows that an earlier event file changed after the next event recorded its bytes. It is not a signature. It does not authenticate someone who rewrites the whole store, and it has no anchor beyond the last event. `verify` exits `2` for a broken or incomplete record and `1` when the record is intact but an artifact's bytes changed. A changed artifact is `artifact changed` and `not-returned-clean`, never a clean return.

Corrupt and incomplete jobs are listed for every inbox caller. Omitting them would make a damaged store look like an empty queue. A person who is not the assignee or the reviewer still sees no clean job.

## What this lab does not do

No accept, close, route, scheduler, model call, worker launch, app import, or SQLite. Tests and `demo.py` keep their stores in a temporary directory outside the Git working tree. `python -B demo.py --out <new absolute temp dir>` runs the seven-step demonstration in separate processes. `python -B tests/test_clerk.py` runs the refusal and resume tests. A link type this Windows account cannot create is reported as a skip, not as a pass.
