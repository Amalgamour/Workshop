# Resolution report — three deferred historical rows

Date: 2026-10-27. Recorder: Grok Builder 2. This is a plan. It captures none of the three historical targets and allocates no archive member for them.

Inventory commit: `75ae515d826482113c4126274d015de112aa249b`. Inventory plan: `evidence/plan05.03/backfill-plan.json`, SHA-256 `28994db7ef036af72282d0ff42068d090a7fbbeb5bc23ab550f8e5852b4fd16c`, 84040 bytes. That file is unchanged. The old report is unchanged.

The old plan left these three rows unresolved, with empty payload lists, because a named directory had more than 12 files or a named path was absent. This plan drops that bound for these three rows only. A larger target-owned directory is evidence. Other inventory rows stay outside this plan.

Every companion below was read with `git cat-file blob` at the inventory commit. Hashes were computed from those bytes. No archived script was executed. No product suite was rerun. No product file was edited.

## How a candidate is described

Each candidate keeps its own origin book, page, and batch. The return source is the whole page at the inventory commit, including the Director reply inside the return and the Prime Review section. `includes_prime_review` is true and `retrospective` is true because that is what the old row recorded and what the page bytes contain.

Checkpoint custody means the whole return page, stored as the bytes at the inventory commit. Recovery of an originally delivered artifact means a declared hash and length match a retained blob. Those are separate statements. A file can be checkpoint evidence of the inventory tree and still be the wrong bytes for a hash the return declared.

Relationships used here: delivered artifact, source input, review/test evidence, proposed/future output, cited dependency, genuinely absent evidence. Unknown means the return declared a hash and no retained blob in this repository has it.

## Reconciliation

| Old row | Old unresolved items | Old payloads | Companions now | Still unknown |
| --- | --- | --- | --- | --- |
| `0506.clerk-handoff/05.03` | 4 | 0 | 29 | 0 |
| `0508.return-capture/05.01` | 3 | 0 | 37 | 3 code files |
| `0509.pack-assembly/05.01` | 1 | 0 | 47 | 0 |

The eight old items are classified below. Companions also include files the returns name that the old row omitted when it withheld the whole proposal.

## `0506.clerk-handoff/05.03` — accepted seam design

Return `00.kernel/00.00.10.work/0506.clerk-handoff/05.03.md`, SHA-256 `59468d0976229899136f0120df3315583de65a79e4e06d8ec5bcd3b94cce50dd`, 14383 bytes. Verified against the inventory blob. One Review heading. Prime's disposition in the page is ACCEPTED AS DESIGN INPUT.

This candidate is checkpoint custody of that whole page, plus recovered design artifacts, plus recovered input snapshots. It is not a recovery of a later seam implementation.

Delivered artifacts, 8, all verified:

- `06.06.md`, SHA-256 `be428b4069d9d63ed03cd5cc5e9f175fb24d91c8fa1ea42b5c0d4845a84325ae`, 7839 bytes. The return prints the prefix `be428b40`. The full hash is the inventory blob at the path the return names.
- `evidence/design05.03/SEAM.md`, SHA-256 `ef0c75072d050a77f9a5ac59449165a00a7752244ce4ea2576b38564389c8930`, 18616 bytes. The return prints the prefix `ef0c7507` and the length 18616. The design manifest line matches.
- Five example files listed by `evidence/design05.03/SHA256SUMS.txt`. Each inventory blob matches that line.
- `SHA256SUMS.txt` itself, SHA-256 `b3f9dcf780081d4e016ea69ef9de4cb903de0a9ceeb041668452bb65f19da0b7`, 579 bytes. That is the hash the return records. The file lists the six design files and does not list itself.

`examples/app/clerk-seam.json` is one of those delivered examples. The proposed module `app/clerk-seam.json` is a different path and is absent at this commit.

Source inputs, 16, all verified:

- `evidence/pack05.03/source-manifest.tsv` names 15 files at commit `54274e698dde1c6cbd5e25177395c62c2a2c645a`.
- Each file under `evidence/pack05.03/inputs/` matches that row. The same hash matches `git cat-file` of that path at `54274e69`. `source_path` in the plan is the bundle. `logical_name` is the path in the manifest.

Review evidence, 5, verified as inventory blobs. The directory is `evidence/prime-review-05.03-2026-10-27/`, named by the page. `reviewed-return.md` is SHA-256 `936023d145ff6fd84423eee25779fa27a14cd7c586c74f04ca3cc8658088c562`, 11954 bytes, the hash the review prints. Two of the files are Python. This plan does not execute them.

Old items:

- `evidence/pack05.03/inputs`, 15 files. Expanded. All 15 are source inputs. The directory was withheld by the 12-file bound.
- `app/clerk_seam.py`, `app/clerk-seam.json`, and `app/tests/test_clerk_seam.py`. Proposed future outputs. The return names them as the next slice and says the command and the tests were not run. All three paths are absent at the inventory commit. Later worktree files of those names were not read and are not companions. The proposed dispatch in `app/librarian.py` and the proposed README section are the same kind of proposal. The `librarian.py` bytes inside the input bundle are the frozen input.

## `0509.pack-assembly/05.01` — assembler return and evidence

Return `00.kernel/00.00.10.work/0509.pack-assembly/05.01.md`, SHA-256 `9545b7457a0e37fbcd3efeec2a379fcef6e4a02e2c41558a18673a7b14ae89a7`, 10398 bytes. Verified. One Review heading. The embedded disposition accepts the fixture component. This plan does not publish it.

Two separate facts:

- The whole page is checkpoint custody of the inventory bytes.
- The lab files at their Git paths match the hashes the return declared, so those lab files are the originally delivered bytes.

Delivered artifacts, 6, verified:

- `labs/pack-assembly-pass01/pack_assembly.py`, SHA-256 `75d49679cbf3e624a82573229ca8c7cd9b758799bc26b6f080111feb6eaa275c`, 43928 bytes.
- `labs/pack-assembly-pass01/README.md`, SHA-256 `bfc2178908889fb238d8c7218683ef8367c57fe65cc94df54fe1f21f825ecd68`, 4849 bytes.
- `labs/pack-assembly-pass01/tests/test_pack_assembly.py`, SHA-256 `e39a9481ac66ddef1fd76d6bd17083d3d5f236756384843c3552c3307e1a0296`, 31745 bytes.
- `labs/pack-assembly-pass01/evidence/SHA256SUMS.txt`, SHA-256 `58e67e2d12045ce1f2daf0483eb2041e2e0c4f6f72fd80781fce007e5e692574`, 253 bytes. Its three lines are the three files above.
- `00.kernel/00.00.10.work/0509.pack-assembly/06.02.md`, SHA-256 `d09497bcdb699bac1477cc96d100d64cdce41216b8e0874577e3745194897fe7`, 9815 bytes.
- `evidence/build05.01/SHA256SUMS.txt`, SHA-256 `a2156b25bbd13261a66be928dc82a365c22d98f4adaf84f1a3cbcefd90991b38`, 2220 bytes.

Review and test evidence, 32. Twenty-six build files match `SHA256SUMS.txt`. The lab log `labs/pack-assembly-pass01/evidence/tests.txt` has the same hash as the build copy of `tests.txt`. Five files are `evidence/prime-review05.01/`. Named checks inside that set: `draft-05.14.md` is SHA-256 `589bd1b842927b31e93c4238b5fa95bc221d03af13c8a9b058a52176eddcbace`, 1058 bytes; `source-manifest.json` is SHA-256 `b4a17dc7668b37a079c2de1dd02fba6d6450af278e3adb3bcd4c0fad620a0665`, 481 bytes; `completion-receipt.json` is SHA-256 `40ba90694101645a5e9b65500a36f54a8ad14b4716ccd5da9cf5c4d9d4e95d49`, 1539 bytes. Empty logs in that directory are the empty-file hash and are listed by the sums file.

Source inputs, 7, and cited dependencies, 2. `evidence/pack05.01/source-manifest.json` is SHA-256 `4db26ef3c1d9c0a2ee03eef2469fc84f146d02b1e4e4ff6ce66c682285f40d75`, 1862 bytes. Each snapshot matches a manifest row. `source_path` is the snapshot. `logical_name` is the manifest path.

- Checker: `snapshots/0003.blob` is SHA-256 `9bbd9d57f3b7da43234ac2e6ae4ce40a0ab6af2f53c8135ecfb2ee0c8a6e322d`, 21563 bytes. The manifest logical name is `labs/pack-custody-pass01/pack_check.py`. `labs/pack-assembly-pass01/pack_check.py` is absent at the inventory commit. The return says this checker was not edited. This plan does not execute it.
- Jobs formatter: `snapshots/0006.blob` is the pin of `00.kernel/00.00.01.law/0303.jobs/02.jobs.010.py`. The return says it was not run. This plan does not execute it.
- `snapshots/0007.blob` is an earlier pin of `0508.return-capture/05.01.md`, 9747 bytes, SHA-256 `fca5b450312f0201fa9a2e60d686cb3e982524266030a54353d65dfb6655001e`. The inventory page of that path is the 18493-byte file in the next section.

Old item: `evidence/build05.01`, 27 files. Expanded. The sums file accounts for the other 26. Nothing in that directory is missing.

## `0508.return-capture/05.01` — first capture implementation, held

Return `00.kernel/00.00.10.work/0508.return-capture/05.01.md`, SHA-256 `9da830f28f340fb6142a12908e8d60a3b5050cc8ff075d32405133f39853d472`, 18493 bytes. Verified. One Review heading. The disposition is HELD FOR RC-01 REPAIR. This candidate keeps that hold. It is checkpoint custody of the page, recovery of the files whose declared hashes still match, and an explicit unknown for the three code files whose declared hashes do not.

Recovered delivered bytes, verified:

- `labs/return-capture-pass01/demo.py`, SHA-256 `b205d0ddf5136416ab5767f04c505bfff89ae82efd419409e726e586073d865b`, 13969 bytes.
- `labs/return-capture-pass01/inventory.py`, SHA-256 `765765cbdab87ec17304cd891c1f46ddfe7249d9128f0f203a1fd9dc0609aa64`, 4462 bytes. This plan does not execute it.
- `06.02.md`, SHA-256 `fc3ba08e9fa676dec9d76c9c663693a799146483b924bef3320a479eaf3d689d`, 10669 bytes.
- Three evidence `after/` copies match the return's After column: `0100.band.returns/01.md` SHA-256 `55c5e8e285c5fda8ab7f29c211e987ddf5a9a6b12cd5bb9fb5468a28f7319fee`, 1488 bytes; `0500.band.packs/01.md` SHA-256 `c0b8516b834d89a28bfed23a4779629be7b00556f21ff029d174ff9040e7b053`, 2561 bytes; `0014.design/01.001.md` SHA-256 `20ba376e05a5ab09fed5d6e9644e3e74a6db954d7e476ff94f76b6469c780d0a`, 1448 bytes. `source_path` is the evidence copy. `intended_logical_name` is the furniture path.

The inventory blob of `0500.band.packs/01.md` and of `0014.design/01.001.md` has the same hash as the matching after copy. The inventory blob of `0100.band.returns/01.md` is SHA-256 `9d9efcd2f5bfbb5b`, 2844 bytes. The delivered after bytes stay the evidence copy.

Three `before/` copies match the return's Before column. They are source inputs, retained prior bytes.

Unknown, and left without companions:

| Declared path | Declared hash | Declared bytes | Inventory path |
| --- | --- | --- | --- |
| `labs/return-capture-pass01/return_capture.py` | `655bd4a005d1210eef8f5ae62a462d4cf8a2591bfe318c2f428bcfb3ae5c3269` | 45898 | SHA-256 `8f3da5c651f6924fca6dedb0b95da7d181eb58884dc030dd9cbc3d8b6a5b15ac`, 45767 bytes |
| `labs/return-capture-pass01/README.md` | `4d82b7feeacf055f180f9a6c483bfa920faccbd0788fc15482732c0cf3f8de4e` | 8515 | SHA-256 `281d31c026d0bbb213a1d3a793c17175fe5d4ed8527d1f0ba8567d579f9c21e4`, 9162 bytes |
| `labs/return-capture-pass01/tests/test_return_capture.py` | `9de8908a371839789586bee10f2d3a01d4a53b43cea5db2efeaa5c625a87afbe` | 26254 | SHA-256 `842547f798288af6b82baeedd2adf48d59c0723e3756dfecef8c4fcafc5bc2ba`, 42348 bytes |

`git cat-file -t` does not find the three declared hashes in this repository. `custody.json` records the same three hashes and itself matches the return: SHA-256 `c3cc6baafc8321f01a177cdfc93540e593ed6f04dfc3fededc16002cacade1f3`, 7893 bytes. The inventory `return_capture.py` is the later helper pinned by this batch. It is not a companion of the 05.01 candidate.

`evidence/build05.01` has 15 files. All 15 are companions. `discovery.patch` matches SHA-256 `3d4403419817c7d562e7c6173edbe55b8ec347118281940f87a1725d148165fe`, 3585 bytes. This plan does not apply it.

`evidence/pack05.01` has 12 snapshots and `source-manifest.json`. Each snapshot matches the manifest. The manifest records commit `e6d6eb75538732c7eedbc840042242d386b25c2f`. These are input pins. `snapshots/0007.blob` is the pin of `0504.app-entry/05.06.md` named by the return. `snapshots/0011.blob` is the pin of `labs/clerk-handoff-pass02/README.md` named by the return, SHA-256 `13e5148f91957a109a2560622c09c87de5369c6e1e3591cb223de252440914cc`, 8530 bytes.

`evidence/prime-review05.01/` has 6 files. They are review evidence. They do not convert the hold into acceptance.

`labs/return-capture-pass01/.gitignore` is present, 23 bytes, and is not in the return's lab table. It is not a companion.

Old items:

- `returns`, 15 files. `git ls-tree` confirms 15 files. The return names that root as the bootstrap location new submissions were to leave. Those files are other historical returns. This plan does not expand them and adds zero companions from them.
- `evidence/build05.01`, 15 files. Expanded, as above.
- `returns/01.md`. Absent at that exact path. The return's furniture path is `0100.band.returns/01.md`. Calling the old path a suffix of the furniture path is an inference from the two spellings. The absence itself is verified.

## Next batch

One batch: `0506.clerk-handoff/05.03`, book `00.00.10.work`. No member number. No capture in this plan.

That row is the accepted design. Its old block was the 15-file input directory and three proposed app paths. The inputs now match their manifest. The app modules stay proposed. The design bytes match their manifest.

`0509.pack-assembly/05.01` is hash-complete and is not the selected batch. `0508.return-capture/05.01` stays unselected while the three declared code blobs are unknown. The held review stays held.

## Verified, inferred, unknown

Verified: the three return hashes and lengths; every companion hash in `resolved-slices.json`; the design sums; the 15 input rows against both the bundle and commit `54274e69`; the pack-assembly sums and both pack manifests; the three pack-assembly lab hashes; the return-capture files whose declared hashes match; the absence of the three unknown hashes as Git objects; the absence of the three proposed app paths and of `returns/01.md`; the 15-file `returns/` listing; the 0100 furniture mismatch at the inventory path.

Inferred: the old names `returns` and `returns/01.md` come from the return's bootstrap wording and from `0100.band.returns/01.md`. This plan does not have the old scanner. The classification of the app modules as proposals is the return's own next-slice wording, checked against absence at the commit.

Unknown: the original bytes of `return_capture.py`, `README.md`, and `tests/test_return_capture.py` declared by `0508.return-capture/05.01`.
