# 0705.prime-desk-check / pass02: executable independent desk checks (lab)

The successor to pass01, which is unchanged. Contract: `00.kernel/00.00.10.work/0705.prime-desk-check/evidence/return05.02/CONTRACT.md`. Standard-library Python. No product code. No 0524 or 0522 code is read or run.

| File | What |
|---|---|
| `cases.json` | 18 cases traced to pass01 (`from_pass01`) with Prime's 06.01 corrections; `mode` is executable (16) or manual (C12, C15) |
| `expected.json` | 54 assertions, frozen before evaluation; the checker requires its sha256 |
| `manual-checklist.json` | 24 manual items (M-01…M-06, F-C12, F-C15, and one forbidden-inference item per executable case) |
| `build_fixture.py` | fixtures from pinned pack05.02 snapshot bytes plus declarative ops, into a NEW external directory; generated files listed |
| `synth_obs.py` | SYNTHETIC self-test observations only |
| `check.py` | per-assertion statuses and a separate desk verdict |
| `harness.py` | two-process build and check; HARNESS RESTART ONLY |
| `tests/test_lab.py` | 20 self-tests with planted faults |
| `rehearsal/0521-05.03/` | first-use package |

```text
python -I -B build_fixture.py --cases <abs>/cases.json --manifest <abs pack05.02 source-manifest.json> --out <new abs dir>
python -I -B check.py --expected <abs>/expected.json --expected-sha256 <pinned> --fixtures <dir> --observations <dir> --manual-checklist <abs>/manual-checklist.json [--manual-results <file>]
python -I -B tests/test_lab.py --pack-manifest <abs pack05.02 source-manifest.json> [--report <file>]
python -I -B harness.py --pack-manifest <abs> --out <new abs dir>
```

**A desk pass needs all of these:**
- candidate observations from a connected adapter;
- all 16 executable cases observed;
- all 54 mandatory assertions `pass`;
- all 24 manual items answered `yes` with `by` and `date`.

**Not met in this pass:**
- The adapter for 0524 is NOT CONNECTED.
- Synthetic runs report `desk_verdict: not-applicable (synthetic self-test)`.
