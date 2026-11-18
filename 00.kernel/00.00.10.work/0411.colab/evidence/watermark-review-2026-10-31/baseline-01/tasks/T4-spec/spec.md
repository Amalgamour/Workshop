# Drop-box intake — spec v1

R01. A submission MUST arrive as one ZIP file no larger than 25 MB.
R02. The ZIP MUST contain `manifest.json` at its root, and MUST NOT contain absolute paths or `..` segments.
R03. Every file listed in `manifest.json` MUST carry its `sha256`; a file present but not listed is an error, not a warning.
R04. Intake MUST reserve the member before capture. A reservation older than 48 hours MAY be released, by the Director only.
R05. The capture step MUST NOT rewrite line endings, and MUST record the original byte count.
R06. If verification fails, the member stays `reserved`, and intake MUST NOT delete the received ZIP.
R07. A member's state is one of `reserved`, `captured`, `verified` or `withdrawn`; no other state is valid.
R08. `withdrawn` is final. A withdrawn member MUST NOT be reused; a new submission takes a new member number.
R09. Intake MAY accept up to 3 submissions per day per sender; a fourth is refused with code `E-RATE`.
R10. Error messages MUST name the rule (for example `R03`) and the file involved, and MUST NOT include file contents.
R11. These rules apply from 2026-11-01. Earlier submissions are read under spec v0 and are not re-checked.
