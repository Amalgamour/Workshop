# Failure rules — return-lines pass02

A refusal keeps the bytes it has already written. Nothing is deleted to obtain a later success. Exit 0 is a finished command on that invocation. It is not acceptance, seating, publication, or live authority. Exit 1 is reserved or incomplete. Exit 2 is a refusal or a byte conflict. Exit 3 is an interrupted phase: the completion marker was not written.

Successor refusals name `0521.return-placement/05.04` in the correction. Forwarded pass01 commands keep pass01's own envelope, including its 05.03 escalation sentence, because pass01 produced that envelope.

## Authorization

| Condition | Result |
|---|---|
| Mutating command on the live work book | exit 2, check `live book`, no layout file written |
| Authorization names the live path | exit 2, check `live book`, even if executor is Codex Prime |
| Door-marked book and no authorization | exit 2, check `live book` |
| `synthetic` is not boolean true | exit 2, check `return-line-authorization/1` |
| Executor is not `Codex Prime` | exit 2. The builder's own name is not permission |
| Release text differs from release.txt | exit 2 |
| Book path, book name, operation, audit hash, audit length, plan hash, or layout hash differs | exit 2, no success marker |
| A root is inside the book, inside the live book, contains the door, or overlaps another root | exit 2 |
| Book without the door, not the live book, forwarded pass01 command | pass01's own rule. New reconstruct, publish, retire, and their rollbacks still require authorization |

## Phase refusals

| Condition | Result |
|---|---|
| Audit route or target return disagrees with `compute_route` | exit 2, check `audit identity`, no retirement |
| Source files differ from the audit, or a source member is missing | exit 2. Stage may have copied the stale bytes as evidence. The marker is not written. The live tree is not the thing that was flipped |
| Page-local tail missing or different from the member return | exit 2, check `N7 tail`. The tail is not overwritten and no return is invented |
| Verified record fails the pinned reader, or a present return fails the reader | exit 2, check `sealed reader` |
| `0154` has no return.md | not a failure. State stays `incomplete`. No return.md is written |
| Reconstruction or publication file already exists and its bytes differ | exit 2, `reconstruction bytes differ` or `publication bytes differ`. The partial file stays |
| Occupant of a destination is not one of the staged sources | exit 2, check `occupied-line`. It is not overwritten |
| Retired or displaced destination already exists | exit 2, check `occupied-archive`. It is not overwritten |
| Old member name equals the logical target page | exit 2 before any retire move |
| Backup, staging, or retired hash no longer matches its journal | exit 2. Rollback stops. Evidence stays |
| Rollback destination slot is already occupied | exit 2. The retired copy stays |
| `adopt`, `adopt-resume`, `rollback-adopt` | exit 2, check `successor command`. Those commands are not forwarded |
| Interrupt budget exhausted | exit 3. Journal saved. Marker absent. The same roots can resume |
| Partial test write | exit 3. Short bytes stay. Resume on that root exits 2 and does not delete them |
| Pin of pass01, placement, or reader mismatches | exit 2 before a book write. The successor writes nothing |

## What is not claimed

No power-loss, race, or sandbox result is claimed. An interrupt is a counted stop in the tool, or a test fault that writes a short file and then raises after that write has closed. A cross-device rename stops with the filesystem error. The tool does not copy-then-delete as a fallback.
