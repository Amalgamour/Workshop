# CONTRACT (proposed) — reserved two-pass support for the existing Colab tools
date: 2026-11-01 · who: claude-opus-5-5 (Claude), informed design author · state: design proposal for Codex Prime; not implemented, not released, no new law

Policy source: 0411/01.003 §Reserved two-pass investigation; Director decision 0411/06.03.
Current-API citations: 06.05.md A1–A5.
The rule prototype is `colab/labs/0510-reserved-review/pass01/reserved_rules.py` (nonproduction).

## 0. Shape of the extension
**Use two existing N7NN passes on one investigation page, not stage files inside one pass.**

| Stage | Pass | Packet | Return | Review |
|---|---|---|---|---|
| independent | `05.NN` | reviewer packet = an ordinary v2 package whose required sources include `evidence/reserved05.NN.json` | `05.NN.return.md`, the exact captured bytes, containing one `reserved-findings` block | `06.NN.review.md`, route `request-next` with `next_pass: 05.MM`. Findings are not dispositioned yet; findings may be `[]` |
| informed | `05.MM` (MM > NN) | builder-context packet = an ordinary v2 package whose required sources add the builder-context files, the sealed `05.NN.return.md` bytes and `evidence/reserved05.MM.json` | `05.MM.return.md` with one `reserved-reconciliation` block | `06.MM.review.md`: Prime's ordinary dispositions (adopted, held …) with Director replies |

**Why two passes rather than stage files inside one pass:**
- **The workflow already refuses a second return or review under an occupied pass** (A4). Capture already seals a submitted return (A5).
- **`request-next` already links passes.** The informed packet carries the first return's exact bytes as a source, so the package digest itself proves the second packet was built after the first return existed.
- **Nothing gets a new address axis, face, tail, status store or gate.** The stage files named in 01.003 ("may live under the same pass's evidence directory") are then just the per-pass descriptor and the checker's record.
- **Rejected alternative:** a single pass with `05.NN.stage1/stage2` files. It needs a second return body per pass, which the workflow forbids by design (X02 in Prime review 05.03), and its own sealing.

**Ordinary Colab is untouched.** No producer, checker or workflow behaviour changes. A pass without a descriptor is ordinary. The new checker answers `ordinary` and checks nothing (test `test_ordinary_has_no_descriptor`).

## 1. Data contracts (all NEW, versioned, optional)
### 1.1 `reserved-review/1` — launch descriptor (Prime-authored)
- **Location (fixed):** `<desk>/<book>/<page>/evidence/reserved05.NN.json` for pass `05.NN`.
- **How it travels:** it is committed, then listed in the request's `required_sources` with role text `reserved-review descriptor`. It is packaged as an ordinary snapshot and bound by the launch digest. The checker finds it through `trusted.source_map` (A3).
- **Exact keys:**

| Key | Meaning | Compute can check | Only declared |
|---|---|---|---|
| `schema` | `reserved-review/1` | exact value | |
| `investigation` | {book, page, pass} | equals the package investigation | |
| `stage` | `independent` or `informed` | enum; order (§3) | |
| `first_pass` | null (independent) or `05.NN` (informed) | earlier pass on the same page | |
| `first_return` | null or {member, return_sha256, receipt_sha256} | return hash equals the capture and the packaged bytes (receipt equality proposed; the prototype checks the return hash) | |
| `trigger` | {kind: `stuck`\|`pre-release-testing`, named_by, statement} | present and non-empty; enum | whether the work is really stuck or ready |
| `question` | the bounded question | non-empty (proposed; the prototype does not check it yet) | |
| `artifact_cut` | {repository, commit, targets[{id, path, sha256, bytes}]} | present; equals the package binding and target snapshots; equal across stages | |
| `environment` | {os, python, relevant, …}: text or `unknown` | differences between stages are listed | whether the environment is relevant |
| `requirements` | [{path, sha256, why}]: authoritative requirement sources | each is in the packet (path and hash) | whether the list is complete |
| `authority_limits` | [{path, sha256}] | each is in the packet (`authority-missing`) | whether the limits are complete |
| `builder_context` | [{path, sha256, kind: reasoning\|notes\|return\|chat}] | absent from the independent packet by path **and** bytes; each named in `request.withheld`; present in the informed packet, or listed as not supplied | whether undeclared context leaked |
| `unavailable` | [{item, reason}] | shape | |
| `reviewer_assignment` | {model, family, session: new\|continuing\|unknown, prior_involvement}; text `unknown` allowed | enum; `continuing` cannot be independent | the truth of every value |
| `builder_identity` | {model, family} | used only to state `same_family_declared` true/false/unknown | |

### 1.2 `reserved-findings/1` — first-pass findings (reviewer-authored, inside the return)
- One fenced block ```` ```reserved-findings ```` in `05.NN.return.md`, holding strict JSON: `{schema, stage: "independent", reviewer{model, family, session, prior_involvement, exposure[]}, findings[{id: R01–R99, claim, evidence[]}]}`.
- The block is read from the exact captured bytes. Nothing is edited or extracted into a second editable copy.
- The rest of the return is free prose, as today.

### 1.3 `reserved-reconciliation/1` — informed reconciliation (reviewer-authored)
- One block ```` ```reserved-reconciliation ```` in `05.MM.return.md`: `{schema, stage: "informed", reviewer{…}, exposure_added[], dispositions[{finding, status, reason, evidence[]}], agreements[], disagreements[], unique[{id: U01–U99, origin: reviewer|builder, observation, evidence[]}]}`.
- `status` ∈ {confirmed, withdrawn, different-conditions, unresolved, out-of-scope}. Every status except `confirmed` needs a reason.

### 1.4 `reserved-review-record/1` — the checker's output (append-only)
- Emitted on stdout. With `--record ABS` it is also written by exclusive create, at `<page>/evidence/reserved05.NN-05.MM.record.json`.
- An identical replay is a no-op. Different content at an occupied path is refused, and the existing file is kept.
- It contains: inputs by hash (both package digests, both descriptor hashes, the member, receipt and return hashes), the launch, stage and reconcile results, the condition differences, the reviewer-assignment changes, and `not_established` (the truth of findings, acceptance, independence of errors, authenticated identity).
- **It is not a status authority.** The workflow's pass flags remain the record of finish, hold or next.

## 2. Connector: one NEW read-only checker
`labs/colab-reserved-pass01/reserved_check.py`, standard library only. It is not a producer and imports no producer or workflow code.

```text
python -B reserved_check.py launch    --output ABS-OUT --expected-digest HEX --json
python -B reserved_check.py stage     --first-output ABS --first-digest HEX --output ABS --expected-digest HEX
                                       --book ABS --member 01NN.slug --json
python -B reserved_check.py reconcile --book ABS --first-member 01NN.a --second-member 01NN.b
                                       [--first-output ABS --first-digest HEX --output ABS --expected-digest HEX]
                                       [--record ABS] --json
```

**Inputs come only from existing verifiers:**
- Package claims come from the pinned `handoff_check.py check` (`trusted`, digest-anchored; A3), run as a subprocess after its hash is checked.
- `package/colab-request.json` and `package/binding.json` are read only after their bytes are confirmed bound (`binding_sha256`; the request file hash in `envelope`).
- Capture status and origin come from the pinned `return_inspect.py`. The return bytes are read from the member and must equal its manifest hash.

**Exits:** 0 for `ordinary`, `launch-ready-as-declared`, `informed-launch-ready-as-declared` and `reconciled-as-declared`. 1 for `incomplete` (undispositioned findings). 2 for a refusal, with the codes in §3. Never a traceback.

**Not included:** no model call, no package preparation, no capture, no workflow write, no live-book write, no review writing.

## 3. Rules and refusal codes (prototype `reserved_rules.py`)
**All commands** (checker level, not in the rule prototype):
- `package-unverified`: `handoff_check` did not return `valid` for the expected digest. No trusted claim is used.
- `pin`: a pinned tool's hash differs.
- `descriptor`: the descriptor path appears twice or with a role other than `required`.

**`launch`** (independent stage):
- `ordinary`: no descriptor.
- `version`: wrong schema.
- `no-trigger`: trigger absent or empty.
- `identity`: the investigation differs.
- `launch-unready`: the cut, commit or a target hash was not supplied.
- `cut-mismatch`: the cut differs from the binding or the target snapshots.
- `requirement-missing`, `authority-missing`.
- `context-in-first-packet`: a builder-context path **or bytes** appear in the packet.
- `withhold-undeclared`: builder context not named in `request.withheld`.
- `not-fresh`: `session: continuing` labelled independent.

On success the label is `independent-fresh-declared` or `independent-freshness-unknown`, plus `same_family_declared`.

**`stage`** (informed stage):
- `stage-order`: not later than, or not naming, the first pass.
- `first-not-sealed`: the capture is not complete or has the wrong origin, the descriptor names other bytes, or the bytes differ from the capture.
- `missing-reserved-findings` / `duplicate-reserved-findings`.
- `order`: the informed packet does not carry the sealed first return.
- `target-changed`: refused as "new comparison".

**Recorded, not refused:** `builder_context_not_supplied`, `condition_differences`, `reviewer_assignment_changed`.

**`reconcile`:**
- `unknown-finding`, `duplicate-disposition`, `status`, `reason`, `unique`, `json` (duplicate keys or non-strict JSON), and missing or duplicate blocks.
- Undispositioned findings give `incomplete`.
- The result counts dispositions, agreements, disagreements and unique observations. It never ranks or votes them.

**Already enforced by existing tools (re-test only, no new code):**
- a second return or review under an occupied pass (workflow `occupied different content`);
- an edited captured return (capture verify / hash conflict);
- a review before any return (`review before return`);
- `finish` with unresolved findings (`unresolved findings`).

## 4. What compute verifies, and what it only records
| Verified mechanically | Only recorded as declared or observed |
|---|---|
| descriptor bytes bound by the launch digest | that the reviewer session was fresh |
| the same artifact cut in both stages | model identity, family, training independence |
| builder context absent from the first packet (declared items, by path and bytes) | that no *undeclared* context reached the reviewer (chat, memory, other files) |
| first findings sealed (complete capture) before the informed packet existed (hash dependency) | what the reviewer actually read (`exposure`, `exposure_added`) |
| every first finding has one disposition; reasons present | whether a disposition or finding is correct |
| environment and reviewer-assignment differences between stages | whether a difference matters |

## 5. Optional later deltas (not in the first slice)
1. **Producer v3** (`colab-request/3` = `/2` plus an optional `reserved` object mirroring the descriptor; digest domain `/3`). It would render the trigger, exposure and block templates into ENTRY and the return template. This avoids instructing the reviewer through `method` text. It needs handoff_check `/3`. Defer it until slice 1 has been used once.
2. **Workflow:** an interim review for `request-next` with findings `[]` works today (A4). If Prime wants per-finding interim holds, the `director_reply` requirement (1064–1067) forces text even when no Director reply exists; the existing practice ("not needed as explicitly supplied") applies. No change is proposed.
3. **A `show` view** in the workflow listing the reserved record for a page. Defer it.

## 6. Assumptions for Prime to reconcile with Grok-1's 0708 audit
- **H1.** `handoff_check` trusted `source_map` roles (`target`/`required`) are stable for v2 packages (probe P1 shows them).
- **H2.** A JSON file committed under `<page>/evidence/` is a valid `required_sources` path for the producer. This was not probed, because preparation needs a commit.
- **H3.** The workflow `open` and `attach` accept a second pass `05.MM` on an existing page after `request-next`. Read from the source (`fresh_record`, pass slots); not exercised.
- **H4.** The inspector exposes the member's return sha256 and origin in the form the checker needs (exchange05.03 intake uses it).
- **H5.** A reviewer can reliably emit a strict-JSON fenced block. If not, the reconcile result is `incomplete` or a refusal. That is a format failure, not a finding.
