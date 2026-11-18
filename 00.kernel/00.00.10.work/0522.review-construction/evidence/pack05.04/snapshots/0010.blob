# Integration inventory — RP-04 still open

This file is a proposal. No pinned caller, app door, capture, or kernel page was edited. The repaired lab computes a route, plans a read-only migration, checks sealed custody, and can stage a fixture copy. That does not enforce the live book.

Pins for the callers below are the ones already recorded in evidence/build05.01/INTEGRATION.md. This pass did not change those bytes. The helper pin was checked again before this repair and still matches the pack: `labs/return-capture-pass01/return_capture.py`, sha256 8f3da5c651f6924fca6dedb0b95da7d181eb58884dc030dd9cbc3d8b6a5b15ac, 45767 bytes. `return_inspect.py` remains sha256 947915febaa5918f56b6be03c81840c030d081fcab9a3bead2cd660973a9999b, 11402 bytes. Neither file was edited.

## What this candidate implements

- Route computation for band 5 and band 7, preserving the leading workflow-space digit. `1504.app-entry` becomes `1104.app-entry`. `1702.design` stays on that page. Other bands are refused.
- A read-only plan that lists every different-name occupant of a target number, including the current 18 lines. It does not create pages.
- Fixture apply, resume, rollback, and lookup. An occupied number is staged under `staging/{old-member}/`. The final page is not created beside the occupant. Retirement is not performed.
- A read-only call to the pinned reader's `verify_member`. `complete` requires a valid sealed package and an adopted line. Acceptance stays null.

## What new-work operations are still missing

- Reserve: there is no replacement allocator. `return_capture.py reserve` is still the live allocator. This lab does not call it, and it is not retired.
- Capture: nothing in this lab writes a new live `return-capture/1` package. Historical packages are read only.
- Verify: the pinned reader is called on sources this lab is planning or rehearsing. The live doors and Prime cycle do not call this route before they treat a return as ready.
- Lookup: journal lookup works inside a fixture. `prime_cycle.py` and the app doors still open a historical `01NN.slug` member. They do not resolve `N5NN` / `N7NN` to the computed line.

## Smallest follow-up

One later pack, after Prime accepts this repair, edits the callers named in evidence/build05.01/INTEGRATION.md and updates every pin those callers hold, including the helper, in that same pack. Frozen copies under `colab/labs/` and `evidence/**/before/` stay frozen.

The rule that pack must use, which the 05.01 proposal did not yet state:

- Band 5 keeps `N`. The target is `N1NN.subject`, not a hardcoded `01NN`.
- Band 7 stays on `N7NN.subject` at any prefix.
- Before writing the final page, list every different-name directory on that number. Stage and preserve bytes. Do not overwrite the occupant and do not create a second active name. Retire a source only after Prime accepts that retirement.
- Call the pinned `verify_member` before treating a source as ready. A file copy without a valid reservation, manifest, receipt, and payload relationship is not complete. Acceptance stays null.

Callers that still have to change, at the lines already cited in the 05.01 inventory:

- `return_capture.py` `reserve` at line 608, the CLI parser at line 1198, and the dispatch at line 1233. New work in `00.00.10.work` stops entering `reserve`. Historical `/1` reads stay.
- `labs/capture-flow-rehearsal-pass01/rehearse.py` `bind` around line 588.
- `labs/capture-handoff-pass01/demo.py` around line 133. `handoff.py` does not reserve; it must accept the computed custody path.
- `labs/desk-loop-replay-pass01/replay.py` `reserve` at line 194.
- `labs/desk-app-integration-pass01/demo.py` lines 170, 257, and 288. `desk_lab.py` prints capture and verify commands and does not allocate; those printed commands must name the computed line.
- `labs/colab-workflow-pass02/colab_workflow.py` `command_place` at line 964, which writes `05.NN.return.md` on the source page.
- `labs/colab-support-pass02/colab_support.py` `intake` at line 917, whose proposed destination is still the source page.
- `labs/prime-cycle-pass01/prime_cycle.py`, which pins the helper at line 39 and accepts `01NN.slug` at line 46. It must read the receipt from the computed custody path, and keep reading a historical member until that member is retired.
- The app doors that only pin the helper. Their pins move only in the pack that changes the helper. They do not allocate today, and they do not route returns.

Until that pack lands, sequential allocation remains available and this candidate does not enforce the live workflow.

## Order after this repair

1. Prime reviews this repair and evidence/build05.02/migration-plan.json. `live_moves` false is not permission to move.
2. The caller pack above makes the corrected route mandatory and retires `reserve` for new work in this book.
3. A separate accepted run performs the live move from the lowest capture upward. Occupied lines are staged. Sources are retired only after Prime accepts that retirement.
4. After `0121.archive-resolution-0508` has been migrated and retired, this batch may be filed on `0121.return-placement`.
5. `0184` is not a destination at any step.
