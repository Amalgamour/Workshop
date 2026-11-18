# First failures

These rows are the defects this successor was required to reproduce, and the blocks that remain. The passing author suite keeps both. Historical modules were left unchanged.

## Reproduced from the Prime evidence, then closed on the author path

1. `evidence/prime-review05.18/prime-probes.json` records `door_control` and `door_changed` both at exit 0. The changed pass02 loop door still ran. The pass03 dispatcher checks the trust anchor and both door byte hashes before `load_module`. The author door probe appended `MARKER-DOOR-RAN` in a copy. That marker stayed out of the output, and the command exited nonzero.
2. `evidence/prime-review05.18/reporter-observation-probes.json` already withheld unsupported authority, stale recovery, and a missing recover id. Three complete measurements still returned state `readable` with a judgment: a wrong inspect `current` id, a stale inspect, and a nonzero prepare. The pass03 reporter withholds those three as state `noncurrent`. Held, both-stale, and empty cuts stay on their earlier paths.
3. The pass02 builder command was `make_candidate.py --output ABS`, and that command wrote generated files into the delivered lab. Prime excluded that CLI from RC-1. The pass03 command is `make_candidate.py --root ABS`. The author suite compared two new roots, including `CANDIDATE.json` and `harness-inputs.json`, and they matched. The CLI left the lab unchanged. The suite then copied `harness-inputs.json` into the lab. That copy is the filer step.

## Still open

The full harness in `labs/loop-convergence-harness-pass03/harness.py` was not run. N5-1, N5-2, N5-3, the harness pages for CTX-1, PR-7 on the harness path, RC-1, RP-1, and RP-2 have no harness result in this return. RP-1 and RP-2 stay blocked while R is pending. `KF-RP` stays a diagnostic: the candidate dispatcher contains `review-report`, so a harness call on that route would reach this candidate. `KF-IN` matches the copied-book hold the author suite recorded.

Same-path replacement of a book that keeps the same stored state stays undetected. `instance_id` follows the path, the page, and the pass.

Native custody for matching line `0122.review-construction` is pending. That member directory is absent. No receipt was invented.

The sealed pass01 author suite still stops when the filed 05.17 pointer is no longer PENDING. This successor leaves that suite and that page unchanged. The preserved record remains `evidence/prime-review05.17/suite-first-failure.txt`.

## Author result

The pass03 author suite exited 0. Nineteen cases passed and none failed. That log is `suite.log`. It is builder evidence. It is not Prime acceptance and it is not combined readiness.
