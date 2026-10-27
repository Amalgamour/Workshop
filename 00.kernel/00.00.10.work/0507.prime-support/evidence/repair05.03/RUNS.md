# Runs for 05.03, in order

Every run used a disposable copy outside the shared checkout.
- Interpreter: `C:\Users\misg\AppData\Local\Python\pythoncore-3.14-64\python.exe`.
- Environment: `PYTHONDONTWRITEBYTECODE=1`.
- All test repositories were created under the system temp directory.

| File | Code under test | Command | Result | Disposition |
|---|---|---|---|---|
| runs/psi-failure-before-run01-duplicated.txt | before/ (05.02 bytes) + new tests/test_psi.py | `python -B -X dev tests\test_psi.py -v` | 48 run, 8 FAIL | Valid failure evidence. My test file also re-ran the 19 inherited tests, so it is kept but superseded for clarity. |
| runs/psi-failure-before.txt | before/ + test_psi.py with inherited tests disabled | same | **10 run, 8 FAIL, 2 ok** | **The failure-before record.** It reproduces Prime's PSI-01 (`('verified-fixed', 'closed', 2) != ('unresolved', 'open', 1)`) and PSI-02 (inverted timestamps `('verified-fixed', 'closed')`). Repeated observations and ack deletion already passed, and stay as guards. |
| runs/psi-after-intermediate.txt | corrected code, before the per-call read-only snapshot was added to test_psi | `python -B -X dev tests\test_psi.py -v` | 10 ok | superseded |
| runs/orig-after-intermediate.txt | corrected code | `python -B -X dev tests\test_prime_support.py -v` | 19 ok | superseded |
| runs/final-test_prime_support-dev.txt / -default.txt | final code and tests | `python -B [-X dev] tests\test_prime_support.py -v` | 19 run, 19 ok, 0 skipped | final |
| runs/final-test_psi-dev.txt / -default.txt | final | `python -B [-X dev] tests\test_psi.py -v` | 10 run, 10 ok, 0 skipped | final. Every status call also asserts that HEAD, index, refs, status and page bytes are unchanged |
| runs/final-demo.txt, demo/ | final | `python -B demo.py --out <temp> --workshop-repo D:\Git\lib-build --sof-repo D:\Git\SoF` | exit 0, 14 processes, 18 checks, 0 failed, demo ok | final |

Around the final demo, `git status --porcelain=v1`, the `.git/index` hash and `for-each-ref` of both `D:\Git\lib-build` and `D:\Git\SoF` were identical before and after.

README.md was edited after the final runs. That was a documentation change only; its final hash is in SHA256SUMS.txt.

The Prime's original fixture script is not in the pack; independent-probes.json records only its results. The two counterexamples were reproduced as regressions from that description: `test_psi01_unknown_hash_cannot_close` (worktree on and off) and `test_psi02_inverted_timestamps` (worktree off).
