# Backfill report — historical returns at one published commit

Date: 2026-10-27. Recorder: Grok Builder 2. Schema of the row file: `return-capture-backfill-plan/1`.

This report reconciles the inventory. Exact payload rows live in `backfill-plan.json` beside this file. The method is in `0508.return-capture/06.04.md`, written before either evidence file.

## Count reconciliation

Inventory commit `75ae515d826482113c4126274d015de112aa249b`. Tree files: 2920. Batch pages: 31. Expansion bound: 12 files. A directory above that bound, and any path under `returns/`, stays unresolved with a count.

Classification of the 31 batch pages:

- `no-return`: 2
- `return-present`: 1
- `return-pending`: 2
- `review-without-return`: 1
- `return-and-review`: 25
- Sum: 31

Status of the same 31 pages:

- `excluded`: 5
- `not-proposed`: 3
- `proposed`: 3
- `unresolved`: 20
- Sum: 31

Root `returns/` files are outside the 31. Three files were inventoried. Two are proposed historical slices. One proposal stays unresolved. Pack A and Pack B are not the recommended next batch.

A classification is a heading check. It does not mean the work is complete, accepted, or ready to capture.

## Already captured

These members stay sealed. Baseline hashes are the inventory-commit page. Sealed hashes are the current return file named by the receipt. This plan does not recapture them.

### `0101.app-entry-0506`

- Submission: `0504-05-06-pinned`. Origin page `0504.app-entry`, batch `05.06`.
- Sealed return `51332cea6913d812c940574432a891f05c4b2667719f465b4a613dbea0a62cf6` | 13251. Receipt `bb71698f903c786497fa44b34cef046f32fabc01a039b40e53e8bd940a1a3580`. Captured at `2026-10-27T19:25:40.059655Z`. Payloads in the sealed package: 60.
- Sealed retrospective: `true`. Sealed Prime-review flag: `true`. Sealed source commit: `e6d6eb75538732c7eedbc840042242d386b25c2f`.
- Baseline page `00.kernel/00.00.10.work/0504.app-entry/05.06.md` `a9ee40b19dd6af021df32e5a89a344ca829146dd9a9b9a6a8f88bffbe8c7f4fc` | 13597. Baseline classification `return-and-review`.
- Reason: Already preserved as 0101.app-entry-0506. This plan does not recapture it. The baseline page bytes and the sealed return bytes are recorded separately.

### `0104.app-entry-0508`

- Submission: `grok-1-0504-0508`. Origin page `0504.app-entry`, batch `05.08`.
- Sealed return `6fc2925a80d858a0be69e14a801856c6eefba3720e7ff1a31e31fe02ad26013f` | 8371. Receipt `84397f6c2d42c457aeccfba8d06c4e6ce7cb674d040c7e98d1463863a3d80acf`. Captured at `2026-10-27T19:35:29.531725Z`. Payloads in the sealed package: 40.
- Sealed retrospective: `false`. Sealed Prime-review flag: `false`. Sealed source commit: null.
- Baseline page `00.kernel/00.00.10.work/0504.app-entry/05.08.md` `fcff6376e35e54e881cbdc7fa641f712bc03fabb2ad2d949be85db62918a0fb1` | 3650. Baseline classification `return-pending`.
- Reason: Already preserved as 0104.app-entry-0508. This plan does not recapture it. The baseline page bytes and the sealed return bytes are recorded separately.

### `0102.prime-support-0501`

- Submission: `0507-05-01-pinned`. Origin page `0507.prime-support`, batch `05.01`.
- Sealed return `0c91acfe02943770c25950670bbcfc5b6fe732a747707185f7d40bf00968c983` | 17634. Receipt `51cf321df7da075155dee7d6c604d016b09ccacfca05026f29f776d58f88fa4a`. Captured at `2026-10-27T19:25:41.052436Z`. Payloads in the sealed package: 28.
- Sealed retrospective: `true`. Sealed Prime-review flag: `true`. Sealed source commit: `e6d6eb75538732c7eedbc840042242d386b25c2f`.
- Baseline page `00.kernel/00.00.10.work/0507.prime-support/05.01.md` `7b4a032a55a1c69ca2ac39441c688927460cedfd2787ce3748fa87dabda6e86f` | 17984. Baseline classification `return-and-review`.
- Reason: Already preserved as 0102.prime-support-0501. This plan does not recapture it. The baseline page bytes and the sealed return bytes are recorded separately.

### `0105.prime-clerk-0504`

- Submission: `claude-0507-0504`. Origin page `0507.prime-support`, batch `05.04`.
- Sealed return `5e3995f136f8a586b8a8fd29f665ad4d099703bfbe23301d7be74aaf683ba21c` | 11195. Receipt `c24d2441a28e0f511181db337ef32aedfe7b951ca011a44ffc04c93ac4eebb9c`. Captured at `2026-10-27T19:35:30.081353Z`. Payloads in the sealed package: 35.
- Sealed retrospective: `false`. Sealed Prime-review flag: `false`. Sealed source commit: null.
- Baseline page `00.kernel/00.00.10.work/0507.prime-support/05.04.md` `09743de103e4111c951b88032a49e13ea5956aefb8a73d8b0a7d32cd73538668` | 5055. Baseline classification `return-pending`.
- Reason: Already preserved as 0105.prime-clerk-0504. This plan does not recapture it. The baseline page bytes and the sealed return bytes are recorded separately.

### `0103.return-capture-0502`

- Submission: `0508-05-02-local-return`. Origin page `0508.return-capture`, batch `05.02`.
- Sealed return `235b1a2b6483a84a473ca494a01bd3931422eb7675162bc559ec8f14d5ec6b51` | 7802. Receipt `1781cf57eb74cede72343bd1895b2463c2b8c76094488403731f2bb72b96166a`. Captured at `2026-10-27T19:25:41.366514Z`. Payloads in the sealed package: 14.
- Sealed retrospective: `false`. Sealed Prime-review flag: `false`. Sealed source commit: null.
- Baseline page `00.kernel/00.00.10.work/0508.return-capture/05.02.md` `7cc77a8f11647366b398d769ce1029b6017e3d1ecfdcdbd59a14041538f3c191` | 9592. Baseline classification `return-and-review`.
- Reason: Already preserved as 0103.return-capture-0502. This plan does not recapture it. The baseline page bytes and the sealed return bytes are recorded separately.

`0104` and `0105` baseline pages are pending returns. The baseline does not contain their latest submissions. `0103` baseline page hash matches the pack pin of `05.02.md` (9592 bytes). The sealed return is a dedicated submission of 7802 bytes.

## Occupied reservations

This plan allocates nothing. The occupied names below are recorded so a later backfill does not pick them.

- `0106.entry-regression-0509`
- `0107.clerk-types-0505`
- `0108.backfill-plan-0503`

`0106.entry-regression-0509` reserves a later `0504.app-entry/05.09` submission. `0107.clerk-types-0505` reserves a later `0507.prime-support/05.05` submission. Those two pages are absent from the 31 pages at the inventory commit. `0108.backfill-plan-0503` is the slot that captures this plan only.

## Not proposed

These pages have no completed return body. They are not treated as finished work.

### `00.kernel/00.00.10.work/0501.bootstrap/05.01.md`

- Origin book: `00.00.10.work`.
- Page: `00.kernel/00.00.10.work/0501.bootstrap/05.01.md`.
- Batch: `05.01`.
- Source commit: `75ae515d826482113c4126274d015de112aa249b`.
- Return source: `00.kernel/00.00.10.work/0501.bootstrap/05.01.md` | `05df1a710a5add38f278458004d21dabc6fc80f124af98162f890a170090a966` | 1577.
- Prime review already in the return source: `false`.
- Retrospective: `true`.
- Classification: `no-return`.
- Scope: Retrospective custody of these exact bytes at the inventory commit. The return file is stored whole. Embedded Director replies and a Review heading stay inside that file. This plan does not allocate a member, does not claim a standalone reproduction, and does not accept the work.
- Reason: No completed return body at this commit. An assignment or a review without that body is not treated as finished work.

### `00.kernel/00.00.10.work/0501.bootstrap/05.02.md`

- Origin book: `00.00.10.work`.
- Page: `00.kernel/00.00.10.work/0501.bootstrap/05.02.md`.
- Batch: `05.02`.
- Source commit: `75ae515d826482113c4126274d015de112aa249b`.
- Return source: `00.kernel/00.00.10.work/0501.bootstrap/05.02.md` | `24f92751533df3f1287626ca21a5ed847666ec6fd3cf5c53fefdd3637da59979` | 5281.
- Prime review already in the return source: `false`.
- Retrospective: `true`.
- Classification: `no-return`.
- Scope: Retrospective custody of these exact bytes at the inventory commit. The return file is stored whole. Embedded Director replies and a Review heading stay inside that file. This plan does not allocate a member, does not claim a standalone reproduction, and does not accept the work.
- Reason: No completed return body at this commit. An assignment or a review without that body is not treated as finished work.

### `00.kernel/00.00.10.work/0504.app-entry/05.02.md`

- Origin book: `00.00.10.work`.
- Page: `00.kernel/00.00.10.work/0504.app-entry/05.02.md`.
- Batch: `05.02`.
- Source commit: `75ae515d826482113c4126274d015de112aa249b`.
- Return source: `00.kernel/00.00.10.work/0504.app-entry/05.02.md` | `7772d79831d5bdc86764ec0d8a0ffa0374c98fd326757f6e770842f577739107` | 13834.
- Prime review already in the return source: `true`.
- Retrospective: `true`.
- Classification: `review-without-return`.
- Scope: Retrospective custody of these exact bytes at the inventory commit. The return file is stored whole. Embedded Director replies and a Review heading stay inside that file. This plan does not allocate a member, does not claim a standalone reproduction, and does not accept the work.
- Reason: No completed return body at this commit. An assignment or a review without that body is not treated as finished work.

## Proposed batch pages

Each row below is a closed named set at the inventory commit. Historical submissions stay retrospective. The return file is stored whole. No member address is chosen.

### `00.kernel/00.00.10.work/0502.workflow-start/05.01.md`

- Origin book: `00.00.10.work`.
- Page: `00.kernel/00.00.10.work/0502.workflow-start/05.01.md`.
- Batch: `05.01`.
- Source commit: `75ae515d826482113c4126274d015de112aa249b`.
- Return source: `00.kernel/00.00.10.work/0502.workflow-start/05.01.md` | `7f43ea75f0fc6f01229e0171312bc1f42a067df7a27e9689eab602d5f1bcfe17` | 20298.
- Prime review already in the return source: `true`.
- Retrospective: `true`.
- Classification: `return-and-review`.
- Scope: Retrospective custody of these exact bytes at the inventory commit. The return file is stored whole. Embedded Director replies and a Review heading stay inside that file. This plan does not allocate a member, does not claim a standalone reproduction, and does not accept the work.
- Reason: The page has one return body. Every named file is present, and every named directory is within the expansion bound. The payload is that closed set.
- Payload count besides the return file: 28.
- Payloads:
- `00.kernel/00.00.10.work/0502.workflow-start/01.md` | `93f0bf4f5d36ec9d7cc7064e9eca394dab9d1a2d00f011701e59cb63ce3f85fa` | 2063 | Path named by the page and present in the originating book at the inventory commit.
- `00.kernel/00.00.10.work/0502.workflow-start/06.01.md` | `70e294d3a7a75b430f039316e152f1ca269369d2de3cc34486d0eaaa4ff29cc7` | 12920 | Path named by the page and present in the originating book at the inventory commit.
- `returns/pack-B-prime-report-2026-10-26.md` | `824784cbc762569832e03e44929091dfd3486bc89e5a4f24e218394184e5ba37` | 10148 | Path named by the page and present at the inventory commit. It is a cited dependency, not a claim that this return reproduces that other batch.
- `00.kernel/00.00.10.work/0502.workflow-start/evidence/source-manifest-check.txt` | `7f1064cf2971c04a8322dd7151633c536ac5a25031b5a3328fce3665bc7441c7` | 4436 | Path named by the page and present in the originating book at the inventory commit.
- `00.kernel/00.00.10.work/0502.workflow-start/evidence/packed/06.01.md` | `c4b0ac43b4298b5a50be91f7bac2f7301c4f85d44c606d9645d8bb5819f51428` | 2782 | Path named by the page and present in the originating book at the inventory commit.
- `00.kernel/00.00.10.work/0502.workflow-start/evidence/live-running.md` | `3870d885c3977b26f6709e3b5ba1ce1c195eccfd797ced670d80c2b944b04d0e` | 1126 | Path named by the page and present in the originating book at the inventory commit.
- `00.kernel/00.00.10.work/0502.workflow-start/evidence/render-check.txt` | `22ac1f7cf91b38fc4b017c062d1d238a580f19e91f25f4e1771314f69ac83268` | 188 | Path named by the page and present in the originating book at the inventory commit.
- `00.kernel/00.00.10.work/0502.workflow-start/evidence/gitbytes-attrs.txt` | `af93bb161e326ed784d61e538690183fc3a39f8d7399fe9df6a8998372321dbc` | 22 | Path named by the page and present in the originating book at the inventory commit.
- `00.kernel/00.00.10.work/0502.workflow-start/evidence/gitbytes-worktree.txt` | `34495e8c048280e0b1aff1407e3aec1b170d06ab1b3ada455ebc8976311ce8b1` | 25 | Path named by the page and present in the originating book at the inventory commit.
- `00.kernel/00.00.10.work/0502.workflow-start/evidence/gitbytes-index.txt` | `8e78ab2c8fe78020fb6fbca44ba56621d3aad6a0b8efa683b221b58352c3922d` | 22 | Path named by the page and present in the originating book at the inventory commit.
- `00.kernel/00.00.10.work/0502.workflow-start/evidence/claim-status.txt` | `840f59f75db2e282f9cb31b1a8b1f912f322dddbfd907b94f63d0864740beace` | 1702 | Path named by the page and present in the originating book at the inventory commit.
- `00.kernel/00.00.10.work/0502.workflow-start/evidence/assignment-running.md` | `cc678936508ec0779a4001c2ae76b73586bbd067f740341eb00fe00697aa18bb` | 511 | Path named by the page and present in the originating book at the inventory commit.
- `00.kernel/00.00.10.work/0502.workflow-start/evidence/record-hashes.txt` | `6dafc451e348010ba8d82be04c03162bfeba1fd36dcf3536e7088ca81e641c36` | 1940 | Path named by the page and present in the originating book at the inventory commit.
- `00.kernel/00.00.10.work/0502.workflow-start/evidence/custody.tsv` | `ead3fe67793dda39317b2360155b8a6f1678bbc519cfbd725137ba82aa220105` | 4425 | Path named by the page and present in the originating book at the inventory commit.
- `labs/worker-bridge-pass01/evidence/page-before.sha256` | `fc8d64111c2b2b1be8a6d714d30e713fb940a0f24880241cab584720754c0f5e` | 308 | Path named by the page and present at the inventory commit. It is a cited dependency, not a claim that this return reproduces that other batch.
- `00.kernel/00.00.10.work/0502.workflow-start/evidence/readme-custody.tsv` | `32f949120b544f3fcac0d796f5596e34a53790c44825b012d4533746462607fb` | 98 | Path named by the page and present in the originating book at the inventory commit.
- `00.kernel/00.00.10.work/0502.workflow-start/evidence/packed/01.md` | `93f0bf4f5d36ec9d7cc7064e9eca394dab9d1a2d00f011701e59cb63ce3f85fa` | 2063 | File under 00.kernel/00.00.10.work/0502.workflow-start/evidence/packed, named by the page. The directory has 4 files, within this plan's expansion bound of 12.
- `00.kernel/00.00.10.work/0502.workflow-start/evidence/packed/05.01.md` | `458c790a8330596bba88e56645bdd5020a6f92f1e9fea0c2e5f2e31d59999687` | 9787 | File under 00.kernel/00.00.10.work/0502.workflow-start/evidence/packed, named by the page. The directory has 4 files, within this plan's expansion bound of 12.
- `00.kernel/00.00.10.work/0502.workflow-start/evidence/packed/source-manifest.tsv` | `f0c053aeff3a117e1158a112c58161970095e9d5f07fe297b2be047f02e448b0` | 1708 | File under 00.kernel/00.00.10.work/0502.workflow-start/evidence/packed, named by the page. The directory has 4 files, within this plan's expansion bound of 12.
- `00.kernel/00.00.10.work/0502.workflow-start/evidence/prime-review-2026-10-26/check-after-review.txt` | `b7b52de46a876676417a4729935c3e3eb9816f4fa6c41a71a8c34ba8b0a0738d` | 48 | File under 00.kernel/00.00.10.work/0502.workflow-start/evidence/prime-review-2026-10-26, named by the page. The directory has 6 files, within this plan's expansion bound of 12.
- `00.kernel/00.00.10.work/0502.workflow-start/evidence/prime-review-2026-10-26/render-after-review.txt` | `dedeafe4c7b72eb5d094d0299c125f33360d1dd41e0d4039a4b7233e327ca676` | 115 | File under 00.kernel/00.00.10.work/0502.workflow-start/evidence/prime-review-2026-10-26, named by the page. The directory has 6 files, within this plan's expansion bound of 12.
- `00.kernel/00.00.10.work/0502.workflow-start/evidence/prime-review-2026-10-26/returned-assignment-before-review.md` | `fe105bd5826854f8362751330b2f1fad0d61f69ea38258f2151246a195de0a49` | 507 | File under 00.kernel/00.00.10.work/0502.workflow-start/evidence/prime-review-2026-10-26, named by the page. The directory has 6 files, within this plan's expansion bound of 12.
- `00.kernel/00.00.10.work/0502.workflow-start/evidence/prime-review-2026-10-26/review-checks.py` | `15e8e2274154a17e0865ff75c54d6f098ed2f965334c1553918e626fbe368468` | 4966 | File under 00.kernel/00.00.10.work/0502.workflow-start/evidence/prime-review-2026-10-26, named by the page. The directory has 6 files, within this plan's expansion bound of 12.
- `00.kernel/00.00.10.work/0502.workflow-start/evidence/prime-review-2026-10-26/review-transition.json` | `a16bbb0e4562c09ce6126992c165f2223faf0e2f51eb7317aded0129135501e3` | 1081 | File under 00.kernel/00.00.10.work/0502.workflow-start/evidence/prime-review-2026-10-26, named by the page. The directory has 6 files, within this plan's expansion bound of 12.
- `00.kernel/00.00.10.work/0502.workflow-start/evidence/prime-review-2026-10-26/verification.json` | `f4e59484055cbd6855776d2ba1357ce9f5f144b5302cd02020805947f049eafd` | 1251 | File under 00.kernel/00.00.10.work/0502.workflow-start/evidence/prime-review-2026-10-26, named by the page. The directory has 6 files, within this plan's expansion bound of 12.
- `00.kernel/00.00.10.work/0502.workflow-start/evidence/observer-intake-2026-10-27/historical-custody-check.txt` | `dabeb71b344c0be0780b6b52696c9daca25f66b625a625bd1ad7c28506a67b25` | 199 | File under 00.kernel/00.00.10.work/0502.workflow-start/evidence/observer-intake-2026-10-27, named by the page. The directory has 3 files, within this plan's expansion bound of 12.
- `00.kernel/00.00.10.work/0502.workflow-start/evidence/observer-intake-2026-10-27/original-review.md` | `c41c9094461895c52411038ed70a6a91921ac506eb2747637a5c9dd66b432c1b` | 21621 | File under 00.kernel/00.00.10.work/0502.workflow-start/evidence/observer-intake-2026-10-27, named by the page. The directory has 3 files, within this plan's expansion bound of 12.
- `00.kernel/00.00.10.work/0502.workflow-start/evidence/observer-intake-2026-10-27/source.json` | `fdd6ca101269b2138e452064edf4d774fb63264b48bdd7fd86b057acbb87516c` | 482 | File under 00.kernel/00.00.10.work/0502.workflow-start/evidence/observer-intake-2026-10-27, named by the page. The directory has 3 files, within this plan's expansion bound of 12.

### `00.kernel/00.00.10.work/0504.app-entry/05.03.md`

- Origin book: `00.00.10.work`.
- Page: `00.kernel/00.00.10.work/0504.app-entry/05.03.md`.
- Batch: `05.03`.
- Source commit: `75ae515d826482113c4126274d015de112aa249b`.
- Return source: `00.kernel/00.00.10.work/0504.app-entry/05.03.md` | `6452628638d2237a82ca850da3925a57cc9c128ba1f92f28454087acce486187` | 12335.
- Prime review already in the return source: `true`.
- Retrospective: `true`.
- Classification: `return-and-review`.
- Scope: Retrospective custody of these exact bytes at the inventory commit. The return file is stored whole. Embedded Director replies and a Review heading stay inside that file. This plan does not allocate a member, does not claim a standalone reproduction, and does not accept the work.
- Reason: The page has one return body. Every named file is present, and every named directory is within the expansion bound. The payload is that closed set.
- Payload count besides the return file: 19.
- Payloads:
- `00.kernel/00.00.10.work/0504.app-entry/evidence/pack05.03/source-manifest.tsv` | `c5e1a1b524867179046d88459b6611ca8c3e8dccb54ef9fdecf3069f92c47f8f` | 974 | Path named by the page and present in the originating book at the inventory commit.
- `app/README.md` | `f57ff8b523dbdd7fdc6cc19da9ee34dc611a5cef1aed5a01b544726384ca6cbf` | 6930 | Path named by the page and present at the inventory commit. It is a cited dependency, not a claim that this return reproduces that other batch.
- `00.kernel/00.00.10.work/0504.app-entry/06.03.md` | `ec2c3004094d5b9ab770c53b78b135e5115dfab02f2f3778c098d2533ff8c4cc` | 5969 | Path named by the page and present in the originating book at the inventory commit.
- `00.kernel/00.00.10.work/0504.app-entry/fixtures/02.inventory.py` | `dd6a78b5a3781fe840e68950805b9838e569095d15dac3c678f00782341ed69b` | 2988 | Path named by the page and present in the originating book at the inventory commit.
- `app/development-workspace.json` | `b6f4e13b3157416a05b102dfe8a01605e007c2608ba6b0fd06987757d2e33018` | 538 | Path named by the page and present at the inventory commit. It is a cited dependency, not a claim that this return reproduces that other batch.
- `00.kernel/00.00.10.work/0504.app-entry/evidence/colab05.03/reviewed-sources.tsv` | `5bca63acc6af63ea6d0c7dbc0c69952f6f5bc975f32641d2b81371eee67ac795` | 833 | Path named by the page and present in the originating book at the inventory commit.
- `00.kernel/00.00.10.work/0504.app-entry/evidence/colab05.03/SHA256SUMS.txt` | `a11a75b4f8be5b55c8356ee693021856babeb9b87c43242208b2f6f878bb5845` | 485 | File under 00.kernel/00.00.10.work/0504.app-entry/evidence/colab05.03, named by the page. The directory has 7 files, within this plan's expansion bound of 12.
- `00.kernel/00.00.10.work/0504.app-entry/evidence/colab05.03/app-suite.txt` | `a0588b17efe9556f599193ea4a66f44fdc9bbd603844ddf8550945fa2874e42e` | 2111 | File under 00.kernel/00.00.10.work/0504.app-entry/evidence/colab05.03, named by the page. The directory has 7 files, within this plan's expansion bound of 12.
- `00.kernel/00.00.10.work/0504.app-entry/evidence/colab05.03/probes.py` | `abeac9cba98a3b375fb027cda07c205f422b2f2c08810cf22127aff0838d1005` | 10812 | File under 00.kernel/00.00.10.work/0504.app-entry/evidence/colab05.03, named by the page. The directory has 7 files, within this plan's expansion bound of 12.
- `00.kernel/00.00.10.work/0504.app-entry/evidence/colab05.03/probes.txt` | `a999164caba539c1dae03ba5634c11482de5e6020087f67091e19281430ba87a` | 12965 | File under 00.kernel/00.00.10.work/0504.app-entry/evidence/colab05.03, named by the page. The directory has 7 files, within this plan's expansion bound of 12.
- `00.kernel/00.00.10.work/0504.app-entry/evidence/colab05.03/status-probe.txt` | `a9022b64c528891826bf6cf58b385e4dfad3ced4b2aa90c33045ba738289d9f3` | 896 | File under 00.kernel/00.00.10.work/0504.app-entry/evidence/colab05.03, named by the page. The directory has 7 files, within this plan's expansion bound of 12.
- `00.kernel/00.00.10.work/0504.app-entry/evidence/colab05.03/status_probe.py` | `a9f5839bdf7636aa95d001c92633242fd4963d30b6a52773fb68a5c75e391720` | 1411 | File under 00.kernel/00.00.10.work/0504.app-entry/evidence/colab05.03, named by the page. The directory has 7 files, within this plan's expansion bound of 12.
- `00.kernel/00.00.10.work/0504.app-entry/evidence/prime-review05.03-2026-10-27/hardlink-probe.stderr.txt` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 0 | File under 00.kernel/00.00.10.work/0504.app-entry/evidence/prime-review05.03-2026-10-27, named by the page. The directory has 7 files, within this plan's expansion bound of 12.
- `00.kernel/00.00.10.work/0504.app-entry/evidence/prime-review05.03-2026-10-27/hardlink-probe.stdout.txt` | `e58610f1359dd3b4120f3343e33404b5f131e7be0a83e51b047a1a2f06d512cb` | 858 | File under 00.kernel/00.00.10.work/0504.app-entry/evidence/prime-review05.03-2026-10-27, named by the page. The directory has 7 files, within this plan's expansion bound of 12.
- `00.kernel/00.00.10.work/0504.app-entry/evidence/prime-review05.03-2026-10-27/hardlink-proof.json` | `6c5c305ebe1d021fbbbfc5f30ba30b73e78eabfdb54e8de96adef4b062fa8e46` | 347 | File under 00.kernel/00.00.10.work/0504.app-entry/evidence/prime-review05.03-2026-10-27, named by the page. The directory has 7 files, within this plan's expansion bound of 12.
- `00.kernel/00.00.10.work/0504.app-entry/evidence/prime-review05.03-2026-10-27/morning-finish-verification.py` | `3aff732f37188f27b3721ea3c2b8710d66f5473cf54075453b558bf24cbc08fc` | 1327 | File under 00.kernel/00.00.10.work/0504.app-entry/evidence/prime-review05.03-2026-10-27, named by the page. The directory has 7 files, within this plan's expansion bound of 12.
- `00.kernel/00.00.10.work/0504.app-entry/evidence/prime-review05.03-2026-10-27/morning-verify-2026-10-27.py` | `64f46e4b08e937725a796d39cc1b504f310de8a5ebc4f0628dee6f2fa1ee98a7` | 3409 | File under 00.kernel/00.00.10.work/0504.app-entry/evidence/prime-review05.03-2026-10-27, named by the page. The directory has 7 files, within this plan's expansion bound of 12.
- `00.kernel/00.00.10.work/0504.app-entry/evidence/prime-review05.03-2026-10-27/reviewed-return.md` | `aa4bdb053d83bd5c3fab22f6be5848f17af3515388dc19f3600f745e7387ca3c` | 10837 | File under 00.kernel/00.00.10.work/0504.app-entry/evidence/prime-review05.03-2026-10-27, named by the page. The directory has 7 files, within this plan's expansion bound of 12.
- `00.kernel/00.00.10.work/0504.app-entry/evidence/prime-review05.03-2026-10-27/verification.json` | `b3f38500738310923226d4028a580adccdde83a4e13fa8489162ad30aabf5e26` | 884 | File under 00.kernel/00.00.10.work/0504.app-entry/evidence/prime-review05.03-2026-10-27, named by the page. The directory has 7 files, within this plan's expansion bound of 12.

### `00.kernel/00.00.10.work/0505.observer-design/05.01.md`

- Origin book: `00.00.10.work`.
- Page: `00.kernel/00.00.10.work/0505.observer-design/05.01.md`.
- Batch: `05.01`.
- Source commit: `75ae515d826482113c4126274d015de112aa249b`.
- Return source: `00.kernel/00.00.10.work/0505.observer-design/05.01.md` | `952fb8a774cb174fe1b96ddbfdc9bc9df42a2f0e18e42557d21da02a52f2fea3` | 3216.
- Prime review already in the return source: `false`.
- Retrospective: `true`.
- Classification: `return-present`.
- Scope: Retrospective custody of these exact bytes at the inventory commit. The return file is stored whole. Embedded Director replies and a Review heading stay inside that file. This plan does not allocate a member, does not claim a standalone reproduction, and does not accept the work.
- Reason: The page has one return body. Every named file is present, and every named directory is within the expansion bound. The payload is that closed set.
- Payload count besides the return file: 5.
- Payloads:
- `00.kernel/00.00.10.work/0505.observer-design/01.md` | `2a9c65992d569f54f27d798c58e681b3afed644cd443e1c21d0f0e42693eb3de` | 16251 | Path named by the page and present in the originating book at the inventory commit.
- `00.kernel/00.00.10.work/0502.workflow-start/05.01.md` | `7f43ea75f0fc6f01229e0171312bc1f42a067df7a27e9689eab602d5f1bcfe17` | 20298 | Path named by the page and present at the inventory commit. It is a cited dependency, not a claim that this return reproduces that other batch.
- `00.kernel/00.00.10.work/0505.observer-design/templates/role-observer.md` | `e49f10a9e6daed2e93122d338a60290073f66d21fb24aa6be7dc4a29ea8682e7` | 2997 | Path named by the page and present in the originating book at the inventory commit.
- `00.kernel/00.00.10.work/0502.workflow-start/06.02.md` | `4bb3101fd9f91243c97f24dfe35e6c8ce2d3e881115d8bba9122d7b61cd377a6` | 25057 | Path named by the page and present at the inventory commit. It is a cited dependency, not a claim that this return reproduces that other batch.
- `00.kernel/00.00.10.work/0505.observer-design/templates/review-record.md` | `1e84077338c00d74061ff4f56a22bf1efeb2ef4b4a515b3b8d9c76def556e461` | 2068 | Path named by the page and present in the originating book at the inventory commit.

## Proposed root returns

The door keeps `returns/` historical. These rows do not move those files and do not assign member numbers. Companion checker source is stored as bytes and was not executed. `includes_prime_review` is false because the return file itself has no Review heading. The Prime report is sibling evidence.

### `returns/pack-A-preserve-return.md`

- Origin book: `00.00.10.work`.
- Page: `returns/pack-A-preserve-return.md`.
- Batch: `none (root return)`.
- Source commit: `75ae515d826482113c4126274d015de112aa249b`.
- Return source: `returns/pack-A-preserve-return.md` | `e92c98059c92a597424a3be858d1a47af5db4fa2c58f7dfa2e80dea6b669bae6` | 12878.
- Prime review already in the return source: `false`.
- Retrospective: `true`.
- Classification: `historical-root-return`.
- Scope: Retrospective custody of these exact bytes at the inventory commit. The return file is stored whole. Embedded Director replies and a Review heading stay inside that file. This plan does not allocate a member, does not claim a standalone reproduction, and does not accept the work. The Prime report and review files are sibling evidence, not a split of the return body. Checker source is stored as bytes and was not executed.
- Reason: Historical file under returns/. The door keeps that root historical. The title identifies a return. No 05.NN heading is invented.
- Companion count: 3.
- Companions:
- `returns/pack-A-prime-report-2026-10-26.md` | `89fb7f9c631be480c1ec968ea9d9a2bd70cc32a197e3cd98402391ecdd7b7d31` | 4527 | Sibling evidence of this historical root return at the inventory commit.
- `returns/pack-A-prime-verification-2026-10-26.json` | `aed66636eb9222e25fff2fbb436342bb30ae3ba6b79d7d47c9fa1aa6103ba7f2` | 1902 | Sibling evidence of this historical root return at the inventory commit.
- `returns/pack-A-prime-review-checks-2026-10-26.py` | `c9bb737a481aeaa8e85ef87d90ca6430a1537f5ecfc8c3437b00b853326115d9` | 4771 | Sibling evidence of this historical root return at the inventory commit.

### `returns/pack-B-establish-return.md`

- Origin book: `00.00.10.work`.
- Page: `returns/pack-B-establish-return.md`.
- Batch: `none (root return)`.
- Source commit: `75ae515d826482113c4126274d015de112aa249b`.
- Return source: `returns/pack-B-establish-return.md` | `c51ef636e2ca6c19a6e0ee7e6872ebdf5ff64176ec1ce9e4a487d8dabf72b924` | 18735.
- Prime review already in the return source: `false`.
- Retrospective: `true`.
- Classification: `historical-root-return`.
- Scope: Retrospective custody of these exact bytes at the inventory commit. The return file is stored whole. Embedded Director replies and a Review heading stay inside that file. This plan does not allocate a member, does not claim a standalone reproduction, and does not accept the work. The Prime report and review files are sibling evidence, not a split of the return body. Checker source is stored as bytes and was not executed.
- Reason: Historical file under returns/. The door keeps that root historical. The title identifies a return. No 05.NN heading is invented.
- Companion count: 9.
- Companions:
- `returns/pack-B-prime-report-2026-10-26.md` | `824784cbc762569832e03e44929091dfd3486bc89e5a4f24e218394184e5ba37` | 10148 | Sibling evidence of this historical root return at the inventory commit.
- `returns/pack-B-prime-review-2026-10-26/publication-hashes.json` | `54ad2ab6b71ad5f4d7c160d078f299de5d02f532159b4e092031d16aaff0f76a` | 1285 | Sibling evidence of this historical root return at the inventory commit.
- `returns/pack-B-prime-review-2026-10-26/remote-refs.json` | `e7f0d580862665eb2c11c502f8590f42c27ec602a6440787d03ec2d4964a169e` | 618 | Sibling evidence of this historical root return at the inventory commit.
- `returns/pack-B-prime-review-2026-10-26/review-pack-b-2026-10-26.py` | `508a05af9aa5160da9e8f56506512d743f4d205cc42dc6d0b2f72ab15cfbb065` | 6629 | Sibling evidence of this historical root return at the inventory commit.
- `returns/pack-B-prime-review-2026-10-26/test_gitbytes.py.log` | `797c6950f152474897ccf33ec3897c9fd75c42f4f1fa1c7f56993d0dfd12c353` | 5456 | Sibling evidence of this historical root return at the inventory commit.
- `returns/pack-B-prime-review-2026-10-26/test_gitbytes.py.retry.log` | `814f6c8bf3958ba37654bea5b5f7e2d978b1bbd709b01b2ff3241d974b556f16` | 651 | Sibling evidence of this historical root return at the inventory commit.
- `returns/pack-B-prime-review-2026-10-26/test_import_blobs.py.retry.log` | `4764e8495346f6c3d86bbe1f7b20e08c9b1b23d69d58a50858ede01c060bafc9` | 1220 | Sibling evidence of this historical root return at the inventory commit.
- `returns/pack-B-prime-review-2026-10-26/test_render_live.py.retry.log` | `5636e8697ec4efbb2f42f24e0b449010bb66ef6e39aaf0242c3a9f883515a4a0` | 475 | Sibling evidence of this historical root return at the inventory commit.
- `returns/pack-B-prime-review-2026-10-26/verification.json` | `2222e6324bddb204543384135051f434a7cd844219f319a7c853f52519c2085e` | 2873 | Sibling evidence of this historical root return at the inventory commit.

## Unresolved

A return body may exist. The payload is withheld because a named path is absent or a named directory exceeds 12 files. Empty payload lists are intentional. Missing evidence is not fabricated.

### `00.kernel/00.00.10.work/0502.workflow-start/05.02.md`

- Return source `c25ba5502b51632bb92888322cbe80f980b925edbacf1c08f59bdb1a1c479ae9` | 11578. Classification `return-and-review`. Prime review in the file: `true`.
- Reason: The page has a return body, and the whole file would be the return source. The payload is not proposed as complete because named evidence is missing or a named directory exceeds the expansion bound.
- Withheld:
- `00.kernel/00.00.10.work/0502.workflow-start/evidence/check05.02` | 14 files | Named directory has 14 files. This plan does not expand directories above 12 files, and it does not expand the historical returns root.

### `00.kernel/00.00.10.work/0502.workflow-start/05.03.md`

- Return source `5bda1a2b445d1d35b086aae2a71c5513eafb04791c660c749d1c9df925d47a85` | 10287. Classification `return-and-review`. Prime review in the file: `true`.
- Reason: The page has a return body, and the whole file would be the return source. The payload is not proposed as complete because named evidence is missing or a named directory exceeds the expansion bound.
- Withheld:
- `00.kernel/00.00.10.work/0502.workflow-start/evidence/repair05.03` | 19 files | Named directory has 19 files. This plan does not expand directories above 12 files, and it does not expand the historical returns root.
- `00.kernel/00.00.10.work/0502.workflow-start/evidence/SHA256SUMS.pass02.txt` | Named path is not a file or directory at the inventory commit.
- `00.kernel/00.00.10.work/0502.workflow-start/evidence/SHA256SUMS.txt` | Named path is not a file or directory at the inventory commit.

### `00.kernel/00.00.10.work/0503.worker-bridge/05.01.md`

- Return source `8b133e4e4c2356d1bac364f25e14bacaac84c89165545cb731109075c793fadc` | 21102. Classification `return-and-review`. Prime review in the file: `true`.
- Reason: The page has a return body, and the whole file would be the return source. The payload is not proposed as complete because named evidence is missing or a named directory exceeds the expansion bound.
- Withheld:
- `labs/worker-bridge-pass01` | 170 files | Named directory has 170 files. This plan does not expand directories above 12 files, and it does not expand the historical returns root.
- `returns` | 15 files | Named directory has 15 files. This plan does not expand directories above 12 files, and it does not expand the historical returns root.
- `00.kernel/00.00.10.work/0503.worker-bridge/evidence/CONTRACT.before-implementation.md` | Named path is not a file or directory at the inventory commit.
- `00.kernel/00.00.10.work/0503.worker-bridge/evidence/demo-run-01/trace.md` | Named path is not a file or directory at the inventory commit.
- `00.kernel/00.00.10.work/0503.worker-bridge/evidence/tests/run-01.txt` | Named path is not a file or directory at the inventory commit.

### `00.kernel/00.00.10.work/0503.worker-bridge/05.02.md`

- Return source `c40d25813055db11e1d6a2b9dfee265526a77afcaa7d8983d71e77a0ef3b9b80` | 17529. Classification `return-and-review`. Prime review in the file: `true`.
- Reason: The page has a return body, and the whole file would be the return source. The payload is not proposed as complete because named evidence is missing or a named directory exceeds the expansion bound.
- Withheld:
- `labs/worker-bridge-pass01` | 170 files | Named directory has 170 files. This plan does not expand directories above 12 files, and it does not expand the historical returns root.
- `00.kernel/00.00.10.work/0503.worker-bridge/evidence/SHA256SUMS.txt` | Named path is not a file or directory at the inventory commit.
- `00.kernel/00.00.10.work/0503.worker-bridge/evidence/pass02/pass02.patch` | Named path is not a file or directory at the inventory commit.
- `00.kernel/00.00.10.work/0503.worker-bridge/evidence/pass02/probes/probes-before.json` | Named path is not a file or directory at the inventory commit.
- `00.kernel/00.00.10.work/0503.worker-bridge/evidence/pass02/SHA256SUMS.pass02.txt` | Named path is not a file or directory at the inventory commit.

### `00.kernel/00.00.10.work/0503.worker-bridge/05.03.md`

- Return source `baf277dd5babc40cf754018eeab7a1398d7542f6e5bbaf3940e19711dd653381` | 13747. Classification `return-and-review`. Prime review in the file: `true`.
- Reason: The page has a return body, and the whole file would be the return source. The payload is not proposed as complete because named evidence is missing or a named directory exceeds the expansion bound.
- Withheld:
- `labs/worker-bridge-pass01` | 170 files | Named directory has 170 files. This plan does not expand directories above 12 files, and it does not expand the historical returns root.
- `00.kernel/00.00.10.work/0503.worker-bridge/evidence/prime-review-latest-2026-10-26` | 14 files | Named directory has 14 files. This plan does not expand directories above 12 files, and it does not expand the historical returns root.
- `00.kernel/00.00.10.work/0503.worker-bridge/evidence/pass02/SHA256SUMS.pass02.txt` | Named path is not a file or directory at the inventory commit.
- `00.kernel/00.00.10.work/0503.worker-bridge/evidence/pass03/tests/pass03-BEFORE-fix.txt` | Named path is not a file or directory at the inventory commit.
- `00.kernel/00.00.10.work/0503.worker-bridge/evidence/pass03/probes/prime-inherited-before.json` | Named path is not a file or directory at the inventory commit.
- `00.kernel/00.00.10.work/0503.worker-bridge/evidence/pass03/probes/prime-inherited-after.json` | Named path is not a file or directory at the inventory commit.
- `00.kernel/00.00.10.work/0503.worker-bridge/evidence/pass03/probes/original-three-probes-after.json` | Named path is not a file or directory at the inventory commit.
- `00.kernel/00.00.10.work/0503.worker-bridge/evidence/pass03/leftover-processes.txt` | Named path is not a file or directory at the inventory commit.
- `00.kernel/00.00.10.work/0503.worker-bridge/evidence/pass03/source-before.sha256` | Named path is not a file or directory at the inventory commit.
- `00.kernel/00.00.10.work/0503.worker-bridge/evidence/pass03/SHA256SUMS.pass03.txt` | Named path is not a file or directory at the inventory commit.
- `00.kernel/00.00.10.work/0503.worker-bridge/evidence/pass03/05.03.packed-snapshot.md` | Named path is not a file or directory at the inventory commit.

### `00.kernel/00.00.10.work/0503.worker-bridge/05.04.md`

- Return source `98dbf8b490e438fb95ba65b61b4d88ece8d083a0c9a1f6b146de5ee2fe3ed779` | 14697. Classification `return-and-review`. Prime review in the file: `true`.
- Reason: The page has a return body, and the whole file would be the return source. The payload is not proposed as complete because named evidence is missing or a named directory exceeds the expansion bound.
- Withheld:
- `00.kernel/00.00.10.work/0503.worker-bridge/fixtures/worker_fixture.py` | Named path is not a file or directory at the inventory commit.

### `00.kernel/00.00.10.work/0504.app-entry/05.01.md`

- Return source `56b043010b09bed02b8eba249b539ca4aedfd33652453637c9eafc850c20fbe5` | 20769. Classification `return-and-review`. Prime review in the file: `true`.
- Reason: The page has a return body, and the whole file would be the return source. The payload is not proposed as complete because named evidence is missing or a named directory exceeds the expansion bound.
- Withheld:
- `labs/worker-bridge-pass01` | 170 files | Named directory has 170 files. This plan does not expand directories above 12 files, and it does not expand the historical returns root.

### `00.kernel/00.00.10.work/0504.app-entry/05.04.md`

- Return source `96535f9f05c08c97ed750f4a80834d7454d03ec1487aad74550ddf5aaf20ebc9` | 15615. Classification `return-and-review`. Prime review in the file: `true`.
- Reason: The page has a return body, and the whole file would be the return source. The payload is not proposed as complete because named evidence is missing or a named directory exceeds the expansion bound.
- Withheld:
- `00.kernel/00.00.10.work/0504.app-entry/evidence/05.04` | 26 files | Named directory has 26 files. This plan does not expand directories above 12 files, and it does not expand the historical returns root.

### `00.kernel/00.00.10.work/0504.app-entry/05.05.md`

- Return source `5a52d9e9905faf2cbb36e4b0d70e701fbab55b63faccb8617ed8e507341c5d6f` | 17442. Classification `return-and-review`. Prime review in the file: `true`.
- Reason: The page has a return body, and the whole file would be the return source. The payload is not proposed as complete because named evidence is missing or a named directory exceeds the expansion bound.
- Withheld:
- `labs/clerk-handoff-pass02` | 21 files | Named directory has 21 files. This plan does not expand directories above 12 files, and it does not expand the historical returns root.
- `labs/worker-bridge-pass01` | 170 files | Named directory has 170 files. This plan does not expand directories above 12 files, and it does not expand the historical returns root.
- `00.kernel/00.00.10.work/0504.app-entry/evidence/05.05/demo` | 16 files | Named directory has 16 files. This plan does not expand directories above 12 files, and it does not expand the historical returns root.

### `00.kernel/00.00.10.work/0504.app-entry/05.07.md`

- Return source `246153bcaa86b2b3e056ae84263899a99dc39e011b54e4ed3f588334330fe8e7` | 9634. Classification `return-and-review`. Prime review in the file: `true`.
- Reason: The page has a return body, and the whole file would be the return source. The payload is not proposed as complete because named evidence is missing or a named directory exceeds the expansion bound.
- Withheld:
- `00.kernel/00.00.10.work/0504.app-entry/evidence/pack-check05.07` | 29 files | Named directory has 29 files. This plan does not expand directories above 12 files, and it does not expand the historical returns root.

### `00.kernel/00.00.10.work/0506.clerk-handoff/05.01.md`

- Return source `7c68b7d4095aeec9563b0ccdbdd73d4050c4d31817efbf148fa25e4a223861e6` | 11307. Classification `return-and-review`. Prime review in the file: `true`.
- Reason: The page has a return body, and the whole file would be the return source. The payload is not proposed as complete because named evidence is missing or a named directory exceeds the expansion bound.
- Withheld:
- `labs/clerk-handoff-pass02` | 21 files | Named directory has 21 files. This plan does not expand directories above 12 files, and it does not expand the historical returns root.
- `00.kernel/00.00.10.work/0506.clerk-handoff/evidence/SHA256SUMS.txt` | Named path is not a file or directory at the inventory commit.
- `00.kernel/00.00.10.work/0506.clerk-handoff/evidence/tests-fail-01.txt` | Named path is not a file or directory at the inventory commit.

### `00.kernel/00.00.10.work/0506.clerk-handoff/05.02.md`

- Return source `395cb773b6bf5a6551704be88b80d0f355b86e6a43fa12ebc072887f42f1543d` | 10408. Classification `return-and-review`. Prime review in the file: `true`.
- Reason: The page has a return body, and the whole file would be the return source. The payload is not proposed as complete because named evidence is missing or a named directory exceeds the expansion bound.
- Withheld:
- `labs/clerk-handoff-pass02` | 21 files | Named directory has 21 files. This plan does not expand directories above 12 files, and it does not expand the historical returns root.
- `00.kernel/00.00.10.work/0506.clerk-handoff/evidence/SHA256SUMS.pass02.txt` | Named path is not a file or directory at the inventory commit.
- `00.kernel/00.00.10.work/0506.clerk-handoff/evidence/colab-review05.02` | Named path is not a file or directory at the inventory commit.
- `00.kernel/00.00.10.work/0506.clerk-handoff/evidence/SHA256SUMS.txt` | Named path is not a file or directory at the inventory commit.

### `00.kernel/00.00.10.work/0506.clerk-handoff/05.03.md`

- Return source `59468d0976229899136f0120df3315583de65a79e4e06d8ec5bcd3b94cce50dd` | 14383. Classification `return-and-review`. Prime review in the file: `true`.
- Reason: The page has a return body, and the whole file would be the return source. The payload is not proposed as complete because named evidence is missing or a named directory exceeds the expansion bound.
- Withheld:
- `00.kernel/00.00.10.work/0506.clerk-handoff/evidence/pack05.03/inputs` | 15 files | Named directory has 15 files. This plan does not expand directories above 12 files, and it does not expand the historical returns root.
- `app/clerk_seam.py` | Named path is not a file or directory at the inventory commit.
- `app/clerk-seam.json` | Named path is not a file or directory at the inventory commit.
- `app/tests/test_clerk_seam.py` | Named path is not a file or directory at the inventory commit.

### `00.kernel/00.00.10.work/0506.clerk-handoff/05.04.md`

- Return source `0e28bfc80cc7e8d3f6f39e1a7c1b95aad83062ad5955f4e19c0d881262a1dacb` | 18559. Classification `return-and-review`. Prime review in the file: `true`.
- Reason: The page has a return body, and the whole file would be the return source. The payload is not proposed as complete because named evidence is missing or a named directory exceeds the expansion bound.
- Withheld:
- `00.kernel/00.00.10.work/0506.clerk-handoff/evidence/colab-review05.04` | 13 files | Named directory has 13 files. This plan does not expand directories above 12 files, and it does not expand the historical returns root.
- `labs/clerk-handoff-pass02` | 21 files | Named directory has 21 files. This plan does not expand directories above 12 files, and it does not expand the historical returns root.
- `00.kernel/00.00.10.work/0506.clerk-handoff/evidence/inspection05.04` | 19 files | Named directory has 19 files. This plan does not expand directories above 12 files, and it does not expand the historical returns root.
- `00.kernel/00.00.10.work/0506.clerk-handoff/evidence/inspection05.04/examples` | 13 files | Named directory has 13 files. This plan does not expand directories above 12 files, and it does not expand the historical returns root.
- `00.kernel/00.00.10.work/0506.clerk-handoff/evidence/SHA256SUMS.pass03.txt` | Named path is not a file or directory at the inventory commit.
- `00.kernel/00.00.10.work/0506.clerk-handoff/evidence/SHA256SUMS.txt` | Named path is not a file or directory at the inventory commit.

### `00.kernel/00.00.10.work/0506.clerk-handoff/05.05.md`

- Return source `d4828b1b8ec3d65ed96de6b4018c64dac035b951cebf5c4178184841de2dae58` | 8288. Classification `return-and-review`. Prime review in the file: `true`.
- Reason: The page has a return body, and the whole file would be the return source. The payload is not proposed as complete because named evidence is missing or a named directory exceeds the expansion bound.
- Withheld:
- `00.kernel/00.00.10.work/0506.clerk-handoff/evidence/colab-review05.04` | 13 files | Named directory has 13 files. This plan does not expand directories above 12 files, and it does not expand the historical returns root.

### `00.kernel/00.00.10.work/0506.clerk-handoff/05.06.md`

- Return source `e8762ea29d92a9bbca3fcf3dfceec8a3249c38cab0d61cfb03065726da62f4e0` | 11394. Classification `return-and-review`. Prime review in the file: `true`.
- Reason: The page has a return body, and the whole file would be the return source. The payload is not proposed as complete because named evidence is missing or a named directory exceeds the expansion bound.
- Withheld:
- `labs/clerk-handoff-pass02` | 21 files | Named directory has 21 files. This plan does not expand directories above 12 files, and it does not expand the historical returns root.
- `00.kernel/00.00.10.work/0506.clerk-handoff/evidence/identity05.06` | 15 files | Named directory has 15 files. This plan does not expand directories above 12 files, and it does not expand the historical returns root.
- `00.kernel/00.00.10.work/0506.clerk-handoff/evidence/SHA256SUMS.pass04.txt` | Named path is not a file or directory at the inventory commit.

### `00.kernel/00.00.10.work/0507.prime-support/05.02.md`

- Return source `1968ac637db71dfeae3734cfbbd02dd402b741956a2c4ac549001e379a0cc76b` | 13411. Classification `return-and-review`. Prime review in the file: `true`.
- Reason: The page has a return body, and the whole file would be the return source. The payload is not proposed as complete because named evidence is missing or a named directory exceeds the expansion bound.
- Withheld:
- `00.kernel/00.00.10.work/0507.prime-support/evidence/build05.02` | 16 files | Named directory has 16 files. This plan does not expand directories above 12 files, and it does not expand the historical returns root.
- `returns/sof-gm-kit-pass01.md` | Named path is not a file or directory at the inventory commit.

### `00.kernel/00.00.10.work/0507.prime-support/05.03.md`

- Return source `9585247bff03bb8f9b3743571cb7d4d6e1b15d6246b676d8ae8e7ad524bcdf24` | 10927. Classification `return-and-review`. Prime review in the file: `true`.
- Reason: The page has a return body, and the whole file would be the return source. The payload is not proposed as complete because named evidence is missing or a named directory exceeds the expansion bound.
- Withheld:
- `00.kernel/00.00.10.work/0507.prime-support/evidence/repair05.03` | 19 files | Named directory has 19 files. This plan does not expand directories above 12 files, and it does not expand the historical returns root.

### `00.kernel/00.00.10.work/0508.return-capture/05.01.md`

- Return source `9da830f28f340fb6142a12908e8d60a3b5050cc8ff075d32405133f39853d472` | 18493. Classification `return-and-review`. Prime review in the file: `true`.
- Reason: The page has a return body, and the whole file would be the return source. The payload is not proposed as complete because named evidence is missing or a named directory exceeds the expansion bound.
- Withheld:
- `returns` | 15 files | Named directory has 15 files. This plan does not expand directories above 12 files, and it does not expand the historical returns root.
- `00.kernel/00.00.10.work/0508.return-capture/evidence/build05.01` | 15 files | Named directory has 15 files. This plan does not expand directories above 12 files, and it does not expand the historical returns root.
- `returns/01.md` | Named path is not a file or directory at the inventory commit.

### `00.kernel/00.00.10.work/0509.pack-assembly/05.01.md`

- Return source `9545b7457a0e37fbcd3efeec2a379fcef6e4a02e2c41558a18673a7b14ae89a7` | 10398. Classification `return-and-review`. Prime review in the file: `true`.
- Reason: The page has a return body, and the whole file would be the return source. The payload is not proposed as complete because named evidence is missing or a named directory exceeds the expansion bound.
- Withheld:
- `00.kernel/00.00.10.work/0509.pack-assembly/evidence/build05.01` | 27 files | Named directory has 27 files. This plan does not expand directories above 12 files, and it does not expand the historical returns root.

### Root proposal left unresolved

- Origin book: `00.00.10.work`.
- Page: `returns/clerk-handoff-proposal-claude-2026-10-27.md`.
- Batch: `none (root return)`.
- Source commit: `75ae515d826482113c4126274d015de112aa249b`.
- Return source: `returns/clerk-handoff-proposal-claude-2026-10-27.md` | `3795eb572e2b6ed3411a1026d005f20d719a71fbd607f4083f1f100d726acb97` | 9445.
- Prime review already in the return source: `false`.
- Retrospective: `true`.
- Classification: `historical-root-proposal`.
- Scope: Retrospective custody of these exact bytes at the inventory commit. The return file is stored whole. Embedded Director replies and a Review heading stay inside that file. This plan does not allocate a member, does not claim a standalone reproduction, and does not accept the work.
- Reason: The file is a proposal at the historical returns root. It has no Return heading. This plan does not decide that it is a completed return.

`returns/sof-gm-kit-pass01.md` is named by `0507.prime-support/05.02.md` and is absent at this commit. It is not invented. SoF stays outside this book's backfill.

## Recommended next batch

One page only: `00.kernel/00.00.10.work/0505.observer-design/05.01.md`.

It is a draft. The return body opens with the draft layout in `01.md` section 1, the review shape `templates/review-record.md`, the draft role `templates/role-observer.md`, and decisions D1–D5. It names a future 0066 only if that role is approved and checked. The same file later records a historical proposal outcome. There is no Review heading, so `includes_prime_review` is false, and the whole file stays unsplit. Five payloads close the named set. No member number is assigned. Approving this recommendation is a separate decision from this plan's receipt.

The other two proposed batch pages are closed sets and are larger: `0502.workflow-start/05.01.md` has 28 payloads, and `0504.app-entry/05.03.md` has 19. They wait behind the observer draft. Pack A (3 companions) and Pack B (9 companions) are a separate historical slice.

## Limits

- The live door `0100.band.returns/01.md` is `e0f3abc3eeb4afcf23e2515126ea18f459c7258b2432746ae3479444d495d868` (3435). The supplied snapshot remains `9d9efcd2f5bfbb5b4f44789303e27025ebbba6ffc5c281a2120fb5e7cb24cff5` (2844). The door was not edited.
- HEAD at the note was `acc3831f9560c86d4c000b84e9f026ca0570207b` on `workshop`. No shared commit or push.
- Rollout publication commit `086da87a07978413d810d3663d98df10d2a4bda3` is not the inventory commit.
- The expansion bound of 12 is this plan's rule. It is not a claim that a larger directory is unknowable.
- An earlier scanner joined book-relative paths onto the filename. That scan is discarded.
- No new capture code. The helper remains `8f3da5c651f6924fca6dedb0b95da7d181eb58884dc030dd9cbc3d8b6a5b15ac` (45767).
- No mass backfill, no second reserve, no edit to historical pages, furniture, pack snapshots, or other members.
