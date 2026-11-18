# Failure rules — return-lines pass04

A refusal keeps the bytes it has already written. Nothing is deleted to obtain a later success. Exit 0 is a finished command on that invocation. It is not acceptance, seating, publication, or live authority. Exit 1 is reserved or incomplete. Exit 2 is a refusal or a byte conflict. Exit 3 is an interrupted phase: the completion marker was not written.

Pass04 refusals name `0521.return-placement/05.06` in the correction. Fixture refusals that pass02 itself produces keep the 05.04 sentence. Forwarded pass01 envelopes keep the 05.03 sentence when pass02 did not wrap them. Pass03's own veto sentences are not reused.

## Authority

| Condition | Result |
|---|---|
| Authorization path empty or missing, including on the canonical book | exit 2, check `authorization`, reason `authorization is absent`. No layout file is written. |
| Schema not one of the three records | exit 2, check `authorization`, reason `authorization schema is not a known record` |
| Canonical book, or a record whose `book_path` is that identity, with `return-line-authorization/1` | exit 2, check `return-line-authorization/1`, reason `fixture authorization cannot authorize the canonical book` |
| Ordinary door-marked copy and `return-line-authorization/1` | pass02's fixture rules. A pass02 failure keeps the 05.04 sentence. |
| `return-line-recorded-release/1` and `synthetic` is not false | exit 2, check `return-line-recorded-release/1`, reason `synthetic fixture is not a recorded release` |
| Recorded schema, `synthetic` false, and every CONTRACT precondition matches | Same result for a copy and for a canonical identity. No designation call. Preflight exits 0, check `readiness`, `mutated` false, `executed` false, `live_execution` false, and creates nothing. A mutation command may then create the three roots and run that one operation. |
| Candidate schema, including `active` true, on a copy or on the canonical book | exit 2, check `return-line-release-candidate/1`. Reason `candidate is not authority`, or `candidate claims active authority` when `active` is true. No directory is created. |
| Release file bytes differ from `release_sha256` or `release_bytes` | exit 2, check `return-line-director-release/1`, reason `release bytes no longer match the authorization pin` |
| Release file and recorded file disagree on a binding field | exit 2, check `return-line-recorded-release/1`, reason `authorization binding disagrees with the release file`. Neither side is preferred. |
| Release file or authorization file is inside the target book or the live book, or they are the same path | exit 2, check `return-line-recorded-release/1` |
| Operation not in the list, or the list is empty, repeated, or not strings | exit 2, reason contains `not authorized` or `operations` |
| Plan hash or length differs | exit 2, check `return-line-plan/1`, reason `plan hash or length does not match the recorded release`, state `conflict` |
| Plan `live_moves` or `live_apply` is not false | exit 2, check `return-line-plan/1`, reason `plan is not a read-only plan` |
| Audit hash or length differs | exit 2, check `audit identity` |
| An audit-listed member file is missing or its bytes differ during preflight, init, stage, reconstruct, or publish | exit 2, check `stale source`, before any root is created. Retire, rollback, reserve, and capture do not apply this book-location check |
| Root overlap, a root inside the book, a root containing the door, a missing parent, or a different volume | exit 2, check `filesystem`. Volume reason: `roots are not on the book volume`. Missing parent reason: `parent is missing`. The parent is not created. |
| Canonical mutation whose same-process binding is missing or is not a recorded release with `synthetic` false | exit 2, check `return-line-recorded-release/1` |
| Door-marked copy whose same-process binding is missing | exit 2, check `live book`, reason `book contains 0100.band.returns` |

`live_refusal` returns without a refusal. The production source does not contain the reason `this pack does not execute the canonical live book`.

Preflight uses the same table and creates nothing.

## Phase refusals

Pass02's phase rules still apply after the gate: audit identity, sealed reader, N7 tail, incomplete `0154` with no invented return, partial bytes kept, occupied line, occupied archive, rollback hash mismatch, interrupt exit 3, and refused `adopt`. A partial file that does not match is kept. Resume does not delete it.

A pin mismatch of pass03, or of the pins pass03 and pass02 check, exits before a book write. The successor writes nothing.

## What is not claimed

No power-loss, race, or sandbox result is claimed. An interrupt is a counted `--interrupt-after` stop, or the pass02 test fault `arm_fault`, which is not a CLI flag. A cross-device rename stops with the filesystem error. The tool does not copy-then-delete. Exit 0 from preflight is not execution. A disposable test release file is not a Director release for the live book. This build does not write that release for the live book and does not run the live mutators.
