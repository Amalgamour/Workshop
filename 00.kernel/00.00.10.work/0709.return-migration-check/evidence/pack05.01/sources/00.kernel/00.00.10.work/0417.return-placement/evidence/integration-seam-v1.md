# Integration seam v1 - explicit placed return descriptor
date: 2026-10-31
who: Codex Prime
state: common integration input contract for 0521/05.03 and 0522/05.03

This is an adapter contract, not a new address axis or permission grant.
Descriptor JSON uses schema return-line-descriptor/1 with these exact keys:
schema, origin, route, target_page, return_path, custody_path, receipt_path,
manifest_path, submission_id, custody_format, receipt_sha256, return_sha256,
return_bytes, state, verification.
origin has exact book, page and batch (05.NN). route is matched-workflow-return-line
or page-local-colab. N5NN maps to N1NN with the same N/NN/subject. N7NN stays local.
All paths are explicit normalized paths relative to the declared work-book root.
No arbitrary absolute path overrides, newest version selection or sequential slot.
custody_format is legacy-relocated/1 or return-line-capture/1. The implementation
documents the exact schema of the latter; do not relabel /1 sealed metadata.
receipt_sha256 is the SHA256 of actual receipt bytes, not a self-asserted label.
state is complete, reserved, incomplete or conflict. Missing bytes have null hashes
and lengths, not fabricated empty-file hashes. Unresolved items remain visible.
verification has exact tool_path, tool_sha256, result and evidence_path, all explicit;
it records observed checks, not authentication or a boolean granting authority.

Consumers validate origin-to-route, matching line/subject/pass, descriptor shape,
actual receipt/return/manifest/payload identities and task/evidence binding. A stated
complete result never replaces those checks. Legacy-relocated inputs preserve their
original destination and use declared relocation provenance plus exact custody
verification. Wrong/missing sources are refused or held with preserved reasons.

Both lanes must publish a minimal synthetic descriptor fixture and raw verified
evidence using this shape. If a substantive change is necessary, report it to Prime
before changing the shared contract. Do not consume the other lane's live output.
Local constructor/cycle fixtures can use supplied descriptors with honest synthetic
provenance; they must not claim real custody or model execution.
