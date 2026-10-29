# RUN-GUIDE — starting a disposable Prime bench trial

For: the Director, and the separate Codex bench coordinator. Tool: `labs/prime-bench-pass01/prime_bench.py`.
This guide authorizes nothing. The harness makes no model call and launches no session; the coordinator does that by hand.

## What the Director decides first
These are open in 0414.bench and stay with the Director:
1. Which model and effort labels, how many runs, and the spending.
2. The session surface. It must start a **fresh** session with no earlier context and **confine** it to one folder, so the session cannot read lib-build, where the keys live. If it cannot, the run is still allowed, but it is reported as not clean.
3. Prime's N7NN investigation page (0701–0799) and pass, and the reserved member for the coordinator's return.

## What the coordinator needs
- The repository checked out read-only at a known commit, and Python 3.
- One folder outside the repository for the whole trial, for example `D:\bench-trials\trial-01\`.
- An investigation record, `investigation.json` (`prime-bench-investigation/1`). It holds:
  - the page, pass and question;
  - every Director reply kept **exactly**, with its source path and sha256;
  - the source references;
  - the coordinator's label.

## Steps
1. **Check the bench:** `python -B labs/prime-bench-pass01/prime_bench.py validate`. It must print `valid` and a bench version. Record that version.
2. **Plan the pairs.** For each case, one `baseline` run and one `assisted` run, each with its own run id (`r0001`, …) and its **own session**. Balance the order, so that half the cases run assisted first. No session ever sees two runs.
3. **Prepare each run:**
   ```text
   python -B labs/prime-bench-pass01/prime_bench.py prepare --investigation D:\bench-trials\trial-01\investigation.json --run-id r0001 --case correction-a --condition baseline --model-label "MODEL" --effort-label "EFFORT" --fresh-session supported --workspace-confined supported --tool-log unknown --usage unknown --run-dir D:\bench-trials\trial-01\runs\r0001 --candidate-dir D:\bench-trials\trial-01\candidates\r0001
   ```
   Declare each capability truthfully: `supported`, `unsupported` or `unknown`.
4. **Run the session by hand.** Follow `runs\r0001\COORDINATOR.md`:
   - Open one new session confined to `candidates\r0001` and paste `PROMPT.md`. Record the start time.
   - Do not help, hint or answer questions.
   - Save the final message exactly to a file outside the candidate folder, and record the finish time.
   - Export the tool log and usage if the surface offers them.
5. **Collect**, with the exact command printed in COORDINATOR.md. Use `--label ACTUAL`. A failed or abandoned run is collected with `--status failed|abandoned --reason TEXT`; it stays in the data. If you helped, pass `--intervention TEXT`.
6. **Review.** A reviewer, blind to the condition where possible, scores each rubric item in a `prime-bench-review/1` record bound to the run's rubric sha256 from run.json. Then run `review --run-dir … --record …`. Later corrections go in as `event --kind correction`; the original answer never changes.
7. **Compare** with `compare --run-dir … --run-dir …`. Read the "What is counted" and "Not clean" sections first.
8. **Export** with `export --run-dir … --investigation … --dest D:\bench-trials\trial-01\export`. This writes:
   - `comparison.md` and `comparison.json`, which binds every run record by sha256;
   - `investigation.json`;
   - `runs\`;
   - `05.NN.return.TEMPLATE.md`;
   - `CAPTURE.txt`.

## Where the return lands
1. The coordinator writes `05.NN.return.md` in the export folder from the TEMPLATE, starting with Did, Blocked, Need.
2. Prime reserves a member whose expected outputs are `comparison.md`, `comparison.json`, `investigation.json`, in that order.
3. The coordinator runs the two commands in `CAPTURE.txt` (`return_capture.py capture`, then `verify`) from the repository root. The return is then in that N1NN member. The receipt is custody, not acceptance.
4. Prime places it into the N7NN page as `05.NN.return.md` with the reviewed workflow, then writes `06.NN.review.md`. The harness writes no live page.

## What a trial can and cannot say
- **It can say:** per run, what was answered, whether the deterministic checks passed, what the reviewer scored, and what was supplied for time, tool events and usage. It also says which runs were not clean, and why.
- **It cannot say:** a productivity multiple, a time or token saving, or a model ranking. Eight synthetic cases are a first slice; repeated balanced runs and unseen cases come first.
- **Self-test data:** the fixture tests and `sample-report.md` are SYNTHETIC. They show the format, not performance.
