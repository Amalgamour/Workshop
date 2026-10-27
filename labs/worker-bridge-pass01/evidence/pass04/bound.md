# Pass 04 test budget
Date: 2026-10-27

Runtime code is unchanged. `CLEANUP_ALLOWANCE_S` stays 2.0. The eight configured file hashes stay the hashes in `app/worker-bridge.json`. `_driver_pass03.py` is unchanged.

`tests/test_pass03.py` had `TIMEOUT_S` 0.2. Prime's integration run classified both inherited-pipe cases as `timeout` at `duration_s` 0.235, with cleanup complete and `retained` empty. The direct child was still alive at the deadline, so the five-second descendant never held the pipes. That failure is preserved in `evidence/prime-review-05.05-2026-10-27/`. It is not relabeled as incomplete output.

The replacement budget is `TIMEOUT_S` 1.5, outer slack 1.0, and bound 4.5. 1.5 seconds lets the direct child start and exit. The descendant still sleeps 5 seconds, which is longer than 1.5 plus the 2.0 second cleanup allowance, so a correct return is near 3.5 seconds and still names the open readers. The bound 4.5 is less than the reviewed blockage of 5.078 seconds, so that old wait would still fail `assertLess`. A result whose transport is `timeout` still fails the incomplete-output assertion.

The isolated run kept under `evidence/pass04/tests/` returned `incomplete-output`, `collection: not attempted`, `cleanup.complete` false, and retained `stdout reader` and `stderr reader`. The first calls took 3.516 seconds and 3.531 seconds. The identical replay took 0.0 seconds and did not launch again.
