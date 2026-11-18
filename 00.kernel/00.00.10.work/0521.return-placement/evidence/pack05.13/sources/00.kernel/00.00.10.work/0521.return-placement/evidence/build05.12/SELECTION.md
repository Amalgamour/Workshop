# Selection — two substitutions for Prime

Schema: `connected-return-review-selection/0512`
Date: 2026-11-03. Executor: Grok-2. Reviewer: Codex Prime.

This file proposes the narrow dispatcher edit. It does not apply that edit. Prime remeasures the shared files before any selection.

## Measured before identities

Live `app/librarian.py` at the pin check and again after the official run: sha256 `c3a5be3b612c021d95effaa5da4a151bf89026422b94f4cad98331014c7f0cd9`, 12204 bytes.

Live `app/README.md` at the pin check and again after the official run: sha256 `3c2125aa0cebd7ddc1604de2a823c1250edf40a8e97bd7dbd2eb09ca91155920`, 39687 bytes. This build left README unread as a document and left it unedited.

Door `0100.band.returns/01.md`: sha256 `c9ff0949c09268451a8e2a2113c1612047b374b3ecc0b3c177b6c5fd22b6842d`, 10206 bytes. Live `return-line-layout.json` stayed absent.

## Two substitutions

On a copy of the measured dispatcher, and only after Prime's review, replace these quoted loads once each:

1. `parent / "return_line_tools_v2.py"` becomes `parent / "return_line_tools_v3.py"`.
2. `parent / "handoff_tools.py"` becomes `parent / "handoff_tools_v2.py"`.

The proof copy is sha256 `b0dc477f268494a16388914a1300a4c0ee2044dae0883a5ec934165604a77de6`, 12207 bytes, at `D:\librarian\temp\0521-0512\20261103T174543190015Z\code\app\librarian.py`. Those two quoted replacements account for the whole difference from the live dispatcher. `authoring_tools_v2.py` and `review_loop_tools_v7.py` stay named. The copy was left off `app/librarian.py`.

## Additive documentation

Prime may add these sentences when applying the two substitutions. They are the proposed text already written in `evidence/build05.09/SELECTION.md`. This build left them unapplied.

`return-lines` forwards status, lookup, and verify to `app/return_line_tools_v3.py`. Writes go to the pinned pass04 door. Reserve and capture also require the band door and the exact line-pass layout.

`capture-return` forwards one absolute binding to `app/handoff_tools_v2.py`. That facade pin-checks `labs/capture-handoff-guard-pass01/handoff.py` and the reviewed guard before launch. The sealed handoff remains directly runnable.

## Tested successor pins

The copy readiness observation matched these bytes. A mismatch at Prime's remeasure stops the selection.

| Piece | Path | sha256 | bytes |
| --- | --- | --- | --- |
| Return-lines facade | `app/return_line_tools_v3.py` | `8ae3e6f9281667502a5a3573e32234391880a4d8c49033d47c112651b2070616` | 13435 |
| Return-lines declaration | `app/return-lines-v3.json` | `2e182bd0681cd04b1874fba029da2eab0ebdbe00d98280004303ea7ba69a23c3` | 1878 |
| Return-access adapter | `labs/return-access-pass02/return_access.py` | `f5a62ecb90d1a2ce8739df92e7df2e399057b3c1a059ae66ce8368d3c8abb5a8` | 27831 |
| Return-lines pass04 | `labs/return-lines-pass04/return_lines.py` | `708443c5b3af457f930e8751be4224234d1494f2a2b4e18e3cf08bd7a7af1df6` | 12124 |
| Return-lines pass03 | `labs/return-lines-pass03/return_lines.py` | `78cc4d8679bb6e54b3f2456ce777643da7a9a650ef5c79c216abd38a4c209c63` | 33349 |
| Return-lines pass02 | `labs/return-lines-pass02/return_lines.py` | `6691d0587ab97ba24a1709c9950b506961152939e2d112ee608f9dbd23e92908` | 82908 |
| Return-lines pass01 | `labs/return-lines-pass01/return_lines.py` | `863968c59974d85910626ba5e80cf49f14a3186c8d33b855efe00bf6ccec378a` | 100897 |
| Placement | `labs/return-placement-pass01/return_placement.py` | `db96f7023c73dcececba0e7d42b821da8193af7534a4bdf8cd2e5d6cd53d0754` | 66097 |
| Historical reader | `labs/return-capture-pass01/return_capture.py` | `8f3da5c651f6924fca6dedb0b95da7d181eb58884dc030dd9cbc3d8b6a5b15ac` | 45767 |
| Handoff facade | `app/handoff_tools_v2.py` | `7cd5955c74c8993401b99b581f40c152c36e858deafc56fffbc603aade3a8f54` | 10962 |
| Handoff declaration | `app/capture-handoff-v2.json` | `dacbfcb4d2290d51ae7976359d755e7a7a42fccd85bf3013052457d2801c7643` | 1410 |
| Guarded handoff | `labs/capture-handoff-guard-pass01/handoff.py` | `1b2e76915965d3a48bf158e01c96057e72bddf1cfa3b7c9abd53efa4a76b13c5` | 7851 |
| Guard | `labs/return-capture-guard-pass01/return_capture_guard.py` | `ca2707845a033901053620c70512a0a6a5ebf52d1b3069704aae8a93e17c7b2a` | 8931 |
| Clerk | `labs/clerk-handoff-pass02/clerk.py` | `f697a7e443117c3d1face62d3021f7634154d76214b77fadec1a5cc3c99d394c` | 52279 |
| Return inspect | `labs/return-capture-pass01/return_inspect.py` | `947915febaa5918f56b6be03c81840c030d081fcab9a3bead2cd660973a9999b` | 11402 |

The live selected handoff stays `labs/capture-handoff-pass01/handoff.py`, sha256 `a8380136a84469b8975b38f084a4d34802ccf079ed69cf85d107f6ca3643426a`, 51828 bytes. The live selected return-lines adapter stays `labs/return-access-pass01/return_access.py`, sha256 `501d40d7c7b08720d3ae061441284ac26d544e7b80100059b2ddce25f67358f5`, 26561 bytes. Both remain directly runnable until Prime selects the successors.

## Compatibility

The proof left the live dispatcher, README, and door page at the hashes above. The disposable book is outside `D:\Git\lib-build`. The copied review launchers still read `D:\Git\lib-build`, so the proof is tied to this checkout. Whole-file dispatcher equality, plus the two quoted strings, is the compatibility check. This file is a proposal. It is a general patching service on neither page.

## Remaining manual steps

Original captures stay in place. The live book stays undeclared. Matching custody for `0121.return-placement` stays pending. Legacy direct callers stay runnable after the two substitutions. Candidate roots `D:\librarian\return-placement\0521-staging`, `D:\librarian\return-placement\0521-backup`, and `D:\Git\lib-build\00.archive\0521.return-lines` stay uncreated.

One next action: after Prime reviews this return and the other relevant builder return, Prime remeasures the shared dispatcher and applies only the two substitutions, using inspect, a full read, and a separate publish pause.
