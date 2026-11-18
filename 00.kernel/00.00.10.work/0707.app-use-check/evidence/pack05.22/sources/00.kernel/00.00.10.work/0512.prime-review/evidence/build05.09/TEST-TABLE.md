# Test table - 0512.prime-review/05.09

accepted: false
provenance: author
independent: false

The successor suite is python -B labs/review-report-hardening-pass01/tests/test_hardening.py. Python 3.14.0. 25 tests, 15.932 seconds, OK, exit 0. The first run failed the missing-review case. The contract was corrected once for the not-recorded absent-journal path, then locked at sha256 1ac2b93a03e5a17a38c0deb3046b78324d374e3cec9d6239830d006019917f5b, 7827 bytes. The passing run embeds that lock. The contract was not revised after the passing run. The first log is author-suite-first.txt. These cases are not Prime's independent probes.

| Case | Provenance | Result |
| --- | --- | --- |
| contract, active dispatcher, and active v3 refusal | author | OK |
| lifecycle body stays; PENDING and filed regions both pass | author | OK |
| prime probes are named and not run | author | OK |
| historical modules and helper root stay | author | OK |
| live 0512/05.06 baseline equals installed command | author | OK |
| live 0521/05.13 baseline equals installed command | author | OK |
| missing review keeps the validated advisory envelope | author | OK |
| stale note keeps a coherent historical envelope | author | OK |
| held digest withholds the current-cut envelope | author | OK |
| wrong app hash | author | OK |
| wrong transitive hash | author | OK |
| malformed and repeated arguments | author | OK |
| historical pass03, v1, v2, and the 05.08 deployment runtime refuse the installed dispatcher | author hostile | OK |
| swapped runtime stops the app command before observe | author hostile | OK |
| malformed envelope is withheld | author hostile | OK |
| invalid rows do not complete a measured total | author hostile | OK |
| malformed envelope types | author | OK |
| each envelope field on hold and mismatch | author | OK |
| empty versus absent rows and sizes | author | OK |
| uppercase and invalid digest | author | OK |
| unreadable cut does not become stable true | author | OK |
| review-loop, authoring, return-lines, and where | author | OK |
| direct lab dispatcher is not an install | author | OK |
| unseated connector is refused | author | OK |
| linked pin is not followed | author | OK |

The B-05 and B-01 logs under known-reproductions/ are the pre-repair reproductions through the 05.08 deployment runtime. They are not rows in this table and they are not new coverage.

Post-filing rerun path, outside this manifest: D:/librarian/temp/0512-0509-report/author-suite-after-filing.txt.
