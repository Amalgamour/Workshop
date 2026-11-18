# Integration - 0512.prime-review/05.08 deployment candidate

accepted: false
applied: false
state: unapplied candidate bytes

## What a coherent selection changes

One existing file changes:

- app/librarian.py is replaced by labs/review-report-deployment-pass01/librarian.py, 12805 bytes, sha256 d37dd14ccb921f92ff1a05c00890d57ee0f3d9f27d766bd86d81861abdd80a52.

Three new files must already be present. This pack adds them. Selection does not rewrite them:

- app/review_report_tools_v2.py
- app/review-report-v2.json
- labs/review-report-deployment-pass01/report.py, 6294 bytes, sha256 0f7def8d353506b93c71d130d740cd1262717ce493a868fc356e09ab925f7506

Historical files stay at their current hashes. After the replacement, these still refuse the candidate dispatcher, and that refusal is the preserved boundary:

- app/review_report_tools_v1.py
- app/review-report-v1.json
- labs/review-report-pass01/report.py through pass03 main

labs/workbook-review-pass03/workbook.py stays byte-identical. Its REPO remains D:\Git\lib-build. That is the fixed live helper root.

The 05.07 dispatcher, sha256 b253a89751a48b64089bb95c4fde3715de00e6dc3c61dd8bad8653051234f3fa, 12792 bytes, loads the frozen v1 connector. It is not the candidate. Writing it on disk remains the known R1 refusal.

## Verify before apply

Confirm app/librarian.py is sha256 c3a5be3b612c021d95effaa5da4a151bf89026422b94f4cad98331014c7f0cd9, 12204 bytes. Confirm the three new files match app/review-report-v2.json. Confirm the diff in labs/review-report-deployment-pass01/DISPATCHER.diff is the only text between the current dispatcher and the candidate. If any of those bytes differ, stop. Do not apply.

## Apply

Copy labs/review-report-deployment-pass01/librarian.py onto app/librarian.py. Do not edit the historical reporters. The installed command is:

```
python -B app/librarian.py review-report --book ABS --source PAGE --pass 05.NN
```

That command executes the on-disk app/librarian.py. Exit 0 is not a release.

## Rollback

Restore app/librarian.py from evidence/build05.08/rollback-librarian.py. The restored file is sha256 c3a5be3b612c021d95effaa5da4a151bf89026422b94f4cad98331014c7f0cd9, 12204 bytes. Leave the new v2 files in place. They refuse the restored dispatcher. v1 and pass03 main accept it again.
