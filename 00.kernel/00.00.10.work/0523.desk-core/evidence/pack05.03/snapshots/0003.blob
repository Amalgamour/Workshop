# Prime review - 0523/05.02

date: 2026-10-31
who: Codex Prime
reviewed_commit: eeefbeced8587991e4b4a80ce6620ea78a90c1e3
disposition: substantially improved exploratory prototype; Windows repair remains; no production integration

### Verified result
All 33 original pins, 16 repair snapshot pins and 23 declared artifact rows
match. Changed paths stay within the repair scope. The builder reports 15/15
on Linux Python 3.11.2, with supplementary 3.10 checks; Prime did not independently
repeat those Linux runs. Prime ran the unmodified exact Git export on Windows
Python 3.12.14: 15 tests, 13 passed, two failed, no skips. The native CLI demo
succeeded with all twelve expected exits. Raw commands/results and source are
preserved under evidence/prime-review05.02. The review export is not deployed.

### Improvements independently confirmed
Binary writes preserve bytes and occupied temporary files are refused. Revision
history preserves the original task and face bytes. A separate native serial
API probe retrieved prior task wording in history, refused an old return after
the task changed (stale-return), and produced different task bindings for equal
text at different source pages. Leading-N identity tests pass. Actual production
Windows locking was independently checked using a child process with msvcrt:
the child could not acquire the parent-held byte lock. This is a useful lock
exclusion check, not a proof of concurrent race freedom or exhaustive crash safety.
The suite's interruption case passes; not every write interruption was injected.

### CC-05 - lock regression test remains Unix-only
app/desk_core/test_repair.py test_lock_is_held_and_windows_lock_is_not_a_no_op
launches a child that imports fcntl unconditionally. It fails on Windows even
though the repaired runtime uses msvcrt and the independent native probe passes.
Make the child probe platform-aware and preserve a real contention check on
both platforms. Do not replace locking with a no-op to make the test pass.

### CC-06 - Windows newline conversion hides headings
app/desk_core/test_loop.py test_review_without_return_duplicate_key_and_projection
rewrites a face using write_text with default Windows newline translation. LF
becomes CRLF. The reader's exact-byte section matching then fails to recognize
headings: show returns exit 2 instead of the expected assignment-conflict result.
This is both a test isolation problem and a reader portability boundary. Mutate
bytes without unrelated newline conversion for the assignment-conflict test, and
add a separate CRLF test. Prefer recognizing CRLF headings while preserving source
bytes; any explicit refusal must name the actual format problem rather than
misreport a missing section. Do not globally normalize sealed records or hashes.

### Assessment and next bounded action
The repair addressed the important history and stale-return defects and now
executes its synthetic loop on our Windows host. That is meaningful progress,
not merely more Linux-only test claims. Remaining failures prevent describing
the Windows suite as clean. If another prototype pass is run, limit it to CC-05,
CC-06 and regressions. No architecture rewrite is justified by these failures.
This cloud exercise remains exploratory, as the Director clarified. It does not
replace the local app work, authorize adoption of its schemas, prove actual model
dispatch, or complete live return migration. No production app source was copied.
Matching 0123 custody remains pending reviewed placement; this page and evidence
retain the cloud handback without inventing a completed receipt.
