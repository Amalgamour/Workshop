# Clerk handoff lab — report, 2026-10-26

## Result

STATUS: PASS

The local verification returned exit 0. Twenty acceptance tests ran; see
[test output](runs/local-pass/tests.txt). The demonstration used 8
separate processes and produced 14 recorded events.

| Expected | Observed |
|---|---|
| Builder returns first revision | build-1 -> built |
| Colab requests correction of that revision | review-1 -> changes; whitespace-only lines expose the seeded defect |
| Builder receives the correction through Clerk | build-2 -> built |
| Colab reviews the exact corrected revision | review-2 -> accepted |
| Fresh process reconstructs completion | audit passes, job closed |

No work-item or artifact path was handed manually to a role process. The launcher
did supply the workspace and role and did start each process in a fixed schedule.

## What I learned

1. **The hub can be small.** Recorded routes, identities, durable events, and exact
   artifact references are enough for this bounded loop. A complete kernel is not
   a prerequisite for testing the handoff mechanism.
2. **Return plus routing is one operation.** Failure injected between them rolls
   back, allowing retry without losing work or duplicating a review action.
3. **Delivery needs an identity.** Identical resubmission is harmless; changed
   contents under the same delivery identity are refused.
4. **Resume state should be derived.** A misleading 00.live file does not change
   the actual inbox or convince the acceptance checker that an unfinished job is
   complete. Refreshing the view reconstructs the recorded state.
5. **Review covers a revision.** Editing a source before or after the reviewer
   claims it stops the return. A review cannot silently migrate to changed work.
6. **Waiting for review need not idle Builder.** A separate independent assignment
   remains available while the earlier result awaits Colab.
7. **Resource handling is part of correctness.** The first Windows run found open
   SQLite handles during cleanup. Explicit connection closure fixed it. The failed
   run is preserved, rather than discarded after obtaining green output.

## What your check can assess

The checker reads the ledger and artifacts, compares the required route, checks
revision links, and executes the final function against known input/output cases.
Negative tests show it rejects incomplete work hidden by a forged summary, changed
accepted output, and ledger corruption. It shares the reducer/hash helpers with
Clerk; it is not a wholly independent storage implementation.

## Boundaries

This is a real persistence/dispatch experiment with scripted roles. It does not
prove live-model behavior, automatic wakeup, Director authentication, production
concurrency, distributed sync, or complete Workshop integration. SQLite is an
experimental backing store, not an approved architectural commitment.

The role launcher is explicitly allowed manual work for this pass. The same code
has not been used to send another model a message or execute a kernel pack.

## Next step

Use this as evidence for the shared handoff contract, then test one real Builder
and Colab against the inbox. Keep the initial route bounded. Link this lab ID from
the agreed work book once its address is established; no speculative book or page
was created here.

## Evidence

- [Machine results](runs/local-pass/results.json)
- [Process-by-process transcript](runs/local-pass/transcript.json)
- [Acceptance suite output](runs/local-pass/tests.txt)
- [Current state view](runs/local-pass/demo/00.live.md)
- [Initial failed run](runs/initial-failure/tests.txt)
- [Construction notes](NOTES.md)
