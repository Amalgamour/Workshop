# Prime use — 0521.return-placement/05.04

Date: 2026-11-02. Executor: Grok-2. Reviewer: Codex Prime.
This page is the builder's handoff. It is not acceptance, seating, publication, or a live release.

## What is ready for review

`labs/return-lines-pass02/return_lines.py` reconstructs corrected return pages, publishes them on a caller-supplied copy, and retires every audited old member. It loads frozen pass01 by pin and does not edit it. `adopt` is refused. The live work book is refused. A door-marked book proceeds only under a synthetic `return-line-authorization/1` whose book path, roots, layout hash, plan hash, audit hash, audit length, operation, and release text match the command.

Read `06.07.md` for the invocation, the claim, and the measured result. Read `CONTRACT.md`, `FAILURE.md`, and `AUTHORIZATION.md` for the rules written before the tool. Read `commands.txt` for the rehearsal command and the phase exits.

## What the copies showed

Work root: `D:\librarian\temp\0521-0504\20261102T173638945721Z-suite`.

One primary copy went through plan, init, stage, reconstruct, publish, and retire. Lookup by old member then resolved the new logical home and the retained original. `0154.colab-support-first-0501` stayed incomplete, with null return hash and length, and no invented `return.md`. Seven synthetic filings then used the freed lines: two passes on `0121.synthetic-filing`, one each on `0122` through `0125`, and one page-local pass on `0721.synthetic-local`. Receipts stay `accepted` false.

A second copy retired and then rolled back, before any filing on that copy. Original bytes returned. The created logical return was removed. The page-local tail stayed.

`colab/labs/0709.return-migration-check/pass01/seam.py` ran unchanged against a third copy of the retired book. Both the new capture descriptor and the relocated `0101` descriptor prepared with exit 0, custody verified, and `task_association` `not-established`. That seam file is outside the 37-file pack manifest.

The plan hash on the copy equalled `52951e1dbc0f37fa7f8c76be390a9510999a6944d7dc9f4e20c00c365f326f66`. The contract does not require that equality. Live source bytes and the door were unchanged. The fingerprint that includes the door is `75061b0c183e299c36623e809be8518a0d6efd4482ff13ed3bb3d4865c5e2e6d`.

## What this review does not authorize

Live migration, a band-door edit, caller enforcement, an app change, N3NN registration, and filing of `0121.return-placement` stay outside this pack. The disposable retired root is not an approved live archive. A verified receipt is not approval. Exit 0 is a finished rehearsal. `## Review - Codex Prime` on `05.04.md` stays `PENDING` until Prime writes it.

The builder did not allocate `0184`, did not call `return_capture.py`, and did not write `05.04.return.md`.
