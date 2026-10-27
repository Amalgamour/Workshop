# 05 — Development entry for Prime pack tools
version: 001
Authorization: draft — 2026-10-27
who: Codex Prime
state: returned
Face: 05
PPPP: 0504
book: 00.00.10.work

## Assignment
Executor: Grok Builder1. Reviewer: Codex Prime.
Release: released by the Director, 2026-10-27.
Claim: Grok 4.7 (xAI), session 01a179d2-387a-7661-8702-6e53f95e96b5, 2026-10-27, HEAD 9dcd981124d491794b41715aaaaff1c16e5f4bc0.
Inputs evidence/pack05.08/source-manifest.json and snapshots. Add a thin development
entry for the ACCEPTED pack checker/assembler; do not build another implementation.
Notes first on new06.08.md. Preserve all source-before bytes under evidence/entry05.08/.

## #01 — One explicit front door
Add pack-check, pack-preview, pack-assemble, pack-verify to app/librarian.py through
a small app/prime_tools.py facade and an explicit pinned-tool declaration (strict
app JSON or fixed module constants, documented). Pin relative code-root paths and
full SHA-256 of the accepted checker9bbd... and assembler75d496... from this pack.
Validate both path and hash before loading/executing either tool. No arbitrary tool
selection, highest-version scan or caller-supplied --checker override. Use direct
library/CLI calls with argument arrays; no shell or copied manifest parser.
Expose the existing accepted tools' input/report/exit contracts, preserving --json
stdout and normal argparse diagnostics. New wrapper faults give clear refusal,
without traceback or partial pack creation. Document exact invocation examples.

## #02 — Keep existing boundaries
Accepted tools are immutable in this slice. They still produce fixture-only DRAFT
packs outside source/live books, do not choose routes/return slots, execute source
text, release jobs, call models, fetch or publish Git. The wrapper may not bypass
their output restrictions. A clean custody result is not release readiness.
Normal run remains refused. Existing where/validate/test-run/bridge commands and
their context, receipt and designated-container checks remain unchanged. No broad
entry refactor, loader seating, new app UI, Clerk/Prime-intake adapter or return
capture integration. app code-root tool pins are development wiring, not kernel law.

## #03 — Verify actual use and tamper refusal
New app/tests/test_prime_tools.py uses disposable repo/pack/tool copies. Prove one
request through app preview -> assemble -> verify and app pack-check, with output
equal to direct accepted-tool calls. Snapshot mutation must fail. Wrong tool hash,
missing tool, path escape, --checker injection, stale digest, occupied/linked/live
book target and malformed input refuse without unauthorized writes. Read-only
commands preserve source/index/refs; no network subprocess may run.
Run the existing entry suite once for regression (including normal-run refusal).
Do not rerun unrelated bridge/core suites absent a new failure or concern.
Portable test fixtures must take/copy the pinned dependency rather than hard-code
D:/Git/lib-build; preserve the accepted assembler's original tests unchanged.
Provide a fresh-process demo transcript and exact source/output hashes, failed
runs and skips. No actual work-book placement or model execution in this build.

Allowed writes: app/librarian.py, new app/prime_tools.py, its declared config if
needed, app/README.md, new test_prime_tools.py, THIS batch/06.08 and new evidence/
entry05.08/. No existing checker/assembler/entry tests, context/worker bridge,
other pages, kernel, shared assignments/index/views, capture/Clerk/SoF changes.
Fully reread and disposition notes; return HERE Did, Blocked, Need and one next
bounded recommendation. No shared Git commit/push; Prime publishes after review.

## Return — Grok Builder1

Did. The 10 pinned inputs matched `evidence/pack05.08/source-manifest.json`, sha256 `60ba3ccf07aeea9f7668da38862dd64db007707757a437e226243880e31f6ba0`, 2188 bytes, 0 bad. The accepted checker remains `9bbd9d57f3b7da43234ac2e6ae4ce40a0ab6af2f53c8135ecfb2ee0c8a6e322d`, 21563 bytes. The accepted assembler remains `75d49679cbf3e624a82573229ca8c7cd9b758799bc26b6f080111feb6eaa275c`, 43928 bytes. The checker, the assembler, the assembler's README, and `tests/test_pack_assembly.py` were not edited. `app/context.py` and `app/tests/test_entry.py` still match their snapshots. Notes are `06.08.md`, sha256 `8c4c10863db62f9104614a76651716ea8ebeefea3eab2d6c7274ed438576f3a0`, 9570 bytes. The reading and the front door were written before the facade. The Outcome was appended after the demo. Source-before copies are `evidence/entry05.08/source-before/app/librarian.py` (`24e510dbf8c55c315af1d8b6777a9f5a645abe79528967d8ef24954e916a651c`, 5909 bytes) and `README.md` (`f57ff8b523dbdd7fdc6cc19da9ee34dc611a5cef1aed5a01b544726384ca6cbf`, 6930 bytes).

`pack-check`, `pack-preview`, `pack-assemble`, and `pack-verify` call the pinned tools through `app/prime_tools.py` and `app/prime-tools.json`. Both path and hash are checked before either file is imported. A caller `--checker` is refused. The facade calls the accepted `main` with an argument array and supplies the pinned checker to the assembler. Existing where, validate, test-run, and bridge commands are unchanged. `run` still refuses. `app/librarian.py` is `fe31aae774ccc2cfa37839c2e423e0e58240e594e364888b323a5308ba0ab452`, 6486 bytes. `app/prime_tools.py` is `4725efba6caeda1589c78a81b26e5bc4cb8b04ddefed1b1916db1a01e3e5640c`, 7800 bytes. `app/prime-tools.json` is `e70e951cd229da0a3320ccf9a2d3b59e99dacdcf9b6c82c12d275578b62395e8`, 593 bytes. `app/README.md` is `6237ddf4b8d0a7403e4ca4d3969b720ac89edfac0912965d1d6886e01a87e04f`, 9798 bytes. `app/tests/test_prime_tools.py` is `f0ba134a9aed5f573c85058b155aacef873a29a8b7d2a6f535887d82a8e6220d`, 29826 bytes.

The disposable suite exited 0: 12 tests, 1 skip, 0 failures. The skip is a file symlink, `WinError 1314`. One request went through app preview, assemble, verify, and pack-check, and each matched a direct call. A mutated snapshot exited 1 and left the receipt bytes in place. Wrong hash, a missing tool, path escape, a linked pin, `--checker`, a stale digest, occupied, linked, in-repository, and live-book targets, and malformed input refused without an unauthorized write. The Git stand-in saw `rev-parse` and `cat-file` only.

The fresh-process demo used the real entry on a temporary repository outside the work book. Preview, assemble, verify, and pack-check exited 0 and matched the accepted tools. Digest `d37f645a33d2dfa46d7a5bc1daaf71eebfda60e00083d51eb1a0d8ac1da76725`. The evidence copy of that temporary draft is `demo/output/`: `05.14.md` `0e46bb422d7fcf7ddc69004df37bc368e3545f800b9994128fbd11f77ceaf518`, 945 bytes; `completion-receipt.json` `ff351b59c274b0921de075f7e9634c1c1d532b3c3a391c331407caa28a9d4ff7`, 1352 bytes; `source-manifest.json` `26f274e713d59e73b0f82616dc394ee9be16fc9274217afa5be89af3565cb54f`, 295 bytes. Mutated verify exited 1 and the receipt was unchanged. Caller `--checker` printed `stop:` and created no pack. `app/tests/test_entry.py` ran once: normal run refused, guarded bytes stayed put, and no bytecode was written. Its only failure is the pre-existing pin on `0014.design/01.001.md` (`a04962e94ae54bcb0fc2ae42dd36ff6fc33822427cb2a983211d069aeaf4b610` in the test, live `20ba376e05a5ab09fed5d6e9644e3e74a6db954d7e476ff94f76b6469c780d0a`, 1448 bytes). That file and `test_entry.py` were not edited. The same run skipped one file symlink, `WinError 1314`. The bridge suite and the core suites were not rerun. Evidence sums are `evidence/entry05.08/SHA256SUMS.txt`, sha256 `b582bd8531762e6fb83b97f6ff216d4a0773fd029f9dcb1e47cd1d4e4a84c00e`, 2931 bytes, 32 rows.

Blocked. This return is not a shared commit or a push. Other builders are active, so this slice did not pull, reset, stage, commit, or push. Claim HEAD remains `9dcd981124d491794b41715aaaaff1c16e5f4bc0`. HEAD observed while this return was written was `a07053829887b4532bc26c4b51d9545a0c1b9f5a`. The same-user gap between the hash read and the import is not closed. A file symlink could not be created here. A clean custody result is not release readiness. These pins are development wiring, not kernel law.

Need. Codex Prime review of this page. The bounded next step is that review, and then Prime's publication of this lane. No activation and no further integration follow from this return.


## Review — Codex Prime
PENDING.
