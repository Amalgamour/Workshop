# Proposal — smallest file-backed Clerk handoff loop
Date: 2026-10-27
From: claude-opus-5-5, Colab, proposed technical lead for this subproject
For: Codex Prime review. Director decides.
State: proposal only. Nothing implemented or dispatched. No address allocated, no shared record changed.

## 1. Goal
One explicitly routed job is queued, claimed, returned, and then shown to its named reviewer. Nothing more.
Clerk copies routing from the job record. It never selects a recipient, approves, closes, retries or infers authority.

## 2. Evidence: labs/clerk-handoff-pass01 (read, unchanged)
Preservation check (2026-10-27): all 35 manifest.json entries match their bytes; manifest.json is a5f3d9ce…. The lab is tracked at d0bdd53, with no working-tree changes.

Reusable as patterns. These are copied and cited, not imported, so pass01 stays untouched and nothing depends on it:
- canonical JSON and sha256 helpers (clerk_lab.py:21-30);
- the hash-linked event chain, and the reducer that rebuilds state and refuses a broken chain (clerk_lab.py:29-84);
- delivery identity: an identical resend is "already-recorded", changed contents under the same id are refused (clerk_lab.py:183-188);
- the claim token, and the return-must-match-claim check (clerk_lab.py:166-169, 191-193);
- an artifact recorded with its path and hash, re-verified on every read (clerk_lab.py:135-141);
- path containment (clerk_lab.py:126-133);
- explicit resume of an unfinished claim (clerk_lab.py:154-160);
- "the view is a projection, never authority" (clerk_lab.py:224-232).

Not reusable, because it conflicts with the new rule:
- **Hard-coded recipients:** the JOB record stores a `route` (clerk_lab.py:114), but `hand()` never reads it. The next recipient is hard-coded: build goes to "colab", changes go to "builder" (clerk_lab.py:206-216).
- **Recipient choice and closure:** `next(role)` hands any ready item to any caller asserting that role (clerk_lab.py:161-169). Clerk records CLOSED when a review says accepted (clerk_lab.py:217-219).
- **Role fixtures:** scripted roles write into one shared artifacts/ folder (clerk_lab.py:259).
- **Storage:** SQLite, which the lab itself calls a lab choice. This loop needs plain files.

Lesson carried in from the 0504/05.03 review (AR-01): writes through pre-existing files can escape path checks via hard links. Every Clerk write is therefore an exclusive create inside a folder Clerk itself created fresh.

## 3. Module boundary
Proposed lab folder `labs/clerk-handoff-pass02/`. This is a lab path, not a book or page address; Prime confirms the name.
- **`clerk.py`:** library and CLI. Python standard library only. It imports nothing from app/, labs/worker-bridge-pass01, labs/clerk-handoff-pass01 or the kernel.
- **`README.md`:** the record format and the commands.
- **`tests/test_clerk.py`:** runs in temporary stores only.
- **`demo.py`:** the acceptance demonstration in section 6.
- **`evidence/`:** run outputs and SHA256SUMS.txt.

The store is an explicit `--store <dir>` outside the shared workspace in all tests and demos. Clerk refuses a store inside a Git working tree unless `--allow-repo-store` is given, and the demo never gives it.

Record layout, one folder per job; events are numbered files, written with exclusive create (`open(..., "xb")`):

```text
<store>/jobs/<job-id>/
  0001.queued.json     the job record, verbatim and canonicalised, plus prev=null
  0002.claimed.json    {claim, by, at, prev}
  outbox/              created by Clerk at claim (exclusive mkdir), the only place a return may cite
  0003.returned.json   {claim, by, delivery, artifacts:[{path,sha256,bytes}], evidence, at, prev}
```

Each event carries the sha256 of the previous event file. State comes only from these files. Any gap, extra file, unknown name, or bad hash refuses.

Job record, an exact-key schema written by the router (Prime or the Director), not by Clerk:
- job_id;
- assignee and reviewer (non-empty, different);
- instructions, as {path, sha256};
- release, as the citation string, for example "Director, chat 2026-10-27";
- routed_by;
- expected_outputs, a list of outbox-relative names.

Clerk records `release` and `routed_by` as given. It checks only their presence, never their truth. A missing field is refused, never defaulted.

## 4. Commands
- **`queue --store S --job job.json`:** validate and write 0001.
- **`claim --store S --job ID --as NAME`:** only the recorded assignee may claim. The exclusive create of 0002 settles a race.
- **`return --store S --job ID --as NAME --claim TOKEN --delivery DID --evidence TEXT`:**
  - accepted only from the claimant holding that token;
  - every expected output must be present in the outbox, a regular file with one link (no symlink, junction or hard link), with no extra files;
  - Clerk hashes them and writes 0003.
- **`inbox --store S --as NAME`:** read-only.
  - The assignee sees jobs in the queued state, and claimed jobs to resume.
  - The reviewer sees returned jobs, with re-verified artifact hashes.
  - Anyone else sees nothing.
- **`show --store S --job ID`** and **`verify --store S`:** read-only. They rebuild the chain and re-hash each artifact. A changed artifact is reported as "artifact changed", never as returned-clean.

Exit codes: 0 ok, 1 findings (verify), 2 refused.

There is no `accept`, `close`, `route` or `next-recipient` command. Review results are out of scope for this loop.

## 5. Ownership
- **Director:** releases the assignment; any address allocation; any later integration or gate wiring.
- **Codex Prime:** reviews this proposal; packs and issues the assignment; accepts or rejects the build.
- **Claude, lead:**
  - holds the record contract and the acceptance list in this file;
  - answers the builder's contract questions;
  - reviews the build against section 6 and returns findings. I do not edit the builder's files.
- **Grok, second builder:** implements `labs/clerk-handoff-pass02/` only.
- **Grok, first builder:** not involved; the output-alias repair stays separate.

## 6. Acceptance demonstration (one, end to end)
`python -B demo.py --out <new temp dir>`. Separate processes, each given only the store path and its own name:
1. **Router fixture:** writes job.json: job_id demo-0001, assignee builder-b, reviewer codex-prime, instructions = a fixture file plus its hash, release "fixture release", expected_outputs ["count.py"]. Then `queue`.
2. **`inbox --as builder-b`:** lists demo-0001 as queued. **`inbox --as codex-prime`:** lists nothing.
3. **`claim --as builder-b`:** prints the token. A second `claim --as builder-b` is refused. So is `claim --as colab`.
4. **Builder fixture:** writes outbox/count.py. Then `return --as builder-b`, with its token and delivery d-1.
5. **`inbox --as codex-prime`:** lists demo-0001 as returned, with count.py's sha256 equal to the file's. `inbox --as builder-b` and `inbox --as colab` do not list it for review.
6. **A fresh process runs `verify`:** chain ok; states queued, claimed, returned; exit 0.
7. **Tamper step:** count.py is edited after the return. `show` and `inbox --as codex-prime` report "artifact changed", and `verify` exits 1.

Pass means all seven steps match exactly. The transcript, the store tree listing and SHA256SUMS go in evidence/.

## 7. Required refusals (tests)
Each must exit 2 with no new event file:
- unknown or missing job key;
- assignee equal to reviewer;
- missing reviewer (never defaulted);
- queueing the same job_id twice;
- a claim by a non-assignee;
- a second claim;
- a return before a claim;
- a return with the wrong token or by the wrong name;
- an expected output missing, or an extra file;
- a symlink, junction or hard-linked output;
- a path escape in expected_outputs;
- the same delivery id with different contents (an identical resend reports already-recorded);
- a tampered, missing or extra event file;
- a store inside a Git working tree;
- a planted 0003 before the claim.

Each test also proves Clerk wrote nothing outside the store.

## 8. Recommended assignment for the second Grok builder (text to issue)
> Build `labs/clerk-handoff-pass02/` as specified in
> `returns/clerk-handoff-proposal-claude-2026-10-27.md` sections 3-7: `clerk.py`, `README.md`,
> `tests/test_clerk.py`, `demo.py`, `evidence/`. Standard library only. Do not import from or edit app/,
> labs/worker-bridge-pass01, labs/clerk-handoff-pass01, the kernel, or any work page. Clerk copies routing
> from the job record and has no accept, close or route command. Every write is an exclusive create inside
> the store. Use temporary stores outside the repository. No Git writes, no model calls, no activation.
> Done when: every section 7 refusal has a passing test, `demo.py` reproduces all seven section 6 steps
> in a fresh temp store, and you return the test output, the demo transcript and SHA256SUMS for review by
> Claude (lead) and acceptance by Codex Prime. Questions about the record contract go to Claude; any
> change to scope goes to Prime.

## 9. Open questions for Prime
- Q1. Is the lab folder name `clerk-handoff-pass02` acceptable, given that pass01 is a different design (SQLite, role-selected)?
- Q2. Should "assignee differs from reviewer" be a Clerk schema rule, or left to the router? I recommend the rule: it checks the record and grants no authority.
- Q3. Callers name themselves with `--as`; identity is not authenticated. This is acceptable for the lab, and must be stated as a limit.
