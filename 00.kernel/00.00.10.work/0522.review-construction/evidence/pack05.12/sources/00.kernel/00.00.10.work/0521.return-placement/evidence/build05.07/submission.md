# Submission - 0521.return-placement/05.07

date: 2026-11-02
executor: Grok-1
reviewer: Codex Prime
accepted: false
committed_by_this_builder: false
custody: pending
matching line: 0121.return-placement unfiled; slot occupied by 0121.archive-resolution-0508
readiness: blocked

This is the builder return for the named invocation of 05.07. It is not acceptance, not a live migration, and not a caller closure. Notes in 06.12.md were reread at close and integrated below. The contract was not revised after tests. This file does not carry the artifact-manifest hash. That hash is written only on the 05.07 return pointer after the manifest exists.

## Did

Built `labs/return-access-pass01`. It loads reviewed return-lines pass03 by pin, and pass03 loads pass02, pass01, placement, and the legacy reader by their existing pins. The adapter does not fork custody validation and does not import `labs/return-lines-pass04`.

A caller names a book and one selector. The selector is a source page plus a pass, or one old member, or one submission. Compute derives the target. N5NN uses the pinned placement rule: same workflow digit, band digit 1, same two-digit tail, same subject, same pass. N7NN stays on that page. Any other band is undeclared. `missing` then contains `route`, and no target page is invented.

A native line-pass return is checked with the line descriptor and the line verifier. The legacy reader is not pointed at the N1NN folder. A relocated historical member is checked with the line tool and with `verify(parent, member)`. The parent is `originals` or `occupants` under the recorded retired root. If both parents contain the member, the reader is not called. Ambiguous claims return no descriptor.

`app/librarian.py` gained one branch, `return-lines`, loading `app/return_line_tools_v2.py` as `librarian_return_line_tools_v2`. The declaration is `app/return-lines-v2.json`. Status, lookup, and verify are read-only. Reserve and capture forward to pinned pass03 only for a declared line-pass book that is not the canonical live book, and only with the authorization arguments pass03 already requires. The synthetic fixture is `return-line-authorization/1`. This door does not add `--force`, `--allow-live`, or `--designate`. Stage, publish, retire, rollback, adopt, init, preflight, and plan are not commands of this door.

Authoring remains `app/authoring_tools_v2.py` loaded as `librarian_authoring_tools_v2`. Review-loop remains `app/review_loop_tools_v4.py` loaded as `librarian_review_loop_tools_v4`. Those declarations were not rewritten. Their suites were not rerun.

The clean suite is `D:\librarian\temp\0521-0507\20261102T193704Z`. Schema `return-access-entry-run/1`. 91 cases, failed 0, first_failure null. The consumer read `descriptor.target_page`, `descriptor.return_path`, and `descriptor.custody_path`. Source bytes after retirement matched the copied audit bytes. The live book gained no `return-line-layout.json`.

First new filing `0521.return-placement` pass `05.01` resolved to `0121.return-placement/05.01.return.md`, sha256 `74dbfd2f52cbac30e8bd6203ac018e6bbc504b3416edfc1537a53ef85db2f660`. Pass `05.02` on that line is sha256 `191012aa6b4bc682e613027541ae6f7ce1ff212ff43f9bf4c8e0aca28f3e4621`. The legacy reader was not called for those native returns.

## Blocked

`0121.return-placement` is unfiled on the live book. Directory `0121.archive-resolution-0508` occupies that number. This slice does not free it, file a live return, allocate a sequential member, or invent a receipt. Readiness stays blocked.

`labs/return-lines-pass04` is on disk. It was not read for an interface and was not imported. Legacy `return_capture.py reserve` can still allocate, including through the capture-handoff demo and the capture-flow rehearsal. `librarian capture-return` still writes custody on a member reserve already created. Boot and batch observation still launch `return_inspect.py` and do not call reserve. Closure of those routes is not established. No sentinel was installed.

A reserve against `D:\Git\lib-build\00.kernel\00.00.10.work` is refused with `stop: canonical live book is refused` and writes nothing.

This builder does not commit.

## Need

Codex Prime review of this return. Stop here. Do not start caller closure, a pass04 integration, or a live cutover in this build. Runnable commands begin with a source page and a pass in `evidence/build05.07/PRIME-USE.md`.

## Tests

Clean run `20261102T193704Z`: 91 cases, failed 0, first_failure null. Copied to `evidence/build05.07/runs/20261102T193704Z`.

Retained earlier assertion failures, with stdout left in place:

- `20261102T193328Z` first failure `producer-plan`. pass03 plan returns state incomplete and exit 0. The plan file was written. Occupancy conflict count was 1.
- `20261102T193354Z` first failure `occupied`. Reserve exited 2, state conflict, evidence `0198.blocker`. The suite had looked in the correction text.
- `20261102T193526Z` first failure `pass04-present`. The successor directory exists. The adapter does not name it.

The clean run then covered two historical passes on `0508.return-capture`, historical members 0121 through 0125, the occupant parent for `0104.app-entry-0508`, the originals parent for `0121.archive-resolution-0508`, incomplete `0154`, the N7 tail `0701.bench-method/05.01`, first filings from the real pages 0521 through 0525, a second pass on `0521.return-placement`, a reserved pass, a partial custody, a changed payload, a same-byte replay, a conflicting capture, a wrong band, a wrong subject, a wrong pass, ambiguous selectors, an occupied number, a junction refusal, and the live-book refusal. One bounded check confirmed the authoring-v2 and review-loop-v4 load lines and pin hashes.

## Closure plan, not performed

A later helper successor refuses `reserve` when the book layout is line-pass. `verify` and `inspect` stay. After that refusal exists, refuse `librarian capture-return` on a line-pass book. Keep the boot and batch sibling hashes until inspect no longer requires them. No sentinel. No global repin of historical captures. This pack does not make that edit.
