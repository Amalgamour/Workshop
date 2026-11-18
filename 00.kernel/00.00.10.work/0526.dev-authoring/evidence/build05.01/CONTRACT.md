# CONTRACT - incremental source-linked authoring
date: 2026-11-02
pack: 0526.dev-authoring/05.01
schema: authoring-contract/1
status: written before code; do not revise after tests

This contract is the behavior of labs/pack-authoring-pass01 and the app door app/authoring_tools.py. It is not approval, release, seating, or a Prime authoring pilot. accepted is false. This builder does not commit.

## Authority
Compute reserves the pass, assigns #NN, renders the draft, hashes sources and the draft, and looks up declared dependencies. The model supplies goal, scope, finish, executor, reviewer, each item's meaning, note dispositions, and the semantic review. Compute binds a review to the exact rendered draft bytes and the source, template, and dependency-set bytes measured with it. Compute does not decide that the meaning is correct and does not turn prose into Director authority.

One canonical record, evidence/authoring05.NN/record.json under the linked work page, owns the authored content and the revision history. draft.md is a derived face. A manual edit of draft.md is reported as a conflict and is not imported. The previous record stays in place until os.replace of a fully written partial succeeds. A failed replace leaves the partial file and does not truncate the record.

## Profiles
Profiles are declared files in the module. The caller selects a profile id. The caller cannot pass an executable path, a template path, or a dependency-set path.

Profile 0423-to-0526:

- source home 00.kernel/00.00.10.work/0423.dev-authoring
- work home 00.kernel/00.00.10.work/0526.dev-authoring
- source page 01.md, declared notes 06.01.md and 06.02.md, template templates/build-pack-v1.draft.md, work-page note 0526.dev-authoring/01.md
- dependency set root code, path labs/app-dependencies-pass02/set.json
- book policy live-or-outside

Profile fixture-authoring:

- source home 00.kernel/00.00.10.work/0491.fixture-source
- work home 00.kernel/00.00.10.work/0591.fixture-authoring
- declared note 06.01.md, template templates/build-pack-v1.draft.md, raw source raw/blob.bin
- dependency set root book, path dependency/set.json, labelled measured-file when read
- book policy outside-only

Another id is refused. Digit replacement is not a profile.

Book policy live-or-outside allows the canonical checkout D:\Git\lib-build, and allows a book that is outside that checkout and outside the live work book. Book policy outside-only refuses the checkout and the live work book. A book inside the checkout other than the checkout itself is refused. A book that contains the checkout is refused.

Every book path is absolute. UNC, a relative path, and a dot-dot part are refused. The path and every existing lexical ancestor are lstat'd. A symlink, junction, or other reparse point is not followed. The refusal before any lab process is `book root ancestor is linked and was not followed` when an ancestor is linked, and `book root is not a directory` when the final path itself is linked or is not a directory. After that check, realpath is canonical and the containment rules are applied to both the lexical path and the canonical path. This is not a sandbox and not a race-proof guarantee.

## Commands
The app command is `authoring`. librarian.py adds that branch only. The review-loop branch continues to load review_loop_tools_v4.py. The nine review-loop pins are unchanged. The lab command is the same argument list without the word authoring.

```text
authoring start --book ABS --profile ID --operation ID [--input ABS] [--json]
authoring add-note --book ABS --profile ID --operation ID --input ABS [--json]
authoring add-item --book ABS --profile ID --operation ID --input ABS [--json]
authoring revise --book ABS --profile ID --operation ID --target intent|item|disposition --input ABS [--item NN] [--note ID] [--json]
authoring inspect --book ABS --profile ID [--json]
authoring review --book ABS --profile ID --operation ID --input ABS [--draft-sha256 HEX] [--json]
authoring freeze --book ABS --profile ID --operation ID --draft-sha256 HEX [--json]
```

Operation ids match `^[A-Za-z0-9][A-Za-z0-9._-]{0,63}$`. A mutation requires `--operation`. Inspect does not. The request identity is the SHA-256 of the raw input bytes, or of the empty bytes when start has no input, plus the command and the target flags. The same operation id and the same request bytes return the stored result and the stored exit and write nothing. A different request under the same operation id exits 2, leaves the record unchanged, and says the conflict. One open session exists per book and profile. start with a new operation id while that session is open exits 2 and does not reserve another pass. A frozen session is not open. A later start may reserve the next pass.

## Reservation and record
The next pass is the lowest positive 05.NN whose page 05.NN.md, partial page, and evidence/authoring05.NN directory are all absent. Existing 05.01 on the live page stays. Reservation is the exclusive creation of evidence/authoring05.NN. Two overlapping creates cannot keep the same directory. A directory without record.json occupies the pass and is not reused.

record.json is schema authoring-record/1. Writes use a new partial name record.json.partial-<operation>, O_CREAT|O_EXCL, then os.replace. Exit 0 is a committed mutation or a read-only inspect. Exit 2 is a refusal: stdout empty, stderr `stop: ...`. Exit 4 is an interrupted replace: stdout empty, stderr `partial: ...`, previous record bytes unchanged, partial retained. Help for a field error names the field, the expected shape, the retained input path, and labs/pack-authoring-pass01/PRIME-USE.md.

UTF-8 is required for JSON, notes, template, and item text. Invalid UTF-8 is a refusal. A declared raw source is hashed and copied raw and is not decoded. Item prose is not executed and is not parsed for paths, numbers, or hashes.

## Typed form
Start returns the missing intent fields and the declared notes. Intent JSON keys are goal, scope, finish, executor, reviewer. scope keys are included, excluded, allowed_writes. All of those values are strings. Item JSON keys are title, purpose, requirements, interfaces, acceptance, note_refs, open_choices, dependency_refs, and optional relationship and condition. The list fields are arrays of strings. dependency_refs entries are repository, path, and optional claimed_sha256. relationship is target_repository, target_path, and meaning. condition is module, id, and state. state is applicable, inapplicable, or unknown. Unknown keys are refused, including tests_passed. A wrong JSON type is refused. The caller's input file is the retained input.

add-note keys are text, attribution, source, and optional mark. mark is only discussion, proposal, or recorded-decision, and only when the caller supplies it. Draft note ids are d01, d02, and so on. Declared note ids are their book-relative paths. Dispositions are integrated with an existing #NN, deferred with why, rejected with why, or unresolved. Coverage is this declared set plus draft notes. It is not a reading of arbitrary prose.

revise --target item requires --item NN, keeps that id, stores the previous item in revisions, and clears a bound review into review_history. Deletion and reordering are not commands. A delete flag is refused. revise does not renumber.

## Dependencies
The reader is the pinned subprocess labs/module-dependencies-pass02/depdecl.py, hash a517b0ec3906589e16e2df9bcfb6b3e21a5dd0bd3ef1099d59bf95c0f15ff4e7, 53693 bytes. The code-root set is labs/app-dependencies-pass02/set.json, hash 444dba1589c0d6a0204e7a3d6be334b3135d524e4b376e7e92eb8fb434e6f706, 7054 bytes. The checker is labs/pack-custody-pass01/pack_check.py, hash 9bbd9d57f3b7da43234ac2e6ae4ce40a0ab6af2f53c8135ecfb2ee0c8a6e322d, 21563 bytes. Hashes are checked before the subprocess. A linked tool path is refused. The commands used are validate and requires. index and delta are not called. The assembler labs/pack-assembly-pass01/pack_assembly.py is not called.

Profile queries are fixed by the profile. 0423-to-0526 and fixture-authoring both query validate, requires for lib-build:app/librarian.py at depth 1, and requires for lib-build:labs/review-loop-pass02/review_loop.py at depth 1 with condition render-or-recover=inapplicable. Item dependency_refs add one requires each. Reader exit 0 is an answer, not closure, and not a review. complete_claim stays false. Exit 1 is preserved as findings. Exit 2 is preserved as a reader refusal.

Classifications, from the reader result, not from a new graph:

- missing: root state undeclared, or resolution record-missing
- stale: resolution pin-differs, or a supplied claimed_sha256 different from the resolved implementation sha256, or the measured set digest different from the digest stored on the session
- ambiguous: ambiguous-version or identity-conflict
- conditional: condition-inapplicable, condition-unknown, or a returned edge whose condition applies is conditional
- environment: environment-unverified or environment-unavailable, preserved and not treated as a resolved environment

A new relationship with meaning stays unresolved-not-in-set. It is not written into the declaration set and is not a kernel registration. A relationship without meaning blocks freeze.

## Review and freeze
review stores the supplied assessment, unresolved issues, and stop conditions, plus the compute-owned draft, template, source, and set digests. If --draft-sha256 is present it must equal the current render. Changed item meaning, intent, dispositions, template bytes, source bytes, or set bytes make the bound review invalid. Inspect is read-only: it reports the current measurements, the gaps, the whole derived draft, the note coverage, and the dependency findings, including when the on-disk draft.md does not match the record.

freeze is refused when the canonical book is the checkout or lies inside it. The refusal is `freeze on the live checkout is outside this slice` and it writes nothing. On an outside book, freeze rechecks sources, notes, template, set bytes, review binding, dispositions, intent, items, and dependency classifications. It refuses missing or stale required refs, ambiguous refs, unresolved declared notes, and a draft digest that is not the reviewed digest. It writes measured-file snapshots and a prime-pack-sources/1 manifest under the authoring directory, then runs the pinned checker without --root. A checker failure leaves the staging files and does not write the page. On a match, it exclusive-creates work-home/05.NN.md with the exact reviewed draft bytes. An existing page or partial page is an occupied slot and is not overwritten. The page does not allocate a return, does not say approved, and does not launch a builder.

Return intent is derived only for a work directory matching 05NN.subject. The intended return directory is 01NN.subject in the same work band. N7NN is reported page-local and is not created. If another 01NN directory exists, the status is occupied and the occupant name is reported. If none exists, the status is unfiled. If the exact return directory exists, the status is named-slot-present. All three block readiness. Freeze may still emit the unreleased work page on an outside book while the footer says readiness blocked. No file is created in the return band.

## Current-book preview
Profile 0423-to-0526 on D:\Git\lib-build may start and update an authoring record in the next free slot after 05.01. It must not write 05.NN.md, must not change 05.01, and must not freeze. Demonstration text is supplied synthetic. The open session is the preview Prime can inspect. It is not the Prime pilot.

## Limits
No worker loop, no migration, no kernel or law or 00.live or current-assignment edit, no N3NN address, no N1NN receipt, no 0184 fallback, no Git publish, no network, no model call. A clean check, a frozen page, and a reader answer are not release readiness. Same-user actions between a hash read and a subprocess are not closed.
