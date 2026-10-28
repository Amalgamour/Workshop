# Contract — capture-handoff failure reporting

Schema of the binding, the handoff record, and the failure log stay `clerk-capture-handoff/1`, `clerk-capture-handoff-record/1`, and `clerk-capture-handoff-failure/1`. This contract adds report fields and stdout lines. It does not replace the 05.17 handoff contract. CH-01 and CH-02 guards stay in force.

`perform(binding_path, *, hook=None, pins=None, fault=None)` returns an exit code. `hook` and `pins` stay the existing in-process seams. `fault` is also in-process. The CLI is `handoff.py perform --binding ABS`. It has no fault switch. The module does not import the pinned tools. It launches the current Python executable with `-B`, `shell` false, and the packed script paths. Pins are checked before every launch and before the completed record. A failed pin does not start that tool.

## Capture attempt and later observation

The adapter remembers whether it attempted capture. The child outcome is `captured` only when the capture tool returns the line `result captured` and the bound member line. A non-success return is `returned`. A timeout, or a launch that does not return, stays `unknown`. The attempt is marked before the wait. Absence of a success code is not a claim that the child wrote nothing.

On a failure after an attempt, stdout adds, after the original reason:

- `capture-attempt <member>`
- `capture-child captured`, `capture-child returned`, or `capture-child unknown`
- `observed <relative>` for each direct entry of that member and each file in its `payload` directory, using a forward slash in `payload/<name>`
- `member-written observed` when `return.md`, `manifest.json`, and `receipt.json` were listed
- `member-written partial` when at least one of those three was listed and at least one was not
- `capture-files absent` when the listing succeeded and none of those three is present
- `member-written unknown` when the member cannot be listed safely
- `custody <status>` from a later `return_inspect --json` observation
- `custody unverified` when the pins are bad, the inspection raises, or the bytes cannot be read
- `verify unverified` when the later status is `complete` but verify does not return custody
- `observed-at <utc>`

The later inspection is launched only when `pin_problem` is clear. Verify is launched only when that later status is `complete`. Verify of a reserved member is not used as evidence of zero writes. Exact tool stdout, including a timeout's captured stdout, is appended to `tool_stdout`. A verify refusal is not rewritten into a second validator.

The failure record's `inspect` field is that later observation, or null when it is unverified. The pre-capture reserved inspection is kept only as an earlier phase. `observations` holds:

- `before-capture`, with `at`, `status`, and the earlier `inspect`, when a capture was attempted
- `capture`, with `attempted`, `child`, and the exact capture stdout
- `after-capture`, with `at`, `member_state`, `files`, `custody`, and the later `inspect` or null

`member_state` is `observed`, `partial`, `absent`, or `unknown` from the listing above. `capture` in the record is `{attempted, child, stdout}` and `attempted` is false when this call did not launch capture. `reporting_error` in a successfully written log is null.

The listing reads only the explicit member, one `payload` child, the record directory, and the failure-log path. It does not walk the band. A reparse point, a non-regular entry, or an unreadable entry stops that listing and the outcome is unobserved or unverified. Links are not followed.

## Record files

When the binding parsed, a failure also reports the record directory:

- `record absent` when the directory is not there
- `record unobserved` when it is a link, not a plain directory, or cannot be listed
- `observed-record intent.json` or `record-absent intent.json`
- `observed-record completed.json` or `record-absent completed.json`
- `handoff-complete no`

A partial or unreadable record file is still `observed-record` when the name is a regular file. That line does not mean the handoff completed. `completed.json` is still written only on the success path, after verify, inspect, and the payload comparison. The failure path does not create it and does not delete bytes already there.

Observed capture markers, payload blobs, and present record files are added to the retained paths. Paths are de-duplicated. Pre-existing `01.md` and `reservation.json` are listed as `observed` names and are not treated as adapter writes.

Adapter `writes` stay the record files this call created: `intent`, `completed`, and, on stdout, the failure log. Capture files are observed facts, not adapter writes.

## Failure of the failure log

`try_failure_log` returns a secondary message or None. It does not raise `OSError` or `Refuse`. If the log path already exists, it is retained and the function returns without writing and without applying a fault. If the parent is not a plain directory, the secondary message says so and nothing is written.

Otherwise the log is exclusive-created. `FileExistsError` retains the path. `Refuse` retains the path when any file is present and returns `failure log: <message>`. `OSError` retains the path when any bytes landed and returns `failure log: OSError: <message>`.

The JSON payload is built before that write. A failed write is not rebuilt to include its own error. Stdout inserts `reporting-error <secondary>` after the original reason. Exit is 2. No traceback is printed. An existing log is not overwritten. The original reason remains. A logging failure does not erase earlier writes and does not return `result ok`.

`except OSError` and `except Refuse` are the reporting catches. `FileExistsError` is handled before `OSError`. A programming error is not turned into `result ok`.

Stdout order on a failure is: the original `attention:` or `refused:` line, the reporting-error line when present, the capture and record lines, `retained <path>` lines, `writes <path>` or `writes none`, then `result attention` or `result refused`. Exit 0 remains only a fresh success or an identical completed retry that writes nothing.

## Fault seam

`fault(event)` returns None or one marker: `oserror-before`, `oserror-partial`, `readback`, or `timeout`. Any other marker refuses with `fault returned an unknown marker`. The context is set for the duration of `execute` and is read inside `launch(script, args, pins)` and `write_exclusive`. The launch signature stays those three parameters.

`launch:<command>` accepts only `timeout`. The pin check runs first. A timeout marker or `subprocess.TimeoutExpired` raises `ToolTimeout` and keeps any stdout already captured. The process is not started after a bad pin. The refusal is `tool timed out: <command>`.

`write:<role>` accepts the three write markers. `timeout` on a write refuses as not usable. `oserror-before` raises `OSError` before the file is created. The failure-log message is `injected failure-log write error`. The intent and completed message is `injected record write error`. `oserror-partial` exclusive-creates the file, writes `partial\n`, fsyncs, and raises that `OSError`, leaving those bytes. `readback` writes the full payload and then raises the existing attention `record write did not land intact: <name>` without deleting those bytes. The failure-log path checks `lexists` before the marker is applied, so a retry does not inject into or overwrite an existing log.

A readback refusal is not success (`handoff-complete no`, exit 2) even if the retained bytes are the full payload. A later call uses the existing completed-record check. If those bytes are a matching completed record, that later call is the read-only identical retry and does not capture again. If they are not readable, the later call refuses `completed handoff record is not readable` and does not redraw or capture. A partial intent is refused on retry as `intent is retained` without parsing those bytes and without capture.

## Unchanged limits

The same-user gap stays open. This is not an operating-system sandbox. File-symlink creation may skip on WinError 1314. The bytes-changed race is rechecked, not closed. The adapter does not call queue, claim, return, or reserve. It does not delete, resume, clean, or allocate around a partial. A verified receipt is custody, not review, acceptance, acknowledgement, closure, or publication.
