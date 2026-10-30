# Prime replay lab mechanics

Single instruction contract: ../../../00.kernel/00.00.10.work/0703.prime-replay/01.md.
Read your matching 05.NN.pack.md there. Do not read coordinator/history during runs.
This is contextual Colab. No model benchmark or fresh context is implied.

Run from D:/Git/lib-build with a working Python interpreter (standard library):

```text
python -B colab/labs/prime-replay-pass01/replay_lab.py verify
python -B colab/labs/prime-replay-pass01/replay_lab.py prepare --model grok
```

Use claude or codex for your assigned model. Prepare creates all four folders in
the fixed order and refuses an existing model root. Never remove or overwrite it
to retry. A genuine failed setup needs a recorded finding and new Prime direction.
Model label is a folder assignment, not identity authentication.

Every run.json gives exact repository, output, journal and registration paths.
Use absolute paths from that file; run commands through this wrapper:

```text
python -B colab/labs/prime-replay-pass01/replay_lab.py command --model grok --run 01-case-a-assisted -- python -B ABS_ASSISTANCE_TOOL read --registration ABS_REGISTRATION --templates ABS_OUT/templates --journal-root ABS_JOURNAL --caller "Grok Colab"
```

Use the actual Python executable path if python is unavailable. The wrapper cwd
is the disposable repository, not lib-build. Retain stdout/stderr/end records;
printed output is capped at 16000 bytes per stream, with full bytes on disk.
For assisted packet use --work case-a (or case-b) --out ABS_OUT/packet; inspect
packet coverage. Fill only judgment/attribution in the template. Continue only
with fresh bindings. Then record, read and day; no invented completion required.
For manual runs, use ordinary commands in the same wrapper and write the same
review and next-pack outputs without invoking the optional assistance bundle.

Save per-run deliverables as the contract states. Write your cross-run return at
runs/<model>/return.md, then:

```text
python -B colab/labs/prime-replay-pass01/replay_lab.py export --model grok
```

Export retains outputs, logs, typed reviews, source diff and measurements under
results/<model>. It does not grade meaning or claim complete telemetry. It refuses
an existing export root. Copy the final substantive return to your named N7 exchange
file, then capture the three named outputs per your pack. Original captures stay
byte-identical. No Git staging/pushing by participants; Prime publishes returns.

This runner is trusted local orchestration, not an OS sandbox or arbitrary-command
security boundary. No command timeout is imposed; interrupted wrappers preserve
a start without an end. No model or network calls are made by the runner.

CONTRACT-SNAPSHOT.md is the byte-identical sealed transport copy of the single
0703/01.md contract. It is not independently edited or a second authority.
