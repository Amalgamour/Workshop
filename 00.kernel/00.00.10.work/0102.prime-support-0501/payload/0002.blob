# DESIGN — Prime status and intake (0507.prime-support 05.01)

Author: claude-opus-5-5, Colab/design lead. Date: 2026-10-27.
Inputs: pack05.01 (12 files at 54274e6). Line references are to those snapshots.
Extra design evidence (my own, not accepted): 0506/05.03 return (page sha256 936023d1…), design manifest b3f9dcf7….
Nothing here is built, run or released. Examples are in `examples/`. Synthetic items are labelled SYNTHETIC.

## 1. What it is, and what it is not

Prime support is a read-mostly lab tool with two jobs:
1. **STATUS:** one entry that shows every registered lane, from its owning records, with conflicts, missing sources and staleness left visible.
2. **INTAKE:** it tells Prime which returned revisions are new, lets Prime acknowledge one durably, and derives review and finding state from the page-local records.

It does not:
- queue, route, release, claim, dispatch, review or accept;
- choose a recipient or guess a next command;
- crawl repositories;
- fetch by default.

Clerk remains the job/handoff record (0506). When a lane runs through Clerk, this tool reads Clerk's inbox. It never keeps a second queue.

Later modules (outlined only, §9): assignment preparation, and handoff readiness.

## 2. Discovery: an explicit registry that owns paths, not state

**`lanes.json`** (example `examples/lanes.json`):
- Prime writes it. Its proposed home is `0507.prime-support/lanes.json` (a routine recommendation; the intake store's location is the separate decision M01).
- It names repositories (local path, branch, remote-tracking ref, worktree policy), the canonical assignment record and the lane it describes, and lanes. A lane holds page folders, Clerk store paths, delivery ids, review records, or an external repository and ref.
- It holds no state, no current batch, and no assignee permission. `owner_label` is a display label, not identity (0408 seats remain the authority).

**Bounded reading:**
- Within a registered page folder, only root `05.NN.md` and `06.NN.md` files are read. `evidence/`, `packed/` and copies are never treated as returns.
- An unregistered page, even one with a return, is invisible. The status report says the registry is the scope, so nothing implies completeness.
- External repositories (SoF) are read only at their registered ref, through `git show`/`git rev-parse`. Their working tree is read only if the registration says `worktree_status: registered-paths`, and SoF's says `off`.

## 3. STATUS

### 3.1 Sources and fact ownership

| Displayed fact | Owner | Status reads it as |
|---|---|---|
| canonical current work, state, waits_on, next | `0401.goal/06.01.md` (schema 0410) | read; one lane only |
| release eligibility | batch `Release:` line, plus the Director quote in the Return | read; `PENDING` means not released; absent means `unknown` |
| claim / current execution | batch `Claim:` plus a proposed `execution:` line (06.02 G01) | read; prose is never parsed; absent means `unknown` |
| transport completion | app receipt (bridge-status) or Clerk 0003 | read through their read-only commands |
| review | the batch Review section (`Reviewed return SHA-256`, proposed `reviewed_return_prefix`, `Disposition:`) | read; matched to a return revision (§4) |
| findings and resolutions | page-local review records: Observer tables, proposed Prime `findings:` line (G03) | read; otherwise `not machine-readable` |
| acceptance | the Prime review `Disposition: ACCEPTED…`, or a Director record | read; never inferred from intake |
| dependencies | proposed `depends_on:` (G04) | read; otherwise `unknown` |
| published / local / uncommitted revision | Git: remote-tracking ref, HEAD, `git status --porcelain -- <registered paths>` | read; the remote is "last observed", never fetched |
| intake seen | intake acknowledgement store (§4) | read |

Five states stay distinct on every row: **released → executing → transport complete → reviewed → accepted**. A missing link shows as `unknown`, never as the next state.

### 3.2 CLI (proposed)

```text
python -B prime_support.py status --registry <lanes.json> [--intake <store>] [--lane <id>] [--json]
```

- Read-only and offline. Git runs with `GIT_OPTIONAL_LOCKS=0`, and only `rev-parse`, `show`, `ls-tree`, `log` (bounded to registered paths) and `status --porcelain -- <paths>` are used. No fetch, no worker, no view regeneration, no mark.
- Exit codes: 0 when nothing needs attention, 1 when there are conflicts, review-needed returns, missing sources or open findings, 2 when the registry is invalid or the tool fails.

### 3.3 Sample report

`examples/status-report.txt` is illustrative. It shows:
- **The real present conflict:** the canonical record says `0504/05.06 waiting`, the published page still says `Release PENDING`, and yet `git status` shows local work on that lane's registered paths. Status shows all three. It does not decide whether a release happened in chat.
- **A local-only return:** 0506/05.03, untracked and not on origin/workshop, is marked LOCAL ONLY. Prime cannot review it from the published tree.
- Findings that are `not machine-readable`, rather than guessed.
- One attention target.

### 3.4 One attention target, by a written rule (not judgment)

Order:
1. conflict or missing source;
2. a return seen but unreviewed, oldest first;
3. a return not yet seen;
4. a finding at the escalation threshold (0505 two-pass rule);
5. director-pending;
6. open findings;
7. otherwise none.

Ties go to registry order. Status names the item and its context packet. It never names a command.

### 3.5 Context packets

For the attention target, status prints the exact sources to read: path plus revision or hash. That is:
- the return revision (path plus prefix sha, and the commit if published);
- its pack manifest;
- the evidence manifest the return names;
- the open review records it touches.

A fresh model reads those, not every historical artifact. Example: `packet: 0401.goal/06.01.md@1ee161c5…, 0504/05.06.md@<prefix>, git status -- 0504.app-entry app/`.

## 4. INTAKE and durable review identity

### 4.1 Return revision identity (tested on pinned history)

`return_id = (repository, page path, prefix_sha256)`. `prefix_sha256` is sha256 of the page bytes from the start of the file up to, not including, the first line that begins `## Review`. If there is no Review heading, it is the whole file, flagged `no review section`.

Evidence (06.02 R01), from read-only Git object reads at ancestors of the pin:

| 0504/05.05 at | whole-file sha256 | prefix sha256 | meaning |
|---|---|---|---|
| d9775fa (Builder return) | 56f15524… | 25ca0e6d… | revision 1 |
| cf25d56 (Builder amends: names the evidence commit) | 56c4e2c1… | 8c1dfe6f… | revision 2, a new reviewable revision |
| 2c581eb (Prime appends review) | 5a52d9e9… | 8c1dfe6f… | the same revision: not a new return |

Prime's recorded `Reviewed return SHA-256 56c4e2c1…` is the whole file at cf25d56. Intake keeps both hashes, so old reviews still bind to exactly one revision.

**Rules:**
- **NEW:** a registered page whose Return section says `execution: returned` (or, on historical pages, carries a non-PENDING return body, flagged `execution unknown`) and whose `return_id` is not acknowledged.
- **SAME:** an identical `return_id`. Re-reading writes nothing, and appending a Review never re-queues it, including Prime's own review.
- **AMENDED:** a new `prefix_sha256` on the same page after an earlier revision. It is a new revision with `supersedes` set. The earlier revision's review and findings stay attached to it and stay open until answered.
- **INCOMPLETE:** `execution: claimed|running`, `Execution: IN PROGRESS`, or a Return body of `PENDING`. Shown as executing, not intake-eligible.
- **MISSING EVIDENCE:** the return names an evidence manifest that is absent at that revision. Intake shows `evidence missing` and still allows a seen acknowledgement. It does not verify contents: that is review.
- **DUPLICATE:** the same prefix bytes at another path (a pack copy). Not read, because only registered page roots are read (§2). The same `return_id` from both the worktree and a commit is one revision, with both observations recorded.
- **CONFLICTING SOURCE:** the worktree prefix differs from the published prefix. These are two revisions: `local-unpublished` and `published`. Neither hides the other.
- **Clerk-routed work:** `return_id = (clerk store, job_id, sha256 of 0003, plus the 05.02 witness)`, read from `clerk.py inbox --as codex-prime`. This applies only after 0506/05.02 is accepted.

### 4.2 The intake store keeps acknowledgements only

- Layout: `intake/<page-key>/<prefix12>/0001.seen.json` (example `examples/intake/`).
- It copies Clerk's file discipline, cited and not imported: exclusive create, exact keys, a version stamp, and a `prev` hash for any later event.
- A seen record holds the subject identity, what was observed (worktree or commit, whole sha, execution line), `supersedes`, `by` (a label), `at`, and a note.
- `intake ack` with an identical identity reports `already-recorded` and writes nothing. A conflicting record under the same identity is refused.
- **Reviewed, findings and resolutions are not stored here.** They are derived each time from the page's Review section and the page-local review records. Deleting or regenerating the intake store can only return a revision to `unseen`. It can never hide an open finding.
- An acknowledgement is not a review, not a disposition and not acceptance. The record says so in its note field.

### 4.3 States, and one synthetic walk (`examples/synthetic/`)

| Step | Records | Derived status |
|---|---|---|
| 1 | v1 page returned (prefix 5e4439fc…), no ack | **unseen** |
| 2 | `intake ack` → `5e4439fc0dc7/0001.seen.json` | **seen**, review-needed |
| 3 | the same ack again | already-recorded, no write (idempotent) |
| 4 | Prime appends a Review (`reviewed_return_prefix: 5e4439fc…`, `findings: SY-01=unresolved`); whole file changes, prefix the same | **reviewed**, 1 unresolved finding; not re-queued |
| 5 | a synthetic Observer note on SN-01 targets the same prefix (advisory) | note **unseen** in the observer section. Not a pass; not a finding until Prime records a response |
| 6 | the Builder amends the Return (prefix 4443b4b2…) | **new revision**, unseen, `supersedes 5e4439fc…`. SY-01 is still unresolved on v1 |
| 7 | ack v2 → `4443b4b2e216/0001.seen.json` | v2 seen, review-needed |
| 8a | Prime reviews v2 with `findings: SY-01=verified-fixed` | SY-01 answered; lineage passes = 2 |
| 8b | or `findings: SY-01=director-pending` | escalated; attention rule 5 |

Pass count = the number of reviewed return revisions in a finding's lineage (0505 §4). Here v1 and v2 give 2. Observer notes, re-reads, acks and Prime edits are not passes.

### 4.4 Observer intake (slice 2, explicit)

```text
python -B prime_support.py observer fetch --registry <lanes.json>
```

- Updates only an independent bare cache, `git fetch <allowlisted remote> refs/heads/observer/reviews`, never a shared checkout. It records `last_seen` (the commit) in the cache.
- Note identity = (commit, path, blob sha).
- New notes are the paths added under `notes_path` between `last_seen` and the new tip. A note modified or removed later is shown as `append-only violated` with both blobs, and nothing is overwritten.
- The `YYYY-MM-DD-HHMM` Central-time name is a label. Order comes from the commit graph.
- No scheduler and no hidden polling. The tool stores no credentials: if Git needs auth and has none, the fetch fails and says so.
- Prime replies on the relevant work page (0505 §3-4). Notes are never edited.

## 5. When canonical and page-local disagree

Status prints both, the owning record of each, and a CONFLICT line. It never reconciles them. Three cases:
- the canonical record names work that the page still marks `Release PENDING`;
- the page shows a Claim or Return while the canonical record says `waiting`;
- the canonical record names a lane it does not describe.

The fix is a human edit of the owning record. Today's real case is in `examples/status-report.txt`.

## 6. What exists and what is proposed

| Item | Status |
|---|---|
| canonical assignment record v1 (0410 schema); page batches with Release/Claim/Return/Review; Observer review records with finding tables; Prime "Reviewed return SHA-256" and "Disposition" lines | exist (convention, hand-written) |
| Clerk CLI: inbox, show, verify | exists (pass02); correction 0506/05.02 pending |
| app bridge-status | exists (0504/05.05); BRI-01 fix 05.06 pending |
| local remote-tracking refs | exist (last observed: origin/workshop 54274e6, origin/observer/reviews e865d3c) |
| `lanes.json`, `prime_support.py status/intake`, intake store `prime-intake/1`, the prefix identity rule, the attention rule, context packets | proposed |
| page conventions `execution:`, `reviewed_return_prefix:`, `findings:`, `depends_on:` (06.02 G01-G04) | proposed, for new batches only (Director decision M02) |
| Observer fetch cache | proposed, slice 2 |

## 7. The first implementation slice (ONE)

**Name:** "prime-support status + intake, fixture only".

**Location:** `labs/prime-support-pass01/`. No `app/`, kernel, Clerk or bridge change.

**Files:**
- `prime_support.py`: library and CLI, standard library plus the `git` executable;
- `README.md`;
- `tests/test_prime_support.py`;
- `.gitignore`;
- `evidence/`.

**Commands:**
- `status`;
- `intake scan`: read-only, lists unseen, amended and incomplete revisions;
- `intake ack --page P --prefix-sha H --as LABEL --intake <store>`: one exclusive write;
- `intake show`.

**Not in it:** observer fetch, the Clerk adapter (it waits on 0506/05.02, and is then a small follow-up reading `clerk.py inbox`), assignment preparation, readiness.

**Dependencies:**
- Python 3 stdlib.
- Git CLI (read subcommands only).
- Registry schema `prime-support-registry/1`.
- Intake schema `prime-intake/1`.
- The prefix rule in §4.1.
- No dependency on unaccepted Builder work.

**Fixture acceptance tests.** Each runs in its own disposable `git init` repositories with a bare "origin":
1. A three-lane registry (two page lanes plus one external synthetic repository) gives the exact report. The repository's HEAD, index bytes, refs and status are unchanged, and no file is written.
2. Canonical-vs-page conflict, in all three §5 shapes, is visible with both sources.
3. Published, local commit and uncommitted states are all shown. The remote-tracking ref is behind and labelled "last observed". No network subprocess is ever run (asserted by a git-runner allowlist).
4. Identity: an appended Review keeps the prefix (no new intake). Prime's own review is not re-queued. An amended return gives a new revision with `supersedes`.
5. Incomplete returns (`claimed`, `running`, `IN PROGRESS`, `PENDING`) are not intake-eligible.
6. `ack` is idempotent. A conflicting ack is refused. Refusal leaves the store unchanged.
7. A Review bound by whole-file or prefix hash gives `reviewed`. A `findings:` line drives unresolved, answered and escalated counts. Passes count only reviewed revisions.
8. Deleting the intake store returns revisions to unseen, and open findings stay listed.
9. A missing registered page or source shows as `missing`, never omitted.
10. A decoy unregistered page holding a return is never read (no crawl).
11. Historical pages without the new fields show `unknown` and `not machine-readable`, and never a guessed state.
12. A worktree-vs-published prefix difference gives two revisions.

**Demonstration:** a fixture run of the §4.3 walk, steps 1-8, with transcript and hashes.

**Owner:** Prime assigns the builder. It is a new lab, independent of both current builder lanes.

## 8. Shadow-Prime trial (proposed; nothing launched; no authority granted)

**When:** after slice 1 is accepted. The Clerk adapter is optional.

**Setup:**
- A disposable clone of the published repository at a pinned commit.
- A fixture lane with one synthetic return.
- `boot_mode` recorded honestly: `fresh-session` only if the session really starts with nothing but the sources below.

**The fresh Prime receives only:**
- the published root entry;
- `lanes.json`;
- the `status` output;
- the context packets it names;
- the Prime role page.

It gets no chat history and no Codex conclusions.

**Tasks:**
1. Report the situation in its own words: lanes, states, conflicts, the attention target.
2. Propose the next assignments as drafts. Nothing is released or written to real pages.
3. Handle one fixture return in the clone: `intake scan`, `intake ack`, a review with a disposition and a `findings:` line, and an answer to one pre-planted open finding.

**What Codex checks**, independently and from the same sources:
- every lane and state matches the owning record;
- each conflict, unknown and stale fact was surfaced, not smoothed over;
- the return identity is correct (prefix);
- no finding was dropped;
- no action was taken outside the clone;
- no authority was claimed (release, acceptance, recipient choice);
- proposals cite sources.

**Records** (a later 0507 06.NN, allocated when the trial is released):
- the trial request;
- the shadow's transcript and outputs;
- Codex's independent reading;
- a disagreement table: item, shadow, Codex, owning source, and who was right per that source;
- every Codex or Director intervention, verbatim, with its reason.

Nothing is edited after the fact.

**Evidence that could support expanding responsibility:**
- repeated trials (for example three) with zero authority violations, zero dropped findings and zero unexplained disagreements;
- at least one trial containing a conflict and an amended return.

The Director decides any expansion. Nothing is promoted automatically. This design does not claim that a cold-boot test has happened.

## 9. Later modules (boundary only)

- **Assignment preparation:** builds a draft pack (a manifest of named sources at a commit) from Prime's chosen sources. It consumes status packets and writes only a draft batch for Prime to edit.
- **Handoff readiness:** checks a drafted pack before release: pins resolve, `depends_on` targets are accepted, the lane has no running claim, and there is no conflict. It reports. Prime and the Director release.

Neither one routes, releases or accepts.

## 10. Material decisions

- **M01. Real intake store location.** Recommended: `0507.prime-support/intake/`, written only by Prime's explicit ack and published by Prime. The alternative is an external store with periodic custody export.
- **M02. Adopt four one-line conventions for new batches** (`execution:`, `reviewed_return_prefix:`, `findings:`, `depends_on:`). Historical pages stay as they are and read as `unknown`.

Everything else is a routine recommendation.
