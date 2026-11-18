# Selection — measured pins for Prime

Schema: `return-access-handoff-selection/0509`
Date: 2026-11-02. Executor: Grok-2. Reviewer: Codex Prime.
This file records measured pins after the official suite. It does not revise `DELTA.md`. It does not select the app.

## Two substitutions

After Grok-1's review-loop return, and after Prime review of this build, Prime measures the then-current dispatcher and applies only these load-path substitutions:

1. In the `return-lines` branch, replace `parent / "return_line_tools_v2.py"` with `parent / "return_line_tools_v3.py"`.
2. In the `capture-return` branch, replace `parent / "handoff_tools.py"` with `parent / "handoff_tools_v2.py"`.

The replacement is those two path strings plus the additive sentences below. It is not a wholesale dispatcher. `authoring` stays on `authoring_tools_v2.py`. `review-loop` stays on the successor Grok-1 returns. Boot and batch stay on their current helper pins.

The fixture dispatcher used for the full-entry check lived only under `D:\librarian\temp\0521-0509\20261102T213852169046Z-suite\fixture-app\`. It was labeled FIXTURE. It was not copied onto `app/librarian.py`.

The pre-Grok-1 snapshot is `00.kernel/00.00.10.work/0522.review-construction/evidence/pack05.11/sources/app/librarian.py`, sha256 `826167161000ac3eab78c466ae47e31b37ff435ea33f4104caf7651ecd21436e`, 12153 bytes.

Live `app/librarian.py` at the claim and again at this close: sha256 `e2d85b1b641d8a1113b0afaa67a9b8203eb58e9f1028308be922a806fffa5f90`, 12204 bytes. It still differs from the snapshot. This build did not edit it.

Live `app/README.md` at the claim: sha256 `7a5b94ff6732e0a49fd712ea447608d7407e85dfa5eeb5d290f12fbeb736fd54`, 6877 bytes. At this close: sha256 `d30d68d47cf90475f7f4b7abe9215c3ad2b323535494e2000bfc306f302f6c16`, 38352 bytes. This build did not edit README and did not read it. Prime remeasures README at selection time. The sentences below are proposed text. They are not a patch against the current README.

## Additive documentation

Prime may add these sentences when applying the two substitutions. This build did not apply them.

`return-lines` forwards status, lookup, and verify to `app/return_line_tools_v3.py`. Writes go to the pinned pass04 door. Reserve and capture also require the band door and the exact line-pass layout.

`capture-return` forwards one absolute binding to `app/handoff_tools_v2.py`. That facade pin-checks `labs/capture-handoff-guard-pass01/handoff.py` and the reviewed guard before launch. The sealed handoff remains directly runnable.

## Measured successor pins

| Piece | Path | sha256 | bytes |
| --- | --- | --- | --- |
| Return-access successor | `labs/return-access-pass02/return_access.py` | `f5a62ecb90d1a2ce8739df92e7df2e399057b3c1a059ae66ce8368d3c8abb5a8` | 27831 |
| Return-access note | `labs/return-access-pass02/README.md` | `59594bb07cddf7e3512c21eb2b314d699e834bc7644db4fe160611fd43af5438` | 471 |
| Return-lines facade | `app/return_line_tools_v3.py` | `8ae3e6f9281667502a5a3573e32234391880a4d8c49033d47c112651b2070616` | 13435 |
| Return-lines declaration | `app/return-lines-v3.json` | `2e182bd0681cd04b1874fba029da2eab0ebdbe00d98280004303ea7ba69a23c3` | 1878 |
| Guarded handoff | `labs/capture-handoff-guard-pass01/handoff.py` | `1b2e76915965d3a48bf158e01c96057e72bddf1cfa3b7c9abd53efa4a76b13c5` | 7851 |
| Guarded handoff note | `labs/capture-handoff-guard-pass01/README.md` | `fc1930a8c11d692e5113d98804dd45999872bb2152b78778d1a2e8d2834012fb` | 758 |
| Handoff facade | `app/handoff_tools_v2.py` | `7cd5955c74c8993401b99b581f40c152c36e858deafc56fffbc603aade3a8f54` | 10962 |
| Handoff declaration | `app/capture-handoff-v2.json` | `dacbfcb4d2290d51ae7976359d755e7a7a42fccd85bf3013052457d2801c7643` | 1410 |
| Combined suite | `labs/return-access-pass02/tests/run_suite.py` | `1f0739bde1b592993e6d90f1c0a4aebdcc735ec92881ccf95d00711c17e14eb1` | 50049 |

## Dependency closure

Prime remeasures these bytes at selection time. A mismatch stops the selection. This build does not silently repin.

| Role | Path | sha256 | bytes |
| --- | --- | --- | --- |
| Pass04 | `labs/return-lines-pass04/return_lines.py` | `708443c5b3af457f930e8751be4224234d1494f2a2b4e18e3cf08bd7a7af1df6` | 12124 |
| Pass03 | `labs/return-lines-pass03/return_lines.py` | `78cc4d8679bb6e54b3f2456ce777643da7a9a650ef5c79c216abd38a4c209c63` | 33349 |
| Pass02 | `labs/return-lines-pass02/return_lines.py` | `6691d0587ab97ba24a1709c9950b506961152939e2d112ee608f9dbd23e92908` | 82908 |
| Pass01 | `labs/return-lines-pass01/return_lines.py` | `863968c59974d85910626ba5e80cf49f14a3186c8d33b855efe00bf6ccec378a` | 100897 |
| Placement | `labs/return-placement-pass01/return_placement.py` | `db96f7023c73dcececba0e7d42b821da8193af7534a4bdf8cd2e5d6cd53d0754` | 66097 |
| Reader and historical writer | `labs/return-capture-pass01/return_capture.py` | `8f3da5c651f6924fca6dedb0b95da7d181eb58884dc030dd9cbc3d8b6a5b15ac` | 45767 |
| Inspector | `labs/return-capture-pass01/return_inspect.py` | `947915febaa5918f56b6be03c81840c030d081fcab9a3bead2cd660973a9999b` | 11402 |
| Reviewed guard | `labs/return-capture-guard-pass01/return_capture_guard.py` | `ca2707845a033901053620c70512a0a6a5ebf52d1b3069704aae8a93e17c7b2a` | 8931 |
| Sealed handoff | `labs/capture-handoff-pass01/handoff.py` | `a8380136a84469b8975b38f084a4d34802ccf079ed69cf85d107f6ca3643426a` | 51828 |
| Clerk | `labs/clerk-handoff-pass02/clerk.py` | `f697a7e443117c3d1face62d3021f7634154d76214b77fadec1a5cc3c99d394c` | 52279 |

Access pass01 stays `501d40d7c7b08720d3ae061441284ac26d544e7b80100059b2ddce25f67358f5`, 26561 bytes. The 05.08 harness stays `9e6b60601cf7646e21c2d53b98e79a582679c89a47b711f7012e7cb6791b334f`, 2362 bytes. This build does not select that harness.

## Not selected

accepted: false. approved: false. published: false. seated: false. committed: false. App routes are not selected. No live layout, live authority, or live root was created.
