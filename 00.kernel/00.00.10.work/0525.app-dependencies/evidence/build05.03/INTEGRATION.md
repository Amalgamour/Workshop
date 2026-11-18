# Integration recipe

Historical declarations in `labs/app-dependencies-pass03` stay as set `accepted-loop-preflight-1`. Binding a reviewed combined workbook W and a reviewed reporter-on-W happens in a new set.

1. Wait until W and reporter-on-W have reviewed paths and reviewed measurements.
2. Create a new set id and new declaration files. Copy forward only the records that still apply.
3. Add versioned records for W and for reporter-on-W. Use `observed-file` with form `working-tree` and `context_head` null while the measurement is a working-tree digest. Use `git-blob` only with verification `supplied-unverified` until a separate pass actually checks the commit. A working-tree hash stays a file digest.
4. Select the new records in the new set. Leave the select rows in `accepted-loop-preflight-1` unchanged.
5. In the new set only, replace the `pending-w` and `pending-reporter` address edges with the reviewed module edges and the caller-enforced pin form. Leave the historical JSON files in this lab unchanged.
6. Run `labs/module-dependencies-pass02/depdecl.py` on the new set. There is no automatic pin update.

`labs/app-dependencies-pass03/preflight.py` always emits the two pending slots with null path and null hash, and it always sets `activation_ready` false. A later set does not turn this wrapper into an activation report. Activation remains a separate Prime decision.
