# CONTRACT v2 (proposed) — reserved two-pass Colab support, corrected
date: 2026-11-01 · who: claude-opus-5-5 (Claude), informed design author · state: design proposal; supersedes design05.05/CONTRACT.md for review purposes (that file is kept unchanged). Not implemented, released or seated.

Policy: 0411/01.003 §Reserved two-pass; 0411/06.03. Prime review C01–C05: `evidence/prime-review05.05/REVIEW.md`. Audit: 0708/05.01 and its review (F01–F04). Source facts S1–S7: `06.07.md`. Prototype: `colab/labs/0510-reserved-review/pass02/` (nonproduction).

## 0. Kept from 05.05
- **Two existing N7NN passes on one page:** `05.NN` independent, then `05.MM` informed, linked by the review route `request-next`.
- **A descriptor carried as an ordinary required source**, bound by the launch digest.
- **Two fenced JSON blocks** in the reviewer's returns.
- **Ordinary Colab is unchanged,** and no new producer, address axis, face, tail, role or gate is added.

## 1. Custody: N7NN page-local (C01)
**Rule applied** (from Prime C01 and pack #01):
- N5NN packs use the matching N1NN line.
- N7NN keeps `05.NN.pack.md` → `05.NN.return.md` → `06.NN.review.md` on its own page.
- No N1NN reservation, member or capture for either reserved pass. Legacy N1NN captures stay history.

**Current tools cannot do this** (06.07 S1–S4). Three connectors are missing. They are named here and modelled in `workflow_model.py`:

| Missing connector | Proposed home | Inputs | Output and effect | Refusals |
|---|---|---|---|---|
| **K1 `seal-return-local`** | workflow successor (`labs/colab-workflow-pass03`) | `--book --page --pass --return-file ABS --declared-transport TEXT` | fills `passes[pass].return` with `colab-exchange-local-return/1` {return_sha256, return_bytes, declared_transport, package_digest}; writes `05.NN.return.md` with the exact bytes; appends a `seal-return` transition | `missing investigation` (no attached package); `occupied different content`; identical replay is a no-op |
| **K2 `open-pass`** | workflow successor | `--book --page --pass 05.MM` | adds an empty slot for 05.MM; appends an `open-pass` transition naming the requesting review's seq | `occupied pass`; `next pass not requested` (no single recorded review `request-next` naming 05.MM) |
| **K3 transition chain** | workflow successor record (`investigation.json`) | — | `transitions[]`: {seq, action, pass, prev, sha256, …facts}, hash-chained. Every commit must extend the previous list unchanged (prefix rule) | `history rewritten` |

- K1 also makes ordinary N7NN-local returns reviewable. Whether ordinary returns switch route is **not** decided here (06.07 D1).
- The existing N1NN `place-return` stays as it is.

**Smallest build slice for custody:** K2 + K3 + K1 in one workflow successor, on disposable books only (the existing live-book refusal is kept). `seal.json` keeps its meaning: the hash of the current record.

## 2. Four facts, kept separate (C02)
| Fact | What establishes it | What it does **not** establish |
|---|---|---|
| **return-byte identity** | sha256 and length of the exact bytes on the page (`05.NN.return.md`) = the K1 slot = the `seal-return` transition | anything about when those bytes were written |
| **seal identity** | the `seal-return` transition's `seq` and `sha256` in the chain | that the record was not rewritten wholesale outside the tool (Git history, committed by Prime, is the durable anchor) |
| **recorded transition order** | chain seq: `attach(05.NN)` < `seal-return(05.NN)` < `review(05.NN, request-next 05.MM)` < `open-pass(05.MM)`, with `attach(05.MM)` absent at check time | wall-clock order of sealing, preparation or reading |
| **declared exposure** | `reviewer_assignment` in each descriptor; `reviewer.exposure` and `exposure_added` in the blocks | that a person or model actually saw only that, or saw it at that time |

**Binding the informed stage.** The informed descriptor names:
- `first_return {pass, return_sha256, return_bytes, package_digest, seal_seq, seal_transition_sha256}`;
- the identical artifact cut.

The informed packet must carry the sealed first-return bytes and that descriptor. **What this proves:** the packet depends on those exact bytes and that recorded seal. Nothing more: not chronology, not exposure, not independent cognition.

**Any failure blocks attaching 05.MM:**
- `chain` (bad seq, prev or hash, or duplicate actions);
- `first-packet`;
- `first-not-sealed`;
- `missing-reserved-findings`;
- `stage-order`;
- `dependency`;
- `target-changed`;
- `identity`.

**Recorded, not blocking:** builder context not supplied; condition differences; reviewer-assignment changes.

**Reconcile keeps these visible:** unresolved findings with reasons, unique observations (origin reviewer or builder), agreements and disagreements, each as a list, never only a count.

## 3. Verifier boundary (C04)
**Launch readiness for either stage needs both verifiers, at one expected digest Prime binds at launch:**
1. **Full producer verify.** `labs/colab-support-pass02/colab_support.py` (pin below), run as `verify --output ABS --config ABS --json`. It must give `colab-support-report/2`, `command: verify`, `result: intact`, `findings: []`, and `digest` equal to the expected digest. This is the mechanical package check (prose rendering, section ranges, v1 rules, assembler verify, no pre-created return or review).
2. **Standalone handoff check.** `labs/colab-support-pass02/handoff_check.py`, run as `check --output ABS --expected-digest HEX --json`. It must give `result: valid`, with `trusted.digest` equal to the expected digest. **Only its `trusted` claims feed the reserved rules.**
3. **Both name the same investigation,** otherwise `identity-split`.

| Code | Meaning |
|---|---|
| `producer-not-verified` | wrong report kind |
| `producer-not-intact` | not intact, or there are findings |
| `digest` | either verifier's digest is not the expected digest |
| `handoff-not-valid` | the handoff check did not return `valid` |
| `identity-split` | the two verifiers name different investigations |
| `pin` | a tool hash differs (implementation) |

**A valid handoff alone is never treated as launch readiness** (test `test_handoff_valid_alone_is_not_enough`).

**Pins** (pack05.06, unchanged tools):
- producer v2 `colab_support.py` `2b720434ac4c4331835c1484b0eca362e01e8afbecde0ab800ca392530abf68b`, 53892 bytes (the Prime 05.03 freeze; recomputed here);
- `handoff_check.py` `7d62dde48165c5ac80f7f92a2a91f73a66b40c1e8dd2383f0269027038c6a268`, 27722 bytes;
- workflow pass02 `4a2ece9e646224468b36ce63947c739d8ecd73155fbb62fb34f0442cbd2dceec`, 47247 bytes (0708).

The reserved checker never edits or wraps these validators. It calls them and parses their output.

## 4. Mode expectation (C05)
**Every reserved-checker call names `--expect ordinary|reserved`:**

| `--expect` | descriptor in the packet | result |
|---|---|---|
| `reserved` | absent | **refuse** `reserved-expected-missing-descriptor` |
| `reserved` | present | reserved rules run |
| `ordinary` | absent | `ordinary-confirmed` |
| `ordinary` | present | **refuse** `descriptor-in-ordinary-job` |

- **Ordinary jobs need not call the checker at all.** No new universal gate is added.
- **An orchestrator that requested reserved mode must check `result == reserved-launch-ready-as-declared`,** not exit 0.

## 5. Parsing (C03)
**Parse view:**
- The raw return bytes are hashed as received.
- The parse view decodes strict UTF-8 (otherwise `encoding`), records and strips a leading BOM, and refuses a lone CR (`line-endings`).
- It converts CRLF to LF **for parsing only**.
- Exactly one block of the given name is required (`missing-…`, `duplicate-…`), holding strict JSON (no duplicate keys or non-finite numbers, otherwise `json`).

**Typed accessors:** every field goes through one, so a wrong type is a coded refusal (`type`, `enum`, `hash`, `keys`, `empty`), never a TypeError.

**Example:** LF and CRLF versions of the same return yield identical findings and different recorded raw hashes.

## 6. Data contracts (deltas from 05.05)
**`reserved-review/2`** (was `/1`): the same keys.
- `first_return` becomes {pass, return_sha256, return_bytes, package_digest, seal_seq, seal_transition_sha256}. The N1NN `member` and `receipt_sha256` are removed.
- `requirements` must have at least one entry.

**`reserved-findings/1` and `reserved-reconciliation/1`:** unchanged, and parsed through §5.

**The checker record** (05.05 §1.4) becomes a K3 transition fact, not a separate file. Optionally a `check` transition records {stage, result, digest, input hashes} through the workflow successor, which avoids a parallel status store.

## 7. Operator instructions (proposed; Prime operates)
1. **Prime names the trigger** (stuck or pre-release-testing). Otherwise use an ordinary Colab and stop here.
2. **Commit the descriptor `evidence/reserved05.NN.json`** (independent), with requirements, authority limits, builder context (also listed in `request.withheld`) and the cut. Prepare the package.
3. **Run producer `verify` and `handoff_check check`** at the launch digest, then `reserved_check launch --expect reserved`. Proceed only on `reserved-launch-ready-as-declared`.
4. **Launch** to a reviewer session. Record what is known; unknown stays unknown.
5. **On receipt:**
   - `seal-return-local` (K1) for 05.NN with the exact bytes and a declared transport note;
   - Prime records `06.NN.review.md` with route `request-next`, `next_pass` 05.MM, and findings not yet dispositioned;
   - `open-pass 05.MM` (K2).
6. **Commit `05.NN.return.md` and `evidence/reserved05.MM.json`** (informed, naming the seal transition). Prepare the informed package with the builder context and the sealed return.
7. **Run both verifiers**, then `reserved_check stage --expect reserved` **before** `attach 05.MM`. Proceed only on `informed-launch-ready-as-declared`.
8. **On receipt:** `seal-return-local` 05.MM, then `reserved_check reconcile`. The unresolved and unique lists go into Prime's `06.MM.review.md`, which is the ordinary review. The reserved result is evidence, not a verdict.

**Every lab or test execution of these steps uses a new run directory and deletes nothing (0708 F01).**

## 8. Missing compute, honestly
- **K1–K3** (custody, pass slot, recorded order) do not exist.
- **`reserved_check.py`** does not exist; only the pure-rule prototype does.
- **The descriptor is not packaged end to end** (H2), and the producer reads committed blobs only (0708 Factfind 6).
- **Nothing can detect undeclared exposure**, prove freshness or authenticate a model.
