# Cutover proposal — unapproved

Schema: `return-access-handoff-cutover/0509`
Date: 2026-11-02. Executor: Grok-2. Reviewer: Codex Prime.
This file names a proposal. It does not approve roots, a real release, or a live move. Filling it does not revise `DELTA.md`.

## Current identities

| Identity | Value | Source |
| --- | --- | --- |
| Audit | sha256 `c3bf8c1e25bfd1a59ce40230d87f650897f3105691db732eadfe5abf4e275606`, 391778 bytes | `00.kernel/00.00.10.work/0417.return-placement/evidence/audit-corrected.json`. The suite used this path. The file was not edited. |
| Layout body | sha256 `2c414ac4e11cd874d28b8c477b7eed30ee477e216ed1653552d802f03c4d7804`, 216 bytes | Pass01 `dump(layout_body("00.00.10.work"))` for book name `00.00.10.work`. This is the declaration body. |
| Live layout file | absent | `00.kernel/00.00.10.work/return-line-layout.json` was absent at the claim, absent at suite start, and absent after the official run. `suite-report.json` records `live_layout_written: false`. |
| Live plan | sha256 `52951e1dbc0f37fa7f8c76be390a9510999a6944d7dc9f4e20c00c365f326f66`, 789717 bytes | `return_line_tools_v3.py plan` wrote this file under the temporary root, outside the live book. `matches_05_06_plan` is true. The suite required `live_moves` false and `live_apply` false. The book gained no layout. |
| Live fingerprint | `75061b0c183e299c36623e809be8518a0d6efd4482ff13ed3bb3d4865c5e2e6d` | `suite-report.json` before and after. The same fingerprint was recorded at the 05.06 close. |
| Door | sha256 `c9ff0949c09268451a8e2a2113c1612047b374b3ecc0b3c177b6c5fd22b6842d`, 10206 bytes | `0100.band.returns/01.md`, remeasured at this close. 0 CR. |
| HEAD | `960d20c5290656095df8457b1740d2d5e586b111` | `git rev-parse HEAD` on `workshop` at the claim and again at this close. No Git write. |

## Candidate roots

These paths are named and unapproved. The suite refused to continue if any of them existed, and none was created.

| Role | Path | Exists after the suite |
| --- | --- | --- |
| Staging | `D:\librarian\return-placement\0521-staging` | no |
| Backup | `D:\librarian\return-placement\0521-backup` | no |
| Git-trackable retirement | `D:\Git\lib-build\00.archive\0521.return-lines` | no |

## What the official run showed

Work root: `D:\librarian\temp\0521-0509\20261102T213852169046Z-suite`. Temporary retention. Not a durable archive. The index is `evidence/build05.09/fixture-index.json`.

Guard selection: the new handoff checks the reviewed guard hash before launch. On the marked primary copy, `return_capture_guard.py` reserve exited 2 and capture exited 2. The facade mismatch case refused a tampered guard path before launch and wrote sidecar schema `capture-handoff-guard-mismatch/1`. The real guard file was not edited.

Historical lookup on the marked copy: two lookups exited 0 (`0101.app-entry-0506` and `0104.app-entry-0508`) and one exited 1 (`0154`). `0154` stays incomplete. A reader result does not establish task association or approval.

Recovery on a one-member copy: `rollback-retire` exit 0, `rollback-publish` exit 0, `publish --interrupt-after 1` exit 3, `publish-resume` exit 0. This is the recovery case inside the same suite. It is not a second full migration.

Primary retirement of the 83-member copy: originals 65, occupants 18, `remaining_old_members` 0. New filings landed on matching `0121` through `0125`, with two passes on `0121.synthetic-filing`, plus the N7NN local return at `0721.synthetic-local`. Matching `0121.return-placement` custody stays pending. The allocator was not used. `0184` was not allocated. No receipt was invented.

Positive authority on the copies is synthetic `return-line-authorization/1` with `synthetic: true`. It is copy evidence. It is not a Director release. The live init that aimed a copy fixture at the live book stayed refused and wrote no layout.

## Staged modules and active capability

The successors and facades exist as files. The current app still loads `return_line_tools_v2.py` and `handoff_tools.py` in the measured live dispatcher. Those routes are not this build's successors. Staged modules are not active capability.

## Remaining Director decisions

Exact staging, backup, and retirement roots. The exact real recorded release. Whether to file matching `0121.return-placement`. Kernel law and any physical move of the `01NN` band. Evidence relocation stays queued on `0419/06.02`. This build does not clean or move that evidence.

## Pre-code sentence superseded by measurement

`CONTRACT.md` and `PRIME-USE.md` say a book that already contains the door cannot show a historical reserve, because the writer refuses that door. Those files were written before the suite and were not revised. The official run then called the historical writer directly on two disposable side copies. Both reserves exited 0 with `result reserved`: one doorless book that already held the exact layout, and one small marked book that held the real door plus the exact layout. The door does not confine the historical writer. The selected guard does. Supported-route closure is not total. There is no same-user confinement and no sentinel.

The current app is unchanged, so it remains without these successors. The live book has no layout file. Invoking the guard there for a real write would delegate to the historical writer. This build did not invoke the guard against the live book. `demo.py` and `labs/capture-flow-rehearsal-pass01/rehearse.py` still name the old reserve. They were not executed. A later supported reserve demo would be a new file.
