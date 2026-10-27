# Runs: what executed, in order, with dispositions

All runs used a disposable copy of `labs/prime-support-pass01/` under the session scratchpad.
- Interpreter: `C:\Users\misg\AppData\Local\Python\pythoncore-3.14-64\python.exe`.
- Environment: `PYTHONDONTWRITEBYTECODE=1`.
- Every test repository was created under the system temp directory.

| File | Command | Result | Disposition |
|---|---|---|---|
| runs/tests-run01-fail.txt | `python -B -X dev tests\test_prime_support.py -v` | 19 run, 18 ok, 1 FAIL (test_scan_show_read_only) | A fault in my test, not the tool. Its final assertion treated the bare origin's files (under `work-origin.git`, not `.git`) as unexpected writes. I replaced it with an exact before/after comparison of every file outside the store. Kept. |
| runs/tests-run02-intermediate-devmode.txt | same, dev mode | 19 ok | Superseded. Run before two edits: the canonical "inside but absent" message, and compact grouped rows with the committed review source. Kept. |
| runs/tests-run03-intermediate-default.txt | `python -B tests\test_prime_support.py` | 19 ok | Superseded, for the same reason. Kept. |
| runs/demo-run01-intermediate.txt | `python -B demo.py --out <temp> --workshop-repo D:\Git\lib-build --sof-repo D:\Git\SoF` | exit 0, 14 processes, 18 checks, 0 failed, demo ok | Superseded by the same edits. Kept. |
| runs/tests-final-devmode.txt | `python -B -X dev tests\test_prime_support.py -v` | 19 run, 19 ok, 0 skipped | final |
| runs/tests-final-default.txt | `python -B tests\test_prime_support.py -v` | 19 run, 19 ok, 0 skipped | final |
| runs/demo-final.txt and demo/ | the demo command, from the final copy | exit 0, 14 processes, 18 checks, 0 failed, demo ok | final. demo/ holds transcript.json, checks.json, both registries, the file listing, and the one acknowledgement it wrote |

**Around both demo runs**, `git status --porcelain=v1` and the `.git/index` hash of `D:\Git\lib-build` and `D:\Git\SoF` were identical before and after. The demo read only these blobs:
- `0504.app-entry/05.05.md` at d9775fa, cf25d56 and 2c581eb;
- `0504.app-entry/05.06.md` at 54274e6;
- `0401.goal/06.01.md` at 54274e6;
- SoF `returns/sof-gm-kit-pass01.md` at 01b8fe6.
Each was hash-checked against `demo.py` PINNED.

No test was skipped on this machine. The suite creates no symlink.

The acknowledgement in demo/intake-store was written by the demo with the label `codex-prime`, in a disposable store. It is a fixture value. Codex Prime did not acknowledge anything.
