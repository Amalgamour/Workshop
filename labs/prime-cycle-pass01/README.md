# prime-cycle-pass01

The Prime read-record-read cycle over one registered work book (0515.prime-cycle/05.01). Standard library only. Experimental lab adapter: not seated, not wired into the app, and not a canonical-state migration.

- **Contract:** `00.kernel/00.00.10.work/0515.prime-cycle/evidence/build05.01/CONTRACT.md`
- **Design:** `0415.prime-cycle/01.md`
- **Current-Prime guide:** `evidence/build05.01/PRIME-USE.md`

```
python -B labs/prime-cycle-pass01/prime_cycle.py read     --registration ABS [--json] [--templates DIR]
python -B labs/prime-cycle-pass01/prime_cycle.py record   --registration ABS --decision ABS
python -B labs/prime-cycle-pass01/prime_cycle.py inspect  --registration ABS --work ID
python -B labs/prime-cycle-pass01/prime_cycle.py packet   --registration ABS --work ID --out DIR
python -B -X dev labs/prime-cycle-pass01/tests/test_prime_cycle.py -v
python -B labs/prime-cycle-pass01/demo.py
```

## What it does

**read** observes each registered work page with the accepted reader, which runs the pinned inspector and helper for custody. It reads that work's committed review records and derives a view. The view has, per work:
- **pass state:** no-return, awaiting-review, reviewed, or review-stale;
- **review disposition;**
- **pass terminal;**
- **page-goal terminal** for the *current* goal;
- holds, the recorded next actions with their author and source, and attention.

With `--templates`, read also writes one decision template per work. The template has every mechanical field pre-filled; Prime fills only the judgment.

**record** re-observes the page and refuses if anything bound in the template has changed. It validates the judgment, including the terminal rules, and runs the accepted `prime_review report` on it. It then writes one work-local review: `record.json` (authoritative), `REVIEW.md` (the readable projection) and `COMMITTED.json` (the completion marker, written last). An identical replay is a no-op; a different review needs a new id with `supersedes`.

**inspect** shows the phase of every review directory, and the recovery rule.

**packet** assembles the accepted review packet for one work, under the output root.

## Pass and goal are separate

A review states three things separately:
- its disposition: accepted, held or correction-required;
- the pass terminal: finished or open;
- the goal terminal: open or completed.

A completed goal must name the registration's current goal id and statement hash, carry evidence, and pass prime_review's complete-as-supplied check. Accepted with the pass finished leaves the goal open unless completion is declared. A new or changed goal never inherits an old completion.

## Dependencies (pinned, checked before launch)

- **batch_observe, return_inspect and return_capture** (through the reader): the observation and custody.
- **prime_review:** report, and check-next.
- **review_packet:** assemble, on `packet` only.

prime_brief, state_projection and desk_state are **not** invoked. Their closure semantics are batch-level, or they need a hand-maintained desk record. CONTRACT §9 explains why.

## Limits

- A label is not authentication.
- The local user is trusted. Same-user races between a check and a write are not prevented, and there is no OS sandbox.
- There is no transaction across files. COMMITTED.json is the only usable-state marker, and a partial is never read as a review.
- Builder use writes only disposable books. Prime's later live use writes only the declared work-local review location.
