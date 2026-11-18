# Submission — 0523/05.03 reliability lab
date: 2026-11-01
who: Grok Build (xAI), grok.com GitHub-connected builder
state: exploratory prototype returned for Prime review; not accepted

## Did
Fast-forwarded builder/grok-core-pass01 to 42563e669457a46b73f0be8c8caf30d9d16c819d.
Pack pins: 19 of 19 at eeefbeced8587991e4b4a80ce6620ea78a90c1e3.
Notes commit 3309b0e549878340b581687520aa86cced6e3b3b.
Implementation 46505955f141196db187d491f301d29156389f96.

CC-05. The lock child is a separate process. POSIX uses `fcntl` nonblocking.
Windows source uses `msvcrt.LK_NBLCK` for one byte. The parent holds `file_lock`.
This host ran the POSIX child. It was excluded. The Windows child was not run.
CC-06. The tamper test writes bytes. LF and CRLF headings are recognized.
CR-only headings refuse `face-format` / `cr-only`. Sealed bytes are not
normalized. A section replace leaves bytes outside that section unchanged.
UTF-8 `café` round-trips. Occupied temporary files are still refused.

Revision crashes use `DESK_CORE_FAULT`, which is not a request field.
`os._exit(91)` runs at nine boundaries. A new process `show` then `recover`
keeps A, restores A from the preserved bytes, or writes `selected.json` only
when both live files already match one sealed proposal. A different request
is `revision-unfinished`. A missing staged file is `revision-corrupt` and the
other files stay. The same request does not open a second history directory.

Linux Python 3.11.2: 22 tests, 0 failed, about 14.9 seconds.
Linux Python 3.10.22: 22 tests, 0 failed, about 19.6 seconds.
Demo exits `[0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0]`.
Transcripts: evidence/build05.03/unittest.txt, unittest-py310.txt,
demo-transcript.txt, fault-matrix.json, fault-matrix.md.

Fresh-process reproduction, from a disposable book that already has task A:

```text
DESK_CORE_FAULT=after-task-replacement python3.11 -B -m app.desk_core revise-task --book /absolute/book --input revise.json
python3.11 -B -m app.desk_core show --book /absolute/book --page 0523 --subject sample --pass 01
python3.11 -B -m app.desk_core recover --book /absolute/book --page 0523 --subject sample --pass 01
```

The first command exits 91. `show` reports conflict and not complete.
`recover` restores the previous pair and leaves the proposal in history.

## Blocked
Windows Python 3.12+ was not installed and was not run. The Windows lock
child and the Windows CRLF suite are pending Prime. No runtime was installed.
Live matching-line custody is still blocked by `0123.boot-validation-0508`.
No production integration.

## Need
Prime review, including the native Windows rerun of the unmodified tree.
No other input is required to inspect the Linux evidence.

## Not claimed
This is not the normal app and it was not copied into it. The lesson for that
app is the check, not this package: a heading in another newline is not
missing, one replaced file is not a selected pair, and recovery must name
whether it kept, restored, or committed an already matching proposal.
`accepted` is false. A receipt is not a review. A review is not approval.
These tests do not prove power loss, all filesystems, OS isolation, or race
freedom. A green Linux run is not Windows acceptance.
