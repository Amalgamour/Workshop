# Prime use - review-report hardening candidate

accepted: false
state: staged candidate; active dispatcher unchanged

## Proof command

On a candidate root where app/librarian.py is the hardening file and the v3 files are present:

```
python -B app/librarian.py review-report --book ABS --source PAGE --pass 05.NN
```

The process is that root's app/librarian.py. The connector derives the code root from the installed app. It does not take a public --code-root. Exit 0 is not a release.

The active D:\Git\lib-build app is unchanged. Running app/review_report_tools_v3.py there refuses the current dispatcher because the pin expects the candidate bytes. That refusal is the unselected state.

## Candidate identity

labs/review-report-hardening-pass01/librarian.py is 12804 bytes, sha256 f1d23d455f20319e3f430d345b2893bda039fd8c84be4f3691b4e4be123b8983. It is the accepted deployment command hunk with the review-report door loading review_report_tools_v3.py. The 05.08 dispatcher d37dd14ccb921f92ff1a05c00890d57ee0f3d9f27d766bd86d81861abdd80a52 remains the accepted deployment candidate and is not this file.

The runtime is labs/review-report-hardening-pass01/report.py, 18139 bytes, sha256 27e513f462b241e9c7298d3077d50d08ea5ac703a6f2d0769dc5935fcb51b58b.

## Selection and rollback

Selection is not applied. A later selection copies that librarian.py onto app/librarian.py and keeps the v3 connector, the v3 declaration, and the hardening runtime. It does not change v1, v2, pass01, pass02, pass03, or the 05.08 deployment files. Those historical checks still refuse the replaced dispatcher. Rollback restores evidence/build05.09/rollback-librarian.py, sha256 c3a5be3b612c021d95effaa5da4a151bf89026422b94f4cad98331014c7f0cd9, 12204 bytes. The exact steps are in INTEGRATION.md. This note does not file 0112.prime-review.

## Helper root

labs/workbook-review-pass03/workbook.py still loads pass02 from D:\Git\lib-build. A candidate copy of that module does the same. The source root and that helper root stay distinct.
