# Contract — return access and guarded handoff

Schema: `return-access-handoff-contract/0509`
Date: 2026-11-02. Executor: Grok-2. Reviewer: Codex Prime.
This contract is written before the successors. It is not a release and not a receipt.

## Pins the successors check

| Role | Path | sha256 | bytes |
| --- | --- | --- | --- |
| Recorded-release backend | `labs/return-lines-pass04/return_lines.py` | `708443c5b3af457f930e8751be4224234d1494f2a2b4e18e3cf08bd7a7af1df6` | 12124 |
| Pass03 | `labs/return-lines-pass03/return_lines.py` | `78cc4d8679bb6e54b3f2456ce777643da7a9a650ef5c79c216abd38a4c209c63` | 33349 |
| Pass02 | `labs/return-lines-pass02/return_lines.py` | `6691d0587ab97ba24a1709c9950b506961152939e2d112ee608f9dbd23e92908` | 82908 |
| Pass01 | `labs/return-lines-pass01/return_lines.py` | `863968c59974d85910626ba5e80cf49f14a3186c8d33b855efe00bf6ccec378a` | 100897 |
| Placement | `labs/return-placement-pass01/return_placement.py` | `db96f7023c73dcececba0e7d42b821da8193af7534a4bdf8cd2e5d6cd53d0754` | 66097 |
| Historical writer and reader | `labs/return-capture-pass01/return_capture.py` | `8f3da5c651f6924fca6dedb0b95da7d181eb58884dc030dd9cbc3d8b6a5b15ac` | 45767 |
| Inspector | `labs/return-capture-pass01/return_inspect.py` | `947915febaa5918f56b6be03c81840c030d081fcab9a3bead2cd660973a9999b` | 11402 |
| Sealed handoff | `labs/capture-handoff-pass01/handoff.py` | `a8380136a84469b8975b38f084a4d34802ccf079ed69cf85d107f6ca3643426a` | 51828 |
| Clerk | `labs/clerk-handoff-pass02/clerk.py` | `f697a7e443117c3d1face62d3021f7634154d76214b77fadec1a5cc3c99d394c` | 52279 |
| Reviewed guard | `labs/return-capture-guard-pass01/return_capture_guard.py` | `ca2707845a033901053620c70512a0a6a5ebf52d1b3069704aae8a93e17c7b2a` | 8931 |

Pack inputs: `evidence/pack05.09/source-manifest.json`, 46 files, 15819 bytes, sha256 `62df066966930658c969313a75b45cd8bcba13e87eb2b5bf8687e1ca1312d3fe`. 0 mismatches at the claim. The manifest keeps its CR bytes.

The predecessor reader `labs/return-access-pass01/return_access.py` stays at `501d40d7c7b08720d3ae061441284ac26d544e7b80100059b2ddce25f67358f5`, 26561 bytes. The 05.08 harness stays at `9e6b60601cf7646e21c2d53b98e79a582679c89a47b711f7012e7cb6791b334f`, 2362 bytes. This build does not select that harness.

## Successor paths

| Piece | Path |
| --- | --- |
| Return-access successor | `labs/return-access-pass02/return_access.py` |
| Return-lines facade | `app/return_line_tools_v3.py` |
| Return-lines declaration | `app/return-lines-v3.json` |
| Guarded handoff successor | `labs/capture-handoff-guard-pass01/handoff.py` |
| Handoff facade | `app/handoff_tools_v2.py` |
| Handoff declaration | `app/capture-handoff-v2.json` |

The hashes of these six files are measured after they exist. This contract does not guess them.

## Return access

Commands: `status`, `lookup`, `verify`. Selectors stay `--book` plus one of source-and-pass, member, or submission. The outer schema stays `return-access-result/1`. Status uses `return-access-status/1`.

The loaded write backend named in the result is pass04. Lookup still reaches pass02 through pass04's loaded pass03. Native line returns, relocated legacy envelopes, and N7NN local tails keep their existing verification paths. A reader result has `task_association` `not-established`. It does not establish approval.

Authority text: canonical writes use the pass04 recorded-release validator. A synthetic fixture `return-line-authorization/1` is copy evidence. No live release exists.

Status names `legacy_writer_closure` as `supported-routes-prepared` and `app_selected` as false. The route inventory keeps the historical reserve callers and states their disposition:

| Route | Disposition |
| --- | --- |
| `return_capture.py` reserve | Historical script remains runnable. Selected closure is the reviewed guard when a caller selects that guard. |
| `labs/capture-handoff-pass01/demo.py` | Unselected historical fixture. A later supported demo would be a new file. |
| `labs/capture-flow-rehearsal-pass01/rehearse.py` | Unselected historical fixture. It stays runnable. |
| `labs/capture-handoff-pass01/handoff.py` | Prepared successor is the new handoff module. The sealed script remains directly runnable. The app has not selected the successor. |
| Boot and batch inspect | Not repinned. They stay on the old helper sibling pin. |

## Return-lines facade

Reads launch the new adapter. `preflight` and `plan` launch pass04. `preflight` requires the six authority flags and does not require a layout. `plan` requires an absolute `--out` outside the target book and outside the live book.

Writes forwarded to pass04: `init`, `reserve`, `capture`, `stage`, `stage-resume`, `reconstruct`, `reconstruct-resume`, `publish`, `publish-resume`, `retire`, `retire-resume`, `rollback-stage`, `rollback-publish`, `rollback-retire`. Each of those requires the six authority flags. `reserve` and `capture` also require a regular layout whose bytes equal pass01 `dump(layout_body(book))` for schema `return-line-layout/1`, plus the band door. A missing, linked, malformed, duplicate-key, or conflicting layout refuses before pass04 starts. The facade does not call the historical allocator.

`adopt`, `adopt-resume`, and `rollback-adopt` are forwarded so pass04 emits its own refusal.

There is no `--force`, no `--allow-live`, and no `--designate`. The facade source does not contain the pre-launch string `canonical live book is refused`. A live write still meets pass04's normal validator. This build does not create a recorded release bound to the live book. Fixture authority in the suite is copy evidence on a non-live book.

The declaration schema is `return-lines-pins/1`. Its note says canonical writes are the pass04 validator, app selection is a later file, and legacy closure is not total. The declaration lists the adapter, pass04, pass03, pass02, pass01, placement, and the reader. Changing one JSON pin without the facade constants is still insufficient; this facade changes the constants, the declaration, the status path, and the live pre-launch veto together.

## Guarded handoff

The new module loads the sealed handoff by pin. `check_pins` still requires the historical capture, inspect, and clerk paths. For a launch whose command is `capture` or `reserve`, the module substitutes the guard script after `require_guard` matches sha256 `ca2707845a033901053620c70512a0a6a5ebf52d1b3069704aae8a93e17c7b2a` and 8931 bytes. It checks those bytes again immediately before the subprocess. Verify and inspect launches keep the historical scripts.

A guard mismatch writes stdout with `launched: false`, `writer_started: false`, and `result refused`, and returns exit 2 before the sealed handoff runs. When the binding parent is a plain directory outside the live book, it also writes a sidecar schema `capture-handoff-guard-mismatch/1`. The public CLI has no `--guard` flag. Tests may pass `guard_path` to `perform` and `require_guard`; that argument still has to match the pin.

On a declared book, reserve and capture through the guard refuse before the historical writer loads. An old reservation followed by a declaration, then a handoff capture, keeps the failure record and the intent. A second perform does not report `result ok` and does not replace an existing failure log. An undeclared book keeps the historical reserve behavior and the sentence that line-pass protection is absent.

A book that already contains `0100.band.returns` cannot show a successful undeclared delegation: the historical writer refuses that door before it allocates. The undeclared demonstration uses a doorless book. The marked-copy demonstration is the declared refusal.

## What this build does not do

It does not edit the historical writer, the inspector, pass04, pass03, pass02, pass01, the placement tool, the pass01 reader, the sealed handoff, the Clerk, the 05.08 guard, the 05.08 harness, or any existing app file. It does not edit `app/librarian.py` or `README.md`. It does not write a live layout, a live reservation, or a live authority file. It does not install a sentinel. It does not allocate `0184`. Matching `0121.return-placement` custody stays pending. It does not claim that every script on the machine is confined to the guard.
