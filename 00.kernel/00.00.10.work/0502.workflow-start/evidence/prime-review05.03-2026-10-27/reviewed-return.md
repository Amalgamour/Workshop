# 05 — Complete Other books inspection
version: 001
Authorization: draft — 2026-10-26
who: Codex Prime
state: draft; awaiting Director release
Face: 05
PPPP: 0502
book: 00.00.10.work
keyword: workflow-start

## Assignment
Executor: Claude Colab. Reviewer: Codex Prime. Release: PENDING. Claim: PENDING.
Repair OR-01 from 05.02 Prime Review; preserve the working published-tree checker.
Read the review, exact reviewed return, verification and independent probe JSON.

## #01 — Notes and narrow repair
Use new 06.04.md notes. Preserve the current code/evidence before the fix.
parse_contents must account for the complete declared Other books section up to
the next heading or EOF, rather than inspect its first line and ignore the rest.
Either support a precisely documented multiline form or refuse unsupported extra
section content with exit 2. Do not extend this into arbitrary prose/link crawling.
Within the supported reference-list form, do not silently skip malformed or
unconsumed reference text and call the result clean. Retain the existing known
trailing explanatory sentence only through an explicit documented rule.

## #02 — Reproduce and verify
Reproduce Prime's committed fixture: append the explicit missing reference as a
second line in Other books; current code returns clean. Keep failure-before.
After repair, require either its missing-reference finding or unsupported refusal,
never clean. Cover additional same-line malformed reference text as well, proving
it cannot be silently dropped; preserve the valid existing local format and
section boundaries. Run the existing 14 tests and focused regressions in disposable
repositories. Repeat the pinned historical/current checks and record any findings.
No shared Git mutation or source-content repairs. Inspect at exact commit SHA.

## #03 — Return
Reread code/docs and notes, preserve prior manifests/evidence, write a new pass02
manifest and return on this page with Did, Blocked, Need; exact hashes, commands,
counts, failure-before/success-after evidence and remaining scope limits.
Allowed changes: this batch, new 06.04.md and evidence/repair05.03/ on this page;
labs/book-orientation-pass01/ only. No rewriting prior batches/reviews/manifests.
No app, bridge, other pages, Observer 06.02, writer, shared records, kernel or Git
writes. Fixture-repository Git init/commits are allowed only in disposable tests.
No model calls, activation or gate wiring.

## Return — Claude
Release: the Director, chat 2026-10-26: "I release these two batches. Run them in this order and return separately on each page: 1. Independent review of Grok's fixture-boundary repair: D:\Git\lib-build\00.kernel\00.00.10.work\0504.app-entry\05.03.md 2. Repair the orientation checker's false-clean finding OR-01: D:\Git\lib-build\00.kernel\00.00.10.work\0502.workflow-start\05.03.md Follow each batch's scope. Do not edit the app during its review. Preserve Grok's work and the Observer's reserved review page. No shared Git writes, integration, activation or model calls. Return both for Codex Prime review."
Claim: claude-opus-5-5 (Anthropic), Colab, claimed 2026-10-26T18:32-05:00.
Execution: RETURNED for Codex Prime review, 2026-10-26. No shared Git write, no source-content repair, no app, bridge, writer, kernel or shared-record change, no model call, no gate wiring. 06.02.md (Observer) was not touched; it does not exist on this page.

Did:
- Read the 05.02 Prime review, the reviewed return and the Prime's evidence. Its SHA256SUMS.txt verifies 9 of 9. orientation-extra-line.json shows exit 0, result clean.
- Preserved first: the pass01 lab, 7 of 7 manifest files plus the manifest, copied unchanged to evidence/repair05.03/before/. It verifies against its own SHA256SUMS.txt.
- Wrote the notes before the code: 06.04.md (sha256 60ceef67…), with cause I03, contract C01-C06, outcomes O01-O06.
- Reproduced the failure before the repair: repro.py ran 15 committed fixtures through a copy of the pass01 tool. 11 came back clean where the contract requires a finding or a refusal (failure-before.json, sha256 c4f99105…). Among them: R01, the Prime's fixture byte for byte (clean, 2 references); R02, an unlabelled missing path on the same line; R15, a valid two-line form with a missing book on line 2.
- Repaired parse_contents in labs/book-orientation-pass01/check_book.py. The new parse_other_books accounts for the complete section, from its heading to the next Markdown heading or the end of the face. The supported, documented multiline form: each nonblank line holds one or more ``Label: `path`.`` items joined by single spaces; blank lines are allowed; the heading is exactly `## Other books`, once. The known sentence `Each lists what it holds.` is accepted by one explicit rule: once, at the end of the section's last nonblank line. Any other text refuses with exit 2 and names the line. A second or near-miss heading refuses. Nothing after the next heading is read; there is no prose or link crawl. The Pages table, Book files, selection, Git custody, findings and exit codes are unchanged.
- Tests: 14 earlier plus 3 new (OR-01 exactly; the multiline form and section boundary, 3 cases; 12 refusal variants). run_tool now also requires the tool's stderr to be empty, see "Unsure".
- The README states the form and the rule; the module docstring says the same.
Blocked: nothing.
Need: nothing from the Director for this batch.

Hashes:
- Pass02 lab manifest: evidence/SHA256SUMS.pass02.txt, sha256 bab50801ca17f8473d81bebc9bacbb9b7eb98d8111432550159b279342bfb6f2. Files: check_book.py fc16d2f6…; tests/test_check_book.py 57709ad1…; README.md d06ca803…; .gitignore 8da0a2bb… (unchanged); the preserved pass01 manifest evidence/SHA256SUMS.txt 06168454… and the pass01 test logs; tests-pass02-devmode.txt 3ad14a3d…; tests-pass02-default.txt 8b80848e….
- Page evidence: evidence/repair05.03/SHA256SUMS.txt, sha256 3ddd237110905b2c2bb3612eca0e99e7f37636718089a917341b625996fa6547. Files: repro.py, demos.py, failure-before.json, success-after.json (d08ad2e0…), tests-warncheck.txt, and demos/ (4 reports plus demos-summary.json).
- The pass01 manifest is preserved unchanged and no longer matches the three edited files. Their pass01 bytes are in before/.

Commands, all in disposable copies under the session scratchpad except the read-only demonstrations:
`python -B -X dev tests/test_check_book.py -v` and `python -B tests/test_check_book.py -v` (from the lab copy)
`python -B -W error repro.py <lab-copy> <out.json>`
`python -B demos.py <lab-copy> D:\Git\lib-build <out-dir>` (each run is `check_book.py --root D:\Git\lib-build --revision <sha> --book 00.kernel/00.00.10.work --json [--contents 0011.contents/01.002.md]`)

Counts and results:
- Suite: 17 run, OK in dev mode and in default mode, 0 bytecode.
- repro after the repair: 15 of 15 meet the contract. R01 and R15 give missing-other-book (exit 1). R02-R05 and R08-R13 refuse (exit 2). R06 (a later heading ends the section), R07 (a valid two-line form) and R14 (the existing committed form) stay clean.
- Pinned checks with the repaired tool, unchanged from 05.02 where pinned:
  - a5853b7 selected 01.001: extra-file 01.002.md, extra-page.
  - a5853b7 with --contents 01.002: extra-file 01.002.md, missing-page.
  - 15b9cceb: missing-page.
  - Current HEAD d3bcdab: extra-file 05.02.md, extra-file 06.02.md, count-mismatch evidence/, missing-page, consistent with the Prime's review.
  - Every run: exit 1, empty stderr, other_books 2.
- The checkout's HEAD, index, status and refs fingerprints were identical before and after those runs (demos-summary.json). HEAD stays d3bcdab, and the index stays e2f6591e….

Unsure:
- My first repair put backslash-backquote escapes in the docstring, a SyntaxWarning. The suite passed anyway, because run_tool discarded the tool's stderr. That gap also existed in pass 01, so pass 01's "0 warnings" covered the test process only. Fixed: the docstring is corrected, and run_tool now asserts empty stderr. Control: the warning restored in a copy fails 39 checks (tests-warncheck.txt).
- One recorded deviation (06.04 O06): the label grammar is tighter than pass 01's, with no trailing space before the colon. Published faces are unaffected.
- Trailing whitespace on a reference line now refuses. That is strict on purpose; Prime may prefer to tolerate it.

Remaining scope limits:
- Only the Pages table, Book files and the Other books section are covered.
- Text in the Pages section between the table and Book files, and the rest of the face, is still not inspected. That is unchanged and out of OR-01's scope.
- The pointer and the reference form are this book's local provisional format, not kernel grammar.
- Nested page layouts and gitlinks are not modelled.
- A clean result is advisory. The checker is still not wired into any gate.
Overflow: "Book files:" is found by scanning every line after the table, not within a declared section. Parked, not changed. One thing I would have done differently: assert empty stderr in pass 01's helper from the start.

## Review — Codex Prime
PENDING.
