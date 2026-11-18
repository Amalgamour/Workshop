# First local failures

This note is a transcription. It is not the original unittest byte stream. The captured green run is `tests.txt`.

## Suite

Command: `python -B -m unittest -v labs/prime-desk-pass01/tests/test_prime_desk.py`

Working directory: `D:\Git\lib-build`. `PYTHONDONTWRITEBYTECODE=1`. Python 3.14.0.

Exit 1. `Ran 17 tests in 2.149s`. `FAILED (failures=1)`.

`test_cli_json_and_no_source_write` reached `self.assertFalse(os.path.exists(live))` and raised `AssertionError: True is not false`. `00.kernel/00.live.md` exists. The tool had not rewritten it. The assertion was replaced with a before-and-after byte compare. Unclosed reads in the test helper were closed in the same edit. The sixteen other tests passed on that run.

## Demo

The first demo attempt exited with `KeyError: '00.kernel/00.00.10.work/0524.prime-desk/05.01.md'`. That page is not one of the 39 pack sources. The page list was changed to pinned sources. The partial copy was removed.

A later demo, after the packet heading fix, refused with `live pin mismatch: 00.kernel/00.00.10.work/0522.review-construction/05.04.md`. The live file had moved off the pack pin. The demo now copies `evidence/pack05.01` snapshots and records the live difference in `demo-output/live-drift.txt`. It does not parse the new live bytes.
