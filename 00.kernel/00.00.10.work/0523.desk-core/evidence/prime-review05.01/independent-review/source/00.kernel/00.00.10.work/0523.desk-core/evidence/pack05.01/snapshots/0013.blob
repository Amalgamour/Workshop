# desk-app-integration-pass01

Lab for 0519.desk-app/05.01: the first desk workflow (Prime reviews one builder return) composed from existing modules, plus the minimum compute construction of the records that loop types by hand. Standard library only. Lab code, not app wiring, not seated.

Design and plan: `00.kernel/00.00.10.work/0519.desk-app/evidence/build05.01/DESIGN.md`, `BUILD-PLAN.md`.

```text
python -B desk_lab.py view      --repo ABS [--book REL] [--as LABEL]... [--registration ABS] [--member NAME]... [--json]
python -B desk_lab.py construct --template batch-page/1|return-pointer/1|review-section/1 --input ABS --target ABS --expect-sha256 HEX|absent [--repo ABS] [--book REL] [--write]
python -B demo.py [--transcript OUT.json] [--keep]
```

**view** is read-only.
- **Inputs:** it enumerates `01NN/reservation.json`, runs the pinned `return_inspect` per member and the pinned `batch_observe --live` per origin page, and with `--registration` merges `prime_cycle read --json`.
- **Output:** each task's state, the actor who moves it, the next step and attention.
- **Cache:** none.
- **Exits:** 0 means no attention, 1 attention, 2 refused.
- **Pins** (checked before every launch):
  - `return_capture` 8f3da5c6…
  - `return_inspect` 947915fe…
  - `batch_observe` 8bea1817…
  - `prime_cycle` 19ede9c2…

**construct** renders a record from structured input.
- **The caller supplies** text and judgment.
- **Compute supplies** addresses, the assignment hash, and receipt and manifest hashes (from `return_inspect`), plus the disposition and next action (from a committed prime_cycle `record.json`).
- **Edits allowed:** create an absent file, replace a `PENDING.` placeholder, or append inside the declared section, under compare-and-swap on `--expect-sha256`.
- **Refused:** anything else, including a construction into this checkout. This lab writes disposable books only.
- **Default** is a preview. `--write` applies.

**demo** runs 36 steps in one disposable Git repository under the system temp directory, each a separate process, with a stated expectation per step. The cases:
- the full loop;
- a missing return versus done;
- identical and changed handback;
- a superseding return;
- a stale compare-and-swap;
- an assignment edited after claim;
- an interrupted capture;
- restart digests;
- the review-binding conflict (8b, a finding);
- refusal to construct into the checkout.

SYNTHETIC data only. No model, reviewer or session runs. The directory is removed at the end unless `--keep` is given.

**Limits:**
- Labels are not authentication.
- Same-user, no OS sandbox.
- view does not resolve `05.NN.VVV.md` text versions or the 07NN `.pack.md`/`.return.md` layout. It reports those pages as not observed.
- Legacy reviews outside the page Review section read as `awaiting-review` (DESIGN F3).
- The broad execution and replay lab is Grok-2's on 0520. This lab does not duplicate it.
