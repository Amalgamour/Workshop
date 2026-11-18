# Integration plan — guarded legacy writer

Schema: `return-capture-guard-integration/0508`
Date: 2026-11-02. Executor: Grok-2. Reviewer: Codex Prime.
This plan is not activation, not an app edit, and not a live migration.

## Status

`labs/return-capture-guard-pass01` is built and proved on disposable copies. It is not selected by the app. The current app is unprotected. Grok-1 owns the current app integration. This build did not edit `app/librarian.py`, `README`, the live handoff, boot, or batch facades, registrations, the current assignment, or `00.live`. It did not open those live facades as a design source. The inventory below is the pack snapshots plus the sealed lab files.

A declared layout changes the supported route once a caller selects this guard. It does not confine a historical script. The official copy proved that: the unchanged `return_capture.py`, run directly, still reserved on a declared disposable book.

## Measured identities in this build

| Identity | Path | sha256 | bytes | Role |
| --- | --- | --- | --- | --- |
| Guarded successor | `labs/return-capture-guard-pass01/return_capture_guard.py` | `ca2707845a033901053620c70512a0a6a5ebf52d1b3069704aae8a93e17c7b2a` | 8931 | Reserve and capture classify the layout. Verify forwards. |
| Selected caller | `labs/return-capture-guard-pass01/harness.py` | `9e6b60601cf7646e21c2d53b98e79a582679c89a47b711f7012e7cb6791b334f` | 2362 | The only selector in this build. |
| Disposable proof | `labs/return-capture-guard-pass01/tests/run_suite.py` | `280a6d1a54b52e725eb514fdefa58c0f5044d415f818a53f6c6f761040d0606c` | 20273 | Official suite. |
| Unit seams | `labs/return-capture-guard-pass01/tests/test_guard.py` | `0c3c872d611526e1d857f202f7ced715a7087b160746140fe6f12a31784b1e8d` | 5431 | Writer-not-started proof. |

No hash below is a guess of a file that does not exist.

## API the later caller must keep

Commands are `reserve`, `capture`, and `verify`, with the same flags as `labs/return-capture-pass01/return_capture.py`. There is no `--force`, no `--allow-live`, and no sentinel.

An absent `return-line-layout.json` delegates to the pinned writer and appends: an undeclared book has not gained line-pass protection. An exact accepted `return-line-layout/1` declaration refuses reserve and capture before the writer module is executed. Exit 2. `writer_started: false`. `sequential_allocation: not-used`. `result refused`. The correction names the line-pass route. A linked, malformed, or conflicting layout is `state: attention` and does not allocate. Verify still calls the pinned writer, including on a declared book. A pin mismatch refuses before either module is executed.

## Three kinds of caller

Selected runtime caller, this build only: `harness.py`. It pin-checks sealed `handoff.py`, leaves `TOOL_FILES` unchanged, and for a launch whose first argument is `capture` passes the guard path. Inspect and verify keep the packed paths. The official perform returned `result attention`, wrote `clerk-capture-handoff-failure/1`, and the log contains the guard lines `result refused` and `writer_started: false`. The retry kept the log.

Historical fixtures, unchanged and not selected:

| Fixture | sha256 | bytes | What it still does |
| --- | --- | --- | --- |
| `labs/capture-handoff-pass01/demo.py` | `b3b3bb24db34199c8841c46bbf4942bd9f3b0b6b77ed95ccf8b2d6a33681695b` | 7376 | Calls the historical reserve. |
| `labs/capture-flow-rehearsal-pass01/rehearse.py` | `4a92e5d1914ecc9e9b2b6d51099d7caf5441024b83c3aaa5d085811c6caf088e` | 45513 | Calls the historical reserve. |
| `labs/capture-handoff-pass01/handoff.py` | `a8380136a84469b8975b38f084a4d34802ccf079ed69cf85d107f6ca3643426a` | 51828 | Packed capture path is the historical writer. |
| `labs/return-capture-pass01/return_capture.py` | `8f3da5c651f6924fca6dedb0b95da7d181eb58884dc030dd9cbc3d8b6a5b15ac` | 45767 | Direct reserve and capture remain runnable. |

Sealed evidence: `evidence/pack05.08/source-manifest.json` sha256 `aa64824019e45f388a703530fb22708bb405f6ae13c499ab8753e61485c7af20`, 8226 bytes, 24 files. The manifest keeps its 150 CR bytes. Snapshots under `evidence/pack05.08/sources/` are the inventory for the app doors. They are not a license to edit the live doors.

## Later write edges

These edges still send a capture or a reserve to the historical writer. A later reviewed change selects the guard there. This plan does not perform that change.

1. Sealed handoff capture launch. File `labs/capture-handoff-pass01/handoff.py`, sha256 `a8380136a84469b8975b38f084a4d34802ccf079ed69cf85d107f6ca3643426a`, 51828 bytes. `TOOL_FILES["capture"]` is `labs/return-capture-pass01/return_capture.py` at `8f3da5c651f6924fca6dedb0b95da7d181eb58884dc030dd9cbc3d8b6a5b15ac`. `execute` calls `launch(pins["capture"][0], capture_command(parsed), pins)`. `check_pins` requires that capture path, the inspect path, and `labs/clerk-handoff-pass02/clerk.py` at `f697a7e443117c3d1face62d3021f7634154d76214b77fadec1a5cc3c99d394c`, 52279 bytes. The clerk file is outside the pack manifest. It was hashed and not edited. Later work writes a new handoff module. It does not edit this sealed file and it does not change `TOOL_FILES` to force a successful capture. After `check_pins`, a capture launch uses `labs/return-capture-guard-pass01/return_capture_guard.py` at the measured hash above. Inspect and verify keep the packed historical paths. The measured pattern is `harness.py`.

2. App capture door. Snapshot `app/handoff_tools.py`, sha256 `f1d76a517b64a82ff8e348b811a5c59dfe8870385e6737b67878e0749e705bc2`, 9901 bytes. Schema `librarian-capture-handoff`. `DECLARATION_NAME` is `capture-handoff.json`. `perform` pins the four tools and launches `handoff.py`. It does not reserve. `TOOLS["return_capture"]` is the historical writer at `8f3da5c651f6924fca6dedb0b95da7d181eb58884dc030dd9cbc3d8b6a5b15ac`. `TOOLS["handoff"]` is the sealed handoff at `a8380136a84469b8975b38f084a4d34802ccf079ed69cf85d107f6ca3643426a`. `OVERRIDE_FLAGS` includes `--capture` and `--inspect`. The pack snapshot does not contain `capture-handoff.json`, so this plan does not state its hash. Later work, with Grok-1, adds a new facade and a new declaration that select the new handoff module. It does not edit the current facade in place as part of this pack. It does not add `--force`.

3. Historical reserve demos. `demo.py` and `labs/capture-flow-rehearsal-pass01/rehearse.py` stay historical fixtures. A later supported reserve demonstration is a new file that calls the guard. Those two files are not edited to make the old route disappear.

## Edges that stay

| Edge | sha256 | bytes | Later action for this closure |
| --- | --- | --- | --- |
| `labs/return-capture-pass01/return_inspect.py` | `947915febaa5918f56b6be03c81840c030d081fcab9a3bead2cd660973a9999b` | 11402 | Keep. It loads the sibling writer by hash `8f3da5c6...`. Inspect does not allocate. |
| `labs/return-access-pass01/return_access.py` | `501d40d7c7b08720d3ae061441284ac26d544e7b80100059b2ddce25f67358f5` | 26561 | Keep. It pins pass03 and the same reader hash. It does not reserve. |
| Snapshot `app/boot_tools.py` | `409901b1f18027b8b42a582cb14c0add82a4f5422aec9f66cda2e7a9efc2deac` | 9601 | Keep for this closure. Schema `librarian-prime-boot`. Declaration name `prime-boot.json`, hash not in the pack snapshot and not guessed. Commands are `boot-prepare`, `boot-check`, `boot-judge`, `boot-show`. It launches `prime_boot`. The return helper and inspector are sibling pins. It does not call reserve. |
| Snapshot `app/batch_tools.py` | `555cd07daf778f9faaa95fcb5ccdcf0653c9118252a203c748c171f244e0a8be` | 11299 | Keep for this closure. Schema `librarian-batch-observer`. Declaration name `batch-observer.json`, hash not in the pack snapshot and not guessed. It launches `batch_observe`. The return helper and inspector are sibling pins. It does not call reserve. |
| `labs/return-lines-pass04/return_lines.py` | `708443c5b3af457f930e8751be4224234d1494f2a2b4e18e3cf08bd7a7af1df6` | 12124 | Stays the reviewed line-pass writer. Selecting it in the app is a separate adapter, as `06.13` recorded. This plan does not do that. |
| `labs/return-lines-pass01/return_lines.py` | `863968c59974d85910626ba5e80cf49f14a3186c8d33b855efe00bf6ccec378a` | 100897 | Stays the layout-rule pin. |

Sibling reader pin: this successor does not require a change to `return_inspect.py` or `return_access.py`. Both keep helper pin `8f3da5c651f6924fca6dedb0b95da7d181eb58884dc030dd9cbc3d8b6a5b15ac` because verify and inspect still execute that file. The dependency appears only if a later change replaces `return_capture.py` in place. That replacement is forbidden. Write callers change their capture launch path to the guard and leave the sibling pin.

## Proposed identities that do not exist yet

These names are the later integration targets. They were not created. No pin is measured for them.

| Proposed identity | Path to create later | Measured pin |
| --- | --- | --- |
| Handoff successor | `labs/capture-handoff-guard-pass01/handoff.py` | unmeasured |
| App facade successor | a new module beside `app/handoff_tools.py` | unmeasured |
| App declaration | `capture-handoff-guard.json` beside the current declaration | unmeasured |

The helper identity and the caller identity that do exist are the two measured rows at the top of this plan.

## What the later change must prove before any live release

The new handoff successor and the new app facade select the guard for capture on a declared book. Reserve demonstrations that are supported callers do the same. Verify and inspect still use the historical helper. An old completed receipt stays byte-identical and readable. A repeated reserve and a pre-existing unfinished member are refused before the historical writer starts. An undeclared book still receives the sentence that it has not gained line-pass protection. No sentinel is installed. Sealed history is not repinned. Pass04 app selection remains the separate adapter from `06.13`. `06.14` still requires one combined copy cycle before a Director live release. This plan is not that release.

## Compatibility

An undeclared disposable book keeps the historical reserve and capture results, plus the protection sentence. A completed legacy member stays verifiable after a later declaration. Declaration does not rewrite old receipt bytes. Malformed, linked, and conflicting layouts do not fall back to sequential allocation. Folder names are not a declaration. The live book had no layout file during this build, so it is undeclared. Pointing reserve or capture at it would delegate to the historical writer. This build did not do that.
