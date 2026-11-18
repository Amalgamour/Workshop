# Supported schema and types - 0512.prime-review/05.09

accepted: false
schema: review-report/3
contract: review-report-hardening/1

The report schema stays review-report/3. On a valid coherent source the JSON matches the accepted pass03 projection aside from code_root. The keys envelope_withheld, historical_supplied, invalid_rows, raw_rows, measurement_withheld, and size_observation appear only on the rejected or malformed paths in evidence/build05.09/CONTRACT.md.

The supported current-cut values come from labs/workbook-review-pass01/workbook.py flags() and descriptor_facts():

| Field | Type | Supported value |
| --- | --- | --- |
| accepted | bool | false |
| approved | bool | false |
| authority | string | none |
| closes_work | bool | false |
| releases_action | bool | false |
| task_association | string | not-established |
| action_released | bool | false |

action_released is the reporter's copy of a validated releases_action. A bool is a distinct type from an int. A supported false or none remains the constructor's advisory flag. The report stays read-only.

Exit 0 is the readable state. Exit 1 is stale, held, not-recorded, or identity mismatch, and the stdout is one JSON object. Exit 2 is refusal. unique_files is absent. physical_files count and bytes stay null, with provenance not-established. tests_note is an object. Custody stays the review's custody.
