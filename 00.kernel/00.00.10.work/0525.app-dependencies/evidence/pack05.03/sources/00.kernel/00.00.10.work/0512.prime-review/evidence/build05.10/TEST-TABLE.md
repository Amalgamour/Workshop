# Test table - 0512.prime-review/05.10

accepted: false
provenance: author unless a row says otherwise
independent: false

The successor suite is python -B labs/review-source-capacity-pass01/tests/test_capacity.py. Python 3.14.0. The passing run is 18 tests, 62.369 seconds, OK, exit 0. The first run is 18 tests, 89.820 seconds, FAILED (failures=2), exit 1. The contract body was not revised after that first run. The two failures were suite expectations, and the expectations were corrected before the passing run. The successor, the adapter, and the candidate were left unchanged between those runs. These cases are not Prime's independent probes.

| Case | Provenance | Result |
| --- | --- | --- |
| active librarian, app README, page body, and unfilled pointer | author | OK on the pre-filing run |
| historical pass02, pass03, pass01, and v7 pins stay, and candidate copies match | author | OK |
| naive external copy is ambiguous-declared-root | known reproduction | OK |
| historical replay of 0512/05.09 refuses `limit sources` | known reproduction | OK |
| candidate cycle 0512/05.09, 29 sources, 125955 bytes, preliminary publish, section-verified | author | OK |
| candidate cycle 0522/05.14, 20 sources, 62200 bytes, publish `stale-own-review`, not-published | author | OK on the passing run; the first run expected a vacant review |
| generated bounds 24, 25, 32, and 33 | author | OK |
| holds of 25 stay `limit holds` | author | OK |
| document above 262144 bytes with 22 sources | author | OK |
| 33-long source list containing a duplicate path is refused at 33 | author hostile | OK |
| document bound again, labeled hostile | author hostile | OK |
| duplicate path, same bytes, collapses; conflicting hash stays incomplete | author | OK |
| code-root row app/review-loop-v7.json is measured and is not emitted | author | OK |
| changed artifact before record is artifact-hash-mismatch; missing artifact before record is artifact-missing; change or delete after record is stale and keeps the stored finding | author | OK on the passing run; the first run expected stale before any stored intake |
| malformed manifest row stays incomplete; unknown content_bytes is `bad type sources[0].content_bytes` | author | OK |
| wrong successor pin and wrong pass02 pin stop before record | author | OK |
| direct lab door is not an install | author | OK |
| linked labs junction is not followed | author | OK |

The raw first log is author-suite-first.txt. The passing log is author-suite.txt. Post-filing rerun path, outside this manifest: D:/librarian/temp/0512-0510-report/author-suite-after-filing.txt.
