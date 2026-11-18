# Contract — source/pass return access

Schema of this file: `return-access-contract/0507`. Written before `labs/return-access-pass01` and before the app door. The tools follow this file. A later verification command does not revise it.

## Pins

The adapter and the door load these files by pin. A mismatch writes nothing and does not launch.

| Input | sha256 | bytes |
|---|---|---|
| pass03 `labs/return-lines-pass03/return_lines.py` | `78cc4d8679bb6e54b3f2456ce777643da7a9a650ef5c79c216abd38a4c209c63` | 33349 |
| pass02 `labs/return-lines-pass02/return_lines.py` | `6691d0587ab97ba24a1709c9950b506961152939e2d112ee608f9dbd23e92908` | 82908 |
| pass01 `labs/return-lines-pass01/return_lines.py` | `863968c59974d85910626ba5e80cf49f14a3186c8d33b855efe00bf6ccec378a` | 100897 |
| placement `labs/return-placement-pass01/return_placement.py` | `db96f7023c73dcececba0e7d42b821da8193af7534a4bdf8cd2e5d6cd53d0754` | 66097 |
| reader `labs/return-capture-pass01/return_capture.py` | `8f3da5c651f6924fca6dedb0b95da7d181eb58884dc030dd9cbc3d8b6a5b15ac` | 45767 |

Pass03 already checks the pass02 pin. Pass02 already checks pass01, placement, and the reader. This door checks the same five pins again. The new adapter's own hash is measured when that file is written and stored in `app/return-lines-v2.json`. This contract does not predict that hash. `labs/return-lines-pass04` is not a pin and is not imported.

Authoring stays `app/authoring_tools_v2.py` loaded as `librarian_authoring_tools_v2`. Review-loop stays `app/review_loop_tools_v4.py` loaded as `librarian_review_loop_tools_v4`. Those declarations are not rewritten.

Before this build, `app/librarian.py` is sha256 `3f9dbfec25f71b4b3e0845d367d1d08138854bc1862b3b5b150aa6ce9250bc22`, 11581 bytes, and `app/README.md` is sha256 `82f839d211e1e4471f89cbc53f04b427d2929b9e67f139f4edd228925415355c`, 35626 bytes.

Pack inputs: schema `prime-pack-inputs/1`, 33 rows, manifest sha256 `87f10acee10c646ea14f25342fa2e4c877cfa64c34e14ba38a6221cce86e0fdc`, 10956 bytes.

## What this pack releases

Permission to add a source/pass resolver and one app branch on copies. The canonical book `D:\Git\lib-build\00.kernel\00.00.10.work` is not a mutation target. No sentinel is installed. No live layout, archive, or authorization is written. Custody is not acceptance. `task_association` on every access result is `not-established`. `accepted`, `approved`, and `published` stay false.

## Resolution

The caller identifies a book and exactly one selector: source page plus pass, or one old member, or one submission. Compute derives the path. Two selectors, or a source without a pass, is ambiguity and returns no descriptor.

N5NN uses the pinned placement rule: same workflow digit, band digit 1, same two-digit tail, same subject, same pass. The return path is `{N1NN.subject}/{pass}.return.md`. N7NN stays on that page. The tail is `{page}/{pass}.return.md`. Any other band is an undeclared source. The result's `missing` list contains `route`. No target page is invented.

A computed route is a verified fact even when the files are absent. Absent files are listed under `missing`. They are not replaced by another directory that shares the number. The highest number is not a selection rule.

If more than one custody claims the same old member, or the same source page and pass, the result is refused. `descriptor` is null. No claimant is chosen.

States from the line tool are kept: `complete`, `reserved`, `incomplete`, `conflict`, and a refusal stays `refused`. A reserved pass is not reported as a missing route. An incomplete pass with a payload, manifest, or return file and no receipt sets `partial` true and stays `incomplete`. Bytes on disk are not rewritten to make a check pass.

## Line verifier and legacy reader

A native line-pass return uses pass03 lookup, descriptor, and verify. The legacy reader is not called on the N1NN folder and not called on the line page. The access result says why: `native line-pass return is not a legacy single-envelope page`.

A relocated historical member is verified by the line tool for the derived page and pass, and by the unchanged reader `verify(parent, member)`. The parent is the directory that actually contains the member: `originals` or `occupants` under the recorded retired root. If the member is still a direct child of the book and that child has `reservation.json`, the parent is the book. If both `originals` and `occupants` contain the member, the result is ambiguity and the reader is not called. The reader is never pointed at the line page.

Verified hashes and the legacy parent are `verified` facts. A missing return, including incomplete 0154, stays under `missing`. The tool does not create the return.

## App door

`app/librarian.py` gains one branch, `return-lines`, loading `app/return_line_tools_v2.py`. The declaration is `app/return-lines-v2.json`.

Read-only commands `status`, `lookup`, and `verify` launch the adapter with an argument array. No shell. No backend, tool, python, module, or pins override.

`reserve` and `capture` launch pinned pass03 with the caller's argument array only when the book is a declared line-pass book: `return-line-layout.json` says `allocation` `line-pass` and `sequential_allocation` false, and `0100.band.returns` is present. The call must include the authority arguments pass03 already requires: `--authorization`, `--audit`, `--plan`, `--backup`, `--staging`, `--retired`. The canonical book is refused before launch. Pass03's own live refusal and fixture checks still apply. This door does not add `--force`, `--allow-live`, or `--designate`.

`stage`, `publish`, `retire`, `rollback`, `adopt`, `init`, `preflight`, and `plan` are not commands of this door.

`status` is read-only. It reports the layout hash when the file is present, and `missing` contains `layout` when it is absent. Authority `established` is false. The requirement text names the pass03 synthetic fixture for a door-marked copy and states that the reviewed pass03 production CLI has no recorded-release path without the in-process test seam. `live_release` is false. `successor_consumed` is false. `sentinel_policy` is `not-adopted`. `incomplete_closure` and `legacy_writer_closure` are `not-established`. Incomplete index rows are findings. They are not completed.

## Legacy writers still able to allocate

This door does not make the old routes safe and does not patch them.

| Route | What it does now | Later change, not this pack |
|---|---|---|
| `labs/return-capture-pass01/return_capture.py reserve` | Allocates the next sequential member. Also called by `labs/capture-handoff-pass01/demo.py` and `labs/capture-flow-rehearsal-pass01/rehearse.py`. | A later helper successor refuses `reserve` when the book layout is line-pass. `verify` and `inspect` stay. No sentinel. |
| `librarian capture-return` through `app/handoff_tools.py` and `labs/capture-handoff-pass01/handoff.py` | Launches `return_capture.py capture` on a member that reserve already created. It writes custody. It does not mint the member. | After that helper refusal exists, refuse this door on a line-pass book. |
| `librarian boot-prepare` and the other boot commands through `app/boot_tools.py` and `labs/prime-boot-pass01/prime_boot.py` | Hash the helper and launch `return_inspect.py`. They do not call `reserve`. | Keep the sibling hash until inspect no longer requires it. |
| `librarian batch-observe` through `app/batch_tools.py` and `labs/batch-observation-pass01/batch_observe.py` | Launches `return_inspect.py inspect`. It does not call `reserve`. | Same pin stays until the helper and the inspector change together. |

No global repin of historical captures. Closure is not claimed.

## Results

Access commands emit `return-access-result/1` as UTF-8 JSON, indent 2, one trailing newline. `reserve` and `capture` emit pass03's `return-line-result/1` unchanged. A door refusal prints `stop:` on stderr, empty stdout, exit 2, and does not launch. The line tool's exit is preserved for a resolved return: 0 complete, 1 reserved or incomplete, 2 refused or conflict. Ambiguity and an undeclared source are exit 2.

A linked book, or a linked ancestor of the book, is refused before launch and is not followed.

## Copies

Disposable books and retired roots live under `D:\librarian\temp\0521-0507\`. The suite retains that tree, including the first run's stdout. It copies the band door and the audited members it needs. It does not write the live book. New filings use the existing synthetic fixture `return-line-authorization/1` that pass03 already accepts for an ordinary door-marked copy. This build does not create a director release.

The required seam, through `app/librarian.py`, is: two passes on one N5NN line; the historical members 0121 through 0125 and a first new filing on each freed number from the real source pages 0521 through 0525; an N7NN page-local return; an originals parent and an occupants parent; incomplete 0154; a wrong band, a wrong subject, and a wrong pass; a changed payload; an occupied number; a partial custody; a repeated same-byte capture; a conflicting capture. The consumer reads `descriptor.target_page`, `descriptor.return_path`, and `descriptor.custody_path`. One bounded check shows the authoring-v2 and review-loop-v4 load lines and pin hashes unchanged. Their suites are not rerun.

## Limits

Caller closure, a sentinel, pass04, app edits beyond this registration, old helper edits, the band door, N3NN, kernel law, `00.live`, current assignment, the live return band, the archive, authoring05.02, sealed evidence, Git, network, installs, models, bots, and AR-01 are outside this contract. Matching custody remains `0121.return-placement`, unfiled. This pack does not allocate it.
