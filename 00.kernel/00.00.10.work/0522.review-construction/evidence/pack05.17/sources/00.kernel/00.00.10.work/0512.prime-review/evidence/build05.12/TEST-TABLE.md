# Tests - 05.12 author suite

| Case | Expectation | Result |
| --- | --- | --- |
| active-surface | revised | author |
| capacity64-0510 | preserved | sources=44; document_bytes=137328; external_bytes=276423; correction=refused: limit sources[24].content_bytes |
| case-reconciliation | revised | author |
| changed-and-missing | preserved | author |
| code-root-excluded | preserved | author |
| cycle-0509 | preserved | sources=29; document_bytes=125955; review_id=wa2e4f7a1d3e48fab; publish=published |
| cycle-0510 | revised | sources=44; document_bytes=137328; review_id=wa7922b9b4f84d400; publish=published |
| cycle-0510-binding | revised | sources=44; document_bytes=137328; external_bytes=276423 |
| cycle-0514 | preserved | sources=20; document_bytes=62200; review_id=w5da8c91e140b119c; publish=stale-own-review |
| document-bound | preserved | sources=22 |
| duplicate-and-conflict | preserved | author |
| first-gate-log | preserved | known-reproduction |
| generated-bounds | revised | author |
| historical-modules | preserved | author |
| historical-replay-0509 | preserved | correction=refused: limit sources |
| holds-stay-24 | preserved | author |
| hostile-above-source-bound | new | external_bytes=16777217 |
| hostile-count | revised | author-hostile |
| hostile-document | revised | sources=40 |
| hostile-prefix | new | author-hostile |
| known-pending-failure | known-failure | known-reproduction |
| lab-door-not-install | preserved | author |
| answers-stay-24 | preserved | author |
| linked-pin | preserved | author |
| malformed-and-unknown-size | preserved | author |
| naive-external-copy | preserved | known-reproduction |
| predecessor-0510 | revised | sources=44; correction=refused: limit sources: 44 sources exceeds supported limit 32; split the return so one record binds at most 32 sources |
| semantic-versus-raw | new | author |
| source-size-bounds | new | author |
| wrong-pins | preserved | author |
| no-live-write | new | author |

The first __main__ run is the passing run. The earlier literal-join assertion is first-failures/literal-join.txt. The historical gate refusals are first-failures/both-gates.txt.
