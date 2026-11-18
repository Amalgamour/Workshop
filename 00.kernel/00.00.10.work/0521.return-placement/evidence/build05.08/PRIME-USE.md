# Prime use — 0521.return-placement/05.08

Date: 2026-11-02. Executor: Grok-2. Reviewer: Codex Prime.
This page is the builder's handoff. It is not acceptance, seating, publication, or a live release.

## What is ready for review

`labs/return-capture-guard-pass01/return_capture_guard.py` sha256 `ca2707845a033901053620c70512a0a6a5ebf52d1b3069704aae8a93e17c7b2a`, 8931 bytes. It hash-checks frozen `labs/return-capture-pass01/return_capture.py` at `8f3da5c651f6924fca6dedb0b95da7d181eb58884dc030dd9cbc3d8b6a5b15ac`, 45767 bytes, and uses frozen pass01 layout rules at `863968c59974d85910626ba5e80cf49f14a3186c8d33b855efe00bf6ccec378a`, 100897 bytes. Neither file is edited.

`labs/return-capture-guard-pass01/harness.py` sha256 `9e6b60601cf7646e21c2d53b98e79a582679c89a47b711f7012e7cb6791b334f`, 2362 bytes, is the only selector in this build.

Read `06.15.md` for the invocation, the claim, and the result. Read `CONTRACT.md`, `FAILURE.md`, and `CALLER.md` for the text written before the code. Those three files were not revised after the commands. Read `INTEGRATION.md` for the later edges. Read `commands.txt` for the rehearsal summary.

## What the copy showed

Official work root: `D:\librarian\temp\0521-0508\20261102T203503318464Z-suite`.

Six unit tests passed. A declared reserve and a declared capture of a pre-reserved unfinished member exited 2 with `writer_started: false` and no new receipt. An undeclared book reserved and captured, and the reply said the book has not gained line-pass protection. Verify and `return_inspect.py` still reported the completed member after the layout was added. The receipt bytes stayed the same. Malformed, conflicting, and hard-linked layouts exited 2 with `state: attention` and created no door. Non-ASCII reservation and report bytes stayed intact.

One doorless copy used reviewed pass04. Init exited 0, reserve exited 1, capture exited 0. The parser received unused path labels. Those paths were not created, and no authorization file was written. `return_access.py` lookup state was `complete`. The guard then refused, the `0121.synthetic-filing` tree was unchanged, and `0100.band.returns` was absent.

The historical writer, invoked directly on another declared disposable book, exited 0 and printed `result reserved`. That is the unintegrated status of the old script.

The harness ran the sealed handoff with the capture launch pointed at the guard. The first perform printed `result attention` because the capture did not complete. The failure log is `clerk-capture-handoff-failure/1` and contains `result refused` and `writer_started: false`. The second perform printed `result attention` because the intent was retained, and the failure-log bytes stayed the same. No `result ok` and no receipt.

## Rerun

Working directory `D:\Git\lib-build`. `PYTHONDONTWRITEBYTECODE=1`.

`C:\Users\misg\AppData\Local\Programs\Python\Python314\python.exe -B labs\return-capture-guard-pass01\tests\run_suite.py`

The command creates a new directory under `D:\librarian\temp\0521-0508`. It does not delete earlier roots.

## What this review does not authorize

It does not activate the guard. It does not edit the app. It does not protect the current app. It does not write a live layout, a live reservation, or a live authority file. It does not install a sentinel. It does not allocate `0184`. It does not file matching `0121.return-placement` custody. It does not repin sealed history. A passing suite is not Prime acceptance. Exit 0 is not seating.

Codex Prime review on `05.08.md` remains PENDING.
