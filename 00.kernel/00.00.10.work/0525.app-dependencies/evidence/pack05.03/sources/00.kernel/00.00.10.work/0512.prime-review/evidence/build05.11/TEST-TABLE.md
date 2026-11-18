# Test table - 05.11

The pre-filing author command is `python -B labs/review-source-capacity-pass02/tests/test_capacity.py`.
The passing run is 25 tests, 201.252 seconds, OK, exit 0, Python 3.14.0.
The first run is preserved as author-suite-first.txt. It ran 25 tests and failed 2.
Those failures are the split source-text assertion for the 64-step sentence and the 05.10 record refusal `limit sources[24].content_bytes`.
The pass01 suite was not re-run. Its preserved Prime log remains evidence/prime-review05.10/author-suite.txt.
Revised rows are not an unchanged 18/18.

| Case | Expectation | Provenance | Detail |
| --- | --- | --- | --- |
| active-surface | revised | author | librarian_sha256=c3a5be3b612c021d95effaa5da4a151bf89026422b94f4cad98331014c7f0cd9, pointer=pending, readme_sha256=3c2125aa0cebd7ddc1604de2a823c1250edf40a8e97bd7dbd2eb09ca91155920, review=pending |
| case-reconciliation | revised | author | preserved_count=14, revised=['active_surface', 'generated_bounds', 'hostile_count', 'hostile_document'], unchanged_18=False |
| changed-and-missing | preserved | author |  |
| code-root-excluded | preserved | author | emitted=3 |
| cycle-0509 | preserved | author | custody=missing, document_bytes=125955, mode=preliminary, publish=published, review_id=wecc2ddb1f86340b2, sources=29 |
| cycle-0510 | blocked-by-preserved-content-bytes | author | content_bytes=276423, correction=refused: limit sources[24].content_bytes, document_bytes=137328, recorded=False, sources=44 |
| cycle-0514 | preserved | author | custody=missing, document_bytes=62200, mode=preliminary, publish=stale-own-review, review_id=w72c59674fc0615ad, sources=20 |
| document-bound | preserved | author | bytes=276423, sources=22 |
| duplicate-and-conflict | preserved | author |  |
| generated-bounds | revised | author | new_33=33, new_64=64, new_65=65, old_24=True, old_25=limit sources, prior_32=32, prior_33=33 |
| historical-modules | preserved | author |  |
| historical-replay-0509 | preserved | known-reproduction | correction=refused: limit sources |
| holds-stay-24 | preserved | author |  |
| hostile-count | revised | author-hostile |  |
| hostile-document | revised | author-hostile | bytes=502359, sources=40 |
| known-pending-failure | known-failure | known-reproduction |  |
| lab-door-not-install | preserved | author |  |
| answers-stay-24 | preserved | author |  |
| linked-pin | preserved | author |  |
| malformed-and-unknown-size | preserved | author |  |
| naive-external-copy | preserved | known-reproduction |  |
| predecessor-0510 | revised | known-reproduction | correction=refused: limit sources: 44 sources exceeds supported limit 32; split the return so one record binds at most 32 sources, sources=44 |
| semantic-versus-raw | new | author | already_recorded=True |
| wrong-pins | preserved | author |  |
| no-live-write | new | author |  |
