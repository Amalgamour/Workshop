# Prime use — first view and a live-read proposal

This pass already produced a useful view from an explicit new output. The command was:

```text
python -B labs/prime-desk-pass01/demo.py --out D:\Git\lib-build\00.kernel\00.00.10.work\0524.prime-desk\evidence\build05.01\demo-output
```

Run it from `D:\Git\lib-build` with `PYTHONDONTWRITEBYTECODE=1`. Python was 3.14.0. The same `--out` now exists, so a repeat refuses. To generate again, pass a new absolute directory.

Read these files:

- `demo-output/view.md` and `demo-output/view.json`
- `demo-output/packet.md` and `demo-output/packet.json`
- `demo-output/request.json`
- `demo-output/live-drift.txt`

The overview is about one minute. Selected work is `work-0522-0504` at the pinned `0522.review-construction/05.04.md` (`9da5a0ba30dc45ba926237a6c5690263ae68758964647539078c552714784c11`, 7395 bytes). Tool exit is 1. That exit is the visible hold, the null verification, the catalog item that was not chosen, the missing return, and the worker with no evidence file. It is not acceptance.

## Live-read proposal — not run

This pass did not point the tool at the live book.

A later review can do that only with a new request file. Start from `demo-output/request.json`. Set `instance.root` to `D:\Git\lib-build\00.kernel\00.00.10.work`. Keep `tools_root` as the repository root. Then:

```text
python -B labs/prime-desk-pass01/prime_desk.py view --request ABS
python -B labs/prime-desk-pass01/prime_desk.py packet --request ABS --work-id work-0522-0504
```

Before that command, decide the `0522/05.04` bytes. At demo time the live file was sha256 `7280a0fadd520b5ad02d72ed3a30d08d0289e61a0bdb0fa7db159c7ba6d0b3f1`, 8250 bytes. The request still names the pack pin. Left unchanged, the tool will mark that one file stale, withhold the new bytes, and keep the other matched facts. Rehashing is a new request written by a person. The tool will not silently refresh.

`assignment_state: running` in the pinned assignment record stays a record field. A supplied sentence that a worker is running stays supplied. Neither one is a live process check.

Manual work that remains: keep the request, the selector, and the catalog hashes current by hand. The tool does not crawl for a newer page. Review-loop integration stays pending until a later reviewed pass. This proposal does not seat `00.live`, register a librarian command, or file 0124 custody.
