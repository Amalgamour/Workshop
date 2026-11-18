# Integration - 0512.prime-review/05.09 hardening candidate

accepted: false
applied: false
state: unapplied candidate bytes

## What a coherent selection changes

One existing file changes:

- app/librarian.py is replaced by labs/review-report-hardening-pass01/librarian.py, 12804 bytes, sha256 f1d23d455f20319e3f430d345b2893bda039fd8c84be4f3691b4e4be123b8983.

Three new files must already be present. This pack adds them. Selection does not rewrite them:

- app/review_report_tools_v3.py
- app/review-report-v3.json
- labs/review-report-hardening-pass01/report.py, 18139 bytes, sha256 27e513f462b241e9c7298d3077d50d08ea5ac703a6f2d0769dc5935fcb51b58b

Historical files stay at their current hashes. After the replacement, these still refuse the candidate dispatcher, and that refusal is the preserved boundary:

- app/review_report_tools_v1.py and app/review-report-v1.json
- app/review_report_tools_v2.py and app/review-report-v2.json
- labs/review-report-deployment-pass01/report.py
- labs/review-report-pass01/report.py through pass03 main

labs/workbook-review-pass03/workbook.py stays byte-identical. Its REPO remains D:\Git\lib-build. That is the fixed live helper root.

The 05.08 dispatcher, sha256 d37dd14ccb921f92ff1a05c00890d57ee0f3d9f27d766bd86d81861abdd80a52, 12805 bytes, loads the frozen v2 connector. It is not this candidate.

## Verify before apply

Confirm app/librarian.py is sha256 c3a5be3b612c021d95effaa5da4a151bf89026422b94f4cad98331014c7f0cd9, 12204 bytes. Confirm the three new files match app/review-report-v3.json. Confirm the diff in labs/review-report-hardening-pass01/DISPATCHER.diff is the only text between the current dispatcher and the candidate. If any of those bytes differ, stop. Do not apply.

## Apply

Copy labs/review-report-hardening-pass01/librarian.py onto app/librarian.py. Do not edit the historical reporters. The installed command is:

```
python -B app/librarian.py review-report --book ABS --source PAGE --pass 05.NN
```

That command executes the on-disk app/librarian.py. Exit 0 is not a release.

## Rollback

Restore app/librarian.py from evidence/build05.09/rollback-librarian.py. The restored file is sha256 c3a5be3b612c021d95effaa5da4a151bf89026422b94f4cad98331014c7f0cd9, 12204 bytes. Leave the v3 files in place. They refuse the restored dispatcher. v1 and pass03 main accept that restored dispatcher again. v2 and the 05.08 deployment runtime still expect the 05.08 candidate dispatcher.
