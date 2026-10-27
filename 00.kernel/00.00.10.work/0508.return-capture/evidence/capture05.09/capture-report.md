# Capture report — seam design and AR-01

Date: 2026-10-27. Recorder: Grok Builder 2. This report is current work. It is not the historical page.

## Custody

Member `0124.clerk-seam-design-0503` is checkpoint custody of the whole page `00.kernel/00.00.10.work/0506.clerk-handoff/05.03.md` at commit `75ae515d826482113c4126274d015de112aa249b`, plus the 29 companions from the preserved 05.08 plan. The return hash is `59468d0976229899136f0120df3315583de65a79e4e06d8ec5bcd3b94cce50dd`, 14383 bytes. Design files match the design manifest that the preserved plan already checked. The 15 input companions are the pinned bundles, recovered by those recorded hashes. This capture is not a new seam implementation and it is not a fresh approval. Proposed app modules are not companions. Input files and review scripts were stored as data and were not executed.

## AR-01

The preserved 05.08 plan, notes, submission, and member `0121` are unchanged. The additive file is `evidence/capture05.09/resolution-addendum.json`. Three original code files are retained at the same commit. Their Git source paths are the snapshot files. Their logical paths are the names in `evidence/pack05.02/source-manifest.json`. SHA-256 of the blob bytes matches the declared hashes. A SHA-256 digest is not a Git object id in this SHA-1 repository. The RC-01 hold remains. This batch does not capture `0508.return-capture/05.01` or `0509.pack-assembly/05.01`.

| Source path | Logical path | SHA-256 | Bytes |
| --- | --- | --- | --- |
| `evidence/pack05.02/snapshots/0008.blob` | `labs/return-capture-pass01/README.md` | `4d82b7feeacf055f180f9a6c483bfa920faccbd0788fc15482732c0cf3f8de4e` | 8515 |
| `evidence/pack05.02/snapshots/0009.blob` | `labs/return-capture-pass01/return_capture.py` | `655bd4a005d1210eef8f5ae62a462d4cf8a2591bfe318c2f428bcfb3ae5c3269` | 45898 |
| `evidence/pack05.02/snapshots/0010.blob` | `labs/return-capture-pass01/tests/test_return_capture.py` | `9de8908a371839789586bee10f2d3a01d4a53b43cea5db2efeaa5c625a87afbe` | 26254 |

## Historical capture

Submission `historical-0506-0503`. Origin book `00.00.10.work`, page `0506.clerk-handoff`, batch `05.03`. Flags: retrospective true, `source_commit` `75ae515d826482113c4126274d015de112aa249b`, `includes_prime_review` true. Manifest `94487a067c1da03bd7f8cfba29578fd1e52d11c643ff55397044c4c7829454dc`. Receipt `74faa288e05e74403cae4d3dc4c1745b20bd31094096118b2ff139384da612e0`, 303 bytes, hashed from `receipt.json`. Fresh verify exit 0: result complete, not approved, not accepted, not published. Fresh inspect exit 0: status `complete`, problems empty, the same flags and the 29 payload hashes. Member bytes were hashed before verify and again after verify and after inspect. Both reads left every member file unchanged.

Each row below was exported with `git cat-file blob` into a disposable staging directory, hashed there, and matched to the preserved plan before capture. `source_path` is the inventory path that supplied the bytes. `logical_name` is the reservation name. Where they differ, the bytes are the pinned input bundle, not the live file at the logical path.

| # | Logical name | Source path | SHA-256 | Bytes |
| --- | --- | --- | --- | --- |
| return | `00.kernel/00.00.10.work/0506.clerk-handoff/05.03.md` | same path at the inventory commit | `59468d0976229899136f0120df3315583de65a79e4e06d8ec5bcd3b94cce50dd` | 14383 |
| 0001 | `00.kernel/00.00.10.work/0506.clerk-handoff/06.06.md` | `same` | `be428b4069d9d63ed03cd5cc5e9f175fb24d91c8fa1ea42b5c0d4845a84325ae` | 7839 |
| 0002 | `00.kernel/00.00.10.work/0506.clerk-handoff/evidence/design05.03/SEAM.md` | `same` | `ef0c75072d050a77f9a5ac59449165a00a7752244ce4ea2576b38564389c8930` | 18616 |
| 0003 | `00.kernel/00.00.10.work/0506.clerk-handoff/evidence/design05.03/examples/app/clerk-seam.json` | `same` | `29ed7bd914067cae4e116488829cf61d987714e3528da47d57a335eeea464749` | 323 |
| 0004 | `00.kernel/00.00.10.work/0506.clerk-handoff/evidence/design05.03/examples/fixture/bridge/job.json` | `same` | `4d57cdb9ea210bfaedf4bdf6974c723735abcf431cb16b3ec946222fab05e1cf` | 496 |
| 0005 | `00.kernel/00.00.10.work/0506.clerk-handoff/evidence/design05.03/examples/fixture/clerk-link/bridge-0001.json` | `same` | `1141738b55af63b4d3425c26fd1e877772f53177bed542eb9b319526f87dc859` | 345 |
| 0006 | `00.kernel/00.00.10.work/0506.clerk-handoff/evidence/design05.03/examples/router/clerk-job.json` | `same` | `c4c9ddd38d3da0f72570404be23eb4c267d78653ff0ac23f0741ad8433bb1f5f` | 350 |
| 0007 | `00.kernel/00.00.10.work/0506.clerk-handoff/evidence/design05.03/examples/router/instructions/task.md` | `same` | `6c913091d80948e3be49fa384b023ee3c43762599f3f61b47db885b4f846fe66` | 175 |
| 0008 | `00.kernel/00.00.10.work/0506.clerk-handoff/evidence/design05.03/SHA256SUMS.txt` | `same` | `b3f9dcf780081d4e016ea69ef9de4cb903de0a9ceeb041668452bb65f19da0b7` | 579 |
| 0009 | `00.kernel/00.00.10.work/0506.clerk-handoff/evidence/pack05.03/source-manifest.tsv` | `same` | `b9cd0760aa11fd9defd5ca0d22a22bce37b365c587dd8094a61000fafd3623b5` | 2284 |
| 0010 | `00.kernel/00.00.10.work/0506.clerk-handoff/01.md` | `00.kernel/00.00.10.work/0506.clerk-handoff/evidence/pack05.03/inputs/00.kernel/00.00.10.work/0506.clerk-handoff/01.md` | `ec47b135cfd7614f5535ac600d7ec2e94d8cab6c6299e21296d7da0c8a9603f1` | 1409 |
| 0011 | `00.kernel/00.00.10.work/0506.clerk-handoff/05.01.md` | `00.kernel/00.00.10.work/0506.clerk-handoff/evidence/pack05.03/inputs/00.kernel/00.00.10.work/0506.clerk-handoff/05.01.md` | `7c68b7d4095aeec9563b0ccdbdd73d4050c4d31817efbf148fa25e4a223861e6` | 11307 |
| 0012 | `00.kernel/00.00.10.work/0506.clerk-handoff/05.02.md` | `00.kernel/00.00.10.work/0506.clerk-handoff/evidence/pack05.03/inputs/00.kernel/00.00.10.work/0506.clerk-handoff/05.02.md` | `7c96dfa17db7eda44535adbb86677380def3c00a27b7acc7958e301de1a6f469` | 4270 |
| 0013 | `00.kernel/00.00.10.work/0506.clerk-handoff/06.01.md` | `00.kernel/00.00.10.work/0506.clerk-handoff/evidence/pack05.03/inputs/00.kernel/00.00.10.work/0506.clerk-handoff/06.01.md` | `1de4675be5cd393868bc751cdc3d97b2bf8882bba7b88037b746de1510728be5` | 4285 |
| 0014 | `00.kernel/00.00.10.work/0506.clerk-handoff/06.02.md` | `00.kernel/00.00.10.work/0506.clerk-handoff/evidence/pack05.03/inputs/00.kernel/00.00.10.work/0506.clerk-handoff/06.02.md` | `c2e37d3ba93d45d72e2c0110bd3199e03d66bb8ddab5da9710c196a12ef48509` | 9337 |
| 0015 | `00.kernel/00.00.10.work/0504.app-entry/05.05.md` | `00.kernel/00.00.10.work/0506.clerk-handoff/evidence/pack05.03/inputs/00.kernel/00.00.10.work/0504.app-entry/05.05.md` | `5a52d9e9905faf2cbb36e4b0d70e701fbab55b63faccb8617ed8e507341c5d6f` | 17442 |
| 0016 | `00.kernel/00.00.10.work/0504.app-entry/05.06.md` | `00.kernel/00.00.10.work/0506.clerk-handoff/evidence/pack05.03/inputs/00.kernel/00.00.10.work/0504.app-entry/05.06.md` | `8365ec5ebe811d34bb61f81d5ce8b46a212fbf3b1dd334a1a6d81d7607b65805` | 3937 |
| 0017 | `app/librarian.py` | `00.kernel/00.00.10.work/0506.clerk-handoff/evidence/pack05.03/inputs/app/librarian.py` | `24e510dbf8c55c315af1d8b6777a9f5a645abe79528967d8ef24954e916a651c` | 5909 |
| 0018 | `app/context.py` | `00.kernel/00.00.10.work/0506.clerk-handoff/evidence/pack05.03/inputs/app/context.py` | `5b1a31d47bb9f9b465a8492541467abbd9bd3a99ae524be7aa0dbffe2380eb9f` | 22063 |
| 0019 | `app/worker_bridge.py` | `00.kernel/00.00.10.work/0506.clerk-handoff/evidence/pack05.03/inputs/app/worker_bridge.py` | `69650662fa08c3bcfbfc4d180579a104a0f9edcfa39652e0aeaf741f006f6ba6` | 31166 |
| 0020 | `app/worker-bridge.json` | `00.kernel/00.00.10.work/0506.clerk-handoff/evidence/pack05.03/inputs/app/worker-bridge.json` | `94dd3c4770d77f30482f75086d6ebc58335eb51b4a8641c86dcc6d55ce4385ea` | 1136 |
| 0021 | `labs/clerk-handoff-pass02/clerk.py` | `00.kernel/00.00.10.work/0506.clerk-handoff/evidence/pack05.03/inputs/labs/clerk-handoff-pass02/clerk.py` | `b75b6d0f5afc6d901d183739817ca5b0bfba8d1b1ddda2fc5bf67f50e5e24eab` | 38060 |
| 0022 | `labs/clerk-handoff-pass02/README.md` | `00.kernel/00.00.10.work/0506.clerk-handoff/evidence/pack05.03/inputs/labs/clerk-handoff-pass02/README.md` | `263dc2d2d57c22c469347efcce02a47c387e428ae03e27b6da6ae9d0e9115ca6` | 6882 |
| 0023 | `labs/worker-bridge-pass01/docs/CONTRACT.md` | `00.kernel/00.00.10.work/0506.clerk-handoff/evidence/pack05.03/inputs/labs/worker-bridge-pass01/docs/CONTRACT.md` | `2d62b602bd4249d9e7cea29c56f524b69cbfac42a46e60768a2dc93aef7bcccf` | 14468 |
| 0024 | `labs/worker-bridge-pass01/bridge/adapter.py` | `00.kernel/00.00.10.work/0506.clerk-handoff/evidence/pack05.03/inputs/labs/worker-bridge-pass01/bridge/adapter.py` | `27d683b494c13bd120d5099f863bb68ab96c6d458dd2a7641c0129122b89c9de` | 17038 |
| 0025 | `00.kernel/00.00.10.work/0506.clerk-handoff/evidence/prime-review-05.03-2026-10-27/finish-correction-evidence-2026-10-27.py` | `same` | `ae91994f9fc323cc5b3e5cfd02d8ed5660eb47b1b4d7125b09baa4e3ddf6e438` | 1416 |
| 0026 | `00.kernel/00.00.10.work/0506.clerk-handoff/evidence/prime-review-05.03-2026-10-27/publication-followup.json` | `same` | `7ad292d6ebc4d97b5a1d44ada643998ab257ace5efa1d1c21970ea43d97f5426` | 2196 |
| 0027 | `00.kernel/00.00.10.work/0506.clerk-handoff/evidence/prime-review-05.03-2026-10-27/reviewed-return.md` | `same` | `936023d145ff6fd84423eee25779fa27a14cd7c586c74f04ca3cc8658088c562` | 11954 |
| 0028 | `00.kernel/00.00.10.work/0506.clerk-handoff/evidence/prime-review-05.03-2026-10-27/verification.json` | `same` | `1e6477b53475d82c265626a9da0817aff475244cb5508cc84c8b765c6bab8053` | 1974 |
| 0029 | `00.kernel/00.00.10.work/0506.clerk-handoff/evidence/prime-review-05.03-2026-10-27/verify-corrections-and-seam-2026-10-27.py` | `same` | `55dc06394b548b6f90cef5c0e23659271342b9d1c3d53bfe897f31c78c18901d` | 6866 |

## Failures

None. Capture, verify, and inspect of `0124` exited 0. No partial package was left.

## Current report

`0125.mapping-capture-0509` is the separate current capture. It is not retrospective. Its source commit is null. It does not set the embedded-review flag. This report is one of its four outputs and does not contain the later `0125` receipt.
