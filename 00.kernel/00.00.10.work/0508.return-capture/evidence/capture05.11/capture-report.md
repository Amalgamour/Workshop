# Capture report — original held capture, 05.11
Date: 2026-10-27
Recorder: Grok 4.7, Grok Builder 2
Session: 01a17dfa-bc23-7730-bec3-c49938f96187

This report records custody of the original held capture implementation and its declared companions. A receipt is not approval, acceptance, seating, publication, or finish. The historical RC-01 hold remains.

## Custody

The capture stores the whole `0508.return-capture/05.01` page from commit `75ae515d826482113c4126274d015de112aa249b`, including its Director reply and the historical `HELD FOR RC-01 REPAIR` review, plus the 40 logical names in `evidence/pack05.11/original-source-map.json` and in `0132.return-capture-origin-0501/reservation.json`. The first 37 companions match the qualified 05.08 plan row. The last three are the recovered original delivered files from `pack05.02` snapshots `0008.blob`, `0009.blob`, and `0010.blob`, and those hashes match the 05.09 addendum. Staged bytes match the supplied SHA-256 values and lengths. Fifteen Git source paths differ from their logical names. Recovered code was not executed or installed. Today's pinned helper and reader performed verify and inspect. This is historical checkpoint custody plus declared-hash-supported artifact recovery. It does not accept the held implementation, replace today's helper, or renew an old execution request.

## Boundary

This completes custody for the three resolved deferred rows from the 05.08 plan: `0506.clerk-handoff/05.03` in `0124.clerk-seam-design-0503`, `0509.pack-assembly/05.01` in `0128.pack-assembly-0501`, and `0508.return-capture/05.01` in `0132.return-capture-origin-0501`. It does not claim that every historical return in the repository is recovered.

## Historical identities

Submission `historical-0508-0501`. Retrospective true. Source commit `75ae515d826482113c4126274d015de112aa249b`. `includes_prime_review` true. Return SHA-256 `9da830f28f340fb6142a12908e8d60a3b5050cc8ff075d32405133f39853d472`, 18493 bytes. Supplied map SHA-256 `5fffa32a59e0a9641a69417c318864330b43ceeb77d6074c5566991a12681ad4`, 26841 bytes.

Before capture the member held two files:

| Path | SHA-256 | Bytes |
| --- | --- | --- |
| `01.md` | `4bcf355d960c3d50b0c16a157a6f5f0bd36313638b0eef0356311c61b6a8f6db` | 341 |
| `reservation.json` | `7485a6ac770fb464ff199c1fcbcba2887d0cf61f304a70a0717ab79a8713a2f5` | 3454 |

Capture exited 0. Manifest `60d7f3528486a263e0a1769e3a780dbdfc93e9d9a444719f8526079a4c3f1716`, 11280 bytes. Receipt `8526f3e38c3118ae9dea0d371f051cc85f1370133b2c464e6fbf8c870b96422d`, 303 bytes. Fresh verify exited 0: result complete, not approved, not accepted, not published. Inspect exited 0: schema `return-capture-inspection/1`, status `complete`, problems empty, retrospective true, source commit set, embedded review true, 40 payloads. The member file inventory after verify matched the inventory after capture, and the inventory after inspect matched the inventory after verify. The plan, the addendum, the supplied map, and the receipts of members 0121, 0124, 0125, 0128, and 0129 were unchanged.

Post-capture member files:

| Path | SHA-256 | Bytes |
| --- | --- | --- |
| `01.md` | `4bcf355d960c3d50b0c16a157a6f5f0bd36313638b0eef0356311c61b6a8f6db` | 341 |
| `manifest.json` | `60d7f3528486a263e0a1769e3a780dbdfc93e9d9a444719f8526079a4c3f1716` | 11280 |
| `payload/0001.blob` | `b205d0ddf5136416ab5767f04c505bfff89ae82efd419409e726e586073d865b` | 13969 |
| `payload/0002.blob` | `765765cbdab87ec17304cd891c1f46ddfe7249d9128f0f203a1fd9dc0609aa64` | 4462 |
| `payload/0003.blob` | `fc3ba08e9fa676dec9d76c9c663693a799146483b924bef3320a479eaf3d689d` | 10669 |
| `payload/0004.blob` | `20ba376e05a5ab09fed5d6e9644e3e74a6db954d7e476ff94f76b6469c780d0a` | 1448 |
| `payload/0005.blob` | `55c5e8e285c5fda8ab7f29c211e987ddf5a9a6b12cd5bb9fb5468a28f7319fee` | 1488 |
| `payload/0006.blob` | `c0b8516b834d89a28bfed23a4779629be7b00556f21ff029d174ff9040e7b053` | 2561 |
| `payload/0007.blob` | `39cc192816469aa359db0853fedbb2370303af9789caa2bbc0bd061fc4bf7f68` | 2740 |
| `payload/0008.blob` | `a04962e94ae54bcb0fc2ae42dd36ff6fc33822427cb2a983211d069aeaf4b610` | 1075 |
| `payload/0009.blob` | `f66b010a74fe879431cc17093b236dd1dd113658e22c041252fe2719c0c1a3be` | 669 |
| `payload/0010.blob` | `f358b4315ee604aa20203671bcf8b97d149c9034bb694f77d31fa8e2440dc635` | 1104 |
| `payload/0011.blob` | `c3cc6baafc8321f01a177cdfc93540e593ed6f04dfc3fededc16002cacade1f3` | 7893 |
| `payload/0012.blob` | `079dc6de98157887289a9438e19e087cfc950d4dcb0e8864bdf2da988b5f382c` | 1243 |
| `payload/0013.blob` | `3d4403419817c7d562e7c6173edbe55b8ec347118281940f87a1725d148165fe` | 3585 |
| `payload/0014.blob` | `d697f57a3998d1af58987a42fa1a17273c6276336c2dd2c76aa0de0feb6a9af1` | 11970 |
| `payload/0015.blob` | `f9cef3eff1d04f4c47e67734034f13cc1fbd9bb70d76a90b983a3c118b10fa5d` | 1947 |
| `payload/0016.blob` | `61d203eb9450c60d912ef621d3848532e76e4887da7bc202453aa1b8ab344979` | 1902 |
| `payload/0017.blob` | `47814afde6ed62be1963c7816fc6ab1df4572d0916ae9e25601c3b127bfb3e91` | 2628 |
| `payload/0018.blob` | `11fcfbeb1ce238494ea5c47b7bdbf6932ae6a5b98981e76a7784df47241f4437` | 3624 |
| `payload/0019.blob` | `7f32a599bdbbe12f370afa3e4b88bcd83df6136fd9520b02637ed6856c5a2db8` | 2794 |
| `payload/0020.blob` | `f66b010a74fe879431cc17093b236dd1dd113658e22c041252fe2719c0c1a3be` | 669 |
| `payload/0021.blob` | `f358b4315ee604aa20203671bcf8b97d149c9034bb694f77d31fa8e2440dc635` | 1104 |
| `payload/0022.blob` | `a04962e94ae54bcb0fc2ae42dd36ff6fc33822427cb2a983211d069aeaf4b610` | 1075 |
| `payload/0023.blob` | `17a0cbca1ba6287efd13df9746021a5881ab06b324ef44d1bbd245a20d4fbb13` | 2188 |
| `payload/0024.blob` | `7f1803d3efec7e62709df0ff4b082cfd3dba4e57609f51559437e7a189b4d57c` | 98 |
| `payload/0025.blob` | `93f0bf4f5d36ec9d7cc7064e9eca394dab9d1a2d00f011701e59cb63ce3f85fa` | 2063 |
| `payload/0026.blob` | `51332cea6913d812c940574432a891f05c4b2667719f465b4a613dbea0a62cf6` | 13251 |
| `payload/0027.blob` | `0c91acfe02943770c25950670bbcfc5b6fe732a747707185f7d40bf00968c983` | 17634 |
| `payload/0028.blob` | `fb30c940ea36b62b9e673d124834702c3be4ce260730f46aa0883077b1a7c943` | 3632 |
| `payload/0029.blob` | `ec47b135cfd7614f5535ac600d7ec2e94d8cab6c6299e21296d7da0c8a9603f1` | 1409 |
| `payload/0030.blob` | `13e5148f91957a109a2560622c09c87de5369c6e1e3591cb223de252440914cc` | 8530 |
| `payload/0031.blob` | `7a5b94ff6732e0a49fd712ea447608d7407e85dfa5eeb5d290f12fbeb736fd54` | 6877 |
| `payload/0032.blob` | `55c5e8e285c5fda8ab7f29c211e987ddf5a9a6b12cd5bb9fb5468a28f7319fee` | 1488 |
| `payload/0033.blob` | `1b2bb3bcecc54a94e8b6565f12c4bc83c7ab9278b1636c22566271706e001bc4` | 895 |
| `payload/0034.blob` | `f60c7f1d878908887a451d329eedb12d03d755778ded924cf22f0071783d4988` | 3611 |
| `payload/0035.blob` | `56a03ab860f6c7a85ddd3be60f90ade70229b781b8db976c978b5af7073da214` | 1952 |
| `payload/0036.blob` | `72e40237948012bd3259e59d0d87f06f86bedaebf454e52fe3d58f0d3d3118fe` | 16576 |
| `payload/0037.blob` | `0768d05a32bfbe9e93a86f776cca39b494b367ee0dff04dadb974904d195faad` | 1845 |
| `payload/0038.blob` | `4d82b7feeacf055f180f9a6c483bfa920faccbd0788fc15482732c0cf3f8de4e` | 8515 |
| `payload/0039.blob` | `655bd4a005d1210eef8f5ae62a462d4cf8a2591bfe318c2f428bcfb3ae5c3269` | 45898 |
| `payload/0040.blob` | `9de8908a371839789586bee10f2d3a01d4a53b43cea5db2efeaa5c625a87afbe` | 26254 |
| `receipt.json` | `8526f3e38c3118ae9dea0d371f051cc85f1370133b2c464e6fbf8c870b96422d` | 303 |
| `reservation.json` | `7485a6ac770fb464ff199c1fcbcba2887d0cf61f304a70a0717ab79a8713a2f5` | 3454 |
| `return.md` | `9da830f28f340fb6142a12908e8d60a3b5050cc8ff075d32405133f39853d472` | 18493 |

## Commands

The capture ran from `D:\Git\lib-build` with today's pinned helper. No recovered script was invoked.

```text
C:\Users\misg\AppData\Local\Programs\Python\Python314\python.exe
-B
labs/return-capture-pass01/return_capture.py
capture
--book
D:/Git/lib-build/00.kernel/00.00.10.work
--submission
historical-0508-0501
--return-file
C:/Users/misg/AppData/Local/Temp/rc0511-stage/return.md
--source-root
C:/Users/misg/AppData/Local/Temp/rc0511-stage
--retrospective
--source-commit
75ae515d826482113c4126274d015de112aa249b
--return-includes-prime-review
--artifact
labs/return-capture-pass01/demo.py|labs/return-capture-pass01/demo.py
--artifact
labs/return-capture-pass01/inventory.py|labs/return-capture-pass01/inventory.py
--artifact
00.kernel/00.00.10.work/0508.return-capture/06.02.md|00.kernel/00.00.10.work/0508.return-capture/06.02.md
--artifact
00.kernel/00.00.10.work/0508.return-capture/evidence/build05.01/after/00.kernel__00.00.10.work__0014.design__01.001.md|00.kernel/00.00.10.work/0508.return-capture/evidence/build05.01/after/00.kernel__00.00.10.work__0014.design__01.001.md
--artifact
00.kernel/00.00.10.work/0508.return-capture/evidence/build05.01/after/00.kernel__00.00.10.work__0100.band.returns__01.md|00.kernel/00.00.10.work/0508.return-capture/evidence/build05.01/after/00.kernel__00.00.10.work__0100.band.returns__01.md
--artifact
00.kernel/00.00.10.work/0508.return-capture/evidence/build05.01/after/00.kernel__00.00.10.work__0500.band.packs__01.md|00.kernel/00.00.10.work/0508.return-capture/evidence/build05.01/after/00.kernel__00.00.10.work__0500.band.packs__01.md
--artifact
00.kernel/00.00.10.work/0508.return-capture/evidence/build05.01/backfill.json|00.kernel/00.00.10.work/0508.return-capture/evidence/build05.01/backfill.json
--artifact
00.kernel/00.00.10.work/0508.return-capture/evidence/build05.01/before/00.kernel__00.00.10.work__0014.design__01.001.md|00.kernel/00.00.10.work/0508.return-capture/evidence/build05.01/before/00.kernel__00.00.10.work__0014.design__01.001.md
--artifact
00.kernel/00.00.10.work/0508.return-capture/evidence/build05.01/before/00.kernel__00.00.10.work__0100.band.returns__01.md|00.kernel/00.00.10.work/0508.return-capture/evidence/build05.01/before/00.kernel__00.00.10.work__0100.band.returns__01.md
--artifact
00.kernel/00.00.10.work/0508.return-capture/evidence/build05.01/before/00.kernel__00.00.10.work__0500.band.packs__01.md|00.kernel/00.00.10.work/0508.return-capture/evidence/build05.01/before/00.kernel__00.00.10.work__0500.band.packs__01.md
--artifact
00.kernel/00.00.10.work/0508.return-capture/evidence/build05.01/custody.json|00.kernel/00.00.10.work/0508.return-capture/evidence/build05.01/custody.json
--artifact
00.kernel/00.00.10.work/0508.return-capture/evidence/build05.01/demo.txt|00.kernel/00.00.10.work/0508.return-capture/evidence/build05.01/demo.txt
--artifact
00.kernel/00.00.10.work/0508.return-capture/evidence/build05.01/discovery.patch|00.kernel/00.00.10.work/0508.return-capture/evidence/build05.01/discovery.patch
--artifact
00.kernel/00.00.10.work/0508.return-capture/evidence/build05.01/inventory.json|00.kernel/00.00.10.work/0508.return-capture/evidence/build05.01/inventory.json
--artifact
00.kernel/00.00.10.work/0508.return-capture/evidence/build05.01/limits.md|00.kernel/00.00.10.work/0508.return-capture/evidence/build05.01/limits.md
--artifact
00.kernel/00.00.10.work/0508.return-capture/evidence/build05.01/publication.json|00.kernel/00.00.10.work/0508.return-capture/evidence/build05.01/publication.json
--artifact
00.kernel/00.00.10.work/0508.return-capture/evidence/build05.01/retrospective.json|00.kernel/00.00.10.work/0508.return-capture/evidence/build05.01/retrospective.json
--artifact
00.kernel/00.00.10.work/0508.return-capture/evidence/build05.01/tests.pass01.txt|00.kernel/00.00.10.work/0508.return-capture/evidence/build05.01/tests.pass01.txt
--artifact
00.kernel/00.00.10.work/0508.return-capture/evidence/pack05.01/source-manifest.json|00.kernel/00.00.10.work/0508.return-capture/evidence/pack05.01/source-manifest.json
--artifact
00.kernel/00.00.10.work/0508.return-capture/evidence/pack05.01/snapshots/0001.blob|00.kernel/00.00.10.work/0100.band.returns/01.md
--artifact
00.kernel/00.00.10.work/0508.return-capture/evidence/pack05.01/snapshots/0002.blob|00.kernel/00.00.10.work/0500.band.packs/01.md
--artifact
00.kernel/00.00.10.work/0508.return-capture/evidence/pack05.01/snapshots/0003.blob|00.kernel/00.00.10.work/0014.design/01.001.md
--artifact
00.kernel/00.00.10.work/0508.return-capture/evidence/pack05.01/snapshots/0004.blob|00.kernel/00.00.10.work/0014.design/01.002.md
--artifact
00.kernel/00.00.10.work/0508.return-capture/evidence/pack05.01/snapshots/0005.blob|00.kernel/00.00.10.work/00.md
--artifact
00.kernel/00.00.10.work/0508.return-capture/evidence/pack05.01/snapshots/0006.blob|00.kernel/00.00.10.work/0502.workflow-start/01.md
--artifact
00.kernel/00.00.10.work/0508.return-capture/evidence/pack05.01/snapshots/0007.blob|00.kernel/00.00.10.work/0504.app-entry/05.06.md
--artifact
00.kernel/00.00.10.work/0508.return-capture/evidence/pack05.01/snapshots/0008.blob|00.kernel/00.00.10.work/0507.prime-support/05.01.md
--artifact
00.kernel/00.00.10.work/0508.return-capture/evidence/pack05.01/snapshots/0009.blob|00.kernel/00.00.10.work/0507.prime-support/evidence/prime-review05.01/review.md
--artifact
00.kernel/00.00.10.work/0508.return-capture/evidence/pack05.01/snapshots/0010.blob|00.kernel/00.00.10.work/0506.clerk-handoff/01.md
--artifact
00.kernel/00.00.10.work/0508.return-capture/evidence/pack05.01/snapshots/0011.blob|labs/clerk-handoff-pass02/README.md
--artifact
00.kernel/00.00.10.work/0508.return-capture/evidence/pack05.01/snapshots/0012.blob|README.md
--artifact
00.kernel/00.00.10.work/0508.return-capture/evidence/prime-review05.01/builder-door-before-prime-status.md|00.kernel/00.00.10.work/0508.return-capture/evidence/prime-review05.01/builder-door-before-prime-status.md
--artifact
00.kernel/00.00.10.work/0508.return-capture/evidence/prime-review05.01/custody.json|00.kernel/00.00.10.work/0508.return-capture/evidence/prime-review05.01/custody.json
--artifact
00.kernel/00.00.10.work/0508.return-capture/evidence/prime-review05.01/return-capture-pass01.txt|00.kernel/00.00.10.work/0508.return-capture/evidence/prime-review05.01/return-capture-pass01.txt
--artifact
00.kernel/00.00.10.work/0508.return-capture/evidence/prime-review05.01/review.md|00.kernel/00.00.10.work/0508.return-capture/evidence/prime-review05.01/review.md
--artifact
00.kernel/00.00.10.work/0508.return-capture/evidence/prime-review05.01/reviewed-05.01.md|00.kernel/00.00.10.work/0508.return-capture/evidence/prime-review05.01/reviewed-05.01.md
--artifact
00.kernel/00.00.10.work/0508.return-capture/evidence/prime-review05.01/verification.json|00.kernel/00.00.10.work/0508.return-capture/evidence/prime-review05.01/verification.json
--artifact
00.kernel/00.00.10.work/0508.return-capture/evidence/pack05.02/snapshots/0008.blob|labs/return-capture-pass01/README.md
--artifact
00.kernel/00.00.10.work/0508.return-capture/evidence/pack05.02/snapshots/0009.blob|labs/return-capture-pass01/return_capture.py
--artifact
00.kernel/00.00.10.work/0508.return-capture/evidence/pack05.02/snapshots/0010.blob|labs/return-capture-pass01/tests/test_return_capture.py
```

```text
python -B labs/return-capture-pass01/return_capture.py verify --book "D:/Git/lib-build/00.kernel/00.00.10.work" --member 0132.return-capture-origin-0501
python -B labs/return-capture-pass01/return_inspect.py inspect --book "D:/Git/lib-build/00.kernel/00.00.10.work" --member 0132.return-capture-origin-0501 --json
```

## Original to staged

Git export and the staged file share each hash below. A source cell of `same` means the Git path equals the logical name. `source-map.json` records every source path and the 0132 receipt hash.

| # | Logical name | Git source | SHA-256 | Bytes |
| --- | --- | --- | --- | --- |
| return | `00.kernel/00.00.10.work/0508.return-capture/05.01.md` | same | `9da830f28f340fb6142a12908e8d60a3b5050cc8ff075d32405133f39853d472` | 18493 |
| 01 | `labs/return-capture-pass01/demo.py` | same | `b205d0ddf5136416ab5767f04c505bfff89ae82efd419409e726e586073d865b` | 13969 |
| 02 | `labs/return-capture-pass01/inventory.py` | same | `765765cbdab87ec17304cd891c1f46ddfe7249d9128f0f203a1fd9dc0609aa64` | 4462 |
| 03 | `00.kernel/00.00.10.work/0508.return-capture/06.02.md` | same | `fc3ba08e9fa676dec9d76c9c663693a799146483b924bef3320a479eaf3d689d` | 10669 |
| 04 | `00.kernel/00.00.10.work/0508.return-capture/evidence/build05.01/after/00.kernel__00.00.10.work__0014.design__01.001.md` | same | `20ba376e05a5ab09fed5d6e9644e3e74a6db954d7e476ff94f76b6469c780d0a` | 1448 |
| 05 | `00.kernel/00.00.10.work/0508.return-capture/evidence/build05.01/after/00.kernel__00.00.10.work__0100.band.returns__01.md` | same | `55c5e8e285c5fda8ab7f29c211e987ddf5a9a6b12cd5bb9fb5468a28f7319fee` | 1488 |
| 06 | `00.kernel/00.00.10.work/0508.return-capture/evidence/build05.01/after/00.kernel__00.00.10.work__0500.band.packs__01.md` | same | `c0b8516b834d89a28bfed23a4779629be7b00556f21ff029d174ff9040e7b053` | 2561 |
| 07 | `00.kernel/00.00.10.work/0508.return-capture/evidence/build05.01/backfill.json` | same | `39cc192816469aa359db0853fedbb2370303af9789caa2bbc0bd061fc4bf7f68` | 2740 |
| 08 | `00.kernel/00.00.10.work/0508.return-capture/evidence/build05.01/before/00.kernel__00.00.10.work__0014.design__01.001.md` | same | `a04962e94ae54bcb0fc2ae42dd36ff6fc33822427cb2a983211d069aeaf4b610` | 1075 |
| 09 | `00.kernel/00.00.10.work/0508.return-capture/evidence/build05.01/before/00.kernel__00.00.10.work__0100.band.returns__01.md` | same | `f66b010a74fe879431cc17093b236dd1dd113658e22c041252fe2719c0c1a3be` | 669 |
| 10 | `00.kernel/00.00.10.work/0508.return-capture/evidence/build05.01/before/00.kernel__00.00.10.work__0500.band.packs__01.md` | same | `f358b4315ee604aa20203671bcf8b97d149c9034bb694f77d31fa8e2440dc635` | 1104 |
| 11 | `00.kernel/00.00.10.work/0508.return-capture/evidence/build05.01/custody.json` | same | `c3cc6baafc8321f01a177cdfc93540e593ed6f04dfc3fededc16002cacade1f3` | 7893 |
| 12 | `00.kernel/00.00.10.work/0508.return-capture/evidence/build05.01/demo.txt` | same | `079dc6de98157887289a9438e19e087cfc950d4dcb0e8864bdf2da988b5f382c` | 1243 |
| 13 | `00.kernel/00.00.10.work/0508.return-capture/evidence/build05.01/discovery.patch` | same | `3d4403419817c7d562e7c6173edbe55b8ec347118281940f87a1725d148165fe` | 3585 |
| 14 | `00.kernel/00.00.10.work/0508.return-capture/evidence/build05.01/inventory.json` | same | `d697f57a3998d1af58987a42fa1a17273c6276336c2dd2c76aa0de0feb6a9af1` | 11970 |
| 15 | `00.kernel/00.00.10.work/0508.return-capture/evidence/build05.01/limits.md` | same | `f9cef3eff1d04f4c47e67734034f13cc1fbd9bb70d76a90b983a3c118b10fa5d` | 1947 |
| 16 | `00.kernel/00.00.10.work/0508.return-capture/evidence/build05.01/publication.json` | same | `61d203eb9450c60d912ef621d3848532e76e4887da7bc202453aa1b8ab344979` | 1902 |
| 17 | `00.kernel/00.00.10.work/0508.return-capture/evidence/build05.01/retrospective.json` | same | `47814afde6ed62be1963c7816fc6ab1df4572d0916ae9e25601c3b127bfb3e91` | 2628 |
| 18 | `00.kernel/00.00.10.work/0508.return-capture/evidence/build05.01/tests.pass01.txt` | same | `11fcfbeb1ce238494ea5c47b7bdbf6932ae6a5b98981e76a7784df47241f4437` | 3624 |
| 19 | `00.kernel/00.00.10.work/0508.return-capture/evidence/pack05.01/source-manifest.json` | same | `7f32a599bdbbe12f370afa3e4b88bcd83df6136fd9520b02637ed6856c5a2db8` | 2794 |
| 20 | `00.kernel/00.00.10.work/0100.band.returns/01.md` | `00.kernel/00.00.10.work/0508.return-capture/evidence/pack05.01/snapshots/0001.blob` | `f66b010a74fe879431cc17093b236dd1dd113658e22c041252fe2719c0c1a3be` | 669 |
| 21 | `00.kernel/00.00.10.work/0500.band.packs/01.md` | `00.kernel/00.00.10.work/0508.return-capture/evidence/pack05.01/snapshots/0002.blob` | `f358b4315ee604aa20203671bcf8b97d149c9034bb694f77d31fa8e2440dc635` | 1104 |
| 22 | `00.kernel/00.00.10.work/0014.design/01.001.md` | `00.kernel/00.00.10.work/0508.return-capture/evidence/pack05.01/snapshots/0003.blob` | `a04962e94ae54bcb0fc2ae42dd36ff6fc33822427cb2a983211d069aeaf4b610` | 1075 |
| 23 | `00.kernel/00.00.10.work/0014.design/01.002.md` | `00.kernel/00.00.10.work/0508.return-capture/evidence/pack05.01/snapshots/0004.blob` | `17a0cbca1ba6287efd13df9746021a5881ab06b324ef44d1bbd245a20d4fbb13` | 2188 |
| 24 | `00.kernel/00.00.10.work/00.md` | `00.kernel/00.00.10.work/0508.return-capture/evidence/pack05.01/snapshots/0005.blob` | `7f1803d3efec7e62709df0ff4b082cfd3dba4e57609f51559437e7a189b4d57c` | 98 |
| 25 | `00.kernel/00.00.10.work/0502.workflow-start/01.md` | `00.kernel/00.00.10.work/0508.return-capture/evidence/pack05.01/snapshots/0006.blob` | `93f0bf4f5d36ec9d7cc7064e9eca394dab9d1a2d00f011701e59cb63ce3f85fa` | 2063 |
| 26 | `00.kernel/00.00.10.work/0504.app-entry/05.06.md` | `00.kernel/00.00.10.work/0508.return-capture/evidence/pack05.01/snapshots/0007.blob` | `51332cea6913d812c940574432a891f05c4b2667719f465b4a613dbea0a62cf6` | 13251 |
| 27 | `00.kernel/00.00.10.work/0507.prime-support/05.01.md` | `00.kernel/00.00.10.work/0508.return-capture/evidence/pack05.01/snapshots/0008.blob` | `0c91acfe02943770c25950670bbcfc5b6fe732a747707185f7d40bf00968c983` | 17634 |
| 28 | `00.kernel/00.00.10.work/0507.prime-support/evidence/prime-review05.01/review.md` | `00.kernel/00.00.10.work/0508.return-capture/evidence/pack05.01/snapshots/0009.blob` | `fb30c940ea36b62b9e673d124834702c3be4ce260730f46aa0883077b1a7c943` | 3632 |
| 29 | `00.kernel/00.00.10.work/0506.clerk-handoff/01.md` | `00.kernel/00.00.10.work/0508.return-capture/evidence/pack05.01/snapshots/0010.blob` | `ec47b135cfd7614f5535ac600d7ec2e94d8cab6c6299e21296d7da0c8a9603f1` | 1409 |
| 30 | `labs/clerk-handoff-pass02/README.md` | `00.kernel/00.00.10.work/0508.return-capture/evidence/pack05.01/snapshots/0011.blob` | `13e5148f91957a109a2560622c09c87de5369c6e1e3591cb223de252440914cc` | 8530 |
| 31 | `README.md` | `00.kernel/00.00.10.work/0508.return-capture/evidence/pack05.01/snapshots/0012.blob` | `7a5b94ff6732e0a49fd712ea447608d7407e85dfa5eeb5d290f12fbeb736fd54` | 6877 |
| 32 | `00.kernel/00.00.10.work/0508.return-capture/evidence/prime-review05.01/builder-door-before-prime-status.md` | same | `55c5e8e285c5fda8ab7f29c211e987ddf5a9a6b12cd5bb9fb5468a28f7319fee` | 1488 |
| 33 | `00.kernel/00.00.10.work/0508.return-capture/evidence/prime-review05.01/custody.json` | same | `1b2bb3bcecc54a94e8b6565f12c4bc83c7ab9278b1636c22566271706e001bc4` | 895 |
| 34 | `00.kernel/00.00.10.work/0508.return-capture/evidence/prime-review05.01/return-capture-pass01.txt` | same | `f60c7f1d878908887a451d329eedb12d03d755778ded924cf22f0071783d4988` | 3611 |
| 35 | `00.kernel/00.00.10.work/0508.return-capture/evidence/prime-review05.01/review.md` | same | `56a03ab860f6c7a85ddd3be60f90ade70229b781b8db976c978b5af7073da214` | 1952 |
| 36 | `00.kernel/00.00.10.work/0508.return-capture/evidence/prime-review05.01/reviewed-05.01.md` | same | `72e40237948012bd3259e59d0d87f06f86bedaebf454e52fe3d58f0d3d3118fe` | 16576 |
| 37 | `00.kernel/00.00.10.work/0508.return-capture/evidence/prime-review05.01/verification.json` | same | `0768d05a32bfbe9e93a86f776cca39b494b367ee0dff04dadb974904d195faad` | 1845 |
| 38 | `labs/return-capture-pass01/README.md` | `00.kernel/00.00.10.work/0508.return-capture/evidence/pack05.02/snapshots/0008.blob` | `4d82b7feeacf055f180f9a6c483bfa920faccbd0788fc15482732c0cf3f8de4e` | 8515 |
| 39 | `labs/return-capture-pass01/return_capture.py` | `00.kernel/00.00.10.work/0508.return-capture/evidence/pack05.02/snapshots/0009.blob` | `655bd4a005d1210eef8f5ae62a462d4cf8a2591bfe318c2f428bcfb3ae5c3269` | 45898 |
| 40 | `labs/return-capture-pass01/tests/test_return_capture.py` | `00.kernel/00.00.10.work/0508.return-capture/evidence/pack05.02/snapshots/0010.blob` | `9de8908a371839789586bee10f2d3a01d4a53b43cea5db2efeaa5c625a87afbe` | 26254 |

Relationship counts from the supplied map: delivered artifact 6, recovered original delivered artifact 3, review/test evidence 15, source input 16.

## Failures

None. Blob export, hash checks, capture, verify, and inspect each finished on the first attempt. No partial member was left. No substitute member was allocated.

## Current report

`0133.original-capture-0511` is the separate current capture, submission `grok-2-0508-0511`. It is not retrospective, it has no source commit, and it does not carry the embedded-review flag. Its outputs are `06.12.md`, `source-map.json`, this report, and `verification.json`. The dedicated submission is the return file. When this report was written, `0133` held only `01.md` and `reservation.json`. This report does not contain the later `0133` receipt.
