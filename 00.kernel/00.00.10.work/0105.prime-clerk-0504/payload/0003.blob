# Runs for 05.04, in order

All runs used disposable copies in which `labs/prime-support-pass01` and `labs/clerk-handoff-pass02` sit side by side, outside the shared checkout.
- Interpreter: pythoncore-3.14-64.
- Environment: `PYTHONDONTWRITEBYTECODE=1`.
- Every test Git repository, Clerk store and intake store was under the system temp directory.

| File | Command | Result | Disposition |
|---|---|---|---|
| runs/run01-test_clerk_adapter-fail.txt | `python -B -X dev tests\test_clerk_adapter.py -v` | 14 run, 3 FAIL | See the three failures below. Kept. |
| runs/run01-test_prime_support.txt, run01-test_psi.txt | same, for the two existing suites | 19 ok; 10 ok | superseded |
| runs/final-test_clerk_adapter-dev.txt / -default.txt | `python -B [-X dev] tests\test_clerk_adapter.py -v` | 14 run, 14 ok, 0 skipped | final |
| runs/final-test_prime_support-dev.txt / -default.txt | the existing suite | 19 ok, 0 skipped | final |
| runs/final-test_psi-dev.txt / -default.txt | the existing PSI regressions | 10 ok, 0 skipped | final |
| runs/final-demo-clerk.txt, demo-clerk/ | `python -B demo_clerk.py --out <temp> --clerk <copied accepted clerk.py>` | exit 0; 11 processes (3 fixture setup, 8 adapter); 14 checks, 0 failed; demo ok | final |
| runs/final-demo.txt, demo/ | `python -B demo.py --out <temp> --workshop-repo D:\Git\lib-build --sof-repo D:\Git\SoF` | exit 0; 14 processes; 18 checks; demo ok | final, unchanged demo |

The three run-01 failures:
1. **Test fault.** The source scan banned the literal `"claim"`, but that is a legitimate inspection/2 key. The subcommand guarantee rests on the exact argv assertion, and the scan now bans `"queue"`, `"return"` and `"--resume"`.
2. **Test fault.** I expected exit 1 from a version-1 registry whose fixture page has no attention item. The test now asserts only "not refused".
3. **Product diagnostic, fixed.** `ack-clerk` on an unknown or incomplete job refused with "registration binding unknown". It now refuses with "no returned-event identity (state …)". A binding mismatch is still refused first.

Around the original demo, `git status` and the index hash of `D:\Git\lib-build`, and `git status` of `D:\Git\SoF`, were identical before and after. The Clerk lab's pass04 manifest still verifies 9 of 9, and Git shows no change on labs/clerk-handoff-pass02 or the 0506 page.
