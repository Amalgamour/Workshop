# Friction — case-a assisted

## Tool refusals
- `prime_cycle.py read` writes a template and then reports `no-return` because `batch_observe` exits 2 with `missing clerk_adapter.py`. Path the reader wants: `assistance/labs/prime-support-pass01/clerk_adapter.py`. That file is not in the assistance tree.
- The same `read` therefore binds `receipt_sha256: null` and `page_sha256: null`.
- `packet` does not use that reader. It exited 0 and verified member 0163. The two tools disagree, and both outputs are kept. The packet's artifact list is empty, so it is not an inventory of the harness.
- `record` of `out/decision-case-a.json` exited 2: `observation failed: reader exit 2`. `inspect` found no committed review. The binding was not edited to invent a receipt.

## Subject checks in this frozen tree
- `validate` exit 1. Five support paths are missing on disk. Pack snapshots for the 10 manifest rows match their pins, and those live paths are still absent.
- `test_prime_bench.py` exit 5. Ran 0 tests. `setUpModule` could not read `labs/prime-review-pass01/prime_review.py`.
- I did not copy the assistance copy of `prime_review.py` into the repository to make `validate` pass.

## Corrections during this run
- The first `day` was launched with the re-read and listed one read. I ran `day` again after the re-read finished. The second day lists two reads, one packet, one refused record, and one inspect. Both day outputs are kept.
- Direct `batch_observe` was an extra wrapped command so the reader stderr was on disk. The cycle journal does not store that stderr. The direct command does, in operation `e45b09cbd40d4a6c97276ebbde8441ac`.

## Manual copies
- One binding copy: the template binding was written into `out/decision-case-a.json` unchanged, including the null receipt. I did not count keystrokes.

## Not counted as Prime time
- Setup is `runs/grok/setup.json`: 2.086901400005445 seconds. It is not a per-run saving.
- Wrapper seconds are only the subprocesses. Reasoning and file-reader time are not in those seconds.
