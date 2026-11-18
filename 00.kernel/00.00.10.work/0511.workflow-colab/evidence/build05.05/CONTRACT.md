# Contract — workflow pass04 preservation

date: 2026-11-01
who: Grok-2
state: written before labs/colab-workflow-pass04

Predecessor labs/colab-workflow-pass03/colab_workflow.py sha256 fc469af91f8bdcbaa980457535b7276a5c4e2421a81ad861e93ff750a511c944, 68410 bytes. Pinned producer labs/colab-support-pass02/colab_support.py sha256 2b720434ac4c4331835c1484b0eca362e01e8afbecde0ab800ca392530abf68b, 53892 bytes. This contract does not retarget those pins and does not edit pass03.

This slice repairs WF01. It keeps the pass03 custody and order behavior and changes only the way a commit publishes investigation.json and seal.json. It is not a reserved-exposure checker, not an app door, and not a migration.

## Schemas kept

Unchanged names and meanings: colab-exchange-result/1, colab-exchange-investigation/2, colab-exchange-local-return/1, colab-exchange-open/1, colab-exchange-review/1, colab-exchange-seal/1, colab-exchange-partial/1, colab-exchange-provenance/1, colab-package-digest/2, colab-package-verification/2, colab-config/2.

A pass02 record remains unknown schema. Pass04 does not rewrite it. Show on a loaded page keeps transitions and return_kind. A partial page is partial true, passes [], transitions null. The show result name complete means the read finished.

K1, K2, and K3 stay. seal-return-local stores the supplied bytes at artifacts/<pass>/return.md and 05.NN.return.md. open-pass creates one empty later slot only from one recorded request-next review with that pass's package and page-local return. Transitions stay in the investigation record. The transition object, fact keys, RETURN_LIMIT 1048576, TRANSITION_LIMIT 64, and TEXT_LIMIT 4096 stay as in the pass03 contract. place-return fact keys stay kind, manifest_sha256, member, origin_batch, origin_book, origin_page, receipt_sha256, return_sha256, return_bytes.

## Authority

The current authority pair is page/investigation.json and page/seal.json. It is authoritative only when all of these hold: partial.json is absent, attempt.json is absent, .write.lock is absent, seal.json is schema colab-exchange-seal/1, and its sha256 field equals the sha256 of the investigation bytes. require_loaded uses that pair. It does not read checkpoints and it does not choose among them.

## Predecessor

When neither authority file exists, the publication predecessor is none and retained_checkpoint is null. No checkpoints directory is created. No empty record and no synthetic seal is written.

When both files exist and the seal matches, the predecessor is retained-prior. The checkpoint id is the sha256 of those investigation bytes, which is the seal field. When one file exists without the other, or the seal does not match, commit refuses resume refused before it creates a checkpoint.

## Retained checkpoint

Directory checkpoints/<checkpoint id>/. Created only for retained-prior. If the directory or any of its three files already exists, commit refuses checkpoint collision, wrote false, and does not overwrite it.

Files, each created with O_CREAT|O_EXCL and written in full, never O_TRUNC:

- investigation.json, the exact prior investigation bytes
- seal.json, the exact prior seal bytes
- identity.json, schema colab-exchange-checkpoint/1

identity.json keys: schema, role, checkpoint_id, investigation_sha256, investigation_bytes, seal_sha256, publication_id. role is retained-prior. checkpoint_id, investigation_sha256, and seal_sha256 are the same digest. publication_id is the candidate that caused this retention.

The checkpoint is evidence of the pair that was authoritative at the start of that publication. It is not a second status store.

## Publication records

publication_id is the sha256 of the candidate investigation bytes. It is fixed before any authority name changes.

publications/<publication id>.json is created with O_EXCL before the authority replace. Schema colab-exchange-publication/1. Keys: schema, publication_id, predecessor, retained_checkpoint, candidate_investigation_sha256, candidate_investigation_bytes, candidate_seal_sha256. The file is not rewritten. If that file or publications/<publication id>.published already exists, commit refuses publication collision, wrote false, before it creates the lock or a checkpoint. An identical candidate therefore does not leave a new checkpoint.

publications/<publication id>.published is created with O_EXCL only after the page-root pair reads back as the candidate bytes and the candidate seal. Schema colab-exchange-published/1. Keys: schema, publication_id, predecessor, retained_checkpoint. require_loaded does not treat this file as authority.

attempt.json is created with O_EXCL before extras, projections, and the authority replace. Schema colab-exchange-attempt/1. Keys: schema, publication_id, predecessor, retained_checkpoint. If it exists at entry, commit and require_loaded refuse resume refused. On success it is removed only after the published marker exists and the root pair matches the candidate. On failure it stays.

## Staging and replacement

Candidate investigation bytes, candidate seal bytes, and projection bytes are written under staging/<publication id>/ with O_EXCL. A staging name that already exists refuses occupied staging, wrote false. Staging names are not reused and are not truncated.

publication then replaces names with os.replace from those staged files onto the page paths. investigation.json and seal.json are never opened with O_TRUNC. The replace order is projections, then investigation.json, then seal.json. Extras, including a new artifacts/<pass>/return.md, are written before the authority replace. An existing extra path is not the prior sealed pair. Prior artifact files that this commit does not name stay in place.

REPLACE_HOOK, when set by a test, runs immediately before os.replace. WRITE_HOOK, when set, runs before an exclusive or ordinary byte write, as in pass03. Neither hook is a power-loss model.

## Partial result

An exception other than Refuse writes partial.json and raises Refuse interrupted write with wrote true. partial.json schema stays colab-exchange-partial/1. Keys: schema, reason, publication_id, predecessor, retained_checkpoint. reason is interrupted write. The lock is removed in finally. attempt.json, the publication record, the checkpoint, and any staged or replaced debris stay. No command deletes them to make a later call succeed.

A later command sees partial.json or attempt.json and returns resume refused, wrote false. show reports that page partial true and does not load its transitions.

A Refuse before any of those writes, including checkpoint collision, publication collision, and occupied staging, leaves wrote false and does not write partial.json.

## What a failed commit leaves

Every failed commit leaves one of these, together with partial.json when the failure was an interrupted write:

- The page-root pair still verifies and matches the bytes from before the call. The checkpoint, when the predecessor was retained-prior and the copy finished, matches those same bytes.
- The page-root investigation is the candidate and the page-root seal is still the prior seal. The checkpoint holds the prior pair, and attempt.json names that checkpoint id.
- The predecessor was none. No checkpoint exists. The publication record says predecessor none. The unfinished open is not given a fabricated prior success.

Prior package, return, and review artifact bytes for a pass this commit does not rewrite stay hash-identical. A torn projection is not authority. The retained record and the artifact return bytes are the recovery source for that projection. The tool does not rewrite the projection during inspection.

## Inspection and recovery

There is no recover command. Prime inspection is:

1. If partial.json, attempt.json, and .write.lock are all absent and the root seal matches the root investigation bytes, that root pair is the current authority. Ignore every checkpoints directory.
2. Otherwise read attempt.json. Its retained_checkpoint is the only prior id. Open checkpoints/<that id>/ only. Verify identity.json checkpoint_id equals that id, the investigation file hashes to it, and the seal file's sha256 field equals it. Do not scan other checkpoint ids and do not pick the highest id.
3. Copying the checkpoint pair back onto the page, or deleting partial.json, is outside the tool. The tool will not do either.

No power-loss guarantee and no race guarantee. An injected exception is not a killed process and not a disk failure. AR-01 stays held.

## Commands and compatibility

propose, open, attach, append-note, place-return, record-review, seal-return-local, open-pass, and show stay. Attach still pins the v2 producer and runs verify. Identical replay still commits nothing and adds no checkpoint. Show's loaded JSON shape stays the pass03 shape. Pass03 remains the tool that truncates authority files in place. Pass04 does not open the live book, allocate 0184, write a receipt, or open a capture slot.
