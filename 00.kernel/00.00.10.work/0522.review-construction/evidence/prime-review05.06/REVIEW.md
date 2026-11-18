# Prime review — 0522.review-construction / 05.06
Date: 2026-11-01. Reviewer: Codex Prime.
Disposition: correction required; do not select constructor pass03 in the app/loop yet.

## What works
The isolated successor adds supplied disposition/pass/goal state, preserves /1 rendering and task binding, displays decision source hashes, distinguishes null from an empty decision list, and adds read-only target inspection. State remains explicitly supplied, not an approval or an independently validated cycle judgment. Retaining the judgment despite a later render block remains the Director's selected behavior.

## Independent checks
All 78 frozen sources and snapshots match their pins and current bytes. All 31 listed artifacts match. Inspected the entire pass02-to-pass03 code delta and focused tests, contract, submission and verification. On Python 3.12.14 the 11-test suite ran: 10 passed, 1 Windows symlink-privilege skip; no failures. Preserve the skip, not a claim of exercised symlink protection.

Independently replayed the one unchanged-cycle /2-envelope experiment in a new disposable copy, with outputs under this Prime evidence directory. The original evidence writer was copied to a new location, its fixture deletion replaced with retention, and no original evidence was overwritten. record/read/bind succeeded; pass02/candidate binding equality held; target page bytes stayed unchanged. This proves that one envelope case, not general app integration or coupling validation.

## Defects found beyond the submitted tests
G01 — inspect mishandles CRLF task_binding. The same synthetic review with the expected binding returns constructed-same-binding under LF but existing-review and binding=null under CRLF. The new regex anchors the digest at end of line without accepting CRLF. Both targets remained byte-identical. Repair classification with newline-aware parsing while preserving raw bytes/hashes, and test actual rendered LF and CRLF sections. A matching binding still must not authorize a changed body overwrite.

G02 — malformed enum types produce an uncaught traceback. supplied_review_state.disposition=[] raises TypeError in set membership. Confirmed through the actual preview CLI: exit 1 with traceback rather than the promised bounded refusal; target unchanged. Validate enum value types before membership for all new fields, refuse arrays/objects and other invalid JSON shapes through the normal refusal path, and test CLI output and writes-none. No need to redesign state semantics.

## Limits retained
The constructor does not compare supplied state with hash-verified cycle record.json; that belongs in the later loop successor. ROOT remains the selected literal checkout path, so this is not a portability repair. No active app/loop/cycle/pin changed. Custody on matching 0122 remains pending; no receipt or new allocation is invented.

## Next bounded action
Repair G01 and G02 in a new isolated constructor successor with focused regression checks. Keep the successful /1 and binding behavior. Then review the repaired constructor before selecting it in the planned loop/door successor. No new pack or execution release is created by this review; the Director requested reviews before assignments.

Evidence: evidence/prime-review05.06/ including checks.json, raw suite results, malformed-cli evidence and cycle-replay/.
