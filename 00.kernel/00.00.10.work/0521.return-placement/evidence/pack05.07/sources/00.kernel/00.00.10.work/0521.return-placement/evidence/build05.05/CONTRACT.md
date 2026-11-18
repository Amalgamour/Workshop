# Contract — return-lines pass03

Schema of this file: `return-line-contract/0505`. Written before `labs/return-lines-pass03`. The tool follows this file. A later verification command does not revise it.

## Pins

| Input | sha256 | bytes |
|---|---|---|
| pass02 `labs/return-lines-pass02/return_lines.py` | `6691d0587ab97ba24a1709c9950b506961152939e2d112ee608f9dbd23e92908` | 82908 |
| pass01 `labs/return-lines-pass01/return_lines.py` | `863968c59974d85910626ba5e80cf49f14a3186c8d33b855efe00bf6ccec378a` | 100897 |
| placement `labs/return-placement-pass01/return_placement.py` | `db96f7023c73dcececba0e7d42b821da8193af7534a4bdf8cd2e5d6cd53d0754` | 66097 |
| reader `labs/return-capture-pass01/return_capture.py` | `8f3da5c651f6924fca6dedb0b95da7d181eb58884dc030dd9cbc3d8b6a5b15ac` | 45767 |
| audit `0417.../audit-corrected.json` | `c3bf8c1e25bfd1a59ce40230d87f650897f3105691db732eadfe5abf4e275606` | 391778 |
| door `0100.band.returns/01.md` | `c9ff0949c09268451a8e2a2113c1612047b374b3ecc0b3c177b6c5fd22b6842d` | 10206 |
| pack05.05 source-manifest | `8e84793f8a6af510ad3ecd07e92769c859e3e90c07b8a7f47195409057e3be7d` | 8696 |
| seam `colab/labs/0709.return-migration-check/pass01/seam.py` | `dccd66af39dc8ca688610ca67a7b8903e6631191df2f232c3cd21574e8f08a4f` | 5625 |
| review loop pass03 | `47f47d16426e4d69987398a8244877de58b6089326874f3279003f696814450b` | 55474 |
| prime cycle pass03 | `496b4d721cfb136fa847d998d421209616c60508beb5cda5620af73041eed17c` | 76045 |

The successor loads pass02 by that pin. Pass02 loads pass01, placement, and the reader by the pins pass02 already checks. A mismatch writes nothing. Pass01 and pass02 on disk are not patched. The layout body for book name `00.00.10.work` stays 216 bytes, sha256 `2c414ac4e11cd874d28b8c477b7eed30ee477e216ed1653552d802f03c4d7804`.

## What this pack releases

Permission to implement the capability and to write a proposal. The canonical live book `D:\Git\lib-build\00.kernel\00.00.10.work` is not a mutation target. Check name for that refusal is `live execution`. The reason is `this pack does not execute the canonical live book`. That check is not the pass02 blanket `synthetic authorization required`. Designating the canonical path with the test seam does not remove the check.

`evidence/build05.05/invocation.txt` and `evidence/build05.04/release.txt` are not a migration release. The tool has no hard-coded release string that authorizes a book.

## Authority records

Exact rules are in `AUTHORITY.md`. Three schemas:

| Schema | Role |
|---|---|
| `return-line-authorization/1` | Existing synthetic fixture. Authorizes an ordinary disposable door-marked copy under pass02's rules, including `synthetic` true and the 05.04 fixture release text. Does not authorize a designated-live identity or the canonical book. |
| `return-line-recorded-release/1` | Points at an external `return-line-director-release/1` file. `synthetic` is false. Authorizes mutation only of a copy the in-process test seam has designated, and only when every binding matches the re-read release file. |
| `return-line-release-candidate/1` | Human-bound proposal. Not authority. `active` true is still not authority. |

No conflict between these records is resolved by picking the more permissive one. The file passed in `--authorization` is the only record consulted. A Prime label, a boolean, a build invocation, or the word force is not a record.

The correction route for a changed plan is a new director-release file and a new recorded-release file that pins the new bytes. Editing the plan, the release file, or the recorded pin alone refuses before the next phase. This is a byte record. It is not a cryptographic identity guarantee.

## Sequence

The pass02 order is unchanged: plan, authorization, init, stage, reconstruct, verify logical pages, publish with occupant displacement, retire every remaining audited old member, lookup, rollback-retire then rollback-publish. `adopt` stays refused. `0154` stays incomplete. Page-local tails stay on their pages. Raw custody bytes and N7NN tails are not normalized. Pass02 re-reads source bytes inside each irreversible phase. The recorded-release path also re-reads the release file, the plan, and the audit at the start of every authorized command. The audit-listed member files are compared to the book before preflight, init, stage, reconstruct, and publish, including resumes, and before any root is created. Retire, rollback, reserve, and capture do not demand that a member already moved by publish or retire still sit in the book. Those commands keep pass02's backup and journal byte checks.

`preflight` is read-only. It uses the same checks and writes no layout, archive, marker, or root. Exit 0 means the record matched and nothing was written. It does not mean the migration ran.

## Retirement layout

Publication moves colliding occupants to `{retired}/occupants/{name}`. Retirement moves every remaining audited old member to `{retired}/originals/{name}`. Both sets are retired. The pass03 README says that. The pass02 README is not edited.

Lookup still delegates the descriptor to pass01 and adds `detail.new_home` and `detail.retained_original`. `retired_rel` is `originals/{name}` or `occupants/{name}`. There is no single book-shaped archive. The historical reader is `return_capture.py` `verify --book --member`. Its member argument cannot contain a slash, and it expects a capture envelope as a direct child of `--book`. The rehearsal points that reader at the retired root, at `originals/`, and at `occupants/`, and records the exits. An adapter is not added.

## CLI delta

Tool: `labs/return-lines-pass03/return_lines.py`.

New command, read-only:

`preflight --book --authorization --audit --plan --backup --staging --retired [--operation NAME]`

Every other command is pass02's CLI, forwarded after the pass03 gate. There is no `--force`, no `--allow-live`, and no `--designate`. The test seam is `designate_live(absolute_path)` and `clear_designation()` in this process only.

Envelopes stay `return-line-result/1`. Detail `acceptance` is null. `approved`, `accepted`, and `published` stay false. Pass03 refusals name `0521.return-placement/05.05`. Fixture refusals produced by pass02 keep pass02's 05.04 sentence. Forwarded pass01 envelopes keep pass01's 05.03 sentence when pass02 did not already wrap them.

## Copies and proposal

Disposable books live under `D:\librarian\temp\0521-0505\`. Each run has its own directory. Nothing in that tree is deleted. A copy includes the band door, the audited member directories, and the page-local tail files. Roots stay on the same volume as the book because a cross-device rename stops and the tool does not copy-then-delete.

The future cutover proposal names these unresolved candidate paths and does not create them:

| Role | Path |
|---|---|
| staging | `D:\librarian\return-placement\0521-staging` |
| backup | `D:\librarian\return-placement\0521-backup` |
| git-trackable retirement | `D:\Git\lib-build\00.archive\0521.return-lines` |

They are outside the work book, outside each other, and on volume `D:`. The retirement path is inside the Git checkout and outside the work book, so a later review could track it. This pack does not create the directories, does not move archives, and does not commit. The candidate file is `return-line-release-candidate/1` with `active` false and a non-empty `unresolved` list. Preflight of that candidate exits 2. It is not an active authorization.

The measured plan hash is recorded after the read-only plan. It is not required to equal `52951e1dbc0f37fa7f8c76be390a9510999a6944d7dc9f4e20c00c365f326f66`.

## Limits

Caller enforcement, a sentinel, `app/` edits, old allocator patches, the band door, N3NN registration, Git writes, network, model calls, bots, and AR-01 are outside this contract. `0154` stays incomplete. Pending captures `0121` through `0126` are named as pending. This pack does not invent their receipts or a task association. Matching custody remains `0121.return-placement`, unfiled.
