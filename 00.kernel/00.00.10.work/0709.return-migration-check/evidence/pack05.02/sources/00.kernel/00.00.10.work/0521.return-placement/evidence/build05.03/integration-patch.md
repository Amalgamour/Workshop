# Integration patch proposal — not applied

Date: 2026-10-31. Batch: 0521.return-placement/05.03. Executor: Grok-1.
This file is a proposal. No listed file was edited. Live enforcement is pending.
Prime applies this only after both parallel lanes freeze. Grok-2 still relies on the hashes below.

A book with `return-line-layout.json` of schema `return-line-layout/1` stops sending new work to the sequential allocator. Historical `return-capture/1` reads stay. A book without that declaration keeps today's reads and the current allocator until Prime retires it. This new tool being present does not enforce the current book.

## Measured pins, unchanged

| path | sha256 | bytes | current write |
| --- | --- | --- | --- |
| labs/return-capture-pass01/return_capture.py | 8f3da5c651f6924fca6dedb0b95da7d181eb58884dc030dd9cbc3d8b6a5b15ac | 45767 | `reserve` at line 608, parser at line 1198, dispatch `return reserve(` at line 1234 |
| labs/return-capture-pass01/return_inspect.py | 947915febaa5918f56b6be03c81840c030d081fcab9a3bead2cd660973a9999b | 11402 | reads a historical member |
| labs/return-placement-pass01/return_placement.py | db96f7023c73dcececba0e7d42b821da8193af7534a4bdf8cd2e5d6cd53d0754 | 66097 | route and read-only plan; live apply still refused |
| labs/capture-flow-rehearsal-pass01/rehearse.py | 4a92e5d1914ecc9e9b2b6d51099d7caf5441024b83c3aaa5d085811c6caf088e | 45513 | `bind` calls `reserve` through the helper CLI at line 587 |
| labs/capture-handoff-pass01/demo.py | b3b3bb24db34199c8841c46bbf4942bd9f3b0b6b77ed95ccf8b2d6a33681695b | 7376 | names the helper at line 131 |
| labs/capture-handoff-pass01/handoff.py | a8380136a84469b8975b38f084a4d34802ccf079ed69cf85d107f6ca3643426a | 51828 | pins the helper at line 76; it does not allocate |
| labs/desk-loop-replay-pass01/replay.py | 137fbae93019ed6a3b67e026ef7a54404b4483511be81422ce024667286541f1 | 31280 | `reserve` method at line 194 |
| labs/desk-app-integration-pass01/demo.py | 79db81bb1266f2de0a807da6897209cc650d44c6b10f47af1f5a2f088321c6b9 | 22157 | helper `reserve` at lines 170, 257, and 288 |
| labs/desk-app-integration-pass01/desk_lab.py | db115e77e457fca3debd9d25e4e4a34d28d50fad8413befc8053df534bde697d | 28477 | pin at line 33; printed capture command at line 390 |
| labs/colab-workflow-pass02/colab_workflow.py | 4a2ece9e646224468b36ce63947c739d8ecd73155fbb62fb34f0442cbd2dceec | 47247 | `command_place` at line 964 writes the pass tail on the source page at line 1026 |
| labs/colab-support-pass02/colab_support.py | 2b720434ac4c4331835c1484b0eca362e01e8afbecde0ab800ca392530abf68b | 53892 | `intake` at line 917 proposes the source page at line 999 |
| labs/colab-support-pass02/handoff_check.py | 7d62dde48165c5ac80f7f92a2a91f73a66b40c1e8dd2383f0269027038c6a268 | 27722 | unchanged checker; update it only if it still requires a sequential member |
| labs/prime-cycle-pass01/prime_cycle.py | 19ede9c2125307595d0be867bae1a3cb71bf3db0515ad83e7c04d3333e17861d | 77846 | helper pin at line 39; `MEMBER` is `01NN` at line 46 |
| labs/desk-state-pass01/desk_state.py | 4d924bf6549fe37b229962d4f3a81924109a879a8206ea95066f4bfde11701b4 | 55144 | helper path at line 61 |
| labs/prime-bench-pass01/prime_bench.py | a6dc98b8b6dbcaa8e080903a3ec537381e511b2b94206b259bb5c723c0696fe3 | 106951 | custody pin at line 114; printed helper command at line 1969 |
| app/batch_tools.py | 555cd07daf778f9faaa95fcb5ccdcf0653c9118252a203c748c171f244e0a8be | 11299 | helper pin at line 46 |
| app/boot_tools.py | 409901b1f18027b8b42a582cb14c0add82a4f5422aec9f66cda2e7a9efc2deac | 9601 | helper pin at line 46 |
| app/handoff_tools.py | f1d76a517b64a82ff8e348b811a5c59dfe8870385e6737b67878e0749e705bc2 | 9901 | helper pin at line 38 |

`app/librarian.py` and `app/prime_intake.py` do not name the helper path. They stay as they are in this proposal. Frozen copies under `colab/labs/`, `evidence/**`, and `0523.desk-core` stay frozen.

## Required change, later pack only

For a book whose layout says `allocation` is `line-pass` and `sequential_allocation` is false:

- New reserve, capture, verify, and lookup call `labs/return-lines-pass01/return_lines.py` or `app/return_line_tools.py`. They do not call `return_capture.py reserve`.
- Band 5 writes one `N1NN.subject` line and a `05.NN` tail. A second pass does not take another page number.
- Band 7 writes the tail on that same page.
- Any other band is refused. No route is invented.
- The descriptor emitted to the next lane is `return-line-descriptor/1` with the keys in `0417.return-placement/evidence/integration-seam-v1.md`.
- `command_place` and `intake` stop proposing the source page as the custody file. They pass the origin page and batch to this tool and write only where the route says.
- `prime_cycle.py` keeps reading a historical `01NN.slug` member until that member is retired, and reads new work from `{target_page}/{batch}.custody`.
- Printed commands in `desk_lab.py`, `demo.py`, and `prime_bench.py` name the line tool for a declaring book.
- App doors gain the `return_lines` pin beside the existing helper pin. Their helper pin stays until the helper itself changes. This proposal does not change the helper.

Old-format reads that must keep working:

- `verify_member` on an untouched `01NN.slug` directory.
- `return_inspect.py` on that same directory.
- A relocated package is not renamed into `return-capture/1` and is not passed to `verify_member` under the new folder name. Its backup copy keeps the original directory name. `relocation.json` says `reservation_destination_rewritten` is false.

## Tests the later pack runs

- A declaring fixture: two `05.NN` passes on `0504.app-entry` land on one `0104.app-entry`, and `reserve` of the helper is not called.
- `0701` and `1701` stay page-local. `0201`, `0301`, `0401`, `0601`, and `1201` are refused.
- A book without the layout can still read an existing `return-capture/1` member.
- The helper hash stays `8f3da5c6…` / 45767 unless that same pack is the one that changes it and updates every pin in the same change.
- No fixture inventory, bridge, or race suite from the held AR-01 work is revived here.

## Order

1. Prime reviews evidence/build05.03/migration-plan.json. `live_moves` false is not permission to move.
2. Prime applies this caller patch after both lanes freeze, then re-measures every pin in the table.
3. A separate accepted run stages the live book from the lowest capture, retires an occupant only after that backup verifies, and does not delete the only copy.
4. After `0121.archive-resolution-0508` is migrated and Prime accepts that retirement, this batch may be filed on `0121.return-placement`.
5. `0184` is not a destination at any step.
