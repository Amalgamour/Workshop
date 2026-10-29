# Contract — pinned capture-return door
Date: 2026-10-28
Schema: apphandoff05.20-contract
State: expected outcomes, written after 06.20.md and before code.

This contract is the fixture proof for one app door onto the accepted capture handoff. It does not seat a workflow, launch a worker, or accept a return. A verified receipt is custody. It is not review, acceptance, acknowledgement, closure, or publication.

## Door
`app/librarian.py` gains `capture-return --binding <absolute-binding>`. The facade is `app/handoff_tools.py`. The declaration is `app/capture-handoff.json`, schema `librarian-capture-handoff` version 1. The subprocess is the current Python executable and the argument array `perform --binding <absolute-binding>` against `labs/capture-handoff-pass01/handoff.py`. There is no shell. The caller cannot supply a tool path, a pin, an executable, or a timeout.

`clerk-deliver` remains the separate delivery command. This door does not queue, claim, return, reserve, route, or choose a member. It does not launch a model or a protocol worker. `run` stays refused.

## Pins checked before launch
The declaration and the facade both name these paths and hashes, relative to the workspace that contains the entry:

- `labs/capture-handoff-pass01/handoff.py` `a8380136a84469b8975b38f084a4d34802ccf079ed69cf85d107f6ca3643426a`
- `labs/clerk-handoff-pass02/clerk.py` `f697a7e443117c3d1face62d3021f7634154d76214b77fadec1a5cc3c99d394c`
- `labs/return-capture-pass01/return_capture.py` `8f3da5c651f6924fca6dedb0b95da7d181eb58884dc030dd9cbc3d8b6a5b15ac`
- `labs/return-capture-pass01/return_inspect.py` `947915febaa5918f56b6be03c81840c030d081fcab9a3bead2cd660973a9999b`

A symlink or junction on the declaration or on a tool path is refused and is not followed. An unknown field, a duplicate field, a missing declaration, a schema or version mismatch, or a hash that is not one of those pins is refused. The refusal prints `stop:` on stderr, exits 2, leaves stdout empty, and does not start `handoff.py`. There is no version scan and no second declaration path.

## Paths checked before launch
`--binding` is required once. The value must be an absolute path of a plain file. A relative path, a missing path, a directory, or a reparse point on the path or an ancestor is `stop:`, exit 2, empty stdout, and no `handoff.py`. A caller `--handoff`, `--clerk`, `--tool`, `--pins`, `--capture`, `--inspect`, `--executable`, `--python`, or `--timeout` is the same kind of refusal. Any other flag is an unsupported argument. The facade does not parse the binding object. The backend owns that check.

## Complete capture
Fixture setup is explicit and disposable. The root, the Clerk store, and the book are absolute directories outside the checkout and outside Git. Setup queues, claims, and returns one fixture Clerk job, writes the report bytes into the outbox and the source root, and pre-reserves one member with the pinned capture tool. Those calls are setup. They are not this door's lifecycle.

The same fixture bytes are then given to `capture-return` and, after the tree is restored, to `handoff.py perform --binding`. Both exit 0. Stderr is empty. Stdout contains `result ok`, `result complete`, `not approved`, `not accepted`, and `not published`, and it does not contain `writes none`. `return.md` and the payload blobs equal the report bytes. `intent.json` and `completed.json` exist. The failure log does not.

`captured_at` is inside the manifest and the receipt, so two separate captures do not share those two hashes. The comparison treats `manifest` and `receipt` lines as present and well-formed, and requires every other stdout line to match. Reservation bytes and report bytes match. This limit is the accepted tool's clock. The door does not remove it.

## Read-only repetition
On that completed member, `capture-return` and `handoff.py perform` are run again. Their stdout, stderr, and exit match byte for byte. Both exit 0 and contain `writes none`. The member files and the handoff record files are unchanged. This is one fixture observation. It is not a general exactly-once guarantee.

## Changed event and changed payload
A binding whose returned-event hash differs is refused with `returned event does not match the binding`. Exit 2. The app stdout, stderr, and exit match the direct backend on a restored tree. The member bytes stay as they were.

Changing the report source bytes, leaving the outbox and the original binding hashes in place, is refused with `report source bytes are not the outbox bytes`. Exit 2. The app output matches the direct backend. The member bytes stay as they were. The door does not repair, delete, or recapture.

## Malformed binding
An absolute plain file that is not the binding object is refused by the backend with `binding is not strict json`. The door forwards that stdout, stderr, and exit 2. Clerk and capture are not started: the refusal is the parse refusal, and no failure log is written. The door does not invent a second parser.

## Partial capture
A separate fixture is handed off in-process with the accepted private hook returning `stop` at `after-capture`. That hook is not added to the CLI. The member then holds the captured files, `completed.json` is absent, and the receipt bytes are the partial's receipt.

The next `capture-return` and the next direct `perform` match byte for byte. Exit 2. The text contains `complete capture has no completed handoff record` and `result attention`. It does not contain `result ok`. `completed.json` stays absent. The receipt bytes stay the same. The door does not resume and does not allocate another member.

## Interrupted child
The facade starts the child once and sets no outer timeout. Exit 0 and exit 2 are copied unchanged, including a backend line that says `writes none` when that completed report is exit 2. An exit other than 0 or 2, or a missing exit code, is returned without being coerced to 0 and without a second launch. The wrapper does not add `writes none`. It adds one stderr line: inspect retained state; this call does not retry. A failure to start, before a child exists, is `stop:` and does not say `writes none`.

## Evidence
The suite prints the exact app and direct outputs for the capture, the repeat, the two custody refusals, and the partial forward. It asserts member bytes, record files, and launch refusals as above. It also runs `app/tests/test_entry.py`. Failures and privilege skips are preserved. Unrelated suites are not run. Test writes stay in disposable directories.

## Out of scope
No edit to `handoff.py`, Clerk, return capture, return inspect, `clerk-deliver`, or kernel law. No live queue, live job, or model. No new retry policy. No second receipt validator. No recovery.
