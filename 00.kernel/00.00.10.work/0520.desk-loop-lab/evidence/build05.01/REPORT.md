# Report — independent desk-loop replay

Date: 2026-10-31. Recorder: Grok-2. Synthetic work, disposable books, no model. This report does not adopt the loop.

## Did

The lab called the existing clerk, capture-handoff, return-capture, and prime-cycle CLIs in new processes. Judgment sentences were supplied by `labs/desk-loop-replay-pass01/replay.py`. The live book was not used as a fixture.

`python -B labs/desk-loop-replay-pass01/test_replay.py` from `D:\Git\lib-build` ran 1 test, 16 checks, 0 failed, 0 skipped, 8.435s, exit 0. The raw transcript is `evidence/build05.01/transcript.json`.

On the supported path the clerk claim reported usable instructions. Handoff capture exited 0. A new-process read before any review showed `awaiting-review`, custody `present`, role `primary-current-candidate`, pass terminal `unknown`, and no next action. A supplied held judgment recorded. The next process showed `reviewed`, disposition `held`, pass `open`, goal `open`, and next action `pack-correction`: "Pack one bounded correction for the synthetic piece." `elected` stayed null.

## Stage table

| Stage | Observed result | Class |
| --- | --- | --- |
| Clerk queue of a supplied job | exit 0 | existing |
| Clerk claim and show of the instruction hash | exit 0; `checks.instructions` usable | existing |
| Job file, instruction file, and `piece.txt` | written beside the disposable repo | lab glue |
| Clerk return | exit 0 | existing |
| Reserve and `handoff.py perform` | exit 0; later read saw the member | existing |
| Disposable `05.01` page, Return pointer, and registration | written by this lab; no tool builds them | lab glue |
| New-process read before review | exit 1; `awaiting-review`; custody present; next action null | existing |
| Record a held judgment | exit 0; stdout begins `recorded` | existing check; supplied words are glue |
| New-process read after that record | exit 0; held; pass open; goal open; next action recovered | existing |
| Page bytes changed after the review | exit 1; `review-stale`; current next action null; the old action kept as historical | existing |
| Record with the old template | exit 2; `refused: source changed since read: source` | existing |
| Clerk job returned and no member reserved | show state `returned`; book has the lane and no `01xx` member; read `no-return`, custody `absent`, both terminals `unknown` | existing read; the sentence "the worker says this assignment is done" is glue |
| Accepted judgment with no receipt | exit 2; `refused: an accepted review needs a bound captured return`; no review directory | existing |
| Same clerk delivery, actor, token, evidence, and bytes | exit 0; `already-recorded job-repeat`; event file unchanged | existing |
| Same handoff binding again | exit 0; `writes none`; `result ok`; receipt bytes unchanged | existing |
| Same clerk delivery with different artifact bytes | exit 2; `refused: delivery conflict`; event file unchanged | existing |
| Same capture submission with a different return file | exit 2; `conflict submission loop-repeat`; receipt bytes unchanged | existing |
| Instruction file changed after queue, then claim | exit 2; `refused: instruction hash mismatch`; `0002.claimed.json` absent | existing |
| Supplied director-input question, then a new-process read | record exit 1 and stdout begins `recorded`; hold `H1` status `unresolved`; the question string is in `unresolved`; pass open; goal open; `elected` null | existing cycle; the question words are glue |
| `return_capture.py capture` of identical bytes (`already-captured`) | not invoked; the handoff retry does not call capture again | unverified |
| `inventory.py`, `worker_bridge.py`, app tests, link races | not run; AR-01 stays held | blocked |
| `0519.desk-app/05.01.md` text | hash checked, text not read | blocked for this lane |
| One tool that writes the live page, the pointer, and the registration from a clerk job | no such command was found | missing |
| A model judgment or a fresh-model restart | not called; process restart only rereads files | missing by design |

## What remains manual

Prime still supplies the finding, the disposition, the pass terminal, the goal terminal, and any question. This lab typed those words. `prime_cycle.py record` checks the shape and calls `prime_review.py report`. It does not decide that the work is right.

The work-book page on a real desk is still model-written. In this lab the disposable page was glue. `REVIEW.md` inside a committed cycle review is compute: it is the readable projection of `record.json`, and `COMMITTED.json` is written last. The template's empty judgment fields are compute. Filling them is the supplied judgment.

`elected` stayed null on every view. The recovered next action is stored text. Nothing queued a new clerk job from it.

## Blocked

The modules stay unreviewed. A receipt and the 16 checks do not accept, release, or publish this work. AR-01 stays held, so the app bridge and inventory were not exercised. Claude's `0519` page was not read. At the opening pin check it matched snapshot `9b99e4b3e6bcfb6c3aa7ee1eeb1aeed2b590bcbe55ed940629457d7dc351ee4c`, 8300 bytes. When this report was written the live file was `69db85b719c42ad6549cc2369226c6c059c987513a8e00871444d801a4cd390b`, 9941 bytes. This lane did not edit it and did not restore it. The other 52 pack sources still match. This builder did not commit. Workshop HEAD while this report was written is recorded in `verification.json`.

## Need

The smallest next implementation pack is one page and one disposable-or-draft target: given a verified receipt and a page path, compute writes the Return pointer's member and receipt lines and writes one `prime-cycle-registration/1` row, then stops. Prime fills only the decision template. The pack does not build a universal face builder, does not dispatch a worker, and does not treat the receipt as acceptance.

Director decision: whether that pack may write those pointer lines on a live draft page while `Review — Codex Prime` stays `PENDING.` The release sentence on a live pointer stays the Director's own sentence. This lab wrote a synthetic pointer only inside a temporary book.
