# submission — 0510.colab-tools/05.06 corrected reserved Colab support design
date: 2026-11-01
who: claude-opus-5-5 (Claude), informed design author; reviewer Codex Prime
notes: 06.07.md · evidence: evidence/design05.06/ · lab: colab/labs/0510-reserved-review/pass02/ (nonproduction)
state: design correction. No existing tool, prior design, pass01 or source changed. No Git write, repository, capture or workflow side effect.

## Did
- **Inputs.** Verified pack05.06 by compute: 75 of 75 snapshots match their pins and equal live. Recorded the invocation and claim on the 05.06 pointer and in 06.07.md.
- **Read** Prime's 05.05 review (C01–C05, H1–H5) and its check script, and Grok-1's 0708 return with its review (F01–F04).
- **Source-inspected the actual custody and verifier APIs** before any probe (06.07 S1–S7):
  - workflow `place-return` is N1NN-only;
  - `record-review` needs a filled return slot;
  - no command creates a second pass slot on a page;
  - `seal.json` keeps no history;
  - the producer `verify` report shape;
  - the source of the CRLF defect.
- **Revised the design** (`CONTRACT.md` v2): page-local custody with three named missing connectors (K1 `seal-return-local`, K2 `open-pass`, K3 transition chain); four separated facts; two-verifier launch; a required `--expect`; a parse view; descriptor `/2`.
- **Built a new nonproduction prototype** (`pass02/`): `reserved_rules2.py`, `workflow_model.py`, `examples.py`, `test_rules2.py` and `run_probe.py`, the last creating a unique run directory for every execution.
  - **Run 1** (`runs/20261101T203634Z-8fb571`): P1 re-observed the pass01 CRLF failure; P2 had 1 error, from my own fuzz test, which I kept.
  - **Run 2** (`runs/20261101T203654Z-84a6ef`): 51 of 51 OK.
- **Wrote** `CHANGES-AND-LEDGER.md` (C01–C05 account; H1–H5 ledger), `IMPACT-MAP.md`, `ACCEPTANCE.md` (what ran, plus an exact later integration plan), `EXAMPLES.md`, `verification.json` and `artifact-manifest.json`.

## Blocked
- **Integration is unproven:** H2 (descriptor packaging), K1–K3 and the real checker. This needs a disposable repository and books, which were outside this pack's scope. The exact plan is in `ACCEPTANCE.md` §Planned.
- **Ordinary N7NN returns still route through N1NN** in the accepted workflow (06.07 D1). I did not change or decide that.

## Need
- **Prime: confirm D1's scope.** The N7NN-local rule applies to the reserved pair here. Do ordinary workflow N7NN returns also move to K1? The Director-verbatim source for the rule is not in pack05.06; exchange-layout CONTRACT.002 labels its N1NN custody text as Prime's interpretation.
- **Prime: release the next slice** (below) and its disposable-repository permission for H2.

## Contract delta (summary; full text `CONTRACT.md`)
**C01:**
- No N1NN for the reserved pair.
- K1 seals a supplied return page-locally with exact bytes (identical replay is a no-op; different bytes refuse).
- K2 opens 05.MM only when a recorded review `request-next` names it.
- K3 is an append-only, hash-chained transition list inside the page record, with a prefix rule.
- Descriptor `/2` names the seal transition, not a member or receipt.

**C02:**
- **Return-byte identity, seal identity, recorded order and declared exposure are kept separate.**
- **The informed stage binds** the first package digest (as attached), the seal seq and hash, the return bytes and length, and the identical cut.
- **Any failure blocks attaching 05.MM.**
- **Results state `not_proved`:** wall clock, exposure time, and wholesale rewrite outside the tool.
- Unresolved findings, unique observations and disagreements are listed.

**C03:** strict UTF-8; BOM recorded; lone CR refused; CRLF→LF for parsing only; raw bytes hashed; typed accessors (no TypeError escapes).

**C04:** launch needs producer `verify` (intact, no findings) **and** handoff `valid`, both at the expected digest and naming the same investigation. The pins were recomputed: producer 2b720434…, checker 7d62dde4…, workflow 4a2ece9e…. Handoff valid alone refuses.

**C05:** `--expect ordinary|reserved` is required.
- Reserved with no descriptor refuses.
- A descriptor in an ordinary job refuses.
- Ordinary jobs need not call the checker, so there is no universal gate.

## Operator instructions
Eight steps, in CONTRACT §7.

## Focused verification
- Run 2: **51 of 51** in 8 groups (ParseView, Types, Mode, Verifier, Launch, Stage, WorkflowModel, Reconcile).
- Raw stdout, stderr, exits and the interpreter are in each run's `run.json`.
- The source check at the end is in `verification.json`.

## Exact changes
**New:**
- `06.07.md`;
- `evidence/design05.06/*`;
- `colab/labs/0510-reserved-review/pass02/*`.

**Edited:** the 05.06 pointer only.

**Not edited:** everything else, including pass01, design05.05, the producer, checker, workflow, app and kernel.

## Limits
- Pure functions and an in-memory model only. No real workflow, producer or checker integration.
- The examples imitate verifier output shapes.
- Undeclared exposure, freshness and identity stay undetectable.
- Block compliance by real reviewers is unmeasured (H5).
- **The page-local seal is internal consistency, not tamper-proofing.** Prime's Git commit is the durable anchor.

## Factfind (opinion lives here only)
- **The custody correction exposed a wider gap than the reserved method.** The accepted workflow has no page-local return route at all, so under the N7NN-local rule even an ordinary N7NN return cannot reach `record-review` without an N1NN member. K1 fixes both, which is why it belongs in the workflow successor and not in a reserved-only tool.
- **H3 was not merely unproven; the source shows it false.** The 05.05 two-pass plan could not have run on the current workflow.

## Hostile
- **K3's hash chain proves only that the record is consistent with itself.** Someone rewriting `investigation.json` and recomputing the chain defeats it. Only the prefix rule at the next write through the tool, and Git history, catch that.
- **`declared_transport` is text a person types.** It must not be read as provenance of the reviewer.
- **The fuzz test's accepted-substitution list is a design decision:** for example, an empty builder context is allowed. Prime may want an empty builder context to refuse in reserved mode, since the second pass then has nothing to disclose.
- **The CRLF fix accepts mixed endings.** A deliberately mixed file still parses. That is intended, but noted.

## Overflow (parked)
- D1 for ordinary N7NN returns.
- A workflow `show` that lists K3 transitions.
- 0708 F03 `review_pending` wording.
- The producer's stale `NOT_CHECKED` sentence (0708 F04). Not touched.

## Unprompted
- **Consider making an empty `builder_context` a refusal under `--expect reserved`.** A reserved pair with nothing withheld is an ordinary Colab done twice.

## One next bounded implementation slice
**Workflow pass03 with K2 `open-pass`, K3 transitions and K1 `seal-return-local`,** on disposable books only:
- with pass02 behaviour and the live-book refusal kept;
- with ACCEPTANCE §Planned item 2 as its tests.

**Why first:** it closes the custody and ordering gap that both the reserved checker and N7NN-local ordinary returns depend on.

**Then:** `reserved_check.py` can be built against a real record, and H2 can be proven in a disposable repository.

One thing I would write differently: the 05.05 contract should have started from the workflow's slot-creation code. Reading `fresh_record` first would have shown H3 false before the design depended on it.
