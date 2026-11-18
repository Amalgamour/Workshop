# Submission - 0526.dev-authoring/05.01

date: 2026-11-02
executor: Grok-1
reviewer: Codex Prime
accepted: false
committed_by_this_builder: false
custody: pending
matching line: 0126.dev-authoring unfiled; slot occupied by 0126.boot-members-0509
readiness: blocked

This is the builder return for the named invocation of 05.01. It is not acceptance, not a live review, and not a Prime authoring pilot. Notes in 06.01.md were reread at close and integrated below. The contract was not revised after tests. This file does not carry the artifact-manifest hash. That hash is written only on 05.01 after the manifest exists.

## Did

Built `labs/pack-authoring-pass01` and the narrow app door. Profile `0423-to-0526` is stored configuration from `0423.dev-authoring` to `0526.dev-authoring`. It is not a digit substitution. `app/librarian.py` gained one `authoring` branch and still loads `review_loop_tools_v4.py` as `librarian_review_loop_tools_v4` for `review-loop`. `app/README.md` gained an authoring section. No other app or lab module was edited. The two migration lanes were not edited.

Compute reserves the next free `05.NN`, assigns `#NN`, renders one derived draft, hashes sources, checks UTF-8, and calls the pinned dependency reader and, on an outside-book freeze, the pinned pack checker. The caller supplies goal, scope, finish, executor, reviewer, one item's meaning, note dispositions, and the semantic review. `complete_claim` stays false. Approval and release stay false.

The current-book preview reserved pass `05.02` under `evidence/authoring05.02`. State is drafting. Review is absent. `05.01.md` was not overwritten by the preview. No `05.02.md` page was written. Freeze was not run on that draft.

## Blocked

`0126.dev-authoring` is unfiled. Directory `0126.boot-members-0509` occupies slot 0126. This slice does not free it, file a return, allocate 0184, or invent a receipt. Readiness stays blocked.

Freeze on `D:\Git\lib-build` is refused with `freeze on the live checkout is outside this slice` and writes nothing.

File-symlink creation in the suite is a skip: `WinError 1314`. Junction refusal was executed.

This builder does not commit.

## Need

Codex Prime review of this return. Stop here. Do not start the Prime authoring pilot in this build. The open draft is the thing Prime can inspect with the commands in `evidence/build05.01/PRIME-USE.md`. The synthetic sentences are demonstration meaning, not Prime's review.

## Template, schema, and API

Readable source template: `00.kernel/00.00.10.work/0423.dev-authoring/templates/build-pack-v1.draft.md`, sha256 `9cea6540155a59b470adcd2dab93d0e674b379478f311113271e632aa58e9fd0`, 1394 bytes. Machine template: `labs/pack-authoring-pass01/template/build-pack-v1.json`, schema `authoring-template/1`, template id `build-pack-v1`, sha256 `9e92ee322c5c4e20bb0006e2f92ab9f1fd1308f2812ab70b34c248ddebb5bdcc`, 1008 bytes.

Schemas in use: `authoring-contract/1`, `authoring-pins/1` version 1, `authoring-record/1`, `authoring-result/1`, `authoring-frozen-inputs/1`, `authoring-before-pins/1`, `authoring-entry-run/1`, `authoring-verification/1`. An outside-book freeze emits `prime-pack-sources/1`. The live preview did not emit one.

The app command is `authoring`. The caller cannot pass an executable, a template path, or a dependency-set path.

```text
authoring start --book ABS --profile ID --operation ID [--input ABS] [--json]
authoring add-note --book ABS --profile ID --operation ID --input ABS [--json]
authoring add-item --book ABS --profile ID --operation ID --input ABS [--json]
authoring revise --book ABS --profile ID --operation ID --target intent|item|disposition --input ABS [--item NN] [--note ID] [--json]
authoring inspect --book ABS --profile ID [--json]
authoring review --book ABS --profile ID --operation ID --input ABS [--draft-sha256 HEX] [--json]
authoring freeze --book ABS --profile ID --operation ID --draft-sha256 HEX [--json]
```

Exit 0 is a committed result or an idempotent replay. Exit 2 is `stop:` on stderr and empty stdout. Exit 4 is `partial:` after a failed replace; the previous record stays. The same operation id and the same raw input bytes replay. Different bytes under that id conflict and preserve the record. A typed refusal is not stored, so a corrected request may reuse the operation id.

## Authority

Compute owns pass reservation, item numbers, structure, source references, hashes, UTF-8, dependency lookup, and the derived return directory name. The model owns meaning and the semantic review. Compute binds a review to the render made after the assessment is included. That digest is not printed inside the rendered page. Changed meaning or source bytes invalidate the review. This build does not decide that the synthetic preview meaning is correct.

One record, `evidence/authoring05.NN/record.json`, is authoritative. `draft.md` is a derived face. A manual edit of that face is a conflict and is not imported.

## Source and dependency reuse

Frozen inputs: `evidence/pack05.01/source-manifest.json`, schema `prime-pack-inputs/1`, sha256 `7b354d8123bea276a7547009d2191f1a87512c2e337f14c64ca35c41643c3b94`, 17589 bytes, 53 rows, bad 0, missing 0, live bytes 978050. Close recheck: missing 0, snapshot mismatches 0, not repinned. Live drift is only `app/librarian.py` and `app/README.md`.

Reused without editing them:

- reader `labs/module-dependencies-pass02/depdecl.py` sha256 `a517b0ec3906589e16e2df9bcfb6b3e21a5dd0bd3ef1099d59bf95c0f15ff4e7`, 53693 bytes; commands `validate` and `requires` only
- set `labs/app-dependencies-pass02/set.json` sha256 `444dba1589c0d6a0204e7a3d6be334b3135d524e4b376e7e92eb8fb434e6f706`, 7054 bytes; label measured-file, form working-tree
- checker `labs/pack-custody-pass01/pack_check.py` sha256 `9bbd9d57f3b7da43234ac2e6ae4ce40a0ab6af2f53c8135ecfb2ee0c8a6e322d`, 21563 bytes; freeze on an outside book only

The assembler `labs/pack-assembly-pass01/pack_assembly.py` is not called. Review-loop v4 declaration sha256 `769f81321e19a9f3296020e3b0b4a4905ec1b3a66c1629bf53d9548b7182d723`, 2519 bytes. Door sha256 `0769179366a6c1659f38cb2c79c51981d5cb76fa8d48ee7325f9eaf00d14c296`, 13381 bytes. The nine pins match their files.

Gaps: no N3NN address, no return filing, `complete_claim` false, environment and conditional findings stay visible and do not by themselves block an outside-book freeze, a new relationship with meaning stays `unresolved-not-in-set`, coverage is the declared notes only, and the hash-to-subprocess gap is not closed.

## Pins

Module `labs/pack-authoring-pass01/pack_author.py` sha256 `30908475162fe9b1a566018d217d26465151b1243bb3a8f391cb54254f3ba10c`, 67547 bytes. Door `app/authoring_tools.py` sha256 `13cbc91f880c13dfd5b07afe9284092d16bba01afe1a0d5c06b7b3ff35f3ab54`, 7817 bytes. Declaration `app/authoring.json` sha256 `8a59bbd93086ac88c37e1e7a44f7db4b6f3d77fe1294aa67ce559d3550885816`, 1864 bytes.

Before: `app/librarian.py` sha256 `f3dc2108dfff2bade5db4e7354b31b94b5a53e423bbe4fff1071a4a9cd1d42a9`, 11037 bytes; `app/README.md` sha256 `69584469c654f5d7fcd4993dc36b01afc87434be33a7c2ae60741473af6f7e86`, 31547 bytes. Copies are under `evidence/build05.01/before/`.

After: `app/librarian.py` sha256 `dab9bba639da15ae264333f92503167da97a8608e46192092328ad1cc146e35d`, 11566 bytes; `app/README.md` sha256 `5f1ee92125b7613823ea3ceffdab052537380b41b60f01199ba4f5dceeec31dd`, 34696 bytes.

Contract `evidence/build05.01/CONTRACT.md` sha256 `a24620357c94be2a7f77057dc7926f41c53362c2e6148cb59de32c4db3e9b20b`, 12012 bytes.

Close check: authoring pins and the nine v4 pins match the files. No copy of module hash `29c8d05a` or `2bf5aa5f` remains under `app/`.

## Commands, exits, and first failures

Suite module: `app/tests/test_authoring_entry.py`, run only as `__main__`. Interpreter: `C:\Users\misg\AppData\Local\Programs\Python\Python314\python.exe -B`. Working directory `D:\Git\lib-build`. `PYTHONDONTWRITEBYTECODE=1`. The suite returns 1 when `first_failure` is set and 0 when it is null. This close did not re-run it.

Preserved first run `evidence/build05.01/runs/20261102T173741Z`: 60 cases, failed 3.

- `inspect shows source drift` / `drift flag`. The freeze path had already stored the new source hashes, so a later inspect no longer saw drift. The freeze refusal `stop: source-drift` had passed. The cited run inspects before freeze.
- `typed start reserves nothing`. Stderr was `stop: typed-field: title expected an absent field` and the work lock had already created `evidence/`. Start now measures and parses before the lock. A typed-bad start creates no evidence directory.
- `stale claim labelled` / `label`. The draft said `labels environment,stale` and freeze refused with `dependency lib-build:app/librarian.py is stale`. The assertion now looks for `stale`.

Cited run `evidence/build05.01/runs/20261102T173920Z`: 60 cases, failed 0, `first_failure` null. Live page sha256 during that run `ac80298989190fab6aebffcedf28e8dd7e49a98f639f8e6007df7c33daa25b78`. `evidence/authoring05.02` was absent. Selected green details:

- `where missing root`: exit 2, empty stdout, `stop: missing --root`
- `ancestor junction does not launch`: `book root ancestor is linked and was not followed`
- `ancestor junction cli` and `checkout alias ancestor refused`: `stop: book root ancestor is linked and was not followed`
- `direct junction refused`: `stop: book root is not a directory`
- `file symlink skip`: `WinError 1314`
- `interrupted replace`: previous record retained, partial `record.json.partial-op-interrupt`
- `two reserves differ`: `05.01` and `05.02`
- `malformed input`: `stop: input is not strict json`
- `typed field`: `stop: typed-field: tests_passed expected an absent field`
- `conflicting retry`: `stop: conflicting operation; the record was preserved`
- `freeze before disposition`: `stop: note .../06.01.md is unresolved`
- `freeze prepared page` and `page matches reviewed bytes`: exit 0 on a disposable book; the page bytes matched the reviewed draft
- `return directory not created`: no `0126.dev-authoring` on that book
- `inspect shows source drift`: `source_drift` true; `source drift refuses freeze`: `stop: source-drift`
- `typed start reserves nothing`: refusal and no evidence directory
- `stale set refuses freeze`: `stop: stale dependency set`
- `missing dependency refuses freeze`: `stop: dependency lib-build:labs/not-a-declared-module.py is missing`
- `stale claim refuses freeze`: `stop: dependency lib-build:app/librarian.py is stale`
- `two starts one session`: exits `[0, 2]`, one record, `an open session already exists`
- `live freeze refused`: `stop: freeze on the live checkout is outside this slice`
- `live page unchanged` and `live slot absent after`: both passed

Preview command, same interpreter, cwd `D:\Git\lib-build`. Each exit was 0.

```text
python -B app/librarian.py authoring start --book D:\Git\lib-build --profile 0423-to-0526 --operation prime-start-01 --json
python -B app/librarian.py authoring add-item --book D:\Git\lib-build --profile 0423-to-0526 --operation prime-item-01 --input D:\Git\lib-build\00.kernel\00.00.10.work\0526.dev-authoring\evidence\build05.01\preview-inputs\item-01.json --json
python -B app/librarian.py authoring add-item --book D:\Git\lib-build --profile 0423-to-0526 --operation prime-item-02 --input D:\Git\lib-build\00.kernel\00.00.10.work\0526.dev-authoring\evidence\build05.01\preview-inputs\item-02.json --json
python -B app/librarian.py authoring revise --book D:\Git\lib-build --profile 0423-to-0526 --operation prime-intent-01 --target intent --input D:\Git\lib-build\00.kernel\00.00.10.work\0526.dev-authoring\evidence\build05.01\preview-inputs\intent.json --json
python -B app/librarian.py authoring revise --book D:\Git\lib-build --profile 0423-to-0526 --operation prime-disp-01 --target disposition --note 00.kernel/00.00.10.work/0423.dev-authoring/06.01.md --input D:\Git\lib-build\00.kernel\00.00.10.work\0526.dev-authoring\evidence\build05.01\preview-inputs\disp-01.json --json
python -B app/librarian.py authoring revise --book D:\Git\lib-build --profile 0423-to-0526 --operation prime-disp-02 --target disposition --note 00.kernel/00.00.10.work/0423.dev-authoring/06.02.md --input D:\Git\lib-build\00.kernel\00.00.10.work\0526.dev-authoring\evidence\build05.01\preview-inputs\disp-02.json --json
python -B app/librarian.py authoring inspect --book D:\Git\lib-build --profile 0423-to-0526 --json
```

Replay instructions are `evidence/build05.01/PRIME-USE.md`. Use those input files. Item 2 contains Δ (U+0394).

## Actual generated draft

Path: `D:\Git\lib-build\00.kernel\00.00.10.work\0526.dev-authoring\evidence\authoring05.02\draft.md`

sha256 `547c3ae566323d6f821abed79a004a08a143f0246f14d110476560e1eee98cf3`, 3431 bytes.

Record: `D:\Git\lib-build\00.kernel\00.00.10.work\0526.dev-authoring\evidence\authoring05.02\record.json`

sha256 `35d5f90ca94dc4a864d1c9e3964301ab8b5c6d3235cd863dfef77ff8b2ff6a50`, 36033 bytes.

Pass `05.02`. State drafting. Approval false. Release false. Review absent. Missing: review, return readiness. Next: Prime can inspect this draft. Freeze on the live checkout is refused. This is not the Prime pilot. Return intended `0126.dev-authoring`, status occupied, occupants `0126.boot-members-0509`, readiness blocked. `complete_claim` false. Five `draft.md.conflict-prime-*` files are earlier derived faces. The record is the authority.

```text
# 05.02 - authored draft
profile: 0423-to-0526
pass: 05.02
approval: false
release: false
authority: authoring record; this face is derived
label: the meaning below is supplied by the caller

## Intent
goal: Supplied synthetic preview of the authoring command. Not a release and not the Prime pilot.
finish: Prime can inspect the draft with the actual command
executor: Grok-1
reviewer: Codex Prime
scope.included: one unreleased draft after 05.01
scope.excluded: freeze, release, and return filing
scope.allowed_writes: evidence/authoring05.NN under 0526.dev-authoring

## Declared notes
- 00.kernel/00.00.10.work/0423.dev-authoring/06.01.md disposition integrated item 01 why -
  sha256 7a81cb8b1db369a39014cd0025780d4ef9c3812f624a5ffd1761b83073504cfe bytes 2261
- 00.kernel/00.00.10.work/0423.dev-authoring/06.02.md disposition deferred item - why Supplied synthetic: this preview does not decide the draft review.
  sha256 b4bc1a36c165545f47a82569ad2dcbabd4ea252443489dc452f1ccf39ee3190e bytes 788

## Draft notes
- none

## Items
## #01 - Show the source form
Supplied synthetic demonstration. Load the registered 0423 source and reserve the next pass.
requirements:
- The model does not choose the pass or the item number.
interfaces:
- authoring start
acceptance:
- Inspect shows this meaning under the computed item number.
note-refs:
- 00.kernel/00.00.10.work/0423.dev-authoring/06.01.md
open-choices:
- Prime replaces this synthetic item in a later pilot.
dependency-refs:
- none

## #02 - Keep the second meaning separate
Supplied synthetic demonstration. A second item is meaning only, including the mark Δ.
requirements:
- UTF-8 text is stored as text.
interfaces:
- authoring add-item
acceptance:
- Inspect shows both items in one draft.
note-refs:
- 00.kernel/00.00.10.work/0423.dev-authoring/06.02.md
open-choices:
- none
dependency-refs:
- none

## Dependencies
set-path: labs/app-dependencies-pass02/set.json
set-sha256: 444dba1589c0d6a0204e7a3d6be334b3135d524e4b376e7e92eb8fb434e6f706
set-label: measured-file
set-form: working-tree
complete_claim: false
query validate module - exit 0 status valid labels -
query requires module lib-build:app/librarian.py exit 0 status complete-for-declared-coverage labels environment
query requires module lib-build:labs/review-loop-pass02/review_loop.py exit 0 status complete-for-declared-coverage labels conditional,environment

## Return
intended: 0126.dev-authoring
status: occupied
occupants: 0126.boot-members-0509
readiness: blocked
n7nn: page-local

## Review
review: absent

## Sources
- source 00.kernel/00.00.10.work/0423.dev-authoring/01.md sha256 8c2b430c02f9eef74e9ea05976071e6bf24bd29b1809dd8491d0d8072188e411 bytes 8719 utf8 true
- work-note 00.kernel/00.00.10.work/0526.dev-authoring/01.md sha256 21f8106f9722fd9c8f168ffd6a9de9e8c4f5ed6086d2a4f0937caf51f6b4d44d bytes 474 utf8 true
- template 00.kernel/00.00.10.work/0423.dev-authoring/templates/build-pack-v1.draft.md sha256 9cea6540155a59b470adcd2dab93d0e674b379478f311113271e632aa58e9fd0 bytes 1394 utf8 true
- declared-note 00.kernel/00.00.10.work/0423.dev-authoring/06.01.md sha256 7a81cb8b1db369a39014cd0025780d4ef9c3812f624a5ffd1761b83073504cfe bytes 2261 utf8 true
- declared-note 00.kernel/00.00.10.work/0423.dev-authoring/06.02.md sha256 b4bc1a36c165545f47a82569ad2dcbabd4ea252443489dc452f1ccf39ee3190e bytes 788 utf8 true

Freeze emits these bytes unchanged. Approval and release stay separate.
```

## Factfind

- Pack05.01 was verified before edits. The close recheck still shows 53 rows, missing 0, and snapshot mismatches 0.
- Before the authoring edit, `app/librarian.py` and `app/README.md` matched the frozen rows, and the review-loop load was `review_loop_tools_v4.py`.
- `0126.dev-authoring` is absent. `0126.boot-members-0509` is present.
- Close check before this submission was written: HEAD `960d20c5290656095df8457b1740d2d5e586b111`, branch `workshop`, `git diff --cached` empty.
- Python 3.14.0. No `__pycache__` under `app/` or `labs/pack-authoring-pass01/` at that check.
- A start parses intent before the work lock. The contract was not revised to say so. The existing sentence already requires validation before reserve.

## Hostile

- A linked ancestor is refused before the lab process starts.
- A junction alias of this checkout is refused the same way. A direct junction is `book root is not a directory`.
- Item prose is data. It is not executed and it is not a hash source.
- Reader exit 0 is not closure. `complete_claim` stays false. A passing pack check is not release.
- A conflicting operation preserves the record.
- Measured files are labelled measured-file / working-tree.
- This preview may use the canonical checkout. A junction alias of the checkout may not.
- The same-user gap between the hash read and the subprocess is not closed.

## Overflow

None before code. The cited green run followed three corrections: book-policy parentheses, an empty-list render, and moving start measurement ahead of the lock. The failed run is kept. The module pin was updated to the 67547-byte file before that green run. `perform()` does not inject a crash. The interrupted-update case calls `commit_record` directly. The preview ran after the green suite, so `evidence/authoring05.02` now exists and the suite must not be re-run against this book. The five conflict faces are expected.

## Unprompted

No kernel registration, no migration-lane edit, no memory edit, no model call, no Git write, no `05.02.md`, no freeze of the live draft, no Prime pilot, no contract revision after tests, and no review-loop suite rerun.

## Stop

Review on 05.01 stays PENDING. Prime reviews. This builder stops.
