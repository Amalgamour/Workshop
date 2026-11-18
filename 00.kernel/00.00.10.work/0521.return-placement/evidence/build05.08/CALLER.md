# Caller contract — selected guard, historical pins kept

Schema: `return-capture-guard-caller/0508`
Date: 2026-11-02. Written before the successor.

## This build's caller

`labs/return-capture-guard-pass01/harness.py` is the only selector in this build. It pin-checks `labs/capture-handoff-pass01/handoff.py` at sha256 `a8380136a84469b8975b38f084a4d34802ccf079ed69cf85d107f6ca3643426a`, 51828 bytes, and imports that module. It does not edit the file and it does not change `TOOL_FILES`.

For a launch whose first argument is `capture`, the harness passes the guard path instead of the packed writer path. `check_pins` still requires the historical capture, inspect, and clerk files. Inspect and verify launches keep those packed paths.

When the guard refuses, the handoff reports attention or refused, writes `clerk-capture-handoff-failure/1` when the failure log is absent, and retains the intent record. It does not write `result ok`. A later attempt keeps the existing failure log.

The harness hash is measured after the file exists. This contract does not guess it.

## What stays on the historical writer

These supplied files still name `labs/return-capture-pass01/return_capture.py` at `8f3da5c651f6924fca6dedb0b95da7d181eb58884dc030dd9cbc3d8b6a5b15ac`:

- `labs/capture-handoff-pass01/handoff.py` `TOOL_FILES["capture"]`, and the `launch` call that captures.
- `labs/capture-handoff-pass01/demo.py` reserve setup.
- `labs/capture-flow-rehearsal-pass01/rehearse.py` reserve setup.
- `labs/return-capture-pass01/return_inspect.py` sibling helper. This pin stays. Inspect does not allocate.
- `labs/return-access-pass01/return_access.py` reader pin. This pin stays. The reader does not reserve.
- Supplied `app/handoff_tools.py` tool table and its declaration check. This build does not read or edit the live facade. The snapshot is the inventory.
- Supplied `app/boot_tools.py` pins the helper and launches `prime_boot`, not reserve.
- Supplied `app/batch_tools.py` pins the helper and launches `batch_observe`, not reserve.

A later integration selects the guard at the write edges above. It keeps the inspect sibling hash until inspect and the helper change together. It does not repin sealed history. It does not add a sentinel. App selection belongs to a later reviewed change. Grok-1 owns the current app integration. This contract does not activate the guard.
