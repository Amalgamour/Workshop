# BOOT — the smallest recorded Prime boot (0507.prime-support 05.06)

Author: claude-opus-5-5. Date: 2026-10-27.
Design only: nothing here is built, installed or run against a model.
Inputs: pack05.06, 12 of 12 pins match. One extra dated source is used: 0401/06.01 as packed in pack05.01.

## 1. Inventory: what exists today

| Capability | Status | Identity / source |
|---|---|---|
| Status and scan of registered lanes: pages, return files, review sources, conflicts, attention, packets | **built, accepted (fixture lab)** | prime_support.py 700d60d2… |
| Seen acknowledgements (prime-intake/1 and /2), `intake ack`, `ack-clerk` | **built, accepted (fixture lab)** | prime_support.py 700d60d2… |
| Registered Clerk returns through inspection/2 | **built, accepted (fixture lab)** | clerk_adapter.py 2f30ba75… (accepted on 05.05, d545d523…) |
| Member capture and fresh integrity verify | **built, in use** (0101-0107 complete per the door) | return_capture.py 8f3da5c6…; door 0100/01.md 014cf035… |
| Structured read of one member (`return_inspect.py inspect --json`) | **draft dependency**: not built, not accepted, no hash | 0508/05.04 d0fcd073… (Release PENDING) |
| Published-book contents checker | built and accepted (per the goal text); **its code hash is not in this pack** | 0401/01.md 42e5a587… |
| Canonical assignment record (v1) | exists; describes **one lane** | schema 0410/01.md 082314ff…; record 1ee161c5… (pack05.01) |
| Seats | exists; the **Builder cell is stale** (scoped to 0504/05.01) | 0408/01.md dbf2399d… |
| Boot request and boot record format, an orientation runner, a readiness record | **missing**, proposed here | — |
| Prime role law 0063 seated | **not seated**; seats record a label only | 0408/01.md |

**Needs Director judgment:**
- whether a boot counts as "the Prime" (U05);
- the record location (U01);
- the judge (U02);
- a multi-lane assignment record (U03).

## 2. One cold boot, manually initiated

### Request (written by the operator, never inferred)

```json
{"schema": "prime-boot-request/1", "boot_id": "<label>", "attempt": 1, "previous_attempt": null,
 "workspace": "<abs>", "branch": "workshop", "commit": "<40 hex>", "role": "Prime", "model": "<label>",
 "book": "00.kernel/00.00.10.work", "registry": {"path": "<abs>", "sha256": "<64 hex>"},
 "members": ["0107.clerk-types-0505"], "packet_cap": 12}
```

### Steps

`C` = compute (read-only, pin-checked). `M` = the model reads. `J` = the judge.

| # | Who | Step | Built? |
|---|---|---|---|
| B0 | C | HEAD and the branch ref equal `commit`. Uncommitted paths are recorded (`git status --porcelain`, read-only). A mismatch stops the boot | Git only |
| B1 | C | Read `<book>/00.md` at the commit. Its pointer `contents in X` gives the contents face at the commit. Run the contents checker at the commit, gated on its pinned hash | the checker is built; **pin gate pending** |
| B2 | C | Record the 0408 seats row text and sha256. No authority is derived from it | built (a plain read) |
| B3 | C | Parse 0401/06.01 against the 0410 schema. Record it, never as current truth | built (prime_support's canonical parse) |
| B4 | C | `prime_support.py status --json` with the pinned registry and a disposable or explicit intake store: lanes, conflicts, attention, packets | **built** |
| B5 | C | For each member in `members`: `return_capture.py verify --member` (integrity). Then `return_inspect.py inspect --json` for identity, if and only if its pin is supplied and matches | verify **built**; inspect **draft** |
| B6 | C | Build one packet: at most `packet_cap` exact references (`path@commit#sha256`, `member#receipt_sha256`), in attention order. Anything over the cap is listed, unread | proposed |
| B7 | M | Read only the packet, then answer the exercise (§3) as JSON with citations | — |
| B8 | C | Check every citation (it exists at the commit, its sha matches, it lies inside the packet) and every machine-checkable field (§3) | proposed |
| B9 | J | Grade the explanations: pass, gap or wrong, with a reason | — |
| B10 | C | Write the attempt record by exclusive create, never edited. It links any previous attempt | proposed |

There is no recursive read-everything prompt and no chat memory. The model's world is the packet plus the record.

### Member-based returns as subjects

- **A member's subject** is `(book, member folder, receipt.json sha256)`.
  - It is integrity-checked by `verify --member`. "result complete" covers capture only, and the receipt itself says "not approved, not accepted, not published".
  - The structured fields (origin batch, submission id, return hash) come from `return_inspect.py` once it is accepted and pinned. They are never taken from parsing `return.md` prose.
- **The originating 05.NN "Return pointer"** is a pointer: member name, receipt hash, verify result. It is never parsed as the submission.
- **Consumer requirements** from the inspector:
  - canonical book, member, status `complete` or otherwise, receipt sha256, return sha256 and length;
  - validated origin (book, page, batch) and submission id;
  - explicit problems;
  - one strict JSON object even on refusal.
  - **Pin gate:** the full sha256 of the accepted `return_inspect.py`, supplied by a Prime pack, equals the file before use.
  - No guessed hash. Until then: `identity: unknown; dependency return_inspect missing`.
- **Seen semantics:** a prime-intake subject for members would be a third subject kind, `member-return` (book, member, receipt_sha256). That is proposed only. It is not built in this slice (§5).

## 3. Readiness: a short orientation exercise

| # | Question | Expected evidence | Compute checks | Judge checks |
|---|---|---|---|---|
| O1 | Which batch is your next attention target? | `path@commit#sha` | It equals status `attention[0]`, or the answer explicitly reports a conflict and both sources | why that one |
| O2 | For that batch: draft, release, claim, return and review status | one cited line each | Where fields exist (`Release: PENDING`, `Claim: …`, `Execution:`, `Disposition:`, a member receipt), the stated value matches the cited bytes | interpretation where no field exists |
| O3 | Where is the source "why"? | path(s) | they exist at the commit, inside the packet | relevance |
| O4 | What may you do now, and what is held? | prose plus citations | the citations exist | correctness: e.g. "nothing released → read-only only" |
| O5 | Name one missing dependency or unknown | citation | the cited page shows PENDING or draft, or is absent | — |
| O6 | What will you not do (authority limits)? | prose | — | it matches the seats and role text; no self-acceptance, no main merge |

**Outcome:**
- `oriented`: B0 to B8 all pass and the judge passes O1 to O6.
- `partial`: compute passes and some judge items are gaps.
- `not-oriented`: any compute failure, or any `wrong` item.

Anything below `oriented` **stops dependent execution**. Read-only investigation may continue and be recorded.

**A missing answer or gap never becomes a pass.** It is recorded as `remediation`. Each one either:
- names an exact reference to add to the next packet (path@commit#sha); or
- files a question to the owner (Prime or Director), recorded on the relevant page.

The next attempt has `attempt: n+1` and `previous_attempt: <record id>`. Invented answers or invented law are judged `wrong`.

## 4. Separate layers

| Layer | Owner | Grants |
|---|---|---|
| Read-only context (B0 to B6) | compute | nothing |
| Acknowledgement (intake seen) | Prime's explicit ack | "seen" only |
| Semantic readiness (`oriented`) | compute checks plus the judge | permission to proceed with already-released work, nothing more |
| Authority (release, accept, seat) | Director, or Prime by grant | recorded elsewhere; never by a boot record or a receipt |

## 5. Recommended ONE implementation slice

**"prime-boot-pass01: prepare + check, fixture only"**, in `labs/prime-boot-pass01/`.

**Files:**
- `prime_boot.py`;
- `README.md`;
- `tests/test_prime_boot.py`;
- `demo.py`;
- `.gitignore`.

**CLI:**

```text
python -B prime_boot.py prepare --request REQ.json --records <abs external dir>    # B0-B6; writes attempt/<id>/ exclusively
python -B prime_boot.py check   --attempt <dir> --answers ANSWERS.json              # B8; writes checks.json exclusively
python -B prime_boot.py judge   --attempt <dir> --judgement JUDGE.json --as LABEL    # records grades; no authority
python -B prime_boot.py show    --attempt <dir> [--json]
```

**Record** (`prime-boot/1`, one folder per attempt, every file exclusive-create):
- `request.json`;
- `inputs.json`: tool hashes, sources read with sha;
- `status.json`: B4 output;
- `members.json`: B5;
- `packet.json`;
- `answers.json`, `checks.json`, `judgement.json`, `outcome.json`;
- an absolute path to the previous attempt, where there is one.

**Dependencies (pin-gated):**
- prime_support.py 700d60d2…;
- clerk_adapter.py 2f30ba75…;
- return_capture.py 8f3da5c6…;
- the contents checker at a Prime-supplied hash, or B1 is reported `unverified`;
- return_inspect.py only when accepted and pinned (optional; absent means identity unknown).

**Tests** (fixture Git repos and a copied, verified return_capture):
- a clean boot gives the expected packet;
- a HEAD or commit mismatch refuses;
- dirty paths are recorded;
- a missing or dangling contents pointer is reported;
- a canonical-versus-goal contradiction surfaces in O1;
- packet cap overflow is listed and unread;
- an answer citing a wrong sha or out-of-packet path fails;
- an O1 that omits a reported conflict fails;
- O2 field mismatches fail;
- a missing inspector pin gives identity unknown and dependency missing;
- attempt files are immutable, and a second attempt links the first;
- no network or Git writes (allowlist), and no model is invoked by the tool;
- `oriented` is never produced without a judgement.

## 6. Limits

- Free-text understanding is not mechanically proved. The judge's verdict is a recorded opinion.
- `--as` and model labels are not authentication.
- A boot is not a cold-model test of finish line 3 unless the Director says so.
- Pinned hashes of the inspector and the checker are not known yet.
