# Prime review — 0510.colab-tools / 05.05
Date: 2026-11-01. Reviewer: Codex Prime.
Disposition: useful design proposal; correction required before implementation release.

## Alignment and verified evidence
The proposal reuses two existing N7NN passes on the same page, an optional digest-bound descriptor, and structured findings/reconciliation blocks. This preserves ordinary contextual Colabs and avoids a parallel producer. That is a promising fit for 0411's reserved stuck/readiness method, not a deployed capability.

Independently verified 32 source rows against snapshots and live bytes and all 31 artifact rows: no mismatches. Independently ran the pure prototype suite on Python 3.12.14: 31 tests passed. Read the contract, impact map, acceptance plan, submission, notes and new rule prototype; compared with 0708's accepted capability audit. Prototype results are not real capture/workflow integration.

## Findings
C01 — N7NN custody regression. CONTRACT stage/reconcile interfaces use --member 01NN.*, and the submission explicitly anticipates two N1NN reservations. The Director's existing rule is N5NN -> matching N1NN, while N7NN keeps 05.NN.pack, 05.NN.return and 06.NN.review locally. Revise the proposal to that rule. Existing capture/inspector limitations may require a bounded page-local sealing connector; expose that missing mechanism instead of silently moving Colab returns into N1NN. Retain any legacy captures as history, not a precedent for new routing.

C02 — Hash dependency is overstated as chronology. Carrying first-return bytes proves a dependency on those bytes. By itself it does not prove they were captured/sealed before package preparation, or prove when a human/model saw builder context. Bind and validate the specific seal/receipt and prior packet, preserve recorded transitions, and state actual exposure as declared. Even receipt dependency alone is not proof of wall-clock order or hidden exposure. The prototype currently checks return hash but not the proposed receipt equality. No claim of independent cognition follows.

C03 — Reproduced CRLF format defect. The same synthetic findings block is accepted with LF but rejected as missing-reserved-findings with CRLF. Parse using a newline-aware view while hashing and preserving the original raw bytes. Add malformed-type, duplicate and missing-block tests in the later implementation. Current prototype is nonproduction and must not be silently repaired in its sealed pass.

C04 — Verifier capability boundary. The standalone handoff checker explicitly does not re-render prose, recheck all v1 request rules, or rerun custody checks. The contract must retain the full producer verification requirement for launch readiness, or explicitly label its own narrower check and require prior full verification. A narrow valid handoff is not full mechanical approval. Retain expected digests and pins at both boundaries.

C05 — Ordinary result versus requested reserved job. A missing descriptor can legitimately yield ordinary for an ordinary job. The orchestrator must not accept that result as readiness when it requested reserved mode. Add an explicit expectation/contract comparison and a missing-descriptor negative for that route.

## Assumptions reconciled
H1: source-map roles are present in current checker outputs and source; 0708 independently confirmed package identity checks. H2: evidence-descriptor packaging remains an end-to-end untested assumption; use a disposable local repository in a later explicitly scoped lab, with no project Git mutation, push or network. H3: 0708 did not exercise second-pass open/request-next, so it stays unproven. H4: the existing inspector's N1 member route is not proof of a legal N7 page-local seal route. H5: block compliance remains an empirical model limitation, and C03 adds a concrete parser issue. Do not convert any of these into acceptance by assertion.

## Next bounded action
Revise the design on a new version to address C01–C05 before a checker implementation pack. Keep the two-pass reuse idea and ordinary-mode compatibility. Incorporate 0708 F01's unique run-directory requirement into future lab instructions. Do not assign the implementation until the custody dependency and verifier contract are explicit. The known N7 routing rule needs no new Director choice; if satisfying it requires a design fork, elevate that fork before building.

No app change, implementation release, custody receipt, fresh reviewer proof or kernel seating is granted. Original return/prototype files are preserved. Evidence: evidence/prime-review05.05/.
