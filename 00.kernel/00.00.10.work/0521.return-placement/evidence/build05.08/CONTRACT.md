# Contract — guarded legacy return writer

Schema: `return-capture-guard-contract/0508`
Date: 2026-11-02. Executor: Grok-2. Reviewer: Codex Prime.
This contract is written before the successor. It is not a release and not a receipt.

## Pins this guard checks

| Role | Path | sha256 | bytes |
| --- | --- | --- | --- |
| Historical writer | `labs/return-capture-pass01/return_capture.py` | `8f3da5c651f6924fca6dedb0b95da7d181eb58884dc030dd9cbc3d8b6a5b15ac` | 45767 |
| Layout rules | `labs/return-lines-pass01/return_lines.py` | `863968c59974d85910626ba5e80cf49f14a3186c8d33b855efe00bf6ccec378a` | 100897 |

Pack inputs: `evidence/pack05.08/source-manifest.json`, 24 files, 8226 bytes, sha256 `aa64824019e45f388a703530fb22708bb405f6ae13c499ab8753e61485c7af20`. 0 mismatches at the claim. The manifest keeps its CR bytes.

Inspection stays on `labs/return-capture-pass01/return_inspect.py`, sha256 `947915febaa5918f56b6be03c81840c030d081fcab9a3bead2cd660973a9999b`, 11402 bytes. The guard does not replace that sibling pin.

## Successor

Path: `labs/return-capture-guard-pass01/return_capture_guard.py`.
The hash is measured after the file exists. This contract does not guess it.

Commands: `reserve`, `capture`, `verify`, with the same flags as the historical writer. There is no `--force`, no `--allow-live`, and no sentinel.

## Layout decision

The decision reads `return-line-layout.json` in the target book. It uses pass01 `layout_body`, `read_layout`, `dump`, and `is_reparse`. It does not classify a book by folder names.

| Observation | Status | Reserve and capture |
| --- | --- | --- |
| Layout path absent | `undeclared` | Delegate to the pinned writer. The reply adds: an undeclared book has not gained line-pass protection. |
| Regular file, link count 1, bytes equal `dump(layout_body(book))` for schema `return-line-layout/1` | `declared` | Refuse before the writer loads. Correction: use the line-pass route. No receipt and no success line. |
| Reparse point, or link count other than 1 | `linked` | Attention refusal. The path is not followed. No allocation. |
| Unreadable, non-regular, or not the line-pass schema | `malformed` | Attention refusal. No allocation. |
| Parsed shape differs in bytes from the accepted declaration | `conflict` | Attention refusal. No allocation. |

`verify` still calls the pinned writer after the pin check, including on a declared book. A declared layout does not rewrite an old receipt.

A pin mismatch on either file refuses before either module is executed.

## What this build does not do

It does not edit the historical writer, the inspector, pass04, the reader, the handoff, or any app file. It does not write a live layout, a live reservation, or a live authority file. It does not install a sentinel. It does not allocate `0184`. Matching `0121.return-placement` custody stays pending.

An unchanged copy of the historical script remains runnable. Selection of this guard by a caller is what closes that caller's reserve and capture on a declared book. This build does not claim that every existing script is confined.
