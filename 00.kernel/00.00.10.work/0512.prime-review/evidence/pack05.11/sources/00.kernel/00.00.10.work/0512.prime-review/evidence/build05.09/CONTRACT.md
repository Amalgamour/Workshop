# Contract - review-report hardening before activation

contract: review-report-hardening/1
date: 2026-11-03
executor: Grok-1
reviewer: Codex Prime
accepted: false
activated: false
state: pre-code; locked before the repair

This contract is the pre-code agreement for 0512.prime-review/05.09. It is not acceptance, not activation, and not a release. The repair that follows this file has to match these rules. A later test failure does not revise this file.

## Freeze

evidence/pack05.09/source-manifest.json was verified before these notes. Schema prime-pack-inputs/1. 97 files. bad 0. missing live 0. missing snapshot 0. Manifest sha256 114cadf253a8b23b6841d7868059d2919f3d7629e68142b8f5e8661f0e9c74c2, 28421 bytes. 05.09.md is outside that manifest. HEAD 960d20c5290656095df8457b1740d2d5e586b111. Branch workshop. Index empty. Porcelain dirt is context and is not a freeze failure. The frozen bytes are not repinned.

## Known reproductions

Both were run through labs/review-report-deployment-pass01/report.py on synthetic core data before the repair. They are known reproductions, not independent tests. They are not evidence that the validated core emitted these values or granted authority.

B-05. A report carrying authority "Director" and action_released {"x": 1} was passed to the inherited mark_unstable. After the call the state was held and both values were still present. Accepted false and approved false stayed as well.

B-01. Four intake rows, one dict and three non-dicts ("garbage", 7, null), with measurement "complete", produced one kept row. intake_roles count was 1 and count_state was measured. No invalid-row count was recorded.

## Supported envelope

The supported current-cut envelope is the value set written by labs/workbook-review-pass01/workbook.py flags() and descriptor_facts(), which result() applies before caller extras. No result() call site in that module or in the pass02 workbook overrides these keys:

- accepted: JSON false
- approved: JSON false
- authority: the string none
- closes_work: JSON false
- releases_action: JSON false
- task_association: the string not-established

action_released is not a core field. The reporter may set it from a validated releases_action. Its only supported projected value is JSON false.

A bool is not an int. A string, object, array, number, or null is not one of these values. Unsupported or malformed envelope data is unverified before projection. It is not displayed as a verified authority or action state. A supported false or none is the core constructor's advisory flag. It is not Director approval. The report stays read-only.

## Rejected observations

When source identity is unstable, mismatched, or unestablished, the current-cut fields accepted, approved, authority, closes_work, releases_action, task_association, and action_released are withheld. Withheld means JSON null. Null is unknown. Unknown is not false.

The withheld fields are named on envelope_withheld with provenance withheld-current-cut. That object is absent when the observation is coherent and the envelope validated.

A held or mismatched result does not keep projecting the cut it rejected. Historical judgment values that were already supplied are copied to historical_supplied with provenance historical-supplied before the current judgment is cleared. They are not a current judgment. If none were supplied, that object is absent.

These paths withhold the envelope:

- observation status unstable, including mark_unstable
- observation status mismatch, including hold_mismatch and a core identity or digest mismatch
- an unreadable or bad cut that is not the not-recorded case below

These paths keep a validated envelope:

- coherent readable
- coherent historical stale, state stale
- not-recorded, including an absent journal whose observation status is unreadable and whose stable flag is null. The validated advisory envelope remains. This is not a rejected current cut
- coherent held only because no judgment is recorded while the cut itself is stable

## Rows and sizes

A non-dict intake row is retained. invalid_rows.count is the number retained, invalid_rows.dropped is false, and raw_rows keeps the source list. Affected counts, byte totals, and hash totals become unknown. measurement may still show the core's word. measurement_withheld says that word is not a complete measured total. The reporter does not claim the filtered dicts are that total.

A verified empty list with measurement complete may report count 0. Absent or non-list rows stay count null. They are not rewritten to a declared zero.

Null and missing sizes are a missing-size reason, not a disagreement between two int sizes. A bool size is not 1. A negative size is not a measured total. Both use the reason "negative or bool size is not a valid measurement" and size_observation. Two different non-negative int sizes keep the existing conflict reason. size_observation is absent on that path and on a clean path.

A content hash is a 64-character lowercase sha256, which is what the core hashlib hex digest is. Uppercase or other strings are not rewritten. They are not hash matches. They count as not verified.

## Stale and unreadable cuts

Historical staleness is state stale, observation coherent, stale true, envelope still projected when it validated. Integrity failure is state held, observation mismatch, stale true, envelope withheld. Movement during the observation is state held, observation unstable, stale true, envelope withheld. Those existing fields are the distinction. No new authority ledger is added.

stable true requires both the bound cut and the recheck to be readable objects. Two unreadable reads do not establish stable true; stable stays null and the status is unreadable. One unreadable side is stable false and the changed list includes cut. A missing or non-bool core stale flag is not rewritten into a new hold. That label question is not a second policy.

## Report shape

Schema stays review-report/3. On a valid coherent source the JSON matches the accepted pass03 projection aside from code_root. The keys envelope_withheld, historical_supplied, invalid_rows, raw_rows, measurement_withheld, and size_observation appear only on the rejected or malformed paths above.

Exit 0 remains readable, not approval, custody, or release. Exit 1 remains stale, held, not-recorded, or identity mismatch. Exit 2 remains refusal.

## Candidate

New files only: app/review_report_tools_v3.py, app/review-report-v3.json, and labs/review-report-hardening-pass01. v1, v2, pass01, pass02, pass03, and the 05.08 deployment files stay byte-for-byte. The active app/librarian.py stays the current dispatcher.

The candidate librarian loads the v3 connector by filename. The v3 connector pins that candidate librarian, every pin the v2 connector pinned, and the new runtime. It does not pin itself. The runtime pins that same set except its own file. It does not call pass01.check_pins and it does not launch pass03 main. It loads pass03 and patches the loaded envelope, row, and observation functions in that process only.

Historical pass03, v1, v2, and the 05.08 deployment runtime still refuse this candidate dispatcher. That refusal stays.

The proof command is python -B on the candidate root's own app/librarian.py review-report. Direct execution of the lab librarian is not an install. The public command has no --code-root. The helper root inside labs/workbook-review-pass03/workbook.py stays D:\Git\lib-build.

Selection is not applied. A later selection would replace only app/librarian.py with the candidate file and would require the v3 connector, the v3 declaration, and the hardening runtime to be present. Rollback restores the active dispatcher from evidence/build05.09/rollback-librarian.py. This pack does not select, approve, or release.
