# Test table - 0512.prime-review/05.08

accepted: false
provenance: author
independent: false

The successor suite is python -B labs/review-report-deployment-pass01/tests/test_deployment.py. Python 3.14.0. 18 tests, 14.755 seconds, OK, exit 0. The contract was not revised after the first failure. The first log is author-suite-first.txt. These cases are not Prime's independent probes.

| Case | Provenance | Result |
| --- | --- | --- |
| contract, active dispatcher, and active v2 refusal | author | OK |
| lifecycle body stays; PENDING and filed regions both pass | author | OK |
| prime probes are named and not run | author | OK |
| historical modules and helper root stay | author | OK |
| live 0512/05.06 baseline equals installed command | author | OK |
| live 0521/05.13 baseline equals installed command | author | OK |
| missing review | author | OK |
| stale note | author | OK |
| held digest | author | OK |
| wrong app hash | author | OK |
| wrong transitive hash, runtime and connector | author | OK |
| malformed and repeated arguments | author | OK |
| historical pass03 and v1 refuse the installed dispatcher | author hostile deployment | OK |
| swapped runtime stops the app command before observe | author hostile deployment | OK |
| review-loop, authoring, return-lines, and where | author | OK |
| direct lab dispatcher is not an install | author | OK |
| unseated connector is refused | author | OK |
| linked pin is not followed | author | OK |

The R1 installed-copy refusal and the R2 PENDING assertion failure are retained under known-failures/. They are the 06.12 reproductions. They are not rows in this table and they are not new coverage.

Post-filing rerun path, outside this manifest: D:/librarian/temp/0512-0508-report/author-suite-after-filing.txt.
