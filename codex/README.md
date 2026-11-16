# Workshop build preparation

State: working handoff for the Director. Build preparation, 2026-11-11.

axioms: 1.4.5.6.7.8.9

Workshop preserves the reasons behind decisions in a persistent, human-inspectable record. A book stores Markdown faces in an append-only JSON Lines log. SeqAddr identifies pages, faces and cards. Face 04 preserves the explanation and `why:` that let a person inspect a choice and a future builder recover its reasoning.

## Read before building

| Source | What it governs or provides |
|---|---|
| [AGENTS.md](../AGENTS.md) | Workshop brief, authority, storage goals, and Next.js UI requirement |
| [Axioms.md](../Axioms.md) and [decisions.md](../decisions.md) | Current axioms and numbered decisions. Check each entry's status. |
| [seqAddr.md](../seqAddr.md), [format.md](../format.md), [brands.md](../brands.md), [drafting.md](../drafting.md), [Design.md](../Design.md) | Applied geometry, book format, meanings, change process, and component boundaries. Resolve discrepancies against the numbered decisions. |
| [agents.003.md](../agents.003.md) | Proposed agent brief and first-build scope. The root `AGENTS.md` governs. |
| [kernel-design.md](../kernel-design.md) and [workflow-loop.md](../workflow-loop.md) | Proposed kernel and draft workflow. Consult E8/E9 and the workflow review before deriving implementation rules. |
| [review.md](../review.md) | Historical condensation review. Some path and version references describe an earlier branch layout. |

The current axes are `DD.SS.BB.PPPP.FF` with widths `2.2.2.4.2`. A counter is an optional part after the face. A title is a checked label, and a tail records state according to its position. The physical export is one `DD.SS.BB.book` per container. Read the grammar in `seqAddr.md` §8 and the title, tail and card rules in A2 and C8.2 together.

## First build proposed in `agents.003.md`

The Rust core is the first slice because address parsing and log replay can be checked independently and reused by Compute and the reader. Compute later owns canonical writes. The Next.js reader uses the same core through WebAssembly. Agent clients submit proposals to Compute. This handoff is prepared for an explicit build start.

| Check | Evidence to produce | Source |
|---|---|---|
| Parse and expand addresses | Parse `10.11.21.1001.04`. With active book `10.11.21`, expand `1001.04` to the same address. Reject `1001.4`. Resolve `.04` with exactly one active page and report ambiguity when multiple pages are active. | A1.1–A1.7, `seqAddr.md` §§2, 8 |
| Replay the book | Read the `seqbook` header and replay `put` and `tail` entries. Reject a stale `from` state. Recover the valid prefix when the last entry is partially written. Exercise tail changes using a counted-face example. | `format.md` §§3.1–3.3, A4.4 |
| Append through the writer API | Exercise appending to a disposable book through the Rust writer API, then reopen and compare the replayed state. The first slice exercises the API boundary. Production ownership belongs to Compute. | `agents.003.md` first build, `format.md` §§1.2, 3 |
| Read the why in a text editor | Prepare `10.11.21.book` with identity page `0000` and page `1001` stamped `timer`. Include faces `00`, `01` and `04` on `1001`, with a shared `purpose` card key on `01` and `04` and a `why:` and explanation on `04`. Give the identity page a content face to satisfy C1.1. | A2.8, A3.1, C1.1, C2, C3, `agents.003.md` first build |

`7` Before generalizing the writer, reconcile how boards are derived versus validated (`format.md` §§3.3, 4.1 and A4.4), how multi-entry writes become visible together (C1.1, C3.2, A5.3), and the recovery contract for appending after a partial final record. The fixture should distinguish valid replay, recovery of an interrupted final append, and malformed history. Proposal batching, drafting operations, full workflow transition policy, and cross-book links need their own agreements before production writes depend on them.

`7` Keep hardware, client transport, snapshot/archive policy, fork reconciliation, the kernel bootstrap, and the read path open. `format.md` §§2–3 records the choice of JSON Lines and why SQLite remains a fallback. No hardware selection is needed for the first core fixture.

## Next work

1. Review [workflow `.003`](../workflow-loop.003.md) and its [drafting notes](../workflow-loop.003-notes.md). [Decision F.1](../decisions.md#f1-approval-record-for-s01s12) records S01–S12. F.2 and the `7` items in `.003` remain for review. See the [`.002` review](workflow-loop-review.md) for the predecessor findings.
2. Review the first-build frame and confirm when implementation starts. The parser and replay checks can be specified using settled sources while the workflow decisions are pending.
3. Once building starts, return the exact changed paths and revisions, test commands and results, and the fixture for human inspection. Record unresolved choices with their source and why.
