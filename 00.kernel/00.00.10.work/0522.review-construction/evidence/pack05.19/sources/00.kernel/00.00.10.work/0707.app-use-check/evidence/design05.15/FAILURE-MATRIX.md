# Failure matrix — runs and case classes (0707/05.15)
who: claude-opus-5-5. **Every row is a lab result on retained external fixtures** (`D:/librarian/temp/task-agreement-0715/…`, local retention, not an archive). **No row is independent coverage or production behavior.**

## Runs
| Run | Suite | Test file sha256 | Result | First failure and notes |
|---|---|---|---|---|
| new-run01 | `tests/test_ta2.py` | 629f9750… | 21 PASS (exit 0) | **Two test defects, found by reviewing my own results:** KR-pointer passed **vacuously** (pass01 stopped at construct, and the assertion defaulted to true); C-helper-pin claimed a refusal it never exercised. Both were corrected in the test file. **The tool was unchanged** |
| new-run02 | `tests/test_ta2.py` | 87a25959… | **21 PASS** (exit 0) | KR-pointer now asserts the positive truncation evidence (pass01 "'Scope' occurs 0 times" because its cut ends at the fenced pointer); C-helper-pin exercises a wrong-pin refusal |
| compat16-run01 | `compat16/tests/test_ta.py` (**byte-identical** to pass01, 8e653250…) through the shim | 16 PASS (exit 0) | **adapted author cases** (the shim inserts `--lab-root`); T08 symlink sub-check still SKIP (no privilege) |

## Case classes (new-run02)
| Class | Cases | Result |
|---|---|---|
| **known-failure reproduction** (Prime 06.14) | KR-tilde, KR-long_backtick, KR-indented (pass01 count 2 → pass02 resolves); KR-pointer (pass01 cut truncated → pass02 true cut); KR-binding-path (pass01 compare `current` → pass02 refused "escape", before any read) | 5 PASS |
| author test: J1 | A-unclosed (refused), A-longer-close (closes), A-indented-heading (refused) | 3 PASS |
| author test: J2 | A-pack-path (compare and inspect refused), A-binding-shape (missing field / old version / basis misuse refused) | 2 PASS |
| author test: J3 | A-room (outside, sibling-prefix, in-book refused with nothing created; occupied untouched; inside ok), A-mock-checkout (**a mocked boundary;** no real live path probed), A-junction (**junctions really created;** output and source through a junction refused) | 3 PASS |
| author test: read-only and flow | A-readonly; **W-flow** (construct → assemble → freeze-copy → bind → inspect → compare; own pointer `current`; outside-cut revocation `context-changed`; nothing written outside the room; CRLF) | 2 PASS |
| compat observation | C-lf-six, C-crlf, C-absent-empty, C-hyphen, C-fenced-goal, C-helper-pin | 6 PASS (**observed as is,** see `COMPAT.md`) |

**Environment skips:** T08 symlink (adapted suite). A-junction ran for real; **symlinks were not exercised.**
