# Integration proposal — make the return line mandatory

This file is a proposal. No pinned module, app door, capture, or kernel page was edited. Calling `labs/return-placement-pass01/return_placement.py` from a fixture does not enforce the live book. The route becomes mandatory only when the callers below and their pins change in one later pack.

Pins below are the digests in `0521.return-placement/evidence/pack05.01/source-manifest.json`. They matched the live files before this candidate was built. This pass does not change those bytes.

## Rule the callers must share

Origin comes from `reservation.json`, never from the folder slug.

- Band 5 (`N5NN.subject`, batch `05.NN`): tail and custody go to `01NN.subject`. Pass `05.06` and pass `05.08` of the same page are two tails on that one page.
- Band 7 (`07NN.subject`): the tails `05.NN.pack.md`, `05.NN.return.md`, and `06.NN.review.md` stay on that page. No N1NN page is allocated. Pack and review bytes are not invented. An existing return tail that matches `return.md` is verified and not rewritten. The custody directory is still required.
- Any other band, or a page or batch that is not these shapes: stop with `undeclared origin`.
- Copy `01.md`, `reservation.json`, `manifest.json`, `receipt.json`, `return.md`, and `payload/` unchanged. Add `relocation.json` (`return-placement-relocation/1`). Do not rewrite the sealed reservation destination.
- No `return.md` means the item is incomplete. `0154.colab-support-first-0501` stays incomplete.
- Do not call `return_capture.py reserve`. Do not allocate `0184`. Do not file `0121.return-placement` while any other `0121.*` directory remains.

## Live allocator

`labs/return-capture-pass01/return_capture.py`  
Pin `8f3da5c651f6924fca6dedb0b95da7d181eb58884dc030dd9cbc3d8b6a5b15ac`, 45767 bytes. Snapshot 0011.

`reserve` is defined at line 608. The CLI parser is at line 1198 and the command dispatch at line 1233. It takes the lowest free number from 0101 through 0199. The destination name is the caller's name plus that number. `occupied_numbers` treats every directory `01NN.*` as occupying `01NN`, so `0121.archive-resolution-0508` already occupies 0121.

Required change, in the follow-up pack, not here: for book `00.00.10.work`, new work stops entering `reserve`. Placement is the computed line above. `verify` and the other historical `return-capture/1` reads stay. Do not describe `reserve` as already retired. The inspector stays pinned with it:

`labs/return-capture-pass01/return_inspect.py`  
Pin `947915febaa5918f56b6be03c81840c030d081fcab9a3bead2cd660973a9999b`, 11402 bytes. Snapshot 0012.

## Callers that still reserve

These pass `reserve` to the pinned helper. Each must stop, and its pin of the helper must move in the same pack that changes the helper or the caller.

| Caller | Current call | Required change |
| --- | --- | --- |
| `labs/capture-flow-rehearsal-pass01/rehearse.py` `bind` around line 588 | `reserve` then capture | Reserve the computed line inside the fixture book. Do not take the next free number. |
| `labs/capture-handoff-pass01/demo.py` around line 133 | `reserve` for `fixture-demo` | Same. `handoff.py` does not reserve. It requires a member that is already reserved. |
| `labs/desk-loop-replay-pass01/replay.py` `reserve` at line 194 | `reserve` then capture | Pass origin `LANE` / `BATCH` through the route. The member path becomes the computed tail's custody, not the next number. |
| `labs/desk-app-integration-pass01/demo.py` lines 170, 257, and 288 | three `reserve` calls | Same, on the disposable book only. |

`labs/capture-handoff-pass01/handoff.py` pin `a8380136a84469b8975b38f084a4d34802ccf079ed69cf85d107f6ca3643426a`, 51828 bytes, snapshot 0014. It pins the helper at lines 75–80 and reads a pre-reserved member. Follow-up: accept a placed line (`01NN.subject` plus `05.NN.custody`) as the custody package, and keep accepting a historical `01NN.slug` member until that member is retired.

`labs/desk-app-integration-pass01/desk_lab.py` pins the helper at line 33 and prints `capture` / `verify` commands around lines 389–393. It does not allocate. Follow-up: those printed commands must name the computed line, and the pin moves with the helper.

## Callers that write the return on the source page

`labs/colab-workflow-pass02/colab_workflow.py`  
Pin `4a2ece9e646224468b36ce63947c739d8ecd73155fbb62fb34f0442cbd2dceec`, 47247 bytes. Snapshot 0016.

`command_place` at line 964 requires a complete sequential member, then writes the return tail with `page / return_name(pass_id)` at lines 1018–1026. `return_name` (line 353) is `05.NN.return.md` on the source page. For an N5 origin that page is the work page, which is the wrong line. For an N7 origin the page-local tail is the right file, and a matching tail must be left in place.

Required change: compute the route from the reservation origin. Band 5 writes `01NN.subject/05.NN.return.md` and `01NN.subject/05.NN.custody/`. Band 7 writes the tail only when it is absent, verifies it when the bytes match, refuses when they differ, and still writes the custody directory on that same N7 page. Record `05.NN.pack.md` and `06.NN.review.md` and do not invent those bytes. Delete the requirement that `reserve` has already chosen a member number.

`labs/colab-support-pass02/colab_support.py`  
Pin `2b720434ac4c4331835c1484b0eca362e01e8afbecde0ab800ca392530abf68b`, 53892 bytes. Snapshot 0018.

`intake` at line 917 requires `member` to match `01NN.slug`, runs the pinned helper `capture` into that member, then sets `placement.destination` to `inv["page"]` and `names["return_name"]` with action `proposed; not written` (lines 996–1004). For an N5 investigation, `inv["page"]` is the work page. That proposal is the bug. For an N7 investigation the page is already the page-local tail.

Required change: set the proposed destination from the computed route. Band 5 proposes `01NN.subject/05.NN.return.md` plus the custody directory. Band 7 proposes the existing page-local return and the custody directory, and does not propose an N1 page. Stop requiring a sequentially reserved member. `handoff_check.py` stays with it until that pack: pin `7d62dde48165c5ac80f7f92a2a91f73a66b40c1e8dd2383f0269027038c6a268`, 27722 bytes, snapshot 0019.

## Prime retrieval

`labs/prime-cycle-pass01/prime_cycle.py`  
Pin `19ede9c2125307595d0be867bae1a3cb71bf3db0515ad83e7c04d3333e17861d`, 77846 bytes. Snapshot 0022.

Line 39 pins `return_capture.py`. Line 46 accepts a member name `01NN.slug`. Later reads open that member's `receipt.json` and return bytes. It does not call `reserve`. It also does not know that `0504.app-entry` pass `05.06` lives at `0104.app-entry/05.06.return.md`.

Required change: when the registration origin is band 5 or band 7, resolve the tail and the custody directory with the same route, and read the receipt from that custody directory. When the registration still names a historical member, keep reading that `return-capture/1` directory until the accepted migration retires it. Do not treat a missing line as a new `reserve`.

## App doors

These pin the helper and do not allocate. Their pins stay valid until a follow-up edits `return_capture.py`. Editing the placement lab does not update them, and they do not enforce the new route.

| File | Pin | Bytes | Snapshot |
| --- | --- | --- | --- |
| `app/batch_tools.py` | `555cd07daf778f9faaa95fcb5ccdcf0653c9118252a203c748c171f244e0a8be` | 11299 | 0025 |
| `app/boot_tools.py` | `409901b1f18027b8b42a582cb14c0add82a4f5422aec9f66cda2e7a9efc2deac` | 9601 | 0026 |
| `app/handoff_tools.py` | `f1d76a517b64a82ff8e348b811a5c59dfe8870385e6737b67878e0749e705bc2` | 9901 | 0032 |
| `app/prime_intake.py` | `5a06c302dce4d9d6102cc11c78cb9adc961d49c9eb095e4fdd2632e49971611e` | 8501 | 0038 |
| `app/prime_review_tools.py` | `2a5a59a3fd4cbab97f078c024fc31e2fa0dd34f4aec9ce1d4ebf404961f5246f` | 10770 | 0039 |
| `app/prime_tools.py` | `4725efba6caeda1589c78a81b26e5bc4cb8b04ddefed1b1916db1a01e3e5640c` | 7800 | 0040 |
| `app/worker_bridge.py` | `29f29223f63146198be01f1a4015bb5f1a9143875a13b28db3b6dd7b117a208e` | 34532 | 0043 |
| `app/librarian.py` | `939484f152c9227482e857f9ce88eaf40649f433a57d6c9d213a07bde16baee5` | 10463 | 0033 |
| `app/clerk_seam.py` | `038962090cc2a18973fc87635625becee1719ed8f7a23ae980a58cfcb0e10159` | 31663 | 0029 |
| `app/context.py` | `5b1a31d47bb9f9b465a8492541467abbd9bd3a99ae524be7aa0dbffe2380eb9f` | 22063 | 0030 |

`app/handoff_tools.py` line 6 states that the door does not queue, claim, return, or reserve. That statement stays true. The pin at line 37 is the helper path. `batch_tools.py` and `boot_tools.py` pin the same helper near line 45.

Follow-up: when the helper's placement behavior changes, these pins and `app/README.md` (pin `4164ee218ac7e2bffdfea5bbf8c6f7b0d2a7edf01bb1dd4684d60d4e909c535d`, 26362 bytes, snapshot 0041) change in that same pack. Until then they keep verifying the current helper and they do not route returns.

## Tests that still call reserve

These are disposable-book tests. They are not the live door. They have to move with the callers or they will keep teaching the old number. Do not run them in this pass.

- `app/tests/test_handoff_tools.py` (`do_reserve`, around line 357)
- `labs/desk-state-pass01/tests/test_desk_state.py`
- `labs/colab-workflow-pass02/tests/test_real_handoff.py`
- `labs/colab-workflow-pass01/tests/test_real_handoff.py` and `tests/test_colab_workflow.py`
- `labs/colab-support-pass02/tests/test_colab_support_v2.py`
- `labs/colab-support-pass01/tests/test_colab_support.py`
- `labs/colab-readiness-pass01/tests/test_colab_readiness.py`
- `labs/state-projection-pass01/tests/test_state_projection.py`
- `labs/review-packet-pass01/tests/test_review_packet.py`
- `labs/capture-handoff-pass01/tests/test_handoff.py`
- `labs/prime-brief-pass01/tests/test_prime_brief.py`
- `labs/prime-boot-pass01/tests/test_prime_boot.py`
- `labs/batch-observation-pass01/tests/test_batch_observe.py`

Copies under `colab/labs/` and files under `evidence/**/before/` are frozen snapshots. They are not the live tools. Do not edit them to “fix” the route.

## Follow-up order

1. Prime reviews this candidate and the read-only plan. The plan has `live_moves` false. It is not permission to move.
2. One later pack edits the callers in this file and updates every pin those callers hold, including the helper pin, in the same pack. That pack is what makes the route mandatory. Landing this lab alone does not.
3. That pack retires `reserve` for new work in `00.00.10.work`. Historical `return-capture/1` reads stay available.
4. A separate accepted run performs the live move from the lowest capture upward, with the journal, the per-file checks, and rollback kept until Prime acceptance. This pass did not do that run.
5. After that move is accepted, retire `0121.archive-resolution-0508`. Only then may this batch be filed on `0121.return-placement`.
6. `0184` is not a destination at any step.
