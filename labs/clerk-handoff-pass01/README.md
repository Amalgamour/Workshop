# Clerk handoff lab — pass 01

Lab ID: `clerk-handoff-pass01`  
Date: 2026-10-26  
Status: experiment, not seated Workshop compute  
Authority: Director requested `>build >test >report` in `D:\Git\lib-build\labs`.

This lab exercises real persistent work records, role inbox selection, claims,
hash-bound returns, recorded routing, and an acceptance checker. Python scripts
stand in for Builder and Colab. They are deliberately scripted fixtures, not
live AI workers. No model is messaged or awakened.

## Read first

- [Report and learning](REPORT.md)
- [Demonstration transcript](runs/local-pass/transcript.json)
- [Machine result](runs/local-pass/results.json)
- [Acceptance tests](runs/local-pass/tests.txt)
- [Generated current-state view](runs/local-pass/demo/00.live.md)
- [Construction notes](NOTES.md)

## Run

Python 3.10+ and its standard library are sufficient. Use the configured Python
runtime on the machine. From this lab folder:

```powershell
python -B run_lab.py --output runs/my-new-run
python -B clerk_lab.py audit runs/my-new-run/demo
python -B clerk_lab.py live runs/my-new-run/demo
```

Choose an unused output directory. Existing demonstration results are preserved.
`run_lab.py` first runs the tests, then starts eight separate processes. Each role
receives only the workspace and role name, obtains its action from Clerk, and
returns through Clerk. The launcher starts the roles in a known order; it is not
a scheduler that dynamically wakes models.

For roles individually, use `init ROOT`, then `role ROOT --role builder` or
`role ROOT --role colab`. `live ROOT` regenerates the summary from recorded state.
`audit ROOT` returns exit 0 only when the declared demonstration route, artifacts,
and final task checks pass. A refusal uses exit 2; an incomplete audit uses exit 1.

## Frozen acceptance contract

Task: count lines containing at least one non-whitespace character.

1. Builder obtains build-1 and returns revision 1 plus a limited test result.
2. Colab receives review-1 referring to that exact revision. Its broader fixture
   includes whitespace-only lines and requests changes.
3. Builder receives build-2 with the review artifact as its input.
4. Colab receives review-2 tied to revision 2 and accepts after all four declared
   input/output cases pass.
5. Clerk records closure. A separate process reconstructs current state and audits
   raw events and artifacts.

The original task's correction route is pre-authorized for this experiment and
limited to two build attempts. Clerk does not invent another plan when exhausted.
The intentional first defect tests whether review can reject a concrete result;
it is not presented as a discovery about an actual model's reasoning.

Allowed manual action: starting a role process.
Not supplied by the launcher: work-item ID, artifact path, or recipient decision.
The code fixture discovers those from Clerk. This does not prove how a live model
will use the interface.

Negative tests cover duplicate delivery, conflicting delivery identity, interrupted
claims and explicit resume, unfinished dependencies, a synthetic Director gate,
rejection, changed artifacts before/after claim, wrong-role return, builder self-
acceptance, missing output, failed routing transaction, independent queued work,
empty inbox, misleading summary, incomplete workflow, changed accepted output,
ledger tampering, and path escape.

## Record and projections

`events.sqlite` is the experimental record. It has ordered, hash-linked events.
Returning work and creating its successor occur in one transaction. Inboxes and
`00.live.md` are projections of those events. The summary is refreshed on request
and never used as the dispatcher or acceptance checker's authority.

SQLite is a lab implementation choice, not an adopted storage decision for the
Workshop. The event reducer and hash helpers are shared with the checker; this
is not an independently implemented second persistence engine. External expected
route and functional cases guard additional properties.

## Work-book link

The desk and book addresses are being designed separately. This lab creates no
book, assigns no reserved page, and edits no old worktree. A later work-book page
can reference:

```text
lab: clerk-handoff-pass01
path: labs/clerk-handoff-pass01
report: labs/clerk-handoff-pass01/REPORT.md
test: python -B labs/clerk-handoff-pass01/run_lab.py --output labs/clerk-handoff-pass01/runs/NEW-RUN
status: experimental; scripted roles
```

## Not established

Live-model dispatch, automatic prompting, authenticated Director approvals,
multi-session identity/leases, distributed Git synchronization, sustained parallel
writes, arbitrary workflow graphs, production durability, actual kernel lifecycle
integration, and a complete application are outside this pass.
