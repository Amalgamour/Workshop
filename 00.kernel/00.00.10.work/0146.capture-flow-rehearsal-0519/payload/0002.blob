# capture-flow-rehearsal-pass01

Disposable rehearsal of one accepted path from a protocol test worker to a pre-reserved capture. This lab is not an installed app command, not a dispatcher, and not a new lifecycle.

`rehearse.py` hash-checks the 05.19 source pack, writes the declared tool closure into a temporary source-view, and hashes that view again before import. The closure is the accepted `clerk_seam` and `worker_bridge` modules, their pin files, the pinned Clerk, the pinned return-capture tools, and `labs/capture-handoff-pass01/handoff.py`. `app/librarian.py` is not copied. The runner file is copied only when its bytes match the hash in the accepted `development-workspace.json`. That copy is a declared config pin, not a pack snapshot.

The only worker is the allowlisted protocol test worker. `fixture-ok` is the success path. `fixture-crash` is the failed path. Neither is a model.

What compute does, on a disposable fixture outside the checkout:

1. Setup queues and claims one Clerk job. Those calls are setup.
2. `clerk_seam.perform` launches the worker once, collects `result.json`, and returns the job.
3. That `result.json` is the synthetic final-report payload. Its bytes are preserved. It is not a narrative report and not a semantic review. Transport evidence stays a separate field.
4. Setup pre-reserves a member. `handoff.perform` captures that payload.
5. Repeating the same delivery and handoff does not launch the worker again and does not change the source, job, member, or handoff record.
6. A changed returned-event binding, or a changed report payload, is refused. The capture stays. No second worker starts.
7. A crashed worker does not reserve a member and does not capture.
8. A stop after capture keeps the member files and the intent, leaves `completed.json` absent, and the next call is attention. It does not resume.

`work_ref` is a supplied label. A verified receipt is custody. It is not review, acceptance, acknowledgement, closure, or publication. The same-user gap stays open. This is not an operating-system sandbox, and the single-launch observation is not a general exactly-once guarantee.

Prime still decides whether this fixture proof is enough, and whether any later integration is acceptable. Review, acceptance, and publication are not done here.

The smallest next integration step is one explicit app command that calls this same fixture composition, still with no model profile, no live queue, and no automatic recovery. That command is not built in this slice.

Run from the checkout root:

```text
python -B labs/capture-flow-rehearsal-pass01/tests/test_rehearse.py
python -B labs/capture-flow-rehearsal-pass01/demo.py
```

The tests and the demo use disposable directories outside the checkout. They remove those directories, including junctions, before they finish. The demo writes `00.kernel/00.00.10.work/0504.app-entry/evidence/flow05.19/results.json`.
