# Prime use - review-report deployment candidate

accepted: false
state: staged candidate; active dispatcher unchanged

## Proof command

On a candidate root where app/librarian.py is the deployment file and the v2 files are present:

```
python -B app/librarian.py review-report --book ABS --source PAGE --pass 05.NN
```

The process is that root's app/librarian.py. The connector derives the code root from the installed app. It does not take a public --code-root. Exit 0 is not a release.

The active D:\Git\lib-build app is unchanged. Running app/review_report_tools_v2.py there refuses the current dispatcher because the pin expects the candidate bytes. That refusal is the unselected state.

## Candidate identity

labs/review-report-deployment-pass01/librarian.py is 12805 bytes, sha256 d37dd14ccb921f92ff1a05c00890d57ee0f3d9f27d766bd86d81861abdd80a52. It is the 05.07 command hunk with the review-report door loading review_report_tools_v2.py. The 05.07 file b253a89751a48b64089bb95c4fde3715de00e6dc3c61dd8bad8653051234f3fa remains the known refusal.

## Selection and rollback

Selection copies that librarian.py onto app/librarian.py and keeps the three new pinned files. It does not change v1 or pass01. Rollback restores evidence/build05.08/rollback-librarian.py, sha256 c3a5be3b612c021d95effaa5da4a151bf89026422b94f4cad98331014c7f0cd9, 12204 bytes. The exact steps are in INTEGRATION.md. This note does not file 0112.prime-review.

## Helper root

labs/workbook-review-pass03/workbook.py still loads pass02 from D:\Git\lib-build. A candidate copy of that module does the same. The source root and that helper root stay distinct.
