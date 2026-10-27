# Capture report — assembler custody, 05.10
Date: 2026-10-27
Recorder: Grok 4.7, Grok Builder 2
Session: 01a17dfa-bc23-7730-bec3-c49938f96187

This report records custody of one historical assembler page and its declared companions. A receipt is not approval, acceptance, seating, publication, or finish.

## Custody

The capture stores the whole `0509.pack-assembly/05.01` page from commit `75ae515d826482113c4126274d015de112aa249b`, including its Director reply and embedded Review section, plus the 47 companions named by the qualified `resolved-slices.json` row and by `0128.pack-assembly-0501/reservation.json`. Staged bytes match those declared SHA-256 values and lengths. Thirty-nine companions use one path as both Git source and logical name. Eight companions are retained pack snapshots: the Git source path is the snapshot, and the logical name is the path the reservation declares. The checker and the jobs formatter are those snapshot dependencies. They were stored and not executed. This is historical checkpoint custody plus declared-hash-supported artifact recovery. It is not a new assembler implementation, not a product-suite rerun, and not a fresh approval. The historical RC-01 hold remains. The recovered original helper was not captured.

## Historical identities

Submission `historical-0509-0501`. Retrospective true. Source commit `75ae515d826482113c4126274d015de112aa249b`. `includes_prime_review` true. Return SHA-256 `9545b7457a0e37fbcd3efeec2a379fcef6e4a02e2c41558a18673a7b14ae89a7`, 10398 bytes. The return blob contains a `## Review` heading.

Before capture the member held two files:

| Path | SHA-256 | Bytes |
| --- | --- | --- |
| `01.md` | `7a4de4c4fa7cfd1ddb0cabf6ac7a3178b28e69fbb4c9419089a12494970f0ce1` | 332 |
| `reservation.json` | `773436661f4a045b5f690575c72d42fc6c7d3129abe3eed2589f9e5feae53028` | 4002 |

Capture exited 0. Manifest `ae1f999645208785517ffd12f99a55ebcbcbee720a95e7998120b92df4fc6e98`, 13232 bytes. Receipt `8aefe871d65c9fc6d98388f2eca6492bc03e4f44795f89fc4fe84994e5ba5727`, 303 bytes. Fresh verify exited 0: result complete, not approved, not accepted, not published. Inspect exited 0: schema `return-capture-inspection/1`, status `complete`, problems empty, retrospective true, source commit set, embedded review true, 47 payloads. The member file inventory after verify matched the inventory after capture, and the inventory after inspect matched the inventory after verify.

Post-capture member files:

| Path | SHA-256 | Bytes |
| --- | --- | --- |
| `01.md` | `7a4de4c4fa7cfd1ddb0cabf6ac7a3178b28e69fbb4c9419089a12494970f0ce1` | 332 |
| `manifest.json` | `ae1f999645208785517ffd12f99a55ebcbcbee720a95e7998120b92df4fc6e98` | 13232 |
| `payload/0001.blob` | `75d49679cbf3e624a82573229ca8c7cd9b758799bc26b6f080111feb6eaa275c` | 43928 |
| `payload/0002.blob` | `bfc2178908889fb238d8c7218683ef8367c57fe65cc94df54fe1f21f825ecd68` | 4849 |
| `payload/0003.blob` | `e39a9481ac66ddef1fd76d6bd17083d3d5f236756384843c3552c3307e1a0296` | 31745 |
| `payload/0004.blob` | `d09497bcdb699bac1477cc96d100d64cdce41216b8e0874577e3745194897fe7` | 9815 |
| `payload/0005.blob` | `58e67e2d12045ce1f2daf0483eb2041e2e0c4f6f72fd80781fce007e5e692574` | 253 |
| `payload/0006.blob` | `b80826e0b65a2567db13faeaf8078ebbe3da4ff49f66bc3ca2119950ff7da394` | 1866 |
| `payload/0007.blob` | `9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa` | 2 |
| `payload/0008.blob` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 0 |
| `payload/0009.blob` | `ff9e9e5a34c2eb615e4a6273da266a204e42c644cba69b8a02660595765f0b34` | 2857 |
| `payload/0010.blob` | `66730333bfb4d6335ddca3ab9002ad0954ac114d2cffc1e6ff7fb86cf4a4b6a5` | 2036 |
| `payload/0011.blob` | `40ba90694101645a5e9b65500a36f54a8ad14b4716ccd5da9cf5c4d9d4e95d49` | 1539 |
| `payload/0012.blob` | `589bd1b842927b31e93c4238b5fa95bc221d03af13c8a9b058a52176eddcbace` | 1058 |
| `payload/0013.blob` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 0 |
| `payload/0014.blob` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 0 |
| `payload/0015.blob` | `4355a46b19d348dc2f57c046f8ef63d4538ebb936000f3c9ee954a27460dd865` | 2 |
| `payload/0016.blob` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 0 |
| `payload/0017.blob` | `ddbb239eae4d22e59cd0854ac2624d731dd6ba89a0059f5d220285d36d2b83b2` | 1847 |
| `payload/0018.blob` | `52e63c41107662c76c6a58104c008dd26cc07dc397726cd7b72e923cd2fe2688` | 832 |
| `payload/0019.blob` | `52e63c41107662c76c6a58104c008dd26cc07dc397726cd7b72e923cd2fe2688` | 832 |
| `payload/0020.blob` | `9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa` | 2 |
| `payload/0021.blob` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 0 |
| `payload/0022.blob` | `7f70c35cfd9cf3c6a3a135e27539a770120d136784e0c68fa300dda30d3b470a` | 2045 |
| `payload/0023.blob` | `9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa` | 2 |
| `payload/0024.blob` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 0 |
| `payload/0025.blob` | `853e811f108c6cc77fc0784e4cc78cb90436522145f3a81feb63ba782eaf4f26` | 2546 |
| `payload/0026.blob` | `b4a17dc7668b37a079c2de1dd02fba6d6450af278e3adb3bcd4c0fad620a0665` | 481 |
| `payload/0027.blob` | `0fb09e71f655ca484f5d35953a319c465e18a59c29030de3648dc792820c4279` | 1885 |
| `payload/0028.blob` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 0 |
| `payload/0029.blob` | `b80826e0b65a2567db13faeaf8078ebbe3da4ff49f66bc3ca2119950ff7da394` | 1866 |
| `payload/0030.blob` | `9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa` | 2 |
| `payload/0031.blob` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 0 |
| `payload/0032.blob` | `b8c0583b745de93f9acafcb62b4c3d69c3325794d3348c9515f3d0537961bdba` | 1504 |
| `payload/0033.blob` | `a2156b25bbd13261a66be928dc82a365c22d98f4adaf84f1a3cbcefd90991b38` | 2220 |
| `payload/0034.blob` | `4db26ef3c1d9c0a2ee03eef2469fc84f146d02b1e4e4ff6ce66c682285f40d75` | 1862 |
| `payload/0035.blob` | `246153bcaa86b2b3e056ae84263899a99dc39e011b54e4ed3f588334330fe8e7` | 9634 |
| `payload/0036.blob` | `013ffb0c11a3ef8daae309b3176560b6bca31d5ce24646733508338569ef144e` | 1311 |
| `payload/0037.blob` | `9bbd9d57f3b7da43234ac2e6ae4ce40a0ab6af2f53c8135ecfb2ee0c8a6e322d` | 21563 |
| `payload/0038.blob` | `657ef6032cb4fdead6a8f93450792c97a3e46b837d3a191aa3f19983ff4969af` | 5074 |
| `payload/0039.blob` | `07a50f4b719f8de71119c1459e40f1bfe6c6ce992aff64d3818a2d994656f69b` | 26105 |
| `payload/0040.blob` | `7b39308592b63f080820de907eed996e6e9ac30c5b90e9502c628578fc1c3547` | 97270 |
| `payload/0041.blob` | `fca5b450312f0201fa9a2e60d686cb3e982524266030a54353d65dfb6655001e` | 9747 |
| `payload/0042.blob` | `19cf1e4e5c9317d85e7dc4283ed7abe793c32cf8dceeac90a777c89b05339fea` | 4151 |
| `payload/0043.blob` | `14ab3a9577958d70147749ad029319aaff18882843a939a993aacc75fd8cd3e7` | 722 |
| `payload/0044.blob` | `d4dfe4825778562ec483b89ec7ee3c101a877b24b67b587a044ff03b901e9070` | 126 |
| `payload/0045.blob` | `70bd68aaa86f5f9da2ef95530601c61e2288a5c50259231fc5ec1732731b6ef9` | 1239 |
| `payload/0046.blob` | `e0945f4a5cc356ccc571dcc877167c0e4cadc19b34ca547b33135f5375e6f1fc` | 9194 |
| `payload/0047.blob` | `0768d05a32bfbe9e93a86f776cca39b494b367ee0dff04dadb974904d195faad` | 1845 |
| `receipt.json` | `8aefe871d65c9fc6d98388f2eca6492bc03e4f44795f89fc4fe84994e5ba5727` | 303 |
| `reservation.json` | `773436661f4a045b5f690575c72d42fc6c7d3129abe3eed2589f9e5feae53028` | 4002 |
| `return.md` | `9545b7457a0e37fbcd3efeec2a379fcef6e4a02e2c41558a18673a7b14ae89a7` | 10398 |

## Original to staged

Git export and the staged file share each hash below. A source cell of `same` means the Git path equals the logical name. The eight other rows keep the snapshot path. `source-map.json` records every source path.

| # | Logical name | Git source | SHA-256 | Bytes |
| --- | --- | --- | --- | --- |
| return | `00.kernel/00.00.10.work/0509.pack-assembly/05.01.md` | same | `9545b7457a0e37fbcd3efeec2a379fcef6e4a02e2c41558a18673a7b14ae89a7` | 10398 |
| 01 | `labs/pack-assembly-pass01/pack_assembly.py` | same | `75d49679cbf3e624a82573229ca8c7cd9b758799bc26b6f080111feb6eaa275c` | 43928 |
| 02 | `labs/pack-assembly-pass01/README.md` | same | `bfc2178908889fb238d8c7218683ef8367c57fe65cc94df54fe1f21f825ecd68` | 4849 |
| 03 | `labs/pack-assembly-pass01/tests/test_pack_assembly.py` | same | `e39a9481ac66ddef1fd76d6bd17083d3d5f236756384843c3552c3307e1a0296` | 31745 |
| 04 | `00.kernel/00.00.10.work/0509.pack-assembly/06.02.md` | same | `d09497bcdb699bac1477cc96d100d64cdce41216b8e0874577e3745194897fe7` | 9815 |
| 05 | `labs/pack-assembly-pass01/evidence/SHA256SUMS.txt` | same | `58e67e2d12045ce1f2daf0483eb2041e2e0c4f6f72fd80781fce007e5e692574` | 253 |
| 06 | `labs/pack-assembly-pass01/evidence/tests.txt` | same | `b80826e0b65a2567db13faeaf8078ebbe3da4ff49f66bc3ca2119950ff7da394` | 1866 |
| 07 | `00.kernel/00.00.10.work/0509.pack-assembly/evidence/build05.01/assemble.exit.txt` | same | `9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa` | 2 |
| 08 | `00.kernel/00.00.10.work/0509.pack-assembly/evidence/build05.01/assemble.stderr.txt` | same | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 0 |
| 09 | `00.kernel/00.00.10.work/0509.pack-assembly/evidence/build05.01/assemble.stdout.txt` | same | `ff9e9e5a34c2eb615e4a6273da266a204e42c644cba69b8a02660595765f0b34` | 2857 |
| 10 | `00.kernel/00.00.10.work/0509.pack-assembly/evidence/build05.01/commands.txt` | same | `66730333bfb4d6335ddca3ab9002ad0954ac114d2cffc1e6ff7fb86cf4a4b6a5` | 2036 |
| 11 | `00.kernel/00.00.10.work/0509.pack-assembly/evidence/build05.01/completion-receipt.json` | same | `40ba90694101645a5e9b65500a36f54a8ad14b4716ccd5da9cf5c4d9d4e95d49` | 1539 |
| 12 | `00.kernel/00.00.10.work/0509.pack-assembly/evidence/build05.01/draft-05.14.md` | same | `589bd1b842927b31e93c4238b5fa95bc221d03af13c8a9b058a52176eddcbace` | 1058 |
| 13 | `00.kernel/00.00.10.work/0509.pack-assembly/evidence/build05.01/git-add.stderr.txt` | same | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 0 |
| 14 | `00.kernel/00.00.10.work/0509.pack-assembly/evidence/build05.01/git-commit.stderr.txt` | same | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 0 |
| 15 | `00.kernel/00.00.10.work/0509.pack-assembly/evidence/build05.01/mutated-verify.exit.txt` | same | `4355a46b19d348dc2f57c046f8ef63d4538ebb936000f3c9ee954a27460dd865` | 2 |
| 16 | `00.kernel/00.00.10.work/0509.pack-assembly/evidence/build05.01/mutated-verify.stderr.txt` | same | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 0 |
| 17 | `00.kernel/00.00.10.work/0509.pack-assembly/evidence/build05.01/mutated-verify.stdout.txt` | same | `ddbb239eae4d22e59cd0854ac2624d731dd6ba89a0059f5d220285d36d2b83b2` | 1847 |
| 18 | `00.kernel/00.00.10.work/0509.pack-assembly/evidence/build05.01/originals-after.txt` | same | `52e63c41107662c76c6a58104c008dd26cc07dc397726cd7b72e923cd2fe2688` | 832 |
| 19 | `00.kernel/00.00.10.work/0509.pack-assembly/evidence/build05.01/originals-before.txt` | same | `52e63c41107662c76c6a58104c008dd26cc07dc397726cd7b72e923cd2fe2688` | 832 |
| 20 | `00.kernel/00.00.10.work/0509.pack-assembly/evidence/build05.01/pack-check.exit.txt` | same | `9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa` | 2 |
| 21 | `00.kernel/00.00.10.work/0509.pack-assembly/evidence/build05.01/pack-check.stderr.txt` | same | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 0 |
| 22 | `00.kernel/00.00.10.work/0509.pack-assembly/evidence/build05.01/pack-check.stdout.txt` | same | `7f70c35cfd9cf3c6a3a135e27539a770120d136784e0c68fa300dda30d3b470a` | 2045 |
| 23 | `00.kernel/00.00.10.work/0509.pack-assembly/evidence/build05.01/preview.exit.txt` | same | `9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa` | 2 |
| 24 | `00.kernel/00.00.10.work/0509.pack-assembly/evidence/build05.01/preview.stderr.txt` | same | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 0 |
| 25 | `00.kernel/00.00.10.work/0509.pack-assembly/evidence/build05.01/preview.stdout.txt` | same | `853e811f108c6cc77fc0784e4cc78cb90436522145f3a81feb63ba782eaf4f26` | 2546 |
| 26 | `00.kernel/00.00.10.work/0509.pack-assembly/evidence/build05.01/source-manifest.json` | same | `b4a17dc7668b37a079c2de1dd02fba6d6450af278e3adb3bcd4c0fad620a0665` | 481 |
| 27 | `00.kernel/00.00.10.work/0509.pack-assembly/evidence/build05.01/tests.stderr.txt` | same | `0fb09e71f655ca484f5d35953a319c465e18a59c29030de3648dc792820c4279` | 1885 |
| 28 | `00.kernel/00.00.10.work/0509.pack-assembly/evidence/build05.01/tests.stdout.txt` | same | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 0 |
| 29 | `00.kernel/00.00.10.work/0509.pack-assembly/evidence/build05.01/tests.txt` | same | `b80826e0b65a2567db13faeaf8078ebbe3da4ff49f66bc3ca2119950ff7da394` | 1866 |
| 30 | `00.kernel/00.00.10.work/0509.pack-assembly/evidence/build05.01/verify.exit.txt` | same | `9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa` | 2 |
| 31 | `00.kernel/00.00.10.work/0509.pack-assembly/evidence/build05.01/verify.stderr.txt` | same | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 0 |
| 32 | `00.kernel/00.00.10.work/0509.pack-assembly/evidence/build05.01/verify.stdout.txt` | same | `b8c0583b745de93f9acafcb62b4c3d69c3325794d3348c9515f3d0537961bdba` | 1504 |
| 33 | `00.kernel/00.00.10.work/0509.pack-assembly/evidence/build05.01/SHA256SUMS.txt` | same | `a2156b25bbd13261a66be928dc82a365c22d98f4adaf84f1a3cbcefd90991b38` | 2220 |
| 34 | `00.kernel/00.00.10.work/0509.pack-assembly/evidence/pack05.01/source-manifest.json` | same | `4db26ef3c1d9c0a2ee03eef2469fc84f146d02b1e4e4ff6ce66c682285f40d75` | 1862 |
| 35 | `00.kernel/00.00.10.work/0504.app-entry/05.07.md` | `00.kernel/00.00.10.work/0509.pack-assembly/evidence/pack05.01/snapshots/0001.blob` | `246153bcaa86b2b3e056ae84263899a99dc39e011b54e4ed3f588334330fe8e7` | 9634 |
| 36 | `00.kernel/00.00.10.work/0504.app-entry/evidence/prime-review05.07/review.md` | `00.kernel/00.00.10.work/0509.pack-assembly/evidence/pack05.01/snapshots/0002.blob` | `013ffb0c11a3ef8daae309b3176560b6bca31d5ce24646733508338569ef144e` | 1311 |
| 37 | `labs/pack-custody-pass01/pack_check.py` | `00.kernel/00.00.10.work/0509.pack-assembly/evidence/pack05.01/snapshots/0003.blob` | `9bbd9d57f3b7da43234ac2e6ae4ce40a0ab6af2f53c8135ecfb2ee0c8a6e322d` | 21563 |
| 38 | `labs/pack-custody-pass01/README.md` | `00.kernel/00.00.10.work/0509.pack-assembly/evidence/pack05.01/snapshots/0004.blob` | `657ef6032cb4fdead6a8f93450792c97a3e46b837d3a191aa3f19983ff4969af` | 5074 |
| 39 | `labs/pack-custody-pass01/tests/test_pack_check.py` | `00.kernel/00.00.10.work/0509.pack-assembly/evidence/pack05.01/snapshots/0005.blob` | `07a50f4b719f8de71119c1459e40f1bfe6c6ce992aff64d3818a2d994656f69b` | 26105 |
| 40 | `00.kernel/00.00.01.law/0303.jobs/02.jobs.010.py` | `00.kernel/00.00.10.work/0509.pack-assembly/evidence/pack05.01/snapshots/0006.blob` | `7b39308592b63f080820de907eed996e6e9ac30c5b90e9502c628578fc1c3547` | 97270 |
| 41 | `00.kernel/00.00.10.work/0508.return-capture/05.01.md` | `00.kernel/00.00.10.work/0509.pack-assembly/evidence/pack05.01/snapshots/0007.blob` | `fca5b450312f0201fa9a2e60d686cb3e982524266030a54353d65dfb6655001e` | 9747 |
| 42 | `00.kernel/00.00.10.work/0507.prime-support/05.03.md` | `00.kernel/00.00.10.work/0509.pack-assembly/evidence/pack05.01/snapshots/0008.blob` | `19cf1e4e5c9317d85e7dc4283ed7abe793c32cf8dceeac90a777c89b05339fea` | 4151 |
| 43 | `00.kernel/00.00.10.work/0509.pack-assembly/evidence/prime-review05.01/custody.json` | same | `14ab3a9577958d70147749ad029319aaff18882843a939a993aacc75fd8cd3e7` | 722 |
| 44 | `00.kernel/00.00.10.work/0509.pack-assembly/evidence/prime-review05.01/pack-assembly-pass01.txt` | same | `d4dfe4825778562ec483b89ec7ee3c101a877b24b67b587a044ff03b901e9070` | 126 |
| 45 | `00.kernel/00.00.10.work/0509.pack-assembly/evidence/prime-review05.01/review.md` | same | `70bd68aaa86f5f9da2ef95530601c61e2288a5c50259231fc5ec1732731b6ef9` | 1239 |
| 46 | `00.kernel/00.00.10.work/0509.pack-assembly/evidence/prime-review05.01/reviewed-05.01.md` | same | `e0945f4a5cc356ccc571dcc877167c0e4cadc19b34ca547b33135f5375e6f1fc` | 9194 |
| 47 | `00.kernel/00.00.10.work/0509.pack-assembly/evidence/prime-review05.01/verification.json` | same | `0768d05a32bfbe9e93a86f776cca39b494b367ee0dff04dadb974904d195faad` | 1845 |

Relationship counts from the qualified row: cited dependency 2, delivered artifact 6, review/test evidence 32, source input 7.

## Failures

None. Blob export, hash checks, capture, verify, and inspect each finished on the first attempt. No partial member was left. No substitute member was allocated.

## Current report

`0129.assembly-capture-0510` is the separate current capture, submission `grok-2-0508-0510`. It is not retrospective, it has no source commit, and it does not carry the embedded-review flag. Its outputs are `06.11.md`, `source-map.json`, this report, and `verification.json`. The dedicated submission is the return file. When this report was written, `0129` held only `01.md` and `reservation.json`. This report does not contain the later `0129` receipt.
