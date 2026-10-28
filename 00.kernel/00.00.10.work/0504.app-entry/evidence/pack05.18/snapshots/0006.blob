# capture-handoff-pass01

Fixture adapter from one returned Clerk job to one pre-reserved capture member. This lab is not app wiring, not kernel law, and not a seated workflow.

`handoff.py` does not import the Clerk or capture tools. `perform(binding_path)` launches the current Python executable with `-B`, `shell` false, and the pinned scripts:

- `labs/clerk-handoff-pass02/clerk.py`
- `labs/return-capture-pass01/return_capture.py`
- `labs/return-capture-pass01/return_inspect.py`

The CLI is `handoff.py perform --binding ABS`. It has no fault switch. `hook` and `pins` are in-process seams for tests.

CH-01: the return file is a returned artifact under `source_root`. `artifact_base` is that job's outbox. `returned.delivery` and `returned.evidence` stay transport fields. CH-02: `intent.json` is exclusive-created before capture, and `completed.json` is exclusive-created only after verify, inspect, and a payload comparison. An identical completed retry writes nothing. A complete member without that record is attention. The adapter does not call queue, claim, return, or reserve.

A verified receipt is custody. It is not review, acceptance, acknowledgement, closure, or publication. `work_ref` is a declared label. The same-user gap between a hash read and a later write stays open.

Run from the checkout root:

```text
python -B labs/capture-handoff-pass01/tests/test_handoff.py
python -B labs/capture-handoff-pass01/demo.py
```

The tests and the demo use disposable directories outside the checkout. They remove those directories, including junctions, before they finish.
