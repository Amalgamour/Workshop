# Prime review — structured local return inspection
Date: 2026-10-27. Reviewer: Codex Prime.
Disposition: ACCEPTED for explicit valid return-band members, with RI-01/02 follow-up.
Inspector SHA-256: 0066bc87f60c95371a6421313b81c8d5d05e551a50bd6f090cef33188b22f534.

Independent disposable suite: 12 tests, 11 passed, one directory-symlink privilege
skip. A fresh copied-helper fixture independently produced a complete structured
read whose receipt hash matched actual bytes, then an incomplete read after
receipt mutation. Capture identity was null on damage; both reads changed nothing.
All seven declared outputs of builder-local 0110 match; fresh capture verify passes.
The accepted capture helper remains exactly 8f3da5c6... and its code/tests were
not edited. Loading executes the actual hash-checked bytes, not a reread of the
path after checking. No duplicate validator, receipt prose parser, Git/network
call, allocation, repair or claim of external review/acceptance/publication.

RI-01 (small boundary diagnostic): member band bounds are checked after the
missing-path return. Absent 0100.door, 0200.outside and 9999.outside all report
missing/exit1 rather than refused/exit2. None exposes capture identity or certifies
a package. Move the existing range validation before existence classification;
prove equal refusal for absent and existing out-of-band paths. Do not broaden
the band or change the core. This finding does not negate verified valid-member
integrity behavior; freeze the consumer pin after its bounded correction.
RI-02 (example clarity): the worked synthetic CONTRACT example swaps the meaning
of origin book/page (0508.return-capture and 05.04.md). These are caller-provided
metadata, not values verified for historical truth by the reader. Regenerate the
worked example using book 00.00.10.work, page 0508.return-capture, batch 05.04,
with fresh fixture hashes. Retain the old contract as historical submitted bytes.

Next bounded draft 0508/05.05 fixes those two points only. No live consumer wiring
is added here. Claude's active boot prototype explicitly excludes this unaccepted
future pin and does not need interrupting. Evidence: verification.json and suite.txt.
