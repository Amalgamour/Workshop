# Contract — workflow pass03 delta

date: 2026-11-01
who: Grok-2
state: written before labs/colab-workflow-pass03

Predecessor labs/colab-workflow-pass02/colab_workflow.py sha256 4a2ece9e646224468b36ce63947c739d8ecd73155fbb62fb34f0442cbd2dceec, 47247 bytes. Pinned producer labs/colab-support-pass02/colab_support.py sha256 2b720434ac4c4331835c1484b0eca362e01e8afbecde0ab800ca392530abf68b, 53892 bytes. This contract does not retarget those pins.

This slice is the custody and order substrate for one disposable investigation book. It is not a reserved-exposure checker, not an app door, and not a migration. Prototype ready and blocked results are not copied. V01–V03 are not implemented here.

## Schemas

Unchanged names: colab-exchange-result/1, colab-exchange-open/1, colab-exchange-review/1, colab-exchange-seal/1, colab-exchange-partial/1, colab-exchange-provenance/1, colab-package-digest/2, colab-package-verification/2, colab-config/2.

Changed: the investigation schema is colab-exchange-investigation/2. A pass02 record is unknown schema. Pass03 does not rewrite it.

New object colab-exchange-local-return/1, stored at passes.<05.NN>.return when the selected route is used. Exact keys: schema, kind, return_sha256, return_bytes, declared_transport, package_digest, pass. kind is page-local. return_bytes is the integer length of the raw file. declared_transport is the supplied label. package_digest is the attached package digest. pass is the slot id.

Legacy place-return remains. Its object keeps the pass02 keys and adds kind with value n1nn. Exact keys: kind, manifest_sha256, member, origin_batch, origin_book, origin_page, receipt_sha256, return_bytes, return_sha256. That object is not a local seal.

The command result schema stays colab-exchange-result/1. Show is not byte-identical to pass02: each loaded page gains transitions, and each pass flag gains return_kind. A partial page is reported as partial true, passes [], transitions null. The null list means the history was not loaded. An empty transitions list on a loaded page means no transitions were stored, which a successful open does not produce.

## Canonical return bytes

The canonical bytes are the bytes of the file passed to --return-file. They are stored at artifacts/<pass>/return.md and projected to 05.NN.return.md. Those two files are the same bytes. The slot holds the sha256 and the length. LF and CRLF are both stored as supplied. The tool does not transcode newlines.

RETURN_LIMIT is 1048576 bytes. A larger regular file refuses declared limit and writes nothing. declared_transport uses the existing one_line rule: non-empty text, no character below U+0020, at most TEXT_LIMIT 4096. A violation refuses malformed declared transport.

Links, relative paths, and non-regular inputs refuse through the existing path checks. A declared transport is not authenticated provenance.

Identical replay is the same local-return object and the same two files. The result is repeat, wrote false, and the transition list is unchanged. Different bytes, or a legacy return already in the slot, refuse occupied different content with wrote false. The same bytes and the same package digest with a different label refuse declared transport differs, wrote false, and the stored label stays. Return-byte agreement is not semantic acceptance, review, or release.

A later load refuses hash conflict when the artifact, the projection, and the slot disagree, or when either return file is missing while the slot has a return, or when a return file exists while the slot has none. A reparse on those paths refuses unsafe path. The load does not rewrite the files.

## seal-return-local

```
seal-return-local --book ABS --page NNNN.name --pass 05.NN --return-file ABS --declared-transport TEXT
```

The pass must already be in the record and must already have a package. Otherwise missing investigation. The command does not allocate a pass and does not place an N1NN member.

## open-pass

```
open-pass --book ABS --page NNNN.name --pass 05.MM
```

Count loaded reviews whose route is request-next and whose next_pass is 05.MM. Zero refuses next pass not requested. More than one refuses conflicting requests. The requester’s pass number must be strictly lower than 05.MM. Equality or a lower target refuses earlier pass. That earlier refusal covers a request that names its own pass. The requester must have a package. A missing return refuses sealed return missing. A return whose kind is not page-local refuses local return required. An N1 placement does not qualify.

When the slot is absent, the command adds one empty slot, notes [], package null, return null, review null, and one open-pass transition. It writes no 05.MM.pack.md, no 05.MM.return.md, no 06.MM.notes.md, and no 06.MM.review.md. It does not launch a model or fabricate those texts. Derived projections 01.md and 08.md may change. Every earlier pass’s pack, notes snapshot, notes projection, return artifact, return projection, and review projection stay byte-identical.

When the slot is already present and exactly one open-pass transition for that pass names this same requester and the same review sha256, the result is repeat, wrote false. The slot is not cleared, including after a later attach. Any other existing slot refuses occupied pass when its creating transition is open, and occupied different state otherwise.

Under one review per pass, the review that opened a later pass still has to name that pass. A second review that names the same future pass cannot be introduced through these commands without breaking that recorded link. The conflicting-requests branch still runs on a loaded record. The occupied-pass and occupied-different-state branches also still run. Tests may exercise those three branches with synthetic in-memory records. A sealed book that cannot represent them without a hash conflict is reported as hash conflict, not rewritten into a conflict.

## Transitions

The list is record.transitions. There is no second queue. TRANSITION_LIMIT is 64. A longer list refuses declared limit.

Each object has exact keys action, facts, pass, prev, seq, sha256. seq starts at 1 and is contiguous. prev is null on the first object and otherwise the previous object’s sha256. sha256 is the sha256 of the canonical JSON of the object without its sha256 field. action is one of open, attach, append-note, place-return, seal-return, review, open-pass.

facts:

- open: page, title, targets_sha256
- attach: package_digest, pack_sha256, notes_sha256, verification_sha256, zip_sha256
- append-note: notes_count, note_sha256
- place-return: kind n1nn, manifest_sha256, member, origin_batch, origin_book, origin_page, receipt_sha256, return_sha256, return_bytes
- seal-return: kind page-local, return_sha256, return_bytes, declared_transport, package_digest
- review: route, next_pass, review_sha256
- open-pass: opened_pass, requested_by, review_sha256

Every successful mutation appends exactly one object. The previous list is the unchanged prefix. Identical replay appends nothing. The first object is open for the pass named by the open request. Each later pass has one open-pass object. Slot package, notes, return, and review must match the latest matching transition, and the counts of note and return and review transitions must match the slot. An open-pass object must still match the requester’s current page-local return, package, and request-next review.

Show includes the stored list on a loaded page and writes nothing. return_kind is null, page-local, or n1nn. explicit_finish, review_recorded, return_placed, and review_pending keep their pass02 meanings. review_pending false is not completeness. return_placed is true for either return kind. No complete flag is added.

## Seal checkpoint

Before a mutation, require_loaded reads investigation.json and seal.json. The seal schema stays colab-exchange-seal/1. Its sha256 must equal the sha256 of the investigation bytes. Those bytes must parse as schema /2, and the transition chain and the slot files must agree as specified above. The new list’s prefix is that loaded list. After a successful commit, seal.json is the sha256 of the new canonical record, which includes the extended list.

That is the whole checkpoint. The tool does not keep a second copy of the previous seal. A person who rewrites investigation.json and seal.json together, and recomputes every transition hash, is not detected. The chain is not authentication, not an external clock, and not tamper-proofing.

## Commands kept

propose, open, attach, append-note, place-return, record-review, and show stay. Attach still requires the pinned producer file and runs verify --output --config --json. A stub may be used only in tests that say they are synthetic. The ordinary two-pass evidence calls the real producer. Config paths stay out of provenance. place-return still requires the inspector and the helper. record-review still refuses a review before a return, a conflicting review, and a request-next whose next pack file already exists. That last refusal remains after the commit, with wrote true, as in pass02. open-pass does not create that pack file.

Exit 0 writes canonical JSON to stdout. Refuse exits 2 with canonical JSON on stdout, reason and wrote set, and empty stderr. Usage exits 2 with stderr usage and a newline.

## Projections

01.md lists sorted pass ids in one passes line. It no longer copies pass02’s single pass line. 08.md uses the pass02 member sentence for an n1nn return. A page-local return renders as: pass, page-local return, sha256, bytes, transport, package digest, and file name. Neither projection is the canonical return.

## Compatibility

Pass02 remains the tool for schema /1 books. Pass03 does not open those books and does not claim byte-identical investigation records, show JSON, 01.md, or 08.md. Ordinary refusal reasons of the kept commands stay where the new checks do not name a more specific reason. No live book, no 00.kernel write, no capture reservation, no 0184 allocation, no receipt, and no Git write is added.
