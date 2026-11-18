# Worker B, unit 1: cold audit of report evidence and identity handling
Read ../COMMON.md first; it applies in full.

## Purpose
Independently audit the frozen, accepted review-report reader for failure paths not already known.

## Read, in the source room (/workspace/prima/run0502/source-room)
- labs/review-report-pass01/report.py
- labs/review-report-pass02/report.py
- labs/review-report-pass03/report.py, plus its tests/, README.md and PRIME-USE.md
- app/review_report_tools_v1.py
- app/review-report-v1.json, plus any relevant contracts or data in the room

## Focus
- Whether observations are coherent.
- Separation of stale data from history.
- Counts: declared, measured, content, addressed, and unknown-physical.
- Null or invalid metadata.
- Authority projection.

## Already known (not new)
These are already assigned locally; don't present them as new findings:
- the dispatcher-pin deployment blocker
- the pre-filing PENDING test assumption

Look for different failure paths, or clearly scope the questions you can't resolve.
