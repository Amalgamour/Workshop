# PRIME-USE — 0522.review-construction/05.07

Interpreter: C:\Users\misg\AppData\Local\Programs\Python\Python314\python.exe
Python 3.14.0. Commands run with python -B from D:\Git\lib-build.

## Reproduction, separate from the candidate suite

python -B 00.kernel/00.00.10.work/0522.review-construction/evidence/build05.07/reproduce/run.py

The runner exit is 0 because the saved findings list is empty. The inner pass03 results are the defect:

- LF inspect exit 0, state constructed-same-binding, binding ababababababababababababababababababababababababababababababababab, page unchanged, show exit 0.
- CRLF inspect exit 0, state existing-review, binding null, page unchanged, show exit 2.
- preview of supplied disposition [] exit 1. stderr contains TypeError: cannot use 'list' as a set element (unhashable type: 'list'). The target and the fixture tree stayed unchanged.

Those outputs are under evidence/build05.07/reproduce/. The stored logs are LF. The Windows runner wrote CRLF; the text and the exits were left as captured. The retained page and section files keep the original LF or CRLF bytes. pass03 was not edited. Its sha256 remains 6eec5653c6818cfdeb98ffcd929cdf26f0ddf15c3121c703ce795abea6eb755d, 42216 bytes.

## Candidate constructor checks

python -B labs/review-construction-pass04/tests/test_pass04.py

Saved exit 0. 12 tests ran, 11 passed, 1 skipped. The skip is test_symlink_is_refused, WinError 1314. No symlink was created. The checkout-root refusal is a separate test and passed. The log is evidence/build05.07/tests/suite.stderr. It is stored as LF. The Windows runner wrote CRLF.

The suite keeps /1 section text equal to pass02 and pass03, /2 section text equal to pass03, and /1-/2 binding equality with pass02. An actual CRLF apply is inspected by pass04 as constructed-same-binding and by pass03 as existing-review with a null binding. The section hash is the CRLF located bytes. The same binding with a different CRLF body still conflicts, and the page stays unchanged. Malformed enums through preview, apply, and bind exit 2 with `refused:` and no traceback.

## Limits

CONTRACT.md sha256 d112ad4abe02fe9eea79708d06f01f380648d7a66b7ebb9bf4ce43514a4d4251, 4424 bytes, was left as written before the code. Envelope and bind interfaces are unchanged, so this build does not continue into the cycle, the loop, or the door. Do not point those tools at pass04 from this page.

The constructor still does not compare supplied state with hash-verified record.json. constructed-same-binding is not permission to replace a different body. ROOT stays the literal checkout. The symlink refusal did not run. The 05.06 cycle evidence writer was not rerun. Custody on 0122.review-construction stays pending. No receipt was written. 0184 was not allocated. accepted is false. Exit 0 is not Prime review, seating, or app activation.
