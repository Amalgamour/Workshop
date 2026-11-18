# review-report-pass01

Read-only projection of one selected workbook review. The command is:

```
python -B labs/review-report-pass01/report.py --code-root ABS --book ABS --source PAGE --pass 05.NN
```

Stdout is one JSON object, schema review-report/1. The `projection` field is the readable view of that same object. Exit 0 means the selected record was readable and not stale. It does not approve, publish, file custody, or release work.

The process calls librarian review-loop inspect, read, and recover. It does not call prepare, form, record, or publish. Attention is shown only when record.json matches the journal hash and the judgment matches the core.

Author tests:

```
python -B labs/review-report-pass01/tests/test_report.py
```

Those tests are not an independent run. The integration note is PRIME-USE.md. Accepted is false.
