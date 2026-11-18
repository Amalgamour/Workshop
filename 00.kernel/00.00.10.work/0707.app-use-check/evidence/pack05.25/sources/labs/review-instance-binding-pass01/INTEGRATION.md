# Integration interface - review-instance-binding pass01

Unselected. 0522/05.16, note 06.34. This file describes the later composition point. It does not select a dispatcher.

## Call order on one workbook chain

1. `n5_instance_hold(stored, live, book)` from labs/review-instance-binding-pass01/workbook.py. A returned dict means N5 current applicability is held. `source_changed` returns true before row equality can clear it.
2. The N7-local book check in labs/n7-local-lifecycle-pass01/workbook.py, for `live["kind"] == "N7NN"` only. This pack does not rebuild that check.
3. pass02 `source_changed` row comparison, including its own-write exception for a publication this journal recorded.

A later overlay replaces `p2.source_changed` with a function that calls these three in that order. Pass05 `build_intake` and `parse_pointer` stay installed for the strict N7 grammar. The N7-local exchange stays its own wrapper around `build_intake`. The two wrappers compose by nesting, each calling the captured predecessor.

## Root contract

The workbook and the door each refuse to start unless the running file's resolved path is their canonical path under D:\Git\lib-build. That check happens before the pass05 pin read. There is no lab root adapter and no second REPO value. A copied file with the same bytes still fails that check.

The door's `perform(args, code_root)` resolves the declaration and tool pins under the supplied code root. `main()` supplies only D:\Git\lib-build. A test root can therefore refuse a missing, retargeted, or tampered pin without editing the canonical files.

## App candidate

candidate/app/librarian.py is a byte copy of app/librarian.py with the review-loop branch pointed at labs/review-instance-binding-pass01/review_loop_tools.py and with code_root set to D:\Git\lib-build for that command only. Executing that file runs this door. It is not selected. app/librarian.py stays on review_loop_tools_v7.py, sha256 c3a5be3b612c021d95effaa5da4a151bf89026422b94f4cad98331014c7f0cd9, 12204 bytes.

Rollback: leave app/librarian.py at that hash. Leave this lab on disk, inert.

## Minimum selection patch, not applied

When Prime composes one dispatcher, the review-loop load in app/librarian.py names the composed door, and that door's workbook pin names the composed workbook. The composed workbook calls `n5_instance_hold` and the accepted N7-local check and the accepted pass05 parser. This pack does not write that composition and does not edit app/librarian.py.

## Limits

form does not carry `instance_applicability`, stale, or the judgment. prepare, inspect, read, recover, publish, and the record repin guard do. `prime-guard` stays the pinned read-only Prime command. A refused record may write `failed/` on the commanded external book. recover does not write. No concurrency, power-loss, or AR-01 guarantee is added. Observation is each command's own read.
