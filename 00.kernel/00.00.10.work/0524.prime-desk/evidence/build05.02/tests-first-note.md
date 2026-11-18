# First local failure

`tests-first.txt` is the unittest stderr stream. `tests-first.exit` is `1`. Stdout was empty. The official green stream is `tests.txt`.

Command: `python -B -m unittest -v labs/prime-desk-pass02/tests/test_prime_desk.py`

Working directory: `D:\Git\lib-build`. `PYTHONDONTWRITEBYTECODE=1`. Python 3.14.0.

Exit 1. `Ran 12 tests in 2.995s`. `FAILED (errors=1)`.

`test_authority_conflict_keeps_canonical_page` called `snapshot("0521.return-placement/05.03.md")`. The pack manifest path is `00.kernel/00.00.10.work/0521.return-placement/05.03.md`. The helper raised `StopIteration` before the tool ran. The two page lookups now use the manifest path. The other eleven tests passed on that run.
