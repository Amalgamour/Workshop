# Prime use - review-report app connector

accepted: false
state: staged connector; dispatcher unchanged

## Observe one review

```
python -B app/review_report_tools_v1.py --book D:\Git\lib-build\00.kernel\00.00.10.work --source 0512.prime-review --pass 05.06
```

The same command reads 0521.return-placement pass 05.13. The process does not record, publish, or approve. Exit 0 is not a release. Stdout is the pass03 report object, copied as bytes.

## Proposed shared command

This route is not selected. After a separate review the command would be:

```
python -B app/librarian.py review-report --book ABS --source PAGE --pass 05.NN
```

The exact diff and the rollback are in evidence/build05.07/INTEGRATION.md and labs/review-report-app-pass01/DISPATCHER.diff. Applying that diff changes app/librarian.py. The pass01 pin and this connector then refuse that file. This pack does not update the pin.

## Harness

labs/review-report-app-pass01/invoke.py checks the on-disk dispatcher hash, then executes the proposed source with __file__ set to app/librarian.py. Running the lab librarian.py file directly is not an install.

## Limit

The connector checks the reporter import chain and the pass01 dependency cut, then starts one pass03 process. It adds no report field. Verified physical files stay unknown for the reason the reporter already carries. Custody stays the review's custody. This note does not file 0112.prime-review.
